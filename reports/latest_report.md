# Legacy supervised mobility ONE SHOT 구현 — 2026-10-21 v01

**두 보완 구현 완료 / offline PASS / 별도 simulator 1회 승인 대기.** 실제 simulator·ROS·physics·publish·actuator·retry 실행은 0회다. 실행 명령은 아래 실제 존재하는 새 wrapper를 가리킨다. Runtime admission과 실제 정지 성공은 UNKNOWN이다. 과거 진단 보고서를 대체하거나 재실행 결과로 해석하지 않는다.

## 변경 파일과 보존

- `scripts/legacy_supervised_session_v01.py`: 기존 stopping session의 버전 분리본. 제어 경로·수치 유지, admission/live guard·정지 평가·target 계측·child 종료 기록 추가. baseline만 독립 1초 판정에 필요한 75 tick으로 확장했다.
- `scripts/legacy_supervised_ros_v01.py`: 기존 ROS child의 버전 분리본. 기존 StoppingAdapter 호출/감속/최종20 zero 유지, endpoint discovery 및 heartbeat 추가.
- `scripts/legacy_supervised_observer_v01.py`: 기존 observer의 버전 분리본. 상태 timestamp 추가. 요청 시10 zero를 상태 갱신과 함께 발행하도록 바꿔 stale 오탐을 방지했다.
- `scripts/legacy_supervised_one_shot_v01.py`: required `--output`, atomic mkdir, 빈 domain probe, 정확히 attempt_0001 한 번, pinned 입력 확인, argv/env/PID/group/exit/internal verdict 기록. 자동 retry 없음.
- `evaluation/legacy_supervised_guard_v01.py`: simulator/ROS import 없는 공용 실제 guard·독립 평가 함수.
- `scripts/legacy_supervised_offline_checks_v01.py`: 저장 로그/합성 fixture의 집중 검사.
- `scripts/legacy_supervised_sources_v01.json`: 새 소스6개·기존 adapter3개·원본 graph/contract의 **정확한 경로와 전체 SHA256**, 11 entries. wrapper가 시작 전에 검증한다. 과거 plan의 legacy dependency SHA도 별도로 검증한다. 보고서에 긴 SHA 목록을 중복하지 않는다.
- 이 보고서, `reports/legacy_supervised_mobility_one_shot_implementation_20261021_v01_checks.json`, `docs/PROJECT_STATE.md` append.

원본 session/ROS/observer/supervisor, USD/controller/drives/protocol, 이전 보고서와 attempt는 수정하지 않았다. 과거 plan에 등록된 dependency6개 SHA 일치 PASS. 원본 session SHA `dd881de1a3699f49bc8be7354b09815f2c9d834095119693b712065a8892e232`, 원본 ROS SHA `675ebb52a0aaf0c955d2d52e02c412f7a846931e52c1f4bf64eea9c0d4beedf7` 보존. 이 경로는 v07 HOLD branch와 연결하지 않는다.

## 실제 guard와 범위

`validate_graph`/`graph_signature`: 현재 composed stage의 모든 OmniGraph node 집합을 저장된 graph와 비교한다. 기존 세 `IsaacArticulationController`의 named jointNames, targetPrim=현재 base_link, robotPath, exec/velocity/position/source 연결, upstream 설정을 대조한다. domain191 ROS2Context와 bridge context wiring, camera/render disable도 확인한다. articulation 초기화 후 10 DOF **정확한 순서**를 요구한다. 시작 snapshot 이후 매 tick graph 설정·연결 및 rigid/collision/joint actor schema·enabled·relationship 변경을 거부하고 script hook은 fail closed한다. 기존 node enable/drive/gain을 바꾸지 않는다.

`EndpointGuard.check`: observer가 수집한 domain191 node·publisher/subscriber GID/type/namespace를 검사한다. 허용 node는 `eng_smoke_observer`, `_World_ENG_FE2E_Rover_ActionGraph_ros2_subscribe_twist`, `_World_ENG_FE2E_Rover_ActionGraph_ros2_publish_transform_tree`, driver `v02_stopping_single_validation`뿐이다. TF publisher1, command subscriber2를 고정한다. 시작 isolation은 publisher0, discovery는 observer zero publisher/driver의 점진적 등장을 허용하며, driver_ready→session driver_admitted→pulse_start 뒤에만 비영 command를 허용한다. active에서는 두 publisher가 필요하며 정상 driver 완료 후 zero 단계에서는 driver 제거를 허용한다. 등장한 GID 교체, 추가 publisher/node, subscriber/TF 변경, observer 사망, heartbeat/TF wall age>.5초, TF sim 차이>.1초, driver heartbeat 손실은 fault다. driver도 같은 공용 guard를 비영 publish 전에 실행한다.

각 tick에 세 controller input readback(jointNames/positionCommand/velocityCommand/effortCommand), Ackermann output targets, 모든10 named joint q/dq 및 PhysX position/velocity targets를 기록한다. 설치된 `Articulation.get_applied_actions()` 구현이 `get_dof_position_targets/get_dof_velocity_targets`를 읽는 것을 정적으로 확인했다. command가 흐른 후 controller input 크기/이름 수가 맞지 않거나 target readback이 없으면 중단한다. 실제 API/readback 동작은 runtime UNKNOWN이다.

외부 collider inventory는 floor만 허용하고 guarded sweep floor clearance>90m를 assert한다. 실행 중 floor/rover 외 contact, graph/actor/endpoint 변화는 `abort_motion`+`zero_request.json` 요청 후 pause/failure로 기록한다. 기존 .03m/s zero 요청, >.25m/s emergency pause, >2m 이탈, source .07/KMAX/PRE_FINAL, 6 sim초 정상 감속 요청, 14.5 sim초/20 wall초 pulse 한도, zero480 tick을 유지한다. .03은 overshoot 없는 hard invariant라는 주장이 아니다.

이는 **관측 가능한 composed graph·actor 구조·ROS endpoint·소유 subprocess 범위의 guard**다. 관측되지 않는 native C++ callback 전체의 writer 부재 인증이 아니다. Kit update가 멈추면 파일 zero/pause가 물리 정지를 보장하지 않는다. wrapper는 180 wall초 watchdog 및 abort 후35초 유예 뒤 자기 process group만 종료·기록한다. 세션은 소유 ROS child를 wait→terminate→kill/reap하며 PID/exit를 남긴다. group 잔류·강제 종료는 NOT_READY다. 다른 기존 process/GPU는 건드리지 않는다.

## 오프라인 검사

- `python3 -m py_compile scripts/legacy_supervised*py evaluation/legacy_supervised_guard_v01.py`: 6 files PASS. 해당 검사는 compile만 하며 session import/launch 없음.
- `python3 scripts/legacy_supervised_offline_checks_v01.py`: **21 checks PASS**. 실제 공용 평가/변화 검출 함수를 직접 호출한다. raw COM/root/FD 초과, NaN, 누락, gap, 60표본 coverage 부족, pose span, saved prior failure/retreat, discovery→active→zero, GID 교체, foreign node, stale observer, graph source 교체/누락 writer, OS0/internal failure를 포함한다.
- wrapper에 이미 존재하는 reports 경로를 넘긴 검사: `FileExistsError`, nonzero exit PASS, simulator/ROS 미실행. 실제 fresh output은 생성하지 않았다.
- 기존 dependency6 SHA 대조 PASS. 새 output 부재 PASS. 실제 simulator/bridge/graph·접촉/target readiness는 **UNKNOWN/NOT_RUN**. 오프라인 PASS를 runtime PASS로 쓰지 않는다.

## 현재 실행 가능한 정확한 1회 명령 — 이 턴 미실행

사용자가 다음 턴에 이 경로의 simulator-only engineering **한 번**을 명시 승인한 뒤 실행한다. root가 존재하면 atomic mkdir에서 즉시 실패하며 자동 다른 경로 선택/재시도는 하지 않는다.

```bash
cd /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
export ROS_DOMAIN_ID=191 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_DISTRO=jazzy
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}:/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim/exts/isaacsim.ros2.bridge/jazzy/lib"
/usr/bin/python3 scripts/legacy_supervised_one_shot_v01.py \
  --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01
```

Wrapper는 위 환경을 내부에도 고정하고, `/opt/ros/jazzy/setup.bash`를 source한 `/usr/bin/python3` observer로 빈 domain을 먼저 확인한다. 이후 `/home/user/anaconda3/envs/hh_isaac51/bin/python scripts/legacy_supervised_session_v01.py --output <root>/attempt_0001 --domain 191`을 딱 한 번 호출한다. 세션이 같은 source된 Jazzy 환경의 `/usr/bin/python3 scripts/legacy_supervised_ros_v01.py --output <attempt>`를 생성한다. driver 수동 별도 실행 금지. 기존 hardcoded supervisor는 호출하지 않는다.

승인 체크: simulator-only/연구분모0/attempt1/retry0, 위 exact output와 source manifest, domain191에 실제 로봇이나 별도 ROS node가 연결되지 않음, 운영자가 runtime stdout/feedback을 감독하고 아래 abort terminal을 준비함, 이전 quiet FAIL을 인정하며 이번 성공을 예상하거나 보장하지 않음. Runtime preflight가 실패하면 그 attempt를 NOT_READY로 보존하고 멈춘다.

별도 terminal의 중단 명령(ROS publish 없음):

```bash
attempt=/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01/attempt_0001
test -d "$attempt" && touch "$attempt/abort_motion"
```

세션/driver가 abort를 읽고 기존 zero/abort 경로로 진입한다. zero_request 파일만 생성해도 session이 abort_motion으로 전환한다. wrapper terminal Ctrl-C도 같은 요청이며 자동 retry하지 않는다. 프로세스 종료는 물리 quiet 확인을 대신하지 않는다.

## Zero→quiet 산술과 판정 파일

`attempt_0001/stop_quiet_result.json`: MOVED / QUIET / RESEARCH_E2E를 분리한다. MOVED는 첫 관측 대비 planar displacement>.002m인 engineering 표시일 뿐 task success가 아니다. RESEARCH_E2E는 항상 `NOT_ASSESSED`다.

최종 표본에서 역으로 **연속 최소1 sim초**를 포함하는 구간을 고르고 모든 dt가 0<dt≤.1초인지 확인한다. raw `tensor_COM_velocity[:2]`, root-origin `base_origin_v[:2]`, 실제 pose FD `fd_velocity[:2]` 각각 planar norm 최대≤.002m/s, 구간 모든 pose 쌍 최대거리≤.002m를 요구한다. raw COM을 보정 origin/FD로 대체하지 않는다. NaN/누락/coverage 부족/gap이면 NOT_READY, 유효 자료에서 기준 초과면 FAIL. baseline도 동일 함수로 판정한다.

최초 ZERO_SETTLING/FAULT_LATCHED이며 실제 wire_v=wire_z=0인 adapter command의 source_step에 연결된 pose/yaw를 zero 기준으로 사용한다. dx,dy를 당시 yaw의 forward/left 축에 투영해 signed along/left 최종 변위, backward=max(0,-min along), reverse-from-running-peak, 최대 |lateral|를 기록한다. sim/wall zero 시각도 보존한다. 비동기 command→physics의 즉시 인과를 주장하지 않는다.

저장된 이전 attempt 재평가: 1.000000052초, max dt=.016666668초, raw COM=.002620264860, root-origin=.002619135991, FD=0m/s, span=0m. **MOVED=YES, QUIET=FAIL, RESEARCH_E2E=NOT_ASSESSED**, backward=.034127288744m, signed lateral=-.000002164250m. pose가 고정되거나 zero target인 것만으로 quiet PASS가 되지 않음을 실제 자료로 확인했다.

세션 `execution_complete.json`은 guard/child fault, raw quiet 미달, zero 관측 누락, adapter FAULT를 NOT_READY로 남긴다. 정상 기록은 QUIET PASS·zero 식별·ZERO_SETTLING·observer zero receipt를 요구한다. wrapper의 `supervisor_complete.json`은 OS exit뿐 아니라 내부 status·QUIET·RESEARCH_E2E·종료 bookkeeping을 함께 확인한다. engineering verdict가 좋아도 research terminal success가 아니다. raw steps/commands/contacts/실패를 삭제하거나 분모에서 숨기지 않는다.

실제 구현 blocker는 남아 있지 않다. 남은 단계는 **사용자 별도 1회 실행 승인과 그 실행 안의 실시간 admission**이다. UNKNOWN을 해결하기 위한 추가 paused/graph audit나 범용 native lease 개발을 요구하지 않는다. ENG001/QUAL12/432는 HOLD이며 이 경로로 해제하지 않는다.
