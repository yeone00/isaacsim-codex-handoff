# B1 혼합 실험 사전 검증: 실제 라벨 충돌 · checkpoint 규칙 · 증강 구현 · 50:50 smoke (2026-11-08)

성격: 39개 본 학습 전 검증 단계다.
- 본 학습 0, HPO 0, B1 test / Real Test189 추론 0.
- GPU 사용은 HR seed 42, 50:50 조건의 **3 epoch smoke 1회**뿐이다.
- 원본 라벨, 이미지, split, 기존 baseline 9개, 기존 결과는 변경하지 않았다.
- 결정: 안 A(총 1000 고정), 비율 100:0 / 75:25 / 50:50 / 25:75 / 0:100(연구자 2026-11-08).

## 요약 — 5개 보고 항목

| # | 항목 | 결과 |
|---|---|---|
| 1 | 실제 라벨 충돌 | **심각도: 음성 이미지는 높음, 양성은 중간.** real train 352장 중 **최소 58장(16.5%)**에 라벨 없는 적재물이 보인다. 그중 **음성 65장 중 39장(60%)**은 "벽돌 없음" 라벨인데 벽돌 팔레트가 보인다. 양성 287장 중 최소 19장(6.6%)은 보조 적재물이 라벨 없이 남아 있거나 옆 팔레트가 대상 polygon에 합쳐져 있다. real val은 48장 중 최소 21장(44%). 실제 라벨 내부에서도 모순이 있다(같은 종류의 먼 팔레트가 양성 이미지에서는 라벨, 음성 이미지에서는 미라벨). **권고: 실행 전에 처리 방식을 결정**해야 한다. 1순위는 사람이 누락 load를 보충한 별도 라벨 세트, 대안은 충돌 음성 39장을 제외하는 것. |
| 2 | checkpoint 규칙 | **권고: 합성 val과 real val을 함께 쓰는 공통 규칙(best_combined)을 주 규칙으로 한다.** 매 epoch 0.5 × (B1 자기 표현 val + real val) mask mAP50-95가 최대인 epoch를 쓴다. 비용은 epoch당 0.45초다. Q1(증강 vs 기존 baseline)은 양쪽 모두 B1 val best로 비교한다. 네 checkpoint를 모두 저장하지만 주 규칙은 지금 고정한다. |
| 3 | 증강 검증 | **PASS.** 기하 증강 후 mask 정렬 정상(no-geometry 대조군보다 나쁘지 않음). 광도 변형은 라벨에 영향 없음. 평가 세트에는 증강이 없음. 실제 반복 수가 막 목록과 정확히 일치하고 반복본마다 증강이 다름. HR / LR / CAD 설정이 같음. 검증 코드 결함 2건은 고친 뒤 재실행했다(아래). |
| 4 | 50:50 smoke | **PASS**(run_status 15개 check 모두 true). 실제 갱신 47/48(첫 batch overflow 1회), NONFINITE 0, 음수 box batch 0, fp32 box, 실제 이미지 비율 50.0%, real val 매 epoch 계산, checkpoint 4종 저장, 원본 hash 불변, peak 10.2 GB. |
| 5 | 39개 본 학습 | **기술적으로는 실행 가능**(smoke와 검증 PASS, 예상 약 10시간). **다만 시작 전에 연구자 결정 두 가지가 필요하다.** (a) 실제 라벨 충돌 처리. 실제 train 구성이 바뀌면 막 목록을 v02로 새로 만든다. (b) recipe v04와 혼합 프로토콜을 LOCKED로 승인. |

## 1. 실제 라벨 충돌 점검

**방법(사람 QA가 아님, AI 선별)**
1. 색 선별: 대상 GT를 dilate해 지운 뒤, 남은 부분에서 빨강·주황 영역(HSV)이 1500px 이상인 곳을 후보로 잡았다. 후보는 147개다.
2. 후보 crop 147개를 육안으로 분류했다. 벽돌 적재물 / 피부·옷·팔레트 목재.
3. **음성 65장은 전부** 큰 크기로 육안 재검토했다. 색 선별은 그중 15장을 놓쳤다. 따라서 양성과 val의 수는 **하한값**이다.
- 표: `reports/real_label_conflict_audit_20261108_v01/real_label_conflict_table.csv`
- 그림(사람 얼굴 포함, Git 밖): `/home/user/hh/isaac_cosmos/sdg_final/REAL_LABEL_CONFLICT_AUDIT_20261108_v01/`
  - `representative_cases.jpg`, 전체 contact sheet, crop sheet

**결과**

| 세트 | 그룹 | 이미지 | 충돌 | 비율 | 유형 |
|---|---|---|---|---|---|
| train 양성 | B | 261 | 8 | 3.1% | 보조 / 배경 팔레트 미라벨 7, 옆 팔레트 합쳐짐 1 |
| train 양성 | D | 26 | 11 | 42% | 여러 팔레트 중 1개만 라벨(나무 앞 적치장, 적재 더미) |
| train 음성 | D | 65 | **39** | **60%** | "빈 팔레트" 음성인데 배경(흰 승합차 옆)에 벽돌 팔레트 더미나 작은 팔레트가 보임 |
| **train 합계** | | **352** | **58** | **16.5%** | 하한값 |
| val | C | 48 | 21 | 44% | 배경 적치 더미 미라벨(하한값) |
| test(참고) | A | 189 | — | — | visual block A1(98장)에 배경 더미 있음(이전 보고서) |

**대표 사례**(`representative_cases.jpg`)
- 0406, 0457: 음성인데 벽돌 더미가 보인다.
- 0436, 0465: 여러 팔레트 중 1개만 라벨이 있다.
- 0775: 쌓인 팔레트 중 1개만 라벨이 있다.
- 0715: 옆 팔레트가 대상 polygon에 합쳐져 있다.
- val 0802: 배경 더미가 있다.
- **0485**: 멀리 있는 작은 팔레트가 대상으로 라벨돼 있다. 그런데 0457 등 음성 이미지에서는 같은 종류의 먼 팔레트가 라벨 없이 남아 있다. **실제 라벨 안에서 서로 모순이다.**

**혼합 학습에 미치는 영향(분석)**
- YOLO는 라벨이 없는 영역의 예측을 배경(음성)으로 학습한다. 그래서 위 이미지들은 "작거나 멀거나 보조인 벽돌 적재물은 배경"이라는 신호를 준다.
- B1 라벨은 반대다. ≥100px인 모든 load가 양성이고 보조 load도 포함된다. 두 정책이 같은 개념(멀리 있는 / 보조 적재물)에 반대 감독 신호를 준다.
- 전체 train 1000장 중 충돌 항목의 비중은 비율에 따라 커진다.

| 비율 | 실제 항목 | 충돌 항목(음성 / 양성) | 1000장 중 비중 |
|---|---|---|---|
| 75:25 | 250 | 27 / 13 | 4.0% |
| 50:50 | 500 | 52 / 28 | 8.0% |
| 25:75 | 750 | 82 / 40 | 12.2% |
| 0:100 | 1000 | 112 / 53 | 16.5% |

- 예상되는 효과(검증 전 가설)
  - (i) 실제 비율이 오를수록 B1의 **보조 load와 작은 load의 recall이 떨어질** 수 있다. domain 효과와 섞여 분리하기 어렵다.
  - (ii) real val과 Test189에서는 배경 더미를 찾아내면 FP로 세어진다. 그래서 **B1식으로 "모든 load를 찾는" 모델이 실제 지표에서 불리**하다. 실제 비중이 큰 모델이 실제 지표에서 유리하게 보이는 편향이 생긴다.
  - (iii) real val을 checkpoint 선정에도 쓰므로 같은 편향이 선정에도 들어간다.
- 결과적으로 "실제 비율 효과"에 "라벨 정책 효과"가 섞인다. 기존 혼합 연구(M50)도 같은 라벨을 썼으므로 같은 교란을 갖고 있었다.

**대응 방안(원본 라벨은 수정하지 않음)**

| 안 | 내용 | 장점 | 단점 |
|---|---|---|---|
| R1 **보충 라벨 세트(권장)** | 사람이 real train 58장과 val 21장(+ 선별이 놓친 것)에 누락 load를 추가한다. 크기 기준은 B1과 같은 ≥100px@640×480 ≈ ≥410px@972×1296. 원본 옆에 새 폴더 `labels_v02`를 만든다. Test189 라벨은 그대로 둔다(기존 결과와 비교 유지). | B1 "모든 load" 정책과 일치한다. 교란을 가장 잘 없앤다. | 사람 작업이 필요하다(이미지 약 80장, 수 시간). 새 라벨 버전에 대한 QA와 승인 기록이 필요하다. |
| R2 **충돌 음성 제외(대안)** | 음성 65장 중 충돌 39장을 실제 풀에서 뺀다(고유 313장, 깨끗한 음성 26장). 양성은 그대로 둔다. 막 목록 v02를 만든다. | 라벨 작업이 없다. 가장 강한 반대 신호(명시적 음성)를 없앤다. | 실제 고유 수와 hard negative가 줄어든다. 양성의 충돌(6.6%)과 val의 충돌은 남는다. |
| R3 무시 영역 처리 | 누락 load에 사람이 박스를 그려 해당 영역을 학습 이미지 사본에서 회색으로 칠한다. | 라벨 정책 문제를 회피한다. | 사람 작업이 필요하다. 이미지가 인위적으로 바뀐다. Ultralytics에는 기본 지원이 없다. |
| R4 그대로 진행 | 현재 352장을 그대로 쓰고 제한으로 보고한다. B1 주 / 보조, 크기 층, 실제 fp_far를 모든 비율에서 보고한다. | 추가 작업이 없다. 기존 M50과 같은 조건이다. | 비율 효과와 라벨 효과를 분리할 수 없다. |

**권고:** 사람 보충 작업이 며칠 안에 가능하면 **R1**을 택한다. 어렵다면 **R2 + 층별 보고**다. 어느 쪽이든 split은 그대로 두고, 39개 학습을 시작하기 전에 정해야 한다(막 목록과 프로토콜에 반영). real val도 선정에 쓰이므로 R1에 val 보충을 포함하기를 권한다.

## 2. checkpoint 선정 규칙

**기존 baseline 근거(9 run, 증강 없음)**
- best epoch 26–75
- best → epoch 200 하락 0.014–0.031(B1 자기 표현 val)
- val seg loss 약 0.8 → 2.0–2.4(mask 과적합)

| 규칙 | 연구 목표 부합 | 장점 | 문제 |
|---|---|---|---|
| (a) epoch 200 last.pt | 낮음 | 선택이 전혀 없다. val이 편향되지 않는다. | 모든 run에서 과적합 구간의 모델이다. 반복이 많은 실제 위주 비율(0:100은 실제 1장을 568회 봄)에서 더 불리할 수 있다. 비율 비교에 "과적합 민감도" 차이가 섞인다. |
| (b) B1 val best(v05 규칙) | 부분적 | baseline과 연속된다. | 실제 성능을 무시한다. 0:100(합성 없음)에서는 의미가 없다. 합성 위주 비율에 유리하다. |
| (c) real val best | 부분적 | 실제 목표에 직접 맞춘다. | 48장, group C 하나로 잡음이 크다. 라벨 충돌이 44%다. 합성 유지를 무시한다. 100:0에서는 거의 0 근처라 임의 선택이 된다. |
| **(d) 공통 결합 규칙** | **높음** | "합성 유지 + 실제 향상"을 한 기준으로 모든 비율에 똑같이 적용한다. 비율별로 유리한 기준을 사후에 고를 여지가 없다. | real val이 선정에 쓰이므로 real val 결과가 낙관적이 된다(Test189이 편향 없는 실제 추정치). real val 라벨 충돌의 영향을 받는다(§1 R1로 완화). 두 척도를 단순 평균한다. |

**권고(프로토콜 후보에 고정)**
- 주 규칙: **(d) best_combined.pt** = argmax over epoch of 0.5 × (B1 자기 표현 val mAP50-95 + real val mAP50-95). 둘 다 Ultralytics validator의 같은 지표 코드로 계산하고, 동점이면 이른 epoch다.
  - 0:100의 합성 성분은 B1 HR val(명목)로 미리 선언했다.
- Q1(증강 vs 기존 무증강 baseline): 기존 9개는 epoch별 real val 기록이 없다. 그래서 양쪽 모두 **(b)**로 비교한다(사전 선언).
- 보조: (a), (b), (c) checkpoint를 run마다 모두 저장하고 보고한다. **주 규칙을 바꾸거나 test 결과로 다시 고르는 것은 금지**다.
- 비용: smoke에서 real val 48장 검증이 epoch당 평균 0.45초였다. run당 약 1.5분이 늘어난다.

## 3. augmentation 구현과 검증

**구현(신규)**
- `docs/b1_yolo_recipe_LOCK_CANDIDATE_v04_20261108.{json,md}`: v03 + train 전용 moderate 증강. v03은 보존한다.
- `scripts/b1_mixing_data_20261108_v01.py`
  - 막 목록을 run별 symlink 데이터셋으로 바꾼다. test는 연결하지 않는다.
  - PhotoDegrade(blur / motion blur / noise / JPEG, 이미지만, Format 직전, train만)
  - 원본 hash 가드
- `scripts/train_b1_yolo_20261108_v06.py`
  - v05 학습 로직과 audit는 그대로다.
  - 매 epoch real val 검증을 추가하고(EMA 복사본으로) checkpoint 4종을 저장한다.
  - 원본 hash 전후 비교, 실제 이미지 비율 기록을 추가했다.
- `analysis/verify_aug_pipeline_20261108_v01.py`, `analysis/verify_aug_alignment_detail_20261108_v01.py`

**검증 결과**(50:50 막 목록, 출력 `/home/user/hh/isaac_cosmos/sdg_final/B1_AUG_VERIFY_20261108_v03`, 요약은 `reports/b1_augmentation_mixing_checkpoint_smoke_20261108_v01/`)

| 검사 | 결과 |
|---|---|
| 기하 정렬 방법 | 실제로 쓰인 affine M과 flip을 기록했다. 원본 raster mask(합성은 HR canonical PNG로 라벨과 독립, 실제는 polygon raster)를 같은 변환으로 옮겨 loss에 들어가는 160×160 mask와 비교했다. |
| 기하 정렬, 큰 instance(≥300px@160) | 합성 IoU 중앙값 0.976 / 최소 0.906. 실제 0.984 / 0.934. 중심 오차 중앙값 0.1–0.2px |
| 기하 정렬, 작은 instance(<50px@160) | 합성 중앙값 0.75 / 최소 0.38. **같은 표본에서 기하 증강을 끈 대조군(= baseline 경로)도 0.53 / 0.11로 더 낮다.** 원인은 mask_ratio 4 해상도이고 증강이 아니다. |
| 좌우반전 / 크기 | 160개 중 78개 반전, 크기 0.75–1.25배 확인 |
| 광도(강제 p=1) | bbox와 segment가 비트 단위로 같다. 이미지만 바뀐다. 형식 uint8 유지 |
| 광도(데이터셋 안) | 같은 표본·같은 RNG에서 PhotoDegrade 유무에 관계없이 mask와 bbox가 40/40 동일하다. 적용률(400표본): blur 0.105, motion 0.073, noise 0.085, JPEG 0.155(설정 0.10 / 0.05 / 0.10 / 0.15) |
| train 전용 | val과 realval 변환은 LetterBox, Format뿐이다. 이미지 10장이 단순 letterbox와 비트 단위로 같다. smoke에서도 `photo_only_in_train` true |
| 실제 반복 | 실제 항목 500 = 고유 352(1회 204, 2회 148). 막 목록과 정확히 일치한다. 같은 이미지의 반복본 10쌍 모두 증강 결과가 다르다(평균 픽셀 차 33–44). |
| HR / LR / CAD 동일 설정 | 변환 파라미터 덤프가 같다. 같은 장면·같은 RNG면 M, flip, mask가 세 표현에서 같다. |
| contact sheet | `contact_before_after_0.jpg`(합성), `_1.jpg`(실제). 왼쪽 원본 + GT, 오른쪽 증강 + loss mask. 실제 사진이라 Git 밖에 둔다. |

**검증 코드 결함과 보존**
- v01 실행: 평가 이미지 비교에서 RGB/BGR 순서를 빠뜨려 거짓 FAIL이 났다.
- v02 실행: 고친 줄의 주석이 비교 코드를 가려 검사 0건인데 PASS가 나왔다(공허한 PASS).
- v03 실행: 둘 다 고친 뒤 10건을 실제로 확인해 PASS다.
- 세 출력은 모두 보존했다. 판정은 v03 기준이다.
- 재확인 과정에서 검증 표본 40개 중 이미지가 달라진 표본이 6개로, 기대치(약 14개)보다 적었다. 400표본으로 따로 측정한 적용률은 설정값과 맞았다(어떤 변형이든 적용된 비율 0.37).

## 4. 50:50 smoke(HR, seed 42, 200 epoch schedule 유지, 3 epoch 후 중지)

- 출력: `/home/user/hh/isaac_cosmos/sdg_final/B1_MIX_SMOKE_RECIPEv04_20261108_v01/HR_Scan_seed42_A1000_S050_R050_stop3`(SMOKE root, 결과로 쓰지 않음)
- 상태 **PASS**. check 15개가 모두 true였다.
  - all_epochs_ran, every_epoch_real_update, no_runaway_amp_skips, weights_changed, ema_updated, finite_losses, val_metric_finite
  - realval_every_epoch, checkpoints_saved, no_nonfinite_forward, fp32_box_dtypes, photo_only_in_train
  - train_entries_match_manifest, real_fraction_seen_matches, source_guard_unchanged
- 데이터: train 1000(합성 500 + 실제 500, 고유 352, 2회 148), val 200, realval 48, epoch마다 실제 500 / 1000 사용
- 최적화
  - STEP 47, GRAD_OVERFLOW_SKIP 1(첫 batch, scale 128 → 64), NONFINITE 0, 음수 box loss batch 0
  - bbox_iou 입력은 fp32 / fp32, autocast off
  - lr warmup이 200 epoch 일정대로 진행됐다.
- epoch별 지표(3 epoch 모델이라 수치 자체는 의미 없음)

| epoch | B1 val mAP50-95 | real val mAP50-95 | 결합 점수 |
|---|---|---|---|
| 1 | 0.003 | 0.000 | — |
| 2 | 0.094 | 0.007 | — |
| 3 | 0.193 | 0.227 | 0.210 |

- 자원: epoch당 4.5–4.7초(real val 0.4–0.5초 포함), peak 할당 10.2 GB(baseline ep1과 같다). 원본 hash 불변.
- 참고: Ultralytics가 `half` 인자 사용 중단 예정 경고를 냈다(동작에는 영향 없음).

## 5. 39개 본 학습 실행 가능 여부

- **기술 준비: 완료.** trainer v06, 증강, 막 목록, checkpoint 규칙, smoke가 모두 PASS다.
- 예상 시간: run당 약 15분(baseline 12.7분 + 증강과 real val), 39 run이면 약 10시간이다.
- **시작 전에 필요한 결정**
  1. 실제 라벨 충돌 처리(R1 / R2 / R4). R1이나 R2면 막 목록 v02, 프로토콜 후보 v02, 필요하면 recipe 후보를 갱신한다.
  2. recipe v04 후보와 혼합 프로토콜 후보를 LOCKED로 승인한다(status와 승인 필드만 바뀐다).
- 실행 순서(승인 후)
  1. 증강만(100:0) 9 run
  2. 혼합 27 run
  3. 실제만 3 run
  - 각 run은 결과 파일 PASS일 때만 다음으로 넘어가고, 재시도와 설정 변경은 하지 않는다.
  - 그 뒤 val 평가를 하고, test는 별도 LOCK v02를 거친다.
- HPO는 이 실험과 분리하며 하지 않는다.

## 파일

- 신규 문서
  - `docs/b1_yolo_recipe_LOCK_CANDIDATE_v04_20261108.{json,md}`
  - `docs/b1_mixing_experiment_protocol_LOCK_CANDIDATE_v01_20261108.{json,md}`
- 신규 코드
  - `scripts/b1_mixing_data_20261108_v01.py`
  - `scripts/train_b1_yolo_20261108_v06.py`
  - `analysis/verify_aug_pipeline_20261108_v01.py`
  - `analysis/verify_aug_alignment_detail_20261108_v01.py`
- 보고서 첨부
  - `reports/real_label_conflict_audit_20261108_v01/real_label_conflict_table.csv`
  - `reports/b1_augmentation_mixing_checkpoint_smoke_20261108_v01/`(검증 요약, 정렬 csv, smoke run_status / epochs)
- Git 밖(대용량 또는 사람 얼굴 포함)
  - `REAL_LABEL_CONFLICT_AUDIT_20261108_v01/`
  - `B1_AUG_VERIFY_20261108_v01`(결함 보존) / `v02`(결함 보존) / `v03`(유효)
  - `B1_MIX_SMOKE_RECIPEv04_20261108_v01/`
- 변경 없음: 실제 / B1 원본 데이터·라벨·split, baseline 9개, recipe v01–v03, Test LOCK 후보, 기존 막 목록
