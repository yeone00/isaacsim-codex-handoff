# Full E2E v02 — Wheel HOLD runtime integration, offline-only implementation

상태: READY_FOR_MANUAL_APPROVAL
프로젝트: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013

## 출발점
AGENTS.md, docs/PROJECT_STATE.md, reports/full_e2e_v02_wheel_hold_implementation_20261019_v01.md를 먼저 읽어라.
HOLD 방식 선정과 분리 구현은 이미 완료됐다. 15/15 offline PASS. 후보 선정, 알고리즘 재탐색, 기존 감사 반복 금지.

완료된 것:
- evaluation/fe2e_v02_wheel_hold_adapter_v01.py: wheel-position→signed velocity HOLD adapter
- evaluation/fe2e_v02_wheel_hold_owner_v01.py: single-owner mux 및 legacy writer 비활성화 edit-layer helper
- evaluation/fe2e_v02_wheel_hold_contract_v01.json: PROPOSED numeric contract, runtime approval=false
- 기존 148개 SHA 보존. Isaac/ROS/physics 실행0.

아직 미완료인 것: 실제 graph-output reader/physics callback과 HOLD entry epoch 동기화, 외부 direct articulation writer 배제 검증, 독립 pause/wall watchdog, 단일 시험용 runner·계측.
K_hold=1s^-1, velocity ±0.020rad/s, slew=.2rad/s², base guard=.004m 등은 PROPOSED이지 안정성 인증이 아니다.

## 이번 작업 목표: runtime integration 코드 구현 (실행 금지)
1. 현재 derived scene/reference의 graph 3개 articulation writer 경로를 정확히 확인하고, 별도 derived-layer patch를 **테스트할 수 있는 코드**로 완성하라. 원본 USD 및 frozen controller 불변.
2. APPROACH/DECEL에서 기존 Ackermann graph-output target을 단일 physics-thread writer가 재전달하도록 graph reader/DOF 이름·매핑 검사를 구현하라. HOLD에서는 legacy write를 차단하고 HOLD adapter wheel6/steer4 target만 같은 owner가 적용하도록 명시하라. 실제 exclusivity 검증이 불가능한 환경에선 진입 거부.
3. 첫 ZERO_SETTLING 동일 epoch에서 fresh synchronized wheel q/dq, steer, base pose를 **zero writer 적용 전에** latch하고, out-of-order·missing sample·duplicate owner·direct writer를 fail-closed로 처리하라.
4. independent physics observer와 별도 wall-time watchdog/pause interface를 연결할 소규모 코드를 구현하라. 실제 pause guard 미설치 시 runtime 승인 금지. Zero는 안전정지 보장 아님.
5. One-shot validation runner의 명령·상태·계측·hash·실패 종료 interface를 준비하되, 이번 턴에는 launch도 ROS 명령도 수행하지 마라. 실제 actor control 호출은 전부 gated로 둬라.
6. 오프라인 테스트를 수행해 실제 구현된 부분과 여전히 실환경 검증이 필요한 부분을 명확히 구분하라. 제안된 수치의 임의 승인/변경, 무단 signed correction 실주행, 속도·clearance·task tolerance 완화 금지.

## 종료 기준
- 새 engineering integration 코드와 관련 단위·mock 계약 검사 PASS/FAIL를 보고하라.
- reports/full_e2e_v02_hold_runtime_integration_20261019_v01.md 작성: 구현 파일, 정적 계약 근거, 남은 blocker 최대 3개, 단일 실제 시험 사전조건, GO/NO-GO를 구체적으로 요약.
- docs/PROJECT_STATE.md 갱신, 원본·기존 결과 hash 보존.
- Isaac Sim/ROS/physics command, ENG001, QUAL12, 432-run, retry/sweep 모두 금지. 별도 사용자 명시 승인 전에는 runtime flag를 승인으로 바꾸지 마라.
- 보고서 생성 시 최종 메시지 마지막 줄:
HANDOFF_REPORT: reports/full_e2e_v02_hold_runtime_integration_20261019_v01.md
