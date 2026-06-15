#!/usr/bin/env python3
"""퍼즐별 공개 힌트 페이지 정적 사이트 생성 (Cloudflare Workers Static Assets용).

각 퍼즐(원본 240개)을 한 페이지로 만든다. 한 장 = 인쇄 카드와 동일한 십자말풀이
격자를 그대로 렌더한 것이다. 칸을 탭하면 그 단어의 모든 예문 힌트가 화면 하단의
고정 패널에 뜬다(격자와 겹치지 않는 상하 분할 레이아웃이라 격자는 항상 보이고
계속 탭된다). 정답 글자는 페이지에 넣지 않는다(선완성 단어만 예외;
카드에 이미 인쇄되어 공개된 글자라 격자에 같이 표시한다). 예문은 정답을 _____ 로
가린 cloze 이며, 출처 링크는 새 탭으로 연다.

URL 규약: /NNNN  (4자리 0패딩 seq). 카드 앞면 seq(= 원본 1-based 인덱스)와 동일.
  make_print 가 seq.mode=source 에서 p["_src"]=i+1 을 쓰므로 /0101 == puzzles_raw[100].
  디렉터리 방식(public/0101/index.html)이라 클린 URL 로 뜬다.

상호작용 모델(확정):
  - 화면을 상하 분할: 위=격자(스크롤), 아래=힌트 고정 패널. 둘이 겹치지 않는다.
  - 빈칸 탭 -> 그 칸이 속한 단어 선택+하이라이트, 같은 칸 재탭 -> 가로/세로 전환.
    교차칸은 패널 헤더의 Across/Down 토글로도 전환(격자를 안 가려 재탭도 정상 작동).
  - 선택 단어의 예문 힌트를 전부 펼쳐 아래 패널에 표시(본문은 비례폰트, UI 는 모노).
  - 텍스트 클루 리스트는 두지 않는다(격자만).

입력(환경변수로 교체 가능):
  data/<CW_PUZZLES>  퍼즐(기본 puzzles_raw.json). 순서가 seq 의 근거다.
  data/templates.json 격자 템플릿(template_id 로 참조).
  data/<CW_HINTS>    힌트 선택 결과(기본: hint_final.json 있으면 그것, 없으면 hint_prefill.json).
  data/<CW_SENT>     코퍼스 용례(기본 word_sentences.json) - 폴백 예문/cloze 원문.
  CW_PREFILL         선완성 단어 수(기본 3). print_config.yaml 의 select.prefill 과 같아야
                     카드의 선완성 글자와 웹 격자가 일치한다.
산출:
  public/NNNN/index.html (퍼즐별) + public/index.html + public/404.html
  + public/style.css + public/app.js + public/_headers

주의: 이 스크립트는 인쇄 코드(make_print.py)에 의존하지 않는다(공개 레포 분리).
  클루 번호 규칙(cell_numbers)과 선완성 선택(pick_prefill)을 make_print 와 동일하게
  재구현했다. 두 곳이 갈라지면 카드와 웹이 어긋나니 함께 고쳐야 한다.
"""
import collections
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

# 한 단어당 폴백(코퍼스) 예문 최대 개수. 사람검수/LLM 선택분은 전부 보여 준다.
MAX_FALLBACK = 3


def env(name, default):
    return os.environ.get(name, default)


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


# ---- cloze 매처: llm_hint_select.py 와 동일 규칙 (Cycle-1 측정과 일치 보장) ----
_SUF = r"(?:s|es|ed|ing|'s|d)?"


def find_surface(text, word):
    """문장에서 정답 단어 span 을 찾는다. 없으면 None. (2단계: 엄격->구분자 허용)"""
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


def pick_prefill(slots, assign, themed, n_prefill):
    """make_print.pick_prefill 과 동일: themed 중 교차 칸 수 내림차순 상위 n_prefill개.

    반환 (선완성 글자 {cell:char}, 선완성 슬롯 id 집합). 카드와 동일 정렬/타이브레이크.
    """
    if n_prefill <= 0:
        return {}, set()
    occ = collections.Counter()
    for s in slots:
        for cell in s["cells"]:
            occ[cell] += 1
    themed_set = set(themed)
    cand = []
    for s in slots:
        w = assign.get(str(s["id"]))
        if not w or w not in themed_set:
            continue
        crossings = sum(1 for cell in s["cells"] if occ[cell] > 1)
        cand.append((-crossings, -s["len"], w, s))
    cand.sort(key=lambda t: t[:3])
    cells, ids = {}, set()
    for _, _, w, s in cand[:n_prefill]:
        ids.add(s["id"])
        for ch, cell in zip(w, s["cells"]):
            cells[cell] = ch
    return cells, ids


def domain_of(url):
    m = re.match(r"https?://([^/]+)", url or "")
    d = m.group(1) if m else (url or "")
    return d[4:] if d.startswith("www.") else d


def cloze_html(text, word):
    """예문에서 정답을 _____ 로 가린 HTML 을 돌려준다. 매칭 실패 시 None.

    None 을 절대 그대로 노출하지 않는 것이 정답 비공개 정책의 핵심이다.
    """
    span = find_surface(text, word)
    if span is None:
        return None
    s, e = span
    return html.escape(text[:s]) + '<span class="blank"></span>' + html.escape(text[e:])


# ---- 단어별 '모든' 힌트 해석: 사람검수(custom) > LLM(primary+backups) > 코퍼스 폴백 ----
def resolve_hints(word, hints, ws):
    """반환 [{html, url, domain}, ...]. 매칭 성공분만 담는다(정답 노출 차단).

    custom 힌트는 사람이 쓴 클루라 cloze 없이 그대로 1건만 돌려준다.
    """
    sel = (hints.get("selections") or {}).get(word)
    if sel:
        custom = (sel.get("custom") or "").strip()
        if custom:
            return [{"html": html.escape(custom), "url": None, "domain": None}]
        cands = []
        pri = sel.get("primary")
        if pri and pri.get("text"):
            cands.append(pri)
        for b in (sel.get("backups") or []):
            if b.get("text"):
                cands.append(b)
        out = []
        for c in cands:
            ch = cloze_html(c["text"], word)
            if ch is None:
                continue
            u = c.get("url")
            out.append({"html": ch, "url": u, "domain": domain_of(u) if u else None})
        if out:
            return out
    # 폴백: 선택 데이터가 없거나 전부 매칭 실패한 단어. 코퍼스 용례 상위에서 채운다.
    rec = ws.get(word) or {}
    out = []
    for sent in (rec.get("sentences") or []):
        ch = cloze_html(sent.get("text", ""), word)
        if ch is None:
            continue
        u = sent.get("url")
        out.append({"html": ch, "url": u, "domain": domain_of(u) if u else None})
        if len(out) >= MAX_FALLBACK:
            break
    return out


def build_slot_data(pz, grid, hints, ws):
    """격자에서 슬롯 데이터를 만든다.

    반환 (slots, num, cellslot, pre_cells, slotdata).
      cellslot: (r,c) -> {"A": id, "D": id}  (그 칸이 속한 가로/세로 슬롯 id)
      slotdata: { "<id>": {dir, num, len, given, hints:[...]} }  (정답 단어 미포함)
    """
    slots = build_slots(grid)
    num = cell_numbers(slots)
    pre_cells, pre_ids = pick_prefill(slots, pz.get("assign") or {}, pz.get("themed", []),
                                      int(env("CW_PREFILL", "3")))
    assign = pz.get("assign") or {}
    cellslot = {}
    slotdata = {}
    for s in slots:
        for (r, c) in s["cells"]:
            cellslot.setdefault((r, c), {})[s["dir"]] = s["id"]
        word = assign.get(str(s["id"]))
        given = s["id"] in pre_ids
        if not word and not given:
            continue
        dir_label = "Across" if s["dir"] == "A" else "Down"
        entry = {"dir": dir_label, "num": num[s["cells"][0]], "len": s["len"],
                 "given": given, "hints": []}
        if word and not given:
            entry["hints"] = resolve_hints(word, hints, ws)
        slotdata[str(s["id"])] = entry
    return slots, num, cellslot, pre_cells, slotdata


def grid_html(grid, num, cellslot, pre_cells, slotdata):
    """격자를 HTML 로 렌더. 선완성 칸만 글자를 넣고, 나머지는 빈 칸."""
    n = len(grid)
    rows = []
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch == "#":
                rows.append('<div class="cell block"></div>')
                continue
            cs = cellslot.get((r, c), {})
            attrs = []
            interactive = False
            aid = cs.get("A")
            did = cs.get("D")
            if aid is not None and str(aid) in slotdata:
                attrs.append(f'data-a="{aid}"')
                interactive = True
            if did is not None and str(did) in slotdata:
                attrs.append(f'data-d="{did}"')
                interactive = True
            cls = "cell"
            if interactive:
                cls += " clue"
            badge = ""
            if (r, c) in num:
                badge = f'<span class="num">{num[(r, c)]}</span>'
            letter = ""
            if (r, c) in pre_cells:
                cls += " fill"
                letter = html.escape(pre_cells[(r, c)].upper())
            attr_str = (" " + " ".join(attrs)) if attrs else ""
            rows.append(f'<div class="{cls}"{attr_str}>{badge}{letter}</div>')
    return f'<div class="grid" style="--n:{n}">' + "".join(rows) + "</div>"


def page_html(seq, pz, grid, hints, ws):
    slots, num, cellslot, pre_cells, slotdata = build_slot_data(pz, grid, hints, ws)
    gh = grid_html(grid, num, cellslot, pre_cells, slotdata)
    data_json = json.dumps(slotdata, ensure_ascii=False).replace("</", "<\\/")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{seq:04d} · {html.escape(TITLE)}</title>
<link rel="stylesheet" href="/style.css">
</head>
<body class="puzzle">
<header class="top">
  <span class="mark">{html.escape(WORDMARK)}</span>
  <span class="seq">puzzle {seq:04d}</span>
</header>
<div class="stage" id="stage">
  <p class="lead">Tap a square to read its clue. Answers are not shown.</p>
  {gh}
  <footer class="bot">{html.escape(TITLE)}</footer>
</div>

<section id="hints" hidden aria-live="polite" aria-labelledby="hints-title">
  <header class="hints-head">
    <h2 id="hints-title"></h2>
    <div id="hints-toggle" class="dirtoggle" role="group" aria-label="Across or Down" hidden></div>
    <button id="hints-close" type="button" aria-label="Close">×</button>
  </header>
  <div id="hints-body"></div>
</section>

<script type="application/json" id="slot-data">{data_json}</script>
<script src="/app.js"></script>
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
  <nav class="index">{cells}</nav>
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

CSS = """:root{--fg:#111;--bg:#fff;--mut:#888;--line:#ddd;--sel:#cfe3ff;--panel:#fff}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{font-family:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color:var(--fg);background:var(--bg);margin:0;line-height:1.6;font-size:15px}
header.top,footer.bot{display:flex;justify-content:space-between;align-items:baseline;
  padding:14px 20px;border-bottom:1px solid var(--line);font-size:12px;letter-spacing:.04em}
footer.bot{border-bottom:none;border-top:1px solid var(--line);color:var(--mut);margin-top:40px}
.mark{font-weight:500}.seq{color:var(--mut)}
main{max-width:520px;margin:0 auto;padding:20px 16px 8px}
.lead{color:var(--mut);font-size:13px;margin:0 0 18px;text-align:center}

/* 퍼즐 페이지: 상하 분할 앱 셸. 위=격자(스크롤), 아래=힌트 패널. 서로 안 겹친다.
   (index/404 는 .puzzle 미적용 -> 일반 흐름.) */
body.puzzle{height:100vh;height:100dvh;display:flex;flex-direction:column;overflow:hidden}
body.puzzle header.top{flex:0 0 auto}
.stage{flex:1 1 auto;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;
  display:flex;flex-direction:column;padding:18px 16px 8px}
.stage .lead{flex:0 0 auto}
.stage>footer.bot{margin-top:auto}

/* 격자: 카드와 동일 모양. 칸 글자 크기는 칸 폭에 비례. */
.grid{display:grid;grid-template-columns:repeat(var(--n),1fr);
  width:min(100vw - 32px,440px);margin:0 auto;border:2px solid var(--fg);
  font-size:calc(min(100vw - 32px,440px) / var(--n) * 0.46)}
.cell{position:relative;aspect-ratio:1;border:1px solid var(--line);
  display:flex;align-items:center;justify-content:center;font-weight:700;
  -webkit-user-select:none;user-select:none}
.cell.block{background:var(--fg);border-color:var(--fg)}
.cell.clue{cursor:pointer}
.cell .num{position:absolute;top:1px;left:2px;font-size:.42em;line-height:1;
  font-weight:400;color:var(--mut)}
.cell.sel{background:var(--sel)}
.cell.sel.fill{background:var(--sel)}

/* 힌트 패널: 분할의 아래 칸. 격자와 겹치지 않는 일반 흐름 요소. */
#hints{flex:0 0 auto;background:var(--panel);border-top:1px solid var(--line);
  max-height:48dvh;overflow-y:auto;-webkit-overflow-scrolling:touch;
  padding:0 18px 22px;box-shadow:0 -6px 24px rgba(0,0,0,.12);
  transform:translateY(8px);opacity:0;transition:transform .18s ease,opacity .18s ease}
#hints[hidden]{display:none}
#hints.in{transform:none;opacity:1}
.hints-head{display:flex;align-items:center;gap:10px;
  position:sticky;top:0;background:var(--panel);padding:12px 0 10px;
  border-bottom:1px solid var(--line)}
.hints-head h2{font-size:12px;text-transform:uppercase;letter-spacing:.12em;
  color:var(--mut);margin:0;font-weight:500;flex:1 1 auto}
#hints-close{flex:0 0 auto;background:none;border:none;color:var(--mut);font-size:26px;
  line-height:1;cursor:pointer;padding:0 4px}
.dirtoggle{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.dirtoggle[hidden]{display:none}
.dirtoggle button{background:none;border:none;font:inherit;font-size:11px;
  letter-spacing:.06em;padding:5px 9px;color:var(--mut);cursor:pointer;white-space:nowrap}
.dirtoggle button+button{border-left:1px solid var(--line)}
.dirtoggle button.on{background:var(--sel);color:var(--fg)}
#hints-body{padding-top:14px}

/* 예문: 본문만 비례폰트. 출처는 모노 작은 글씨. */
.ex{padding:0 0 16px;margin:0 0 16px;border-bottom:1px dotted var(--line)}
.ex:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.ex .sent{font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,
  Helvetica,Arial,sans-serif;font-size:16px;line-height:1.7;margin:0 0 8px}
.ex .src{font-size:12px;color:var(--mut);text-decoration:none}
.ex .src::before{content:"↳ "}
.ex .src:hover{text-decoration:underline}
.blank{display:inline-block;min-width:2.6em;border-bottom:2px solid currentColor;
  vertical-align:baseline;margin:0 .15em}
.note{color:var(--mut);font-size:13px;margin:4px 0}

nav.index{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:8px;margin-top:16px}
nav.index a{border:1px solid var(--line);padding:10px 0;text-align:center;text-decoration:none;
  color:var(--fg);font-size:13px}
nav.index a:hover{background:#f4f4f4}
a{color:#1a5fb4}
@media(prefers-color-scheme:dark){
  :root{--fg:#eee;--bg:#111;--mut:#999;--line:#333;--sel:#274868;--panel:#1a1a1a}
  nav.index a:hover{background:#1a1a1a}a{color:#7bb}
}
"""

APP_JS = """// 상하 분할: 격자 칸 탭 -> 단어 선택/토글 -> 화면 하단 고정 패널에 그 단어 힌트 표시.
// 패널은 격자와 겹치지 않는 별개 영역이라 격자는 항상 보이고 계속 탭된다(재탭 토글 정상).
// 교차칸은 패널 헤더의 Across/Down 토글 버튼으로도 방향 전환 가능.
// 정적 사이트라 의존성 없음. 데이터는 페이지 인라인 JSON(#slot-data).
(function () {
  var data = {};
  try { data = JSON.parse(document.getElementById('slot-data').textContent || '{}'); }
  catch (e) { data = {}; }

  var grid = document.querySelector('.grid');
  var panel = document.getElementById('hints');
  var titleEl = document.getElementById('hints-title');
  var toggleEl = document.getElementById('hints-toggle');
  var bodyEl = document.getElementById('hints-body');
  var closeBtn = document.getElementById('hints-close');
  if (!grid || !panel) return;

  var current = null;   // 현재 선택 슬롯 id (문자열)
  var curOpts = [];     // 마지막 탭한 칸의 [가로, 세로] 슬롯 id (방향 토글 대상)

  function clearSel() {
    var on = grid.querySelectorAll('.cell.sel');
    for (var i = 0; i < on.length; i++) on[i].classList.remove('sel');
  }

  function highlight(id) {
    clearSel();
    var cells = grid.querySelectorAll('[data-a="' + id + '"],[data-d="' + id + '"]');
    for (var i = 0; i < cells.length; i++) cells[i].classList.add('sel');
  }

  function renderToggle() {
    toggleEl.innerHTML = '';
    if (curOpts.length < 2) { toggleEl.hidden = true; return; }
    toggleEl.hidden = false;
    for (var i = 0; i < curOpts.length; i++) {
      (function (id) {
        var slot = data[id];
        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = slot ? (slot.dir + ' ' + slot.num) : id;
        if (id === current) b.className = 'on';
        b.addEventListener('click', function () { if (id !== current) select(id); });
        toggleEl.appendChild(b);
      })(curOpts[i]);
    }
  }

  function renderBody(slot) {
    bodyEl.innerHTML = '';
    if (slot.given) {
      var g = document.createElement('p');
      g.className = 'note';
      g.textContent = 'This word is already filled in on the grid.';
      bodyEl.appendChild(g);
      return;
    }
    if (!slot.hints || !slot.hints.length) {
      var nn = document.createElement('p');
      nn.className = 'note';
      nn.textContent = 'No example available for this word yet.';
      bodyEl.appendChild(nn);
      return;
    }
    for (var i = 0; i < slot.hints.length; i++) {
      var h = slot.hints[i];
      var ex = document.createElement('div');
      ex.className = 'ex';
      var p = document.createElement('p');
      p.className = 'sent';
      p.innerHTML = h.html;
      ex.appendChild(p);
      if (h.url) {
        var a = document.createElement('a');
        a.className = 'src';
        a.href = h.url;
        a.target = '_blank';
        a.rel = 'noopener';
        a.textContent = h.domain || 'source';
        ex.appendChild(a);
      }
      bodyEl.appendChild(ex);
    }
  }

  function select(id) {
    var slot = data[id];
    if (!slot) return;
    current = id;
    highlight(id);
    titleEl.textContent = slot.dir + ' ' + slot.num + ' · ' + slot.len + ' letters';
    renderToggle();
    renderBody(slot);
    panel.hidden = false;
    requestAnimationFrame(function () { panel.classList.add('in'); });
    // 선택 칸이 패널 위쪽 격자 영역 안에 보이도록 스크롤(패널과 겹치지 않음).
    var first = grid.querySelector('.cell.sel');
    if (first && first.scrollIntoView) first.scrollIntoView({block: 'center', behavior: 'smooth'});
  }

  function closePanel() {
    if (panel.hidden) return;
    panel.classList.remove('in');
    clearSel();
    current = null;
    curOpts = [];
    panel.hidden = true;
  }

  // 문서 전역 탭 처리:
  //  - 클루 칸 탭 -> 선택/전환(교차칸 재탭은 방향 토글)
  //  - 패널 내부 탭 -> 패널이 처리(닫기/토글 버튼)
  //  - 그 외(검은칸/여백) 탭 -> 패널 닫기
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (panel.contains(t)) return;
    var cell = t.closest ? t.closest('.cell.clue') : null;
    if (!cell) { closePanel(); return; }
    var a = cell.getAttribute('data-a');
    var d = cell.getAttribute('data-d');
    var opts = [];
    if (a) opts.push(a);
    if (d) opts.push(d);
    if (!opts.length) { closePanel(); return; }
    curOpts = opts;
    var pick;
    if (opts.length === 1) {
      pick = opts[0];
    } else if (current && opts.indexOf(current) !== -1) {
      pick = opts[(opts.indexOf(current) + 1) % 2];  // 같은 교차칸 재탭 -> 방향 전환
    } else {
      pick = opts[0];
    }
    select(pick);
  });

  closeBtn.addEventListener('click', closePanel);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) closePanel();
  });
})();
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
    n_slot = n_given = n_with = n_empty = 0
    ex_total = 0
    for i, pz in enumerate(puzzles):
        seq = i + 1
        grid = grid_by_id.get(pz["template_id"])
        if grid is None:
            print(f"  ! seq {seq:04d}: template {pz['template_id']} 없음, 건너뜀", flush=True)
            continue
        slots, num, cellslot, pre_cells, slotdata = build_slot_data(pz, grid, hints, ws)
        for sid, e in slotdata.items():
            n_slot += 1
            if e["given"]:
                n_given += 1
            elif e["hints"]:
                n_with += 1
                ex_total += len(e["hints"])
            else:
                n_empty += 1
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
    with open(os.path.join(out_dir, "app.js"), "w", encoding="utf-8") as f:
        f.write(APP_JS)
    with open(os.path.join(out_dir, "_headers"), "w", encoding="utf-8") as f:
        f.write("/*\n  X-Robots-Tag: noindex\n")

    solvable = n_with + n_empty
    avg = ex_total / n_with if n_with else 0
    print(f"빌드 완료: {len(seqs)} 페이지 → {out_dir}", flush=True)
    print(f"  슬롯 {n_slot}개 | 선완성(given) {n_given} / 힌트있음 {n_with} / 힌트없음 {n_empty}", flush=True)
    print(f"  풀 단어 {solvable}개 | 예문 총 {ex_total}개 (단어당 평균 {avg:.2f})", flush=True)
    print(f"  힌트데이터: {hints_name}", flush=True)
    print(f"  base={BASE_URL}  생성시각={datetime.datetime.now().isoformat(timespec='seconds')}", flush=True)


if __name__ == "__main__":
    main()
