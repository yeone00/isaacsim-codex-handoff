# 현장 단일 로버 v03 — geometry 오탐 수정, 실제 Kit 1회 / 명령 전 중단

2026-11-01 KST. **v02의 거대 AABB 차단은 제거했다. 실제 Kit 한 세션을 실행했으나 baseline `CLOCK_NOT_ADVANCING`에서 실패했다. 물리 forward+stop milestone은 달성하지 못했다.** 재실행하지 않았다.

| 항목 | 결과 |
|---|---|
| 충돌체별 오프라인 geometry / graph admission | PASS |
| 실제 Kit launch | 1회, headless / 로컬 hh_isaac51 runtime |
| 비영 명령 / actual drive attempts | 0 / 0 |
| MOVED / STOPPED | NO(구동 미시도) / NOT_TESTED; QUIET NOT_READY |
| CONTACT | 관측됨: 여섯 바퀴 및 차체 shell–현장 mesh, 총 168 events |
| PhysX swept support raycast | NOT_RUN — 선행 clock gate 실패 |
| 실제 실행 판정 | FAIL / NOT_READY, `CLOCK_NOT_ADVANCING` |
| 연구 denominator / HPO·training·B300·E2E·432 | 0 / 미실행, HPO PAUSED 유지 |

## 좁은 변경과 오탐 교정

새 파일은 `scripts/construction_site_drive_geometry_20261101_v03.py`, `construction_site_drive_runner_20261101_v03.py`, `construction_site_drive_session_20261101_v03.py`, `construction_site_drive_geometry_checks_20261101_v03.py`다. v02 runner/session을 복사해 geometry import와 v03 경로를 연결했고, session에는 비영 명령 전 정지 PhysX 지지 검사만 추가했다. 기존 v02 ROS pulse·세 articulation controller·stopping adapter·endpoint guard를 그대로 재사용한다. 원본 USD/연구 controller/ActionGraph 원본/모델/기존 출력은 수정하지 않았다.

전체 visual subtree AABB를 충돌 판정에서 제거했다. 활성 collider마다 world 3D AABB와 개별 반경을 사용해 원래 guard 범위인 역방향 .05m~전방 .15m, yaw ±2°, clearance .10m를 보수적으로 확장한다. yaw 변위 상계는 `2*r*sin(1°)`다. site geometry와 Z 교차부터 검사하고 그 다음 XY를 검사한다. mesh는 각 world triangle과 pair·원래 bounds·swept bounds·겹친 Z를 기록한다. 높은 collider가 실제 활성인 경우에도 이 알고리즘에 포함된다.

**입력 설명과 로컬 권위 자료의 차이:** 원래 robot asset의 Cube는 collision/rigid body `True`지만, 실제 site composition에서 더 강한 `construction_scene_robot_task_rover_smoke_v03.usd` override는 둘 다 `False`다. source property stack을 확인했으며 v02의 기존 collider inventory에도 Cube가 없다. 현재 source/의존성 42개 expected hash는 실행 전후 일치한다. 따라서 이 현장에 적용되는 composed 값은 False다. 이번 작업에서 Cube를 끈 것이 아니다. Cube Z[9.49164806,10.49164806]와 비활성 상태를 inventory에 보존했고, Cube를 참조하는 joint는 0개였다. 원격 질량/constraint가 활성인 증거는 없다. rolltainer/caster collision 10개도 원래 비활성이며 삭제·활성화하지 않았다. 활성 로버 collider는 13개다.

v02는 이러한 visual/비활성 bound까지 묶어 높이3.623–3.652m의 site triangle 8개를 차단했다. v03에서는 그 높이에 활성 로버 점유가 없어 해당 차단이 없다. synthetic USD 회귀검사에서 **활성 high Cube–3.65m triangle은 분리**, **활성 high Cube–10m triangle은 차단(Z 교차 [10,10])**됨을 검증했다. 실제 upper 장애물을 무조건 제외하는 수정이 아니다.

바닥은 빈 공간을 포함하는 31×31 expanded box 대신, 실제 활성 cylinder 바퀴의 변환된 최하단 접촉선에서 축 방향 세 점을 채취했다. 여섯 바퀴×41개 travel 위치(5mm 간격, -.05~+.15m)×yaw -2/0/+2°×접촉선 3점=2,214개다. 명목 start와 .05m endpoint도 포함한다. 비활성 caster는 별도 inventory로 남겼으며 지지 역할을 가정하지 않았다.

첫 `prepare_0001`은 기존 “triangle 높이차<.005m” 분류를 유지해 floor 부근 pair20/지원 누락827을 기록했다. 이는 실제 미지지 확정이 아니다. 원본 floor 높이 band [-.03,.02]m는 유지하면서 triangle의 작은 경사/분할에 따른 flatness 조건을 제거하고 실제 표본 높이와 비교했다. wheel bottom 약 -8.35mm인 원본 기하를 기준으로 10mm 내 표면 교차를 요구하며, 이를 물리 인증으로 간주하지 않는다. 최종 `prepare_0003`은 pair0/지지 누락0이다. 연속 정확 충돌·traction 인증이 아니라 보수적 장애물 AABB 및 이산 지지 검사다.

모호한 mesh 지지는 비영 명령 전에 **진짜 PhysX raycast_all로 동일 2,214점의 site surface를 검증하고, 여섯 바퀴 각각의 실제 floor contact가 있어야 통과**하도록 추가했다. 바닥 예외는 원래 floor band 안에 한정된다. 실제 실행에서는 clock gate가 먼저 실패해 이 raycast 검증에 도달하지 못했다. 초기 geometry PASS를 실제 지지/비침투 PASS로 승격하지 않는다.

## 실제 한 세션의 결과

외부 출력 root:
`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v03/`

실행 명령:
```bash
python3 scripts/construction_site_drive_runner_20261101_v03.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v03/prepare_0003
```

실행 전 Kit/학습 후보0, GPU compute는 기존 rustdesk PID953930/535MiB뿐이었다. domain191 probe·입력 hash 검사 후 Kit을 한 번 열었다. `/Render`, 원래 site floor, 1m/Z 및 source sublayer를 유지했다. 새 EngineeringFloor/teleport는 없다. 종료 후에도 Kit/학습 후보0이며 사용자 프로세스를 중지하지 않았다.

180 settling updates 후 baseline75와 exception_zero120, 총195개 telemetry를 보존했다. baseline 마지막30행의 timeline 차이가 필요한 .4s를 충족하지 못했다. 전체 기록 time은 약 0.000000161~0.033333657s 범위에서 **78회 감소**했다. 반면 ROS TF stamp는 약6.2833s였다. source stage는 start/end time code 모두0, FPS/timeCodesPerSecond24다. 짧은 stage 구간 looping 또는 clock 선택 문제가 의심되지만 직접 원인을 확정하지 않았다. 원본 timing을 바꾸거나 연구 gate를 낮춰 재시도하지 않았다.

첫/마지막 기록 pose XY는 (-25.8879776001,28.4708671570)로 같았고, 기록 구간 signed forward displacement0m였다. 이는 명령 주행·정지 후 drift 수치가 아니다. 기록 최대 planar COM .000388869m/s, root-origin .000394140m/s, FD0m/s지만 clock이 비단조이고 유효한 연속1s 관측이 없어 **정지 PASS는 아니다**. joint q/dq·graph targets는 `steps.jsonl`에 있다. 이전34.127288744mm retreat/quiet FAIL은 해결되지 않았다.

접촉은 여섯 바퀴 각각24 events와 `base_link/collisions/gl_shell/mesh`–현장 mesh24 events다. 후자는 차체 접촉이므로 실제 penetration/접촉 위치 확인이 필요하다. callback은 collider pair/point count만 기록했으며 contact 위치·힘·침투 깊이는 확보하지 못했다. floor support 전체/안전 traction 인증은 UNKNOWN이다.

ROS에는 TF publisher1, cmd subscriber2(observer 포함), cmd publisher0, 관측 command0이 있었다. 이름·GID·phase 자료는 `ros_status.json`, `ros_observed.jsonl`에 보존했다. driver discovery/nonzero admission 이전에 실패했으므로 publisher guard 실패로 오분류하지 않는다. zero_request/abort 파일 및 graph zero cleanup 경로를 실행했지만 ROS zero publisher는 시작되지 않았고 `zero=NOT_READY`다. 실제 postzero ≥1s hold와 endpoint 성공은 미검증이다.

**주의할 실제 실패 기록:** native Kit shutdown과 외부 runner의 OS exit code는0이었지만 `execution_complete.json`과 `run_status.json`은 `NOT_READY/CLOCK_NOT_ADVANCING`이다. 성공으로 세지 않았고 `final_verification.json`에 normalized FAIL로 명시했다. 원시 status/exit를 덮어쓰지 않았다.

## 검사·보존·다음 행동

- Python4개 compile PASS. 작은 USD 높이 분리/진짜 upper 충돌/비활성 구분 회귀검사 PASS.
- prepare0001 FAIL 진단 보존, prepare0002/0003 offline PASS. 첫 worker 환경의 libusd_tf.so 누락과 출력 parent 미생성 오류도 `early_failures.json`에 보존; Kit 미실행 오류다.
- 재사용 source42개 hash 전후 PASS, 실행 input hash 재검사 PASS. 준비 overlay의 graph 밖 property0, Cube joint reference0. 전체 속성 직렬화/대용량 복사 없음.
- 핵심 증거: `source_property_authority.json`, `source_physics_inspection.json`, `source_joint_and_overlay_check.json`, `geometry_regression.json`, `source_hashes_after.json`, `runtime_summary.json`, `final_verification.json`; 실제 실패는 `prepare_0003/attempt_0001/` 및 `run_status.json`.
- `reports/latest_report.md`는 시작 시 없었으며 이번 v03 보고서와 같은 내용으로 생성했다. PROJECT_STATE에 이번 실패를 추가했다.

**다음 구체적 작업은 기존 session의 timeline/ROS physics clock 불일치와 shell–floor contact를 정지 상태에서 확인하는 좁은 수정이다.** 단조 clock/실제 ≥1s baseline, PhysX support 및 차체 비침투가 확인된 후에만 새 승인 범위에서 단일 forward+stop을 진행할 수 있다. 현재 motion milestone 미달이며 broad audit/아키텍처 재설계/연구 실행으로 확대하지 않았다. 연구 denominator0을 유지한다.
