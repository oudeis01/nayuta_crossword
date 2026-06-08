#!/usr/bin/env python3
"""전체 단어 풀에 어휘 필터 적용 → 정제된 풀 생성(재생성용).

자동 제거(사용자 결정, general 티어에만 적용; themed=core/marker/name은 항상 보호):
  - 외래어 : 단어 용례 문장의 지배 언어가 영어가 아니고 확률 >= 0.90
  - 낯선 고유명사 : cap_ratio(문장중간 Title-case 비율) >= 0.95 AND corpus_freq < 100

검토 전용 리스트(삭제 안 함, 보존):
  - 아티팩트 후보 : NLTK 사전 미존재 AND corpus_freq < 10 (굴절형 오탐 가능)
  - 약어 후보 : allcaps_ratio >= 0.5

신호 계산은 자동제거 기준에 필요한 cap_ratio + lang만 전체 풀에 대해 수행(NER 미사용).
입력 : data/wordpool.json
산출 : data/wordpool_filtered.json, data/pool_filter_report.json,
       data/pool_review_lists.json
"""
import json, os, re, sys, glob, time, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORD_CASE_RE = re.compile(r"[A-Za-z]+")
TOKEN_RE = re.compile(r"[a-z]+")
SENT_INIT_PREV = set(".!?\n\r")
_WS = re.compile(r"\s+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
LANG_BUF_MAX = 300            # 단어별 언어판정용 누적 텍스트 길이 상한
MIN_SENT_LEN, MAX_SENT_LEN = 25, 320
PROPER_CAP = 0.95
PROPER_FREQ_FLOOR = 100
FOREIGN_PROB = 0.90


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def iter_pages(corpus_root, include_dirs):
    for d in include_dirs:
        for f in glob.glob(os.path.join(corpus_root, d, "**", "*.json"), recursive=True):
            yield d, f


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    pool = json.load(open(os.path.join(data_dir, "wordpool.json"), encoding="utf-8"))
    pool_tokens = set(pool.keys())
    general = {w for w, r in pool.items() if r["tier"] == "general"}
    print(f"풀 {len(pool):,} (general {len(general):,}, themed {len(pool)-len(general):,})", flush=True)

    total = collections.Counter()
    midcap = collections.Counter()
    allcaps = collections.Counter()
    lang_buf = collections.defaultdict(str)   # general word -> 누적 텍스트

    corpus_root = cfg["paths"]["corpus_root"]
    include_dirs = cfg["corpus"]["include_dirs"]
    include_seg = set(cfg["corpus"]["include_segment_types"])
    n_pages = 0
    t0 = time.time()
    for d, f in iter_pages(corpus_root, include_dirs):
        try:
            doc = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        n_pages += 1
        for b in doc.get("blocks", []):
            cls = b.get("classification") or {}
            if cls.get("segment_type") not in include_seg:
                continue
            content = b.get("content") or ""
            if not content:
                continue
            # 대문자 카운트
            for m in WORD_CASE_RE.finditer(content):
                tok = m.group(0)
                low = tok.lower()
                if low not in pool_tokens:
                    continue
                total[low] += 1
                if len(tok) > 1 and tok.isupper():
                    allcaps[low] += 1
                elif tok[0].isupper():
                    j = m.start() - 1
                    while j >= 0 and content[j] in " \t":
                        j -= 1
                    prev = content[j] if j >= 0 else ""
                    if prev and prev not in SENT_INIT_PREV:
                        midcap[low] += 1
            # 언어판정용 문장 버퍼(general만)
            for part in _SENT_SPLIT.split(content):
                s = _WS.sub(" ", part).strip()
                if not (MIN_SENT_LEN <= len(s) <= MAX_SENT_LEN):
                    continue
                toks = set(TOKEN_RE.findall(s.lower()))
                hit = toks & general
                if not hit:
                    continue
                for w in hit:
                    if len(lang_buf[w]) < LANG_BUF_MAX:
                        lang_buf[w] += " " + s
        if n_pages % 10000 == 0:
            print(f"  scan {n_pages} pages {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    print(f"스캔 완료 {time.time()-t0:.0f}s ({n_pages} pages)", flush=True)

    # 언어 감지
    from langdetect import detect_langs, DetectorFactory, LangDetectException
    DetectorFactory.seed = 0
    lang = {}
    t0 = time.time()
    for w in general:
        buf = lang_buf.get(w, "").strip()
        if len(buf) < 25:
            lang[w] = (None, 0.0)
            continue
        try:
            res = detect_langs(buf)
            lang[w] = (res[0].lang, round(res[0].prob, 3))
        except LangDetectException:
            lang[w] = (None, 0.0)
    print(f"언어 감지 완료 {time.time()-t0:.0f}s", flush=True)

    # NLTK 사전(아티팩트 검토 리스트용)
    from nltk.corpus import words as nltk_words
    english = set(w.lower() for w in nltk_words.words())

    # --- 필터 적용 ---
    removed_foreign, removed_proper = [], []
    review_artifact, review_acronym = [], []
    filtered = {}
    for w, rec in pool.items():
        if rec["tier"] != "general":
            filtered[w] = rec       # themed 보호
            continue
        tot = total.get(w, 0)
        cap = (midcap.get(w, 0) / tot) if tot else 0.0
        ac = (allcaps.get(w, 0) / tot) if tot else 0.0
        lg, lgp = lang.get(w, (None, 0.0))
        freq = rec.get("corpus_freq") or 0
        is_foreign = lg not in (None, "en") and lgp >= FOREIGN_PROB
        is_proper_obscure = cap >= PROPER_CAP and freq < PROPER_FREQ_FLOOR
        if is_foreign:
            removed_foreign.append(w)
            continue
        if is_proper_obscure:
            removed_proper.append(w)
            continue
        filtered[w] = rec
        # 검토 리스트(유지하되 표시)
        if w not in english and freq < 10:
            review_artifact.append(w)
        if ac >= 0.5:
            review_acronym.append(w)

    json.dump(filtered, open(os.path.join(data_dir, "wordpool_filtered.json"), "w",
              encoding="utf-8"), ensure_ascii=False)
    report = {
        "pool_before": len(pool),
        "pool_after": len(filtered),
        "removed_total": len(pool) - len(filtered),
        "removed_foreign": len(removed_foreign),
        "removed_proper_obscure": len(removed_proper),
        "criteria": {
            "foreign": f"lang!=en & prob>={FOREIGN_PROB}",
            "proper_obscure": f"cap_ratio>={PROPER_CAP} & corpus_freq<{PROPER_FREQ_FLOOR}",
        },
        "review_artifact_count": len(review_artifact),
        "review_acronym_count": len(review_acronym),
        "general_before": len(general),
        "general_after": sum(1 for r in filtered.values() if r["tier"] == "general"),
    }
    json.dump(report, open(os.path.join(data_dir, "pool_filter_report.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump({
        "removed_foreign": sorted(removed_foreign),
        "removed_proper_obscure": sorted(removed_proper),
        "review_artifact": sorted(review_artifact),
        "review_acronym": sorted(review_acronym),
    }, open(os.path.join(data_dir, "pool_review_lists.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)

    print("\n" + "=" * 60)
    print(f"풀 {report['pool_before']:,} → {report['pool_after']:,} "
          f"(제거 {report['removed_total']:,})")
    print(f"  외래어 제거: {report['removed_foreign']:,}")
    print(f"  낯선 고유명사 제거: {report['removed_proper_obscure']:,}")
    print(f"  (검토 보존) 아티팩트 후보: {report['review_artifact_count']:,} | "
          f"약어 후보: {report['review_acronym_count']:,}")
    print("=" * 60)
    print("저장: wordpool_filtered.json, pool_filter_report.json, pool_review_lists.json", flush=True)


if __name__ == "__main__":
    main()
