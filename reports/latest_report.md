# 현장 단일 로버 v08 — 첫 실제 ROS 물리 이동·zero·정지 확인

2026-11-01 KST. **요청한 짧은 A→근방 B 물리 이동은 달성: MOVED YES, ROS 구동, 전진 +0.021970749m, 주행 후 정지 PASS.** 기존 실제 건설 현장과 동일 로버에서 단 한 번의 Kit 세션·한 번의 주행 episode를 수행했다. NONZERO 발행 45회는 한 pulse 안의 연속 제어 발행 수이며 45개 실험이 아니다. Native fallback은 실행하지 않았다. HPO·training PAUSED, 연구 denominator **0**, autonomous/Full E2E NOT_YET_VALIDATED.

**전체 runner는 NOT_READY, 호출 명령 종료코드 1을 보존한다.** 실제 이동·정지는 확인했지만, 정상 감속·zero 이후 기존 wall watchdog/종료 zero가 adapter를 FAULT_LATCHED로 바꿨다. 이를 성공 코드로 고치거나 재실행하지 않았다.

## 실제 측정

| 항목 | 관측·판정 |
|---|---|
| 실제 구동 경로 | ROS `/rover/cmd_vel` → 공급자 기존 Action Graph → articulation wheel/steer controller → PhysX |
| 실제 articulation root | `/World/ENG_FE2E/Rover/base_link` |
| 승인 discovery 대기 | 0.460262283초 wall; 원본 guard PASS 후 admission |
| 비영 Twist 발행 | 45회; 요청 surface speed .02m/s, yaw rate0 |
| pulse 시작 / 정상 감속 요청 | sim4.433333565 / 6.433333669초 |
| 첫 zero command | sim6.683333682초; 정상 감속 후 |
| graph wheel target 최대 | 0.145805219rad/s |
| 실제 wheel 최대 abs dq / 최종 | 0.362895578rad/s / 0rad/s |
| 실제 wheel 최대 abs Δq | 0.174609396rad |
| base 시작 world XY | (-25.887977600098, 28.470867156982)m |
| base 끝 world XY | (-25.887977600098, 28.492837905884)m |
| world ΔX / ΔY | 0 / +0.021970748901m |
| 초기 heading 기준 signed forward / left | +0.021970748901 / +0.000000160891m |
| base 최종 net / 최대 XY 변위 | .021970748901 / .021980285645m; <.05m |
| base 최대 planar 속도 | .020390048268m/s; 기존 .03m/s pulse abort 이하 |
| zero 이후 추가 전진 | .000917434692m |
| zero 이후 backward excursion / reverse from peak | 0 / .000036239630m |
| 정지 마지막 관측 창 | sim15.416667471–16.416667523초, 1.000000052초 |
| 정지 raw COM / base origin 최대 속도 | .000168157284 / .000174916640m/s |
| 정지 FD 최대 속도 / XY span | 0m/s / 0m; 기존 .002m/s·.002m 기준 PASS |
| 물리 clock | 실제 PhysX callback·SimulationManager를 기존 코드로 사용; 803 telemetry samples |

Wheel 회전만으로 이동을 판정하지 않았다. 기존 world base pose의 +Y 진행, physics named targets, q/dq, graph readback, 명령, zero 이후 같은 live 물리 세션에서의 정지를 함께 확인했다. 원래 연구용 FINAL 위치/yaw 또는 정밀 접근 성공으로 해석하지 않는다. 실행 코드가 계산한 target.pass는 기존 engineering waypoint 진단일 뿐 연구 결과가 아니다.

## 발견된 GID와 이름: 이번 승인 PASS, v07 unknown의 해소는 입증되지 않음

이번 session/child의 `discovery_wait.jsonl`에는 46개 관측이 기록됐고 **unknown endpoint 관측은 0개**였다. 새 driver가 나타날 때 이미 승인된 이름과 namespace로 관측됐다. 따라서 이번 driver 신원 검증은 YES이지만, **unknown→known 동일 GID 해소 관측은 NO / v07 익명 GID의 정체는 UNKNOWN**이다. 이전 프로세스의 GID를 새 프로세스 GID와 동일시하지 않는다.

- 승인 driver: `v02_stopping_single_validation`, namespace `/`, type `geometry_msgs/msg/Twist`, GID `[1,15,113,9,254,172,163,2,0,0,0,0,0,0,19,3]`.
- zero observer: `eng_smoke_observer`, namespace `/`, GID `[1,15,113,9,0,171,129,139,0,0,0,0,0,0,21,3]`.
- v07 unknown GID `[1,15,113,9,166,117,164,188,0,0,0,0,0,0,19,3]`는 승인 목록에 넣지 않았다.

수정은 새 v08 session/ROS child의 startup-only 최대5초 관측 대기다. 미해결 endpoint가 있으면 비영 발행과 admission을 계속 막고 ROS spin·observer endpoint 재표본·fresh TF를 유지한다. 재표본의 GID가 바뀌거나 승인 driver 이름·namespace로 해소되지 않으면 거절한다. 준비 완료는 기존 원본 guard가 전체 publisher/subscriber/node 집합과 GID pinning·fresh TF를 통과해야만 가능하다. 원본 `evaluation/legacy_supervised_guard_v01.py`, v02 forensic guard 및 controller는 수정하지 않았다. 이번에는 실제 unknown 전이 분기를 재현하지 못했으며, 추출 함수 검사에서 unknown 대기·동일 GID 승인 이름 해소·다른 GID 거절을 확인했다.

## 충돌·접촉과 보존

기존 real-site collision·PhysX contact·.10m obstacle clearance·yaw ±2°·속도/변위 abort를 유지했다. 기존 런타임 support·shell 검사 코드를 재사용했으며 ray/AABB/clock 문제를 재구현하거나 별도 조사 세션을 열지 않았다. 실행 결과 주행/정지 단계 contact event3094개, 허용 rover/support 밖 접촉0개다. shell event442개/point2652개는 proximity report이며 최소 separation +.082013533m, 최대 impulse0Ns였다. **주행 중 shell penetration/load는 관측되지 않았고 접촉 안전 검사 PASS**다. Contact event 존재 자체를 장애물 충돌로 계산하지 않는다. 실제 wheel 지지와 collision을 끄지 않았다.

소스 stage `CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v02/stage_metrics_1m_z.usda`와 원래 로버·원본 USD를 보존했다. EngineeringFloor·새 로버·teleport·kinematic SetWorldPose·B4/B5·학습·연구 trial은 없다. v08 output의 run overlay만 생성했다. v07 provenance를 읽어 재사용했고 53개 원본 hash의 전수 재감사는 하지 않았다. 새 실행 코드와 실행 snapshot의 hash 일치를 확인했다.

Native fallback 코드는 과거 `fe2e_v02_normalized_physics_session_v08.py`의 physical joint target 경로를 정적으로 확인해 준비했다. 해당 과거 결과는 별도 derived model의 증거이므로 현장 로버 성공으로 전용하지 않았다. Fallback은 ROS child 종료/비영0·publisher 제거 확인·실제 10DOF/six wheel/four steer mapping·API 확인 후에만 run overlay graph를 비활성화하고 .02m/s equivalent의1.5초 단일 target→zero를 허용한다. 이번에는 ROS admission 성공으로 **native admission·graph 비활성화·native command 모두 미실행**이며 이 branch의 현장 runtime 검증은 UNKNOWN이다.

## 남겨 둔 실패와 원자료 불일치

Adapter 로그는 MOVING → sim6.433333669 BRAKING/NORMAL_DECELERATION → sim6.683333682 ZERO_SETTLING → sim8.383333771 FAULT_LATCHED/EMERGENCY_ZERO다. 첫 zero 이후 약1.7sim초 뒤에 fault로 바뀌었으며 그 이후 모든 command는 zero다. 기존 child의 전체 wall20초 hard 조건과 session wall20초 종료/abort 조건이 있고, 첫 fault 기록은 첫 command 후19.871wall초다. Child 시작은 첫 command보다 앞서므로 이 시각은 watchdog 경로와 부합한다. 속도·충돌 초과를 원인으로 새로 주장하지 않는다. `calibration_ros_complete.json`의 reason은 최초 zero 시점 `NORMAL_DECELERATION`을 보존하지만 최종 state는 `FAULT_LATCHED`다. 둘을 같은 시점의 상태로 읽지 않는다.

`run_status.json` 최상위 `MOVED=NO`, `STOPPED=NOT_TESTED`는 기존 runner가 초기값을 nested result로 갱신하지 않은 표시 결함이다. 같은 파일의 `result.outcomes.MOVED=YES`, `QUIET=PASS`, `base_stop_confirmed=true` 및 실제 pose/q/dq/quiet 원자료가 위 물리 판정 근거다. 최상위 stale 표기를 덮어쓰지 않았다. 별도 `measurement_summary.json`에서 불일치를 포함해 보존했다. Kit child exit0·ROS driver/observer exit0만으로 성공을 주장하지 않으며 **최종 adapter state 조건 불충족으로 NOT_READY/runner exit1은 그대로 유지**했다.

종료 final zero publish20회와 observer zero10회, 실제 graph zero readback, 최종 wheel dq0 및 주행 후 quiet PASS를 확인했다. 소유 child/observer는 exit0, 종료 후 Kit/training 프로세스0개다. 다른 사용자 프로세스를 종료하지 않았다. 추가 Kit·추가 주행·재시도0회.

## 변경·검사·다음 작업

새 파일: `scripts/construction_site_drive_runner_20261101_v08.py`, `scripts/construction_site_drive_session_20261101_v08.py`, `scripts/construction_site_drive_ros_20261101_v08.py`, 이 보고서. `reports/latest_report.md`, `docs/PROJECT_STATE.md`를 갱신했다. v01–v07 실행 소스·기존 출력·frozen guard는 쓰기 대상으로 사용하지 않았다.

검사: 새 script3개 syntax PASS; startup helper3조건 PASS; prepare/corridor PASS; 실행 전 resource gate PASS; 실제 ROS admission·nonzero→graph→wheel→world base→zero→quiet PASS; contact safety PASS; 새 code snapshot hash PASS; 전체 adapter/runner qualification **FAIL/NOT_READY**; v07 unknown identity 및 native 현장 실행 UNKNOWN. 이 저장소 경로에는 `.git`이 없어 `git status`는 exit128이었다. Git stage/push는 하지 않았다.

다음 구체적 작업은 **이번 로그만으로 watchdog/종료 zero가 정상 ZERO_SETTLING을 fault로 바꾸는 생명주기를 수정하고 runner 최상위 상태 표시를 nested 결과와 맞추는 별도 코드 작업**이다. 이번 달성한 기본 이동을 위해 추가 driving은 필요하지 않다. Precision2mm/30mm/yaw·autonomous perception/Pose·B4/B5·324/432-run은 향후 작업이며 이번 결과로 인증하지 않는다.

실행 명령:
```bash
python3 scripts/construction_site_drive_runner_20261101_v08.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v08
python3 scripts/construction_site_drive_runner_20261101_v08.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v08
```

외부 증거 root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v08/`. `prepare.json`, `code_versions.json`, `executed_code/`, `static_checks.json`, `runtime.log`, `run_status.json`, `measurement_summary.json`, `final_verification.json`, `attempt_0001/`의 `discovery_wait.jsonl`, `discovery_result.json`, 두 endpoint forensic JSONL, `adapter_commands.jsonl`, `steps.jsonl`, `contacts.json`, `stop_quiet_result.json`, `calibration_ros_complete.json`, `owned_processes.json`, `execution_complete.json`을 함께 보존한다.
