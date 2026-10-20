# Full E2E v02 graph compute dispatch 표적 수정 — 2026-10-20

**READY_FOR_MANUAL_APPROVAL / offline PASS / live dispatch UNKNOWN / physical NO-GO.** 이번 Isaac/SimulationApp launch, graph live execution, physics.play, ROS publish, actuator command, actual HOLD, ENG001, QUAL12, 432-run, 자동 retry/튜닝 모두 0. 연구 denominator=0. numerical K/sign/dynamics/runtime approval=false 유지. 다음 실행도 별도 명시적 수동 승인 후 graph-only 정확히 1회다.

## 실제 v02 증거

`/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v02`의 status/events/execution_complete/stage_inventory/graph_only.usda/synthetic_inputs/runtime_sources/manifest와 `.external_v02`의 final_adjudication/external_exit/terminal을 읽었다. AGENTS/README/PROJECT_STATE/PROTOCOL_LOCKS, 이전 edge 수정 보고서 및 지정 runner/CLI/wrapper/evaluation 원본도 정적으로 확인했다.

- `EXEC_EDGE_BEFORE_CONNECT`: 같은 graph의 유효한 OG attribute, uint(execution), OUTPUT→INPUT. `EXEC_EDGE_CONNECTED`가 실제 기록됐다. 이전 상대경로 edge 결함은 해결됐으며 해당 helper를 수정하지 않았다.
- ONDEMAND/evaluator=execution, graph_evaluations=1, ack_compute_count=0, witness_invocation_count=0. 내부 `FAILED_GRAPH_ONLY`, `MISSING_DUPLICATE_GRAPH_COMPUTE_OR_WITNESS`. physics_callbacks/actuator_writes/ros_publishes/retry/research_denominator=0.
- child_exit=0, internal FAILED_GRAPH_ONLY, wrapper_exit=1, overall_success=false. 기존 wrapper 판정은 성공적으로 실패를 검출했다. 새 wrapper는 CLI 버전과 sidecar 이름만 변경했고 판정 로직을 유지한다.
- [실제 manifest 검증](fe2e_v02_graph_compute_dispatch_20261020_v01/v02_verification.json): 입력 35/35 SHA PASS. [최종 검사](fe2e_v02_graph_compute_dispatch_20261020_v01/final_checks.json): status output hash 및 execution_complete 일치 PASS. 기존183을 포함한198 SHA PASS. baseline expected를 변경하여 통과시키지 않았다. 새 preservation inventory는 작업 전 관측값을 추가한 것이며 독립 과학 lock 인증이 아니다. v01/v02 실패·USD·기존 code 모두 보존했다.

## 확인된 사실과 원인 UNKNOWN의 경계

**확인된 구성 결함:** v04는 stage에서 Ackermann의 모든 inputs 연결을 해제한다. 실제 저장 stage도 execIn upstream이 없고 synthetic_inputs의 원래 execIn은 None이다. 이후 `request_compute()`와 `evaluate_sync()`만 호출하며 명시적인 execution 입력 발생기를 구성하지 않는다. request_compute 반환값도 기록하지 않았다. 따라서 해당 평가 호출이 downstream 실행 신호를 만들었다는 증거가 없다.

**확정하지 않은 것:** 이 결함이 v02의 compute0을 발생시킨 유일한 native scheduler 원인인지는 UNKNOWN이다. request_compute는 설치 API상 compute 요청이며, 이 요청이 해당 execution evaluator/dirty 상태에서 어떻게 처리됐는지 v02에는 native count·disabled state·평가 직후 output 기록이 없다. “scheduler 고장” 또는 “monkeypatch 실패”로 단정하지 않는다. graph_evaluations는 노드 compute 횟수가 아니다. 기존 Probe는 fn 실행 전, 심지어 gate 전 카운터를 올렸다. v02는 traceback상 fn에서 예외 없이 돌아왔지만 이것은 Ack compute 증명이 아니다.

설치 Python ABI는 `NODE_TYPE_CLASS.compute`를 호출 시점에 동적으로 조회한다. 현재 등록 module/hash도 그 설치 파일과 일치한다. Python ABI가 실제 진입했다면 class wrapper가 관측할 구조이며, 설치 소스에서는 캐시된 별도 compute 함수로 우회하는 근거를 찾지 못했다. 그러나 native 등록 dispatch가 실제 그 ABI를 호출했는지는 v02 로그만으로 입증되지 않는다. class/registry를 교체해서 해결됐다고 주장하지 않으며 등록 ABI를 재등록하지 않았다.

## 설치 공식 API 근거

아래는 실제 파일을 import하지 않고 읽은 경로다. 전체 절대경로와 SHA는 [installed_sources.json](fe2e_v02_graph_compute_dispatch_20261020_v01/installed_sources.json)에 있다. 설치 root는 `/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim`이다.

| root 아래 실제 source | 확인 내용 |
|---|---|
| `extscache/omni.graph-1.141.2+69cbf6ad.lx64.r.cp311/omni/graph/core/_impl/controller.py:388` | evaluate_sync는 대상 graph를 해석하고 ONDEMAND를 포함한 일반 분기에서 graph.evaluate() 호출. 반환값은 별도 compute 성공 receipt가 아니다. |
| 같은 extension `omni/graph/core/_omni_graph_core.pyi:4234,4345,4429` | Node.get_compute_count는 native computation instance 수, is_disabled readback, request_compute()->bool 정의. Graph.get_evaluator_name/is_disabled도 제공된다. native counter 단독으로 Python 계산 성공을 주장하지 않는다. |
| `extscache/omni.graph.action_nodes-1.50.4+107.3.0.lx64.r.cp311.u353/omni/graph/action_nodes/ogn/nodes/OgnOnImpulseEvent.ogn` | 공식 실행 발생기. compute-on-request/threadsafe, state:enableImpulse=true이면 execOut 1회 후 false로 reset. inputs:onlyPlayback=false는 paused 사용 경로다. 내장 test도 해당 조합을 정의한다. |
| 같은 extension `omni/graph/action_nodes/tests/test_action_graph_nodes_02.py:277` | execution graph에서 OnImpulse.execOut→Counter.execIn, onlyPlayback=false, enableImpulse=true 후 count1 확인. 해당 공식 test는 update yield 기반이므로 ONDEMAND evaluate_sync 조합의 live 성공까지 입증하지는 않는다. |
| `exts/isaacsim.robot.wheeled_robots/isaacsim/robot/wheeled_robots/ogn/OgnAckermannControllerDatabase.py:331` | ABI는 동적 NODE_TYPE_CLASS.compute(db), input prefetch 및 output commit. 다인자 compute 분기도 존재하나 실제 설치 compute는 단일 db 인자다. |
| 같은 extension `isaacsim/robot/wheeled_robots/ogn/python/nodes/OgnAckermannController.py:81` | 실제 계산은 synthetic command로 controller.forward 후 wheel/steer output을 기록하고 execOut=ENABLED. 오류면 False 반환. 물리 actuator apply 호출은 없다. |
| `extscache/omni.graph.scriptnode-1.50.0+107.3.0/omni/graph/scriptnode/ogn/python/nodes/OgnScriptNode.py` 및 `.ogn` | execIn execution 입력, usd-write scheduling, 등록 compute가 사용자 script를 compile하고 compute(db)를 호출한다. Witness를 직접 호출하지 않고 이 경로로 관측한다. |

초기 source 검색에서 존재하지 않는 `ogn/nodes/OgnAckermannController*` 경로에 rg 오류가 있었으며 이후 실제 `ogn/python/nodes`와 등록 runtime_sources 경로를 확인했다. 설치 파일 실행이나 수정은 없었다.

## 새 versioned code와 fail-closed 판정

- `scripts/fe2e_v02_hold_host_binding_v05.py`: 기존 edge helper 유지. 새 `GraphOnlyImpulseV03`(OnImpulseEvent)→Ackermann.execIn→기존 GraphOnlyWitnessV03. onlyPlayback=false. synthetic scalar/출력 sentinel/paused·ONDEMAND·execution/legacy writers inactive/전체 active node 3개 allowlist/외부 Ack scalar 연결 금지를 강제한다. trigger는 Isaac/ROS/Twist/physics/actuator writer와 연결하지 않는다. 기존 derived stage는 새 layer에서만 참조한다.
- `evaluation/fe2e_v02_graph_probe_v02.py`: graph_evaluations는 실제 evaluate_sync 호출 직전에만 증가. attempt 재사용은 별도 guard로 금지. witness scheduler entry에서 실제 db.node path/exec input, token/epoch/thread를 기록하고 path를 검사한다. witness 실패 traceback도 저장한다. gate 실패는 evaluate0으로 남는다.
- `evaluation/fe2e_v02_graph_dispatch_v01.py`: trigger/Ack/witness의 독립 native counter 전후 delta 각각1 요구. counter unavailable/rollover/0/중복/해석 불가능은 FAIL. 별도의 등록 class wrapper count1과 witness1도 반드시 필요하다.
- `scripts/fe2e_v02_hold_one_shot_v06.py`, `scripts/fe2e_v02_graph_probe_external_v03.py`: graph-only 전용 새 entry와 `.external_v03`. wrapper adjudication 유지, retry 없음.
- `analysis/test_fe2e_v02_graph_dispatch_v01.py`: native delta0/중복/불명확/rollover, evaluate1+callback0 거부, gate 전 평가0, 두 번째 시도 거부, 실제 생성 script 문법 검사.

새 이벤트는 DISPATCH_BEFORE/AFTER의 evaluator/pipeline/graph·node disabled/native count/execIn/impulse/output sentinel 전후, EXPLICIT_IMPULSE_ARMED readback, EVALUATE_SYNC_RETURN 실제 반환형·repr, ACK_ABI_INSTRUMENTATION 실제 ABI/compute code 위치·인자 수, ACK_COMPUTE_ENTER/RETURN, WITNESS_SCHEDULER_ENTRY 및 검증 receipt, 실패 complete traceback이다. 기존 terminal-before-close와 외부 terminal 보존도 유지한다. ABI 재등록/registry 교체 없이 class wrapper와 native node counter를 독립 비교한다.

판독은 다음과 같다. native Ack delta0+wrapper0이면 native 계산 호출도 관측되지 않은 상태다. native delta1+wrapper0이면 ABI 계측/dispatch 경로 불일치이며 FAIL이다. wrapper1이지만 witness0이면 compute 반환/execOut/output/ScriptNode 경로를 조사하며 FAIL이다. 모든 계수1이어도 token/epoch/thread/source/output shape·finite·expected value 검증 또는 zero counter gate가 실패하면 FAIL이다. 어떤 경우도 연결 성공만으로 PASS하지 않는다. registered compute/Witness.compute/registry.deliver를 host에서 직접 호출하지 않는다. wrapper는 scheduler에서 들어온 원래 compute만 위임한다.

## 오프라인 결과와 제한

[최종 tests 로그](fe2e_v02_graph_compute_dispatch_20261020_v01/offline_tests_final_29.txt): 신규5+기존24=29/29 PASS. 새6개 Python 파일 compile PASS, 실제 생성 ScriptNode 문자열 compile PASS. legacy/설치 scientific module import·SimulationApp 실행 없음. [새 code hash](fe2e_v02_graph_compute_dispatch_20261020_v01/new_code_hashes.json).

최초 생성 script compile에서 닫는 괄호 누락 SyntaxError가 발견됐다. module py_compile만으로는 문자열 내부 문법을 검출하지 못했다. 이를 수정하고 실제 문자열 compile 회귀검사를 추가했으며 [초기 실패 기록](fe2e_v02_graph_compute_dispatch_20261020_v01/generated_script_initial_failure.txt)과 이전28tests 로그를 보존했다. live 실패/연구 denominator로 치환하지 않는다.

PASS는 offline 논리·문법·보존 범위다. 설치 공식 trigger의 paused/ONDEMAND 실제 dispatch, native counter 작동, ScriptNode 실제 실행은 UNKNOWN이며 다음 단1회에서 확인한다. 외부 native/direct writer 전역 배제는 UNKNOWN. 새 expected threshold/gain/K/sign/dynamics 승인을 만들지 않았다.

## 다음 정확히 1회 명령 — 준비만, 이번에는 실행하지 않음

최종 로컬 검사에서 output과 sidecar 모두 미존재. 사전 생성하지 않았다. 별도 수동 승인 이후 실행 직전 충돌·hash를 재확인한다. 충돌 시 재사용/자동 version retry하지 않는다.

```bash
ROS_DOMAIN_ID=193 /home/user/anaconda3/envs/hh_isaac51/bin/python /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/fe2e_v02_graph_probe_external_v03.py --domain 193 --approve-graph-only-launch --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v03
```

sidecar: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v03.external_v03`. 목표 evaluate=1, actual Ack compute=1, ScriptNode witness=1, trigger native delta1, physics_callbacks=actuator_writes=ros_publishes=0. callback0/compute 불명확/해석 불가능은 반드시 FAILED_GRAPH_ONLY와 wrapper exit1. 실패해도 자동 재시도 없다.

남은 blocker는 3개다.

1. v02 native scheduler 단일 root cause UNKNOWN; 새 공식 trigger/ONDEMAND 및 독립 native 계수 live 검증 미실시.
2. 물리 thread ownership/외부 native writer 배제/독립 정지·observer/stop envelope 미인증.
3. numerical K/sign/dynamics/runtime approval=false. **physical NO-GO**, HOLD/ENG001/QUAL12/432 승인 없음.
