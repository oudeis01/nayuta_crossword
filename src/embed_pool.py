#!/usr/bin/env python3
"""B단계-1: 전체 풀 단어의 '문장맥락 중심' 임베딩 산출 (병렬 스캔 + GPU 인코딩).

각 단어를 그 단어가 등장하는 코퍼스 문장 임베딩의 평균(센트로이드)으로 표현한다.
도메인 맥락이 반영되며, 아티팩트가 연락처/잡문 맥락이면 자동으로 주제에서 멀어진다.

병렬화(사용자 방침 2026-06-06): 코퍼스 문서는 독립적이므로 파일 샤드를 워커에 분배해
워커별 부분 수집(word -> 문장 리스트, 단어당 MAX_CAND 상한) 후 부모에서 병합한다.
GPU는 1개라 인코딩은 부모에서 배치로 수행(스캔만 병렬).

입력 : data/wordpool.json, data/keyword_tokens.json (멀티워드 매칭)
산출 :
  data/pool_centroids.npy        float32 [n_words, dim]  (행=단어, L2 정규화; 용례 없으면 0벡터)
  data/pool_centroids_words.json [{token, tier, n_sent}] 행 순서대로
모델 : sentence-transformers/all-MiniLM-L6-v2 (대조학습 → 비교적 등방).
"""
import json, os, re, sys, glob, time, collections, multiprocessing as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("HF_HOME", "/home/choiharam/storage/models/huggingface")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_vocab import clean  # 신 토크나이저와 동일 정규화(음역 포함)로 일관 매칭

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOKEN_RE = re.compile(r"[a-z]+")
_WS = re.compile(r"\s+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
MIN_SENT_LEN, MAX_SENT_LEN = 25, 320
MAX_CAND = 20            # 단어당 센트로이드 계산용 문장 상한

_TARGET = None           # set[str] 단일토큰 타깃
_MWORD = None            # list[(token, compiled_pattern)] 멀티워드
_SEG = None              # set[str] 포함 segment_type


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def init_worker(target, mword, seg):
    global _TARGET, _MWORD, _SEG
    _TARGET, _MWORD, _SEG = target, mword, seg


def scan_file(path):
    """문서 1개 → {word: [문장,...]} (단어당 MAX_CAND 상한, 문서 내 중복 제거)."""
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except Exception:
        return {}
    out = collections.defaultdict(list)
    seen = collections.defaultdict(set)
    for b in doc.get("blocks", []):
        cls = b.get("classification") or {}
        if cls.get("segment_type") not in _SEG:
            continue
        content = b.get("content") or ""
        if not content:
            continue
        for part in _SENT_SPLIT.split(content):
            s = _WS.sub(" ", part).strip()
            if not (MIN_SENT_LEN <= len(s) <= MAX_SENT_LEN):
                continue
            cl = clean(s)
            toks = set(TOKEN_RE.findall(cl))
            matched = toks & _TARGET
            if _MWORD:
                for tok, pat in _MWORD:
                    if pat.search(cl):
                        matched.add(tok)
            if not matched:
                continue
            for w in matched:
                if len(out[w]) >= MAX_CAND or s in seen[w]:
                    continue
                seen[w].add(s)
                out[w].append(s)
    return dict(out)


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    pool = json.load(open(os.path.join(data_dir, "wordpool.json"), encoding="utf-8"))
    kw = json.load(open(os.path.join(data_dir, "keyword_tokens.json"), encoding="utf-8"))
    seg = set(cfg["corpus"]["include_segment_types"])

    target = set(pool.keys())
    mword = [(k["token"], re.compile(r"\b" + re.escape(k["norm_spaced"]) + r"\b"))
             for k in kw if k["n_words"] > 1 and k["token"] in target]
    single = target - {t for t, _ in mword}

    files = []
    for d in cfg["corpus"]["include_dirs"]:
        files += glob.glob(os.path.join(cfg["paths"]["corpus_root"], d, "**", "*.json"),
                           recursive=True)
    workers = max(1, os.cpu_count() - 2)
    print(f"풀 {len(pool):,} (멀티워드 {len(mword)}) | 문서 {len(files):,} | 워커 {workers}",
          flush=True)

    # --- 병렬 스캔 + 병합 ---
    cand = collections.defaultdict(list)
    seen = collections.defaultdict(set)
    t0 = time.time()
    done = 0
    with mp.Pool(workers, initializer=init_worker, initargs=(single, mword, seg)) as p:
        for partial in p.imap_unordered(scan_file, files, chunksize=50):
            done += 1
            for w, sents in partial.items():
                bucket = cand[w]
                if len(bucket) >= MAX_CAND:
                    continue
                sw = seen[w]
                for s in sents:
                    if len(bucket) >= MAX_CAND:
                        break
                    if s in sw:
                        continue
                    sw.add(s)
                    bucket.append(s)
            if done % 10000 == 0:
                cov = sum(1 for w in target if cand.get(w))
                print(f"  scan {done}/{len(files)} | 용례확보 {cov:,}/{len(target):,} | "
                      f"{time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    cov = sum(1 for w in target if cand.get(w))
    print(f"스캔 완료 {time.time()-t0:.0f}s | 용례확보 {cov:,}/{len(target):,}", flush=True)

    # --- GPU 인코딩: 고유 문장 1회 ---
    from sentence_transformers import SentenceTransformer
    import numpy as np
    model = SentenceTransformer(MODEL_NAME, device="cuda")
    uniq = sorted({s for ss in cand.values() for s in ss})
    sidx = {s: i for i, s in enumerate(uniq)}
    print(f"고유 문장 {len(uniq):,}개 인코딩...", flush=True)
    t1 = time.time()
    S = model.encode(uniq, batch_size=512, convert_to_numpy=True,
                     normalize_embeddings=True, show_progress_bar=False) \
        if uniq else np.zeros((0, 384), dtype="float32")
    dim = S.shape[1] if S.size else 384
    print(f"  인코딩 완료 {time.time()-t1:.0f}s (dim {dim})", flush=True)

    # --- 단어별 센트로이드(평균 후 L2 정규화) ---
    words = sorted(target)
    M = np.zeros((len(words), dim), dtype="float32")
    meta = []
    for r, w in enumerate(words):
        sents = cand.get(w, [])
        if sents:
            v = S[[sidx[s] for s in sents]].mean(axis=0)
            nrm = np.linalg.norm(v)
            if nrm > 0:
                M[r] = v / nrm
        meta.append({"token": w, "tier": pool[w]["tier"], "n_sent": len(sents)})
    np.save(os.path.join(data_dir, "pool_centroids.npy"), M)
    json.dump(meta, open(os.path.join(data_dir, "pool_centroids_words.json"), "w",
              encoding="utf-8"), ensure_ascii=False)
    n_zero = sum(1 for m in meta if m["n_sent"] == 0)
    print(f"저장: pool_centroids.npy [{M.shape}], pool_centroids_words.json "
          f"(용례0 {n_zero:,}개는 0벡터)", flush=True)


if __name__ == "__main__":
    main()
