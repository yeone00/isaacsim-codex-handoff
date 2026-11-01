# 현장 perception→approach v12 — 2026-11-01

**새 RGB-D→frozen YOLO→B4→수동 ROI 보조 B5→추정 PRE/FINAL까지 PASS. 실제 접근은 미완료이며 전체 NOT_READY다.** 기존 전진형 탐색기가 허용 경로를 찾지 못해 주행하지 않았다. Kit **1회**, 실제 구동 episode **0회**, 추가 Kit 재시도0. HPO/training PAUSED, 연구 denominator0.

## 실제 관측 결과

출력 root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v12_01`. 원자료는 `attempt_0001/`에 있다. 원본 현장 USD를 sublayer로 사용한 실행 overlay이며 1m/Z, 활성 /Render, 기존 rover/적재물 및 공급자 ROS graph를 유지했다. 원본 USD나 실제 base pose를 직접 변경하지 않았다.

| 단계 | 결과 |
|---|---|
| CAPTURE | PASS, 새 front_rgb.png/npy + front_depth.npy, 640×480 동일 render product |
| YOLO | PASS, frozen HR instance segmentation 1회, brick_load confidence 0.894056618, mask 29588px |
| B4 | 계산 완료, 최종 B4/B5 heading 90.021636963° modulo180 |
| B5/ROI provenance | PASS, 수동 영상 ROI 보조; 자동 pallet segmentation 아님 |
| ESTIMATED PRE/FINAL | 같은 새 RGB-D에서 산출, 아래 좌표 |
| ROUTE | 직선 공간 sweep PASS; 기존 forward R=2.8m 탐색 NO_PATH |
| PRE PHYSICAL ARRIVAL | NOT_ATTEMPTED |
| FINAL PHYSICAL ARRIVAL | NOT_ATTEMPTED |
| POSTZERO QUIET | NOT_TESTED; 무구동 baseline quiet만 PASS, cleanup receipt MISSING |
| PERSISTENCE | close 전 provisional + 실제 Kit exit 후 outer final 생성; 성공 인증은 NOT_READY |

새 카메라 K: fx=fy=317.043120119px, cx=320, cy=240. optical right/down/forward→world extrinsic은 `camera_metadata.json`, raw projection/view는 `camera_params_raw.json`에 저장했다. axial depth 단위 m, renderer extrinsic 교차검사 PASS. `pause_barrier.json`은 4 update 모두 is_playing=False, physical time 4.283333556727s 불변이다. `capture_stability.json`의 capture 전후 base pose와 물리 시간도 같다. 옛 영상을 입력하지 않았다.

수동 polygon `(158,269),(185,239),(444,239),(482,269)`을 새 영상과 `roi_overlay.png`에서 **Codex가 직접 시각 검토**했다. brick 제외/erosion 후 좌우 노출 상판과 얇은 앞 상판 영역에 놓여 있어 이번 frame에서 채택했다. 새로운 사용자 annotation 입력은 없었다. `roi_review.json`에 해당 새 RGB/overlay hash·검토자를 기록했다. 상판 inlier1261/1271, tilt0.080220415°, observed top0.146920474m. 잔차는 한 frame 내부 fit scatter이며 센서 절대 정확도 인증이 아니다.

B5 center=(-25.936516793278, 30.481230052508)m. B4/B5에는 새 depth 역투영과 영상 mask/관측 상판 datum을 넣었다. USD 적재물 좌표/GT를 prediction 또는 driver에 주입하지 않았다. +90° local_-X는 기존 task face policy이며 B4를 task face로 자동 대체한 것이 아니다.

- **PRE = (-25.936516793278, 28.277485021247)m**, yaw90°.
- **FINAL = (-25.936516793278, 29.077485021247)m**, yaw90°.
- 실측 start=(-25.887977600098,28.470867156982)m. PRE는 forward **−0.193382491m**, lateral **+0.048537777m**, 거리0.199380801m다.

## 첫 미해결 차단: 현재 배치의 전진 경로 admission

Kit 안에서는 관측 PRE/FINAL 직선 sweep의 전체 활성 collider·바퀴 support를 검사했고 두 공간 통로는 PASS였다. 그러나 이 사실은 뒤쪽 PRE를 전진 전용 follower로 갈 수 있다는 뜻이 아니다. 실제 세션은 `OBSERVED_PRE_OUTSIDE_EXISTING_FORWARD_DRIVER_ENVELOPE`에서 명령 전 중단했다. 이 assertion으로 작업을 끝내지 않고 같은 Codex 작업에서 기존 `fe2e_v02_demo_reuse_planner_v01.search`로 대안을 실제 계산했다. 기존 world-goal/structured follower는 Goal behind에 reverse fallback이 없다.

최종 근거는 **`existing_forward_route_search_final.json`**이다. 실제 rover 활성 collider13개, 현장 detailed triangle 및 load collider 보수 경계4270개, 원래 floor band 삼각형18900개를 분리했다. 0.10m clearance와 1cm arc sample 사이 최대 이동을 덮는 추가0.012337485m 여유를 썼다. 기존 planner의 R2.8m/0.10m primitive/0.01m sweep/2° state grid를 유지했다. 고정 nominal footprint 수치는 planner 반환 metadata에 남지만 실제 collision oracle는 **13개 실제 collider 각각의 회전·이동 경계**를 사용했다. 116 expansions/5083 collision calls/10.695662s 뒤 **NO_PATH**, path 빈 배열이다. FOUND 후보가 없으므로 path support/runtime admission과 controller 생성은 진행하지 않았다.

대표 spatial conflict: 직진 candidate base=(-25.887971083,29.360867157)m에서 shell expanded bounds X[-26.363625896,-25.410850604], Y[28.705116391,30.013850013], Z[-0.034438743,0.627515326]m가 `Layer_01_A/Bundle_06_R/Brick_05/.../geometry_0`의 X[-25.935500003,-25.745499997], Y[30.005500001,30.062500001], Z[0.145215620,0.235215620]m와 겹친다. 좌우 곡률 primitive도 앞쪽 load clearance에서 차단된다. 뒤쪽 PRE에 도달하려면 방향 전환 우회가 필요하나 이 유한 전진 탐색은 그런 허용 경로를 찾지 못했다. **모든 실제 경로의 불가능/실제 접촉 발생을 주장하지 않는다.**

작은 조정 제안은 관측 PRE의 약0.30m 뒤, 같은 X/yaw에서 시작하는 별도 engineering 초기배치다: 대략 (-25.936517,27.977485)m/+90°. 현 위치 대비 약0.493m 뒤·0.049m 옆이다. PRE→FINAL 목표값·인식 결과는 유지하면서 두 구간을 전방에 두는 안이다. **실제 relocation은 하지 않았고, 변경 배치의 전체 collider/support/새 관측 및 과학적 geometry 승인 검사가 필요하다.** 현재 장면에서 목표를 FINAL로 건너뛰거나 고정50mm 목표로 바꿔 성공 처리하지 않았다.

## 실제 운동·정지·저장

steps records=75, 최대 base XY변위 **0.0m**, joint |dq| peak **0.0rad/s**. 실제 MOVED=NO, 비영 Twist0, driver 생성0. 무구동 baseline quiet1.000000052s/FD0/span0m PASS는 주행 후 정지 성공과 구분한다. baseline strict PhysX support2214/2214 및 shell 검사 PASS. 실제 관측 route의 물리 추종/contact/arrival은 NOT_TESTED다.

`execution_provisional.json`은 close 전에 기록됐고 evidence8개 hash가 일치한다. Kit PID1196128/exit0, shutdown 로그 뒤 outer `execution_complete.json`, root `run_status.json`이 생성됐다. outer status **NOT_READY / MISSING_WITNESS**, runner exit1. adapter command/physical stop certificate/zero receipt/driver completion 등 미주행 witness가 없어서 성공 인증을 거절한 것이다. 성공 조건을 완화하거나 witness를 만들지 않았다. admission 전 종료이므로 cleanup zero receipt도 MISSING이며 guaranteed post-drive stop 검증을 달성하지 못했다.

실제 접근이 없어 접근 동영상은 만들지 않았다. 새 `front_rgb.png`, `detection_overlay.png`, `roi_overlay.png`가 실제 stationary 관측 frame 증거이며 이동 영상으로 부르지 않는다.

## 같은 작업에서 한 수정과 검사

1. 새 v12 pause helper: pause 요청 후 bounded app.update, 실제 playing=False 및 physical clock 3회 연속 안정 확인. timeline reset/guard 삭제 없음. CPU delayed-pause/unstable-clock regression **2/2 PASS**, 실제 barrier PASS.
2. v12 adapter/runner/session은 v11을 새 파일로 재사용했다. 새 RGB-D 뒤 base/clock 불변 검사, fresh ROI 시각 검토 대기와 RGB hash 결합을 추가했다. 도달 불가능한 inherited fixed B/50mm/native driving 본문은 제거했다. 현재 v12 session은 일반 목표 physical follower 통합 완료 코드가 아니며, 이 실행에서 추정 목표를 driver에 전달한 성과는 없다. 또한 재사용한 v10C outer verifier에는 아직 고정 B target 검사가 남아 있어 향후 실제 PRE/FINAL 실행 전 목표별 witness 검증으로 새 버전에서 연결해야 한다. 이번 NOT_READY 판정은 이 검사 이전의 실제 witness 누락에서 내려졌다.
3. 별도 CPU-only route worker 첫 시도는 반복 load mesh triangulation으로100s timeout **FAIL**. 이후 load full AABB로 보수 계산을 줄였다. 두 번째는 거대한 site mesh를 중심거리로 잘못 제외한 것을 발견해 **INVALIDATED**했다. 세 번째는 AABB 교차로 고쳐 site mesh를 포함했고 최종 NO_PATH를 얻었다. 첫 실패와 두 번째 무효 결과를 삭제하지 않았다. Kit 추가 실행0.
4. v12 source py_compile 및 pause unittest PASS. 원본 stage SHA `424cb17b104d7a68a4c264216e38b9823f371524a8704e07fb4eec8b08d1e264` 일치, HR model frozen hash 일치, prepared input 28개 hash 불변, v11 adapter/runner/session3개 원본 hash 불변. 광범위 protocol/53-file 재감사는 반복하지 않았다. Git status는 이 디렉터리에 .git이 없어 exit128이며 commit/push 없음.

신규 source: `scripts/construction_site_perception_{adapter,runner,session}_20261101_v12.py`, `scripts/construction_site_route_20261101_v12.py`, `evaluation/construction_site_pause_20261101_v12.py`, `tests/test_construction_site_pause_20261101_v12.py`. 실행 source snapshot은 root `executed_code/`, source hash/검사는 `v12_independent_checks.json`, 단계 ledger는 `v12_stage_ledger.json`, 시도 이력은 `v12_attempt_corrections.json`이다. 보고서/latest_report/PROJECT_STATE를 갱신했다.

실제 명령은 `python3 scripts/construction_site_perception_runner_20261101_v12.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v12_01` 후 같은 명령의 `--run`이다. Kit runtime은 설치된 hh_isaac51 Python/Isaac Sim5.1, 추론은 기존 sdg_tools Python, ROS는 Jazzy/domain191을 사용했다. 경로 worker는 pxr 라이브러리 경로를 지정한 hh_isaac51 CPU subprocess이며 Kit 세션 수에 포함하지 않는다.

**다음 구체 작업:** 제안 초기배치를 별도 engineering geometry로 승인·검사하거나 현재 배치용 검증된 reverse 접근을 확보한 뒤, 관측 목표→supplier ROS graph의 물리 PRE hold→FINAL→zero/quiet를 연결한다. 현재 상태는 assisted perception 성공 / 실제 접근 미완료다. unassisted full chain에는 pallet ROI 자동 선택·검증도 남아 있다. 별도 formal test admission 전 연구 denominator0을 유지한다.
