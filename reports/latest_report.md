# 건설현장 단일 로버 drive runner v02 — 2026-11-01

실제 현장 USD에 기존 ROS/세 articulation controller를 연결하는 러너를 구현했다. Kit startup·물리 stepping·Twist·zero·측정·종료 코드가 포함된다. 실제 실행은 통로 안전 gate에서 중단했다. GUI 점유를 구현 중단 이유로 사용하지 않았다. **구현 완료와 물리 검증 완료는 구분한다.**

| 필드 | 결과 |
|---|---|
| actual runner IMPLEMENTED | YES — 신규 Python 4개, 총 388줄 |
| prepare-only | PASS (`prepare_0003/prepare.json`) |
| GUI | free — 현재 Kit/학습 후보 0; GPU compute 목록은 rustdesk PID953930/535MiB만 검출 |
| actual Kit launch | NO |
| actual MOVED | NO — motion attempt 0, 실제 운동 관측 없음 |
| quiet STOPPED | NOT_TESTED |
| swept collision clearance | FAIL / NO_SAFE_CORRIDOR |
| 연구 denominator | 0 |
| HPO/training/Qual12/B300/324/432 | 미실행; HPO scheduling 중지 유지 |

## 구현과 실행 계약

- `scripts/construction_site_drive_runner_20261101_v02.py`: 일반 Python 진입점. `--prepare-only`는 로컬 bundled USD 라이브러리만 사용하는 별도 CPU worker를 실행하며 Kit/GPU/ROS를 시작하지 않는다. provenance SHA, 실제 경로, 현장 composed geometry, graph admission, 출력 schema와 다음 명령을 저장한다. `--run`은 기존 프로세스/GPU·통로·hash·domain isolation을 검사한 뒤 실제 로컬 Isaac Python으로 단 한 session을 실행한다. GUI_BUSY에서는 simulator를 시작하지 않는다. 실행 상태·실패는 파일에 남긴다.
- `scripts/construction_site_drive_geometry_20261101_v02.py`: 원본 `stage_metrics_1m_z.usda`를 sublayer로 유지하는 새 layer에 원본 ActionGraph만 reference하고, 191 domain/context와 세 controller의 targetPrim을 실제 `/World/ENG_FE2E/Rover/base_link`로 연결한다. Render active·카메라 namespace·원래 floor/pallet/brick collision과 rover pose를 유지한다. floor 생성·로버 teleport·원본 USD 수정 없음.
- `scripts/construction_site_drive_session_20261101_v02.py`: 정적으로 읽은 `legacy_supervised_session_v02.py`에서 IO/물리 step/측정/접촉/endpoint forensic을 적응했다. 기존 guard v02 및 관측기 v02를 그대로 재사용한다. 정지 baseline, graph/actor signature, 실제 articulation DOF, target TF를 검사한다. actual joint q/dq, controller inputs/targets, root transform/raw COM velocity/origin 보정 속도/FD, 접촉과 command를 기록한다. 비상 정지 요청 및 timeline pause, 소유한 ROS child만 정리한다. SIGINT/SIGTERM·watchdog에서도 zero 파일과 publisher/final graph-zero 경로를 갖는다. 강제 종료·프로세스 장애는 성공으로 처리하지 않는다.
- `scripts/construction_site_drive_ros_20261101_v02.py`: 기존 StoppingAdapter/DriveContract/gains와 endpoint guard를 유지한다. engineering request만 직진 surface .02m/s·angular 0·최대 2sim-s로 선언했다. 정상 감속·zero, emergency fault latch, 최종 zero 20회를 유지한다. 새 controller framework나 frozen controller 수정은 없다.

선택한 engineering waypoint는 현재 base `(-25.8879776800,28.4708691133)`, yaw90°에서 전방 .05m인 **(-25.8879776800,28.5208691133)** 이다. 팔레트 작업·perception 목표가 아니다. pulse는 .04m 이동 또는 측정속도 .03m/s에서 zero 요청하며, .15m displacement/2° yaw를 넘으면 물리를 pause한다. zero 뒤 8sim-s hold와 최종 연속 ≥1s raw COM/origin/FD 모두 ≤.002m/s·pose span≤.002m를 요구한다. target long/lat≤.030m, yaw≤2°, clearance .10m는 유지한다. 이전 34.127mm 역방향 drift/quiet FAIL/PUBLISHER_SET 원인 UNKNOWN은 해결됐다고 주장하지 않는다. zero publication만으로 정지 성공을 판정하지 않는다.

## 실제 통로 차단 근거

`prepare_0003/corridor.json`에 collision 314개와 전체 문제 geometry를 저장했다. rolltainer·4 caster·rover wheel links를 포함한 전체 subtree bound는 X[-26.583534,-25.192422], Y[27.727124,29.214614], Z[-.008438,10.491648]m다. 그 높이는 `/World/ENG_FE2E/Rover/Cube`의 실제 enabled collision이 Z[9.491648,10.491648]m에 있기 때문이다. 이를 임의로 삭제하거나 시각화용이라고 간주하지 않았다.

.10m clearance+2° yaw envelope, -.05m 역방향부터 +.15m 전방까지의 보수적 sweep은 X[-26.719072,-25.056883], Y[27.541586,29.500153]m다. 현장 단일 mesh `/World/ConstructionSite/Env/cb5ce5926fdd4ce2b8f8f548239dcfaf/cb5ce5926fdd4ce2b8f8f548239dcfaf`의 삼각형 AABB 8개가 높이 약3.623–3.652m에서 이 전체 높이 sweep과 겹쳤다. 예: face36800 bounds X[-26.568000,-23.491001],Y[27.086000,31.476002],Z[3.649996,3.651996]. 또한 바닥 후보를 높이[-.03,.02]m·삼각형 높이변화<.005m로 제한한 31×31 support grid에서 353개 점의 지지가 확인되지 않았다. 예 (-26.719072,29.304296).

이는 **보수적 인증 실패이며 실제 접촉/주행 불가능의 증명은 아니다.** subtree의 원격 Cube와 별도 높이 물체를 하나의 AABB로 합친 공백, 실제 floor 경사/높이·미세 hole은 추가 검토가 필요하다. 현재 실패 근거를 무시해 drive하지 않는다. obstacle triangle AABB와 표본 support 검사는 연속 정확 swept-volume/PhysX traction 인증을 대체하지 않는다.

## 검사와 실패 보존

- 신규 4파일 `py_compile` PASS.
- 로컬 source manifest/센서 provenance SHA 일치 PASS. 기존 broad audit를 다시 수행하지 않고 실제 재사용 dependency만 검증했다.
- derived graph의 기존 `validate_graph` PASS: 세 controller 및 wiring/config/domain/target 검증. 로컬 USD에서 카메라 relationship의 reference 외부 target 경고는 남아 있다. ROS camera helpers는 꺼 두고 원래 /Render는 유지한다.
- prepare 첫 시도 FAIL: bundled USD BBoxCache keyword 인자 호환 오류. root `geometry_stdout.log`와 prepared layer 보존. positional 인자 수정 후 새 `prepare_0002`, 최종 코드 hash를 반영한 `prepare_0003`에서 prepare PASS/clearance FAIL.
- 실제 `--run --output .../prepare_0003` gate 검사 exit1 / `reason=NO_SAFE_CORRIDOR`, `Kit_launch=false`. domain probe/ROS/Kit/physics/command/재시도 모두 0. `run_status.json` 보존. 일반 host 성공으로 MOVED/STOPPED를 만들지 않았다.
- synthetic GUI_BUSY 분기 검사 PASS (`test_gui_busy/resource_gate.json`, pid=-1은 시험값이며 실제 프로세스 아님): subprocess/Kit/attempt 생성 없음.
- 보존 검사: 전체 mesh 속성을 문자열로 직렬화한 첫 자체 check가 약15GB 메모리를 사용해 해당 자체 CPU check만 SIGINT로 중단(exit130, `verification_attempt_0001.json`)했다. 사용자 프로세스는 중지하지 않았다. `verification.json` 첫 source-stack 비교 FAIL은 새 ancestor overs를 차이로 세었고, `verification_0002.json`은 의도한 stage pseudoroot를 차이로 세어 FAIL이었다. 이 기록을 보존했다. 최종 `verification_0003.json`은 graph 밖 원본 membership/type/contributing source stacks 동일·변경 path 0, 새 layer의 graph 밖 property 0(ancestor overs와 의도한 stage metadata 제외)로 PASS. 원본 source SHA/Render/1m-Z/one rover/300 brick mesh/EngineeringFloor 없음도 PASS. 실제 runtime의 nested articulation/caster support/traction·native teardown은 NOT_TESTED다.

## 출력과 다음 단일 행동

외부 신규 출력 root:
`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v02/`

**다음 단일 행동: 원본을 바꾸지 않고 `/World/ENG_FE2E/Rover/Cube`의 물리 소속과 현장 floor 삼각형 높이를 정밀 확인해 NO_SAFE_CORRIDOR를 해소할 수 있는지 검사한다.** 현재 GUI를 닫는 것만으로 주행이 허용되지 않는다. 이번 실행은 gate 실패 기록을 보존하며 실제 drive를 시도하지 않았다.

새 미사용 preparation 경로에서 재검사하는 실제 실행 명령은 다음과 같다. 이것은 자동 주행이나 추가 실행 허가를 뜻하지 않으며, 통로 FAIL이면 run이 다시 차단된다.

```bash
python3 scripts/construction_site_drive_runner_20261101_v02.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v02/prepare_0004
python3 scripts/construction_site_drive_runner_20261101_v02.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v02/prepare_0004
```

실행 가능한 최종 명령은 새 `prepare.json`에도 저장된다. 사용한 prepare_0003은 run_status가 있어 재실행을 거부한다. 이전 v01·원본 scripts/USD/controller/checkpoints·기존 출력은 보존했다. 수동 ROI B5/PRE/FINAL은 자동 Full E2E 증거가 아니며 B4 modulo180을 목표 heading으로 연결하지 않았다. 실제 로봇 배치 검증이나 연구 성공을 주장하지 않는다.
