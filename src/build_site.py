#!/usr/bin/env python3
"""퍼즐별 공개 힌트 페이지 정적 사이트 생성 (Cloudflare Pages용).

각 퍼즐(원본 240개)을 한 페이지로 만든다. 한 장 = 그 퍼즐의 Across/Down 클루
목록이며, 클루는 "정답을 _____ 로 가린 코퍼스 예문"(cloze)이다. 정답은 공개하지
않는다(QR 정책). 클루마다 원본 출처 URL을 각주(부록)로 단다.

URL 규약: /NNNN  (4자리 0패딩 seq). 카드 앞면 seq(= 원본 1-based 인덱스)와 동일.
  make_print 가 seq.mode=source 에서 p["_src"]=i+1 을 쓰므로 /0101 == puzzles_raw[100].
  디렉터리 방식(public/0101/index.html)이라 Cloudflare Pages 에서 클린 URL 로 뜬다.

입력(환경변수로 교체 가능):
  data/<CW_PUZZLES>  퍼즐(기본 puzzles_raw.json). 순서가 seq 의 근거다.
  data/templates.json 격자 템플릿(template_id 로 참조).
  data/<CW_HINTS>    힌트 선택 결과(기본: hint_final.json 있으면 그것, 없으면 hint_prefill.json).
  data/<CW_SENT>     코퍼스 용례(기본 word_sentences.json) - 폴백 예문/cloze 원문.
산출:
  public/NNNN/index.html (퍼즐별) + public/index.html + public/404.html + public/_headers

주의: 이 스크립트는 인쇄 코드(make_print.py)에 의존하지 않는다(공개 레포 분리).
  클루 번호 규칙은 make_print.cell_numbers 와 동일하게 재구현했다.
"""
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fill import build_slots  # noqa: E402

# ---- 사이트 메타 (도메인 확정값) -------------------------------------------
TITLE = "Nayuta: The Transformer"
WORDMARK = "nayuta"
BASE_URL = "https://crossword.choiharam.com"


def env(name, default):
    return os.environ.get(name, default)


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


# ---- cloze 매처: llm_hint_select.py 와 동일 규칙 (Cycle-1 측정과 일치 보장) ----
_SUF = r"(?:s|es|ed|ing|'s|d)?"


def find_surface(text, word):
    """문장에서 정답 단어 span 을 찾는다. 없으면 None. (2단계: 엄격→구분자 허용)"""
    w = re.escape(word)
    m = re.search(r"\b" + w + _SUF + r"\b", text, re.IGNORECASE)
    if m:
        return m.start(), m.end()
    if word.endswith("y"):
        m = re.search(r"\b" + re.escape(word[:-1]) + r"ies\b", text, re.IGNORECASE)
        if m:
            return m.start(), m.end()
    sep = r"[\s\-.’']{0,2}"
    core = sep.join(re.escape(ch) for ch in word)
    m = re.search(r"\b" + core + _SUF + r"\b", text, re.IGNORECASE)
    return (m.start(), m.end()) if m else None


def cell_numbers(slots):
    """make_print.cell_numbers 와 동일: 시작칸을 (row,col) 순으로 1..n 번호."""
    starts = sorted({s["cells"][0] for s in slots}, key=lambda rc: (rc[0], rc[1]))
    return {cell: i + 1 for i, cell in enumerate(starts)}


def domain_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    d = m.group(1) if m else (url or "")
    return d[4:] if d.startswith("www.") else d


# ---- 힌트 1개 해석: 사람검수 > LLM prefill > top-sim 폴백 --------------------
def resolve_hint(word, hints, ws):
    """반환 {kind, text, url}. text 는 원문(cloze 전). url 은 출처(custom 은 None)."""
    sel = (hints.get("selections") or {}).get(word)
    if sel:
        custom = (sel.get("custom") or "").strip()
        if custom:
            return {"kind": "custom", "text": custom, "url": None}
        pri = sel.get("primary")
        if pri and pri.get("text"):
            return {"kind": "llm", "text": pri["text"], "url": pri.get("url")}
    rec = ws.get(word) or {}
    sents = rec.get("sentences") or []
    if sents:
        top = sents[0]
        return {"kind": "fallback", "text": top.get("text", ""), "url": top.get("url")}
    return {"kind": "missing", "text": "", "url": None}


def clue_html(word, hint):
    """cloze 적용한 클루 HTML 과 (출처 url 또는 None) 을 돌려준다.

    custom 힌트는 단어를 가리지 않고 그대로 보여 준다(사람이 쓴 클루).
    """
    text = hint["text"]
    if hint["kind"] == "missing" or not text:
        return '<span class="missing">(예문 없음 - 검토 필요)</span>', None
    if hint["kind"] == "custom":
        return html.escape(text), None
    span = find_surface(text, word)
    if span is None:
        # 정답을 문장에서 못 찾음(드묾). 가리지 못한 채 표시 + 표식.
        return (html.escape(text) + ' <span class="missing">(빈칸 매칭 실패)</span>',
                hint["url"])
    s, e = span
    body = (html.escape(text[:s]) + '<span class="blank"></span>' + html.escape(text[e:]))
    return body, hint["url"]


def page_html(seq, pz, grid, hints, ws):
    slots = build_slots(grid)
    num = cell_numbers(slots)
    across = sorted([s for s in slots if s["dir"] == "A"], key=lambda s: num[s["cells"][0]])
    down = sorted([s for s in slots if s["dir"] == "D"], key=lambda s: num[s["cells"][0]])

    refs = []  # 부록 각주: [(url)] (중복 url 은 합침)
    ref_index = {}

    def add_ref(url):
        if not url:
            return None
        if url not in ref_index:
            ref_index[url] = len(refs) + 1
            refs.append(url)
        return ref_index[url]

    def col(title, slist):
        rows = []
        for s in slist:
            word = (pz.get("assign") or {}).get(str(s["id"]))
            n = num[s["cells"][0]]
            if not word:
                body = '<span class="missing">(빈 슬롯)</span>'
                fn = ""
            else:
                hint = resolve_hint(word, hints, ws)
                body, url = clue_html(word, hint)
                r = add_ref(url)
                fn = f'<sup class="fn">{r}</sup>' if r else ""
            rows.append(
                f'<li><span class="cn">{n}</span>'
                f'<span class="enum">({s["len"]})</span>'
                f'<span class="clue">{body}{fn}</span></li>'
            )
        return f'<section class="dir"><h2>{title}</h2><ol class="clues">' + "".join(rows) + "</ol></section>"

    body_across = col("Across", across)
    body_down = col("Down", down)

    if refs:
        items = "".join(
            f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(domain_of(u))}</a></li>'
            for u in refs
        )
        appendix = f'<section class="refs"><h2>Sources</h2><ol class="srclist">{items}</ol></section>'
    else:
        appendix = ""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{seq:04d} · {html.escape(TITLE)}</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="top">
  <span class="mark">{html.escape(WORDMARK)}</span>
  <span class="seq">puzzle {seq:04d}</span>
</header>
<main>
  <p class="lead">Fill each blank from its sentence. Answers are not shown.</p>
  {body_across}
  {body_down}
  {appendix}
</main>
<footer class="bot">{html.escape(TITLE)}</footer>
</body>
</html>
"""


def index_html(seqs):
    cells = "".join(f'<a href="/{n:04d}">{n:04d}</a>' for n in seqs)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{html.escape(TITLE)}</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="top"><span class="mark">{html.escape(WORDMARK)}</span><span class="seq">{len(seqs)} puzzles</span></header>
<main>
  <p class="lead">{html.escape(TITLE)} — crossword hint index.</p>
  <nav class="grid">{cells}</nav>
</main>
<footer class="bot">{html.escape(TITLE)}</footer>
</body>
</html>
"""


NOT_FOUND = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 · {html.escape(TITLE)}</title><link rel="stylesheet" href="/style.css"></head>
<body><header class="top"><span class="mark">{html.escape(WORDMARK)}</span></header>
<main><p class="lead">No such puzzle.</p><p><a href="/">index</a></p></main>
<footer class="bot">{html.escape(TITLE)}</footer></body></html>
"""

CSS = """:root{--fg:#111;--bg:#fff;--mut:#888;--line:#ddd}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{font-family:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color:var(--fg);background:var(--bg);margin:0;line-height:1.6;font-size:15px}
header.top,footer.bot{display:flex;justify-content:space-between;align-items:baseline;
  padding:14px 20px;border-bottom:1px solid var(--line);font-size:12px;letter-spacing:.04em}
footer.bot{border-bottom:none;border-top:1px solid var(--line);color:var(--mut);margin-top:40px}
.mark{font-weight:500}.seq{color:var(--mut)}
main{max-width:680px;margin:0 auto;padding:24px 20px 8px}
.lead{color:var(--mut);font-size:13px;margin:0 0 24px}
h2{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--mut);
  border-bottom:1px solid var(--line);padding-bottom:6px;margin:28px 0 12px}
ol.clues{list-style:none;margin:0;padding:0}
ol.clues li{display:grid;grid-template-columns:2.2em 2.6em 1fr;gap:.4em;
  padding:8px 0;border-bottom:1px dotted var(--line);align-items:start}
.cn{font-weight:700;text-align:right}
.enum{color:var(--mut);font-size:12px;text-align:right;padding-top:1px}
.clue{}
.blank{display:inline-block;min-width:3.2em;border-bottom:1.5px solid var(--fg);
  vertical-align:baseline;margin:0 .12em}
.fn{font-size:.7em;color:var(--mut);margin-left:.15em}
.missing{color:#b00;font-size:12px}
.refs{margin-top:32px}
ol.srclist{font-size:12px;color:var(--mut);padding-left:1.6em}
ol.srclist a{color:var(--mut)}
nav.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:8px;margin-top:16px}
nav.grid a{border:1px solid var(--line);padding:10px 0;text-align:center;text-decoration:none;
  color:var(--fg);font-size:13px}
nav.grid a:hover{background:#f4f4f4}
a{color:#1a5fb4}
@media(prefers-color-scheme:dark){
  :root{--fg:#eee;--bg:#111;--mut:#888;--line:#333}
  nav.grid a:hover{background:#1a1a1a}a{color:#7bb}.missing{color:#e88}
}
"""


def main():
    puzzles = load(env("CW_PUZZLES", "puzzles_raw.json"))
    templates = load("templates.json")
    grid_by_id = {t["id"]: t["grid"] for t in templates}
    ws = load(env("CW_SENT", "word_sentences.json"))

    hints_name = env("CW_HINTS", "")
    if not hints_name:
        hints_name = "hint_final.json" if os.path.exists(
            os.path.join(ROOT, "data", "hint_final.json")) else "hint_prefill.json"
    hints = load(hints_name)

    out_dir = os.path.join(ROOT, env("CW_SITE_OUT", "public"))
    os.makedirs(out_dir, exist_ok=True)

    seqs = []
    n_clue = n_custom = n_llm = n_fallback = n_missing = n_unblanked = 0
    for i, pz in enumerate(puzzles):
        seq = i + 1
        grid = grid_by_id.get(pz["template_id"])
        if grid is None:
            print(f"  ! seq {seq:04d}: template {pz['template_id']} 없음, 건너뜀", flush=True)
            continue
        # 통계용 사전 집계
        slots = build_slots(grid)
        for s in slots:
            w = (pz.get("assign") or {}).get(str(s["id"]))
            if not w:
                continue
            n_clue += 1
            h = resolve_hint(w, hints, ws)
            n_custom += h["kind"] == "custom"
            n_llm += h["kind"] == "llm"
            n_fallback += h["kind"] == "fallback"
            n_missing += h["kind"] == "missing"
            if h["kind"] in ("llm", "fallback") and h["text"] and find_surface(h["text"], w) is None:
                n_unblanked += 1
        d = os.path.join(out_dir, f"{seq:04d}")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_html(seq, pz, grid, hints, ws))
        seqs.append(seq)

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html(seqs))
    with open(os.path.join(out_dir, "404.html"), "w", encoding="utf-8") as f:
        f.write(NOT_FOUND)
    with open(os.path.join(out_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(out_dir, "_headers"), "w", encoding="utf-8") as f:
        f.write("/*\n  X-Robots-Tag: noindex\n")

    print(f"빌드 완료: {len(seqs)} 페이지 → {out_dir}", flush=True)
    print(f"  클루 {n_clue}개 | 출처: llm {n_llm} / 폴백 {n_fallback} / custom {n_custom} / 없음 {n_missing}", flush=True)
    print(f"  힌트데이터: {hints_name} | 빈칸매칭 실패 {n_unblanked}개", flush=True)
    print(f"  base={BASE_URL}  생성시각={datetime.datetime.now().isoformat(timespec='seconds')}", flush=True)


if __name__ == "__main__":
    main()
