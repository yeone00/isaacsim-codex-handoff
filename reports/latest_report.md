# B1 YOLO recipe v02(200 epoch) 잠금 · 200 epoch 대응 검증 · 학습곡선 분석 준비 · 사람 검토 패키지 (2026-11-08)

성격: 준비 단계다. **200 epoch 본 학습 0, HPO 0, test 0.** GPU 사용은 4 epoch에서 멈추는 smoke 2회(1회 FAILED 보존, 1회 PASS)뿐이다. 기존 데이터, 라벨, QA, 1 epoch smoke 결과, recipe v01은 그대로 두었다.

## 요약

| 항목 | 결과 |
|---|---|
| recipe | **LOCKED v02**(md `064bbb1a…`, json `05d070a2…`). v01과의 차이는 epochs 60→200뿐이다. v01은 보존 |
| 학습률 변화 | warmup(48 iteration)은 같다. epoch당 감소폭이 1.5e-5 → 4.5e-6으로 줄어든다. 실측 lr이 재현값과 오차 0으로 일치 |
| 학습 스크립트 | `scripts/train_b1_yolo_20261108_v04.py`. v03은 smoke FAILED(final-eval 판별 결함)로 보존 |
| 200 epoch 대응 smoke | HR seed 42, epochs=200 설정에서 4 epoch 후 중단: **PASS** |
| 학습곡선 분석 | `analysis/b1_learning_curve_20261108_v01.py` 준비. smoke와 가짜 200 epoch 곡선으로 동작을 확인했다 |
| 사람 검토 패키지 | 컨택트시트 5장과 ZIP(18MB). 분류 4개, 판정 칸은 비어 있다 |
| seed 42 실행 절차 | `scripts/run_b1_baseline_seed42_20261108_v01.sh`(dry-run만) |

## 1. Recipe v02와 학습률

- 지시하신 값 그대로다. JSON의 train_args를 v01과 비교하면 다른 항목은 `epochs`(60→200) 하나뿐이다.
- Ultralytics 선형 스케줄: lr(e) = lr0 × [(1 − e/E)·0.9 + 0.1]
  - warmup은 3 epoch = 48 iteration이다. weight 그룹은 0에서, bias 그룹은 0.1에서 시작해 lr0·lf(e)로 이동한다.

| epoch | E=60 lr | E=200 lr |
|---:|---:|---:|
| 1(warmup, 마지막 iteration) | 3.13e-4 | 3.13e-4 |
| 4(warmup 직후) | 9.55e-4 | 9.87e-4 |
| 30 | 5.65e-4 | 8.70e-4 |
| 60 | **1.15e-4(마지막)** | **7.35e-4** |
| 100 | — | 5.55e-4 |
| 150 | — | 3.30e-4 |
| 200 | — | 1.05e-4 |

- **주의:** 200 run의 epoch 60은 lr이 아직 lr0의 73%다. 60 epoch run이 끝난 상태와 다르다. 그래서 "60/100/150/200 시점 비교"는 같은 200 run 안의 진행 정도를 보여 줄 뿐이다. 60 epoch으로 따로 학습한 결과를 대신하지 않는다.
- 그림과 표: `b1_yolo_recipe_v02_prep_20261108_v01/lr_schedule_60_vs_200.png`, `.csv`, `lr_schedule_per_iteration.csv`

![lr](b1_yolo_recipe_v02_prep_20261108_v01/lr_schedule_60_vs_200.png)

## 2. 학습 스크립트 200 epoch 대응 검증

- v04가 v02 대비 추가한 것
  - recipe v02만 받는다(sha 고정).
  - iteration별 lr을 기록한다(모든 param group).
  - val mask/box mAP50·mAP75·mAP50-95를 epoch마다 기록한다(Ultralytics 기본 로그에는 mAP75가 없다).
  - epoch마다 학습+val 시간을 기록한다.
  - `--stop-after-epochs`: SMOKE 전용. 200 epoch 스케줄은 그대로 두고 N epoch에서 멈춘다.
- **v03 smoke FAILED(보존):** 중간에 멈추면 Ultralytics의 final_eval 재호출이 `epoch >= epochs` 조건에 걸리지 않아 assert로 멈췄다. v04는 "열린 epoch 기록이 있는가"로 판별한다. 학습 로직은 바뀌지 않았다.
- **v04 smoke**: `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_SMOKE_RECIPEv02_20261108_v01/HR_Scan_seed42_stop4_v04`
  - planned epochs 200, 4 epoch에서 중단, **PASS**

| epoch | optimizer 호출 / 실제 갱신(누적) | AMP skip | scale | train seg loss | val mask mAP50 / 75 / 50-95 | 학습+val 시간 | GPU peak |
|---:|---|---:|---:|---:|---|---:|---:|
| 1 | 16 / 15 | 1 | 64 | 1.93 | 0.058 / 0.000 / 0.013 | 6.6 s | 10.2 GB |
| 2 | 16 / 31 | 0 | 64 | 0.95 | 0.170 / 0.008 / 0.049 | 3.8 s | 10.3 GB |
| 3 | 16 / 47 | 0 | 64 | 0.75 | 0.166 / 0.014 / 0.054 | 3.7 s | 10.3 GB |
| 4 | 16 / 63 | 0 | 64 | 0.61 | 0.777 / 0.413 / 0.427 | 3.7 s | 10.3 GB |

- iteration별 lr 64개(weight 2그룹, bias 그룹)가 E=200 재현값과 **최대 차이 0.0**이었다. 예: iteration 0은 0 / 0 / 0.1, iteration 47은 9.70e-4 / 3.05e-3, iteration 48 이후는 9.87e-4.
- 선정 checkpoint는 epoch 4다. final_eval은 따로 기록되어 선정에 섞이지 않았다.
- 참고: 앞선 1 epoch smoke(v01 recipe)는 epochs=1이라 warmup이 0(min(3, E−1)=0)이었다. 그래서 첫 epoch loss가 훨씬 컸다(seg 8.25 vs 1.93). 이번 결과와 직접 비교하지 않는다.
- 예상 시간: epoch당 약 3.7초 × 200이면 **run당 약 13분**, seed 42 세 표현이면 약 40분이다. 평가까지 넣으면 약 50분이다.

## 3. 학습곡선 · 수렴 분석 준비

- 스크립트: `analysis/b1_learning_curve_20261108_v01.py`
- 출력
  - run별 그림 6칸: train loss, val loss, val mask mAP50/75/50-95와 선정 epoch, lr, AMP skip과 실제 갱신, GPU 메모리와 epoch 시간
  - 세 표현 비교 그림
  - `epoch_table_*.csv`
  - `checkpoints.csv`: 60/100/150/200 시점 값, 최고 epoch과 그 값
  - `last30.csv`: 마지막 30 epoch의 평균, 표준편차, 최소, 최대, 10 epoch당 기울기, 그 이전 최고 대비 향상분
  - `convergence.json`
- 수렴 읽기(**제안 기준이며 판단은 연구자가 한다**)
  - PLATEAU: 마지막 30 epoch 기울기의 절대값 < 0.002/10 epoch, 그리고 향상분 < 0.005
  - STILL_IMPROVING: 기울기 ≥ 0.002/10 epoch, 또는 최고 epoch이 마지막 10 epoch 안에 있고 향상분 ≥ 0.005
  - 그 외: UNCLEAR
- 동작 확인
  - 4 epoch smoke → INSUFFICIENT_EPOCHS(정상)
  - 가짜 200 epoch 곡선 2개(scratchpad) → 포화형은 PLATEAU, 선형 증가형은 STILL_IMPROVING. 의도대로 분류됐다.
- 예시 그림(4 epoch smoke): `b1_yolo_recipe_v02_prep_20261108_v01/example_curves_smoke_stop4.png`

## 4. 사람 QA 검토 패키지

- 위치: `/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/reports/b1_human_review_pack_20261108_v02/`
  - ZIP: `b1_human_review_20261108_v02.zip`(18MB, sha `ad2b668a…`). 분류별 폴더, 컨택트시트, `REVIEW_GUIDE_v02.md`, `review_checklist_v02.csv`(엑셀용 UTF-8 BOM)
  - 컨택트시트: `contact_1_NORMAL_PRIMARY_1.jpg`, `contact_2_REP_DISAGREEMENT_1.jpg`, `contact_3_FLAG_1.jpg`, `contact_3_FLAG_2.jpg`, `contact_4_LOW_SUPPORT_1.jpg`

| 분류 | 사례 수 | 내용 |
|---|---:|---|
| 1 정상 메인 load | 6 | 기준 눈높이용 |
| 2 표현 간 판정 불일치 | 4 | VAL_000148 L3, TST_000188 L5, TRN_000926 L3(WATCH/FLAG/FLAG), VAL_000212 L4(LOW/OK/OK) |
| 3 FLAG(세 표현 일치) | 15 | |
| 4 LOW_SUPPORT | 5 | 1개는 판정 불일치라 분류 2로 옮겼다 |

- 패널 하나에 원본 RGB + GT mask(초록) / 실제 mask(빨강), YOLO polygon(청록), 확대 RGB, 가림 지도가 HR/LR/CAD 행으로 나란히 있다. 컨택트시트에는 사례마다 세 표현의 판정과 vis를 적었다.
- 판정 칸 8개(Q1–Q4, 최종, 검토자, 날짜, 메모)는 비어 있는지 스크립트로 확인했다. AI 판독은 넣지 않았다.
- v01 패키지는 바꾸지 않았다(checklist sha `2bef5432…` 그대로).

## 5. seed 42 본 학습 실행 절차(승인 대기)

```
~/.claude/hooks/isaacsim/ntfy_run.sh --name B1_baseline_seed42 -- \
  scripts/run_b1_baseline_seed42_20261108_v01.sh
```

1. HR → LR → CAD 순서로 `train_b1_yolo_20261108_v04.py`를 실행한다(recipe v02, seed 42). root는 `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_BASELINE_20261108_v01`(아직 없음)이다.
2. run마다 `run_status.json`의 state가 PASS여야 다음 run으로 간다. 아니면 멈추고, 재시도하지 않으며, 실패 기록은 보존한다. 기존 run 디렉터리가 있으면 덮어쓰지 않고 거부한다.
3. 셋 다 PASS면 학습곡선 분석과 **val** 3×3 평가(bootstrap 1000)를 한다. test는 쓰지 않는다.
- `DRY_RUN=1`로 명령 5개가 출력되는 것을 확인했다. 실제 실행은 하지 않았다.
- 디스크 여유는 239GB, run당 예상 사용량은 수십 MB다.

## 남은 일

1. 사람 QA 검토(연구자)
2. seed 42 본 학습 승인
3. seed 42 학습곡선 검토 → seed 43/44 승인
4. 본 학습 뒤, test 전에 평가 절차를 LOCKED로 확정

## 파일

- 신규 문서
  - `docs/b1_yolo_baseline_recipe_LOCKED_v02_20261108.md`
  - `docs/b1_yolo_baseline_recipe_LOCKED_v02_20261108.json`
- 신규 코드
  - `scripts/train_b1_yolo_20261108_v03.py`(FAILED 기록용)
  - `scripts/train_b1_yolo_20261108_v04.py`(6f35400f…)
  - `scripts/run_b1_baseline_seed42_20261108_v01.sh`(6f3ba359…)
  - `analysis/b1_lr_schedule_replay_20261108_v01.py`
  - `analysis/b1_learning_curve_20261108_v01.py`(56a7578f…)
  - `analysis/b1_human_review_package_20261108_v02.py`
- smoke root: `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_SMOKE_RECIPEv02_20261108_v01`
  - v03 FAILED run과 v04 PASS run, stdout/stderr, command json, input_hashes, learning_curve_smoke_v01
