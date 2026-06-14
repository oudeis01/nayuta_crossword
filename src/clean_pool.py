#!/usr/bin/env python3
"""Phase 2: 풀 정제(삭제 트랙) - general tier 글루어를 allowlist + 코퍼스 신호로 정제.

기본은 DRY-RUN(풀 미수정): 생존/제거 통계·표본 출력 + 제거 토큰을
data/removed_general.json 에 저장(검토용). CW_APPLY=1 이면 실제 wordpool.json 수정+백업.
보호 tier(core/marker/name/theme)는 절대 건드리지 않는다.

게이트 철학(데이터로 확정):
  - 크로스워드 워드리스트(broda/common)는 '진짜 답어' 양성 필터. 단, 유명 인명·약어·
    외국어 crosswordese 도 답으로 일부러 담으므로(EST/ERE=70, CSI/NES=80) 그것들의
    제거에는 못 쓴다. 제거는 코퍼스 신호·영어성 신호로 따로 한다.
  - 영어성 게이트(2026-06-11 추가, 수동검증에서 비영어 163개 통과 발견):
      english_ok = zipf_en≥ZEN  OR  (사전수록(복수형 포함) AND zipf_en≥ZLO)
    단 est/que/dans 같은 외국어 기능어는 영어 코퍼스 혼입으로 zipf_en 이 높아
    zipf 만으론 못 잡는다 → 외국어 스탑워드(fr/de/es/it/nl/pt) 차감을 병행.
    이때 aura/ante/bin/door/over 같은 영어 정당어 충돌은 보호:
      보호 = w∈common.owl  OR  zipf_en≥FSHI  OR  (사전수록 AND zipf_en≥FSLO)
  - 인명/약어 제거는 '우리 코퍼스의 대문자 신호'로 한다(전수, NER 비의존).
    그러나 미술 코퍼스에선 iris/viola/zen/salon 같은 흔한 단어도 고유명사로 자주
    대문자화돼 cap 만으론 인명과 분리 불가(zen 0.89 vs selene 0.86). 그래서 사전과
    결합한 2단 규칙을 쓴다:
      고유명사 제거 = cap_ratio≥CAP_HI  OR  (cap_ratio≥CAP_LO AND 사전 미수록)
    → 확실한 인명(renoir/dante/fagan/epps; 고cap 또는 비사전)은 제거,
      사전수록 흔한단어(iris/viola/zen/salon)는 보존.
    약어 제거 = allcaps_ratio≥ACRO  OR  (allcaps_ratio≥ACRO2 AND 사전 미수록).
  - 인명사전 교차(2026-06-11 결정): NLTK names ∧ cap≥CAP_LO ∧ z<FSHI 제거.
    사전수록+중간cap 인명(annie/rebecca/ken/eva, cap 0.5~0.89 약 1,096개)이 2단
    규칙을 빠져나가는 잔존 덩어리 해소. viola/iris/hazel 동반 손실은 수용
    (이들의 코퍼스 용례도 인명 위주라 힌트 품질상 실손실 작음), rose/june 등
    고빈도어는 z≥FSHI 로 보호.
  - 사용자 keep-list(data/keep_words.json)는 모든 제거 규칙에 우선해 보존.

판정(general tier, w):
  keep-list → 무조건 유지
  멤버십(양성): w∈common.owl  또는  (broda_score(w) ≥ 길이별 바닥 AND english_ok)
  음성 제거   : 외국어 스탑워드(보호 제외) / 고유명사 / 약어 / 복원이름 비사전조각
  → 멤버십 통과 ∧ 음성 미해당 이면 유지.

환경 : CW_S3(len3 broda 바닥, 기본 70), CW_S4(len>=4 바닥, 기본 50),
        CW_ZEN(영어성 zipf 단독 임계, 기본 3.0), CW_ZLO(사전결합 zipf 바닥, 기본 2.0),
        CW_FSHI(스탑워드 보호 zipf 단독, 기본 4.5), CW_FSLO(사전결합 보호, 기본 3.3),
        CW_CAPHI(고cap 단독 제거 임계, 기본 0.9),
        CW_CAPLO(비사전 결합 제거 임계, 기본 0.5), CW_ACRO(약어 임계, 기본 0.5),
        CW_ACRO2(비사전 결합 약어 임계, 기본 0.35),
        CW_APPLY(=1 이면 실제 수정+백업)
입력 : data/wordpool.json, data/cap_signals.json(scan_caps.py 산출),
        data/keep_words.json(선택), vendor/crossword-owl/wordlists/{common,broda}.owl
"""
import json, os, random, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OWL = os.path.join(ROOT, "vendor", "crossword-owl", "wordlists")
PROTECTED = {"core", "marker", "name", "theme"}


def load_common():
    p = os.path.join(OWL, "common.owl")
    return {l.strip().lower() for l in open(p, encoding="utf-8")
            if l.strip() and l.strip() != "word"}


def load_broda():
    """소문자 폴딩 단일 알파토큰 -> 최고점. (broda 는 대소문자로 인명/일반어를 구분 안 함.)"""
    p = os.path.join(OWL, "broda.owl")
    broda = {}
    for l in open(p, encoding="utf-8"):
        if "," not in l:
            continue
        w, _, s = l.rpartition(",")
        if not w.isalpha():
            continue
        try:
            sc = int(s)
        except ValueError:
            continue
        lw = w.lower()
        broda[lw] = max(broda.get(lw, 0), sc)
    return broda


def main():
    S3 = float(os.environ.get("CW_S3", "70"))
    S4 = float(os.environ.get("CW_S4", "50"))
    ZEN = float(os.environ.get("CW_ZEN", "3.0"))
    ZLO = float(os.environ.get("CW_ZLO", "2.0"))
    FSHI = float(os.environ.get("CW_FSHI", "4.5"))
    FSLO = float(os.environ.get("CW_FSLO", "3.3"))
    CAP_HI = float(os.environ.get("CW_CAPHI", "0.9"))
    CAP_LO = float(os.environ.get("CW_CAPLO", "0.5"))
    ACRO = float(os.environ.get("CW_ACRO", "0.5"))
    ACRO2 = float(os.environ.get("CW_ACRO2", "0.35"))
    apply = os.environ.get("CW_APPLY") == "1"

    pool = json.load(open(os.path.join(DATA, "wordpool.json"), encoding="utf-8"))
    cap = json.load(open(os.path.join(DATA, "cap_signals.json"), encoding="utf-8"))
    common = load_common()
    broda = load_broda()
    print(f"[게이트] S3={S3} S4={S4} ZEN={ZEN} ZLO={ZLO} FSHI={FSHI} FSLO={FSLO} "
          f"CAP_HI={CAP_HI} CAP_LO={CAP_LO} ACRO={ACRO} | common {len(common):,} broda {len(broda):,}")

    # 사전 D(NLTK ∪ web2): 고유명사 2단 규칙·영어성 게이트의 사전 판정에 사용.
    from nltk.corpus import words as nw
    from english_words import get_english_words_set
    D = set(w.lower() for w in nw.words()) | {w.lower() for w in get_english_words_set(["web2"], lower=True)}

    def in_dict(w):
        """사전수록(단순 복수형 포함). D 는 복수형이 거의 없어 -s/-es 를 어간으로 환원.
        단 어간이 4글자 미만이면 불인정: dans→dan, ades→ade, ches→che 같은 거짓
        적중이 외국어/인명을 사전어로 둔갑시킨다(taboos/talons/auras/states 는 보호)."""
        if w in D:
            return True
        if w.endswith("s") and len(w) >= 5 and w[:-1] in D:
            return True
        if w.endswith("es") and len(w) >= 6 and w[:-2] in D:
            return True
        return False

    # 영어 zipf (wordfreq). 외국어 기능어는 영어 코퍼스 혼입으로 높게 나올 수 있음에 유의.
    from wordfreq import zipf_frequency

    # 인명사전(NLTK names): 사전수록+중간cap 인명 잔존 덩어리 교차 제거용.
    from nltk.corpus import names as nltk_names
    NAMES = {n.lower() for n in nltk_names.words()}

    # 외국어 스탑워드(fr/de/es/it/nl/pt, len>=3, 영어 스탑워드 제외)
    from nltk.corpus import stopwords
    fstop = set()
    for lg in ("french", "german", "spanish", "italian", "dutch", "portuguese"):
        fstop |= {x.lower() for x in stopwords.words(lg) if x.isalpha() and len(x) >= 3}
    fstop -= {x.lower() for x in stopwords.words("english")}

    # 사용자 keep-list: 모든 제거 규칙에 우선 (to-keep.md 큐레이션, 용례 힌트 고정과 짝).
    keep = set()
    kp_path = os.path.join(DATA, "keep_words.json")
    if os.path.exists(kp_path):
        keep = set(json.load(open(kp_path, encoding="utf-8")).keys())
        print(f"  keep-list {len(keep)}개 로드")

    # 복원 이름의 '비사전 구성토큰'(성씨 등) = 단독 조각이면 제거 대상.
    # in_dict(복수형 인식)를 써야 unitedstates 의 'states' 같은 정상 단어가 조각으로 안 잡힌다.
    name_frags = set()
    rn_path = os.path.join(DATA, "recovered_names.json")
    if os.path.exists(rn_path):
        rn = json.load(open(rn_path, encoding="utf-8"))
        for v in rn.values():
            for t in v["parts"]:
                # 고빈도 영어(z≥FSHI)는 면제: 기관명 parts 의 'arts'(어간 art 가 3글자라
                # 복수형 가드에 걸려 사전 불인정) 같은 필수 글루어 보호.
                if not in_dict(t) and zipf_frequency(t, "en") < FSHI:
                    name_frags.add(t)

    def fs_protected(w):
        """외국어 스탑워드의 영어 정당어 보호. 복수형은 단수형의 보호를 상속
        (auras 는 aura 가 보호되므로 보호; 어간 4글자 미만은 dans→dan 방지로 불상속)."""
        z = zipf_frequency(w, "en")
        if w in common or z >= FSHI or (in_dict(w) and z >= FSLO):
            return True
        if w.endswith("s") and len(w) >= 5 and w[:-1] in D:
            return fs_protected(w[:-1])
        return False

    def reason(w, freq=0):
        """제거 사유(없으면 None=유지)."""
        if w in keep:
            return None                # 사용자 keep-list 우선
        cs = cap.get(w, {})
        # 토크나이저 불일치 유령(RC5): 풀 구축(build_vocab)은 아포스트로피를 삭제-결합
        # (else's→elses, L'Oréal→loreal)하지만 scan_caps/mine_sentences 는 분리한다.
        # 그래서 이런 토큰은 cap 신호 0(인명 게이트 발화 불가) + 용례 0(힌트 없음).
        nocc = cs.get("n_occ", 0)
        if nocc == 0:
            return "유령"              # 스캔 토크나이저 기준 코퍼스 미등장
        # 부분 유령: 문자 그대로도 드물게 등장(독일어 속격 Freuds 등)하지만 빌드 freq 가
        # 결합 유입으로 크게 부풀려진 경우(thats 7287/15, citys 2679/19). dart(d'art 결합
        # + 진짜 dart 123회)는 사전수록 AND 실측 n_occ>=50 으로 보호.
        if freq >= 20 and freq / nocc >= 10 and not (in_dict(w) and nocc >= 50):
            return "소유격유령"
        L = len(w)
        floor = S3 if L == 3 else S4
        z = zipf_frequency(w, "en")
        english_ok = z >= ZEN or (in_dict(w) and z >= ZLO)
        member = (w in common) or (broda.get(w, 0) >= floor and english_ok)
        if not member:
            return "비멤버십"          # 파편/비단어/비영어(목록 미수록·점수 미달·영어성 미달)
        if w in fstop and not fs_protected(w):
            return "외국어"            # 외국어 기능어(영어 정당어 보호 제외)
        cr = cs.get("cap_ratio") or 0
        # 중간cap 비사전 규칙은 고빈도 영어(z≥FSHI)는 면제: arts(0.60, 사전엔 단수 art 만,
        # z4.7) 같은 필수 글루어가 미술 코퍼스 대문자화로 오인 제거되는 것 방지.
        if cr >= CAP_HI or (cr >= CAP_LO and not in_dict(w) and z < FSHI):
            return "고유명사"          # 인명/지명 (고cap 또는 비사전·중cap)
        if w in NAMES and cr >= CAP_LO and z < FSHI:
            return "고유명사"          # 사전수록 인명 (인명사전 교차)
        acro = cs.get("allcaps_ratio") or 0
        if acro >= ACRO or (acro >= ACRO2 and not in_dict(w)):
            return "약어"
        if w in name_frags:
            return "이름조각"
        return None

    kept, removed = [], collections.OrderedDict()
    rcount = collections.Counter()
    for w, r in pool.items():
        if r["tier"] != "general":
            continue
        why = reason(w, r.get("corpus_freq") or 0)
        if why is None:
            kept.append(w)
        else:
            removed[w] = why
            rcount[why] += 1

    json.dump(sorted(removed), open(os.path.join(DATA, "removed_general.json"), "w",
              encoding="utf-8"), ensure_ascii=False)

    gen_total = len(kept) + len(removed)
    klen = collections.Counter(len(w) for w in kept)
    rlen = collections.Counter(len(w) for w in removed)
    print(f"general {gen_total:,} → 유지 {len(kept):,} / 제거 {len(removed):,}")
    print(f"  제거 사유: {dict(rcount)}")
    print("  길이별 유지/제거 (3~8):")
    for L in range(3, 9):
        print(f"    len{L}: 유지 {klen[L]:6,} / 제거 {rlen[L]:6,}")

    # 길이별 제거 사유 표본
    random.seed(0)
    for L in (3, 4, 5, 6):
        samp = [w for w in removed if len(w) == L]
        print(f"\n  len{L} 제거 표본: " + " ".join(
            f"{w}<{removed[w]}>" for w in sorted(random.sample(samp, min(40, len(samp))))))

    if apply:
        import shutil
        shutil.copyfile(os.path.join(DATA, "wordpool.json"),
                        os.path.join(DATA, "wordpool.preclean.bak.json"))
        for w in removed:
            del pool[w]
        json.dump(pool, open(os.path.join(DATA, "wordpool.json"), "w", encoding="utf-8"),
                  ensure_ascii=False)
        dist = collections.Counter(v["tier"] for v in pool.values())
        print(f"\n[APPLY] {len(removed):,}개 제거 완료. 백업 wordpool.preclean.bak.json")
        print(f"  최종 tier 분포: {dict(dist)}")


if __name__ == "__main__":
    main()
