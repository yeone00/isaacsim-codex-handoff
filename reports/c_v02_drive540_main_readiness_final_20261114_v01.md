# 540회 본실험 최종 준비 점검과 시작 절차 — 2026-11-14 v01

승인받은 범위만 진행했습니다. S1·S6 기술 파일럿 2회(모두 counted=false)와 Controller v05 모의 검증입니다.

다음은 하지 않았습니다.
- 540회 본실험 시작
- Controller v04 승인 파일 생성
- v04 / Watchdog 종료
- 렌더·재학습 재개, 보정 B 사용

## 결론: 최종 준비 5개 항목 모두 PASS

| 항목 | 결과 |
|---|---|
| 1. S1·S6 기술 파일럿 | **PASS.** 두 시작점 모두 SUCCESS, 기술 판정 PASS |
| 2. Controller v05 모의 검증 | **PASS (T1–T9 9/9).** 검증 과정에서 Controller 결함 2건을 찾아 고친 뒤 처음부터 다시 검증함 |
| 3. v04 / Watchdog 전환 준비 | **준비 완료.** 둘 다 대기 상태, 실행 중인 작업 없음, 승인 파일 없음. 종료 절차와 명령 정리 (실행은 연구자) |
| 4. 프로토콜·manifest·잠금 확정본 | **확정본 작성.** 아래 SHA 참고 |
| 5. 외장 볼륨 | **PASS.** UUID 일치, ext4 읽기·쓰기 가능, 여유 7.54 TB, 쓰기 시험 통과 |

## 1. S1·S6 기술 파일럿 (GeoCAD C100, ROBUST_A만, 모델과 임계값 동일, V3 최적화 적용)

| 시작점 | 위치 | 결과 | 시간 | 검출 conf | 위치 오차 | 경로 최대 곡률 (한계 0.364) | 주행 거리 | 최종 오차 | 방향 오차 | 최대 속도 | 충돌 | 정지 인증 | 명령 반영 지연 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | −3 cm, 86° | SUCCESS | 309.0초 | 0.809 | 0.35 cm | 0.172 | 1.797 m | **0.335 cm** | 0.000° | 0.0261 | 없음 | 2/2 | sim 0.017초 / 25 ms |
| S6 | +3 cm, 94° | SUCCESS | 303.4초 | 0.817 | 0.31 cm | 0.199 | 1.797 m | **0.338 cm** | 0.004° | 0.0261 | 없음 | 2/2 | sim 0.017초 / 21 ms |

- 그래프 검사 대조 불일치 0건, 구간 시작 pacing 적용(각 29스텝), 기존 technical gate PASS
- **새로 확인한 점:** 비스듬한 시작점(S1, S6)에서는 GeoCAD C100 검출 conf가 약 0.81로, E1 정면(0.27–0.36)보다 훨씬 높았습니다. 같은 적재물이라도 시점에 따라 인식 여유가 크게 다릅니다.
- **운영상 기록:** 첫 실행 시도에서 경쟁 프로세스 검사가 제 셸 명령의 텍스트 자체에 걸려 HOLD로 멈췄습니다. 이때 주행은 실행되지 않았고, 로그(`grid_attempt0_false_hold.log`)를 보존했습니다. 실행 파일 이름 기준으로 검사하도록 고친 뒤 다시 실행했습니다.

## 2. Controller v05 모의 검증 (Isaac·ROS·GPU 없음)

**시험 방법**
- 실제 v05 코드에 가짜 runner와 가짜 판정기를 넣었습니다(`evaluation/c_v05_controller_mock_20261114_v01.py`).
- E1 manifest의 앞 120행을 썼고, 보고 시점은 30회와 100회입니다.
- 알림은 로그에만 남기고 실제로 보내지 않았습니다.
- 출력은 실제 외장 볼륨의 `MOCK_controller_v05_test_v03`입니다.

| 시험 | 기대 동작 | 결과 |
|---|---|---|
| T1 승인 파일 없음 | 실행 0회, HOLD (`START_GATES_FAILED:researcher_authorization`) | PASS |
| T2 45번째 실행 후 정지 요청 | 45회 후 `STOPPED_BY_REQUEST`, 30회 보고 파일 생성 | PASS |
| T3 재시작 | 46회부터 이어서 실행. 정상 실패 16건은 기록하고 계속 진행. 70번째 기술 실패에서 HOLD | PASS |
| T4 해제 파일 없이 재시작 | 실행 0회, HOLD (`no_unresolved_hold`) | PASS |
| T5 해제 후 재시작 | 71회부터 이어서 실행. 85번째에서 결과 파일 없이 종료되자 HOLD | PASS |
| T6 해제 후 재시작 | 결과 없는 기존 폴더를 **자동으로 다시 실행하지 않고** HOLD (`INCOMPLETE_RUN_DIR`) | PASS |
| T7 연구자가 해당 폴더를 격리한 뒤 재시작 | 끝까지 완료, 100회 보고 파일 생성, `MAIN_COMPLETE` | PASS |
| T8 압축 | 압축본 119개 모두 복원 후 전 파일 SHA-256 일치 | PASS |
| T9 알림 | 알림 9건이 로그에 기록됨 (모의 시험이라 발송은 안 함) | PASS |

**100회 보고 예시 (모의)**
- 표현별 집계: 무검출, 주행, 경로 거절, 기술 HOLD 횟수
- 주행 비율, 최근 30회 평균 시간, 남은 시간, 완료 예상 시각, 총 예상 시간, 36시간 초과 위험

**검증 중 발견해 고친 Controller 결함 2건** (각각 고친 뒤 새 폴더에서 처음부터 다시 검증)
1. **로그 이름 충돌 (모의 v01의 T7):** 격리한 행을 다시 실행할 때 이전 runner 로그 이름과 겹쳐 Controller가 예외로 종료됐습니다. 이제 이전 로그는 그대로 두고 새 로그 이름에 시각을 붙입니다.
2. **보고서 분류 오류 (모의 v02 점검 중):** 기술 HOLD 실행이 보고서에서 "기타 정상 실패"로 분류됐습니다. 이제 `technical_hold`로 따로 세고, 보고서에 `technical_holds` 건수를 표시합니다.

**HOLD 종류**
- **기술 HOLD** (`TECHNICAL_HOLD`, `INCOMPLETE_RUN_DIR`, `ARCHIVE_VERIFY_FAILED`): `hold_resolution_<attempt>.json`(연구자 결정)이 있어야 재시작할 수 있습니다. 그 실행은 기록에 남습니다.
- **조건 HOLD** (승인 없음, 경쟁 프로세스, 볼륨 문제): 원인을 해결하고 재시작하면 다시 점검합니다.
- **정상 정지:** `STOP_REQUEST` 파일을 만들면 다음 실행 전에 멈추고, 재시작하면 이어서 실행합니다.

## 3. v04 / Watchdog 상태와 종료 절차 (실행은 연구자)

**상태**

| 서비스 | PID | 상태 | 재시작 정책 | 부팅 시 자동 시작 |
|---|---|---|---|---|
| `c-v02-drive540-technical-20261113-v04.service` (Controller v04) | 2869572 | `WAITING_STORAGE_AUTHORIZATION_AND_CAPACITY`, 실행 중인 작업 없음, 30초마다 대기 확인 | `Restart=no` | disabled |
| `c-v02-drive540-technical-watchdog-20261113-v01.service` (Watchdog v05) | 2881294 | 감시만 함 | `Restart=on-failure` | **enabled** |

- 두 서비스 모두 systemd 사용자 서비스이며, 소유자는 user입니다.
- v04 승인 파일(`storage_authorization.json`)은 없는 상태 그대로입니다.
- 같은 사용자 서비스 중 `c-depletion-controller`(HOLD, GPU 작업 시작 0건), `c-depletion-watchdog`, `c-depletion-bitmap-sync`, `c-v02-drive540-monitor`(Controller 생존을 확인하지 않음)는 v05와 충돌하지 않습니다.
- **종료 순서 주의:** Watchdog은 v04 상태가 HOLD가 아닐 때 Controller가 사라지면 `CONTROLLER_LOST` 경고를 보냅니다. 그래서 **Watchdog을 먼저** 멈춥니다.
- 종료하지 않고 그대로 두어도 v05는 실행 직전마다 v04 승인 파일이 없음을 확인하므로 옛 manifest가 실행될 수 없습니다. 다만 혼선을 줄이려면 종료를 권장합니다.

**정상 종료 절차** (모두 정상 stop이고 강제 종료가 아니며, 로그 파일은 보존됨)

```bash
# 0) 확인: v04가 작업 없이 대기 중이고, 승인 파일이 없는지
python3 -c "import json;s=json.load(open('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/drive540_technical_execution_summary_20261113_v01.json'))['status'];print(s['state'],s['current'])"
ls /home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_policy_amendment_v01/storage_authorization.json   # "No such file" 이어야 함
# 1) Watchdog 먼저 정지 + 부팅 시 자동 시작 해제
systemctl --user stop c-v02-drive540-technical-watchdog-20261113-v01.service
systemctl --user disable c-v02-drive540-technical-watchdog-20261113-v01.service
# 2) v04 Controller 정지 (Restart=no 이므로 다시 뜨지 않음)
systemctl --user stop c-v02-drive540-technical-20261113-v04.service
# 3) 확인
systemctl --user is-active c-v02-drive540-technical-20261113-v04.service c-v02-drive540-technical-watchdog-20261113-v01.service   # inactive, inactive
```

## 4. 확정본 (승인 대상)

모두 `/home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_E1_20261114_v01/` 아래에 있습니다.

| 파일 | SHA-256 | 내용 |
|---|---|---|
| `protocol_amendment_E1_FINAL_v03.json` | be4a2c70d4045c3a… | 아래 표 참고 |
| `manifest_draft_v01/attempt_manifest_E1_draft.csv` | 1ce636ce56052f9a… | 540행. HR/LR/CAD × C100–C20 × base 36개, 시작점 7개(base 단위). 기존 manifest 92ba7c29…는 수정하지 않음 |
| `main_execution_lock_FINAL_v02.json` | **f10c380fc79714aa1236cc06f8cd4cca8bffcaa0dd49cc4c882a8c5cd79cc2b4** | 아래 표 참고 |

**개정안 v03 내용**
- 시작점: E1 격자 7개
- 보정: ROBUST_A만 사용, 보정 B 사용 안 함
- 실행 최적화: O1·O3·O4와 구간 시작 pacing
- 기술 파일럿 기록: E1 GeoCAD 9회, HR 무검출 1회, S1·S6
- **Test 계보 base(C2D_B01)에서 기술 파일럿을 본 뒤 시작점을 개정했다는 사실 명시**
- 일정 규칙: 보고만 하고, 생략·변경은 별도 승인

**실행 잠금 v02 내용**
- manifest·개정안 SHA, 코드 32개 SHA
- 실행 옵션: `--opt-contact-compact --opt-graph-cache --opt-fsync-batch 15 --opt-leg-start-pacing-s 0.5 --pace-period-s 0.042 --profile-steps`
- 출력 위치: 외장 볼륨 `.../isaac_research/C_V02_DRIVE540_20261113_v01/E1_main_v01`
- 최소 여유 공간 600 GiB, 보고 시점 30/100/180/270/360/450, 기준 36시간, 상태 폴더 `main_controller_v05_state`
- 모의 검증 결과 SHA

**v05 사전점검 (확정 잠금 기준)**
- manifest, 개정안, 코드, v04 승인 파일 없음, 경쟁 프로세스 없음, UUID, 여유 공간, 쓰기 권한, 미해결 HOLD 없음: **모두 PASS**
- 연구자 승인만 남았습니다.

이전 잠금(`main_execution_lock_FINAL_v01_SUPERSEDED_controller_fix.json`)과 초안들은 이력으로 보존했습니다.

## 5. 외장 볼륨과 저장 정책

**볼륨 상태**
- `/dev/nvme0n1p1`, ext4, rw, UUID 1997fec1-5a55-49af-a41b-e2095924fd81
- 대상 폴더 소유자 user, 권한 750, 여유 7.54 TB
- 쓰기 시험 파일은 만들고 SHA를 확인한 뒤 삭제했습니다.

**저장 정책**
- 원본 run 폴더는 그대로 보존합니다.
- 실행마다 `<run>.tar.zst`(zstd -3, 무손실)와 SHA-256을 만듭니다.
- 압축을 풀어 전 파일 SHA가 원본과 같은지 확인합니다. 다르면 기술 HOLD입니다.
- 예상 용량: 원본 약 300 GB 이하, 압축본 약 36 GB

## 6. 본실험 시작 절차 (연구자 승인 후)

```bash
cd /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
# (선택, 권장) 3절의 v04/Watchdog 정상 종료
# 1) 확정본 3개 확인 후 승인 (이 잠금 SHA에만 유효)
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/c_v02_drive540_e1_main_approve_20261114_v05.py --approve-e1-main540 \
  --lock /home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_E1_20261114_v01/main_execution_lock_FINAL_v02.json
# 2) 사전점검 (모든 항목 true 확인)
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/c_v02_drive540_e1_main_controller_20261114_v05.py \
  --lock /home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_E1_20261114_v01/main_execution_lock_FINAL_v02.json --dry-run
# 3) 시작 (systemd 사용자 서비스로 실행. 터미널을 닫아도 계속 돌고, 실패해도 자동 재시작하지 않음)
systemd-run --user --unit=c-v02-drive540-e1-main-v05 -p Restart=no \
  --working-directory=/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013 \
  /home/user/anaconda3/envs/sdg_tools/bin/python -u scripts/c_v02_drive540_e1_main_controller_20261114_v05.py \
  --lock /home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_E1_20261114_v01/main_execution_lock_FINAL_v02.json
```

**운영**
- 상태 확인: `cat .../main_controller_v05_state/status.json`
- 보고 파일: `.../main_controller_v05_state/milestone_NNN.json`
- 정상 정지: `touch .../main_controller_v05_state/STOP_REQUEST`. 실행 중인 1회가 끝난 뒤 멈추고, 재시작하면 이어서 실행합니다.

1–3단계를 직접 실행하셔도 되고, "본실험 시작 승인"이라고 명시해 지시해 주시면 제가 2–3단계를 실행합니다. 승인 스크립트(1단계)는 연구자의 명시적 승인 행위이므로 직접 실행하시는 것을 권장합니다.

## 7. 남은 위험
- **36시간 초과 위험:** 주행 비율이 약 74%를 넘으면 36시간을 넘습니다. 비스듬한 시작점에서 검출 conf가 높았던 점(S1·S6 약 0.81)으로 보면 주행 비율이 E1 진단 때보다 높을 수 있습니다. 보고 시점에 판단하시면 됩니다.
- **검출 결과의 확률적 변동:** 같은 조건이라도 검출 conf가 렌더 노이즈로 변하므로, 결과를 해석할 때 반영해야 합니다.
- **명령 반영 지연 (readback):** 지금까지 구간 10개에서 재발하지 않았습니다. 재발하면 기술 HOLD로 처리하고 우회하지 않습니다.
- **모의 검증의 한계:** 실제 Isaac 실행과 Controller의 결합은 runner v05로만 확인했습니다(재검증 4회, S1·S6 2회). v05 Controller로 Isaac을 직접 돌린 것은 아직 없으므로, 본실험의 첫 1–3회를 주의해서 지켜봐야 합니다.

## 산출물
- **새 코드:**
  - `scripts/c_v02_drive540_e1_main_controller_20261114_v05.py` (확정)
  - `scripts/c_v02_drive540_e1_main_approve_20261114_v05.py` (FINAL 잠금만 허용, 모의 시험용 키가 있으면 거부)
  - `evaluation/c_v05_controller_mock_20261114_v01.py`
  - `analysis/c_v05_controller_mock_test_20261114_v01.py`, `_v02.py`, `_v03.py`
  - `sdg_final/C_V02_E1_GRID_PILOT_20261114_v01/check_competing.py`
- **파일럿 기록:** `/home/user/hh/isaac_cosmos/sdg_final/C_V02_E1_GRID_PILOT_20261114_v01/`
- **모의 시험 기록:** `.../C_V02_DRIVE540_E1_20261114_v01/controller_v05_mock_test_v01|v02|v03/`, 외장 볼륨 `MOCK_controller_v05_test_v01|v02|v03(+_quarantine)`
- **보고서 첨부:** `reports/c_v02_drive540_main_readiness_final_20261114_v01/`
