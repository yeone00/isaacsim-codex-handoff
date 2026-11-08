# B1 HR 실패 원인 추가 점검 · FP32 box loss(B안) 구현 · 짧은 GPU 검증 (2026-11-08)

성격: 원인 분석, recipe v03 amendment, 짧은 GPU 시험(5 epoch과 3 epoch에서 중단)과 forward 전용 진단. **200 epoch 재학습 0, LR/CAD 0, seed 43/44 0, HPO 0, test 0.** v02 HR FAILED run(epoch 182)과 epoch 95 checkpoint(sha 105b62c8…)는 그대로이고 상태도 FAILED 그대로다.

## 요약

| 질문 | 답 |
|---|---|
| B안이 정상 구현됐나 | **예.** 실제 학습 조건 smoke에서 bbox_iou 입력이 fp32 / fp32이고 autocast off, loss 출력도 fp32다. 실제 갱신, 가중치 변화, EMA 갱신 정상, 비정상 forward 0건 → **PASS** |
| inf는 FP16 중간 계산에서 생기나, 비정상 예측이 넘어오나 | **FP16 중간 계산.** 후반 가중치 probe에서 inf가 난 10개 batch 모두 예측값(pred_dist, decode된 box)은 유한했다. 같은 예측으로 fp32 계산을 하면 0건이다 |
| 수치 메커니즘 | CIoU 안에서 `w1*h1`은 fp16, 교집합과 합집합은 fp32로 계산된다. 거의 완벽한 box에서 iou > 1이 되면 `alpha = v/(v − iou + 1 + eps)`의 분모가 0 이하가 되어 −inf나 음수 loss가 나온다 |
| 미확인 | 실패한 batch를 정확히 재현하는 것(원 가중치가 저장되지 않음), 다른 inf 원인이 없다는 것, 200 epoch 장기 거동, 이미지·라벨이 기여했을 가능성(완전 배제 아님) |
| 200 epoch 재학습 | **진행해도 된다고 판단한다(승인 필요).** v05의 감사 정책으로 비정상 forward가 생기면 PASS가 아니라 FLAGGED로 남는다 |

## 1. 계산 경로(Ultralytics 8.4.129, 소스를 읽어 확인)

- trainer L496–503: `with autocast(amp)`: `loss, loss_items = model.loss(batch, preds)`. loss 전체가 autocast(fp16) 안에서 계산된다.
- `v8DetectionLoss.get_assigned_targets_and_loss`(loss.py L402–470)
  - `make_anchors`: anchor_points와 stride_tensor의 dtype이 feats와 같은 **fp16**이다(tal.py L396–405).
  - `bbox_decode`(L393–400): softmax는 fp32로 autocast되지만 `matmul`은 fp16으로 autocast되고, `dist2bbox`는 fp16 anchor를 쓴다. 그래서 **pred_bboxes는 fp16**이다. smoke probe로 확인했다(decode 입력 fp16 / fp16).
  - target_bboxes / stride_tensor는 fp32다.
- `BboxLoss.forward`(L119–156) → `bbox_iou(pred fp16, target fp32, CIoU=True)`(metrics.py L142–167)
  - `w1, h1 = b1_x2 − b1_x1, b1_y2 − b1_y1 + eps`: **fp16**(eps 1e-7은 fp16 subnormal)
  - `inter`: fp16과 fp32가 섞여 **fp32**로 승격
  - `union = w1*h1 + w2*h2 − inter + eps`: `w1*h1`은 fp16 곱이고 나머지는 fp32
  - `alpha = v / (v − iou + (1 + eps))`(no_grad) → `iou − (rho2/c2 + v·alpha)`
- DFL: `log_softmax(pred_dist)`는 fp32로 autocast된다. 실패 run에서 DFL loss는 항상 유한했다.

## 2. 수치 원인 점검

### 2-1 단위 시험(모델 없음, box 200만 쌍, `analysis/b1_ciou_fp16_unit_20261108_v01.py`)

| 예측 노이즈 | A: pred fp16 / target fp32(학습 경로) | B: 같은 fp16 값을 fp32로 계산 | C: 모두 fp32 |
|---|---|---|---|
| 0.1 | iou>1 0, −inf 0 | 0 / 0 | 0 / 0 |
| 0.01 | iou>1 **894** | 0 | 0 |
| 0.001 | iou>1 **15,842**, −inf **7** | 0 | 0 |
| 0.0001 | iou>1 **19,308**, −inf **14** | 0 | 0 |

- 노이즈 0.001에서 유한한 loss만 보면 A는 음수 loss가 16,220개이고 최대 loss가 1.01이다(거의 완벽한 box인데 loss가 튐). C는 음수 0개, 최대 0.10이다.
- B가 0건이라는 것은 문제가 **예측값의 반올림이 아니라 계산 정밀도가 섞이는 것**에 있다는 뜻이다.
- 결과 파일: `b1_fp32_boxloss_20261108_v01/ciou_fp16_unit.json`, `ciou_fp16_finite_outliers.txt`

### 2-2 후반 학습 상태 probe(forward와 loss만, `analysis/b1_late_state_boxloss_probe_20261108_v01.py`)

- 대상: 실패 run의 last.pt(epoch 181 EMA). BN은 train mode, 64장 batch를 학습처럼 섞어 320 batch, autocast fp16
- 같은 예측에 대해 원래 fp16 경로와 fp32 경로를 함께 계산했다.

| | fp16 경로(v02) | fp32 경로(v03) |
|---|---:|---:|
| box loss inf인 batch | **10 / 320** | 0 |
| −inf CIoU 개수 | 18 | 0 |
| 음수 CIoU loss(iou>1) | **10,917**(320 batch 전부) | 0 |
| 예측 pred_dist / decode box 유한 | 전부 유한(absmax 31.2) | — |
| 유한 batch의 box loss 차이 | 최대 0.0017(fp32 평균 0.0095) | |

- **inf는 비정상 예측이 넘어와서가 아니라 fp16 중간 계산에서 생긴다**고 판단한다.
- 학습 중 빈도는 epoch 107–182의 1216 batch 중 9건(0.7%)이었고, probe에서는 3.1%였다. probe가 더 높은 이유는 EMA 가중치가 더 정확해서(거의 완벽한 box가 많아서)로 추정한다.
- 결과: `b1_fp32_boxloss_20261108_v01/late_state_probe_summary.json`. 전체 per-batch 기록은 baseline root의 `diag_late_state_boxloss_probe_v01/`에 있다.

### 2-3 무엇이 확인됐고 무엇이 미확인인가

- **확인**
  1. 학습 경로에서 pred box는 fp16, target은 fp32이고 CIoU 안에서 정밀도가 섞인다.
  2. 이 경로는 거의 완벽한 box에서 −inf와 음수 loss를 만든다(단위 시험과 후반 probe).
  3. 같은 예측을 fp32로 계산하면 0건이다.
  4. 실패 run과 같은 양상이다: 후반(box loss가 작을 때)에만 생기고 box loss만 inf다.
- **추가로 드러난 문제:** v02 학습은 후반 매 batch에 iou>1에서 오는 **음수 CIoU loss**를 포함하고 있었을 가능성이 높다. inf가 아니어서 감지되지 않았다. 이것이 후반 box gradient를 왜곡했을 수 있다(정량 미확인).
- **미확인**
  - 실패 batch 9건을 정확히 재현하는 것. 원 가중치와 batch 이미지 목록이 저장되지 않았다. v05부터 이미지 목록을 기록한다.
  - 다른 inf 원인이 없다는 증명
  - 200 epoch 장기 거동
  - 이미지·라벨 요인: 단일 이미지 1000장 정상만으로는 완전히 배제하지 않는다. 특정 box 형태(얇은 띠 등)가 거의 완벽한 일치를 더 쉽게 만들어 빈도를 높였을 가능성이 남는다.
- 기존 inf 9건과 조건 보존: `b1_fp32_boxloss_20261108_v01/v02_HR_failed_run_inf_events.json`
  - epoch과 batch 위치: 107/11, 118/11, 120/12, 140/5, 146/8, 167/7, 171/11, 179/9, 182/15
  - scale 변화: 64 → 0.125
  - epoch 1 warmup의 초기 scale 조정 1건은 따로 구분했다.

## 3. B안 구현과 짧은 GPU 검증

- 모듈: `scripts/b1_fp32_boxloss_20261108_v01.py`
  - `SegLossFP32Box`: `bbox_decode`와 `BboxLossFP32`를 autocast off, float32로 계산한다.
  - 나머지 loss와 forward는 AMP 그대로다.
- recipe: **LOCKED v03 amendment**(md `83b67b29…`, json `76654f9b…`). train_args는 v02와 차이가 없다. v02와 v01은 보존했다.
- 학습 스크립트: `scripts/train_b1_yolo_20261108_v05.py`(ca1175c8…)
- smoke root: `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_SMOKE_RECIPEv03_FP32BOX_20261108_v01`
- 공통 조건: HR, seed 42, 200 epoch 스케줄 유지

| run | 내용 | 결과 |
|---|---|---|
| stop5_compare | 5 epoch. 매 batch fp16 경로를 함께 계산해 비교 | 학습은 정상(아래). **판정 FAIL_AUDIT**: 진단 코드 순서 문제로 dtype probe가 fp16 비교 계산의 첫 호출을 기록했다. 보존 |
| **stop3_nocompare** | 3 epoch, 실제 학습과 같은 조건 | **PASS**. probe: bbox_iou 입력 fp32 / fp32, autocast off, decode 출력 fp32, loss fp32 |

stop5_compare의 epoch별 값:

| epoch | 실제 갱신(누적) | NONFINITE_FORWARD | GRAD_OVERFLOW_SKIP | scale | box / seg loss | 최대 grad norm(unscaled) | Δ가중치 | val mask mAP50-95 |
|---:|---:|---:|---:|---:|---|---:|---:|---:|
| 1 | 15 | 0 | 1(batch 1) | 64 | 0.939 / 1.946 | 9142 | +1168 | 0.001 |
| 2 | 31 | 0 | 0 | 64 | 0.746 / 0.953 | 1835 | +1753 | 0.001 |
| 3 | 47 | 0 | 0 | 64 | 0.666 / 0.746 | 1210 | +2253 | 0.020 |
| 4 | 63 | 0 | 0 | 64 | 0.627 / 0.653 | 911 | +2801 | 0.219 |
| 5 | 79 | 0 | 0 | 64 | 0.577 / 0.583 | 907 | +3292 | 0.523 |

- 80 batch 비교: fp32와 fp16 box loss 차이는 최대 0.00027(상대 0.36%)이고 DFL 차이는 0이다. 초반에는 두 경로에서 비유한값과 음수 loss가 모두 0건이었다. 거의 완벽한 box가 아직 없기 때문이다.
- 첫 batch의 GRAD_OVERFLOW_SKIP 1건은 forward loss가 유한했고, scale 128에서 gradient가 overflow난 것이다(초기 조정). NONFINITE_FORWARD와 구분되어 기록됐다.
- GPU peak는 10.3GB, epoch당 약 3.8초로 v02와 같은 수준이다.
- stop3와 stop5의 epoch 1–3 loss가 같았다. 같은 조건에서 일치한다.
- **주의:** 짧은 시험은 학습 초반 상태라 후반의 간헐적 inf 조건(거의 완벽한 box)을 만들지 못한다. 그래서 FP32로 문제가 해결됐다고 **단정하지 않는다.** 후반 상태 근거는 §2-2의 forward probe뿐이다.

## 4. 학습 감사 로직 정비(v05)

- v04의 결함(epoch 마지막 batch의 loss만 검사)을 고쳤다. 이제 **모든 batch**의 loss 항목을 기록한다.
- optimizer_step마다 STEP / GRAD_OVERFLOW_SKIP / NONFINITE_FORWARD로 분류하고 다음을 기록한다.
  - scale 전후, unscaled grad norm, AdamW counter
  - 비정상 forward가 난 batch의 이미지 파일 목록
- epoch 평균은 Ultralytics 값을 그대로 둔다(inf가 있으면 inf). 비정상 batch를 빼고 정상 학습처럼 처리하지 않는다. 유한 batch만의 평균은 `…_DIAGNOSTIC_ONLY` 필드로 따로 둔다.
- 판정
  - NONFINITE_FORWARD가 1건이라도 있으면 **FLAGGED_NONFINITE_FORWARD**(PASS 아님). driver는 PASS일 때만 다음 표현으로 넘어간다.
  - 즉시 FAILED: 가중치 비유한, 연속 3 batch 비정상, scale < 2⁻⁸, val fitness 비유한
  - 재로드와 재시도는 없다.

## 5. 기존 HR 결과와 과적합 분석(별도)

- v02 HR run은 **FAILED 그대로**다. 200 epoch 완료 결과로 쓰지 않는다. epoch 95 checkpoint는 보존만 한다.
- 분석: `b1_fp32_boxloss_20261108_v01/v02_HR_post_epoch95_overfitting_analysis.json`, `.png`
  - val mask mAP50-95 최고는 0.821(epoch 95)이다. 그 뒤 기울기는 −0.0004/10 epoch이다.
  - 구간 평균은 80–110: 0.811, 111–140: 0.813, 141–170: 0.811, 152–181: 0.811이다. **성능 저하는 매우 작다.** 사실상 0.81 근처에서 평탄하고, 0.821은 단일 epoch 최고값이다.
  - val seg loss는 1.21 → 1.54 → 1.81 → 1.91로 꾸준히 늘었고, train seg loss는 0.025 → 0.002로 줄었다. **loss 기준으로는 mask head 과적합 신호가 분명하다.** mAP는 거의 변하지 않았다.
  - 교란 요인: fp16 CIoU의 음수 loss(후반 매 batch), epoch 107 이후 scale이 0.25까지 감소, seed 1개, 실패 run. 이 요인들의 기여는 분리하지 못했다.
- epoch은 200 그대로 두었다. HR / LR / CAD 결과를 본 뒤 공통 학습 예산을 재검토한다(연구자 결정).

## 6. 200 epoch 재학습 진행 판단

- **권고: 진행해도 된다(승인 필요).**
  - B안이 dtype 수준에서 정상 구현됐다.
  - 확인된 메커니즘(fp16과 fp32가 섞인 CIoU)을 제거한다.
  - 후반 상태 probe에서 fp32 경로는 0건이었다.
  - v05 감사가 비정상을 숨기지 않고 FLAGGED로 남긴다.
- 실행하려면 seed 42 driver를 v03/v05용 새 버전(v02 driver)으로 만들어야 한다. root도 새로 만든다(`B1_YOLO_BASELINE_FP32BOX_<날짜>_v01`). 예상 시간은 약 50분(HR / LR / CAD + 분석 + val 3×3)이다.
- 남는 위험
  - fp32에서도 iou 반올림이 아주 드물게 경계에 걸릴 수 있다. 단위 시험에서는 0건이었다.
  - 다른 원인의 inf가 생길 수 있다.
  - 이런 경우에는 FLAGGED나 FAILED로 기록되고 멈춘다.

## 파일

- 신규 코드
  - `scripts/b1_fp32_boxloss_20261108_v01.py`
  - `scripts/train_b1_yolo_20261108_v05.py`
  - `analysis/b1_ciou_fp16_unit_20261108_v01.py`
  - `analysis/b1_late_state_boxloss_probe_20261108_v01.py`
- 신규 문서: `docs/b1_yolo_baseline_recipe_LOCKED_v03_20261108.{md,json}`
- 보고서 첨부: `reports/b1_fp32_boxloss_20261108_v01/`(단위 시험, probe 요약, inf 이벤트, 과적합 분석)
