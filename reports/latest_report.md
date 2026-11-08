# v42 GPU 재현 2개 · B1 사람 검토 자료 · 공통 YOLO recipe 초안 (2026-11-08)

성격: 연구자가 승인한 engineering 재현(GPU 약 45초) + 검토 자료 + recipe 초안. **본 학습 0, HPO 0.** B1 데이터, QA, 라벨, split은 변경 없음. Real Test189는 사용하지 않았다.

## 요약

| 항목 | 판정 |
|---|---|
| 실험 B — Ray checkpoint 복원 후 optimizer 진행(batch 64, accumulate 1) | **PASS** |
| 실험 A v01 — gradient accumulation 조건(batch 6, accumulate 11)에서 실제 AdamW step | **FAIL**: 실험 설계 결함(AMP scaler 초기값). 기록 보존 |
| 실험 A **v02** — 같은 실험을 v42c scaler(init 128)로 1회 다시 실행(연구자 승인) | **PASS** |
| 사람 검토 자료 | 준비 완료. **검토는 미실행**이고 판정 칸은 비어 있다 |
| 공통 recipe | DRAFT v01 작성. 결정 항목 6개가 비어 있다 |
| 학습 가능 상태 | **조건부 가능.** 데이터와 batch 64 경로는 준비됐다. recipe 결정과 실행 승인이 남았다 |

## 1. GPU 재현

- root: `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_REPRO_20261108_v01`(v42 root는 읽기만 함)
- driver: `scripts/run_v42_gpu_repro_20261108_v01.sh`. 실험마다 1회만 실행했고 재시도는 없다. stdout/stderr와 command json을 보존했다.
- 판정은 결과 JSON과 checkpoint로 했다. exit code는 모두 0이었지만 판정에 쓰지 않았다.
- 실행 시각 15:47:01–15:47:45

### 실험 B — Ray 복원 후 학습 진행: **PASS**

- 스크립트: `scripts/bitmap_ray_resume_v42r_20261108.py`. v42c를 복사했고 원본(sha `fddcbd72…139e`)은 수정하지 않았다.
- 바꾼 것
  - root
  - train 64장(v42 `batch64_records.json`)과 v42와 같은 val 6장
  - batch 6 → 64, workers 2 → 8
  - 증거 기록 추가(EMA updates, 가중치 fingerprint, train_end)
- 그대로 둔 것: 모델, AdamW, seed, AMP(init_scale 128), no-aug, Optuna/ASHA, raw_state 복원과 exact 검사, 첫 checkpoint 직후의 의도적 SIGINT
- gate: `analysis/v42r_ray_gate_20261108_v01.py` → `exp_B_gate.json`(dbc86fe7…). raw_state를 checkpoint_000000과 checkpoint_000001에서 직접 비교했다.

| 검사 | checkpoint_000000(epoch 1, 중단 전) | checkpoint_000001(epoch 2, 복원 후) | 결과 |
|---|---:|---:|---|
| AdamW step | 1 | **2** | PASS |
| real_updates | 1 | **2** | PASS |
| EMA updates | 1 | **2** | PASS |
| scaler `_growth_tracker` | 1 | 2 (scale 128 유지, skip 0) | PASS |
| 바뀐 model tensor | — | 560개(float 471개 전부 finite), 최대 변화 1.0 | PASS |

- 복원 직후 exact 검사 PASS: weights, optimizer, scaler, scheduler, EMA. 재개 epoch은 1(0부터 셈)이다.
- `ray_interrupt.json`이 남아 있어 의도적 중단이 확인된다. 복원 결과에 오류가 없고 mAP50-95(M) 0.00461이다(유한값인지만 확인했고 성능 의미는 없다).
- **결론:** v42의 "복원 후 step 1→1"은 batch 64(accumulate 1)에서는 재현되지 않았다. 복원 뒤 optimizer, EMA, 가중치가 정상적으로 갱신된다. 11-06 정적 분석의 예측(ep2 step 1)과 같다.
- 참고 사항(판정에는 영향 없음)
  - 복원 세션의 `train_start` 이벤트에 `workers=0`이 기록됐다. Ray trial 안에서 Ultralytics가 실제 loader worker를 몇 개로 정했는지는 따로 확인하지 않았다.
  - 첫 세션의 runtime 이벤트는 복원 뒤 trial 로그에 남아 있지 않았다. 그래서 첫 세션 값은 checkpoint_000000의 raw_state로 판정했다.

### 실험 A — accumulation 조건의 실제 step: **FAIL(실험 설계 결함)**

- 스크립트: `scripts/bitmap_accum_repro_20261108_v01.py`. Ray 없이 2 epoch을 연속으로 돌렸고 batch 6(accumulate 11)이다.
  - A1 대조군: v42 tiny 데이터(train 9장)
  - A2: train 64장
- 결과 파일: `exp_A_result.json`(6149e5c4…)

| run | 예측(정적 replay): optimizer_step 호출 ni | EMA updates(epoch 1→2) | 실제 AdamW step | 가중치 변화 |
|---|---|---|---|---|
| A1 | ep1 [0], ep2 [] | 1 → 1 | **0** | 없음 |
| A2 | ep1 [0, 5], ep2 [15] | 2 → 3 | **0** | 없음 |

- **확인된 것:** `optimizer_step()` 호출 횟수가 정적 예측과 정확히 같다(A1 1회, A2 3회). EMA 갱신은 이 함수 안에서만 일어나므로, accumulation 스케줄 계산 자체는 GPU 실행으로 확인됐다.
- **실패한 것:** 그 호출들에서 AdamW step이 한 번도 실행되지 않았다. state step 0, 가중치 불변.
- **원인(강한 추정):** AMP GradScaler가 step을 건너뛰었다.
  - 이 스크립트는 v42c `StrictTrainer`의 `init_scale=128` 설정을 가져오지 않았다. 그래서 Ultralytics 기본값 65536으로 시작했다.
  - v42 실측 gradient absmax는 약 114였다. 114 × 65536 ≈ 7.5M으로 fp16 최대값 65504를 넘는다. 따라서 inf가 생기고 `scaler.step`이 optimizer를 건너뛴다.
  - v41c와 v42가 scale을 128로 고친 이유와 같은 현상이다.
  - 다만 scale 값 자체는 로그에 남기지 않았다. 성공한 step만 기록했기 때문이다. 그래서 "추정"이다.
  - 이것은 **내 실험 설계의 실수**다. Ultralytics나 v42 코드의 결함이 아니다.
- 지시에 따라 설정을 바꾼 재실행은 하지 않았다.
  - 제안: v02 스크립트에서 v42c `StrictTrainer`(init_scale 128)를 그대로 상속해 A1과 A2를 다시 1회 돌린다. 약 15초 걸린다. 승인이 필요하다.
- 영향: baseline recipe는 batch 64(accumulate 1)를 쓰므로 이 실패가 baseline을 막지 않는다. accumulate > 1의 실제 갱신 여부는 아래 v02에서 확인했다.

### 실험 A v02 — 같은 조건, v42c scaler: **PASS**(연구자 승인 후 1회 실행)

- 스크립트: `scripts/bitmap_accum_repro_20261108_v02.py`(33da0820…)
  - v01 대비 바꾼 것은 한 가지다. trainer가 v42c `StrictTrainer`(init_scale 128)를 상속한다.
  - 기록을 늘렸다. 모든 `optimizer_step()` 호출에서 scale과 AdamW counter를 남긴다.
  - 데이터, batch 6, seed, lr, epoch은 v01과 같다.
- 결과 파일: `exp_A_accum_v02/exp_A_result.json`(1177f133…). command json과 stdout/stderr를 보존했다.

| run | 예측 step ni | 관측 step ni | AdamW counter(epoch 1 / 2 끝) | EMA | scale | 가중치(epoch 1→2) |
|---|---|---|---|---|---|---|
| A1 대조군(train 9) | ep1 [0], ep2 [] | ep1 [0], ep2 [] | 1 / 1 | 1 / 1 | 128, skip 0 | 불변(예측대로 ep2 step 0) |
| A2(train 64) | ep1 [0, 5], ep2 [15] | ep1 [0, 5], ep2 [15] | 2 / 3 | 2 / 3 | 128, skip 0 | **변경** |

- **확인된 것**
  1. accumulate > 1 조건에서 optimizer step이 Ultralytics 스케줄 예측대로 정확히 증가하고, 그때마다 실제로 갱신된다(A2).
  2. v42 tiny 구성은 **복원 없이 연속으로 학습해도 epoch 2에서 step이 0**이다(A1). 따라서 v42의 "복원 후 step 1→1"은 Ray 문제가 아니라 데이터 9장, batch 6, accumulate 구조 때문이었다. 이제 GPU 실측으로 확정됐다.
- v01의 실패 원인 추정(scale 65536에서 overflow로 skip)은 v02로 간접 확인했다. scale만 128로 바꾸자 모든 호출이 실제 step이 됐다.
- **남는 주의:** accumulate > 1이면 `last_opt_step`과 누적 중인 gradient가 checkpoint에 저장되지 않는다. 그래서 중간에 복원하면 연속 학습과 궤적이 같지 않다. 이는 batch 64(accumulate 1)를 쓰는 이유이기도 하다.
- 부수 사항: Ultralytics AMP 사전 검사가 `yolo26n.pt`를 내려받아 `scripts/weights/yolo26n.pt`(5.5MB)를 만들었다. 학습에는 쓰이지 않는다. v42 때도 같은 동작이 있었다(`weights/yolo26n.pt`). 이 파일은 지우지 않고 그대로 두었다.

## 2. 사람 QA 검토 자료 — 준비 완료(검토 미실행)

- 생성 스크립트: `analysis/b1_human_review_pack_20261108_v01.py`
- 위치: `reports/b1_human_review_pack_20261108_v01/`
  - `panels/` 30장
  - `review_checklist.md`, `review_checklist.csv`
  - `pack_meta.json`
- 사례 30개
  - FLAG 전부 18개(train 10 / val 4 / test 4)
    - 필수 사례 VAL_000148 Load_03(#17)과 TST_000188 Load_05(#13)도 FLAG에 포함되어 있다.
  - LOW_SUPPORT 표본 6개(split별 2개)
  - 정상 primary 표본 6개(split별 2개)
  - 표본은 seed 20261108로 무작위 추출했다.
- 패널 구성: 행은 HR / LR / CAD이고, 열은 다음 네 가지다.
  1. RGB + GT mask(초록) / 실제 mask(빨강)
  2. YOLO 라벨 polygon(청록)
  3. 확대 RGB
  4. 확대 `|I−E|>τ`(흰색 = 보임, 자홍 = 가림)
  - 행마다 vis, 가림률(1−vis), px_e2, QA 판정을 적었다.
- 체크리스트 질문: Q1 실제 가림인가, Q2 판정에 동의하는가, Q3 GT가 맞는가, Q4 polygon이 맞는가, 그리고 최종 판단. **모든 칸이 비어 있다.**
- AI 판독은 체크리스트에 적지 않았다.

## 3. 공통 YOLO recipe — DRAFT v01

- 문서: `docs/b1_yolo_baseline_recipe_DRAFT_20261108_v01.md`(5e4a6f21…)
- 고정 설정
  - 데이터: B1 패키지(1000 / 200 / 200)
  - 모델: yolo11n-seg.pt(55ed65c5…)
  - AdamW, lr0 0.001, lrf 0.1, wd 0.0005, warmup 3
  - batch 64(accumulate 1), workers 8, imgsz 640
  - epochs 60(조기 종료 없음), seed 42, deterministic, AMP(init_scale 128), v41 no-aug, mask_ratio 4
  - best.pt는 val로만 고른다. test는 한 번만 평가한다.
- v42와 다른 점
  - dataset/trainer: B1은 polygon 형식이라 표준 trainer를 쓰고, AMP scale만 v42와 같게 맞춘다.
  - epochs 60: v40 Stage-1 계획값이다.
  - mask_ratio: v42 full-pilot은 2, 기본값과 Ray 탐색은 4였다. 결정 항목이다.
  - 근거는 문서 §3에 적었다.
- HPO는 baseline 뒤의 별도 단계다. Stage-1 entrypoint를 B1용으로 새로 만들어야 한다.
- 결정 항목(빈칸)
  1. seed 수(권장 3)
  2. no-aug 정책
  3. mask_ratio
  4. 교차 평가
  5. epochs
  6. 사람 검토 시점

## 4. 학습 가능 상태 판정

- 데이터: **READY.** 패키지 COMPLETE, data.yaml 3개, QA 열 준비.
- 학습 경로(batch 64, accumulate 1): **READY**(실험 B). 복원 후에도 optimizer, EMA, 가중치가 갱신된다.
- accumulate > 1 경로: **확인**(실험 A v02 PASS). 다만 이 경로에서는 복원했을 때 궤적이 연속 학습과 같지 않다.
- recipe: **DRAFT.** 결정 항목 확정, 잠금, 실행 승인이 필요하다.
- B1용 학습 스크립트: **미작성.** 잠근 recipe로 만들고 1 epoch smoke를 따로 돌려야 한다.
- 사람 QA 검토: **미실행.** 라벨에 영향이 없어 학습을 막지는 않는다. 다만 "FLAG 제외" 분석 해석에는 필요하다.
- 종합: **조건부 학습 가능.** recipe를 확정하고 승인하면 smoke 1회 → baseline 순서로 진행할 수 있다.

## 5. 남은 문제

1. ~~실험 A v02~~ 완료(PASS)
2. recipe 결정 항목 6개
3. B1 학습 스크립트, FLAG 제외 load 단위 평가 스크립트 작성(미작성)
4. HPO용 B1 Stage-1 entrypoint(미작성)
5. 사람 검토 수행
6. Ray trial 안 loader workers=0 기록 확인(성능 문제일 뿐, 정확성 문제는 아님)

## 파일

- 신규 코드
  - `scripts/bitmap_accum_repro_20261108_v02.py`(A v02)
  - `scripts/bitmap_accum_repro_20261108_v01.py`
  - `scripts/bitmap_ray_resume_v42r_20261108.py`
  - `scripts/run_v42_gpu_repro_20261108_v01.sh`
  - `analysis/v42r_ray_gate_20261108_v01.py`
  - `analysis/b1_human_review_pack_20261108_v01.py`
  - 해시는 repro root의 `input_hashes.txt`에 있다.
- 신규 문서: `docs/b1_yolo_baseline_recipe_DRAFT_20261108_v01.md`
- 보존: 실험 A의 FAIL 결과, 모든 stdout/stderr, v42 원본 출력과 코드
