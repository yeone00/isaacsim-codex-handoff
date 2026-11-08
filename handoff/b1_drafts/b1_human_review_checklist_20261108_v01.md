# B1 QA v02 사람 검토 체크리스트 (2026-11-08)

> **검토 전 상태다. 아래 판정 칸은 모두 비어 있다.** AI가 한 판독은 이 체크리스트의 검토로 치지 않는다.
> 검토자는 각 패널을 열어 칸을 채운다. 같은 내용을 `review_checklist.csv`의 빈 열에 적어도 된다.

## 패널 읽는 법

- 각 패널의 행은 HR / LR / CAD다.
- 열 1: RGB 원본 위에 윤곽선을 그렸다.
  - 초록: 공통 GT(HR canonical) mask
  - 빨강: 그 표현의 실제 load mask
- 열 2: YOLO 라벨 polygon(청록)을 RGB 위에 그렸다. canonical이 100px 미만이면 라벨이 없다고 표시된다.
- 열 3: load 주변을 잘라 확대한 RGB다.
- 열 4: 확대 영역의 `|I−E| > τ` 결과다. 흰색은 보이는 벽돌(빈 배경과 다름), 자홍은 가려진 부분이다. mask는 2px 침식했다.
- 행 왼쪽 글자
  - `vis` = vis_hard_e2(보임 비율)
  - `occ` = 1 − vis(가림 비율)
  - `px_e2` = 침식 후 mask 픽셀 수
  - 마지막 줄 = QA 판정

## 질문(각 사례마다)

- Q1: 실제로 NuRec(안개, floater 등)에 가려져 있는가? (예 / 아니오 / 판단 불가)
- Q2: QA 판정(OK / WATCH / FLAG / LOW_SUPPORT)에 동의하는가? (동의 / 비동의 + 이유)
- Q3: GT mask(초록)가 실제 벽돌 적재물과 맞는가? (예 / 아니오)
- Q4: YOLO polygon(청록)이 GT mask와 맞는가? (예 / 아니오 / 라벨 없음)
- 최종: 승인 / 보류 / 반려

## 사례 목록

| # | 사례 | split | 선정 이유 | HR / LR / CAD vis | HR / LR / CAD 판정 | Q1 | Q2 | Q3 | Q4 | 최종 | 검토자 | 날짜 | 메모 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [B1R_TRN_000236 L03](panels/01_B1R_TRN_000236_Load_03.png) | train | FLAG | 0.79232 / 0.78904 / 0.79532 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 2 | [B1R_TRN_000266 L03](panels/02_B1R_TRN_000266_Load_03.png) | train | FLAG | 0.81313 / 0.81501 / 0.80721 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 3 | [B1R_TRN_000334 L03](panels/03_B1R_TRN_000334_Load_03.png) | train | FLAG | 0.77518 / 0.79247 / 0.76053 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 4 | [B1R_TRN_000391 L03](panels/04_B1R_TRN_000391_Load_03.png) | train | FLAG | 0.35435 / 0.3581 / 0.38737 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 5 | [B1R_TRN_000612 L03](panels/05_B1R_TRN_000612_Load_03.png) | train | FLAG | 0.72129 / 0.73482 / 0.72125 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 6 | [B1R_TRN_000688 L05](panels/06_B1R_TRN_000688_Load_05.png) | train | FLAG | 0.8 / 0.76316 / 0.865 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 7 | [B1R_TRN_000919 L03](panels/07_B1R_TRN_000919_Load_03.png) | train | FLAG | 0.58306 / 0.56826 / 0.52941 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 8 | [B1R_TRN_000926 L03](panels/08_B1R_TRN_000926_Load_03.png) | train | FLAG | 0.9266 / 0.86149 / 0.86412 | WATCH / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 9 | [B1R_TRN_000934 L03](panels/09_B1R_TRN_000934_Load_03.png) | train | FLAG | 0.88648 / 0.89354 / 0.88972 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 10 | [B1R_TRN_001773 L05](panels/10_B1R_TRN_001773_Load_05.png) | train | FLAG | 0.7 / 0.70927 / 0.74336 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 11 | [B1R_TST_000114 L03](panels/11_B1R_TST_000114_Load_03.png) | test | FLAG | 0.87336 / 0.88025 / 0.87251 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 12 | [B1R_TST_000137 L05](panels/12_B1R_TST_000137_Load_05.png) | test | FLAG | 0.88743 / 0.86328 / 0.88134 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 13 | [B1R_TST_000188 L05](panels/13_B1R_TST_000188_Load_05.png) | test | FLAG | 1.0 / 0.87121 / 1.0 | LOW / FLAG / LOW |  |  |  |  |  |  |  |  |
| 14 | [B1R_TST_000392 L03](panels/14_B1R_TST_000392_Load_03.png) | test | FLAG | 0.47557 / 0.46846 / 0.46545 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 15 | [B1R_VAL_000045 L03](panels/15_B1R_VAL_000045_Load_03.png) | val | FLAG | 0.81369 / 0.84207 / 0.83365 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 16 | [B1R_VAL_000127 L03](panels/16_B1R_VAL_000127_Load_03.png) | val | FLAG | 0.75866 / 0.74752 / 0.74746 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 17 | [B1R_VAL_000148 L03](panels/17_B1R_VAL_000148_Load_03.png) | val | FLAG | 0.87763 / 0.85114 / 0.90246 | FLAG / FLAG / WATCH |  |  |  |  |  |  |  |  |
| 18 | [B1R_VAL_000203 L03](panels/18_B1R_VAL_000203_Load_03.png) | val | FLAG | 0.86946 / 0.881 / 0.85149 | FLAG / FLAG / FLAG |  |  |  |  |  |  |  |  |
| 19 | [B1R_TRN_000622 L05](panels/19_B1R_TRN_000622_Load_05.png) | train | LOW_SUPPORT_SAMPLE |  /  /  | LOW / LOW / LOW |  |  |  |  |  |  |  |  |
| 20 | [B1R_TRN_000795 L04](panels/20_B1R_TRN_000795_Load_04.png) | train | LOW_SUPPORT_SAMPLE | 1.0 / 1.0 / 1.0 | LOW / LOW / LOW |  |  |  |  |  |  |  |  |
| 21 | [B1R_VAL_000168 L05](panels/21_B1R_VAL_000168_Load_05.png) | val | LOW_SUPPORT_SAMPLE | 1.0 / 1.0 / 1.0 | LOW / LOW / LOW |  |  |  |  |  |  |  |  |
| 22 | [B1R_VAL_000212 L04](panels/22_B1R_VAL_000212_Load_04.png) | val | LOW_SUPPORT_SAMPLE | 1.0 / 1.0 / 0.98291 | LOW / OK / OK |  |  |  |  |  |  |  |  |
| 23 | [B1R_TST_000151 L04](panels/23_B1R_TST_000151_Load_04.png) | test | LOW_SUPPORT_SAMPLE | 1.0 / 1.0 / 1.0 | LOW / LOW / LOW |  |  |  |  |  |  |  |  |
| 24 | [B1R_TST_000269 L04](panels/24_B1R_TST_000269_Load_04.png) | test | LOW_SUPPORT_SAMPLE | 1.0 / 1.0 / 1.0 | LOW / LOW / LOW |  |  |  |  |  |  |  |  |
| 25 | [B1R_TRN_000040 L01](panels/25_B1R_TRN_000040_Load_01.png) | train | NORMAL_PRIMARY_SAMPLE | 1.0 / 1.0 / 1.0 | OK / OK / OK |  |  |  |  |  |  |  |  |
| 26 | [B1R_TRN_001207 L01](panels/26_B1R_TRN_001207_Load_01.png) | train | NORMAL_PRIMARY_SAMPLE | 0.99905 / 0.99696 / 0.9994 | OK / OK / OK |  |  |  |  |  |  |  |  |
| 27 | [B1R_VAL_R000285_01 L01](panels/27_B1R_VAL_R000285_01_Load_01.png) | val | NORMAL_PRIMARY_SAMPLE | 0.99749 / 0.99792 / 0.9999 | OK / OK / OK |  |  |  |  |  |  |  |  |
| 28 | [B1R_VAL_000372 L01](panels/28_B1R_VAL_000372_Load_01.png) | val | NORMAL_PRIMARY_SAMPLE | 0.99963 / 0.99855 / 0.99812 | OK / OK / OK |  |  |  |  |  |  |  |  |
| 29 | [B1R_TST_000227 L01](panels/29_B1R_TST_000227_Load_01.png) | test | NORMAL_PRIMARY_SAMPLE | 1.0 / 1.0 / 1.0 | OK / OK / OK |  |  |  |  |  |  |  |  |
| 30 | [B1R_TST_000039 L01](panels/30_B1R_TST_000039_Load_01.png) | test | NORMAL_PRIMARY_SAMPLE | 1.0 / 1.0 / 1.0 | OK / OK / OK |  |  |  |  |  |  |  |  |

## 서명(비어 있음)

- 검토자: 
- 검토 일시: 
- 전체 의견: 
- 이 결과로 QA v02를 개정할 필요가 있는가: (예 → v03 amendment / 아니오)
