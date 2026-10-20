# Full E2E v02 — 실제 paused preflight 후속 host wiring, 2026-10-20

판정: **host wiring 증분 구현, 물리 GO는 NO-GO. 실제로 작동이 검증된 전체 physical runner 완성은 FAIL/미달**이다. 단순 schema 추가로 끝내지 않고 Ackermann execOut witness 설치, 실제 StoppingAdapter→단일 owner dispatch, tensor/COM/FD/contact/clearance acquisition, Kit thread pause 전달 코드를 추가했다. 그러나 이번에 허용된 검사는 오프라인뿐이며, 새 witness의 live 실행과 native writer 배제 인증이 없다. 새 코드를 실물 검증 완료로 표현하지 않는다.

이번 작업의 Isaac launch/physics.play/ROS 발행/actuator 명령/물리 episode/ENG001/QUAL12/432/자동 retry는 모두 0이다. 기존 실제 stopping validation은 참고 증거이며 새 HOLD의 실측으로 재사용하지 않았다. 연구 denominator는 0으로 유지한다.

## 실제 최초 결과의 의미

우선 읽은 실제 디렉터리: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v01`.

- `status.json`: PREPARED, attempts=0. `execution_complete.json`은 존재하지 않는다. 따라서 정상 완료나 물리 성공으로 판정할 수 없다.
- `host_installation.json`: subscriptions_installed=true, pause_readback=true, physics_played=false, graph_barrier_certified=false, foreign_writers_excluded=false, metrics NOT_ACQUIRED_NO_PHYSICS, host_bound PARTIAL.
- `events.jsonl`은 PAUSE_READBACK 1행이며 success=false와 의도적인 failure-terminal 문구를 담는다. 이 행은 실제 pause 예외를 뜻하지 않는다.
- 실제 `stage_inventory.json`은 graph node 20개, articulation writer 3개 inactive를 기록한다. ROS subscriber, Ackermann, tick 등은 active다. `derived_hold.usda`는 기존 bench subtree reference 및 새 floor를 갖고, `hold_writer_override.usda`는 정확한 세 writer만 비활성화한다. 파일 생성을 물리 quiet/전체 writer 배제 인증으로 확대하지 않는다.
- 실제 manifest의 원본 입력 7개 SHA를 현재 파일과 재검사하여 **7/7 PASS**. 분석과 소스 hash는 [actual_preflight_analysis.json](fe2e_v02_hold_live_followup_20261020_v01/actual_preflight_analysis.json)에 기록했다.

`TimelinePause.__call__`은 `timeline.pause()`를 호출하고 `is_playing()`이 false이면 delivered를 set한 뒤 **literal `success=False`**를 쓴다. 실제 API 반환값을 그 필드에 쓴 것이 아니다. 따라서 pause_readback=true와 event success=false는 호출 실패의 상충 증거가 아니라, readback과 의도적 NO-GO 종료를 한 성공 필드로 혼동한 기록이다. 원본 결과/소스는 수정하지 않았다.

설치된 `omni.timeline/_timeline.pyi`의 signature는 `pause() -> None`, `is_playing() -> bool`이다. **최초 호출의 실제 반환값은 기록되지 않아 UNKNOWN**이다. None이 반환되었을 것이라고 소급 확정하지 않는다. `not is_playing()`은 실제 물리 정지나 stopped/paused 구분을 보장하지 않는다.

약 11.54초 종료는 사용자 제공 실제 관측이다. 해당 디렉터리에 elapsed/exit 로그가 없어 시간·exit code는 독립 재검증하지 못했다. 설치된 `SimulationApp.close()`는 `shutdown_and_release_framework()`를 호출하며, 기존 runner는 close 뒤에 terminal을 저장한다. terminal 미기록을 설명할 수 있는 소스상의 위험이지만 최초 종료 원인으로 확정하지 않는다. 새 runner는 **close 전에 terminal을 저장**하고 shutdown completion은 외부 exit 관측 전 UNKNOWN으로 남긴다.

## 추가 코드와 구체적 host 연결

기존 v01 host, v02 CLI, 모든 derived layer와 source controller/drive/protocol은 보존했다. 새 파일은 다음 4개다.

| 파일 | 구현한 연결 |
|---|---|
| `evaluation/fe2e_v02_hold_host_ports_v02.py` | CompletionBarrier/AckermannPort, PhaseDispatch, batched_writer, LiveObserver, PausePort |
| `scripts/fe2e_v02_hold_host_binding_v02.py` | 실제 API 설치와 EpisodeHost frame/bind/fail 경로, 새 journal 및 진입 gate |
| `scripts/fe2e_v02_hold_one_shot_v03.py` | 새 versioned CLI. 기존 CLI 보존 |
| `analysis/test_fe2e_v02_hold_host_followup_v02.py` | 새 경로의 fault injection/phase/target/COM/pause 검사 |

**Ackermann 완료 witness.** 설치된 `OgnAckermannController.compute`는 출력 계산 성공 후 `db.outputs.execOut=og.ExecutionAttributeState.ENABLED`를 설정하고 True를 반환한다. exception 경로는 False를 반환한다. 새 derived override에서 `/World/ENG_FE2E/Rover/ActionGraph/HoldAckermannWitnessV02`를 `omni.graph.scriptnode.ScriptNode` v2로 만들고, 그 `inputs:execIn`을 정확히 `/World/ENG_FE2E/Rover/ActionGraph/ackermann_controller.outputs:execOut`에 연결한다. ScriptNode compute가 process-local registry의 `CompletionBarrier.witness()`를 호출한다. wall time·cached execOut 값·physics callback 개수만으로 graph 완료를 인증하지 않는다.

새 engineering host 명령 경로는 원래의 ROS/tick 자동 평가와 경합하지 않도록 **새 override에서만** Ackermann 외 기존 graph 자식들을 inactive로 만들고 graph를 ONDEMAND로 바꾼다. Ackermann의 execIn/speed/steeringAngle/dt upstream 연결을 끊고 host가 명시 입력을 넣는다. 기존 graph의 `speed=15*wire_v`, `steeringAngle=degrees(atan2(-.7*wire_z,abs(wire_v)))`를 그대로 계산한다. Ackermann node의 radii, invertSteering, limits, wheelBase/trackWidth 및 원본 controller/drive gain은 바꾸지 않는다. 이는 기존 전체 graph를 그대로 실행했다고 주장하는 방식이 아니라, 기존 command 수학을 명시적으로 옮긴 새 derived ingress다. 실제 ROS publish는 없다.

Host는 실제 physics receipt 이후의 `(receipt_count, timeline_time)`을 고정하고 command마다 고유 token을 arm한다. `node.request_compute()` → `og.Controller.evaluate_sync(GRAPH)` → execOut witness 1회 → 동일 frame 확인 → native output read 순서다. 누락/중복/unsolicited/wrong-thread/평가 중 physics 진행은 FAIL이며 해당 barrier는 terminal poison 상태다. `evaluate_sync` 반환만으로 node 성공을 선언하지 않는다. ScriptNode extension/attribute/connection/scheduler가 live에서 동작하지 않거나 witness가 graph worker thread로 전달되면 **FAIL**하며 epoch를 임의 설정해 우회하지 않는다. 새 경로는 이번에 live exercise하지 않았으므로 실제 completion 보장은 UNKNOWN이다.

**Stopping phase와 latch.** 이전 `fe2e_v02_stopping_validation_ros_v01.py`의 실제 `StoppingAdapter`, drive contract, source .07/KMAX/PRE_FINAL/6초 normal stop profile을 연결했다. 새 `PhaseDispatch`가 관측 feedback으로 adapter를 갱신하고 실제 state MOVING→APPROACH, BRAKING→DECEL, ZERO_SETTLING→HOLD로 dispatch한다. 20Hz에 가까운 sim-time update 간격을 유지하며 그 사이에도 매 step graph command를 계산한다. 승인된 별도 profile 외 controller/threshold를 바꾸는 범용 조정 기능은 없다.

최초 ZERO_SETTLING epoch에서는 graph zero나 actuator write보다 앞서 그 epoch의 wheel6 q/dq, steer4, base pose를 검증·기록하고 기존 `JointOwnerMux.enter_hold`가 immutable latch를 만든다. HOLD 이후 graph 계산/command 전달을 하지 않는다. 정상 감속을 zero publish로 우회하지 않는다. sample epoch/freshness/단위/unwrap 검사와 외부 observer guard가 쓰기 전 적용된다. 오프라인 전환 검사는 실제 adapter/mux 객체를 사용했지만 plant 응답은 합성이므로 감속·HOLD 안정성 증거가 아니다.

`batched_writer`는 현재 `isaacsim.core.prims.Articulation` view에 맞는 **(1,6) velocity, (1,4) position** 배열과 이름으로 구한 disjoint joint_indices로 `set_joint_velocity_targets`/`set_joint_position_targets`를 호출한다. SingleArticulation용 action shape를 그대로 쓰지 않는다. `_physics_view.get_dof_velocity_targets/get_dof_position_targets`로 target readback을 확인하고 다음 dispatch 직전 외부 변경을 검출하면 fail-closed다. 두 API 쓰기가 atomic transaction이라는 보장은 없으며 도중 오류는 episode terminal/pause 요청이다.

세 legacy writer 비활성화·추가 active articulation/script node 검출·target readback은 구현했으나, **native/direct writer 전체 부재를 인증하지는 못한다.** 같은 값을 쓰거나 값을 바꿨다 복구하는 writer는 target equality로 배제할 수 없다. `EpisodeHost.attest`는 이 점을 UNKNOWN으로 거부한다. native exclusion을 True로 허위 발급하거나 기존 integration을 offline=True로 실행하지 않았다.

**실제 observer API.** `LiveObserver`는 initialized articulation의 DOF/body mapping과 base_link body index를 검사하고 다음을 acquire/기록한다.

- `get_root_transforms/get_root_velocities/get_coms`, joint positions/velocities. PhysX xyzw를 회전행렬로 바꿔 `v_origin=v_COM−omega×R*r_COM`를 계산하고 raw COM velocity를 별도 보존한다. 실제 tensor root pose와 USD world pose/yaw 불일치는 fail-closed다.
- 서로 다른 실제 sim time의 base origin FD, 원래 native USD velocity, wheel surface speed. FD baseline이 없는 최초 sample에서는 command를 내보내지 않는다.
- 새 override에 contact report threshold 0을 설정하고 `get_physx_simulation_interface().subscribe_contact_report_events`에서 실제 collider path/point count를 저장한다. decoding 오류는 guard failure다. floor/self 외 contact 및 외부 collider는 거부한다. 비어 있는 header 목록을 실측 접촉 인증 완료로 소급 표시하지 않는다.
- 매 acquisition의 whole-rover USD world AABB와 유한 floor edge ±100m 간 거리. 허용 외부 collider는 floor뿐이다. 이는 비어 있는 calibration floor 경계 여유이고 ENG001 corridor/obstacle/footprint 인증이 아니다.
- 별도 `IndependentGuard.observe`와 wall watchdog에 planar/FD/clearance/radius/contact를 전달한다. safety/evaluation GT는 명시 label을 갖고 perception/pose estimator/controller goal로 전달하지 않는다.

LiveObserver의 API 호출 코드는 연결했지만 **실제 물리 metric은 이번에 하나도 취득하지 않았다.** NOT_ACQUIRED_NO_PHYSICS 출력과 live 획득 시에만 쓰는 ACQUIRED_LIVE를 구분한다. 실제 contact stream health/COM frame/USD sync/clearance 유효성은 live 미검증이다.

**독립 pause.** `PausePort`는 wall thread에서 request ID/reason/thread/monotonic time만 queue에 넣는다. Kit post-update subscription 또는 명시 host pump가 installing Kit thread에서 `timeline.pause()`와 is_playing/is_stopped readback을 수행한다. 실제 API 반환 repr/type, call_ok, readback, delivery_ok, failure_terminal, physical_stop_verified=false를 따로 기록한다. 정상 paused installation probe는 failure=false이며 watchdog을 arm하지 않는다. physics heartbeat가 없는 preflight 자체를 wall timeout 실패로 오판하지 않는다. watchdog은 episode bind 후에만 arm한다.

Kit이 stall되면 queue가 소비되지 않을 수 있다. wall thread가 요청했다고 delivery/정지가 성공한 것으로 기록하지 않는다. GIL stall/Kit hang/네이티브 hang에서 강제 정지 보장은 **UNKNOWN**이며 독립 강제 정지 수단을 구현했다고 주장하지 않는다.

## 검증 및 보존

- 신규 검사 **16/16 PASS**. 신규 14개 최초 로그와 최종 16개 로그 모두 보존했다. 최종 전체 회귀 **57/57 PASS**: 기존 HOLD33 + stopping8 + 신규16. [최종 로그](fe2e_v02_hold_live_followup_20261020_v01/regression_tests_verified.txt).
- 검증에는 실제 StoppingAdapter의 MOVING/BRAKING/ZERO_SETTLING 전환→immutable latch→HOLD에서 graph 차단, native batched target shape/변조 거부, COM 회전 보정, witness 누락·중복·진행 오류, worker→Kit pause 전달, API 예외/readback 실패, stalled queue UNKNOWN, contract 차단, output 재사용 거부와 terminal pre-shutdown 저장이 포함된다. 새 API 설치·물리 plant는 검증 범위 밖이다.
- 새 4개 Python 파일 py_compile PASS. scientific package 설치/갱신 없음.
- 실제 CLI `offline-preflight` exit0, 실제 CLI `one-shot` **예상된 exit1/FAILED_NO_GO**, physics_episodes=0/actuator_commands=0/retry=0을 기록했다. 이 실패를 성공 episode나 denominator에서 사라진 run으로 바꾸지 않았다. [차단 결과](fe2e_v02_hold_live_followup_20261020_v01/physical_entry_blocked/status.json). 후속 소스 수정 전 CLI manifest와 최종 source hash는 구분해 보존한다.
- 기존 inventory **148/148 SHA PASS, FAIL0**. 작업 전후 각각 `preservation_before.json`/`preservation_after.json`; 최초 live preflight 산출물 및 기존 HOLD 코드/contract 14개 작업 전후 hash도 모두 PASS다. expected를 observed로 교체하지 않았다.
- known protocol lock subset 도구 exit0/PASS. full_experiment_ready=false이며 전체 USD closure/live pairing/432 readiness 인증으로 확대하지 않는다. 기존 원본/weights/locked manifests/v01-v03 결과/실제 실패 기록을 수정하지 않았다.
- 이 starter에는 `.git`이 없어 git diff/status 검증은 불가능했다. 변경 파일은 filesystem hash로 확인하며 Git remotes/staging/push는 수행하지 않았다.

## 진입 gate와 남은 blocker 3개

| Gate | 실제 보장 / 아직 미보장 |
|---|---|
| command | one-shot launch 전 차단, 원본 수치 불변. K=1s⁻¹/±.020rad/s/.2rad/s²/.004m 및 sign은 PROPOSED/UNAPPROVED. contract bool 변경 없음 |
| owner | 새 코드의 이름별 단일 mux/세 legacy writer 차단/target 변조 검출. native/direct writer 전체 부재는 UNKNOWN이므로 dispatch 거부 |
| metric | 실제 API acquisition 구현. 이번 취득0, quiet/contact/physical stability 모두 UNKNOWN |
| episode/output | 미사용 output 강제, 명령·입력SHA·환경·오류·retry0·terminal revision 기록. paused 성공 scope와 물리 GO 분리. shutdown 완료는 외부 exit 관측 전 UNKNOWN |

1. **새 graph/observer live 동작 미검증.** 다음 paused 1회는 설치/API/connection/readback만 확인한다. physics0이므로 same-frame completion이나 실제 observer를 인증할 수 없다. 이후에도 별도 승인 없이 물리 검증으로 자동 이어가지 않는다.
2. **writer 배제 및 stalled Kit 정지 인증 부재.** target 변조 검출은 native 배제 증명이 아니며 queue pause는 Kit hang을 강제 중단하지 못한다. 인증 UNKNOWN일 때 physical gate를 유지한다.
3. **numeric/sign/dynamics·단일 physical episode 승인 미확보.** runtime/signed policy/dynamics 모두 false. 새 CLI는 지금도 launch 전에 거부되며, fully executable physical session의 승인/초기화/종료 lifecycle까지 완료했다고 주장하지 않는다.

## 다음 단 1회 명령 — 이번에 실행하지 않음

다음 단계는 **별도 수동 승인 후 paused live preflight 1회만**이다. physics.play/graph 계산/ROS publish/actuator 명령은 없다. 아래 v02 output은 이번 read-only 확인 시 미존재였고 실행 시에도 exclusive mkdir로 재검사한다. domain192의 현재 ROS 격리는 UNKNOWN이며 publisher는 설치하지 않는다.

```bash
ROS_DOMAIN_ID=192 /home/user/anaconda3/envs/hh_isaac51/bin/python /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/fe2e_v02_hold_one_shot_v03.py --mode live-preflight --approve-paused-launch --domain 192 --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v02
```

확인 대상은 새 on-demand graph/execOut→ScriptNode 연결의 설치, 구독 보관, worker queue→Kit pause API 반환/readback 기록, physics receipt0, terminal 사전 저장이다. 결과는 PAUSED_INSTALLATION_RECORDED_NO_GO 또는 FAILED_NO_GO이고, Ackermann 계산 exercise와 metric 획득은 NOT_RUN이다. 종료한 process의 exit code는 외부 실행자가 따로 기록해야 한다.

물리 episode용 별도 CLI 형식은 아래와 같다. **현재 실행 가능한 승인된 물리 명령이 아니다. 반드시 launch 전에 FAILED_NO_GO/exit1로 차단된다. 이번 또는 다음 paused preflight 뒤에 자동 실행하지 않는다.**

```bash
ROS_DOMAIN_ID=192 /home/user/anaconda3/envs/hh_isaac51/bin/python /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/fe2e_v02_hold_one_shot_v03.py --mode one-shot --domain 192 --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_PHYSICAL_20261020_v02
```

물리 GO/NO-GO: **NO-GO**. 실측 preflight의 부분 성공은 인정하되, 새 host wiring과 offline PASS를 live HOLD/quiet/배타 writer 보장으로 치환하지 않는다.
