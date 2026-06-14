#!/usr/bin/env python3
"""Phase 1: 코퍼스 다어절 고유명사를 결합형 namedrop 답안으로 복원.

입력 : data/mw_entities.json ([[text, label, freq], ...] freq>=8, analyze_entities.py)
       data/wordpool.json (충돌/승격 판정), data/word_signals.json(참고)
출력 : data/recovered_names.json (결합형 -> {display, label, freq, parts, n_noise, status})
       docs/recovered_names_review.md (수동 점검용 상위 목록)  ← 체크포인트 1

처리:
 1) 전처리: deaccent+소문자, 선행 영어관사 the/a/an 제거, 영문자 토큰만.
    (외국어 관사 le/la/der/el은 이름 일부로 보존)
 2) 결합형(concat) 생성, 길이 3~17만.
 3) 중복 병합: 동일 concat 빈도 합산(예: "the Centre Pompidou"+"Centre Pompidou").
 4) 접두 변이 병합(truncation 제거): A.parts가 B.parts의 접두 부분리스트이고
    freq(A)<=freq(B)이면 A를 B로 흡수. (freq 가드로 New York vs New York City 보존)
 5) freq>=CW_NAME_MINFREQ(기본 25) 필터.
 6) 풀 대조: 보호 tier 존재=skip, general=승격대상, 미존재=신규.

환경 : CW_NAME_MINFREQ(기본 25)
"""
import json, os, re, unicodedata, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
PROTECTED = {"core", "marker", "name", "theme"}
LEAD_ARTICLES = {"the", "a", "an"}


def deaccent(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def to_parts(text):
    parts = re.findall(r"[a-z]+", deaccent(text).lower())
    while parts and parts[0] in LEAD_ARTICLES:
        parts = parts[1:]
    # 단일문자 토큰 제거: 소유격 's, 단일 이니셜(John F.), 끼인 약자 정리.
    # 부수효과: "John F. Kennedy"->johnkennedy 완성형 복원, "New York's"->newyork 병합.
    parts = [p for p in parts if len(p) > 1]
    return parts


def main():
    minfreq = int(os.environ.get("CW_NAME_MINFREQ", "25"))
    from nltk.corpus import words as nw
    from english_words import get_english_words_set
    from wordfreq import zipf_frequency as zf
    D = set(w.lower() for w in nw.words()) | {w.lower() for w in get_english_words_set(["web2"], lower=True)}

    mw = json.load(open(os.path.join(DATA, "mw_entities.json"), encoding="utf-8"))
    pool = json.load(open(os.path.join(DATA, "wordpool.json"), encoding="utf-8"))

    def is_noise(tok):
        return tok not in D and zf(tok, "en") < 3.5

    # 1~3) 전처리 + concat 집계(동일 concat 병합)
    agg = {}   # concat -> {freq, parts, label:Counter, display:Counter}
    for text, label, freq in mw:
        parts = to_parts(text)
        if len(parts) < 2:
            continue
        concat = "".join(parts)
        if not (3 <= len(concat) <= 17):
            continue
        r = agg.get(concat)
        if r is None:
            r = agg[concat] = {"freq": 0, "parts": parts,
                               "label": collections.Counter(), "display": collections.Counter()}
        r["freq"] += freq
        r["label"][label] += freq
        r["display"][text] += freq

    # 4) 접두 변이 병합: A.parts가 B.parts의 접두이고 freq(A)<=freq(B)면 A→B 흡수
    items = sorted(agg.items(), key=lambda kv: len(kv[1]["parts"]))  # 짧은 것부터
    parts_index = collections.defaultdict(list)   # 첫 토큰 -> [concat,...]
    for c, r in agg.items():
        parts_index[r["parts"][0]].append(c)
    merged_into = {}
    for c, r in items:
        ap = r["parts"]
        best = None
        for c2 in parts_index[ap[0]]:
            if c2 == c:
                continue
            r2 = agg[c2]
            bp = r2["parts"]
            if len(bp) > len(ap) and bp[:len(ap)] == ap and r["freq"] <= r2["freq"]:
                if best is None or r2["freq"] > agg[best]["freq"]:
                    best = c2
        if best is not None:
            merged_into[c] = best

    # 흡수 적용(체이닝 해결: 최종 타깃까지)
    def final_target(c):
        seen = set()
        while c in merged_into and c not in seen:
            seen.add(c)
            c = merged_into[c]
        return c

    canon = {}
    for c, r in agg.items():
        if c in merged_into:
            continue
        canon[c] = {"freq": r["freq"], "parts": r["parts"],
                    "label": r["label"], "display": r["display"]}
    for c, r in agg.items():
        if c in merged_into:
            tgt = final_target(c)
            if tgt in canon:
                canon[tgt]["freq"] += r["freq"]
                canon[tgt]["label"].update(r["label"])
                canon[tgt]["display"].update(r["display"])

    # 5~6) 필터 + 풀 대조
    out = {}
    skip_protected, promote, new = 0, 0, 0
    for c, r in canon.items():
        if r["freq"] < minfreq:
            continue
        rec0 = pool.get(c)
        if rec0 and rec0["tier"] in PROTECTED:
            status = "skip_protected"; skip_protected += 1
        elif rec0:
            status = "promote_general"; promote += 1
        else:
            status = "new"; new += 1
        n_noise = sum(1 for t in r["parts"] if is_noise(t))
        out[c] = {"display": r["display"].most_common(1)[0][0],
                  "label": r["label"].most_common(1)[0][0],
                  "freq": r["freq"], "parts": r["parts"],
                  "n_noise": n_noise, "status": status}

    json.dump(out, open(os.path.join(DATA, "recovered_names.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)

    # 통계
    n_noise1 = sum(1 for v in out.values() if v["n_noise"] >= 1)
    lab = collections.Counter(v["label"] for v in out.values())
    print(f"복원 이름(freq>={minfreq}): {len(out):,}개")
    print(f"  상태: 신규 {new:,} | general승격 {promote:,} | 보호tier존재(skip) {skip_protected:,}")
    print(f"  구성에 노이즈조각>=1 포함: {n_noise1:,} | 전부 일반단어: {len(out)-n_noise1:,}")
    print(f"  라벨 분포: {dict(lab.most_common())}")
    print(f"  접두변이 흡수: {len(merged_into):,}건")

    # 체크포인트 1: 수동 점검 마크다운
    os.makedirs(DOCS, exist_ok=True)
    rows = sorted(out.items(), key=lambda kv: -kv[1]["freq"])
    with open(os.path.join(DOCS, "recovered_names_review.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# 복원 이름 점검 (freq>={minfreq}, 총 {len(out):,}개)\n\n")
        fh.write("| freq | 결합형(답안) | 길이 | 원개체 | 라벨 | 노이즈조각수 | 상태 |\n")
        fh.write("|---:|---|---:|---|---|---:|---|\n")
        for c, v in rows:
            fh.write(f"| {v['freq']} | `{c}` | {len(c)} | {v['display']} | "
                     f"{v['label']} | {v['n_noise']} | {v['status']} |\n")
    print(f"  점검 파일: docs/recovered_names_review.md (상위순 {len(out):,}행)")


if __name__ == "__main__":
    main()
