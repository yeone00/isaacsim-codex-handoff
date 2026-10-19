# Stopping adapter 실제 Isaac Sim 단일 engineering validation

**ENG001 재진입 NOT_READY. 단일 blocker: MEASURED_ACTUATION_STOP_ENVELOPE_OUTSIDE_TERMINAL_BUDGET.** DriveContract는 확정했고 새 adapter의 실제 ROS 주행/정상 감속을 1회 실행했다. 이번 profile의 속도 cap은 PASS지만 zero 이후 후퇴34.127289mm 및 quiet 미충족으로 terminal 정지 예산은 FAIL이다. ENG001 Full E2E는 실행하지 않았다. 자동 retry/추가 motion/QUAL12/revised smoke/confirmatory/432-run/연구 denominator 추가 모두0. 새로운 물리 진단이나 parameter sweep은 하지 않았다.

Bulk: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01` (이하 OUTPUT). 실행은 `attempt_0001` 하나이며 motion episodes=1, simulator initialization=1이다. 기존 calibration/output/보고서/controller/governor/curvature adapter/stopping adapter/USD/protocol은 수정하지 않았다.

## 1. 확정한 DriveContract

Read-only USD composition은 `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`의 `/World/ROBOT_TASK/RuntimeRover`를 기준으로 했다. SHA256 `224cac492d267d0403c9402484fcf84011191208fb4689e7e3fc33eadf3756fe`. 기존 demo와 동일 reference를 새 scene의 `/World/ENG_FE2E/Rover`에 사용했다. Passive caster8joint 복원이나 mobility/drive/gain 변경은 없다.

- 여섯 `front_left/right`, `middle_left/right`, `rear_left/right_wheel_link/collisions/mesh_0/cylinder`는 활성 Cylinder collider다. Radius=`0.13300000131130219`, axis Z, local→world scale 세 축 모두1(수치 오차 약2e−16), stage metersPerUnit=1. 따라서 geometry 기준 rolling radius **0.13300000131130219m**다. Radius의 property stack source는 `/home/user/hh/isaac_cosmos/assets/assets/robot/rover_base.usd`다. Source instance proxy 안에 있으므로 `Usd.TraverseInstanceProxies()`로 확인했다. 충돌 중 유효 접촉반경이나 slip 없는 base-speed tracking을 인증한 것은 아니다.
- Graph `/ActionGraph/ros2_subscribe_twist`의 linearVelocity→`break_3_vector_01.outputs:x`→`multiply_01` inputs:b=15→Ackermann inputs:speed. Front/backWheelRadius=.5m, wheelBase=.7m, trackWidth=.569m, invertSteering=true. Ackermann wheelRotationVelocity는 articulation controller의 rad/s velocityCommand로 FL/FR/RL/RR에 연결된다. Middle wheels는 출력 index0/1을 복사한다. WheelAngles는 front steer positionCommand(rad)로 전달된다. Derived scene은 이 세 controller의 targetPrim을 현재 base_link에 연결했다.
- Governor u는 wheel-equivalent/surface request(m/s)다. Straight wheel target을 `u/r_actual`로 일치시키려면 `15*wire_v/.5=u/r_actual`. 따라서 **wire_per_surface=.5/(15*.13300000131130219)=0.2506265639450088**. 이는 물리 geometry와 graph의 대수적 역변환이며 평균 base/wire 관측2.39475로 fitting한 값이 아니다. 이 custom topic의 linear.x는 그대로 SI base speed라고 해석할 수 없다.
- Angular 입력은 frozen compensated 값에서 curvature를 한 번 복원하고 기존 `encode_legacy`로 **scaled wire_v와 함께** encode한다. Degree ATan2→radian Ackermann 경로를 정확히 역변환한다. Wire angular.z는 SI yaw rate가 아닌 graph compatibility encoding이다. Semantic nominal omega=u*k와 구분하며 중복 π/180은 없다.
- `DriveContract(scale, evidence, approved=True)`를 새 publisher에 명시했다. 기존 curvature Adapter의 scalar 출력에 다시 governor를 직렬 중복 적용하지 않는다. StoppingAdapter가 기존 governor를 단 한 번 호출하고 curvature 모듈의 COMP/KMAX/encode_legacy를 재사용한다. 기존 파일을 변경하지 않았다.

증거: OUTPUT의 `drive_contract.json`, `graph.json`(connections/relationships 포함), `graph_contract_check.json`, `drive_target_roundtrip.json`. 설치된 Ackermann class AST를 불변 실행한 roundtrip에서 .022m/s surface 요청의 변환 후 wheel target/steer가 실제 radius를 사용하는 동형 kinematics와 **1e−12 이내 일치**했다. 기존 설치 numeric 계약3/3 및 stopping adapter8/8 PASS. 이 결과는 actuator target 단위 계약이고 actual base dynamics 보장이 아니다.

## 2. 실행 전 safety와 실제 command

GPU memory264MiB/여유31856MiB, 기존 Isaac/ROS 실행 없음(기존 image viewer는 유지)을 확인했다. Domain191 probe 통과 후, 새200×200m default floor만 있는 scene을 초기화했다. 바닥은 기존 calibration과 같은 구성이지만 연구 workspace ground와 동일한 traction 인증은 아니다. Reference physics/mobility는 보존했다.

Settled pose: (−5.790355205535889,3.15647554397583,0.000000631902367)m, yaw0.04363332615116316rad. 정지 baseline과 TF 좌표/시간을 대조했고, 단일 TF publisher/목표 cmd subscriber 및 외부 cmd publisher 부재를 확인한 뒤 command를 허용했다. 증거는 `settling.json`, `isolation_check.json`, `isolation_verified.json`이다.

1.68×1.61m footprint corner radius1.163453910m, base displacement2m guard와 floor edge 사이 실제 여유91.046190885m다. Pallet/brick/wall/column은 이 시험 공간에 없다. 외부 활성 collider floor 하나, actual contacts5304headers 중 unexpected external0이다. 따라서 pallet 근처 clearance/비접촉을 시험했다고 해석하지 않는다.

사전 요청은 기존 calibration과 같은 frozen first-step 형태 v=.07/k=.382784560616, phase PRE_FINAL, moving6sim s다. 이후 새 stopping adapter를 계속 호출하여 정상 감속을 수행했다. Cap .03m/s 이상, stale .50s, invalid measurement, abort 또는 wall watchdog에는 즉시 zero fault다. 별도 speed>.25m/s/center2m 이탈에는 자기 timeline pause guard가 있다. 이것은 terminal cap을 .25로 높인 것이 아니다. 정상 감속 .035m/s² reference/.07m/s² surface-command 및 PI gains는 기존값 그대로다. Zero가 즉시 정지를 보장한다고 가정하지 않고 큰 이격 공간을 확보했다.

실제 실행 command(완료됐으므로 재실행하지 말 것):

```bash
cd /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
python scripts/run_fe2e_v02_stopping_validation_v01.py
```

내부 Isaac launcher는 `/home/user/anaconda3/envs/hh_isaac51/bin/python scripts/fe2e_v02_stopping_validation_session_v01.py --output OUTPUT/attempt_0001 --domain 191`이다. ROS child는 `/opt/ros/jazzy/setup.bash` 환경의 `/usr/bin/python3 scripts/fe2e_v02_stopping_validation_ros_v01.py`이며 실제 cmd_vel→ActionGraph→articulation을 사용했다. 상세 argv/environment는 OUTPUT의 `runtime_command_attempt_0001.json`/preexecution plan/log에 남겼다. Supervisor는 기존 attempt directory가 있으면 재실행을 거부한다. Resume/retry dispatcher는 없다.

Owned simulator PID1752511은 종료 확인됐고 GPU 사용량도264MiB로 복귀했다. 기존 프로세스를 종료하지 않았다. Nonzero publish127회, 정상 감속 후 지속zero 및 finally zero20회, observer의 별도 zero가 기록됐다. Node의 예정 정상 감속을 observer zero로 미리 덮지 않았다. Runtime log에 기존 nested rigid-body/material 계열 경고는 보존했으며 추가 원인 진단/모델 수정하지 않았다.

## 3. 실제 측정과 이전 calibration 비교

Post-update 동일 physics step의 pose/root COM→origin velocity/FD/q/dq/graph target을 기록했다. Graph outputs는1308개 frame에서 읽혔으며 velocityCommand와 measured dq는 다른 양이다. ROS command와 physics step은 비동기이므로 command 다음 frame에 아직 이전 target이 남은 경우도 그대로 보존했다. Source/received ROS log, graph target과 actuator joint response를 구분했다.

| 지표 | 이전 calibration | 이번 validation |
|---|---:|---:|
| Root planar peak | .032404730583m/s | **.022805331797m/s** |
| FD planar peak | .030265943315m/s | **.021279668484m/s** |
| PRE_FINAL .03 cap | FAIL | **PASS, 이번 episode 한정** |
| 마지막2s mean actual forward | .018659932364m/s | .015682987583m/s |
| 마지막2s mean ROS wire v | .007792015845 | .006760963271 |
| 이번 마지막2s mean surface request | 이전은 wire와 동일 사용 | .026976243716m/s |
| Front steer mean L/R | 16.720345/13.571946° | 16.722965/13.570772° |
| Moving+decel 구간 yaw 변화 | 1.592932°(이전6s) | 1.244864°(이번6.4s) |
| 정상 감속 요청→첫 zero command | 즉시zero/정상ramp우회 | **.400000021sim s** |
| Zero 후 최대 추가 XY | .009790530547m | **.034127288813m** |
| Zero 후 along 최소/최종 | −.009790488242m | **−.034127288744m** |
| Zero 후 forward 최대 | +.000518505392m | +.000020538077m |
| Zero 후 root/FD speed peak | .014922909/.014790409 | .006236286/.008429888m/s |
| Excursion+1sample allowance | .010039245709m | **.034231226913m** |
| Zero→1s quiet window 시작 | 2.766666811sim s | **미달성** |
| 마지막1s pose span/FD/native | 0/0/0 | 0/0/0 |
| 마지막1s raw root peak | .001828388815m/s | **.002619135991m/s** |
| 마지막1s active wheel dq | 0 | 0rad/s |

새 시도는 명령 peak를 낮췄지만 baseline wake motion, corrective scale, 피드백 supervisory 제한 및 stop profile이 다르다. 같은 요청 v/k와6s 기간만으로 adapter 단독 인과적 성능 개선을 주장하지 않는다. 특히 stop 위치 유지가 개선됐다는 주장은 불가능하다. 두 시도 모두 단일 표본이며 statistical comparison이 아니다.

정상 감속 요청 sim10.516667215, 첫zero10.916667236, 관측종료26.250001369다. 즉 zero 이후 약15.333334s까지 기록했다. 이 추가 구간은 같은 단일 episode의 zero 관측이며 재구동이 아니다. Publisher는 firstzero 이후 약7s까지 지속zero를 발행했고 이어 observerzero로 관측했다. 마지막 actual pose가 고정돼도 raw root 기준을 버리지 않았으므로 **quiet FAIL/base_stop_confirmed=false**다. 2mm/s 기준을 .002619 이상으로 완화하지 않았다. Post-zero 후퇴의 역학 원인을 특정하지 않는다.

최종 actual pose:

- x=−5.76229190826416m, y=3.1642923355102544m, z=.000000684405677m.
- yaw=.06534378620512268rad=3.743923166959°.
- Zero 시점 XY=(−5.728237628936768,3.1665234565734863), yaw=.06535969563288561rad.
- Explicit post-hoc zero-pose hold 기준 goal축 최종 long error **+.034127288744m**, lat+.000002164250m, yaw+.000015909428rad. ±.030m longitudinal에도 실패한다. Calibration에는 사전 FINAL이나 frozen stable6 event가 없으므로 이를 ENG001 terminal success로 평가하지 않았다.

예상궤적 비교는 같은 actual surface-command profile을 unit-speed/no-delay bicycle에 넣었다. Actual과 max XY 차이 **.070626711482m**, yaw **1.678444808903°**다. 예상/실제 좌표는 `expected_actual_trajectory.csv`에 있다. 이전 보고서 .043250628m/.735678520°는 raw wire를 SI speed로 가정한 다른 모델이었다. 그러므로 이 두 residual 숫자의 대소를 성능 개선/악화로 비교하지 않는다. 이번 residual 또한 global gain/lag/error bound가 아니다.

## 4. ENG001 재진입 판정과 필요한 최소 변경

**NOT_READY**, 직접 관측된 단일 원인은 **normal zero-stop 이후 terminal 위치를 예산 안에 유지하지 못함**이다. 실측 후퇴34.127289mm는 전체 longitudinal tolerance30mm보다 크며 기존 nominal FINAL 잔여여유5.119679mm/lat4.580750mm 안에도 들어가지 않는다. Root quiet 미충족 역시 성공을 차단한다. 속도 cap PASS만으로 이 문제를 해소할 수 없다.

기존 nominal fixture gap .195114871m와 clearance requirement .10m는 유지한다. 이번 open-space pulse의 약70.627mm XY/1.678° yaw residual과34.231mm stop estimate를 다른 ENG001 waveform의 확정 bound로 사용할 수 없다. 따라서 fresh predicted corridor/terminal 허용오차를 충족할 근거가 확보되지 않았고 ENG001 실행조건은 열리지 않았다. Actual pallet clearance/FINAL 도달/영상은 이번 범위에서 미실행이다.

필요한 최소 설계 변경은 별도 engineering stopping 계층이 **wheel target zero를 종료로 간주하는 정책을 넘어 actual post-zero pose 유지와 실제 정지 확인을 보장**하도록 하는 것이다. 구체적인 brake/hold actuator capability와 제어 계약이 없는데 보정 목표, reverse, GT, gain fitting 또는 자동 재접근을 넣지 않는다. Frozen terminal controller/연구 protocol은 그대로 두며, 필요한 정지 유지 정책은 별도 결정 대상이다. 이번에는 설계를 추가 구현하거나 재측정하지 않았다. 허용오차·속도·footprint·clearance 완화도 없다. 단일 episode 허용량을 모두 사용했으므로 더 이상의 자동 calibration/retry는 하지 않는다.

## 5. 파일·검사·보존

새 코드:

- `analysis/fe2e_v02_drive_contract_v01.py`: USD-only geometry/connection 근거 추출.
- `scripts/run_fe2e_v02_stopping_validation_v01.py`: 독립domain probe/unique attempt/no-retry supervisor.
- `scripts/fe2e_v02_stopping_validation_session_v01.py`: 기존 demo reference의 새 open-space scene, 안전 boundary/step instrumentation.
- `scripts/fe2e_v02_stopping_validation_ros_v01.py`: 새 stopping adapter와 exact curvature IO를 사용하는 단일 pulse+normal stopping.
- `analysis/fe2e_v02_stopping_validation_metrics_v01.py`: 실제 peak/stop/expected-actual trajectory 집계.

Stopping adapter8/8, 설치 Ackermann numeric3/3 및 physical-radius target roundtrip PASS. 증거/metrics/trajectory/command/ROS/contact/runtime logs는 OUTPUT에 있고 hash inventory는 아래 보고서와 함께 저장했다. 기존 source hash는 실행 전후 대조했고 frozen originals/기존 결과를 변경하지 않았다. Runtime source/adapter/hash와 새 USD도 함께 기록했다. 최종 판정은 연구 success나 navigation readiness PASS가 아니다.
