#!/usr/bin/env python3
"""
2단계: 가중치 답안 풀(answer pool) 구축.

1단계 산출물(vocab.json, keyword_tokens.json)을 받아 티어별 답안 단어를 정리한다.
티어 우선순위(중복 시): core > marker > name > general.

규칙(사용자 결정):
 - 키워드 복합어는 결합 토큰(climate change -> climatechange) 사용.
 - 코어 복합어가 결합 후 그리드 길이를 초과하면 구성 단어로 분절(불용어 제거).
 - 코어 키워드는 코퍼스 미등장이어도 강제 포함.
 - 마커/이름은 코퍼스 등장(freq>0) + 격자 적합(3~grid)만 채택.
 - 일반 어휘는 빈도 임계값 이상 + 격자 적합.

산출물:
  data/wordpool.json   token -> {length, tier, weight, corpus_freq, doc_freq, sources, origin, forced}
  data/wordpool_report.json + 콘솔 요약 (티어별 수, 코어 커버리지, 분절 내역, 슬롯/중복상한 제안)
"""
import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIER_RANK = {"core": 3, "marker": 2, "name": 1, "general": 0}


def load_config():
    import yaml
    with open(os.path.join(ROOT, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    cfg = load_config()
    data_dir = os.path.join(ROOT, cfg["paths"]["data_dir"])
    G = cfg["grid"]["size"]
    min_len = cfg["vocab"]["min_len"]
    max_len = min(cfg["vocab"]["max_len"], G)
    thr = cfg["vocab"]["candidate_min_count"]
    weights = cfg["weights"]
    stop = set(cfg["keywords"]["split_stopwords"])
    split_core = cfg["keywords"]["split_oversize_core"]
    force_core = cfg["keywords"]["force_include_core"]

    vocab = json.load(open(os.path.join(data_dir, "vocab.json"), encoding="utf-8"))
    keywords = json.load(open(os.path.join(data_dir, "keyword_tokens.json"), encoding="utf-8"))

    pool = {}        # token -> record
    dropped = {"single_core_too_long": [], "marker_name_oversize": [],
               "marker_name_absent": [], "split_stopword_drop": []}
    split_detail = []

    def add(token, tier, corpus_freq, origin, forced=False):
        if not (min_len <= len(token) <= max_len):
            return False
        cur = pool.get(token)
        if cur and TIER_RANK[cur["tier"]] >= TIER_RANK[tier]:
            # 이미 더 높은(또는 같은) 티어로 존재 -> 기원만 누적
            cur["origins"].add(origin)
            return False
        info = vocab.get(token, {})
        rec = {
            "token": token,
            "length": len(token),
            "tier": tier,
            "weight": weights[tier],
            "corpus_freq": info.get("count", corpus_freq),
            "doc_freq": info.get("doc_freq", 0),
            "sources": info.get("sources", []),
            "origins": (cur["origins"] if cur else set()) | {origin},
            "forced": forced and info.get("count", corpus_freq) == 0,
        }
        pool[token] = rec
        return True

    # --- 키워드 처리 ---
    core_represented = {}  # 코어 phrase -> 풀에 들어간 토큰 리스트 (커버리지 측정)
    for k in keywords:
        tier = k["tier"]
        tok = k["token"]
        n_words = k["n_words"]
        cfreq = k["corpus_freq"]
        if tier == "core":
            reps = []
            if len(tok) <= max_len:
                forced = force_core
                if add(tok, "core", cfreq, f"keyword:{k['phrase']}", forced=forced):
                    reps.append(tok)
                elif tok in pool:
                    reps.append(tok)
            elif n_words > 1 and split_core:
                comps = k["norm_spaced"].split()
                for w in comps:
                    if w in stop or len(w) < min_len:
                        dropped["split_stopword_drop"].append((k["phrase"], w))
                        continue
                    if add(w, "core", vocab.get(w, {}).get("count", 0),
                           f"split:{k['phrase']}", forced=force_core) or w in pool:
                        reps.append(w)
                split_detail.append({"phrase": k["phrase"], "components": comps,
                                     "kept": [w for w in comps
                                              if w not in stop and len(w) >= min_len]})
            else:
                # 분절 불가 단일 장단어
                dropped["single_core_too_long"].append((k["phrase"], len(tok)))
            core_represented[k["phrase"]] = reps
        else:  # marker / name
            if len(tok) > max_len:
                dropped["marker_name_oversize"].append((tier, k["phrase"], len(tok)))
                continue
            if cfreq <= 0:
                dropped["marker_name_absent"].append((tier, k["phrase"]))
                continue
            add(tok, tier, cfreq, f"keyword:{k['phrase']}")

    # --- 일반 어휘 ---
    for token, info in vocab.items():
        if info["count"] >= thr and min_len <= len(token) <= max_len:
            if token not in pool:
                add(token, "general", info["count"], "general")

    # origins set -> 정렬 리스트 (JSON 직렬화)
    for rec in pool.values():
        rec["origins"] = sorted(rec["origins"])

    # 저장
    json.dump(pool, open(os.path.join(data_dir, "wordpool.json"), "w",
              encoding="utf-8"), ensure_ascii=False)

    # --- 통계 ---
    by_tier = collections.Counter(r["tier"] for r in pool.values())
    len_dist = collections.Counter(r["length"] for r in pool.values())
    forced_n = sum(1 for r in pool.values() if r["forced"])
    core_covered = sum(1 for reps in core_represented.values() if reps)

    # 슬롯/중복상한 추정 (17x17 fully-checked 대략 단어 수)
    # 미국식 fully-checked 대략 단어수 ~ size*size*0.27 (15x15=78 근사) -> 17x17 ~78~84
    est_words = round(G * G * 0.27)
    target_puzzles = 200
    total_slots = est_words * target_puzzles

    report = {
        "grid": G, "max_len": max_len, "general_threshold": thr,
        "pool_size": len(pool),
        "by_tier": dict(by_tier),
        "forced_core_absent_in_corpus": forced_n,
        "core_phrases_total": len(core_represented),
        "core_phrases_represented": core_covered,
        "length_distribution": dict(sorted(len_dist.items())),
        "dropped_counts": {k: len(v) for k, v in dropped.items()},
        "est_words_per_puzzle": est_words,
        "target_puzzles": target_puzzles,
        "est_total_slots": total_slots,
    }
    json.dump({**report,
               "dropped_detail": dropped,
               "split_detail": split_detail},
              open(os.path.join(data_dir, "wordpool_report.json"), "w",
                   encoding="utf-8"), ensure_ascii=False, indent=2)

    # --- 콘솔 ---
    print("=" * 60)
    print(f"답안 풀 구축 완료 (grid {G}x{G}, max_len {max_len}, 일반 임계값 >={thr})")
    print(f"  총 풀 크기: {len(pool):,}")
    print(f"  티어별: {dict(by_tier)}")
    print(f"  코어 강제포함(코퍼스 미등장): {forced_n}")
    print(f"  코어 phrase 커버리지: {core_covered}/{len(core_represented)}")
    print("\n[탈락 내역]")
    for k, v in dropped.items():
        print(f"  {k}: {len(v)}")
    if dropped["single_core_too_long"]:
        print("   - 분절불가 코어 장단어:",
              ", ".join(f"{p}({n})" for p, n in dropped["single_core_too_long"]))
    print("\n[풀 길이 분포]")
    for L in range(min_len, max_len + 1):
        print(f"  len {L:2}: {len_dist.get(L,0):7,}")
    print("\n[슬롯/중복 상한 추정]")
    print(f"  추정 단어수/퍼즐 ≈ {est_words}, 목표 {target_puzzles}퍼즐")
    print(f"  총 슬롯 ≈ {total_slots:,}")
    print("=" * 60)


if __name__ == "__main__":
    main()
