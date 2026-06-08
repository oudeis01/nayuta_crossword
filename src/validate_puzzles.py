#!/usr/bin/env python3
"""산출 퍼즐(puzzles_raw.json)이 rule.md 절대 규칙을 지키는지 검증.

검사:
 - 모든 슬롯이 채워짐(빈 슬롯 없음).
 - 단어 길이 == 슬롯 길이.
 - 교차 셀 글자 일관성(가로/세로가 같은 칸에서 동일 글자).
 - 단어 중복 금지(rule ⑤): 한 퍼즐 내 동일 단어 2회 금지.
 - 모든 답이 풀(wordpool)에 존재(rule ⑨, 코어 예외 포함 — 풀에 이미 반영됨).
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fill import build_slots  # noqa: E402


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    pool = set(json.load(open(os.path.join(data_dir, "wordpool.json"), encoding="utf-8")))
    templates = {t["id"]: t for t in
                 json.load(open(os.path.join(data_dir, "templates.json"), encoding="utf-8"))}
    puzzles = json.load(open(os.path.join(data_dir, "puzzles_raw.json"), encoding="utf-8"))

    issues = collections.Counter()
    checked = 0
    for p in puzzles:
        if not p.get("ok"):
            continue
        checked += 1
        t = templates[p["template_id"]]
        slots = build_slots(t["grid"])
        assign = {int(k): v for k, v in p["assign"].items()}
        n = len(t["grid"])
        canvas = [[None] * n for _ in range(n)]
        words = []
        for s in slots:
            w = assign.get(s["id"])
            if w is None:
                issues["빈 슬롯"] += 1
                continue
            words.append(w)
            if len(w) != s["len"]:
                issues["길이 불일치"] += 1
            if w not in pool:
                issues["풀 미존재"] += 1
            for ch, (r, c) in zip(w, s["cells"]):
                if canvas[r][c] is not None and canvas[r][c] != ch:
                    issues["교차 글자 충돌"] += 1
                canvas[r][c] = ch
        if len(words) != len(set(words)):
            issues["단어 중복"] += 1

    print(f"검증 퍼즐 {checked}개")
    if not issues:
        print("  절대 규칙 위반 없음 (빈 슬롯/길이/교차/중복/풀존재 모두 통과)")
    else:
        for k, v in issues.items():
            print(f"  위반 [{k}]: {v}건")


if __name__ == "__main__":
    main()
