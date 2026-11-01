# 현장 단일 로버 v07 — fresh TF PASS / ROS discovery 차단으로 이동 FAIL

2026-11-01 KST. **실제 Kit 1회, NONZERO 명령 0회, wheel 최대 |dq|=0rad/s, base XY 변위=0m, MOVED NO, 주행 후 STOPPED NOT_TESTED.** 요청한 A→B 이동은 달성하지 못했다. 수정된 v06 TF 대기는 실제 runtime에서 통과했고 ROS driver child도 생성됐지만, 비영 명령 허가 전 `PUBLISHER_SET`으로 중단됐다. HPO·GPU training **PAUSED**, 연구 denominator **0**, Full E2E NOT_YET_VALIDATED. 추가 Kit 실행·재시도는 없다.

| 검사/측정 | 결과 |
|---|---|
| 실행 전 Kit/training resource gate | PASS, 해당 프로세스 없음; GPU 기존 rustdesk 535MiB만 존재 |
| 새 v07 prepare / 원본 출처 해시 / 기존 graph / corridor | PASS |
| 실제 PhysX callback / manager | 266 steps / 4.433333564550s, dt=.016666667536s; callback 누적과 manager 일치 |
| fresh TF admission | PASS, wall age .063626766s ≤ .5s, sim 차 .016666668s ≤ .1s |
| 실제 wheel support / wheel contact | 2,214/2,214 PASS / 6개 wheel 경로 contact |
| shell-floor ray | 9/9 PASS, 최소 gap .070647287m |
| 기존 obstacle clearance | PASS, .10m·yaw ±2°·기존 sweep 유지 |
| ROS child / driver ready·admitted | 생성됨 / 미도달 |
| NONZERO / Action Graph 비영 명령 수신 | 0 / NOT_TESTED |
| wheel 최대 abs dq / base net·max XY 변위 | 0rad/s / 0m·0m |
| 주행 후 zero→STOPPED / 목표 도달 | NOT_TESTED / NOT_TESTED |
| 내부 결과 / native child / runner exit | NOT_READY(PUBLISHER_SET) / 0 / 1 |
| 종료 후 Kit/training | 없음 |

v06 runner/session과 기존 ROS v02를 **수정 없이 재사용**했다. `--output` 지원 및 기존 output 충돌 차단을 실제 코드에서 확인했다. 이미 검증된 RaycastHit 속성 접근·stage clock·geometry·supplier graph·linear.x×15·저속 .02m/s surface 요청/2s pulse·guard threshold·연구 FINAL 기준을 바꾸지 않았다. 예정 waypoint는 (-25.887977680, 28.520869113)m이며 약 +Y .05m이나 pulse branch에는 도달하지 않았다. EngineeringFloor·teleport·새 controller/planner·원본 USD 재구성은 없다. 실행 중 파생 overlay만 기존 코드가 새 output에 생성했다.

## 새 TF의 직접 증거

`session_endpoint_forensics.jsonl`의 isolated 입력은 wall now=1793516278.0833058, physics sim=4.333333559334278s이다. 채택한 TF stamp=4.316666891s, 실제 수신 wall=1793516278.019679, count=255, observer status wall=1793516278.0603328이다. status age=.022973061s와 별개로 **TF 자체 wall age=.063626766s**를 확인했다. 직전 TF stamp=4.300000224s/수신 wall=1793516277.95724에서 stamp와 arrival이 둘 다 새로 진행했다. 이후 TF stamp=4.433333564s/count262도 관측돼 TF 발행이 계속됐음을 확인했다. `/tf` publisher는 기존 `_World_ENG_FE2E_Rover_ActionGraph_ros2_publish_transform_tree` 1개였다. `ros_observed.jsonl`, `physics_steps.jsonl`, `steps.jsonl`과 measurement summary에 원자료가 있다. 옛 v06 TF_STALE를 이번 blocker로 재보고하지 않는다.

## 단일 코드 차단점: discovery의 미해결 endpoint 이름을 즉시 fatal 처리

실제 `isolation_check.json`·`isolation_verified.json` PASS 뒤 기존 `/usr/bin/python3 scripts/construction_site_drive_ros_20261101_v02.py --output <attempt>` child PID1078694가 실행됐다. `driver_ready.json`, `driver_admitted.json`, `pulse_start.json`은 생성되지 않았다.

최초 driver 실패 시각은 wall1793516278.4923873, phase=`discovery`, sim4.4333335645496845s다. 당시 publisher 이름은 **[`eng_smoke_observer`, `_NODE_NAME_UNKNOWN_`]**이며 두 번째 namespace는 `_NODE_NAMESPACE_UNKNOWN_`이었다. 중복 이름에 걸린 것이 아니다. 기존 `evaluation/legacy_supervised_guard_v01.py:23`의 허용 이름 집합 `{eng_smoke_observer, v02_stopping_single_validation}` 밖인 이름을 발견해 정확히 **AssertionError: PUBLISHER_SET**이 발생했다. v02 guard는 원본 snapshot을 저장한 뒤 이 검사를 호출한다. child는 `ENDPOINT_GUARD_FAULT`로 중단했고 session도 같은 discovery snapshot에서 실패했다. TF는 이 시점에도 신선했다(driver 입력 TF wall age=.022589922s, sim 차 약 .000000001s).

원본 endpoint 식별값을 유지한다. 모두 `/rover/cmd_vel`, type=`geometry_msgs/msg/Twist`다.

| 역할/관측 이름 | namespace | 원본 GID bytes |
|---|---|---|
| zero publisher `eng_smoke_observer` | `/` | `[1,15,113,9,166,115,133,151,0,0,0,0,0,0,21,3]` |
| 미해결 publisher `_NODE_NAME_UNKNOWN_` | `_NODE_NAMESPACE_UNKNOWN_` | `[1,15,113,9,166,117,164,188,0,0,0,0,0,0,19,3]` |
| 공급자 graph subscriber `_World_ENG_FE2E_Rover_ActionGraph_ros2_subscribe_twist` | `/` | `[1,15,113,9,212,111,150,194,0,0,0,0,0,0,4,4]` |

unknown endpoint는 child 시작 뒤 출현했고 이름 메타데이터보다 endpoint discovery가 먼저 보인 상황과 부합한다. 다만 해당 GID가 나중에 승인된 driver 이름으로 해소되는 증거는 없으므로 **driver 신원으로 확정하거나 guard를 우회하지 않았다**. 두 forensic JSONL의 GID·이름·phase·pinned_before를 보존했다. 바닥·geometry·traction을 이번 원인으로 추정하지 않는다. command가 도착했는데 움직이지 않은 사례도 아니다.

## 측정·종료·보존

84개 base/joint telemetry에서 world base 시작과 끝은 모두 (-25.887977600098, 28.470867156982, -.008307690732)m이고 XY net/max 변위0이다. named wheel dq 최대0rad/s. `adapter_commands.jsonl`은 비어 있고 driver `nonzero_publish_count=0`, `start_sim_s=null`, `zero_start_sim_s=null`이다. adapter 초기 state `MOVING`은 실제 이동 증거가 아니다.

오류 후 abort/zero_request, timeline pause 및 기존 graph velocity/effort zero cleanup을 수행했다. driver final zero publish20회, observer zero publish10회가 기록됐고 observer 실제 관측 cmd29개는 모두 zero다(발행 수와 수신 수를 동일시하지 않음). observer/driver exit0, 남은 Kit/training 없음. 마지막 quiet PASS는 무구동 baseline이며 **주행 후 STOPPED PASS로 전용하지 않는다**. pause 이후 물리 이동을 관찰하지 못했으므로 postzero stop은 NOT_TESTED다. 연구 FINAL의 30mm/yaw/strict quiet 기준을 변경하거나 공학적 주행 판정으로 대체하지 않았다.

실행 전 fresh-TF 함수 정적 회귀3개(stale wall 거절/fresh 수락/stale sim 거절), runner/session/ROS syntax3개 PASS. prepare 검증 PASS 후 단 한 번 실행했다. 종료 후 prepare에 기록된 **53 input SHA256 모두 일치**, 실행 코드 snapshot/hash 보존 PASS. v06 두 시도의 기존 출력과 소스, 원본 stage·잠금·weights는 덮어쓰지 않았다. 진단 중 runtime.log가 아직 생성되기 전 tail exit1은 파일 생성 전 조회이며 실험 재실행이 아니다. native exit0만으로 성공이라 주장하지 않고 내부 NOT_READY 및 runner exit1을 유지했다.

명령:
```bash
python3 scripts/construction_site_drive_runner_20261101_v06.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v07
python3 scripts/construction_site_drive_runner_20261101_v06.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v07
```

외부 증거 root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v07/`. 핵심 파일은 `prepare.json`, `run_status.json`, `runtime.log`, `code_versions.json`, `executed_code/`, `measurement_summary.json`, `final_verification.json`, `attempt_0001/`의 두 endpoint forensic JSONL·driver_guard_fault·calibration_ros_complete·runtime_summary·physics_steps·steps·support/shell·zero_published·owned_processes다. Terminal 실패와 연구 분모0을 유지했다.

변경 파일은 이 보고서, `reports/latest_report.md`, `docs/PROJECT_STATE.md`이며 실행 소스 변경0이다. 다음 구체적 조치는 **새 버전 discovery에서 unknown name/namespace endpoint를 비영 명령 차단 상태로만 bounded 대기시키고, 실제 승인 이름·동일 GID·허용 집합·fresh TF가 모두 검증돼야 admission을 허용하는 처리**다. 승인되지 않은 신원/다중 GID/timeout은 계속 fatal이어야 한다. 이번에는 해당 수정이나 추가 주행을 실행하지 않았다. HPO·324 E2E·B300·Qual12·432·B4/B5·autonomous datum·training은 모두 미실행이다.
