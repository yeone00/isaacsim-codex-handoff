# Full E2E v02 graph completion witness — 단일 paused probe 준비

2026-10-20. **오프라인 구현·검사 PASS / 실제 graph 실행 UNKNOWN / physical NO-GO.** 다음 단일 graph-only 시험은 수동 승인 대기다. 이번 작업에서 Isaac/SimulationApp launch, ROS publish, physics.play, actuator write, actual HOLD, ENG001/QUAL12/432-run, retry·튜닝은 모두 0이며 연구 denominator=0이다. 기존 설치+pause readback 시험을 반복하지 않았다.

## 새 실제 v02 근거

읽은 디렉터리: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v02`. status, host_installation, events, execution_complete, stage_inventory, derived_hold.usda, hold_writer_override.usda 및 manifest를 직접 확인했다. manifest 입력 **11/11 SHA PASS**: [검증](fe2e_v02_graph_probe_preparation_20261020_v01/live_v02_manifest_verification.json).

| 항목 | 판정과 범위 |
|---|---|
| 설치 및 정상 terminal | PASS: PAUSED_INSTALLATION_RECORDED_NO_GO, execution_complete 존재, subscriptions_installed=true, ack_witness_installed=true |
| pause 전달 | PASS: pause_call_ok/paused_readback/delivery_ok=true, api_return 문자열 `None`, api_return_type=NoneType. request thread 132575114806976 → delivery thread 132606506420032. 이전 literal success=false 혼동은 해결됨 |
| 무물리 결과 | 기록상 physics_episodes=0, actuator_commands=0, retry=0, research_denominator=0, metrics NOT_ACQUIRED_NO_PHYSICS |
| graph | active Ackermann + witness, 기존 3 articulation writer와 ROS/tick 등 inactive. witness execIn 연결은 Ackermann.outputs:execOut. pipelineStageOnDemand. 설치 PASS이나 ack_witness_exercised=false, graph_barrier_certified=false이므로 실제 계산 UNKNOWN |
| 정지·배타성 | foreign_writers_excluded=false, physical_stop_verified=false, stalled_kit_stop_guarantee UNKNOWN. physical GO 아님 |
| 외부 종료 | 사용자 제공 실제 관측 exit=0 / 11.267초. 기존 디렉터리에 독립 external exit/elapsed 파일은 없어 이 숫자의 로컬 파일 재검증은 UNKNOWN. 내부 shutdown_completion도 UNKNOWN 유지 |

## 정적 진단과 구현

기존 host binding v02 / CLI v03 / ports v02와 graph_contract를 읽었고 원본은 변경하지 않았다. 설치된 Ackermann .py/.ogn, 등록 DB ABI, 실제 controller 수식과 ScriptNode 구현을 **텍스트로만** 확인했다. [설치 소스·contract SHA](fe2e_v02_graph_probe_preparation_20261020_v01/static_source_evidence.json).

- 기존 CompletionBarrier는 actual physics receipt>0을 요구한다. 이를 완화하면 physical barrier 의미가 바뀌므로 기존 코드를 유지하고 physics_epoch=0 전용 Probe를 새로 작성했다.
- 기존 witness는 USD custom token execIn으로 작성되어 있다. 등록 schema의 execution 포트와의 live 호환성은 미검증이다. 신규 witness는 `og.Controller.edit`의 등록 ScriptNode schema로 생성하고 정확한 execOut→execIn 연결을 읽어 검사한다. 이전 방식이 반드시 실패했다고 단정하지 않는다.
- 새 stage는 검증된 v02 derived_hold.usda를 sublayer로 읽는 **새 stronger layer**다. 전체 composed stage의 node:type inventory를 순회해 Ackermann 이외 노드를 inactive로 작성하고 새 witness만 추가한다. inherited input 연결 제거는 `SetConnections([])`로 명시적으로 차단한다. `ClearConnections()`로 상위 layer 연결이 다시 드러날 여지를 피한다. 원본 USD/controller/protocol/기존 layer를 저장하지 않는다.
- ONDEMAND readback, legacy writer 3개 존재·inactive, 전체 active node 집합이 Ackermann+witness와 정확히 일치, Ackermann 모든 input 연결 없음, witness source 연결 일치, timeline not playing·동일 time, PhysX callback count0, probe-owned actuator/ROS count0, ROS bridge extension 비활성화를 평가 전·compute 진입·callback·평가 후 gate로 요구한다. bridge가 이미 활성화되어 있으면 FAIL하며 이 runner는 bridge를 시작하거나 ROS publisher/subscriber를 생성하지 않는다. Physics subscription은 SimulationApp 생성 후 stage attach 전에 설치한다. bootstrap 이전 물리 이벤트나 외부 native/direct writer의 전역 계측을 주장하지 않는다.
- 명시 synthetic scalar는 speed=.015m/s, steeringAngle=0rad, steeringAngleVelocity=0rad/s, acceleration=0m/s², dt=.01s다. 외부 ROS/Twist는 읽지 않는다. radius/limits/geometry는 stage 값을 읽고 바꾸지 않는다. registered controller의 직진식으로 wheel4 rad/s와 steer2 rad를 예상한다. 정상 radii=.5m·비포화이면 wheel4=.03rad/s, steer2=0rad. 실제 radii/limit으로 검증하며 shape4/2, finite, absolute tolerance1e-8을 요구한다. 여기서 dt는 수식 입력이며 물리 step 증거가 아니다.
- 기존 ingress의 degrees 변환과 설치 Ackermann .ogn의 steeringAngle **rad** 명세를 구분했다. 이번 직진 시험은 단위/sign/곡선·수치 dynamics 인증을 하지 않으며 기존 ingress를 수정·튜닝하지 않았다. wheel4/steer2 native 출력은 실제 wheel6/steer4 actuator command로 변환·전달하지 않는다.

새 파일:

| 파일 | 역할 |
|---|---|
| `evaluation/fe2e_v02_graph_probe_v01.py` | 별도 token/epoch barrier, registry, finite/shape/expected output validator |
| `scripts/fe2e_v02_hold_host_binding_v03.py` | 실제 paused stage/ONDEMAND 단일 평가와 journal; physical mode 없음 |
| `scripts/fe2e_v02_hold_one_shot_v04.py` | 실사용 graph-only-preflight entrypoint |
| `scripts/fe2e_v02_graph_probe_external_v01.py` | child 정확히 1회, terminal·실제 외부 exit·elapsed·SHA 저장; retry 없음 |
| `analysis/test_fe2e_v02_graph_probe_v01.py` | 신규 오프라인 fault injection 및 CLI/wrapper 검사 |

callback은 ScriptNode.compute → `evaluation.fe2e_v02_graph_probe_v01.deliver` → process-local REGISTRY의 동일 Probe로 들어온다. inline script에 explicit token과 `{probe_epoch:1, physics_epoch:0, timeline_s:...}`를 고정하고 callback의 thread/source output paths/값을 기록한다. callback 안에서 native 출력을 읽어 예상값과 비교한다. cached 출력은 평가 전 -999 sentinel로 채워 오래된 값의 재사용을 거부한다. registry 누락/잘못된 module identity면 예외 또는 receipt 누락으로 FAIL한다.

실제 등록 `OgnAckermannControllerDatabase.NODE_TYPE_CLASS.compute`를 process-local counting wrapper로 감싸 **원래 compute를 그대로 호출**한다. evaluate 호출1·실제 Ack compute1·실제 ScriptNode callback1 모두 필요하다. ABI는 이 등록 class의 compute를 동적으로 조회하므로 source상의 경로가 연결된다. 중복 compute가 ABI에서 예외를 삼켜도 count2로 FAIL한다. ScriptNode가 callback 예외를 삼켜도 poison/receipt 검사가 FAIL한다. 반환값·cached execOut만으로 PASS하지 않는다. worker thread callback은 FAIL하며 허용 thread를 임의로 변경하지 않는다. API/schema/scheduler가 paused 계산을 지원하지 않거나 receipt가 없으면 FAILED_GRAPH_ONLY로 종료한다. mock receipt를 live에 주입하는 경로는 없다.

`PASS_GRAPH_ONLY`/exit0 또는 `FAILED_GRAPH_ONLY`/exit1을 Kit close **전에** status/execution_complete에 쓴다. count/token/epoch/실제 source SHA/출력과 output SHA, 실패 traceback, 입력·명령·환경을 보존한다. close 자체가 내부 terminal과 다른 방식으로 종료될 수 있으므로 외부 wrapper가 terminal.txt, external_exit.json을 따로 저장하고 exit0+내부 PASS 모두 있어야 성공을 반환한다. fatal crash/Kit hang 시 내부 terminal은 없을 수 있으며 이를 PASS로 대체하지 않는다. 자동 timeout/kill/retry는 없다.

## 오프라인 검사 및 보존

- **신규 18/18 PASS**: 누락·중복 callback/중복 Ack compute, explicit token/epoch, worker thread, gate 실패, swallowed ScriptNode exception, registry identity/누락, shape4/2·finite·expected values, radius/limit, terminal 사전 저장·output 재사용 거부, 승인 없는 CLI launch 차단, 외부 exit0만으로 PASS하지 않음. [최종 로그](fe2e_v02_graph_probe_preparation_20261020_v01/offline_tests_v02.txt). 초기16개 로그도 보존했다. Synthetic 검사는 live witness 증거가 아니다. 기존57 tests 재보고로 대체하지 않았다.
- 새 Python 5개 py_compile PASS. 실제 unapproved CLI는 **예상된 exit1/FAILED_GRAPH_ONLY**, reason MANUAL_GRAPH_ONLY_LAUNCH_APPROVAL_REQUIRED, graph eval0/physics0. [차단 status](fe2e_v02_graph_probe_preparation_20261020_v01/cli_unapproved/status.json). 실패를 삭제하지 않았다.
- 기존 **148/148 SHA PASS**, 이전 preflight·기존 host/ports/contract 및 새 live v02 결과 포함 **172/172 보존 PASS**. [작업 전 baseline](fe2e_v02_graph_probe_preparation_20261020_v01/preservation_baseline.json), [작업 후](fe2e_v02_graph_probe_preparation_20261020_v01/preservation_after.json). 기존 expected를 observed로 고치지 않았다. baseline의 새 v02 결과 hash는 이번 관측값이며 독립 과거 expected로 주장하지 않는다.
- known-lock subset exit0/PASS, full_experiment_ready=false 유지. [결과](fe2e_v02_graph_probe_preparation_20261020_v01/known_locks.json). 신규 source SHA는 [별도 inventory](fe2e_v02_graph_probe_preparation_20261020_v01/new_source_sha256.json)에 기록했다. package 설치/업그레이드, legacy Python 실행, Git staging/push 없음.

## 다음 딱 1회 live command — 이번에는 실행하지 않음

별도 수동 승인 후 아래 **한 명령만** 실행한다. output 및 `.external_v01` sidecar는 이번 확인에서 둘 다 미존재이며 실행 때도 exclusive mkdir로 검사한다. ROS_DOMAIN_ID193에 다른 publisher가 없는지는 **UNKNOWN**이다. domain 설정만으로 격리 PASS라고 하지 않으며 bridge/publisher는 시작하지 않는다.

```bash
ROS_DOMAIN_ID=193 python3 /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/fe2e_v02_graph_probe_external_v01.py --approve-graph-only-launch --domain 193 --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v01
```

wrapper가 실제 Isaac5.1 `/home/user/anaconda3/envs/hh_isaac51/bin/python`으로 `scripts/fe2e_v02_hold_one_shot_v04.py --mode graph-only-preflight --approve-graph-only-launch --domain 193 --output <위 경로>`를 정확히 1회 호출한다. 이것이 실사용 Isaac entrypoint다. wrapper와 child를 각각 실행하면 2회가 되므로 하나만 실행한다.

성공 evidence: external_exit=0 및 내부 PASS_GRAPH_ONLY, graph_evaluations=1, ack_compute_count=1, witness_invocation_count=1, 동일 explicit token/epoch/thread, callback 내부 wheel4/steer2 유한·예상값 일치, source paths, timeline 정지·physics/actuator/ROS0, legacy3 inactive·active allowlist 및 output/source SHA. 성공 범위는 **graph 계산 경로만 GO**다.

실패 evidence: FAILED_GRAPH_ONLY/비영 exit 또는 내부 terminal 부재, CALLBACK 누락/중복, schema·registry·스레드·scheduler·output mismatch·ROS bridge 활성·zero gate 실패에 대한 reason/traceback/terminal. external exit0만 있어도 내부 PASS가 없으면 FAIL이다. paused 계산 불가능이면 해당 실제 예외를 그대로 기록하고 종료한다. 재시도·튜닝·물리 전환은 승인되지 않는다.

## 남은 blocker — 최대 3개

1. 실제 paused Kit에서 새 typed witness/ONDEMAND 경로는 **NOT_RUN/UNKNOWN**이다. 위 단일 시험이 이를 확인한다. 오프라인18 PASS는 live PASS가 아니다.
2. 독립 native/script/direct actuator writer 배제, 실제 physics step 동기화·StoppingAdapter phase, observer·물리 pause/stop 및 stalled Kit 강제정지 보장은 **UNKNOWN**이다. active graph inventory와 probe-owned zero count를 전역 배제 인증으로 확대하지 않는다.
3. 수치·sign·dynamics·actual HOLD와 physical launch는 미승인이다. **physical NO-GO**, ENG001/QUAL12/432 진입 금지와 기존 실패/연구 denominator를 유지한다.
