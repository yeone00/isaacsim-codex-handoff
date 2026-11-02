# v45 — v43 대응 감사·3×3 교차 평가·두 재질 정적 시험 실제 결과

2026-11-02 KST. **324개 대응 장면 검사 PASS, 원래 972개 저장 RGB에서 2,916개 모델–이미지 평가 완료, 새 두 팔레트 정적 RGB-D 108/108 완료.** 추가로 새 혼합 영상에 세 모델을 적용한 324개 추론을 완료했다. 새 주행·조향·ROS·physics play·HPO·Ray·학습은 0이다. B5는 새 파일럿54 중51계산/1거절/2무검출, 추가918은 사람 ROI 검토 게이트 때문에 NOT_RUN이다. 전체 요청을 무조건 PASS로 판정하지 않는다.

외부 원자료·CSV·PNG·마스크 root: `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_CROSS_AND_MIXED_20261102_v45`. 원본 v43 root는 변경하지 않았다. HR_Scan / LR_Scan / GeoCAD만 비교했다. LR은 독립 저취득 재구성이며 HR decimation이 아니다.

## v43 실제 데이터 감사 A1–A4

실제 파일에서 972행·324 scene_id·각3표현을 확인했다. material/C/명목O/거리/시점/조명/잔존 벽돌 membership/trajectory/panel 좌표/rover pose가 동일하고 카메라 extrinsic·intrinsic은 절대오차1e−9 이내다. seed·geometry·mask membership은 `scene_specs_locked.json`의 공유 설정 SHA로 결합했다. **실제 가림률은 표현별 값이며 공통키의 equality 조건으로 강요하지 않았다.** `v43_audit_common_324.csv`는 324키×3행=972행이다. `pairing_checks.csv`는324행이다.

원본 capture receipt의5832개 파일 SHA를 포함해10525개 입력 SHA를 다시 검증했다. 원본 expected193개 dependency도 재검증 PASS, known9 잠금/count PASS. prelock v01→amendment v02/v03→geometry v02를 사용하며 geometry lock 자체 독립 expected는 UNKNOWN으로 유지한다. 입력SHA 목록은 `immutable_input_sha256.json`이다.

검출 패턴 순서는 HR/LR/CAD다.

|pattern|count|
|---|---|
|000|16|
|001|8|
|010|27|
|011|35|
|100|1|
|101|7|
|110|12|
|111|218|

세 표현 모두 검출218개, 모두 선택IoU≥.5인 장면173개다. 공통 집합 수치:

|subset|representation|n|mean|median|q25|q75|
|---|---|---|---|---|---|---|
|unconditional|HR_Scan|324|0.6778607675001871|0.9436559586448814|0.0|0.9687446276416856|
|unconditional|LR_Scan|324|0.635469737434991|0.9330338364369778|0.00018034816530355|0.96564490177102|
|unconditional|GeoCAD|324|0.7449061042583013|0.91595543409712|0.7692379911918337|0.9494533095952435|
|all_three_detected|HR_Scan|218|0.9317449862104317|0.9601122834793296|0.934603889391912|0.9725991626454661|
|all_three_detected|LR_Scan|218|0.760510596591542|0.948084770328331|0.879136598920006|0.9693901351837773|
|all_three_detected|GeoCAD|218|0.9044663808248516|0.9262181936835148|0.8845150609706857|0.9528629684167381|
|all_three_iou50|HR_Scan|173|0.9462096440467551|0.961253612716763|0.939622641509434|0.974950560316414|
|all_three_iou50|LR_Scan|173|0.9452838394387848|0.9606907822092664|0.9374570446735396|0.9725792630676948|
|all_three_iou50|GeoCAD|173|0.9082511039888367|0.9278562259306804|0.886687306501548|0.9562144935568796|

전체 평균은 무검출을0으로 유지했다. 검출된 서로 다른 집합의 조건부 평균을 직접 비교하지 않는다. 같은 장면 전부 검출 집합에서는 HR−LR 평균차.17123, HR−CAD .02728, LR−CAD −.14396이다. 모두 IoU≥.5인 집합에서는 HR−LR .000926이다. 조건부 표본 선택이 결과를 바꾼다. 전체 unconditional HR−LR .04239의 탐색95% CI [−.02698,.11007], HR−CAD −.06705 [−.11763,−.01866], LR−CAD −.10944 [−.17904,−.04311]. 모든 win/loss/tie와 CI는 `paired_diagonal_deltas.csv`다. 원래108 base_scenario_id를 재표집해 O triplet을 유지한2000회 cluster bootstrap(seed261102)이다. 다중검정 보정된 확증적 우열·동등성·비열등성 주장은 하지 않는다.

`hr_86_misses.csv`에 정확한 원래 HR 무검출86개 ID와 LR/CAD의 검출·신뢰도·IoU, 원래 조건 및 actual 가림률을 저장했다. `hr_86_threshold_trace.csv`/`threshold_sweep.csv`에는 별도 conf.05 추론의 후보를 .05/.10/.25/.50으로 필터한 진단이 있다. HR86개 중 .05에서22개 검출,14개 IoU≥.5 회복,8개는 충분한 GT 일치가 없는 검출이다. .10에서는14검출/12일치, .25/.50에서는0이다. 부정확 검출8개를 모두 배경 false-positive라고 단정하지 않는다. low-conf candidate trace와 GT-match logs로 구분 가능하다. 새 최적 threshold를 선택하거나 baseline으로 승격하지 않았다. 낮은 threshold 호출의 NMS와 .25 직접호출은 별도 기록했으며 .25 집계도 원래와 일치했다. 대표 GT 윤곽 및 low-confidence overlay를 저장했다.

`Cxactual_occlusion_summary.csv`는 C×명목O와 거리/시점/조명/재질의 세분 분모·조건부/무조건 IoU를 제공한다. `Cxactual_occlusion_bootstrap.csv`와 `C_actual_occlusion.png`는 measured continuous 가림 및 구간별 기술분석/cluster CI다. 기존 O50 최저21.79%를50%로 취급하지 않았다. 원래 Near 사선에서 표면 일부가1m판보다 앞에 있었던 설명은 유지한다. 새 상관 패턴을 깊이 문제의 독립 인과 증명으로 부르지 않는다. factorial cell 반복1이어서 세부집단 분산 추론은 제한된다.

GT는 표현별 렌더의 semantic brick_load union이다. 단일 load에서의 union을 두 인스턴스 판별능력이라고 하지 않는다. visible GT는 외부 판 적용후 가시면, external-only amodal은 판을 숨긴 투영이며 자기 가림 뒤 전체 형상 GT가 아니다. 972개 shape640×480·정렬·GT외부픽셀·mask IoU 재계산 PASS. fragment count/작은 연결성분은 `instance_audit_cases.csv`, 설명은 `instance_eval_audit.md`다. 높은 신뢰도 class0/동률최소index를 선택했다. `GT_matching_oracle_diagnostic.csv`는 GT와 가장 잘 맞는 후보를 **점수 계산에만** 택한 상한이며 deployable selection/B4/B5 입력이 아니다. 원래 diagonal은 모델 출처와 렌더 표현이 함께 달라진다. pixel IoU와 IoU threshold는 AP/mAP가 아니다.

## B — 균형3×3 실제 교차 추론

각 셀324장, 전체2,916 모델–이미지 기록이며 원본 고유 RGB는972장이다. 새 캡처2,916장이 아니다. off-diagonal1,944개를 새로 추론했다. 감사 강화를 위해 diagonal972개도 재추론해 원본 검출972/972 일치·선택mask pixel 차이0·IoU최대오차1.11e−16(허용1e−6)을 확인했다. 원본 inference는 불변이다.

공통 설정 imgsz1280/conf.25/NMS IoU.70/mask threshold.5, RGB→BGR 입력 변환은 실제 v43와 같다. 모델은 class0 brick_load 하나뿐이다. 모델 origin과 render domain을 별도 축으로 저장했다.

|model|render|n|detected|iou50|iou75|mean_iou|conditional_mean_iou|ci_low|ci_high|
|---|---|---|---|---|---|---|---|---|---|
|GeoCAD|GeoCAD|324|268|267|249|0.7449061042583013|0.9005581260436178|0.6959725880196681|0.7904551809443802|
|GeoCAD|HR_Scan|324|255|253|229|0.7068197634838084|0.8980768759558977|0.6629781373014091|0.7538930487703471|
|GeoCAD|LR_Scan|324|242|238|222|0.6698358267182636|0.8968049911434602|0.6184550040620893|0.7201613656900535|
|HR_Scan|GeoCAD|324|187|180|172|0.5250607636892106|0.9097309488518945|0.4548252398018959|0.5900517652583691|
|HR_Scan|HR_Scan|324|238|231|224|0.6778607675001871|0.9228020532355489|0.6169801267197396|0.7391859663243942|
|HR_Scan|LR_Scan|324|222|218|216|0.640934467910467|0.9354178720855464|0.5769428440807477|0.7051572437295114|
|LR_Scan|GeoCAD|324|233|144|125|0.40075416676188913|0.5572718885444294|0.3422991449838768|0.4650870366171675|
|LR_Scan|HR_Scan|324|280|198|191|0.5806754601146292|0.6719244609897852|0.5238485391091462|0.637294589525746|
|LR_Scan|LR_Scan|324|292|218|210|0.635469737434991|0.7051102566059488|0.5811706619151105|0.6895051406353249|

|model|n|equal_domain_mean_iou|ci_low|ci_high|diagonal_mean|off_diagonal_mean|diagonal_minus_off|
|---|---|---|---|---|---|---|---|
|GeoCAD|972|0.707187231486791|0.664006766315515|0.7511361933105911|0.7449061042583013|0.6883277951010359|0.05657830915726536|
|HR_Scan|972|0.6146186663666215|0.5554279075370795|0.6726860278422411|0.6778607675001871|0.5829976157998388|0.09486315170034831|
|LR_Scan|972|0.5389664547705031|0.48937936983701247|0.58928474322182|0.635469737434991|0.4907148134382592|0.14475492399673184|

이 표본의 동일 render 열에서도 CAD 모델은 무조건 평균IoU가 가장 높았으며, LR은 더 많은 검출과 낮은 선택mask 일치가 함께 나타난다. 순수 기하 인과효과나 sim-to-real 검증으로 확대하지 않는다. 같은 이미지 내 모델간 차이·승패와 base cluster CI는 `same_image_paired_comparisons.csv`다. `cross_rep_detection_IoU_heatmap.png`에 검출/IoU/IoU≥.5를 함께 표시했다. 후보 confidence·GT-match는 `cross_all_candidate_GT_match_logs.csv`, 후보/선택mask는 `cross_predictions/<model>__<case>/`에 저장했다.

## C — 빨강1+시멘트1 실제 정적108장

3표현×red C3×O3×좌우2×seed2=108개,36개 공통 설정이다. cement는C100이며 외부판이 빨강 target에만 적용되도록 target bbox 범위에 panel을 구성했다. 고정 center-front/Mid camera·상속 Nominal 조명, x오프셋±.75m, seed별 공통 y오프셋±.02m를 사전에 고정했다. 각 표현의 red/cement 자산을 각각 사용했다. 별도 물리 pallet2개와 GT stack label2개가 있으며 화면crop·mask overlap0이다. 색상 heuristic은 적용하지 않았다.

`mixed_108_cases_locked.csv`와 `mixed/policy_locked.json`은 관측 전 고정했다. 첫12장은 C100/O0×좌우2×seed2×표현3이며 `mixed/pilot_12_released.json`과 `mixed_pilot12_GT_contact_sheet.png`로 먼저 공개했다. 나머지96장도 같은 단일 세션에서 취득했다. 패널은 모든 표현 target 최소 depth의절반에 두고, 추론 결과를 보지 않고3표현 silhouette의 공통 minimax column을 고정했다. 각 표현별 튜닝은 없다.

실제 O0=0, O25=23.7857–25.4809%, O50=49.2238–50.4256%, **108/108 새±2%p 범위 충족**. GT의 사용은 fixture calibration과 사후 scoring뿐이며 frozen-model 추론·후보선택에는 없다. 캡처 결과는 actual만108행, 나머지 예정행을 성공으로 채우지 않았다.

선택baseline은 class0 최고신뢰도다. 선택mask red IoU≥.5/cement<.5이면 RED_TARGET, 반대이면 WRONG_CEMENT, 검출없으면 MISS, 그 외 AMBIGUOUS_OR_LOW_IOU로 사전에 점수화했다. 이 IoU association cut .5의 명시적 scoring 규칙은 실행 inference 소스에 기록되며, 별도 관측 전 policy파일에는 association cut이 상세히 기록되지 않았다는 문서 한계가 있다. 모델이 언어로 지시한 빨강을 이해하거나 빨강/시멘트를 분류했다고 하지 않는다.

|scope|model|render|n|red|wrong_cement|miss|ambiguous|oracle_red50|oracle_cement50|both_coverage|
|---|---|---|---|---|---|---|---|---|---|---|
|matched|GeoCAD|GeoCAD|36|11|25|0|0|25|35|24|
|matched|HR_Scan|HR_Scan|36|18|10|5|3|21|27|17|
|matched|LR_Scan|LR_Scan|36|13|18|0|5|24|28|18|
|all3|GeoCAD|GeoCAD|36|11|25|0|0|25|35|24|
|all3|GeoCAD|HR_Scan|36|13|22|0|1|21|36|21|
|all3|GeoCAD|LR_Scan|36|10|26|0|0|22|36|22|
|all3|HR_Scan|GeoCAD|36|19|0|15|2|21|0|0|
|all3|HR_Scan|HR_Scan|36|18|10|5|3|21|27|17|
|all3|HR_Scan|LR_Scan|36|14|22|0|0|19|35|18|
|all3|LR_Scan|GeoCAD|36|9|0|2|25|20|1|0|
|all3|LR_Scan|HR_Scan|36|12|6|1|17|21|19|9|
|all3|LR_Scan|LR_Scan|36|13|18|0|5|24|28|18|

matched만108평가, all3는동일108저장영상에서324평가다. Oracle coverage는 GT-best matching 상한이며 실제 최고confidence 선택과 다르다. `mixed_target_confusion_heatmap.png`, `mixed_material_GT_predictions_contact_sheet.png`, `two_stack_candidate_predictions.csv`와 모든 candidate masks/overlays가 있다. semantic material recognition은 **NOT_ESTABLISHED**다.

발견한 결함: locked red_position의 left/right가 실제 영상 좌우와108개 모두 반대다. 원래case ID/잠금/표본은 수정하지 않았고 `mixed_instance_geometry_audit.csv`의 actual_red_position에 영상에서 측정한 좌우를 별도로 제공한다. 양쪽이 균형이라 aggregate 분모는 유지되지만 좌우별 해석에는 반드시 actual 열을 사용해야 한다.

## A5 — B5 부분완료와 기존v44의 충돌 해결

요청문은v44 미실행이라고 했지만 로컬에는v44 manifest/실행CSV/소스/로그가 실제 존재했다. manifest가 고정한5658개 sourceSHA를 직접 재검증해 PASS,972행 역사자료를 `B5_v44_historical_verified.csv`로 구분해 참조했다. 이 자료의319계산/479거절/174무검출 및 **HUMAN_REVIEW_BEFORE_ROLLOUT=FAIL**을 그대로 보존했다. v44를 없는 실행으로 만들거나319건을v45 새 결과로 세지 않았다.

v45는 sensor-only estimator의 감사한 AST 함수만 추출해 새54 pilot에서 재실행했다. erosion2/brick exclusion3/inlier80%·100point·3mm/5° 및height/연결표면gate 유지, GT ROI 보정0이다. 첫wrapper는 `__file__` 누락으로54건 FAILED였다. 실패 CSV/log/source를 보존하고 새v45b에서 namespace만 수정해54건 재검사했다: **계산51(HR16/LR17/CAD18), datum거절1, 원무검출2**. 추가918은 사람의 ROI검토 전 확장게이트 때문에 NOT_RUN이다. `B5_972_offline_results.csv`에 최종상태와 최초실패상태를 함께 남겼으며 실패54개를 분모에서 지우지 않았다. v45b estimate의codeSHA는추출된원함수source를 가리키며 wrapper SHA는final_validation에별도 있다.

계산51건의 task-design(-25.888,30.509)/yaw90°에 대한 signed X/Y/heading과 old/smooth offline 결과는 `offline_planner_summary.csv`다. old곡률4/51, smooth12/51 통과이며 full geometry0/실제로버0이다. heading은180°주기 convention을 유지했으며 큰오차도그대로 남겼다. independent physical metrology 인증이 아니다. 다음 구체 작업은 **54개sensor ROI/plane의 사람 검토 기록을 확보한 뒤 별도버전으로918개 rollout**이다. 같은알고리즘 재실행이 미충족 사람검토를 대신하지 않는다.

## 실행·실패·보존 및 판정

Kit1회, timeline stopped/OmniGraph attach전 비활성화/rover world pose 불변검사. 시작→close139.321초, sampled RSS최대7.72075GiB≤8GiB, exit0/owner잔존0. close_return관측0이며 process정상종료와구분한다. renderer `[Error]`0이지만 **Warning824줄, 초기flattened prototype 미해결reference 경고600줄**이 있다. 복사초기 내부 prototype을 새 layer에 가져오지 않아 발생했으며 capture전brick visual references를각자산class로설정한뒤실제양쪽mask를확인했다. 전체로그를warning-free라고하지않는다. 후속패치는fixture복제시내부reference closure를포함하거나초기clone을instance reference로구성한뒤attach전모든visualbinding을완료하는것이다. 이번추가Kit재시도없다.

감사manifest 저장전 시작된 첫cross호출은FileNotFoundError로종료해 `cross_startup_failure.log`에보존했다. 이후manifest생성후 실제2,916추론완료. 초기mixed소스compile unmatched괄호FAIL도실행전수정했다. standalone sdg_tools의pxr불가도확인해실제Isaac USD library 경로로read-only fixture검사를수행했다. B5첫실패54와새v45b를구분했다.

실제 명령은 scripts/three_rep_cross_infer_20261102_v45.py 및mixed_infer를 `/home/user/anaconda3/envs/sdg_tools/bin/python`으로 실행, Kit은 `/home/user/anaconda3/envs/hh_isaac51/bin/python scripts/three_rep_mixed_session_20261102_v45.py`이다. 추론환경 torch2.7.1+cu128/ultralytics8.4.129/numpy2.4.6/Python3.11.15. 설치·업그레이드0. 코드snapshot은 `source/`, 전체SHA는 `final_validation.json`에 있다. 원본weights/USD/v43RGB-D/GT/추론/lockedartifacts expected를수정하지않았다.

모델SHA:

- HR `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`
- LR `d58e18a87f4cafba6fd92d8bade6e2ff12ad2380db427311b072859fd2cca42f`
- CAD `bbfb9fc8d0c421154844f7e299b6d8162b9394eb07d36a31110f593c0813ce8f`

주요 실행sourceSHA:

- `three_rep_B5_recheck_20261102_v45.py`: `f7ca0ea52e08ce691ef03c119336eea3588c8684635f97324f4ea03bdaaaa131`
- `three_rep_cross_infer_20261102_v45.py`: `4b3dba7b4977971c06dabce0ac6ef26ae4126e34dc8bec2d933ad755f7d5c85c`
- `three_rep_mixed_session_20261102_v45.py`: `357b6491313a950b3ed255ae9ae93433d44f15993be8dec4fbe5554e26e82e32`
- `three_rep_B5_recheck_20261102_v45b.py`: `049498f51c8b1c08ac2a46c7bc2153ee42eec860a476171cc7476a58b4255967`
- `three_rep_mixed_infer_20261102_v45.py`: `40690fac7d191222897066ef48b9409a536d7a346844195a5fc4ddd87276d171`
- `three_rep_final_verify_20261102_v45.py`: `960f63a5bb776907467e67267c0b5d8f82f33701ab70c6eb807c01299fb8ab9c`
- `three_rep_cross_results_20261102_v45.py`: `0c14c8994c29aa324ea4231756011c29a59b9f3e63c9a34e2752f422e9b7d679`
- `three_rep_extra_diagnostics_20261102_v45.py`: `4216f288eedbd35273f27fbf59645ac4aa63ce548f3028cbaa5309bcb4377b0e`
- `three_rep_cross_audit_20261102_v45.py`: `9cf594def615511888015e8241bb1e53a251aac1ded1de65ba58bead6fab362a`

판정: A1–A4 실제CSV/그림및B2,916/C108actual취득·324추론 **RUN**, B5파일럿54 **RUN**, 추가918B5 **NOT_RUN/HUMAN_REVIEW_HOLD**. mask성과는주행성과가아니다. RealTest189는이미역사평가완료이며선택/재평가에사용0, real외부검증red-only범위불변. v30HR n1성공과v31/v32curvatureFAIL/v38steeringHOLD는불변이다.

변경파일은새v45/v45b code9개, 본보고서/latest_report/PROJECT_STATE다. bulk는Git밖에있다. `.git`없음으로stage/push없고원격동기화완료는UNKNOWN이다. HANDOFF marker는정상보고서동기화요청이며실험추가승인이아니다.
