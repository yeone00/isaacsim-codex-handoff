# v37 — 승인된 HR smooth-S의 실제 조향 게이트 판정

2026-11-02 KST. **HOLD_STEERING_RESPONSE_UNVERIFIED. HR live pilot은 실행하지 못했다. Kit 0 / motion 0 / retry 0 / confirmatory science denominator 0.** 사용자 실행 승인은 유효하며 추가 승인을 요청하지 않았다. 실제 configured bound는 찾았으나, 그것을 smooth-S 추종 능력으로 해석할 수 없고 동일 원래 ROS supplier에서 안전한 작은 stationary steering 시험 입력을 만들 수 없다는 구체 근거가 확인됐다. 허용속도를 발명하거나 rate limiter/graph를 바꿔 이동하지 않았다.

교수 면담용 [전체 연구·통계 계획](professor_briefing_research_and_statistics_plan_20261103_DRAFT.md)은 완료했다. 모든 미래 결과 칸은 PLANNED/NOT_RUN이고 p-value·새 실험 성과는 없다.

## 실제 확인한 설정과 실행 코드

v30 성공 root `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03`의 실제 `executed_code` driver v21/follower v19/stopping adapter v21/runner/session을 정적으로 읽고, prepared stage를 **standalone USD**로 합성했다. legacy script import/Kit 실행 없이 조사했다. [원자료 JSON](construction_site_steering_gate_20261102_v37_01/steering_evidence.json)에 네 joint 전체 attribute·authored 여부·source layer, graph 연결, 코드 SHA, 환경/명령을 저장했다.

|실제 설정|로컬 값|판정|
|---|---:|---|
|네 steer joint `physxJoint:maxJointVelocity`|286.4788818359375 degrees/s ≈5 rad/s|설정된 joint 상한 확인; 그 속도로 원하는 각을 추종한다는 보장 아님|
|angular drive stiffness/damping/maxForce|836.6141357421875 / 40 / 200, force drive|설정 확인; 실제 부하·타이어 접촉 하 응답 UNKNOWN|
|joint lower/upper|약 ±52°|실험 허용 조향15°/기존 측정20° gate를 확대하지 않음|
|Ackermann `maxSteeringAngleVelocity`|5 rad/s|이 값만으로 slew 제한이 작동한다고 판단 불가|
|`steeringAngleVelocity` input|연결/작성값 없음; 설치 database 기본값0|실제 controller는 0일 때 target angle 즉시 변경 분기|
|`invertSteering` / wheelBase|True / .7m|원래 graph 보존|
|원래 driver|50ms, `v*k*COMP`, COMP=π/180 → v21 stopping adapter|SI `v*k`를 wire angular.z에 바로 넣지 않음|

Angular joint velocity의 USD 단위는 degrees/s다. 상한은 solver가 넘지 않도록 제한하는 값이며 achievable tracking certificate가 아니다. [NVIDIA PhysxJointAPI 정의](https://docs.omniverse.nvidia.com/kit/docs/omni_usd_schema_physics/latest/physxschema/class_physx_schema_physx_joint_a_p_i.html).

설치 `AckermannController.forward` 및 Ogn database를 읽었다. rate input 0이면 `steering_angle=command[0]`이고, max rate5는 이 snap 분기를 연속 변화로 바꾸지 않는다. [AST-only CPU 검사](construction_site_steering_gate_20261102_v37_01/cpu_counterexample.json)는 ±.2rad(각11.46°) target을50ms 간격으로 주면 virtual target 변화율8rad/s가 됨을 재현했다. **실제 wheel이8rad/s 움직였다는 결과가 아니다.** controller에는 |angle|<.0157rad에서 wheel target0으로 만드는 분기도 있어 nominal smooth geometry만으로 graph target rate를 보장하지 못한다.

원래 graph는 `atan2(−.7*angular.z, abs(linear.x))`의 degree 결과를 steering input으로 보낸다. v=0에서 z=0이면0, z≠0이면±90의 입력이 된다. 따라서 원래 wire 경로로 ±수°의 bounded stationary 조향 sweep을 지정할 수 없다. v36 encoder도 v=0일 때 z=0을 반환한다. angle clamp를 믿고±90 입력을 보내거나, articulation target에 직접 쓰거나, graph에 새 supplier를 넣는 시험은 이번 보존 조건의 독립 안전 입증이 없어 실행하지 않았다. 작은 조향을 시험하려고 base를 먼저 움직이는 것도 사전 rate gate를 우회하므로 하지 않았다.

HR nominal feedforward28.406°/s는 요구량일 뿐이다. joint 상한286.479°/s보다 작다는 비교는 **필요조건 일부**이며, 50ms nearest-index·feedback·deadband·BRAKING·개별 Ackermann wheel 차등각을 포함한 실제 tracking 및 rate 검증을 대체하지 못한다. 이 결론은 “조향이 물리적으로 불가능하다”가 아니라 **현 입력 계약에서 사전 qualification 근거가 부족하다**는 뜻이다.

## 확인 결과와 미실행 단계

|항목|이번 결과|
|---|---|
|v30 prepared input + v36 authoritative expected SHA 대조|1,118 참조 비교, mismatch0. 중복 포함이며 독립 파일1118개라는 뜻 아님|
|v36 CPU 회귀 새 output|27case / 55,221 checks PASS_OFFLINE, exit0|
|원래 v21 정지 CPU 검사|20/20 PASS, exit0; 실제 새 PRE/FINAL 정지 아님|
|base108/execution432|108/432행, exact base IDs, 4표현/base·각108 PASS|
|실제 새 joint response / live steer rate|UNKNOWN / NOT_RUN|
|v37 fresh RGB-D·HR M50·B4·count-preview/ROI·B5|NOT_RUN|
|새 PhysX28/native0·6wheel support/contact·clearance·TF/GID·memory admission|NOT_RUN; v30 PASS를 새 live PASS로 복사하지 않음|
|새 PRE/FINAL sweep·drive·BRAKING→zero→독립≥1s quiet|NOT_RUN|
|endpoint E−Gobs / E−design, signed long/left/yaw, tracking max/RMS|NOT_RUN; 숫자 생성0|
|새 RSS/contacts/Kit·driver·observer·runner exit|NOT_RUN; 위 CPU process exit와 구별|
|ROS zero receipt|**MISSING/NOT_APPLICABLE_PRE_DRIVER**|

새 [CPU 회귀 폴더](construction_site_common_planner_checks_20261102_v37_01/execution.json), [manifest·검사 기록](construction_site_steering_gate_20261102_v37_01/manifest_and_checks.json). geometry lock 자체의 독립 expected UNKNOWN은 그대로다. 이번에는 전체 geometry join 재감사를 반복하지 않았고 기존 authority와 새 count/pairing 확인의 범위를 구분한다.

개발 실패도 보존: 첫 v37 AST harness는 mock Base 생성자의 positional `name` 지원 누락으로 exit1이었다. legacy controller 문제가 아니며 새 harness만 수정 후 PASS했다. 실패 내용은 manifest_and_checks에 남겼다. 부수 `rg`는 존재하지 않는 `extsPhysics` 경로 검색에서 exit2였고, 설치 code와 공식 schema 문서로 단위를 확인했다. 둘 다 Kit/live 실패나 retry로 합치지 않는다.

## 변경 범위와 바로 다음 작업

새 코드: `analysis/construction_site_steering_gate_20261102_v37.py`, `analysis/construction_site_steering_cpu_20261102_v37.py`. 새 보고서2개·증거/CPU 폴더2개, latest_report와 PROJECT_STATE 갱신. **안전한 live bridge 준비 완료로 주장하지 않으며 새 driver/runner는 만들지 않았다.** raw Kit output root도 없다. 원래 quintic/HR weights/USD/protocol·기존 v30 성공/v31·v32 실패·v35 제안18행은 수정하지 않았다. HPO/training/scale-model/18회/324·432 실행0, GPU job0.

다음 최소 기술 작업은 작은 stationary steering 명령을 별도 characterization 모드에서 만들되 sole writer·base zero·contact/support·20° 측정 gate·footprint·원래 graph 복원과 fail-closed stop을 증명할 계측 연결이다. 이것은 graph/actuator 입력 경로를 다루므로 v37에서 검증 없이 끼워 넣지 않았다. 이 characterization과 50ms 실제 command/개별 wheel rate·tracking admission을 확보한 뒤에만 v30 실행 snapshot의 copy-on-write session/driver에 v36 `plan/command`를 연결한다. rear .338m, base/rear≤.02m/s, COMP/invertSteering, v21 stop, clearance .10m, GC8GiB/+768MiB를 유지한다. fresh PRE와 실제 stopped PRE→fresh 독립 FINAL을 각각 plan/sweep/stop한다.

HR smooth-S가 아직 통과하지 않았으므로 **LR/GeoCAD live port는 이번에 진행하지 않는다.** HR가 두 leg·두 독립 stop·안전/종료를 통과한 이후의 최소 port 범위는 동일 코드/정책에서 selection·matched model·asset metadata만 LR로 바꾸는 fresh one-shot, 그 결과를 보존하고 동일 GeoCAD one-shot이다. 표현별 planner tuning·HR rescue·자동 retry를 추가하지 않는다. 기존 HR FINAL 관측목표 .279451cm/design5.523288cm와 LR/CAD 원래 curvature FAIL은 불변이다.
