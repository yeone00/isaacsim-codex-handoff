# Full E2E v02 — 실제 graph-only 실패 1건 수정: execOut → ScriptNode execIn

상태: READY_FOR_MANUAL_APPROVAL — 표적 오프라인 진단/코드 수정만
기준: 2026-10-20 graph-only live probe v01 실패
프로젝트: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013

## 기존 실제 실패 증거를 먼저 읽어라
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v01/status.json
- 같은 폴더 execution_complete.json, events.jsonl, graph_only.usda, manifest.json
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v01.external_v01/external_exit.json, terminal.txt, command.json
- AGENTS.md, docs/PROJECT_STATE.md, reports/full_e2e_v02_hold_graph_witness_probe_preparation_20261020_v01.md
- scripts/fe2e_v02_hold_host_binding_v03.py, scripts/fe2e_v02_hold_one_shot_v04.py, scripts/fe2e_v02_graph_probe_external_v01.py, evaluation/fe2e_v02_graph_probe_v01.py

실제 관측:
- internal status=FAILED_GRAPH_ONLY
- reason=OmniGraphError('Failed to connect ackermann_controller.outputs:execOut -> /World/ENG_FE2E/Rover/ActionGraph/GraphOnlyWitnessV03.inputs:execIn')
- graph_evaluations=0, ack_compute_count=0, witness_invocation_count=0
- physics_callbacks=0, actuator_writes=0, ros_publishes=0, retry=0, research_denominator=0
- external wrapper external_process_exit=0. 내부 FAIL과 external exit0 불일치! 동일 output 재실행은 FileExistsError; 이 재실행은 실제 Isaac launch 전 차단됨.
- v01 output/sidecar 및 SHA 절대 수정·삭제·재사용 금지.

## 이번 작업의 정확한 목표
1. 연결 에러가 발생한 OG edge만 집중 진단. 실제 설치된 Isaac Sim 5.1 패키지의 ScriptNode 등록 node type/exec 속성 schema, execution port 존재/type, graph parent/path, 연결 API contract, USD custom attribute와 OG node attribute 차이를 소스 기반으로 확인.
2. 에러 직전 source/destination의 실제 node type, attribute path, OG type, existence, graph mode, 생성 순서와 API error detail을 기록할 수 있도록 코드를 보완. node path/relative-vs-absolute names/creation order/port type 문제는 확인 전 가설로 구분.
3. 가장 작은 versioned code repair로 정확한 native execOut -> ScriptNode execIn edge 연결을 고쳐라. controller 계산/witness 함수를 직접 호출해서 건너뛰는 편법 금지. 원본 controller/USD/protocol 보존.
4. 신규 다음 단일 live graph-only test에서는 연결 완료 후에도 실제 graph_evaluations=1, ack_compute_count=1, witness_invocation_count=1, token/epoch/thread/output matching, physics/actuator/ROS=0을 요구하도록 유지. graph edge만 이어졌다고 PASS 처리 금지.
5. wrapper가 external process exit0 + internal FAILED_GRAPH_ONLY이면 전체 성공으로 보이지 않도록 exit/final adjudication을 수정하고 오프라인 회귀검사에 이 케이스 포함. 이전 실패 파일을 소급 수정하지 말고 두 관측 분리 기록.
6. 단일 실패에 집중한 오프라인 tests, 변경 코드/기존 148 hashes 및 이전 실측 산출물 보존 확인. numerics/sign/dynamics/runtime approval false 유지.

## 실행 경계
- 이번 Codex 작업에서 Isaac/SimulationApp launch, graph live evaluation, ROS publish, physics.play, actuator commands, robot motion, ENG001, QUAL12, 432-run, retries/sweeps 모두 금지.
- 기존 v01 결과 보존; 새 미사용 v02 output+sidecar의 live graph-only 명령을 보고서에 준비하기만 하고 실행하지 말라.
- root cause를 확인하지 못하면 진실하게 UNKNOWN과 필요한 작은 다음 검사만 적어라. 이미 구현된 mock 계약을 반복 재보고하는 것으로 끝내지 말라.

## 완료 결과
reports/full_e2e_v02_graph_edge_failure_fix_20261020_v01.md: v01 실패 근거, root cause verified vs hypotheses, patch와 단위검사, wrapper exit 불일치 수정, 다음 실제 v02 단 1회 명령, NO-GO 및 최대 3개 blockers.
docs/PROJECT_STATE.md append. 원본/기존 결과 SHA 보존, physical NO-GO 유지.
보고서 실제 생성 시 최종 응답 마지막 줄:
HANDOFF_REPORT: reports/full_e2e_v02_graph_edge_failure_fix_20261020_v01.md
