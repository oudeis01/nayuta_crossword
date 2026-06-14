#!/usr/bin/env python3
"""분석: 토큰화에서 분절돼 '노이즈 조각'으로 보이는 토큰들 중,
   well-known 다어절 고유명사라서 결합형(예: São Paulo -> saopaulo)으로
   복원하면 답안으로 허용 가능한 케이스가 얼마나 되는지 정량화한다.

방법(효율):
 1) 노이즈 조각 집합 정의 = general tier ∩ 영어사전 미수록 ∩ 일반영어빈도(zipf)<3.5.
 2) 코퍼스(CURATORIAL) 문장 중 '노이즈 조각 토큰을 포함한 문장'에만 spaCy NER 적용
    (대부분 문장엔 조각이 없어 NER 부하를 크게 절감). 병렬 스캔(fork COW).
 3) 2토큰 이상 고유명사 개체를 수집 → 결합형(악센트 제거·소문자·영문자)으로 정규화.
 4) 결합형 길이 3~17 + 구성 토큰이 노이즈 조각인 '복원 가능' 개체를 빈도순 집계.

환경 : CW_NER_PAGES(표본 페이지 수, 0/미설정=전체), CW_ZIPF(기본 3.5),
        CW_ENT_MINFREQ(well-known 최소 코퍼스 빈도, 기본 5)
출력 : data/entity_recover.json + 요약 출력
"""
import json, os, re, glob, time, unicodedata, collections
import multiprocessing as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

_WS = re.compile(r"\s+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
TOKEN_RE = re.compile(r"[a-z]+")
MIN_SENT_LEN, MAX_SENT_LEN = 25, 320
KEEP_LABELS = {"PERSON", "ORG", "GPE", "LOC", "NORP", "FAC", "EVENT", "WORK_OF_ART"}


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def deaccent(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def norm_tok(s):
    return re.sub(r"[^a-z]+", "", deaccent(s).lower())


def split_sentences(content):
    for part in _SENT_SPLIT.split(content):
        s = _WS.sub(" ", part).strip()
        if MIN_SENT_LEN <= len(s) <= MAX_SENT_LEN:
            yield s


def iter_pages(corpus_root, include_dirs):
    for d in include_dirs:
        for f in glob.glob(os.path.join(corpus_root, d, "**", "*.json"), recursive=True):
            yield f


# --- fork COW 공유 전역 ---
_NOISE = None   # set: 노이즈 조각 토큰
_SEG = None     # set: include_segment_types
_NLP = None     # spaCy nlp (NER)


def _worker(files):
    # 결과: 개체텍스트 -> count, 그리고 noise 조각 등장 카운트
    ent_count = collections.Counter()
    cand_sents = []
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
                toks = set(TOKEN_RE.findall(deaccent(sent).lower()))
                if toks & _NOISE:
                    cand_sents.append(sent)
    # 후보 문장에만 NER 적용 (배치)
    for sdoc in _NLP.pipe(cand_sents, batch_size=128):
        for e in sdoc.ents:
            if e.label_ not in KEEP_LABELS:
                continue
            parts = [p for p in re.split(r"[\s\-]+", e.text) if p]
            if len(parts) < 2:
                continue
            ent_count[(e.text.strip(), e.label_)] += 1
    return ent_count


def main():
    from nltk.corpus import words as nw
    from english_words import get_english_words_set
    from wordfreq import zipf_frequency as zf
    import spacy

    global _NOISE, _SEG, _NLP
    cfg = load_config()
    corpus_root = cfg["paths"]["corpus_root"]
    include_dirs = cfg["corpus"]["include_dirs"]
    _SEG = set(cfg["corpus"]["include_segment_types"])
    zthr = float(os.environ.get("CW_ZIPF", "3.5"))
    ent_minfreq = int(os.environ.get("CW_ENT_MINFREQ", "5"))
    sample = int(os.environ.get("CW_NER_PAGES", "0"))

    D = set(w.lower() for w in nw.words()) | {w.lower() for w in get_english_words_set(["web2"], lower=True)}
    pool = json.load(open(os.path.join(DATA, "wordpool.json"), encoding="utf-8"))
    _NOISE = {w for w, r in pool.items()
              if r["tier"] == "general" and w not in D and zf(w, "en") < zthr}
    print(f"노이즈 조각 집합: {len(_NOISE):,} (general·사전미수록·zipf<{zthr})", flush=True)

    _NLP = spacy.load("en_core_web_sm",
                      disable=["lemmatizer", "tagger", "parser", "attribute_ruler"])

    files = list(iter_pages(corpus_root, include_dirs))
    if sample and sample < len(files):
        import random
        random.seed(0)
        files = random.sample(files, sample)
    n_pages = len(files)
    workers = max(1, min(os.cpu_count() - 2, n_pages))
    n_chunks = workers * 4
    sz = (len(files) + n_chunks - 1) // max(1, n_chunks)
    chunks = [files[i:i + sz] for i in range(0, len(files), sz)]
    print(f"NER 스캔: 페이지 {n_pages:,} | 워커 {workers} | 청크 {len(chunks)}", flush=True)

    t0 = time.time()
    total = collections.Counter()
    ctx = mp.get_context("fork")
    done = 0
    with ctx.Pool(workers) as pp:
        for part in pp.imap_unordered(_worker, chunks):
            total.update(part)
            done += 1
            if done % max(1, len(chunks) // 10) == 0:
                el = time.time() - t0
                print(f"  청크 {done}/{len(chunks)} | 누적개체 {len(total):,} | {el:.0f}s", flush=True)
    print(f"NER 완료 {time.time()-t0:.0f}s | 고유 다어절개체 {len(total):,}", flush=True)

    # 변이 병합용: freq>=8 다어절 개체 전체 카운터 저장 (build_names.py 입력)
    mw = [[text, label, freq] for (text, label), freq in total.items() if freq >= 8]
    mw.sort(key=lambda r: -r[2])
    json.dump(mw, open(os.path.join(DATA, "mw_entities.json"), "w", encoding="utf-8"),
              ensure_ascii=False)
    print(f"  mw_entities.json 저장: freq>=8 개체 {len(mw):,}개", flush=True)

    # 결합형 정규화 + 복원 가능성 판정
    recover = {}   # concat -> {entity, label, freq, comps, n_noise, all_nondict}
    for (text, label), freq in total.items():
        if freq < ent_minfreq:
            continue
        parts = [p for p in re.split(r"[\s\-]+", text) if p]
        comps = [norm_tok(p) for p in parts]
        comps = [c for c in comps if c]
        if len(comps) < 2:
            continue
        concat = "".join(comps)
        if not (3 <= len(concat) <= 17):
            continue
        n_noise = sum(1 for c in comps if c in _NOISE)
        all_nondict = all(c in _NOISE or c not in D for c in comps)
        prev = recover.get(concat)
        if prev is None or freq > prev["freq"]:
            recover[concat] = {"entity": text, "label": label, "freq": freq,
                               "comps": comps, "n_noise": n_noise,
                               "all_nondict": all_nondict}

    rec_list = sorted(recover.values(), key=lambda r: -r["freq"])
    # 분류
    has1 = [r for r in recover.values() if r["n_noise"] >= 1]
    has2 = [r for r in recover.values() if r["n_noise"] >= 2]
    alln = [r for r in recover.values() if r["all_nondict"]]
    by_label = collections.Counter(r["label"] for r in has1)

    json.dump({"params": {"zipf": zthr, "ent_minfreq": ent_minfreq,
                          "pages": n_pages, "noise_set": len(_NOISE)},
               "recover": {k: v for k, v in recover.items()}},
              open(os.path.join(DATA, "entity_recover.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)

    print(f"\n=== 복원 가능 다어절 고유명사 (결합형 길이3~17, freq>={ent_minfreq}) ===")
    print(f"결합형 후보 총: {len(recover):,}")
    print(f"  구성토큰 중 노이즈조각 >=1개: {len(has1):,}  (이것이 '조각 복원' 케이스)")
    print(f"  구성토큰 중 노이즈조각 >=2개: {len(has2):,}")
    print(f"  전체 구성토큰이 비단어:        {len(alln):,}")
    print(f"  >=1 라벨분포: {dict(by_label.most_common())}")
    print(f"\n--- 상위 40 (freq순, 노이즈>=1) ---")
    for r in sorted(has1, key=lambda r: -r["freq"])[:40]:
        print(f"  {r['freq']:5}  {r['entity']:30} [{r['label']:11}] -> {'+'.join(r['comps'])} = {''.join(r['comps'])}")


if __name__ == "__main__":
    main()
