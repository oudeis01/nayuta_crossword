#!/usr/bin/env python3
"""B단계-2: 주제 게이트 검증 하니스 (이방성 교정 전/후 변별력 측정).

피자 테스트(E5 cone effect)의 재현을 막기 위해, 게이트를 적용하기 전에 임베딩이
실제로 '주제어'와 '비주제어(아티팩트/보일러플레이트)'를 구분하는지 직접 검증한다.

설계:
 - 앵커 = core+marker 티어 단어 센트로이드의 80% (담론 주제 표현).
 - 양성(positive) = 나머지 20% core+marker (주제어여야 하므로 높은 점수 기대).
 - 음성(negative) = 코퍼스 보일러플레이트(newsletter, copyright...) + 알려진 아티팩트.
 - 점수 = 단어 센트로이드와 앵커 집합의 상위-k 평균 코사인.
 - raw vs (평균중심화 + soft-ZCA whitening) 두 조건에서 점수 분포와 ROC-AUC 비교.
   cone effect가 있으면 raw AUC ~ 0.5, 점수범위 압축. 화이트닝이 효과적이면 AUC 상승.

입력 : data/pool_centroids.npy, data/pool_centroids_words.json
산출 : data/gate_validation.json + 콘솔 요약 (alpha 후보별 AUC/분리도)
"""
import json, os, sys, numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# 코퍼스에 흔하지만 주제와 무관한 보일러플레이트/일반어(음성 대조군 후보)
BOILERPLATE = """newsletter subscribe copyright website email phone address contact login
password cookie cookies privacy terms account password monday tuesday wednesday thursday
friday saturday sunday january february march april august september october november december
click download upload register username homepage sitemap faq helpdesk advertisement
""".split()
# 알려진 잔존 아티팩트(누락공백/조각)
ARTIFACTS = "aet taten andn paradoxa habibrania alserkalavenue mondialit".split()
TOPK = 10          # 앵커 상위 k 평균
ALPHAS = [1.0, 0.1, 0.05, 0.01, 1e-3]   # soft-ZCA 정규화 강도 후보


def fit_whiten(M, alpha):
    """평균중심화 + soft-ZCA. 반환: (mu, W) 변환기."""
    mu = M.mean(axis=0)
    Xc = M - mu
    C = (Xc.T @ Xc) / max(1, Xc.shape[0])
    s, U = np.linalg.eigh(C)            # 대칭 → eigh
    s = np.clip(s, 0, None)
    W = U @ np.diag(1.0 / np.sqrt(s + alpha)) @ U.T
    return mu, W.astype("float32")


def apply_whiten(X, mu, W):
    Y = (X - mu) @ W
    n = np.linalg.norm(Y, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return (Y / n).astype("float32")


def topk_score(X, A, k):
    """각 X행에 대해 앵커 A와의 상위-k 코사인 평균(둘 다 L2정규화 가정)."""
    sims = X @ A.T                      # [nx, na]
    k = min(k, A.shape[0])
    part = np.partition(sims, -k, axis=1)[:, -k:]
    return part.mean(axis=1)


def auc(pos, neg):
    """ROC-AUC = P(pos점수 > neg점수). Mann-Whitney U / (n*m)."""
    allv = np.concatenate([pos, neg])
    order = allv.argsort()
    ranks = np.empty_like(order, dtype="float64")
    ranks[order] = np.arange(1, len(allv) + 1)
    # 동점 평균순위 보정
    _, inv, cnt = np.unique(allv, return_inverse=True, return_counts=True)
    csum = np.cumsum(cnt)
    avg_rank = {}
    start = 0
    for i, c in enumerate(cnt):
        avg_rank[i] = (start + 1 + start + c) / 2.0
        start += c
    ranks = np.array([avg_rank[i] for i in inv])
    n = len(pos); m = len(neg)
    rpos = ranks[:n].sum()
    return (rpos - n * (n + 1) / 2.0) / (n * m)


def main():
    M = np.load(os.path.join(DATA, "pool_centroids.npy"))
    meta = json.load(open(os.path.join(DATA, "pool_centroids_words.json"), encoding="utf-8"))
    idx = {m["token"]: i for i, m in enumerate(meta)}
    has = np.array([m["n_sent"] > 0 for m in meta])

    rng = np.random.default_rng(0)
    anchors_all = [i for i, m in enumerate(meta)
                   if m["tier"] in ("core", "marker") and m["n_sent"] > 0]
    anchors_all = np.array(anchors_all)
    rng.shuffle(anchors_all)
    n_anchor = int(len(anchors_all) * 0.8)
    anchor_idx = anchors_all[:n_anchor]
    pos_idx = anchors_all[n_anchor:]

    neg_words = [w for w in BOILERPLATE + ARTIFACTS if w in idx and has[idx[w]]]
    neg_idx = np.array([idx[w] for w in neg_words])
    print(f"앵커 {len(anchor_idx)} | 양성(held-out theme) {len(pos_idx)} | "
          f"음성(보일러+아티팩트) {len(neg_idx)}: {neg_words}", flush=True)

    results = {}
    # raw
    A = M[anchor_idx]
    sp = topk_score(M[pos_idx], A, TOPK)
    sn = topk_score(M[neg_idx], A, TOPK)
    results["raw"] = {"auc": round(float(auc(sp, sn)), 4),
                      "pos_mean": round(float(sp.mean()), 4),
                      "neg_mean": round(float(sn.mean()), 4),
                      "pos_std": round(float(sp.std()), 4),
                      "all_std": round(float(topk_score(M[has], A, TOPK).std()), 4)}
    # whitened (alpha 후보별)
    for a in ALPHAS:
        mu, W = fit_whiten(M[has], a)
        Mw = apply_whiten(M, mu, W)
        Aw = Mw[anchor_idx]
        sp = topk_score(Mw[pos_idx], Aw, TOPK)
        sn = topk_score(Mw[neg_idx], Aw, TOPK)
        results[f"whiten_a{a}"] = {
            "auc": round(float(auc(sp, sn)), 4),
            "pos_mean": round(float(sp.mean()), 4),
            "neg_mean": round(float(sn.mean()), 4),
            "pos_std": round(float(sp.std()), 4),
            "all_std": round(float(topk_score(Mw[has], Aw, TOPK).std()), 4)}

    json.dump(results, open(os.path.join(DATA, "gate_validation.json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n" + "=" * 70)
    print(f"{'조건':16} {'AUC':>7} {'pos평균':>8} {'neg평균':>8} {'pos표준':>8} {'전체표준':>8}")
    for k, v in results.items():
        print(f"{k:16} {v['auc']:>7} {v['pos_mean']:>8} {v['neg_mean']:>8} "
              f"{v['pos_std']:>8} {v['all_std']:>8}")
    print("=" * 70)
    print("AUC 1.0=완벽분리, 0.5=무변별(cone effect 의심). 전체표준↑=점수분포 펴짐.", flush=True)


if __name__ == "__main__":
    main()
