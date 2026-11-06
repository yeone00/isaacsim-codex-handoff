# B1 적벽돌 train 생성 검증과 NuRec 가시도 QA 임계값 후보 (2026-11-06)

성격: **production(train split만).** C1 구성, H1 처리. 학습 0, val/test 생성 0. val/test의 QA 분포는 열지 않았다. 모델 성능과 Real Test189는 사용하지 않았다.

**QA 임계값은 아직 잠그지 않았다.** 아래는 제안이며, 연구자가 승인하면 `docs/b1_visibility_qa_rule_LOCKED_v02_<날짜>.md`로 잠근다.

- 결정 기록: `docs/b1_production_decisions_20261106_v01.md`
- 측정 정의: `docs/b1_visibility_qa_rule_DRAFT_20261105_v01.md`
- 잠금 틀: `docs/b1_visibility_qa_rule_v02_LOCK_TEMPLATE_20261106.md`

## A. 생성 완료와 검증 — **PASS**

- root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_TRAIN_20261106_v01`(1.7 GB)
- driver: `scripts/run_b1_train_production_20261106_v01.sh`(sha `da879980…5bf`)
  - 내부에서 `scripts/b1_red_production_capture_20261105_v03.py`를 `--empty-bg --settle-updates 8 --allow-production`으로 실행했다. HR에는 `--canonical`을 추가했다.
  - manifest `red_only_manifest_1400_v03.csv`의 sha256은 `56c8acbb…79e0`으로 실행 전에 일치를 확인했다. train은 1000행이다.

| 표현 | result | 장면 PASS/FAIL | load | 소요 | 장면당 | primary 재시도 | verify |
|---|---|---|---:|---:|---:|---:|---|
| HR_Scan(+canonical) | PASS_CAPTURE | 1000 / 0 | 2969 | 95.5분 | 5.71 s | 0 | **PASS** (`verify_HR_Scan_v01.json` e5e93094…) |
| LR_Scan | PASS_CAPTURE | 1000 / 0 | 2969 | 65.4분 | 3.89 s | 0 | **PASS** (`verify_LR_Scan_v01.json` 2707bf80…) |
| GeoCAD | PASS_CAPTURE | 1000 / 0 | 2969 | 69.0분 | 4.11 s | 0 | **PASS** (`verify_GeoCAD_v01.json` 8b7ba4b7…) |

- verify 검사 항목(모두 PASS)
  - `result.json`이 PASS_CAPTURE
  - `failure.json` 없음
  - complete 1000개, 모두 PASS
  - RGB PNG는 640×480이고 SHA가 기록과 일치
  - actual mask 개수 일치, E(빈 배경) 1000장, HR canonical mask 개수 일치
  - renderer `[Error]` 0줄
- **pairing:** `crossrep_pairing_v01.json`(1624cf1a…) **PASS**
  - 공통 장면 1000개에서 카메라 행렬, dome, 생성 브릭 수가 모두 같았다.
  - HR mask가 500px 이상인 5756개 load 쌍에서 LR/CAD mask IoU ≥ 0.7, 면적비 0.8–1.25였다. 위반은 0이다.
- FAIL 장면이 없어서 resume은 필요 없었다. 분모는 1000 × 3 그대로다.
- 판정은 위 결과 파일로 했다. exit code(전부 0)는 판정에 쓰지 않았다.
- 실측 합계는 3.8시간이다(pilot 추정 C1 ≈ 5.5 h/1400장면과 같은 수준).

## B. train 가시도 분포

- 계산: `analysis/b1_train_visibility_qa_20261106_v01.py`
  - 출력 `analysis_train_qa_v01/b1_visibility_qa_train_metrics_v01.csv`(60fae522…)
  - 8907 load-표현 행(2969 × 3), 2937 scene-load에 세 표현이 모두 있다.
- 지표: `vis_hard_e2`(2px 침식). `vis_soft_e2`는 C1이라 NOT_COMPUTED다.

### 분포 요약

| 구분 | HR | LR | CAD |
|---|---:|---:|---:|
| 전체 load 최소 | 0.354 | 0.358 | 0.387 |
| 전체 0.1 / 1 / 5 pct | 0.720 / 0.984 / 0.999 | 0.733 / 0.983 / 0.998 | 0.742 / 0.974 / 0.998 |
| **primary Load_01 최소(n=1000)** | **0.990** | **0.988** | **0.995** |
| primary `px_e2` 최소 | 2719 | 2646 | 2897 |
| R3 양성 대조군(진단 pilot, TRN_000027 Load_01) | 0.815 | 0.814 | 0.826 |

R3는 production에서 제외된 ROI이므로 진단 pilot 값을 참고선으로만 표시했다.

![vis_hard_e2 히스토그램](b1_train_production_qa_20261106_v01/hist_vis_hard_e2_by_rep.png)

`px_e2` 분포와 N_min 후보선: `b1_train_production_qa_20261106_v01/hist_px_e2_HR.png`

### 낮은 값의 정체 — 실제 NuRec 가림

- 0.95 미만인 scene-load는 18개다(`px_e2` ≥ 50 기준). **모두 보조 load(Load_03/05)이고 primary는 0개다.**
- ROI별로 보면 R1_NORTH_2가 대부분이다(0.95 미만이 HR 14 / LR 11 / CAD 13). R5_WEST는 2–3개, R4_EAST는 0개다(`low_by_roi.csv`).
- 세 표현이 같은 방향으로 낮다. 예: TRN_000391 Load_03은 0.354 / 0.358 / 0.387이다. 표현 차이가 아니라 장면 원인이라는 뜻이다.
- 패널을 육안으로 보면(AI 판독이며 사람 검토는 아님), R1_NORTH_2 화면 왼쪽의 **반투명 NuRec 안개 기둥(gaussian floater)**이 뒤쪽 Load_03의 왼쪽 끝을 가리고 있다. 지표가 의도한 가림을 잡고 있다.

![TRN_000391 Load_03](b1_train_production_qa_20261106_v01/panel_B1R_TRN_000391_Load_03.png)

- 패널 구성: 각 행이 HR/LR/CAD이고, 열은 I(초록 = 실제 load mask) / E / |I−E| > τ이다.
- 나머지 패널: `panel_*_Load_0N.png` 5개(TRN_000919, 000612, 000334, 000236, 001773)
- **라벨 관련 주의:** 공통 canonical label은 NuRec를 모른다. 그래서 이런 보조 load에서는 RGB에서 가려진 부분까지 라벨에 포함된다. H1이므로 라벨과 장면은 그대로 두고 FLAG만 기록한다.

### 임계값 근거 (`analysis/b1_train_qa_threshold_evidence_20261106_v01.py` → `threshold_evidence.json`)

**크기별 표현 간 차이(세 표현 max−min):**

| 세 표현 중 최소 `px_e2` | scene-load | spread p99 | spread max |
|---|---:|---:|---:|
| < 100 | 88 | 0 | 0 |
| 100–200 | 51 | 0.053 | **0.102** |
| 200–500 | 107 | 0.027 | 0.043 |
| 500–1000 | 108 | 0.004 | 0.009 |
| ≥ 1000 | 2583 | 0.011 | 0.065 |

100px 미만의 spread가 0인 이유는 값이 대부분 1.0이기 때문이다. 크기가 작아서 지표가 안정적이라는 뜻은 아니다.

**후보 조합별 결과(train):**

| N_min | T_flag | T_watch | FLAG 행 | FLAG scene-load | primary base-scene FLAG | WATCH 행 | LOW_SUPPORT 행 | 경계 걸침* |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 0.95 | 0.98 | 46 | 18 | 0 | 48 | 254 | 5 |
| **100** | **0.90** | **0.95** | **29** | **10** | **0** | **17** | **254** | **1** |
| 100 | 0.80 | 0.90 | 19 | 7 | 0 | 10 | 254 | 1 |
| 50 | 0.90 | 0.95 | 29 | 10 | 0 | 17 | 144 | 1 |
| 200 | 0.90 | 0.95 | 28 | 10 | 0 | 17 | 396 | 1 |

\*경계 걸침: 같은 scene-load인데 세 표현이 T_flag 양쪽으로 갈린 수. 전체 9개 조합은 json에 있다.

## 제안(승인 대기 — 잠그지 않음)

| 기호 | 제안 | 근거 |
|---|---|---|
| `T_flag` | **0.90** | R3 대조군(0.814–0.826)을 0.07 이상 여유로 FLAG에 포함한다. 0.80은 R3를 놓친다. 0.95는 0.94–0.95 근처에 몰린 load 때문에 경계 걸침이 5개로 늘고, 0.90은 1개다(TRN_000926: 0.927 / 0.861 / 0.864). 큰 load의 표현 간 spread p99(0.011)보다 간격이 훨씬 크다 |
| `T_watch` | **0.95** | 0.90–0.95 구간(17행)을 보고용으로만 따로 표시한다. 0.95 근처 경계 걸침 5건이 이 구간에 들어간다 |
| `N_min` | **100 px**(대안 200) | 기존 canonical 라벨 규칙(≥ 100px)과 같은 수준이다. 100–200px에서 표현 간 spread가 최대 0.10으로 커진다는 점을 더 엄격하게 반영하려면 200이다(LOW_SUPPORT 254 → 396행). 어느 쪽이든 T_flag 0.90에서 FLAG scene-load는 10개로 같다 |

제안값을 쓰면 train 결과는 다음과 같다.

- FLAG 29행 / 10 scene-load / 10 base scene. 모두 보조 load다.
- **primary 기준 base-scene FLAG는 0**이다.
- H1에 따라 장면 삭제와 대체는 없고 FLAG 열만 기록한다.

## 판정·미해결

- A: **PASS.** train 1000 × 3, verify 3개와 pairing 모두 PASS.
- B: 분포와 후보 제안 완료. **잠금은 미실행이며 연구자 승인을 기다린다.**
- 사람 육안 검토는 미실행이다(위 패널은 AI 판독이다).
- val/test는 생성하지 않았다. 잠금 후 같은 v03과 같은 검증기로 생성한다. YOLO 학습은 별도 승인 사항이다.
- 알려진 제한은 변동 없다.
  - 바닥 접촉 그림자가 약하다(matte 보류).
  - NuRec depth는 무효다.
  - C1에는 soft 지표가 없다. 반투명 안개 가림을 hard 지표가 얼마나 과소 또는 과대 평가하는지는 UNKNOWN이다.

## 파일

- 신규 코드
  - `analysis/b1_train_qa_figures_20261106_v01.py`(d66988de…)
  - `analysis/b1_train_qa_threshold_evidence_20261106_v01.py`(80b5f67d…)
- 보고서 첨부: `reports/b1_train_production_qa_20261106_v01/`
  - 히스토그램 2개, 패널 6개
  - `low_by_roi.csv`, `threshold_evidence.json`, `figures_meta.json`
- 데이터 root의 산출물
  - `verify_*_v01.json`, `crossrep_pairing_v01.json`, `driver.log`, `wrapper.log`
  - `analysis_train_qa_v01/`(metrics CSV, grid CSV f25b207d…, summary.json)
- 변경 없음: 원본 USD, 브릭 에셋, manifest, split, 기존 출력. 각 capture 세션 시작 시 입력 hash gate를 통과했다.
