# 현장 perception → steering approach v14 — 2026-11-01

**NOT_READY / 목표 미달성. Fresh capture PASS, 최신 YOLO+B4+수동 ROI 보조 B5 PASS. 물리 PRE NO, 물리 FINAL NO, 비영 Twist 0. 주행 후 stop NOT_TESTED, baseline quiet PASS, 예상 밖 접촉 0. 최신 Kit exit −9 / runner exit 1.** 자동 팔레트 검출·무보조 접근 성공 주장은 없다. HPO/training PAUSED, 공식 연구 denominator0.

주 차단 원인은 인식·곡선 경로 검사 후 첫 `tick()`의 **`GRAPH_CHANGED`**다. 변경 항목을 저장하지 않아 공급자 graph 변경인지 capture가 추가한 render graph인지 **UNKNOWN**이다. 기존 fingerprint가 현장 전체의 모든 `node:type`를 포함한다는 소스는 확인했다. 보호장치를 해제하지 않았다. 실제 조향 명령·wheel physics 기반 PRE/FINAL 시연은 이번에도 달성하지 못했다.

## 실행과 관측

외부 출력 root는 `/home/user/hh/isaac_cosmos/sdg_final/` 아래다.

| 항목 | `CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v14_02` | `CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v14_03` |
|---|---|---|
| 실제 Kit PID / exit | 1343938 / 0 | 1348954 / −9 |
| 실제 시작 XY(m) | (−25.936516,26.799959) | (−25.887981,27.400135) |
| YOLO confidence | .824668 | .707539 |
| 수동 ROI 보조 B5 | FAIL, 유효 상판점43<100 | PASS,130/130 inliers |
| 중단 | FRESH_PERCEPTION_FAILED | GRAPH_CHANGED |
| driver / nonzero / wheel dq | null / 0 / 0 | null / 0 / 0 |
| 기록 base XY 변위 | 0m | 0m |
| runner | exit1 / NOT_READY | exit1 / NOT_READY |

각 `attempt_0001/`에 RGB/depth/mask/K/extrinsics, frozen model manifest, ROI, steps·contacts, provisional 및 outer final을 보존했다. `_01`은 이전 준비 전용 namespace로 Kit 실행이 없었다. 실제 Kit는 총2회이며 이후 실행은 없다. 명령은 각각 v14 runner `--prepare-only`, `--run --output …v14_02`; v14b runner `--prepare-only`, `--run`이다. Kit Python은 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, ROS Jazzy/domain191. 실행 전 사용자 Kit/training 없음·GPU gate를 확인했고 rustdesk는 보존했다.

첫 초기 배치는 곡선 접근 거리를 확보하려고 고정한 engineering startup이었다. ROI를 넓힌 별도 오프라인 후보도 plane gate에서 실패했으며 기준을 낮추지 않았다. 두 번째는 팔레트 상판의 영상 지지를 확보하는 입력 연결 보정으로 고정 XY(−25.88797768,27.4)를 사용했다. X는 원래 rover baseline에서 가져왔으며 직전 추정 PRE X를 따라 옮기지 않았다. startup overlay만 physics 전에 작성했고 실행 중 pose assignment·teleport는 없다. 이 재배치는 과학 manifest 조건과 별개다. 첫 실패는 수동 ROI/관측 배치 문제였으며 순수 소프트웨어 오류라고 주장하지 않는다.

최신 새 영상의 관측 목표는 PRE **(−25.934821307,28.278040424)**, FINAL **(−25.934821307,29.078040424)**m, yaw90°다. 수동 polygon은 `(236,197),(251,181),(383,181),(403,197)`이며 fresh RGB·overlay를 직접 검토하고 hash로 결합했다. 목표를 GT로 교체하거나 주행 중 재검출하도록 연결하지 않았다.

## 조향 연결과 안전 검증 범위

기존 v13/v12 capture·YOLO·B4/B5와 frozen recipe를 재사용했다. 두 저장 v13 frame의 B5 exact replay, renderer optical transform, right/down/forward world 변환·역변환 PASS; 입증된 좌표 오류가 없어 recipe를 바꾸지 않았다. 결과는 `construction_site_frame_check_20261101_v14.json`에 있다. B4 modulo180 축과 명시적 +90° task face를 구별했다.

새 follower는 measured base XY/yaw와 latch된 world goal로 cubic Hermite 경로를 만들고 feedforward curvature에 cross-track·heading 피드백을 더한다. 기존 `StoppingAdapter`·Governor·`encode_legacy`를 사용한다. 공급자 Twist angular.z는 SI yaw rate가 아닌 기존 조향 인코딩이며 KMAX=tan15°/.7, request≤.02m/s를 유지했다. PRE 물리 stop certificate 후 FINAL을 실제 정지 pose에서 독립적으로 계획·검사하도록 연결했다. 이 전환·명령 발행은 **runtime 미검증**이다.

최신 PRE 경로는 441 poses, 길이 .879498m, 최대곡률 .268572/m로 기존 KMAX 이내다. 실제13 collider에 곡선 yaw/translation 전체 envelope, .10m clearance, tracking .025m/yaw±2°/보간 및 steering 변위 여유를 적용했다. front steering collider의 실제 pivot 기준20° 회전 변위가 .15m 확장 안인지 검사했다. wheel bottom의 곡선 support patch와 실제 PhysX ray **24,300/24,300 PASS**. `leg_0_path.json`, `leg_0_swept.json`, `leg_0_live_support.json`에 원자료가 있다. FINAL 경로는 PRE 미도달로 검사·실행하지 않았다. 실제 곡선 추종·충돌 회피 성공 증거로 해석하지 않는다.

수동 review 대기 중 새 v14 Hermite tangent를 chord×1.2로 보정해 불필요하게 큰 endpoint curvature를 줄였다. 목표·KMAX·안전 한계는 유지했다. `in_session_software_correction.json`과 before/loaded source를 외부 root에 보존했다. **prepare expected hash를 갱신하지 않았고**, 현재 follower hash는 두 준비 기록과 다르다. 최초 executed snapshot과 최종 source를 구분한다. 이 실행을 prepared-code hash 불변 PASS로 보고하지 않는다.

## 종료·검사·남은 조치

두 provisional은 실제 실패를 담는다. 1차 Kit 정상 종료 후 outer final은 MISSING_WITNESS다. 2차는 `SimulationApp.close` 요청 후60초 이상 남아, driver null/nonzero0·observer exit0·소유 PID와 argv를 확인하고 소유 Kit에 SIGTERM, 10초 이상 뒤 SIGKILL했다. 사용자 프로세스·GPU는 건드리지 않았다. `owned_close_watchdog*.json`을 보존했다. Outer final은 KIT_EXIT_NOT_ZERO다.

2차 종료 신호 handler가 `zero_request.json`을 바꿔 provisional evidence 중 **해당 파일 hash 불일치**가 발생했다. 다른 provisional witness는 유지됐다. 이 실패도 숨기지 않는다. 최상위 STOPPED PASS가 나타난 1차 값은 baseline quiet 집계이며 주행 후 stop이 아니다. 결합된 실제 결과는 `_03/engineering_outcome_v14.json`에 있다.

- PASS: 신규 compile, CPU11 tests(곡선 좌우 추종·인코딩·불가능 곡률/추종 이탈 거절과 기존 target/persistence/pause), known lock subset9 hash/count. 전체 formal pairing/readiness 재인증은 하지 않았다.
- FAIL/UNKNOWN: 실제 physical PRE/FINAL, steering runtime, graph 변화의 구체 항목, 최신 Kit 정상 close, 2차 provisional 전체 hash 불변. 사용자 요청의 실제 구동은 미완료다.
- 새 파일: `analysis/construction_site_frame_check_20261101_v14.py`; `evaluation/construction_site_follower_20261101_v14.py`, persistence v14; `scripts/construction_site_{start,perception_session,perception_runner}_20261101_v14.py` 및 v14b, ROS driver/sweep v14; follower CPU test; 본 보고서·latest·PROJECT_STATE. 기존 v01–v13, source USD·HR brick·weights·과학 lock은 수정하지 않았다.
- 실행 뒤 작성한 **미실행** session v14c는 같은 GRAPH_CHANGED 거절을 유지하면서 added/removed/changed 항목을 먼저 저장하고 signal 증거를 별도 파일에 기록한다. compile PASS; 추가 Kit/prepare 없음.

**직접 다음 조치:** v14c의 graph diff를 기존 supplier graph와 비교해 capture가 만든 비구동 render 변경인지 실제 actuator/ROS wiring 변경인지 확정하고, 확인된 capture lifecycle만 수정한다. 안전 fingerprint를 맹목적으로 재설정하거나 전체 guard를 끄지 않는다. 이후 별도 허용된 실행에서 이미 통과한 관측 PRE 곡선에 실제 ROS 조향을 연결해야 한다. 이번 두 번 한도 뒤에는 추가 launch하지 않았다.
