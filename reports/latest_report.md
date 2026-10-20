# Full E2E v02 exec edge 실패 수정 — 2026-10-20

**오프라인 표적 수정 PASS / 실제 수정 연결 UNKNOWN / physical NO-GO.** 상태는 READY_FOR_MANUAL_APPROVAL이다. 이번 Isaac/SimulationApp launch·graph live evaluation·physics.play·ROS publish·actuator command·motion·ENG001·QUAL12·432-run·retry/sweep는 모두 0이다. 연구 denominator=0, numerics/sign/dynamics/runtime approval=false를 유지한다.

## 실제 실패 근거와 보존

원본 `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v01`의 status.json, execution_complete.json, events.jsonl, graph_only.usda, manifest.json과 `.external_v01`의 external_exit.json, terminal.txt, command.json을 직접 읽었다. 기존 준비 보고서와 host v03/CLI v04/wrapper v01/evaluation probe v01도 읽었다.

- 내부 FAILED_GRAPH_ONLY. graph_evaluations=ack_compute_count=witness_invocation_count=0. physics_callbacks=actuator_writes=ros_publishes=retry=research_denominator=0.
- events의 chained traceback: `Parsed source 'ackermann_controller.outputs:execOut' as a path attribute, which cannot connect to a destination of type uint (execution)`. 바깥 예외는 `Failed to connect ... -> /World/ENG_FE2E/Rover/ActionGraph/GraphOnlyWitnessV03.inputs:execIn`이다.
- 외부 child process exit=0, elapsed=14.303175623062998s와 내부 FAIL은 서로 다른 관측이다. Kit shutdown이 Python 반환을 앞설 수 있다는 기존 코드 설명은 있으나 exit0 발생의 내부 shutdown 원인 자체는 이번에 확정하지 않았다.
- 같은 output 재사용은 기존 wrapper의 FileExistsError 선행 gate로 child launch 전에 차단된다. 기존 재실행 terminal의 별도 산출물은 제공 경로에 없으므로 그 시도의 독립 로그/hash는 UNKNOWN이다. 새 회귀검사로 선행 차단을 확인했다.
- [검증 JSON](fe2e_v02_graph_edge_fix_20261020_v01/v01_verification.json): v01 manifest 입력 33/33 SHA, status의 3 output SHA, execution_complete와 status equality PASS.
- [보존 검사](fe2e_v02_graph_edge_fix_20261020_v01/preservation_after.json): 기존 준비 baseline 172개(기존 148개 포함) + 이번 실패 output/sidecar 8개 + 기존 runner/CLI/wrapper 3개 = **183/183 SHA PASS**. 원본·기존 결과·expected SHA 변경/삭제/재사용 없음. 새 baseline의 실패 산출물 SHA는 작업 전 관측값이며 독립 사전 expected라고 주장하지 않는다.

## 확인된 원인과 미확인 가설

실제 설치 루트는 `/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim`이다. 파일별 절대경로/SHA는 [설치 소스 inventory](fe2e_v02_graph_edge_fix_20261020_v01/installed_source_hashes.json)에 있다. 패키지는 import하지 않고 텍스트/AST로 확인했다.

| 근거 | 확인 내용 |
|---|---|
| `extscache/omni.graph-1.141.2+69cbf6ad.lx64.r.cp311/omni/graph/core/_impl/controller.py:429–438, 440–463, 671–694` | edit의 상대 이름은 path_to_object_map에 있는 생성 노드만 매핑한다. 기존 Ackermann은 CREATE_NODES에 없어 이름이 그대로 남는다. 새 Witness는 절대경로로 매핑된다. CONNECT는 이 결과를 connect에 넘긴다. |
| 같은 패키지 `graph_controller.py:836–895` | source가 string으로 decode되고 destination이 실행 attribute이면 PATH role 조건에 걸려 바로 예외가 난다. 실제 traceback의 내부 메시지/줄번호와 일치한다. |
| `omni.graph.scriptnode-1.50.0+107.3.0/.../OgnScriptNode.ogn`, `OgnScriptNodeDatabase.py:61–75, 206 이후, 324–328` | 등록명 `omni.graph.scriptnode.ScriptNode`, node version2. inputs:execIn/outputs:execOut은 execution이며 role EXECUTION. script는 string, usePath는 bool이다. |
| `exts/isaacsim.robot.wheeled_robots/.../OgnAckermannControllerDatabase.py:69–91` | Ackermann execIn/execOut은 execution, execOut role EXECUTION이다. |

**확정한 직접 원인:** 기존 source 상대 이름의 edit 매핑 누락 → 실제 OG attribute 대신 path 문자열로 연결 API에 전달됨. 이는 단순 포트 타입 불일치 가설보다 구체적인 실제 실패 지점이다. 설치된 순수 매핑 함수만 AST로 분리 실행한 회귀검사에서도 재현된다. legacy/OG 모듈 import나 graph 실행은 하지 않았다.

USD `custom`은 authored attribute 여부이지 OG 실행 role 인증이 아니다. USD에 이름과 uint 또는 token 속성을 만들었다고 등록 node schema/실행 포트가 생성됐다고 판단할 수 없다. terminal의 **기존 inactive HoldAckermannWitnessV02** `token` 대 `uint` 경고는 별도 관측이다. 이번 실패 destination GraphOnlyWitnessV03은 traceback에서 이미 uint(execution)으로 해석됐다. 이 경고를 해당 edge의 직접 원인으로 바꾸어 설명하지 않는다.

기존 v01은 연결 전 실제 source OG node type/port validity, evaluator/pipeline mode, destination node parent 등의 snapshot을 남기지 않았다. 따라서 source의 실제 live 포트 존재/type, graph parent/runtime hydration 정상 여부는 **UNKNOWN**이다. 생성 순서·graph mode 문제와 추가 runtime 문제 가능성은 미확인 가설이다. 기존 코드는 connect 실패 뒤에 ONDEMAND를 설정하려 했으므로 v01의 실패 순간 ONDEMAND라고 주장하지 않는다. 이번 수리는 확인된 이름 해석 문제를 제거하지만 live 성공의 증거는 아니다.

## 최소 버전 수정

기존 파일은 보존하고 다음 파일만 새 버전으로 만들었다.

- `scripts/fe2e_v02_hold_host_binding_v04.py`, `scripts/fe2e_v02_hold_one_shot_v05.py`: ScriptNode 등록 생성 → ONDEMAND 설정 → 양쪽 절대경로의 실제 OG Attribute 조회 → native connect 순서. 기존 single evaluation/compute 계수·witness 검증 로직 유지. manifest에 새 helper/wrapper/CLI hash 포함, approval 네 항목 false 명시.
- `evaluation/fe2e_v02_graph_edge_v01.py`: 연결 직전에 양쪽 실제 node type/validity, attribute absolute path/OG existence/resolved type/port type, actual graph path, USD type/custom, graph evaluator/pipeline mode, 생성 순서를 events에 기록한다. 실행 role/parent 검사 후 `og.Controller.connect(source_attribute, destination_attribute)`를 호출하고 native upstream readback을 검사한다. 실패 시 traceback과 chained API detail·수집된 evidence를 남기며 재시도하지 않는다.
- `scripts/fe2e_v02_graph_probe_external_v02.py`: child exit는 external_exit.json에 그대로 보존. 최종 internal status 읽기 실패/malformed/missing도 실패로 처리하며 `final_adjudication.json`에 child_exit/internal_status/wrapper_exit/overall_success를 별도 기록. child0 + internal FAILED_GRAPH_ONLY이면 wrapper1/overall_success=false. 기존 v01도 반환식 자체는 internal PASS를 요구했지만 sidecar에는 최종 판정이 없었다는 차이를 명확히 한다.
- `analysis/test_fe2e_v02_graph_edge_fix_v01.py`: 실제 설치 매핑 동작 및 wrapper의 해당 실패 조합/child nonzero/PASS/중복 output 차단 회귀검사.

Controller compute와 witness 함수를 직접 불러 연결을 우회하지 않는다. 기존 등록 compute를 감싸 호출수를 계측하는 방식과 ScriptNode의 실제 exec 신호 전달을 그대로 유지한다. 연결 readback만으로 PASS를 발행하지 않는다. 최종 PASS는 graph_evaluations=ack_compute_count=witness_invocation_count=1, token/epoch/thread 일치, witness 내부 출력 shape/finite/expected matching, ONDEMAND·active allowlist·paused gate, physics/actuator/ROS=0을 모두 요구한다. foreign/native writer 전역 배제는 여전히 UNKNOWN이다.

## 오프라인 검사

- 신규6 + 기존 graph probe18 = **24/24 PASS**, [최종 로그](fe2e_v02_graph_edge_fix_20261020_v01/tests_final_after_metadata.txt).
- 새 Python 5파일 py_compile PASS. 설치 모듈/legacy 모듈은 실행하지 않았다.
- 최초 검사 24개 중 annotation context 누락으로 1 ERROR가 있었다. 테스트 추출 함수의 타입 annotation 환경을 보완했으며 [최초 실패 로그](fe2e_v02_graph_edge_fix_20261020_v01/tests.txt), [수정 후 로그](fe2e_v02_graph_edge_fix_20261020_v01/tests_final.txt)를 보존했다. 연구 실행 실패로 합치거나 숨기지 않는다.
- 기존148을 포함한183 SHA 및 실제 실패 manifest33 SHA PASS. 과학 패키지 설치/업그레이드 없음.

## 다음 v02 단 한 번 명령 — 준비만, 실행 금지

작업 시점에 다음 output 및 `.external_v02` sidecar 모두 미존재임을 확인했다. 디렉터리를 미리 만들지 않았다. 별도 명시적 수동 승인 이후에만 아래 한 명령을 실행한다. 사용 전 path 충돌/원본 hash를 다시 확인하며 충돌 시 재사용하지 않는다.

```bash
ROS_DOMAIN_ID=193 /home/user/anaconda3/envs/hh_isaac51/bin/python /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/fe2e_v02_graph_probe_external_v02.py --domain 193 --approve-graph-only-launch --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v02
```

sidecar: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v02.external_v02`. 실패하더라도 자동 retry/sweep는 없다. 이 명령은 graph-only engineering 증거이며 물리 실행 승인이나 Full E2E 관측 대체가 아니다.

## NO-GO / 남은 blockers

1. 수정된 native edge와 정확히1회 실제 graph/witness/output 동작은 live 미검증. 다음 최소 검사는 위 graph-only 1회뿐이다.
2. 실제 physics-thread ownership/foreign native writer 배제·stalled engine 정지 및 stopping/hold 물리 envelope 인증은 미완료다.
3. numerics/sign/dynamics/runtime approval=false. ENG001/QUAL12/432와 physical 실행은 계속 NO-GO다.
