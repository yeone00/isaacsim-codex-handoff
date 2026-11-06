# v42 Ray 복원 후 optimizer step 1→1 — 정적 원인 분석 (2026-11-06)

성격: **정적 코드 분석과 CPU 정수 로직 재현.** GPU 0, 학습 0, Ray 0, 설치/업그레이드 0. v42 출력과 소스는 읽기만 했다. 실행은 B1 train 생성(Isaac, GPU)과 동시에 했으며 GPU는 쓰지 않았다.

대상 기록: `reports/three_rep_bitmap_v41c_amp_optimizer_full_epoch_20261102_v42.md`. PROJECT_STATE 2026-11-02 v42 항목 기준으로 "Ray gate FAIL, STAGE1_READY=NO"이며, 이 판정은 그대로 유지한다.

## 결론

1. **Ray 복원이나 checkpoint 손상 때문이 아니다.** step이 늘지 않은 원인은 Ultralytics의 gradient accumulation 스케줄이다.
   - v42 tiny 시험 구성은 Train 9장, batch 6, nbs 64, epochs 2였다.
   - 이 구성에서는 **중단 없이 연속으로 학습해도 epoch 2의 optimizer step이 0회다**(재현 결과 아래 표).
   - 따라서 "복원 후 step 1→1"은 복원과 무관하게 이 구성에서 당연히 나오는 결과다.
2. scaler growth_tracker 1→1과 EMA 불변은 **원인이 아니라 결과**다. 둘 다 `optimizer_step()` 안에서만 갱신되는데, 그 함수가 호출되지 않았다.
3. v42 보고서의 원인 설명(accumulate=11, ni=2,3, 차이 3,4 < 11)은 설치 소스와 일치한다. 이번 분석은 여기에 "연속 실행에서도 0회"라는 대조 결과를 더해 복원 가설을 배제한다.
4. 실제 full pilot 설정(batch 64, nbs 64)에서는 accumulate가 1이므로 같은 문제가 생기지 않는다. 다만 **GPU에서 실제로 확인하기 전까지는 UNKNOWN**이다.

## 근거 1 — 설치 Ultralytics 8.4.129 `engine/trainer.py`

소스 sha256: `2f60a3dc…f871`(sdg_tools env).

| 위치 | 내용 | 의미 |
|---|---|---|
| L302 | `accumulate = max(round(nbs / batch_size), 1)` | round(64/6) = **11** |
| L258–261 | `nw = round(min(warmup_epochs, max(epochs-1,0)) * nb)` | epochs 2이면 warmup은 1 epoch, nb=2이므로 nw=2 |
| L434 | `last_opt_step = -1` | **지역 변수다.** `_do_train` 호출마다 -1로 다시 시작하고 checkpoint에 저장되지 않는다 |
| L475–478 | `ni = i + nb*epoch`, `ni < nw`일 때만 accumulate를 1에서 nbs/batch로 선형 보간 | epoch 2(ni=2,3)는 warmup이 끝난 구간이라 accumulate가 11로 고정된다 |
| L551–553 | `if ni - last_opt_step >= accumulate: optimizer_step()` | 3, 4 < 11 → 호출 없음 |
| L846–857 | `optimizer_step` 안에서 `scaler.step/update`, `zero_grad`, `ema.update`를 한다 | scaler와 EMA는 step이 있을 때만 바뀐다 |
| L305, L1008–1013 | `_setup_train`마다 optimizer, scaler, EMA를 새로 만든다. 그 뒤 `resume_training`이 checkpoint 상태를 불러온다 | 새로 만든 뒤에 상태를 덮어쓰므로 상태가 손실되지 않는다 |
| L449 | 학습 시작 시 `optimizer.zero_grad()` | 중단 전에 쌓였지만 step하지 않은 gradient는 버려진다(bitwise 연속성은 깨짐) |

## 근거 2 — v42c 복원 경로(`scripts/bitmap_ray_resume_v42c.py`)

소스 sha256: `fddcbd72…139e`.

- **복원 순서는 올바르다.** `StrictTrainer._setup_train`(L15–28)에서 다음 순서로 진행된다.
  1. `super()._setup_train()`: optimizer, scaler, EMA 생성과 last.pt 복원
  2. `raw_state.pt`에서 model, EMA, optimizer, scaler, scheduler를 다시 덮어씀
  - 그 뒤에 optimizer를 다시 만드는 코드는 없다.
  - OOM 자동 축소 경로(trainer L531–548)는 `_oom_retries=3`(L78)으로 막혀 있다.
- 복원 직후 `on_train_start` 검사(L60–75)에서 모두 exact PASS였다(v42 기록). weights, AdamW 각 tensor, scaler, scheduler, EMA, real_updates를 비교했다.
- `SearchTrainer`(`scripts/bitmap_stage1_v40.py`)는 `build_dataset`만 재정의한다. accumulate, optimizer, scaler 로직은 건드리지 않는다.
- 학습 인자(L102): `epochs=2, batch=6, close_mosaic=0`, nbs는 지정하지 않아 기본 64다.
- 실제 기록과의 일치:
  - `ray_records.json` 기준 train은 3 scene × 3 표현 = **9장**이므로 nb = ceil(9/6) = 2다.
  - 복원 세션의 runtime_events에는 `start_epoch=1, batch=6, real_updates 1→1, optimizer_step 1.0, growth_tracker 1`이 기록되어 있다.

## 근거 3 — 정수 로직 재현

`analysis/v42_resume_optimizer_step_static_20261106_v01.py`가 위 소스 라인의 정수 로직만 그대로 옮겨 계산한다(torch와 ultralytics를 import하지 않음).

결과 파일: `reports/v42_ray_resume_optimizer_step_static_20261106_v01/step_schedule_replay.json`

| 구성 | nb | nw | epoch별 optimizer step 수 |
|---|---:|---:|---|
| v42 tiny, **연속 실행**(Train 9, batch 6, epochs 2) | 2 | 2 | ep1: 1, **ep2: 0** |
| v42 tiny, 세션 1(epoch 1 뒤 중단) | 2 | 2 | ep1: 1 |
| v42 tiny, 세션 2(start_epoch 1로 복원) | 2 | 2 | **ep2: 0** ← v42 관측과 일치 |
| 제안 수정안 연속(Train 64, batch 64) | 1 | 1 | ep1: 1, ep2: 1 |
| 제안 수정안 복원(start_epoch 1) | 1 | 1 | ep2: 1 |
| full pilot 복원(Train 6000, batch 64, epochs 60, epoch 3부터 재개) | 94 | 282 | 각 epoch 94 |

## 점검한 후보와 판정

| 후보 | 판정 | 이유 |
|---|---|---|
| gradient accumulation(accumulate 11 > 복원 후 batch 수) | **원인(정적 근거, GPU 미재현)** | 연속 실행에서도 ep2 step 0. 관측 수치와 일치 |
| checkpoint 복원 경로 오류 | 배제(정적) | 복원 순서가 올바르고, 복원 직후 exact assertion PASS |
| Ultralytics가 optimizer를 다시 만들면서 상태 손실 | 배제(정적) | 다시 만든 뒤 상태를 load한다(L305 → L1008 → v42c L25) |
| scaler 연결 문제 | 배제(결과) | `scaler.update()`는 optimizer_step 안에서만 호출된다. tracker 1→1은 step이 없었다는 결과다 |
| EMA 연결 문제 | 배제(결과) | `ema.update()`도 optimizer_step 안에서만 호출된다 |
| last.pt의 fp16 optimizer 직렬화 | 이번 현상과 무관 | v42c가 raw float32 상태를 따로 저장해 복원했다 |

## 남은 위험(수정안을 써도 남음)

- `last_opt_step`과 누적 중인 gradient는 checkpoint에 저장되지 않는다. 따라서 accumulate가 1보다 큰 구성에서는 복원 후 학습 궤적이 연속 실행과 bitwise로 같지 않다. batch 64(accumulate 1)이면 epoch 경계마다 누적분이 0이라 실질적으로 같은 조건이 된다.
- OOM 자동 축소가 일어나면 batch가 줄고 accumulate가 1보다 커진다. 현재는 `_oom_retries=3`으로 축소를 금지했으므로 OOM이면 실패로 끝난다(의도된 동작).
- Stage1 entrypoint `bitmap_stage1_v40.py`는 v42 raw-state adapter와 연결되어 있지 않다(v42 기록 그대로).

## GPU 재현 제안(승인 후, B1 생성이 끝난 뒤)

새 버전 파일과 새 출력 root로 다음 두 가지를 짧게 실행한다. v42 원본은 수정하지 않는다.

1. **대조 실험(복원 가설 반증):** v42 tiny 구성(Train 9, batch 6)을 중단 없이 2 epoch 연속 실행한다. 예측은 ep2 step 0이다. 이렇게 나오면 원인이 accumulation임이 실험으로 확정된다.
2. **수정안 실험:** Train 64(검증된 `batch64_records.json`), batch 64, workers 8로 1 epoch 뒤 SIGINT, 그다음 `Tuner.restore`를 실행한다.
   - 다음 조건을 assert한다: `resumed optimizer_step > saved optimizer_step`, scaler tracker 또는 scale 변화, EMA updates 증가.
   - 예측은 ep2 step 1이다.

판정은 exit code가 아니라 raw_state와 events 파일로 한다.

## 파일과 해시

- 신규 `analysis/v42_resume_optimizer_step_static_20261106_v01.py` — `ebb4a9a8…4e99`
- 신규 `reports/v42_ray_resume_optimizer_step_static_20261106_v01/step_schedule_replay.json` — `92172326…a86`
- 읽기만 함:
  - `scripts/bitmap_ray_resume_v42c.py` `fddcbd72…139e`
  - `scripts/bitmap_stage1_v40.py` `82cd24c9…d13b`
  - ultralytics `engine/trainer.py` `2f60a3dc…f871`
  - v42 root `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v42`의 `ray_records.json`, runtime_events
- 상태: STAGE1_READY=NO, TECHNICAL_READY=NO 유지. 원인은 **정적으로 식별(GPU 미확인)**.
