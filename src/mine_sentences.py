#!/usr/bin/env python3
"""4단계(부분): 퍼즐에 쓰인 모든 단어의 코퍼스 용례 문장 채굴 + 의미유사도 랭킹.

목적: 어휘 필터링 검토용 문서 생성(+ 힌트 문장 후보). 각 단어마다 코퍼스에서 그 단어가
실제 쓰인 문장을 모아, 단어 임베딩과의 코사인 유사도 순으로 최대 N개를 남긴다.
각 문장에는 출처 문서의 원본 url을 함께 기록한다(검토 UI 링크용).

입력:
  data/<CW_PUZZLES>      성공 퍼즐 (assign 값 = 사용된 단어). 기본 puzzles_raw.json
  data/wordpool.json     단어 메타(tier, corpus_freq, doc_freq, sources)
  data/keyword_tokens.json 멀티워드 키워드의 결합토큰 -> 띄어쓴 원형(스캔용)
산출:
  data/<CW_SENT_OUT>     구조화 결과(필터링/렌더링용). 기본 word_sentences.json
  docs/word_review.md    알파벳순 사람이 읽는 검토 문서

환경변수:
  CW_PUZZLES   입력 퍼즐 파일명(data_dir 기준). 기본 puzzles_raw.json
  CW_SENT_OUT  출력 용례 파일명(data_dir 기준). 기본 word_sentences.json

임베딩 모델: sentence-transformers/all-MiniLM-L6-v2 (HF_HOME 캐시 사용, GPU).
"""
import json, os, re, sys, glob, time, collections, multiprocessing as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("HF_HOME", "/home/choiharam/storage/models/huggingface")
os.environ.setdefault("HF_HUB_OFFLINE", "1")          # 캐시 우선(오프라인)
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

TOKEN_RE = re.compile(r"[a-z]+")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MAX_KEEP = 10          # 단어당 문서에 남길 문장 수
MAX_CAND = 60          # 단어당 임베딩 후보 상한(스캔 중 수집)
MIN_SENT_LEN = 25      # 문장 최소 길이(문자)
MAX_SENT_LEN = 320     # 문장 최대 길이(문자)


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize(text):
    return re.sub(r"[^a-z]+", " ", text.lower())


_WS = re.compile(r"\s+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def clean_sentence(s):
    return _WS.sub(" ", s).strip()


def split_sentences(content):
    for part in _SENT_SPLIT.split(content):
        s = clean_sentence(part)
        if MIN_SENT_LEN <= len(s) <= MAX_SENT_LEN:
            yield s


def iter_pages(corpus_root, include_dirs):
    for d in include_dirs:
        for f in glob.glob(os.path.join(corpus_root, d, "**", "*.json"), recursive=True):
            yield d, f


# --- CPU 병렬 코퍼스 스캔(페이지 단위 독립). fork COW로 read-only 전역 공유 ---
_SINGLE = None      # single_targets (set)
_MWTOK = None       # [(token, compiled_pattern)]
_SEG = None         # include_segment_types (set)


def _scan_chunk(files):
    """페이지 청크를 스캔해 단어별 후보 (문장,url) 수집. 워커 내 MAX_CAND 상한."""
    cand = collections.defaultdict(list)
    seen = collections.defaultdict(set)
    for f in files:
        try:
            doc = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        url = doc.get("url") or ""
        for b in doc.get("blocks", []):
            cls = b.get("classification") or {}
            if cls.get("segment_type") not in _SEG:
                continue
            content = b.get("content") or ""
            if not content:
                continue
            for sent in split_sentences(content):
                norm = normalize(sent)
                toks = set(TOKEN_RE.findall(norm))
                matched = toks & _SINGLE
                if _MWTOK:
                    for tok, pat in _MWTOK:
                        if pat.search(norm):
                            matched.add(tok)
                if not matched:
                    continue
                for w in matched:
                    if len(cand[w]) >= MAX_CAND or norm in seen[w]:
                        continue
                    seen[w].add(norm)
                    cand[w].append((sent, url))
    return dict(cand)


def main():
    cfg = load_config()
    p = cfg["paths"]
    corpus_root = p["corpus_root"]
    data_dir = os.path.join(ROOT, p["data_dir"])
    docs_dir = os.path.join(ROOT, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    include_dirs = cfg["corpus"]["include_dirs"]
    include_seg = set(cfg["corpus"]["include_segment_types"])

    puzzles_file = os.environ.get("CW_PUZZLES", "puzzles_raw.json")
    out_file = os.environ.get("CW_SENT_OUT", "word_sentences.json")

    # --- 타깃 단어 + 메타 ---
    puzzles = json.load(open(os.path.join(data_dir, puzzles_file), encoding="utf-8"))
    pool = json.load(open(os.path.join(data_dir, "wordpool.json"), encoding="utf-8"))
    target = set()
    for z in puzzles:
        if z.get("ok"):
            target.update(z["assign"].values())
    print(f"입력 {puzzles_file} | 타깃 단어 {len(target):,}개", flush=True)

    # 멀티워드 키워드: 결합토큰 -> 띄어쓴 원형 (정규화 텍스트에서 \b 매칭)
    kw = json.load(open(os.path.join(data_dir, "keyword_tokens.json"), encoding="utf-8"))
    mw_pat = {k["token"]: re.compile(r"\b" + re.escape(k["norm_spaced"]) + r"\b")
              for k in kw if k["n_words"] > 1 and k["token"] in target}
    mw_tokens = list(mw_pat.items())
    single_targets = {t for t in target if t not in mw_pat}
    print(f"  단일토큰 {len(single_targets):,} / 멀티워드 {len(mw_pat)}", flush=True)

    # --- 코퍼스 스캔: 페이지 단위 CPU 병렬(fork COW로 타깃/패턴 공유) ---
    global _SINGLE, _MWTOK, _SEG
    _SINGLE, _MWTOK, _SEG = single_targets, mw_tokens, include_seg
    t0 = time.time()
    files = [f for _d, f in iter_pages(corpus_root, include_dirs)]
    n_pages = len(files)
    workers = max(1, min(os.cpu_count() - 2, n_pages))
    # 워커당 여러 청크로 쪼개 로드밸런싱(꼬리 페이지 편중 방지)
    n_chunks = max(workers, workers * 6)
    sz = (len(files) + n_chunks - 1) // max(1, n_chunks)
    chunks = [files[i:i + sz] for i in range(0, len(files), sz)]
    print(f"  코퍼스 {n_pages:,} pages | 워커 {workers} | 청크 {len(chunks)}", flush=True)

    cand = collections.defaultdict(list)   # word -> [(sentence, url)]
    seen = collections.defaultdict(set)    # word -> {정규화 문장} (전역 중복 방지)
    ctx = mp.get_context("fork")
    done = 0
    with ctx.Pool(workers) as pp:          # initargs 없음 → 무거운 전역은 fork로 공유
        for part in pp.imap_unordered(_scan_chunk, chunks):
            for w, lst in part.items():
                cw, sw = cand[w], seen[w]
                for sent, url in lst:
                    if len(cw) >= MAX_CAND:
                        break
                    norm = normalize(sent)
                    if norm in sw:
                        continue
                    sw.add(norm)
                    cw.append((sent, url))
            done += 1
            if done % 6 == 0 or done == len(chunks):
                covered = sum(1 for w in target if cand.get(w))
                print(f"  ... 청크 {done}/{len(chunks)} | 용례 확보 {covered:,}/{len(target):,} | "
                      f"{time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    print(f"스캔 완료 {time.time()-t0:.0f}s | {n_pages:,} pages", flush=True)
    covered = sum(1 for w in target if cand.get(w))
    print(f"  용례 1건 이상 확보: {covered:,}/{len(target):,} "
          f"(미확보 {len(target)-covered:,}는 코퍼스 미등장/강제포함 등)", flush=True)

    # --- 임베딩: 전역 중복 제거 후 일괄 인코딩 ---
    from sentence_transformers import SentenceTransformer
    import numpy as np
    print(f"모델 로드: {MODEL_NAME}", flush=True)
    model = SentenceTransformer(MODEL_NAME, device="cuda")

    all_sents = sorted({s for ss in cand.values() for (s, _u) in ss})
    sent_idx = {s: i for i, s in enumerate(all_sents)}
    print(f"고유 문장 {len(all_sents):,}개 인코딩...", flush=True)
    t1 = time.time()
    S = model.encode(all_sents, batch_size=512, convert_to_numpy=True,
                     normalize_embeddings=True, show_progress_bar=False) \
        if all_sents else np.zeros((0, 384), dtype="float32")
    words_with_cand = [w for w in target if cand.get(w)]
    W = model.encode(words_with_cand, batch_size=512, convert_to_numpy=True,
                     normalize_embeddings=True, show_progress_bar=False)
    wemb = {w: W[i] for i, w in enumerate(words_with_cand)}
    print(f"  인코딩 완료 {time.time()-t1:.0f}s", flush=True)

    # --- 단어별 top-N 랭킹 (url 보존) ---
    result = {}
    for w in sorted(target):
        rec = pool.get(w, {})
        sents = cand.get(w, [])      # [(text, url)]
        ranked = []
        if sents:
            idxs = [sent_idx[s] for (s, _u) in sents]
            sims = S[idxs] @ wemb[w]
            order = sims.argsort()[::-1][:MAX_KEEP]
            ranked = [{"text": sents[j][0], "url": sents[j][1],
                       "sim": round(float(sims[j]), 4)} for j in order]
        result[w] = {
            "tier": rec.get("tier"),
            "corpus_freq": rec.get("corpus_freq"),
            "doc_freq": rec.get("doc_freq"),
            "length": rec.get("length", len(w)),
            "sources": rec.get("sources", []),
            "forced": rec.get("forced", False),
            "n_found": len(sents),
            "sentences": ranked,
        }
    json.dump(result, open(os.path.join(data_dir, out_file), "w",
              encoding="utf-8"), ensure_ascii=False)
    print(f"저장: data/{out_file}", flush=True)

    # --- 마크다운 문서 ---
    lines = []
    lines.append("# 단어 용례 검토 문서")
    lines.append("")
    lines.append(f"퍼즐에 쓰인 전체 단어 {len(target):,}개. 알파벳순. 각 단어마다 코퍼스 "
                 f"용례를 단어 임베딩과의 의미유사도(코사인) 순으로 최대 {MAX_KEEP}개 표시.")
    lines.append(f"모델 {MODEL_NAME}. 필터링 검토용(비영어/고유명사/추출 아티팩트 식별) "
                 f"및 힌트 문장 후보.")
    lines.append("")
    lines.append("표기: `[tier] corpus_freq=빈도 doc_freq=문서수 len=길이` / 유사도는 각 문장 앞 `(0.xx)`.")
    lines.append("")
    no_sent = [w for w in sorted(target) if not result[w]["sentences"]]
    if no_sent:
        lines.append(f"## 용례 미확보 ({len(no_sent)}개)")
        lines.append("")
        lines.append("코퍼스에서 문장을 찾지 못함(강제포함 코어/멀티워드 매칭 실패 등). 우선 검토 대상.")
        lines.append("")
        lines.append(", ".join(f"`{w}`" for w in no_sent))
        lines.append("")
    lines.append("---")
    lines.append("")
    cur_letter = None
    for w in sorted(target):
        first = w[0].upper()
        if first != cur_letter:
            cur_letter = first
            lines.append(f"## {cur_letter}")
            lines.append("")
        r = result[w]
        meta = f"[{r['tier']}] corpus_freq={r['corpus_freq']} doc_freq={r['doc_freq']} len={r['length']}"
        if r["forced"]:
            meta += " FORCED"
        lines.append(f"### {w}")
        lines.append(f"{meta}")
        lines.append("")
        if not r["sentences"]:
            lines.append("_용례 없음._")
            lines.append("")
            continue
        for s in r["sentences"]:
            lines.append(f"- ({s['sim']:.2f}) {s['text']}")
        lines.append("")
    with open(os.path.join(docs_dir, "word_review.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"저장: docs/word_review.md", flush=True)


if __name__ == "__main__":
    main()
