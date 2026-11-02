# v35 — 전향 측정 정의와 공통 안전 경로의 오프라인 가능성

2026-11-02 KST. **개발 단위 완료.** 원래 quintic의 HR 통과/LR·GeoCAD 거절을 재현했다. 별도 고정 smooth-S 후보는 같은 저장 start/goal/yaw에서 **3/3**, 각 표현의 world XY ±10mm 3×3 격자에서 **27/27** 곡률 한도와 강화된 오프라인 전체 collider/sampled-support 검사를 통과했다. 실제 안전 주행의 입증은 **조건부 / LIVE_PHYSX_UNTESTED**다. Kit/ROS/추론/학습0, formal science denominator0, HPO PAUSED. 기존 실패와 endpoint를 소급 변경하지 않았다.

## 측정 계약과 다음 표본

[PILOT-only measurement amendment DRAFT](../docs/construction_site_pilot_measurement_amendment_DRAFT_20261102_v35.md)에 프레임·부호·stage schema·실패 분모·부모 SHA를 명시했다. task-design pallet/support 원점 D, authored visible load AABB 중심 V, B5 assumed rectangle 중심 B, 관측 목표 Gobs, 실제 physics endpoint E를 구별한다. D는 독립 metrology로 검증한 sensing GT가 아니며 V로 바꾸지 않는다. v34의 전방503.5mm 대 가정475mm 차이−28.5mm, side quantile의46.7–52.9mm 안쪽 위치는 그대로 모델/관측·datum 관계의 설명이다. 치수/분위수/GT 보정은 없다.

World m/Z-up, task yaw+90°, +long=+Y/+left=−X, 오차=estimate 또는 endpoint−reference, cm=100m. B4 축 heading은 wrap180, 방향을 가진 endpoint/명령 yaw는 wrap360이다. B5 heading과 고정 goal yaw90°를 혼동하지 않는다. 기존 PRE/FINAL offset2.203745031260775/1.403745031260775m·성공 thresholds·카메라/ROI/model/원래 planner/controller는 불변이다.

후속안은 [구체 manifest 초안](../manifests/construction_site_paired_variance_PROPOSED_20261102_v35.json)의 **3 viewpoint 셀×반복2×3표현=18 planned pilot**이다. nominal과 base X ±.050m의 명시된 새 viewpoint 셀, seed261022/261023, 고정 camera mount/cement300/4층/추가occluder0, 공통 ROI 정책을 선언했다. 이 pose/seed 변경은 **미승인 전향 설계**이며 기존 nominal을 바꾼 것이 아니다. pair 안에서는 모든 조건을 공유하고 결과에 따라 셀/순서/표본을 교체하지 않는다. 먼저 반복분산·scene 효과·단계 실패를 측정하고, 과학적 최소중요차·alpha/다중비교·목표 power·clustering/missingness를 정한 뒤 통계 표본수를 계산한다. 18회로 신뢰도/검정력을 주장하지 않는다. 원래 planner baseline과 대안 arm을 별도 namespace/분모로 둔다.

## 저장 세 행: 수정 없는 측정 예시

[원래 3행 JSON](construction_site_prospective_planner_20261102_v35_07/historical_stage_rows_UNMODIFIED.json)은 v33 저장 내용을 값 변경 없이 보존한다. [간결 stage CSV](construction_site_prospective_planner_20261102_v35_07/stage_example.csv)와 [JSON](construction_site_prospective_planner_20261102_v35_07/stage_example.json)은 그 값의 평가용 펼침이다. 새로운 관측이 아니다.

|표현 (각 n=1)|detector/B4/B5|GT mask IoU/AP/mAP|B5 long / left cm|B4 축 오차°|원래 admission|실제 motion/PRE/FINAL|
|---|---|---|---:|---:|---|---|
|HR_Scan|PASS|UNAVAILABLE|−2.721454 / +4.682131|+.011093|PASS|실행·독립 정상정지 PASS|
|LR_Scan|PASS|UNAVAILABLE|−2.700578 / +5.183266|−.005779|FAIL: CURVATURE_INFEASIBLE|NOT_RUN|
|GeoCAD|PASS|UNAVAILABLE|−3.064894 / +4.870526|−.546102|FAIL: CURVATURE_INFEASIBLE|NOT_RUN|

|HR 실제 측정|observed-goal 거리 cm / yaw°|task-design 거리 cm / yaw°|normal zero 뒤 fresh quiet|
|---|---:|---:|---|
|PRE|.288352604 / −.037820318|5.572512493 / −.037820318|PASS /1.000000052s|
|FINAL|.279451388 / −.039722360|5.523288386 / −.039722360|PASS /1.000000052s|

각 reference의 signed long/left 및 physical pose는 CSV/원본에 있다. HR FINAL의 기존 posthoc task-design strict FAIL/main·relaxed PASS도 불변이다. LR/CAD endpoint 거리·yaw·normal stop은 모두 **NOT_RUN**이다. HR tracking max/RMS는 이 표에서 새로 집계하지 않아 `UNAVAILABLE_NOT_AGGREGATED_HERE`이며 원래 QC PASS를 수치 대신 대입하지 않았다. LR/CAD tracking도 실제 trace가 없다. confidence .791759/.972648/.959305는 정확도/mAP가 아니다.

분모는 historical detector/B4/B5 3/3, 원래 planner admission1/3, motion시작1/3, 실제 PRE/FINAL·독립 정지1/3 planned 및1/1 motion이다. offline replay27(저장목표3+합성24)은 신규 observation0, variance pilot18은 NOT_RUN, confirmatory0이다. FAIL은 실제 gate 실패, NOT_RUN은 미시도, UNAVAILABLE은 라벨/평가자료 부재로 분리한다. terminal error/timeout을 분모에서 삭제하지 않는다.

독립 segmentation GT pipeline은 **아직 구현 필요**다. detector/ROI/target/controller와 분리해 저장 RGB hash에 연결한 instance/class/occlusion·ignore 라벨을 독립 annotation/review로 생성해야 한다. 실제 라벨이 생긴 뒤에만 one-to-one class matching과 IoU .50:.05:.95/COCO101 recall의 class AP/mAP를 집계한다. v25의 semantic annotator 추가로 actuation graph가 변형된 실패를 우회하지 않으며 GT를 actuation graph나 perception 입력에 공급하지 않는다. 현재 labels/mAP/정확도 IoU를 생성·추정하지 않았다.

표현별 frozen matched M50와 수동 ROI를 포함한 전체 pipeline estimand다. 순수 geometry 효과·독립 sensing metrology·일반 신뢰도는 UNKNOWN이다. 과거 reviewer는 HR `Codex-visual-review-v30`, LR/CAD `Codex-visual-review-v28`로 다르다. 이번 machine replay/check의 코드 SHA와 human protocol approval PENDING을 구분하며 독립 인간 검토가 완료됐다고 하지 않는다. LR은 독립 저감 acquisition 재구성이며 red-only real validation을 cement/실로봇 배포로 확장하지 않는다.

## 원래 계획과 공통 후보

실행 snapshot의 원래 `plan` 함수만 AST 추출했다. strict는 원래 예외를 보존하고, 진단 사본만 curvature 예외 하나를 제거한다. HR 저장 leg0 전체 배열은1e−12 이내 일치한다. 별도 선형방정식으로 6개 Hermite endpoint 조건을 풀어 세 원래 peak를 독립 재현했다. 원래 rear offset .338m, wheelbase .7m, steering15°, bound=.95 tan15°/.7=**.363645332585095 /m**, forward-distance .05…3m를 유지했다. 후보는 원래 동일 start에서 **perceived** PRE에 도달하며 yaw90°와 endpoint 곡률0을 보존한다. task D/V/GT는 후보 생성에 들어가지 않는다.

접선 길이81개+endpoint-null shape16개의 작은 다항식 탐색은 LR을 통과시키지 못했다([완료된 제한 탐색](construction_site_prospective_planner_20261102_v35_03/comparison.csv)); 이는 해당 scope의 NO_PATH_FOUND_WITHIN_SEARCH이며 전역 불가능이 아니다. 최종 후보는 별도 고정식 smooth continuous-curvature S primitive다. 표현별 parameter tuning 없이 동일 epsilon .05, amplitude bracket [−.5,+.5], bearing 이분법48회, 4001점 적분을 사용한다.

u=s/L, f(u)=tanh(sin(2πu)/.05), H(u)=∫f du. θ(u)=θstart+Δθ(3u²−2u³)+A H(u), k=(A f+6Δθu(1−u))/L. H(1)의 수치잔여만 적분 정합을 위해 제거했다. 목표 rear displacement의 bearing으로 A를 결정하고 L=distance/|∫exp(iθ)du|로 끝점을 맞춘다. 양의 rear 속도와 시작 방향의 양의 progress를 검사하며 reverse/cusp/teleport가 없다. curvature는 연속이고 양 끝0이다. **연속구간 전체의 보수적 상한 (|A|+1.5|Δθ|)/L**로 admission한다. 8001점 적분과 endpoint/yaw/curve를 교차 확인했다. 일반 장애물 우회나 전역 완전성은 주장하지 않는다.

|표현|원래 max k /m · margin|공통 후보 k 상한 /m · margin|rear/base 길이 m|steering 상한°|명목 PRE 시간 s*|확장 sweep 장애물 거리 하한 m**|
|---|---:|---:|---:|---:|---:|---:|
|HR_Scan|0.350094192 / +0.013551141|0.247883579 / +0.115761753|0.879589/0.882572|9.843864|44.128604|0.129149|
|LR_Scan|0.387170521 / -0.023525188|0.274096983 / +0.089548350|0.880176/0.883825|10.861225|44.191247|0.128940|
|GeoCAD|0.366967770 / -0.003322437|0.259815546 / +0.103829787|0.876299/0.879564|10.307769|43.978209|0.132583|

* rear speed=.02/√(1+(.338k)²)로 base/rear 모두≤.02m/s인 별도 오프라인 profile을 [speed_summary](construction_site_prospective_planner_20261102_v35_07/speed_summary.json)과27개 speed CSV에 기록했다. 정속 명목 시간이며 가속·감속·추종·stop/quiet 시간이 없어 실제 주행시간/성공 예측이 아니다. 원래 CSV의 `time_lower_bound_s_at_02`는 rear length/.02이고 위 표는 base ceiling을 반영한 profile 시간이다. 명목 PRE→FINAL .8m 직선은 별도40초이며 실제 PRE 측정 뒤 독립 replan/sweep/stop을 대신하지 않는다. 조향 rate/torque·슬립·동역학은 미검증이다.

** 같은 표현의9개 PRE와9개 nominal FINAL 경로 전체 합집합에 대한, **10cm clearance 등 모든 여유로 이미 확장된 collider AABB**와 비바닥 obstacle triangle AABB 간3D 거리 하한이다. 원시 물체간 실측 최소거리나 실물 인증이 아니다. 원래 baseline의 LR/CAD는 curvature에서 거절돼 sweep/endpoint PASS를 부여하지 않는다. HR 기존 live sweep의 요구 clearance10cm는 보존하되 위 새 하한과 동일 지표로 혼동하지 않는다.

![원래 경로와 공통 후보 / 곡률](construction_site_prospective_planner_20261102_v35_07/paths_curvature.png)

![27조건의 후보 margin](construction_site_prospective_planner_20261102_v35_07/perturbation.png)

같은 world dx,dy∈{−10,0,+10}mm를 **각자의 관측 목표**에 더해27조건을 검사했다. 원래 planner 통과는 HR6/9, LR3/9, CAD4/9이고 후보9/9씩이다. 후보 최소 margin은 HR .056315313/LR .029644369/CAD .043705665 /m, 전체 최고 curvature 상한 .334000963 /m이다. 9개 점 사이 모든 연속 perturbation에 대한 보장은 없고 통계 reliability 표본도 아니다. [비교CSV](construction_site_prospective_planner_20261102_v35_07/comparison.csv), [JSON](construction_site_prospective_planner_20261102_v35_07/comparison.json)에 실패 이유·길이·시간·동일 한도·안전상태를 보존했다.

## 전체 footprint·지지와 안전 한계

세 read-only 실제 prepared stage를 사용했고 original raw/snapshot/authority **1010건 expected hash 대조 불일치0**이다. stage provenance의 v34 SHA도 별도 최종 검증한다. collider42개 중 rover enabled13개(차체3+wheel/steer10), static union28+환경 mesh1을 포함한다. 시각 전체 bounds도 원자료에 남겼으나 충돌 검증은 enabled collider 전체를 쓴다. 기존 padding .10m clearance+.025m tracking+2° yaw chord+.01m interpolation 및 wheel/steer .15m를 유지한다. support는5mm 이내 path sampling, ±2° yaw/실제 tread3점/±.18m patch guards·바닥 Z/높이 gate를 유지했다.

기존 helper의 `Usd.PrimRange`가 instance 내부 wheel/steer를 빠뜨릴 수 있어 **새 오프라인 AST 사본만** TraverseInstanceProxies로 강화했다. final 각 표현4개 front steering collider chord(20° 보수적 범위) 최대 .048234248m≤.15m를 실제 기하로 확인한다. `_06` 이전 steering evidence가 빈 결과를 최종 full-footprint 인증으로 쓰지 않는다. wheel/steer 모든 bounds에 .15m를 적용한 `_07`만 최종 근거다. live legacy helper는 수정하지 않았다.

각 표현 **973,350 support queries / 실패0**, 전체 union sweep PASS. 공간색인은 같은 삼각형의 검색만 줄이며 각10000번째 support query에서 원래 brute-force hits와 exact equality를 assert했다. 강제로 load 안쪽/바닥 밖으로 옮긴 두 **오프라인 음성대조**는 collision/unsupported FAIL을 검출했다. 그 좌표변경은 안전검사 변조시험일 뿐 후보·실험 목표가 아니다. [안전요약](construction_site_prospective_planner_20261102_v35_07/safety_summary.json), [음성대조](construction_site_prospective_planner_20261102_v35_07/safety_negative_tests.json), 각 표현 `_swept.json`에 전체 bounds·issues·support 수·조향증거가 있다.

![전체 collider와 확장 swept envelope](construction_site_prospective_planner_20261102_v35_07/swept_footprint.png)

union은18개 독립 곡선의 geometry 집합이다. JSON의 경로 배열을 이어 붙여 실제 drive하면 안 된다. FULL support는 authored static triangle의 sampled coverage이며 actual settled suspension/contact, continuous tread contact, tracking/tire dynamics·fresh FINAL admission은 **LIVE_PHYSX_UNTESTED**다. 원래 .05…3m local distance와 전진 convention, 실제 scene obstacle/support 영역 안에서만 조건부 존재를 보였다. 새로운 GT/환경지도 허용 정책이나 더 넓은 reachable workspace를 선언하지 않았다.

## 결정과 다음 단 한 번의 실험이 답할 것

|질문|판정|다음 의미|
|---|---|---|
|datum의 공통 cm 불일치|v34 수치 재현된 설명; 독립 metrology UNKNOWN|B5를 task-design 원점 추정기로 평가한다는 모델 가정을 명시. 같은 D로 사후 보정 금지|
|perception vs assumed model|중심·heading·quantile 차이 관측됨; 단독 원인/정확도 UNKNOWN|독립 GT masks/메트롤로지와 paired 반복 필요|
|원래 planner 민감도|PROVEN, 저장 목표와 strict code 범위|LR/CAD 기존 FAIL 보존. planner gate가 perception 비교를 검열함|
|공통 대안 존재|27점 kinematic+offline scene/footprint/support **조건부 PASS**|전역/실물 안전성·모든 perturbation 보장은 아님|
|실제 HR/LR/CAD endpoint 비교|HR만 측정; LR/CAD NOT_RUN|공통 planner qualification 뒤 새 fresh paired observations 필요|

다음 Kit는 **아직 승인/실행하지 않았다.** 이 measurement/planner proposal을 prospectively 승인한 뒤 별도 engineering namespace에서 기존 nominal pair의 HR/LR/CAD 각1행(3 planned, research분모 제외)을 같은 새 policy로 qualification하는 것이 구체 다음 단계다. 각 행에서 fresh capture→원래 detector/ROI/B4/B5→새 observed PRE→공통 후보의 live swept/ray/contact/조향rate/추종→실제 PRE normalzero/quiet→측정 PRE에서 독립 FINAL sweep/주행/정지를 검증한다. 이는 offline 경로가 실제 PhysX/ROS에 연결되는지를 답하고, planner 거절로 비어 있던 LR/CAD endpoint를 **새 관측**으로 측정할 수 있게 한다. 성공을 보장하거나 v31/v32를 구제하지 않는다. qualification은18회 variance pilot/confirmatory와 분리한다. 독립 segmentation GT 구현은 별도로 남는다.

## 재현·검사·실패 이력

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_prospective_planner_20261102_v35.py --out reports/<새_미사용_폴더>
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_planner_checks_20261102_v35.py reports/<위_폴더>
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_measurement_example_20261102_v35.py reports/<위_폴더>
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_planner_speed_profile_20261102_v35.py reports/<위_폴더>
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_planner_footprint_plot_20261102_v35.py reports/<위_폴더>
```

새 output만 허용한다. 완료 후 CLI 진입 guard만 보강해 기존 폴더 재실행이 failure.json조차 쓰지 않고 거절됨을 전체 파일 SHA 전후 동일로 검증했다. 수치 실행 snapshot과 최종 guard-only source delta/hash는 [artifact checks](construction_site_prospective_planner_20261102_v35_07/artifact_checks.json)에 보존했다. 수치 구현 변경은 없다. main CPU120초/standalone USD180초/27개×48회 bounded shooting/256MiB free-space 진입·study output64MiB 한도, case별 path SHA/status journal과 code snapshot을 둔다. journal은 실패 후 어떤 case가 완료됐는지 식별하는 재개 근거이며 현재 CLI가 중간 case를 자동 skip/resume하지는 않는다. 재실행은 새 폴더를 쓴다. core 최종 elapsed 108.786초. standalone은 기존 hh_isaac51의 발견된 USD libs만 사용하며 Kit/omni/ROS는 시작하지 않는다. dependencies/command/environment/code·parent SHA는 [execution.json](construction_site_prospective_planner_20261102_v35_07/execution.json)에 있다. 입력 bulk는 원래 경로를 참조한다.

**PASS:** core31 checks, 독립 선형계 original replay/고해상도 dyaw/ds·전진/연속성·동일 admission·음성대조38 checks, speed27, compile, 27case pairing·manifest18·원자료 보존·실제 stage SHA/최종 artifact checks. 곡률/XY·perturbation·swept 그림 검토. 독립 checker는 별도 수치 계산의 machine check이며 별도 인간 reviewer/외부 인증은 아니다.

**FAIL 보존:** `_01` NumPy bool JSON serialization, `_02` 기존 brute support worker180초 timeout, `_04`/`_05` spatial-index 교차검사 AST 삽입 indentation/newline 오류. `_03`은 제한 다항식 탐색 완료(PASS이며 LR no path), `_06`은 smooth-S 계산 완료하되 wheel instance traversal 보강 전 안전결과, 최종 `_07`은 보강 후 PASS다. 전부 저장자료 CPU 개발 실행이며 새 simulator 관측/retry가 아니다. 실패폴더와 failure.json은 삭제하지 않았고 분모에서 숨기지 않았다.

**UNKNOWN/미완료:** 실제 candidate PhysX/ROS·동역학/stop, 독립 segmentation GT/실물 metrology, representation 단독 인과·분산/통계power, human protocol 승인. 이 보고서의 완성은 live 승인이나 frozen108/432 readiness PASS가 아니다.

변경: 새 analysis v35 코드5개, measurement DRAFT, paired18 PROPOSED manifest, 본 보고서·v35 CSV/JSON/PNG/실패기록; 갱신 latest_report 및 PROJECT_STATE. 원본 USD/weights/GT/source/4rep locks·기존 v01/v02/v03 결과 변경0. Git remote/push/외부전송0. HPO/training PAUSED·formal science denominator0.
