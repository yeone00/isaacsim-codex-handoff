# C-V02 HR 무검출 분석·기술 파일럿 판정 개정 및 독립 실행 현황

갱신: 2026-11-13T18:14:59.108602+09:00

## 현재 실행 상태

RUNNING_ENGINEERING; pilot기술통과=15/15; task성공=0; main=0/540

Controller PID 2823783, 현재 {'role': 'engineering', 'attempt_id': 'ENGINEERING_HISTORICAL_ROUTE_HR_C100', 'pid': 2850513, 'output': '/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_e2e_v03/engineering/ENGINEERING_HISTORICAL_ROUTE_HR_C100', 'log': '/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_e2e_v03/engineering_ENGINEERING_HISTORICAL_ROUTE_HR_C100.log'}. 독립제어시험 RUNNING_ACTUAL_CONTROL_TEST. Main gate HOLD. HOLD 원인 None.

기존540단일적재물/O0/36base/5C/3rep·C06·75:25·seed42·층수prior4/4/3/2/1·Main.11m/7.341774deg·도달5mm2deg·속도정지.03mps는변경없음. 학습/HPO/모델선정/정적Test 변경0. 기존HR무검출/4크래시/복구시험은보존. 이번작업은빈Kit/v30비교나기본15등록시험을다시실행하지않았다. 기존HR full파일럿은원본그대로새기술판정만적용하고재실행하지않았다.

## HR-C100 무검출 원인: 확인된 사실

- 실제적재물·팔레트가이미지에존재. 평가전용3D bbox 투영좌표 [235, 136, 407, 208],크기 172×72px,화면밖잘림False. 실제Depth점 11221개가타깃3Dbox(1cm진단범위)안에위치. 이GT는모델/마스크선택/pose계산에전달하지않음.
- 투영bbox ROI 밝기평균 12.857/255,중앙값 1.0,20미만픽셀 82.84%. 창가역광에서적재물매우어두움. ROI는정확한GTmask아닌boundingrectangle이라static의mask내평균과같은분모로비교하지않음.
- PNG와원본RGB.npy 완전일치,cv2 BGR=RGB채널역순,PIL RGB입력과numpy BGR입력의고정운용추론일치. shape640×480·calibration정상. 체크포인트SHA일치,클래스brick_load/마스크출력해석정상.
- conf.25운용후보0 재현. 별도conf.001진단후보 2개,최대confidence 0.01680009. 최대후보bbox [233.24652099609375, 210.51869201660156, 418.5069580078125, 237.06773376464844]는brick bbox 아래팔레트쪽으로나타나며GTbrick bbox와겹치지않음. 낮은threshold로실험성공을만들지않음.
- 동일HR체크포인트로고정한static C100 Train/Val/Test각1장추론은후보1/4/5개. Train 예confidence약.965. 모델자체로딩/출력파싱이전부고장난상태는아님. 이3장은진단예시이지도메인성능의새정확도평가나모델선정이아님.

## 촬영 도메인·계약 비교

`perception_diagnosis_20261113_v01/camera_domain_comparison.csv`:

- static B1_CLOSED_EV vs물리v30건설실내배경은다름. 각각높은실내조명/노란통로와창가역광·다른바닥배경.
- 해상도둘다640×480,카메라높이는static.6m vs로버약.596m.
- fx/fy static554.256px vs로버317.043px;로버시야각이더넓음.
- 시선pitch static예시−4.17~−5.61deg vs로버−19.945deg. 카메라는동일해상도여도동일광학/시점이아님.
- 정적HR타깃canonical-mask내평균밝기예시Train48.14/Val38.52/Test30.63. 물리투영bbox의중앙값1과어두운영상은강한관측차이증거이며분모차이/시점/재질·역광이함께바뀌어원인별효과를독립분리한것은아님.
- static잠금tonemap6/ISO25/shutter50/f5는알려져있으나원래v30물리캡처의당시전체carb tone/exposure값은저장되지않아완전동등성은확인불가. 기존mounted camera의FOV/pitch차이는실측차이지RGB채널버그로판정하지않음. 임의카메라·노출·조명변경으로성공을유도하지않았다.

판정: 화면밖/거의관측불가/채널오류/잘못된checkpoint·출력해석은현재증거로배제. **역광·어두운재질및촬영도메인차이에따른모델실패가유력**하나단일변수인과확정은아님. 낮은confidence에서의두후보도유효brick검출이라는뜻아님. 이연구실패는성공조건으로수정하지않음.

## 별도로 확인한 저장 캘리브레이션 문제

이전15기본검사metadata는축약schema로raw_parameters/provenance가없었고,USD카메라형상scale (.124,.026,.029)가회전행렬에섞여있었다. 처음오프라인pose에서PIPELINE_ERROR_KeyError를기록했고,단순schema변환후에도그scale때문에3D점이카메라주위높이약.59m로압축되어insufficient_side_points가나왔다. 모두분리기록보존.

`analysis/c_v02_drive540_saved_calibration_pose_20261113_v02.py`는저장된intrinsics·extrinsics에서정식E2E가이미사용하는column-scale제거/직교성검사를동일적용하고기존parser가읽는2개projection계수와view행렬을유도했다. fullraw카메라센서버퍼가복원됐다고주장하지않는다. GT입력0/행렬round-trip PASS. 기존데이터/알고리즘수식/주행카메라설정을수정하지않고별도진단adapter만사용.

그결과저장15영상에서운용검출9/15,9마스크모두ROBUST_A계산성공,6무검출은pose미진입. **이15개는한base의진단결과이며540회주행성공률이아님.** 정식E2E는처음부터scale제거·raw_parameters및7개renderer보정검사를사용했으므로이문제는HR무검출의원인이아니며이번운용pose식변경이필요하지않다.

## 파일럿 기준 개정 및 검증

새 `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_policy_amendment_v01/technical_policy.json`: 전파일럿SUCCESS요구삭제. 정상NO_DETECTION/기하학적pose거절/이동전경로거절/안전하게완료한Main오차초과는과학적실패로보존한다. 센서/보정/모델SHA/기록누락/PIPELINE_ERROR/nativecrash/제어상태불명/접촉·속도·조향/정지인증위반은HOLD.

무검출의정상처리는driver미시작+nonzero명령0+실측quietPASS+최종graph-wheel-zero+observer정상종료+강한pre-drive 물리/카메라기록을검사한다. 초기zero receipt가없는것을운동후stop인증으로둔갑시키지않음. **이판정은actual_motion/control_motion_certified=False**로남는다.

원본HR파일럿결과FAIL_A는그대로두고새assessment에서PASS_TECHNICAL/task_success=False로기록. `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_policy_amendment_v01/validator_regression_v01/result.json`의8안전회귀시험PASS: 정상무검출수용,무이동으로제어인증불가,속도guard/보정/PIPELINE_ERROR/모델SHA/비제로명령/필수증거누락HOLD. 실패/중단출력은덮어쓰거나완료로간주하지않고재개시그결과/기술상태를재검증한다.

독립실행기는 `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_e2e_v03`. 단일GPUlock,동일사전등록Base01 15대표조건(기존HR재사용/나머지14freshE2E),immutable SHA,정상실패후안전종료→다음조건구조. 성공시키기위한쉬운base교체없음. 기존첫base의일부경로가CURVATURE_INFEASIBLE로거절되는것도정상연구실패이지controller상한을완화할근거가아님.

## 실제 대표15조건 상태

|표현|C|운용검출수|pose상태|과학적결과|기술판정|
|---|---|---:|---|---|---|
|HR_Scan|C100|0|NO_DETECTION|FAIL_A|PASS_TECHNICAL|
|LR_Scan|C100|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|GeoCAD|C100|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|HR_Scan|C80|0|NO_DETECTION|FAIL_A|PASS_TECHNICAL|
|LR_Scan|C80|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|GeoCAD|C80|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|HR_Scan|C60|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|LR_Scan|C60|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|GeoCAD|C60|0|NO_DETECTION|FAIL_A|PASS_TECHNICAL|
|HR_Scan|C40|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|LR_Scan|C40|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|GeoCAD|C40|0|NO_DETECTION|FAIL_A|PASS_TECHNICAL|
|HR_Scan|C20|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|LR_Scan|C20|1|B5_COMPUTED|FAIL_C|PASS_TECHNICAL|
|GeoCAD|C20|0|NO_DETECTION|FAIL_A|PASS_TECHNICAL|

CSV: `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_policy_amendment_v01/representative_15_actual_technical_results.csv`. PENDING은미실행/미완료이며실패로계산하지않음. 실제prediction mask는존재시원bitmap저장·오버레이확인가능;정확한물리GTbitmap이없어MaskIoU를가공해제시하지않음. sourceGTgeometry/scene/원본RGBDepth를보존해후속평가가능. 무검출은NO_MASK이지계산된IoU값이아님.

## 실제 이동·정지 및 본실험 gate

독립제어시험: RUNNING_ACTUAL_CONTROL_TEST. 고정된과거v30검증route의두goals와기존검증start를새engineering-only role로사용한다. 이좌표는현재Test GT/정답mask/신규pose를주입한운용E2E가아니라독립적인controller입출력시험. 새scope를engineering_reference_goals.json·sourceSHA·run_spec에명시하고**E2E성공/본540분모로집계하지않음**. 본540장면/시작조건을이engineering경로로대체하지않음.

Fullactual이동,원TC-S경로·곡률·조향·속도상한,PRE/FINAL5mm2deg+정지인증,ROScleanup/실측quiet/video/JPEG·원trace가PASS해야만control_motion_certified. source의메모리8GiB/GC/timeout도유지. 15개무검출처리PASS만으로이gate를대체불가.

본실험은15기술조건PASS +독립실제이동/정지PASS +필수증거/모델·프로토콜SHA/디스크25GiB및540회전망조건을모두통과해야자동진입. 그렇지않으면HOLD/ntfy. 540ID전체PENDING/RUNNING/과학적성공·실패/HOLD를분리하며이미완료된시도중복실행금지. Wilson은nominal이항가정과원천10family·36base반복구조의한계를별도보고하며비열등성마진을임의고정하지않음.

## 시각자료·재현 자료

- [실제 RGB/운용예측 비교 contact sheet](/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/perception_diagnosis_20261113_v01/RGB_operational_comparison_contact_sheet.png)
- [HR 투영bbox 진단](/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/perception_diagnosis_20261113_v01/HR_pilot_eval_bbox_DIAGNOSTIC_ONLY.png)
- 낮은confidence진단각PNG/JSON은같은diagnosis디렉터리. raw이미지는공개GitHub에올리지않음.
- 카메라도메인CSV/축약metadata수정전후/대표15오프라인poseCSV/실제15기술결과CSV/원본모델·배열SHA보존.
- 소스/입력잠금 `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/technical_e2e_v03/execution_lock.json`, 과학프로토콜·540manifestSHA불변. 기술판정개정SHA별도.
- 상태: `bash /home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/status.sh`. Controller service c-v02-drive540-technical-20261113-v03, watchdog service c-v02-drive540-technical-watchdog-20261113-v01. Codex호출은실행필수의존성이아님.
- 재개는같은controller service의수동start로완료artifact기술검증/중복방지하되HOLD/부분출력은자동덮어쓰지않음. 중단작업은새버전/attempt계획검토필요. 서비스Restart=no이며실패를성공까지반복하지않음.

현재성공률0%라고해석할수없음: main실제완료 0/540. 기술파일럿성능과main분모별도. 본문갱신전버전은report_history에보존.
