#!/usr/bin/env python3
"""검토용 HTML 생성: 채워진 퍼즐을 실제 크로스워드 보드로 렌더 + 단어별 용례 문장(+출처 url).

사람이 직접 퍼즐 품질을 판단하기 위한 도구. 재사용 자동화 스크립트.
 - 각 퍼즐을 17x17 보드로 렌더(이미 모두 채워진 상태, 십자말 번호 표기).
 - 보드 아래 Across/Down 단어 목록. 각 단어는 접이식(details)으로 코퍼스 용례 문장을
   의미유사도 순 최대 10개 표시하고, 각 문장에 출처 문서 원본 url 링크를 단다.
 - index.html에서 전체 퍼즐을 한눈에 보고 개별 페이지로 이동.

입력(환경변수로 교체 가능):
  data/<CW_PUZZLES>    퍼즐 파일. 기본 puzzles_raw.json
  data/<CW_SENT>       용례 파일(mine_sentences.py 산출). 기본 word_sentences.json
  data/templates.json  격자 템플릿(tidx로 참조)
산출:
  docs/<CW_REVIEW_DIR>/index.html + puzzle_NNN.html. 기본 review
"""
import json, os, sys, html, collections
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fill import build_slots  # noqa: E402

STYLE = """
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:24px;color:#1a1a1a;line-height:1.45}
a{color:#1a5fb4}
h1{font-size:20px}h2{font-size:16px;margin-top:24px;border-bottom:1px solid #ddd;padding-bottom:4px}
table.board{border-collapse:collapse;margin:8px 0}
table.board td{width:30px;height:30px;border:1px solid #888;text-align:center;
  vertical-align:middle;font-size:15px;font-weight:600;position:relative;text-transform:uppercase}
table.board td.blk{background:#222}
table.board td .num{position:absolute;top:0;left:2px;font-size:8px;font-weight:400;color:#555}
.cols{display:flex;gap:32px;flex-wrap:wrap}
.col{flex:1;min-width:340px}
details{margin:2px 0;padding:3px 6px;border:1px solid #eee;border-radius:4px}
details[open]{background:#fafafa}
summary{cursor:pointer;font-size:14px}
summary .w{font-weight:700;letter-spacing:.5px}
.meta{color:#888;font-size:12px;margin-left:6px}
.themed summary .w{color:#a51d2d}
.short summary .w{color:#c64600}
ul.sent{margin:6px 0 6px 0;padding-left:18px}
ul.sent li{font-size:13px;margin:3px 0}
.sim{color:#999;font-size:11px}
.src{font-size:11px;margin-left:6px;white-space:nowrap}
.nosent{color:#b00;font-size:12px}
.legend{font-size:12px;color:#555}
table.idx{border-collapse:collapse}table.idx td,table.idx th{border:1px solid #ddd;padding:4px 10px;font-size:13px}
"""


def load(name, default):
    fn = os.environ.get(name, default)
    return fn


def cell_grid(grid, slots, assign):
    """(r,c)->letter, 그리고 (r,c)->clue number."""
    n = len(grid)
    letter = {}
    for s in slots:
        w = assign.get(str(s["id"]))
        if not w:
            continue
        for ch, cell in zip(w, s["cells"]):
            letter[cell] = ch
    starts = sorted({s["cells"][0] for s in slots}, key=lambda rc: (rc[0], rc[1]))
    num = {cell: i + 1 for i, cell in enumerate(starts)}
    return letter, num


def board_html(grid, letter, num):
    n = len(grid)
    rows = []
    for r in range(n):
        tds = []
        for c in range(n):
            if grid[r][c] == "#":
                tds.append('<td class="blk"></td>')
            else:
                lab = f'<span class="num">{num[(r,c)]}</span>' if (r, c) in num else ""
                ch = html.escape(letter.get((r, c), "")).upper()
                tds.append(f"<td>{lab}{ch}</td>")
        rows.append("<tr>" + "".join(tds) + "</tr>")
    return '<table class="board">' + "".join(rows) + "</table>"


def word_block(word, ws):
    """단어 1개의 접이식 details(요약 + 용례 문장)."""
    rec = ws.get(word, {})
    tier = rec.get("tier") or "general"
    freq = rec.get("corpus_freq")
    doc = rec.get("doc_freq")
    sents = rec.get("sentences", [])
    cls = []
    if tier != "general":
        cls.append("themed")
    if len(word) <= 3:
        cls.append("short")
    clsattr = f' class="{" ".join(cls)}"' if cls else ""
    meta = f'<span class="meta">[{tier}] freq={freq} doc={doc} len={len(word)} 용례 {rec.get("n_found",0)}</span>'
    parts = [f"<details{clsattr}><summary><span class=\"w\">{html.escape(word)}</span>{meta}</summary>"]
    if sents:
        parts.append('<ul class="sent">')
        for s in sents:
            u = s.get("url") or ""
            host = urlparse(u).netloc if u else ""
            link = f' <a class="src" href="{html.escape(u)}" target="_blank">[{html.escape(host)}]</a>' if u else ""
            parts.append(f'<li><span class="sim">({s["sim"]:.2f})</span> '
                         f'{html.escape(s["text"])}{link}</li>')
        parts.append("</ul>")
    else:
        parts.append('<div class="nosent">코퍼스 용례 없음(강제포함/멀티워드 매칭 실패 가능).</div>')
    parts.append("</details>")
    return "".join(parts)


def puzzle_page(pz, template, ws):
    grid = template["grid"]
    slots = build_slots(grid)
    letter, num = cell_grid(grid, slots, pz["assign"])
    board = board_html(grid, letter, num)

    # Across/Down 목록(번호순)
    across = sorted([s for s in slots if s["dir"] == "A"], key=lambda s: num[s["cells"][0]])
    down = sorted([s for s in slots if s["dir"] == "D"], key=lambda s: num[s["cells"][0]])

    def col(title, slist):
        out = [f"<div class='col'><h2>{title} ({len(slist)})</h2>"]
        for s in slist:
            w = pz["assign"].get(str(s["id"]), "")
            n = num[s["cells"][0]]
            out.append(f'<div><b>{n}.</b> {word_block(w, ws)}</div>')
        out.append("</div>")
        return "".join(out)

    tiers = pz.get("tiers", {})
    themed = pz.get("themed", [])
    head = (f"<h1>{pz.get('template_id','?')} · seed {pz.get('seed')} · "
            f"단어 {pz.get('n_words')}개</h1>"
            f"<div class='legend'>티어 {html.escape(json.dumps(tiers, ensure_ascii=False))} · "
            f"themed {len(themed)}개: {html.escape(', '.join(themed))}</div>"
            f"<div class='legend'>빨강=테마어, 주황=3자 단어. 단어를 클릭하면 코퍼스 용례+출처가 펼쳐집니다.</div>")
    body = (f"{head}{board}<div class='cols'>{col('Across', across)}{col('Down', down)}</div>"
            f"<p><a href='index.html'>← 목록</a></p>")
    return f"<!doctype html><html lang='ko'><head><meta charset='utf-8'>" \
           f"<title>{pz.get('template_id','?')}</title><style>{STYLE}</style></head>" \
           f"<body>{body}</body></html>"


def main():
    cfg_path = os.path.join(ROOT, "config.yaml")
    import yaml
    cfg = yaml.safe_load(open(cfg_path, encoding="utf-8"))
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    docs_dir = os.path.join(ROOT, "docs")

    puzzles_file = load("CW_PUZZLES", "puzzles_raw.json")
    sent_file = load("CW_SENT", "word_sentences.json")
    review_dir = os.path.join(docs_dir, load("CW_REVIEW_DIR", "review"))
    os.makedirs(review_dir, exist_ok=True)

    # 이전 세대 잔재 제거: 퍼즐 수가 줄면 구본 puzzle_*.html이 남아 검수를 오염시킨다.
    import glob as _glob
    stale = _glob.glob(os.path.join(review_dir, "puzzle_*.html"))
    for f in stale:
        os.remove(f)
    if stale:
        print(f"기존 puzzle_*.html {len(stale)}개 삭제(세대 혼합 방지)", flush=True)

    puzzles = json.load(open(os.path.join(data_dir, puzzles_file), encoding="utf-8"))
    templates = json.load(open(os.path.join(data_dir, "templates.json"), encoding="utf-8"))
    ws = json.load(open(os.path.join(data_dir, sent_file), encoding="utf-8"))
    puzzles = [z for z in puzzles if z.get("ok")]

    # 동일 채움(같은 template + 동일 배치) 중복 제거: race로 같은 답이 여러 번 나올 수 있음.
    seen, dedup = set(), []
    for z in puzzles:
        key = (z["tidx"], tuple(sorted(z["assign"].items())))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(z)
    puzzles = dedup

    # 크기 주입 후 (크기, 템플릿) 순 정렬 → 크기별로 모아 검수.
    for z in puzzles:
        z["_size"] = len(templates[z["tidx"]]["grid"])
    puzzles.sort(key=lambda z: (z["_size"], z.get("template_id", ""), z.get("seed", 0)))
    by_size = collections.Counter(z["_size"] for z in puzzles)
    print(f"퍼즐 {len(puzzles)}개(중복제거 후) | 용례 단어 {len(ws):,}개 → {review_dir}", flush=True)
    print(f"  크기별: {dict(sorted(by_size.items()))}", flush=True)

    # 개별 페이지 (크기별 그룹 인덱스)
    idx_groups = collections.OrderedDict()
    for i, pz in enumerate(puzzles):
        template = templates[pz["tidx"]]
        page = puzzle_page(pz, template, ws)
        fn = f"puzzle_{i:03d}.html"
        with open(os.path.join(review_dir, fn), "w", encoding="utf-8") as fh:
            fh.write(page)
        sz = pz["_size"]
        row = (f"<tr><td>{i}</td><td><a href='{fn}'>{html.escape(pz.get('template_id','?'))}</a></td>"
               f"<td>{sz}x{sz}</td><td>{pz.get('seed')}</td><td>{pz.get('n_words')}</td>"
               f"<td>{len(pz.get('themed',[]))}</td></tr>")
        idx_groups.setdefault(sz, []).append(row)

    summary = "".join(f"<tr><td>{s}x{s}</td><td>{len(rows)}</td></tr>"
                      for s, rows in sorted(idx_groups.items()))
    sections = []
    for s, rows in sorted(idx_groups.items()):
        sections.append(
            f"<h2>{s}x{s} ({len(rows)}개)</h2>"
            f"<table class='idx'><tr><th>#</th><th>템플릿</th><th>크기</th><th>seed</th>"
            f"<th>단어수</th><th>themed</th></tr>{''.join(rows)}</table>")

    index = (f"<!doctype html><html lang='ko'><head><meta charset='utf-8'>"
             f"<title>퍼즐 검토</title><style>{STYLE}</style></head><body>"
             f"<h1>퍼즐 검토 ({len(puzzles)}개)</h1>"
             f"<div class='legend'>입력: {html.escape(puzzles_file)} / 용례: {html.escape(sent_file)}</div>"
             f"<h2>크기별 생산량</h2>"
             f"<table class='idx'><tr><th>크기</th><th>퍼즐 수</th></tr>{summary}</table>"
             f"{''.join(sections)}"
             f"</body></html>")
    with open(os.path.join(review_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    print(f"저장: {review_dir}/index.html (+ puzzle_*.html {len(puzzles)}개)", flush=True)


if __name__ == "__main__":
    main()
