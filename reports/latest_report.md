# 건설현장 단일 로버 물리 주행 — 2026-11-01 v01

**BLOCKED_NOT_LAUNCHED. 실제 물리 주행 목표는 미달성이다.** 기존 사용자 Isaac Sim GUI PID 955077이 실행 중이므로 동시 실행 금지 조건에 따라 새 Kit를 시작하지 않았다. 기존 프로세스를 종료하거나 명령을 보내지 않았다. 실제 실패 지점은 simulator bootstrap 이전 resource gate다. 주행 실패나 정지 성공으로 해석하지 않는다.

## 실제 증거

출력: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v01/`.
`status.json`과 `gpu_processes.log`에 현재 프로세스·입력별 expected/observed SHA256·host/internal 상태를 보존했다. 최초 nvidia-smi에서 RTX5090 전체 4236MiB/32607MiB, PID955077은3379MiB였다. 명령은 `/home/user/anaconda3/envs/hh_isaac51/bin/python /home/user/anaconda3/envs/hh_isaac51/bin/isaacsim`이다. 실행 스크립트의 재확인에서도 기존 Isaac 프로세스를 검출했다. HPO/training 후보 프로세스는 이 점검에서 검출되지 않았다. VRAM 여유만으로 GUI 동시 실행을 허용하지 않았다.

성공한 센서 스테이지는 `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v02/stage_metrics_1m_z.usda`, SHA256 `424cb17b104d7a68a4c264216e38b9823f371524a8704e07fb4eec8b08d1e264`다. 내용은 LIT USD의 subLayer + metersPerUnit=1/upAxis=Z인 metadata-only root다. 원본 변경/100배 scale/geometry rotation은 하지 않았다. 이 스테이지와 기존 preflight가 참조하는 총25개 입력의 현재 해시는 모두 일치했다. 이는 이전 센서 preflight의 입력 보존 검사이며 현재 물리 collider/clearance 인증은 아니다.

## 소스에서 확인한 재사용 경로와 제한

- 센서 capture `scripts/construction_site_front_rgbd_capture_20261022_v02.py:26`은 활성 OmniGraph가 없음을 요구한다. 센서 스테이지에 ROS 구동이 이미 켜져 있다고 가정할 수 없다. 로버 base는 `/World/ENG_FE2E/Rover/base_link`다. `/Render`와 calibration compatibility namespace의 활성 상태를 보존해야 한다.
- 실제 ROS motion/zero 소스는 `scripts/fe2e_v02_stopping_validation_session_v01.py`와 ROS child `scripts/fe2e_v02_stopping_validation_ros_v01.py`다. session은 새200m EngineeringFloor를 만들므로 이번 현장 실행용으로 그대로 사용할 수 없다. 최신 forensic session `scripts/legacy_supervised_session_v02.py` 역시 별도 floor를 만든다. 둘 다 실행하지 않았다.
- 원래 controller는 bench `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`의 `/World/ROBOT_TASK/RuntimeRover/ActionGraph`다. 기존 session은 파생 로버의 ActionGraph 아래 세 articulation controller를 base_link에 bind한다. source physics는 `/home/user/hh/isaac_cosmos/assets/assets/robot/rover_base.usd`이며 위 해시 검사에 포함했다. 기존 geometry 근거 wheel radius .133m, graph speed multiplier15/radius .5의 custom Twist 계약은 SI base speed와 구별해야 한다.
- `evaluation/legacy_supervised_guard_v02.py`는 check 이전 snapshot/names/phase/sim/wall/pinned identity를 fsync한다. 기존 observer v02의 endpoint topic/GID를 함께 보존하는 경로가 이미 있으므로 새 guard framework는 필요 없다. 과거 PUBLISHER_SET 원인은 여전히 UNKNOWN이다.
- 이전 실제 정지 보고서의 post-zero retreat34.127288744mm와 raw-root quiet .002619135991m/s는 FAIL 유지다. long/lat .030m, yaw2°, quiet root+COM+FD .002m/s, clearance .10m를 완화하지 않았다. 이번에는 새 stop 측정이 없다.

## 이번 실행 및 검사

실행 가능한 신규 준비 코드: `scripts/construction_site_mobility_preflight_20261101_v01.py`. 표준 Python으로 입력 해시와 실제 프로세스를 기록하며 simulator나 ROS를 시작하지 않는다. **완성된 물리 drive runner는 아니다.** GPU가 비어도 현장 drive runner 미구현 blocker를 유지하며 우회 실행하지 않는다.

실제 명령:

```bash
python3 scripts/construction_site_mobility_preflight_20261101_v01.py --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v01
```

host exit **2**, internal **NOT_STARTED**, status **BLOCKED_NOT_LAUNCHED**. 동일 output으로 재실행하면 충돌을 거부한다. 후속 준비 점검은 새 미사용 output을 지정해야 한다. 초기 process matcher는 경로에 isaacsim이 포함된 GitHub runner 서비스 PID3222/3245도 후보로 오탐했다. status.json 원본은 보존했고 matcher를 executable basename 기준으로 수정했다. 실제 GUI PID955077의 blocker는 유효하다. 수정 후 AST parse PASS, 입력25개 hash PASS, resource admission FAIL. Git status는 `.git` 없는 디렉터리여서 exit128/FAIL이며 stage/commit/push 없음. 신규 코드/보고서/PROJECT_STATE append 외 원본 소스·USD·weights·잠금은 수정하지 않았다.

| 판정 | 결과 |
|---|---|
| MOVED | NOT_TESTED |
| STOPPED | NOT_TESTED |
| TARGET_REACHED | NOT_TESTED |
| FULL_E2E | NOT_RUN |
| RESEARCH_SAMPLE | 0 |

시뮬레이터 launch0, physics step0, nonzero/zero publish0, motion attempt0, retry0, training0. 초기/최종 pose·physics timestamp·wheel response·path CSV·contact·capture는 실제 관측하지 않았으므로 생성하지 않았다. 빈 CSV나 가상 정지 수치를 증거로 남기지 않았다. 현장 floor·footprint·pallet 방향 swept clearance는 아직 미검증이며 수동 engineering waypoint도 아직 선정하지 않았다. 자동 pallet datum과 B4 axis→face-normal mapping 역시 미해결이다. 기존 수동 ROI B5 target은 제어에 사용하지 않았다.

## 가장 짧은 다음 조치

현재 사용자 GUI에서 작업을 저장하고 정상 종료한 뒤 PID955077 종료와 GPU 점유를 다시 확인한다. HPO가 새로 실행 중이면 해당 실행 터미널에서 저장/checkpoint 가능한 정상 Ctrl-C 절차로 종료하고 프로세스 종료를 확인한다. 이번에는 자동 종료하지 않았다.

그 다음 위 metadata-only 현장 root를 유지하는 **단일 현장 runner**에 기존 ROS graph/세 controller binding과 v02 endpoint forensic을 연결하고, 현장 collision footprint/swept corridor 검사 후 짧은 forward-only 수동 engineering target을 정한다. 기존 empty-floor runner를 대신 실행하지 않는다. 실제 단1회 주행에서 zero 후 root+COM+FD와 접촉을 기록해야 물리 milestone을 판정할 수 있다. 이번 세션은 resource-blocked 결과가 확인되어 추가 launch/재시도 없이 종료한다.

사용자 최신 결정에 따라 3-rep HPO/training의 후속 scheduling은 중지한다. 향후 표현은 HR_Scan/LR_Scan/GeoCAD만 사용하고 Proxy 제외; 과거4-rep 잠금/결과는 보존한다. 기존 PROJECT_STATE의 HPO next action은 이번 결정으로 대체되며 연구 thresholds와 denominator는 변경하지 않는다.
