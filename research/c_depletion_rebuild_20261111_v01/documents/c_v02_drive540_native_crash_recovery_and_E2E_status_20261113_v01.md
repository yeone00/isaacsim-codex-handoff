# C-V02 540회 네이티브 크래시 복구 및 실제 Full E2E 파일럿 결과

시각 2026-11-13T17:42:23.140117+09:00

## 결론

**Kit 네이티브 크래시는 실행 초기화 순서 복원으로 재현 없이 통과했다.** 실제 새 단일 적재물15조합에서 RGB-D/PhysX등록·접촉을 기록했다. 이어 HR-C100 Full E2E 파일럿의 강한 물리·카메라 검사를 통과했지만 **고정된 HR 모델 NO_DETECTION**으로 마스크/위치추정/경로/주행 전에 멈췄다. 본실험0/540,현재HOLD. 크래시복구와주행완료를구분한다.

## 원인 분리와 확인 범위

|진단|실제결과|
|---|---|
|A 빈 Kit,60 update|PASS,정상종료|
|B 원래v30,extension직후비어있지않은stage로딩|first update nativeSIGSEGV,신규C에한정되지않음|
|C 신규C,graph분리 첫진단|expired-prim Python실패. app.close후exit0으로남았으며PASS아님|
|C 수정된graphs-off 진단|여전히nativecrash. graph비활성만으로해결안됨|
|D ROS/로봇extension활성후빈update5회→빈stage60update|PASS|
|E 원래v30,동일한빈update5회→원래graph그대로stage60update|PASS,정상종료|
|신규C,동일초기화복원|15조합basic실행통과,이후HR-C100엄격물리/센서진입통과|

원래검증된 `scripts/stage4_ablation_drive_session_20261111_v04.py`에는extension활성후빈app.update5회가있었다. 최초새admissionv01~04에는이절차가빠져첫stage update에서OmniGraph core/image native스택으로crash. 동일v30에서준비update유무를바꾼대조로 **stage로드전extension초기화장벽 누락이라는실행순서 의존성**을확인했다. 수정은원래5회를그대로복원한것이며안전숫자변경아님.

정확한C++포인터/특정OmniGraph노드가문제를일으키는내부기전까지확정한것은아니다. native스택의vector관련표시가가까운exportedsymbol일수있어실제함수명/소스라인으로단정하지않는다. pending extension/imagegraph 초기화의일관성 문제는유력기전이지만내부race확정은아님. 원래4건로그·덤프및추가분리실패는모두보존. 초기C진단을종료코드만보고정상으로설명했던실수는즉시정정했으며이번판정은result.json/state/실제update기록을검증했다.

## 복구 구현·변경 범위

- 실제기본검증worker `scripts/c_v02_drive540_physical_admission_20261113_v06.py`:원래extension후5update복원,Usd instance proxy까지차륜열거,physics/updateToUsd활성화. v05의wheel_count0은Proxy순회누락검사버그였으며wheel6실제존재/접촉증거와구분·보존.
- basic controller v06은GPUlock하에15조합순차진행,기존4실패폴더덮어쓰기없음.
- Full E2E `scripts/c_v02_drive540_e2e_session_20261113_v01.py` /runner v02:원Stage4의ROS·TF·actuator graph/제어·경로·정지·메모리·속도·조향guard유지. **진단용sensor노드비활성판은본E2E에사용하지않았다.** scene v06은원래graph를그대로두고graph_signature정확일치를검사한다.
- 새C의단일적재물/팔레트잔여형상 공통명목충돌체검사만기존full-load28union검사대신별도C버전으로전달. 제어guard를완화하지않음. pallet5부품+잔여벽돌별동일box. 실제main 모델은기존C06/75:25/seed42/checkpointSHA그대로.
- task_layer_count4/4/3/2/1만사전운용입력. 장면생성의잔여슬롯은sim builder에만사용,perception subprocess에는RGBD/캘리브레이션/작업층수/모델lock만전달. GT마스크/pose/slot/FINAL운용입력없음.
- protocol SHA `fa5ef9a20d0d9172f48f25b20e7a72e3dcb2c953759eafb0a4da3e18af2630d2` 및manifest SHA `92ba7c2909f78110d4fa985de17ce6863538b0110dfb3e42a7e7784f05ce19fc` **변경없음**.
- 코드SHA/모델SHA는 `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/recovery_e2e_v01/execution_lock.json`. 실제커맨드/실행snapshot/scene/hash는파일럿폴더보존. 원본USD·학습·모델·정적평가 변경0. 패키지업그레이드/재설치/GPUreset/기존연구프로세스kill없음.

## 실제 Kit/센서/물리 증거

basic15조합은RGB640×480/Depth480×640생성,모든잔여공통collider(벽돌수+5)실제PhysX등록,6차륜접촉이벤트,articulation과카메라존재를확인했다. 각basic검사는실제시뮬레이션 `0.0833~0.0833`초의짧은검사다. 240app.update를240physicsstep이나4초로잘못해석하지않는다. basicPASS가장시간안정/주행/정지검증을뜻하지않음.

HR-C100 엄격Full E2E 파일럿은별도로 **257 actual PhysX steps/4.283334초** 및실측timeline/ROS TF/graph physics clock을기록. support2214 ray검사/6차륜접촉/PRE-driverquiet window/graph·bodyjointidentity/actualcollider305·safetyinventory 모두PASS. camera7보정검사모두PASS,유효Depth 288471픽셀. 실제카메라prim유지/rendererOpticalWorld와USD보정일치. `[Error]` physics schema미해결조건0.

자료: `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/recovery_e2e_v01/pilot/C2D_B01_C100_HR_Scan_O0/attempt_0001`의 actual_loaded_C_stage_manifest.json /pilot_physx_C.json /stationary_PhysX_support.json /support_admission.json /pilot_physical_admission.json /camera_metadata.json /runtime_summary.json.

## 기술 파일럿 결과와 현재새BLOCKER

첫HR-C100-O0 파일럿 `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/recovery_e2e_v01/pilot/C2D_B01_C100_HR_Scan_O0`:

- freshRGBD실제생성,원본배열/PNG/SHA보존.
- 고정HR checkpoint SHA검증,YOLO11n-seg imgsz640/conf.25/NMS.7/max100/retina_mask 정책대로실제GPU추론수행.
- detections.json 후보0,perception_result NO_DETECTION. ROBUST_A 자체실패가아니라운용mask미생성으로위치추정에진입하지못함.
- 계획/실제이동/조향추종/목표도달/drive-stop/주행영상은NOT_RUN. driver process미시작,nonzero command0. 전후카메라정지/quiet증거는있으나운동후정지인증으로대체불가.
- 결과는기술파일럿실패로보존. 기술파일럿본실험분모0. 다른대표14 Full E2E파일럿은아직미실행. basic15성공과구분.
- callbackcleanup zero receipt는driver미시작상태에서MISSING,observerexit0확인. 주행성공/전체정리인증PASS로표시하지않음.

현재영상은창가역광아래적재물이매우어둡게보이며도메인/조명차이가가능한원인이다. 그러나renderer자동검사의PASS는보정·파일·심각shadererror무발견에관한것이며학습분포동등성을보장하지않는다. v30물리배경과B1_CLOSED_EV학습배경은다르다. sourceC조명intensity를사용했지만기존v30tone-mapping과C학습촬영레시피전체의동등성은미검증. 이관측만으로원인을확정하거나조명/confidence를성공에맞춰변경하지않았다. 시나리오교체/모델재선정/재학습/GTmask우회/허용오차완화없음.

## 실행·안전·재개 상태

독립E2E controller PID2783174는첫기술파일럿미통과로HOLD에종료했다. 본540미시작. 기본정지검증15는종료. passive monitor/원래watchdog/ntfy/Git계속동작. 상태는 `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/recovery_e2e_v01/status.json`가복구후우선자료이며이전D/pipeline_status는basic진행단계기록이다.

완전E2E용자동연결은15파일럿SUCCESS+필수증거+disk전망검증후에만main540으로넘어가도록구성했다. 현재이조건을충족하지못했으므로실제전환검증은아직NOT_RUN. 이전실패artifact를재개때완료로잘못간주할수있는후보코드분기를별도v02에수정하고추가all15SUCCESS검사를넣었으며,**v02는미실행후보**다. 첫HOLD서비스를무조건restart하지말것. 원인과수정근거를확인한뒤새version/root/attempt에서실패원본을보존하여재개한다.

540본실험의정확한manifest/조건별36/단일load·pallet/O0/seed42/층수prior/Main.11m·7.341774deg/도달5mm2deg/.03mps안전정지모두유지. 물리HOLD를임의로해제하지않음. Main밴드의기존원정밀도7.34177432289679deg와새protocol6자리7.341774deg차이는새outcome에서더엄격한승인값으로평가하며허용범위를넓히지않음.

## 산출물

- `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/recovery_evidence_v01/drive540_native_crash_isolation_matrix_20261113_v01.csv`
- `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/recovery_evidence_v01/drive540_recovered_basic_15_conditions_20261113_v01.csv`
- `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/recovery_evidence_v01/drive540_crash_recovery_summary_20261113_v01.json`
- 원본4crash/추가분리진단/실제15기본실행/HR-C100실패파일럿원자료및SHA.

최종상태: **Kit recovered / RGBD confirmed / stationary physics admission confirmed for HR / actual driving NOT_RUN / main0/540 HOLD due no detection.**
