#!/usr/bin/env python3
"""4단계(부분): 퍼즐에 쓰인 모든 단어의 코퍼스 용례 문장 채굴 + 의미유사도 랭킹.

목적: 어휘 필터링 검토용 문서 생성(+ 힌트 문장 후보). 각 단어마다 코퍼스에서 그 단어가
실제 쓰인 문장을 모아, 단어 임베딩과의 코사인 유사도 순으로 최대 N개를 남긴다.
각 문장에는 출처 문서의 원본 url을 함께 기록한다(검토 UI 링크용).

힌트 후보 품질 필터(2026-06-12 퍼즐 검토 결과 도입, 사용자 결정):
 - URL/이메일 포함 문장 제외 (smith-stewart.com 류 가짜 용례 차단)
 - 비영어 문장 제외 (langdetect. 이탈리아어 una sorta di, 포르투갈어 fez 류 차단)
 - OCR 행분리 파편 용례 제외 (meth ods, jus tice 류: 인접 비단어 토큰과 결합하면
   더 흔한 진짜 단어가 되는 경우)
 - 이름 tier 가 아닌 단어는 "문중 소문자 단독 토큰" 용례를 우선(good), 그 외
   (문두/대문자/하이픈 결합 x-ray 류)는 weak 으로 별도 상한(MAX_WEAK) 수집 후 후순위
 - 의미 고정 핀(data/sense_pins.json): led=LED, cis=cisgender, topos(소문자),
   matt(소문자), tom=floor tom, cel(소문자) 등 사용자 지정 의미의 용례만 수집

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
import json, os, re, sys, glob, time, collections, unicodedata, multiprocessing as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("HF_HOME", "/home/choiharam/storage/models/huggingface")
os.environ.setdefault("HF_HUB_OFFLINE", "1")          # 캐시 우선(오프라인)
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

TOKEN_RE = re.compile(r"[a-z]+")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MAX_KEEP = 10          # 단어당 문서에 남길 문장 수
MAX_CAND = 60          # 단어당 임베딩 후보 상한(good: 소문자 문중 용례)
MAX_WEAK = 20          # weak 후보 상한(문두/대문자/하이픈 결합 용례, 후순위)
MIN_SENT_LEN = 25      # 문장 최소 길이(문자)
MAX_SENT_LEN = 320     # 문장 최대 길이(문자)

from wordfreq import zipf_frequency as _zipf            # noqa: E402
try:
    from langdetect import detect_langs as _detect_langs, DetectorFactory
    DetectorFactory.seed = 0                            # 재현성
except ImportError:
    _detect_langs = None

# URL/이메일 흔적: 이런 문장은 힌트 후보에서 통째로 제외
URLISH_RE = re.compile(
    r"https?://|www\.|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"|\b[A-Za-z0-9-]+\.(?:com|org|net|edu|gov|info|io|co|uk|de|fr|nl|kr|jp"
    r"|it|es|ch|at|be|se|html?|php|aspx?)\b", re.I)
_CASE_TOKEN_RE = re.compile(r"[A-Za-z]+")


def _is_english(sent):
    """문장 단위 언어 판별. 코퍼스에 통째로 섞인 비영어 문서의 문장을 차단한다.
    판정 불가 문장은 통과(과차단 방지)."""
    if _detect_langs is None:
        return True
    try:
        langs = _detect_langs(sent)
    except Exception:
        return True
    if not langs or langs[0].lang == "en":
        return True
    return any(l.lang == "en" and l.prob >= 0.4 for l in langs)


def _ocr_fragment_only(w, toks):
    """w의 모든 등장이 OCR 행분리 파편인지 (예: meth ods, jus tice, cel lular).
    파편 판정: 인접 토큰이 비단어(zipf<2)이고, 결합형이 w보다 흔한 진짜 단어."""
    hit = False
    zw = _zipf(w, "en")
    for i, t in enumerate(toks):
        if t != w:
            continue
        hit = True
        frag = False
        for adj, comb in ((toks[i - 1] if i > 0 else None, lambda a: a + w),
                          (toks[i + 1] if i + 1 < len(toks) else None, lambda a: w + a)):
            if adj and _zipf(adj, "en") < 2.0:
                zc = _zipf(comb(adj), "en")
                if zc >= 3.0 and zc > zw:
                    frag = True
                    break
        if not frag:
            return False
    return hit


_SOFT_HYPH = "­"


def _frag_ctx(sent, start, end):
    """행분리 하이픈 절단 파편 문맥 검사 (2026-06-12 cess/rial/sion/sup 건).
    파편: 글자/숫자에 붙은 하이픈+공백 뒤 토큰(mate- rial 의 rial, 500- acre),
    토큰+하이픈+공백(pro- cess 의 pro), 소프트하이픈 인접(어느 쪽이든).
    붙은 하이픈 복합어(x-ray, cast-offs)는 파편이 아니라 기존 weak 취급 유지."""
    k = start - 1
    sp = False
    while k >= 0 and sent[k].isspace():
        sp, k = True, k - 1
    if k >= 0 and sent[k] == _SOFT_HYPH:
        return True
    if sp and k >= 1 and sent[k] == "-" and sent[k - 1].isalnum():
        return True
    if end < len(sent):
        c = sent[end]
        if c == _SOFT_HYPH:
            return True
        if c == "-" and (end + 1 == len(sent) or sent[end + 1].isspace()):
            return True
    return False


def _hyph_fragment_only(sent, w):
    """w의 모든 등장(케이스 무시)이 하이픈 절단 파편 문맥이면 True."""
    hit = False
    for m in _CASE_TOKEN_RE.finditer(sent):
        if m.group(0).lower() != w:
            continue
        hit = True
        if not _frag_ctx(sent, m.start(), m.end()):
            return False
    return hit


def _case_good(sent, w):
    """원문에서 w가 '문중 소문자 단독 토큰'으로 한 번이라도 등장하면 True.
    문두/대문자/하이픈 결합(x-ray 류)/행분리 파편 용례만 있으면 False(weak)."""
    for m in _CASE_TOKEN_RE.finditer(sent):
        if m.group(0) != w or m.start() == 0:
            continue
        post = sent[m.end()] if m.end() < len(sent) else ""
        if sent[m.start() - 1] == "-" or post == "-":
            continue
        if _frag_ctx(sent, m.start(), m.end()):
            continue
        return True
    return False


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize(text):
    # 악센트 제거 후 소문자·영문자만 (São Paulo -> "sao paulo" 로 다어절 매칭 가능)
    de = "".join(c for c in unicodedata.normalize("NFKD", text)
                 if not unicodedata.combining(c))
    return re.sub(r"[^a-z]+", " ", de.lower())


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
_LOWPREF = None     # 소문자 문중 용례 우선 대상(비이름 tier 단일토큰) (set)
_PINS = None        # 의미 고정 핀 {word: (require_pat|None, exclude_pat|None)}


def _scan_chunk(files):
    """페이지 청크를 스캔해 단어별 후보 (문장,url,good) 수집.
    good=True 는 우선 후보(소문자 문중 용례/핀 일치/이름 tier), False 는 weak.
    워커 내 상한: good MAX_CAND, weak MAX_WEAK."""
    cand = collections.defaultdict(list)
    seen = collections.defaultdict(set)
    ngood = collections.Counter()
    nweak = collections.Counter()
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
                toks = TOKEN_RE.findall(norm)
                matched = set(toks) & _SINGLE
                mw_hit = set()
                if _MWTOK:
                    for tok, pat in _MWTOK:
                        if pat.search(norm):
                            mw_hit.add(tok)
                live = [w for w in (matched | mw_hit)
                        if (ngood[w] < MAX_CAND or nweak[w] < MAX_WEAK)
                        and norm not in seen[w]]
                if not live:
                    continue
                # 문장 단위 품질 필터(후보가 있을 때만 비용 지불)
                if URLISH_RE.search(sent) or not _is_english(sent):
                    continue
                for w in live:
                    if w in mw_hit:
                        good = True                  # 다어절 이름: 케이스 분류 비적용
                    elif w in _PINS:
                        req, exc = _PINS[w]
                        if req and not req.search(sent):
                            continue                 # 지정 의미의 용례만 수집
                        if exc and exc.search(sent):
                            continue                 # 배제 문맥(요일 표기 등) 제외
                        if (_ocr_fragment_only(w, toks)
                                or _hyph_fragment_only(sent, w)):
                            continue
                        # require 없는 핀(배제 전용)은 케이스 선호를 그대로 적용
                        good = True if req else (
                            _case_good(sent, w) if w in _LOWPREF else True)
                    elif w in _LOWPREF:
                        if (_ocr_fragment_only(w, toks)
                                or _hyph_fragment_only(sent, w)):
                            continue
                        good = _case_good(sent, w)
                    else:
                        good = True                  # 이름 tier: 대문자 용례가 정상
                    if good:
                        if ngood[w] >= MAX_CAND:
                            continue
                        ngood[w] += 1
                    else:
                        if nweak[w] >= MAX_WEAK:
                            continue
                        nweak[w] += 1
                    seen[w].add(norm)
                    cand[w].append((sent, url, good))
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
    # 복원 이름(결합형): pool 레코드의 parts 로 다어절 패턴 생성 (andywarhol -> andy\s+warhol)
    n_recovered = 0
    for t in target:
        rec = pool.get(t)
        if rec and rec.get("parts") and t not in mw_pat:
            mw_pat[t] = re.compile(r"\b" + r"\s+".join(re.escape(p) for p in rec["parts"]) + r"\b")
            n_recovered += 1
    mw_tokens = list(mw_pat.items())
    single_targets = {t for t in target if t not in mw_pat}
    print(f"  단일토큰 {len(single_targets):,} / 멀티워드 {len(mw_pat)} (복원이름 {n_recovered})", flush=True)

    # 소문자 문중 용례 우선 대상: 이름 tier 가 아닌 단일토큰.
    # 사용자 기준(2026-06-12): 힌트는 코퍼스의 보통명사/동사 용례로 판단하므로
    # 고유명사/약어 표기 용례는 weak 으로 후순위. 이름 tier 는 대문자가 정상이라 제외.
    lowpref = {t for t in single_targets
               if (pool.get(t) or {}).get("tier") != "name"}
    pins = {}
    sp_path = os.path.join(data_dir, "sense_pins.json")
    if os.path.exists(sp_path):
        raw_pins = json.load(open(sp_path, encoding="utf-8"))
        pins = {w: (re.compile(v["require"]) if v.get("require") else None,
                    re.compile(v["exclude"]) if v.get("exclude") else None)
                for w, v in raw_pins.items() if w in target}
        print(f"  의미 고정 핀 {len(pins)}개 적용: {sorted(pins)}", flush=True)

    # --- 코퍼스 스캔: 페이지 단위 CPU 병렬(fork COW로 타깃/패턴 공유) ---
    global _SINGLE, _MWTOK, _SEG, _LOWPREF, _PINS
    _SINGLE, _MWTOK, _SEG = single_targets, mw_tokens, include_seg
    _LOWPREF, _PINS = lowpref, pins
    # wordfreq/langdetect 데이터를 부모에서 미리 로드(fork 공유, 워커 중복 로드 방지)
    _zipf("the", "en")
    _is_english("This is a warm-up sentence for the language detector.")
    t0 = time.time()
    files = [f for _d, f in iter_pages(corpus_root, include_dirs)]
    n_pages = len(files)
    workers = max(1, min(os.cpu_count() - 2, n_pages))
    # 워커당 여러 청크로 쪼개 로드밸런싱(꼬리 페이지 편중 방지)
    n_chunks = max(workers, workers * 6)
    sz = (len(files) + n_chunks - 1) // max(1, n_chunks)
    chunks = [files[i:i + sz] for i in range(0, len(files), sz)]
    print(f"  코퍼스 {n_pages:,} pages | 워커 {workers} | 청크 {len(chunks)}", flush=True)

    cand = collections.defaultdict(list)   # word -> [(sentence, url, good)]
    seen = collections.defaultdict(set)    # word -> {정규화 문장} (전역 중복 방지)
    ngood = collections.Counter()
    nweak = collections.Counter()
    ctx = mp.get_context("fork")
    done = 0
    with ctx.Pool(workers) as pp:          # initargs 없음 → 무거운 전역은 fork로 공유
        for part in pp.imap_unordered(_scan_chunk, chunks):
            for w, lst in part.items():
                cw, sw = cand[w], seen[w]
                for sent, url, good in lst:
                    if good and ngood[w] >= MAX_CAND:
                        continue
                    if not good and nweak[w] >= MAX_WEAK:
                        continue
                    norm = normalize(sent)
                    if norm in sw:
                        continue
                    sw.add(norm)
                    cw.append((sent, url, good))
                    if good:
                        ngood[w] += 1
                    else:
                        nweak[w] += 1
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

    all_sents = sorted({s for ss in cand.values() for (s, _u, _g) in ss})
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

    # 사용자 keep-list: 큐레이션된 용례 문장을 힌트 1순위로 고정 (to-keep.md 유래).
    keep_pins = {}
    kp_path = os.path.join(data_dir, "keep_words.json")
    if os.path.exists(kp_path):
        keep_pins = json.load(open(kp_path, encoding="utf-8"))
        print(f"  keep-list 고정 힌트 {len(keep_pins)}개 로드", flush=True)

    # --- 단어별 top-N 랭킹 (url 보존) ---
    # 정렬 키: good(소문자 문중 용례/핀 일치) 우선, 그 안에서 유사도 내림차순.
    # weak 후보는 good 이 부족할 때만 뒤에 붙는다(weak=True 표시).
    result = {}
    for w in sorted(target):
        rec = pool.get(w, {})
        sents = cand.get(w, [])      # [(text, url, good)]
        ranked = []
        if sents:
            idxs = [sent_idx[s] for (s, _u, _g) in sents]
            sims = S[idxs] @ wemb[w]
            order = sorted(range(len(sents)),
                           key=lambda j: (not sents[j][2], -sims[j]))[:MAX_KEEP]
            for j in order:
                item = {"text": sents[j][0], "url": sents[j][1],
                        "sim": round(float(sims[j]), 4)}
                if not sents[j][2]:
                    item["weak"] = True
                ranked.append(item)
        if w in keep_pins:
            pin = keep_pins[w]
            pin_norm = normalize(pin["sentence"])
            ranked = [s for s in ranked if normalize(s["text"]) != pin_norm]
            ranked.insert(0, {"text": pin["sentence"], "url": pin.get("url") or "",
                              "sim": 1.0, "pinned": True})
            ranked = ranked[:MAX_KEEP]
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
            tag = " `[weak]`" if s.get("weak") else ""
            lines.append(f"- ({s['sim']:.2f}){tag} {s['text']}")
        lines.append("")
    with open(os.path.join(docs_dir, "word_review.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"저장: docs/word_review.md", flush=True)


if __name__ == "__main__":
    main()
