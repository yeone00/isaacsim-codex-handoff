# v36 — 공통 smooth-S의 별도 engineering 어댑터와 결정 게이트

2026-11-02 KST. **소프트웨어 연결 가능성 PASS_OFFLINE / 실제 실행 HOLD.** 새 [어댑터](../evaluation/construction_site_common_planner_20261102_v36.py)와 [CPU 검사](../analysis/construction_site_common_planner_checks_20261102_v36.py)를 작성했다. 원래 quintic·driver·controller·stop·USD·weights·locks는 수정하지 않았다. Kit/ROS/비영 명령/센서 획득/추론 실행0. 신규 실제 endpoint0, formal scientific denominator0, HPO/training PAUSED. 이 문서는 v35 DRAFT나 18회 실험을 승인하지 않는다.

## 실제 API 연결과 변경 범위

v30 성공 실행의 `executed_code` follower v19, driver v21, stopping adapter v21, curvature encoder를 정적으로 읽었다. legacy 모듈 import 없이 필요한 순수 함수만 AST로 분리해 CPU 대조했다. 입력은 **관측된 world base_link (x m, y m, yaw rad)** 두 개이며 PRE/FINAL 구분·표현명·task GT는 planner 인자가 아니다. World Z-up, yaw +Z 반시계, x/y 교환 없음. rear=base−.338(cos yaw,sin yaw); 출력 행은 기존 그대로 `[base_x,base_y,body_yaw,rear_k,rear_s]`. 경로마다 처음/끝 heading과 끝 곡률0을 유지한다.

v35 smooth-S 식·epsilon .05·A bracket ±.5·48회 이분법·4001 적분점→매4번째 1001점·wheelbase .7m·15°·.95 admission bound .363645332585095/m을 그대로 복제했다. 모델별 분기·상수·최적화가 없다. plan은 live 관측값을 받을 수 있는 순수 API이며 저장 목표는 테스트 입력에만 있다. 비유한 pose·불가능 목표·곡률 위반은 거절한다.

follower는 rear 최근접 index를 사용하며 보간하지 않는다. 기존 횡오차 .025m/heading2°·feedback 보정 `k_ref−12e−6h`·KMAX clamp·3mm 정상 stop 요청·overshoot gate를 유지했다. **새 candidate에서만** 속도 상한을 `.02/sqrt(1+(.338*k_command)^2)`로 바꿨다. v35 base/rear .02m/s profile과 기존 follower .02 rear 요청의 불일치를 보정한다. 원래 .004 floor/거리 taper는 유지하므로 speed CSV 정속 시간은 실제 follower 시간과 다르다. `profile()`의 별도 열은 nominal time/rear speed/base speed/semantic omega/virtual steer이며 stop·가속 certification이 아니다.

실제 driver는 follower `(v,k)`를 `v*k*COMP`, COMP=π/180 형태로 stopping adapter에 전달한다. 최종 wire는 `abs(wire_v)/.7*tan(radians(atan(.7*k)))`이고 graph의 degree/radian 해석과 invertSteering이 결합된다. angular.z에 SI `v*k`를 직접 넣으면 계약 위반이다. 양·음 k roundtrip과 부호 반전 음성검사를 수행했다. 새 모듈은 publisher/launcher가 없고 `require_live_qualification()`는 항상 거절한다. 기존 driver import를 자동 교체하지 않았다. 다음 연결 patch·정확한 launcher/command는 사용자 승인 이후 별도 검토해야 한다.

## 오프라인 수치와 회귀 근거

최종 [실행기록](construction_site_common_planner_20261102_v36_02/execution.json), [검사](construction_site_common_planner_20261102_v36_02/checks.json), [입력 SHA 대조](construction_site_common_planner_20261102_v36_02/integrity.json), [전체 CSV](construction_site_common_planner_20261102_v36_02/summary.csv), [JSON](construction_site_common_planner_20261102_v36_02/summary.json). 각 표현별 summary CSV/JSON과 9개 trace CSV도 같은 폴더에 있다. `_01`은 첫 검사 완료본이며 삭제하지 않았다. `_02`는 독립 전진·v35 speed/time 대조를 추가한 완료본이다. 새 명령은 아래와 같고 기존 output은 쓰기 전에 거절한다.

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_common_planner_checks_20261102_v36.py reports/<새_미사용_폴더>
```

저장 관측 nominal3과 같은 XY ±10mm 격자를 합친 **27개(저장3+합성24)**이며 신규 관측 표본이 아니다. 별도 exact-PRE→FINAL 합성 직선3개는 실제 PRE 정지 관측을 대체하지 않는다.

|nominal 표현|끝점 수학 오차 mm / °|sample max k / 연속 upper /m|steer upper °|sample steer rate °/s|정속 / taper 명목 s|
|---|---:|---:|---:|---:|---:|
|HR|0 / 0|.247883360 / .247883579|9.843864|28.252114|44.128604 / 57.503672|
|LR|0 / 0|.274096761 / .274096983|10.861225|31.217733|44.191247 / 57.558026|
|GeoCAD|0 / 0|.259815325 / .259815546|10.307769|29.722700|43.978209 / 57.349824|

위 0은 수치 적분 경로의 목표 일치이며 **실제 endpoint 관측이 아니다**. 모든27개 geometry 배열은 v35와 bitwise exact, speed/time은 저장 speed CSV와 tolerance 내 일치했다. finite·양의 rear arc·독립 rear segment 전진·끝 tangent/곡률·같은 admission·원본 command와 speed 외 결과 동일·wire encode/decode PASS. 경로별 min progress/길이/speed/time 및 sample dk/ds를 CSV에 남겼다. 연속 `|dk/ds|` 상한은 `(|A|2π/.05+6|Δyaw|)/L²`, nominal HR35.412840/LR39.131723/CAD37.256834 /m²다. 이에 따른 .02m/s 조향 rate 보수 상한은28.406088/31.389156/29.885231°/s다. **실제 actuator limit NOT_VERIFIED**이며 이 수치를 허용 한도로 만들어 쓰지 않는다.

잘못된 rear/base frame, 반대 조향 부호, unsafe curvature, 뒤쪽 불가능 목표, NaN 입력, live guard 거절 PASS. v35 collision/out-of-map 음성대조와 전체 sweep/support 결과를 hash로 연결해 보존했다. 원래 v35 source recorded SHA·권위 dependency expected SHA를 다시 비교했으며 expected 변경0이다. 개별 snapshot 추가 observed SHA는 독립 expected 인증으로 승격하지 않았다. geometry lock 자체 독립 expected UNKNOWN은 유지한다.

## 안전 판정과 다음 engineering qualification 제안 — 사용자 승인 필수

**PASS_OFFLINE:** 27개 adapted sampled path가 v35와 정확히 같아 동일 static scene/확장 AABB/전체 collider13개·instance-aware front steering4개/5mm support 결과를 재사용할 근거가 있다. v35 각 표현 support973,350/실패0, expanded obstacle 거리 하한 HR .129149/LR .128940/CAD .132583m다. 새 USD/PhysX 검사를 실행한 것은 아니다. sampler rear 간격은 nominal .876–.880mm로5mm 이내다. 독립 경로들의 union을 이어 주행하면 안 된다.

**UNKNOWN/HOLD:** 50ms driver update에서 nearest index가 건너뛰는 구간, 횡/heading 보정과 governor의 실제 속도, BRAKING에서 고정되는 마지막 k가 만드는 이동은 nominal time 배열로 증명되지 않는다. 점별 steer-rate는 feedforward 요구량이며 실제 command rate·조향 torque/지연·slip·contact·settled suspension·PhysX ray/support·정상 stop proof는 LIVE_PHYSX_UNTESTED다. 새 모듈의 시간표로 open-loop 주행하면 검증한 경로와 다른 실행이 된다. offline geometry PASS만으로 nonzero 실행을 허용하지 않는다. 기존 HR quintic 성공은 새 후보의 안전 증거가 아니다.

다음 작업은 **별도 사용자 승인된 engineering namespace의 nominal HR/LR/CAD 각1행, planned3** 제안이다. 아직 승인/시작0이며18-run variance·formal study와 분모를 분리한다. 운영자가 먼저 (1) v35 measurement/planner 정책과 새 candidate speed 계약, (2) 동일3표현 코드·순서·nominal pair와 실패 처리, (3) actuator 조향 rate 근거 및 해당 경계 검증, (4) 실제 driver 연결 diff/발견된 Kit launcher와 정확한 command·새 output·abort 담당자를 승인해야 한다. 이 보고서는 실행 명령 승인 요청이나 실행 허가가 아니다.

승인 후에도 motion 전 fresh live PhysX clearance/contact/ray/support·steering footprint·기존10cm clearance/추종 여유를 재검사한다. fresh capture→v28 count-only ROI preview/단일 finalized 제출→frozen matched M50→fresh B4/B5→observed PRE를 같은 정책으로 사용한다. GT는 입력 금지이며 task-design은 평가에만 둔다. 8GiB GC/+768MiB·TF/GID·BRAKE·zero/quiet limits와 controller settings를 그대로 재확인하고 약화하지 않는다. 실제 steering-rate 근거를 얻지 못하면 motion HOLD다.

각 PRE는 event-aware normal request→BRAKING→output zero→독립 fresh quiet 증명 후 평가한다. 그 **실제 stopped PRE**에서 observed FINAL로 독립 replan/sweep/admission하고 동일 stop 증명을 반복한다. 실제 E−Gobs와 E−Gdesign의 signed long/left/norm cm 및 wrap yaw deg를 별도 기록하고 trace max/RMS·누락·실패도 남긴다. planned3/각 단계 시도/실제 motion 분모와 예외·timeout·종료코드를 보존하며 자동 재시도·표본 교체하지 않는다. 1회 dry-run이나 engineering3으로18회 분산 실험 readiness/통계 power를 선언하지 않는다.

기존 HR FINAL observed .279451cm/design5.523288cm 및 정상 정지 성공, LR/CAD original curvature FAIL와 실제 endpoint NOT_RUN은 불변이다. 새 GT/mAP/독립 metrology를 만들지 않았다. 원본 protocol prelock v01→amendment v03/geometry v02, sample membership/seed/weights/B5/threshold는 변경0이다. 변경 파일은 새 adapter·검사·v36 출력/본 보고서, latest_report 및 PROJECT_STATE다. Git status는 이 폴더에 .git이 없어 실패했으며 stage/push/remote 변경0이다.
