"""풀 전수 감사: 코퍼스 케이스 통계로 불량 답어 후보를 일괄 검출.

배경: 퍼즐 단위 수동 검토는 매 생성마다 풀의 일부(약 3,500단어)만 표본으로
노출되어 검토 사이클이 반복된다. 이 감사는 풀 전체를 한 번에 측정해
"진성 용례"(소문자, 문중, 경계 정상, 영어 문장, URL 문맥 아님)가 없거나
희박한 단어를 목록화한다. 판정 규칙은 사용자 확정 원칙
"힌트는 코퍼스 용례로만 판단"(2026-06-12)을 기계화한 것.

출현 분류:
  trunc    인접 문자가 비ASCII 글자/소프트하이픈 (Maria->mar, vie­wed 절단)
  allcaps  전대문자 (MAXXI, WED)
  capinit  문두 두문대문자 (보통명사도 문두에선 정상: Esophagus ...)
  cap      문중 두문대문자 (고유명사 신호: ... Michael Asher ...)
  hyph     하이픈 인접 소문자 (intra-human)
  urlish   . / @ : 인접 소문자 (ngv.vic.gov.au, /mar/26/)
  initial  문두 소문자
  noneng   비영어 문장 내 소문자 (junto al mar)
  genuine  문중 소문자 정상 경계 영어 문장

판정 (general tier, genuine==0 또는 희박):
  사전(vendor/hunspell en_US, SCOWL 계열)의 소문자 수용 여부를 결합.
  hunspell은 대소문자를 구분하므로 michael은 거부, esophagus는 수용된다.
  - 사전 거부               -> 제거 권고 (인명/지명/비단어)
  - 사전 수용 + 문두 대문자 위주 -> 유지 권고 (희귀 보통명사의 정상 표기)
  - 사전 수용 + 문중 대문자 위주 -> 판단 필요 (wales 류: 사전어지만
    코퍼스는 고유명사 전용. 사용자 규칙상 제거 대상이나 확인 필요)

산출:
  data/pool_audit.json        플래그 단어 전체 통계
  docs/pool_audit_review.md   처분별 검토 목록

면제: name tier(대문자가 정상), keep_words.json(고정 힌트 확정),
sense_pins.json(의미 핀으로 이미 사람이 판정), 사용자 keep 확정 단어.
theme/marker/core tier는 큐레이션된 키워드(고유명사 정상)라 제거 권고에서
제외하고 정보용 목록만 출력. 토큰 미출현 단어(santafe 류 결합형)는
판정 불가로 건너뜀(별도 집계).

사용: .venv/bin/python src/audit_pool.py
"""
import json, os, re, sys, glob, time, collections, multiprocessing as mp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mine_sentences import (ROOT, load_config, iter_pages, split_sentences,
                            _is_english, _frag_ctx)

CATS = ["trunc", "allcaps", "capinit", "cap", "hyph", "urlish", "initial",
        "noneng", "genuine"]
CIDX = {c: i for i, c in enumerate(CATS)}
USER_KEEP = {"balder", "faun", "mecca", "satyr", "lamoca", "santafe"}
MAX_SAMPLE = 2

_TOKEN = re.compile(r"[A-Za-z]+")
_POOLSET = None
_SEG = None


def _classify(sent, i, j, tok, eng_cache):
    pre = sent[i - 1] if i > 0 else ""
    post = sent[j] if j < len(sent) else ""
    if pre.isalpha() or post.isalpha() or pre == "­" or post == "­":
        return "trunc"
    if _frag_ctx(sent, i, j):
        return "trunc"               # 하이픈+공백 건너 절단 파편 (mate- rial)
    if tok.isupper() and len(tok) > 1:
        return "allcaps"
    if tok[0].isupper():
        return "capinit" if i == 0 else "cap"
    if pre == "-" or post == "-":
        return "hyph"
    if pre in "./@:" or post in "./@:":
        return "urlish"
    if i == 0:
        return "initial"
    if eng_cache[0] is None:
        eng_cache[0] = _is_english(sent)
    if not eng_cache[0]:
        return "noneng"
    return "genuine"


def _dict_accepts(words):
    """hunspell이 소문자 그대로 수용하는 단어 집합.
    사전이 대소문자를 구분하므로 michael(Michael 등재)은 거부된다."""
    import subprocess
    env = dict(os.environ,
               DICPATH=os.path.join(ROOT, "vendor", "hunspell"))
    proc = subprocess.run(["hunspell", "-d", "en_US", "-G"],
                          input="\n".join(words) + "\n", text=True,
                          capture_output=True, env=env)
    if proc.returncode not in (0, 1) and not proc.stdout:
        raise RuntimeError(f"hunspell 실행 실패: {proc.stderr[:200]}")
    return set(proc.stdout.split())


def _scan_chunk(files):
    stats = collections.defaultdict(lambda: [0] * len(CATS))
    samples = collections.defaultdict(dict)
    for f in files:
        try:
            doc = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for b in doc.get("blocks", []):
            cls = b.get("classification") or {}
            if cls.get("segment_type") not in _SEG:
                continue
            content = b.get("content") or ""
            if not content:
                continue
            for sent in split_sentences(content):
                eng_cache = [None]
                for m in _TOKEN.finditer(sent):
                    lw = m.group(0).lower()
                    if lw not in _POOLSET:
                        continue
                    cat = _classify(sent, m.start(), m.end(), m.group(0),
                                    eng_cache)
                    stats[lw][CIDX[cat]] += 1
                    sl = samples[lw].setdefault(cat, [])
                    if len(sl) < MAX_SAMPLE:
                        sl.append(sent[:160])
    return dict(stats), dict(samples)


def main():
    global _POOLSET, _SEG
    cfg = load_config()
    p = cfg["paths"]
    data_dir = os.path.join(ROOT, p["data_dir"])
    pool = json.load(open(os.path.join(data_dir, "wordpool.json"),
                          encoding="utf-8"))

    exempt = set(USER_KEEP)
    for fn in ("keep_words.json", "sense_pins.json"):
        fp = os.path.join(data_dir, fn)
        if os.path.exists(fp):
            exempt |= set(json.load(open(fp, encoding="utf-8")))
    audit_words = {w for w, rec in pool.items()
                   if rec["tier"] != "name" and w not in exempt}
    _POOLSET = audit_words
    _SEG = set(cfg["corpus"]["include_segment_types"])
    print(f"감사 대상 {len(audit_words)}개 (풀 {len(pool)} - name tier "
          f"- 면제 {len(exempt)}개 중 풀 존재분)", flush=True)

    files = [f for _d, f in iter_pages(p["corpus_root"],
                                       cfg["corpus"]["include_dirs"])]
    _is_english("warm up the detector before fork")
    nw = max(1, (os.cpu_count() or 4) - 2)
    chunks = [files[i::nw] for i in range(nw)]
    t0 = time.time()
    with mp.Pool(nw) as mpool:
        results = mpool.map(_scan_chunk, chunks)
    print(f"스캔 완료 {time.time()-t0:.0f}s | {len(files)} pages", flush=True)

    stats = collections.defaultdict(lambda: [0] * len(CATS))
    samples = collections.defaultdict(dict)
    for st, sa in results:
        for w, v in st.items():
            acc = stats[w]
            for i, n in enumerate(v):
                acc[i] += n
        for w, cats in sa.items():
            for c, sl in cats.items():
                cur = samples[w].setdefault(c, [])
                if len(cur) < MAX_SAMPLE:
                    cur.extend(sl[:MAX_SAMPLE - len(cur)])

    gi = CIDX["genuine"]
    neutral = {"genuine", "capinit", "initial"}
    rows = []
    n_notoken = 0
    for w in sorted(audit_words):
        v = stats.get(w)
        if v is None or sum(v) == 0:
            n_notoken += 1
            continue
        total, genuine = sum(v), v[gi]
        cats = {c: v[CIDX[c]] for c in CATS if v[CIDX[c]]}
        rows.append({
            "word": w, "tier": pool[w]["tier"], "total": total,
            "genuine": genuine, "ratio": round(genuine / total, 3),
            "neutral": sum(n for c, n in cats.items() if c in neutral),
            "midbad": sum(n for c, n in cats.items() if c not in neutral),
            "cats": cats,
        })

    gen = [r for r in rows if r["tier"] == "general"]
    flag0 = [r for r in gen if r["genuine"] == 0]
    flagg = [r for r in gen if 0 < r["genuine"] <= 2 and r["total"] >= 8]
    flagg += [r for r in gen
              if r["genuine"] > 2 and r["ratio"] < 0.1 and r["total"] >= 30]
    accepted = _dict_accepts([r["word"] for r in flag0 + flagg])

    rem, judge, keep_rare = [], [], []
    for r in flag0:
        if r["word"] not in accepted:
            rem.append(r)
        elif r["neutral"] > r["midbad"]:
            keep_rare.append(r)
        else:
            judge.append(r)
    gray_rem, gray_rev = [], []
    for r in flagg:
        if (r["word"] not in accepted and r["genuine"] <= 2
                and r["total"] >= 30):
            gray_rem.append(r)
        else:
            gray_rev.append(r)
    curated = [r for r in rows if r["tier"] != "general"
               and r["genuine"] == 0]
    gray_nm = [r for r in gray_rev if r["word"] not in accepted]
    gray_dw = [r for r in gray_rev if r["word"] in accepted]
    for ls in (rem, judge, keep_rare, gray_rem, gray_nm, curated):
        ls.sort(key=lambda r: -r["total"])
    gray_dw.sort(key=lambda r: (r["ratio"], -r["total"]))

    out = {"remove": rem, "gray_remove": gray_rem, "judge": judge,
           "gray_review_names": gray_nm, "gray_review_dictwords": gray_dw,
           "keep_rare": keep_rare, "curated_info": curated,
           "n_audited": len(rows), "n_no_token": n_notoken}
    ap = os.path.join(data_dir, "pool_audit.json")
    json.dump(out, open(ap, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"저장: {ap}")
    print(f"  측정 {len(rows)} | 토큰 미출현 {n_notoken} | 제거 권고 "
          f"{len(rem)}+{len(gray_rem)} | 판단 필요 {len(judge)} | "
          f"회색(이름) {len(gray_nm)} | 회색(사전어) {len(gray_dw)} | "
          f"유지 권고 {len(keep_rare)} | 큐레이션 정보 {len(curated)}")

    lines = ["# 풀 전수 감사 결과 (코퍼스 케이스 통계 x 사전 케이스 등재)", "",
             "판정 원칙: 힌트는 코퍼스 용례로만 판단 (사용자 확정 2026-06-12).",
             "genuine = 소문자, 문중, 경계 정상, 영어 문장, URL 문맥 아님.",
             "사전 = vendor/hunspell en_US (SCOWL 계열, 대소문자 구분).", ""]

    def compact(items):
        ws = [f"{r['word']}({r['total']})" for r in items]
        return ["  " + " ".join(ws[i:i + 8]) for i in range(0, len(ws), 8)]

    def fmt(r, with_genuine):
        badcats = {c: n for c, n in r["cats"].items() if c not in neutral}
        l = [f"### {r['word']}  [{r['tier']}] 총 {r['total']} / "
             f"genuine {r['genuine']} ({r['ratio']:.0%})",
             "- 분포: " + ", ".join(f"{c} {n}"
                                    for c, n in r["cats"].items())]
        if badcats:
            bad = max(badcats, key=badcats.get)
            for s in samples[r["word"]].get(bad, [])[:MAX_SAMPLE]:
                l.append(f"- ({bad}) {s}")
        if with_genuine:
            for s in samples[r["word"]].get("genuine", [])[:MAX_SAMPLE]:
                l.append(f"- (genuine) {s}")
        return l + [""]

    lines += [f"## A. 제거 권고 {len(rem)}개", "",
              "general tier, genuine 0건, 사전 소문자 거부 (인명/지명/비단어).",
              ""] + compact(rem) + [""]
    lines += [f"## B. 회색 제거 권고 {len(gray_rem)}개", "",
              "사전 거부 + 총 30회 이상 중 genuine 1~2건(잡음 수준).",
              "genuine 표본을 확인하고 진짜 용례가 보이면 구제 대상.", ""]
    for r in gray_rem:
        lines += fmt(r, True)
    lines += [f"## C. 판단 필요 {len(judge)}개", "",
              "사전어인데 코퍼스는 문중 대문자 위주 (wales 류).",
              "사용자 규칙상 제거 대상이나 단어별 확인 필요.", ""]
    for r in judge:
        lines += fmt(r, False)
    lines += [f"## D1. 회색지대(사전 거부) {len(gray_nm)}개", "",
              "david/john 류: genuine이 있어도 소문자 스타일 표기 잡음일",
              "가능성이 높음. genuine 표본만 훑고 일괄 처분 권장.", ""]
    for r in gray_nm:
        lines += fmt(r, True)
    lines += [f"## D2. 회색지대(사전어) {len(gray_dw)}개", "",
              "genuine 희박하나 실존. 채굴 필터가 genuine 우선 수집하므로",
              "유지해도 힌트는 genuine 문장이 1순위가 됨. 표본 확인 후 처분.",
              ""]
    for r in gray_dw:
        lines += fmt(r, True)
    lines += [f"## E. 유지 권고 {len(keep_rare)}개", "",
              "사전어 + 문두 대문자/문두 소문자 위주 (희귀 보통명사 정상 표기).",
              ""] + compact(keep_rare) + [""]
    lines += [f"## F. 큐레이션 tier 정보 {len(curated)}개 (제거 비권고)", "",
              "theme/marker/core는 의도된 키워드(고유명사 정상). 참고용.",
              ""] + compact(curated) + [""]
    rp = os.path.join(ROOT, "docs", "pool_audit_review.md")
    open(rp, "w", encoding="utf-8").write("\n".join(lines))
    print(f"저장: {rp}")


if __name__ == "__main__":
    main()
