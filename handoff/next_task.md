# Full E2E v02 — verified paused v02 result -> next graph-only witness test

상태: READY_FOR_MANUAL_APPROVAL (오프라인 코드 구현만; launch/physics 미승인)
작성일: 2026-10-20
프로젝트: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013

## 반드시 사용할 새 live 근거
먼저 AGENTS.md, docs/PROJECT_STATE.md, reports/full_e2e_v02_hold_live_preflight_followup_20261020_v01.md,
그리고 아래 실제 2026-10-20 v02 결과를 읽어라.
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v02/status.json
- 위 디렉터리의 host_installation.json, events.jsonl, execution_complete.json, stage_inventory.json 및 derived .usda
실제 외부 process exit=0, 11.267초 종료. status PAUSED_INSTALLATION_RECORDED_NO_GO, physics_episodes=0, actuator_commands=0, retry=0, research_denominator=0.
subscriptions_installed=true; ack_witness_installed=true; ack_witness_exercised=false; graph_barrier_certified=false; foreign_writers_excluded=false; metrics NOT_ACQUIRED_NO_PHYSICS.
PausePort event에서 pause_call_ok=true, paused_readback=true, delivery_ok=true, api_return=None, delivery_thread는 request_thread와 다름; physical_stop_verified=false, stalled_kit_stop_guarantee UNKNOWN.
이전 pause success=false 혼동은 해결됨. 똑같은 설치+pause readback만 재검증하는 미션은 하지 말 것.

## 이번 작업 목표
**Ackermann graph completion witness가 실제 설치된 paused Kit에서 ONDEMAND evaluate로 발화하고 값/epoch가 정확한지 확인할 수 있는 단일 무주행 테스트용 runner를 구현하라.**

1. 기존 scripts/fe2e_v02_hold_host_binding_v02.py, scripts/fe2e_v02_hold_one_shot_v03.py,
evaluation/fe2e_v02_hold_host_ports_v02.py 및 graph contract/stage inventory를 확인. 현재 v02 작업에서 설치만 한 Ackermann witness의 execIn/execOut 연결·ONDEMAND scheduler·ScriptNode registry/스레드 실행 경로를 정적/오프라인 진단하라.
2. 기존 Python host runner를 versioned v03/v04로 증분 작성해 신규 `graph-only-preflight` 모드를 마련하라. 반드시 timeline is_playing=false, physics callback count=0, actuator write count=0, ROS publish count=0, legacy 3 articulation writer inactive readback, 전체 active actuator writer inventory 확인을 gate로 요구. Graph 계산에는 명시적인 소형 synthetic Ackermann scalar 입력만 전달하고 실제 외부 ROS/Twist subscribe 값을 읽어 명령으로 보내지 말라. Graph node execution 외 모든 actuator writer는 영구 비활성화 상태여야 한다.
3. **witness를 실제 graph execOut → ScriptNode callback로 관측**, invocation count=1, 동일 explicit token/epoch, thread, source attribute paths, wheel/steer outputs 및 expected Ackermann node output 유한·단위·형상과 기록. evaluate_sync 반환이나 cached execOut 상태만 보고 성공으로 판단하지 말라. 같은 graph가 2회 실행되거나 증거 없으면 fail-closed. Physics paused 상태에서 graph computation이 불가능하면 명확한 FAIL reason을 제공하고 모의 witness로 채우지 마라.
4. graph-only의 GO는 graph 계산 경로에만 한정. 이번 시험으로 실제 Physics step 동기화, StoppingAdapter 실제 phase 전환, 독립 native/script writer 배제, physical pause/stop, observer 계측을 인증하지 않는다. 외부 direct writer 존재 가능성은 UNKNOWN으로 유지.
5. 새 versioned journal/CLI에는 PASS_GRAPH_ONLY, FAILED_GRAPH_ONLY 등 명확한 상태·exit. 런타임 preflight 중 정확한 이벤트/물리 count·output SHA·수정 source SHA/terminal 저장. 종료 시 Kit close 전 status 저장, 외부 exit 별도 표시.
6. 이번 Codex 작업에서는 위 runner 구현 및 오프라인 테스트만 시행. **Isaac/SimulationApp launch, ROS publish, physics.play, actuator 움직임, actual HOLD, ENG001/QUAL12/432-run, 재시도/튜닝 금지**. 원본 USD/controller/protocol/기존 148 hash와 연구 기록 보존.

## 단일 다음 live 시험 준비
이번 코드 구현이 끝나면 위 `graph-only-preflight`를 실제 Isaac5.1에서 단 한 번 실행할 정확한 command를 보고서에 제공하되 직접 실행하지 말 것. output은 unused versioned location, ROS domain은 다른 publisher 없는지 확인 전 UNKNOWN. Graph-only probe 시 반드시 ROS bridge/publisher는 시작하지 말고 actuator writes/physics zero 유지.

## 완료 보고
reports/full_e2e_v02_hold_graph_witness_probe_preparation_20261020_v01.md
- 실제 v02 preflight 결과 PASS/UNKNOWN 구분
- 신규 graph-only CLI/host 파일과 검사 결과, 실사용 entrypoint
- 다음 딱 1회 실제 graph-only test command, 실패/성공 evidence
- max 3 blockers, 수치/sign/dynamics unapproved, **physical NO-GO**
- legacy 원본·이전 결과 hash 보존, docs/PROJECT_STATE.md append
- 추가 코드가 불가능할 경우 감추지 말고 FAIL/구체 원인을 보고. 기존 57tests 재보고만 하고 종료하면 안 됨.
실제로 보고서를 생성한 경우 최종 메시지 끝에 정확히:
HANDOFF_REPORT: reports/full_e2e_v02_hold_graph_witness_probe_preparation_20261020_v01.md
