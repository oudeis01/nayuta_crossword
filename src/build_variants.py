#!/usr/bin/env python3
"""미/영 철자 변형 동치 그룹 생성 (단일 퍼즐 내 변형 철자 중복 방지용).

배경: 사용자 결정(2026-06-12). honour 등 영국식 철자를 풀에 유지하되,
"단일 퍼즐 내 동일 단어 중복 금지" 규정이 미/영 철자 차이(honour/honor,
colour/color, analyse/analyze 등)로 우회되지 않도록, 변형 철자 쌍을
같은 단어로 취급하는 동치 맵을 만든다. fill.py 의 used 집합에서 사용.

입력 : vendor/varcon/varcon.txt (SCOWL VarCon, 미/영/캐나다 철자 변형 DB)
       data/wordpool.json
출력 : data/spelling_variants.json  {단어: 그룹키}
       그룹키 = 클러스터 내 풀 단어 중 알파벳순 첫 단어. 풀에 2개 이상
       공존하는 클러스터만 기록(싱글턴은 동치 처리 불필요).
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
VARCON = os.path.join(ROOT, "vendor", "varcon", "varcon.txt")


def parse_clusters():
    """VarCon 한 줄 = 동등 철자 클러스터. 'TAGS: word / TAGS: word ...' 형식."""
    clusters = []
    for line in open(VARCON, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line = line.split("|")[0].split("##")[0]
        ws = set()
        for part in line.split("/"):
            if ":" not in part:
                continue
            w = part.split(":", 1)[1].strip().lower()
            if re.fullmatch(r"[a-z]+", w):
                ws.add(w)
        if len(ws) >= 2:
            clusters.append(ws)
    return clusters


def main():
    pool = json.load(open(os.path.join(DATA, "wordpool.json"), encoding="utf-8"))
    words = set(pool)

    # union-find 로 줄 단위 클러스터를 전이적으로 병합
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for ws in parse_clusters():
        ws = sorted(ws)
        for w in ws:
            parent.setdefault(w, w)
        for w in ws[1:]:
            ra, rb = find(ws[0]), find(w)
            if ra != rb:
                parent[rb] = ra

    groups = collections.defaultdict(set)
    for w in parent:
        if w in words:
            groups[find(w)].add(w)

    out = {}
    n_groups = 0
    for g in groups.values():
        if len(g) < 2:
            continue
        n_groups += 1
        key = min(g)
        for w in g:
            out[w] = key

    json.dump(out, open(os.path.join(DATA, "spelling_variants.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
    print(f"변형 철자 동치: {n_groups}그룹 / {len(out)}단어 (풀 {len(words):,})")
    print("저장: data/spelling_variants.json")


if __name__ == "__main__":
    main()
