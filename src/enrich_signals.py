#!/usr/bin/env python3
"""어휘 필터링 검토용 신호 4종을 비파괴적으로 산출(주석).

신호:
 1) 대문자 비율  - 코퍼스 재스캔. 문장 중간 Title-case 비율(고유명사 신호) + ALLCAPS 비율(약어).
 2) 언어 감지    - langdetect로 각 단어 용례 문장의 지배 언어(비영어 신호).
 3) spaCy NER    - 용례 문장에서 단어가 PERSON/ORG/GPE/LOC 등으로 태깅되는지.
 4) NLTK 사전    - 영어 어휘 목록 존재 여부(이진).

입력 : data/word_sentences.json (용례), data/puzzles_raw.json (타깃)
산출 : data/word_signals.json, docs/word_review_enriched.md, 콘솔 요약(조합 후보 수)

주의: 신호는 주석일 뿐 삭제하지 않는다(하이브리드 방식). 자동 제거 후보는 별도 리스트로만 제시.
"""
import json, os, re, sys, glob, time, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("HF_HOME", "/home/choiharam/storage/models/huggingface")

WORD_CASE_RE = re.compile(r"[A-Za-z]+")
SENT_INIT_PREV = set(".!?\n\r")


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def iter_pages(corpus_root, include_dirs):
    for d in include_dirs:
        for f in glob.glob(os.path.join(corpus_root, d, "**", "*.json"), recursive=True):
            yield d, f


def scan_capitalization(cfg, target):
    """코퍼스 재스캔: 단어별 (총등장, 문장중간 Title-case, ALLCAPS)."""
    corpus_root = cfg["paths"]["corpus_root"]
    include_dirs = cfg["corpus"]["include_dirs"]
    include_seg = set(cfg["corpus"]["include_segment_types"])
    total = collections.Counter()
    midcap = collections.Counter()
    allcaps = collections.Counter()
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
            for m in WORD_CASE_RE.finditer(content):
                tok = m.group(0)
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
                        midcap[low] += 1   # 문장 중간 대문자 = 고유명사 신호
        if n_pages % 10000 == 0:
            print(f"  cap-scan {n_pages} pages {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
    print(f"  대문자 스캔 완료 {time.time()-t0:.0f}s ({n_pages} pages)", flush=True)
    return total, midcap, allcaps


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    docs_dir = os.path.join(ROOT, "docs")
    ws = json.load(open(os.path.join(data_dir, "word_sentences.json"), encoding="utf-8"))
    target = set(ws.keys())
    print(f"타깃 {len(target):,}개", flush=True)

    # 1) 대문자 비율
    total, midcap, allcaps = scan_capitalization(cfg, target)

    # 4) NLTK 영어 사전
    from nltk.corpus import words as nltk_words
    english = set(w.lower() for w in nltk_words.words())
    print(f"NLTK 사전 {len(english):,}", flush=True)

    # 2) 언어 감지 (단어별 용례 문장 결합)
    from langdetect import detect_langs, DetectorFactory, LangDetectException
    DetectorFactory.seed = 0
    lang = {}
    t0 = time.time()
    for w, rec in ws.items():
        sents = [s["text"] for s in rec["sentences"]]
        if not sents:
            lang[w] = (None, 0.0)
            continue
        try:
            res = detect_langs(" ".join(sents))
            lang[w] = (res[0].lang, round(res[0].prob, 3))
        except LangDetectException:
            lang[w] = (None, 0.0)
    print(f"언어 감지 완료 {time.time()-t0:.0f}s", flush=True)

    # 3) spaCy NER (용례 문장 고유집합에 대해 1회)
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["lemmatizer", "tagger", "parser",
                                                 "attribute_ruler"])
    uniq = sorted({s["text"] for rec in ws.values() for s in rec["sentences"]})
    print(f"NER 대상 고유 문장 {len(uniq):,}개...", flush=True)
    ENT_KEEP = {"PERSON", "ORG", "GPE", "LOC", "NORP", "FAC", "EVENT", "WORK_OF_ART"}
    sent_ents = {}   # 문장 -> [(토큰소문자, label)]
    t0 = time.time()
    for s, doc in zip(uniq, nlp.pipe(uniq, batch_size=256)):
        ents = []
        for e in doc.ents:
            if e.label_ in ENT_KEEP:
                for tk in e.text.lower().split():
                    ents.append((tk, e.label_))
        sent_ents[s] = ents
    print(f"  NER 완료 {time.time()-t0:.0f}s", flush=True)

    # 단어별 NER 집계
    signals = {}
    for w, rec in ws.items():
        tot = total.get(w, 0)
        cap_ratio = round(midcap.get(w, 0) / tot, 3) if tot else 0.0
        allcaps_ratio = round(allcaps.get(w, 0) / tot, 3) if tot else 0.0
        # NER: 용례 문장 중 단어가 개체로 태깅된 비율 + 최빈 라벨
        labels = collections.Counter()
        n_checked = 0
        for s in rec["sentences"]:
            n_checked += 1
            for tk, lab in sent_ents.get(s["text"], []):
                if tk == w:
                    labels[lab] += 1
                    break
        ner_label = labels.most_common(1)[0][0] if labels else None
        ner_frac = round(sum(labels.values()) / n_checked, 3) if n_checked else 0.0
        lg, lgp = lang[w]
        signals[w] = {
            "tier": rec["tier"],
            "corpus_freq": rec["corpus_freq"],
            "doc_freq": rec["doc_freq"],
            "length": rec["length"],
            "n_found": rec["n_found"],
            "cap_ratio": cap_ratio,
            "allcaps_ratio": allcaps_ratio,
            "n_occ": tot,
            "lang": lg,
            "lang_prob": lgp,
            "ner_label": ner_label,
            "ner_frac": ner_frac,
            "in_dict": w in english,
        }
    json.dump(signals, open(os.path.join(data_dir, "word_signals.json"), "w",
              encoding="utf-8"), ensure_ascii=False)
    print(f"저장: data/word_signals.json", flush=True)

    # --- 조합 후보 분석 (자동 제거는 안 함; 수치만 제시) ---
    def is_general(w):
        return signals[w]["tier"] == "general"
    gen = [w for w in signals if is_general(w)]
    foreign = [w for w in gen if signals[w]["lang"] not in (None, "en")
               and signals[w]["lang_prob"] >= 0.90]
    proper = [w for w in gen if signals[w]["cap_ratio"] >= 0.8 or
              (signals[w]["ner_frac"] >= 0.5 and signals[w]["ner_label"])]
    acro = [w for w in gen if signals[w]["allcaps_ratio"] >= 0.5]
    nodict_lowfreq = [w for w in gen if not signals[w]["in_dict"]
                      and (signals[w]["corpus_freq"] or 0) < 10]
    no_sent = [w for w in gen if signals[w]["n_found"] == 0]
    # 고신뢰 아티팩트 후보(하이브리드 자동제거 후보): 사전X ∩ 저빈도 ∩ 고유명사아님 ∩ 비영어아님
    hi_artifact = [w for w in nodict_lowfreq
                   if w not in set(proper) and w not in set(foreign)]

    print("\n" + "=" * 60)
    print(f"일반어 {len(gen):,}개 기준 신호별/조합 후보 수 (참고용, 미삭제)")
    print(f"  비영어(lang!=en, prob>=.90)        : {len(foreign):,}")
    print(f"  고유명사 의심(cap>=.8 또는 NER>=.5): {len(proper):,}")
    print(f"  약어 의심(ALLCAPS>=.5)             : {len(acro):,}")
    print(f"  사전X ∩ 저빈도(<10)               : {len(nodict_lowfreq):,}")
    print(f"  용례 0건                           : {len(no_sent):,}")
    print(f"  → 고신뢰 아티팩트 후보(사전X∩저빈도∩비고유명사∩비외래어): {len(hi_artifact):,}")
    print("=" * 60)
    json.dump({
        "general_total": len(gen),
        "foreign": sorted(foreign),
        "proper_suspect": sorted(proper),
        "acronym_suspect": sorted(acro),
        "nodict_lowfreq": sorted(nodict_lowfreq),
        "no_sentence": sorted(no_sent),
        "hi_artifact_candidate": sorted(hi_artifact),
    }, open(os.path.join(data_dir, "filter_candidates.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("저장: data/filter_candidates.json", flush=True)

    # --- 보강 문서: 신호를 메타에 붙여 알파벳순 재출력 ---
    lines = ["# 단어 검토 문서 (신호 보강)", "",
             "각 단어: `[tier] freq=코퍼스빈도 doc=문서수 len=길이 | cap=문장중간대문자비율 "
             "ALLCAPS=약어비율 lang=감지언어(확률) NER=라벨(비율) dict=사전존재` + 용례.",
             "신호는 판단 보조용 주석이며 자동 삭제하지 않음.", ""]
    cur = None
    for w in sorted(signals):
        s = signals[w]
        if w[0].upper() != cur:
            cur = w[0].upper()
            lines.append(f"## {cur}")
            lines.append("")
        flags = []
        if s["lang"] not in (None, "en") and s["lang_prob"] >= 0.90:
            flags.append("⚑외래어")
        if s["cap_ratio"] >= 0.8 or (s["ner_frac"] >= 0.5 and s["ner_label"]):
            flags.append("⚑고유명사")
        if s["allcaps_ratio"] >= 0.5:
            flags.append("⚑약어")
        if not s["in_dict"] and (s["corpus_freq"] or 0) < 10 and not flags:
            flags.append("⚑아티팩트?")
        flag = (" " + " ".join(flags)) if flags else ""
        meta = (f"[{s['tier']}] freq={s['corpus_freq']} doc={s['doc_freq']} len={s['length']} | "
                f"cap={s['cap_ratio']} ALLCAPS={s['allcaps_ratio']} "
                f"lang={s['lang']}({s['lang_prob']}) "
                f"NER={s['ner_label']}({s['ner_frac']}) dict={'Y' if s['in_dict'] else 'N'}")
        lines.append(f"### {w}{flag}")
        lines.append(meta)
        lines.append("")
        for st in ws[w]["sentences"]:
            lines.append(f"- ({st['sim']:.2f}) {st['text']}")
        if not ws[w]["sentences"]:
            lines.append("_용례 없음._")
        lines.append("")
    with open(os.path.join(docs_dir, "word_review_enriched.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("저장: docs/word_review_enriched.md", flush=True)


if __name__ == "__main__":
    main()
