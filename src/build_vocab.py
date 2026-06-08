#!/usr/bin/env python3
"""
1단계: 어휘 인벤토리 + 타당성 분석.

코퍼스 13개 디렉토리를 순회하며 CURATORIAL 블록의 텍스트를 토큰화하여
 - 단일 토큰 빈도/문서빈도(doc freq)
 - 키워드(JSON) 결합 토큰의 코퍼스 빈도
를 집계하고, fully-checked 11x11 격자 채우기 타당성을 가늠하는 리포트를 출력한다.

산출물:
  data/vocab.json           단일 토큰 -> {count, doc_freq, sources}
  data/keyword_tokens.json  키워드 결합 토큰 메타 + 코퍼스 빈도
  data/vocab_report.json    요약 통계 (길이 분포, 임계값별 통과 수, 키워드 커버리지)
콘솔에도 사람이 읽는 요약을 출력한다.
"""
import json, os, re, sys, glob, time, collections
from unidecode import unidecode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


# 아티팩트 내성 토큰화(사용자 결정 2026-06-06):
#  ① unidecode 음역: 발음부호 단어를 분절 없이 보존(Mondialité -> mondialite).
#  ② 이메일/URL 스팬 제거: '...@...aeT', 'http(s)://', 'www.' 조각 차단.
#  ③ 숫자 섞인 영숫자 런 전체 거부: 'n06090andn06091' -> 토큰 없음(andn 차단).
EMAIL_URL_RE = re.compile(r"\S+@\S+|https?://\S+|www\.\S+", re.I)
ALNUM_RUN_RE = re.compile(r"[a-z0-9]+")
TOKEN_RE = re.compile(r"[a-z]+")   # (호환용; 직접 토큰화는 tokenize 사용)


def clean(text):
    """음역 + 이메일/URL 제거 + 소문자화 + 아포스트로피 결합."""
    t = unidecode(text)
    t = EMAIL_URL_RE.sub(" ", t)
    return t.lower().replace("'", "")


def tokenize(text):
    """clean 후 순수 알파벳 런만 토큰으로(숫자 섞인 런은 통째로 버림)."""
    return [run for run in ALNUM_RUN_RE.findall(clean(text)) if run.isalpha()]


def normalize(text):
    """구(phrase) 스캔용: clean 후 알파벳 외(숫자 포함)는 공백."""
    return re.sub(r"[^a-z]+", " ", clean(text))


def concat_token(phrase):
    """키워드 구를 결합 토큰으로: 'climate change' -> 'climatechange'."""
    return re.sub(r"[^a-z]", "", clean(phrase))


def load_keywords(path, concatenate=True):
    """키워드 JSON -> 리스트[dict(category, tier, phrase, token, n_words, length)]."""
    data = json.load(open(path, encoding="utf-8"))
    tier_map = {
        "core_theoretical_keywords": "core",
        "broad_discourse_markers": "marker",
        "names": "name",
    }
    out = []
    for category, tiers in data.items():
        for tier_key, tier in tier_map.items():
            for phrase in tiers.get(tier_key, []):
                tok = concat_token(phrase) if concatenate else phrase.lower()
                norm = normalize(phrase).strip()
                out.append({
                    "category": category,
                    "tier": tier,
                    "phrase": phrase,
                    "token": tok,
                    "norm_spaced": norm,           # 'eco feminism' 형태 (스캔용)
                    "n_words": len(norm.split()),
                    "length": len(tok),
                })
    return out


def iter_pages(corpus_root, include_dirs):
    for d in include_dirs:
        for f in glob.glob(os.path.join(corpus_root, d, "**", "*.json"), recursive=True):
            yield d, f


def main():
    cfg = load_config()
    p = cfg["paths"]
    corpus_root = p["corpus_root"]
    data_dir = os.path.join(ROOT, p["data_dir"])
    os.makedirs(data_dir, exist_ok=True)

    include_dirs = cfg["corpus"]["include_dirs"]
    include_seg = set(cfg["corpus"]["include_segment_types"])
    min_len = cfg["vocab"]["min_len"]
    max_len = cfg["vocab"]["max_len"]

    keywords = load_keywords(p["keywords_json"], cfg["keywords"]["concatenate"])
    # 다중어/하이픈 구만 텍스트 스캔 필요 (단일 토큰 키워드는 토큰 카운터에서 조회)
    multiword = [k for k in keywords if k["n_words"] > 1]
    multiword_patterns = [(k["token"], re.compile(r"\b" + re.escape(k["norm_spaced"]) + r"\b"))
                          for k in multiword]

    counts = collections.Counter()          # 토큰 -> 총 등장 수
    docfreq = collections.Counter()         # 토큰 -> 등장 페이지 수
    sources = collections.defaultdict(set)  # 토큰 -> {코퍼스 디렉토리}
    phrase_counts = collections.Counter()   # 결합토큰 -> 다중어 구 등장 수

    n_pages = 0
    n_blocks = 0
    t0 = time.time()
    for d, f in iter_pages(corpus_root, include_dirs):
        try:
            doc = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        n_pages += 1
        page_tokens = set()
        page_norm_parts = []
        for b in doc.get("blocks", []):
            cls = b.get("classification") or {}
            if cls.get("segment_type") not in include_seg:
                continue
            content = b.get("content") or ""
            if not content:
                continue
            n_blocks += 1
            norm = normalize(content)
            page_norm_parts.append(norm)
            for tok in tokenize(content):
                counts[tok] += 1
                page_tokens.add(tok)
                sources[tok].add(d)
        for tok in page_tokens:
            docfreq[tok] += 1
        # 다중어 키워드 구 스캔 (페이지 단위 결합 텍스트)
        if multiword_patterns:
            page_text = " " + " ".join(page_norm_parts) + " "
            for tok, pat in multiword_patterns:
                c = len(pat.findall(page_text))
                if c:
                    phrase_counts[tok] += c
        if n_pages % 5000 == 0:
            print(f"  ... {n_pages} pages, {len(counts)} unique tokens, "
                  f"{time.time()-t0:.0f}s", file=sys.stderr)

    elapsed = time.time() - t0

    # --- vocab.json (min_len 이상만 저장; 분석은 별도 길이 분포에서) ---
    vocab = {}
    for tok, c in counts.items():
        if len(tok) >= min_len:
            vocab[tok] = {"count": c, "doc_freq": docfreq[tok],
                          "sources": sorted(sources[tok])}
    json.dump(vocab, open(os.path.join(data_dir, "vocab.json"), "w", encoding="utf-8"),
              ensure_ascii=False)

    # --- 키워드 토큰 빈도 산출 ---
    kw_out = []
    for k in keywords:
        if k["n_words"] > 1:
            corpus_freq = phrase_counts.get(k["token"], 0) + counts.get(k["token"], 0)
        else:
            corpus_freq = counts.get(k["token"], 0)
        rec = dict(k)
        rec["corpus_freq"] = corpus_freq
        rec["fits_grid"] = min_len <= k["length"] <= max_len
        kw_out.append(rec)
    json.dump(kw_out, open(os.path.join(data_dir, "keyword_tokens.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=2)

    # --- 통계 ---
    len_dist = collections.Counter(len(t) for t in counts)
    def passing(thr):
        return sum(1 for t, c in counts.items()
                   if c >= thr and min_len <= len(t) <= max_len)
    thresholds = [1, 3, 5, 10, 20, 50, 100]
    pass_by_thr = {thr: passing(thr) for thr in thresholds}

    # 길이별, 임계값별 (fully-checked 타당성: 3~5자 재고가 관건)
    len_by_thr = {}
    for L in range(min_len, max_len + 1):
        len_by_thr[L] = {thr: sum(1 for t, c in counts.items()
                                  if len(t) == L and c >= thr)
                         for thr in [5, 10, 20]}

    kw_fit = [k for k in kw_out if k["fits_grid"]]
    kw_present = [k for k in kw_fit if k["corpus_freq"] > 0]
    by_tier = collections.Counter(k["tier"] for k in kw_out)
    by_tier_present = collections.Counter(
        k["tier"] for k in kw_out if k["fits_grid"] and k["corpus_freq"] > 0)
    oversize = [k for k in kw_out if k["length"] > max_len]

    report = {
        "elapsed_sec": round(elapsed, 1),
        "n_pages": n_pages,
        "n_blocks": n_blocks,
        "unique_tokens_all_len": len(counts),
        "length_distribution": dict(sorted(len_dist.items())),
        "candidates_by_threshold": pass_by_thr,
        "candidates_by_length_and_threshold": len_by_thr,
        "keywords_total": len(kw_out),
        "keywords_fit_grid": len(kw_fit),
        "keywords_present_in_corpus": len(kw_present),
        "keywords_oversize_gt_maxlen": len(oversize),
        "keywords_by_tier": dict(by_tier),
        "keywords_present_by_tier": dict(by_tier_present),
    }
    json.dump(report, open(os.path.join(data_dir, "vocab_report.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=2)

    # --- 콘솔 요약 ---
    print("\n" + "=" * 60)
    print(f"코퍼스: {n_pages} pages, {n_blocks} blocks ({include_seg}) / {elapsed:.0f}s")
    print(f"고유 토큰(전체 길이): {len(counts):,}")
    print("\n[길이 분포] (min_len 미만 포함)")
    for L in range(1, max_len + 2):
        bar = "#" * min(60, len_dist.get(L, 0) // 200)
        tag = " <max" if L <= max_len else " (>max, 제외)"
        print(f"  len {L:2}: {len_dist.get(L,0):7,} {bar}{tag if L==max_len+1 else ''}")
    print("\n[후보 단어 수: 길이 3~11, 빈도 임계값별]")
    for thr in thresholds:
        print(f"  count >= {thr:3}: {pass_by_thr[thr]:7,}")
    print("\n[길이별 재고 (fully-checked 11x11은 3~5자 다수 필요)]")
    print("  len |  >=5    >=10    >=20")
    for L in range(min_len, max_len + 1):
        r = len_by_thr[L]
        print(f"  {L:3} | {r[5]:6,} {r[10]:6,} {r[20]:6,}")
    print("\n[키워드 커버리지]")
    print(f"  전체 키워드 항목: {len(kw_out)}")
    print(f"  격자 적합(3~11자): {len(kw_fit)}")
    print(f"  코퍼스 등장(>0): {len(kw_present)}")
    print(f"  결합 후 11자 초과(격자 불가): {len(oversize)}")
    print(f"  tier별 전체: {dict(by_tier)}")
    print(f"  tier별 코퍼스 등장: {dict(by_tier_present)}")
    print("=" * 60)
    print(f"\n저장: {data_dir}/vocab.json, keyword_tokens.json, vocab_report.json")


if __name__ == "__main__":
    main()
