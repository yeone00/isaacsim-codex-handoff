# 현장 perception → approach v13 — 2026-11-01

**NOT_READY. 새 engineering 초기 배치 두 곳에서 fresh RGB-D → frozen HR YOLO → B4 → 수동 영상 ROI 보조 B5 → 새 PRE/FINAL까지 실행했으나, 두 관측 모두 직진 구동 허용 범위를 벗어나 명령 전에 종료했다. PRE 물리 도달 NO, FINAL 물리 도달 NO.** 요청된 물리 접근은 달성하지 못했다. Kit 2회, 비영 ROS 명령0, 실제 구동 episode0, 추가 재시도0. HPO/training PAUSED, 공식 연구 denominator0.

## 실제 출력과 실행

- 1차: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v13_01/attempt_0001/`
- 2차: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v13_02/attempt_0001/`
- 각 root의 `engineering_outcome_v13.json`에 구체적인 차단 이유와 도달 NO를 기록했다. 2차 root의 `evidence_summary_v13.json`은 두 실행 원자료를 읽어 만든 수치·hash 요약이다.
- 명령: `python3 scripts/construction_site_perception_runner_20261101_v13.py --prepare-only`, 같은 runner `--run`; 이후 새 v13b runner로 별도 `_02` namespace에서 각각 `--prepare-only`, `--run`. 실제 Kit Python은 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, ROS Jazzy/domain191이다. 각 root에 command, environment 관련 증거, 코드 hash 및 실행 코드 snapshot을 보존했다.

사용자 Kit/학습 process 없음과 GPU resource gate를 각 실행 전 확인했다. 기존 rustdesk process를 유지했다. Kit PID는 1차1277817, 2차1281693이며 둘 다 exit0/shutdown 로그가 있다. 사용자 process를 종료하지 않았다.

## 초기 배치와 안전

원래 `stage_metrics_1m_z.usda`를 sublayer로 둔 새 overlay를 만들었다. 같은 현장, rover, 팔레트, HR cement 벽돌, /Render와 공급자 ROS ActionGraph를 유지했다. 새 root transform은 stage attach/physics 시작 **전에만** 작성했다. 모든 composed rigid body의 world translation이 같은 delta만큼 변했는지, base yaw가 +90°인지 확인했다. 실행 중 pose 변경, SetWorldPose, teleport, 인공 floor 추가는 없다. 초기 위치로 이동했다고 주장하지 않는다.

| 항목 | 1차 | 2차 |
|---|---:|---:|
| 지정 초기 X,Y(m) | −25.936517,27.977485 | −25.979248789,27.977485 |
| 정착 후 실제 X,Y(m) | −25.936521530,27.977468491 | −25.979246140,27.977462769 |
| 실제 yaw(deg, 근사) | 89.999548 | 90.000185 |
| 초기 전체 collider 검사 | PASS | PASS |
| 실제 stationary PhysX support | 2214/2214 PASS | 2214/2214 PASS |
| shell 바닥 접촉/간격 검사 | PASS | PASS |
| baseline quiet | PASS | PASS |

v12 실제 start (−25.887977600,28.470867157)m 대비 1차는 X 약−0.04854m/Y−0.49338m, 2차는 X 약−0.09127m/Y−0.49338m의 **별도 engineering 배치**다. 연구 manifest/geometry를 수정하거나 향후 네 representation의 표준 초기 배치로 확정하지 않았다. 2차 X는 1차 관측 PRE X에서만 선택했다. 과거 목표는 startup proposal 용도이며 새 run 명령 목표로 재사용하지 않았다.

## fresh 관측 단계

| 단계 | 1차 | 2차 |
|---|---:|---:|
| 새 mounted RGB-D | PASS,640×480 | PASS,640×480 |
| frozen HR YOLO confidence | 0.864772201 | 0.788470566 |
| 선택 mask(px) | 14674 | 14565 |
| B4/B5 최종 heading modulo180(deg) | 90.016624451 | 91.471206665 |
| 수동 ROI 보조 B5 | COMPUTED | COMPUTED |
| 관측 팔레트 plane inlier | 316/316 | 새 plane gate PASS |
| 관측 top(m) | 0.147654397 | 0.147654474 |
| PRE(m) | −25.979248789,28.230225564 | −25.840856779,28.229027866 |
| FINAL(m) | −25.979248789,29.030225564 | −25.840856779,29.029027866 |
| 목표 yaw | 90° | 90° |

각 frame의 RGB/depth/mask/K/extrinsics, renderer calibration 교차검사, 실제 plane fit, 모델/영상 hash를 해당 attempt에 저장했다. capture 전후 pose 및 physics time4.283333557s는 불변이다. YOLO는 각 새 frame에 실제1회 수행했고 frozen checkpoint hash를 확인했다. USD/GT target 좌표를 prediction 또는 driver 입력으로 사용하지 않았다.

Codex가 각각의 새 `front_rgb.png`를 직접 보고 수동 polygon을 지정했다. 1차 `(216,226),(236,205),(412,205),(444,225)`, 2차 `(225,226),(245,205),(422,205),(453,225)`이다. 각각의 새 `roi_overlay.png`도 직접 확인했다. 노출된 팔레트 상판의 좌우 영역이며 brick mask exclusion/erosion을 적용했다. `manual_roi.json`, `roi_provenance.json`, `roi_review.json`에 해당 frame/hash와 검토 근거가 있다. **자동 pallet segmentation 또는 무보조 E2E가 아니다.** Plane scatter는 한 frame 내부 잔차이며 센서 절대 정확도를 인증하지 않는다.

## 차단된 물리 접근

| 구간/증거 | 1차 | 2차 |
|---|---:|---:|
| PRE 전방거리(m) | +0.252756736 | +0.251564651 |
| PRE 측방거리(m) | +0.042729254 | −0.138390172 |
| PRE 방위 오차(deg) | +9.594843 | −28.815787 |
| start→PRE 공간 sweep | PASS, support2862/2862 | PASS,3186/3186 |
| start→FINAL 공간 sweep | PASS,11448/11448 | PASS,11556/11556 |
| PRE physical reached | **NO** | **NO** |
| FINAL physical reached | **NO** | **NO** |
| postdrive zero/quiet | NOT_TESTED | NOT_TESTED |

공간 sweep은 실제 활성 rover collider13개(steer/wheel 포함)와 현장 obstacle/floor를 사용하며 clearance0.10m 및 yaw±2° 여유를 유지했다. 그러나 **대각선 공간 sweep PASS는 그 방향을 +90° 직진 구동으로 추종할 수 있다는 증거가 아니다.** start→FINAL sweep만으로 PRE→FINAL의 순차 실구동 인증을 주장하지 않는다. 두 실행 모두 그 다음 `OBSERVED_FORWARD_STRAIGHT_ENVELOPE` assertion에서 중단됐다.

v13의 구동 admission은 PRE가 앞에 있고 시작 X와 목표 X 차이가≤2mm일 때만 직진 두 구간으로 허용한다. 실제 42.73mm/138.39mm는 이를 초과한다. ±2° heading을 유지하며 약0.252m 전진하는 단순 구간에서 가능한 측방 이동 규모는 약8.8mm이고 이번 오차보다 작다. 이것은 **현재 제한된 직진 구성의 부적합**이며 현장 전체에서 경로가 없다는 증명이나 물리 충돌 발생 증거가 아니다. 실제 obstacle 충돌 때문에 차단됐다고 기록하지 않는다. 후진/큰 선회/global planner/FINAL 건너뛰기로 우회하지 않았다.

2차 시작 X를 42.73mm 줄였는데 새 추정 목표 X는 1차보다138.39mm 증가했다. 관측 heading도90.0166°→91.4712°로 변했다. 두 frame 모두 `b5_center_flip_90=true`지만 그 사실만으로 원인을 확정할 수 없다. 새 배치에서 다시 인식하면 과거 PRE와 같은 X가 유지될 것이라는 가정이 이번 실제 관측에서 성립하지 않았다. ROI plane top은 거의 같았다. GT 비교나 모델 재선정으로 이 값을 고치지 않았다.

## 구동 코드와 timeout 변경의 실제 검증 범위

새 v13 ROS driver는 `live_goals.json`의 관측 PRE/FINAL 두 목표와 leg별 timeout을 읽고, 기존 StoppingAdapter/속도 governor/endpoint freshness를 유지하도록 연결했다. PRE normal brake→실제 confirmed_stop→다음 leg 승인→FINAL normal stop 순서의 session 연결 및 최종 두 관측 목표를 재확인하는 outer helper를 추가했다. 속도 request0.02m/s, 목표오차5mm, yaw±2°, stop 관찰/신선도/접촉 guard는 유지했다. Leg sim bound45/90s, wall bound120/200s, overlay timeline240s, runner620s abort/650s 종료 상한으로 장거리 제한을 구분했다. 실제 guard travel bound1.25m다. 과거 고정 B는 새 성공 predicate에서 제거했다.

**이 코드는 일반적인 lateral/heading 보정 world-goal follower가 아니다.** 같은 X의 +Y 직진 admission 안에서 목표 Y 피드백과 두 구간 전환을 구현한 수준이며, 실제 admission 실패로 driver 생성/명령/leg 전환은 한 번도 실행되지 않았다. 일반 goal follower 통합과 두 구간 실구동 검증을 완료했다고 부를 수 없다. 사용자 요청의 핵심 물리 체인은 미완료다.

prepare metadata에는 과거50mm의 `original_B/max_travel_m/normal_pulse_limit_s/phase_wall_bounds_s` 설명 필드가 잔존한다. 실제 새 코드의 구동 authority가 아니며 이번 명령으로 발행된 적도 없다. `_01/policy_clarification.json` 및 각 root `engineering_outcome_v13.json`에 실제 적용값과 이 한계를 명시했다. 기존 prepare/hash를 사후 수정하여 맞추지 않았다. 실행 코드 snapshot을 보존했다.

## ROS·접촉·Kit 및 외부 저장

두 attempt 모두 records75, 기록 구간 base XY변위0m, 전체 joint |dq| peak0rad/s, 비영 Twist0, driver null, observer exit0이다. 각 contact event168개는 허용된 rover/floor 경로이며 예상 밖 접촉0이다. baseline quiet PASS를 주행 후 정지 성공으로 바꾸어 해석하지 않는다. 주행 후 stop certificate, adapter command log, driver completion, zero receipt는 **실제로 없으므로 생성하지 않았다**. 접근 동영상도 없다.

close 전 `execution_provisional.json`에 실제 assertion/traceback을 기록했다. 두 provisional digest/evidence hash, 준비 input hash는 현재 원자료와 일치한다. 실제 Kit close 뒤 outer가 `execution_complete.json`, root `run_status.json`을 만들었고 필수 motion witness 부재로 **NOT_READY/MISSING_WITNESS**, runner exit1로 종료했다. Kit exit0은 접근 성공이 아니다. 외부 finalizer 이름 문자열은 v10C에서 이어졌지만 실제 사용한 helper는 신규 v13이며 고정 B 목표 검사를 제거한 코드다. Outer가 witness 검사 전에 provisional result를 최종 result로 복사하지 않아 구체적 assertion은 provisional에 남고 final에는 MISSING_WITNESS만 남는 한계가 있다. 이를 숨기지 않고 별도 `engineering_outcome_v13.json`에 결합했다. 기존 final 파일을 덮어쓰지 않았다.

## 변경·검사와 다음 행동

새 코드: `scripts/construction_site_start_20261101_v13.py`/`v13b.py`, perception adapter v13, perception session/runner v13 및 v13b, ROS driver v13, `evaluation/construction_site_persistence_20261101_v13.py`, `analysis/construction_site_approach_evidence_20261101_v13.py`, CPU test v13. 기존 v01–v12 source/output, source USD, weights, scientific protocol 및 guards를 수정하지 않았다.

- 신규 실행 코드 compile PASS. 기존 target/persistence/pause CPU27 tests PASS.
- 새 두-leg outer CPU3 tests PASS: 두 관측 목표 witness 통과, 고정50mm 목표 대체 거절, PRE 미도달 거절. 합성 fixture이며 실제 물리 성공 증거가 아니다.
- Known lock subset9 hash/count PASS. 이 검사만으로 전체 pairing/readiness를 새 인증하지 않는다.
- source site USD와 기존 governor/stopping/guard 등5개 recorded expected hash 재검증 PASS; 모델 hash는 각 worker에서 PASS. 각 실행 prepare inputs 불변/provisional evidence hash PASS.
- 일반 conda Python의 직접 `pxr` 조회는 ModuleNotFoundError로 실패했다. 이후 검증된 USD library 환경을 구성하는 geometry worker/실제 Kit runtime을 사용했다. 설치/업그레이드 없음.
- `git status`는 비Git 디렉터리여서 FAIL. stage/push/publish/remote 변경 없음.

**다음 구체 행동:** 추가 Kit를 시작하지 않고, 보존된 두 frame의 mask/depth와 B4/B5 중간값으로 4.27cm viewpoint 이동에서 추정 중심이13.84cm 반대로 변한 원인을 우선 재현·분해한다. Frozen recipe를 임의 수정하거나 GT 목표로 steering하지 않는다. 이 관측 안정성 문제와 제한된 직진 admission을 해결하지 않은 채 세 번째 spawn 추측을 반복하는 것은 권하지 않는다. 그 다음에 새 버전의 제한된 world-goal 보정과 실제 swept corridor를 결합하고, 독립적인 실행 승인 범위에서 접근을 재검증해야 한다. 현재 요청의 physical PRE→FINAL은 **미달성**, formal readiness도 **NOT_READY**다.
