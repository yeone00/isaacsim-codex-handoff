# v34 — B5 중심의 공통 cm 편향과 표현별 mm 차이

2026-11-02 KST. 저장된 HR v30/LR v31/GeoCAD v32 각 1관측의 **오프라인 분석 완료**. 세 B5 중심·count·score·heading을 오차 1e−10 이내, PRE/FINAL은 저장 dictionary와 정확히 재현했다. 새 관측·추론·Kit·ROS·훈련·주행은 없다.

핵심은 두 가지다. **종방향 약 −2.85cm는 실제 authored 적재물 경계와 B5의 고정 반치수 사이 차이로 설명된다. 횡방향 약 −4.7∼−5.3cm는 선택된 side 점 전체의 98% X 분위수가 실제 authored 오른쪽 경계보다 안쪽에 있는 항이다.** CAD에는 축 회전에 따른 약 (+4.21, −3.24)mm 잔여가 더해진다. 이 둘을 합치면 저장된 모든 중심 편향이 닫힌다. 이는 설계 기준점 대비 계산·형상 관계를 확인한 결과이며, 독립 실물 metrology로 입증한 센서 정확도가 아니다.

## 1. 기준점과 프레임의 정확한 의미

|단계|소스의 실제 계산과 의미|
|---|---|
|RGB-D|640×480 RGB uint8, depth는 `distance_to_image_plane`, 1m/unit. RGB 파일은 RGB이고 YOLO 입력에서만 BGR로 교환. 마스크는 bool이며 색상 palette에서 추출한 GT mask가 아님. ROI overlay의 분홍색은 표시 전용|
|optical→world|`p_opt=[(u−320)z/fx,(v−240)z/fy,z]`, fx=fy=317.04312011949685px. `p_world=R p_opt+t`, optical right/down/forward, column convention, world m/Z-up. USD row matrix는 transpose 뒤 camera Y/Z 반전|
|평면 datum|관측 pallet ROI의 near-horizontal plane을 fitting하고 ROI centroid 위치의 Z를 사용. 공간적으로 평면을 평탄화하지 않고 **Z에만** `−top+.144` 적용. 이후 Z≥.124 필터|
|B4|top 99% Z−.020m band, 부족하면 상위20%; convex hull/minAreaRect의 장축 heading. B4 90° flip에는 margin gate .014116 적용|
|B5 side|4층×.090+.144−.030=.474m 이하; 부족하면 Z≤70% 분위수. 별도의 좌우 면 segmentation 없음|
|B5 center|`ex=(cosθ,sinθ)`, `ey=(−sinθ,cosθ)`. 카메라 전방의 반대 XY를 각 축에 내적해 sign 결정. 각 축 전체 side projection의 sign<0이면 2%, sign≥0이면 98% 분위수 `f`. `c=(f_u−sign_x·.475)ex+(f_v−sign_y·.4275)ey`|
|선택 주의|중심 후보는 **B2 θ와 θ+90°의 B5 score를 비교**한다. B4 final heading을 그대로 중심 축으로 소비하는 구조가 아님. 이번 3행은 B4 flip=false, B5 center flip=false이며 결과적으로 같은 θ 사용|
|B5 명칭|관측 visible-face projection에 치수를 더한 **추정 적재물 직사각형 중심**. 점 평균·가시 전면 자체·팔레트 검출 중심·질량중심·접근 anchor가 아님. task policy는 이를 팔레트/support 중심의 대용치로 사용|
|canonical|workspace lock의 (−25.888,30.509)m는 실험 배치용 pallet/support task-design datum. 실제 Fixture·ActualBrickLoad 원점 XY 및 300 slot 원점 평균과 일치. 시각 mesh AABB 중심과는 다름|
|targets|`n=R(90°)[−1,0]=(0,−1)`. FINAL=c+1.403745031260775n; PRE=c+2.203745031260775n. B5 heading으로 task axis를 돌리지 않음. 명령 yaw는 π/2|
|offset 출처|잠금 robot protocol v05: pallet half .55 + mounted-system front .743745031260775 + clearance .11 = FINAL offset1.403745031260775m, PRE는 추가 .8m. planner rear .338m는 base↔rear 경로 변환이며 B5나 target 생성 항이 아님|

따라서 commanded yaw 오차0°는 B4 정확도0°라는 뜻이 아니다. B5 load model과 task-design support datum은 **동일한 물리적 점이라는 가정이 필요**하다. 이번 authored 상태에서는 원점은 일치하지만 실제 비대칭 시각 경계와 고정 치수 가정이 그 가정을 깨뜨린다. canonical 좌표·GT 정의·성공 기준은 변경하지 않았다.

## 2. 실제 scene의 300 배치와 공통 datum 항

세 실제 `prepared_site_drive.usda`를 witness SHA와 대조한 뒤 standalone USD로 읽었다. Kit를 시작하지 않았다. 각 stage는 m/Z-up, Load 회전은 world +90°이다. 300 slot의 전체 행렬과 bounds는 `scene_slots_900.csv`에 기록했다. world matrix와 bound는 원본 slot별로 보존했다. 세 표현의 slot 원점 평균=(−25.88800000000002,30.509000000000007)m; min XY=(−26.287,30.0625), max=(−25.489,30.9555)m. Fixture 원점=(−25.888,30.509,.00121562)m, Load 원점=(−25.888,30.509,.14521562)m. 원점 평균 오차는 부동소수점 수준이다.

공통 authored visual union bound는 XY 약 [(−26.344,30.0055),(−25.4605,30.984)]m, 크기 world X .8835m/Y .9785m이다. B5가 가정한 yaw90 적재물 X .855m/Y .950m보다 각 .0285m 크다. AABB 중심은 (−25.90225,30.49475)m로 canonical보다 (−14.25,−14.25)mm이며, 이것을 새 GT로 바꾸지 않는다. 표현 간 bound 수치차는 nm 수준이다.

실제 normalized asset bounds는 약 x=[−.095,+.095], y=[−.045,+.045], z=[0,.057]m다. 즉 asset origin은 높이 중심이 아닌 밑면이다. `full_e2e_scene_geometry_v01.py:create_actual_brick`는 slot을 Z=.045m에 놓고 `SideStanding`에 RotateX(−90°)를 적용한다. 이때 원래 z=[0,.057]은 slot의 +Y=[0,.057]로 가며 ±.0285로 대칭화하지 않는다. `create_actual_bundle`의 R패턴 RotateZ(+90°)도 이를 회전한다. 실제 transform/bounds가 이 비대칭을 확인한다. 이는 셀 배치/asset origin과 고정 B5 rectangle의 관계이며 이번에 수정하지 않았다.

world 앞면 minY=30.0055, canonical Y=30.509이므로 앞면은 **503.5mm** 앞이다. B5는 +475mm를 더해 중심을 복구하므로, 앞면을 정확히 잡아도 Y는 **−28.5mm**가 된다. 반면 우측 maxX는 canonical X+.4275m이므로 그쪽 dimension/reference 항은 약0mm다. 이에 더해 X는 full side cloud의 극값 자체가 아니라 98% 분위수를 쓰므로 오른쪽 경계까지 복구하지 못한다.

다음 표는 **평가용 정확한 대수 분해**다. 동일 저장 side 점에서 world q98(X), q02(Y)를 구한 뒤, 실제 authored maxX/minY 및 고정 반치수를 비교했다. axis90은 설명용 진단 좌표이며 새 perception 입력·수정 목표가 아니다. 마지막 잔여는 실제 선택 heading의 결과와 이 axis90 진단 중심의 차이다. 이 표를 독립 인과 성분으로 해석하지 않는다.

|표현|분위수−authored face ΔX/ΔY(mm)|authored face+반치수−design ΔX/ΔY(mm)|실제 중심−axis90 진단 ΔX/ΔY(mm)|합계 ΔX/ΔY(mm)|
|---|---:|---:|---:|---:|
|HR_Scan|-46.735339 / +1.284289|+0.000003 / -28.499999|-0.085972 / +0.001165|-46.821307 / -27.214544|
|LR_Scan|-51.877676 / +1.499169|+0.000001 / -28.500000|+0.045015 / -0.004952|-51.832659 / -27.005782|
|GeoCAD|-52.910610 / +1.092880|-0.000001 / -28.500000|+4.205352 / -3.241822|-48.705259 / -30.648942|

**관측에서 무엇이 식별되는가:** q02(Y)는 actual 앞면보다 약1.1∼1.5mm 뒤에 있다. 반면 q98(X)는 actual 오른쪽 경계보다 46.7∼52.9mm 안쪽이다. B5는 모든 전면/측면 점을 함께 투영하며, 오른쪽 면 점만 모아 fitting하지 않는다. 정면 관측에서 넓은 전면의 연속 X 분포와 끝부분 마스크·가림·배경 혼입이 이 분위수에 들어간다. 실제 side maxX는 HR −25.20459/LR −25.08732/CAD −25.29668m로 물체 bound 밖까지 나가므로, 단순 max로 바꾸는 것도 정당하지 않다. 분위수의 후퇴는 저장자료로 확인했지만, 실제 물체 pixel GT가 없어 누락/배경/가림 각각의 원인 몫은 UNKNOWN이다. 새 annotation이나 speculative fix는 만들지 않았다.

scene task frame은 frozen design lock과 다른 방식인 composed transform으로 확인되지만, **같은 설계에서 저작된 값**이다. 독립 실물 측정·렌더 surface metrology 인증은 아니다. 보고하는 5.4∼5.8cm는 ‘canonical task-design datum 대비 오차’이며, 모두 sensing error로 부르지 않는다. Pallet 원점은 Fixture와 중심을 공유하고, rolltainer는 rover에 장착된 별도 프레임이다. `scene_authored.json`에 rolltainer world origin/bounds도 남겼다. +90° 초기 rover에서 mounted front는 base Y보다 .74374503126077m 앞이며 protocol 값과 맞는다. 이를 center나 rear offset으로 잘못 더한 흔적은 없다.

## 3. 저장 B4/B5 단계와 표현별 mm 차이

|표현|mask px; centroid u/v(px)|수직필터 후 / top / side 점|plane top(m); tilt(°)|B5 θ(°); score; inside|
|---|---|---|---|---|
|HR_Scan|7710; 316.307263/163.611414|7701 / 946 / 6505|0.148475024142; 0.079800|90.011093140; 0.073583255; 0.991429684|
|LR_Scan|7718; 316.015159/163.844519|7713 / 945 / 6529|0.148479396141; 0.079800|89.994220915; 0.072482191; 0.993128484|
|GeoCAD|7703; 315.957289/163.867195|7703 / 956 / 6495|0.148486793385; 0.079799|89.453897834; 0.076246113; 0.999480722|

mask bounds HR=[250,134,381,193], LR=[251,134,381,194], CAD=[250,134,381,194]px. 각각 수직필터에서 9/5/0점 제거. 모든 행에서 camera-to-face sign=(-1,-1), 따라서 2% u/v를 사용한다. sign_y는 정면 시야에서 작은 카메라 XY방향 차이에도 좌우 선택을 할 수 있는 연산 구조다. 여기서는 세 sign이 같고 flip도 없어, 실제 flip 전환이 표현 차이를 만들었다는 증거는 없다.

실제 연산 `center=visible-face-intersection + dimension-offset`를 그대로 분해하면 다음과 같다. face intersection은 두 투영 분위수의 교점으로 실제 surface 위의 한 점이라고 보장하지 않는다.

|HR 대비|face intersection ΔX/ΔY(mm)|치수×회전축 항 ΔX/ΔY(mm)|최종 ΔX/ΔY(mm)|
|---|---:|---:|---:|
|LR_Scan|-5.151222302/+0.082867172|+0.139870203/+0.125894923|-5.011352100/+0.208762095|
|GeoCAD|-6.522617642/-7.570161083|+4.638665493/+4.135763224|-1.883952149/-3.434397859|

LR은 face 교점 X −5.151mm에 축 offset +.140mm가 더해져 −5.011mm다. CAD는 교점 (−6.523,−7.570)mm에 치수축 (+4.639,+4.136)mm가 더해져 (−1.884,−3.434)mm다. CAD의 작은 최종 X 차이는 중간 변화가 작아서가 아니라 상쇄 결과다. 좌표 원점이 큰 global projection 값은 개별 항이 크므로, 그 자체를 좌표 오차로 읽지 않는다.

48개 bounded 합성 replay(각 행 heading/plane/mask/depth의 HR 치환 2⁴)에서 원래 candidate score 비교와 최소점 gate를 유지했다. intrinsic/extrinsic/frame1/sim_time4.250000221654773s·초기 base가 exact 동일임을 확인한 후 image-coordinate mask/depth 치환을 허용했다. mask는 같은 pixel ray의 선택자로만 전송했고 surface 대응이나 실제 혼합 장면 관측이라고 주장하지 않는다. 다른 calibration/frame이면 코드가 중단한다. GT·scene bound·target을 치환 입력으로 사용하지 않았다. ‘heading만’은 B2 heading을 HR로 고정하고 두 후보/B4 gate/B5 score를 다시 계산한 연산 개입이다.

|HR 요소 하나만 치환|LR ΔX/ΔY(mm)|CAD ΔX/ΔY(mm)|
|---|---:|---:|
|heading|-0.131435934/-0.001674585|-4.291801519/+3.229069396|
|관측 plane 높이|+0.000000000/+0.000000000|+0.000855903/-0.000042184|
|mask 선택자|+4.693212156/+0.011643520|+10.296628495/-3.788228119|
|depth 이미지|+0.680686507/-0.209233110|-3.888374779/+3.433413887|

전체 네 항을 HR로 치환하면 LR→HR (+5.011352100,−.208762095)mm, CAD→HR (+1.883952149,+3.434397859)mm로 정확히 돌아온다. 단일 효과는 상호작용 때문에 합산할 수 없다. mask-only는 동일 depth에서 **pixel selection 차이**를 식별하지만 그 mask 차이를 geometry와 학습모델 중 어디에 귀속할지는 식별하지 않는다. depth-only도 표면 전환과 B4 재계산을 포함한다. HR heading만으로 LR의 X 차이가 해소되지 않고 CAD에서는 X가 오히려 −4.292mm 이동한다. 따라서 ‘CAD heading이 X 편향 전부의 원인’이라는 결론은 틀리다.

plane의 실제 소비값은 normal 전체가 아니라 centroid의 top Z다. HR 대비 top 차이는 LR +.004372mm, CAD +.011769mm이며 plane-only XY 영향은 LR0, CAD (+.000856,−.000042)mm다. 현재 관측의 5mm X 차이를 이 plane 차이로 설명할 수 없다. 평면 gate는 실제 저장값으로 모두 PASS이며 ROI/inlier=114/114,132/132,138/138. normal·잔차·범위·ROI polygon/깊이 분위수는 `stage_details.json`에 있다. plane residual은 fitting scatter이며 절대 depth accuracy가 아니다.

추가 ±.1mm top 및 ±.01° heading 중앙차분 12회: heading 민감도 XY는 HR(−7.751,+.065), LR(−7.789,+.532), CAD(−7.609,+5.970)mm/°. top 민감도는 HR(−.084899,+.000903), LR(−.316806,+.000859), CAD(−.059768,+.002934)mm/mm. 필터 membership·분위수·minrect/candidate 전환 때문에 국소값이다. world optical cloud의 분포 covariance와 분위수는 JSON에 기록했으나, **한 관측의 표면 분산은 estimator 불확실성 covariance가 아니다**. 반복 표본·센서 noise model이 없어 center uncertainty ellipse/CI는 UNKNOWN이다.

## 4. pixel/depth 관측 비교의 범위

|HR 대비|공통 mask / HR만 / 상대만(px)|예측끼리 IoU(GT 아님)|동일 ray 절대 Δz ≤5 / 5–20 / 20–100 / >100mm(px)|signed depth median(mm)|
|---|---|---:|---|---:|
|LR_Scan|7635 / 75 / 83|0.979725395|6762 / 498 / 318 / 57|+0.347614|
|GeoCAD|7617 / 93 / 86|0.977039507|6642 / 280 / 669 / 26|-0.761271|

공통 마스크 pixel 모두 양의 finite depth다. LR depth signed min/max=−1493.223/+2127.940mm, CAD=−1931.627/0mm. 이는 axial z 차이이며 world 3D norm과 숫자가 다르다. 2m 차이를 geometry error라고 부르지 않는다. 같은 ray가 경계·빈틈·가림에서 서로 다른 표면을 볼 수 있다. pixel GT가 없어 outlier를 임의 제거해 accuracy를 만들지 않았다. 모델 confidence(.791759/.972648/.959305)는 mAP가 아니다. segmentation GT/mAP/GT IoU·독립 metrology·실로봇 deployment는 UNKNOWN이다.

## 5. 세 중심·PRE/FINAL 및 cm/degree 평가

부호는 pred−locked design, 종방향=+Y, 좌측=−X. yaw90 고정이라 center와 PRE/FINAL의 XY 오차 벡터는 같다. canonical PRE=(−25.888,28.305254968739225)m, FINAL=(−25.888,29.105254968739224)m.

|표현|예측 center XY(m)|PRE XY(m)|FINAL XY(m)|
|---|---|---|---|
|HR_Scan|(-25.934821307220,30.481785455652)|(-25.934821307220,28.278040424391)|(-25.934821307220,29.078040424391)|
|LR_Scan|(-25.939832659320,30.481994217747)|(-25.939832659320,28.278249186486)|(-25.939832659320,29.078249186486)|
|GeoCAD|(-25.936705259370,30.478351057793)|(-25.936705259370,28.274606026532)|(-25.936705259370,29.074606026532)|

|표현|world dx/dy(cm)|종방향/좌측(cm)|중心距離(cm)|B4 heading 오차 mod180(°)|goal yaw 오차(°)|
|---|---:|---:|---:|---:|---:|
|HR_Scan|-4.682130722/-2.721454435|-2.721454435/+4.682130722|5.415594366|+0.011093140|0.0|
|LR_Scan|-5.183265932/-2.700578225|-2.700578225/+5.183265932|5.844601652|-0.005779085|0.0|
|GeoCAD|-4.870525937/-3.064894221|-3.064894221/+4.870525937|5.754615494|-0.546102166|0.0|

![잠금 설계 기준에서 예측 중심으로의 벡터](construction_site_b5_datum_and_error_budget_20261102_v34_05/GT_vectors.png)

cm 축으로 확대한 평면도다. 독립 물리 GT가 없음을 그림에 명시했다. LR/CAD의 endpoint를 그린 것이 아니다.

HR 실제 FINAL은 observed-goal 거리 .279451388cm, yaw−.039722360°이며 canonical task FINAL 거리는 5.523288386cm, 종방향−2.997573290cm/좌측+4.639102173cm다. 5.5cm strict보다 .23288386mm 크고 main11cm/relaxed16.5cm는 통과한다. 이는 기존 v33의 동일 physical endpoint 평가를 재사용·검증한 것이며 원래 HR engineering success를 바꾸지 않는다. LR/CAD 실제 PRE/FINAL은 **NOT_RUN**, endpoint 오차/성공률을 대입하지 않는다. v33 original planner kmax와 HR 음의 X margin1.821718mm 결과도 그대로다. 이번에 planner sweep/Kit를 반복하지 않았다.

## 6. 논문 지표와 정확한 다음 연구

현재는 representation당 n=1, 표현과 matched frozen M50 모델이 함께 달라지고 수동 ROI도 달라진 탐색 결과다. HR reviewer 문자열 v30 대 LR/CAD v28의 기존 불일치도 그대로이며 완전통제/맹검을 주장하지 않는다. representation 단독 인과·통계적 우열·동등성·비열등성은 식별되지 않는다. LR은 HR decimation이 아니라 독립 저감 acquisition 재구성이다. red-only real validation을 cement나 실로봇 배포로 확대하지 않는다.

다음은 **새 구현 없이 권고만** 한다. 먼저 datum 정의/비대칭 asset origin 관계를 설계 검토하고 기존 잠금과 분리된 전향 measurement 계획을 정한다. 같은 paired seeds/초기 pose/camera/load/occlusion 셀마다 HR/LR/CAD를 반복하며 seed·paired membership·실패 분모와 관측 정책을 사전 잠근다. 반복수는 최소 검출 차이와 pilot 반복분산에 근거해 정하고 지금 n을 임의 확장하지 않는다. matched-model pipeline 효과와 geometry 효과는 구분하고, geometry 단독 귀속에는 별도 사전 정의된 model 통제 설계가 필요하다.

|단계|측정 계획|
|---|---|
|segmentation|독립 라벨 GT에서 class/matching/IoU thresholds 고정한 AP50/AP75/mAP50–95와 matched mask IoU·precision/recall. confidence 대체 금지|
|B4/B5|검증된 동일 의미의 reference point 대비 signed XY/long/lat cm, heading degree; visible-face support·dimensions·ROI plane·mask/depth의 단계별 진단과 반복 covariance|
|task target|고정 task axis로 생성한 PRE/FINAL cm/deg, sensing error와 datum/model 오차 구분|
|planner|원래 quintic의 feasibility·kmax/margin·실패 원인과 분모 유지. perception 통과와 motion 성공 분리|
|endpoint|실제 endpoint를 perceived goal과 검증된 task datum 양쪽에서 평가; 도달·timeout·미시작·terminal error를 누락 없이 기록|

별도 **prospective 공통 planner robustness 연구**는 steering/전체 footprint/clearance/sweep/contact/safety를 동일하게 유지하며 작은 목표 변화와 load/occlusion 조건을 모든 표현에 적용한다. 대체 안전 경로 존재는 현재 UNKNOWN이다. 정책 변경은 새 amendment·새 version/output/분모로 승인·잠금 후 평가하고 기존 v31/v32 실패는 소급 변경하지 않는다. 이번 v34에는 보정·retuning·새 annotation·planner 구현이 없다.

## 7. 재현·검사·제한과 변경 파일

[재현 코드](../analysis/construction_site_pilot_b5_datum_and_error_budget_20261102_v34.py)는 statically inspected simulator-free extracted core와 camera/datum adapter만 사용하며 legacy module을 import하지 않는다. frozen source SHA 및 AST 비교로 함수·상수를 검증했다. 세 snapshot adapter의 datum 함수 AST도 동일(PASS, SHA `663ac6584caad336b143cdd9a8b7f1af3268b7cd01b7b629c5832f168ec6c6cc`)하다. source snapshots의 관련 adapter/ROI SHA와 원본 frozen pose/protocol/model dependency SHA, 필요한 RGB-D/mask/calibration/ROI/plane/B5 파일, matched weights, prelock/amendment through v03/geometry v02 등 selected authority를 대조했다. 실행한 CPU helper 5개와 geometry source는 observed SHA를 별도로 기록했다. runtime code_versions에 이 helper들의 독립 expected가 없어 historical byte identity는 UNKNOWN이지만 frozen core의 원본 AST 일치와 세 저장 출력 재현은 PASS다. 전체 v33 930 hash나 441점 geometry sweep을 다시 하지 않았다. geometry lock 자체의 독립 expected UNKNOWN은 그대로다.

카메라 metadata의 `source_usd`는 **부모 pilot layer 경로**다. 이를 단독으로 열면 root stage metadata가 없어 USD 기본 .01m/Y-up이 나온다. 실제 실행 root `prepared_site_drive.usda`는 명시적1m/Z-up이며 capture calibration8/8 및 renderer matrix와 맞는다. 첫 분석 `_01`은 이 차이를 감지해 USD 단계 FAIL로 중단했고 `failure.json`/log와 부분 출력은 보존했다. 이후 witness SHA로 actual root를 선택했으며 expected hash나 원본 metadata를 수정하지 않았다. 부모 경로만을 실제 capture stage라고 해석하지 않는다. `_02`는 수정 후 PASS, `_03`는 side-world/asset bounds 추가 PASS, `_04`는 ROI·protocol provenance 및 그림 가독성 추가 PASS, 최종 `_05`는 실행된 CPU dependency의 observed hash 기록을 추가해 PASS다. 모두 저장자료 CPU 재분석이며 새 실험 retry가 아니다.

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_pilot_b5_datum_and_error_budget_20261102_v34.py --out reports/<새_미사용_폴더>
```

기존 output overwrite 거부. 3 original replay+48 factorial+12 local sensitivity, 3 standalone read-only USD stage만 제한적으로 처리한다. 선택된 입력과 source SHA·환경·command·code SHA·실패를 기록한다. bulk RGB/depth/USD/weights는 복사하지 않고 원래 경로를 참조한다. GT/scene는 평가 단계에서만 읽으며 perception/target 치환 입력에 들어가지 않는다.

- **PASS:** 원본 B5/target 재현, 관련 입력/authority/model SHA, 카메라 exact co-registration와 단위/프레임 확인, 실제300 slot/표현×3 USD 조회, 기여도 합계, 공통 HR 전체 치환 복귀, compile/최종 artifact 검사·그림 검토.
- **FAIL 보존:** `_01` standalone 부모 stage 단위 assertion. v31/v32 curvature FAIL 및 기존 모든 결과 불변.
- **UNKNOWN:** 독립 segmentation/실물 GT·센서 absolute accuracy·개별 원인 귀속·반복 covariance·다른 안전 경로·LR/CAD physical endpoint. 실제 ROI plane 표본분산/표면 covariance를 정확도 CI로 해석하지 않음.

Git status는 이 starter 경로에 .git이 없어 확인 불가였고 파일을 stage/commit하지 않았다.

새 파일: analysis v34, 본 보고서, `_01`∼`_05` 분석 JSON/CSV/PNG/log. 갱신: `reports/latest_report.md`, `docs/PROJECT_STATE.md`. scene/asset/model/GT/ROI/planner/controller/physics 변경0, formal confirmatory science denominator0, HPO/training **PAUSED**. 다음 구체 행동은 **이 datum/치수 결과를 반영한 전향 측정·반복 설계 초안 검토**이며 실행/수정은 이번 범위 밖이다.

정밀 자료: [stage_details.json](construction_site_b5_datum_and_error_budget_20261102_v34_05/stage_details.json), [stage_contributions.csv](construction_site_b5_datum_and_error_budget_20261102_v34_05/stage_contributions.csv), [datum_budget.csv](construction_site_b5_datum_and_error_budget_20261102_v34_05/datum_budget.csv), [interventions.csv](construction_site_b5_datum_and_error_budget_20261102_v34_05/interventions.csv), [pixel_differences.json](construction_site_b5_datum_and_error_budget_20261102_v34_05/pixel_differences.json), [scene_authored.json](construction_site_b5_datum_and_error_budget_20261102_v34_05/scene_authored.json), [scene_slots_900.csv](construction_site_b5_datum_and_error_budget_20261102_v34_05/scene_slots_900.csv), [GT_metrics.csv](construction_site_b5_datum_and_error_budget_20261102_v34_05/GT_metrics.csv), [integrity.json](construction_site_b5_datum_and_error_budget_20261102_v34_05/integrity.json), [execution.json](construction_site_b5_datum_and_error_budget_20261102_v34_05/execution.json).

최종 검사: expected SHA 비교143건 불일치0, observed-only8건(독립 expected 없음), 48/48 치환 유효, 900 slot 및 예산합계 오차<1e−8mm PASS. [검사 기록](construction_site_b5_datum_and_error_budget_20261102_v34_05/artifact_checks.json), [세 snapshot datum AST 비교](construction_site_b5_datum_and_error_budget_20261102_v34_05/snapshot_datum_AST_checks.json).
