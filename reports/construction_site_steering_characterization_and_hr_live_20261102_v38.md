# v38 — 정지 조향 characterization 구현 일부 완료, 실제 측정 HOLD

2026-11-02 KST. **HOLD_CHARACTERIZATION_POLICY_UNDEFINED. Kit 0 / chassis motion 0 / stationary steer 시험 0 / driver 0 / retry 0 / research denominator 0.** v37을 재실행하거나 PASS로 바꾸지 않았다. 실제 wheel 응답을 얻지 못했으며 HR PRE/FINAL은 NOT_RUN이다.

단일 진입 blocker는 **정지 조향 시험에 적용할 승인된 실측 조향속도 중단 한계가 확인되지 않은 것**이다. 286.4788818359375°/s joint 설정이나 smooth-S의 요구속도를 허용 실측속도로 바꾸지 않았다. 사용자 지시의 “한계를 발명하지 말 것 / 정책이나 미검증 graph 변경이 필요하면 Kit 0”에 따라 중단했다. 별도 재승인을 요구한 것이 아니라 누락된 수치·출처를 질문했다. 답변이나 시간 경과를 승인으로 간주하지 않았다.

## 이번에 실제 구현·검사한 것

새 [모듈](../evaluation/construction_site_stationary_steering_20261102_v38.py)과 [preflight runner](../scripts/construction_site_steering_preflight_20261102_v38.py)를 작성·실행했다. 원본 stage를 read-only로 열고 anonymous session sublayer에서 정상 articulation controller 3개의 `execIn` 연결을 차단한 뒤, 그 계층만 제거해 graph signature exact 복원을 검사한다. 임시 delta는 증거로 export했지만 원본 USD는 저장하지 않았다. 정상 소유권일 때 test writer 비활성, test 소유권일 때 정상 writer 부재를 강제하는 검사와 timestamp/fsync JSONL 로그, per-wheel target/angle/rate·transform 및 propulsion zero/contact/support/TF/GID/clearance/memory 검사 함수를 구현했다.

**완성된 live 측정 runner는 아니다.** 정책 미확정 상태에서 smooth sweep 수치·setpoint generator·Kit backend/제어권 전환 callback을 연결하지 않았다. source-level exec 차단은 native scheduler나 잔류 actuator target 차단의 증명이 아니다. 측정 함수는 실제 센서/PhysX 데이터를 취득하거나 zero/cleanup을 수행하지 않는다. 임시 supplier를 구현 일부 했다는 사실로 정상 ROS control을 인증하지 않는다.

| 항목 | 새 증거 / 판정 |
|---|---|
| second writer 동시 활성 | CPU 거절 PASS |
| −90°, +90° / NaN target | 각각 CPU 거절 PASS; clamp로 처리하지 않음 |
| 원래 graph 복원 누락 | CPU 거절 PASS |
| 실제 composed stage의 정상 exec edge 재연결 | CPU 거절 PASS |
| 임시 계층 제거 / 원래 graph exact / source stage hash 유지 | PASS_CPU |
| 위 CPU 검사 합계 | 7/7; physical test 7회라는 뜻 아님 |
| 기록된 expected 대비 입력 SHA | 중복 path를 합친 783개, mismatch 0 |
| prelock v01 → amendment v02/v03 + geometry v02 known subset | 9개 SHA 및 108/432 count PASS; 전체 readiness 아님 |
| runner exit | **2, 의도된 preflight HOLD**; live 실패나 PASS로 바꾸지 않음 |
| native sole writer·잔류 target flush·원래 ROS graph runtime 복원 | NOT_RUN / UNKNOWN |
| stationary support/contact/footprint·10cm clearance·brake/zero/quiet | NOT_RUN |
| smooth setpoint / wheel actual rate·tracking·settling/reversal·base transform | NOT_RUN |
| fresh RGB-D 640×480 → HR M50 → B4 → count-preview ROI → B5 | NOT_RUN |
| 실제 HR PRE / 측정 PRE에서 독립 FINAL / 두 정상 stop | NOT_RUN |
| Kit/driver/observer exits | NOT_APPLICABLE_NOT_STARTED; runner exit2와 구분 |
| ROS zero receipt | **MISSING/NOT_APPLICABLE_PRE_DRIVER** |

## 실제 source·ownership 확인

성공 v30의 실제 source는 워크스테이션 `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03/executed_code/` 아래 session v30, driver v21, follower v19, stopping adapter v21이다. stage는 같은 root의 `prepared_site_drive.usda`다. 설치 source는 `/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim/exts/isaacsim.robot.wheeled_robots/isaacsim/robot/wheeled_robots/` 아래 `controllers/ackermann_controller.py`, `ogn/python/nodes/OgnAckermannController.py`를 읽었다. legacy Python import/실행 없이 검사했다.

정상 graph의 controller 3개는 front/rear 구동4개, front steer2개, middle 구동2개를 각각 쓴다. 네 steer joint 모두 angular drive를 갖지만 composed joint에 mimic schema/관계는 없고 정상 graph에서 rear steer target writer는 발견되지 않았다. 따라서 “네 wheel이 동일하게 명령된다”는 전제를 두지 않는다. [joint schema·관계 원자료](construction_site_steering_characterization_20261102_v38_01/joint_ownership.json).

실제 angular drive stiffness/damping/maxForce는 v37 근거의 836.6141357421875/40/200, joint configured cap은 286.4788818359375°/s다. 설치 Ackermann의 rate input은 default0/snap이고 .0157rad deadband·invertSteering=True·wheelbase .7m를 갖는다. 원래 Twist의 v=0 경로는 0 또는 ±90°여서 작은 stationary angle supplier로 사용하지 않았다. v30 session의 `check_graph`는 baseline graph 변경을 거절하므로 기존 session에 direct writer를 끼워 실행하지 않았다. 임시 characterization과 원래 정상 제어의 policy/state 전환은 별도 검증 대상이다.

15° 명령 한계와 독립 측정20° emergency gate, 기존 quiet의 1s/.002m/s/.002m span은 확인했다. 그러나 quiet의 translation 기준을 모든 stationary motion 허가로 해석하지 않았고, stationary yaw/steer tracking 허용오차도 새로운 승인값으로 만들지 않았다. 새 logger의 해당 필드는 authority가 없으면 거절한다. 정책 출처와 관련 source 줄·SHA는 [정책 증거](construction_site_steering_characterization_20261102_v38_01/policy_source_evidence.json)에 있다. 이는 명시된 authority의 제한된 검색 결과이며 workstation 전체에 문서가 없다는 단정은 아니다.

## HR와 다음 port 판정

HR nominal smooth-S 약28.406°/s, LR31.389°/s, CAD29.885°/s는 **기존 계산상의 요구량**이다. 새 실측률은 전 wheel UNKNOWN이다. 50ms 실제 nearest-index/feedback, Ackermann inside/outside 개별 target, deadband 통과, saturation, v21 BRAKING→zero 때의 target 변화와 실제 추종은 NOT_QUALIFIED다. 임시 stationary 시험만 통과해도 정상 ROS route 인증을 대체하지 못한다.

따라서 HR motion을 시작하지 않았다. E−observed/E−design의 signed long/left/yaw 및 norm, QC5mm/2°, main11cm/strict5.5cm, actual track RMS/max, contacts, zero receipts, fresh quiet, RSS/peak/growth/scope는 모두 새 측정 NOT_RUN이다. 예전 값을 새 run의 결과에 채워 넣지 않았다. 8GiB/+768MiB/600s, rear .338m, base/rear≤.02m/s, COMP=π/180, 원래 v21 stopping/TF/GID/union28/native0/6-wheel 정책을 약화하지 않았다.

**다음 작은 단계 하나:** 출처가 명시된 characterization 전용 정책에 실측 rate 중단 한계와 그 한계로 정의한 작은 smooth stationary sweep을 확정한다. 그 전까지 현재 preflight를 반복하거나 Kit를 띄우지 않는다. 정책 확보가 곧 live PASS는 아니며, native sole writer와 복원·stop은 같은 one-shot에서 실제 증명해야 한다.

HR 두 leg와 독립 두 stop이 미통과이므로 **v39 LR / v40 GeoCAD 실행 승인 gate 미충족**이다. HR 성공 후에만 identical policy의 fresh matched LR one-kit을 v39, 이어 GeoCAD 별도 one-shot을 v40으로 정할 수 있다. 이번 LR/CAD 실행0, 표현별 tuning/target 이동/fallback0. original quintic과 제안 smooth-S branch를 별도로 보존했다.

## 교수 브리핑에서 유지할 기존 결과

| 기존 근거 | 변경 없는 해석 |
|---|---|
| v30 HR physical simulator | observed target 기준0.279451cm, design datum 기준5.523288cm; n=1 기술 관측 |
| v31 LR / v32 CAD | old quintic curvature admission FAIL, 실제 motion/endpoint NOT_RUN |
| v35/v36 | offline27case/55,221checks PASS_OFFLINE, 새 실측 아님 |
| v37 | COMPLETE report / HOLD_STEERING_RESPONSE_UNVERIFIED, Kit0/motion0/retry0/science0 |
| v38 | CPU isolation 일부 구현, 정책 부재로 실측0·HR NOT_RUN |

새 HPO는 disconnected-instance bitmap→stock polygon artificial bridge 문제(기존31 low-fidelity 사례)로 여전히 막혀 있다. scale model/explicit occlusion/18·324·432/훈련/확증통계는 실행0. p-value나 통계적 성공률을 만들지 않았다. 2026-11-03 면담 자료의 미래 계획을 완료 성과로 제시하지 않는다.

## 원자료·검사·변경 범위

[raw result](construction_site_steering_characterization_20261102_v38_01/result.json), [negative tests](construction_site_steering_characterization_20261102_v38_01/negative_tests.json), [events](construction_site_steering_characterization_20261102_v38_01/events.jsonl), [783개 expected/observed](construction_site_steering_characterization_20261102_v38_01/integrity.json), [실행 명령·환경·stderr](construction_site_steering_characterization_20261102_v38_invocation.json), [known locks](construction_site_known_locks_20261102_v38.json), [최종 SHA inventory](construction_site_steering_characterization_20261102_v38_final_hashes.json). command의 runtime은 실제 발견한 hh_isaac51 Python+standalone USD libs이며 **SimulationApp/Kit 실행이 아니다**.

새 코드 두 파일 compile PASS. 새로운 stdout/stderr를 삭제하지 않았다. standalone USD는 기존 disabled camera relationship의 out-of-reference-scope 경고를 출력했고 invocation에 보존했다. 부수 `rg`가 잘못된 evaluation geometry 파일 경로에서 exit2인 것도 정책 증거에 기록했다. 이를 physical 시험 실패·재시도로 합치지 않는다. 기존 raw 전체를 새로 재해시했다는 주장은 하지 않으며, 비교한 dependency 범위는 integrity에 명시한다.

변경은 새 v38 코드2개·보고서/증거, `reports/latest_report.md`, `docs/PROJECT_STATE.md`다. 원본 source/locks/weights/USD 및 v30–v37 성공·실패 출력 수정0, 설치0, 기존 process 종료0, GPU작업0. GitHub handoff는 완료 메시지의 marker로 요청하며 원격 동기화 완료를 로컬에서 주장하지 않는다.
