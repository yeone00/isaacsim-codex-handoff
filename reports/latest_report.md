# B1 혼합 39-run 학습 — 26번째 run 멈춤(HANG)과 복구 기록 (2026-11-09)

상태: 복구 절차 실행 완료. 남은 학습 진행 중 (최종 결과는 별도 분석 보고서에 기록 예정)

## 1. 무슨 일이 있었나
- 대상 run: 26/39 `A1000_S050_R050__LR_Scan__seed44` (실제 50 : 합성 50, LR_Scan, seed 44)
- 출력 루트: `/home/user/hh/isaac_cosmos/sdg_final/B1_MIX_AUG_RECIPEv04_20261108_v01/`
- 1–25번 run은 모두 PASS로 끝났습니다. run당 약 14.7분, 최대 GPU 할당 10.33 GB.
- 26번 run은 05:47:38에 시작해 epoch 148/200까지 정상으로 학습했습니다.
  - epoch 148 지표: B1 val mask mAP50-95 0.848, real val 0.951. loss와 지표 모두 정상 범위였습니다.
  - epoch 148의 real-val 평가 후 `last.pt` 저장(05:58:33)이 마지막 기록입니다.
  - 그 뒤 epoch 149가 시작되지 않은 채 약 5시간 48분 동안 아무 기록도 없었습니다.
- 증상:
  - 메인 스레드가 `futex_wait` 상태였습니다(스레드 96개).
  - DataLoader 워커 프로세스(8 + 2개)는 `do_poll` 대기였습니다.
  - GPU 사용률은 0–3%였고, 05:58:37에 GPU 메모리가 12.3 GB에서 1.76 GB로 떨어졌습니다.
  - stdout에 예외는 없었습니다.
- 원인으로 배제한 것: OOM, NaN이나 비정상 loss, 디스크, 호스트 RAM(여유 408 GB).
- 추정 원인: epoch 경계에서 DataLoader 워커나 pin-memory 스레드가 교착(deadlock)된 것으로 봅니다.
  - 이 시점은 epoch마다 도는 real-val validator가 끝난 직후입니다.
  - Python 스택은 확보하지 못했습니다(`kernel.yama.ptrace_scope=1`이라 gdb attach가 거부됨). 따라서 원인은 **추정**이며 확정이 아닙니다.
- driver v01은 run이 종료될 때만 판정하는 구조였습니다. 멈춘 프로세스는 종료되지 않으므로, 실패 처리도 알림도 없이 계속 기다렸습니다. 감시 장치 설계의 빈틈입니다.

## 2. 처리 절차 (연구자 승인 2026-11-09, 옵션 1)
1. **진단 수집**은 `_HANG_DIAG__A1000_S050_R050__LR_Scan__seed44__20261109/`에 했습니다. 수집한 항목:
   - ps 트리, 스레드별 wchan
   - nvidia-smi
   - run 폴더 목록과 타임스탬프
   - stdout 끝 20 KB
   - epoch, results 끝부분
   - 멈춤 전후 GPU 메모리 기록
   - gdb 시도 결과(실패 사유)
2. **HANG 기록**은 run 폴더에 `HANG_RECORD.json`을 새로 추가해서 남겼습니다. 이 run의 기존 파일은 수정하거나 삭제하지 않았습니다:
   - `run_status.json`(state=RUNNING 그대로)
   - `audit.json`, `epochs.jsonl`, `train/results.csv`
   - weights 5개(last, best, best_val, best_realval, best_combined)
   - stdout 로그
3. **종료**는 해당 학습 메인 PID 3041110과 그 자식 12개에만 SIGTERM을 보냈고, 20초 안에 모두 종료됐습니다.
   - driver v01은 이를 `exit=-15 state=RUNNING → STOP: run not PASS`로 기록하고 exit 10으로 중단했습니다.
   - 후속 체인 v01도 `mixing39_done`이 없어서 exit 10으로 중단했습니다(의도한 동작).
4. **재실행**:
   - 같은 manifest, rep, seed 44, recipe LOCKED v04, trainer v06으로 처음부터 학습합니다.
   - 새 폴더 `A1000_S050_R050__LR_Scan__seed44__rerun01/`을 씁니다.
   - 실패본의 checkpoint는 재사용하지 않고, 이어 학습하지도 않습니다.
   - 1–25번 PASS run은 재학습하지 않고 건너뜁니다(SKIP).
5. 이 run은 분석에서 실패본 대신 rerun01을 씁니다. 실패본은 보존하고 보고서에 계속 표시합니다.

## 3. 멈춤 감지 기능 추가 (학습 설정 변경 없음)
- `scripts/run_mixing_39_20261109_v02.py` (driver v02)
  - 학습 명령, 인자, 프로토콜 sha 검증, 메모리 가드, PASS 조건은 v01과 같습니다.
  - **진행 판정 기준은 실제 학습 기록의 갱신 시각**입니다. 대상 파일은 `epochs.jsonl`, `audit.json`, `run_status.json`, `train/results.csv`입니다. 프로세스가 살아 있다는 것만으로는 정상으로 보지 않습니다.
  - **15분 이상 진행이 없으면 HANG으로 판정**합니다. 그 경우:
    - 진단 폴더 `_HANG_DIAG__<run>__<시각>/`를 저장합니다.
    - `HANG_RECORD.json`을 씁니다.
    - 학습 프로세스 그룹만 종료합니다(SIGTERM, 30초 뒤 남으면 SIGKILL). 학습은 새 세션으로 띄우므로 다른 프로세스는 영향을 받지 않습니다.
    - **driver를 중단합니다(exit 14). 자동 재시도는 없습니다.**
  - 재실행 칸은 run마다 `__rerun01` 하나뿐입니다. rerun01도 멈추면 그대로 중단하고 보고합니다. 무한 재시도는 없습니다.
- 검증: scratch 폴더에서 가짜 멈춤 프로세스(sleep)를 0.4분 기준으로 시험했습니다.
  - 멈춤 판정 → 진단 저장 → 프로세스 그룹 종료(남은 프로세스 0) → HANG_RECORD 작성 → exit 14 순서로 동작했습니다. **PASS.**
- 평가와 분석도 재실행 폴더를 인식하도록 v02를 새로 만들었습니다. v01 원본은 보존했습니다.
  - `scripts/run_mixing_eval_20261109_v02.py`: v01과의 차이는 HANG run을 rerun01로 대체하는 것, 출력이 `eval_v02/`라는 것, 사용한 run 폴더를 `run_dirs.json`에 기록하는 것입니다.
  - `analysis/b1_mixing_analysis_20261109_v02.py`: 같은 대체 규칙을 쓰고, `training_runs.csv`에 `run_dir` 열을 추가했습니다.
  - `scripts/chain_mixing_eval_after_training_20261109_v02.sh`: driver v02가 끝난 뒤 39개가 모두 PASS일 때만 평가와 분석을 실행합니다.

## 4. 해석상 주의
- 26번 run의 최종 모델은 rerun01 결과입니다. 설정은 같지만, GPU 비결정성 때문에 실패본의 epoch 1–148 곡선과 완전히 같지는 않을 수 있습니다.
- 교착은 학습 결과와 무관한 인프라 문제로 보고 재실행했습니다. 연구자가 승인한 1회 예외입니다.

## 5. 재개 시점
- driver v02는 2026-11-09 11:49:46에 시작했습니다. 1–25번 SKIP 후 26번 rerun01 학습을 시작했습니다.
- 예상: 남은 14개 × 약 14.8분이면 15:20 전후에 학습이 끝납니다. 이어지는 Validation 평가와 분석은 약 1.5–2시간 걸립니다.

## 6. 진행 경과 (12:05–12:32)
- 26번 재실행 `…LR_Scan__seed44__rerun01`: **PASS**. 15.0분 소요, best_combined epoch 140, 최대 할당 10.34 GB.
- **27번 `A1000_S050_R050__GeoCAD__seed44`에서 같은 증상이 재발했습니다.**
  - 12:16:29에 `last.pt`를 저장한 뒤 epoch 149로 넘어가지 못했습니다(epoch 148까지만 기록).
  - 같은 순간 GPU 메모리가 12.8 GB에서 2.4 GB로 떨어졌습니다.
  - 메인 스레드는 futex 대기였고, 스레드는 96개였습니다.
- driver v02 watchdog이 15.3분 무진행을 감지했습니다(12:31:46).
  - 진단을 `_HANG_DIAG__A1000_S050_R050__GeoCAD__seed44__20261109T123146/`에 저장했습니다.
  - `HANG_RECORD.json`을 작성했습니다.
  - 프로세스 그룹 13개를 SIGTERM으로 정상 종료했고, SIGKILL은 필요 없었습니다.
  - **driver를 중단했습니다(exit 14).** 후속 체인 v02도 `mixing39_done`이 없어서 exit 10으로 멈췄습니다. 의도한 동작입니다.
- 지시("재발 시 무한 재시도 없이 중단·보고")에 따라 **27번은 재실행하지 않았습니다.** 현재 26/39 PASS입니다.
- 공통 패턴:
  - 두 HANG 모두 **같은 manifest(S050_R050), 같은 seed 44, epoch 148 → 149 경계**에서 발생했습니다.
  - 같은 조건의 HR_Scan seed44와 LR_Scan seed44 rerun01은 epoch 149를 정상 통과했습니다(4.3–4.5 s/epoch).
  - 따라서 완전히 결정적인 오류는 아니고, 특정 데이터·증강 순서에서 확률적으로 일어나는 교착으로 추정합니다.
- 배제한 것:
  - fd 한도 1,048,576
  - /dev/shm 사용 1%
  - 호스트 RAM
  - OOM, NaN
  - OpenCV 스레드(Ultralytics가 `cv2.setNumThreads(0)`을 설정함)
- Python 스택은 여전히 확보하지 못했습니다(ptrace_scope=1). 확보하려면 trainer 수정(faulthandler) 또는 py-spy 설치가 필요합니다. trainer는 LOCKED 프로토콜에 sha가 고정돼 있어 연구자 결정이 필요합니다.
