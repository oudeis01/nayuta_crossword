# 십자말풀이 자동 생성 연구 노트

작성일 2026-06-06. 목적: (1) 지금까지 우리 구현에서 발견된 문제를 정리하고, (2) 십자말풀이
생성을 다룬 실존 학술 문헌을 모아 우리 문제와 매핑한다. 모든 참고 문헌은 실제 논문이며 링크를
함께 명시한다.

---

## 1부. 우리 구현에서 발견된 문제 정리

우리 파이프라인은 두 단계 분리 구조다. (3a) 검은 칸 기하만으로 유효 템플릿 뱅크 생성
(`gen_templates.py`), (3b) 코퍼스 단어로 CSP 백트래킹 채우기(`fill.py`, 병렬 드라이버
`generate.py`). 이 구조에서 관측된 문제는 다음과 같다.

### P1. 채우기 성공률이 낮음 (핵심 병목)
- 증상: 20초 예산으로 50개 템플릿 중 6개만 채워짐.
- 원인: 템플릿 뱅크가 기하 규칙만 통과시키다 보니, 16~17자 슬롯이 4~7개씩 서로 교차하는
  사실상 채우기 불가능한 격자가 다수 생성됨. 풀에 17자 단어가 ~325개뿐이라, 긴 슬롯끼리
  교차하면 동시에 만족시킬 조합이 거의 없음.
- 현재 조치: `fillability_ok()` 추가. 긴 슬롯(>=12자) 개수 상한, 초장 슬롯(>=15자) 상한,
  긴 슬롯끼리 교차 금지. 재생성 결과 798회 시도 중 736개가 이 제약으로 탈락, 60개 확보.
  (성공률 재측정은 아직 미완료.)

### P2. 채우기 알고리즘 thrashing (해결됨)
- 증상: 첫 `fill.py`가 5분 이상 CPU를 먹고도 템플릿 1개를 못 끝냄.
- 원인: 매 노드에서 미배정 슬롯 ~86개 전부의 후보를 재계산하고 수천 개를 재정렬.
- 조치: 증분 도메인 캐싱으로 재작성. 배치 시 교차 슬롯의 도메인만 글자 필터로 축소하고
  이전 상태를 저장/복원. 도메인을 가중치 내림차순 리스트로 유지해 노드당 정렬 비용 0.

### P3. 결정론적 재시작이 무의미 (해결됨)
- 증상: 재시작을 돌려도 동일 경로를 반복.
- 조치: 재시작마다 길이 버킷을 `(-weight, rng.random())`로 재정렬. 동률(general weight=1)이
  매번 다르게 섞여 경로 다양성 확보, 노드당 비용 0.

### P4. 병렬화의 실제 효과 범위
- 단일 격자 채우기는 본질적으로 단일 스레드 백트래킹이라 코어 1개만 쓴다.
- 병렬화가 의미 있는 지점은 두 가지뿐: (a) 200개 퍼즐을 워커에 분배, (b) 어려운 템플릿에
  대한 병렬 재시작 race. `generate.py`가 이를 구현. 단, 템플릿이 채우기 불가능하면
  30코어가 함께 thrashing하므로 P1 해결이 병렬화의 전제 조건.

### P5. 어휘 품질 (미해결, 사용자 결정 필요)
- 빈도 임계값만 사용(사전 검증 없음)하다 보니 고유명사, OCR 잡토큰, 외래어가 답안 풀에
  섞임. 실제 채우기 결과에서 GOMORRAH, OSNABRUECK, BESCHREIBT 관측.
- 트레이드오프: 사전 검증을 넣으면 전문어/고유명사(작가명 등 name 티어)가 같이 탈락.

### P6. 복합어 결합으로 키워드 손실
- concat 정책으로 결합 후 그리드 길이(17)를 넘는 키워드 234/573개가 탈락.
- core 티어는 분절(split_oversize_core)로 일부 회수하지만, marker/general은 그대로 손실.

### P7. 퍼즐당 테마 단어 수가 적음
- 가중치 value ordering만으로는 themed 단어가 퍼즐당 평균 ~3개에 그침.
- 사용자 요구(core 高, marker 中 빈도)를 만족하려면 테마 단어를 적극적으로 우선 배치하는
  별도 메커니즘이 필요.

### P8. 교차-퍼즐 중복 상한 미정
- 같은 단어가 여러 퍼즐에 등장하는 것은 허용하되 상한이 필요. 첫 배치 생성 후 실제 분포를
  보고 확정하기로 함. (테마 단어 556개 대비 슬롯 ~15,600개라 일반어 재사용은 불가피.)

---

## 2부. 관련 학술 문헌 (실존 논문, 링크 명시)

십자말풀이 생성/풀이는 제약충족문제(CSP)의 고전적 벤치마크로 1990년대부터 깊이 연구되었다.
우리 문제와 직접 관련된 순서로 정리한다.

### A. 생성 문제를 CSP로 본 고전 및 핵심 연구

1. **Ginsberg, Frank, Halpin, Torrance (1990) — "Search Lessons Learned from Crossword
   Puzzles."** AAAI-90, pp.210-215.
   링크: https://cdn.aaai.org/AAAI/1990/AAAI90-032.pdf
   - 빈 프레임에 사전 단어를 채워 퍼즐을 *생성*하는 프로그램. 어려운 문제일수록 제약의
     동적 순서화(dynamic ordering)가 필수임을 보임. 변수/값 선택 순서가 성능을 좌우.

2. **Beacham, Chen, Sillito, van Beek (2001) — "Constraint Programming Lessons Learned
   from Crossword Puzzles."** Canadian AI 2001 (LNCS 2056), pp.78-87.
   링크: https://link.springer.com/chapter/10.1007/3-540-45153-6_8
   - 우리 fill 설계와 가장 직접적으로 관련. 세 가지 설계 결정(제약 모델, 탐색 알고리즘,
     휴리스틱)의 상호작용을 십자말풀이 생성으로 분석. 모델 3종(비이진 표현, dual encoding,
     hidden variable encoding), 휴리스틱 2종(minimum domain = MRV, domain/degree),
     알고리즘(forward checking vs generalized arc consistency)을 비교.
   - 핵심 결론: 모델/알고리즘/휴리스틱은 독립적으로 정할 수 없고 상호작용한다.

3. **Ginsberg & McAllester (1994) — "GSAT and Dynamic Backtracking."**
   링크: https://cdn.aaai.org/ARPI/1996/ARPI96-019.pdf
   - 십자말풀이 생성 CSP를 테스트베드로 사용. Dynamic Backtracking(DBT, 충돌 지향 백점프의
     일종)이 고정 시간 내 더 많은 문제를 풂을 실험으로 보임. 우리의 단순 시간순 백트래킹을
     개선할 여지(충돌 원인으로 점프).

### B. 가중/확률 기반 값 선택 (우리 티어 가중치와 직접 대응)

4. **Shazeer, Littman, Keim (1999) — "Solving Crossword Puzzles as Probabilistic
   Constraint Satisfaction."** AAAI-99. (PROVERB 솔버)
   링크: https://www.researchgate.net/publication/2268315_Solving_Crossword_Puzzles_as_Probabilistic_Constraint_Satisfaction
   - 풀이 문제이지만, 단어에 확률/선호도를 부여하고 그 가중치로 탐색을 유도하는 프레임이
     우리의 core/marker/name/general 가중치 value ordering과 같은 발상.

5. **Ginsberg (2011) — "Dr.Fill: Crosswords and an Implemented Solver for Singly
   Weighted CSPs."** JAIR 42:851-886.
   링크: https://arxiv.org/abs/1401.4597
   - 십자말풀이를 가중 CSP로 변환해 푸는 본격 솔버. 변수/값 선택 휴리스틱, limited
     discrepancy search(LDS) 변형, 후처리/분할 기법 제시. "단일 가중 CSP"라는 정식화가
     우리 가중치 채우기와 정확히 같은 범주.

5b. **Menz (Yale) — "Generating 3D Crosswords as a Weighted Constraint Satisfaction
   Problem."** Yale College (지도교수 Dragomir Radev, Dr.Fill 코드 제공 Matt Ginsberg).
   링크: https://yale-lily.github.io/public/michaelmenz.pdf
   - 주의: 제목이 "Generating"이지만 *격자 형태를 단어셋에서 만들어내는* 연구가 아니라,
     고정된 3D 큐브 기하(4x4x4, 5x5x5)를 채우는 연구다. 가중 CSP + branch & bound +
     limited discrepancy search(여기서 discrepancy = 이미 쓴 단어 재배치 시도) 사용.
     회전 대칭을 이용해 2D 해를 방향별로 쌓아 탐색 폭을 줄임. Dr.Fill에서 영감.
     우리 fill(가중치 + 백트래킹)과 같은 계열의 보강 참고이지, "격자 생성" 근거는 아님.

### C. 생성 전용(unconstrained) 및 테마 최대화 (우리 목표와 직접 일치)

6. **Agarwal & Joshi (2020) — "Automation Strategies for Unconstrained Crossword
   Puzzle Generation."** arXiv:2007.04663.
   링크: https://arxiv.org/abs/2007.04663
   - 어휘(와 선택적 격자 크기)만 주어진 상태에서 단어 배치와 격자 기하를 함께 결정하는
     문제. 단어 순열 순서가 격자 적합도에 주는 영향, 격자 크기 조정, 단어 적합도 지표,
     백트래킹을 다룸. 큰 격자도 빠르게 well-packed 생성. 우리의 기하+채우기 결합 단계와
     대응.

7. **Majima & Ishihara (2023) — "Generating News-Centric Crossword Puzzles As A
   Constraint Satisfaction and Optimization Problem."** CIKM 2023 (short paper).
   링크: https://arxiv.org/abs/2308.04688
   - 우리의 P7(테마 단어 최대화)과 가장 직접적으로 일치. "가능한 한 많은 뉴스 유래 단어를
     포함"을 제약충족 *및 최적화* 문제로 정식화하고, 답을 하나씩 백트래킹으로 채움.
     테마 단어가 적어도 테마 중심 퍼즐 생성이 가능함을 실험으로 보임. 우리의 core/marker
     비중 높이기 요구를 "충족 + 최적화"로 다루는 근거.

### D. 일반 배경 참고 (탐색 알고리즘 서베이)

8. **van Beek (2006) — "Backtracking Search Algorithms."** Handbook of Constraint
   Programming, Ch.4.
   링크: https://cs.uwaterloo.ca/~vanbeek/Publications/survey06.pdf
   - MRV(minimum remaining values), dom/degree, forward checking, 충돌 지향 백점프,
     no-good 학습 등 우리가 쓰는/검토할 기법의 표준 정리.

### 비학술 실무 참고 (논문 아님, 구분해 표기)

- Duchi, J. — "Crossword Puzzles and Constraint Satisfaction." Stanford 과제 보고서
  (peer-review 아님). 링크: http://ai.stanford.edu/~jduchi/projects/crossword_writeup.pdf

---

## 3부. 문제 → 문헌 해법 매핑

| 문제 | 관련 문헌 | 시사점 |
|---|---|---|
| P1 채우기 불가능 격자 | Beacham 2001, Agarwal 2020 | 기하 타당성과 채우기를 분리하되, 긴 슬롯 교차 제어는 합리적. 모델/휴리스틱 동시 튜닝 필요. |
| P2/P3 탐색 효율 | van Beek 2006, Ginsberg 1990, Beacham 2001 | MRV는 표준. forward checking vs GAC 선택지 존재. 동적 순서화가 어려운 인스턴스에 유효. |
| P2/P3 막다른 길 회피 | Ginsberg & McAllester 1994 | 단순 시간순 백트래킹 대신 충돌 지향 백점프(DBT)로 더 많은 인스턴스 해결 가능. |
| 가중치 value ordering | Shazeer 1999, Ginsberg 2011 | 단어 선호도를 가중치로 정식화하는 것은 검증된 접근. 단일 가중 CSP 프레임 참고. |
| P7 테마 단어 최대화 | Majima & Ishihara 2023 | 테마 비중을 "제약충족 + 최적화"로 다루는 직접 선례. 단순 우선배치 외 최적화 목표 설정 가능. |

---

## 4부. 사용자 제안 검토: 단어셋에서 격자를 생성하는 방식 (CCPG vs UCPG)

사용자 질문: "템플릿을 고정시키고 맞추는 게 아니라, 주어진 단어셋 기반으로 최적화된 템플릿
(격자)을 찾아주는 방식은 없나?"

이 구분은 문헌에서 명확히 정의되어 있다.

- **CCPG (Constrained CPG, 우리 현재 방식)**: 격자 기하(검은 칸 배치)가 먼저 주어지고,
  거기에 단어를 채운다. Harris 등은 "기본 문제는 사실상 해결됨"이라 평가했고, Crossword
  Compiler/Crossfire/Phil 같은 상용 소프트웨어가 이 방식이다.
- **UCPG (Unconstrained CPG, 사용자가 말한 방식)**: 어휘(와 선택적 격자 크기)만 주고,
  단어 위치 *와 검은 칸 배치까지* 알고리즘이 결정한다. CCPG의 일반화.

UCPG의 직접 근거 논문이 우리가 이미 인용한 **Agarwal & Joshi (2020), arXiv:2007.04663**다.
본문을 직접 확인한 핵심 사실:

1. UCPG는 "테마 퍼즐처럼 손으로 고른 제한된 어휘"를 쓸 때 의미가 있다. 작은 어휘는 고정
   격자에서 해가 없을 수 있어, 격자 기하를 생성의 일부로 둔다. (우리 목표와 발상이 같음.)
2. 그러나 UCPG는 일반적으로 "거의 다루기 불가능(hopelessly intractable)"하다고 문헌이
   지적(Pershits & Stansifer). Agarwal & Joshi가 다루기 쉽게 만든 방법은 **자유형(freeform,
   criss-cross/Crozzle 계열) 격자**로 완화한 것이다.
3. 그들의 알고리즘은 대칭/fully-checked가 아니다. 랭킹된 단어 리스트에서 `pickWord`로
   교차 가능한 단어를 뽑아 `place`로 끼우고, 더 넣을 단어가 없으면 `victim`(그리디 제거)으로
   기존 단어를 빼서 backtrack한다. 결과물(예: 13x13에 단어 13개)은 **성기게 연결된 단어 망**
   이지, 우리 `rule.md`의 조밀한 대칭 미국식 격자가 아니다.

### 핵심 트레이드오프 (의사결정 필요)

UCPG를 채택하면 "단어셋에 맞춰 격자를 생성"하는 사용자 발상은 실현되지만, 우리가 이미
확정한 `rule.md`의 미국식 fully-checked 규칙(180도 대칭, 모든 흰 칸이 가로+세로 두 단어에
동시 소속, 검은 칸 최소화)을 **포기**하게 된다. 대칭 + fully-checked를 유지한 채 UCPG를
풀면 문헌이 말한 "intractable" 영역으로 들어간다.

미국식 규칙을 유지하면서 "단어셋 주도"의 이점을 취하는 현실적 절충안은 **테마 우선
(theme-first) 하이브리드**다. 실제 인간 구성가와 상용 소프트웨어가 쓰는 방식:
1. 테마 단어(우리의 core/marker)를 대칭 위치에 먼저 배치.
2. 그 배치와 양립하는 검은 칸 격자를 (대칭·fully-checked 유지하며) 구성/완성.
3. 나머지를 CCPG 채우기로 자동 완성.

이 절충안의 "테마 단어 최대화" 목표는 **Majima & Ishihara (2023), arXiv:2308.04688**이
"제약충족 + 최적화"로 정식화한 것과 일치한다(2부 7번 참조).

### 우리 상황에 대한 판단

- 우리 어휘는 작지 않다(일반어 풀 12만, 테마 556개). 따라서 UCPG의 본래 동기("작은 어휘라
  고정 격자에 해가 없음")는 약하다. 오히려 P1(채우기 불가능 템플릿)은 *템플릿 타당성 제어*로
  충분히 완화 가능한 문제다.
- 사용자 발상의 진짜 가치는 "격자를 단어에 맞춰 자유 생성"보다, "테마 단어가 더 많이/보기 좋게
  들어가도록 격자를 단어 인지 상태로 만드는 것"에 있다. 이는 미국식 규칙을 깨는 UCPG 전면
  채택보다, 테마 우선 하이브리드(P7 해법)로 얻는 게 더 안전하고 규칙과 양립한다.

- 우리 fill은 forward checking + MRV + 가중치 value ordering 조합이며, 이는 Beacham 2001과
  van Beek 2006 권고 범위 안에 있음. 개선 후보: (1) 충돌 지향 백점프 도입(Ginsberg DBT),
  (2) dom/degree 휴리스틱 비교, (3) 테마 단어를 최적화 목표로 명시(Majima & Ishihara).
- P5(어휘 품질)와 P6(키워드 손실)은 십자말풀이 알고리즘 문헌이 아니라 어휘 큐레이션 문제로,
  별도 결정 필요.

---

## 5부. 적용한 규칙 완화와 측정 결과 (2026-06-06)

사용자 결정: 현재 CCPG 방식 유지 + 테마 우선 시딩, 단 `rule.md` 관습 규칙(6~10)을 config
토글로 선택적 완화. 절대 규칙(1~5)은 항상 강제.

적용 내용 (`config.yaml`의 `rules:`/`theme:` 섹션):
- ⑥ 대칭: rotational 유지(검은 패턴 180도 대칭).
- ⑦ 검은 칸: 상한 16% → 22%, 하한 16%. cheater 허용. P1의 핵심 지렛대 (검은 칸↑ →
  슬롯 길이↓ → 채우기 용이).
- ⑧ 2x2 검은 블록 금지: 유지(외형 품질).
- ⑨ 코퍼스 실존: 유지(코어는 force_include_core 예외).
- ⑩ 테마 대칭 배치: 완화. 대신 테마 우선 시딩(채우기 전 테마 단어를 슬롯에 선배치,
  tiers=core/marker, prefer_long). Majima & Ishihara 2023의 충족+최적화 방향과 일치.

측정 결과(17x17, 30워커):
- 템플릿 재생성: 검은 칸 15.9~22.1%, 단어 80~104(평균 94). 생성 시도 798→238로 급감.
- 채우기 성공률: (이전) 20초 6/50 → (현재) 20초 48/60 단일시드, 3시드 race로 53/60 고유
  템플릿(88%).
- 테마 단어/퍼즐: (이전) ~3 → (현재) 평균 6.7~6.8 (min 4, max 11).
- 절대 규칙 검증(`src/validate_puzzles.py`): 132개 퍼즐 전부 위반 0 (빈 슬롯/길이/교차/중복/
  풀존재 통과).

남은 점:
- 7/60 템플릿은 3시드로도 미해결(까다로운 기하). 200개 생산엔 53개로 충분하나, 필요 시
  시드/시간 상향 또는 해당 템플릿 폐기.
- P5(어휘 잡토큰), P6(키워드 손실), P8(교차-퍼즐 중복 상한)은 여전히 열린 항목.
