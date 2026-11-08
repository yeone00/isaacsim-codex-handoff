# B1 seed 42 본 학습(recipe v03, FP32 box loss): HR / LR / CAD 200 epoch · val 3×3 평가 (2026-11-08)

성격: 연구자가 승인한 본 학습이다(seed 42, 3 run). **seed 43/44 0, HPO 0, test 0.** 데이터, 라벨, QA 기준은 변경하지 않았다.
**사람 QA 최종 검토는 아직 끝나지 않았다.** 이 결과는 QA FLAG / LOW_SUPPORT 판정과 라벨이 사람 승인 전이라는 제한을 가진다.
v02 FP16 HR FAILED run(`B1_YOLO_BASELINE_20261108_v01`)은 진단 자료로만 보존하고, 아래 결과에 섞지 않았다.

## 요약

| 항목 | HR | LR | CAD |
|---|---|---|---|
| run 상태(결과 파일) | **PASS** | **PASS** | **PASS** |
| 최고 val mask mAP50-95(선정 epoch) | 0.8208(ep 62) | 0.8213(ep 32) | 0.8221(ep 32) |
| epoch 200의 val mask mAP50-95 | 0.8041 | 0.7922 | 0.7915 |
| 수렴 읽기(제안 기준) | UNCLEAR(완만한 감소) | PLATEAU | PLATEAU |
| 같은 표현 val mAP50-95(평가 코드) | 0.849 | 0.838 | 0.840 |

- **수치 안정성:** 3 run 합계 9600 batch에서 비정상 forward loss 0, 평균 box loss가 음수인 batch 0이었다. AMP gradient overflow skip은 HR과 LR의 첫 batch 1회씩뿐이다. scale은 줄지 않고 64 → 128–256으로 커졌다.
- **epoch 107 이후 box loss 불안정은 재현되지 않았다.**
- 세 표현 모두 **epoch 32–62에서 최고**를 찍었다. 그 뒤로는 val mAP가 평탄하거나 조금 떨어졌고 val seg loss는 계속 늘었다(과적합 신호). seed 1개 기준으로, **200 epoch까지의 추가 학습은 val 성능을 올리지 않았다.**
- **교차 평가:** 세 평가 표현 모두에서 같은 표현으로 학습한 모델이 가장 높았다. 표현이 바뀌면 크게 떨어지고, 떨어지는 정도는 방향에 따라 다르다(아래 §4).

## 1. 실행

- driver: `scripts/run_b1_baseline_seed42_20261108_v02.sh`(recipe LOCKED v03, trainer v05, FP32 box 모듈 sha gate)
- root: `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_BASELINE_FP32BOX_20261108_v01`(새 디렉터리, 처음부터 학습)
- 시간: HR 17:31–17:44, LR –17:56, CAD –18:09, 분석과 평가 –18:12. run당 약 12.6분이다.
- 판정은 run마다 `run_status.json`으로 했다(모든 check true, state PASS). 자동 재시도와 checkpoint 복구는 없었다.
- 대표 모델(val mask mAP50-95 최고): 각 run의 `train/weights/best_val_maskmAP5095.pt`
  - HR sha `27ba2931…`(ep 62), LR `0f6222d2…`(ep 32), CAD `bdf634af…`(ep 32)

## 2. 학습 안정성(모든 batch)

| 항목 | HR | LR | CAD |
|---|---|---|---|
| optimizer 호출 / 실제 STEP | 3200 / 3199 | 3200 / 3199 | 3200 / 3200 |
| GRAD_OVERFLOW_SKIP(위치, scale) | 1(ep1 b1, 128→64) | 1(ep1 b1, 128→64) | 0 |
| NONFINITE_FORWARD | 0 | 0 | 0 |
| batch 평균 box loss < 0 | 0 | 0 | 0 |
| 비유한 loss batch | 0 | 0 | 0 |
| scale 최소 / 최종 | 64 / 128 | 64 / 128 | 128 / 256 |
| EMA updates | 3200 | 3200 | 3200 |
| GPU peak allocated | 10.4 → 14.8 GB | 같음 | 같음 |

- scale이 커진 이유: GradScaler는 연속 2000 step 동안 skip이 없으면 scale을 두 배로 올린다. 이는 overflow가 없었다는 뜻이다.
- **instance 단위 확인:** v05는 batch 평균만 기록한다. 그래서 학습 후 각 모델의 last.pt(epoch 200, 거의 완벽한 box가 많은 후반 상태)로 forward만 돌려 확인했다. 64장 batch 80개다.

| 모델 | fp16 경로(v02 방식): box loss inf batch / 음수 CIoU loss | **fp32 경로(학습에 쓴 방식)** |
|---|---|---|
| HR | 1 / 10,018 | **0 / 0** |
| LR | 0 / 9,076 | **0 / 0** |
| CAD | 2 / 9,757 | **0 / 0** |

- 새 모델도 후반에는 fp16 경로였다면 inf와 음수 loss가 났을 상태다. 학습에 쓴 fp32 경로에서는 0건이다. 예측값은 전부 유한했다.
- 이는 B안이 v02 실패 메커니즘을 제거했다는 것과 일치한다. 다만 seed 1개, 200 epoch에 대한 결과다.

## 3. 학습곡선과 수렴

![compare](b1_baseline_seed42_fp32box_20261108_v01/compare_mask_map5095.png)

run별 그림 6칸: `b1_baseline_seed42_fp32box_20261108_v01/curves_{HR_Scan,LR_Scan,GeoCAD}_seed42.png`

| val mask mAP50-95 | HR | LR | CAD |
|---|---:|---:|---:|
| 최고(epoch) | 0.8208(62) | 0.8213(32) | 0.8221(32) |
| epoch 60 | 0.8090 | 0.8020 | 0.8172 |
| epoch 100 | 0.8154 | 0.8031 | 0.8046 |
| epoch 150 | 0.8074 | 0.8011 | 0.8039 |
| epoch 200 | 0.8041 | 0.7922 | 0.7915 |
| 30 epoch 구간 평균 21–50 / 81–110 / 171–200 | 0.795 / 0.810 / 0.809 | 0.798 / 0.804 / 0.799 | 0.793 / 0.810 / 0.802 |
| 마지막 30 epoch 평균 ± sd | 0.809 ± 0.003 | 0.799 ± 0.002 | 0.802 ± 0.004 |
| 마지막 30 epoch 기울기(/10 epoch) | −0.0020 | −0.0011 | −0.0019 |
| 수렴 읽기(제안) | UNCLEAR | PLATEAU | PLATEAU |

- HR이 UNCLEAR인 이유는 기울기(−0.0020)가 PLATEAU 기준(|기울기| < 0.002)을 아주 조금 넘었기 때문이다. 내용상으로는 "평탄 또는 완만한 감소"다. 세 표현 모두 **추가 학습으로 val 성능이 오르는 신호는 없다.**
- epoch 200의 mask mAP50 / mAP75: HR 0.972 / 0.901, LR 0.972 / 0.890, CAD 0.973 / 0.884

**과적합(Train/Val loss 차이)**

| | HR train seg / val seg | LR | CAD |
|---|---|---|---|
| epoch 32 | 0.118 / 0.76 | 0.140 / 0.82 | 0.120 / 0.74 |
| epoch 100 | 0.016 / 1.29 | 0.015 / 1.47 | 0.012 / 1.43 |
| epoch 200 | 0.0004 / 2.03 | 0.0004 / 2.32 | 0.0006 / 2.02 |

- train seg loss는 거의 0이 됐고 val seg loss는 2.7–2.8배 커졌다. val box loss는 계속 조금씩 줄었다(HR 0.386 → 0.320).
- 즉 **mask head 과적합이 뚜렷하다.** 다만 val mAP는 큰 폭으로 떨어지지 않았다(최고 대비 −0.017 ~ −0.031).
- **해석상 주의**
  - 선정 epoch이 일찍(32–62) 나왔다. 200 run의 epoch 32–62는 lr이 아직 높은 구간이다(lr0의 86–73%).
  - 학습 예산(epoch 수)은 연구자가 재검토할 사항이다. epoch k 시점 값은 k epoch으로 따로 학습한 결과가 아니다.

## 4. Validation 3×3 교차 평가(대표 모델, val 200장면 × 593 GT)

- 평가 코드: `analysis/eval_b1_yolo_20261108_v01.py`
- GT: HR canonical ≥100px. 100px 미만 load는 ignore.
- 예측 조건: conf 0.001, max_det 100, retina mask. 운영점은 conf 0.25 / IoU 0.5다.

| 학습 → 평가 | mAP50-95 | mAP50 | mAP75 | P | R(=검출률) | instance pixel IoU | 전경 pixel IoU |
|---|---:|---:|---:|---:|---:|---:|---:|
| **HR → HR** | **0.849** | 0.979 | 0.946 | 0.927 | 0.985 | 0.904 | 0.973 |
| HR → LR | 0.615 | 0.931 | 0.693 | 0.925 | 0.919 | 0.775 | 0.937 |
| HR → CAD | 0.627 | 0.922 | 0.693 | 0.896 | 0.901 | 0.767 | 0.921 |
| LR → HR | 0.721 | 0.970 | 0.815 | 0.893 | 0.971 | 0.842 | 0.946 |
| **LR → LR** | **0.838** | 0.979 | 0.934 | 0.920 | 0.983 | 0.896 | 0.969 |
| LR → CAD | 0.450 | 0.748 | 0.453 | 0.733 | 0.754 | 0.641 | 0.857 |
| CAD → HR | 0.527 | 0.891 | 0.569 | 0.946 | 0.791 | 0.657 | 0.885 |
| CAD → LR | 0.259 | 0.570 | 0.206 | 0.883 | 0.445 | 0.384 | 0.766 |
| **CAD → CAD** | **0.840** | 0.978 | 0.932 | 0.901 | 0.983 | 0.901 | 0.973 |

- **QA FLAG 제외** 결과는 모든 칸에서 차이가 0.002 이하다. val의 FLAG GT가 평가 표현마다 3–4개뿐이기 때문이다. FLAG 행은 per-instance 표에 남아 있다.
- 같은 표현 val 값(0.84–0.85)이 Ultralytics val(0.821–0.822)보다 높은 이유는 GT 정의(canonical full-res, <100px ignore), max_det, mask 해상도가 다르기 때문이다. 표현 간 비교는 같은 코드로만 한다.
- **편향 주의:** 같은 표현 칸은 checkpoint를 그 val로 골랐기 때문에 낙관적으로 편향될 수 있다. 교차 칸은 선정에 쓰지 않은 val 표현이다. test는 쓰지 않았다.

**같은 장면 대응 비교**(같은 평가 표현에서 학습 표현 A−B, mAP50-95 차이, 장면 bootstrap 95% CI, 1000회)

| 평가 표현 | A − B | ΔmAP50-95 [95% CI] | 장면별 pixel IoU 차이 평균(sd) |
|---|---|---|---|
| HR | HR − LR | +0.128 [+0.113, +0.143] | +0.054 (0.051) |
| HR | HR − CAD | +0.322 [+0.299, +0.345] | +0.206 (0.196) |
| HR | LR − CAD | +0.194 [+0.168, +0.219] | +0.152 (0.187) |
| LR | LR − HR | +0.224 [+0.200, +0.249] | +0.099 (0.097) |
| LR | LR − CAD | +0.579 [+0.549, +0.607] | +0.431 (0.282) |
| LR | HR − CAD | +0.356 [+0.326, +0.385] | +0.332 (0.256) |
| CAD | CAD − HR | +0.213 [+0.194, +0.233] | +0.115 (0.099) |
| CAD | CAD − LR | +0.390 [+0.357, +0.424] | +0.232 (0.180) |
| CAD | HR − LR | +0.177 [+0.152, +0.204] | +0.118 (0.136) |

- seed 1개 기준이다. CI는 장면 표본 변동만 반영하고 seed 변동은 반영하지 않는다. 동등성이나 비열등성을 주장하지 않는다(미리 정한 margin 없음).
- 비대칭
  - HR 모델은 LR과 CAD에서 0.62–0.63을 유지했다.
  - CAD 모델은 LR에서 0.26으로 크게 떨어졌다. 검출률 0.45, precision 0.88이다. 즉 오검출보다 **미검출**이 주원인이다.
  - LR 모델도 CAD에서는 0.45였다.

**층별(일부, mAP50-95 / 검출률, 칸 순서는 HR→HR, HR→LR, HR→CAD, LR→HR, LR→LR, LR→CAD, CAD→HR, CAD→LR, CAD→CAD)**

- 크기 ≥2000px(n 503): 0.90/1.00, 0.66/0.97, 0.69/0.96, 0.77/1.00, 0.89/1.00, 0.49/0.82, 0.58/0.88, 0.30/0.51, 0.89/1.00
- 크기 500–2000px(n 76): 같은 표현 0.53–0.59, 교차 0.00–0.36
- 크기 <500px(n 14): 모든 칸에서 ≈0
- 적재 층 L4(벽돌 300개 = C100, n 149): 같은 표현 0.75–0.76, 교차 0.15–0.56. L1–L3보다 교차 하락이 크다. C60/C20은 B1에 없다.
- primary(n 200): 같은 표현 0.94–0.96. 보조 load(n 393)는 같은 표현 0.76–0.78이다.
- NuRec 가림 > 10%(FLAG, n 4)와 LOW_SUPPORT(n 19)는 표본이 너무 작아 해석하지 않는다.
- 전체: `b1_baseline_seed42_fp32box_20261108_v01/metrics.csv`. per-instance(장면 ID 단위)는 root의 `eval_val_3x3_seed42_v01/per_instance.csv`(sha 7b9b049c…)에 있다.

## 5. 남은 문제

1. **사람 QA 최종 검토 미완료.** FLAG / LOW_SUPPORT와 라벨 판정은 사람 승인 전이다.
2. **seed 1개.** seed별 평균과 표준편차, 표현 간 차이의 seed 변동은 seed 43/44 이후에 나온다(연구자 승인 필요).
3. **학습 예산:** 세 표현 모두 epoch 32–62에서 최고였고 그 뒤로 mask 과적합이 보였다. 200 epoch 유지 여부와 공통 예산 재검토는 연구자가 결정한다. 바꾼다면 recipe 개정이고, seed 43/44 전에 정하는 것이 일관적이다.
4. 같은 표현 val 칸에는 선정 편향이 있다. 최종 비교는 test에서, 평가 절차를 잠그고 승인받은 뒤에 한다.
5. GPU peak 메모리가 epoch에 따라 10.4 → 14.8GB로 꾸준히 늘었다. 원인은 확인하지 않았다(OOM은 없었다).
6. v02 FP16 실패 run은 별도 진단 자료다(`reports/b1_fp32_boxloss_verification_20261108.md`).

## 파일

- 신규: `scripts/run_b1_baseline_seed42_20261108_v02.sh`
- 보고서 첨부: `reports/b1_baseline_seed42_fp32box_20261108_v01/`
  - 곡선 그림, epoch 표, checkpoints/last30/convergence
  - 3×3 metrics, paired, seed_aggregate, late-state probe 요약
- root: `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_BASELINE_FP32BOX_20261108_v01`
  - run 3개(audit, epochs, weights), learning_curves, eval, diag probe, driver/wrapper 로그, input_hashes
