#!/usr/bin/env python3
"""
3b 병렬 생성 드라이버.

멀티프로세싱으로 템플릿 채우기를 병렬화한다.
 - WordIndex는 부모에서 1회 구축 후 fork로 워커에 상속(copy-on-write).
 - 작업 단위 = (template_idx, seed). 각 워커가 solve()를 시간예산 내 시도.
 - 한 템플릿에 여러 seed를 줘서 '병렬 재시작 race'로 어려운 템플릿도 공략.

사용:
  python src/generate.py [n_puzzles] [seeds_per_template] [max_seconds] [workers]

효율 개선(2026-06-12):
 - 템플릿 사전선별: data/template_stats.json의 성공 이력이 있는 템플릿에 작업을
   집중하고, 무이력 템플릿에는 탐색 쿼터(CW_EXPLORE, 기본 15%)만 배정.
 - 조기 종료: 성공 퍼즐이 목표(CW_TARGET, 기본 240)에 도달하면 잔여 작업 중단.
 - 실행 후 시도/성공 이력을 template_stats.json에 누적해 다음 실행에 반영.
"""
import json, os, sys, time, random, collections, multiprocessing as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fill import WordIndex, solve, load_variants  # noqa: E402

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


def load_template_stats(data_dir):
    path = os.path.join(data_dir, "template_stats.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_template_stats(stats, results, templates, data_dir):
    """이번 실행의 시도/성공을 누적 이력에 합산해 저장."""
    for r in results:
        tid = templates[r["tidx"]]["id"]
        s = stats.setdefault(tid, {"try": 0, "ok": 0})
        s["try"] += 1
        s["ok"] += int(r["ok"])
    path = os.path.join(data_dir, "template_stats.json")
    json.dump(stats, open(path, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


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
    vgroup = load_variants(data_dir)
    print(f"색인 구축...(풀 {len(pool):,} | 변형동치 {len(vgroup)})", flush=True)
    t0 = time.time()
    widx = WordIndex(pool, vgroup)
    print(f"  완료 {time.time()-t0:.1f}s | 워커 {workers} | 템플릿 {len(templates)} | "
          f"테마시딩 {theme['seed_min']}~{theme['seed_max']} {sorted(theme['seed_tiers'])}"
          if theme else f"  완료 {time.time()-t0:.1f}s | 워커 {workers} | 템플릿 {len(templates)}",
          flush=True)

    # 템플릿 사전선별: 성공 이력 템플릿 위주 + 무이력 템플릿 탐색 쿼터
    stats = load_template_stats(data_dir)
    proven = [i for i, t in enumerate(templates)
              if stats.get(t["id"], {}).get("ok", 0) > 0]
    explore = [i for i in range(len(templates)) if i not in set(proven)]
    explore_frac = float(os.environ.get("CW_EXPLORE", "0.15"))
    if not proven:                       # 이력이 없으면 기존 전수 라운드로빈
        proven, explore, explore_frac = list(range(len(templates))), [], 0.0
    n_explore = int(n_puzzles * explore_frac) if explore else 0
    n_main = n_puzzles - n_explore

    tasks = []
    for i in range(n_main):
        tidx = proven[i % len(proven)]
        for s in range(seeds_per):
            tasks.append((tidx, i * 1000 + s, budget, max_seconds))
    for j in range(n_explore):
        tidx = explore[j % len(explore)]
        for s in range(seeds_per):
            tasks.append((tidx, (n_main + j) * 1000 + s, budget, max_seconds))
    random.Random(0).shuffle(tasks)      # 본대/탐색 인터리브
    target = int(os.environ.get("CW_TARGET", "240"))
    print(f"작업 {len(tasks)}개 투입 (검증 템플릿 {len(proven)}개에 {n_main}, "
          f"탐색 {len(explore)}개에 {n_explore}, race x{seeds_per}, "
          f"조기종료 목표 {target or '없음'})", flush=True)

    results = []
    t1 = time.time()
    with mp.Pool(workers, initializer=init_worker, initargs=(widx, templates, theme)) as p:
        done = 0
        ok_count = 0
        for r in p.imap_unordered(work, tasks, chunksize=1):
            results.append(r)
            done += 1
            ok_count += int(r["ok"])
            if done % 25 == 0:
                print(f"  진행 {done}/{len(tasks)} | 성공 {ok_count} | "
                      f"{time.time()-t1:.0f}s", flush=True)
            if target and ok_count >= target:
                print(f"  목표 {target} 도달, 잔여 {len(tasks)-done}개 작업 중단",
                      flush=True)
                break
    elapsed = time.time() - t1
    save_template_stats(stats, results, templates, data_dir)

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
