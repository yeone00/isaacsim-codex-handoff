# B1 seed 42 본 학습 — HR epoch 182에서 FAILED, LR/CAD 미실행 (2026-11-08)

성격: 연구자가 승인한 seed 42 본 학습(recipe LOCKED v02, 200 epoch, HR → LR → CAD). **HR run이 FAILED로 끝나 지시대로 중단했다.** 재시도 0, 설정 변경 0. LR/CAD 학습, val 3×3 평가, seed 43/44, HPO, test는 모두 0. 실패 로그와 checkpoint를 보존했다.

## 1. 무슨 일이 있었나

- driver: `scripts/run_b1_baseline_seed42_20261108_v01.sh`, root `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_BASELINE_20261108_v01`
- HR 시작 16:55:47 → 종료 17:07:22, `run_status.json` state=**FAILED**
  - error: `RuntimeError('nonfinite loss; no retry')`
  - driver가 exit 10으로 멈췄다. LR과 CAD는 시작하지 않았다.
- 실패 지점: **epoch 182**. 마지막 batch의 box loss가 inf였고, 학습 스크립트의 "non-finite loss면 즉시 실패, 재시도 없음" 검사(`_handle_nan_recovery` override)에 걸렸다.
  - Ultralytics 기본 동작이라면 last.pt로 되돌려 최대 3회 재시도했을 것이다. 이 기능은 재시도 금지 원칙에 따라 꺼 두었다.
- **사실 그 전부터 같은 현상이 있었다.** epoch 107, 118, 120, 140, 146, 167, 171, 179에서 epoch 중간 batch 하나의 box loss가 inf였다.
  - 그때마다 AMP GradScaler가 해당 step을 건너뛰고 scale을 절반으로 줄였다(64 → 32 → … → 0.125).
  - 학습은 계속됐다. 스크립트 검사는 epoch 마지막 batch의 loss만 보기 때문에 epoch 182 전까지는 걸리지 않았다.
- 전체 optimizer_step 호출 2912회 중 건너뛴 것은 10회다. epoch 1의 초기 scale 조정 1회 + inf batch 9회다.

## 2. 실패 전까지의 HR 학습곡선(181 epoch, 진단용 — 결과로 쓰지 않음)

진단 분석 출력: `…/learning_curve_HR_failed_diag_v01/`. 그림: `b1_baseline_seed42_HR_failure_20261108_v01/curves_HR_Scan_seed42_FAILED.png`

| epoch | train box / seg loss | val box / seg loss | val mask mAP50 / 75 / 50-95 | lr | AMP scale | GPU peak |
|---:|---|---|---|---:|---:|---:|
| 10 | 0.415 / 0.385 | 0.525 / 0.76 | 0.973 / 0.815 / 0.735 | 9.6e-4 | 64 | 10.4 GB |
| 30 | 0.251 / 0.127 | 0.403 / 0.75 | 0.958 / 0.849 / 0.755 | 8.7e-4 | 64 | 10.9 GB |
| 60 | 0.173 / 0.051 | 0.362 / 0.90 | 0.973 / 0.901 / 0.814 | 7.3e-4 | 64 | 11.6 GB |
| **95(최고)** | 0.149 / 0.029 | 0.349 / 1.08 | 0.973 / 0.907 / **0.821** | 5.8e-4 | 64 | 12.4 GB |
| 100 | 0.136 / 0.018 | 0.344 / 1.26 | 0.974 / 0.899 / 0.820 | 5.5e-4 | 64 | 12.5 GB |
| 150 | 0.089 / 0.0025 | 0.332 / 1.78 | 0.973 / 0.893 / 0.811 | 3.3e-4 | 2 | 13.7 GB |
| 181 | 0.074 / 0.0010 | 0.328 / 2.14 | 0.973 / 0.889 / 0.808 | 1.9e-4 | 0.25 | 14.4 GB |

- 마지막 30 epoch(152–181) 동안 val mask mAP50-95는 평균 0.811 ± 0.004, 기울기 −0.0004/10 epoch이었다. 제안 기준으로 읽으면 **PLATEAU**(변화 거의 없음)다.
- 최고값은 **epoch 95**(0.821)였다. 그 뒤로는 완만하게 떨어졌다.
- **과적합 신호:** train seg loss는 0.38에서 0.001로 계속 줄었다. 반면 val seg loss는 epoch 30의 0.75에서 epoch 181의 2.14로 커졌다.
- 참고(한 seed, 실패한 run): HR에서는 200 epoch까지 갈 필요가 없어 보인다. 그러나 LR/CAD와 다른 seed가 없으므로 결론은 내리지 않는다.
- epoch당 학습+val 시간은 3.8초다. GPU peak 메모리가 10.4GB에서 14.4GB로 점점 늘었다. 원인은 확인하지 않았다.

## 3. 원인 분석

- **이미지와 라벨 원인은 아닌 것으로 보인다.** `analysis/b1_nonfinite_loss_diag_20261108_v01.py`로 확인했다.
  - 실패 run의 last.pt(epoch 181 EMA 가중치)로 train 1000장을 한 장씩 넣고 loss만 계산했다. 학습과 가중치 변경은 없다.
  - fp16 autocast와 fp32 모두에서 **1000장 전부 box/seg loss가 유한**했다. fp32 box loss 최대는 0.62다.
  - 결과: `…/diag_nonfinite_loss_v01/`
- 따라서 inf는 특정 이미지 때문이 아니다. **학습 중의 조건에서만** 생기는 것으로 보인다.
  - 그 조건: EMA가 아닌 원 가중치, BN의 batch 통계, 64장 batch 구성, fp16 forward와 loss
  - 위 진단은 그 조건을 재현하지 못했다. last.pt에는 원 가중치(`model`)가 저장되지 않는다.
  - 그래서 **수치적 정확한 원인(CIoU 계산의 fp16 범위 등)은 UNCONFIRMED**다.
- 정황
  - inf는 train box loss가 작아진 후반(epoch 107 이후)에만 나타났다.
  - 매번 box loss 하나만 inf였고 seg/cls/dfl은 유한했다.
  - inf batch가 생길 때마다 GradScaler가 그 step을 건너뛰어, **가중치는 오염되지 않았다.** 다음 epoch의 val 지표도 정상이었다.
- 부작용: scale이 128 → 0.125로 계속 줄었다. growth_interval이 2000이라 다시 커지지 않는다. scale < 1이면 작은 gradient가 fp16에서 0이 될(underflow) 위험이 있다.
- 감사 로직 관점: Ultralytics의 epoch 평균 train loss(tloss)는 inf batch를 포함해 계산한다. 그래서 inf가 있었던 epoch은 loss가 inf로 기록됐다. 학습이 끝났더라도 v04의 `finite_losses` 검사는 FAIL이었을 것이다.

## 4. 다음 진행을 위한 선택지(연구자 결정 필요 — 아무것도 실행하지 않았음)

| 안 | 내용 | recipe 변경 | 장단점 |
|---|---|---|---|
| **A(권장)** | 학습 스크립트 v05: GradScaler가 건너뛴 non-finite batch는 "AMP skip"으로 세고 run을 실패시키지 않는다. 실패 조건은 non-finite batch > 1%, scale < 2⁻⁸, 연속 3 batch 이상으로 정한다. inf batch의 이미지 목록과 loss 항목을 기록하고, epoch loss는 유한 batch만으로 따로 기록한다 | 없음(감사 정책만 바뀜) | 이번 HR에서 실제로 일어난 학습 경로(skip 후 계속)와 같다. scale 감소 위험은 감시로 대응한다 |
| B | loss 계산만 fp32로 한다(forward는 AMP 유지) | v03 amendment | 원인일 가능성이 높은 부분을 직접 제거한다. 수치 경로가 바뀐다 |
| C | AMP를 끈다(fp32 학습) | v03 amendment | 가장 안전하다. 느려지고 메모리가 늘며 v42 검증 조건과 달라진다 |
| D | Ultralytics 기본 NaN 복구(last.pt로 되돌려 최대 3회) | 스크립트 정책 변경 | 재시도에 해당하므로 기존 원칙과 충돌한다 |

- 어느 안이든 HR부터 새 디렉터리에서 다시 돌린다. 실패한 HR run은 그대로 보존한다.
- A안이라면 HR의 결과 경로는 이번 실패 run과 거의 같을 것으로 예상한다. 비트 단위로는 같지 않다.
- HR 곡선은 epoch 95 이후 개선이 없었다. 다만 epoch 수를 바꾸는 것은 recipe 변경이고 이번 범위가 아니다. LR/CAD 곡선까지 본 뒤 판단하는 것을 권한다.

## 5. 보존한 파일

- `…/B1_YOLO_BASELINE_20261108_v01/`
  - `driver.log`, `wrapper.log`, `input_hashes.txt`
  - `HR_Scan_seed42/`(run_status FAILED와 traceback, audit.json, epochs.jsonl, last.pt(epoch 181), best.pt, `best_val_maskmAP5095.pt`(epoch 95, sha 105b62c8…))
  - `diag_nonfinite_loss_v01/`, `learning_curve_HR_failed_diag_v01/`
- 신규 코드: `analysis/b1_nonfinite_loss_diag_20261108_v01.py`
