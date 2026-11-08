# B1 YOLO 학습 준비: recipe 잠금 · 1 epoch smoke · 라벨 점검 · 평가 코드 (2026-11-08)

성격: 연구자가 승인한 준비 단계다. **60 epoch 본 학습 0, HPO 0, test 사용 0.** 기존 데이터, 라벨, QA, split은 변경하지 않았다(package_checks sha `3ff0a45e…` 재확인, 패키지 안에 `.cache` 생성 0).

GPU 재현(v42)은 완료로 정리한다: B PASS, A v01 FAIL(설계 결함, 보존), A v02 PASS.

## 요약

| 항목 | 결과 |
|---|---|
| recipe | **LOCKED v01**(md `cd3645e8…`, json `c9b2458c…`) |
| 학습 스크립트 | `scripts/train_b1_yolo_20261108_v02.py`. v01은 감사 로직 결함으로 FAIL_AUDIT, 보존 |
| 1 epoch smoke, seed 42 | HR / LR / CAD 모두 **PASS**(v02) |
| 라벨 → 학습 마스크 점검 | 완료. 아주 얇은 보조 load **4개가 학습에서 자동 제외**된다(아래 §3) |
| 평가 코드 | `analysis/eval_b1_yolo_20261108_v01.py`. val 3×3 smoke 동작 확인. test 차단 확인 |
| 사람 검토 안내 | `reports/b1_human_review_pack_20261108_v01/REVIEW_GUIDE.md`. 판정 칸 비어 있음 |
| 본 학습 준비 상태 | **기술적으로 준비됨.** 남은 것은 사람 검토와 본 학습 승인이다 |

## 1. Recipe 잠금

- 지시받은 값 그대로다.
  - YOLO11n-seg(같은 pretrained, `55ed65c5…`), seed 42 / 43 / 44
  - augmentation 없음, mask_ratio 4, 60 epoch(조기 종료 없음)
  - AdamW, lr0 0.001, lrf 0.1, wd 0.0005, warmup 3
  - batch 64, imgsz 640, workers 8, AMP scale 128
  - 선정: val mask mAP50-95. test는 평가 절차를 잠근 뒤에만 쓴다.
- JSON에 기록한 SHA: 패키지, data.yaml 3개, records, train / val / test label set, QA CSV, 가중치, Ultralytics 소스 6개
- Ultralytics 기본 best.pt는 box+mask를 합친 fitness로 고른다. 그래서 val mask mAP50-95로 고르는 별도 checkpoint(`best_val_maskmAP5095.pt`)를 스크립트에서 저장한다.

## 2. 1 epoch smoke(GPU 실측, seed 42)

- root: `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_SMOKE_20261108_v01`
- run마다 stdout/stderr, command json, run_status, audit, epochs.jsonl을 보존했다.

| 항목 | HR | LR | CAD |
|---|---|---|---|
| 판정(v02) | PASS | PASS | PASS |
| optimizer_step 호출 / 실제 AdamW 갱신 | 16 / 13 | 16 / 14 | 16 / 13 |
| AMP overflow skip(scale 변화) | 3 (128→16) | 2 (128→32) | 3 (128→16) |
| EMA updates | 16 | 16 | 16 |
| 가중치 변화(fingerprint Δ) | +2350 | +2448 | +2280 |
| train loss box / seg / cls / dfl | 2.51 / 8.25 / 3.09 / 2.34 | 2.24 / 5.67 / 2.85 / 1.98 | 2.11 / 7.34 / 2.74 / 1.96 |
| val loss box / seg / cls / dfl | 1.96 / 20.4 / 3.93 / 4.61 | 2.21 / 34.8 / 3.57 / 5.22 | 2.38 / 60.7 / 3.98 / 11.3 |
| val mask mAP50-95 / mAP50(1 epoch, 의미 없음) | 0.0039 / 0.013 | 0.0022 / 0.009 | 0.0179 / 0.073 |
| GPU peak allocated / reserved | 10.2 / 11.5 GB | 10.2 / 11.5 GB | 10.2 / 11.5 GB |
| train epoch 시간 / run 전체 | 5.8 s / 12 s | 5.9 s / 12 s | 5.8 s / 12 s |
| 데이터 | train 1000 / val 200, corrupt 0 | 같음 | 같음 |
| loader workers / nb / accumulate | 8 / 16 / 1 | 같음 | 같음 |

- **AMP overflow:** 처음 2–3 step은 scale 128에서 overflow가 나서 GradScaler가 그 step을 건너뛰고 scale을 줄였다. 그 뒤로는 scale 16–32에서 skip 없이 진행됐다.
  - 이는 GradScaler가 설계대로 동작한 것이다.
  - B1은 v42 데이터보다 gradient가 커서, 128로는 첫 몇 step만 건너뛴다.
  - growth_interval이 2000이므로 60 epoch(960 step) 동안 scale이 다시 커지지 않는다. 추가 skip은 거의 없을 것으로 본다.
  - v02 감사 기준: skip이 max(5, 1%)를 넘으면 FAIL.
- **v01 smoke(HR) FAIL_AUDIT:** 보존했다. 학습 자체는 정상이었고, 원인은 감사 로직 두 가지다.
  1. skip을 0으로 요구했다.
  2. Ultralytics `final_eval()`이 `on_fit_epoch_end`를 epoch+1로 한 번 더 부르는데, 이를 걸러내지 않아 선정 checkpoint가 "epoch 2"로 잘못 기록됐다.
  - v02는 이 두 가지만 고쳤다. 학습 인자와 데이터는 그대로다.
- **결정론:** 같은 설정의 HR v01과 v02에서 val mAP가 0.00399 vs 0.00394로 아주 조금 달랐다. deterministic=True여도 GPU 연산이 비트 단위로 재현되지는 않는다. 그래서 seed 3개의 평균과 표준편차로 보고한다.
- 예상 본 학습 시간: epoch당 약 7–8초 × 60 → run당 약 8–10분, 9 run이면 약 1.5시간이다. smoke로 외삽한 값이다.

## 3. 라벨 → 학습 마스크 점검

- 스크립트: `analysis/b1_label_pipeline_check_20261108_v01.py`
- 결과: smoke root의 `label_pipeline_check_v02/`
  - 첫 실행은 instance 수 assert로 멈췄고, `label_pipeline_check_v01_ABORTED_assert`로 보존했다.
- 방법: Ultralytics가 실제로 학습에 넣는 160×160 mask를 정답 canonical mask(같은 letterbox, 축소)와 instance마다 비교했다. 대상은 train 2969개, val 593개다.

**(1) Ultralytics가 자동으로 빼는 instance — 얇은 보조 load**

- train에서 4개가 빠진다: TRN_000425 L4, 000887 L4, 001061 L4, 001154 L4
  - canonical 202–243px, 폭 약 110px, **높이 1–3px**인 띠 모양이다.
  - Ultralytics `box_candidates`(폭과 높이가 2px보다 커야 함)가 이를 버린다. 전체 train instance의 0.13%다.
- val은 이 필터를 거치지 않지만, VAL_R000193_01의 L4와 L5(높이 1–4px)는 160×160 mask가 0–3px로 거의 비어 있다.
- 라벨 파일은 그대로다. 학습에서만 빠진다.
- 평가 코드는 이들을 GT로 그대로 포함한다. 그래서 놓치면 미검출로 집계된다.

**(2) 크기별 학습 mask와 정답의 일치도(IoU)**

| canonical 크기 | n | 중앙값 | 하위 5% |
|---|---:|---:|---:|
| ≥2000px | 2973 | 0.980 | 0.913 |
| 500–2000px | 482 | 0.952 | 0.722 |
| 200–500px | 92 | 0.925 | 0.349 |
| 100–200px | 10 | 0.532 | 0.143 |

- 작은 보조 load는 mask_ratio 4(4배 축소) 때문에 학습 mask가 거칠다.
- IoU가 0.5 미만인 instance는 13개다. 모두 높이 1–4px인 띠다.

**(3) 불연속 마스크의 인공 연결**

- canonical mask가 2조각 이상인 instance는 61개다.
- polygon은 61개 모두 **하나로 이어져** 있다(왕복 연결선).
- 그 연결선이 정답 밖에 더하는 면적은 원본 해상도에서 **최대 12px**이다. 전체 instance 기준으로도 최대 23px이다.
- 버려진 1–2px 조각 때문에 놓치는 정답 면적은 최대 30px이다.
- 따라서 인공 연결의 실제 면적 영향은 무시할 수준이다. 다만 위상(조각이 하나로 이어짐)은 바뀐다.
- 예시: `reports/b1_yolo_smoke_20261108_v01/label_overlays/`(8장. 왼쪽 원본 해상도, 오른쪽 160×160 학습 mask. 초록 = 일치, 자홍 = 추가됨, 파랑 = 빠짐)

## 4. 평가 코드

- 스크립트: `analysis/eval_b1_yolo_20261108_v01.py`
- 평가 범위: 같은 표현 평가와 3×3 교차 평가
- 지표
  - mask mAP50-95, mAP50, mAP75(COCO 101-point)
  - 운영점(conf 0.25, IoU 0.5)에서 precision, recall, 검출률, instance pixel IoU, 이미지 전경 pixel IoU
- GT
  - HR canonical mask 중 100px 이상(= 라벨 집합)
  - 100px 미만 load는 ignore 영역으로 둔다. 그 위의 예측은 FP로 세지 않는다.
- **FLAG 포함 / 제외**
  - 제외 집계에서는 FLAG GT를 ignore 영역으로 둔다.
  - per-instance 표에는 FLAG 행이 그대로 남는다. 원자료에서 삭제하지 않는다.
- 층별(strata) 분석
  - QA 판정
  - NuRec 가림률 구간(1−vis: ≤1% / 1–5% / 5–10% / >10% / LOW_SUPPORT)
  - primary 여부, 적재 층 L1–L4, ROI, 거리 bin, 크기 구간
- **C100/C60/C20:** B1 데이터에는 이 축이 없다. B1에는 적재 층 L1–L4(벽돌 75 / 150 / 225 / 300개 = 25 / 50 / 75 / 100%)만 있다. 코드는 L1–L4로 층별 집계하고, C100은 L4와 같다고 명시했다. C60과 C20은 "해당 없음"으로 기록한다.
- 대응 비교
  - 같은 평가 표현에서 학습 표현 쌍(A−B)의 mAP50-95 차이를 계산한다. 신뢰구간은 장면 단위 bootstrap이다.
  - 장면별 pixel IoU 차이도 계산한다.
  - 동등성은 주장하지 않는다(미리 정한 margin 없음).
- seed별 평균과 표준편차: `seed_aggregate.csv`
- **test 차단:** `--split test`는 LOCKED 평가 절차 JSON이 없으면 거부한다. smoke 모델로는 test를 쓸 수 없다. 음성 대조군으로 거부되는 것을 확인했다.
- smoke 실행: smoke 모델 3개로 val 3×3, bootstrap 200, 164초 → `eval_smoke_val_3x3_v02/`
  - 첫 실행 v01에서 **버그를 발견해 고쳤다.** IoU를 fp16으로 계산해서 큰 mask에서 inf가 나왔다. fp32로 바꿨다.
  - v01 출력은 `INVALID_fp16_iou_overflow.txt` 표시를 붙여 보존했다.
  - 같은 표현에서의 mAP가 Ultralytics val과 비슷한 수준이다(HR 0.0045 vs 0.0039, LR 0.0027 vs 0.0022, CAD 0.0189 vs 0.0179). 차이는 GT 정의(canonical mask와 ignore), max_det 100 대 300, mask 해상도 때문이다. 1 epoch 모델이라 수치 자체에는 의미가 없다.

## 5. 사람 검토 안내

- `reports/b1_human_review_pack_20261108_v01/REVIEW_GUIDE.md`
  - 절대경로 30개
  - 권장 순서: 정상 6 → 판정이 갈린 2 → FLAG 16 → LOW_SUPPORT 6
  - `eog` 명령
- 판정 칸은 비어 있다.

## 6. 전체 준비 상태와 남은 문제

- **준비됨:** recipe 잠금, 학습 스크립트(감사, 선정, gate), 3표현 smoke PASS, 데이터와 라벨 로딩, 평가 코드(val), test 차단
- **남은 일**
  1. 사람 QA 검토(연구자)
  2. 60 epoch × 9 run 본 학습 승인
  3. test 평가 전에 "평가 절차" LOCKED JSON 작성과 승인(본 학습 후)
- **알려진 제한**(라벨은 잠긴 것이라 바꾸지 않음)
  - 높이 2px 안팎의 띠 모양 보조 load 4개는 학습에서 빠진다.
  - 200px 미만의 작은 load는 mask_ratio 4 때문에 학습 mask가 거칠다.
  - 불연속 mask는 연결선으로 위상이 바뀐다(면적 영향 ≤12px).
  - 비트 단위 재현성은 없다.
- 기타: v42 GPU 재현 때 AMP 검사가 내려받은 `scripts/weights/yolo26n.pt`는 그대로 두었다.

## 파일

- 신규 문서
  - `docs/b1_yolo_baseline_recipe_LOCKED_v01_20261108.md`
  - `docs/b1_yolo_baseline_recipe_LOCKED_v01_20261108.json`
- 신규 코드
  - `scripts/train_b1_yolo_20261108_v01.py`(FAIL_AUDIT 기록용으로 보존)
  - `scripts/train_b1_yolo_20261108_v02.py`
  - `analysis/b1_label_pipeline_check_20261108_v01.py`
  - `analysis/eval_b1_yolo_20261108_v01.py`
- 해시: smoke root의 `input_hashes.txt`
- smoke 선정 checkpoint sha: HR 18593216…, LR 8da7a42c…, CAD 65dd0f0e…(smoke 전용, 결과로 쓰지 않음)
