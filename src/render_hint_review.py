#!/usr/bin/env python3
"""힌트 수동 검토용 단일 HTML 생성 (단어 중심, 퍼즐 인덱스 무관).

목적: 현재 퍼즐(전체 240개)에 쓰인 모든 단어를 알파벳 순으로 모으고, 각 단어마다
코퍼스 용례(예문)를 접이식으로 보여 준다. 사람이 단어별로
  - 대표 예문 1개(★, 클로즈 정답이 강조됨)
  - 백업 예문 여러 개(체크박스)
  - 보류 표시 / 직접 입력 힌트
를 고르고, 그 결과를 구조화된 JSON으로 내보낸다(+ 브라우저 localStorage 자동저장).

특징:
 - 단일 파일. 용례 데이터를 HTML 안에 임베드하므로 file://로 열어도 동작한다.
   (localStorage 안정성을 위해 `python -m http.server`로 여는 것을 권장)
 - 단어 본문(예문 목록)은 펼칠 때만 렌더(lazy)해 3,000+ 단어도 가볍게 다룬다.
 - 자동저장(localStorage) + JSON 내보내기/불러오기로 중간 저장·재개를 지원한다.

입력(환경변수로 교체 가능):
  data/<CW_PUZZLES>   퍼즐 파일(기본 puzzles_raw.json) - 단어 집합 산출
  data/<CW_SENT>      용례 파일(기본 word_sentences.json) - 예문
산출:
  docs/<CW_REVIEW_DIR>/hint_review.html (기본 review)
"""
import collections
import datetime
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def env(name, default):
    return os.environ.get(name, default)


def build_data(words, ws):
    """단어 -> {tier, sents:[{t,u,s,(w),(p)}]} 의 임베드용 경량 구조."""
    data = {}
    for w in words:
        rec = ws.get(w, {})
        tier = rec.get("tier") or "general"
        sents = []
        for s in rec.get("sentences", []):
            o = {"t": s.get("text", ""), "u": s.get("url", "") or "",
                 "s": round(float(s.get("sim", 0)), 2)}
            if s.get("weak"):
                o["w"] = 1
            if s.get("pinned"):
                o["p"] = 1
            sents.append(o)
        data[w] = {"tier": tier, "sents": sents}
    return data


def build_llm(sel, data):
    """LLM 선택 결과를 도구 상태로 병합할 경량 구조로 변환.

    word -> {p:대표idx|None, k:[백업idx], d:보류bool, c:직접입력,
             cf:confidence, (fl:flags), (r:reason), (tg:primary_tag)}
    idx 는 0-based 로 data[w].sents 와 정렬됨(검증 완료).
    """
    out = {}
    for w, v in (sel or {}).items():
        if w not in data:
            continue
        pri = v.get("primary")
        p = pri.get("idx") if isinstance(pri, dict) and pri.get("idx") is not None else None
        k = [b.get("idx") for b in (v.get("backups") or [])
             if isinstance(b, dict) and b.get("idx") is not None]
        meta = v.get("_llm") or {}
        o = {"p": p, "k": k, "d": bool(v.get("defer")), "c": (v.get("custom") or ""),
             "cf": meta.get("confidence") or ""}
        fl = [x for x in (meta.get("flags") or []) if x]
        if fl:
            o["fl"] = fl
        if meta.get("reason"):
            o["r"] = meta["reason"]
        if meta.get("primary_tag"):
            o["tg"] = meta["primary_tag"]
        out[w] = o
    return out


def main():
    data_dir = os.path.join(ROOT, "data")
    docs_dir = os.path.join(ROOT, "docs")
    puzzles_file = env("CW_PUZZLES", "puzzles_raw.json")
    sent_file = env("CW_SENT", "word_sentences.json")
    review_dir = os.path.join(docs_dir, env("CW_REVIEW_DIR", "review"))
    os.makedirs(review_dir, exist_ok=True)

    hints_file = env("CW_HINTS", "hint_prefill.json")

    puzzles = json.load(open(os.path.join(data_dir, puzzles_file), encoding="utf-8"))
    ws = json.load(open(os.path.join(data_dir, sent_file), encoding="utf-8"))
    hp_path = os.path.join(data_dir, hints_file)
    llm_raw = {}
    if os.path.exists(hp_path):
        llm_raw = json.load(open(hp_path, encoding="utf-8")).get("selections", {})

    # 전체 240퍼즐에 배정된 단어 집합(퍼즐 인덱스 무관, 중복 제거).
    word_set = set()
    for p in puzzles:
        word_set.update(p.get("assign", {}).values())
    words = sorted(word_set)

    missing = [w for w in words if w not in ws]
    if missing:
        print(f"경고: 용례 레코드 없는 단어 {len(missing)}개(빈 예문으로 포함): {missing[:10]}")

    data = build_data(words, ws)
    llm = build_llm(llm_raw, data)
    n_sent = sum(len(v["sents"]) for v in data.values())
    weak_words = sum(1 for v in data.values() if any(s.get("w") for s in v["sents"]))
    themed = sum(1 for v in data.values() if v["tier"] != "general")
    llm_low = sum(1 for v in llm.values() if v.get("cf") == "low")
    llm_high = sum(1 for v in llm.values() if v.get("cf") == "high")
    print(f"단어 {len(words)}개 | 예문 {n_sent:,}개 | themed {themed} | weak 보유 단어 {weak_words}")
    print(f"LLM 병합 {len(llm)}개 (고신뢰 {llm_high} / 저신뢰 {llm_low}) ← {hints_file}")

    meta = {"scope": f"all-{len(puzzles)}-puzzles", "source": sent_file,
            "total": len(words),
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds")}

    def js(obj):
        # </ 를 <\/ 로 막아 </script> 조기 종료를 방지한다.
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    out = (SHELL
           .replace("__HR_DATA__", js(data))
           .replace("__HR_WORDS__", js(words))
           .replace("__HR_META__", js(meta))
           .replace("__HR_LLM__", js(llm))
           .replace("__HR_GEN__", html.escape(meta["generated_at"]))
           .replace("__HR_SRC__", html.escape(sent_file))
           .replace("__HR_TOTAL__", str(len(words))))

    path = os.path.join(review_dir, "hint_review.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)
    size_mb = os.path.getsize(path) / 1e6
    rel = os.path.relpath(path, ROOT)
    print(f"저장: {rel} ({size_mb:.1f} MB)")
    print(f"열기(권장): cd {os.path.relpath(ROOT, os.getcwd()) or '.'} && "
          f"python -m http.server 8000  ->  http://localhost:8000/{rel}")


# ---------------------------------------------------------------------------
# 단일 파일 셸: CSS + 데이터 자리(__HR_*__) + 앱 JS. f-string 아님(중괄호 그대로).
# ---------------------------------------------------------------------------
SHELL = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>힌트 검토 (단어별 예문 선택)</title>
<style>
:root{
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:-apple-system,Segoe UI,Roboto,'Noto Sans KR',sans-serif;
  --line:#e2e2e2; --ink:#1a1a1a; --mut:#888; --accent:#1a5fb4;
  --themed:#a51d2d; --ok:#2a8a3e; --okbg:#eef8f0; --defer:#b06a00; --deferbg:#fcf4e6;
}
*{box-sizing:border-box}
body{font-family:var(--sans);margin:0;color:var(--ink);line-height:1.4;background:#fff}
header{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--line);
  padding:8px 14px 6px}
.row1{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
h1{font-size:15px;margin:0;font-weight:700}
.sub{font-size:11px;color:var(--mut)}
#progress{font-size:12px;font-variant-numeric:tabular-nums}
.barwrap{flex:1;min-width:120px;height:7px;background:#eee;border-radius:4px;overflow:hidden}
#bar{height:100%;width:0;background:var(--ok);transition:width .2s}
.row2{display:flex;align-items:center;gap:8px;margin-top:6px;flex-wrap:wrap}
input[type=text],select{font-family:var(--sans);font-size:12px;padding:4px 6px;border:1px solid var(--line);border-radius:5px}
#search{min-width:160px}
button{font-family:var(--sans);font-size:12px;padding:4px 9px;border:1px solid var(--line);
  background:#fafafa;border-radius:5px;cursor:pointer}
button:hover{background:#f0f0f0}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
#saved,#status{font-size:11px;color:var(--mut)}
#status.err{color:#b00}
#azbar{display:flex;flex-wrap:wrap;gap:1px;margin-top:6px}
#azbar a{font-family:var(--mono);font-size:11px;color:var(--accent);text-decoration:none;
  padding:1px 5px;border:1px solid var(--line);border-radius:3px}
#azbar a:hover{background:#eef3fb}
.legend{font-size:11px;color:var(--mut);margin-top:6px}
.legend b{color:var(--ink)}
main{padding:6px 14px 120px;max-width:1100px}
h3.letter{font-family:var(--mono);font-size:13px;color:#fff;background:#333;
  padding:2px 8px;border-radius:4px;margin:18px 0 6px;position:sticky;top:96px;z-index:5;display:inline-block}
details.word{border:1px solid #eee;border-radius:5px;margin:3px 0;padding:2px 8px}
details.word.themed>summary .w{color:var(--themed)}
details.word.resolved{background:var(--okbg);border-color:#cfe8d4}
details.word.deferred{background:var(--deferbg);border-color:#f0e0c0}
details.word[open]{box-shadow:0 1px 4px rgba(0,0,0,.06)}
summary{cursor:pointer;font-size:13px;display:flex;align-items:baseline;gap:8px;list-style:none}
summary::-webkit-details-marker{display:none}
summary .w{font-family:var(--mono);font-weight:700;letter-spacing:.4px}
summary .tier{font-size:11px;color:var(--mut)}
summary .cnt{font-size:11px;color:#aaa;font-variant-numeric:tabular-nums}
summary .llm{font-size:9px;padding:1px 5px;border-radius:3px;font-weight:700;letter-spacing:.3px;white-space:nowrap}
summary .llm.high{background:var(--okbg);color:var(--ok)}
summary .llm.low{background:#fdecea;color:#c0392b}
summary .chip{margin-left:auto;font-size:12px;color:var(--ok);font-variant-numeric:tabular-nums;white-space:nowrap}
.llmnote{font-size:11px;color:var(--mut);padding:3px 4px 5px;border-bottom:1px dashed #eee;margin-bottom:3px}
.llmnote .cf{font-weight:700}
.llmnote .cf.low{color:#c0392b} .llmnote .cf.high{color:var(--ok)}
.llmnote .fl{color:#c0392b;font-weight:700}
.llmnote .tg{font-family:var(--mono)}
.body{padding:6px 0 8px}
.srow{display:grid;grid-template-columns:24px 22px 36px 1fr auto;align-items:start;
  gap:7px;padding:3px 4px;border-top:1px solid #f3f3f3;font-size:13px}
.srow.isprimary{background:#fff7e6;border-radius:4px}
.star{padding:0;border:none;background:none;font-size:15px;line-height:1;cursor:pointer;color:#d8a400}
.star:hover{transform:scale(1.15)}
.keep{margin-top:2px;cursor:pointer}
.sim{font-family:var(--mono);font-size:11px;color:#aaa;text-align:right;margin-top:1px}
.txt{font-size:13px}
.txt mark{background:#ffe08a;padding:0 1px;border-radius:2px}
.badges{display:flex;gap:4px;align-items:center}
.b{font-size:9px;padding:1px 4px;border-radius:3px;white-space:nowrap}
.b.weak{background:#fde7e7;color:#b00}
.b.pin{background:#e7eefd;color:#1a5fb4}
.src{font-size:11px;color:var(--accent);text-decoration:none;white-space:nowrap}
.src:hover{text-decoration:underline}
.nosent{font-size:12px;color:#b00;padding:4px}
.foot{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:8px;padding:6px 4px 2px;border-top:1px dashed #e5e5e5}
.foot label{font-size:12px}
.foot .custom{min-width:280px}
.foot .clr{font-size:11px;padding:2px 7px}
.defer{display:flex;align-items:center;gap:4px}
kbd{font-family:var(--mono);font-size:11px;background:#f3f3f3;border:1px solid #ddd;border-radius:3px;padding:0 3px}
</style>
</head>
<body>
<header>
  <div class="row1">
    <h1>힌트 검토</h1>
    <span class="sub">단어 __HR_TOTAL__개 · 출처 __HR_SRC__ · 생성 __HR_GEN__</span>
    <span id="progress"></span>
    <div class="barwrap"><div id="bar"></div></div>
  </div>
  <div class="row2">
    <input type="text" id="search" placeholder="단어 검색…">
    <select id="filter">
      <option value="all">전체</option>
      <option value="untouched">미검토</option>
      <option value="resolved">결정됨(대표/직접)</option>
      <option value="primary">대표 있음</option>
      <option value="deferred">보류</option>
      <option value="custom">직접입력 있음</option>
      <option value="themed">테마어만</option>
      <option value="weak">weak 예문 포함</option>
      <option value="llm_low">LLM 저신뢰(검토 필요)</option>
      <option value="llm_high">LLM 고신뢰</option>
      <option value="llm_flagged">LLM 플래그</option>
    </select>
    <span id="shown" class="sub"></span>
    <button id="next">미검토로 이동</button>
    <span style="flex:1"></span>
    <span id="saved">자동저장 준비</span>
    <button id="mergellm">LLM 재병합</button>
    <button id="export" class="primary">JSON 내보내기</button>
    <button id="importbtn">불러오기</button>
    <input type="file" id="importfile" accept="application/json,.json" style="display:none">
    <span id="status"></span>
  </div>
  <div id="azbar"></div>
  <div class="legend">
    <b>★</b> 대표 힌트(1개·클로즈 정답 단어가 <mark>강조</mark>됨) ·
    <b>체크</b> 백업 후보(여러 개) ·
    <b>보류</b> 나중에 다시 ·
    <b>직접 입력</b> 적합한 예문이 없을 때. 모든 변경은 자동 저장되며, 완료 후 <b>JSON 내보내기</b>로 data/로 옮깁니다.
    <br><b>LLM✓/LLM⚠</b> 1차 선택의 고신뢰/저신뢰. 첫 실행 시 자동 병합됩니다. 필터 <b>LLM 저신뢰</b>로 검토 대상에 집중하세요.
  </div>
</header>
<main><div id="list"></div></main>

<script>
const DATA = __HR_DATA__;
const WORDS = __HR_WORDS__;
const META = __HR_META__;
const LLM = __HR_LLM__;     // word -> {p,k,d,c,cf,(fl),(r),(tg)} LLM 1차 선택
const LS_KEY = "namedrop_hint_review_v1";
const SEED_KEY = "namedrop_hint_llm_seeded_v1";   // 최초 1회 자동 병합 여부 표식

let state = {};            // {word:{primary:int|null, keep:[int], defer:bool, custom:str}}
let saveTimer = null, statusTimer = null;
let curTerm = "", curMode = "all";

/* ---------- 저장/로드 ---------- */
function loadState(){
  try{ const raw = localStorage.getItem(LS_KEY); if(raw) state = JSON.parse(raw) || {}; }
  catch(e){ console.warn("localStorage 로드 실패", e); state = {}; }
}
function scheduleSave(){ clearTimeout(saveTimer); saveTimer = setTimeout(doSave, 350); }
function doSave(){
  try{ localStorage.setItem(LS_KEY, JSON.stringify(state));
       const d = new Date(); document.getElementById("saved").textContent = "자동저장됨 " + d.toLocaleTimeString(); }
  catch(e){ setStatus("저장 실패: " + e.message, true); }
}
function setStatus(msg, err){
  const el = document.getElementById("status"); el.textContent = msg; el.className = err ? "err" : "";
  clearTimeout(statusTimer); statusTimer = setTimeout(()=>{ el.textContent=""; }, 4000);
}

/* ---------- 상태 헬퍼 ---------- */
function ws(w){ if(!state[w]) state[w] = {primary:null, keep:[], defer:false, custom:""}; return state[w]; }
function touched(s){ return !!(s && (s.primary!=null || (s.keep&&s.keep.length) || s.defer || (s.custom&&s.custom.trim()))); }
function resolved(s){ return !!(s && (s.primary!=null || (s.custom&&s.custom.trim()))); }
function letterOf(w){ const c = w[0].toUpperCase(); return (c>='A'&&c<='Z') ? c : '#'; }

/* ---------- 렌더 ---------- */
function escHtml(s){ return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function highlight(text, word){
  const safe = escHtml(text);
  try{
    const re = new RegExp("\\b(" + word.replace(/[.*+?^${}()|[\]\\]/g,"\\$&") + ")\\b","gi");
    return safe.replace(re, "<mark>$1</mark>");
  }catch(e){ return safe; }
}
function hostOf(u){ try{ return new URL(u).hostname.replace(/^www\./,""); }catch(e){ return u; } }

function initList(){
  const list = document.getElementById("list");
  const frag = document.createDocumentFragment();
  let cur = null;
  for(const word of WORDS){
    const L = letterOf(word);
    if(L !== cur){ cur = L; const h = document.createElement("h3"); h.className="letter"; h.id="L-"+L; h.textContent=L; frag.appendChild(h); }
    frag.appendChild(buildWordEl(word));
  }
  list.appendChild(frag);
}

function buildWordEl(word){
  const d = DATA[word];
  const det = document.createElement("details");
  det.className = "word";
  if(d.tier && d.tier !== "general") det.classList.add("themed");
  det.dataset.word = word;
  const sum = document.createElement("summary");
  const w = document.createElement("span"); w.className="w"; w.textContent = word;
  const tier = document.createElement("span"); tier.className="tier";
  tier.textContent = (d.tier && d.tier!=="general") ? "["+d.tier+"]" : "";
  const cnt = document.createElement("span"); cnt.className="cnt"; cnt.textContent = d.sents.length + " ex.";
  const chip = document.createElement("span"); chip.className="chip";
  const llm = LLM[word];
  if(llm && llm.cf){
    const lb = document.createElement("span"); lb.className = "llm " + llm.cf;
    lb.textContent = (llm.cf==="low") ? "LLM⚠" : "LLM✓";
    lb.title = (llm.r||"") + (llm.fl&&llm.fl.length ? (" ["+llm.fl.join(", ")+"]") : "");
    sum.append(w, tier, lb, cnt, chip);
  } else {
    sum.append(w, tier, cnt, chip);
  }
  det.appendChild(sum);
  det.addEventListener("toggle", ()=>{ if(det.open && !det._built){ buildBody(det, word); det._built = true; } });
  updateChip(det, word);
  return det;
}

function buildBody(det, word){
  const d = DATA[word], s = ws(word);
  const body = document.createElement("div"); body.className="body";
  const llm = LLM[word];
  if(llm && llm.cf){
    const note = document.createElement("div"); note.className="llmnote";
    let h = "LLM <span class='cf "+llm.cf+"'>"+llm.cf+"</span>";
    if(llm.tg) h += " · 난이도 <span class='tg'>"+escHtml(llm.tg)+"</span>";
    if(llm.fl && llm.fl.length) h += " · <span class='fl'>flags: "+escHtml(llm.fl.join(", "))+"</span>";
    if(llm.r) h += " · " + escHtml(llm.r);
    note.innerHTML = h; body.appendChild(note);
  }
  if(!d.sents.length){
    const e = document.createElement("div"); e.className="nosent"; e.textContent="코퍼스 용례 없음(직접 입력 사용).";
    body.appendChild(e);
  }
  d.sents.forEach((sent, i)=>{
    const row = document.createElement("div"); row.className="srow"; row.dataset.idx=i;
    const star = document.createElement("button"); star.type="button"; star.className="star";
    star.title="대표 힌트로 지정/해제"; star.textContent = (s.primary===i) ? "★" : "☆";
    star.addEventListener("click", ()=> togglePrimary(det, word, i));
    const keep = document.createElement("input"); keep.type="checkbox"; keep.className="keep";
    keep.title="백업 후보로 보관"; keep.checked = s.keep.includes(i);
    keep.addEventListener("change", ()=> toggleKeep(det, word, i, keep.checked));
    const sim = document.createElement("span"); sim.className="sim"; sim.textContent = sent.s.toFixed(2);
    const txt = document.createElement("span"); txt.className="txt"; txt.innerHTML = highlight(sent.t, word);
    const badges = document.createElement("span"); badges.className="badges";
    if(sent.w){ const b=document.createElement("span"); b.className="b weak"; b.textContent="weak"; badges.appendChild(b); }
    if(sent.p){ const b=document.createElement("span"); b.className="b pin"; b.textContent="pinned"; badges.appendChild(b); }
    if(sent.u){ const a=document.createElement("a"); a.className="src"; a.href=sent.u; a.target="_blank"; a.rel="noopener"; a.textContent="["+hostOf(sent.u)+"]"; badges.appendChild(a); }
    row.append(star, keep, sim, txt, badges);
    if(s.primary===i) row.classList.add("isprimary");
    body.appendChild(row);
  });
  const foot = document.createElement("div"); foot.className="foot";
  const deferL = document.createElement("label"); deferL.className="defer";
  const deferCb = document.createElement("input"); deferCb.type="checkbox"; deferCb.checked=!!s.defer;
  deferCb.addEventListener("change", ()=>{ ws(word).defer=deferCb.checked; afterChange(det, word); });
  deferL.append(deferCb, document.createTextNode(" 보류"));
  const clr = document.createElement("button"); clr.type="button"; clr.className="clr"; clr.textContent="대표 해제";
  clr.addEventListener("click", ()=>{ ws(word).primary=null; rebuildStars(det, word); afterChange(det, word); });
  const customL = document.createElement("label"); customL.textContent="직접 입력: ";
  const custom = document.createElement("input"); custom.type="text"; custom.className="custom"; custom.value=s.custom||"";
  custom.placeholder="적합한 예문이 없을 때 힌트 직접 작성";
  custom.addEventListener("input", ()=>{ ws(word).custom=custom.value; afterChange(det, word); });
  customL.appendChild(custom);
  foot.append(deferL, clr, customL);
  body.appendChild(foot);
  det.appendChild(body);
}

/* ---------- 변경 핸들러 ---------- */
function togglePrimary(det, word, i){
  const s = ws(word);
  if(s.primary===i){ s.primary=null; }
  else { s.primary=i; if(!s.keep.includes(i)) s.keep.push(i); }
  rebuildStars(det, word); afterChange(det, word);
}
function toggleKeep(det, word, i, on){
  const s = ws(word); const k = s.keep.indexOf(i);
  if(on && k<0) s.keep.push(i);
  if(!on && k>=0) s.keep.splice(k,1);
  if(!on && s.primary===i) s.primary=null;   // 대표의 보관을 풀면 대표도 해제
  rebuildStars(det, word); afterChange(det, word);
}
function rebuildStars(det, word){
  if(!det._built) return;
  const s = ws(word);
  det.querySelectorAll(".srow").forEach(row=>{
    const i = +row.dataset.idx;
    row.querySelector(".star").textContent = (s.primary===i) ? "★" : "☆";
    row.querySelector(".keep").checked = s.keep.includes(i);
    row.classList.toggle("isprimary", s.primary===i);
  });
}
function afterChange(det, word){
  if(state[word] && !touched(state[word])) delete state[word];   // 기본값이면 비워 저장 최소화
  updateChip(det, word); scheduleSave(); updateProgress();
  det.style.display = passFilter(word) ? "" : "none";
}
function updateChip(det, word){
  const s = state[word]; const chip = det.querySelector(".chip"); const parts=[];
  if(s){
    if(s.primary!=null) parts.push("★");
    const bk = s.keep ? s.keep.filter(i=>i!==s.primary).length : 0;
    if(bk) parts.push("+"+bk);
    if(s.custom && s.custom.trim()) parts.push("✎");
    if(s.defer) parts.push("⏸");
  }
  chip.textContent = parts.join(" ");
  det.classList.toggle("resolved", resolved(s));
  det.classList.toggle("deferred", !!(s && s.defer));
}

/* ---------- 진행/필터 ---------- */
function updateProgress(){
  let res=0, dfr=0, tch=0;
  for(const w of WORDS){ const s=state[w]; if(resolved(s))res++; if(s&&s.defer)dfr++; if(touched(s))tch++; }
  document.getElementById("progress").textContent = `결정 ${res} / ${WORDS.length} · 보류 ${dfr} · 미검토 ${WORDS.length-tch}`;
  document.getElementById("bar").style.width = (res/WORDS.length*100).toFixed(1) + "%";
}
function passFilter(word){
  if(curTerm && !word.includes(curTerm)) return false;
  const s = state[word], d = DATA[word];
  switch(curMode){
    case "untouched": return !touched(s);
    case "resolved":  return resolved(s);
    case "primary":   return !!(s && s.primary!=null);
    case "deferred":  return !!(s && s.defer);
    case "custom":    return !!(s && s.custom && s.custom.trim());
    case "themed":    return d.tier && d.tier!=="general";
    case "weak":      return d.sents.some(x=>x.w);
    case "llm_low":     return !!(LLM[word] && LLM[word].cf==="low");
    case "llm_high":    return !!(LLM[word] && LLM[word].cf==="high");
    case "llm_flagged": return !!(LLM[word] && LLM[word].fl && LLM[word].fl.length);
    default:          return true;
  }
}
function applyFilter(){
  curTerm = document.getElementById("search").value.trim().toLowerCase();
  curMode = document.getElementById("filter").value;
  let shown=0;
  document.querySelectorAll("details.word").forEach(det=>{
    const ok = passFilter(det.dataset.word); det.style.display = ok ? "" : "none"; if(ok) shown++;
  });
  document.querySelectorAll("h3.letter").forEach(h=>{
    let n=h.nextElementSibling, any=false;
    while(n && n.tagName!=="H3"){ if(n.tagName==="DETAILS" && n.style.display!=="none"){ any=true; break; } n=n.nextElementSibling; }
    h.style.display = any ? "" : "none";
  });
  document.getElementById("shown").textContent = "표시 " + shown;
}
function jumpNext(){
  const dets = Array.from(document.querySelectorAll("details.word")).filter(d=>d.style.display!=="none");
  const y = window.scrollY; let below=null, first=null;
  for(const d of dets){ if(!touched(state[d.dataset.word])){ if(!first) first=d; if(!below && d.offsetTop > y+10) below=d; } }
  const t = below || first;
  if(t){ t.open=true; t.scrollIntoView({behavior:"smooth", block:"center"}); }
  else setStatus("미검토 단어 없음");
}

/* ---------- LLM 1차 선택 병합 ---------- */
// onlyUntouched=true 면 사용자가 아직 손대지 않은 단어에만 채운다(기존 작업 보존).
function applyLLM(onlyUntouched){
  let n=0;
  for(const w in LLM){
    if(!DATA[w]) continue;
    if(onlyUntouched && touched(state[w])) continue;
    const v = LLM[w], s = ws(w);
    s.primary = (v.p!=null) ? v.p : null;
    s.keep = [];
    if(s.primary!=null) s.keep.push(s.primary);
    (v.k||[]).forEach(i=>{ if(i!=null && !s.keep.includes(i)) s.keep.push(i); });
    s.custom = (v.c||"").trim();
    s.defer = !!v.d;
    if(!touched(s)) delete state[w];
    n++;
  }
  return n;
}
function mergeLLM(){
  if(!confirm("현재 작업 상태를 LLM 1차 선택으로 전부 덮어씁니다. 계속할까요?")) return;
  const n = applyLLM(false); doSave(); refreshAll();
  setStatus("LLM 재병합(전체 덮어쓰기): "+n+" 단어");
}

/* ---------- 내보내기/불러오기 ---------- */
function ts(){ const d=new Date(), p=n=>String(n).padStart(2,"0");
  return d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+"_"+p(d.getHours())+p(d.getMinutes())+p(d.getSeconds()); }
function exportJSON(){
  const sel = {}; let res=0, dfr=0;
  for(const w of WORDS){
    const s = state[w]; if(!touched(s)) continue;
    const d = DATA[w]; const o = {};
    if(s.primary!=null){ const p=d.sents[s.primary]; o.primary={idx:s.primary, sim:p.s, text:p.t, url:p.u}; }
    else o.primary=null;
    o.backups = (s.keep||[]).filter(i=>i!==s.primary).sort((a,b)=>a-b)
      .map(i=>{ const x=d.sents[i]; return {idx:i, sim:x.s, text:x.t, url:x.u}; });
    o.custom = (s.custom||"").trim();
    o.defer = !!s.defer;
    sel[w] = o; if(resolved(s)) res++; if(s.defer) dfr++;
  }
  const out = { _meta:{ tool:"hint_review", version:1, scope:META.scope, source:META.source,
    total_words:WORDS.length, resolved:res, deferred:dfr, exported_at:new Date().toISOString() }, selections: sel };
  const blob = new Blob([JSON.stringify(out, null, 1)], {type:"application/json"});
  const a = document.createElement("a"); a.href=URL.createObjectURL(blob); a.download="hint_review_"+ts()+".json";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href), 2000);
  setStatus("내보냄: "+res+" 결정 / "+Object.keys(sel).length+" 단어");
}
function importJSON(file){
  const r = new FileReader();
  r.onload = ()=>{
    try{
      const obj = JSON.parse(r.result);
      const sel = obj.selections || obj.words || obj;
      let n=0;
      for(const w in sel){
        if(!DATA[w]) continue;
        const v = sel[w], s = ws(w);
        if(v.primary && typeof v.primary==="object") s.primary = (v.primary.idx!=null)?v.primary.idx:null;
        else if(typeof v.primary==="number") s.primary = v.primary;
        else s.primary = null;
        s.keep = [];
        if(s.primary!=null) s.keep.push(s.primary);
        (v.backups||[]).forEach(b=>{ const i=(typeof b==="object")?b.idx:b; if(i!=null && !s.keep.includes(i)) s.keep.push(i); });
        if(Array.isArray(v.keep)) v.keep.forEach(i=>{ if(!s.keep.includes(i)) s.keep.push(i); });
        s.custom = (v.custom||"").trim();
        s.defer = !!v.defer;
        if(!touched(s)) delete state[w];
        n++;
      }
      doSave(); refreshAll(); setStatus("불러옴: "+n+" 단어");
    }catch(e){ setStatus("불러오기 실패: "+e.message, true); }
  };
  r.readAsText(file);
}
function refreshAll(){
  document.querySelectorAll("details.word").forEach(det=>{
    const w = det.dataset.word; updateChip(det, w);
    if(det._built){
      rebuildStars(det, w);
      const c = det.querySelector(".custom"); if(c) c.value = (state[w]&&state[w].custom) || "";
      const df = det.querySelector(".defer input"); if(df) df.checked = !!(state[w]&&state[w].defer);
    }
  });
  updateProgress(); applyFilter();
}

/* ---------- 부팅 ---------- */
function buildAZ(){
  const seen={}, letters=[];
  for(const w of WORDS){ const L=letterOf(w); if(!seen[L]){ seen[L]=1; letters.push(L); } }
  const bar = document.getElementById("azbar");
  letters.forEach(L=>{ const a=document.createElement("a"); a.textContent=L; a.href="#L-"+L; bar.appendChild(a); });
}
function debounce(fn, ms){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a), ms); }; }

document.addEventListener("DOMContentLoaded", ()=>{
  loadState();
  let seeded = 0;
  if(!localStorage.getItem(SEED_KEY)){              // 최초 1회만: 미검토 단어에 LLM 채움(기존 작업 보존)
    seeded = applyLLM(true);
    try{ localStorage.setItem(SEED_KEY, META.generated_at || "1"); }catch(e){}
    doSave();
  }
  initList(); buildAZ(); updateProgress(); applyFilter();
  document.getElementById("search").addEventListener("input", debounce(applyFilter, 180));
  document.getElementById("filter").addEventListener("change", applyFilter);
  document.getElementById("next").addEventListener("click", jumpNext);
  document.getElementById("mergellm").addEventListener("click", mergeLLM);
  document.getElementById("export").addEventListener("click", exportJSON);
  document.getElementById("importbtn").addEventListener("click", ()=>document.getElementById("importfile").click());
  document.getElementById("importfile").addEventListener("change", e=>{ if(e.target.files[0]) importJSON(e.target.files[0]); e.target.value=""; });
  window.addEventListener("beforeunload", doSave);
  document.getElementById("saved").textContent = seeded ? ("LLM 결과 "+seeded+"개 병합됨") :
    (Object.keys(state).length ? "이전 작업 복원됨" : "자동저장 준비");
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
