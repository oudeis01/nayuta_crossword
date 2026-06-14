#!/usr/bin/env python3
"""전수 대문자 신호 스캔: 풀의 모든 토큰에 대해 코퍼스에서 cap_ratio/allcaps_ratio 계산.

enrich_signals.py 의 scan_capitalization 을 '풀 전체'를 타깃으로 1회 패스 수행한다.
(enrich 는 word_sentences 키=퍼즐 등장어만 타깃이라 96.6%가 신호 공백이었음.)
NER/langdetect 는 게이트에 불필요하므로 제외 → 코퍼스 1회 스캔만.

신호 정의(enrich 와 동일):
  cap_ratio     = 문장 중간 Title-case 등장수 / 총등장수   (고유명사 신호)
  allcaps_ratio = ALLCAPS(len>1) 등장수 / 총등장수          (약어 신호)

토큰화(2026-06-11 수정): ASCII 전용 [A-Za-z]+ 는 PDF 추출 잔재·발음구별기호에서
단어를 쪼개 조각 토큰을 만들고 신호를 희석했다
(phys\xad ical -> "ical", façades -> "ades", Colònia -> "nia").
  - 소프트하이픈(\xad)+공백, 하이픈+줄바꿈 을 결합해 분절 단어 복원
  - 유니코드 문자 토큰화 후 NFKD 악센트 제거로 ASCII 폴딩(façades -> facades).
    폴딩 불가(비라틴 스크립트)는 스킵.

입력 : data/wordpool.json (타깃 토큰), config.yaml (코퍼스 경로)
산출 : data/cap_signals.json  {token: {n_occ, cap_ratio, allcaps_ratio}}
"""
import json, os, re, sys, glob, time, collections, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORD_CASE_RE = re.compile(r"[^\W\d_]+")          # 유니코드 문자 연속
SOFT_HYPH_RE = re.compile(r"\xad\s*")            # 소프트하이픈(+후행 공백) = 결합 마커
HARD_BREAK_RE = re.compile(r"-\s*\n\s*")         # 줄바꿈 하이픈 분절 결합
SENT_INIT_PREV = set(".!?\n\r")


def ascii_fold(tok):
    """NFKD 악센트 제거 ASCII 폴딩. 비라틴 스크립트는 빈 문자열이 된다."""
    return unicodedata.normalize("NFKD", tok).encode("ascii", "ignore").decode()


def main():
    import yaml
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config.yaml"), encoding="utf-8"))
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    pool = json.load(open(os.path.join(data_dir, "wordpool.json"), encoding="utf-8"))
    target = set(pool.keys())
    print(f"타깃(풀 전체) {len(target):,}개", flush=True)

    corpus_root = cfg["paths"]["corpus_root"]
    include_dirs = cfg["corpus"]["include_dirs"]
    include_seg = set(cfg["corpus"]["include_segment_types"])
    total = collections.Counter()
    midcap = collections.Counter()
    allcaps = collections.Counter()
    n_pages = 0
    t0 = time.time()
    for d in include_dirs:
        for f in glob.glob(os.path.join(corpus_root, d, "**", "*.json"), recursive=True):
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
                if "\xad" in content:
                    content = SOFT_HYPH_RE.sub("", content)
                if "-" in content:
                    content = HARD_BREAK_RE.sub("", content)
                for m in WORD_CASE_RE.finditer(content):
                    tok = m.group(0)
                    if not tok.isascii():
                        tok = ascii_fold(tok)
                        if not tok:
                            continue
                    low = tok.lower()
                    if low not in target:
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
            if n_pages % 5000 == 0:
                print(f"  cap-scan {n_pages} pages {time.time()-t0:.0f}s", flush=True)
    print(f"대문자 스캔 완료 {time.time()-t0:.0f}s ({n_pages} pages)", flush=True)

    sig = {}
    for w in target:
        tot = total.get(w, 0)
        sig[w] = {
            "n_occ": tot,
            "cap_ratio": round(midcap.get(w, 0) / tot, 3) if tot else 0.0,
            "allcaps_ratio": round(allcaps.get(w, 0) / tot, 3) if tot else 0.0,
        }
    out = os.path.join(data_dir, "cap_signals.json")
    json.dump(sig, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    # 요약
    cov = sum(1 for w in target if sig[w]["n_occ"] > 0)
    hi_cap = sum(1 for w in target if sig[w]["cap_ratio"] >= 0.6)
    hi_acro = sum(1 for w in target if sig[w]["allcaps_ratio"] >= 0.6)
    print(f"저장: {out}")
    print(f"  코퍼스 등장 {cov:,}/{len(target):,} | cap>=0.6 {hi_cap:,} | allcaps>=0.6 {hi_acro:,}", flush=True)


if __name__ == "__main__":
    main()
