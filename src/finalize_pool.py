#!/usr/bin/env python3
"""Phase 3: 최종 풀 기록 = 정제(삭제) + 복원 이름(name tier) 병합.

입력 : data/wordpool.json (현재, theme 승격 반영분)
       data/removed_general.json (clean_pool.py 확정 제거 목록)
       data/recovered_names.json (build_names.py 복원 이름)
       data/theme_remove.json (theme 티어 확정 제거 목록, 사용자 결정)
       data/name_fame_keep.json (name 티어 유명도 keep 목록, 사용자 결정)
       data/manual_remove.json (퍼즐 검토 확정 제거 목록, 전 tier 대상, 사용자 결정)
출력 : data/wordpool.json 갱신, data/wordpool.prefinal.bak.json 백업

순서:
 1) general 정제 제거(removed_general) + 보호 tier 명백 조각(CLEAR_FRAGS) 제거
    + theme 티어 확정 제거(theme_remove: 비유명 인명/다어절 지명 조각/소유격결합).
 2) 복원 이름 추가: status=new → 신규 name 레코드, promote_general → name 으로 승격
    (정제에서 지워졌어도 name 추가가 우선), skip_protected → 기존 보호 tier 유지(skip).
    유명도 필터: 지명 라벨(GPE/LOC/NORP)은 전부 유지, 그 외 라벨은 fame_keep
    목록에 있는 것만 병합(대학 교양 수준 인지도 기준, 사용자 결정).
    복원 레코드엔 parts(원 다어절 토큰)를 저장해 Phase 4 다어절 힌트 채굴에 사용.
 3) 수동 확정 제거(manual_remove): 생성 퍼즐 검토에서 확정된 제거 단어를 전 tier에
    적용. 복원 이름 병합 뒤에 실행해야 name 티어 제거 단어가 재병합되지 않음.
"""
import json, os, shutil, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
NAME_WEIGHT = 20
CLEAR_FRAGS = {"sao", "uks"}     # 보호 tier 명백 조각(사용자 결정)
PLACE_LABELS = {"GPE", "LOC", "NORP"}   # 지명/민족 라벨은 유명도 무관 전부 유지


def main():
    pool = json.load(open(os.path.join(DATA, "wordpool.json"), encoding="utf-8"))
    removed = set(json.load(open(os.path.join(DATA, "removed_general.json"), encoding="utf-8")))
    rn = json.load(open(os.path.join(DATA, "recovered_names.json"), encoding="utf-8"))
    theme_rm = set(json.load(open(os.path.join(DATA, "theme_remove.json"), encoding="utf-8")))
    fame = set(json.load(open(os.path.join(DATA, "name_fame_keep.json"), encoding="utf-8")))
    manual_rm = set()
    mr_path = os.path.join(DATA, "manual_remove.json")
    if os.path.exists(mr_path):
        manual_rm = set(json.load(open(mr_path, encoding="utf-8")))

    shutil.copyfile(os.path.join(DATA, "wordpool.json"),
                    os.path.join(DATA, "wordpool.prefinal.bak.json"))

    # 1) 제거
    n_rm_gen = n_rm_frag = n_rm_theme = 0
    for w in removed:
        if w in pool and pool[w]["tier"] == "general":
            del pool[w]; n_rm_gen += 1
    for w in CLEAR_FRAGS:
        if w in pool:
            del pool[w]; n_rm_frag += 1
    for w in theme_rm:
        if w in pool:
            del pool[w]; n_rm_theme += 1

    # 2) 복원 이름 병합 (지명 라벨 전부 + fame_keep 만)
    add_new = promote = skip = fame_drop = 0
    for concat, v in rn.items():
        if v["status"] == "skip_protected":
            skip += 1
            continue
        if v["label"] not in PLACE_LABELS and concat not in fame:
            fame_drop += 1
            continue
        existed = concat in pool
        pool[concat] = {
            "token": concat, "length": len(concat), "tier": "name",
            "weight": NAME_WEIGHT, "corpus_freq": v["freq"], "doc_freq": 0,
            "sources": [], "origins": ["recovered:" + v["display"]],
            "forced": False, "parts": v["parts"], "ner_label": v["label"],
        }
        if existed:
            promote += 1
        else:
            add_new += 1

    # 3) 수동 확정 제거 (퍼즐 검토 결과, 전 tier 대상. 병합 후 적용)
    n_rm_manual = 0
    for w in manual_rm:
        if w in pool:
            del pool[w]; n_rm_manual += 1

    json.dump(pool, open(os.path.join(DATA, "wordpool.json"), "w", encoding="utf-8"),
              ensure_ascii=False)

    dist = collections.Counter(v["tier"] for v in pool.values())
    print(f"제거: general 정제 {n_rm_gen:,} + 보호tier 조각 {n_rm_frag} ({sorted(CLEAR_FRAGS)})"
          f" + theme 확정제거 {n_rm_theme} + 수동 확정제거 {n_rm_manual}")
    print(f"복원 이름: 신규 {add_new:,} + general승격 {promote:,}"
          f" (skip_protected {skip}, 유명도 탈락 {fame_drop:,})")
    print(f"최종 풀 크기: {len(pool):,}")
    print(f"  tier 분포: {dict(dist.most_common())}")
    print("  백업: data/wordpool.prefinal.bak.json")


if __name__ == "__main__":
    main()
