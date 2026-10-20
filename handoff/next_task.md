# Full E2E v02 — real graph-only v02: edge PASS, Ack compute/witness 0

상태: READY_FOR_MANUAL_APPROVAL. 현 단계는 오프라인 표적 수정만; 실제 Isaac Sim 재실행은 별도 1회 수동 승인
프로젝트: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
기준: 2026-10-20 사용자가 실제 실행한 v02 graph-only probe FAILED_GRAPH_ONLY

## 반드시 실제 v02 증거부터 확인
Read-only:
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v02/status.json
- 동일 폴더 events.jsonl, execution_complete.json, stage_inventory.json, graph_only.usda, synthetic_inputs.json, runtime_sources.json, manifest.json
- /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v02.external_v02/final_adjudication.json, external_exit.json, terminal.txt
- AGENTS.md, docs/PROJECT_STATE.md, reports/full_e2e_v02_graph_edge_failure_fix_20261020_v01.md
- scripts/fe2e_v02_hold_host_binding_v04.py, scripts/fe2e_v02_hold_one_shot_v05.py, scripts/fe2e_v02_graph_probe_external_v02.py, evaluation/fe2e_v02_graph_probe_v01.py, evaluation/fe2e_v02_graph_edge_v01.py
과거 v01 failure 원본도 보존.

실제 이번 관측:
1. EXEC_EDGE_BEFORE_CONNECT: source Ackermann outputs:execOut와 destination GraphOnlyWitnessV03 inputs:execIn 둘 다 valid OG attribute, 동일 graph, 모두 uint(execution), source OUTPUT/dest INPUT.
2. EXEC_EDGE_CONNECTED: 앞선 relative-path edge 문제는 실제로 고쳐졌다. 이것을 다시 고치지 말라.
3. GraphPipelineStage.ONDEMAND, evaluator=execution. graph_evaluations=1; ack_compute_count=0; witness_invocation_count=0.
4. FAILED_GRAPH_ONLY RuntimeError('MISSING_DUPLICATE_GRAPH_COMPUTE_OR_WITNESS'); no physics_callbacks, actuator_writes, ROS publishes, retry or research runs.
5. external child_exit=0, internal FAILED_GRAPH_ONLY, wrapper_exit=1, overall_success=false: wrapper adjudication 개선 성공. 다시 수정 대상 아님.

## 이번의 단일 결함: 평가 호출은 있었는데 실행 노드 compute가 감지되지 않음
근거 없이 scheduler failure나 monkeypatch failure로 단정하지 말 것. 둘을 분리해 진단.
A. Isaac Sim 5.1 설치 소스의 OmniGraph execution evaluator/ONDEMAND, registered OgnAckermannController compute ABI, OnDemand evaluate_sync, execIn input/exec trigger/dirty state, ScriptNode scheduler API와 지금 작성된 stage graph input disconnect/readback을 확인. 오프라인 분석에서 진짜 root cause와 검증 안 된 가설 분리.
B. 현재 GraphOnly runner가 'graph_evaluations=1'을 언제 증가시키는지 확인. 이는 evaluate_sync 호출 횟수이며 Ackermann compute 실제 호출을 보증하지 않음. compute monkeypatch/callback registry를 교체해도 native ABI가 다른 경로에서 처리하는지 확인. 실제 계산이 아예 스케줄되지 않은 경우와 모니터만 빠진 경우를 구분할 수 있도록 별도 live 이벤트/카운터를 도입.
C. Graph node execution을 정상 스케줄하는 설치된 공식 API/포트 경로를 찾아 작은 버전업으로 수정하라. 필요시 paused/on-demand에서 작동하는 명시적인 테스트용 exec trigger를 구성할 수 있으나 Isaac/ROS/Twist/physics stepping/actuator writer에 연결하지 말 것. 임의로 Ackermann compute()나 Witness.compute(), registry.deliver()를 직접 호출해서 PASS로 꾸미지 말 것.
D. 다음 단일 live graph-only에서 evaluate=1, actual Ack compute=1 및 ScriptNode witness=1, token/epoch/thread/source/output 검증. compute 호출/해석 불가능 또는 callback 0이면 반드시 FAIL; 연결 성공만으로 PASS 금지.
E. 향후 live 사용 전 후속 단일 문제점 진단 이벤트에 graph evaluator/scheduler mode, node states enabled/readback, exec input state, live actual evaluation result, ABI instrumentation method, node output before/after sentinel, witness invoke detail, complete traceback 저장. 신규 probe는 stage/graph-only 강제 gating. 물리 callbacks/actuator commands/ROS publishes 반드시 0.
F. 오프라인 최소 테스트 및 원본 파일/출력/해시 보존. 기존 183 SHA 등의 baseline 임의 수정 금지. numerical K/sign/dynamics/runtime approval false 유지, physical NO-GO.

## 절대 금지
이번 Codex 작업에서는 Isaac/SimulationApp live launch, physics.play, graph live execution, ROS 발행, 액추에이터 명령, 실제 HOLD, ENG001, QUAL12, 432-run, 임의 튜닝·자동 재시도 금지.
다음에는 v01/v02와 다른 **새 미사용 v03** output과 sidecar에서만 정확히 1회 graph-only test command를 준비하고 이번 작업 중 실행하지 말 것.

## 종료
- 변경된 versioned code 파일 + 실제 설치 API 소스 경로/확인된 scheduler 원인(근거 부족이면 UNKNOWN) + offline test 로그.
- 보고서 reports/full_e2e_v02_graph_compute_dispatch_fix_20261020_v01.md: v02 관측 정리, 수정 내용, PASS/FAIL·UNKNOWN, 다음 1회 명령, blocker 최대 3개, physical NO-GO.
- docs/PROJECT_STATE.md append; 원본/USD/previous v01-v02 failure 그대로.
- 보고서가 실제 생성된 경우 마지막 줄:
HANDOFF_REPORT: reports/full_e2e_v02_graph_compute_dispatch_fix_20261020_v01.md
