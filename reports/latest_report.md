# v47 — 설계 목표에서도 거절된219건: 시작 좌표·첫 거부 조건 추적

2026-11-02 KST. **오프라인 실행 완료. 시작 좌표 변환 오류는 입증되지 않았다.** v43은 camera-only viewpoint가 아니라 locked geometry에 따라 rover 전체를 정적으로 재배치했다.319개 inferred start는 독립 capture_record의 authored rover 행렬과 최대 x 1.78e-14m/y 1.07e-14m/yaw 8.91e-14° 차이다.219는 이 두 제한된 경로 정책의 거절이며 물리적으로 가능한 모든 경로의 부재를 뜻하지 않는다.

새 raw root: `/home/user/hh/isaac_cosmos/sdg_final/PERCEPTION_TO_ROBOT_20261102_v47`. v43–v46 재렌더/재추론/새 B5/Kit/ROS/physics/조향/주행/훈련/HPO=0. 기존319는 HUMAN_REVIEW_GATE=PENDING, HUMAN_REVIEW_BEFORE_ROLLOUT=FAIL인 탐색 추정치다. 독립 physical scale-video workstream와 latest_report는 수정하지 않았다.

## 재현·좌표계 근거

`v47_original_reproduction_checks.json`: 원래319 unique case/scene/base key와319 B5집합 exact 일치; frozen old plan AST·pure CPU smooth-S로319×2목표×2정책=1276호출의 모든 status/reason exact PASS. 기존 reason CSV의 표현별 각 셀도 `v47_original_reason_count_checks.csv`에서 대조했다. old 예측11/설계100, smooth 예측29/설계100; 양쪽FAIL219, 예측PASS+설계FAIL0 유지. v46 source 및 결과 CSV expected SHA 일치. 이번에 실제 읽은 dependency 2891개를 이전 v46 SHA inventory 및 시작/종료 SHA로 대조했으며 불일치0. 독립 expected 없는 신규/local 항목은 UNKNOWN으로 남겼다. 전체 v46 27930파일 검증을 새로 했다고 주장하지 않는다. known9 SHA와108/432 count PASS; protocol prelock v01→amendment v02/v03 및 geometry v02 JSON을 직접 읽어 별도 저장했다. geometry lock 자체 독립 expected UNKNOWN 보존.

원본 `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_OCCLUSION_20261102_v43/executed_new_code/three_rep_static_session_20261102_v43.py` 91–98행은 `initial_base_x_m/y_m/yaw_deg`로 rover root transform을 설정한다.82행은 매 render에 동일 rover 행렬을 확인하고143행은 `rover_static_matrix`를 저장한다. 이 source SHA는 각319 capture_record의 code_sha256과 일치한다.117–121행은 원시 renderer view의 inverse transpose와 diag(1,-1,-1)로 optical right/down/forward의 column transform을 만들고 camera XY lock을 확인한다. camera는 rover 하위 prim이고 camera-only pose 설정은 이 loop에 없다. source/read hashes는 `v47_capture_transform_provenance_checks.csv` 및 `v47_source_dependency_sha_checks.csv`.

USD row matrix는 transpose한 후 world column SE3로 비교했다. world Z-up·CCW yaw(rad), goal+90°(π/2), optical forward=T[:3,2]. optical rotation determinant=+1. `inv(T_world_rover)@T_world_optical`의 회전 변화 최대 8.88e-16; mount XY는 .5381308867332306/.00002232m, Z≈.605429366196m로319 전부 동일하다. scene specs의 목표 world XY는 전부(-25.888,30.509), original legacy base manifest task_frame_yaw0을 최종 목표로 사용하지 않았다. C/표현/O 변경에도 같은 base scene의 camera/base가 불변인지 수치표로 추적했다. 따라서 **FRAME_CORRECTED_DIAGNOSTIC와v47_frame_counterfactual_319.csv는 생성하지 않았다.** 근거 없는 보정이나 task-goal yaw 변경도 없다.

요청한 Near/Front·Near/30·Mid/Front·Mid/60·Far/60 각각 HR/LR/CAD 총15예는 `v47_five_strata_three_rep_frame_examples.csv`;319 전체는 `v47_start_pose_calibration_audit_319.csv`다. Near/Front의 실제 시작 y28.470869는 PRE y28.305255보다 앞이어서 세 computed case 모두 rear forward projection=-.165614m다. 카메라 관측 거리와 로버 접근 가능 시작 영역은 같은 개념이 아니다.

nominal v30는 별도 saved observed base pose를 사용했다(`v47_nominal_v30_control.csv`). HR 관측 목표 old/smooth PASS, 설계목표도 둘 다PASS; LR/CAD 관측 목표 oldFAIL/smoothPASS로 과거와 일치한다. nominal camera yaw만으로 단순 XY mount를 빼면 saved settled base 대비 dx1.821377mm/dy1.420273mm/yaw.047433° 잔차가 있다. nominal optical transform에는 pitch/roll가 포함되므로 live에 planar inverse를 일반화하지 말고 완전한 SE3 extrinsics와 관측 base TF를 써야 한다. 이 nominal 잔차를 pure-Z reset인 v43의 오류로 바꾸지 않았다.

## 219 설계 목표 거부의 실제 첫 조건

|정책|첫 거부 조건|건수|source bound/관측값|
|---|---|---:|---|
|old|LOCAL_PATH_DISTANCE|52|.05<D<3m 위반; D3.045877–3.806321m|
|old|FORWARD_GOAL_REQUIRED|3|rear projection>0 위반; -.165614m|
|old|CURVATURE_INFEASIBLE|164|최초 sample abs(k)>.363645332585095/m; curvature 제거 진단후 전체 candidate peak2.736040–27.903401/m|
|smooth|NO_PATH_FOUND_WITHIN_SEARCH_BEARING_BRACKET|219|A∈[-.5,.5]의 endpoint error(lo)≤0≤error(hi) 위반|

old는 거리→전방→sample cusp→sample curvature 순서다. smooth는 bearing bracket→48회 shooting→D/fwd/L assertion→forward heading→upper curvature 순서이므로 같은219의 원인명이 다르다. smooth의 219는 **고정 탐색 bracket 불충족**이지 최대 반복횟수 소진이 아니다. bracket을 넓히지 않았다. old curvature 최초 거절 sample k/t/index/margin은 `v47_old_first_curvature_rejection_samples.csv`; curvature guard를 제거한 최대값은 원래v46 diagnostic 열이며 통과 결과가 아니다. smooth conservative upper와 sampled k를 혼동하지 않았다.

거리/view 분해: NearFront3=old전방, Near30 45·Near60 41·Mid30 70·Far30 8=old곡률, Mid60 43·Far60 9=old거리, MidFront100=양정책설계PASS. smooth는 MidFront100만PASS, 나머지219는bracketFAIL다. material/C/표현/실측가림/설계대비사전오차구간 교차표는 `v47_failure_by_*.csv`; 개별 base cluster와 수치 경계 여유는 `v47_all319_first_predicates_long.csv`, 설계219×2정책=438행은 `v47_design_oracle_219_failure_factors.csv`. 독립 distance/forward/bracket mask도 같이 기록했다. first predicate 분모와 중복 가능한 mask 분모는 다르다.

frame inconsistency=관측0. unsupported occupancy/geometry는 이 함수들의 실행 거부 사유가 아니지만 **319전부 full swept collision/support 미검증**이다. unknown/iteration exhausted/physical blockage를 임의 배정하지 않았다. frozen smooth는 blank assertion도 보존하고 해당 D/fwd/L 복합 조건을 별도 이름으로 표시했다.

![거리·시점별 첫 거부](/home/user/hh/isaac_cosmos/sdg_final/PERCEPTION_TO_ROBOT_20261102_v47/v47_failure_stages_distance_view.png)

예측FAIL+설계PASS89/71의 첫 거부: old 곡률87·전방2, smooth bracket60·곡률11. 전방2와bracket60은 candidate curvature admission 이전에 탈락한다. 각각89/71행을 합한160행 `v47_predicted_fail_design_pass_89_71.csv`에 원래 reason·target·start·margin을 보존했다. 따라서219 geometry/policy문제와 별개로, 예측 중심 오차가 판정을 바꾼 사례도 사라지지 않았다.

## 같은 시작·같은 world datum의79/69 대응 비교

`v47_matching79_69_task_comparison.csv`는79장면×3=237행, all-threeIoU≥.5 표식으로69장면×3=207행이다.각 scene의 authored/inferred start가 세 표현에서 같은 조건임을 확인했다. 전체324 paired ID의 IoU·computed/rejected/miss·오차·두목표 reachability는 `v47_condition324_availability.csv`(972 long rows)에 유지했다. 계산 거절/무검출을0mm나경로FAIL로 바꾸지 않았다.

|subset|장면/cluster|설계곡률PASS장면|old 세예측모두FAIL/그중설계PASS|smooth 세예측모두FAIL/그중설계PASS|예측하나이상PASS old/smooth|
|---|---|---:|---|---|---|
|공통computed|79/47|29|71/21|65/15|8/14|
|공통computed+모두IoU≥.5|69/46|27|61/19|55/13|8/14|

한 표현만PASS한장면은 두subset 모두old6/smooth5. 사례별 rep 목록과design reachability는 `v47_matched_scene_task_patterns.csv`. paired pass-rate delta/cluster bootstrap1000회 seed26110247·95%percentile CI는 `v47_paired_task_bootstrap.csv`. 예:79장면HR−LR old .025316(CI−.023256,.078974), smooth .037975(0,.101477). 이는 computed selected subset의 탐색치이고 다른 subset median의 차이나 HR 우월·동등성·비열등성·실제작업성공을 증명하지 않는다.

## 높은IoU 위치outlier와LR mask오선택 근거

`v47_error_chain_examples.csv`는 요청한high-IoU3 + LR IoU0 17=20건의 stored depth/ROI/plane을 직접 계산한 표다. LR의 IoU<.5 49/133 및0인17/133은 과거와 동일하며 새 관측을 추가한 수가 아니다. predicted mask와 visible target GT의 overlap0은 관측된 평가 불일치다. 팔레트 정체성과 정확한 wrong-object 종류는 사람 검토 전 미확정이다.

| case_id | pixel_iou | error_mm | roi_pixels | stored_inlier_fraction | stored_inlier_only_p95_mm | all_ROI_residual_p95_mm |
|---|---|---|---|---|---|---|
| FE2E_S045_O50_v43_HR_Scan | 0.857672 | 489.962286 | 131 | 0.832061 | 1.786234 | 5.886759 |
| FE2E_S097_O50_v43_HR_Scan | 0.941452 | 498.704740 | 155 | 0.870968 | 0.735488 | 7.127384 |
| FE2E_S098_O50_v43_GeoCAD | 0.900787 | 479.465826 | 156 | 0.871795 | 0.737653 | 7.129511 |

주의: frozen plane_fit의p95는 **3mm내inlier만의p95**다. 전체ROI p95가5.887–7.130mm인 것과 source gate PASS는 모순이 아니다. 두 열을 분리했다. ROI는 target mask를dilate해제외한 작은팔레트후보 영역이며, 이3건은131–156pixel이다. HR S097/CAD S098의world ROI범위 x[-25.4801,-25.3609], y[29.9601,30.4254]와 inlier135수준의 좁은지원이 높은 target IoU와 공존한다. target mask의정확성과팔레트datum/visible edge/고정치수에의한B5중심안정성은 별개다. source transform mismatch는 이자료에서 관측되지 않았다. wrong pallet/background plane·bevel/edge·선택 ambiguity와authored task-design offset의 개별 기여는 독립GT/사람판단없이 확정할수없다. GT를B5입력으로교체하지않았다.

실제 저장배열로 만든8개 RGB+pred(red)/GT(cyan)·depth/ROI(magenta)·residual 패널을root에두었다.3개high-IoU필수사례와5개LR IoU0사례다. AI의패널가독성확인은HUMAN_GATE로세지않았다. 독립실물metrology가아닌authored-design대비오차다.

## 실행 가능한 최소 대안과 실패 보존

추가 `/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/analysis/three_rep_source_staging_diagnostic_20261102_v47.py`를 실제 실행했다. 고정된 historical HR nominal observed base를 단 하나의 staging waypoint로 놓고 **원래start→staging→원래PREgoal** 두구간에똑같은frozen함수·곡률·거리·전방조건을적용했다. terminal center/yaw·물리제약변경없음, scene선택이나모델tuning/HPO없음. `v47_source_nominal_staging_diagnostic.csv`는319×2목표×2정책=1276 candidate route rows다.

**이최소우회안은219에서old0/219·smooth0/219통과로실패했다.** 설계목표staging→PRE는219모두PASS지만start→staging은old 거리93/전방48/곡률78, smooth bracket219거절이다. 원래설계통과100도이경유점을강제로거치면첫구간전방/bracket에서거절하므로대체정책으로채택하지않는다. 경유점탐색·yaw변경·bracket확대는하지않았다. 이는구체적실행가능한후보와그실패증거이며수정성공을꾸미지않았다.

따라서현재실행가능한개선은 local terminal planner를global reachability로오해하지않도록 `v47_global_approach_requests_219.csv`로분리하여검증된occupancy를요구하는gate다. actual개선경로를얻으려면같은terminal+curvature를유지하는별도global approach 정책과articulated sweep/support가필요하다. 이번에는그새정책을설계잠금/충돌인증없이실구동가능하다고제공하지않는다. inheritedplanner의제약을완화해통과수를높인결과0이다.

## 사람검토와다음물리게이트

`review/human_signoff_instructions.md`에원본 `/home/user/hh/isaac_cosmos/sdg_final/PERCEPTION_TO_ROBOT_20261102_v46/review` 경로와10–15분표본우선순서를작성했다. 원래78행checklist의approval/notes/reviewer/time은모두blank,서명0. 별도복제checklist를만들어검토이벤트를늘리지않았다. 이검사는해당원본78행범위이며워크스테이션전체에사람서명이없다고단정하지않는다. pilot54+curated24는새78관측이아니다. v45b extra918 NOT_RUN·역사FAIL/PENDING유지.

v38 policy source와v46 MOTION_BLOCKER_DECISION을read-only로읽었다. 다음순서는①사람ROI서명및사용범위결정②검증된SE3/base TF계약을새planner입력gate에묶기(이번v43변환오류없음)③validatedoccupancy·articulatedsweptcollision/support④출처와승인된measuredsteerabort·stationaryyaw/tracking정책+native solewriter/stop/recovery/복원검증⑤**별도명시승인후에만**freshRGB-D와동결모델로동일HR/LR/CAD motion각1회다. commandedvelocity/configuredcap/계산요구rate로새실측한계를만들지않았다. 실제live0이며offlinePASS는로봇작업성공이아니다.

## 실행·변경·미해결

`run_manifest.json`에4개새analysis명령과source SHA, 환경, gates, bootstrap,실제command로그를기록했다. 첫주실행/supplement/staging모두exit0; finalizer첫출력은tabulate미설치로exit1이며FAILED로그보존,패키지설치없이내장표출력으로수정해attempt02실행; candidate경로거절은그대로실패다. discovery중존재하지않는v43파일명rg exit2는executed_new_code로해결, gitremote exit128은이starter가Git저장소가아님을확인한실패로보존했다. remote sync UNKNOWN. final체크에는개수/transition/사람blank/원본SHA/파싱을포함한다.

변경파일:새analysis4개,이report,docs/PROJECT_STATE.md;외부v47root의CSV/JSON/PNG/로그/사람안내. legacy/v43–v46/USD/GT/mask/B5/weights/geometrylocks/scale-video출력불변. latest_report미갱신으로독립scale-video최신기록과history를보존했다. bulk는Git밖이다. 원격push/실행권한확대없음.

PASS:1276원래상태재현,319 frame 검증,reason/319/79/69연결,source불변. FAIL:single nominal staging대안0/219,역사v44사전사람검토FAIL. UNKNOWN/미완료:팔레트정체성·독립위치metrology·새global approach경로·장면별sweptgeometry/support·승인된실측조향abort/nativecontrol·remote sync. 다음구체행동은기존78패키지에서심한outlier와LR IoU0표본을사람이검토·서명하는것이다. 자동추가simulation/주행은없다.
