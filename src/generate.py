#!/usr/bin/env python3
"""
3b 병렬 생성 드라이버.

멀티프로세싱으로 템플릿 채우기를 병렬화한다.
 - WordIndex는 부모에서 1회 구축 후 fork로 워커에 상속(copy-on-write).
 - 작업 단위 = (template_idx, seed). 각 워커가 solve()를 시간예산 내 시도.
 - 한 템플릿에 여러 seed를 줘서 '병렬 재시작 race'로 어려운 템플릿도 공략.

사용:
  python src/generate.py [n_puzzles] [seeds_per_template] [max_seconds] [workers]
"""
import json, os, sys, time, random, collections, multiprocessing as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fill import WordIndex, solve  # noqa: E402

_WIDX = None
_TEMPLATES = None
_THEME = None


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_theme(cfg):
    """config의 theme 섹션을 solve()용 dict로 변환(seed_tiers는 set)."""
    th = cfg.get("theme")
    if not th:
        return None
    return {
        "seed_min": th["seed_min"],
        "seed_max": th["seed_max"],
        "seed_tiers": set(th["seed_tiers"]),
        "prefer_long": th.get("prefer_long_slots", True),
    }


def init_worker(widx, templates, theme):
    global _WIDX, _TEMPLATES, _THEME
    _WIDX = widx
    _TEMPLATES = templates
    _THEME = theme


def work(task):
    tidx, seed, budget, max_seconds = task
    t = _TEMPLATES[tidx]
    rng = random.Random(seed)
    t0 = time.time()
    assign, slots = solve(t["grid"], _WIDX, rng,
                          node_budget=budget, restarts=10**9, max_seconds=max_seconds,
                          theme=_THEME)
    dt = time.time() - t0
    if assign is None:
        return {"tidx": tidx, "seed": seed, "ok": False, "sec": dt}
    words = [assign[s["id"]] for s in slots]
    tiers = collections.Counter(_WIDX.tier[w] for w in words)
    return {
        "tidx": tidx, "template_id": t["id"], "seed": seed, "ok": True, "sec": dt,
        "n_words": len(words),
        "tiers": dict(tiers),
        "themed": sorted(w for w in words if _WIDX.tier[w] != "general"),
        "assign": {str(s["id"]): assign[s["id"]] for s in slots},
    }


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    pool_file = os.environ.get("CW_POOL", "wordpool.json")   # 시험용 풀 교체 가능
    pool = json.load(open(os.path.join(data_dir, pool_file), encoding="utf-8"))
    templates = json.load(open(os.path.join(data_dir, "templates.json"), encoding="utf-8"))

    n_puzzles = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    seeds_per = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    max_seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 30
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else max(1, os.cpu_count() - 2)
    budget = 30000

    theme = build_theme(cfg)
    print(f"색인 구축...(풀 {len(pool):,})", flush=True)
    t0 = time.time()
    widx = WordIndex(pool)
    print(f"  완료 {time.time()-t0:.1f}s | 워커 {workers} | 템플릿 {len(templates)} | "
          f"테마시딩 {theme['seed_min']}~{theme['seed_max']} {sorted(theme['seed_tiers'])}"
          if theme else f"  완료 {time.time()-t0:.1f}s | 워커 {workers} | 템플릿 {len(templates)}",
          flush=True)

    # 작업: n_puzzles개를 템플릿 라운드로빈 + seed 변주, seeds_per로 race
    tasks = []
    for i in range(n_puzzles):
        tidx = i % len(templates)
        for s in range(seeds_per):
            tasks.append((tidx, i * 1000 + s, budget, max_seconds))
    print(f"작업 {len(tasks)}개 투입 (목표 퍼즐 {n_puzzles}, race x{seeds_per})", flush=True)

    results = []
    t1 = time.time()
    with mp.Pool(workers, initializer=init_worker, initargs=(widx, templates, theme)) as p:
        done = 0
        for r in p.imap_unordered(work, tasks, chunksize=1):
            results.append(r)
            done += 1
            if done % 25 == 0:
                ok = sum(1 for x in results if x["ok"])
                print(f"  진행 {done}/{len(tasks)} | 성공 {ok} | "
                      f"{time.time()-t1:.0f}s", flush=True)
    elapsed = time.time() - t1

    ok = [r for r in results if r["ok"]]
    by_template = collections.Counter(r["tidx"] for r in ok)
    fail_templates = collections.Counter(r["tidx"] for r in results if not r["ok"])
    themed_counts = [len(r["themed"]) for r in ok]

    print("\n" + "=" * 60)
    print(f"병렬 생성 완료 {elapsed:.0f}s | 성공 {len(ok)}/{len(tasks)} 작업")
    print(f"  성공한 고유 템플릿: {len(by_template)}/{len(templates)}")
    if themed_counts:
        print(f"  themed/퍼즐: 평균 {sum(themed_counts)/len(themed_counts):.1f} "
              f"(min {min(themed_counts)}, max {max(themed_counts)})")
    print(f"  실패 작업 수: {len(results)-len(ok)}")
    # 성공 결과 저장
    out_file = os.environ.get("CW_OUT", "puzzles_raw.json")
    json.dump(ok, open(os.path.join(data_dir, out_file), "w",
              encoding="utf-8"), ensure_ascii=False)
    print(f"  저장: {data_dir}/{out_file} ({len(ok)}개)")
    print("=" * 60)


if __name__ == "__main__":
    main()
