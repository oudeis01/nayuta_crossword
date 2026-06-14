#!/usr/bin/env python3
"""
외과적 부분 재생성: 특정 invalid 단어를 풀에서 제거하고, 그 단어가 박힌
퍼즐만 같은 템플릿/시드로 다시 풀어 교체한다. 나머지 퍼즐은 손대지 않아
원본 순서(=인쇄 seq 매핑)와 내용이 그대로 보존된다.

배경: 데이터_아티팩트_탐색_결과.md 의 Type A(foreign/fragment) + 오타.
  - 풀(wordpool.json)에서 영구 제거(향후 어떤 생성에서도 채워지지 않음).
  - puzzles_raw.json 에서 해당 단어를 포함한 퍼즐만 재해결.

사용:
  python src/refill_puzzles.py            # 실제 적용(백업 후 덮어씀)
  python src/refill_puzzles.py --dry-run  # 영향 범위만 출력, 파일 변경 없음

힌트/예문 재생성은 별도 단계:
  python src/mine_sentences.py                 # 새 단어 예문 채굴(used set 자동)
  python src/llm_hint_select.py --resume ...   # 신규 단어만 LLM 판단
  python src/build_site.py                     # 페이지 재빌드
"""
import json, os, sys, time, random, collections, shutil, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fill import WordIndex, solve, load_variants  # noqa: E402
from generate import load_config, build_theme, load_template_stats  # noqa: E402

# 격자에서 퇴출할 단어(검토 확정: Type A + alot). desi는 영어 사전 등재어라 유지.
REMOVE = ["afore", "trow", "spina", "reve", "casse", "rideau",
          "akan", "lire", "ultimo", "egal", "alot"]

NODE_BUDGET = 30000
# 성공은 빠르고(~5s) 실패는 느리다. 저성공률(빡빡한) 템플릿 대비:
# 짧은 제한시간 x 많은 시드로 첫 성공을 빠르게 노린다.
MAX_SECONDS = 20          # 재해결 1회 시간예산
SEED_TRIES = 80           # 저장된 seed 실패 시 시도할 대체 seed 개수


def backup(path):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = f"{path}.{ts}.bak"
    shutil.copy2(path, bak)
    return bak


def make_record(tidx, template_id, seed, widx, theme, assign, slots, dt):
    words = [assign[s["id"]] for s in slots]
    tiers = collections.Counter(widx.tier[w] for w in words)
    return {
        "tidx": tidx, "template_id": template_id, "seed": seed,
        "ok": True, "sec": dt, "n_words": len(words),
        "tiers": dict(tiers),
        "themed": sorted(w for w in words if widx.tier[w] != "general"),
        "assign": {str(s["id"]): assign[s["id"]] for s in slots},
    }


def resolve_one(t, base_seed, widx, theme, remove_set):
    """저장된 seed 우선, 실패 시 대체 seed로 깨끗한 채움을 탐색."""
    grid = t["grid"]
    seeds = [base_seed] + [base_seed + 7919 * (k + 1) for k in range(SEED_TRIES)]
    for seed in seeds:
        rng = random.Random(seed)
        t0 = time.time()
        assign, slots = solve(grid, widx, rng, node_budget=NODE_BUDGET,
                              restarts=10**9, max_seconds=MAX_SECONDS, theme=theme)
        dt = time.time() - t0
        if assign is None:
            continue
        words = set(assign.values())
        if words & remove_set:          # 풀에서 뺐으니 정상적으로는 발생 안 함
            continue
        rec = make_record(t["tidx_runtime"], t["id"], seed, widx, theme,
                          assign, slots, dt)
        return rec, seed
    return None, None


def resolve_any_template(p, widx, theme, remove_set, templates, stats):
    """저장된 템플릿이 정제 풀에서 안 풀릴 때의 폴백.
    성공 이력이 높은(=채우기 쉬운) 템플릿부터 시도해 첫 깨끗한 채움을 채택한다.
    seq 매핑은 리스트 인덱스 기준이라 template_id가 바뀌어도 보존된다."""
    base_seed = p["seed"]
    order = sorted(
        range(len(templates)),
        key=lambda i: stats.get(templates[i]["id"], {}).get("ok", 0),
        reverse=True,
    )
    for tidx in order:
        t = dict(templates[tidx]); t["tidx_runtime"] = tidx
        rec, used_seed = resolve_one(t, base_seed, widx, theme, remove_set)
        if rec is not None:
            return rec, used_seed, templates[tidx]["id"]
    return None, None, None


def main():
    dry = "--dry-run" in sys.argv
    data_dir = os.path.join(ROOT, load_config()["paths"]["data_dir"])
    remove_set = set(REMOVE)

    pool = json.load(open(os.path.join(data_dir, "wordpool.json"), encoding="utf-8"))
    templates = json.load(open(os.path.join(data_dir, "templates.json"), encoding="utf-8"))
    puz = json.load(open(os.path.join(data_dir, "puzzles_raw.json"), encoding="utf-8"))
    cfg = load_config()
    theme = build_theme(cfg)
    vgroup = load_variants(data_dir)

    present = [w for w in REMOVE if w in pool]
    missing = [w for w in REMOVE if w not in pool]
    print(f"제거 대상 {len(REMOVE)}개 | 풀에 존재 {len(present)} | 부재 {missing}")

    # 템플릿 id -> 런타임 인덱스 매핑(레코드 검증용)
    tid_to_idx = {t["id"]: i for i, t in enumerate(templates)}

    affected = [i for i, p in enumerate(puz)
                if set(p.get("assign", {}).values()) & remove_set]
    old_used = set()
    for p in puz:
        old_used.update(p.get("assign", {}).values())
    print(f"전체 퍼즐 {len(puz)} | 영향(재해결 대상) {len(affected)}개: "
          f"{[i + 1 for i in affected]}")

    if dry:
        print("[dry-run] 파일 변경 없음.")
        return

    # 풀 정제(영구 제거) + 백업
    print(f"wordpool 백업: {os.path.basename(backup(os.path.join(data_dir, 'wordpool.json')))}")
    for w in present:
        del pool[w]
    json.dump(pool, open(os.path.join(data_dir, "wordpool.json"), "w",
              encoding="utf-8"), ensure_ascii=False)
    print(f"  정제 후 풀 크기 {len(pool):,} (제거 {len(present)})")

    widx = WordIndex(pool, vgroup)
    stats = load_template_stats(data_dir)   # 폴백 템플릿 우선순위용

    # 영향 퍼즐만 재해결
    failed = []
    new_words_total = set()
    for i in affected:
        p = puz[i]
        tidx = tid_to_idx.get(p["template_id"])
        if tidx is None:
            failed.append((i, "template_id 미발견"))
            continue
        t = dict(templates[tidx]); t["tidx_runtime"] = tidx
        old_assign = set(p.get("assign", {}).values())
        rec, used_seed = resolve_one(t, p["seed"], widx, theme, remove_set)
        swapped_tid = None
        if rec is None:
            # 폴백: 저장 템플릿이 정제 풀에서 안 풀리면 다른 템플릿 허용.
            print(f"  seq{i + 1:04d} {p['template_id']} 실패 -> 다른 템플릿 탐색", flush=True)
            rec, used_seed, swapped_tid = resolve_any_template(
                p, widx, theme, remove_set, templates, stats)
        if rec is None:
            failed.append((i, "재해결 실패(전 템플릿 소진)"))
            print(f"  seq{i + 1:04d} 실패")
            continue
        new_assign = set(rec["assign"].values())
        swapped_in = new_assign - old_assign
        new_words_total |= swapped_in
        puz[i] = rec
        if swapped_tid:
            tag = f" (템플릿 {p['template_id']}->{swapped_tid}, seed {used_seed})"
        else:
            tag = "" if used_seed == p["seed"] else f" (대체 seed {used_seed})"
        print(f"  seq{i + 1:04d} OK{tag} | 교체단어 {len(swapped_in)}개")

    # 사후 검증: 어떤 퍼즐에도 제거단어가 없어야 함
    leftover = set()
    new_used = set()
    for p in puz:
        vals = set(p.get("assign", {}).values())
        new_used.update(vals)
        leftover |= vals & remove_set

    # 새로 등장한(기존 used set에 없던) 단어 = 예문/힌트 필요
    truly_new = new_used - old_used

    if failed:
        print(f"\n경고: 재해결 실패 {len(failed)}건 {failed}. "
              f"puzzles_raw.json 저장하지 않음.")
        return

    print(f"\n사후 검증: 잔존 제거단어 {sorted(leftover)} (비어야 정상)")
    print(f"전체 used 단어 {len(old_used)} -> {len(new_used)} "
          f"| 신규(예문/힌트 필요) {len(truly_new)}개")

    print(f"puzzles_raw 백업: "
          f"{os.path.basename(backup(os.path.join(data_dir, 'puzzles_raw.json')))}")
    json.dump(puz, open(os.path.join(data_dir, "puzzles_raw.json"), "w",
              encoding="utf-8"), ensure_ascii=False)
    print(f"  저장 완료 ({len(puz)}개, 순서 보존)")

    # 신규 단어가 기존 예문/힌트에 있는지 진단
    sent_path = os.path.join(data_dir, "word_sentences.json")
    hint_path = os.path.join(data_dir, "hint_prefill.json")
    ws = json.load(open(sent_path)) if os.path.exists(sent_path) else {}
    hints = (json.load(open(hint_path)).get("selections", {})
             if os.path.exists(hint_path) else {})
    no_sent = sorted(w for w in truly_new if w not in ws)
    no_hint = sorted(w for w in truly_new if w not in hints)
    print(f"\n신규 단어 진단:")
    print(f"  예문 없음(mine_sentences 필요) {len(no_sent)}: {no_sent[:30]}")
    print(f"  LLM 힌트 없음(--resume 대상) {len(no_hint)}: {no_hint[:30]}")
    print("\n다음 단계: mine_sentences.py -> llm_hint_select.py --resume -> build_site.py")


if __name__ == "__main__":
    main()
