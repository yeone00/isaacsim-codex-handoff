# Full E2E v02 — wheel-position feedback HOLD engineering implementation

상태: READY_FOR_MANUAL_APPROVAL (지시문을 로컬에서 확인한 후 Codex에 전달)
워크스테이션 프로젝트: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013

## 출발점 — 기존 선정 재검토 반복 금지
최초에 AGENTS.md, docs/PROJECT_STATE.md, 다음 2개 보고서를 읽어라.
- reports/full_e2e_v02_stopping_hold_method_selection_20261019_v01.md
- reports/full_e2e_v02_stopping_adapter_actual_validation_20261019_v01.md

이미 완료된 결정:
- 선정: 기존 wheel velocity drive + 외부 wheel-position→velocity feedback HOLD adapter.
- 원본 wheel DriveAPI: stiffness=0, damping=100 authored. Native position target만 추가해도 위치 복원 불가.
- 기존 post-zero wheel 회전·base 34.127289mm 후퇴, raw-root quiet FAIL. Velocity cap은 해당 시험에서 PASS.
- 공식 근거: PhysX Team, Implicit Spring Joint Drives (2023), 식(9). 외부 cascade는 설계 유도이지 실제 dynamics/stability 보증이 아님.
- 후보 선정은 끝났다. 이번에 또 후보 비교·광범위 USD audit·새 문헌 탐색만 반복하지 마라.

## 이번 산출 목표
**분리된 engineering HOLD adapter + 단일 actuator command owner 계약 + 재현 가능한 오프라인 테스트**를 구현하고, 단일 Isaac Sim 검증의 실행 가능 여부를 GO/NO-GO로 정리하라.
이번 턴의 실제 Isaac/ROS 물리 주행은 실행하지 않는다. 구현 완료와 실험 성공을 혼동하지 않는다.

### 1) 구현 (구체적인 변경)
- 원본 USD, frozen robot_task_controller_goalframe_v04.py, 기존 governor/stopping adapter, 연구 protocol/threshold를 보존한다.
- 새 evaluation/fe2e_v02_wheel_hold_adapter_v01.py 등 분리된 engineering 파일로 설계한 WheelHoldAdapter를 실제 구현하라.
- HOLD entry 때 같은 epoch의 fresh synchronized wheel6 unwrapped q/dq, steering4 angle, base pose를 한 번만 latch한다. 이 후 q_hold/base_hold/steer_hold target을 움직이는 상태에 맞춰 갱신하지 마라.
- HOLD 출력은 6 wheel joint별 signed velocity target(rad/s)과 4 steering position target(rad)을 명시적 joint name으로 돌려라. Wheel position error에 대한 외부 feedback v_target=saturate(K_hold*(q_hold-q), +/-limit)를 사용하되, unwrap, sign, units, sample freshness, nonfinite, time monotonicity, saturation/slew, zero/fault latch를 강제하라.
- Controller와 ROS publisher가 동일 wheel DOF를 동시에 소유하지 못하도록 **실제 적용 가능한 하나의 owner/mux 계약**을 마련하라. 별도 subscriber 설치만으로 독점 ownership을 주장하지 마라. APPROACH/DECEL→HOLD 전환과 Twist zero가 HOLD target을 overwrite하지 않는 경로를 명시하라.
- 경로·게이트·footprint·clearance·velocity cap 변경 금지. HOLD correction에서 필요한 음의 signed wheel velocity는 연구용 reverse approach 명령과 별도 상태/한계로 분리하되, 이를 명시적인 정책 승인 없이 실주행에 적용하지 마라.
- stop 실패 시 fail-latched zero/independent simulation pause guard를 계획하라. Zero는 물리 정지 보증이 아님.
- Gain K_hold, joint-velocity max, slew, max hold displacement/time은 임의 편의 기본값으로 숨기지 마라. 기존 근거에서 사전에 산정·검토 가능한 수치 후보와 단위/안전 조건을 별도 PROPOSED contract에 명시하고 그 선택 근거를 검증하라. 실제 인증이 안 되는 파라미터는 UNRESOLVED로 남기고 실행을 차단하라. Parameter sweep과 '통과할 때까지 조정' 금지.

### 2) 계약과 오프라인 테스트
- 기작성 frozen mobility drive와 동시 쓰기가 발생하지 않는 실제 graph wiring/derived-scene integration plan을 정하라. 필요시 새로운 derived-scene patch 또는 isolated joint-command publisher를 별도 파일로 구현하되 원본을 수정하지 마라.
- Tests: hold entry single latch, signed correction both directions, unwrap, joint order/units, K/limit fail-closed, freshness/stale/NaN, watchdog/timeout, duplicate-owner conflict, Twist overwrite prevention, stop/fault/re-arm prohibition, simulated sample replay로 wheel/steer target sequence 확인.
- 오프라인 replay는 물리학적 stop/safety 성공 증거로 표기하지 마라.
- 샌드박스/권한 오류가 나면 시스템 보안을 끄거나 우회하지 말고, 해당 단계와 해결에 필요한 최소 조치를 보고하라. 무제한 디버깅 금지.

### 3) 다음 1회 Isaac Sim 실험 진입 조건
- 위 코드 및 계약 검사 통과, signed HOLD correction의 정책/상한과 하나의 actuator ownership이 명시적으로 승인돼야 한다.
- 1회 열린공간 isolated nonzero-curvature→정상감속→HOLD에서 실제 q/dq/steer/base pose/root/FD/ROS/target 동일 epoch 기록, post-entry along/XY/yaw drift, quiet(.002m/s, 1s), max planar speed(.03m/s), max clearance/safety/guard 평가.
- 기준 ±.030m longitudinal/lateral·±2° yaw·clearance≥.10m 불변. 이 단일 시험은 ENG001 full-chain success 증거가 아님.
- 실제 Isaac/ROS 구동, ENG001, QUAL12, 432-run, 자동 retry는 **이번 턴 실행하지 마라**. GO 조건을 만족했더라도 다음 단계에서 사용자의 명시적 승인 후 1회만 실행한다.

### 4) 종료 산출물
- 새 engineering adapter, relevant contracts/tests, 최소 derived-scene integration 코드(가능한 경우), unit test 결과.
- reports/full_e2e_v02_wheel_hold_implementation_20261019_v01.md 작성: 구현 유무, 산정한 PROPOSED 값/UNRESOLVED, owner/mux 실현 여부, 실제 시험 전 남은 blocker를 최대 3개 구체화, GO/NO-GO, 다음 1회 시행 방법.
- docs/PROJECT_STATE.md 갱신, 기존 파일/hash inventory 보존.
- 설계 구현이 물리 또는 기술적으로 불가능하면 외부 포장 없이 FAIL/결정 필요 항목과 이유를 명시. 또 다른 선정 보고서만 작성하고 작업을 끝내지 마라.
- 완료 메시지 마지막 줄에 실제 생성된 보고서만 다음 형식으로 적어 Codex notify 동기화를 활성화하라:
HANDOFF_REPORT: reports/full_e2e_v02_wheel_hold_implementation_20261019_v01.md
