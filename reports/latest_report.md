# Legacy supervised mobility 단일 실행 준비 — 2026-10-21 v01

이번 산출물은 새 단일 실행의 구체적 준비다. **기존 경로의 실행 CLI는 확인됐지만, 현재 소스 그대로는 요청된 live writer guard를 충족하지 않아 감독형 실행 승인 대상으로는 NOT_READY다.** 아래 두 보완을 끝내면 같은 ROS driver/graph를 사용하는 한 번의 실행으로 연결할 수 있다. 물리 실행·ROS node 생성·publish·retry는 이번 작업에서 0회다. 기존 STOP_HOLD 보고서는 수정하지 않았다.

## 확인한 실제 경로와 순서

원본 실제 출력(읽기 전용): `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01/attempt_0001`. 부모의 `runtime_command_attempt_0001.json`, `preexecution_plan_attempt_0001.json`, `drive_contract.json`, `graph.json`, `metrics.json`, 실제 attempt의 `joint_io.json`, `isolation_check.json`, `execution_complete.json` 및 두 실행 소스를 읽었다. 기존 303/429 inventory 재계산은 하지 않았다.

당시 launcher는 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, ROS_DOMAIN_ID=191, RMW_IMPLEMENTATION=rmw_fastrtps_cpp, ROS_DISTRO=jazzy였다. supervisor가 bridge jazzy/lib를 LD_LIBRARY_PATH에 추가했다. 빈 domain probe → Isaac 세션 → bridge enable → 파생 stage 구성 → observer → settling 180 tick → read-only articulation 초기화 → baseline 60 tick → TF/endpoint 격리 확인 → ROS driver → pulse_start → 정상 감속 → zero 관측 → pause/소유 child 종료 순서다. ROS child는 `/opt/ros/jazzy/setup.bash`를 source한 `/usr/bin/python3`이다. 따로 driver를 수동 실행하면 안 된다.

Stage는 bench `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`의 `/World/ROBOT_TASK/RuntimeRover`를 `/World/ENG_FE2E/Rover`로 reference한다. 원본 전체 stage를 play하는 경로가 아니다. PhysicsScene도 같은 bench에서 reference하고 별도 200×200m floor를 만든다. 재질은 default이며 원래 연구 바닥 traction 인증이 아니다.

Observed writer 경로: OnPlaybackTick → ROS2SubscribeTwist(`/rover/cmd_vel`) → linear x break/multiply15 및 angular compatibility encoding → AckermannController(radius .5, wheelBase .7, trackWidth .569) → 세 IsaacArticulationController → 현재 base_link. Ackermann 4 wheel target이 front/rear에, index0/1 복사가 middle에 연결되고 wheelAngles는 앞 steering에 연결된다. 물리 wheel radius .13300000131130219m, surface→wire scale .2506265639450088이다. 선형 wire를 SI base speed로 읽으면 안 된다.

Named DOF 순서는 `front_left_steer_joint, front_right_steer_joint, middle_left_wheel_joint, middle_right_wheel_joint, rear_left_steer_joint, rear_right_steer_joint, front_left_wheel_joint, front_right_wheel_joint, rear_left_wheel_joint, rear_right_wheel_joint`; wheel index=2,3,6,7,8,9다. 이는 실제 joint_io와 graph 기록 근거다. 이번 USD-only pxr 직접 열기는 해당 conda Python에 pxr가 없어 ModuleNotFoundError로 실패했다. 따라서 현재 composed USD topology 직접 재검증은 UNKNOWN이며 launch 전 gate에서 확인해야 한다. USD를 변경하거나 패키지를 설치하지 않았다.

## 실제 인자와 검토용 단일 CLI

AST로 확인: session은 `--output`(필수), `--domain`(필수 int)만 받고 ROS driver는 `--output`만 받는다. session은 argparse 뒤에 SimulationApp을 import하지만 ROS driver는 argparse보다 먼저 rclpy를 import하므로 무작정 --help를 실행하지 않았다. 기존 supervisor `run_fe2e_v02_stopping_validation_v01.py`는 출력이 과거 경로로 고정돼 있어 재실행 금지다.

새 경로: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_20261021_v01/attempt_0001`. 이번 검사에서 부모 자체가 존재하지 않는다. 아래는 **기존 두 스크립트를 재사용하는 정확한 route reproduction 명령**이다. 이번에는 실행하지 않았다. 아래 명령만으로 live guard 보완이 생기는 것은 아니므로 현재 실행 승인을 요청하지 않는다. 보완 후 이 명령의 session entry를 검증된 새 버전으로 바꿔 최종 승인해야 한다. 성공한 것처럼 미존재 wrapper 명령을 제시하지 않는다.

```bash
cd /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
(
  set -euo pipefail
  export ROS_DOMAIN_ID=191 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_DISTRO=jazzy
  export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}:/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim/exts/isaacsim.ros2.bridge/jazzy/lib"
  run_root=/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_20261021_v01
  mkdir "$run_root"
  cp --no-clobber /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01/drive_contract.json "$run_root/drive_contract.json"
  /bin/bash -c 'source /opt/ros/jazzy/setup.bash && exec /usr/bin/python3 scripts/full_e2e_ros_observer_v01.py --output "$1/domain_probe_attempt_0001" --probe-only' probe "$run_root" > "$run_root/domain_probe_stdout.log" 2>&1
  /home/user/anaconda3/envs/hh_isaac51/bin/python scripts/fe2e_v02_stopping_validation_session_v01.py --output "$run_root/attempt_0001" --domain 191 > "$run_root/runtime_attempt_0001_stdout.log" 2>&1
)
```

`mkdir` 충돌/실패 또는 probe 실패 시 종료하며 같은 경로를 다시 쓰지 않는다. contract 복사는 작은 provenance JSON만이며 signed 실행 승인이 아니다. 기존 contract의 approved는 drive 단위 계약이고 새 motion 허가가 아니다. 원본 session이 내부에서 `scripts/fe2e_v02_stopping_validation_ros_v01.py --output <attempt>`를 한 번 호출한다. 추가 ros2 topic pub, 별도 observer/driver, v07/OnImpulse/HOLD를 병행하지 않는다.

## 기존 한계·기록·평가

| 항목 | 소스에 실제 있는 값/동작 |
|---|---|
| source request | v=.07, k=KMAX≈.382784560616, PRE_FINAL; governor 단일 사용 |
| 주행 | driver에서 6 sim s 뒤 정상 감속; stale .5s/abort/20 wall s에 zero fault |
| 세션 상한 | pulse 루프 14.5 sim s 또는 20 wall s; 이후 480 tick≈8 sim s zero 관측 |
| 속도 | .03m/s에서 zero 요청; >.25m/s는 emergency pause, .03을 대체하는 허용치 아님 |
| 공간 | settled center로부터 >2m에 pause; footprint 1.68×1.61m, floor edge guard 여유는 >90m 요구 |
| 접촉 | floor만 외부 collider 허용; floor 접촉 정상, 예상 밖 collider/contact는 차단 대상으로 보완 필요 |
| zero | driver finally 20 zero; observer는 isolation 뒤 생성한 publisher로 zero_request 때 10 zero |
| 최종 quiet | 최소 연속 1 sim s, root/COM/FD 각 planar≤.002m/s 및 pose span≤.002m; 누락/시간 gap>.1s면 NOT_READY |

.03m/s zero 요청은 감속 보장이나 overshoot 없는 hard speed invariant가 아니다. app.update가 멈추면 wall watchdog과 pause 전달도 보장되지 않는다. 기존 session 마지막 60 samples 계산은 정확한 1초 coverage, COM/FD를 판정하지 않아 단독 success 근거로 사용할 수 없다. ±.03m/±2° 및 stable6는 연구 terminal 기준이며 이 demo에는 사전 FINAL/stable6가 없다. Full E2E success는 이 실행으로 판정하지 않는다.

기존 instrumentation은 `steps.jsonl`에 sim_s/wall_s/phase, q/dq 전체, graph wheel/steer target, pose, tensor root pose, raw COM velocity, COM→origin velocity, FD, native velocity를 기록한다. `adapter_commands.jsonl`은 source_step와 feedback/adapter state/wire를 기록하고 독립 observer의 `ros_observed.jsonl`은 수신 command/TF wall time을 기록한다. command와 physics는 비동기이므로 동일 frame 인과관계를 가정하지 않는다. graph target은 actuator target API readback과 다른 계층이다. contacts·joint_io·isolation·zero·completion도 보존한다.

이전 실제 active peak root=.022805331797m/s, FD=.021279668484m/s였지만 zero 뒤 후퇴34.127288744mm, 마지막 raw-root .002619135991m/s로 quiet FAIL이었다. 새 run에도 후퇴/반전은 첫 실제 zero source-step pose/yaw 축으로 signed along/left 및 최대 excursion을 기록한다. negative target나 HOLD를 추가하지 않는다. zero 발행, wheel dq=0, pose 고정 어느 하나만으로 정지 성공을 선언하지 않는다.

## 실행을 막는 정확한 두 보완과 최소 수정 위치

1. **현재 legacy 경로의 live writer admission이 빠져 있다.** session의 `good=...`는 시작 전 endpoint 수만 확인하고, 시작 후 publisher 변경·observer 사망·graph writer 변경을 차단하지 않는다. suffix wheel 선택도 named exact topology gate가 아니다. 최소 보완은 별도 버전 session에서 기존 stage가 attach된 뒤 play 전 composed graph 세 writer의 jointNames/targetPrim/velocity·position 연결과 enabled joint body0/body1를 보존 graph/expected names와 대조하고, articulation 초기화 후 named exact set/order를 확인하는 것이다. `tick()`에서 observer 상태 freshness≤.5s와 생존, 고정 TF/subscriber GID, 허용 publisher(observer zero와 v02_stopping_single_validation뿐)를 점검하여 외부 endpoint/변경/누락이면 abort_motion+zero_request를 기록하고 pause/NOT_READY로 끝내야 한다. driver 시작 전에는 무 publisher 또는 observer만, driver discovery 뒤에는 정확한 두 publisher를 요구하고 비영 command 전 driver 자신의 discovery gate를 두어 시작 경쟁을 막는다. 같은 domain의 임의 node도 거부한다. 이것은 관측 가능한 ROS/graph writer 경로의 제한적 gate이며 모든 native callback 부재 증명은 아니다. substantiation 실패 시 비영 명령 금지다. 원본 ROS driver는 로직을 유지한 새 버전에 이 discovery gate만 추가하며 session child 경로도 그 버전을 지목해야 한다.
2. **새 출력/종료 계측 연결이 없다.** 기존 supervisor의 상수 O를 새 버전에서 required `--output`으로 바꾸고 mkdir(exist_ok=False), immutable input hash 확인, parent drive_contract의 pinned hash 확인, argv/env/owned PID/exit/failure 기록을 추가한다. session의 현재 `stop_ok=`를 root+COM+FD의 실제 1초 coverage/finite/gap/span 판정으로 바꾸고 quiet 실패는 status=NOT_READY로 남긴다. 초기 baseline도 같은 세 속도 기준을 적용한다. `collision_preflight` 결과를 emit만 하지 말고 floor edge >90m를 assert하고 tick에서 예상 밖 contact를 abort한다. graph outputs뿐 아니라 세 controller의 velocity/position input readback을 jointNames와 묶어 steps에 추가하고, 기존 독립 command/TF observer를 유지한다. 최초 zero와 종료 시점을 묶은 retreat와 outcome JSON을 생성한다. 새 supervisor는 runtime exit=0이어도 execution_complete.status/quiet 실패를 성공으로 바꾸지 않아야 한다. session은 Exception을 잡고 정상 exit할 수 있기 때문이다.

이들은 새 제어기·gain·sign 실험이 아니라 같은 물리 경로의 admission/recording 최소 보완이다. 이번에는 불완전한 wrapper나 실행 승인 파일을 만들지 않았다. 현재 제출 명령의 실행 가능성은 route CLI 차원 PASS, 요청된 감독 안전 gate 차원 NOT_READY다. 가장 작은 다음 코드 작업은 위 세 원본의 새 버전(supervisor/session/ROS discovery gate)에 이 두 보완만 적용하는 것이며, 이후 별도 사용자 1회 실행 승인으로 이어져야 한다. 범용 lease/C++ 프로젝트는 필요하지 않다.

## 감독·중단·수집

최종 보완본 승인 후 supervisor는 관련 없는 Isaac/ROS process를 종료하지 않고 먼저 발견·기록하며, domain191에 unrelated ROS를 열지 않는다. 시작 전 named topology/현재 source hash/빈 domain/단일 target TF/quiet baseline/floor clearance가 모두 통과해야 비영 명령을 허용한다. supervisor는 로그와 phase/pose/속도를 실시간 관찰하고 예상 밖 publisher·contact·속도/공간 이탈·stale·child failure 시 즉시 abort한다. 외부 감독의 정상 abort 인터페이스는 새 attempt의 `abort_motion` 파일 생성이다. observer zero도 요청하려면 같은 attempt에 domain191/time을 기록한 `zero_request.json`을 생성한다. 이 파일 방식은 Kit hang에 대한 hard emergency stop이 아니다. hang이면 동작/정지 UNKNOWN으로 남기고 승인된 supervisor 외 다른 process나 실제 로봇에 ROS를 보내지 않는다. 무조건 retry하지 않는다.

종료 후 신규 부모/attempt의 command/env/hash, probe, runtime stdout, steps, adapter_commands, ros_observed, joint_io, scene/collision/isolation, contacts, zero, completion을 수집한다. 최종 1초 root+COM+FD와 span, zero 전후 변위/후퇴, command·target·q/dq를 함께 보고 `MOVED`, `QUIET`, `FULL_E2E`를 별개로 기록한다. QUIET 미달/누락/exception/미완료는 NOT_READY로 보존한다. engineering 실패 시도는 사라지지 않으며 연구 denominator는 0, Full E2E/QUAL12/432는 계속 HOLD다.

## focused 검사와 provenance

정적 AST 인자/소스 읽기 PASS. 과거 plan에 등록된 session/ROS/curvature/governor/controller/bench 6 SHA 대조 PASS(6/6). 새 output 부재 PASS. 실제 launch/live endpoint/current composed topology UNKNOWN. USD-only open 실패(ModuleNotFoundError: pxr), usd executable 탐색 실패, git status는 이 디렉터리에 .git가 없어 실패했다. 이를 물리 실패 episode나 정적 PASS로 바꾸지 않았다. 최종 source 승인에는 추가 dependency closure의 hash도 함께 기록해야 한다.

| source | 현재 SHA256 |
|---|---|
| `scripts/fe2e_v02_stopping_validation_session_v01.py` | `dd881de1a3699f49bc8be7354b09815f2c9d834095119693b712065a8892e232` |
| `scripts/fe2e_v02_stopping_validation_ros_v01.py` | `675ebb52a0aaf0c955d2d52e02c412f7a846931e52c1f4bf64eea9c0d4beedf7` |
| `scripts/full_e2e_demo_ros_observer_v01.py` | `8186960b6afd71f8e5edc3647804f1bd5babe4813d59cab8bbf108f7cb70acca` |
| `evaluation/fe2e_v02_stopping_adapter_v01.py` | `dd574fb849c034a9492717b992fe8681fe4a03775dd8599c6256b353c2787d80` |
| prior drive_contract.json | `7e6937a2c14f5be4fea4b50dc9cfb7c533a62f5a54eb3885533d2f6cb81ec551` |

변경 파일은 이 새 보고서와 docs/PROJECT_STATE.md append뿐이다. 원본 scripts/USD/protocol/과거 attempt/최신 STOP_HOLD 보고서는 수정하지 않았다.
