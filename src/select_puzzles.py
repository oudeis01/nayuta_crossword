#!/usr/bin/env python3
"""C단계: 생성된 raw 퍼즐(template 재사용으로 200 초과 생성)에서 교차-퍼즐 단어
중복이 적은 N개를 greedy로 선별한다(P8 = 다양성 우선).

방식(사용자 결정 1번): 빈 집합에서 시작해, 매 단계 '이미 선택된 퍼즐들이 쓴 단어와
가장 덜 겹치는' 퍼즐을 고른다. 퍼즐 비용 = Σ_w usage[w] (선택분에서의 누적 사용수).
- core 테마 복합어는 거의 모든 퍼즐에 공통이라 비용에 균일 기여 → 선별에 영향 적음
  (테마 일관성은 유지, 사용자가 'core 반복 일부 잔존'을 수용).
- general/theme 단어의 중복이 적은 퍼즐이 우선 선택돼 어휘 다양성↑.
- 동률은 themed 많은 퍼즐 우선(테마성 보존), 그 다음 template 다양성(덜 쓴 template).

입력 : data/<CW_PUZZLES> (기본 puzzles_raw.json, ok 퍼즐)
출력 : data/<CW_OUT> (기본 puzzles_final.json) + 선별 전후 중복 통계
환경 : CW_N(선별 개수, 기본 200), CW_PUZZLES, CW_OUT
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def words_of(pz):
    return list(pz["assign"].values())


def rep_stats(puzzles):
    ap = collections.Counter()
    for p in puzzles:
        ap.update(set(words_of(p)))
    c = sorted(ap.values(), reverse=True)
    uniq = len(ap)
    once = sum(1 for v in ap.values() if v == 1)
    return {"n_puzzles": len(puzzles), "uniq_words": uniq, "once_only": once,
            "max_rep": c[0] if c else 0, "top10_rep": c[:10]}


def main():
    N = int(os.environ.get("CW_N", "200"))
    pz_file = os.environ.get("CW_PUZZLES", "puzzles_raw.json")
    out_file = os.environ.get("CW_OUT", "puzzles_final.json")

    puzzles = json.load(open(os.path.join(DATA, pz_file), encoding="utf-8"))
    puzzles = [p for p in puzzles if p.get("ok")]
    if N > len(puzzles):
        print(f"[주의] 요청 {N} > 가용 {len(puzzles)} → {len(puzzles)}개 전부 사용", flush=True)
        N = len(puzzles)

    usage = collections.Counter()
    tmpl_used = collections.Counter()
    remaining = list(range(len(puzzles)))
    pwords = [set(words_of(p)) for p in puzzles]
    selected = []

    for _ in range(N):
        best, best_key = None, None
        for i in remaining:
            cost = sum(usage[w] for w in pwords[i])
            # 동률 타이브레이크: 비용↓, themed↓(많을수록 우선=음수), template 사용수↓
            key = (cost, -len(puzzles[i].get("themed", [])),
                   tmpl_used[puzzles[i]["template_id"]])
            if best_key is None or key < best_key:
                best, best_key = i, key
        selected.append(best)
        remaining.remove(best)
        usage.update(pwords[best])
        tmpl_used[puzzles[best]["template_id"]] += 1

    chosen = [puzzles[i] for i in selected]
    json.dump(chosen, open(os.path.join(DATA, out_file), "w", encoding="utf-8"),
              ensure_ascii=False)

    before, after = rep_stats(puzzles), rep_stats(chosen)
    print(f"선별 {len(chosen)}/{len(puzzles)} → {out_file}")
    print(f"  [전체 {before['n_puzzles']}개] 고유단어 {before['uniq_words']:,} | "
          f"1회만 {before['once_only']:,} | 최대반복 {before['max_rep']}")
    print(f"  [선별 {after['n_puzzles']}개]  고유단어 {after['uniq_words']:,} | "
          f"1회만 {after['once_only']:,} | 최대반복 {after['max_rep']}")
    print(f"  선별분 최다반복 top10: {after['top10_rep']}")
    print(f"  template 분포: {dict(sorted(tmpl_used.items(), key=lambda x:-x[1])[:8])} ...")


if __name__ == "__main__":
    main()
