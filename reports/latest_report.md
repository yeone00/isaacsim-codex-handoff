# v33 — 저장된 3표현 인식→목표→곡률 오차 전파

2026-11-02 KST. **오프라인 분석 완료.** 같은 시작점에서 LR의 X −5.011352mm는 최대곡률을 +0.037259986/m 올리고, Y +0.208762mm는 −0.000166071/m 낮춘다. CAD의 X −1.883952mm만으로도 고정 quintic 한도를 근소하게 넘으며, Y −3.434398mm가 초과를 더 키운다. 이는 저장된 목표 좌표를 바꾼 통제 실험의 결과다. 표현+각 matched M50+ROI 전체 pipeline 중 어느 요소가 그 좌표 편향을 만들었는지는 분리 입증되지 않았다. Kit/ROS/추론/훈련 실행0, 정책 변경0, formal science denominator0.

## 재현과 증거 범위

외부 원본 root 세 개, asset/model 전체 경로·SHA256, fresh capture/calibration, B4/B5, ROI/평면, 실제 baseline, PRE/FINAL, endpoint는 [원자료](construction_site_error_propagation_20261102_v33_02/evidence_3rows.json)에 정밀도 손실 없이 보존했다. 3행 CSV는 [원자료](construction_site_error_propagation_20261102_v33_02/stage_metrics_3rows.csv). raw witness index와 실행 snapshot/input **930건 hash 비교 PASS**; 별도 v24 parent 권위 chain은 [원자료](construction_site_error_propagation_20261102_v33_02/authority_integrity.json)의 실제 hash 전부 PASS. expected를 변경하지 않았다. geometry lock 자체 독립 expected UNKNOWN은 유지한다.

원본 실행 snapshot `construction_site_follower_20261101_v19.py`의 `plan`만 AST로 추출했다. strict 함수는 원래 곡률 예외를 그대로 내며 HR PASS/LR·CAD CURVATURE_INFEASIBLE을 재현한다. 진단 사본은 **그 예외문 하나만 제거**해 거절 이후 후보 형상을 드러낸다. 원본 파일은 수정하지 않았다. 세 kappa는 기존 독립 저장산술과 절대차 <1e−12/m; HR 전체 저장 `leg_0_path.json` 배열도 <1e−12 일치. LR/CAD의 완전 경로 배열은 이번 오프라인 산출물이며 실제 실행 시 완성/승인/주행된 경로가 아니다.

원래 rear offset .338m, wheelbase .700m, steering15°, bound=.95×tan15°/.7 = **.363645332585095/m**. rear endpoint에 대해 quintic Hermite: 양 끝 접선 D×(cos yaw,sin yaw), 두 번째 미분0, D는 rear endpoint 직선거리. N=ceil(D/.001), t=i/N. “1mm”는 이 N 정책이며 정확히 1mm 등호간격의 arc resampling이 아니다. base XY는 rear XY에 접선방향 .338m를 더한 값이다.

세 실제 stopped baseline은 **모든 저장 자리까지 동일**: base (−25.887981414794922,27.400135040283203)m, yaw1.570802304365591rad (90.000342489573°). 따라서 실제 replay와 공통 시작점 counterfactual은 시작점 교란 없이 비교된다. mounted optical T와 intrinsics도 exact 동일, frame1/sim_time4.250000221654773s, physical capture 전후4.283333556726575s에서 pose 변화0. wall epoch/원본 SHA는 각 ROI preview와 capture 증거에 있다. 별도 시점의 세 장면이며 동시 관측은 아니다.

B4→B5→goal 의존성: mask+depth→backprojection→B4 축/flip→B5 visible-face/치수 기반 중심. 원본 evaluator `axes_from_heading` 및 `center_u*ex+center_v*ey`에서 heading이 중심에 영향을 준다. ROI 평면 datum도 B5 필터에 들어간다. adapter는 **중심 XY만** `generate`로 전달하고 yaw90°/local_-X를 고정한다. PRE=center−(0,2.203745031260775)m, FINAL=center−(0,1.403745031260775)m. session은 endpoint yaw π/2를 다시 명시한다. CAD B4−HR=−.557195305824°는 endpoint yaw 변화가 아니다. yaw-only sweep은 실제 소비되지 않아 생략했다.

## 실제 PRE 후보 재현

|표현|PRE XY(m)|max abs(k) (/m)|margin (/m)|rear/base 길이(m)|N+1|최대점 t, 부호|
|---|---|---:|---:|---|---:|---|
|HR_Scan|(-25.934821307220, 28.278040424391)|0.350094191771|+0.013551140814|0.879688718/0.882838932|881|0.788636364, -0.350094192|
|LR_Scan|(-25.939832659320, 28.278249186486)|0.387170520832|-0.023525188247|0.880298454/0.884149283|881|0.789772727, -0.387170521|
|GeoCAD|(-25.936705259370, 28.274606026532)|0.366967769982|-0.003322437397|0.876408056/0.879854578|877|0.788812785, -0.366967770|

|거절 후보|첫 초과 t|rear 진행(m)|그때 base XY(m)|k(/m)|
|---|---:|---:|---|---:|
|LR_Scan|0.155681818182|0.136913969|(-25.899841569685, 27.536876515182)|+0.364405606570|
|GeoCAD|0.189497716895|0.165929436|(-25.903737711418, 27.565772007226)|+0.363842435880|

첫 양의 곡률 lobe에서 한도를 넘고, 뒤 반대 방향 lobe의 절대 최대가 더 크다. 약 .88m의 짧은 전진 구간에서 횡방향 이동 후 다시 +90°로 정렬해야 하므로 양 끝 접선/영곡률 조건을 고정한 S형 quintic의 곡률이 목표 X에 민감하다. “이 고정 quintic이 불합격”이며 “안전한 다른 물리 경로가 없다”는 결론이 아니다. sweep/support gate까지 진행되지 않은 LR/CAD에는 curvature 외 경로 안전성 PASS도 부여하지 않는다.

![후보 XY 경로](construction_site_error_propagation_20261102_v33_02/xy_paths.png)

X축 cm/Y축 m로 횡방향 차이를 확대했다. 점선 LR/CAD는 OFFLINE CANDIDATES이며 실제 로봇 궤적이 아니다. HR 선도 generated path이고 실주행 tracking trace와 구별한다.

![곡률 profile](construction_site_error_propagation_20261102_v33_02/curvature.png)

서로 다른 881/877개 index를 직접 빼지 않았다. rear arc fraction 0…1의 공통1001점에 보간한 비교는 다음과 같다. 절대 동일 arc 거리/최근접 지점의 비교와는 다른 정의이며 작은 경로 길이 차이도 포함한다. 각 CSV에 t, world base XY, body tangent yaw, rear curvature와 arc가 있다.

|HR 대비|최대/RMS 경로변위(mm)|최대 접선각 차(°)|
|---|---:|---:|
|LR_Scan|6.797916/4.962835|0.607503|
|GeoCAD|3.917188/2.822520|0.252304|

## 공통 시작점의 좌표 분해와 경계

시작점·rear offset·yaw·planner를 HR와 동일하게 두고 X만/Y만/XY 함께 교환했다. HR 자기 치환3행은 모두 Δ0이며 아래 수치는 합성 offline 조건이다.

|치환|요소|max abs(k) (/m)|Δk vs HR|margin|상호작용 XY−X−Y|
|---|---|---:|---:|---:|---:|
|LR_Scan|x|0.387354177743|+0.037259985972|-0.023708845158|—|
|LR_Scan|y|0.349928120411|-0.000166071360|+0.013717212174|—|
|LR_Scan|xy|0.387170520832|+0.037076329061|-0.023525188247|-0.000017585551|
|GeoCAD|x|0.364108094393|+0.014013902622|-0.000462761808|—|
|GeoCAD|y|0.352844231811|+0.002750040040|+0.010801100774|—|
|GeoCAD|xy|0.366967769982|+0.016873578211|-0.003322437397|+0.000109635550|

LR에서는 X 단독이 초과를 만들고 Y가 약간 완화한다. CAD도 X 단독 max .364108094/m으로 bound보다 .000462762/m 높다. CAD Y 단독은 통과하지만 XY에서 경로를 더 짧게 만들어 초과를 키운다. 따라서 이번 특정 planner·조건에서는 X 영향이 지배적이라는 통제 근거가 있다. 인식 단계에서 X가 왜 달라졌는지까지 이 분해가 증명하지는 않는다. 모든 첫 초과/위치와 정확한 coordinate pair는 [counterfactual CSV](construction_site_error_propagation_20261102_v33_02/counterfactuals.csv)에 있다.

±10mm XY/1mm grid **441 synthetic points**, dy=−10,−5,0,+5,+10mm 각각 경계20회 이분 refinement. 이는 추가 독립 관측이 아니고 curvature gate만 평가한다.

![합성 feasibility map](construction_site_error_propagation_20261102_v33_02/feasibility.png)

|HR 기준 dy(mm)|통과/실패 경계 dx(mm)|
|---:|---:|
|-10|-0.716791153|
|-5|-1.267709732|
|0|-1.821718216|
|5|-2.378931046|
|10|-2.939329147|

dy0에서 HR의 허용 음의 X 이동은 약 **1.821718mm**뿐이다. 경계 수치 bracket 폭 .000019074mm는 계산 해상도이지 센서 정밀도가 아니다. 이 영역에서는 더 음의 dx가 실패 쪽이며 bound는 완화하지 않았다.

|기준 목표|∂kmax/∂x (/m²), 좌/우|∂kmax/∂y (/m²), 좌/우|
|---|---:|---:|
|HR_Scan|-7.440507/-7.440721|-0.795924/-0.795653|
|LR_Scan|-7.426019/-7.426254|-0.879580/-0.879280|
|GeoCAD|-7.494543/-7.494769|-0.837394/-0.837107|

이는 ±.1mm 국소 one-sided finite difference다. HR에서 X +1mm 효과는 대략 −.00744/m, Y +1mm는 −.000796/m. ±.5/1mm의 비대칭과 peak t 변화도 [derivatives JSON](construction_site_error_propagation_20261102_v33_02/derivatives.json)에 기록했다. 유한 grid의 max는 샘플 수 ceil(D/.001) 변화/최대점 전환에서 미분가능함을 보장하지 않는다. 모든 probe의 peak 부호는 음이지만 peak sample 위치는 일부 전환한다. 전체 ±10mm에 단일 선형 미분을 외삽하지 않는다.

## 인식 지표와 canonical task 오차

|표현|confidence (정확도 아님)|mask 면적(px)|centroid u,v(px)|ROI 유효/평면 inlier|B5 heading(°)|
|---|---:|---:|---|---|---:|
|HR_Scan|0.791759253|7710|316.307263,163.611414|114/114|90.011093139648|
|LR_Scan|0.972648263|7718|316.015159,163.844519|132/132|89.994220914785|
|GeoCAD|0.959305346|7703|315.957289,163.867195|138/138|89.453897833824|

LR−HR B5 dx=−5.011352100mm, dy=+.208762095mm; CAD−HR dx=−1.883952149mm, dy=−3.434397859mm (사용자 예상 근사치 대신 저장 정밀값). 마스크 bounds/edge pixel 수, ROI depth 0/25/50/75/100% 분위수 및 world centroid/covariance/plane 잔차는 3행 JSON에 있다. HR/LR/CAD bounds는 각각 [250,134,381,193], [251,134,381,194], [250,134,381,194]. 경계가 1px만 바뀌어도 소수 잔존 ROI와 B5 face 통계가 달라질 수 있으나 이것을 독립 인과분해로 간주하지 않는다.

|HR 대비|mask symmetric difference(px)|예측 mask 상호 overlap IoU (GT 아님)|공통 mask same-pixel world 거리 median/p95(mm)|
|---|---:|---:|---:|
|LR_Scan|158|0.979725395|0.657169/20.273214|
|GeoCAD|179|0.977039507|0.792139/43.094120|

동일 intrinsics/extrinsics/render 시각 및 정지 pose를 확인한 후 동일 ray pixel을 비교했다. 이는 표현 간 같은 물체 표면점 correspondence를 보장하지 않는다. 최대 depth 차이는 LR2.243m/CAD2.043m로, 경계·빈틈·가림에서 서로 다른 표면을 보는 오염이 가능하다. 모든 차이를 geometry 거리 오차로 해석하지 않는다. labels 전송·GT 입력·추가 inference는 없다. representation/model/ROI가 함께 달라진 결과다.

**독립 GT segmentation mask는 이 세 capture의 준비 증거에 없다.** pixel precision/recall, accuracy IoU, AP50/AP75/mAP50–95는 UNKNOWN/NOT_AVAILABLE. 위 overlap은 예측끼리의 일치도이며 accuracy IoU가 아니다. 단일 YOLO confidence는 정확도가 아니고 세 이미지로 mAP를 산출하지 않았다. 후속 논문 지표는 독립적으로 라벨링된 충분한 paired scene GT에서 정의된 클래스·matching·IoU threshold로 집계해야 한다.

평가용 canonical은 verified workspace lock의 world XY center(−25.888,30.509)m, task yaw+90°/local_-X다. pilot DRAFT가 start/seed를 바꿨지만 target 정책은 유지한다. canonical FINAL=(−25.888,29.105254968739224)m. 이 값은 **잠금 task design GT**이며 별도 실물 metrology 오차/geometry surface 중심의 독립 검증이 아니다. GT는 이번 평가 산술에만 쓰였고 인식·motion 입력에는 넣지 않았다. B5 heading은 modulo180 대칭, task-facing yaw는 방향을 갖는 modulo360으로 평가한다. 중심 오차는 같은 offset를 더하는 predicted PRE/FINAL 위치 오차와 동일하다. 부호는 pred−GT, longitudinal은 +Y, left는 −X다.

|표현|예측 중심/목표 XY 오차(cm)|종방향(cm)|좌측(cm)|B5 heading 오차(°;mod180)|요구 goal yaw 오차(°)|
|---|---:|---:|---:|---:|---:|
|HR_Scan|5.415594366|-2.721454435|+4.682130722|+0.011093140|0|
|LR_Scan|5.844601652|-2.700578225|+5.183265932|-0.005779085|0|
|GeoCAD|5.754615494|-3.064894221|+4.870525937|-0.546102166|0|

**HR 실제 FINAL**: 관측 목표와의 거리 **.279451388cm**, yaw−.039722360°. 같은 physical endpoint를 canonical FINAL로 평가하면 **5.523288386cm**, yaw absolute .039722360°, 종방향−2.997573290cm/좌측+4.639102173cm다. 원래 canonical evaluator의 posthoc strict(5.5cm) FAIL, main(11cm)/relaxed(16.5cm) PASS이며 controller QC PASS. 이는 새 exploratory 평가이고 기존 engineering 성공/정식 science 분모를 바꾸지 않는다. PRE의 observed-goal 거리는 .288352604cm, yaw−.037820318°. LR/CAD 실제 endpoint/GT task 거리·각도는 모두 **NOT_RUN**, 0으로 대체하지 않는다.

## 단계 분모·한계·다음 작업

|단계|HR|LR|CAD|exploratory 서술 분모|
|---|---|---|---|---|
|유효 detection/B4/B5|PASS|PASS|PASS|3/3|
|PRE candidate 산술 생성|PASS|offline candidate|offline candidate|3/3 offline; runtime LR/CAD는 생성 도중 예외|
|PRE admission|PASS|CURVATURE_INFEASIBLE|CURVATURE_INFEASIBLE|1/3|
|실제 motion 시작|YES|NOT_STARTED|NOT_STARTED|1/3|
|PRE와 독립 FINAL arrival/normal stop|PASS|NOT_RUN|NOT_RUN|1/3 시도; motion 시작1행 중1/1|
|GT task main/strict (posthoc)|PASS/FAIL|NOT_RUN|NOT_RUN|측정 가능한 완료1행; 정식 분모0|

세 행은 각 n=1, 순차 실행, 수동 ROI와 matched model이 포함된 탐색 비교다. ROI preview 실제 reviewer ID는 HR `Codex-visual-review-v30`, LR/CAD `Codex-visual-review-v28`로 저장되어 있다. 이전 요약의 “동일 reviewer code” 주장은 실제 문자열과 다르므로 본 보고서는 raw를 우선한다. 동일 운영자 여부를 문자열만으로 인증하지 않으며 representation 완전 맹검도 아니다. 이 불일치는 오프라인 경로 산술을 바꾸지는 않지만 reviewer 통제가 완벽했다는 주장을 제한한다.

확립된 것은 저장 목표의 mm 차이가 **동일 fixed quintic의 연속적 곡률 변화와 이산적 pass/fail**을 만든다는 점이다. 관측/mask/ROI/depth 통계 차이는 측정했지만 모델 대 geometry 대 heading 대 datum의 독립 원인 기여는 아직 가설이다. 다른 안전한 경로 존재 UNKNOWN. 비유의성을 동등성/비열등성으로 해석하지 않으며 LR은 독립 저감 acquisition 재구성이다. 기존 red-only real validation을 cement·실로봇 배포로 일반화하지 않는다.

다음 전향 작업은 원래 정책 그대로 여러 paired common seeds×load/occlusion 조합에서 세 표현 모두를 반복하고, detection/pose/curve gate/physical endpoint의 단계별 분모와 실패를 보존하는 것이다. 선택적 LR/CAD tuning은 하지 않는다. 별도로 원한다면 동일 steering/footprint/sweep/contact 한도를 유지하는 공통 경로 robustness 후보를 세 표현 모두에 전향 평가한다. v31/v32를 소급 구제하지 않는다. 이번에는 planner/ROI/asset/model 변경·새 Kit·HPO/training이 없다.

## 산출물과 검사

[재현 entrypoint](../analysis/construction_site_pilot_error_propagation_20261102_v33.py), [원자료](construction_site_error_propagation_20261102_v33_02/execution.json), [원자료](construction_site_error_propagation_20261102_v33_02/integrity.json), [원자료](construction_site_error_propagation_20261102_v33_02/sweep.csv), [원자료](construction_site_error_propagation_20261102_v33_02/boundary.json), [원자료](construction_site_error_propagation_20261102_v33_02/comparisons.json), [원자료](construction_site_error_propagation_20261102_v33_02/GT_evaluation.json). 외부 bulk data는 복사하지 않았다. 정밀 값은 JSON/CSV가 기준이다.

실행: `/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_pilot_error_propagation_20261102_v33.py --out reports/<새_미사용_폴더>`. 기존 output overwrite를 거절한다. bounded 441 grid+100 refinement+36 derivative probes와 고정 경로 비교만 CPU로 계산한다. 첫 run은 counterfactual CSV의 interaction 열이 첫 행에 없어 ValueError로 **FAIL**했고 [실패 기록](construction_site_error_propagation_20261102_v33/failure.json)과 부분 출력은 보존했다. 수정 후 새 `_02` root run02 exit0, raw/source hash 및 strict replay/HR array 일치 PASS, 3개 PNG 생성·XY/곡률/heatmap 시각 검토 PASS. 이것은 분석 코드의 재실행이며 실험/관측 retry가 아니다.

변경: 새 analysis v33, 이 보고서, v33 데이터/그림/로그, latest_report, PROJECT_STATE. 기존 locks/weights/source/USD/실패 결과 보존. 미해결: segmentation 독립 GT·반복성·원인 분리·대체 안전 경로·실물 metrology. formal science denominator0, HPO/training PAUSED.
