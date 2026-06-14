#!/usr/bin/env python
"""LLM 보조 힌트(예문) 선택 - 2 사이클 파이프라인.

전제: /p/NNNN 힌트 페이지는 정답 단어를 가린 cloze 문장을 보여준다.
따라서 "좋은 예문" = 답을 모르는 사람이 단어를 공정하게 복원할 수 있고(난이도),
앞뒤 문맥 없이 읽혀 깨끗한 문장(편집 품질)이다. 이 둘은 직교하므로 따로 측정한다.

  Cycle 1 (난이도, 정답 가림): 예문마다 정답을 _____ 로 가리고, 모델에게
    빈칸 단어를 묻되 진짜 정답을 teacher-forcing 해 그 logprob 을 읽는다.
    = P(정답 | 가려진 문장) = 실제 복원 확률. 같은 단어 안 후보끼리 비교라 정규화 불필요.
  Cycle 2 (편집 품질, 정답 보여줌): 후보에 난이도 태그를 달아, 자기완결성/문법/
    의미 단일성/톤/타이포(em-dash 등) 기준으로 primary + 백업을 고르게 한다(guided_json).

결과는 hint_review.html 이 불러올 수 있는 import JSON 으로 프리필하고,
사람이 눈으로 볼 검수용 markdown 도 같이 쓴다.

서빙(별도 터미널 또는 백그라운드):
  python -m vllm.entrypoints.openai.api_server \
    --model /home/choiharam/storage/models/Qwen2.5-14B-Instruct-AWQ \
    --quantization awq_marlin --max-model-len 4096 \
    --gpu-memory-utilization 0.92 --served-model-name qwen14b --port 8000

사용:
  python src/llm_hint_select.py --sample 50            # 층화추출 표본 50
  python src/llm_hint_select.py --words abalone,capitalism
  python src/llm_hint_select.py                        # 전체(기본 동시성 16)
  python src/llm_hint_select.py --concurrency 1        # 순차(검증/디버그용)
  python src/llm_hint_select.py --resume               # 중단 후 이어하기

동시성: 요청을 동시에 N개 띄워 vLLM 의 continuous batching 을 끌어내 GPU 를 채운다.
순차(1)는 서버 큐에 항상 1개뿐이라 배칭이 안 일어나 느리다. temperature=0 이라
결과는 동시성과 무관하게 사실상 동일하다(배칭 부동소수 차이로 경계 사례만 드물게 흔들림).
"""
import argparse
import asyncio
import json
import math
import os
import random
import re
import sys
import time

try:
    from openai import AsyncOpenAI
except Exception:
    print("openai 클라이언트가 없습니다(conda base 에서 실행하세요).", file=sys.stderr)
    raise

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENT = os.environ.get("CW_SENT", os.path.join(ROOT, "data", "word_sentences.json"))
PUZ = os.environ.get("CW_PUZZLES", os.path.join(ROOT, "data", "puzzles_raw.json"))

# Cycle 2 가 출력할 flag 어휘 (사람이 우선 검수할 신호).
FLAGS = ["giveaway", "emdash", "fragment", "ambiguous_sense", "offensive", "none_good"]

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "primary": {"type": ["integer", "null"]},
        "backups": {"type": "array", "items": {"type": "integer"}, "maxItems": 2},
        "needs_human": {"type": "boolean"},
        "flags": {"type": "array", "items": {"type": "string", "enum": FLAGS}},
        "reason": {"type": "string", "maxLength": 120},
    },
    "required": ["primary", "backups", "needs_human", "reason"],
    "additionalProperties": False,
}

SYS_JUDGE = (
    "You are an editor choosing the best fill-in-the-blank clue for a crossword "
    "shown at a contemporary-art MFA exhibition and colloquium. The answer word "
    "is HIDDEN: solvers see the sentence with the word blanked and guess it.\n"
    "AUDIENCE: art-world visitors comfortable with academic and art-critical "
    "language. Conceptually rich, theoretical, or florid art-world rhetoric is "
    "ON-THEME and desirable, NOT a defect. Never reject or penalize a sentence "
    "merely for being academic, abstract, or using specialized vocabulary.\n"
    "Pick the sentence(s) that make the clearest, fairest clue:\n"
    "1. Solvability: the blanked sentence gives a fair semantic cue. A clearly "
    "cued, easy sentence is acceptable.\n"
    "2. Self-contained: understandable on its own; no dangling references "
    "('as noted above'), no broken sentence fragments.\n"
    "3. The target word is used in one clear sense.\n"
    "4. Grammatically complete; clean typography (penalize em-dash (—), broken "
    "characters, or encoding junk).\n"
    "For tier=theme or tier=core (the exhibition's key academic/art terms), "
    "PREFER the sentence that best conveys the term's concept in its native "
    "intellectual register, even if demanding.\n"
    "Use indices from the list only. Set primary=null, needs_human=true ONLY if "
    "every candidate is a broken fragment or does not actually use the word. "
    "Keep reason to one short clause."
)


_SUF = r"(?:s|es|ed|ing|'s|d)?"


def find_surface(text, word):
    """문장에서 정답 단어 span 을 찾는다. 없으면 None.

    2단계: (1) 엄격 \\bword\\b(굴절형) 먼저. (2) 실패 시 글자 사이 선택적
    구분자(공백/하이픈/마침표/아포스트로피)를 허용해, 풀의 스쿼시 토큰
    (moma, deepecology, scifi)을 코퍼스 자연 표기(Mo MA, deep ecology, sci-fi)와 매칭.
    """
    w = re.escape(word)
    m = re.search(r"\b" + w + _SUF + r"\b", text, re.IGNORECASE)
    if m:
        return m.start(), m.end()
    if word.endswith("y"):
        m = re.search(r"\b" + re.escape(word[:-1]) + r"ies\b", text, re.IGNORECASE)
        if m:
            return m.start(), m.end()
    # 분리/하이픈 표기 대비: 글자 사이 구분자 0~2개 허용.
    sep = r"[\s\-.’']{0,2}"
    core = sep.join(re.escape(ch) for ch in word)
    m = re.search(r"\b" + core + _SUF + r"\b", text, re.IGNORECASE)
    return (m.start(), m.end()) if m else None


def cloze(text, span):
    s, e = span
    return text[:s] + "_____" + text[e:], text[s:e]


async def score_cloze(client, model, blanked, answer):
    """P(answer | blanked) 를 teacher-forcing logprob 합으로. (sum_logprob, n_tok) 반환."""
    prefix = (
        "Fill in the blank with the single most likely word.\n\n"
        f'Sentence: "{blanked}"\nAnswer:'
    )
    full = prefix + " " + answer
    r = await client.completions.create(
        model=model, prompt=full, max_tokens=1, echo=True, logprobs=1, temperature=0.0,
    )
    lp = r.choices[0].logprobs
    plen = len(prefix)
    total, n = 0.0, 0
    for off, tok_lp in zip(lp.text_offset, lp.token_logprobs):
        if tok_lp is None:
            continue
        if off >= plen:  # 정답 토큰 구간(선행 공백 포함)
            total += tok_lp
            n += 1
    return total, n


def per_token_prob(sum_lp, n):
    if not n:
        return 0.0
    return math.exp(sum_lp / n)


# 난이도 밴드(절대 복원확률 기준, 잠정값 - 표본 검수로 보정 예정).
EASY_REC = 0.50   # 이 이상이면 사실상 giveaway
HARD_REC = 0.005  # 이 이하면 단서 부족(거의 복원 불가)


def difficulty_tag(recover):
    """절대 복원확률 P(정답|가려진 문장)로 거친 난이도 태그."""
    if recover >= EASY_REC:
        return "easy"   # 노출 위험(너무 쉬움)
    if recover <= HARD_REC:
        return "hard"   # 단서 부족(너무 어려움)
    return "fair"


async def judge(client, model, word, tier, cands):
    """cands: [{idx,text,tag}] -> dict(primary,backups,needs_human,flags,reason)."""
    lines = [f"Word to clue: {word}  (tier: {tier})", "", "Candidate sentences:"]
    for c in cands:
        lines.append(f"[{c['idx']}] (difficulty={c['tag']}) {c['text']}")
    lines.append("")
    lines.append(
        "Return JSON: primary (best index or null), backups (up to 2 other good "
        "indices), needs_human (true if none adequate), flags, reason (one clause)."
    )
    msgs = [{"role": "system", "content": SYS_JUDGE},
            {"role": "user", "content": "\n".join(lines)}]
    v = None
    for _ in range(2):  # guided_json 이 가끔 빈 문자열을 반환 → 1회 재시도
        r = await client.chat.completions.create(
            model=model, messages=msgs, temperature=0.0, max_tokens=128,
            extra_body={"guided_json": JUDGE_SCHEMA},
        )
        content = (r.choices[0].message.content or "").strip()
        try:
            v = json.loads(content)
            break
        except Exception:
            m = re.search(r"\{.*\}", content, re.S)
            if m:
                try:
                    v = json.loads(m.group(0)); break
                except Exception:
                    pass
    if v is None:
        return {"primary": None, "backups": [], "needs_human": True,
                "flags": [], "reason": "judge: empty/unparseable response"}
    # guided_json 이 빈 flags 를 {} 로 주거나 enum 밖 값(difficulty=hard 등)을
    # 섞을 때가 있어, 리스트로 정규화하고 알려진 enum 으로만 거른다.
    f = v.get("flags")
    v["flags"] = [x for x in (f if isinstance(f, list) else []) if x in FLAGS]
    if not isinstance(v.get("backups"), list):
        v["backups"] = []
    return v


def confidence(picked_tag, flags, needs_human):
    """high=자동채택 / low=사람 검토. (전시 정책: easy=giveaway 도 수용→high)"""
    neg = set(flags) & {"emdash", "fragment", "ambiguous_sense", "offensive", "none_good"}
    if needs_human or picked_tag is None or neg:
        return "low"
    if picked_tag == "hard":  # LM 복원 거의 불가 → 단서 약함, 사람 확인
        return "low"
    return "high"             # fair/easy & 깨끗 → 자동 채택


def write_prefill(selections, path, model):
    n_high = sum(1 for v in selections.values() if v["_llm"]["confidence"] == "high")
    n_low = sum(1 for v in selections.values() if v["_llm"]["confidence"] == "low")
    out = {
        "_meta": {"tool": "hint_review", "version": 1, "source": "llm_prefill",
                  "model": model, "total_words": len(selections),
                  "high": n_high, "low": n_low,
                  "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S")},
        "selections": selections,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    json.dump(out, open(tmp, "w"), ensure_ascii=False, indent=1)
    os.replace(tmp, path)  # 원자적 교체 - 중단돼도 파일 손상 없음
    return n_high, n_low


def build_word_result(word, tier, sents, scored, v):
    """순수 함수(I/O 없음): 점수+판정 -> (selection, review_entry)."""
    tag_by_idx = {c["idx"]: c.get("tag", "hard") for c in scored}
    rec_by_idx = {c["idx"]: c["recover"] for c in scored}
    valid = {c["idx"] for c in scored if c["ok"]}

    pj = v.get("primary")
    if pj is not None and pj not in valid:  # 모델이 범위 밖/무효 인덱스를 줄 때 방어
        pj = None
        v = dict(v); v["needs_human"] = True
    ptag = tag_by_idx.get(pj) if pj is not None else None
    conf = confidence(ptag, v.get("flags", []), v.get("needs_human", False))

    def entry(i):
        s = sents[i]
        return {"idx": i, "sim": s.get("sim"), "text": s["text"], "url": s.get("url")}

    sel = {
        "primary": entry(pj) if pj is not None else None,
        "backups": [entry(i) for i in v.get("backups", []) if i != pj and i in valid],
        "custom": "",
        "defer": bool(v.get("needs_human")),
        "_llm": {"confidence": conf, "flags": v.get("flags", []),
                 "reason": v.get("reason", ""), "primary_tag": ptag},
    }
    rev = {"word": word, "tier": tier, "conf": conf, "v": v,
           "scored": scored, "rec_by_idx": rec_by_idx, "sents": sents}
    return sel, rev


async def process_word(client, sem, model, word, sents, tier):
    """단어 1개: Cycle 1 cloze 점수(동시) → Cycle 2 판정. sem 이 요청 수를 제한."""
    async def one(idx, s):
        span = find_surface(s["text"], word)
        if span is None:
            return {"idx": idx, "text": s["text"], "ok": False, "recover": None, "sum_lp": None}
        blanked, ans = cloze(s["text"], span)
        try:
            async with sem:
                sum_lp, n = await score_cloze(client, model, blanked, ans)
            return {"idx": idx, "text": s["text"], "ok": True,
                    "recover": per_token_prob(sum_lp, n), "sum_lp": sum_lp}
        except Exception:
            return {"idx": idx, "text": s["text"], "ok": False, "recover": None, "sum_lp": None}

    scored = list(await asyncio.gather(*[one(i, s) for i, s in enumerate(sents)]))
    for c in scored:
        if c["ok"]:
            c["tag"] = difficulty_tag(c["recover"])
    cands = [{"idx": c["idx"], "text": c["text"], "tag": c.get("tag", "hard")}
             for c in scored if c["ok"]]
    if cands:
        try:
            async with sem:
                v = await judge(client, model, word, tier, cands)
        except Exception as e:
            v = {"primary": None, "backups": [], "needs_human": True,
                 "flags": [], "reason": f"judge_error: {e}"}
    else:
        v = {"primary": None, "backups": [], "needs_human": True,
             "flags": ["none_good"], "reason": "no sentence contains the word"}
    return build_word_result(word, tier, sents, scored, v)


async def run_all(client, words, ws, model, conc, out, save_every, init_selections):
    """words 를 동시성 conc 로 처리. as_completed 로 받으며 주기적으로 체크포인트."""
    sem = asyncio.Semaphore(conc)
    selections = dict(init_selections)
    review = []
    t0 = time.time()
    tasks = [asyncio.create_task(
        process_word(client, sem, model, w,
                     ws[w].get("sentences", []), ws[w].get("tier", "?")))
        for w in words]
    done = 0
    for fut in asyncio.as_completed(tasks):
        sel, rev = await fut
        selections[rev["word"]] = sel
        review.append(rev)
        done += 1
        if done % save_every == 0:
            write_prefill(selections, out, model)
            print(f"  {done}/{len(words)}  체크포인트 저장  "
                  f"({time.time()-t0:.0f}s)", file=sys.stderr)
    return selections, review, time.time() - t0


def stratified_sample(ws, words, n, seed=7):
    random.seed(seed)
    buckets = {}
    for w in words:
        tier = ws[w].get("tier", "?")
        ns = len(ws[w].get("sentences", []))
        nb = "few" if ns <= 3 else ("mid" if ns <= 7 else "many")
        buckets.setdefault((tier, nb), []).append(w)
    out, keys = [], list(buckets)
    random.shuffle(keys)
    i = 0
    while len(out) < n and any(buckets.values()):
        k = keys[i % len(keys)]
        if buckets[k]:
            out.append(buckets[k].pop())
        i += 1
        if i > 100000:
            break
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="층화추출 표본 단어 수")
    ap.add_argument("--words", default="", help="쉼표로 구분한 단어 직접 지정")
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--model", default="qwen14b")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "hint_prefill.json"))
    ap.add_argument("--review", default=os.path.join(ROOT, "docs", "review", "llm_pilot.md"))
    ap.add_argument("--resume", action="store_true",
                    help="--out 에 이미 있는 단어는 건너뛴다(중단 후 이어하기)")
    ap.add_argument("--save-every", type=int, default=50, help="체크포인트 저장 주기(단어)")
    ap.add_argument("--concurrency", type=int, default=16,
                    help="동시 in-flight 요청 수(vLLM 배칭 활용). 1이면 순차")
    args = ap.parse_args()

    ws = json.load(open(SENT))
    puz = json.load(open(PUZ))
    used = set()
    for p in puz:
        used.update(p.get("assign", {}).values())
    all_words = sorted(w for w in used if w in ws)

    if args.words:
        words = [w.strip() for w in args.words.split(",") if w.strip() in ws]
    elif args.sample:
        words = stratified_sample(ws, all_words, args.sample)
    else:
        words = all_words

    client = AsyncOpenAI(base_url=args.base_url, api_key="EMPTY")
    print(f"대상 단어 {len(words)}개 | 모델 {args.model} @ {args.base_url} "
          f"| 동시성 {args.concurrency}", file=sys.stderr)

    init = {}
    if args.resume and os.path.exists(args.out):
        init = json.load(open(args.out)).get("selections", {})
        words = [w for w in words if w not in init]
        print(f"이어하기: 기존 {len(init)}개 건너뜀, 남은 {len(words)}개", file=sys.stderr)

    selections, review, elapsed = asyncio.run(run_all(
        client, words, ws, args.model, args.concurrency,
        args.out, args.save_every, init))
    n_high, n_low = write_prefill(selections, args.out, args.model)

    # 검수용 markdown
    os.makedirs(os.path.dirname(args.review), exist_ok=True)
    md = [f"# LLM 파일럿 검수 ({len(selections)}단어)",
          f"high {n_high} · low {n_low} · 소요 {elapsed:.0f}s",
          f"모델 {args.model}\n"]
    for r in sorted(review, key=lambda x: {"low": 0, "med": 1, "high": 2}[x["conf"]]):
        v = r["v"]
        md.append(f"## {r['word']}  `[{r['tier']}]`  conf={r['conf']}  "
                  f"flags={v.get('flags')}  defer={v.get('needs_human')}")
        md.append(f"> {v.get('reason','')}")
        for c in r["scored"]:
            mark = ""
            if c["idx"] == v.get("primary"):
                mark = " **<<PRIMARY**"
            elif c["idx"] in (v.get("backups") or []):
                mark = " *(backup)*"
            rec = c["recover"]
            recs = f"{rec:.3f}" if rec is not None else "  -  "
            tag = c.get("tag", "noword")
            md.append(f"- [{c['idx']}] rec={recs} {tag:5s} {c['text']}{mark}")
        md.append("")
    open(args.review, "w").write("\n".join(md))

    print(f"\n저장: {args.out}", file=sys.stderr)
    print(f"검수: {args.review}", file=sys.stderr)
    print(f"high {n_high} / low {n_low} / 총 {len(selections)}  "
          f"({elapsed:.0f}s, 동시성 {args.concurrency})", file=sys.stderr)


if __name__ == "__main__":
    main()
