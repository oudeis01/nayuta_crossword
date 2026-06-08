#!/usr/bin/env python3
"""B단계-3: LGDE로 시드 사전(담론 키워드)을 코퍼스 어휘로 확장 → 주제 게이트.

배경: 단순 코사인 플랫 임계값은 정당한 도메인어(sculpture 0.21)와 보일러플레이트
(newsletter 0.24)가 같은 점수 띠에 섞여 분리 불가였다(validate_gate.py). LGDE는
원시 거리가 아니라 단어 유사도 그래프의 '커뮤니티 구조'(CkNN + Severability 지역
커뮤니티 검출)를 보므로, 시드 커뮤니티에 다중 경로로 연결된 도메인어만 발견한다.

제약: LGDE 구현은 n x n 밀집 거리 행렬(pdist/squareform)을 만든다. 전체 풀 125,974개는
~1TB라 불가. 따라서 후보를 다룰 수 있는 크기로 사전 축소한다:
  시드      = core+marker 티어(용례 有)  ← discourse_keywords_v3.json 유래
  후보      = general 티어 중 corpus_freq >= CW_LGDE_MINFREQ 이고 길이 3~11, 용례 有
  단어벡터  = data/pool_centroids.npy (문장맥락 센트로이드)
저빈도 아티팩트(aet/paradoxa/lorem 등 freq<25)는 이 빈도 컷에서 이미 제거된다.
LGDE의 역할 = 고빈도 비주제어(monday/dusseldorf 등)를 미술 커뮤니티에서 배제하는 것.

산출:
  data/lgde_expanded.json  {params, n_seed, n_candidate, discovered(general 단어),
                            communities(시드->발견어), probe(스폿체크 결과)}
콘솔에 스폿체크(살려야 할 도메인어 vs 배제해야 할 비주제어)와 통계를 출력한다.
"""
import json, os, sys, time, multiprocessing as mp, numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.environ.setdefault("HF_HOME", "/home/choiharam/storage/models/huggingface")

MINFREQ = int(os.environ.get("CW_LGDE_MINFREQ", "200"))
K = int(os.environ.get("CW_LGDE_K", "5"))           # CkNN 이웃 수(그래프 밀도)
T = int(os.environ.get("CW_LGDE_T", "4"))           # Severability Markov 시간(t=1은 과도하게 국소; CLI 기본 4)
MAXSIZE = int(os.environ.get("CW_LGDE_MAXSIZE", "50"))  # 시드별 커뮤니티 최대 크기
MINLEN, MAXLEN = 3, 11

# 미술 실무 시드 보강: discourse_keywords(담론어)에 큐레토리얼 실무어를 추가해
# 담론 커뮤니티와 미술 커뮤니티를 둘 다 형성시킨다. 다의어(medium/sound/video/print/
# canvas/collection/landscape/portrait/performance/commission)는 게이트가 일반어로
# 끌려가지 않도록 제외. 모두 코퍼스 존재·고빈도(general 티어, n_sent=20) 확인됨.
ART_SEED = ["curator", "curatorial", "curating", "gallery", "gallerist",
            "exhibition", "museum", "biennale", "sculpture", "sculptor",
            "painting", "painter", "drawing", "photography", "photographer",
            "installation", "artwork", "artist", "retrospective", "vitrine",
            "plinth", "pedestal", "catalogue", "monograph", "oeuvre",
            "figurative", "minimalism", "collage", "assemblage", "mural",
            "fresco", "etching", "vernissage", "provenance", "acquisition"]

# 검증 기준: KEEP = 시드에 안 넣은 미술 인접어(발견✓ 기대). DROP = 비주제어(배제 기대).
PROBE_KEEP = ["aesthetics", "avantgarde", "modernism", "surrealism", "dada",
              "readymade", "sculptural", "pictorial", "printmaking", "abstraction",
              "conceptual", "archive"]
PROBE_DROP = ["monday", "tuesday", "friday", "dusseldorf", "newsletter",
              "copyright", "subscribe", "email", "website"]


def _cosine_sim_norm(word_vecs):
    """라이브러리 _compute_semantic_sim 등가물을 GPU matmul로 (가능 시).

    벡터가 L2정규화돼 있으면 코사인거리 = 1 - X@X.T. 라이브러리와 동일하게
    distance/max 로 정규화 후 1-... 반환. GPU 불가 시 numpy(BLAS 멀티코어)로.
    """
    X = np.ascontiguousarray(word_vecs, dtype=np.float32)
    try:
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError("no cuda")
        Xt = torch.from_numpy(X).cuda()
        Xt = torch.nn.functional.normalize(Xt, dim=1)   # 안전상 재정규화
        dist = (1.0 - (Xt @ Xt.T)).clamp_(min=0.0)
        dist.fill_diagonal_(0.0)
        dist /= dist.max()
        sim = (1.0 - dist).cpu().numpy()
        del Xt, dist
        torch.cuda.empty_cache()
        return sim, "gpu"
    except Exception:
        Xn = X / np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None)
        dist = 1.0 - (Xn @ Xn.T)
        np.clip(dist, 0, None, out=dist)
        np.fill_diagonal(dist, 0.0)
        dist /= dist.max()
        return (1.0 - dist).astype(np.float32), "cpu-blas"


# --- CPU 병렬 Severability(시드별 독립). fork COW로 P/adj 공유(복제·피클 없음) ---
_P = _ADJ = _WL = None
_TT = 4
_MAXSZ = 50


def _community_of(ki):
    """라이브러리 _compute_local_community와 동일 로직, 워커에서 실행."""
    from severability import node_component
    if _ADJ[ki].sum() == _ADJ[ki, ki]:        # 그래프 내 고립점
        return ki, [_WL[ki]]
    comp = node_component(P=_P, i=ki, t=_TT, max_size=_MAXSZ)[0]
    if len(comp) == 0:                        # Severability 고아
        return ki, [_WL[ki]]
    return ki, [_WL[i] for i in comp]


def main():
    t0 = time.time()
    M = np.load(os.path.join(DATA, "pool_centroids.npy"))
    meta = json.load(open(os.path.join(DATA, "pool_centroids_words.json"), encoding="utf-8"))
    pool = json.load(open(os.path.join(DATA, "wordpool.json"), encoding="utf-8"))
    idx = {m["token"]: i for i, m in enumerate(meta)}

    def cf(w):
        return pool.get(w, {}).get("corpus_freq", 0)

    # 불용어 사전(NLTK ∪ spaCy): about/and/age/blue 등 고빈도 일반어를 후보에서 제거.
    stop = set()
    try:
        from nltk.corpus import stopwords
        stop |= set(stopwords.words("english"))
    except Exception as e:
        print(f"  [주의] NLTK stopwords 불가: {e}", flush=True)
    try:
        from spacy.lang.en.stop_words import STOP_WORDS
        stop |= set(STOP_WORDS)
    except Exception as e:
        print(f"  [주의] spaCy STOP_WORDS 불가: {e}", flush=True)

    # 시드 = 담론어(core+marker) + 미술 실무어(ART_SEED 중 코퍼스 존재·용례 有)
    art_seed = [w for w in ART_SEED if w in idx and meta[idx[w]]["n_sent"] > 0]
    seeds = [m["token"] for m in meta
             if m["tier"] in ("core", "marker") and m["n_sent"] > 0]
    seeds = list(dict.fromkeys(seeds + art_seed))
    seed_set = set(seeds)
    # 후보 = general 중 빈도·길이 통과, 불용어 아님, 시드 아님(미술어는 시드로 이동)
    cand_general = [m["token"] for m in meta
                    if m["tier"] == "general" and m["n_sent"] > 0
                    and MINLEN <= len(m["token"]) <= MAXLEN and cf(m["token"]) >= MINFREQ
                    and m["token"] not in stop and m["token"] not in seed_set]
    # word_list = 시드 + 후보 (중복 제거, 순서 유지)
    word_list = list(dict.fromkeys(seeds + cand_general))
    rows = [idx[w] for w in word_list]
    word_vecs = M[rows]
    print(f"시드 {len(seeds)}(담론 {len(seeds)-len(art_seed)} + 미술 {len(art_seed)}) | "
          f"general 후보(freq>={MINFREQ}, len{MINLEN}-{MAXLEN}, 불용어/시드 제외) "
          f"{len(cand_general):,} | word_list {len(word_list):,} | k={K} t={T} maxsize={MAXSIZE}",
          flush=True)

    # 스폿체크 단어가 후보에 들어있는지 사전 확인(검증 의미 확보)
    miss_keep = [w for w in PROBE_KEEP if w not in set(word_list)]
    miss_drop = [w for w in PROBE_DROP if w not in set(word_list)]
    if miss_keep:
        print(f"  [주의] KEEP 프로브 중 후보 미포함(빈도/길이 컷): {miss_keep}", flush=True)
    if miss_drop:
        print(f"  [주의] DROP 프로브 중 후보 미포함(빈도 컷에서 이미 제거): {miss_drop}", flush=True)

    from lgde.lgde import LGDE      # baselines(cdlib 의존) 우회 위해 모듈 직접 임포트
    from severability import transition_matrix
    n = len(word_list)
    print(f"n x n float32 행렬 ~{n*n*4/1e9:.1f}GB/벌. 유사도(matmul) 계산...", flush=True)

    # 1) 유사도 행렬: GPU matmul(가능 시) → 라이브러리 _compute_semantic_sim 대체
    class FastLGDE(LGDE):
        def _compute_semantic_sim(self, wv):
            sim, dev = _cosine_sim_norm(wv)
            print(f"  유사도 행렬 {dev} {time.time()-t0:.0f}s", flush=True)
            return sim

    lgde = FastLGDE(seeds, word_list, word_vecs)
    # 2) CkNN 그래프 구성(numpy)
    lgde.construct_network(k=K)
    print(f"  그래프(CkNN) 구성 완료 {time.time()-t0:.0f}s", flush=True)

    # 3) Severability 지역 커뮤니티: 시드별 독립 → CPU 멀티프로세싱.
    #    P/adj/word_list를 모듈 전역에 넣고 fork → 워커가 COW로 상속(피클/복제 없음).
    global _P, _ADJ, _WL, _TT, _MAXSZ
    _P = transition_matrix(np.matrix(lgde.adjacency_))
    _ADJ, _WL, _TT, _MAXSZ = lgde.adjacency_, lgde.word_list, T, MAXSIZE
    seed_inds = [lgde.word_to_ind[w] for w in lgde.seed_dict]
    workers = max(1, min(os.cpu_count() - 2, len(seed_inds)))
    print(f"  지역 커뮤니티 검출: 시드 {len(seed_inds)} | 워커 {workers}", flush=True)
    ctx = mp.get_context("fork")
    n_seed = len(seed_inds)
    done = 0
    with ctx.Pool(workers) as pp:        # initargs 없음 → 무거운 전역은 fork로 공유
        for ki, comm in pp.imap_unordered(_community_of, seed_inds, chunksize=4):
            lgde.semantic_communities_[lgde.word_list[ki]] = comm
            done += 1
            if done % 25 == 0 or done == n_seed:
                el = time.time() - t0
                eta = el / done * (n_seed - done)
                print(f"    진행 {done}/{n_seed} | 경과 {el:.0f}s | ETA {eta:.0f}s", flush=True)
    import itertools as _it
    all_comm = set(_it.chain.from_iterable(lgde.semantic_communities_.values()))
    lgde.discovered_dict_ = list(all_comm - set(lgde.seed_dict))
    lgde.expanded_dict_ = lgde.seed_dict + lgde.discovered_dict_
    print(f"  검출 완료 {time.time()-t0:.0f}s", flush=True)

    discovered = set(lgde.discovered_dict_)          # 시드 제외 발견 단어
    disc_general = sorted(discovered & set(cand_general))
    print(f"\n발견 단어 {len(discovered):,}개 (general {len(disc_general):,}/{len(cand_general):,} "
          f"= {100*len(disc_general)/max(1,len(cand_general)):.0f}% 통과)", flush=True)

    # 스폿체크: KEEP은 발견되어야, DROP은 발견 안 되어야 좋음
    def status(w):
        if w in set(seeds):
            return "SEED"
        if w not in set(word_list):
            return "후보밖"
        return "발견✓" if w in discovered else "배제"
    print("\n=== 살려야 할 도메인어(발견✓ 기대) ===")
    for w in PROBE_KEEP:
        print(f"  {w:14} {status(w)}")
    print("=== 배제해야 할 비주제어(배제 기대) ===")
    for w in PROBE_DROP:
        print(f"  {w:14} {status(w)}")

    out = {
        "params": {"minfreq": MINFREQ, "k": K, "t": T, "maxsize": MAXSIZE,
                   "minlen": MINLEN, "maxlen": MAXLEN},
        "n_seed": lgde.n_seed, "n_candidate_general": len(cand_general),
        "n_word_list": len(word_list), "n_discovered": len(discovered),
        "n_discovered_general": len(disc_general),
        "discovered_general": disc_general,
        "probe": {"keep": {w: status(w) for w in PROBE_KEEP},
                  "drop": {w: status(w) for w in PROBE_DROP}},
        "communities": {k: sorted(v) for k, v in lgde.semantic_communities_.items()},
    }
    json.dump(out, open(os.path.join(DATA, "lgde_expanded.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n저장: data/lgde_expanded.json ({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
