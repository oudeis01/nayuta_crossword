#!/usr/bin/env python3
"""
3b단계: 격자 채우기(fill) - CSP 백트래킹 (증분 도메인 캐싱).

핵심 최적화:
 - 슬롯 도메인을 가중치 내림차순 리스트로 유지(정렬 비용 0, value ordering 무료).
 - 단어 배치 시 '교차 슬롯'의 도메인만 글자 필터로 축소하고 이전 상태를 저장.
 - MRV: 도메인 크기 최소 슬롯 선택(86개 정수 스캔, 저렴).
 - forward check: 축소된 교차 도메인이 비면 즉시 실패.
"""
import json, os, time, random, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


class WordIndex:
    def __init__(self, pool, vgroup=None):
        # vgroup: 미/영 철자 변형 동치 맵 {단어: 그룹키}. 같은 그룹은 한 퍼즐에
        # 하나만 허용 (honour/honor 류, data/spelling_variants.json).
        self.by_len = collections.defaultdict(list)
        self.weight = {}
        self.tier = {}
        self.vkey = vgroup or {}
        for tok, rec in pool.items():
            self.by_len[len(tok)].append(tok)
            self.weight[tok] = rec["weight"]
            self.tier[tok] = rec["tier"]
        for L in self.by_len:
            self.by_len[L].sort(key=lambda t: -self.weight[t])  # 가중치 내림차순


def build_slots(grid):
    """슬롯 + 슬롯별 위치당 교차정보 [(cross_sid, pos_in_cross) or None]."""
    n = len(grid)
    slots = []
    owner = {}   # (r,c,dir) -> (sid, pos)
    cell_across = {}  # (r,c) -> (sid,pos)
    cell_down = {}

    def add_slot(cells, d):
        sid = len(slots)
        slots.append({"id": sid, "cells": cells, "len": len(cells), "dir": d})
        for pos, cell in enumerate(cells):
            (cell_across if d == "A" else cell_down)[cell] = (sid, pos)
        return sid

    for r in range(n):
        c = 0
        while c < n:
            if grid[r][c] == ".":
                cells = []
                while c < n and grid[r][c] == ".":
                    cells.append((r, c)); c += 1
                add_slot(cells, "A")
            else:
                c += 1
    for c in range(n):
        r = 0
        while r < n:
            if grid[r][c] == ".":
                cells = []
                while r < n and grid[r][c] == ".":
                    cells.append((r, c)); r += 1
                add_slot(cells, "D")
            else:
                r += 1
    # 교차정보: 각 슬롯의 위치 pos 셀이 교차하는 반대방향 슬롯
    for s in slots:
        cross = []
        for pos, cell in enumerate(s["cells"]):
            other = cell_down[cell] if s["dir"] == "A" else cell_across[cell]
            cross.append(other)  # (cross_sid, pos_in_cross)
        s["cross"] = cross
    return slots


def solve(grid, widx, rng, node_budget=30000, restarts=200, max_seconds=None,
          theme=None):
    """theme: None이면 시딩 없음. dict면 채우기 전 테마 단어를 일부 슬롯에 선배치.
    theme = {seed_min, seed_max, seed_tiers(set), prefer_long(bool)}."""
    slots = build_slots(grid)
    nslots = len(slots)
    lengths = {s["len"] for s in slots}
    deadline = (time.time() + max_seconds) if max_seconds else None
    vkey = widx.vkey.get   # used 집합은 변형 동치 그룹키로 기록 (중복 금지 확장)

    for _ in range(restarts):
        if deadline and time.time() > deadline:
            break
        # 재시작마다 길이 버킷을 (가중치 내림차순, 무작위) 재정렬 →
        # 동률(general weight=1)이 매번 다르게 섞여 경로 다양성 확보(노드당 0비용).
        bucket = {L: sorted(widx.by_len[L], key=lambda t: (-widx.weight[t], rng.random()))
                  for L in lengths}
        domain = [list(bucket[s["len"]]) for s in slots]
        assigned = [None] * nslots
        used = set()
        nodes = [0]

        # ⑩ 테마 우선 시딩: 채우기 전 일부 슬롯에 테마 단어를 선배치(전파 포함).
        # 실패한 시드는 되돌리고 건너뛴다. 시드 자체는 백트래킹 대상이 아니라,
        # 이 시드 집합으로 풀리지 않으면 다음 재시작이 다르게 시딩한다.
        n_seeded = 0
        if theme:
            seed_tiers = theme["seed_tiers"]
            target = rng.randint(theme["seed_min"], theme["seed_max"])
            elig = list(range(nslots))
            if theme.get("prefer_long"):
                elig.sort(key=lambda i: (-slots[i]["len"], rng.random()))
            else:
                rng.shuffle(elig)
            for i in elig:
                if n_seeded >= target:
                    break
                if assigned[i] is not None:
                    continue
                # 도메인 앞쪽(고가중치)만 훑어 테마 후보 1개 선택. general(weight 1)에
                # 도달하면 테마 없음 → 중단.
                w = None
                for cand in domain[i]:
                    if widx.weight[cand] == 1:
                        break
                    if widx.tier[cand] in seed_tiers and vkey(cand, cand) not in used:
                        w = cand
                        break
                if w is None:
                    continue
                # 교차 슬롯 전파(recurse 본문과 동일 규칙)
                saved = {}
                ok = True
                for pos, ch in enumerate(w):
                    csid, cpos = slots[i]["cross"][pos]
                    if assigned[csid] is not None:
                        continue
                    if csid not in saved:
                        saved[csid] = domain[csid]
                    nd = [ww for ww in domain[csid] if ww[cpos] == ch]
                    domain[csid] = nd
                    if not nd:
                        ok = False
                        break
                if ok:
                    assigned[i] = w
                    used.add(vkey(w, w))
                    domain[i] = [w]
                    n_seeded += 1
                else:
                    for csid, old in saved.items():
                        domain[csid] = old

        def recurse(n_assigned):
            nodes[0] += 1
            if nodes[0] > node_budget:
                return "budget"
            if n_assigned == nslots:
                return True
            # MRV
            best, best_n = -1, None
            for i in range(nslots):
                if assigned[i] is None:
                    d = len(domain[i])
                    if best_n is None or d < best_n:
                        best, best_n = i, d
                        if d == 0:
                            return False  # dead end
            s = slots[best]
            saved = {}   # cross_sid -> old domain list
            for w in domain[best]:
                if vkey(w, w) in used:
                    continue
                # 교차 슬롯 필터
                ok = True
                saved.clear()
                for pos, ch in enumerate(w):
                    csid, cpos = s["cross"][pos]
                    if assigned[csid] is not None:
                        continue
                    if csid not in saved:
                        saved[csid] = domain[csid]
                    nd = [ww for ww in saved.get(csid, domain[csid])
                          if ww[cpos] == ch]
                    domain[csid] = nd
                    if not nd:
                        ok = False
                        break
                if ok:
                    assigned[best] = w
                    used.add(vkey(w, w))
                    res = recurse(n_assigned + 1)
                    if res is True or res == "budget":
                        return res
                    assigned[best] = None
                    used.discard(vkey(w, w))
                # 복원
                for csid, old in saved.items():
                    domain[csid] = old
            return False

        res = recurse(n_seeded)
        if res is True:
            return {s["id"]: assigned[s["id"]] for s in slots}, slots
    return None, slots


def load_variants(data_dir):
    """미/영 철자 변형 동치 맵 로드 (build_variants.py 산출, 없으면 빈 맵)."""
    p = os.path.join(data_dir, "spelling_variants.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def render(grid, assign, slots):
    n = len(grid)
    g = [[("■" if grid[r][c] == "#" else ".") for c in range(n)] for r in range(n)]
    for s in slots:
        w = assign.get(s["id"])
        if not w:
            continue
        for ch, (r, c) in zip(w, s["cells"]):
            g[r][c] = ch.upper()
    return "\n".join(" ".join(row) for row in g)


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    pool = json.load(open(os.path.join(data_dir, "wordpool.json"), encoding="utf-8"))
    templates = json.load(open(os.path.join(data_dir, "templates.json"), encoding="utf-8"))
    vgroup = load_variants(data_dir)

    print(f"단어 색인 구축 중... (풀 {len(pool):,})", flush=True)
    t0 = time.time()
    widx = WordIndex(pool, vgroup)
    print(f"  색인 완료 {time.time()-t0:.1f}s", flush=True)

    import sys
    n_trial = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for t in templates[:n_trial]:
        grid = t["grid"]
        rng = random.Random(hash(t["id"]) & 0xffff)
        t1 = time.time()
        assign, slots = solve(grid, widx, rng, max_seconds=25)
        dt = time.time() - t1
        if assign is None:
            print(f"\n[{t['id']}] 실패 (words={t['n_words']}, len_dist={t['slot_len_dist']}) {dt:.1f}s", flush=True)
            continue
        words = list(assign.values())
        tiers = collections.Counter(widx.tier[w] for w in words)
        themed = sorted(w for w in words if widx.tier[w] != "general")
        print(f"\n[{t['id']}] 성공 {dt:.1f}s | 단어 {len(words)} | 티어 {dict(tiers)}", flush=True)
        print(f"  themed({len(themed)}): {', '.join(themed)}", flush=True)
        print(render(grid, assign, slots), flush=True)


if __name__ == "__main__":
    main()
