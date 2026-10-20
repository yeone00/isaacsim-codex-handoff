# Full E2E v02 HOLD host binding — 2026-10-20

**NO-GO. Host-bound PARTIAL / 물리 owner dispatch FAIL(미완성).** 실제 Isaac API 설치 코드와 별도 paused preflight 진입점은 작성했다. 요청한 실행 가능한 곡률→DECEL→HOLD 전체 runner 완료 기준은 충족하지 못했다. Mock PASS를 실제 독점성·물리 안정성 승인으로 해석하지 않는다. Isaac launch, physics episode, ROS publish, actuator command, ENG001/QUAL12/432, retry/sweep는 이번 작업에서 모두 0이다.

## 생성 파일과 실제 연결

- `scripts/fe2e_v02_hold_host_binding_v01.py`: 새 단일 host entrypoint `main()` → 승인된 경우에만 `install_paused()` → `SimulationApp`. 기존 session과 같은 bench subtree reference, 초기 transform, 200m floor, PhysicsScene reference를 사용한다. 원본 session은 top-level에서 launch하므로 import하지 않았다.
- `scripts/fe2e_v02_hold_one_shot_v02.py`: 새 CLI가 위 host `main`을 직접 호출한다. frozen v01 CLI는 보존했다.
- `analysis/test_fe2e_v02_hold_host_binding_v01.py`: launch 없는 6개 회귀검사.

실제 import는 기존 `evaluation.fe2e_v02_hold_runtime_integration_v01.patch`, `GraphReader`, `acquire`, `IndependentGuard`, 기존 owner의 `make_articulation_writer`이다. patch는 live composed stage의 정확한 세 writer jointNames/upstream을 검사하고 별도 `hold_writer_override.usda` edit target에서만 비활성화한다. 다른 articulation writer 발견 시 거부한다. native/script direct writer 부재를 이 검사만으로 선언하지 않는다.

`IsaacCallbacks`는 `omni.physx.get_physx_interface().subscribe_physics_step_events`와 `omni.kit.app.get_app().get_post_update_event_stream().create_subscription_to_pop`에 실제 메서드를 등록하고 subscription 수명을 보관한다. `TimelinePause`는 실제 timeline.pause 및 is_playing readback을 수행한다. `IndependentGuard.start()`로 physics callback과 독립인 wall thread를 설치한다. pause exception/readback 실패를 FAILED event로 기록하며 성공으로 취급하지 않는다. 단, stalled Kit에서 thread-safe pause 전달을 보증하는 native 독립 경로는 인증하지 못했다.

명시 DOF 이름의 native rad/s·rad writer와 graph reader는 binding 메서드에 연결했다. surface→wire scale·controller·threshold·drive 수정은 없다. snapshot은 q/dq/steer/base 획득 receipt를 기록하지만, 실제 graph-completion witness가 없는 상태에서는 수집/dispatch를 거부한다. app post-update와 PhysX step을 같은 graph epoch라고 추정하지 않는다. `graph_epoch`를 실제 완료 신호로 갱신하는 연결은 **미구현**이다. 기존 `PhysicsIntegration`의 runtime seal을 offline=True로 우회하지 않았다. 따라서 실제 ZERO_SETTLING latch/APPROACH dispatch/독립 raw COM→origin·FD·contact·clearance observer와 StoppingAdapter phase 연결은 **미완료**다. 필드 schema를 물리 계측 결과로 제출하지 않았다.

## 발견된 런타임과 로컬 근거

- Launcher: `/home/user/anaconda3/envs/hh_isaac51/bin/python`.
- 설치 metadata: `/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim-5.1.0.0.dist-info/METADATA`, Name isaacsim / Version **5.1.0.0**. 새 런타임 설치 없음.
- 기존 supervisor: `scripts/run_fe2e_v02_stopping_validation_v01.py`; 실제 entrypoint `scripts/fe2e_v02_stopping_validation_session_v01.py`, `from isaacsim import SimulationApp`.
- Bench: `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`, SHA256 `224cac492d267d0403c9402484fcf84011191208fb4689e7e3fc33eadf3756fe`.
- Reference subtree `/World/ROBOT_TASK/RuntimeRover` → `/World/ENG_FE2E/Rover`. 저층 robot reference `/home/user/hh/isaac_cosmos/assets/assets/robot/rover_camera_add_51_test.usd`, SHA256 `2102cc1fce5f8f626a9c113dab16da5634687b8a693a51cdfe7e1eec1ad0a3f8` 재검사 PASS.
- 실제 graph `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01/graph.json`을 읽었고 기존 inventory SHA와 재대조했다. 추가 source/hash는 evidence `inputs.json`.
- 설치 SimulationContext 소스의 subscribe_physics_step_events 사용을 정적으로 확인했다. 최초 omni.graph.core glob 검색은 경로 부재 오류였으며 graph-completion API 확인 성공으로 간주하지 않는다. USD는 이번에 simulator나 pxr로 새로 열지 않았다. 기존 snapshot을 읽었으며 live composition patch 적용 여부 UNKNOWN이다.

## 검사 및 보존

`python3 -m unittest tests.test_fe2e_v02_wheel_hold_v01 analysis.test_fe2e_v02_hold_runtime_integration_v01 analysis.test_fe2e_v02_hold_host_binding_v01 -v`: **33/33 PASS**. 테스트 로그 `reports/fe2e_v02_hold_host_binding_20261020_v01/tests.txt`. 새 검사는 import 무실행, pause 예외/readback 실패, one-shot launch 전 거부·output 재사용 금지, barrier 누락, 무승인 launch 거부를 확인한다.

기존 inventory의 과거 PROJECT_STATE 항목만 제외한 **148개 SHA PASS, FAIL 0**: `preservation.json`. `python3 scripts/verify_known_locks.py --out reports/fe2e_v02_hold_host_binding_20261020_v01/known_locks.json` exit0 / known subset PASS, full_experiment_ready=false. 해당 도구 범위는 known hash/count이며 전체 pairing 재검사 PASS로 확대하지 않는다. 원본 protocol/USD/controller/adapter/owner/integration/기존 CLI/결과/hash inventory는 변경하지 않았다. 기존 v01/v02/v03 outputs 보존. PROJECT_STATE append만 수행했다.

Journal은 입력 SHA·명령·domain·환경·event·terminal status·retry0·연구denominator0을 기록한다. exclusive output creation으로 재사용을 거부한다. one-shot은 아직 episode를 수행하지 않고 FAILED_NO_GO/exit1로 종료한다. 실제 per-step 물리 metric 계산·terminal 성공 판정은 **NOT_IMPLEMENTED**이며 runtime 설치 metadata와 구분한다.

## Blocker — 3개

1. **FAIL: scheduling/physical dispatch 미완성.** 실제 Ackermann execOut 완료 증거와 PhysX acquisition barrier, StoppingAdapter의 첫 ZERO_SETTLING 직전 latch 및 기존 owner 실행 연결, raw COM/FD/contact/clearance observer가 필요하다. 현재 one-shot은 물리 시험 runner로 사용할 수 없다.
2. **UNRESOLVED: native/direct writer와 독립 pause.** 전체 script/native writer 배제 증거가 없고 thread pause가 physics/Kit hang에서도 전달되는지 미검증이다. paused readback만으로 pause delivery 인증하지 않는다. runtime gate=false.
3. **UNAPPROVED: 수치·sign·실행 승인.** K=1s⁻¹, signed ±.020rad/s, slew .2rad/s², .004m 등 PROPOSED 유지. Wheel sign 계측·signed policy/dynamics 인증 및 별도 launch/단일 episode 승인이 없다. 숫자 승인 bool 변경으로 위 blocker를 우회할 수 없다.

## 다음 단일 live test 명령 — 실행하지 않음

다음 승인 가능한 최소 live test는 **physics를 play하지 않는 설치 preflight 1회**다. output/domain의 미사용 여부는 실제 실행 직전 별도로 확인해야 한다. 아래 domain192의 현재 격리는 UNKNOWN이다. 정확한 interpreter는 확인했으나 실제 API 설치의 시행 성공 여부는 NOT_RUN이다.

```bash
ROS_DOMAIN_ID=192 /home/user/anaconda3/envs/hh_isaac51/bin/python scripts/fe2e_v02_hold_one_shot_v02.py --mode live-preflight --approve-paused-launch --domain 192 --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v01
```

필요한 구체적 승인은 위 **paused SimulationApp launch 1회, 새 derived layer 작성, callback/watchdog/pause 설치·readback 후 종료**다. ROS bridge/publisher를 설치하지 않으며 physics play/actuator write는 하지 않는다. preflight 완료도 연구 성공이 아니므로 exit1/FAILED_NO_GO로 기록한다. 이번에는 이 승인 또는 실행을 추정하지 않았다.

향후 one-shot 별도 명령 형식(현재 의도적으로 launch 전에 거부, 실행 가능 승인된 물리 명령 아님):

```bash
ROS_DOMAIN_ID=192 /home/user/anaconda3/envs/hh_isaac51/bin/python scripts/fe2e_v02_hold_one_shot_v02.py --mode one-shot --domain 192 --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_HOLD_PHYSICAL_20261020_v01
```

**GO/NO-GO: 물리 HOLD NO-GO. 실제 host API에 대한 부분 구현은 있으나 요청된 전체 host runner 완성은 FAIL/UNRESOLVED다.** 다음 구현은 blocker1의 실제 graph completion witness와 phase/계측 연결이며, 독립 writer/pause 증거를 확보하기 전 physics 진입은 계속 거부해야 한다.
