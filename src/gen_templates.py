#!/usr/bin/env python3
"""
3a단계: 유효 17x17 격자 템플릿 뱅크 생성.

rule.md 충족:
 ① fully-checked  ② 최소 길이 3  → 모든 가로/세로 흰 run 길이 >= 3 (동치)
 ③ 연결성(흰 칸 단일 연결)        ④ 전부-검은 행/열 금지
 ⑥ 180도 회전 대칭                ⑧ 2x2 검은 블록 금지
 ⑦ 검은 칸 최소화                 → 목표 검은 칸 수 범위로 제어

검은 칸을 대칭쌍으로 점진 배치하며, 매 배치 시 영향 행/열의 run(1~2 금지)과
2x2 블록을 국소 검사해 불변식을 유지. 마지막에 연결성/전부검은행 검사.

산출물: data/templates.json  (각 템플릿: 17줄 문자열 '#'=검은 '.'=흰, 메타)
"""
import json, os, random, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def line_runs_ok(line):
    """문자열(행 또는 열)에서 흰('.') 연속 길이가 모두 0 또는 >=3 인지."""
    for run in "".join(line).split("#"):
        if 0 < len(run) < 3:
            return False
    return True


def col(grid, c):
    return [grid[r][c] for r in range(len(grid))]


def affected_lines_ok(grid, cells):
    """주어진 셀들이 속한 행/열만 run 검사 (점진 배치 국소 검증)."""
    n = len(grid)
    rows = {r for r, _ in cells}
    cols = {c for _, c in cells}
    for r in rows:
        if not line_runs_ok(grid[r]):
            return False
    for c in cols:
        if not line_runs_ok(col(grid, c)):
            return False
    return True


def makes_2x2(grid, cells):
    """cells를 검게 했을 때 2x2 검은 블록이 생기는지."""
    n = len(grid)
    for (r, c) in cells:
        for dr in (-1, 0):
            for dc in (-1, 0):
                r0, c0 = r + dr, c + dc
                if 0 <= r0 < n - 1 and 0 <= c0 < n - 1:
                    if (grid[r0][c0] == "#" and grid[r0][c0 + 1] == "#"
                            and grid[r0 + 1][c0] == "#" and grid[r0 + 1][c0 + 1] == "#"):
                        return True
    return False


def connected(grid):
    n = len(grid)
    whites = [(r, c) for r in range(n) for c in range(n) if grid[r][c] == "."]
    if not whites:
        return False
    seen = {whites[0]}
    stack = [whites[0]]
    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == "." and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    return len(seen) == len(whites)


def no_full_black_line(grid):
    n = len(grid)
    for r in range(n):
        if all(ch == "#" for ch in grid[r]):
            return False
    for c in range(n):
        if all(grid[r][c] == "#" for r in range(n)):
            return False
    return True


def generate_one(n, target_black, rng, symmetry="rotational",
                 forbid_2x2=True, max_fail=4000):
    grid = [["."] * n for _ in range(n)]
    black = 0
    fails = 0
    cells_all = [(r, c) for r in range(n) for c in range(n)]
    while black < target_black and fails < max_fail:
        r, c = rng.choice(cells_all)
        # ⑥ 대칭 토글: rotational이면 180도 짝까지 함께, none이면 단독 배치
        if symmetry == "rotational":
            cells = {(r, c), (n - 1 - r, n - 1 - c)}
        else:
            cells = {(r, c)}
        if any(grid[a][b] == "#" for a, b in cells):
            fails += 1
            continue
        # 시도 배치
        for a, b in cells:
            grid[a][b] = "#"
        # ⑧ 2x2 금지 토글
        if (forbid_2x2 and makes_2x2(grid, cells)) or not affected_lines_ok(grid, cells):
            for a, b in cells:
                grid[a][b] = "."
            fails += 1
            continue
        black += len(cells)
    if not no_full_black_line(grid) or not connected(grid):
        return None
    return ["".join(row) for row in grid]


def grid_slots(grid):
    """가로/세로 단어 슬롯 추출: (row, col, dir, length)."""
    n = len(grid)
    slots = []
    for r in range(n):
        c = 0
        while c < n:
            if grid[r][c] == ".":
                start = c
                while c < n and grid[r][c] == ".":
                    c += 1
                slots.append((r, start, "A", c - start))
            else:
                c += 1
    for c in range(n):
        r = 0
        while r < n:
            if grid[r][c] == ".":
                start = r
                while r < n and grid[r][c] == ".":
                    r += 1
                slots.append((start, c, "D", r - start))
            else:
                r += 1
    return slots


def slot_cells(slot):
    r, c, d, L = slot
    if d == "A":
        return {(r, c + i) for i in range(L)}
    return {(r + i, c) for i in range(L)}


def fillability_ok(slots, cfg_grid):
    """긴 슬롯 개수/교차 제약으로 채우기 난이도 제어."""
    longT = cfg_grid["long_threshold"]
    xlongT = cfg_grid["xlong_threshold"]
    longs = [s for s in slots if s[3] >= longT]
    if len(longs) > cfg_grid["max_long_slots"]:
        return False
    if sum(1 for s in slots if s[3] >= xlongT) > cfg_grid["max_xlong_slots"]:
        return False
    if cfg_grid["forbid_long_cross"]:
        cells = [slot_cells(s) for s in longs]
        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                if cells[i] & cells[j]:
                    return False
    return True


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    cfg_grid = cfg["grid"]
    cfg_rules = cfg["rules"]
    n = cfg_grid["size"]
    want = cfg_grid["bank_size"]
    symmetry = cfg_rules["symmetry"]
    forbid_2x2 = cfg_rules["forbid_2x2_black"]
    lo = int(n * n * cfg_rules["min_black_pct"])
    hi = int(n * n * cfg_rules["max_black_pct"])
    rng = random.Random(42)

    templates = []
    seen_patterns = set()
    attempts = 0
    rejected_fill = 0
    while len(templates) < want and attempts < 200000:
        attempts += 1
        target_black = rng.randint(lo, hi)  # rules.min/max_black_pct 기반
        g = generate_one(n, target_black, rng, symmetry=symmetry, forbid_2x2=forbid_2x2)
        if g is None:
            continue
        key = "".join(g)
        if key in seen_patterns:
            continue
        slots = grid_slots(g)
        if not fillability_ok(slots, cfg_grid):
            rejected_fill += 1
            continue
        black = sum(row.count("#") for row in g)
        templates.append({
            "id": f"T{len(templates):03d}",
            "grid": g,
            "black": black,
            "black_pct": round(100 * black / (n * n), 1),
            "n_words": len(slots),
            "slot_len_dist": dict(sorted(collections.Counter(s[3] for s in slots).items())),
        })
        seen_patterns.add(key)

    json.dump(templates, open(os.path.join(data_dir, "templates.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"생성 시도 {attempts}, 채우기제약 탈락 {rejected_fill}, 유효 템플릿 {len(templates)}개 저장")
    if templates:
        bl = [t["black"] for t in templates]
        wc = [t["n_words"] for t in templates]
        print(f"  검은 칸: {min(bl)}~{max(bl)} ({min(t['black_pct'] for t in templates)}~"
              f"{max(t['black_pct'] for t in templates)}%)")
        print(f"  단어 수: {min(wc)}~{max(wc)} (평균 {sum(wc)/len(wc):.0f})")
        # 샘플 1개 출력
        print(f"\n[샘플 {templates[0]['id']}] black={templates[0]['black']} "
              f"words={templates[0]['n_words']}")
        for row in templates[0]["grid"]:
            print("  " + row.replace("#", "■").replace(".", "·"))
        print(f"  슬롯 길이 분포: {templates[0]['slot_len_dist']}")


if __name__ == "__main__":
    main()
