#!/usr/bin/env python3
"""B단계-4: LGDE 주제 게이트 결과를 wordpool.json에 '가중치 부스트'로 반영.

사용자 결정(하이브리드): general 풀 전체를 유지하되, LGDE가 식별한 주제어
(발견어 + 미술 실무 시드)를 general 안에서 theme 티어(weight 10)로 승격한다.
- 격자 채우기(fill.py)는 weight 내림차순 value ordering이라 theme 단어가
  general(1)보다 먼저 시도됨 → 주제어가 더 자주 등장.
- theme 티어는 theme.seed_tiers(core/marker)에 없으므로 강제 시딩엔 안 들어가고
  가중치 부스트만 받는다.
- core/marker/name(더 높은 가중치)은 건드리지 않는다.

입력 : data/lgde_expanded.json(discovered_general), src/lgde_expand.py(ART_SEED)
출력 : data/wordpool.json 갱신(승격), data/wordpool.bak.json 백업
"""
import json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.join(ROOT, "src"))

THEME_TIER = "theme"
THEME_WEIGHT = 10


def main():
    from lgde_expand import ART_SEED  # 미술 시드 단일 출처

    lgde = json.load(open(os.path.join(DATA, "lgde_expanded.json"), encoding="utf-8"))
    discovered = set(lgde["discovered_general"])
    pool = json.load(open(os.path.join(DATA, "wordpool.json"), encoding="utf-8"))

    art_in_pool = {w for w in ART_SEED if w in pool}
    theme_words = discovered | art_in_pool          # 승격 대상 집합

    # general 인 것만 승격(core/marker/name 은 이미 더 높은 가중치라 보존)
    promoted, skipped_nonpool, skipped_hi = [], [], []
    for w in sorted(theme_words):
        rec = pool.get(w)
        if rec is None:
            skipped_nonpool.append(w)
            continue
        if rec["tier"] == "general":
            rec["tier"] = THEME_TIER
            rec["weight"] = THEME_WEIGHT
            promoted.append(w)
        else:
            skipped_hi.append((w, rec["tier"]))

    shutil.copyfile(os.path.join(DATA, "wordpool.json"),
                    os.path.join(DATA, "wordpool.bak.json"))
    json.dump(pool, open(os.path.join(DATA, "wordpool.json"), "w", encoding="utf-8"),
              ensure_ascii=False)

    from collections import Counter
    dist = Counter(v["tier"] for v in pool.values())
    print(f"승격 {len(promoted)}개 → tier={THEME_TIER} weight={THEME_WEIGHT}")
    print(f"  (발견어 {len(discovered)} ∪ 미술시드 {len(art_in_pool)} = 대상 {len(theme_words)})")
    if skipped_hi:
        print(f"  이미 상위 티어라 보존 {len(skipped_hi)}개: {skipped_hi[:10]}")
    if skipped_nonpool:
        print(f"  풀 미존재 {len(skipped_nonpool)}개: {skipped_nonpool[:10]}")
    print(f"  최종 tier 분포: {dict(dist)}")
    print("  백업: data/wordpool.bak.json")


if __name__ == "__main__":
    main()
