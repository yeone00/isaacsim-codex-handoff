# Full E2E v02 — Isaac Sim host binding: implementation toward first physical HOLD validation

상태: READY_FOR_MANUAL_APPROVAL
프로젝트: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
작성기준: 2026-10-20 보고서 reports/full_e2e_v02_hold_runtime_integration_20261019_v01.md

## 목적 — mock 추가 반복 금지
기존 wheel HOLD adapter/owner(15/15 offline PASS), HOLD runtime integration(12/12 offline PASS), one-shot metadata CLI까지 구현 완료. 더 이상 선정, 문헌조사, 범용 감사, mock-only 추상 인터페이스를 새로 추가하는 것으로 끝내지 말 것. 다음 단계는 **실제 Isaac Sim host callback/graph/pause 연결을 실행 가능한 코드로 완성**하고 실환경 시험 준비를 끝내는 것이다.

반드시 먼저 AGENTS.md, docs/PROJECT_STATE.md, 두 구현 보고서, 실제 session runner scripts/fe2e_v02_stopping_validation_session_v01.py 및 graph.json, 실제 로봇 USD reference, 새 integration/owner/adapter/one-shot 파일을 확인하라.

## 이번 허용 범위
1. 기존에 사용하던 Isaac Sim launcher와 scene loading 코드를 식별하라. 실제 소스·경로·버전·entrypoint를 보고서에 정확히 남겨라. 완전히 새로운 런타임 스택을 만들지 말라.
2. 기존 실험 runner를 참고하여 **실제 호스트용 단일 진입점** (새 파일)으로 Isaac callback binding을 구현하라. derived edit-layer에서 기존 세 articulation writer만 비활성화하고, stage 전체 추가 writer inventory가 불확실하면 fail-closed. 미리 존재하는 function을 그대로 import하여 실제 callback으로 바인딩, epoch barrier와 same-step samples를 host 측에서 수집하라.
3. APPROACH/DECEL의 Ackermann graph output을 단일 owner의 명시 DOF 이름 매핑으로 보내고, 첫 ZERO_SETTLING에서 latch-before-write 후 HOLD owner만 실행되게 하라. native joint rad/s·rad 계약과 원본 controller/threshold/drive/surface-wire scale 불변.
4. 독립 physics observer + wall-time watchdog + 실제 timeline pause port 설치 코드를 완성하라. watchdog이 physics callback에 의존해 멈추지 않도록 하고, pause failure는 성공으로 취급하지 말라. 비활성 legacy direct writer·foreign direct writer 미배제 시 진입 거부.
5. 기존 one-shot CLI가 실제 host runner를 가리키도록 정리하라. input/output/domain/hash/event/per-step metrics/terminal status와 nonzero failure exit, no-retry 보장. 실제 launcher 호출 예시를 작성하되 정확한 환경에서의 시행 가능 여부를 구분하라.
6. 기존 단위 테스트 + host-binding 정적/오프라인 테스트를 수행하라. mock 통과만으로 물리 안정성 승인하지 말라. 수치 K=1s^-1, signed ±.020rad/s, slew .2rad/s², guard .004m 등은 PROPOSED / UNAPPROVED 유지. Wheel sign 계측 누락·외부 writer 불명·pause 설치 누락 시 runtime gate false 유지.

## 실행 경계 — 아주 중요
- 이번 턴에는 실제 ROS publish, actuator command, wheel movement, 실주행, physics episode, ENG001, QUAL12, 432-run, auto-retry/sweep **절대 실행하지 말라**. 실제 Isaac Sim launch 또한 사전 승인을 받기 전에는 실행하지 말라.
- 원본 USD·기존 frozen controller/기존 결과·연구 protocol/기존 cost denominator·hash inventory를 보호하라.
- 실환경 live smoke/one-shot 실험은 다음 단계의 별도 명시적 승인 사항이다.

## 종료 기준
- 파일만 설명하지 말고 실행 가능한 **실제 host binding runner 코드**와 정확한 별도 live preflight / one-shot 명령을 만들어라. 실행 금지 사항은 그대로 유지.
- 독립 pause·graph writer exclusivity의 host 측 기술적 한계가 남으면 구체적으로 FAIL/UNRESOLVED를 명시하고 임의 승인하지 말라.
- reports/full_e2e_v02_hold_host_binding_20261020_v01.md에: 생성 파일, 실제 import/entrypoint, unit 결과, host-bound 여부, blocker 최대 3개, 다음 단일 live test 호출 명령(실행 안 함), 필요한 구체적 승인 사항, GO/NO-GO.
- docs/PROJECT_STATE.md append; 기존 해시 재검사. 단순 새 mock 보고서로 종료하지 말 것.
- 실제 보고서를 만든 경우 완료 메시지 마지막 줄:
HANDOFF_REPORT: reports/full_e2e_v02_hold_host_binding_20261020_v01.md
