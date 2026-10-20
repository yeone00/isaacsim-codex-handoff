# Full E2E v02 — 실제 paused preflight 결과 기반 HOLD host wiring 완성

상태: READY_FOR_MANUAL_APPROVAL
프로젝트: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
작성기준: 2026-10-20 실제 최초 paused live preflight (physics episode 0)

## 이번에는 실제 실행 결과부터 분석
다음 파일을 우선 읽어라. 추정이나 새 mock 보고서부터 시작하지 말 것:
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v01/status.json
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v01/host_installation.json
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v01/events.jsonl
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v01/stage_inventory.json
- 파생 레이어 derived_hold.usda, hold_writer_override.usda
- 현재 scripts/fe2e_v02_hold_host_binding_v01.py, scripts/fe2e_v02_hold_one_shot_v02.py, 기존 실제 stopping validation session, AGENTS.md, docs/PROJECT_STATE.md

실제 관측:
status={"status":"PREPARED","attempts":0}
host_installation={"subscriptions_installed":true,"pause_readback":true,"physics_played":false,"graph_barrier_certified":false,"foreign_writers_excluded":false,"metrics_status":"NOT_ACQUIRED_NO_PHYSICS","host_bound":"PARTIAL"}
events.jsonl에 PAUSE_READBACK event success=false, reason="paused installation probe; failure terminal, not stability validation".
Simulation App은 약 11.54초 후 종료. 이는 launch/구독/파생USD 생성의 일부 실증이며 live HOLD 작동/physical quiet/배타 writer 증거는 아니다.
pause_readback=true와 event success=false의 정의·실제 API 반환·의도적 negative terminal 여부를 소스 및 증거로 구분하고 거짓 성공 판정/false alarm을 고쳐라.

## 이번 구현의 핵심 결과물 — runner를 전진시킬 것
1. 현재 실제 graph wiring과 step sequence를 근거로 Ackermann 계산 완료 witness를 안전하게 취득하는 방법을 찾아 **작동하는 host adapter 코드**를 구현하라. 단순 bool/schema/mock 추가로 대신하지 말고 정확한 노드/속성/API와 동일 epoch의 증거·불가능한 경우 FAIL 이유를 남겨라.
2. 실제 StoppingAdapter phase를 기존 stopping validation runner로부터 연결하여 최초 ZERO_SETTLING 전에 wheel6 q/dq, steer4, base pose를 acquire+latch하고 단일 writer로 APPROACH/DECEL/HOLD dispatch하는 host path를 구현하라. 원본 controller, USD, drive/speed/threshold는 불변. 외부 direct writer가 검출되거나 배제 인증 실패 시 fail-closed.
3. raw COM→origin/FD, contact, clearance, guard independent observer의 실제 host 계측 취득·기록 연결을 구현하라. 실제 실행 전 스키마만 있는 측정값과 구분한다.
4. independent pause port의 호출/응답/Kit thread 전달과 wall watchdog 장애 경로를 구현·검증 가능한 구조로 정리하라. stalled Kit 중에도 강제 정지 보증이 없으면 UNKNOWN 표기; 성공이라고 하지 마라.
5. 기존 v02 CLI와 derived layer는 보존하고 versioned runner로 증분 구현. 실사용 one-shot 명령을 preflight/episode 용도로 구분하고, command/owner/metric/episode output 각각 런타임 차단 조건을 보존하라.

## 실행 정책
- 이번 턴 Codex는 기존 paused preflight 결과 분석, 코드 구현, 오프라인/정적 테스트만 허용.
- Isaac Sim 다시 launch하지 말 것; ROS 발행·physics.play·actuator 명령·주행·ENG001/QUAL12/432·자동 retry 금지.
- HOLD numeric K=1s^-1, wheel signed limit ±.020rad/s, slew .2rad/s², base guard .004m는 여전히 PROPOSED/UNAPPROVED. runtime 승인 bool을 허위로 변경하지 말라.
- 다음에 시행할 단 1회 live preflight 또는 물리시험 명령을 정확히 문서화하되, 이번에는 실행하지 않는다.
- 이미 33/33 PASS한 mock 결과를 재요약하는 보고서만으로 끝내지 말 것. 실제 host barrier/phase/observer wiring 개선 코드가 없으면 구현 실패로 명시.

## 종료 산출
reports/full_e2e_v02_hold_live_preflight_followup_20261020_v01.md
- 최초 live 결과의 실제 의미 및 pause_readback/event success 불일치 설명
- 추가·변경 구현 파일과 구체적인 host wiring 성취
- 새 테스트 결과, 기존 148 SHA 보존
- 남은 blocker 최대 3개 및 정확한 다음 1회 실행 명령
- 진입 gate(실제 보장/미보장)와 물리 GO/NO-GO
docs/PROJECT_STATE.md append.
보고서 작성 성공 시 마지막 줄:
HANDOFF_REPORT: reports/full_e2e_v02_hold_live_preflight_followup_20261020_v01.md
