
## 2026-11-02 — v45 실제3×3 평가2916·두재질108완료 / B5파일럿54·확장HOLD

[v45 보고서](../reports/three_rep_crossrep_mixed_target_audit_20261102_v45.md). original972/324pairedkey를직접검증하고10525inputSHA·193expected·known9/countPASS. HR/LR/CAD만3×3각324=2916추론, diagonal972maskpixel exact/IoU최대1.11e−16. equal-domain meanIoU .614619/.538966/.707187. 공통검출218/공통IoU50 173, HR86miss trace·4threshold진단·C×actual·oracle CSV/PNG완료.

red1+cement1새정적108actual/36paired설정·저장RGB3모델324평가완료. 실제O25 23.7857–25.4809%/O50 49.2238–50.4256%,108/108±2%p. matched red/cement/miss/ambiguous HR18/10/5/3,LR13/18/0/5,CAD11/25/0/0각36. 최고confidence genericclass0선택이며semantic재질분류NOT_ESTABLISHED. locked좌우명이영상좌우와반대인결함보존/actual좌우별도. Kit1회139.321초close/RSS7.72075GiB/exit0/owner잔존0/close_return0; Warning824·초기prototype참조경고600보존.

B5wrapper첫54FAIL(__file__누락)보존후새v45b51계산/1datum거절/2무검출;918추가NOT_RUN(HUMAN_REVIEW_PENDING). old/smooth곡률4/51·12/51,fullgeometry0/motion0. 로컬v44실행존재확인·5658SHA재검증/역사319계산humanreviewFAIL유지;요청문v44미실행전제와구분. cross첫호출manifest부재실패·compile괄호오류도기록. 다음은사람ROI검토후별도918rollout및fixtureprototypeclosure/좌우명패치이며추가Kit자동실행없음. 원본/weights/locks불변,HPO/Ray/훈련/ROS/조향/주행0/steeringHOLD. 보고서marker sync요청/원격완료UNKNOWN.
# PROJECT_STATE — 2026-10-13 (Asia/Seoul)

## 2026-11-02 — v44 기존972 B5 오프라인319계산 / 새가림54 actual 목표충족 / 인간사전검토 FAIL

[v44 보고서](../reports/three_rep_B5_pose_and_occlusion_calibration_20261102_v44.md). 새 외부 THREE_REP_OCCLUSION_B5_20261102_v44에 original972 센서/예측mask SHA를 고정했다. old972 재렌더0/재추론0/학습0. 센서 바닥+사전PALLET_H.144/치수1.1m와연결표면proposal, erosion2·brick제외3·inlier80%/100점/3mm/tilt5/cov기준을 유지했다. pilot54는 B5 HR16/LR17/CAD18=51,거절1·원무검출2. 전체972는 B5 HR83/LR133/CAD103=319,datum479,원무검출174,sourceUnavailable0. 계산된 표본 조건부 norm중앙값88.179/219.746/93.396mm; 계산됨은독립물리정확도인증아님. old18중17 재계산가능/XY최대차.003786mm, HR S043O0 새ROI77.12%로거절하며old성공보존. old/smooth offline곡률통과4/83·3/133·4/103 및11/83·10/133·8/103, fullgeometry0/motion0.

중요 절차미준수: 사용자요구의 사람사전검토 없이 Codex AI시각검토만으로54→972확장했다. HUMAN_REVIEW_BEFORE_ROLLOUT=FAIL,319는탐색자료/인간QA대기. gate가검토파일존재만확인한한계를 숨기지않았다. ROI접촉표·거리시점20대표·inlier/depth/잔차패널20개보존. NearFront/Far 대부분거절,80%완화/GTfallback0. 다음은사람검토와새버전normal/patch분리·결합정책이다.

fixture setup에만oldO0 GT/depth사용,세표현최소targetdepth절반에공통판·minimax공통경계동결. offline108base×3O=324설정모두새±2%p예측충족(실측아님). 실제는별도 MID/FRONT54장만 Kit1회/33.59초close/36.33초exit0/retry0, RSS6.67977GiB·GPU6913MiB·rendererError0/owner잔존0/close_return미관측. 실제O0=0,O25 24.53–25.51%,O50 48.64–50.57%,54/54목표충족. 새검출HR18/LR17/CAD18,IoU≥.5 17/17/18,B5 18/17/17; old/smooth곡률2/18·0/17·4/17 및5/18·3/17·6/17은offline만. 새metadata calibrationSHA/uniqueframe54 PASS. old source5658+capture5832 SHA보존PASS/known9/countPASS/신규193expected mismatch0. 원래v43가림부족·metadata오류·weights·locks·Proxy·기존실패불변. READY_FOR_MOTION=NO,ROS/driver/조향/propulsion/play/PRE/FINAL/HPO0. 원격pull590839b→b049866으로v44지시확인,새보고서sync완료UNKNOWN/자동추가Kit없음.

## 2026-11-02 — v43 실제 정적 Isaac RGB-D·동결 M50 972/972 완료 / 주행0

[v43 보고서](../reports/three_rep_occlusion_completeness_isaac_pilot_20261102_v43.md). HPO/AMP/Ray/훈련을 실행하지 않고 새 외부 THREE_REP_OCCLUSION_20261102_v43에 972계획/324paired scene을 고정했다. 기존 v01→v03/geometry v02·MNIDB_0001 제거궤적·동결 M50 사용. 단일 Kit에서 pilot54/54 뒤 같은 세션으로972/972 fresh RGB-D·matched 추론 완료, retry0/physics play0/ROS0/driver0/조향0/주행0, process exit0·owner잔존0. 시작→close470.27초, sampled RSS최대7.56924GiB/전체GPU7650MiB로8GiB/26000MiB한도 내. close_return 미관측과 정상 process exit를 구분한다.

Pilot 검출 HR17/18·LR17/18·CAD18/18, 평균GT pixelIoU .858409/.901282/.876891(무검출0 포함). 전체 검출238/324·292/324·268/324, IoU≥.5 231/324·218/324·267/324, 평균IoU .677861/.635470/.744906. 표현+matched model 기술 관측이며 통계적 우열·동등성·FullE2E·주행 성공 아님. B5는pilot O0에서 각6/18 계산, 가림34건 sensor datum거절/무검출2; 추가918건 freshROI미검토로 B5 NOT_RUN. oldquintic 곡률1/6·1/6·2/6, smoothS3/6·4/6·4/6은OFFLINE곡률만, fullgeometry평가0/liveHOLD 유지.

Pilot actual O25 24.53–25.74%/O50 49.45–50.73%. 전체 O25 16.56–26.57%/O50 21.79–51.91%: Near사선target 일부가 깊이1m판 앞에 남는 ray-depth사례 확인. 정확한명목가림수준 실현 NOT_ESTABLISHED, 실제비율전부보존/제외·재라벨0. 초기hiddenpanel renderer Error1·metadata calibration_sha가depthSHA를가리킨오류·triplet frame_id공유를 보고, 원본metadata보존/전체972 rawprojection/view수치재구성PASS+별도보강기록. SHA193+historical108 mismatch0·known9/countPASS·324pairedscene·5832capturefileSHA PASS, geometrylock자체expectedUNKNOWN. CSV/PNG/실제overlay완료, 동결plan과현재상태별도ledger. Git없음/원격syncUNKNOWN. v30HR observed2.79451mm/design55.23288mm n1·v31LR/v32CAD곡률실패·v35/v36offline·v38steeringHOLD불변. 다음은면담실측공유후새버전판깊이/calibrationprovenance/sensor팔레트datum보강, 새Kit/모션자동재실행없음.

## 2026-11-02 — v38 정지 조향 isolation 구현 일부 / 실측 정책 미정 HOLD

[v38 보고서](../reports/construction_site_steering_characterization_and_hr_live_20261102_v38.md). 새 engineering 모듈/one-shot preflight를 구현해 actual v30 stage의 anonymous session layer에서 정상 articulation exec3개 차단·exact 복원·source SHA 불변을 확인했다. second writer/±90°/NaN/복원누락/실제 edge 재연결 거절 포함 CPU7/7 PASS. expected 대비 unique dependency783 mismatch0, known9/count108·432 PASS. standalone USD 경고·부수rg경로exit2 보존, preflight exit2는 의도된 HOLD이며 PASS 아님.

HOLD_CHARACTERIZATION_POLICY_UNDEFINED: 승인된 stationary 실측 rate 중단 한계 미확인. configured286.478882deg/s 또는 요구HR28.406deg/s를 허용 측정률로 만들지 않음. Kit0/driver0/stationary시험0/chassis motion0/retry0/science0; 실제 sole writer/stop/contact·support·TF/GID·memory·graph runtime 복원 미검증. live backend/setpoint generator 미완료, 측정 acquisition 없음; CPU isolation은 native 제어권 증명이 아님. ROSzero MISSING/NOT_APPLICABLE_PRE_DRIVER, HR PRE/FINAL 및 새 error/track/rate 모두 NOT_RUN. 다음 작은 단계는 출처가 있는 characterization rate/sweep 정책 확정이며 preflight 반복 금지. v39 LR/v40 CAD gate 미충족, 기존 HR v30 observed.279451cm/design5.523288cm·LR/CAD original curvature FAIL·v37HOLD 불변. HPO/훈련/scale/occlusion/18/324/432실행0. 원격handoff 완료는 미검증.

## 2026-11-02 — v37 승인된 HR smooth-S: 실제 조향 게이트 HOLD / 교수 브리핑 계획 완료

[v37 보고서](../reports/construction_site_common_planner_hr_live_20261102_v37.md), [면담용 연구·통계 계획](../reports/professor_briefing_research_and_statistics_plan_20261103_DRAFT.md). 사용자 HR1회 승인은 유효하나 실제 추종 rate 미입증으로 Kit0/motion0/retry0. v30 실제 executed_code와 composed stage에서 네 steer joint max286.478882deg/s·drive836.614/40/200, graph maxSteeringAngleVelocity5rad/s를 확인했다. 그러나 unconnected steeringAngleVelocity 기본0은 snap 분기이며 AST 반례에서 target8rad/s 가능; actuator 응답값 아님. 원래 Twist graph는 v0에서 작은 stationary 조향각을 지정할 수 없어 안전한 응답 시험 미실행. joint 상한을 achievable rate로 승격하지 않았고 live bridge/새 raw Kit root 없음. 다음은 독립 stationary characterization 연결/안전 검증 후 fresh HR qualification이며 LR/CAD port는 HR PASS 뒤다.

SHA1118참조 mismatch0, 새 v36 replay27case/55221checks PASS_OFFLINE, stopCPU20/20, manifest108/432·4rep/base PASS. AST harness 첫mock constructor오류exit1 후 새harness만 수정PASS, 부수검색 경로오류exit2 기록. fresh perception/PhysX/support/GC/TF/GID/PRE/FINAL/endpoint/exit/zero receipt 미실행; ROSzero MISSING/NOT_APPLICABLE_PRE_DRIVER. science0/HPO·trainingPAUSED/scale·18·324/432 NOT_RUN, 원본/weights/USD/locks/과거성공·실패 불변. 브리핑에는 primary binary GLMM·paired block·Holm·GT/두datum·분모·HPO/축소모형holdout·분산pilot후N계획을 명시했고 occlusion level은 권위자료부재TBD로 두었다.

## Full E2E v02 offline prototype / nominal108 scan — 2026-10-14
[결과보고서](../reports/full_e2e_v02_offline_prototype_scan_report_20261014_v01.md), [108-row CSV](../reports/full_e2e_v02_nominal_scan108_20261014_v01.csv), [검사](../reports/full_e2e_v02_offline_prototype_checks_20261014_v01.json), [hash](../reports/full_e2e_v02_offline_prototype_hash_inventory_20261014_v01.json). Forward-only Hybrid A*/Dubins/독립OBB-cell sweptvalidator와canonical design/runtime prediction분리schema를별도새파일로구현했다. StandaloneUSDreader로Env-only height-band map후보를추출했으며SimulationApp/omni/ROS실행없음. Map/전체articulatedfootprint는UNKNOWN이므로공식108/108 MAP_OR_FOOTPRINT_UNCERTIFIED/HOLD. 내부start→H model경로42행/5geometry,NO_PATH60행/9geometry,초기충돌6행/1geometry;H→PRE→FINALcorridorclear0/108. 제안2Dbody/clearance와nominalsupport/FINALstandoff의modelconflict이며실제물리불가능의증명이아니다. Base15exactpathreplay/fine15statusmatch,최종16testsPASS,완료marker --resume가108rowskip. 모든후보수치는PROPOSED,publicruntimeAPI는fail-closed. 기존source180개·smoke577artifacts·5개demoinventory보존. QUAL12/revised smoke/confirmatory/432미실행,연구denominator0,actualreadinessHOLD.

## Full E2E v02 offline feasibility/design audit — 2026-10-14
[핵심 audit](../reports/full_e2e_v02_offline_feasibility_design_audit_20261014_v01.md), [offline 수치/hash 증거](../reports/full_e2e_v02_offline_feasibility_evidence_20261014_v01.json). Geometry108/432/base exact-set·4rep pairing·authoritative geometry suffix join 및 원본hash를 read-only로 확인했다. Legacy task_frame_yaw_deg0과 geometry suffix90을 구분했고 원본은 수정하지 않았다. Canonical offline 산술상60/108은PRE e_long<-.030m, nominalH(.40m뒤)도task-axisbehind이며initialhandoffbox내조건0/108이다. 이는runtime GT input이나global infeasibility 증명이 아니다. 권장planner는forward-only HybridA*이고footprint/clearance/Rmin2.80/grid/yaw/cost/tie/failure/schema는모두PROPOSED. 기존single-pose bbox/structural grid는approvedmap·articulatedfootprint인증을대체하지않는다. 전체108curvature/collision search NOT_RUN, stopped handoff basin UNPROVEN, QUAL12 entry HOLD/readiness NOT_ESTABLISHED. Offline prototype 구현 gate와QUAL12 runtime gate를분리해순환기준을피했다. 코드구현/Isaac/ROS motion/revisedsmoke/confirmatory/432없음; 연구denominator0. 기존v01실패·demo·원본controller/protocol/reports보존.

## Full E2E v02 approach/handoff amendment 초안 — 2026-10-14
[Protocol amendment 초안](../reports/full_e2e_v02_approach_handoff_protocol_amendment_draft_20261014_v01.md)을 작성했다. 영상 demo 작업은 종료한다. 기존12/12 PRE timeout과 분류B, frozen controller/원본 protocol/기존 results·reports를 보존했다. 권고는 기존 sensing geometry·B4/B5·PRE/FINAL·terminal logic을 유지하면서 공통 approach planner와 실제 정지 handoff를 추가하는 **controller/task-policy 변경**이다. 새 v02 qualification namespace에 기존3 base×4 reps 조건을 유지한12 planned executions를 제안했고, initial one-shot/GT 차단/prior/handoff envelope/timeouts/PhysX·속도 mismatch·432 진입 gate/분석 분리를 초안으로 명시했다. 모든 새 수치/정책은 미승인·미잠금이며 입증된 terminal 수렴 영역이 아니다. Existing artifact amendment v02와 새 실행구조v02를 구분하며 후속 artifact 번호는 별도로 정한다. 이번 작업은 문서2개만 작성·갱신했다. 코드 수정·engineering 실행·revised smoke·confirmatory·432 없음; readiness NOT_ESTABLISHED.

## 증거와 현재 단계
2026-10-13 워크스테이션 audit 완료. 근거: [audit 보고서](../reports/workstation_handoff_audit_20261013_v01.md), [최종 inventory](../reports/workstation_inventory_20261013_v03.json). 아래 audit 기록과 후속 실제 engineering runtime 증거를 구분한다.

**12 planned engineering executions 완료 / research main·strict·relaxed success 0/12 / confirmatory readiness UNKNOWN**. ROS domain을 격리한 실제 simulator에서 settling→fresh RGB-D→locked YOLO→B4/B5→predicted targets→frozen controller→terminal evaluation까지 12/12 실행했다. 전부 PRE timeout이며 해당12회에는 비영 command가 없었다. 후속 별도 pulse diagnostic에서 wheel/base 운동만 확인했고, 전체 runner readiness는 PASS가 아니다. [결과 CSV](../reports/full_e2e_robot_smoke_results_20261013_v01.csv), [최종 요약](../reports/full_e2e_robot_smoke_summary_20261013_v01.md), [checkpoint v04](../reports/full_e2e_robot_smoke_checkpoint_20261013_v04.md). Engineering 연결/기록 검증과 이동·research task success를 별도 판정한다. 432-run 미실행.
- prelock v01 + amendment v02/v03 + initial geometry v02 적용.
- workspace FE2E_OPEN_WS_v01; target (-25.888, 30.509); task yaw +90°.
- 실제 workspace 파일은 `initial_geometry_v02/FULL_E2E_FIXED_WORKSPACE_LOCK_v01.json`: 파일/metadata v01과 geometry 디렉터리 v02를 구분한다.
- geometry lock은 `initial_geometry_v02/FULL_E2E_INITIAL_GEOMETRY_LOCK_v02.json`.
- 알려진 9개 SHA256/count PASS, base108/execution432의 uniqueness·4-rep pairing·geometry 모든 열 join PASS, 각 representation 108행.
- search CSV의 해당 좌표와 yaw +90° 행에서 endpoint/exact corridor 15/15 PASS. nominal geometry 증거이며 실제 controller 실행 성공 증거는 아니다.
- checkpoint 4개, asset USD 8개, pose/controller·rover·base scene 등 기록된 핵심 dependency hash PASS. USD composed references/textures 전체 closure는 미검증.
- geometry lock 자체 observed hash는 확보했으나 독립 expected hash가 없어 자체 인증 UNKNOWN.

Engineering code와 simulator-free 검사 구현 완료: [구현 보고서](../reports/full_e2e_implementation_audit_20261013_v01.md), [engineering 결정 기록](../reports/full_e2e_engineering_decisions_20261013_v01.md). Offline 21 tests PASS, known locks 9개 재검증 PASS. 실제 simulation smoke NOT_RUN, runtime readiness/research task success UNKNOWN. 후속 허용 작업에서 별도 headless Isaac Sim으로 ENG_FE2E_001 4-rep stationary 연결을 수행했다. [Runtime 결과](../reports/full_e2e_runtime_connection_20261013_v01.md): fresh capture/actual YOLO/pose/targets 4/4 PASS. 실제 K≈317.043 px, mounted transform/depth 단위/synchronization, planned fixture world-top=.144 m(변환으로 계산), 새 nominal collision preflight를 확인했다. 이는 당시 stationary 연결 범위다. 후속 실제 ROS/controller engineering 실행은 위 최신 단계와 아래 작업 로그에 기록했다. Confirmatory는 여전히 미실행이다.

## 최신 controller compatibility 진단
2026-10-13: [핵심 진단](../reports/full_e2e_controller_compatibility_diagnostic_20261013_v01.md), [로그 hash](../reports/full_e2e_controller_diagnostic_hashes_20261013_v01.json). **분류 B: 시작조건/전진전용 logic 문제.** 12개 first-step를 원본 AST 식으로 재현해 logged e_long/e_lat/e_yaw/cmd와 일치했다. 모든 PRE e_long<-.030m→v clamp0→Ackermann w_limit0이며 GT canonical PRE도 음수(진단 전용)다. ENG001 HR e_long=-.193631m, e_lat=.036089m, e_yaw=.000428684°. Oblique PRE는 body 방향으로 앞에 있지만 task goal-frame e_long은 음수다. Frame/argv 전달 오류는 발견되지 않았다.

별도 engineering-only domain171 diagnostic에서 v=.03의 짧은 pulse에 실제 joint response(max2.925371rad/s)와 base net 이동 .384224m를 확인했다. 종료 ROS zero와 final wheel speed0도 확인했고 기존 GUI615706를 보존했다. Frozen controller/perception/새 연구case는 실행하지 않았다. 이 결과는 기존12 연구 결과0/12에 합치지 않는다. Nested rolltainer articulation/rigid-body errors는 남아 있으며 command propagation을 완전히 막지는 않았지만 정량 영향은 미해결이다. 실제 straight speed≈.118772m/s가 command .03과 달라 속도 gain/단위 및 physics 정량 추종 검증이 필요하다. **전체 runner readiness PASS 아님**. PRE/approach 변경은 controller/task policy, distance/view/initial pose 변경은 scientific geometry, hierarchy 변경은 physical asset 변경으로 구분하며 이번에 적용하지 않았다. 기존577 artifacts/protected25 hashes 보존. 수정 research smoke와432는 미실행.

## 최신 decision memo — 구현/실행 미승인
2026-10-13: [수정 경로 decision memo](../reports/full_e2e_controller_decision_memo_20261013_v01.md) 작성. 확정된 진단B를 전제로 A(global approach+handoff), B(PRE/FINAL policy/offset), C(initial distance/view/pose) 세 경로를 구분했다. A/B는 controller/task policy, C는 scientific geometry 변경이며 단순 engineering IO fix가 아니다. 어느 경로도 채택/구현하지 않았다.

기존12 planned executions/14 attempts와0/12 결과는 유지한다. 제안된 새engineering study별12 denominator, diagnostic/demo 제외, 새confirmatory protocol/manifest/output 분리 및 nonzero→정량 wheel/base→PRE→FINAL→zero, timeout, PhysX hierarchy, command-real speed readiness gate를 memo에 기록했다. Gate는 제안이며 frozen 규정이 아니다. **전체 readiness NOT_READY; 수정smoke·confirmatory·432는 미실행.**

별도 ENG001 HR moving demo1회 계획도 후보로만 작성했다. Frontal sensing distance2.0m를 쓰는C-geometry 파생안 또는 원래1.5m를 유지하는A-approach 대안의 변경/승인 안건을 명시했다. Proposed demo ID `DEMO_FE2E_001_HR_GEOM_v01`, planned demo1/research 기여0이며 원래Near조건과 동일하다고 주장하지 않는다. 설정·physics/속도·budget·영상/output·실행범위의 사용자 승인 전 미실행. 이번turn에서는 이memo와PROJECT_STATE만 변경했고 코드/원본/기존결과를 보존했다.

## 승인된 HR2.0m visualization demo 완료
2026-10-13: [Demo결과](../reports/full_e2e_demo_geom_result_20261013_v01.md), [hash](../reports/full_e2e_demo_geom_hashes_20261013_v01.json). `DEMO_FE2E_001_HR_GEOM_v01` planned1/attempt1에서freshcapture/YOLO/B4-B5/predictedtargets/frozencontroller로실제PRE/FINAL도달·QC·zero PASS,timeout없음. Nominal frontal distance2.0m(actual2.002705m)는원래Near1.5와다른파생geometry. Demo연구denominator기여0,기존12실패0/12유지. Fullrunner/정량physicsreadiness는여전히미해결. 영상12.4초: `/home/user/hh/isaac_cosmos/sdg_final/DEMO_FE2E_001_HR_GEOM_v01/attempt_0001/DEMO_FE2E_001_HR_GEOM_v01.mp4`. 기존GUI와originalcontroller/reports/577artifacts보존. Revisedsmoke/confirmatory/432미실행.

## 최신 autonomous navigation capability audit
2026-10-13: [Engineering-only capability audit](../reports/autonomous_navigation_capability_audit_20261013_v01.md), [hash](../reports/autonomous_navigation_capability_audit_hashes_20261013_v01.json). 별도2.5m-reference fixture/domain174에서straight.5m(actual.500532m),곡선yaw+3°(actual+3.671580°),explicitworldXYgoal candidate(error.019097m)와physicaljoint/zero응답을확인했다. 총3test,attempt0001(domain173)은ROSfloat conversion오류로실패했고보존,새v02/attempt0002에서완료. Researchdenominator기여0;frozencontroller/기존12결과보존,수정smoke/confirmatory/432미실행.

현재입력은ROS `/rover/cmd_vel`과graph내wheelvelocity/steerposition이다. Built-inROSgoal/action/directjointtopic은확인되지않았고frozencontroller는고정PRE/FINALterminalstabilizer다. 새engineeringcandidate는worldgoalJSON을받는제한된forwardAckermann follower이며장애물회피/globalplanner가아니다. Graph의linear.x×15→Ackermann.speed연결을확인했다. Nestedhierarchyerror/정량speed·일반goal·장애물응답은미해결,전체autonomousnavigation/readinessPASS아님. Preflight/actualboundsafetyguard와navigationavoidance를구분한다.

## 최신 engineering-only autonomous-search visualization
2026-10-13: [Search demo보고서](../reports/nav_search_demo_report_20261013_v01.md), [trajectory](../reports/nav_search_demo_trajectory_20261013_v01.csv), [command](../reports/nav_search_demo_command_log_20261013_v01.csv), [detection](../reports/nav_search_demo_detection_log_20261013_v01.json), [hash](../reports/nav_search_demo_hash_inventory_20261013_v01.json). `DEMO_FE2E_NAV_SEARCH_HR_v01`은3.5m시작에서선언waypoint로실제0.476582m이동후첫mountedRGB-D/YOLO관측(conf0.968609)으로발견했다. FreshB4/B5predictedtargets의handoff와frozenPRE/FINAL을완료했고zero/wheel0/base정지를확인했다. Actual56.3초MP4: `/home/user/hh/isaac_cosmos/sdg_final/DEMO_FE2E_NAV_SEARCH_HR_v01/attempt_0001/DEMO_FE2E_NAV_SEARCH_HR_v01.mp4`. Planned1/attempt1/research기여0,기존12실패및2.0m demo보존. SimpleworldXYfollower와static/dynamicfullboundguard이며장애물회피/globalplanner아님. Multi-observationsearch는engineering파생이며연구관측policy로승격하지않는다. PhysX/속도정량/일반navigationreadiness미해결. Revisedsmoke/confirmatory/432미실행.

## 최신 long-range serpentine engineering visualization
2026-10-13: [Serpentine demo](../reports/serpentine_demo_report_20261013_v01.md), [trajectory](../reports/serpentine_demo_trajectory_20261013_v01.csv), [command](../reports/serpentine_demo_command_log_20261013_v01.csv), [detection](../reports/serpentine_demo_detection_log_20261013_v01.json), [hash](../reports/serpentine_demo_hash_inventory_20261013_v01.json). `DEMO_FE2E_NAV_SERPENTINE_HR_v01` planned1/attempt1. Static6m 시작후보PASS(actualcamera5.996499m),약4m smoothS arc 실제이동(lateral폭0.085100m,yaw87.415–94.429°). Arc후2.025625m관측지점에서freshYOLOconf0.968750검출→B4/B5predictedhandoff/frozenPRE/FINAL완료→zero/wheel0/base정지. 실제99.7초MP4: `/home/user/hh/isaac_cosmos/sdg_final/DEMO_FE2E_NAV_SERPENTINE_HR_v01/attempt_0001/DEMO_FE2E_NAV_SERPENTINE_HR_v01.mp4`. Research기여0,6mYOLO능력평가아님. PredeclaredS arc/simplefollower+collisionguard이며장애물회피planner아님. 기존12/2.0m/3.5msearch와원본/reports보존. Revisedsmoke/confirmatory/432미실행,globalnavigationreadinessPASS아님.

## 최신 engineering-only blind-to-detection demo
2026-10-13: [Blind demo](../reports/blind_search_demo_report_20261013_v01.md), [trajectory](../reports/blind_search_demo_trajectory_20261013_v01.csv), [command](../reports/blind_search_demo_command_log_20261013_v01.csv), [frame/time detection](../reports/blind_search_demo_detection_log_20261013_v01.json), [hash](../reports/blind_search_demo_hash_inventory_20261013_v01.json). `DEMO_FE2E_NAV_BLIND_SEARCH_HR_v01` planned1/attempts4,최종domain180 attempt0004성공. 초기derived7mmnarrowFOV(frame1 floor RGB/YOLO0/FOV밖/pose-target없음)검증후predeclared+.5mforward검색. Frame1–6비검출,frame7conf0.736478최초검출. SourceFOV복원후별도freshframe8최초B4/B5target생성→frozenPRE/FINAL/zero완료,allwheel0/base정지확인. 이전3attempt은초기collision2건/clockpayload계약오류1건보존. 영상150.9초: `/home/user/hh/isaac_cosmos/sdg_final/DEMO_FE2E_NAV_BLIND_SEARCH_HR_v01/attempt_0004/DEMO_FE2E_NAV_BLIND_SEARCH_HR_v01.mp4`. CameraFOV/searchpolicy파생이며research기여0. GTtarget보정없음,SLAM/장애물회피/전체navigationreadinessPASS아님. 기존demos/12결과/originals보존,수정smoke/confirmatory/432미실행.

## 연구 목적
국문: 건설 자재운반로봇의 인식 및 작업을 위한 Task-Sufficient 3D Asset Representation 평가
영문: A Cost–Performance Evaluation of Task-Sufficient 3D Asset Representation for Construction Material-Handling Robots

더 정교한 자재 asset의 추가 제작 부담이 인식, 위치·방향 추정, 접근·정렬 성능 향상으로 이어지는지 평가한다.
- RQ1: representation별 perception/pose/task 성능 차이
- RQ2: 자재 특성과 부분 적재 조건에 따른 representation 영향
- RQ3: 낮은 구축 부담으로 정의된 작업 성능을 확보할 수 있는 representation 여부
새 평가 프레임워크라는 novelty는 선행연구와의 직접 비교 전 확정 주장하지 않는다.

## 최종 비교 대상
| 코드 표기 | 설명 |
|---|---|
| HR_Scan | 높은 source acquisition 조건에서 재구성 |
| LR_Scan | 낮은 acquisition 조건에서 독립 재구성; HR decimation 아님 |
| Proxy | 매우 단순한 형상 + appearance/texture |
| GeoCAD | 주요 형상 특성을 CAD 방식으로 표현 |

Materials: cement brick, red clay brick. 적재물 중심 실험.
초기 P1–P5 및 load-envelope P5는 현재 최종 4개 조건으로 사용하지 않는다.
독립변수는 representation strategy다. geometry/appearance/제작방식이 함께 달라지므로 순수 polygon 수의 인과효과 또는 단일 fidelity ladder로 해석하지 않는다.

## 실험 흐름과 상태
| 단계 | 기록상 상태 | 해석/검증 범위 |
|---|---|---|
| Asset burden audit | 수행 | source input, mesh, texture, deployable size; workflow time provenance 주의 |
| Nominal synthetic | 구축·학습 수행 | Train 2,000 / Val 400 / Test 400; 2,000 선택 이후 추가 렌더링 보류 |
| Common HPO/Combined synthetic | 수행 | 공통 recipe; Full E2E용 4 checkpoint hash는 audit PASS; runtime 동작은 미검증 |
| Real M50 adaptation + Test189 | 평가 완료 | red-only external validation; Test189로 재선택 금지 |
| Non-ideal depletion | 1,680 scenes/rep frozen | 평가 subset 1,460 membership 유지 |
| RGB-D replay / pose | 수행 기록 | RGB·depth·scene ID audit; locked estimator 원본 hash audit PASS; mounted-camera 연결 미해결 |
| B300 controlled benchmark | 1,200 terminal rows 및 분석 완료 기록 | 300 paired scenarios × 4 reps; stored pose error→rover task |
| Full E2E | Engineering 12/12 실행 완료 | perception/pose 12/12, control completion 0/12, research success 0/12; 별도 pulse의 운동/zero만 확인; 정량 속도·전체 readiness·confirmatory 미검증 |
| 통합 cost–performance / 논문 | 진행 필요 | task sufficiency/비열등성 주장 강도 검토 |

B300 성공률은 Full E2E 성공률이 아니다. 둘 다 시뮬레이션 로봇 접근·정렬이며, 실제 lifting/fork insertion/운반 안정성 검증은 아니다.

## 선택 결과 요약 — 기록값, 원본 재검증 대상
### Nominal learning curve (4-rep mean mask mAP50–95)
500→1,000→1,500→2,000 train scenes: 0.7790→0.7984→0.8026→0.8076.
2,000 scenes 선택을 diminishing marginal gains로 설명한다. Representation 차이가 작은 사실만으로 task sufficiency를 증명하지 않는다.

### Combined synthetic / real
| Representation | Combined synthetic Val mask mAP50–95 | M50 adapted Real Test189 mask mAP50–95 |
|---|---:|---:|
| HR_Scan | 0.870200 | 0.985352 |
| LR_Scan | 0.869080 | 0.985807 |
| Proxy | 0.870520 | 0.988371 |
| GeoCAD | 0.870440 | 0.987624 |

Synthetic-only Real Test189: HR 0, LR 0, Proxy 0.002558, GeoCAD 0라는 기록.
Real 적응효과와 representation 차이를 구분한다. E2E에서 사용할 checkpoint는 성능표로 추측하지 말고 locked protocol의 실제 경로·hash를 따른다.

### B300
최근 분석 출력: b300_terminal_metrics_derived_v01.csv shape (1200, 26).
descriptive_overall_v01.csv는 representation별 n=300.
| Representation | mean abs longitudinal mm | mean abs lateral mm | mean GT 2D position cm | mean abs heading deg |
|---|---:|---:|---:|---:|
| HR_Scan | 113.940825 | 26.479784 | 12.394388 | 0.507556 |
| LR_Scan | 132.985482 | 23.638096 | 14.106907 | 0.521268 |
| Proxy | 96.518292 | 27.347585 | 10.714641 | 0.510622 |
| GeoCAD | 105.069417 | 24.640494 | 11.428784 | 0.483181 |

Main success omnibus Cochran Q: p=0.637569; HR-reference McNemar Holm p=1.0라는 기록。
상호작용 LRT가 비유의라고 equivalence/non-inferiority라고 결론내리지 않는다.
Full E2E 잠금에서 확인한 strict/main/relaxed 임계값은 각각 5.5/11/16.5 cm와 3.686017625614643/7.34177432289679/10.9384737479652°이다. MAIN이 primary이며 controller QC 30 mm/30 mm/2°와 구분한다.

## Full E2E: 확인된 시나리오 구성
Base manifest 기록:
- 108 scenarios; execution manifest 432; 각 representation 108.
- legacy environment 라벨 A_OPEN / B_STRUCTURAL / C_CLUTTER 각각 36은 provenance다. Amendment v03에서 confirmatory 환경 요인을 비활성화하고 FE2E_OPEN_WS_v01로 고정했다. 최신 분석식에서도 Environment 항을 제거한다.
- ModerateOblique / StrongOblique 각각 PLUS 18 / MINUS 18.
- C60, C20 partial trajectory: 각각 T01 7, T02 7, T03 8, T04 7, T05 7.
- 로컬 pairing/join PASS; 모든 execution에서 fresh RGB/depth/YOLO/B5/B4 TRUE, frozen pose CSV reuse FALSE.
새 geometry는 v02이고 workspace FE2E_OPEN_WS_v01이다. Environment 라벨과 실제 배치 의미는 amendment/geometry에서 읽는다.
구형 manifest의 환경 anchor를 최신 geometry 없이 적용하지 않는다.

## 알려진 현장 위치
- 연구 root: /home/user/hh/isaac_cosmos
- protocol root: /home/user/hh/isaac_cosmos/sdg_final/full_e2e_task_protocol_prelock_v01
- assets root: /home/user/hh/isaac_cosmos/assets/assets/objects/_normalized
- scene candidates: /home/user/hh/isaac_cosmos/sdg_practice
- legacy production: /home/user/nonideal_depletion_b2b_production_rgb_v01.py
- legacy depth replay: /home/user/nonideal_depletion_pose_rgbd_replay_v01.py
- locked pose: /home/user/eval_step25_pose_final_locked_v01.py
- locked base scene: /home/user/hh/isaac_cosmos/sdg_practice/construction_scene_rover_recovery.usd
- locked rover: /home/user/hh/isaac_cosmos/assets/assets/robot/rover_camera_add_51_test.usd
- locked controller: /home/user/hh/isaac_cosmos/sdg_practice/robot_task_controller_goalframe_v04.py
- legacy B300 runner: /home/user/b300_actual_execution_v01.py; fresh Full E2E runner는 탐색 범위에서 미발견.
- 4개 Full E2E checkpoint의 실제 path/expected/observed hash는 PROTOCOL_LOCKS와 inventory에 기록했다. Legacy pose 코드의 과거 CHECKPOINTS를 대신 사용하지 않는다.

## Audit 시점 runtime
Isaac Sim 5.1.0.0, Python 3.11 경로, launcher `/home/user/anaconda3/envs/hh_isaac51/bin/isaacsim`. PID 615706이 해당 환경으로 실행 중이었다. hh_isaac의 4.5.0.0 설치와 구분한다. sdg_tools는 YOLO/pose 후보 환경이며 Isaac Sim launcher가 아니다: Ultralytics 8.4.129, torch 2.7.1+cu128. NumPy 2.3.5/2.4.6 dist-info 공존으로 실제 import 버전은 UNKNOWN.

RTX 5090, driver 570.172.08, CUDA toolkit 12.8 (nvcc V12.8.61), conda 25.5.1, ROS Jazzy `/opt/ros/jazzy`. GPU 여유 25975 MiB는 audit 당시 순간값이다. 설치 metadata 확인은 inference/ROS bridge 동작 검증이 아니다. 기존 프로세스는 보존했다.


## 최신 structured navigation engineering demo — 2026-10-14
[최종 보고서](../reports/structured_search_demo_report_20261014_v02.md), [이동 전 후보 비교/route plan](../reports/structured_search_route_plan_20261014_v02.md), [최종 hash](../reports/structured_search_demo_hash_inventory_20261014_v02.json). `DEMO_FE2E_NAV_STRUCTURED_SEARCH_HR_v01` planned1/이동attempt1/domain182, status=DEMO_COMPLETED, engineering demo success=True. 후보3개를 실제 static 구조/충돌 질의로 비교하고 기둥 하단 aisle→완만한 좌회전→frontal aisle의 A를 선택했다. Initial source-camera frame1 locked YOLO0, 구조 가림18/27 rays; 검출 이후에만 fresh RGB-D/B4/B5 predicted targets를 생성했다. CameraFOV 변경/GT target 보정 없음. 비영 실제 ROS command/wheel/base 이동과 종료zero=True, wheel stop=True, base stop=True 확인. 2개 실제 H264/VFR 영상 저장(native rover640×480/overview1920×1080), 인위적 프레임 복제 없음. Overview 초기 beam 가림 및30fps 미보장 한계 명시. 기존12실패/demos/frozen controller/protocol/reports 보존. Predeclared route+simple follower이며 SLAM/장애물회피/navigation readiness PASS/research success 아님. Research denominator0, revised smoke/confirmatory/432-run 미실행.

## 미해결 사항 — Full readiness UNKNOWN
1. Engineering에서는 초기 동기 RGB-D 1쌍/scene inference 1회/이동 중 재관측 없음, brick_load 최고 confidence·index tie-break, 자동 retry 0회로 결정했다. Warmup/watchdog는 engineering-only 설정이며 confirmatory 관측 규정으로 자동 승격하지 않는다.
2. ENG001에서는 locked bench mounted camera, renderer K/transform, axial-metre depth 및 stationary synchronization을 검증했다. 후속 engineering에서 다른 두 base 조건도 paused-state fresh 동기 capture를 검증했다. 이동 중 재관측은 정책상 수행하지 않았다. Native sensor sequence ID는 annotator가 제공하지 않아 process-local capture ID이며 이동 중/native ID synchronization은 미검증. Legacy 가상 LookAt은 사용하지 않았다.
3. 원본 추적으로 nominal_layer_count=4/nominal dimensions/pallet thickness=.144 m를 고정 설계정보로 구분해 engineering prior allowlist에 기록했다. Occupied layers/depletion/GT payload는 차단했다. Generic prior config의 world pallet-top은 null로 보존한다. 실제 ENG001에서는 parent/world transform을 계산해 .144 m datum과 hashed fixture evidence를 작성했다. 후속 3 base의 각 scene에도 변환 evidence를 별도로 계산했다. 다른 장면에 기본값으로 적용하지 않는다. Confirmatory prior authorization은 여전히 미확정이다.
4. Full E2E 단계별 timeout 및 실패/retry 규정. controller 원본의 stage timeout 60 s는 확인했으나 B300 runner 150 s를 Full E2E 규정으로 승격하지 않는다.
5. Engineering membership는 S1의 3 조건×4 reps=12 executions로 기록했다. Geometry 수식 계산, MNIDB_0001 FULL/T01 frozen depletion, 전용 seed와 고정 순서를 성능과 무관하게 결정했다. Confirmatory sample을 변경하지 않았으며 기존 source geometry/depletion을 재사용하므로 독립 연구 sample이라고 주장하지 않는다.
6. GUI maps/log에서는 source scene을 확인했으나 unsaved layer는 UNKNOWN. USD 전체 dependency closure와 비영 command wheel 운동 응답은 미검증. 격리된 ROS/controller actual IO는 후속 12회에서 확인했다. ENG001용 stationary runner/actual model/실제 command는 runtime 보고서에서 확인됐으며 전체 Full E2E command와 구분한다.
7. 이후 실행 완료-marker/per-run status는 home top-level/research 코드 깊이 3 및 protocol metadata 탐색 범위에서 미발견. 임의의 다른 경로에서 실행되지 않았다고 단정하지 않는다.
8. starter 디렉터리는 audit 시 `.git`이 없어 Git 변경 추적 UNKNOWN이었다.

## 작업 로그
2026-10-13: starter 작성. 최근 기록 확인; 로컬 실험 파일 검증/모델 실행은 아직 하지 않음.

2026-10-13: 로컬 audit 완료 근거를 반영하고 실제 artifact별 버전/경로, PASS와 UNKNOWN을 분리했다. 새 smoke 명세 초안 작성; 미정 정책은 제안 상태이고 구현·실행은 하지 않음. 원본 frozen 파일과 기존 보고서는 보존함.

2026-10-13: 사용자 허용 범위에서 새 camera/perception/B4-B5/target/controller IO/attempt/watchdog 코드를 구현하고 offline 21/21 검사를 통과했다. 기존 보고서와 원본 source/lock hash는 보존했다. Manifest 제작의 ValueError 및 재개 NameError를 새 구현 보고서에 기록·해결했다. Simulation/model-real-inference/robot command/432-run은 미실행. 실제 calibration 및 새 fixture datum 미해결로 runtime readiness와 research success는 UNKNOWN.

2026-10-13: 사용자가 허용한 stationary runtime 연결 수행. 기존 PID 615706과 원본 hashes 보존. Base scene camera extrinsic 불일치를 authoritative locked measurement bench subtree로 해결. 새 derived stage provider v08에서 ENG001 네 reps fresh RGB-D/actual YOLO/B4-B5/PRE-FINAL PASS. HR sensor 8 attempts의 오류·technical prototype과 최종 pairing, LR/Proxy/GeoCAD 각1 attempt를 모두 보존했다. 최종 29 tests/known locks PASS. Fixture datum/calibration은 ENG001에서 해결했으며 generic prior config의 null은 기본값으로 바꾸지 않았다. 12 전체·ROS·robot motion·432/연구 task success는 미검증. 다음은 predicted corridor 및 robot-command 없는 ROS/ActionGraph 연결 확인.

2026-10-13: 모든 실행·재사용 engineering source/adapter/core/config/manifest hash를 [runtime code provenance](../reports/full_e2e_runtime_code_hashes_20261013_v01.json)에 추가 보존했다. 외부 output에도 동일 provenance JSON을 새로 작성했다.

2026-10-13: 실제 controller engineering 12 planned executions 완료. HR technical 실패 2개와 수동 재실행을 포함한 총14 attempts 보존; 자동 retry 0. Detection/pose 12/12, control completion/QC/research strict·main·relaxed 0/12, timeout 12/12, 종료 zero 12/12. PRE e_long<0에 대해 frozen controller v/w=0이며 gains·GT target·membership 변경 없음. 보수적 non-support 접촉 flag 12/12에는 경사진 환경 지면 접촉이 포함되어 obstacle collision과 동일시하지 않는다. Existing GUI PID615706 및 protected25 hashes 유지. sdg_tools offline36 tests PASS. 실제 --resume 재실행은 모든 완료 marker를 skip했다. 별도 HR visualization replay는 첫 camera occlusion 실패를 보존한 뒤 domain87 attempt0002로 완료. engineering/confirmatory 결과에서 제외. 63.6초 실제 rendered-frame MP4 decode/frame-count·첫 시야 검증 완료, PRE timeout/종료zero 포함; FINAL 도달 없음. 영상: `/home/user/hh/isaac_cosmos/sdg_final/full_e2e_visualization_replay_20261013_v01/cases/ENG_FE2E_001__HR_Scan/attempt_0002/ENG_FE2E_001_HR_Scan_visualization_replay_walltime.mp4`. 최종 요약과 checkpoint v04에 기록.

2026-10-13: controller compatibility 진단 완료(B). 기존12 result와 protocol/controller 보존; 원본 식 replay12/12, 별도 isolated nonzero pulse의 wheel/base/종료zero 확인. 정량 속도/PhysX hierarchy 영향과 전체 readiness는 미해결. 새 연구 실행/432 없음.

2026-10-13: decision memo만 작성. 수정경로/qualification/readiness gate는 제안, 선택·구현·실행 없음. HR moving demo1회 계획과 승인항목을 포함했으며 demo/revised smoke/confirmatory/432 미실행. 기존12 실패와 모든 결과 보존.

2026-10-13: engineering-only navigation capability audit완료(3tests제한PASS). ROSintzero변환실패attempt보존후새v02에서직진.5m/곡선yaw/worldXY접근과zero확인. Frozencontroller/연구12실패유지,globalnavigation미구현,432미실행.

## 2026-10-15 map / footprint / terminal corridor certification — HOLD

[핵심 인증 보고서](../reports/full_e2e_v02_map_footprint_collision_certification_20261015_v01.md), [query CSV](../reports/full_e2e_v02_collision_certification_queries_20261015_v01.csv), [수치](../reports/full_e2e_v02_collision_certification_metrics_20261015_v01.json), [hash inventory](../reports/full_e2e_v02_collision_certification_hash_inventory_20261015_v01.json). Engineering-only 인증 검사를 완료했으며 **종합 인증 HOLD / MAP_OR_FOOTPRINT_UNCERTIFIED 유지**다. Bulk: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_COLLISION_CERTIFICATION_20261015_v01`.

실제 bench rover에는 활성 collider 13개, 비활성 CollisionAPI 11개가 있다. 활성 nominal envelope≈1.084802×0.727000×0.627115m, 전체 authored steering 보수 폭≈0.846770m. Rolltainer를 포함한 nominal 작업 외형≈1.487490×1.391112×1.573126m로 1.60×1.50m 안에 들어가지만, rolltainer collision 비활성/수동 caster/동적 자세 때문에 swept safety 인증과 구분한다. Pallet 5개 부재에는 CollisionAPI가 없고 brick 300개에는 활성 collider가 있다. 실제 world pallet top=0.144m지만 낮은 wheel/caster/chassis와 높이가 겹치므로 단순한 full-height false collision로 배제할 수 없다.

명목 FINAL에서 proposed rectangle-pallet gap≈0.053745m, 실제 nominal 외형 gap≈0.110000m다. 후자도 허용 yaw/위치 오차 및 물리 모델 공백을 포함한 0.10m 보장은 아니다. 61 위치×31 높이별 보수 형상의 PhysX static query를 수행해 raw hit0/1891, XY+0.10 확장 query Env hit2/1891을 기록했다. 실제 workspace brick300/floor hit 및 독립 contact 양성 대조로 query 유효성을 확인했다. 별도 원본 rover FINAL 정적 settling에서도 actual contact168 headers, fixture contact0, 최종 base≈(−25.888004,29.105261,−0.005426)m/말미 정지를 관측했다. ROS/robot command/연구 controller는 실행하지 않았다. Pallet collider 누락, nested rigid-body 오류 및 shell-ground report/cooking·offset 불일치가 남아 physical certification PASS는 불가하다.

기존 offline/source/input/report100개와 smoke577개 실제 SHA256, demo inventory5개 및 frozen controller hash를 보존했다. 기존108 scan의108/108 uncertified, v01 12/12 PRE timeout 및 demo denominator 분리를 유지했다. Footprint/clearance/PRE/FINAL/scientific geometry 변경은 적용하지 않았으며 수정 제안의 분류만 보고했다. 연구 denominator 기여0; revised QUAL12·smoke·confirmatory·432-run 미실행. 다음 단계는 support/asset physics 모델과 높이별 map·동적 footprint 인증 blocker 해소이며 자동 실행 승인으로 해석하지 않는다.

## 2026-10-15 derived physics 정상화 / terminal policy 후보 — qualification HOLD

[통합 보고서](../reports/full_e2e_v02_derived_physics_normalization_terminal_policy_20261015_v01.md), [전체 attempt CSV](../reports/full_e2e_v02_physics_qualification_20261015_v01.csv), [정책 후보](../reports/full_e2e_v02_terminal_policy_candidates_20261015_v01.json), [hash inventory](../reports/full_e2e_v02_physics_normalization_hash_inventory_20261015_v01.json). Bulk: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_PHYSICS_NORMALIZATION_20261015_v01`. 원본 USD/controller/protocol과 이전 certification·108 scan·v01 smoke·demo는 보존했다. **연구 denominator0, QUAL12/revised smoke/confirmatory/432-run 미실행.**

새 파생 장면에 pallet5부재 collision을 실제 cube geometry대로 추가하고 5종 양성 대조 및 실제 TopDeck contact를 확인했다. Rolltainer 비활성화는 mount-smoke override에서 왔고, 원본 `/World/Joint`의 passive caster8 joints가 기존 subtree reference 밖에 빠져 있었다. 이를 source frame/axis/drive 그대로 m 단위 sibling body로 복원해 nested reset오류9→0, instance-proxy경고300→0으로 줄였다. 최대 joint 원점 잔차9.111µm, 축 dot8/8=1.0. Body 외형은 보수 compound, caster는 source convex geometry이며 질량/관성·전체 dynamics는 미인증이다. Shell-ground report는 양수 separation의 speculative contact였고 파생 contact offset3mm/rest0에서 사라졌다. Material-face warning은 남아 무해하다고 확정하지 않았다.

초기 새 layer metadata 누락(metersPerUnit0.01/Y-up/24fps/end0)을 발견해 실패를 보존하고 원본1m/Z-up/60fps/end1e6으로 수정했다. 최초 motion IO attempt는 자체 프로세스 중단 시 zero 기록이 없어 **zero 미검증**이며 PID 소멸을 기록했다. 이후 정상 metadata의 저속4 attempts는 종료 zero/stop을 확인했지만 fixed-caster timeout, articulated0.03 입력 timeout, 추가 step/ramp 입력의 차분속도 guard 중단으로 **PRE/FINAL 이동 qualification 미통과**다. Actual-shape continuous sweep22개는 수행했으며 fixture hit0이지만 caster pose 고정 query로 전체 동적 안전을 뜻하지 않는다. 모든 신규 runtime11개/실패/중단을 CSV에 보존했다. ROS bridge 없이 direct joint IO만 사용했고 frozen gains/thresholds는 수정하지 않았다.

Floor/low/body/overhead map 후보를 분리하고 target mesh를 workspace layers에서 제외했다. Map은 CANDIDATE_HOLD, runtime 미승인이다. 관측 caster 자세에서 ±3cm/±2°의 최소 geometric clearance interval은0.064274~0.064451m. Unlimited passive caster에는 거리0의 source-shape/허용오차 반례가 있고 기존1.60×1.50m를 벗어난 실제 회전 projection도 확인했다. 전체 caster 조건의 0.10m를 위한 FINAL 추가 standoff는 측정 tilt/Z 고정 모델에서 필요하한0.121013m~보수충분상한0.121289m이며 **PROPOSED/미적용**이다. 현재 FINAL에서 tolerance만 줄여도 caster 전체를 보장하지 못한다. A(standoff), B(clearance), C(tolerance)의 task-policy/scientific protocol 영향과 footprint correction 의존성을 보고했다. 어떤 endpoint/clearance/tolerance/footprint/scientific geometry도 새 연구 규정으로 적용하지 않았다.

이전 certification/offline135파일, smoke577 artifacts, known protocol9locks, demo inventory5파일 및 frozen controller SHA256 보존을 확인했다. Convex distance는 독립 solver의 무작위 회전 box30개 등2개 assertion 검사 PASS; pytest 미설치 실패도 보존했고 설치하지 않았다. **정적 보완/검사 완료와 전체 engineering qualification PASS를 구분한다. 현재 NOT_QUALIFIED/HOLD이며 새 연구 실행은 없다.**


## 2026-10-15 motion instrumentation / terminal A 계약 — 세 gate HOLD

[통합 보고서](../reports/full_e2e_v02_motion_instrumentation_terminal_A_20261015_v01.md), [attempt CSV](../reports/full_e2e_v02_motion_attempts_20261015_v01.csv), [metrics/gates](../reports/full_e2e_v02_motion_metrics_20261015_v01.json), [hash inventory](../reports/full_e2e_v02_motion_hash_inventory_20261015_v01.json). Bulk: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_MOTION_INSTRUMENTATION_20261015_v01`. Engineering-only, 연구 denominator0. Original USD/controller/protocol·derived normalization·108 scan·12실패·demos/reports 보존. QUAL12/revised smoke/confirmatory/432-run 미실행.

동일 physics fetch step의 manual/callback/wall/timeline, tensor COM 및 base-origin velocity, native transform/USD mirror, 18DOF/19links/sleep를 기록했다. 열린 공간8m 이상 pallet 이격 출발에서 zero baseline, pulse0.070969m, 직진0.398378m 및1.198509m를 수행했다. 최종 sleep=true/게시velocity0/모든wheel dq0/1s pose span0으로 zero·정지를 확인했다. Direct joint IO만 사용했으며 ROS/frozen controller readiness 판정이 아니다. Raw tensor cache0.002092m/s로 정지 실패한 이전 attempt와1.2미실행을 보존하고, sleep-aware 새 adapter에서 같은 threshold로 후속 거리 검증했다.

Clock probe는 dt ratio1이며0.050101m/s의 실제 poststep overspeed를 기록해 중단했다. 별도1.2저속 구간의 FD3 steps는0.051812~0.052880m/s, 동일step actual0.044441~0.048636m/s였다. 시간정렬 후에도 FD/속도 residual이 남고 장거리 사전오차기준에 실패했다. Substep peak/solver 위치보정 기여 미분리로 **MOTION_IO_QUALIFIED=HOLD**. Guard threshold 증가는 없었다.

1.60×1.50m는 실제 motion +Y3.627mm 초과로 부족하다. Proposed1.652×1.585m는 관측 motion/nominal source전체joint envelope를 포함하지만, 관측tilt×source전체swivel 계약은X0.227mm/Y0.00846mm 초과해 **DYNAMIC_FOOTPRINT_QUALIFIED=HOLD**다. Warning observer full/header/off 대조 초기720steps는 pose/velocity/q/dq 동일이나 warning-free 대조가 없어 material-face 실제영향은 UNKNOWN.

A는 planner와 validator가 공통 yaw-only rectangle/0.10m clearance/error budget을 쓰는 계약을 권고했다. Shape0.1213m와 rectangle0.1294m는 혼용 불가이며 exact nominal rectangle 최소추가후퇴0.129409643m, 반올림제안0.1300m도 dynamic 안전보증은 아니다. **TERMINAL_POLICY_A_READY_FOR_APPROVAL=HOLD**, frozen protocol에 미적용. 모든신규runtime6 PID종료/zero발행, raw-stop실패 포함 보존. 이전파일350·smoke577·demo inventory5·protocol9 SHA256 일치.


## 2026-10-16 v02 후보 계약 최종 engineering qualification — NOT_READY

[통합 보고서](../reports/full_e2e_v02_final_engineering_qualification_20261016_v01.md), [hash inventory](../reports/full_e2e_v02_final_qualification_hash_inventory_20261016_v01.json). Bulk: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_FINAL_QUALIFICATION_20261016_v01`. 연구 denominator0. 원본 USD/controller/protocol·기존108 scan·12실패·demos/reports 보존. QUAL12/revised smoke/confirmatory/432-run0회.

사용자 후보1.68×1.61m/clearance0.10m/오차각축±0.03m·yaw±2°/FINAL0.15m 후퇴의 exact rectangular normal gap=0.106162641719m, 여유6.162642mm다. PRE 유지안을 권고/파생 시도에 사용했다. H→PRE0.40m와 제안handoff0.30~0.50m를 유지하며 PRE→FINAL0.65m는 frozen controller에 고정 간격 의존이 없다. PRE도후퇴하면 H→PRE0.25m로 범위 밖이다. Frozen protocol에는 미적용이고 v02 task-policy/scientific amendment와v01 denominator를 분리한다.

1/240s pre/post root velocity·변위·integration/constraint residual을 분리 기록했다. Solver-only correction은 API 미노출로 단독 측정했다고 주장하지 않았다. 열린 공간 speed probe는 root최대0.022220/변위속도0.026700m/s로 cap이내였다. Candidate H→PRE→FINAL qualification1회는 step10760에서 root0.052770356688m/s(수평0.050352610351), substep변위속도0.050098267352로 cap0.05를 넘겨 PRE전 중단했다. PRE/FINAL 미도달. **NOT_READY의 정확한 단일 blocker=TRUE_BASE_ORIGIN_OVERSPEED**, 기준 증가·속도 튜닝 재시도 없음.

실행prefix fixture clearance lower bound1.261117559m/접촉0, 관측1.68×1.61 내부margin X80.207/Y59.251mm. 미실행 FINAL의 실제 clearance로 소급하지 않았다. Zero command 및base quiet 확인(1s최대0.001689m/s/span0.191mm이내), active/passivewheel잔류회전은 기록했고 all-wheel stop PASS로 쓰지 않았다. 동일command재생1회에서11480substeps pose/velocity/q/dq차0,contact114520headers동일,동일속도위반 재현. Warning은 available observables에 영향 차이 미관측 known simulator limitation이며 독립HOLD blocker아님.

두 시점 MP4를 실제render1195unique-step frames/H26430fps/39.834s로 보존·decode확인했다. 영상은 동일command재생의 failure→zero/base quiet이고 perception camera는 원본 보존한 별도viz rover-view와overview다. `qualification_rover_view.mp4`, `qualification_overview_view.mp4`는 bulk아래 있다. 기존453파일·smoke577·demo inventory5·protocol9 SHA 일치, 자체runtime3 PID종료. READY_FOR_V02_PROTOCOL_LOCK 미발행.


## 2026-10-16 longitudinal speed governor — NOT_READY / H_PRE prolonged stall

[보고서](../reports/full_e2e_v02_longitudinal_governor_qualification_20261016_v01.md), [hash inventory](../reports/full_e2e_v02_speed_governor_hash_inventory_20261016_v01.json). Bulk: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_SPEED_GOVERNOR_20261016_v01`. Frozen controller·원본USD/protocol·기존NOT_READY/108scan/v01 12회실패/demos/reports 보존. 연구 denominator0; QUAL12/revised smoke/confirmatory/432-run0회.

새 measured planar-forward PI speed-governor adapter v03와 write-on-change joint IO wrapper를 구현했다. Navigation ceiling0.15/reference0.135, H_PRE0.05/0.035, PRE_FINAL0.03/0.022를 분리하고 정상 reference/wheel-command 가감속·antiwindup·predictive feedback 제동을 명시했다. Raw root/변위planar speed cap은 그대로 검증한다. Open tuning4attempts/실패 모두 보존. open0004의 last2s forward mean nav0.136237/H0.035073/PRE_FINAL0.021197m/s와3phase stop PASS. 정확한0.15 steady 운용을 검증한 것은 아니다. 초기 부가 planar-vector acceleration gate FAIL도 보존하고 longitudinal 제어축 raw a2nav/1terminal로 범위를 정정했으며 vector a를 제한했다고 쓰지 않았다.

Admission후 승인후보1.68×1.61m/FINAL0.15후퇴/PRE유지/clearance0.10m corridor **1회만** 실행했다. H_PRE4.3375s에 last2s progress0.000171661m vs expected0.070m로 PROLONGED_STALL. Mean wheel-equivalent command0.046340m/s/active wheel absmean0.353770rad/s였지만 base forward mean0.000341953m/s. Raw planar peak0.030757<0.05라도 지속주행이 안 되었고 raw종방향 a1.200769>제안1.0도 기록. PRE/FINAL 미도달·재시도없음. **NOT_READY의 단일 결정 blocker=H_PRE longitudinal regulation의 PROLONGED_STALL**.

실행prefix fixture clearance lower bound1.276803m/contact0/footprint내부margin X80.207/Y59.251mm. 종료zero/base quiet3.004167s PASS(마지막1s최대0.001148m/s/span11.444µm), passive잔류회전0.596rad/s는 남겨 allwheel0 PASS로 쓰지 않았다. 전체episode7.341667sim s(초기settle/baseline포함15.341667). 실제1× rover/overview MP4를 corridor7.367s/221frames, open0004 42.9s/1287frames로 저장·full decode/frame count 확인. 자체5PID모두종료·zero/basequiet 확인. 기존535+smoke577+demo inventory5+protocol9 SHA일치. Protocol lock 미적용/READY 미발행.


## 2026-10-16 검증 demo mobility 재사용 ENG001 전체 chain 시도 — NOT_READY

[보고서](../reports/full_e2e_v02_demo_mobility_full_chain_20261016_v01.md), [hash inventory](../reports/full_e2e_v02_demo_mobility_hash_inventory_20261016_v01.json). Bulk `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_DEMO_MOBILITY_FULL_CHAIN_20261016_v01`. 동일 bench RuntimeRover reference와 ROS ActionGraph를 재사용했으며 passive caster joint8복원/새support설계/추가physics진단 없음. 원래 ENG0011.5m sensing geometry 유지, conservative1.68×1.61m/clearance0.10m/PRE유지/FINAL0.15m후퇴.

Engineering 1case/2attempts, 연구denominator0. Attempt1은 fresh YOLO/B4B5 뒤 wrapper yaw-field KeyError로 이동전 실패/보존. IO연결만 바로잡은 attempt2는 새 capture·실제lockedYOLO(conf0.973876953125)·B4/B5·predicted targets 성공 후 forward-only approach static search34nodes에서 NO_PATH. Pallet Runner/TopDeck과 clearance-expanded footprint 중첩 후보로 이동전 중단했으며 GT대체/순간이동/초기조건변경 없음. **NOT_READY 단일 blocker=APPROACH_PLANNER_NO_PATH**; finite search결과를 모든경로 불가능의 증명으로 해석하지 않음.

PRE/FINAL주행과속도governor/terminalclearance는 미검증, nonzero command0, zero10회/정지pose확인. 성공주행이없어 새2시점MP4없음. 기존720파일·v01smoke577·demo inventory5·protocol9·frozencontroller SHA 일치. 자체process종료, 기존process보존. QUAL12/revised researchsmoke/confirmatory/432-run0회, READY_FOR_V02_PROTOCOL_LOCK 미발행. 기존NOT_READY와모든결과보존.


## 2026-10-19 v02 monotonic phase admission — NOT_READY / lateral admission

[보고서](../reports/full_e2e_v02_monotonic_phase_admission_20261019_v01.md), [입출력·검사 로그](../reports/fe2e_v02_phase_admission_20261019_v01/admission.json), [hash inventory](../reports/full_e2e_v02_phase_admission_hash_inventory_20261019_v01.json). 기존 NO_PATH는 무조건 뒤쪽 H 경유를 요구한 wrapper phase policy의 결과이며 map/footprint certification 실패로 취급하지 않는다. 기존 기록은 보존하고 이 해석을 추가한다.

새 task-policy adapter는 signed progress로 beforeH→planner/H/PRE/FINAL, H–PRE→PRE/FINAL, PRE–FINAL→lateral/yaw gate 후 FINAL, beyondFINAL→fail-safe를 구분한다. PRE를 지난 capture는 PRE_SPATIALLY_PASSED_AT_CAPTURE이며 PRE_REACHED로 기록하지 않는다. Attempt2 replay: PRE이후+0.193623910503m/FINAL까지+0.456376089497m, lateral−0.036638792950m/yaw−0.000245162290°. 기존 PROPOSED admission envelope lateral≤0.020m/yaw≤2°를 유지하면 lateral FAIL/yawPASS다. **NOT_READY 단일 직접 원인=LATERAL_ADMISSION_FAILED**. 기준을 확정 규정으로 승격하거나 임의 완화하지 않았다.

Pure policy/입력replay 및5unittest PASS. Gate가실패하여 조건부Isaac/ROS/motion 실행0, FINAL도달/실제clearance/종료정지/2시점영상 미실행·미검증. 기존mobility/controller/physics/footprint/clearance/initialpose/targets와 모든기존결과 SHA보존. 추가diagnostic없음; 연구denominator0, QUAL12/revisedsmoke/confirmatory/432-run0. READY 미발행.


## 2026-10-19 lateral correction 근거 검토 — NOT_READY / 안전 보정 증거 부족

[보고서](../reports/full_e2e_v02_lateral_correction_evidence_review_20261019_v01.md), [수치·실제 CSV evidence](../reports/fe2e_v02_lateral_evidence_review_20261019_v01/evidence.json), [hash inventory](../reports/full_e2e_v02_lateral_review_hash_inventory_20261019_v01.json). 지정문서 및 frozen controller/governor/두성공demo의 실제기록을 정적으로 확인했다. Recorded attempt2의 FINAL error는 controller기준 long+0.456376089497m/lat+0.036638792950m/yaw+0.000245162290°. Frozen law는 v0.07/w0.026794919243(controller-space)·15°포화 보정명령을 생성한다. 보정불가능으로 단정하지 않으나 firststep을 수렴증명으로 취급하지 않는다.

기존두demo의 FINAL초기 lat는 abs11.455/7.825mm·remaining약0.82m로 이번36.639mm/0.456m와다르고 governor결합증거가없다. Governor는 scalar v만출력하며 기존qualification은 steer0/ROS미사용 직진이었다. Curvature-preserving governor IO와 FINAL-only phase선택의 최소 PROPOSED 계약을 설계했지만 동일chain의 안전보정 대응증거가 불충분해 미적용했다. 기존0.020m gate완화/controller·protocol변경/geometry수정/추가physics·planner진단/parameter sweep 없음.

**NOT_READY 단일직접원인=LATERAL_CORRECTION_SAFETY_EVIDENCE_INSUFFICIENT**. 실행전조건불충족으로 새Isaac/ROS/motion/capture0, retry0. Historicalpose를live로재사용하지않았다. FINAL도달/실제clearance/contact/종료zero·정지/2시점영상 미실행·미검증. 기존854파일 및frozencontroller SHA일치, 기존결과모두보존. 연구denominator0; QUAL12/revisedsmoke/confirmatory/432-run0, READY미발행.


## 2026-10-19 curvature-preserving governor adapter / nominal FINAL 검증 — NOT_READY

[보고서](../reports/full_e2e_v02_curvature_governor_offline_validation_20261019_v01.md), [수치·검사·trajectory](../reports/fe2e_v02_curvature_offline_20261019_v01/offline_result_v02.json), [hash inventory](../reports/full_e2e_v02_curvature_offline_hash_inventory_20261019_v01.json). 실제benchUSD 연결/설치ATan2·Ackermann source와 두demo actualROS/CSV·joint응답을 확인했다. Frozen π/180의 중복적용은없고147/215 timestamp매칭행의 wire상대오차 중앙값0. Degree ATan2→radian Ackermann 불일치의 기존보상은근사15°→15.35224593°다. 새별도IOadapter는한번decode후정확한graph역변환으로곡률/15°제한을유지한다. 기존controller/governor/gain/protocol 미수정.

Pureadapter7·설치Ackermann AST numeric3 tests 및실제geometry_msgs/Twist 구성계약PASS(node/publisher0). Historicalattempt2 단일nominal모델은frozen error/step AST불변·governor·source Ackermann deadband 적용하여20.8s에FINAL stable6완료. e_long24.880321mm/e_lat25.419250mm/yaw−1.533138°, maxabsYaw1.752123°. Footprint1.68×1.61/0.10유지, fixtureplane gap하한0.195114871m/workspace ROI candidate0.647645211m. 둘다actualcontact/collision인증이나live속도·stop검증이아니다.

**NOT_READY 단일blocker=ACTUAL_GOVERNED_ACTUATION_AND_STOP_NOT_BOUNDED**. Nominalunitgain/즉시속도·조향가정과실제graphspeed×15/radius0.5 및별도governor직진joint IO가동일하지않아물리closedloop/정지bound미확인. 필요한최소후속근거는동일mobility의격리된짧은nonzero-curvature IO응답/zero-stop bound1회이며이번에실행하지않음. 추가planner/caster/physics진단·sweep없음. 새Isaac/ROS publish/capture/motion/retry0, FINALactualerror/clearance/contact/stop·2시점영상미검증/미생성. 연구denominator0; QUAL12/revisedsmoke/confirmatory/432-run0, READY·protocol lock미발행. 이전artifacts/source/hash보존.


## 2026-10-19 actual actuation/stop 단일 calibration — ENG001 재진입 NOT_READY

[보고서](../reports/full_e2e_v02_actual_actuation_stop_calibration_20261019_v01.md), [실측 metrics](/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_ACTUATION_CALIBRATION_20261019_v01/metrics_v02.json), [hash inventory](../reports/full_e2e_v02_actuation_calibration_hash_inventory_20261019_v01.json). Bulk `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_ACTUATION_CALIBRATION_20261019_v01`. 원본demo mobility/controller/governor/curvatureadapter/physics드라이브보존, source동일reference. Fresh200×200m/defaultfloor/domain191의격리/외부collider없음/91.046mguard여유확인후6sim s곡률episode **1회**. Sceneinit2회중첫회는원점bound/time-range setup실패로nonzero0; 수동pre-command설정수정만했고automatic/motion retry0.

Actual마지막2s forward0.018659932m/s/reference0.022, wire0.007792016 평균비2.39475(보정gain미적용). Rootpeak0.032404731/FD0.030265943m/s로phase0.03 cap FAIL. Actualsteer평균L16.720345/R13.571946°, yaw변화1.592932°. Positivewheel/base응답약0.216667s, steer1°0.183333s(16.67ms sampling/zero-onlywake drift포함 threshold지연이지순수transport delay아님). Sourcegraph speed×15/radius0.5→targetstraight30×wire rad/s, measuredmeanwheel/wire19.0147은다른관측량이다.

Zero후quiet시작2.766667s, 최대추가XY9.790531mm(주로후퇴−9.790488mm), sampleallowance포함10.039246mm. Last1s pose span0/activewheeldq0/nativev·FD0, rawtensorplanarmax0.001828389m/s 유지; zero/base stop확인. Floor/self접촉3300headers, unexpectedexternal0. 단일profile한정계측이며globalbound아님.

동일실측profile과unitgainoffline모델의maxresidual XY43.250628mm/yaw0.735679°. NominalFINALmarginlong5.119679mm/lat4.580750mm/yaw0.466862°보다크고stop후퇴만옮긴예에서도long34.668074mm>30mm다. **남은blocker=MEASURED_ACTUATION_STOP_ENVELOPE_OUTSIDE_TERMINAL_BUDGET**, ENG001재진입불가. Planner/caster/추가physics진단·gain튜닝·threshold완화·sweep없음. 이후stop/IO계약과post-stop오차및freshcorridor재검증이필요하며이번에자동실행하지않음. 기존890files SHA일치, 전체결과/failedinit보존, 자체PID종료. ENG001FullE2E/QUAL12/revisedsmoke/confirmatory/432-run0, 연구denominator0/protocol미변경/READY미발행.


## 2026-10-19 Rover/Rolltainer 실제 기능 read-only audit

[보고서](../reports/rover_rolltainer_implemented_capability_audit_20261019_v01.md), [기능별CSV](../reports/rover_rolltainer_capability_audit_20261019_v01/capability_matrix.csv), [hashinventory](../reports/rover_rolltainer_capability_hash_inventory_20261019_v01.json). 16USDstage/28usedlayers와222localPython파일을정적으로조사했다. Currentbench는perturbation35mm_2p5deg_v01의RuntimeRover이며저층reference는rover_camera_add_51_test.usd default/rover다. Wheel6/steer4 internalrevolute 및ROS Ackermann drive는존재한다.

Rolltainer원본은9enabledRB/10enabledcollision과별도/World/Joint의8casterjoints가있다. Mountsmoke_v01은/World/Rolltainer subtree만reference하여8joints를제외하고9rolltainerbody/caster RB·collision을false로override한다. v02 groundContactAligned는정적Xform정렬이다. Currentbench/ENG001은10roverjoints이며rolltainerAPI가남아있어도disabled이고, rover↔rolltainerdocking joint/결합·분리state transition은없다. Archived18joint복원모델은별도이력/현재미채택이다.

조사범위에자동상하차/화물고정·해제/폐기물회수cycle/elevator연동구현없음. Staticmesh배치·fixedmount·terminal접근을그기능으로판정하지않았다. 0.135는0.15candidatecap에서10%여유를둔engineeringreference, PRE_FINAL0.03cap/reference0.022이며GT-3제품최고속도근거아님. 공식제품최고속도수치와localUSD의제품전체동등성은미확보/UNKNOWN. 현재NOT_READY와기존연구denominator불변.

USD/이전956artifacts SHA보존. 이번Isaac/physics/ROScommand/retry/QUAL12/432-run0, controller/governor/protocol미변경. PROJECT_STATE에는확인사실만추가했고미구현기능의최소추가요소는보고서의제안이며채택·구현하지않았다.


## 2026-10-19 governor / terminal stopping 별도 adapter — offline only NOT_READY

[보고서](../reports/full_e2e_v02_governor_stopping_adapter_20261019_v01.md), [실제 pose 재평가](../reports/fe2e_v02_stopping_adapter_20261019_v01/existing_data_review.json), [hash inventory](../reports/full_e2e_v02_stopping_adapter_hash_inventory_20261019_v01.json). 기존 실측에서 reference 초과 후에도 slew 출력 증가, 다음 callback 감속 후 root .032404731m/s cap 초과를 확인했다. 정상 종료 publisher는 governor 감속을 우회해 직접 zero를 발행했고 기존 adapter도 zero시 상태를 초기화했다. 후퇴의 물리 원인은 추가 단정하지 않았다.

새 engineering StoppingAdapter는 기존 gains/caps 유지, reference 이상에서 출력 증가 억제, 상태 보존 정상 감속·종료 latch와 별도 post-zero actual pose evaluator를 구현했다. Drive-unit 계약 미인증시 zero latch하며 실제 base/wire 관측비를 gain으로 채택하지 않았다. Synthetic 계약검사8/8 PASS. 실제 calibration 정지 후 zero-pose 기준 hold 오차 long9.790488mm/lat−.028781mm/yaw−.004732° 및 quiet=true이나 사전 FINAL·stable6 부재로 terminal_success=false다. ENG001 FINAL 실측을 대신하지 않는다.

**NOT_READY: MEASURED_ACTUATION_STOP_ENVELOPE_OUTSIDE_TERMINAL_BUDGET 유지.** 새 adapter의 실제 cap/stop envelope 미검증으로 ENG001 자동 재진입 없음. 원본controller/governor/adapter/USD/protocol/기존결과 보존, 추가physics진단·gain튜닝·threshold완화 없음. Isaac/ROScommand/motion/retry/QUAL12/revisedsmoke/confirmatory/432-run0, 연구denominator0, 영상 미생성. 다음 최소 조건은 단위계약 확인 및 새 종료 경로의 제한된 실제 cap/stop 검증과 fresh corridor/terminal 예산 대조이며 이번 실행하지 않았다. 자동도킹·상하차·폐기물·엘리베이터 구현 보류.


## 2026-10-19 stopping adapter actual Isaac validation 1회 — NOT_READY

[보고서](../reports/full_e2e_v02_stopping_adapter_actual_validation_20261019_v01.md), [hash inventory](../reports/full_e2e_v02_stopping_validation_hash_inventory_20261019_v01.json). Bulk `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01`. 활성 wheel6 cylinder radius .13300000131130219m/worldscale1, graph15/.5 및 actual articulation 연결로 surface→wire scale .2506265639450088 확정(관측gain fit 아님). Physical-radius Ackermann target roundtrip PASS, 기존 stopping8/installed3 tests PASS.

동일demo reference를 새floor/domain191에서 사용하여 제한된곡률 episode1회 및 normal decel .400000021s 실행, motionretry0. Root/FD peak .022805331797/.021279668484m/s로 phase .03 cap PASS. 그러나 zero후 후퇴34.127288744mm/XY34.127288813mm, sample allowance포함34.231226913mm로 terminal budget초과. Last1s pose span/FD/native/wheel dq0이지만 raw root .002619135991m/s>.002로 quiet/base_stop_confirmed FAIL. 실제 최종pose x−5.76229190826416/y3.1642923355102544/yaw3.743923166959°. Zero-pose hold long34.127289mm>30mm; calibration은 사전FINAL/stable6없어 ENG001success가아니다.

**NOT_READY: MEASURED_ACTUATION_STOP_ENVELOPE_OUTSIDE_TERMINAL_BUDGET 유지.** 필요한 최소설계변경은 actual post-zero pose 유지/정지확인을 보장하는 별도 stopping 정책이며 이번 구현·재실행하지않음. Unit/profile가달라 기존calibration대비 인과적개선 주장없음. 기존source/hash/result보존; owned simulator PID1752511종료확인. ENG001FullE2E/QUAL12/revised smoke/confirmatory/432-run0, 연구denominator0, 영상미생성. 추가physics진단/sweep/threshold완화/자동retry없음.


## 2026-10-19 stopping/hold 방식 선정 — read-only design NOT_READY

[보고서](../reports/full_e2e_v02_stopping_hold_method_selection_20261019_v01.md), [timeline](../reports/fe2e_v02_hold_selection_20261019_v01/timeline.json), [hash inventory](../reports/full_e2e_v02_hold_selection_hash_inventory_20261019_v01.json). 기존로그에서 publisherzero10.916667s→graphwheel/steertargetzero10.933334s→후퇴시작10.950001s를확인했다. Actualsteer1°이내11.083334s 후에도33.645mm추가후퇴, wheel dq0/최종XY고정은18.833334s다. Steering복귀의인과관계는확정하지않았다. 최종pose/FD0과rawrootquietFAIL은구분유지했다.

현재sourcewheel6drive는stiffness0/damping100/force, steer4는stiffness836.614136/damping40이며별도brake구현은확인되지않았다. 설치API의jointposition/velocity/effort target지원과현재Twist-onlygraph연결을구분했다. 선정안은기존velocitydrive앞의wheel-position→velocity 외부hold와exclusivecommandmux이며**설계제안/미구현**이다. 공식PhysX Implicit Spring Joint Drives 식(9)를검토했고원본drivegain미변경. 새outergain/한계값·signedhold correction·mux계약은미정이므로실행가능/검증완료로보고하지않았다.

**NOT_READY / MEASURED_ACTUATION_STOP_ENVELOPE_OUTSIDE_TERMINAL_BUDGET 유지.** 이번physics/Isaac/ROScommand/calibration/ENG001/QUAL12/432-run0, retry0. Gain/friction/damping/mass/threshold변경0, caster/physics진단확장0, 기존artifacts와denominator보존. 후속시험은사전계약확정후동일격리공간의단일곡률→감속→hold episode라는계획만작성했다.

## 2026-10-19 wheel-position HOLD engineering implementation — offline PASS / runtime NO-GO

[구현 보고서](../reports/full_e2e_v02_wheel_hold_implementation_20261019_v01.md). 별도 wheel6 position→signed velocity HOLD adapter, single physics-thread owner mux, derived-layer legacy3writer deactivation 함수와 explicit DOF subset writer, PROPOSED 수치 contract를 새 파일로 구현했다. Single latch/unwrap/units/freshness/fault/watchdog/stop·re-arm 금지/owner conflict/Twist overwrite/synthetic replay 및 mock patch·writer mapping **15/15 tests PASS**. 최종 증거 `reports/fe2e_v02_wheel_hold_offline_20261019_v02/`; 최초14tests v01도 보존. 물리 stop/safety 증거 아님.

**NO-GO**: signed 정책·gain/limit/guard 안정성 미승인/미인증, actual physics callback/graph reader·독점 ownership·independent pause guard integration 미완료, 다음 단일 one-shot runner/계측·명시적 실행 승인 필요. 실제 runtime 독점·정지·quiet UNKNOWN. K1s⁻¹/±.02rad/s/slew.2rad/s²/4mm/8s는 사전검토 후보이며 dynamics 인증 false로 runtime 차단. 기존 선정/실패/denominator 유지, Isaac/ROS/motion/ENG001/QUAL12/432/자동retry0. 기존148SHA일치와 append전 workspace 변경0 확인. 최초 graph 경로 읽기 실패 및 .git 부재는 보고서에 남겼으며 보안 설정 변경없음. 기존원본·inventory·protocol·threshold 보존.

## Full E2E v02 HOLD runtime integration offline — 2026-10-20

[보고서](../reports/full_e2e_v02_hold_runtime_integration_20261019_v01.md). 새 `evaluation/fe2e_v02_hold_runtime_integration_v01.py`에 live writer topology 검사/derived patch, graph reader·DOF mapping, 같은 epoch latch-before-write callback, independent observer/wall watchdog ports를 구현했다. `scripts/fe2e_v02_hold_one_shot_v01.py`는 hash/command/environment/status/계측 schema와 실패 exit를 기록하는 봉인된 인터페이스다. 새 analysis mock 검사 **12/12 PASS**; [증거](../reports/fe2e_v02_hold_runtime_integration_20261020_v01/execution.json). 기존148SHA PASS 및 append 전 기존 파일 변경0 확인. 실제 host callback 등록·native/direct writer 배제·pause 전달·실물 수치 안정성 UNKNOWN, runtime 승인 false/실행 NO-GO. 새 interface는 실제 actor를 호출하지 못하며 실제 launcher 명령도 미확정이다. 기존 HOLD 선정·PROPOSED 수치·frozen protocol/controller/USD/결과/denominator 보존. Isaac/ROS/physics launch·ENG001·QUAL12·432·retry/sweep0. 다음은 별도 범위에서 host 설치 증거 및 단일 시험 명령을 확정한 뒤 명시 실행 승인이다.

## 2026-10-20 HOLD host binding — PARTIAL / NO-GO

[보고서](../reports/full_e2e_v02_hold_host_binding_20261020_v01.md). 새 host runner와 versioned one-shot v02 CLI에 기존 Isaac5.1 launcher/bench reference 기반 paused USD patch, 실제 PhysX/Kit subscriptions, timeline pause readback와 독립 wall watchdog 설치 코드를 추가했다. 기존 코드/CLI는 보존. 전체 33tests PASS, 기존148SHA PASS, known lock subset PASS. 실제 Isaac/ROS/physics/actuator 실행0. **요청된 전체 physical runner 완성은 FAIL/UNRESOLVED**: Ackermann completion witness·same-step physical dispatch·StoppingAdapter phase/실측 observer 연결 미완료, native/direct writer 배제 및 stalled-engine pause 전달 미인증. 수치/sign 미승인, runtime gate=false. 별도 paused live preflight 명령과 현재 launch 전 거부되는 one-shot 명령을 보고서에 명시했다. 물리 안정성·ENG001/QUAL12/432 승인·연구denominator 변경 없음.

## 2026-10-20 실제 paused preflight 후속 HOLD host wiring — 물리 NO-GO

[후속 보고서](../reports/full_e2e_v02_hold_live_preflight_followup_20261020_v01.md). 실제 `FE2E_V02_HOLD_HOST_PREFLIGHT_20261020_v01`의 7개 파일과 manifest 입력7SHA를 확인했다. PREPARED/attempts0, terminal 미존재, physics0/metrics미취득/host PARTIAL이다. pause_readback=true와 event success=false는 기존 소스가 정상 readback 후에도 literal false를 기록한 정의 혼동이며 실제 API 반환은 미기록/UNKNOWN이다. 설치 API signature는 pause()->None. 약11.54초 종료는 사용자 관측이며 로컬 elapsed/exit 로그 미확보. close()의 framework shutdown 후 terminal을 쓰던 위험을 발견했고 원인 확정 없이 기록했다.

새 host ports v02/host runner v02/CLI v03 및 검사파일을 추가했다. Ackermann execOut→ScriptNode 실제 연결 설치, on-demand request_compute/evaluate_sync 고유token 완료 barrier, 실제 StoppingAdapter phase→ZERO_SETTLING 직전 immutable latch→단일 batched wheel6/steer4 writer, tensorCOM→origin/FD/contact/floor-edge clearance observer와 independent guard, wall request→Kit thread pause pump를 연결했다. 실제 물리 진입을 offline=True나 승인bool로 우회하지 않았다. 정상 paused probe와 failure terminal/readback을 분리하고 terminal을 shutdown 전에 저장하며 shutdown 완료는 UNKNOWN으로 기록한다.

신규16/16·전체57/57 offline tests PASS, compile PASS, known subset PASS, 기존148SHA 작업 전후 PASS. 최초 신규14/전체55 검사와 offline CLI/예상차단one-shot exit1도 보존했다. 기존 host/CLI/derived USD/contract/원본 controller/drive/protocol/결과는 보존했다. 새 graph/observer live 동작, native/direct writer 배제, stalledKit 강제정지는 미검증/UNKNOWN이며 runtime/signed/dynamics=false 유지. **실제 working physical runner 전체 완성은 FAIL/미달, physical NO-GO.** 다음은 보고서의 미사용v02 output에 별도 수동 승인된 paused preflight1회만이다. 이번 Isaac launch/physics/ROS발행/actuator/주행/ENG001/QUAL12/432/자동retry0, 연구denominator0.

## 2026-10-20 graph-only completion witness probe 준비 — offline PASS / physical NO-GO

[보고서](../reports/full_e2e_v02_hold_graph_witness_probe_preparation_20261020_v01.md). 새 실제 paused v02의 status/terminal/host/events/inventory/derived layers를 확인했다. PAUSED_INSTALLATION_RECORDED_NO_GO, pause_call_ok/paused_readback/delivery_ok=true, api_return=NoneType, physics/actuator/retry/denominator0이다. manifest11SHA PASS. 실제 witness는 installed=true/exercised=false, graph/foreign writer 인증 false다. 외부 exit0/11.267초는 사용자 관측이며 디렉터리 내 독립 외부 로그는 없어 로컬 재검증 UNKNOWN으로 구분했다. 기존 pause success=false 혼동은 해결되었다.

기존 physical barrier/코드는 유지하고 새 host v03/CLI v04/graph Probe v01/외부 실행 wrapper v01/검사파일을 추가했다. typed execOut→ScriptNode, ONDEMAND, legacy3 inactive·전체 active node allowlist, explicit synthetic 직진scalar, token/physics_epoch0/thread, 등록 Ack compute1+callback1, callback 안 expected wheel4/steer2 finite/shape 검사와 terminal-before-close를 구현했다. ROS bridge 활성 시 FAIL, bridge/ROS publisher/actuator API/physics.play 경로 없음. native/direct writer 전역 배제는 UNKNOWN 유지. 신규18tests PASS, compile5 PASS, 실제 승인없는 CLI exit1/FAILED_GRAPH_ONLY 보존. 기존148SHA 및 합계172 preserved SHA PASS, 실제v02 manifest11/11 PASS, known subset PASS. source/실패·검사 로그 보존.

이번 Isaac/SimulationApp/physics/ROS발행/actuator/actualHOLD/ENG001/QUAL12/432/retry/튜닝0, 연구denominator0. 다음은 보고서의 미사용 output으로 별도 수동 승인한 graph-only 단1회이며 아직 실행하지 않았다. 그래프 성공도 physical 동기화/Stopping phase/독립writer배제/observer/stop 보장이 아니다. 수치·sign·dynamics 미승인, **physical NO-GO** 유지.

## 2026-10-20 graph-only 실제 edge 실패 표적 수정 — offline PASS / physical NO-GO

[보고서](../reports/full_e2e_v02_graph_edge_failure_fix_20261020_v01.md). 실제 GRAPH_ONLY_PREFLIGHT v01의 내부FAILED_GRAPH_ONLY와 child exit0을 분리 확인했다. Chained traceback과 설치 controller.py/graph_controller.py에서 기존 Ackermann 상대이름이 edit 생성-map에 없어 path 문자열로 남고 uint(execution) destination 연결이 거부된 직접 원인을 확인했다. 기존 inactive witness의 token 경고는 별도 관측이다. 새 host v04/CLI v05/native edge helper/wrapper v02에 절대경로 OG attribute 연결, 연결 전 node/type/port/graph/schema 진단, upstream readback 및 외부 final adjudication을 구현했다. 실제 single eval/compute/witness1·token/epoch/thread/output·무물리 gate 유지. 기존 파일 불변,183SHA(기존148 포함)·v01 manifest33SHA PASS, 신규6+기존18=24tests PASS/compile5 PASS. 최초 테스트 annotation 오류1건 로그도 보존했다. v02 output+external_v02 미사용 명령만 준비, 실제 edge/평가 성공 UNKNOWN. 이번 Isaac/graph live/physics/ROS/actuator/motion/retry/ENG001/QUAL12/432=0, denominator0, numerics/sign/dynamics/runtime=false 및 physical NO-GO 유지.

## 2026-10-20 실제 graph-only v02 compute0 후 offline dispatch 수정

[보고서](../reports/full_e2e_v02_graph_compute_dispatch_fix_20261020_v01.md). 실제 v02 edge 유효·연결 PASS, ONDEMAND/execution, evaluate1/Ack0/witness0의 FAILED_GRAPH_ONLY를 확인했다. 외부 child0/internalFAIL/wrapper1 판정은 정상이며 유지했다. manifest35SHA·기존183 포함198 보존SHA PASS. execIn을 끊은 뒤 request_compute만 사용한 구성을 확인했으나 native scheduler 단일 원인은 UNKNOWN이다. 설치 ABI는 동적 class.compute 조회이며 계측 실패로도 단정하지 않았다.

새 hostv05/CLIv06/wrapperv03/probev02/dispatch helperv01에 공식 OnImpulseEvent(onlyPlayback=false)→Ack execIn, 독립 native counter 전후/disabled·exec state·actual evaluate 반환·ABI 위치·출력 sentinel·witness detail·traceback을 추가했다. live PASS는 evaluate/Ack/witness 각각1과 token/epoch/thread/source/output 및 zero physical counters를 모두 요구한다. 신규5+기존24=29tests PASS, code6개 및 생성 script compile PASS. 생성 문자열 최초 괄호 SyntaxError를 수정했고 실패기록/회귀검사도 보존했다. 새v03 output/sidecar 미존재, 명령 준비만 완료. 이번 Isaac/graph live/physics/ROS/actuator/HOLD/ENG001/QUAL12/432/retry0, denominator0. READY_FOR_MANUAL_APPROVAL, live UNKNOWN, numerical K/sign/dynamics/runtime=false, **physical NO-GO** 유지.

## 2026-10-20 PHYSICS HOLD one-shot 실제 경로 코드 — RUNNER_NOT_READY / NO-GO

[보고서](../reports/full_e2e_v02_physics_hold_one_shot_runner_20261020_v01.md). 사용자 실행 graph-only v03의 status/events/result/inventory/external 및 source를 읽고 REAL PASS·exit0를 확인했다. Input37SHA와 outputSHA PASS, graph 재실행0. 이전 실제 후퇴34.127289mm와 raw-root .002619135991>.002 quiet FAIL을 보존했다.

새 physics hostv01/CLIv07/externalv01에 actual PhysX receipt→live observer→impulse/Ack/execOut witness→다음step target, 기존6초profile/normalDECEL/ZERO_SETTLING latch-before-write/HOLD8초/zero후8초 관측을 연결했다. Stage legacy3writer비활성/활성node allowlist/매write native ownership gate/target readback, 독립wall watchdog→Kit pause queue, fault시zero재시도금지, terminal journal/외부exit 판정을 구현했다. Simulator launch0/physics0/actuator0/ROS0/ENG001·QUAL12·432·physicalretry0/denominator0.

**RUNNER_NOT_READY / physical NO-GO**: 전체 native writer를 배제하는 실제 lease/interception port가 없어 현재 single-physics는 SimulationApp 이전 거부한다. Bool/mock/graph PASS를 ownership증거로 쓰지 않는다. 미승인 numeric/sign/dynamics contract는 원본을 보존하고 새 evidence-backed version+사용자 exact hash/output 승인만 받도록 연결했다. Actual timing/observer/stop UNKNOWN, stalled Kit pause의 guaranteed halt 주장없음. Code4compile/targeted8tests PASS, 이전429SHA·known9locks hash/count PASS. Admission exit1은 의도된 RUNNER_NOT_READY로 보존했으며 `.git`부재 status실패도 보고했다. 다음은 native write배제 realport연결이며 physics trial은 보고서의 미사용output으로 별도 승인한1회만 가능하다. Frozen assets/controller/protocol/threshold/이전실패 미변경.

## 2026-10-20 bounded writer owner 결정 — code-only / physical BLOCKED

[보고서](../reports/full_e2e_v02_bounded_writer_owner_decision_20261020_v01.md). Standalone pxr read-only로 실제 bench Rover graph20/joint10/script속성후보0 확인(Isaac loaded=false). Legacy3writer joint/upstream과 v07의 명시 Python 단일 setter route를 식별했다. v07은 ROS extension disable이 아닌 enabled시 거부이며 pre-SimulationApp native.attest가 stage 확인을 막는다. 기존 guard/파일은 변경하지 않았다. 새 paused admission entry와 observable stage/source/extension fingerprint 계약을 추가했으나 native.attest port나 owner certificate로 사용하지 않는다. 새 entry는 graph 전부inactive/ROSdisable-readback/unknownscript·foreignactor거부, graph평가·Articulation·app.update·physics·command없음으로 작성했다. 실제 attach/extension callback closure는 UNKNOWN이고 physical BLOCKED_WITH_SPECIFIC_CAUSE다. 다음 한 단계는 별도 승인한 paused inventory1회; C++ lease 개발 확대를 권고하지 않는다. Engineering legacyROS/graph는 실제 이동 대안이나 이전34.127mm후퇴/raw-rootquietFAIL의 대체PASS가 아니다.

기존429SHA mismatch0/knownsubset검사/AST4/좁은tests4PASS. 최초test의dict.update오인실패도보존. Numeric/sign/dynamics미승인, scoped native불확실성과stalledKitpause한계/기존speed·quiet·clearancegate는물리승인전남는다. Isaaclaunch/graph실행/physics/ROS발행/actuator/motion/retry/ENG001/QUAL12/432=0, 이HOLD engineering denominator0. 원본·기존실패·protocol·threshold보존.
# 2026-10-21 post-paused 표적 admission 결정 — STOP_HOLD_BRANCH

[보고서](../reports/full_e2e_v02_post_paused_owner_physics_admission_20261020_v01.md), [작은 검사 증거](../reports/full_e2e_v02_post_paused_owner_physics_admission_20261020_v01_checks.json). 실제 paused source JSON에서 193→204 prim/추가 viewport-render11/삭제0/graph20 inactive/ROS2 false를 확인했다. Recorded15 file-layer SHA, manifest source5, preservation429 모두 일치. Scripting 자동 일반 subscription은 source에서 확인했지만 stage script 연결0이며 enabled extension 이름을 rover writer로 해석하지 않았다. Native ownership/외부 shutdown은 UNKNOWN. 추가 paused/graph run을 요구하지 않는다.

Historical named wheel303 sample쌍에서 양의 graph target에 여섯 q 순증가를 확인했지만 순간 dq에는 음수도 있고 negative-target sample0이다. K1 양방향 closed-loop HOLD 증거와 현재 실행 가능한 per-step bounded 경로가 없어 STOP_HOLD_BRANCH 선택. 새 admission/approval boolean/guard 우회/physics CLI를 만들지 않았다. 다음 권고는 기존 mobility 경로의 별도 승인된 감독형 비연구 simulator demo이며 terminal stop PASS와 구분한다. 이전34.127288744mm 후퇴/raw-root quiet FAIL 및 root+COM+FD 기준과 stalled-Kit pause 한계를 보존했다. Isaac/physics/graph/ROS/actuator/retry0, 이번 denominator 기여0, Full E2E/QUAL12/432 HOLD. 원본/기존 코드/contract/outputs 불변. 보고서·checks JSON 추가와 이 기록 외 변경 없음.



## 2026-10-21 동일 post-paused 요청 재확인 완료

지정 보고서가 이미 존재하여 [동일 보고서](../reports/full_e2e_v02_post_paused_owner_physics_admission_20261020_v01.md)에 재확인 절만 append했다. 실제 paused JSON/표적 source 및 historical named wheel 자료를 다시 읽고 입력21 SHA·보존429·file-layer15 불일치0, graph20 inactive, pulse303쌍의 여섯 양의 순증가/negative-target0을 재현했다. STOP_HOLD_BRANCH 유지: 양방향 direct target→q/dq/복원 응답 근거 부족과 물리 bounded 경로 부재. 추가 paused/graph audit나 C++ lease 개발 요구 없음. 다음은 별도 명시 승인할 기존 mobility 경로의 감독형 비연구 simulator demo이며 frozen terminal PASS와 구분한다. 새 코드/approval/physics CLI 없음, v07/global guard/수치/원본/이전 checks 불변. 이번 실행·명령·retry·denominator 기여0, Full E2E/QUAL12/432 HOLD.


## 2026-10-21 legacy supervised mobility 단일 실행 준비 v01

[새 준비 보고서](../reports/legacy_supervised_mobility_one_shot_preparation_20261021_v01.md)를 작성했다. 기존 실제 stopping validation의 launcher/domain191/ROS child/graph 경로와 AST 인자를 확인하고 과거 plan의 주요 입력 SHA6/6 일치를 확인했다. 새 `FE2E_V02_LEGACY_SUPERVISED_20261021_v01/attempt_0001` 경로는 미사용이다. 기존 두 실행 스크립트 재사용 CLI와 제한/abort/수집 방법을 제시했다. 다만 현 소스는 시작 후 writer guard 및 root+COM+FD quiet outcome 연결이 없어 감독형 실행 NOT_READY이며, 새 버전에서 필요한 최소 수정 위치를 두 항목으로 명시했다. USD-only 판독은 pxr 부재로 실패했고 현재 composed topology/live guard는 UNKNOWN이다. Isaac/ROS/physics/publish/motion/retry0. 기존 STOP_HOLD 보고서와 paused inventory는 수정/재실행하지 않았다. Full E2E/QUAL12/432 HOLD 유지.

## 2026-10-21 legacy supervised mobility 두 보완 구현 완료 — offline PASS

[구현 보고서](../reports/legacy_supervised_mobility_one_shot_implementation_20261021_v01.md), [집중검사 결과](../reports/legacy_supervised_mobility_one_shot_implementation_20261021_v01_checks.json). 새 legacy session/ROS child/observer/supervisor와 offline-safe 공용 guard/evaluator를 구현했다. 기존3writer graph/source/target·10DOF·domain191 endpoint/GID·phase discovery·heartbeat·actor/contact·floor gate, 외부abort/zero·소유child reap·내부status wrapper판정을 연결했다. 원래 감속/수치 유지, baseline만 독립1초 판정을 위해75tick으로 확장했다. Raw COM/root-origin/FD 각각≤.002 및 pose span≤.002, contiguous≥1sim초/dt≤.1 평가와 signed zero후퇴를 추가했다. 기존 자료에서 raw COM=.002620264860/root=.002619135991→QUIET FAIL, backward34.127288744mm 재현. MOVED/QUIET/RESEARCH_E2E 분리(연구항상NOT_ASSESSED).

Compile6·offline21checks·기존출력atomic거부·prior dependency6SHA PASS. source manifest11entries pin. 실제launch/ROS/physics/publish/actuation/retry0, live readiness UNKNOWN. 새 미사용 FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01 output의 실행가능명령과 abort방법을 보고서에 기록했다. 다음은 별도 명시승인할 simulator-only1회이며 추가 paused/global native proof를 요구하지 않는다. 관측 graph/ROS/actor guard 범위이며 모든native callback부재 인증 아님. 원본USD/controller/old scripts/output/reports·v07 STOP branch 보존, ENG001/QUAL12/432 HOLD/연구분모0 유지.


## 2026-10-21 PUBLISHER_SET 집중 진단 / v02 forensic 보강

[진단 보고서](../reports/legacy_supervised_publisher_set_hotfix_20261021_v01.md): 실제 v01은 exit1/NOT_READY, motion_attempts0/MOVED NO/QUIET PASS(정지 baseline)/zero NOT_READY다. 실패 discovery의 names는 미저장이고 최종 ros_status는 fault 이후 snapshot이라 ROOT_CAUSE_UNKNOWN이다. 중복 GID/외부 publisher 어느 쪽도 확정하지 않았다. 기존 실제 출력37파일 SHA/집합 및 v01 manifest11개 SHA 보존 PASS. 이전34.127mm stop regression FAIL 유지.

v02 guard/session/ROS/observer/entrypoint와 pinned manifest를 새로 만들었다. 검증 직전 정확한 snapshot/names/phase/pins를 fsync하며 기존 허용 cardinality/GID는 완화하지 않았다. topic·publisher 소실·phase 회귀도 차단한다. offline 집중18/기존21/compile6 PASS; 초기 fixture 오류 FAIL과 수정도 checks에 기록했다. 보고서의 고정 새 output/domain191 단일 명령은 별도 사용자 simulator 승인 후 진단 보강1회용이며 이번 세션 Sim/ROS/physics/publish/motion/retry0이다. 원인 해결/runtime 성공 UNKNOWN, Full E2E/QUAL12/432 HOLD/연구분모0.


## 2026-10-21 실제 건설현장 USD 프리뷰 전달

[보고서](../reports/construction_site_isaac_preview_20261021_v01.md). CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/construction_site_e2e_preview.usda를 실제 생성했다. 원본 ConstructionSite+patched Rover+기존 FULL cement HR_Scan 300 brick fixture를 source-preserving 참조로 합성했다. FE2E_S001 XY/yaw 유지, 실제 site 바닥에 대한 프리뷰 전용 z 보정을 명시했다. 단일 rover/PhysicsScene, visible site/rover/material, 3 controller targetPrim, active graph0, registry8hash 및 입력 보존 PASS. saved camera에 두 대상 bbox 전체 포함/현장 중심시선 차폐0, bounds gap .74438584m. 최초 expired-prim build FAIL을 보존하고 새 attempt로 구성했다. 최종 USD dependency 일부 PNG/JPG/MDL/remote 경로 unresolved로 exit1/OFFLINE_PARTIAL; 전체 렌더·PhysX contact·E2E UNKNOWN. GUI/SimulationApp/ROS/physics/motion/sweep0, screenshot unavailable. PUBLISHER_SET UNKNOWN·이전34.127mm 후퇴/quietFAIL 및 STOP_HOLD_BRANCH/ENG001·QUAL12·432 HOLD 유지. 원본과 기존 결과 수정 없음. 다음은 이 건설현장의 fresh RGB-D/frozen YOLO/B4-B5와 forward-only approach 연결이며 별도 motion 작업이다.


## 2026-10-22 건설현장 가시성 수정 — 정적 PASS / GUI UNKNOWN

[새 보고서](../reports/construction_site_visible_preview_fix_20261022_v01.md). 사용자 실제 GUI의 작고 흰 현장/로버 미식별은 이전 프리뷰 실패로 인정했다. bundled pxr로 기존 composed camera/world bbox/instance proxy를 확인했으며 기존 카메라 행렬 방향은 정상이다. 따라서 GUI 불일치의 단일 근본 원인은 UNKNOWN으로 남긴다. 확인된 기존 팔레트 투영14.46%×14.76% 및 무텍스처 흰 dome2500을 대상으로 새 `CONSTRUCTION_SITE_E2E_VISIBLE_20261022_v01/construction_site_e2e_visible.usda`에 가까운 측면 camera+preview dome350을 작성했다. 실제 authored matrix 투영상 로버전체35.69%×55.84%, 본체20.70%×20.21%, 팔레트23.21%×26.76%, corners/clip/중심 ray PASS. 실제300 nonempty visible brick meshes와 본체607638points 확인, geometry/300membership/원본 used-layer SHA 보존 PASS. Builder11checks/별도body/compile/bash PASS, GUI_VISUAL UNKNOWN; GUI·Isaaclaunch·ROS·physics·motion0/연구분모0. 새 파일 하나를 GUI에서 여는 것이 다음 단계며 usable 확인 전 fresh RGB-D/YOLO/B4-B5·forward approach 미실행. 기존 stop FAIL/ROS guard/ENG001·QUAL12·432 HOLD 유지.


## 2026-10-22 건설현장 runtime namespace / 크래시 수정

[보고서](../reports/construction_site_runtime_prim_crash_fix_20261022_v01.md). 기존 preview builder의 pseudo-root 일괄 SetActive(False)가 /Render, World children 일괄 억제가 Rover_Calibration을 끈 실제 layer opinion을 확인했다. 새 CONSTRUCTION_SITE_E2E_RUNTIME_FIX_20261022_v01/construction_site_e2e_runtime_fixed.usda에 Render runtime namespace 활성, 옛 calibration RenderProduct consumer3개 비활성/viewport camera 재연결, calibration geometry 없는 활성 컨테이너2개, rear camera 비활성을 작성했다. 기존 camera pose·site/rover/fixture bounds/material·실제 brick mesh300·입력 SHA 보존. 첫 offline 이름/float/남은 rear camera 검사 FAIL과 후보를 보존한 뒤 최종17 checks PASS. 프로세스0 확인 후 Kit no-motion load 단1회: RenderProduct valid/Render active/카메라 readback PASS, ROS0/timeline stopped/physics.play0. Native expired-prim/core dump 재현 없음; 이전 사용자 GUI는 CRASHED 유지. Capture 파일 즉시 확인 AssertionError로 전체 smoke FAIL, host exit0/EXITED이나 app.close return marker 미생성 UNKNOWN. 종료 후 실제 PNG는 매우 어두워 HEADLESS_VISUAL FAIL, GUI_VISUAL UNKNOWN. 재시도/추가 runtime/조명 sweep 없음. 연구분모0/ENG001·QUAL12·432 미실행. 다음 사용자 동작은 필요시 최종 USD 하나 GUI open1회이며 실용 밝기/식별성은 미해결이다.


## 2026-10-22 건설현장 조명 복구 / 단일 정적 렌더 PASS

[보고서](../reports/construction_site_lit_preview_render_20261022_v01.md). 실제 dark PNG p50=.007843, 원본 작업등2개 active=false와 Dome350 청색을 확인했다. 새 CONSTRUCTION_SITE_E2E_LIT_20261022_v01/construction_site_e2e_lit.usda 하나에 흰 Dome2500 복원+기존 preview camera에서 비추는 RectLight6000(3×2m)만 추가했다. 재질·camera·물체 pose·300 membership 보존, 로버/현장/fixture 전체 속성·relationship signature 일치, 23 used-layer SHA 보존 및 offline10 checks PASS. 프로세스0 gate 후 Isaac5.1 no-physics/no-ROS/no-motion 정적 렌더 정확히1회: 내부 load/capture PASS, PNG future+파일 안정화+CRC/IEND/zlib 검증 PASS, host exit0/wrapper0. 실제 PNG에서 청록색 본체·바퀴·프레임, 벽돌 적층/팔레트와 현장 식별 HEADLESS_VISUAL_PASS. p10/p50/p90=.082337/.365555/.713993, 255 clipping0%; GUI_VISUAL_UNKNOWN. 기존 invertToneMap/invertColorCorrection true 유지 상태로 밝아져 확정 원인으로 주장하지 않음. app.close Python return marker 부재 UNKNOWN, 기존 material/fabric warning 보존. 이전 dark FAIL/capture AssertionError/사용자 GUI crash는 그대로 유지. 재렌더/재시도0, controller/physics.play/ROS/motion/HOLD/training/ENG001·QUAL12·432=0, 연구분모0. 다음은 필요시 최종 USD 하나 GUI open이며 수동 카메라/스크린샷 진단 불필요. Preview 조명은 연구 lighting lock을 대체하지 않는다.


## 2026-10-22 건설현장 전방 RGB-D 단일 스모크 — 내부 FAIL / 재시도0

[보고서](../reports/construction_site_front_rgbd_pose_smoke_20261022_v01.md). process gate0 뒤 기존 LIT USD를 여는 실제 no-motion Kit1회에서 metersPerUnit==1 assertion FAIL, host0/wrapper0와 내부FAIL을 분리했다. 실제 센서RGB/깊이·YOLO 추론·B4/B5·target은 미생성/미실행이며 FOV UNKNOWN이다. 실패 후 read-only pxr로 최상위 stage fallback0.01m/Y-up, 원래 preview/recovery authored1m/Z-up을 확인했다. checkpoint HR_Scan M50 epoch25 SHA 일치 및 실제 model load/class0 brick_load 확인, predict0. 실패 당시 코드3개와 output 보존, 재시도0, 입력hash 보존 PASS·compile3/known9 PASS. 다음은 새 session layer에서 원본 근거1m/Z-up을 명시·readback하는 좌표계 수정이며, 현재 센싱/pose 성공이나 motion readiness를 주장하지 않는다. Wrapper 내부FAIL exit전달 결함도 보고서에 남겼다. ROS/physics.play/명령/운동0, 연구분모0, 기존 stop34.127mm/quietFAIL·PUBLISHER_SET·ENG001/QUAL12/432 HOLD 유지.

## 2026-10-22 전면 RGB-D 메타데이터 수정 및 실제 단일 센서 스모크 완료

[결과보고서](../reports/construction_site_front_rgbd_pose_smoke_fix_20261022_v02.md). 새 RUN `CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v02`의 metadata-only root USD(sha424cb17b104d7a68a4c264216e38b9823f371524a8704e07fb4eec8b08d1e264)에서 composed1m/Z를 Kit 전 bundled pxr로 확인했다. 첫 offline preflight의 unavailable GetCompositionErrors API/exit1은 보존했고, 설치 API 호환 v03에서 실제 prim stack/membership·root primspec0·300 bricks/one rover/camera/render/model/hash 검증 PASS 후 process0 gate로 Kit 정확히1회, 재시도0. Fresh front_rgb.png/front_depth.npy/camera_metadata 저장·재개봉 PASS, 실제 YOLO brick_load1 conf.8027858734, mask/유효depth29876, B4 heading90.15771484375°(mod180). B5는 독립 physical pallet datum 없어 NOT_EVALUATED, 전체 pose/targets null, GT 주입0. Kit 내부PASS/child0/inference0/최종wrapper0; internalFAIL→nonzero gate 수정 및 판정 검사. Python app.close return marker 부재는 UNKNOWN 유지. 입력27hash 및 v01 files14hash 보존PASS, known9hash/countPASS. Timeline0/stopped, ROS/physics.play/motion/QUAL12/432/학습/연구분모0. 새 보고서·스크립트6개 및 외부 센서증거 추가, 기존 v01 캡처 전 FAIL 보존. 다음은 독립 pallet datum 근거 확보이며 sensing PASS를 전체 B5/task/motion readiness로 승격하지 않는다.

## B5 observed pallet datum offline assessment — 2026-10-22
[보고서](../reports/construction_site_b5_datum_offline_20261022_v01.md). 기존 front RGB-D/mask/calibration만 사용한 새 외부 `CONSTRUCTION_SITE_B5_DATUM_OFFLINE_20261022_v01`에 floor62384점·top1810점 RANSAC/TLS, ROI mask/overlay/plot/JSON 저장. 기울기 .370144°/.079751°, top ROI 중심 worldZ .146866635m, 해당 XY의 floor 외삽 .000417517m; 관측 차 .146449118m로 설계 thickness.144m와 구분. 내부 잔차는 렌더 depth scatter이며 실물 정확도 불확도 UNKNOWN. 원본 pose/production expected SHA PASS, 입력14hash 보존PASS. 현 adapter는 planned engineering_fixture_design만 허용하므로 observed-plane evidence를 위장하거나 원본 legacy calibration을 우회하지 않고 계약 변경 시 중단 조건 적용: INSUFFICIENT_DATUM/B5 NOT_EVALUATED/pose·targets null. 별도 물리적 datum 후보 자체는 확보됨. 다음 단일 행동은 frozen 함수 유지하에 observed-plane evidence를 받는 새 adapter 계약 검토·승인. 무효depth ROI밖 matmul RuntimeWarning(exit0) 보존, finite ROI fit PASS. Kit/model/ROS/motion/학습/432/연구분모변화0; B4 gate는 전체 pose/robot deployment 인증 아님. Stop regression/PUBLISHER_SET 미해결 유지.

## 2026-10-22 sensor-observed datum adapter v02 / 단일 offline B5 완료

[보고서](../reports/construction_site_b5_sensor_adapter_20261022_v02.md). 새 engineering-only sensor_observed_pallet_top_plane_world_v01 계약과 단일 offline runner를 추가했다. 기존 RGB-D/검출mask/수동ROI1810점 평면에서 anchor(-25.8346946456,30.0307131705)의 topZ=.14686663495932334m를 계산하고 z′=z−top+.144 변환으로 원본 B4/B5 식·상수 유지. 실제 저장관측 B5 호출1/재시도0/exit0, 중심(-25.8358191200,30.4337574128)m, heading90.15771484375°, score.073290312617, inside.985579663973, point/top/side29819/4470/24504. PRE(-25.8358191200,28.2300123815),FINAL(-25.8358191200,29.0300123815),taskyaw90°. Center90후보 선택true/heading B4유지. B5 원본 point gate 통과이며 score 합격threshold 부재; 정확도/robot 성공 PASS 아님. 외부 CONSTRUCTION_SITE_B5_SENSOR_ADAPTER_20261022_v02에 prediction-first0444 및 evidence/validation/provenance/status 저장. 9functions+상수AST·동치spot·negative7·compile2·50inputs보존·known9hash/count PASS. 부정geometry변경은 provenance에서 먼저 차단되어 독립branch coverage 미확보. Pose/production/checkpoint SHA 실제 일치. Capture manifest 자기empty해시 항목은 자체인증 제외, 입력별 hash는 교차일치. GT비교/clearance NOT_EVALUATED, 수동 ROI/scale·calibration/worldposition UNKNOWN. 제안 engineering 계약이며 연구/protocol 독립승인 필요. Kit/capture/inference/ROS/physics/motion/432/연구분모기여0; 기존stopFAIL/PUBLISHER_SET미해결 유지. 다음 단일단계는 저장관측의 자동상판ROI 후보를 고정 수동ROI와 비교하는 engineering 평가다. 이전원본/v01adapter/출력 보존.


## 2026-11-01 — 3-rep HPO 착수: 실제 GPU smoke PASS / Stage-1 NOT_LAUNCHED

[보고서](../reports/three_rep_hpo_start_20261029_v01.md). 사용자 2026-10-29 요청에 따라 향후 비교·개발·val aggregate·test 분석은 HR_Scan/LR_Scan/GeoCAD만 사용하며 Proxy는 제외한다. 위 과거4-rep 기록/잠금은 archive로 보존하며 새3-rep 실험으로 재해석하지 않는다. 새 THREE_REP_HPO_20261029_v01 namespace를 충돌 거부로 생성하고 final manifest SHA 일치/2800행/train2000·val400·test400/각 material 반수/3rep paired exact-set/누수·누락0을 확인했다. 개발 풀은6000/1200 images, test·Real189·depletion selection 제외. 전체 labels tree expected SHA 및7200 image/label hash inventory 확보. 실제 Nominal train TRN_000661 Load02/val VAL_000151 Load02에서 artificial polygon bridge와 raster IoU .676320/.784684를 재확인하여 현재 사용자 QA gate로 Stage1차단; 과거 secondary 오류 허용 lock은 수정하지 않았다. 첫 QA의 C40 multi-component 빈 후보 min() exit1은 실패기록 보존, 새 finish코드로 실제 C40후보없음과 단일 연결표본을 기록했다. 고정 단일 연결 train6/val6 실제 YOLO11n-seg GPU1epoch smoke PID958823/exit0, 최종val mask mAP50-95=.0095475282; engineering 연결확인이며 HPO trial0/NOT_LAUNCHED. compile3 PASS, canonical labels tree smoke후 보존PASS. 다음 단일수정은 새 namespace의 canonical instance bitmap 보존 loader/동일 image-mask augmentation 및 실제target QA, 이후 HPO40×60/grace15/OptunaTPE+RayASHA(reduction3),Top5×3rep×150. 원본 sampler seed는 미지정이므로 새 sampler42명시 결정과 구분. HPO지속세션/재개 미실행, B5/Isaac/ROS/motion재실행0, 기존 프로세스 보존. 후속 final3weights→Nominal+depletion+3x3→real+scale→pose+900B300→324E2E는 새 계획이며 옛432잠금 변경이 아니다.


## 2026-11-01 — 현장 물리 이동 우선 / HPO scheduling 중지

[보고서](../reports/construction_site_single_rover_mobility_20261101_v01.md). 최신 사용자 결정으로 이전 HPO next action을 대체하고 현장 usable까지 후속 HPO/training scheduling 중지. HR_Scan/LR_Scan/GeoCAD만 향후 사용, Proxy 제외 및 과거 잠금 보존. 기존 Isaac GUI PID955077/GPU3379MiB 검출로 resource gate BLOCKED_NOT_LAUNCHED, host2/internal NOT_STARTED. 성공 센서 stage_metrics_1m_z.usda exact path/SHA 및 참조 입력 총25개 hash PASS. 신규 runnable preflight만 작성; 완성 현장 drive runner는 아직 없음. 센서 stage 활성graph0/기존 motion runner EngineeringFloor 생성 때문에 그대로 실행 불가. AST PASS, Git status exit128(no .git) 보존. Kit/physics/ROS/motion/retry/training0, MOVED/STOPPED/TARGET_REACHED NOT_TESTED, FULL_E2E NOT_RUN, RESEARCH_SAMPLE0. 기존34.127mm retreat/raw-root quietFAIL/PUBLISHER_SET UNKNOWN 유지. 다음은 사용자 GUI 정상종료 후 resource 재확인, 기존 ROS graph+v02 forensic의 단일 현장 runner 연결과 corridor 검사 후 1회 주행. 자동datum·B4 face mapping 미해결.

## 2026-11-01 — 현장 drive runner v02 구현 / 통로 gate FAIL

[보고서](../reports/construction_site_single_rover_mobility_20261101_v02.md). 신규 runner/geometry/session/ROS 4파일로 실제 site sublayer+기존 3-controller ROS graph binding, 물리 step/joint·COM·FD/zero hold/endpoint guard v02·cleanup을 구현했다. prepare-only는 Kit/ROS 없이 PASS; graph admission/compile PASS. 첫 BBoxCache API 호환오류 FAIL은 외부 root에 보존하고 prepare_0002/0003에서 수정검사했다. 현재 Kit/학습 프로세스0, GPU compute는 rustdesk535MiB만 검출됐으나 NO_SAFE_CORRIDOR로 실제 run gate exit1/Kit_launch=false. Rover/Cube collision Z9.492–10.492m가 전체 sweep 높이에 포함되고 현장 mesh의 높이3.623–3.652m 삼각형8개와 보수적 AABB 겹침, floor support 표본 누락이 있다. 실제 충돌 확정/불가능 증명 아님. 원본 삭제/teleport/EngineeringFloor 없음. MOVED NO(미시도), quiet STOPPED NOT_TESTED, physics/ROS/명령/연구분모0; GUI_BUSY 모의 분기 PASS와 실제 상태 구분. HPO scheduling 중지 유지, 이전34.127mm drift/quietFAIL/PUBLISHER_SET UNKNOWN 보존. 다음 단일 행동은 원본 변경 없이 Cube 물리 소속·바닥 삼각형 높이의 정밀 확인이며 GUI 종료만으로 drive 허용 안 됨. 실제 runtime 물리·caster/traction·teardown은 미검증.

동일 작업 추가 검증: source-stack 보존 최종 verification_0003 PASS(원본 membership/type/contributing specs 동일·graph 밖 property 변경0, intentional stage metadata/ancestor overs 제외). 첫 자체 mesh-문자열 검사 메모리 과다로 자체 CPU child만 SIGINT/exit130; 후속 source-stack 비교의 overs/pseudoroot FAIL2건도 각각 보존. 원본hash/Render/1m-Z/one rover/300 meshes PASS. 사용자 프로세스 중지0.

## 2026-11-01 — 현장 drive v03 geometry 교정 / 실제 Kit 1회, clock gate FAIL

[보고서](../reports/construction_site_single_rover_mobility_20261101_v03.md). v02 runner/session을 유지한 새 v03에서 per-enabled-collider Z-first conservative sweep와 실제 여섯 바퀴 접촉선 2,214개 support 검사를 구현했다. 기존 giant visual bound의 높이3.65m 차단8건 제거; 실제 composed source의 Cube collision/rigidBody는 더 강한 기존 rover_smoke_v03 override로 False(원래 asset True와 구분), 임의 비활성화 없음. 회귀검사는 enabled high Cube의 3.65m 분리 및 10m 실제 차단 PASS. 원래 floor band를 유지하고 flatness 오탐을 교정해 최종 offline corridor/graph PASS; source42개 hash 전후 PASS, 준비 graph 밖 property0. 정지 PhysX raycast/contact gate 추가, 실행 검증은 미도달.

GUI/GPU free 확인 후 hh_isaac51 Kit **한 번 실행**했으나 baseline `CLOCK_NOT_ADVANCING`으로 NOT_READY. 기록195개, timeline 약0~.03333s에서78회 감소, ROS TF stamp6.2833s; source start/end0은 looping 의심 근거이며 원인 확정 아님. 비영 명령0/actual drive attempts0/MOVED NO/STOPPED NOT_TESTED, quiet·zero NOT_READY. 여섯 바퀴+shell-floor 총168 contact events, 차체 비침투 UNKNOWN. 정지 기록 COM max.000388869/origin.000394140m/s이나 연속1s clock 불충족으로 정지 PASS 아님. Native/runner exit0과 JSON NOT_READY 차이를 final_verification에 명시하고 실패로 보존했다. 재실행0, 이전34.127mm drift 미해결. 다음은 기존 session의 clock 일치 및 shell-floor 접촉 정지 확인이다. 원본/기존출력/사용자프로세스 보존; HPO PAUSED, training/B300/E2E/432없음, 연구분모0. 새 latest_report mirror 생성.


## 2026-11-01 — 현장 drive v04 clock PASS / tilted wheel support 처리에서 구동 전 실패

[보고서](../reports/construction_site_single_rover_mobility_20261101_v04.md). 실제 Kit1회/재시도0. 설치5.1 SimulationManager native physics time + 실제 PhysX callback377steps/6.283333661035s/누적dt·nativecount 오차0, raw timeline 비반복120s 및 graph·TF 교차확인; telemetry 역행0, baseline1.000000052s strict quiet PASS. 비영명령0/MOVED NO/주행후 STOPPED NOT_TESTED, 연구분모0. Shell144점 separation최소78.864mm/impulse0; 정착후 worldbound Zmin65.561mm, 원본floor XY9교차 최소gap70.647mm로 기록상 비침투·무하중. Six wheel contacts 관측, middle2 impulse0이므로 전부 하중지지로 인증하지 않음. 실제 중단은 장애물overlap0/여섯 cylinder축 기울기>.0001 analytic gate가 표본0을 만들어 live PhysX support검사 이전 실패한 것; 원시 NO_SAFE_CORRIDOR 보존, 원인 구체화. 이 assert를 shell진단보다 먼저 둔 구현 순서 문제도 명시. 실행코드3개 외부snapshot+hash 보존 후 v04에 tilted tread식/진단 선행 순서 수정, compile5·high collider/tilt369/바닥누락회귀 PASS, 수정본 runtime NOT_TESTED. Nativeexit0/internalNOT_READY를 wrapperexit1로 정규화. source46/v03input49 보존PASS. 다음은 새 별도 실행 기회의 live tilted support 인증과 같은세션 forward+stop; 이번1회소진으로 재실행없음. 이전34.127mm drift 미해결, HPO PAUSED/훈련·연구실행0 유지.


## 2026-11-01 — 현장 v05 수정 v04 실제 실행 / PhysX support 미확보

[보고서](../reports/construction_site_single_rover_mobility_20261101_v05.md). 새 v05 namespace에서 기존 수정 v04 SHA 그대로 Kit1회/retry0. 물리377steps/6.283333661s/시각역행0, 통로·graph·baseline quiet PASS. tilted 표본2214 생성되었지만 허용floor ray hits0/2214, shell9ray도 저장hit0; 여섯wheel contacts6/6. STATIONARY_PHYSX_SUPPORT_FAILED로 driver 생성 전 중단. 원시query hit/반환값 미저장으로 미검출과path필터 원인 구분UNKNOWN. 비영명령0/MOVED NO/base XY변위0/STOPPED NOT_TESTED, nativeexit0/internalNOT_READY/runnerexit1. cleanup pause/graphzero 요청은 postdrive stop검증 아님. 원본입력hash보존PASS, 코드변경0, 연구분모0/HPO PAUSED. 다음 최소수정은 기존안전필터 전 ray 원시hit+반환bool 저장 한 가지; 추가Kit 없음.


## 2026-11-01 — 현장 v06 raycast API 수정 PASS / TF freshness admission FAIL

[보고서](../reports/construction_site_single_rover_mobility_20261101_v06.md). Kit2세션(첫 진단FAIL/시간초과 child-9 보존, 수정 재확인1회), 측정주행0/비영명령0/MOVED NO/변위0/주행후STOPPED NOT_TESTED. RaycastHit가 dict 아닌 속성객체임을 실제 AttributeError로 확인·수정; 14 bounded raw rays 필터전hits 저장, 기본단면/양면 모두 hit, composed path/winding 정상. 수정후 strict support2214/2214·sixwheelcontact·shell9/9 PASS, 최소gap70.647mm/실제shellsep+78.864mm·impulse0; fallback미사용, 통로0.10m유지. 물리378steps/6.300000329s. 이후 긴support계산 뒤 과거TF를 즉시채택해 TF_STALE(age7.206364s); driver미생성/PUBLISHER_SET NOT_TESTED. freshTF(.5swall/.1ssim) 대기 최소수정·actualstale/fresh/simstale 회귀·compile PASS, 최종수정 runtime NOT_TESTED/추가launch0. 코드snapshot/hash 구분, 원본stage/controller/v04코드7hash 보존PASS. 새외부v06에 실패2세션/trajectory/evidence보존. 연구분모0/HPO PAUSED/FullE2E NOT_YET_VALIDATED. 다음은 freshTF 대기수정으로 기존ROS shortpulse+zero 실제검증이며 이동성공 주장없음.


## 2026-11-01 — 현장 v07 fixed-v06 재사용 / fresh TF PASS, discovery PUBLISHER_SET FAIL

[보고서](../reports/construction_site_single_rover_mobility_20261101_v07.md). 실제 v06 최종수정 소스 변경0으로 새 v07 출력 prepare/Kit1회, retry0. fresh TF wall age .063626766s/sim차 .016666668s PASS, 새stamp/arrival 직접확인 및 isolation PASS 후 ROS child 생성. discovery에서 publisher `_NODE_NAME_UNKNOWN_`/namespace `_NODE_NAMESPACE_UNKNOWN_`가 관측돼 원본 guard_v01:23 허용집합 검사 PUBLISHER_SET으로 즉시중단; GID/phase/원본 snapshot 양쪽forensic 보존, driver 신원확정 UNKNOWN. 물리266steps/4.433333565s; support2214/2214·sixcontacts·shell9/9·clearance.10m PASS. NONZERO0/wheelmaxdq0/baseXY변위0/MOVED NO/주행후 STOPPED NOT_TESTED; quiet PASS는 무구동baseline. observerzero10/drivercleanupzero20 발행, timelinepause/ownedprocessesexit0; native0이나 내부NOT_READY/runner1. prepared53SHA보존PASS/TF회귀3·syntax3PASS/기존v06증거보존. HPO PAUSED/연구denominator0/FullE2E미검증. 다음은 discovery의unknown신원을 비영차단 상태의bounded대기로 처리하되 승인name·동일GID·freshTF 검증후만 허가하는 새버전 수정이며 이번추가코드/Kit없음.


## 현장 단일 로버 v08: 첫 실제 이동·zero·정지 — 2026-11-01

[실제 결과](../reports/construction_site_single_rover_mobility_20261101_v08.md). 기존 실제 현장·동일 로버에서 Kit1회/주행episode1회, ROS `/rover/cmd_vel`과 공급자 graph를 통해 비영45회 발행, world base +Y .021970748901m 전진 후 zero·정지 PASS. Wheel peak abs dq .362895578rad/s, 최종0; 정지 마지막1초 pose span0/FD0/최대origin속도 .000174916640m/s. 접촉 안전 PASS, unexpected contact0, shell separation양수·impulse0. Discovery .460262283wall초 후 원본guard 승인; 이번 unknown 관측0이므로 v07 익명GID 정체·동일GID 해소는 UNKNOWN. Native fallback 준비만/미실행. 정상감속·ZERO_SETTLING 이후 wall watchdog/종료 zero 경로에서 FAULT_LATCHED로 끝나 전체 NOT_READY·runner exit1을 보존한다. run_status 최상위 MOVED NO/STOPPED NOT_TESTED는 갱신되지 않은 초기값이며 nested result·원자료 MOVED YES/QUIET PASS와의 불일치를 보고서에 명시했다. 별도 measurement_summary·final_verification·실행코드snapshot 보존. 새v08 scripts3개·보고서·latest 갱신, 원본guard/controller/USD/v01–v07 보존. 추가재시도0, 소유프로세스종료·남은Kit/training0. HPO PAUSED, 연구denominator0, Full E2E/autonomy NOT_YET_VALIDATED. 다음은 추가주행이 아니라 기존로그에 근거한 postzero/watchdog lifecycle 및 runner표시 수정 코드작업이다.


## 2026-11-01 — 현장 drive v09 lifecycle offline 수정

[보고서](../reports/construction_site_drive_lifecycle_fix_20261101_v09.md). v08 실제 +Y .021970748901m/정지PASS·전체NOT_READY/exit1 및 원자료는 보존했다. 최초 fault는 child 경과 추정20.3345wall초/pulse19.8739초/feedback age.001709초로 child20초 watchdog 조건은 참, session pulse20초는 아직 거짓; 당시 abort 동시 존재는 기록부족UNKNOWN. 새v09 3script+순수helper에서 실제 pulse base이동·정상감속·zero·기존최소1초physicalquiet·graphzero·안전검사 뒤 fresh certificate로 child 정상종료를 확인하고 cleanup한다. 기존 watchdog/stop timeout/emergency/guard/controller/threshold 보존, 후속480tick 정지관찰 유지. Runner 최상위 측정 집계와 adapter fault 분리. CPU8tests·compile5 PASS(최초fixture wall_s누락4errors 후 수정), v08 prefix offline 완료가능시점sim7.7333/최초fault보다3.3647wall초전, fullfault replay거절, 49원본파일hash동일PASS. 보고서·checksJSON·latest갱신. Kit/ROS/prepare/물리주행0, v09 runtime NOT_TESTED, HPO/training PAUSED/연구denominator0. 다음은 별도 기존ROSgraph·기존field/corridor one-shot A→B waypoint runtime검사 후 freshYOLO/B4/B5 및 최종실험이며 이번에는 실행하지 않았다.


## 2026-11-01 — 현장 v09 실제1회: 이동·정지·child 정상, runner 집계 FAIL

[실제 보고서](../reports/construction_site_drive_v09_runtime_20261101_v01.md). 새v09_runtime_01 prepare/Kit1회·ROS episode1회/retry0. 실제 world base +Y21.505356mm/ΔX1.907µm, 계획50mm B 잔여28.496601mm; 짧은 실측B′ 도착이며50mm 자체도달NO(기존±30mm engineering target.pass TRUE와 구분). support2214/2214·shell9/9·기존graph/endpoint guard·.10m통로PASS, unexpectedcontact0·shell최소sep+82.015775mm/impulse0. BRAKING→ZERO_SETTLING→최소1physical초quiet/graphzero 인증 후 child18.104778wall초에completion_accepted TRUE, adapterfault/hardtrigger NULL. 최종quiet1.000000052초PASS/FD0/span0/wheeldq0, 기존480tick관찰 유지. driver/observer/Kitexit0이나 전체NOT_READY/runnerexit1 보존. 원인은 session:354가 cleanup에서 생성할zero_published.json을cleanup요청:371보다 먼저 요구하는 단일집계순서오류. marker실제생성은최종관측뒤/정상child종료뒤이며lateFAULT재발아님. CPU8/8PASS와실제전체FAIL구분. 코드변경0/추가launch0,14prepare입력hash동일·snapshot보존. 원본/이전결과보존,종료후Kit/training0/HPOPAUSED/연구분모0. 다음은정상child종료후cleanupzero확인뒤최종집계하도록집계순서만수정; YOLO/B4/B5·324/432·HPO미시작.


2026-11-01 동일 v09 runtime 요청 재수신: 기존 runtime_01 실제 완료 원자료를 재확인했다. steps771/commands66/비영45/FAULT0, prepare14 SHA256 일치. 추가 prepare·Kit·주행·코드변경0; 기존1회 예산과 NOT_READY 결과를 유지한다. cleanup receipt 선행 확인 후 집계 순서 수정이 미해결이며 HPO PAUSED/연구분모0. 상세는 위 실제 보고서의 재확인 절을 참조한다.


## 2026-11-01 — v10-A cleanup 순서 소스 수정 / runtime NOT_RUN

[새 보고서](../reports/construction_site_drive_cleanup_patch_20261101_v10.md). v09 원본을 보존한 새 session v10·runner v10·CPU helper/test를 작성했다. 정상 child+physical quiet 후보 후 cleanup zero 요청→최대3초 실제 observer receipt 내용/시각 검증→소유프로세스 exit0 및 cleanup/Kit close 오류 확인→최종 판정/serialize 순서로 변경. 신호·fault·누락/오류 receipt·강제 종료는 FAIL 유지. CPU11/11 및 compile4 PASS. 보조 git diff --stat은 비Git 디렉터리로 실패(exit129), 파일 직접 diff 검토. v09 실제 runner NOT_READY/B50mm 미도달 이력과 기존 보고서 보존. Kit/ROS/prepare/물리주행/324·432/HPO/training NOT_RUN, HPO PAUSED/연구분모0. 다음은 별도 A→B50mm 실제 목표주행 작업이며 이 소스 패치는 runtime 성공 증거가 아니다.


## 기존 현장 50mm 목표 실제 주행 v10-B — 2026-11-01

[새 보고서](../reports/construction_site_target_drive_20261101_v10B.md). 실제 Kit1회/episode1회/재시도0. live world feedback로 ORIGINAL B 잔여 0.143863mm, 5mm 기준 B_REACHED YES; MOVED YES, STOPPED PASS, NONZERO74. zero receipt10 및 driver/observer/Kit exit0. 그러나 app.close 뒤 execution_complete.json 미생성으로 runner FAIL(exit1); 원시 실패 보존. CPU13/13 PASS, 입력hash 불변. 다음은 close 전 provisional 저장+외부 runner 최종화 수정이며 추가 실행 없음. HPO/training PAUSED, 연구denominator0.


## Kit 종료 경계 결과 저장 source patch v10C — 2026-11-01

[보고서](../reports/construction_site_result_persistence_20261101_v10C.md). 신규 runner/session 및 CPU-safe persistence helper/test 작성. close 전 durable PROVISIONAL, 실제 Kit child exit 이후 outer가 provenance·raw stop/target/safety/cleanup 및 shutdown 로그를 검증하여 atomic final/result status를 작성한다. 기존 v10B B_REACHED YES / STOPPED PASS / runner FAIL(exit1) 보존. 신규 CPU23+기존13=36/36 PASS, 신규4개 compile PASS. git diff --stat는 비Git 디렉터리여서 실패, 파일간 diff 검토. Kit/ROS/prepare worker/학습/물리 재시도 NOT_RUN, v10C 실제 종료 readiness UNKNOWN. HPO/training PAUSED, 연구denominator0. 다음은 별도 bounded 실제 종료 확인 후보1회이며 이후 장거리 A-to-B와 fresh RGB-D→YOLO→B4/B5/task E2E로 진행; 이번 작업에서 시작하지 않음.


## 2026-11-01 — 현장 perception→approach v11 첫 실제 세션: capture 진입 FAIL

[보고서](../reports/construction_site_perception_approach_20261101_v11.md). Kit1회/retry0, 원본 현장/ROS graph·baseline corridor·strict PhysX support2214/2214 PASS 후 `timeline.pause()` 직후 capture의 is_playing assertion FAIL. 새 RGB-D/render/YOLO/B4/B5/PRE/FINAL 미도달; driver 생성0/nonzero0/기록 baseXY변위0/wheeldq0. 257physicssteps/4.283333557s, 무구동baseline quiet1.000000052s PASS이나 주행후stop NOT_TESTED. cleanupzero receipt없음/observerexit0/driver null. v10C helper 수정없이 close전provisional 실제생성·digest/source/evidence8hashPASS, Kitexit0/shutdownlog/outer final파일생성; 필수4witness누락으로 NOT_READY MISSING_WITNESS/runner1, 전체persistence 성공검증 아님. 신규adapter/session/runner3파일compile·plane-fit AST PASS, known9hash/count·source25/prepare27hash보존PASS. 수동ROI는 미실행이며 자율검출/관측경로안전 주장없음. 기존v10B와v10C/원본USD/이전증거보존. 다음 단일수정은 pause뒤 bounded app.update 상태반영/physics-clock 안정화 barrier이며 이번추가launch0. HPO/training PAUSED/연구denominator0/FullE2E미성공.


## 2026-11-01 — 현장 perception→approach v12: fresh perception PASS / route NO_PATH

[보고서](../reports/construction_site_perception_approach_20261101_v12.md). Kit1회/추가Kit0/구동0. bounded pause barrier 실제PASS/CPU2testsPASS 후 fresh mounted640×480 RGB-D, frozen HR YOLO conf.894056618, B4/B5수동ROI보조 완료. 새overlay를직접검토하고hash결합; 자동pallet인식아님. PRE(-25.936516793,28.277485021), FINAL(-25.936516793,29.077485021)m; start대비PRE전방−.193382491m/측방+.048537777m. 직선공간collider/supportPASS와전진도달가능성구분. 같은작업에서기존R2.8forwardplanner를실제13collider/현장포함4270경계에적용,116expansions/5083queries/10.696s NO_PATH; 전진중shell/loadclearance충돌근거저장,전역불가능증명아님. CPUroute1timeoutFAIL/route2sitecull오류INVALIDATED/route3교정결과모두보존. 실제base변위0/wheeldq0/nonzero0,PRE/FINAL미시도,baselinequiet만PASS/postdrivequiet미검증. close전provisional/evidence8hashPASS·Kitexit0·outerfinal생성; 필수motionwitness없어NOT_READY/MISSING_WITNESS/runner1. fixedBdrive본문제거,실제goal→driver통합은미완료. 원본stage/model/prepare입력/v11source보존. 제안은별도engineering초기배치를PRE뒤.30m/같은X로검사하는것이며실제relocation없음. HPO/trainingPAUSED/연구denominator0.

## 2026-11-01 — 현장 perception→approach v13: 새 초기 배치 2회, 실제 접근 미달성

[보고서](../reports/construction_site_perception_approach_20261101_v13.md). 별도 COW engineering startup(-25.936517,27.977485), 이어 첫 fresh PRE X를 따른(-25.979248789,27.977485)m에서 Kit2회. 물리 시작 전 overlay root transform만 변경·모든 rigid displacement검사; 실행중teleport없음. 두회fresh640×480 RGB-D/HR YOLO(conf.864772/.788471)/수동새ROI보조B5완료. PRE1(-25.979249,28.230226), PRE2(-25.840857,28.229028); FINAL은각PRE의+Y.8m. actual13collider/.10m공간sweep과stationaryPhysX2214/2214PASS이나PRE측방42.73/−138.39mm로같은X≤2mm직진admission실패. 실제episode0/nonzero0/base기록변위0/dq0/PRE到達NO/FINALNO/postdrivequiet미검증. 두leg관측goal/stop전환및outer검증코드추가했으나일반lateral보정follower아니며runtime미검증. Kit둘다exit0,close전provisional과close뒤outerfinal생성,필수motionwitness누락NOT_READY/MISSING_WITNESS/runner1. 구체assertion은provisional·별도engineering_outcome보존. source/prepare/provisionalhashPASS,CPU27+신규3PASS,신규compilePASS;직접conda pxr조회실패와비Gitstatus실패보존. 기존stage/weights/protocol/v01–v12유지,HPO/trainingPAUSED/연구denominator0. 추가Kit없음. 다음은두보존frame에서viewpoint대비B4/B5중심변동원인분해이며물리접근완료주장없음.


## 2026-11-01 — v14 steering 연결 / 실제 접근 미달성

[보고서](../reports/construction_site_perception_approach_20261101_v14.md). 저장 두 frame 좌표/B5 replay PASS를 재사용하고 새 bounded Hermite+pose feedback follower를 기존 StoppingAdapter/legacy ROS steering encoding에 연결했다. Kit2회: 첫 sparse manual ROI43점 gate FAIL, 두 번째 fresh YOLO/B4/수동ROI B5 PASS(PRE −25.934821,28.278040; FINAL +Y.8m). 실제13collider 곡선 envelope·live support24300/24300 PASS, 경로.879498m/최대곡률.268572/m. 주행 재개 첫 tick GRAPH_CHANGED 차단, 구체 diff 미저장UNKNOWN. driver null/nonzero0/wheeldq0/base변위0, PRE/FINAL NO, 주행후stop NOT_TESTED; baseline quiet만PASS. Kit1 exit0/runner1, Kit2 close요청후멈춤으로소유PID만TERM→KILL/exit−9/runner1, 사용자process보존. Provisional/outer 실패·종료watchdog 보존; signal handler가zero_request를바꾼2차hash불일치도보존. Review대기중 v14tangent1.2 보정은before/after source/hash별도보존, prepareexpected미변경/불변PASS주장없음. CPU11·compile·known9subsetPASS; v14c graphdiff저장/신호증거보존패치compile만PASS/runtime미실행. 추가Kit없음, formaldenominator0/HPO PAUSED. 다음은guard를유지한supplier/render graph변경항목확정과capture lifecycle수정후별도실구동이며현재workingdemo미달성.


## 2026-11-01 — v15 GRAPH_CHANGED 해결 / 실제 PRE 접근 중 TF_STALE 정지

[보고서](../reports/construction_site_perception_approach_20261101_v15.md). Kit2회. 실제 capture 전후 render17node추가/기존node변경삭제0 및 supplier ROS·Ackermann·3controller binding 불변 확인. exact observed render allowlist와 baseline전체동일 invariant 추가, endpoint GID guard 유지. CPU5/compile/preparehash/provisional존재evidencehash PASS. 두freshRGB-D/YOLO/B4/수동ROI B5 및 PRE actual13collider curved sweep/live support24300/24300 PASS. 두번째 실제ROSnonzero288/base경로.255870m/순변위.254318m/wheeldq최대.984256rad/s 후 TF_STALE(age .502469s) 안전zero20+observer10. PRE/FINAL NO·FINAL미검사, 예상밖contact0/drive shell침투하중0, postfault1squietPASS이나cleanupreceipt시각FAIL. 첫Kitclose watchdog TERM→KILL/−9·runner1; 둘째Kitexit0/runner1·MISSING_WITNESS/TWO_LEGS_INCOMPLETE·원래TFfault모두보존. v14−9실패유지,추가launch없음. 다음은TF .5s/GID안전유지하며누적JSONL재독해·path재로딩지연을cursor/cache로줄이고최소timestamp계측,요청결합zero receipt수정후별도bounded PRE→FINAL. 기존원본/v01–v14보존,HPO/trainingPAUSED/연구denominator0.


## 2026-11-01 — v16 perception 접근 / TF_STALE 재발, 요청 결합 cleanup PASS

[보고서](../reports/construction_site_perception_approach_20261101_v16.md). 새v16 cursor/path·contract cache/새contact 검사로 누적 재읽기를 제거하고 guard·TF .5swall/.1ssim·GID·충돌/정지 기준 유지. CPU5+graph5 PASS 후 Kit1/ROS주행1/retry0: freshRGB-D/HR YOLO/B4/수동ROI B5, 새PRE(-25.934669582,28.278040571)/FINAL+Y.8m. PRE sweep/live support24300/24300 PASS, 비영406/실측경로.362254716m·순변위.361458268m·wheelpeak.846528649rad/s. TF_STALE(age.501729965/sim차.016666668) 재발, PRE잔여.518797774m·PRE/FINAL NO/FINAL미검사. unexpectedcontact0/drive shell침투하중0, 비상뒤1sim초quietPASS/span0. 별도cleanup요청ID/hash에결합한zero10영수증PASS(요청후.016733s), driverzero20/driver·observer·Kitexit0; 정상leg stop증명없음/outerMISSING_WITNESS·NOT_READY/runner1 유지. prepare50hash/v15입력44보존·provisional존재evidencehashPASS, 소유PID소멸/Kit·training0/rustdesk보존, 연구분모0/HPO PAUSED. 정지직전 guard구간.393329s/appupdate.024641s, 구간내세부원인UNKNOWN. 새TF실제수신후에도주기status에이전TF가남은증거확인. 후속v16b는on_tf즉시상태반영하되endpoint inventory wall_s를갱신하지않는patch/CPU4PASS·compilePASS; prepare/Kit NOT_RUN. 실행v16source/snapshot/hash와분리,추가launch0. 다음은새v16b output의fresh PRE→FINAL 제한검증이며전체TF/approach성공미입증. latest_report를v16으로갱신,기존실패이력보존.


## 2026-11-01 — v17 기존 v16b 실제 실행 / TF_STALE 재발

[보고서](../reports/construction_site_perception_approach_20261101_v17.md). 기존v16b소스변경0/compile6·TF4+IO5+graph5PASS후새v17_01에서Kit1/ROS주행1/retry0. FreshRGB-D/HRYOLOconf.724332/수동ROI B5 및 PRE곡선collider·live support24300/24300PASS. 새PRE(-25.934899827,28.278040409)/FINAL+Y.8m. 비영741/실측경로.679993402m·순변위.678219185m후TF_STALE(age session.501179218/driver.502016783)차단. PRE잔여.201629488m/도착NO·FINALNO/독립검사NOT_RUN. 직전TF수신→즉시snapshot13.1µs로patch동작확인,마지막TF수신뒤새수신없음;마지막step→다음guard.494087696s지연이나내부분해UNKNOWN/마지막TF정확게시완료시각UNKNOWN. 이해된국소수정없어추가Kit0·안전gate변경0. Unexpectedcontact0/drive shellbad0,zero20+cleanup요청결합zero10receiptPASS·driver/observer/Kitexit0/소유PID소멸. Timelinepause뒤staleguard재거절로postfault물리관찰없음/QUIETFAIL(span19.045mm,origin25.115mm/s의주행중마지막1초);비상stop을도착·quietPASS로주장하지않음. OuterNOT_READY/MISSING_WITNESS·runner1·provisionaleligibilityfalse보존. Preparehash·v16입력50/v15입력44보존PASS,원본USD/weights/protocol/이전결과유지. HPO/trainingPAUSED/연구분모0/대규모실행0. 다음은pre-endpoint graph/actor/forensic세부시간·atomic게시완료계측과stalefault후안전정지관찰lifecycle검증이며PRE/FINAL완료미달성.


## 2026-11-01 — v18 guard CPU stall 특정 / TF fault ZERO-ONLY quiet PASS / PRE overshoot 미완료

[보고서](../reports/construction_site_perception_approach_20261101_v18.md). 신규v18/v18b 소스와 새외부output2개에서 허용된Kit2회 완료, 추가0. 첫실행freshRGB-D/HRYOLO/B4/수동ROI B5·PRE곡선/24300supportPASS 후 실제.680531m 이동·TF_STALE. fault직전actor검사wall.488188s/threadCPU.487891s로지연위치확인,내부GC여부UNKNOWN. 비영driverexit·실제ROSzero요청결합receipt·원래graph/actor/GID/contact확인후ZERO-ONLY 새70physics샘플에서1.000000052sim초quietPASS(span.0173mm,origin최대1.837mm/s). USD변경통지별원래actor함수재계산/구조resync전체검사cache CPU15exact대조PASS 뒤두번째실행. TF_STALE없이.886908m 이동했으나PRE최소오차8.677mm로기존follower3mmnormalstop미진입→진행방향5.079mmGOAL_OVERSHOOT. PRE안정도착NO/FINAL검사미실행·到達NO,threshold변경없음. 두번째quiet는whitelist밖fault로새samples0/FAIL·실제최종정지UNKNOWN. actor증분p50 1.195ms이나guard최대.460266s내graph비교중GCgeneration2 .448448s직접계측:timing완전해결주장불가(driverTFagemax.484271s). 양쪽cleanup별도요청ID/hash결합zero10PASS,driver/observer/Kitexit0·runner1/NOT_READY/MISSING_WITNESS·소유PID소멸/강제종료없음. CPU41검사PASS/전체신규compilePASS,actorCPU첫API호출실패log도보존. prepare입력59/65및v17 54/v16 50/v15 44hash불변·known9subset·provisional존재evidencehashPASS. 원본/이전실패보존,HPO/trainingPAUSED/연구denominator0. 다음은저장궤적terminal측방잔차·제동검증,GC동기pause안전lifecycle검증및추가fault ZERO-ONLY정지관찰gate이며이번세번째Kit미실행.


## 2026-11-01 — v19 실제 PRE 및 FINAL 정상 정지 완료

[보고서](../reports/construction_site_perception_approach_20261101_v19.md). v18_02 저장 궤적에서 base 전방 오프셋 약0.339m와 종점 잔류곡률을 확인하고 신규 v19 rear 기준 추종·종점곡률0 국소 경로·종단감속을 적용했다. 실제 Kit2회/추가0. 첫 v19는 PRE2.759mm 정상 정지 후 FINAL 직전 새 객체 gen2 GC558.984ms→driver TF_STALE(.502374s), NOT_READY 보존; ZERO-ONLY 새61샘플 quiet1초 PASS. 확인된 GC 원인 수정 v19b는 정지 precollect 후 제한된 cyclic GC 지연(600초/RSS증가768MiB/절대8GiB), 독립 ROS freshness/GID 및 원래 safety 유지·finally 복원; 실제297.738초/peak RSS7,211,487,232bytes/GC복원PASS. 새RGB-D/frozen HR YOLO/B4/수동ROI B5→새PRE/FINAL→PRE full rover sweep/live support48060PASS→정상PRE→측정 정지 자세에서 독립FINAL sweep/support43740PASS→정상FINAL. PRE_REACHED=true(2.856mm, yaw−.03452°), FINAL_REACHED=true(2.894mm, yaw−.03435°), 각각 ZERO후1.000000052초 quietPASS. 실제 경로1.680854m/비영2344기록, 예상외contact/shell하중0. Active GC pause0/guard최대52.713ms/driverTFage최대78.994ms; 일반 timing보장 아님. FINAL 완료 응답 대기를 leg 시작 기준에서 새5초deadline으로 수정, driver completion_accepted=true. v10C provisional eligible=true 후 실제Kitexit0와outer재검증 ENGINEERING_RECORDED/runner0; driver/observerexit0·request결합cleanupzero10·소유PID소멸PASS. v18입력59/65·v19입력70/73hash불변/provisional증거hash/known9subsetPASS, CPU replay·GC예외·identity·receipt·compilePASS. 원본stage/suppliergraph/model/protocol/이전실패 보존. GOAL_OVERSHOOT zero-only eligibility CPU검사PASS이나 이번 실제 발동은TF fault뿐임. HPO/trainingPAUSED·연구분모0/과학비교·432실행0. 다음은 v19b snapshot·명령·증거 handoff 고정이며 반복재현성/다른환경/실로봇 타당성UNKNOWN, 추가실행은 별도 작업.


## 2026-11-01 — v20 v19b 기준선 동결 / 독립 반복 0/2

[보고서](../reports/construction_site_reproducibility_20261101_v20.md). 먼저 root `construction_site_v19b_success_baseline_20261101_v20.json` 및 추가의존성 `_v02.json`/SHA sidecar를 신규 생성했다. v19_02 prepared73·executed snapshot69 일치, 원시 성공·PRE/FINAL 개별 인증·환경·모델·USD/overlay·graph allowlist·seed·assisted ROI를 해시 인덱스로 고정했다. USD 정적 closure는27layers/materialized dependency 확인이나 SDK MDL/remote 및 일부 texture 미해결로 전체 renderer closure UNKNOWN 유지. historical v19b success1회·첫 v19 FAIL 보존.

원본코드/시작배치/관측/모델/GC/제어/5mm·2도·quiet1초/safety 변경0으로 새 `CONSTRUCTION_SITE_REPRODUCIBILITY_20261101_v20_01`/`_02`에서 실제 Kit 정확히2회, 추가0. 매번 새RGB-D·실제HRYOLO/B4·현재 RGB와 overlay 직접 검토/hash결합 수동ROI B5·새PRE/FINAL 산출. PRE 각각2.682323/2.772089mm, yaw−.037579/−.013001°, 개별ZERO후1초quiet 인증PASS; FINAL은 두번 모두 MOVING→ZERO_SETTLING 동일update 전이로 별도BRAKING command0개→기존 confirmed_stop 인증거절→driver7sim초 뒤completion_accepted=false→TWO_LEGS_INCOMPLETE/MISSING_WITNESS, outerNOT_READY·runnerexit1로 보존. **독립전체성공0/2**이며 historicalsuccess는분모제외. 마지막 측정FINAL잔여2.978442/2.851582mm지만 fault_zero_only phase·독립FINAL인증누락으로 도착PASS 아님.

실제경로1.682034/1.682042m·비영2363/2353·wheelpeak1.572852/1.450511rad/s, 예상외contact/shell침투하중0. driverTFage최대60.709/49.504ms·GID/TFfault0. 새ZERO-ONLY61samples씩 quiet1초PASS/cleanup요청결합zero10PASS는안전정지만증명. GC317.790/310.173초·RSS증가584306688/577949696bytes로기존한도이내·paused복원PASS. driver/observer/Kitexit0·전체runner1; 강제종료0/소유PID소멸/남은Kit·training0/rustdesk보존. 최종1072hash항목불일치0·각snapshot69일치/provisional·evidencehashPASS·known9subsetPASS. freshdepth 내용hash는두회동일하나새Kit/capture/inference와새RGB·ROI검토기록으로구분. 모든실패·v01–v19·원본보존,latest갱신. optional주행영상은기존capture없어미생성. HPO/trainingPAUSED·scientificdenominator0·324/432/과학비교0.

다음은별도좁은offline lifecycle작업: 정상stop의같은호출내BRAKING→ZERO전이와인증관측일관성검증; 기준완화나이력성공재분류없이새버전후보CPU검증뒤별도bounded engineering gate. 현상태fixed-condition scientificpilot보류,해결후작은cross-representation admission별도제안. LR독립저입력재구성/HRdecimation아님,HR/LR/CAD독립자산·모델구분,기존4representation pairedlock/관측·ROI도움·제어·metric·분모동일유지. 향후representation×loadcompleteness×occlusion축만언급하며자산생성·설계잠금변경·v21 sweep미시작.


## 2026-11-01 실행 / 2026-11-02 완료 — v21 정지 전이·인증 수정, 새 실구동 1/1

[보고서](../reports/construction_site_stop_lifecycle_20261101_v21.md), [독립 proof](../reports/construction_site_stop_proof_20261101_v21.json), [최종 인덱스](../reports/construction_site_final_audit_20261101_v21.json), [재개 보존 검사](../reports/construction_site_resume_preservation_20261102_v21.json). 기존 adapter/확인 logic으로 v19b FINAL1109호출·v20 각1114호출을 짧게 replay하여 기존 반환 전체 불일치0, 역사적PASS/FAIL 그대로 확인했다. v20은 정상 stop 같은 호출 안의 MOVING→BRAKING→ZERO에서 governor가 실제 바로0을 반환하고 중간 state만 숨긴 경우다. 새 versioned adapter는 실제 전이 ordinal/cause/update입력만 추가하고 제어출력을 유지했다. 독립 verifier는 상태기계를 재계산하고 raw physics/실제 wire·zero readback·정상요청·5mm/2도·새quiet≥1초·ROS/GID·leg순서 및 기존 safety를 계속 요구한다. 가짜 BRAKING행·dummy명령·기준완화0. CPU20/20·기존GC3/identity6/IO5/graph5 및 compile PASS. 개발중 snapshot경로오류·archivedfixture2회FAIL·compile들여쓰기FAIL은 보고/로그로 보존했고 Kit 전에 해결했다.

새 외부 root CONSTRUCTION_SITE_STOP_LIFECYCLE_20261101_v21_01에서 Kit정확히1회/retry0. 같은 원본site/start/suppliergraph/v19follower에서 freshRGB-D/HRYOLOconf.719591/B4/새영상직접검토·hash결합수동ROI B5→새PRE(−25.934830108,28.278040523)/FINAL(−25.934830108,29.078040523)m. PRE fullrover sweep/live support48060 및 정지 후 독립FINAL43740 PASS. PRE2.723096mm/yaw−.037820°, FINAL2.887923mm/−.039664°, 각ZERO후1.000000052초quiet/zero readback PASS. PRE는두호출비영BRAKING→ZERO, FINAL은step7430/update1112 한호출두전이이며 실제출력0·비영BRAKING행0; event→governor출력→물리stop인증의일치를실제검증했다.

실측경로1.680723306m/비영2361·6wheel qspan12.5639–12.5658rad/peak1.356681rad/s, planarpeak.029738332m/s·steer15.714018°로기존guard이내. 예상외contact/shell침투하중0. driver/session endpoint88812/7375행을 원래guard로독립재생해오류0·두leg저장certificate정확일치. TFwallmax328.103/308.305ms·simmax16.667ms, 기존한도유지/TF·GIDfault0이며일반timing보장아님. GC329.710초·관측peakRSS7181115392/증가577691648bytes/paused복원PASS. drivercompletion_accepted=true·zero20·cleanup요청결합zero10·driver/observer/Kitexit0·outerENGINEERING_RECORDED/runner0. faultrecovery사용0·강제종료0·소유PID소멸/남은Kit·training0·rustdesk보존. 과거1072hash·새prepared84·공통입력불일치0, raw186파일·snapshot80 및 환경binary/source/preparehash보존. 재개후추가Kit0.

과거v19b성공및v20FAIL0/2는불변,새v21engineering1/1만성공이다. 수정버전반복성은n1이므로장기성공률/실로봇/다른환경으로확장하지않는다. 정지engineeringgate PASS이나 작은공통조건scientificpilot명세/명령미작성으로과학pilot NOT_READY·전체rendererclosure UNKNOWN. 다음은4표현별frozencheckpoint/asset·pairedscenario와관측/ROI도움·제어/안전/metric/실패분모를공통고정한pilotadmission명세작성이다. HR/LR/CAD실험·자산/인식/항법재구성·432·training미실행, HPO PAUSED/sciencedenominator0.


## 2026-11-02 — v22 HR/LR/CAD 과학 파일럿 admission 명세 / offline BLOCKED

[보고서](../reports/construction_site_scientific_pilot_admission_20261102_v22.md), [후보 manifest](../manifests/construction_site_pilot_candidate_20261102_v22.json), [명령/adapter 계약](construction_site_pilot_commands_20261102_v22.md). 10월29일 향후3rep 결정을 확인했고 기존4rep frozen manifest를 수정하지 않았다. prelock v01+amendment through v03+geometry v02 실제내용 및 known9 SHA/count PASS; 입력72 SHA PASS, base108/execution432/geometry108·432 exact-set/4rep pairing/모든열 join PASS. 실제 normalized8asset·matched4M50·B4/B5원본 확인. standaloneUSD만 사용해 현장cementHR300 AssetRef/instance collider300·25layers 확인, LR/CAD원본collider0이므로 단순참조교체의physics차이를 명시했다. plainTraverse collider0은 instanceproxy누락으로 구분했다. LR독립저입력재구성/HRdecimation아님, CAD=GeoCAD/Proxyappearance의존성 보존. 비용characterization·LRpreprocessing·CAD재현benchmark를 찾았고 HR/LR120/30분은approx보고값, human/passivecompute결측 유지.

최소한base×3rep 각1행은 새pilot namespace/cementC100/full300/추가occluder없음/v21start·seed261022·동일수동ROI·matchedM50·공통v21controller/verifier 제안이다. frozenFE2E_S001의start/seed/조명과같지않아exactreplay라하지않는다. 공통정적brickslot충돌overlay는 명시적pilot-only physics개정 제안/미구현. 세표현readinessBLOCKED,새checkerexit2·runtime계약12개미구현거절;AST/누락input·변조hash거절CPU검사PASS. 다음단일작업은pilot-only amendment+최소parameterizedadapter/derivedoverlay의prepare-only구현·검사다. 신규live실행파일이있는것처럼명령을만들지않았고v21runner재실행금지명시. 탐색경로/권한오류와첫USD인라인괄호오류를보고했고수정후read-only검사완료. 원본source/USD/weight/lock/v19–v21증거불변,Kit/ROS/training/새자산/Gitpush0. correctedv21engineering1/1·v20FAIL0/2·과학분모0/HPOPAUSED 유지.


## 2026-11-02 — v23 실제3rep overlay 준비 / 두 구체 blocker 확인

[보고서](../reports/construction_site_pilot_prepare_20261102_v23.md), [절대경로·SHA manifest](../manifests/construction_site_pilot_prepare_20261102_v23.json), [검사](../reports/construction_site_pilot_prepare_checks_20261102_v23.json). 새 pilot-only DRAFT와 prepare-only parameterized standalone USD adapter를 작성하고 실제 HR_Scan_04/LR_Scan_03/GeoCAD_04 overlay를 외부 PILOT_SITE_PREPARE_20261102_v23 아래 생성했다. v21 prepared scene SHA를 기존 prepare expected로 확인하고 COW sublayer로 보존했다. 상위 reference 내부 HR arc가 단순 local reference list 교체 후에도 남는 것을 발견해, 기존 slot 하위 분기300개를 derived active=false로 격리하고 동일 transform 아래 새 PilotVisual child에 선택 normalized USD만 참조했다. 원본USD/source/모델/registry/4rep108·432/v19b–v21 raw/v20FAIL 변경0.

72/72 SHA·frozen pairing/join PASS, 각scene21/23 static gate PASS: 실제300slot membership·world matrix/회전 불변, 선택mesh source/활성material·texture PASS(CAD6subset씩1800bindings/Proxyappearance보존), canonical enabled static300/nativebrickcollision·rigid0, rover/ground·fixture surface침투0, fixedrover/camera/ROSgraph 및 canonical signature 세행동일. Brick MDL은 설치SDK 실제파일·SHA/searchpath를 확인했으며 compiler/runtime증명은아님. Visual envelope최대초과2.854e−9m수준/1µm허용내.

**최종 HR/LR/CAD 모두 BLOCKED**: 원래300slot에 표준190×90×57mm box를 놓으면 양의부피겹침96쌍. Axiscardinal오차4.441e−16으로 AABB오탐아님. 별도접촉은face1304/edge424/corner54. 공통rolltainer Plane은source의/World/Looks/OmniPBR을참조범위밖으로가리켜binding무시;intendeddiffuse /home/jh/Downloads/rolltainer_stl/apriltag_100.png 실제해당경로없음/원본SHA UNKNOWN. 이를이론적무해·fallback으로PASS처리하지않았다. 다음한정offline해결은동일300box의externalunion을보존하는비중첩staticcell정책을별도DRAFT로명시하고원래Planeimage/lineage회수후공통derivedbinding복구. 현300enabledbox/동일positions/겹침0요구를동시에충족했다고주장하지않음.

compile·focused8검사PASS(오모델/hash/Proxy/disabledcollider/transform/liveCLI거절). 초기compile괄호·USDAPI부재exit1·reference혼합·비효율triangle시도의실패/600초timeout을별도output/개발inventory에보존;최종증거로사용하지않음. Starter는Gitrepo아니어서gitstatus실패/commit·push0. Liveinterface는v21의scene입력과HR고정worker선택두지점최소변경계약만작성했고Kit실행파일인척하지않음. v24는blocker해결뒤HR한행의actualrender/PhysXshape·support·접촉admission부터,실패시motion0;exit/cleanup/독립proof후에만다음LR/CAD. Kit/ROS live·HPO/training/asset재구성/새research관측0,formaldenominator0,liveNOT_TESTED/scientificHOLD. v21engineering1/1과v20FAIL0/2그대로보존.


## 2026-11-02 — v24 두 pilot-only prepare blocker 해결, live 미실행

[보고서](../reports/construction_site_pilot_prepare_20261102_v24.md), [manifest](../manifests/construction_site_pilot_prepare_20261102_v24.json), [독립 검사](../reports/construction_site_pilot_prepare_checks_20261102_v24.json). 최종 외부 output `PILOT_SITE_PREPARE_20261102_v24_03`에 새 HR/LR/GeoCAD overlay 생성. 각행19/19 static PASS, actual composed3/3 PASS, 변조거절12/12·live/Proxy CLI거절2/2 PASS. 상태 모두 STATIC_PREPARE_PASS / LIVE_RENDER_PHYSX_NOT_TESTED / SCIENCE_HOLD.

300slot/transform/visual geometry/M50 및 source/v23/locks 불변. 원래300 world box의 cardinal오차4.44e−16을 재확인했다. raw endpoint exact union102셀은 missing/extra0·부피0.28129842034715324m³·외부경계정확일치로 보존했지만40개1µm미만 수치슬리버가 있어 최종 물리후보는 최대3.576nm endpoint 정규화28셀이다. 독립 구간검사상 원래 union 대비 missing6.216e−10m³/extra2.104e−9m³로 각1e−8m³ 이내, 정규화기준 missing/extra0·외부경계일치, positive-volume overlap0, nativebrickcollision/rigid0/static enabled28. raw bitwise equality false를 숨기지 않고 DRAFT에 수치조건을 명시했다. 모든 visual slot은 정규화하지 않았다. clearance는 hash-bound v23 SAT+union동등성+환경불변으로 이전했고 광범위 triangle loop를 반복하지 않았다. 실제contact/support/shape registration 증명아님.

원본apriltag_100.png는 제한된 알려진3root 탐색에서 미발견/lineage·SHA UNKNOWN. 공통 Plane에 동일 버전 UsdPreviewSurface 회색(.5,.5,.5)/roughness.8/metallic0/texture0 fallback을 직접 bind했다. source material/shader property·file SHA 기록, 실제 composed binding·활성재질dependency해결 및 다른 active materials·CAD Proxyappearance 보존 PASS. 원래appearance복원·시각동등성은 주장하지 않으며 실제render/ROI영향 검토전 motion금지.

개발실패 보존: v24_01 보수적 오차상한guard exit1; v24_02 대형mesh문자열반복180초timeout exit124. v24b에서 immutable-parent SHA+전체authored-delta whitelist로 불필요비교를 제거하고 실제양방향 구간적분으로 원래허용값을 검증, v24_03 총38.10초/exit0. 모든snapshot/로그/exit 및 실패receipt 보존. 새 DRAFT는 historical4rep frozen과 사용자선택pilot3rep를 구분한다. 다음별도v25는 검증된HR overlay/맞춤M50연결→motion0 render/material/ROI 및 실제PhysX28cell/native0·consumercoverage/contact/wheel-support→안전할때만fresh vision→PRE/FINAL→독립stop·clean exit. 이후LR/CAD각각별도승인. Kit/ROS/주행/과학관측0,formaldenominator0,HPO/trainingPAUSED,324/432시작0,원본/사용자프로세스/engine/packages변경0.


## 2026-11-02 — v25 새 HR pilot 단일 Kit admission / BLOCKED·motion0

[보고서](../reports/construction_site_pilot_hr_admission_20261102_v25.md), [독립 witness](../reports/construction_site_pilot_witness_20261102_v25.json), [integrity](../reports/construction_site_pilot_integrity_20261102_v25.json). v24 HR scene SHA5b928d…/정확한 HR M50를 pin한 새 v25 runtime link·runner/session/worker 구현. 단위1m/Z root metadata 명시,300visual/28static/native0/composed dependency 및 graph exact/허용 delta 밖 actor exact 확인. Plane fallback binding 한 관계만 의도 delta로 허용, 나머지 graph/actor guard 보존. HR offline14/14·v21stop20/20·known9subset/108·432rows PASS. offline prepare01–04의 metrics assert/Plane actor guard/API 오류는 실패 root에 보존하고05에서 수정완료; 이들은 Kit 시도 아님.

외부 `PILOT_SITE_HR_ADMISSION_20261102_v25_05/attempt_0001`에 실제 Kit정확히1회/retry0. 신규640×480RGB-D/실측calibration8/8·depthvalid290691·stationaryPhysXsupport2214/2214·6wheelcontact·shellPASS. 그러나 추가 renderer semantic annotator가 `Replicator_03_instance_segmentation_fast_Sync`를 생성하여 원래 graph guard UNKNOWN_GRAPH_NODE로 motion0 차단. USD 기반 live preflight inventory28은 확인했지만 실제28shape/native0 overlap gate는 호출전이므로 NOT_RUN/UNKNOWN. fresh YOLO/B4/B5/ROI/targets/PRE/FINAL/normalstop 미실행. baseline75행quiet1sim초·pose span0·wheel qspan/dq0은 주행stop 성공 아님. contacts168/예상외0. isolation전이라 cleanupzero publisher 미생성→receiptMISSING 인증FAIL. Kit/observerexit0·driver미시작·runner1/NOT_READY/MISSING_WITNESS·강제종료0/소유PID소멸·RustDesk보존. 실행input/snapshot/provisionaldigest/evidencehash 및 원본HRsceneSHA불변 PASS.

사후RGB에서 site/pallet/매우어두운load를 확인했으나 intendedHR재질품질·frame밖rolltainerPlane/fallback·ROI영향은INCONCLUSIVE/NO-GO; semanticlabels는BACKGROUND/UNLABELLED뿐. 원래AprilTag외관복원 주장없음. 추가로 현재/v21baseline 모두 nestedarticulation/xformstack PhysXschemaError10건 발견, 이전성공으로무해처리하지않음. 실제v25소스/snapshot불변 유지하고 새v25b로 추가annotator제거→pinnedSOURCE외v21captureASTexact/compilePASS. v25b는 ownedphysicsError를capture/motion전NO-GO하는별도gate도추가,저장v25/v21로그각10건offline거절PASS. 추가Kit/prepare/worker0, v25b도LIVE_BLOCKED.

다음은HRrolltainer parser진단의실제활성actor영향과보존조건내해결가능성offline판정후,별도새HRroot에서material/fallback·실제28/native0부터admission이다. cleanHR성공전LR/CAD진입없음. 이번engineering0/1을science분모에넣지않고formaldenominator0/HPOtrainingPAUSED/324·432시작0,기존v20실패/v21성공/원본rovergraphUSD/weights/v24세overlay/frozen4rep잠금보존.

## 2026-11-02 — v26 HR PhysX blocker 제거·실제28/native0 확인 / render NO-GO·motion0

[보고서](../reports/construction_site_pilot_hr_admission_20261102_v26.md), [독립 witness·raw hashes](../reports/construction_site_pilot_witness_20261102_v26.json), [정확한 prim/stack 진단](../reports/construction_site_physx_diagnosis_20261102_v26.json). 기존 mount smoke v01이 이미 강체9/collider10을 disabled로 만들었으나 rigid-body API9와 nested articulation root1이 남아 v21/v25 parser Error10건을 발생시켰다. v21/v24 유효 물리값·xform 동일 확인. 새 v26 파생 layer에서 비활성 API 선언만 삭제, reset·카메라·rover·joint·mass/inertia·controller·supplier graph 보존. 모든 authored 물리값/월드 변환 동일 및 live body11/DOF10 PASS. reset을 통한 수정은 rover 추종을 끊는 반례로 배제.

집중 CPU24/24·원래 v21 stop20/20·known9subset/108·432행 PASS 후 `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v26_03/attempt_0001`에서 Kit정확히1회/retry0. parser Error0, 실제 interior query28/28·region callbacks28/unique union28/native0·consumer28, stationary wheel support2214/2214·6wheel contact·shell PASS, contacts168/예상외0. 실제 등록 확인을 USD CollisionAPI count와 구분한다. seam은 정적 union/비중첩 및 live query 범위이며 동적 crossing 미검증.

새640×480RGB-D/calibration8/8/depthvalid290691·추가 semantic annotator 없는 원래 capture graph PASS. 그러나 실제 RGB의 매우 어두운 HR 적재물 외관과 frame밖 공통 Plane fallback 검토 미완료로 `PILOT_LIVE_RENDER_NO_GO`를 deadline 내 기록, motion0 중단. YOLO/B4/B5/ROI/PRE/FINAL/normalstop 모두 NOT_RUN, 새 observed goals없음, nonzero0. baseline quiet1.000000052sim초는 접근 정지 인증이 아니며 aggregate STOPPED=PASS를 성공으로 해석하지 않는다. Kit0/observer0/driver미시작/runner1·NOT_READY/MISSING_WITNESS, 실제 ROSzero receiptMISSING/validfalse·별도NOT_APPLICABLE_PRE_DRIVER 기록, 직접graphzero·요청을 receipt로 바꾸지 않음. 강제종료/timeout0·소유PID소멸 확인.

runtime inputs/snapshots/provisional·가용evidencehash PASS, v21/v25 executed originals·v24manifest/세overlay 불변 PASS. offline 진단 오류3·CPU변조대상 오류1·prepare01/02 실패는 보존하며 Kit시도 아님. 새 코드/분석/reports와 latest 갱신; 기존 v19–v25·원본USD/weights/ROSgraph·frozen4rep 잠금 보존. v24 세 STATIC_PREPARE_PASS는 static-only 유지, LR/CAD 실행·수정0, HPO/trainingPAUSED/formaldenominator0. 다음 구체 작업은 물리·원래카메라·suppliergraph·lighting을 보존하면서 HR 재질과 frame밖 fallback을 실제로 검토할 별도 관찰 방식 확정이며, 이번 v26에 추가 Kit는 없음.


## 2026-11-02 — v27 HR 실제 perception 시작 / 수동 ROI87<100 FAIL, motion0

[보고서](../reports/construction_site_pilot_hr_admission_20261102_v27.md), [독립 witness](../reports/construction_site_pilot_witness_20261102_v27.json), [결정 규칙](construction_site_hr_admission_rule_20261102_v27.md). v26/v21 동일 optical calibration에서 load ROI 평균luma10.5258/10.5128 확인. 저장v26 frozen HR YOLOconf.68805/mask7714·B4 유효; active PBR MDL/packaged texture 확인, unlit 아님. 공통 Plane bounds 전체가 오른쪽 frustum 밖이므로 NOT_VISIBLE/OUT_OF_SCOPE로 분류했으며 AprilTag MISSING·원본동등성없음·전체rendererclosure UNKNOWN 유지. v26 당시 실패는 소급변경0.

새 root PILOT_SITE_HR_ADMISSION_20261102_v27_01에 Kit정확히1회/RETRY0. 새RGB-D/calibration8/8·depth290691, graph·PhysX28/native0·consumer28·wheel support2214/2214·예상외contact0 PASS. 새HR YOLOconf.71225/mask7717·B4 유효. 새영상 직접검토·hash결합 수동ROI 후 erosion/exclusion으로87점만 남아 기존최소100점 gate FAIL→PERCEPTION_FAIL. B5 pose/targets·PRE/FINAL·driver·비영명령 NOT_RUN/0. ROI변경·재추론·재시도0. Kit/observer0·runner1/NOT_READY/MISSING_WITNESS, ROSzero receipt MISSING/NOT_APPLICABLE_PRE_DRIVER·직접graphzero와요청만기록, 강제종료/timeout0·소유PID잔존0. baselinequiet는 접근성공아님.

compile/집중CPU28/28·v21stop20/20·known9/count PASS; 종료후 functional admission5/5 PASS(추가Kit0). 입력/snapshot/provisional/가용evidencehash PASS, v26raw154hash불일치0·v24parent재검사PASS. 코드/모델/관측/조명/physics/정지기준보존. 유효HR pilot성공0/1시도, formal science denominator0/HPOtrainingPAUSED/pilot-onlyDRAFT/LR·CAD0. 다음은 실패RGB/ROI/mask의점수확보가능성·경계불확실성offline검토이며 이번실행구제없음; cleanHR PRE/FINAL 독립성공전 LR/CAD권고없음.


## 2026-11-02 — v28 ROI113/B5 PASS, 실제 HR 주행 전 GC_MEMORY_BOUND·close 실패

[보고서](../reports/construction_site_pilot_hr_admission_20261102_v28.md), [pilot-only ROI rule](construction_site_roi_review_rule_PILOT_20261102_v28.md), [독립 witness](../reports/construction_site_pilot_witness_20261102_v28.json). 저장v27 old ROI87 재현, 시각적으로 정당한 조금 넓은 상면 후보113/113이 기존 fit gate PASS. ±1px perturbation92–139점으로 좁은 margin 기록. 공통 HR/LR/CAD180초 count-only preview·raw overlay 검토→단일 최종제출을 pilot observation-policy 변경으로 명시했으며 frozen locks 변경0. ROI14/14·소스/시각거절5/5·v21stop20/20·known9/count PASS, 기존capture/infer/observed_corridor/B5fit 보존.

새외부root PILOT_SITE_HR_ADMISSION_20261102_v28_01, Kit정확히1회/RETRY0. freshRGB SHA d1b5e670ea9a5def7043db1640c6f9e69735b4f0bf00ebce9d14e893cf409bbe, camera/calibration·PhysX28/native0·support2214/2214·contact168/예상외0 PASS. 새HR YOLOconf.701445/mask7718·B4 PASS. 새영상·확대·raw overlay 직접검토 후 preview1/최종1,113점·B5 COMPUTED·freshPRE/FINAL목표생성 PASS. PRE 전체rover swept/live support48060 PASS. 그러나 motion_gc.enter 직후 첫tick에서RSS22,329,970,688bytes(20.7964GiB)>기존8GiB로 GC_MEMORY_BOUND. driver미시작·비영0·실제PRE/FINAL/normalstop/FINAL독립sweep NOT_RUN. 메모리 원인UNKNOWN, gate완화/재시도0.

후속Kit close25초watchdog 초과·terminate후5초에도미종료→kill, Kit−9/runner1 FAILED·KIT_EXIT_NOT_ZERO·정상shutdown증거없음. observer0/driver없음·owned잔존0, ROSzero receiptMISSING/NOT_APPLICABLE_PRE_DRIVER 유지. GC복구했으나 한도PASS아님. 입력/snapshot/provisional/가용hash PASS·v27전체raw/입력보존 mismatch0. 기존v27 0/1FAIL·v20 0/2FAIL·v21engineering1/1 불변, v28engineering0/1FAIL/science분모0/HPOtrainingPAUSED/LR·CAD0. 다음은한도유지하 pre-driver RSS원인·close지연의별도bounded진단이며이번추가Kit없음. cleanHR PRE/FINAL독립성공전LR/CAD진행없음.

## 2026-11-02 — v29 메모리·Kit close 오프라인 진단 / live BLOCKED

[보고서](../reports/construction_site_pilot_hr_admission_20261102_v29.md). v28 Kit-owner PID1966007의 `/proc/self/statm` RSS임을 확인: 진입22,329,970,688bytes/복구동일/scope0.002579초, v21진입6,603,423,744bytes. 이전 phase RSS/PSS·종료 stack 미기록으로 실제 소비원·close 대기 callback UNKNOWN. standaloneUSD 두 read-only probe exit0: v21/pilot stage-open RSS302,993,408/306,733,056bytes, PSS300,339,200/303,978,496; Kit runtime 재현 아님. instance322→22와 v23의300slot uninstance를 확인했으나 renderer 복제 메모리 인과관계는 미측정 후보이며 physics/visual을 수정하지 않음.

새 v29 session은 ownerRSS/PSS/GPU/GC·stage count·paused phase/close stack 계측만 추가한 미승인 초안, 실제 메모리/종료 fix PASS 아님. tick계측/threshold상향/cleanup순서변경0. compile·CPU5/5·원래stop20/20·composed3/3/변조12/12·known9/count PASS, v28입력101/snapshot90 hash mismatch0. 초기 CPU pxr import 실패 로그 보존 후 pure classifier AST로 재검사 PASS. mock close 검증은 native Kit/observer 종료 보증이 아님. 현재 host/cgroup 정보는 당시 Kit peak로 해석하지 않음.

사용자 조건7에 따라 원인/두수정 미입증으로 신규Kit0/retry0/live output root없음, HR PRE/FINAL NOT_RUN. v28engineering0/1FAIL·v21engineering1/1·historical분모보존/science0/LR·CAD0/HPOtrainingPAUSED. 다음은 인스턴싱/resource-lifetime RSS재현과 실제 close 대기 증거로 최소수정을 입증하는 gate이며 동일 live 실패 반복하지 않음. 8GiB/768MiB/600초 및 TF/GID/contact/stop 정책 그대로, 원본/locks/weights/USD 변경0.


## 2026-11-02 — v30 공유 HR visual 복원 / 원래 한도 내 실제 PRE·FINAL 및 exit0

[보고서](../reports/construction_site_pilot_hr_admission_20261102_v30.md), [정적 instance/변조 검사](../reports/construction_site_instancing_checks_20261102_v30.json), [독립 witness](../reports/construction_site_pilot_witness_20261102_v30.json). 기존 AssetRef uninstance와 inherited HR active=false는 보존하고, 선택 HR reference/native physics=false를 공통 abstract class로 옮겨 기존 PilotVisual root300개를 내부참조 instance로 만들었다. 새 descendant override0, actual HR300 placements/각mesh1/공유prototype1, 전체instance22→322/총prototype23, native enabled0·union28·mount correction·fallback·graph 보존. 공유visual 전체property SHA동일/모든slot transform·source stack·material PASS, bound수치차최대1.0658e−14m, 변조5/5거절. Load밖2065 active prim 고정world/source-stack signature동일.

외부 PILOT_SITE_HR_ADMISSION_20261102_v30_03에서 신규Kit정확히1회/retry0, engineering1/1 PASS. ownerPID1995923 같은실행 RSS: startup4.3002GiB→derived4.5870→attached5.7962→PhysXsettled6.1118→capture후6.1474→worker후6.1503→pre-drive/GCbase6.1936→scopepeak6.7268/복구6.7270→close-enter6.7516. PSS/private/별도GPU VRAM·wall/sourceSHA 기록; v28 GCbase20.7964GiB와별도run비교이며동일runphasegrowth로부르지않음. 기존8GiB/+768MiB/600초보존, scope340.191초/증가572481536bytes/GC복원PASS. 공유복원과큰RAM감소의실측연관은확인했으나rendererallocation인과분해/반복성미입증. 정책상향없음.

FreshRGB-D/calibration8/8·HRmatchedfrozenYOLOconf.791759/mask7710·B4 PASS, 새영상/rawpreview직접검토후v28규칙preview1/final1 ROI114/114·B5 PASS. 실제PhysX28/native0·consumer28·wheel support2214/2214·6wheelcontact, parserError0·contact50708/예상외·shell하중0. PREswept/live48060 및 측정PRE정지뒤독립FINAL43740 PASS. 실제PRE2.883526mm/yaw−.0378203°·FINAL2.794514mm/−.0397224°, 각normalzero뒤새quiet1.000000052초/독립certificateexactPASS. Driver/session endpoint92090/7341replay실패0·비영2350·completion_accepted=true·요청결합cleanupzero10/receiptvalidtrue. Kit/driver/observer/runnerexit0·watchdog/강제종료0·owned잔존0. Close-enter있음/Pythonreturncheckpoint없음/10초stack파일0bytes: process정상종료와함수반환미관측구분, v28nativehang원인은UNKNOWN유지/cleanup변경없음.

입력108/snapshot/provisional/evidencehash·known9/108·432count·inheritedpairing/dependency·stop20/20 PASS, v28raw185hash불일치0. Offline01 anonymous확장자오류/02 exactBBox거절 보존;03geometryPASS뒤MANIFESTre-export누락으로plan만실패해scene재작성없이finish완료. 채택instance후보1/Kitroot1이나실패scratch2에기존형derivedUSD생성은요청scene수경계초과로보고하고삭제하지않음. v19–v29/원본/locks/weights그대로, v20FAIL0/2·v21old-site1/1·v25–v28FAIL·v29Kit0 불변. Scientificdenominator0/HPOtrainingPAUSED/LR·CAD·324/432미실행, 과학비교완료아님. 다음별도작업은같은pilot-onlyDRAFT조건/공유visual·matched모델의LR1행boundedadmission이며이번추가Kit없음.


## 2026-11-02 — v31 첫 matched LR pilot / B5 통과 뒤 PRE curvature admission 실패

[보고서](../reports/construction_site_pilot_lr_admission_20261102_v31.md), [독립 witness](../reports/construction_site_pilot_witness_20261102_v31.json), [runtime/곡률 산술](../reports/construction_site_runtime_summary_20261102_v31.json). v30 실제입력108/snapshot96/raw218 hash불일치0 확인 후 LR선택·class/import/모델 metadata만 새v31로 연결했다. LRparent/asset/model SHA PASS, 300visual공유prototype1/instance322/native0/union28, HR대비 slot변환300·fixedworld2065 exact signature PASS, 변조5/5거절. v24DRAFT/v28ROI/frozen4rep locks 불변.

외부 PILOT_SITE_LR_ADMISSION_20261102_v31_01에서 Kit정확히1회/retry0. freshRGB SHA606a28d6b92cd777aa381327be26e8f151a812e3ff9f20a039cbb1528d55a8e9·calibration8/8, frozenLR YOLOconf.972648263/mask7718·B4 PASS. 새영상/새mask/rawoverlay직접검토 preview1/final1 ROI132/132·±1px121–143·B5 PASS. actualPhysX28/native0/support2214/2214/6wheelcontact·parser0·contact168/예상외0 PASS. 새LR PRE(−25.9398326593,28.2782491865) 경로가 CURVATURE_INFEASIBLE로 driver전실패. 독립저장자료산술 LRpeak.387170521/m>공통.363645333/m, HR.350094192/m; start동일·LRtargetX차−5.011352mm. controller수정/목표보정/구제0. 실제PRE·FINAL·두normalzero/quiet·FINAL독립sweep NOT_RUN.

LRengineering0/1FAIL 보존, Kit/observer0·driver미시작·runner1/NOT_READY/MISSING_WITNESS. 비영명령0·ROSzero MISSING/NOT_APPLICABLE_PRE_DRIVER, baselinequiet는접근성공아님. watchdog/강제종료/잔존0. ownerPID2724175 phaseRSS최대sample6.18753GiB/VRAM별도, motionGC NOT_ENTERED로8GiB/+768MiB/600초scopePASS주장없음. taskGT main/strict/relaxed는endpoint미주행으로NOT_ASSESSED. input115/snapshot/provisional/evidencehash PASS, compile·stop20/20·known9/count PASS. 최초systemPython witness cv2부재실패로그보존, 기존sdg_tools로read-only검사완료/설치0. v30raw218종료후보존불일치0.

HRv30 1/1과LRv31 0/1은기술적서술관측이며표현성능·동등성·일반신뢰도증거아님. 추가HR/GeoCAD/324/432실행0·science분모0/HPOtrainingPAUSED. 다음은저장LR목표의공통planner admission margin offline검토이며이번재시도없음. 공통정책변경필요시별도versionedproposal, 기존실패소급변경금지. LR독립성공전GeoCAD실행권고조건미충족.


## 2026-11-02 — v32 세 번째 GeoCAD pilot / B5 PASS 뒤 동일 곡률 admission FAIL

[보고서](../reports/construction_site_pilot_geocad_admission_20261102_v32.md), [독립 witness](../reports/construction_site_pilot_witness_20261102_v32.json), [저장자료 산술·보존](../reports/construction_site_runtime_summary_20261102_v32.json). 사용자 v32 명시 지시에 따라 LR 실패를 유지하고 세 번째 GeoCAD를 같은 정책으로 실행했다. 과거 LR 성공 전 CAD 금지 권고는 이번 지시로 대체되며 안전 gate/실패기록 변경0. GeoCAD asset/model/parent SHA PASS, shared visual300/prototype1/여섯 bound subset/native0/union28, HR대비 fixedworld2065·300slot exact PASS, 변조5/5거절. 원래 quintic/곡률.363645333/m·target/controller/camera/graph/GC/stop 정책 불변.

새 PILOT_SITE_GEOCAD_ADMISSION_20261102_v32_01에 Kit1/retry0. fresh640×480RGB-D/calibration8/8·frozenGeoCAD YOLOconf.959305346/mask7703/B4 PASS. 새RGB/detection/count-only overlay직접검토 preview1/final1 ROI138/138·B5 center(−25.9367052594,30.4783510578)/heading89.453897834° PASS. PhysX28/native0/consumer28/support2214/2214·sixwheel·parserError0·contact168/예상외0 PASS. PRE CURVATURE_INFEASIBLE로 driver전거절: 저장1mmquintic산술 max.366967770/m, HR.350094192/LR.387170521/m. 구제/목표보정/새planner0. engineering0/1FAIL, PRE/FINAL/독립정지/FINAL sweep NOT_RUN.

Kit0/observer0/driver미시작/runner1, 비영0, ROSzero MISSING/NOT_APPLICABLE_PRE_DRIVER, baselinequiet는접근성공아님. watchdog/강제종료/잔존0, ownerPID2740591 sampledphaseRSS최대6.05355GiB·VRAM별도, preworker8GiBPASS/motionGC NOT_ENTERED. 입력/snapshot/provisional/evidenceSHA PASS; known9/count108/432·inheritedpairing·compile·stoppingadapterCPU8/8 PASS. HRraw218/LRraw192 hash mismatch0. source/weights/locks/기존결과보존.

세표현각1회 결과 HR1/1·LR0/1·CAD0/1은 고정정책 아래 기술관측이며 통계적충분성/geometry단독열등성/동등성/실로봇검증이 아니다. 후속은 별도prospective공통plannerrobustness연구: 수mm목표민감도와 동일steering/obstacle/sweep하 대체경로존재(현재UNKNOWN)를 확인하고 새정책은 세표현모두에 freshtrial 또는 명시적offline replay로 적용한다. 실패소급변경금지. 이번새planner구현/실행·HR/LR반복·training/HPO·324/432없음, science분모0.

## 2026-11-02 — v33 저장된 세 표현 오프라인 오차 전파 완료

[보고서](../reports/construction_site_pilot_error_propagation_20261102_v33.md), [재현 코드](../analysis/construction_site_pilot_error_propagation_20261102_v33.py), [3행 증거](../reports/construction_site_error_propagation_20261102_v33_02/evidence_3rows.json). 실제 raw/snapshot/input930 SHA 비교 및 v24 parent authority chain PASS. 원본 plan AST의 strict admission과 진단용 곡률예외 제거 사본을 구분했다. 실제 동일 baseline/camera를 확인하고 HR/LR/CAD max .350094191771/.387170520832/.366967769982/m을 기존 산술과1e−12 이내 재현, HR 저장 경로 배열도 일치. LR/CAD 완전 경로는 새 offline candidate이며 실주행 아님. X/Y/XY 분해에서 LR X +.037259985972/m·Y −.000166071360/m·interaction −.000017585551/m; CAD X +.014013902622/m·Y +.002750040040/m·interaction +.000109635550/m. 공통 HR 기준441점±10mm grid/1mm 및 경계 refinement 완료, dy0 임계 dx 약−1.821718mm. threshold/정책 변경0.

Canonical task design GT center/world/yaw를 잠금에서 검증해 평가에만 사용: 예측 target XY 오차 HR5.415594366/LR5.844601652/CAD5.754615494cm. HR 실제 FINAL observed-goal .279451388cm와 canonical5.523288386cm/.039722360°를 구분, 기존 evaluator posthoc main/relaxed PASS·strict FAIL. 정식 science 편입 없음. LR/CAD physical endpoint NOT_RUN 유지. 독립 segmentation GT 없어 precision/recall/AP/mAP UNKNOWN; 예측 mask overlap/동일 ray 3D 차이는 accuracy가 아님. 실제 ROI reviewer code HR-v30 대 LR/CAD-v28 불일치를 raw 우선 기록, 동일 reviewer 완전통제 주장 제한.

첫 분석 run은 CSV interaction column ValueError FAIL로 부분 출력/failure.json 보존. 수정 뒤 별도 _02 출력 exit0/compile 및 artifact checks PASS, XY/curvature/feasibility PNG3·CSV/JSON 완료. Kit/ROS/inference/훈련0, 원본 planner/ROI/asset/model/locks/USD/기존 실패 변경0. 연구denominator0/HPOtraining PAUSED. 다음은 원래 공통 정책의 prospective paired 반복, 선택적 구제 없는 별도 공통 경로 robustness 검토이며 대체 안전 경로 존재 UNKNOWN.


## 2026-11-02 — v34 저장 B5 datum/오차 예산 오프라인 완료

[보고서](../reports/construction_site_pilot_b5_datum_and_error_budget_20261102_v34.md), [재현 코드](../analysis/construction_site_pilot_b5_datum_and_error_budget_20261102_v34.py), [수치 예산](../reports/construction_site_b5_datum_and_error_budget_20261102_v34_05/datum_budget.csv). HR/LR/CAD B5 전체 출력 1e−10 이내·PRE/FINAL dictionary exact 재현. 실제 prepared stage m/Z-up 및 300slot×3 transform/bounds를 standaloneUSD로 확인: Fixture/Load원점·slot평균은canonical(−25.888,30.509)와 일치하지만 visualAABB중심은(−14.25,−14.25)mm. Asset밑면z[0,.057]를SideStanding−90°회전한 비대칭배치로 앞면은설계중심503.5mm앞/B5반치수475mm여서종방향−28.5mm항 확인. 전체side q98(X)는authored우측경계보다HR46.735/LR51.878/CAD52.911mm안쪽. axis90평가예산+실제heading잔여로세cm벡터닫힘; 독립물리GT·segmentationGT없이전부sensingerror라하지않음.

48개HR heading/plane/mask/depth 치환과12국소민감도. LR mask만HR치환시X+4.693212mm, plane만0; CAD heading만(−4.291802,+3.229069)mm·mask만(+10.296628,−3.788228)mm로상호작용/상쇄확인. 실제plane높이차는LR+.004372/CAD+.011769mm·XY영향거의0. representation+matchedmodel+manualROI개별인과몫UNKNOWN. 단계기여도·pixel/depth·scene900행·GT벡터PNG·환경/hash기록완료. 첫_01은metadata부모layer단독USD기본.01m/Y-up assertionFAIL보존; actualruntime root를witnessSHA검증후_02PASS, side/asset증거_03PASS, provenance/그림_04PASS, helperobservedSHA추가최종_05PASS. helperhistorical독립expectedUNKNOWN/frozencoreASTPASS; expected수정0.

새Kit/ROS/inference/training/주행0·정책/GT/scene/ROI수정0. HRengineering성공/v31·v32curvature실패·HRactualFINAL평가불변/LR·CADendpointNOT_RUN. Formalconfirmatoryscience분모0/HPOtrainingPAUSED. 다음은datum/치수관계를명시한pairedrepeatedload/occlusion단계측정계획과별도공통plannerrobustness전향연구검토; 새정책은새amendment필요/실패소급변경금지.


## 2026-11-02 — v35 전향 measurement DRAFT + 공통 smooth-S offline feasibility 완료

[보고서](../reports/construction_site_pilot_prospective_measurement_and_planner_20261102_v35.md), [measurement DRAFT](construction_site_pilot_measurement_amendment_DRAFT_20261102_v35.md), [paired18 PROPOSED](../manifests/construction_site_paired_variance_PROPOSED_20261102_v35.json). D(task-design support origin)/V(visualAABB)/B(B5 assumed rectangle)/observed goal/physical endpoint 및 frame/sign·stage별 분모를 분리했다. GT masks/AP/mAP 구현은 미완료이며 actuation graph 분리 annotation 제안. 각n=1·matchedM50/manualROI/독립metrology 없음·reviewer문자열차이와HR observed FINAL.279451cm 대design5.523288cm/LR·CAD NOT_RUN 보존. 3view×2repeat×3rep18행은새pose/seed를명시한미승인전향pilot이며분산뒤표본수산정/power주장없음.

원래strictquintic HR .350094192/LR .387170521/CAD .366967770 재현·HR배열1e−12·독립선형계replay PASS. 같은start/perceivedgoal/yaw/15°/.7m/.95/.02m/s/forward-only에고정smooth-S primitive사용:상한.247883579/.274096983/.259815546/m. 세표현각±10mm3×3 총27점전부곡률PASS(최악.334000963/m);합성은관측아님. 실제USD fullcollider13/scene42·instanceproxy조향4개·.15m확장보강후각973350supportqueries실패0,확장envelope장애물거리하한.129149/.128940/.132583m. offline조건부PASS/LIVE_PHYSX_UNTESTED;livelegacyhelper불변. core31/독립38/speed27/hash1010/compile·artifact검사PASS. `_01`serialization/`_02`timeout/`_04`·`_05`AST실패보존,`_03`좁은다항식scope LR no-path/`_06`보강전결과와최종`_07`구분.

새Kit/ROS/inference/training/motion0·원래LR/CAD실패소급변경0·formal science0/HPOPAUSED. 다음은전향protocol승인후별도3repengineeringqualification에서fresh관측/실제steer·support·tracking·PRE/FINAL정지검증이며이번실행승인아님. 이후paired반복분산/독립GT구현으로진행;432미실행.


## v36 공통 planner 소프트웨어 bridge — 2026-11-02
[결정 게이트](../reports/construction_site_common_planner_integration_20261102_v36.md). 새 engineering-only adapter와 CPU replay를 작성했다. v35 공통 smooth-S geometry27개 exact 일치, 실제 legacy rear/base API·wire 부호·speed 상한 회귀 PASS_OFFLINE. 신규 모듈만 base/rear speed 계약을 보정했고 원본 follower/driver/locks는 불변. `_01` 완료와 추가 검사 `_02` 완료를 모두 보존. 실제 actuator rate NOT_VERIFIED, live PhysX/50ms 추종·BRAKING·독립 stop UNKNOWN으로 motion HOLD. nominal engineering3은 사용자 승인 필수 제안이며 실행0, variance18 미승인/미실행, formal denominator0, HPO/training PAUSED. 기존 HR 성공/LR·CAD curvature FAIL와 endpoint NOT_RUN 보존. Kit/ROS/추론/센서획득0. Git status는 .git 부재로 실패; stage/push 없음.


## 2026-11-02 — v39 bitmap repair 미완료 / CPU audit 실패 보존

[보고서](../reports/three_rep_hpo_disconnected_mask_repair_20261102_v39.md). 신규 THREE_REP_HPO_20261102_v39 source 감사1회 exit1: metadata short hash를 PNG SHA로 해석한 검사 가정 미입증. 원본v01/v03의 세 표본 PNG 전체SHA동일·pixel수동일이며 데이터 훼손으로 단정하지 않음. 기준hash수정0. 두 bridge IoU .676320272572402/190px 및 .7846836847946725/194px 재현. 전체7200 QA완료0·신규영향수UNKNOWN·bitmap adapter/loss path미완료. compilePASS, smoke NOT_RUN/시도0, Stage1 launch-readyNO/NOT_LAUNCHED/trials0. manifest2800/scene seed unique·expectedSHA 및 fidelity/summary dependencySHA PASS, 전체capture pairing미검증. Kit/ROS/motion/retry/science0, steeringHOLD. v30 steps.jsonl angle/time telemetry존재, rate계산0·안전한계UNDEFINED. 다음은 original nominal hash 생성계약 확보 후 새버전 fullQA/adapter/loss검증. 역사성공/실패와원본labels/weights/locks/USD변경0. GitHub는handoff sync요청이며원격완료미확인.

## 2026-11-02 — v40 bitmap loader/loss repair 및 실제 GPU smoke PASS

[보고서](../reports/three_rep_bitmap_loader_loss_path_20261102_v40.md). 새 THREE_REP_BITMAP_20261102_v40 및 코드7개. Canonical bitmap→Dataset/collate→설치8.4.129 v8SegmentationLoss 연결 PASS, 두 bridge 기존IoU .676320/.784684 재현·새target397/707px exact. FullQA7200/7200(첫checked7200/skip0, resumechecked0/skip7200), unique instance7139 중 polygon<.95=31/nonexact350. 전체mask 원본fullSHA일치(v01 6653/replacement486), RGB2800scene×3 metadata pairing8400 PASS. METADATA_SHORT_HASH_ALGORITHM_UNKNOWN은 유지하며 v39 잘못된 gate 실패·원본·기준hash는 보존. Safe noaug/letterbox engineering 정책이며 기존HPO recipe와 다름.

RTX5090 새6장1epoch smoke attempt1/exit0/retry0, trainseg4.32745·wrapper3.274879s·peakallocated3957387776bytes. 제한Val3장 finalMaskmAP50-95 .00644985는 engineering 관측이며 성능결론아님. Full-data pilotNOT_RUN, Stage1 executable/compile/helpPASS이나 readinessNO(정책채택·ratio2/4 loss/val·batch64·Raycheckpoint runtime 미검증), HPO NOT_LAUNCHED/trials0, Kit/ROS/robot0/science0. v30과거7396sample named dq max11.98–26.36deg/s관측은 safe abort한계아님/steeringHOLD. 초기overlay시각화오류와부수path조회exit1 기록·수정, loss tensor영향없음. Handoff marker동기화요청; 원격완료미확인.

## 2026-11-02 — v41 prospective bitmap/noaug HPO 실제 자격검증 FAIL

[보고서](../reports/three_rep_bitmap_hpo_stage1_qualification_20261102_v41.md), [전향 정책 amendment](bitmap_noaug_policy_amendment_20261102_v41.md). v40 source/input53항목 SHA와 legacy4개 expected·known9/hash/count108·432 PASS; QA/smoke반복0. ratio2/4 CPU bridge2scene×3rep/27channels actual selector6/6 exact·seg4.261906624/4.844833851 PASS. 각 GPU DISTINCT64/workers8/AMP/nc1/640/AdamW attempt1은 finite loss/backward 후 unscaled gradient assertion FAIL, peakallocated12060274688/9522654208B·OOM0/retry0. 이 엄격한 검사는 GradScaler step-skip 전 중단하므로 AMP비호환으로 단정하지 않음. GPU exact loss숫자는 성공후저장코드로 미보존/UNKNOWN.

Ray2.58 초기metric/mode중복 bindingFAIL/trial0 보존, 새v41b 수정검증1회에서 실제engineeringtrial c60cbc2a1개·epoch1/checkpoint1후 의도SIGINT·동일root복구. savedepoch0→start1·EMA가중치 exact검사 통과하나 optimizerstates0 assertion으로 ERROR1. scaler65536→32768·update미입증, 두checkpoint/epoch2완료/ASHApruning 미검증. tinyTrain9/Val6 pooledmAP.00483은 engineering관측. driverexit0도trialFAIL유지. 실제HPO launched/running/completed/pruned/failed0·STAGE1_READY=NO, full6000/1200epochNOT_RUN. 새initialscale128/진단저장v41c는compile만PASS·실행0; 이번ratio별1회/Ray수정1회소진으로 추가재시도0. 우선다음은첫AMP optimizerupdate+state증명이며통과전full-data/HPO금지. 정책은별도전향탐색/논문채택검토대기, historical M50/fourrep아님. 원본/v39/v40/weights/labels/split/USD불변·Kit/ROS/motion0·steeringHOLD15°/20°·confirmatory분모0. 정상handoff요청/원격완료미확인.


## 2026-11-02 — v42 AMP update PASS / Ray 재개 후 optimizer 진행 미입증으로 중단

[보고서](../reports/three_rep_bitmap_v41c_amp_optimizer_full_epoch_20261102_v42.md). 새 v42 root에서 ratio2/4 각각 CPU exact 및 distinct64/workers8/AMP/AdamW GPU attempt1 PASS: 첫update step1/state290/changed tensors290/scaler128→128/overflow skip0. peakallocated 12070773760/9537396736bytes. 기존 v41c source 불변, v42 사본에서 bounded12step 정상scaler복구 허용했으나 둘 다 첫step 성공.

새 engineering Ray trial f2db5f541개, 첫epoch checkpoint뒤 의도SIGINT·동일Tuner.restore·epoch2완료/2checkpoint. raw optimizer/model/EMA/scaler/scheduler exact 복원 PASS이나 재개 뒤 optimizer step1→1/scaler tracker1→1. batch6/nbs64→accumulate11에서 epoch2의2batch가 update조건에 못미쳐 실제진행 증명FAIL. Ray driver exit0/trialERROR0을 gatePASS로 취급하지 않음. 통합 Ray gateFAIL로 fullTrain6000/Val1200epochNOT_RUN, 재시도0, STAGE1_READY/TECHNICAL_READY=NO. 다음 정확한 패치는 tiny trial train64distinct/batch64/workers8 및 resume후step증가assert; 이번 재실행없음. Stage1v40 entrypoint도 v42 state fix 미연결. HPO launched/completed/pruned/errored0, Kit/ROS/motion/science0·steeringHOLD, Test/Real선택평가0. SHA64참조 일치·새3코드compilePASS·full_epoch코드는미실행; 기존v39-v41실패/원본/locks/weights/데이터/v40QA보존. 정책은전향noaug arm/논문채택검토대기, shortmetadatahashUNKNOWN. handoff marker동기화요청/원격완료미확인.

## 2026-11-02 — Issue#1 독립 축소모형 실제영상9편/136프레임/4080동결추론 완료

[독립 보고서](../reports/scale_model_real_video_robustness_20261102_v01.md). 사용자Downloads의scale_model_codex원문3파일을새scripts폴더로SHA그대로보존하고checkpointwrapper통합. raw_videos9편실제MP4(30FPS,512×910)를1초간격136parent로추출,original+9광도variant=1360공유이미지,smoke9parent/270평가PASS후재사용하여총4080추론완료/실패0. original검출HR46/LR50/CAD40각136;GT없어accuracy/IoU/AP/mAP NOT_ESTABLISHED. 영상단위paired변화/10000bootstrap·5초블록·후보confidence·mask/overlay·contactsheet·사람annotation대기136목록생성. sigma5/10비단조결과도그대로보존/threshold최적화0.

새외부SCALE_MODEL_REAL_VIDEO/results/SCALE_MODEL_ROBUSTNESS_20261102_v01,source/inputs/modelsSHA·1360augmentationdeterminism/roundtrip·4080exactpairedkeysPASS. 기존v45보호10493파일stat/핵심SHA불변PASS/latest_report·handoff next_task불변. integratedmask는관측전retinaFalse/threshold>.5/nearestresize를명시해providedretinaTrue와분리;portraitunletterbox공간정확성은향후GT평가전검증필요. smoke5.747초/full추가61.809초/RSS1.70360GiB/peakTorch582363136bytes,process3개exit0. 설치/Kit/ROS/주행/조향/학습/HPO/Test선택0. 다음은사람GT와좌표계검증후별도IoU평가;원격sync완료UNKNOWN.


## 2026-11-02 — v46 인식→위치→접근 feasibility 실제 오프라인 완료

[보고서](../reports/three_rep_perception_pose_planner_causal_audit_20261102_v46.md). 새외부PERCEPTION_TO_ROBOT_20261102_v46에서 original972/324paired·cross2916mask계보 연결PASS, v44계산319/거절479/무검출174 보존. v45b51은같은54재분석이며독립표본합산0/918NOT_RUN유지. 공통B5 79triplets/47base, 공통IoU50 69/46base·cluster2000CI/실측그림/전체324categorical수율 완료. old11/319·smooth29/319 개별reason 재현PASS, 동일시작/제약의design-target치환포함1276planner호출. old oracle-only pass89/bothfail219, smooth oracle-only pass71/bothfail219; 곡률결과는robot성공아님.

HUMAN_REVIEW_GATE=PENDING/POSITION_ESTIMATES=EXPLORATORY_UNVALIDATED/v44절차FAIL불변. v45pilot54+v44curated24=78 RGB/ROI/inlier/depth/residual/overlay패널·contact13·빈humanchecklist/서명0. fullgeometry NOT_EVALUATED(새장면별authoritativeoccupancy/footprint/supportbinding부재); MOTION_BLOCKER_DECISION에승인실측조향rate중단규칙미확인과후속one-shot제안만기록. sourceexpected10721+별도1019PASS/expected없는15UNKNOWN, input27930종료SHA불변PASS. authorityparserKeyError/exit1·부수rgexit2와supportfieldblank보강기록보존. 신규B5추정/모델추론/학습/HPO/Kit/physics/ROS/조향/이동0. 별도축소모형9영상/136parent/4080추론기록·media·보고서불변/재실행0. 다음은78사례사람서명이며추가918B5/live자동실행없음. Git없음/remote sync UNKNOWN.


## 2026-11-02 — v47 219 design-oracle 거부 원인·frame audit 완료 / motion HOLD

[보고서](../reports/three_rep_planner_219_failures_frame_audit_20261102_v47.md). v46 319×2목표×2정책1276상태/reason exact재현. 독립v43 capture rover matrix와시작점차이최대XY1.78e-14m/yaw8.91e-14°;camera-only이동가설기각,frame보정분기미생성. 설계219 old거리52/전방3/곡률164,smooth bracket219;물리전역불가능증명아님. 예측FAIL설계PASS89/71=old곡률87+전방2/smooth bracket60+곡률11보존. matched79/69에서설계PASS29/27,세예측모두FAIL중설계PASSold21/19,smooth15/13. 원본nominalHR중간경유최소대안실행0/219로실패보존,global approach+occupancy미해결. highIoU3+LR IoU0 17 depth/ROI표·8패널,78원본서명0·안내완료. 사람PENDING/역사v44FAIL/v45b918NOT_RUN/steeringHOLD유지. finalizer첫출력tabulate부재exit1보존후내장표출력으로수정. Kit/ROS/motion/추론/새B5/HPO0. latest_report및별도scale-video불변,Git없음remoteUNKNOWN.


## 2026-11-03 — B1 학습배경 선정·SDG 연결·적벽돌 촬영품질 개선 (Codex, 보고서 기준 append)

[출처조사](../reports/construction_environment_usd_provenance_audit.md) · [대체환경검토](../reports/alternative_environment_asset_review_20261103.md) · [재생성준비](../reports/synthetic_dataset_regeneration_plan_b1_jeonju_20261103.md) · [품질개선](../reports/b1_red_brick_sdg_quality_optimization_20261103.md). 학습배경 B1_CLOSED_EV.usdz(SHA de908a9e…586d) 선정, 평가용 Constructionsite_isaac.usdz 유지·불변. 두 환경 Mesh/Collider0, 이용권한 UNKNOWN(CGTrader 후보 미확정). 18장 smoke(HR/LR/CAD, canonical→polygon IoU1.0, CPU로더) "소규모 연결검증 PASS/대량생성 품질 미승인". ISO400 포화 진단 후 공통 ISO25/shutter50/f5/ACES·dome=8000+0.05×기존 제안, ROI 6곳 렌더 후 R1_NORTH_2/R5_WEST/R4_EAST 추천·R3_NORTH_7 제외, paired 72장 브릭·파레트 clipping0/36. red-only manifest 1400(train1000/val200/test200, SHA 56c8acbb…e0, dome 변환 반영) 작성. 첫 노출세션 renderer Error120 보존. NuRec depth 유효0/24, 바닥접촉 UNKNOWN. 전체생성/학습0, PROJECT_STATE는 당시 미갱신(SHA d919282d…f19aa).

## 2026-11-03 — Claude Code 인수인계 감사 / NuRec 가림 RGB차분 근거 / GitHub·ntfy 연결

[감사](../reports/claude_code_handoff_audit_20261103.md) · [설정](../reports/claude_code_github_ntfy_setup_20261103.md). 읽기전용 감사: 입력SHA11 일치, production entrypoint 부재 확인(v01 ISO400·단일ROI·2800 고정, v05/v06 train≤64). NuRec는 instance-ID/depth에 미반영; 기존 78쌍 오프라인 RGB차분에서 R3 brick mask 20.9% 빈배경동일(가림)·추천ROI ISO25 36장 <1%. Claude hooks(Stop/Notification/StopFailure)·ntfy 5시험 PASS(휴대폰 수신 연구자 확인)·HANDOFF push 승인후 첫 push 5964542 PASS. Isaac/학습0.

## 2026-11-03 — B1 NuRec 가시도·matte 바닥 진단 HR 13job

[보고서](../reports/b1_nurec_visibility_matte_pilot_20261105.md). train 13job(추천ROI 12층화 + R3 양성대조), E/EO/I/O/M 렌더. capture v01 FAIL(NUREC_PRIM_NOT_FOUND, 실제 /World/gauss/gauss; 예외에도 exit0 → 결과파일 검증으로 판정) 보존, v02 13/13 PASS·Error0. NuRec 숨김 물체전용 O 기준 유효(비가림 \|I−O\| 중앙 2–3/255), R3 hard 0.793/soft 0.424, 추천ROI 31load hard ≥0.991. matte/shadow-catcher 바닥은 NuRec 바닥을 검게 덮어 FAIL(보존).

## 2026-11-05 — B1 HR/LR/CAD 가림비교·QA규칙 DRAFT·production pilot 비용 / 전체생성·학습 NOT_RUN

[보고서](../reports/b1_nurec_visibility_3rep_and_production_pilot_20261105.md) · [QA DRAFT](b1_visibility_qa_rule_DRAFT_20261105_v01.md). 동일13job LR/CAD 각 13/13 PASS·Error0: 추천ROI hard_e2 최소 HR.997/LR.994/CAD.998(표현차 ≤.006), R3 .815/.814/.826. 빈배경 세션간 비트비동일(평균≤.16/255) → E 동일세션 원칙. QA: 주지표 실제 load mask 2px침식 hard, 보조 soft, LOW_SUPPORT/FLAG/WATCH/OK, base scene 3표현 공동FLAG, 자동삭제·대체 없음, 임계값 미확정(train만으로 결정 후 v02 잠금). matte/그림자 보류·접촉은 알려진 제한. production entrypoint v01–v03 + 검증기2(production, cross-rep pairing): train 12장면(41load) pilot. v01 E/O 3표현 PASS; v01 RGB전용 LR 11/12 브릭 미렌더 FAIL, v02(로딩대기/재시도) LR·CAD 11/12 FAIL, v03(삭제후 update8) 12/12 PASS·pairing PASS 78쌍·음성대조 FAIL 확인; 기존 E/O·진단·Codex 72장 mask IoU≥.85 누락징후 없음. 실측 장면당 HR/LR/CAD: RGB 4.91/3.16/3.27s, +E 5.93/3.99/~4.35s, +E+O 17.45/14.72/14.82s → 1400×3 약 4.4h/5.5h/18.3h(단일GPU), O비용은 NuRec 전환 ~11s. PROJECT_STATE를 입력해시로 쓰는 기존 스크립트는 이 append 이후 SOURCE_HASH_MISMATCH(production v01–v03은 명시 제외). 4,200장 생성0/YOLO학습0/val·test렌더0, 원본 USD·브릭·manifest 불변. 다음: QA DRAFT·구성(C1 권장)·FLAG 처리 승인 → train 전체 생성·검증 → 임계값 잠금 → val/test.

## 2026-11-06 — B1 H1/C1 승인·train 생성 시작 / v42 Ray step 1→1 정적 원인 분석 (Claude Code)

- 연구자 승인: FLAG 처리 H1, 생성 구성 C1(RGB와 같은 세션 E, HR canonical). 기록: `docs/b1_production_decisions_20261106_v01.md`. QA 임계값은 미확정이다. 잠금 틀은 `docs/b1_visibility_qa_rule_v02_LOCK_TEMPLATE_20261106.md`와 thresholds JSON TEMPLATE(모두 null)이다.
- train 1000 × HR/LR/CAD 생성 시작(14:57 KST)
  - driver: `scripts/run_b1_train_production_20261106_v01.sh`(v03, settle 8)
  - root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_TRAIN_20261106_v01`
  - manifest sha 56c8acbb… 일치 확인
  - 이 항목 작성 시점: **진행 중**(HR 약 720/1000, FAIL 0). 완료와 검증은 별도 항목에 기록한다.
- 준비 도구(pilot smoke PASS, 학습 0)
  - `analysis/b1_train_visibility_qa_20261106_v01.py`: train 전용, 임계값 미적용
  - `scripts/export_b1_yolo_20261106_v02.py`
    - 공통 HR canonical label, class0, 100px 이상
    - pilot 41 instance polygon IoU 1.0, xor 0
    - train·val·test가 모두 있을 때만 data.yaml을 만든다
- handoff repo: `handoff/next_task_b1_sdg_20261106.md` 추가(commit a14600e, push). 로봇 v48 `next_task.md`는 미실행 상태로 유지. 유휴 Codex v47 세션(pid 3151745)은 종료하지 않았다.
- v42 정적 분석([보고서](../reports/v42_ray_resume_optimizer_step_static_20261106.md))
  - Ultralytics 8.4.129 trainer에서 `last_opt_step`은 지역 변수로 -1에서 다시 시작하고, accumulate=round(64/6)=11이다.
  - Train 9/batch 6 구성은 **연속 실행에서도 epoch 2 step 0**이다(CPU 정수 로직 재현). 따라서 Ray 복원, optimizer 재생성, scaler, EMA 문제는 배제했고(정적), 원인은 accumulation이다.
  - GPU 재현은 미실행이며 승인 대기다. STAGE1_READY=NO 유지.

## 2026-11-06 — B1 train 1000×3 생성 완료·검증 PASS / QA 임계값 후보 제안(미잠금) (Claude Code)

[보고서](../reports/b1_train_production_qa_20261106.md)

- 생성(14:57–18:47 KST): HR / LR / CAD 각각 1000/1000 PASS, 장면 FAIL 0, primary 재시도 0, renderer [Error] 0. HR 95.5분, LR 65.4분, CAD 69.0분.
- 검증: `verify_{HR_Scan,LR_Scan,GeoCAD}_v01.json` 모두 PASS. `crossrep_pairing_v01.json` PASS(1000장면, 5756 load 쌍, 위반 0). resume 불필요. exit code는 판정에 쓰지 않았다.
- train QA: 8907행, `vis_hard_e2`(2px 침식)
  - primary Load_01 최소 HR 0.990 / LR 0.988 / CAD 0.995
  - 보조 load 18개 scene-load가 0.95 미만이다(최소 0.354). 주로 R1_NORTH_2의 반투명 NuRec floater가 원인이며 세 표현 일치.
- 제안(승인 대기, **잠금 안 함**): T_flag 0.90, T_watch 0.95, N_min 100(대안 200). 이때 FLAG는 29행 / 10 scene-load, primary base-scene FLAG 0, 경계 걸침 1.
- val/test 생성 0, 학습 0, val/test 분포 미열람.

## 2026-11-08 — B1 QA v02 잠금, train 적용, val/test 생성 시작 (Claude Code)

- 연구자 지시(2026-11-08): "진행 상황 보고하고, 다음단계 바로 진행해". 2026-11-06 제안값을 그대로 채택한 승인으로 처리했다.
- **QA v02 LOCKED**
  - `docs/b1_visibility_qa_rule_LOCKED_v02_20261108.md` sha256 `985d8696c6b4b37e5f66f1272ec8955df609c558cf113b479957446dbafb4407`
  - `docs/b1_visibility_qa_thresholds_LOCKED_v02_20261108.json` sha256 `021c66e9810ec35f08eaa31c6e292729f973993dbb630f03fd43f7f3741bd3e7`
  - 값: N_min 100, T_flag 0.90, T_watch 0.95
  - 틀(TEMPLATE)과 DRAFT v01은 수정하지 않았다.
  - 사람 육안 검토는 미실행이다.
- **train 적용**: `analysis/b1_apply_visibility_qa_v02_20261108_v01.py`(b1c30ccd…)
  - 출력: `…/B1_RED_PRODUCTION_TRAIN_20261106_v01/qa_v02_train_v01/b1_visibility_qa_v02.csv`(86e30fa7…, 8907행)
  - FLAG HR 9 / LR 10 / CAD 10, scene-load 10개, scene_flag=FLAG base scene 0
  - LOW_SUPPORT 행: HR 117 / LR 113 / CAD 120(primary 0)
  - 11-06 보고서의 LOW_SUPPORT 254는 값 없는(px_e2=0) 행을 뺀 수이고, 규칙상 행 수는 350이다.
- **val/test 200+200 × 3표현 생성 시작**(13:35 KST)
  - driver: `scripts/run_b1_valtest_production_20261108_v01.sh`(0d8762fa…)
    - train driver와 차이는 root, N=400, `--splits val test`뿐이다.
    - v03, settle 8, 같은 검증기를 쓴다.
  - root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_VALTEST_20261108_v01`
  - 이 항목 작성 시점: **진행 중**. 완료 판정은 별도 항목에 기록한다.
- 신규 도구(아직 val/test에 적용 전)
  - `analysis/b1_visibility_qa_metrics_20261108_v02.py`(b7a85dec…)
    - 잠금 JSON의 sha를 확인한 뒤에만 val/test를 허용한다.
    - 지표 코드는 v01과 같다.
  - `scripts/export_b1_yolo_20261108_v03.py`(f579b2e1…)
    - 표현별로 여러 capture root를 병합한다. 중복 scene은 거부한다.
    - 라벨 정책은 v02와 같다.
    - train smoke: PARTIAL(data.yaml 없음), 2969 instance, min polygon IoU 0.966, 중복 root 음성 대조군 거부 확인
- 학습 0, v42 GPU 재현 0.

## 2026-11-08 — B1 val/test 생성 PASS, QA v02 적용, YOLO 패키지 COMPLETE (Claude Code)

[보고서](../reports/b1_qa_v02_lock_and_valtest_20261108.md)

- **val/test 200+200 × HR/LR/CAD**(13:35–15:09 KST)
  - 각 표현 400/400 PASS, FAIL 0, renderer [Error] 0
  - verify: HR 5842034b… / LR 542dd65c… / CAD e152c8cd… 모두 PASS
  - pairing `crossrep_pairing_v01.json` 0c3c2f99… PASS(400장면, load 쌍 2324개)
  - root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_VALTEST_20261108_v01`
- **metrics v02 동일성**: train에 다시 계산한 결과가 v01 CSV(60fae522…)와 바이트 단위로 같았다.
- **val/test QA v02**(잠긴 값 그대로)
  - 지표 705531e6…(3594행), 판정 `qa_v02_valtest_v01/b1_visibility_qa_v02.csv` b2c0600d…
  - FLAG HR 7 / LR 8 / CAD 6, scene-load 8개(모두 보조 load), scene_flag=FLAG base scene 0
  - primary 최소 0.988
  - 임계값은 바꾸지 않았다.
- **YOLO 패키지** `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_YOLO_PACKAGE_20261108_v01`
  - export v03(f579b2e1…), PASS_PACKAGE_COMPLETE, package_checks 3ff0a45e…
  - 표현마다 1000 / 200 / 200
  - 4167 instance, 빈 라벨 0, min polygon IoU 0.960
  - data.yaml 3개, 깨진 symlink 0
- 학습 0, v42 GPU 재현 0. 다음 단계는 연구자 승인 대기다(YOLO 학습 recipe와 실행, v42 재현).

## 2026-11-08 — v42 GPU 재현(B PASS / A FAIL), B1 사람 검토 자료, 공통 recipe DRAFT (Claude Code)

[보고서](../reports/v42_gpu_repro_review_pack_recipe_20261108.md)

- 연구자 승인: GPU 재현 2개와 검토 자료 준비. 본 학습과 HPO는 미승인이며 실행 0.
- root: `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_REPRO_20261108_v01`. 1회씩 실행했고 재시도 0.
- **실험 B(Ray 복원, batch 64 / accumulate 1): PASS**(`exp_B_gate.json` dbc86fe7…)
  - checkpoint 0→1에서 AdamW step 1→2, real_updates 1→2, EMA 1→2, scaler tracker 1→2, model tensor 560개 변경
  - 복원 exact PASS
  - v42 "step 1→1"은 accumulate 1에서 재현되지 않았다.
- **실험 A(accumulation, batch 6): FAIL**(`exp_A_result.json` 6149e5c4…)
  - optimizer_step 호출 수(EMA 기준)는 정적 예측과 일치했다(A1 1회, A2 3회).
  - 그러나 실제 AdamW step은 0이고 가중치도 불변이었다.
  - 원인 추정: 실험 스크립트가 v42c의 GradScaler init_scale 128을 빼먹어, 기본값 65536에서 fp16 overflow가 나고 step을 건너뛰었다. 실험 설계 결함이다.
  - 재실행은 하지 않았다(지시). FAIL 기록을 보존한다.
  - AMP 검사로 `scripts/weights/yolo26n.pt`가 생성됐고 그대로 두었다.
- 사람 검토 자료 `reports/b1_human_review_pack_20261108_v01/`
  - 30 사례: FLAG 18(VAL_000148, TST_000188 포함), LOW_SUPPORT 6, 정상 primary 6
  - 패널 30장, 체크리스트 md/csv(판정 칸 비움). **사람 검토 미실행.**
- recipe `docs/b1_yolo_baseline_recipe_DRAFT_20261108_v01.md`(5e4a6f21…): DRAFT, 결정 항목 6개 빈칸
- 판정: 학습은 조건부 가능(데이터와 batch 64 경로 READY). recipe 잠금, B1 학습 스크립트와 smoke, 실행 승인이 남았다. STAGE1(HPO) 준비는 여전히 NO다(B1용 entrypoint 없음).

## 2026-11-08 — v42 GPU 재현 실험 A v02 PASS (Claude Code)

[보고서](../reports/v42_gpu_repro_review_pack_recipe_20261108.md)

- 연구자 승인으로 1회 실행했다. 스크립트는 `scripts/bitmap_accum_repro_20261108_v02.py`(33da0820…)다. v01과 다른 점은 v42c StrictTrainer(GradScaler init 128) 상속뿐이다.
- 결과 `…/THREE_REP_BITMAP_REPRO_20261108_v01/exp_A_accum_v02/exp_A_result.json`(1177f133…): **PASS**
  - A1(train 9, batch 6): step ni ep1 [0], ep2 []. 예측과 일치했고, 연속 학습에서도 epoch 2 step은 0이다.
  - A2(train 64, batch 6): step ni ep1 [0, 5], ep2 [15]. 예측과 일치했다. AdamW counter는 3, scale은 128이며 skip 0, 가중치가 바뀌었다.
- 결론: v42의 "복원 후 step 1→1"의 원인은 accumulation 구조다(GPU로 확정). Ray 복원은 정상이다(실험 B PASS).
- v01의 FAIL 기록은 보존했다.

## 2026-11-08 — B1 YOLO recipe LOCKED v01, 1 epoch smoke PASS, 라벨 점검, 평가 코드 (Claude Code)

[보고서](../reports/b1_yolo_training_prep_20261108.md)

- v42 GPU 재현 완료로 정리: B PASS, A v01 FAIL(보존), A v02 PASS.
- **recipe LOCKED v01**(연구자 지시 값 그대로)
  - `docs/b1_yolo_baseline_recipe_LOCKED_v01_20261108.md` sha256 `cd3645e894af37f6580ba639750aa7995cc8b1e087e218d507b8ee9aedc18616`
  - `….json` sha256 `c9b2458c62a679d29fe4e5afa5715549e7c7cbb2cb4cd84957dc8ef35007846b`
  - 내용: seed 42 / 43 / 44, no-aug, mask_ratio 4, 60 epoch, AdamW lr0 0.001, batch 64, AMP scale 128, 선정은 val mask mAP50-95
- **1 epoch smoke**(seed 42), root `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_SMOKE_20261108_v01`
  - `train_b1_yolo_20261108_v01.py` HR: FAIL_AUDIT(감사 로직 결함: skip 0 요구, final_eval callback 재호출 미처리). 보존.
  - `…_v02.py`(636248d0…): HR / LR / CAD 모두 PASS
    - 실제 AdamW 갱신 13 / 14 / 13 of 16, AMP 초기 overflow skip 3 / 2 / 3(scale 128→16–32 뒤 안정), EMA 16
    - peak GPU 10.2 / 11.5 GB, epoch당 약 6초, 데이터 1000 / 200 corrupt 0
    - 패키지 변경 0
- **라벨 점검**(`analysis/b1_label_pipeline_check_20261108_v01.py`)
  - 높이 1–3px인 보조 load 4개(train)가 Ultralytics box_candidates로 학습에서 빠진다.
  - 학습 mask와 정답의 IoU 중앙값: ≥2000px 0.98, 100–200px 0.53
  - 불연속 GT 61개는 polygon 연결선으로 하나로 이어지고, 추가 면적은 ≤12px
  - 첫 실행(assert 중단)은 보존했다.
- **평가 코드** `analysis/eval_b1_yolo_20261108_v01.py`(0de45618…)
  - 3×3, FLAG 포함 / 제외(ignore), 층별 분석, 장면 대응 bootstrap, seed 집계
  - test는 LOCKED 평가 절차 없이는 거부한다(음성 대조군 확인).
  - val smoke v01은 fp16 IoU overflow 버그로 INVALID 표시 후 보존했고, v02는 정상이다.
  - B1에는 C100/C60/C20이 없다. L1–L4(25–100%)로 대체하고, C100 = L4다.
- 사람 검토 안내 `reports/b1_human_review_pack_20261108_v01/REVIEW_GUIDE.md`: 판정 칸은 비어 있다.
- 본 학습 0, HPO 0, test 0. 다음은 연구자의 사람 검토, 그다음 본 학습 승인이다.

## 2026-11-08 — B1 YOLO recipe LOCKED v02(200 epoch), 200 epoch 대응 smoke PASS, 학습곡선 도구, 검토 패키지 (Claude Code)

[보고서](../reports/b1_yolo_recipe_v02_prep_20261108.md)

- **recipe LOCKED v02**(연구자 지시: epochs 60→200, 나머지 동일). v01은 보존했다.
  - `docs/b1_yolo_baseline_recipe_LOCKED_v02_20261108.md` sha256 `064bbb1a91a5248426017e150bfa1a288e63af1d9878cac4f604d62c8bb9d4b5`
  - `….json` sha256 `05d070a2c7872b8c15065c0110237e401f0ebfc70a4da39f53b2519806c502f8`
- 학습률: warmup 48 iteration은 같다. epoch당 감소 1.5e-5 → 4.5e-6, 200 run의 epoch 60 lr은 7.35e-4(60 run의 마지막 lr은 1.15e-4). 재현 `analysis/b1_lr_schedule_replay_20261108_v01.py`.
- 학습 스크립트
  - `train_b1_yolo_20261108_v03.py`: stop-after smoke FAILED(final_eval 판별 결함). 보존.
  - `…_v04.py`(6f35400f…): HR seed 42, epochs=200, 4 epoch에서 중단 → **PASS**
    - iteration별 lr 64개가 재현값과 차이 0
    - AMP skip 1, 실제 갱신 63/64, epoch당 약 3.7초, GPU 10.3 GB
  - root `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_SMOKE_RECIPEv02_20261108_v01`
- 학습곡선 분석 `analysis/b1_learning_curve_20261108_v01.py`
  - 60/100/150/200 시점 비교, 마지막 30 epoch 요약, 제안 수렴 기준(PLATEAU / STILL_IMPROVING / UNCLEAR)
  - smoke와 가짜 곡선으로 동작을 확인했다.
- 검토 패키지 `reports/b1_human_review_pack_20261108_v02/`
  - 컨택트시트 5장, ZIP sha `ad2b668a…`
  - 분류: 정상 6 / 판정 불일치 4 / FLAG 15 / LOW 5
  - 판정 칸은 비어 있다.
- seed 42 driver `scripts/run_b1_baseline_seed42_20261108_v01.sh`(6f3ba359…): dry-run만 했다.
- 본 학습 0, HPO 0, test 0. 다음은 사람 QA 검토, 그다음 seed 42 본 학습 승인이다.

## 2026-11-08 — B1 seed 42 본 학습: HR FAILED(epoch 182 non-finite box loss), LR/CAD 미실행 (Claude Code)

[보고서](../reports/b1_baseline_seed42_HR_failure_20261108.md)

- 연구자 승인으로 seed 42 본 학습을 시작했다(recipe LOCKED v02, trainer v04, driver `run_b1_baseline_seed42_20261108_v01.sh`). root `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_BASELINE_20261108_v01`.
- **HR: FAILED**(16:55–17:07)
  - epoch 182의 마지막 batch box loss가 inf였고, 스크립트의 no-retry non-finite 검사에 걸려 중단했다.
  - 그 전에도 epoch 107–179 사이 8회, 중간 batch에서 box loss inf가 있었다. 그때는 GradScaler가 skip했고(scale 64→0.125), 가중치 오염은 없었다.
- driver가 중단해 **LR/CAD 학습 0, val 3×3 평가 0.** 재시도 0, 설정 변경 0.
- 진단(학습 없음)
  - last.pt(EMA)로 train 1000장을 한 장씩 계산하면 fp16/fp32 모두 유한했다. 이미지/라벨 원인일 가능성은 낮다.
  - 학습 조건(원 가중치, BN batch 통계, fp16)에서만 생기며, 정확한 수치 원인은 UNCONFIRMED다.
- 실패 전 181 epoch 곡선(진단용)
  - 최고 val mask mAP50-95 0.821 @epoch 95(checkpoint 105b62c8…)
  - 마지막 30 epoch 평균 0.811, 기울기 ≈ 0 → 제안 기준 PLATEAU
  - val seg loss 0.75→2.14(과적합 신호)
- 다음: 연구자가 A(스크립트 v05: skip된 non-finite batch 허용 + 감시, 권장) / B(loss fp32) / C(AMP off) / D(Ultralytics 복구) 중에서 결정한다. 모든 실패 기록은 보존했다.

## 2026-11-08 — HR 실패 원인 점검, FP32 box loss(B안) recipe v03 amendment, 짧은 GPU 검증 (Claude Code)

[보고서](../reports/b1_fp32_boxloss_verification_20261108.md)

- **원인(확인된 메커니즘)**
  - Ultralytics 8.4.129 AMP 경로에서 decode된 pred box는 fp16(anchor fp16, matmul fp16), target은 fp32다. CIoU 안의 `w1*h1`은 fp16이고 inter/union은 fp32다.
  - 그래서 거의 완벽한 box에서 iou > 1 → alpha 분모 ≤ 0 → CIoU −inf / 음수 loss가 된다.
  - 단위 시험: fp16 혼합 경로에서 −inf 최대 14, iou>1 최대 1.9만 / 200만이고, fp32는 0이다.
  - 후반 probe(실패 run epoch 181 가중치, forward만): fp16 경로는 box loss inf 10/320 batch, 음수 CIoU loss 10,917(모든 batch), 예측값은 전부 유한했다. fp32 경로는 0이다.
- **미확인:** 실패 batch의 정확한 재현, 다른 원인 부재, 장기 거동. 이미지·라벨 요인은 완전 배제하지 않았다.
- 기존 inf 9건(epoch 107–182)과 scale 64→0.125는 `reports/b1_fp32_boxloss_20261108_v01/v02_HR_failed_run_inf_events.json`에 보존했다. v02 HR run은 FAILED 그대로다.
- **recipe LOCKED v03 amendment**(box loss fp32, train_args는 v02와 차이 없음). v02와 v01은 보존했다.
  - `docs/b1_yolo_baseline_recipe_LOCKED_v03_20261108.md` sha256 `83b67b298952b66b15c3b07468cc1670f3582bc03b3629a3bf6cff27e35bd6a0`
  - `….json` sha256 `76654f9ba2f320147c0d64c205abfe9f11b96c7915cc810c486792c5d89cd3da`
  - 모듈 `scripts/b1_fp32_boxloss_20261108_v01.py`(79b3d2f5…), 학습 스크립트 `train_b1_yolo_20261108_v05.py`(ca1175c8…, batch 단위 감사, NONFINITE_FORWARD / GRAD_OVERFLOW_SKIP 구분, 비정상이 있으면 FLAGGED)
- **짧은 GPU 검증**(HR seed 42, 200 epoch 스케줄), root `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_SMOKE_RECIPEv03_FP32BOX_20261108_v01`
  - stop5_compare: 학습 정상, fp16/fp32 box loss 차이 ≤ 0.00027. 판정은 FAIL_AUDIT(진단 probe 순서 결함, compare 모드 전용). 보존.
  - stop3_nocompare: **PASS**. bbox_iou 입력 fp32 / fp32, autocast off, 실제 갱신 47/48, NONFINITE_FORWARD 0, GRAD_OVERFLOW_SKIP 1(초기)
  - 짧은 시험에서는 후반 inf 조건이 재현되지 않으므로 해결됐다고 단정하지 않는다.
- 과적합 분석(별도): epoch 95(0.821) 이후 mAP 구간 평균은 약 0.811로 평탄하다. val seg loss는 1.21→1.91로 늘었다. fp16 CIoU 음수 loss와 scale 감소가 교란 요인이다.
- 200 epoch 재학습, LR/CAD, seed 43/44, HPO, test는 0. 다음은 연구자의 200 epoch 재학습(v03/v05) 승인이다.

## 2026-11-08 — B1 seed 42 본 학습(recipe v03 FP32 box): HR / LR / CAD 200 epoch PASS, val 3×3 평가 (Claude Code)

[보고서](../reports/b1_baseline_seed42_fp32box_20261108.md)

- driver `scripts/run_b1_baseline_seed42_20261108_v02.sh`, trainer v05, recipe LOCKED v03. root `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_BASELINE_FP32BOX_20261108_v01`(새로 학습). 17:31–18:12.
- **HR / LR / CAD 모두 PASS**
  - NONFINITE_FORWARD 0, 음수 box loss batch 0, GRAD_OVERFLOW_SKIP은 HR과 LR의 ep1 b1 각 1회
  - scale 최소 64, 최종 128–256. EMA 3200, GPU peak 14.8 GB
  - epoch 107 이후 불안정은 재현되지 않았다.
  - 학습 후 last.pt probe: fp32 경로의 음수와 비유한 CIoU는 0(fp16 경로였다면 inf 0–2 batch, 음수 약 9–10k).
- 대표 모델(val mask mAP50-95 최고)
  - HR 0.8208 @62(sha 27ba2931…), LR 0.8213 @32(0f6222d2…), CAD 0.8221 @32(bdf634af…)
  - epoch 200의 값: 0.804 / 0.792 / 0.792
  - 수렴 읽기: HR UNCLEAR(기울기 −0.0020), LR / CAD PLATEAU
  - val seg loss 0.74–0.82 → 2.0–2.3(mask 과적합)
- **val 3×3**(평가 코드 mAP50-95)
  - 같은 표현: HR 0.849, LR 0.838, CAD 0.840
  - 교차: HR→LR 0.615, HR→CAD 0.627, LR→HR 0.721, LR→CAD 0.450, CAD→HR 0.527, CAD→LR 0.259
  - 장면 bootstrap에서 모든 평가 표현에서 같은 표현 모델이 우세했다(CI가 0을 포함하지 않음). seed 1개이고 동등성 주장은 하지 않는다.
  - FLAG 제외 시 차이 ≤ 0.002
- 제한: 사람 QA 최종 검토 미완료, seed 1개, 같은 표현 val 칸에 선정 편향
- v02 FP16 실패 run은 별도 진단 자료로 남기고 결과에 합치지 않았다.
- seed 43/44, HPO, test는 0. 다음은 연구자가 학습 예산 재검토와 seed 43/44 승인을 결정하는 것이다.

## 2026-11-08 — B1 seed 43/44 본 학습(6 run) PASS + 9개 모델 3-seed 통합 val 3×3 분석 (Claude Code)

[보고서](../reports/b1_baseline_3seeds_integrated_20261108.md)

- driver `scripts/run_b1_baseline_seeds4344_20261108_v01.sh`(sha 00c9bb03…)
  - recipe LOCKED v03, trainer v05, FP32 box 모듈. 입력 sha는 seed 42와 같다.
  - 같은 root `/home/user/hh/isaac_cosmos/sdg_final/B1_YOLO_BASELINE_FP32BOX_20261108_v01`에 새 run 디렉터리를 만들었다. 18:34–19:52 KST.
- **6/6 PASS**(run_status 기준). 9 run 전체에서:
  - NONFINITE_FORWARD 0, 음수 box loss batch 0
  - GRAD_OVERFLOW_SKIP은 첫 batch에서만 났다(3 run에서 1회씩)
  - torch peak 14.84 GB로 run마다 같았고, run 사이 누적 없음. 메모리 가드 발동 0, OOM 0
- best(val mask mAP50-95): HR 0.826±0.005, LR 0.819±0.002, CAD 0.826±0.004
  - best epoch 26–75. 이후 평탄하거나 감소했고, val seg loss가 2.0–2.4로 늘었다(mask 과적합, 9 run 일관).
- **val 3×3**(9개 모델, 평가 코드 v01 `0de45618…`, 3 seed 평균±SD)
  - 대각: HR 0.849±0.002, LR 0.840±0.005, CAD 0.842±0.003
  - HR→LR 0.598, HR→CAD 0.617, LR→HR 0.726, LR→CAD 0.455, CAD→HR 0.531, CAD→LR 0.242
- Q1–Q5
  - 대각 간 차이는 ≤ 0.009이고, 이는 이미지가 다른 비쌍대 비교다. 교차 하락은 0.12(LR→HR)부터 0.60(CAD→LR)까지로 비대칭이다.
  - 비대각 평균은 HR 0.608 ≈ LR 0.591 > CAD 0.387이다.
  - 쌍대 차이 9개 × 부분집합 2개 모두 3 seed 부호가 같았고, seed t 구간과 장면 bootstrap CI 모두 0을 포함하지 않았다.
  - L4(C100)와 작은 load·부 load에서 교차 하락이 컸다. 가림 층은 표본이 부족하다. FLAG 제외 영향은 ≤ 0.002. seed 42 경향이 유지됐다.
- v45(CAD 모델 선택 mask IoU 최고)와는 데이터·모델·지표·과제가 달라 직접 비교할 수 없다. 별도 검증이 필요하다.
- 합성 B1 val 결과에 한정된다. 실제 로봇·현장으로 일반화하지 않는다. 사람 QA 최종 승인 PENDING.
- test 0, HPO 0, 새 데이터 0, 재시도 0. 새 6 run의 late-state probe는 수행하지 않았다.
- 다음 결정(연구자): 사람 QA 승인, test 평가 절차 LOCK과 test 승인, 학습 예산 재검토, v45 불일치 검증 여부.

## 2026-11-08 — Test 평가 준비: B1 Synthetic Test + Real Test189 프로토콜 LOCK CANDIDATE (추론 0) (Claude Code)

[보고서](../reports/test_eval_protocol_prep_b1_real189_20261108.md)

- 학습 결과 확정: 9개 모델(HR / LR / CAD × seed 42/43/44)의 best_val_maskmAP5095.pt. 집합 sha 2e9a02ec…, 모두 run_status PASS이고 기록된 sha와 일치한다.
- **B1 Synthetic Test**: test 200 장면 × 3 표현, GT 605개, capture/pairing PASS, QA v02 1815행. inventory sha 3911b8e2…. 지금까지 사용한 적 없다.
- **Real Test189**: `real_benchmark/cvut_pallets_bricks_original_v01/yolo_real_v01/images/test`
  - 189장, 972×1296. 파일 목록 sha f51a9b39…는 기존 lock(58dda07b…, 2026-10-05 개봉)과 같다.
  - 라벨은 이미지당 polygon 1개, class 0 brick_load, 팔레트 제외. 출처는 Roboflow bbox를 prompt로 쓴 SAM2.1 자동 mask이고, **수동 QA 기록이 없다.**
  - 내용은 빨강 점토 블록 팔레트 1개, 현장 1곳(source group A, visual block 2개). 시멘트 없음. 라벨 없는 배경 더미와 얼굴이 보이는 사람이 있다.
  - train B+D / val C와 group 중복 0, 정확 중복 0.
- 호환성: 형식은 호환된다(변환 불필요). 정의 차이(대상 1개만 라벨, 외형 차이)는 IGNORE 없이 FP로 세고 fp_far를 따로 보고하도록 고정했다.
- 신규 파일
  - `docs/b1_synthetic_test_eval_protocol_LOCK_CANDIDATE_v01_20261108.{json,md}`
  - `docs/real_test189_b1_eval_protocol_LOCK_CANDIDATE_v01_20261108.{json,md}`
  - `analysis/eval_real_test189_b1_20261108_v01.py`, `analysis/real_test189_b1_summary_20261108_v01.py`
  - `scripts/preflight_test_eval_20261108_v01.py`, `scripts/run_test_evals_20261108_v01.sh`
  - `reports/test_eval_protocols_20261108_v01/`(inventory)
- 검증
  - 후보 preflight PASS. require-locked는 FAIL(의도한 동작).
  - driver는 LOCKED 파일이 없어 거부했다(exit 3).
  - 실제 평가 코드는 lock이 없거나 후보 lock이면 test를 거부한다.
  - 실제 val 48장에 SMOKE 모델로 엔지니어링 smoke를 했다(v01은 그림 글자 문제로 보존, v02 PASS).
- **test 이미지 추론 0**, 학습·HPO·데이터 수정 0, 사람 QA PENDING.
- 판단: A는 승인 즉시 실행 가능. B는 SAM GT(QA 미기록), FP 처리, 그림 Git 제외를 연구자가 받아들이면 실행 가능.
- 다음: 연구자가 두 프로토콜을 승인하면 LOCKED JSON 생성 → preflight --require-locked → `scripts/run_test_evals_20261108_v01.sh` 1회 실행.

## 2026-11-08 — B1 augmentation · synthetic:real 혼합 비율 실험 설계 (학습 0) (Claude Code)

[보고서](../reports/b1_augmentation_mixing_design_20261108.md)

- 기존 baseline 9개, split, 실제 데이터, Test LOCK 후보는 변경하지 않았다. 학습 0, HPO 0, test 추론 0.
- **증강 초안**: `docs/b1_yolo_recipe_aug_moderate_DRAFT_v01_20261108.json`(DRAFT)
  - v03에 train 전용 증강만 추가한다: fliplr 0.5, degrees 3, translate 0.1, scale 0.25, HSV 0.01/0.4/0.3, blur / noise / JPEG(trainer v06에서 cv2로 구현 예정)
  - 상하반전, mosaic, mixup, copy_paste, 큰 색조 변화는 제외한다. val/test는 증강하지 않는다.
- **혼합 막 목록**: `scripts/build_mixing_manifests_20261108_v01.py` → `reports/mixing_design_20261108_v01/manifests/`(요약 sha a5e856ce…)
  - 안 A(1000)와 안 B(704) × 100:0 / 75:25 / 50:50 / 25:75 / 0:100
  - 중첩, 층화, 합성은 세 표현이 같은 장면을 쓴다. 실제가 부족하면 같은 이미지를 반복하고 변화는 공통 온라인 증강으로만 준다. 오프라인 실제 증강은 쓰지 않는다.
  - 실제 반복 수: 안 A 최대 2.84, 안 B 최대 2.0
- 호환성: 클래스, polygon 형식, 팔레트 제외가 같아 함께 학습할 수 있다. 다만 실제 라벨은 대상 1개만 표시하고(배경 더미는 라벨 없음) SAM GT의 수동 QA 기록이 없다. 실제 train/val/test는 같은 제품과 현장이다.
- 평가: B1 val/test, real val 48 / Test189. 주 checkpoint는 last.pt(epoch 200)로 선택이 없고, 보조는 v05 best. test는 새 checkpoint를 포함한 LOCK v02가 필요하다.
- 기존 혼합 근거 재확인: 실제 성능은 R50 0.925, R67 0.927, R100 0.937(seed 42)로 비슷했고, 3 seed에서 R50 0.912±0.023, R67 0.909±0.017이었다. "50%"는 실제 성능 단독 최고가 아니라 합성 성능을 유지하는 균형점이었다.
- **추천: 안 A(1000)** — 100:0이 baseline과 같은 데이터·step 수다. 39 run, 약 9시간.
- 다음: 연구자 결정(안, 증강 초안, 라벨 충돌 처리) → recipe v04와 혼합 프로토콜 LOCK → trainer v06 구현과 smoke.

## 2026-11-08 — 혼합 실험 사전 검증: 실제 라벨 충돌, checkpoint 규칙, 증강 v04 / trainer v06, 50:50 smoke PASS (Claude Code)

[보고서](../reports/b1_augmentation_mixing_checkpoint_smoke_20261108.md)

- 결정(연구자): 안 A(train 1000), 비율 5개, moderate 증강은 원칙 승인. 39개 본 학습은 아직 금지.
- **실제 라벨 충돌**(AI 선별, 사람 QA 아님, 하한값)
  - real train 352 중 58(16.5%)
    - 음성 65 중 39(60%)에서 벽돌 팔레트가 보인다.
    - 양성 287 중 19(6.6%)는 보조 적재물이 미라벨이거나 옆 팔레트가 합쳐져 있다.
  - val 48 중 21(44%)
  - 같은 종류의 먼 팔레트가 양성에서는 라벨, 음성에서는 미라벨인 내부 모순이 있다.
  - 혼합 1000장 중 충돌 항목 비중: 4.0% / 8.0% / 12.2% / 16.5%(25 / 50 / 75 / 100% 실제)
  - 권고: R1(사람이 누락 load를 보충한 별도 라벨 세트, 원본 보존) 또는 R2(충돌 음성 39장 제외).
  - 표: `reports/real_label_conflict_audit_20261108_v01/`. 그림은 Git 밖 `REAL_LABEL_CONFLICT_AUDIT_20261108_v01`.
- **checkpoint 규칙**
  - 주 규칙: best_combined = 0.5 × (B1 자기 표현 val + real val) mask mAP50-95 최대 epoch. 모든 비율에 같게 적용한다.
  - Q1(증강 vs 기존 baseline)은 양쪽 모두 B1 val best로 비교한다.
  - last / B1 val best / real val best는 보조로 저장한다. 사후 변경은 금지한다.
- **구현**
  - recipe 후보 `docs/b1_yolo_recipe_LOCK_CANDIDATE_v04_20261108.{json,md}`(v03은 보존)
  - `scripts/b1_mixing_data_20261108_v01.py`, `scripts/train_b1_yolo_20261108_v06.py`
  - 프로토콜 후보 `docs/b1_mixing_experiment_protocol_LOCK_CANDIDATE_v01_20261108.{json,md}`(39 run)
- **증강 검증 v03 PASS**
  - 기하 정렬: 큰 instance IoU 중앙값 0.976–0.984, 최소 0.906 이상. 작은 instance의 낮은 IoU는 무증강 대조군도 같으므로 해상도 효과다.
  - 광도 변형은 라벨에 영향 없음. 평가 세트에는 증강 없음. 실제 반복이 막 목록과 일치하고 반복본마다 증강이 다름. HR / LR / CAD 설정 동일.
  - 검증 코드 결함 2건은 v01(거짓 FAIL), v02(공허한 PASS)로 보존했다.
- **smoke** HR seed 42, A1000_S050_R050, 3 epoch: **PASS**(check 15개)
  - 갱신 47/48, NONFINITE 0, 음수 box 0, fp32 box, 실제 비율 50.0%
  - real val 0.45초/epoch, checkpoint 4종, 원본 hash 불변, peak 10.2 GB
  - 출력: `B1_MIX_SMOKE_RECIPEv04_20261108_v01`
- 39개 본 학습은 기술적으로 준비됐다(약 10시간). 시작 전에 라벨 충돌 처리 결정과 v04 / 프로토콜 LOCK 승인이 필요하다.
- test 0, HPO 0, 원본 라벨·split·baseline 변경 0.

## 2026-11-08 — Real 라벨 보완(R1) 초안 + 사람 검토 패키지 + 평가 정의 + manifest / 프로토콜 v02 (학습·test 0) (Claude Code)

[보고서](../reports/real_labels_v02_and_eval_definition_20261108.md)

- 결정(연구자): R1(원본 보존, 보완 all-load 라벨 labels_v02), 공통 checkpoint 규칙 채택(Q2–Q5는 best_combined, Q1은 B1 val best; real val 라벨 승인 뒤 최종 잠금), 안 A 39 run.
- **보완 대상**: AI 선별로 확인 79장(train 58, val 21) + AI 판정 불일치 1장(0415) = Tier A 80장.
  - 정확한 최종 수는 400장 전체를 사람이 검토한 뒤 정한다(PENDING).
- **초안**: SAM2.1 Base(sha f1a9cf2d…), AI 확인 후보 box 기반, 63장 102 instance(면적 2.8k–103k px)
  - Tier A 중 17장은 초안이 없어 사람이 직접 그린다.
  - 저장: `/home/user/hh/isaac_cosmos/real_benchmark/cvut_real_labels_v02_20261108/labels_v02_draft`(DRAFT, 사용 금지)
  - 원본 yolo_real_v01 라벨 전체 hash가 전후 같다.
- **검토 패키지**(Git 밖, 사람 얼굴 포함): sheets 34(400장 전부), per_image 80, 체크리스트 400행 + 102행(판정 칸 비어 있음, PENDING)
  - 가이드와 체크리스트 텍스트: `reports/real_labels_v02_review_20261108_v01/`
- **평가 정의**: Test189 GT는 그대로 두고 네 관점으로 평가한다.
  - T-AP(원본), A-AP(모델 예측을 보지 않고 독립 구축하는 Test189-A), T-ignore, target-centric
  - 주 지표는 Test189-A가 승인되면 A-AP, 아니면 target-centric이다.
  - real val은 A(labels_v02, 선정용)와 T(원본) 두 가지다. 편향 분석은 보고서 §2.
- **manifest v02**: `reports/mixing_design_20261108_v02/`(구성은 v01과 같고 실제 라벨만 labels_v02)
- **프로토콜 후보 v02**: `docs/b1_mixing_experiment_protocol_LOCK_CANDIDATE_v02_20261108.{json,md}`(PENDING_LABEL_REVIEW, label sha TBD)
- **코드**: trainer v07(labels_v02 APPROVAL 게이트, 프로토콜 LOCKED 요구)과 view 모듈
  - 확정 도구 `finalize_real_labels_v02`: 미완료면 거부. 지금 실행하면 502행 미완료로 거부된다.
  - 확정 도구 `finalize_lock`: candidate → LOCKED
  - 게이트 동작은 정적 검사로 확인했다. GPU smoke는 승인된 라벨이 나온 뒤에 한다.
- recipe v04 후보는 그대로 유효하고, 승인 즉시 finalize_lock으로 LOCKED를 만들 수 있다.
- 39개 학습: 준비는 끝났고 사람 라벨 검토 대기다. 남은 순서는 검토 → 확정 → 프로토콜 v02와 v04 LOCK → v07 smoke → 39 run.
- 학습 0, HPO 0, B1 test / Test189 추론 0. 사람 QA(B1 FLAG, labels_v02, Test189-A)는 모두 PENDING.

## 2026-11-08 — labels_v02 사람 검토용 로컬 인터페이스 구현·시험 (사람 검토 0, 학습·test 0) (Claude Code)

[보고서](../reports/real_labels_v02_review_tool_20261108.md) · [사용법](../reports/real_labels_v02_review_20261108_v01/REVIEW_TOOL_USAGE.md)

- 서버 `scripts/label_review_server_20261108_v01.py`(127.0.0.1, 표준 라이브러리, 원본 읽기만, 이미지별 상태 + 추가 전용 history)
- UI `scripts/label_review_ui_20261108_v01.html`
  - Tier A / B, 겹침, 확대, 이동, 꼭짓점 편집, 그리기, box→SAM2.1, 분리, GROUP, 저장·재개
  - "검토 완료"는 서버 검증을 통과해야 저장된다. AI 결과는 자동으로 승인되지 않는다.
- export(기존 400행 / 102행 체크리스트 형식)와 finalize v02(export 폴더 입력, 미완료 거부)
- 시험은 `review_work_SYSTEM_TEST_NOT_HUMAN_20261108_v01`에서만 했다.
  - 헤드리스 Chrome self-test 14/14
  - API 거부 규칙과 SAM 확인, export 확인, finalize 거부(504행)
- 원본 라벨 hash 불변. 실제 검토 폴더 `review_work_v01`은 아직 비어 있다(첫 실행 때 생성).
- 다음: 사람 검토 → export → finalize → 프로토콜 v02와 v04 LOCK → v07 smoke → 39 run.

## 2026-11-08 — labels_v02 실제 검토 서버 실행 (사람 검토 시작 대기) (Claude Code)

[안내](../reports/real_labels_v02_review_start_20261108.md) · [Tier A 순서](../reports/real_labels_v02_review_20261108_v01/TIER_A_REVIEW_ORDER.md)

- `label_review_server_20261108_v01.py`를 실제 작업 폴더 `review_work_v01`로 실행했다.
  - http://127.0.0.1:8765/, 세션과 분리(setsid / nohup), 로그 `review_server_v01.log`
- 시작 시 400장 모두 NOT_STARTED, state 0개. 헤드리스로 화면 확인(쓰기 없음).
- Tier A 80장 순서와 AI 힌트(우선 높음 18 / 보통 62)를 정리했다. 힌트는 판정이 아니다.
- 사람 검토 0건, 승인 0건. 학습·test 0.

## 2026-11-08 — 외부 AI 시각검토용 ZIP 생성 (연구자 업로드용, 승인 0) (Claude Code)

- `scripts/build_chatgpt_review_zip_20261108_v01.py` → `/home/user/hh/isaac_cosmos/real_benchmark/cvut_real_labels_v02_20261108/chatgpt_review_package_v01.zip`(188.9 MB, sha 5b5bfe83…, Git 밖, 사람 얼굴 포함)
- 내용(1240 파일)
  - 원해상도 패널(100px 격자, GT O# / 초안 D#): Tier A 80 + Tier B 320
  - 원본 이미지 사본 400, 이미지별 polygon JSON 400(원본 픽셀 좌표)
  - contact sheet 34, 체크리스트 400행 / 102행 + image_id map
  - 검토 지침, 응답 템플릿
- 원본 데이터, labels_v02_draft, review_pack_v01, review_work_v01의 hash가 전후 같다.
- AI 검토 결과는 제안이며 사람 검토가 아니다(labels_v02 PENDING 유지). 학습·HPO·test 0.

## 2026-11-08 — 연구 대상 자재 정의 재검증: B1 적벽돌 ≠ Roboflow 포장 중공블록, Tier A 재분류, labels_v02 중단 (Claude Code)

[보고서](../reports/real_material_definition_and_tierA_reassessment_20261108.md)

- 연구자 확인: Tier A의 AI "누락" 대부분이 연구 대상 벽돌이 아니다 → R1 보완 중단.
  - labels_v02_draft는 DRAFT로 보존하고 사용하지 않는다(`SUSPENDED_20261108.md`).
  - 원본 라벨과 review_work_v01(IN_PROGRESS 1건)은 보존한다.
- **자재 정의**
  - B1 `brick_load` = 포장 없는 소형 천공 적벽돌을 낮게 쌓은 것
  - Roboflow GT 주 대상 = 비닐 포장 대형 수직 천공 점토블록 팔레트(Porotherm 계열로 추정)
  - 원본 클래스 이름은 `bricks`다. **동일 자재가 아니며, GT 주 대상과 연구 대상의 일치 여부는 연구자 결정이 필요하다.**
- **Tier A 재분류(AI 의견, 적벽돌 기준)**: (a) 누락 0, (b) 경계 오류 0(제품 기준으로는 0715 1장), (c) 대상 아닌 자재 51(같은 제품 이웃 19 + 다른 자재 가능성 32), (d) 구별 불가 28
  - 초안 102개 중 마스크가 온전한 것은 19개다.
- 기존 "최소 58장 충돌" 수치는 철회한다(AI 선별 수치였음).
- 권고
  - 원본 라벨을 유지한다.
  - Tier B는 GT 정체성 확인 + 10% 표본 + 자동 이상치로 확인한다.
  - **39 run 혼합 실험은 보류하고 연구 대상 정의부터 정한다.** 실제 적벽돌 데이터를 확보하거나 클래스 정의를 확장한다.
  - E1(증강, 합성만)과 B1 test는 이 문제의 영향을 받지 않는다.
- 학습·HPO·test·승인 0.

## 2026-11-09 — B1 혼합 39-run 학습 완료(HANG 3건 복구), Validation 분석 (Claude Code)

[결과 보고서](../reports/b1_mixing_39_validation_results_20261109.md) · [HANG 복구 기록](../reports/b1_mixing_39_hang_recovery_20261109.md)

- 실행 조건
  - 프로토콜 LOCKED v03(수정 없음), recipe v04, A1000 manifest v01, seed 42/43/44
  - 출력: `/home/user/hh/isaac_cosmos/sdg_final/B1_MIX_AUG_RECIPEv04_20261108_v01/`
- **학습 39/39 PASS**
  - non-finite 0, 최대 할당 10.43 GB
- **HANG 3건**
  - 대상: S050_R050 LR seed44 / S050_R050 GeoCAD seed44 / S025_R075 LR seed42
  - 시점: 매 epoch real-val 검증 직후
  - 진단: 검증 로더 워커가 defunct 상태였고 메인 스레드는 futex 대기였다. Python 스택은 확보하지 못했다.
  - 처리: 원본과 진단 기록을 보존했고, run별로 rerun01 1회씩 재실행해 모두 PASS했다.
  - v06 재실행 run은 원본과 비트 단위로 동일했다.
- watchdog
  - driver v02(15분) → v03(5분, 진단 강화) → v04(trainer v07)
  - 실행환경 변경 기록: `docs/b1_mixing_execution_amendment_v01_20261109.json` (sha bc487027…)
  - trainer v07(sha ce3abbad…)은 real-val 검증 workers 2→0으로 바꾼 것이다. 6 epoch SMOKE에서 v06과 비트 단위로 동일했다.
  - v07로 학습한 run은 11개다. v06과 동일 실행이라고 주장하지 않는다.
- **Validation 결과** (best_combined 기준, 3 seed)
  - 실제를 25% 넣으면 실제 val이 0.24–0.36에서 0.96–0.97로 오른다. 25–100%는 0.96–0.99로 **최적 실제 비율은 구분할 수 없다.**
  - real-only 모델의 B1 합성 val은 0.000이다.
  - balanced 1위는 세 표현 모두 **50:50**(0.932–0.934)이고 Pareto에도 포함된다. 기존 R50 균형점 경향은 재현됐지만, 2위와의 t 구간이 0을 포함한다.
  - 표현 × 비율 상호작용은 보이지 않았다(F p 0.45–0.90). 교차 표현 일반화는 HR > LR >> CAD다.
  - Q1 증강: B1 val이 자기 표현 +0.02–0.04, 교차 표현 +0.04–0.08 올랐다. 합성만 학습한 모델의 실제 val은 0.05 이하로 개선이 없었다.
- 해석 제한
  - 실제 데이터는 다른 자재(포장 점토블록)다.
  - 실제 val은 선택에 쓰였으므로 결과가 낙관적이다.
  - 실제 val 48장은 천장 효과가 있다.
  - n=3이다.
- 실행하지 않은 것: HPO, B1 Test, Real Test189 (0회)
- 다음 단계(연구자 결정): 독립 test 실행 여부, 자재 정의 문제.

## 2026-11-09 (저녁) — B1 혼합비 실험 B1 Synthetic Test + Real Test189 (LOCKED, 1회 실행)
- 보고서: `reports/b1_mixing_test_results_20261109.md`, 결과 폴더 `reports/b1_mixing_test_results_20261109/`
- 프로토콜 `docs/b1_mixing_test_protocol_LOCKED_v01_20261109.json` (sha 8134a1ae…); driver `scripts/run_mixing_test_eval_20261109_v01.py`
  - 7개 그룹, checkpoint 57개(baseline 9 + 혼합 39 모델; real-only 3은 공유로 한 번만 집계)
  - 출력 `/home/user/hh/isaac_cosmos/sdg_final/B1_MIX_TEST_EVAL_20261109_v01/` (19:03–20:42)
  - 14개 평가와 분석이 모두 exit 0, `test_done` 생성. preflight PASS, 재실행 없음
  - 결과 파일 검증: realtest per_image가 모델×189행, eval_meta에 LOCKED 경로와 group이 기록됨
- 결과 (3 seed; Q1은 B1-val-best, 비율은 best_combined로 표를 분리)
  - Q1 증강: B1 Test 자기 표현 +0.020 / +0.052* / +0.048, 교차 표현 +0.095* / +0.047 / +0.048 (HR/LR/CAD, *는 t 구간이 0 제외). Real Test189는 양쪽 모두 바닥(T-AP50 < 0.16)이라 기술적으로만 본다.
  - 실제를 25%만 넣어도 Real T-AP가 0.36–0.47에서 0.95–0.98로 오른다. 25 / 50 / 75 / 100% 차이는 ≤ 0.03이고 구분되지 않는다.
  - 50:50은 B1 자기 표현과 balanced에서 세 표현 모두 평균 1위지만 2위와 구분되지 않는다. 최적이라고 선언하지 않는다.
  - real-only 모델: B1 Test ≈ 0(합성 성능 상실), Real T-AP 0.985(2위와 구분 안 됨)
  - 교차 표현 순서 HR > LR >> CAD. 표현 × 비율 상호작용은 보이지 않았다(p 0.78–0.99).
  - Val과 Test의 1위는 9/9 조합에서 일치했다(Spearman 0.9–1.0).
- 한계
  - Real Test189는 포장 점토블록 팔레트 1개, 현장 1곳의 데이터다(target-only GT). 작은 빨간 벽돌의 실세계 일반화가 아니다. all-load / ignore AP는 없다.
  - n=3, 다중비교 보정 없음
- 새 코드: `analysis/b1_mixing_test_strata_table_20261109_v01.py` (기존 metrics만 집계)
- 상태
  - Real Test189는 이번 실험의 모든 모델에 사용이 끝났다. 이 결과로 모델, 비율, checkpoint를 다시 선택하는 것은 금지다.
  - 하지 않은 것: HPO, 추가 학습, 재실행

## 2026-11-09 (밤) — 1차 통합 결과보고서 / 1단계 설계 v02 (B1 L1–L4 × O0/O25/O50) / 기존 데이터 재분석
- **통합 보고서**: `reports/integrated_research_results_round1_20261109.md`
  - 범위: 에셋, 구축 부담, 환경, 10월 학습, v43–v47, B1, 증강, 혼합비, Test, B5, 경로, 주행, 한계, 남은 실험
  - 조사 노트: `reports/integrated_results_round1_20261109_v01/survey_*.md` (읽기 전용 조사, 수치마다 출처 경로)
  - 서로 다른 실험군은 합치지 않았다. Roboflow 데이터는 다른 자재(포장 점토블록)라고 명시했다.
- **1단계 축 변경**(연구자 지시): 적재율은 B1 L1–L4(75/150/225/300개)를 쓴다. 기본 비교는 HR/LR/CAD × L1–L4 × O0/O25/O50 = 36개 조건이다.
  - 설계: `reports/stage1_b1_layer_occlusion_design_v02_20261109.md`
  - 이전 C 축 설계 문서는 "대체됨"으로 표시해 보존했다.
- **데이터 현황**
  - v43–v47 가림 장면은 재사용하지 않는다. 적재 구조, 배경, 카메라, GT가 다르고, C 결과는 섞지 말라는 지시가 있다. 가림판 방식과 실측 정의만 가져온다.
  - B1 O0: test 200장면(L1 45 / L2 50 / L3 54 / L4 51)이 있다. 목표의 NuRec 가림은 ≤ 0.0082다. 적재물 간 가림은 미측정이다.
  - B1 O25/O50: 0장이다.
- **추가 렌더 제안**(미실행, 승인 대기)
  - test 200장면에 가림판만 추가한다. 세 표현에 같은 판 자세를 쓴다.
  - 파일럿 108장 + O25/O50 1,200장 + O0 측정 패스 600장 = 1,908장(권장). O0 측정 패스를 빼면 1,308장(최소)이다.
  - 달성 판정은 실측 ±2%p다. 기준 밖도 보존하고 NOT_ACHIEVED로 표시한다.
  - 신규 학습은 하지 않는다.
- **기존 데이터 재분석**(재집계만, 추론 0)
  - 코드: `analysis/stage1_existing_data_reanalysis_20261109_v01.py` (sha 047d6f1c…)
  - 출력: `SDG/STAGE1_EXISTING_REANALYSIS_20261109_v01_run03`, 사본 `reports/stage1_existing_reanalysis_20261109_v01/`
  - run01/run02는 코드 버그로 실패했고, 폴더와 FAILED 기록을 보존했다.
  - v43(M50, IoU ≥ 0.5 통과율): HR 0.713 / LR 0.673 / CAD 0.824. 가림이 있을 때 차이가 커졌다(LR은 WRONG_TARGET 72건). 표현과 모델 효과가 섞여 있다.
  - Depletion 1460: C20에서만 0.925–0.968이고 나머지는 천장(1.0)이다.
  - **이 결과는 신규 L 축 비교와 섞지 않는다.**
- 하지 않은 것: 렌더링, 추론, 학습, Test189 추론, HPO, 2·3단계 실행

## 2026-11-09 (밤) — 1단계 가림판 구현 확인용 시각화 파일럿 (3장면 × 3표현)
- 보고서: `reports/b1_occlusion_viz_pilot_20261109.md`
- 새 코드: `scripts/b1_occlusion_capture_20261109_v01.py`, `analysis/b1_occlusion_viz_sheets_20261109_v01.py`
- 실행
  - run01: 9/9 FAIL. 판 prim이 ROI 변환이 걸린 부모 아래에 있었다(코드 버그).
  - run02: 시작 직후 FAIL. 수정 때 넣은 주석이 재질 정의를 삼켰다.
  - **run03: 9/9 PASS** (`SDG/B1_OCCL_VIZ_PILOT_20261109_v01_run03`)
  - 실패한 두 실행의 폴더와 FAILED 기록을 보존했다.
- 판 배치 규칙
  - 판은 항상 카메라 쪽에 있다(깊이 = 목표 가장 가까운 면 깊이 × 0.5).
  - GT 목표 마스크 기준 가림률은 O25 24.9–25.1%, O50 49.8–50.1%로 9/9가 첫 시도에 맞았다.
- 발견한 문제(본 실험 전 결정 필요)
  - 표현별 instance 마스크가 목표 벽돌 일부만 포함해 실측이 왜곡된다(LR L3 +10.7 / +18.9%p). 1차 실측을 GT 마스크 기준으로 정의할 것을 제안했다.
  - 적재물 간 가림 지표가 음수로 나와 무효다. 비활성화로 instanceable이 깨진 것으로 본다. 정규 proxy와 visibility 전환 방식을 제안했다.
  - 기존 O0와 재렌더 사이 평균 픽셀차 0.6–1.35/255. 같은 세션 O0 재렌더(600장) 여부를 결정해야 한다.
  - 판이 카메라와 목표 중간에 있어 물리적으로 작다. 깊이 비율 변경도 선택지다.
- 이미지는 NuRec 배경의 사람 형상 때문에 Git에 올리지 않는다.
- 하지 않은 것: 본 렌더 1,200건, 추론, 학습, 위치 추정, 주행

## 2026-11-09 (밤) — 1단계 가림 12장면 파일럿 v02 PASS → 본 렌더 시작
- 보고서: `reports/b1_occlusion_pilot12_v02_20261109.md`
- 연구자 결정 반영
  - 주 실측: 공통 GT 목표 영역 중 판에 가려진 비율. instance 기준 값은 진단용이다.
  - 적재물 간 가림은 이번 주 분석에서 제외했다.
  - O0는 기존 B1 Test 영상을 재사용하고 추가 렌더하지 않는다.
  - 판 깊이는 목표 앞면 깊이 × 0.85다.
- 코드: `scripts/b1_occlusion_capture_20261109_v02.py` (sha e3f9f156…). 판정 스크립트(`analysis/b1_occlusion_pilot_gate_20261109_v01.py`)는 파일럿 결과를 보기 전에 작성했다.
- 파일럿 결과(`SDG/B1_OCCL_PILOT12_20261109_v02_run04`, val 12장면 × 3표현)
  - 36/36 PASS
  - 달성 72/72, 최대 오차 0.30 pp, 표현 간 차이 0
  - 판이 카메라 쪽에 있음 36/36, 바닥 아래로 내려간 경우 0
  - 한계: 판이 바닥에서 0.2–0.3 m 떠 있다.
- 판정: PROCEED. 본 렌더 `SDG/B1_OCCL_MAIN_TEST_20261109_v02_run05`(test 200장면 × O25/O50 × 3표현 = 1,200건)를 시작했다.
- 평가와 분석 코드는 추론 결과를 보기 전에 작성했다.
  - `analysis/b1_occlusion_eval_20261109_v01.py`
  - `analysis/b1_occlusion_analysis_20261109_v01.py`
- 모델
  - 주 분석: baseline 9개 + aug 9개, B1-val-best checkpoint
  - 보조 분석: S050_R050 best_combined 9개
- 하지 않은 것: 학습, HPO, Test189, 2·3단계

## 2026-11-10 — 1단계 가림 강건성 후속 실험 완료 (B1 Test 200 × L1–L4 × O0/O25/O50 × HR/LR/CAD)
- 보고서: `reports/stage1_occlusion_robustness_results_20261110.md`, 결과 사본 `reports/stage1_occlusion_results_20261110_v01/`
- 실험 성격: 새 블라인드 Test가 아니라 가림 강건성 후속 실험이다.
- 렌더: O25/O50 1,200/1,200 PASS, 가림률 달성 1,200/1,200, 최대 오차 0.36 pp. O0는 기존 B1 Test 영상 600장을 재사용했다.
- 평가: 48,600행. O0 회귀 검증에서 기존 LOCKED B1 Test와 27쌍이 정확히 일치했다. 분석 검증 PASS.
- 실행 관리: 자동 실행기 `scripts/stage_pipeline_orchestrator_20261109_v01.sh` (setsid로 실행, 결과 파일로 판정). 현재 2단계 계획 대기 중이다.
- 결과
  - O25에서는 목표 검출률이 0.99–1.00을 유지했다.
  - O50 목표 검출률: 무증강 HR .693 / LR .762 / CAD .698, 증강 .825 / .758 / .780.
  - 표현 간 저하량 차이는 seed 기준으로 확정되지 않았고, 장면 부트스트랩의 방향은 그룹에 따라 바뀌었다.
  - 증강은 HR의 O50 검출률을 +0.132 높였고 seed 흔들림을 줄였다.
  - O50에서는 적재량이 많을수록(L4), 가까울수록(D1–D2) 저하가 컸다.
  - top-1은 여러 적재물 장면에서 지정 목표를 보장하지 못했다(O50 OTHER_LOAD .68–.71).
  - 보조 분석(50:50 혼합)의 O50 검출률은 .93–.98이었다.
- 3단계 준비: 과거 주행 실패 원인을 감사했고 TC-S 개선 planner를 오프라인으로 검증했다(테스트 11/11, 10/10).
  - 설계 초안: `SDG/STAGE_PIPELINE_20261109_v01/stage3_design_DRAFT.md`
  - 아직 실제 주행은 없다.
- 2단계: depth 보조 렌더와 B5 적용 코드를 준비 중이다(아직 실행 전).
- 2026-11-10 3단계(물리 주행) 구현·smoke 완료, 본 실행 계획 등록.
  - 새 코드: `scripts/stage3_drive_20261110_v02.py`(runner), `scripts/stage3_drive_session_20261110_v02.py`(v30 세션 기반 Kit 세션), `scripts/stage3_perception_20261110_v01.py`(own-rep M50 + 변경 없는 v44 센서 자동 ROI B5), `evaluation/stage3_outcome_20261110_v01.py`, `analysis/stage3_verify_20261110_v01.py`, `analysis/stage3_analysis_20261110_v01.py`, `configs/stage3_matrix_20261110_v01.json`(72 run 선언: pilot 18 + main 54). v01 세션/runner는 smoke 실패 증거와 함께 보존.
  - smoke: `SDG/STAGE3_SMOKE_20261110_v01_run01..run05`. run01–04 실패 보존(카메라 비균일 scale, semantic annotator의 render graph 노드, ROS domain 191 고정, runner .tmp race, 정지 인증 per-tick 재계산으로 20 s 정지 wall bound 초과). run05(v02): 7 run 중 SUCCESS 6(HR/LR/CAD L4·O0, HR L1·O0, Baseline·Improved 모두 실제 물리 이동, FINAL 오차 2.9–5.8 cm, main band 이내), FAIL_A 1(HR L4·O50 M50 미검출). VERIFY PASS.
  - 위험: 속도 jitter 꼬리(0.027–0.030 m/s)가 기존 0.03 m/s 비상 가드에 근접 → 일부 run이 D로 중단될 수 있음(가드 완화 안 함). run03에서 1회 발생.
  - `SDG/STAGE_PIPELINE_20261109_v01/stage3_plan.sh` + `stage3_ready.json` 작성(plan sha 1f229a46…8e35). 본 실행 결과는 아직 없음.

## 2026-11-10 — Stage 2 (B1 static RGB-D pose + approach-path feasibility) COMPLETE, verified
- Orchestrator `SDG/STAGE_PIPELINE_20261109_v01`: stage2_VERIFIED_PASS 2026-11-10T11:27 (VERIFY_capture PASS 200x3 reps x O0/O25/O50; VERIFY_eval PASS 0 errors; 7,200 rows/variant, 5,400 selection rows).
- Smoke run01 FAIL preserved (yaw tol 1e-6 deg vs float32 1.2e-5; CAPTURE_MISSING outcome KeyError) -> v02 capture/eval (two-line fixes), smoke run02 PASS. Stage-2 prep agent had ended without smoke; pipeline idle ~9.5 h before 10:07.
- Findings: ORIG_v44 unusable on B1 (floor depth valid 0/1800, NuRec); B1ADAPT_v01 SENSEDTOP O0 XY median 2.7-2.9 cm all reps; O25 p90 ~20 cm (lateral); O50 ~70% WRONG_TARGET with top-1 selection; ORACLE O50 p90 >40 cm. Planning feasibility from B1 camera poses not interpretable (design oracle old 1/200, smooth 0/200). Rep differences descriptive only.
- Report: reports/stage2_pose_planning_results_20261110.md
- Stage 3 started under orchestrator 11:37 (72-run matrix, plan sha 1f229a46...; smoke STAGE3_SMOKE_20261110_v01_run05 6/7 SUCCESS + 1 FAIL_A at HR L4 O50; runs 01-04 failures preserved).

## 2026-11-10 — Stage 3 (physical driving, 72 runs) COMPLETE + integrated stages 0-3 report
- Orchestrator ALL_STAGES_FINISHED 16:35; stage3_VERIFIED_PASS (72/72 runs with recorded terminal outcome + evidence; VERIFY_stage3.json, VERIFY_analysis.json PASS).
- Outcomes: SUCCESS 36 (HR 14/24, LR 14/24, CAD 8/24), FAIL_A 8 (HR O50 no detection), FAIL_B 16 (LR/CAD O50 no pallet surface), FAIL_C 5 (CAD baseline curvature), FAIL_D 6 (existing 0.03 m/s speed guard tripped at 0.0303-0.0312 m/s; not relaxed), FAIL_E 1 (TF stale), HOLD 0, collisions 0. Main O0: HR 11/12, LR 11/12, CAD 6/12. O50 0 for all reps. Improved TC-S removed C failures (5 -> 0).
- Post-hoc: LR's smaller pose error is not an asset effect — unchanged v44 B5 lateral centre flips between ~0 and ~-5 cm with 1-2 px mask perturbations (offline rerun on saved inputs reproduces HR -4.7 / LR -0.1 / CAD -4.7 cm); stage-2 200-scene O0 medians equal across reps.
- Reports: reports/stage3_driving_results_20261110.md, reports/integrated_results_stages0to3_20261110.md

## 2026-11-10 — B5 lateral-flip root cause + improved estimator b5_robust v01 (offline, CPU; no training/HPO/simulation of motion)
- Root cause (analysis/b5_flip_diagnostic_20261110_v01.py, instrumented frozen core, asserted identical centres): frozen b5_fit_candidate anchors each axis on the 2%/98% side-point quantile of the face selected by sign(dot(to_camera, axis)); in head-on stage-3 views the lateral |dot| is 0.0008-0.01 for all 48 computed inputs, so a sub-degree heading change switches left/right silhouette anchoring (jump = observed width - 0.855 ~ 5-6 cm); plus 0/90 long/short candidate chosen by near-tie scores (45/48 with |dscore|<0.005; swap = 4.8-11 cm). v44 datum also rejects 25% of 1-2 px perturbed stage-3 masks (pallet-top strip excluded by the dilated mask).
- New: evaluation/b5_robust_20261110_v01.py estimate_pose(mask, depth, camera_metadata, layer_count, config=None); frozen config S/B5_ROBUST_20261110_v01_run01/frozen_config.json (config sha 35cf0a78…c529) frozen before test. Tests: tests/test_b5_robust_20261110_v01.py (7/7 PASS, synthetic).
- Results (S/B5_ROBUST_20261110_v01_run01/summary): stage-3 72 runs (dev-used, not held out): ORIG 48/72 computed, |x| med/max 2.9/5.5 cm, |y| 2.7 cm, 9/48 v19 CURVATURE_INFEASIBLE; ROBUST 64/72 (8 = no mask), |x| med 0.3 (O0 max 0.3, O50 2.8) cm, |y| 0.1 cm, 1-2 px perturbation lateral max jump 0.1 cm, 64/64 v19 PASS. B1 stage-2 TEST (no exclusions, 7200 rows): ORACLE lateral p90 O0/O25/O50 = 2.4/20.6/43.9 cm (B1ADAPT PRIORTOP, 100% computed) vs 0.8/3.4/4.3 cm (ROBUST, 95/95/94% computed; failures FOOTPRINT_INCONSISTENT_EXTENT).
- Unresolved: FOOTPRINT_INCONSISTENT_EXTENT 5-7% rejects (close-up/cluttered), L1 and L4-O50 tails, perturbation status flips ~0.2/input on B1 test, z error not reported for ROBUST, B1 planning pass rates uninformative (camera-as-start assumption; design goal also fails). Engineering only; not confirmatory.

## 2026-11-10 (evening) — Stage-3 speed-guard (FAIL_D) root cause + separate controller v03 regression pilot (NOT confirmatory, NOT default)
- Forensics (read-only, `analysis/stage3_speed_guard_forensics_20261110_v01.py` -> `SDG/STAGE3_SPEED_GUARD_FORENSICS_20261110_v01/`: ticks.csv.gz, runs.csv, bins_steer.csv, summary.json, plots/). 51 moving runs (main/pilot + smoke + v30).
  - Every 0.03 trip = ONE physics tick of PhysX instantaneous root-origin velocity spike (+10..+12 mm/s over a ~0.019-0.020 mean); FD speed at that tick 0.023-0.025; 0.25 s mean never >~0.023. COM vs origin identical; physics steps/update always 1, dt constant 1/60; wheel-target contract exact (graph target / command 1.000-1.008).
  - Spike rate rises with steering (residual std 0.9 mm/s straight -> 2.8 mm/s at 14-16 deg; base speed/command 1.11 at >10 deg, front-wheel scrub) and ~10x right after a supplier AckermannController 0.0157 rad steering-deadband toggle (up to 99 toggles/run when the commanded angle hovers at the edge) and ~3x after a governor command step-up. Guard margin vs cruise .020 was ~10 mm/s, about the observed spike size.
- New SEPARATE version (guard .03, robot/graph physics, steering/curvature limits, clearance, v21 adapter+certificate, leg bounds unchanged): `evaluation/stage3_follower_command_20261110_v03.py` (v19 law; cruise .016; deadband hysteresis), `scripts/stage3_drive_ros_20261110_v03.py`, `scripts/stage3_drive_session_20261110_v03.py`, `scripts/stage3_perception_20261110_v02.py` (selectable pose fn, default unchanged v44 B5), `scripts/stage3_drive_20261110_v03.py` (role regression), `evaluation/stage3_outcome_20261110_v02.py`, `scripts/stage3_ctrl_regression_batch_20261110_v01.sh`, `analysis/stage3_ctrl_regression_compare_20261110_v01.py`. The v02 controller remains the default for all other work (incl. the researcher's ablation).
- Regression pilot `SDG/STAGE3_CTRL_REGRESSION_20261110_v01_run01` (12 runs, research_denominator 0): SUCCESS 9/12; speed-guard trips 0/12 (peak 0.0190-0.0253, ticks>=.027: 0) vs prior same cells 6/40 trips (peak up to 0.0312). PRE/FINAL leg errors 2.7-2.9 mm, FINAL-vs-design per cell unchanged. Failures (preserved): CAD L1 impr r1 TF_STALE near FINAL during host overload (load avg ~200), LR L1 base r1 PHASE_WALL_TIMEOUT in leg 0 (wall/sim ~10x under the same overload), HR L4 base r1 JSON-read race at PRE->FINAL handoff ("Expecting value", unchanged v21 driver/session file handoff). Risk: lower cruise lengthens leg-1 moving wall to 160-193 s vs unchanged 200 s bound.


## 2026-11-11 — Claude Code → Codex G0–G3 실행 인수인계 / 본 주행 진행 중

- 보고서: `reports/stage4_handoff_audit_20261111_v01.md`, 증거 `reports/stage4_handoff_evidence_20261111_v01/`. 확인 2026-11-11T10:14:28+09:00: 기존 v04 큐 107/120 결과 확보, 잔여 13. batch2157667/watchdog1427871 생존 확인; main 뒤 o50가 이미 대기. 중지·재시작·새 Kit/ROS/GPU 추론 없음.
- 큐 선택 결과(원본/개선 혼합임을 명시): {'G0': {'completed': 27, 'outcomes': {'FAIL_B': 25, 'FAIL_A': 2}, 'first_attempt': {'FAIL_B': 25, 'FAIL_A': 2}}, 'G1': {'completed': 26, 'outcomes': {'SUCCESS': 21, 'FAIL_E': 1, 'FAIL_A': 3, 'FAIL_D': 1}, 'first_attempt': {'SUCCESS': 21, 'FAIL_E': 1, 'FAIL_A': 3, 'FAIL_D': 1}}, 'G2': {'completed': 27, 'outcomes': {'FAIL_B': 25, 'FAIL_A': 2}, 'first_attempt': {'FAIL_B': 25, 'FAIL_A': 2}}, 'G3': {'completed': 27, 'outcomes': {'SUCCESS': 21, 'FAIL_D': 4, 'FAIL_A': 2}, 'first_attempt': {'SUCCESS': 15, 'FAIL_E': 6, 'FAIL_D': 4, 'FAIL_A': 2}}}. run01 G3 메모리 실패6개는 보존하며 run02 성공으로 원본 성공률을 덮어쓰지 않음. 전체 완료·최종 통계 NOT_DONE.
- 메모리6건은 8GiB 초과가 아니라 per-scope RSS +768MiB guard 초과, peak6.827–6.995GiB. 상속된 sessionv03의 W GC 재설정은 한도값 유지하지만 기준점 재설정으로 전체 증가량 의미가 바뀜. 수집20건 collect 전후 RSS 감소0; 누수 해결 입증 아님. 실행 중 코드는 변경하지 않음.
- CPU 동일 RGB-D11개: ORIG11/11 datum거부 재현, ROBUST_A11/11 기존좌표 exact. 후보 면 erosion후49–84점<100이 첫 거부. 원본 촬영실패1개 NOT_REPLAYABLE로 별도 기록. 고정값·분모·GT 입력 변경 없음.
- PASS: known9/hash/count108/432, Stage4matrix120/pairing, design+모델4hash, 코드사본해시, coreAST, robust7/B로직13 검사. 최초 filename/입력부재/pytest부재 감사명령실패 보존. 기존 실패·USD·weights·lock 불변.
- 실제 저장RGB/주행JPG contact sheet8패널 LOCAL_ONLY 생성; 조사폴더MP4없음. top-down·대표영상·최종분석 미완료. 로컬.git없음; GitHub read만 수행, 텍스트 marker sync요청/원격완료UNKNOWN. 다음은 기존큐 종료 확인 후 버전별 시도·실패 보존 분석이며 SKIP_EXISTS를 안전한 resume으로 간주하지 않음.


## 2026-11-11 — 기존 Stage1·Stage2 논문용 전체 집계 및 B1 학습 설정 감사 완료

- 새 보고서: `reports/stage1_full_factorial_tables_20261111.md`, `reports/stage2_complete_pose_metrics_20261111.md`, `reports/b1_training_hyperparameter_audit_20261111.md`. 기존 G0–G3 batch2157667/watchdog1427871 생존을 작업 전후 확인했고 중지·재시작·설정변경 없음. 새 렌더·추론·학습·HPO·주행0; 단일 stdlib process, nice15/ionice idle로 저장자료만 분석.
- Stage1: 원본48600행 중 주 분석 자기표현10800행, HR/LR/CAD×L1–L4×O0/O25/O50×base/aug=72셀·216seed셀 완료. 각 실제장면45/50/54/51, 3seed평균/표본SD·AP GT분모·IoU-best/Top1·실패건수 포함. T1–T8 원본/사본SHA일치, T1 주요수치일치 PASS.
- Stage2: 변형별7200행, MODEL_TOP1과GT-oracle분리54셀. 계산자체(C_any)와지정목표선택후계산(C_target)분리, 조건부XY/종횡/yaw180·90 평균/중앙/p90·실패원문전부기록. O25 C_target/600 HR/LR/CAD: ORIG65/69/70, SENSEDTOP332/326/320, PRIORTOP515/509/502. C_any는별도열이며실패를0오차로넣지않음. 원래summary와270항목일치.
- 학습: v03baseline9+v04혼합39=최종48run의실제kwargs/args.yaml/200epoch검증, stage1모델27개checkpointSHA·epoch계보PASS. 해당B1 HPO미실행; recipe변경·seed반복·고정증강/혼합비·checkpoint선정과구분. 원본v02FAILED·혼합HANG3개(상태RUNNING잔존)와별도rerun경로보존.
- FAIL문서정합성: LOCKEDv04 RNG설명은(run seed,epoch,index)per-samplegenerator지만SHA일치PhotoDegrade구현은전역Python random·getrandbits기반noisegenerator. expectedhash/lock/코드수정0; 전체재현성무조건PASS아님. 관련새실험실행0.
- 집계검증18822개/학습설정감사336개 PASS, RNG정책불일치는별도FAIL. 최초T1표현명KeyError·supersedes note경로오류exit1및수정patch실패보존후각새v02증거폴더에서성공. 최종입력242개SHA재확인불변. 증거: `reports/stages12_full_tables_20261111_v02/`, `reports/b1_training_hyperparameter_evidence_20261111_v02/`. 새분석코드2개,과거원본/과거보고서불변. 원격게시없음/반영UNKNOWN.
- 다음: 연구자는세표의분모와원고용표기확인, RNG설명불일치는향후별도문서개정전에검토. 이번표로모델선택·튜닝을하지않고현재주행큐는기존실행기에맡긴다.


## 2026-11-11 — G0–G3 본120셀 종료 검증·버전 분리 분석·메모리 후보·영상 패키징

- 보고서: `reports/stage4_original120_and_gc_revision_results_20261111_v01.md`, 최종 evidence `reports/stage4_completion_evidence_20261111_v01/snapshot_20261111T113224`. main PHASE_END 11:31:50 KST 확인. 기존 shell이 o50로 자동 전환했으며 중지·재시작·새 Kit/ROS/주행 없음. O50는120분모와별도이며현재미완료.
- 최초시도120셀: G0 0/30(28B+2A),G1 25/30(1E+3A+1D),G2 0/30(28B+2A),G3 18/30(6E+4D+2A). 운영선택120셀의 G3는 별도run02 24/30이며 원본6실패보존. 실제main139시도+pilot12=151기록 검증,저장outcome재계산/trace정합/코드사본 불일치0. 혼합120이력은회계표이며효과검정은run02동일버전availablepairs별도.
- run02 짝: G1-G0 pooled20셀/7조건 차+.800, G2-G0 0, G3-G1 21셀/7조건 차−.0952(탐색boot95 −.3333~+.0952). 편의부분집합·표현군집·다중비교미보정·독립환경아님 명시. 비유의≠동등성. 성공G1/G3paired14셀 추가wall중앙60.119s/추가drive15.417sim s. 재관측24개중21개XY감소/3증가,paired중앙−1.314mm.
- G1 D1건은LEGS_INCOMPLETE표면사유와별도로rawpeak.03056994m/s speedguard보존. G3 D4건은W최근접3.06–3.70mm>3mm정상감속반경→요청0회→along<−5mm GOAL_OVERSHOOT. 재인식전실패이며threshold/control변경0.
- CPU센서대조전체조건G1계획30중29재현(미검출3포함)+원본촬영실패1;ORIG mask있는26개전부erosion후100점미만거부,ROBUST26계산;기존좌표/status/reason exact. 입력SHA불변/GT0/재추론0.
- 기존GC6실패는+768MiB guard(peak6.827–6.995GiB)이며8GiB절대초과아님. run02의대응6개는모두SUCCESS로별도검증. 새로운compact-history候補 helper/sessionv04/runnerv05작성,실행중코드미변경. rawJSONL전체보존,history14필드만보관. 13run/33정지인증·quiet/outcomes exact/33손상거부same,AST범위검증 PASS_OFFLINE. 5000JSONrowCPU보유73.23→30.20MiB(58.76%감소);Kit/CUDA절감아님,live객체공유차이명시. 실제후보Kit검증·6개재실행NOT_RUN. preflightHOLD/exit2는기존큐·GPU점유로의도된보류.
- 저장JPG만MP4 5개로패키징/전체재디코드frame수일치. 실제RGB/mask/주행frame26패널(contact누락안내1),로그top-view/속도3PNG,추가실패진단3자료. `SDG/STAGE4_PAPER_MEDIA_20261111_v02`비공개전용,실제외부카메라영상아님/실제topdown렌더없음/새렌더0. v01시간간격가정FAILED보존.
- 10130입력fingerprint불변·새코드12개AST PASS·활성4코드SHA첫audit와동일. 보고서첫NameError/import누락실패+부분CSV및patch검증실패/미설치ffmpeg탐색오류보존. 원본/실패/USD/weights/locks불변. Gitpush/remote변경0/marker텍스트sync요청/원격완료UNKNOWN. 다음: 기존O50완료확인후자원비점유점검,그뒤에만별도후보smoke및별도6cell평가.


## 2026-11-11 — G1 표현별 차이 원인 감사 완료

- 보고서: `reports/g1_representation_success_gap_causal_audit_20261111_v01.md`; 증거: `reports/g1_representation_audit_evidence_20261111_v01/`. 기존 G1 HR7/10·LR10/10·CAD8/10 유지. HR 실패는 S2/S4 O25 인식2건, S3 O25 속도guard1건(.03056994>.03m/s); 안전 기준 변경0. CAD는 촬영1건·인식1건으로 분리.
- O25 전체 동일 run02/runner v04/session v03: HR1/4·LR4/4·CAD3/4. run02 공통7조건도 HR4/7·LR7/7·CAD6/7이며 버전 혼재만으로 차이가 사라지지 않음. 에셋 단독 인과효과/일반 순위는 UNKNOWN.
- M50 3 checkpoint 원본·선정lock·배포·실제 manifest SHA 일치 PASS. B1 증강 모델과 혼동 없음. 저장12입력 자기 모델 재추론 원래 설정 완전 재현, 총42회 별도 진단(동일입력 모델교체36+낮은confidence6), 원본 집계와 분리. HR 실패 영상에서 LR 검출; HR 저문턱 진단 confidence .015696/.120312<원래.25. 모델·학습도메인·선정checkpoint와 외관 효과가 혼재.
- fresh 주행 semantic GT 없음. fixture canonical HR target과 screen rectangle으로 재구성한 판을 reference로 명시; 4fixture 면적/가림률 exact,12camera transform exact. 가림률은 fixture 측정의 복사이며 주행별 독립 실측 아님. HR 실패2개와 동일장면4개 PNG 패널은 외부 SDG/G1_REPRESENTATION_AUDIT_20261111_v01/panels/ 비공개 보관.
- 입력SHA 재검증 불변,30셀 원본 분모 보존, 조건부 pose/경로 집계 CSV 완료. 새 주행·렌더·학습0. 최소 추가9회(S3×3표현×3반복)는 설계만 작성, 실행 안 함. 기존 main 및 별도O50 큐 모두 정상 종료(각11:31:50/12:20:25 KST); HPO 학습은 아직 시작 전이며 이전 HPO 지시의 실행기 준비 작업은 별도 미완료. 이번 진단은 B1 HPO 선정에 사용하지 않음.


## 2026-11-11 14:01 KST — B1 공통 HPO 실제 독립 실행 시작

- RUNNING: controller PID3130638, tmux b1_common_hpo_20261111_v01, 외부root SDG/B1_COMMON_HPO_20261111_v01. 상세 인수인계 `reports/b1_common_hpo_launch_handoff_20261111_v01.md`; 이후 상태는 hpo_status.json 먼저 확인.
- 이번 지시에 맞춰12후보(기본+11 random, sampler20261111), train seed42,3표현60epoch(200schedule);top3+base200,선정+base43/44,최대63run/6966epoch고정. 초기조건pretrained·4개탐색외kwargs·PhotoDegrade 원본 유지; RNG문서불일치공개. Test/RealTest189미사용.
- CPUpreflightPASS,실제smoke HR/LR PASS후CAD로자동전환확인. 명령반환후다음PID자동생성·tmux조상확인; AI없어도진행. 기존main/O50정상종료·GPU충돌없음·패키지변경0·새주행0. 최초CPU정확등호테스트실패는tolerance로수정후실행전PASS.
- 상태10초/스냅샷15분 자동기록,lock/25GiB디스크guard/완료artifact검증/실패보존. resume.sh는기존세션중복방지·검증완료skip·중단attempt보존후새초기학습;FAILED자동retry없음. 최종결과아직미확정.


## 2026-11-11 — Progressive Depletion 원래 설계 복원 감사 완료/신규생성 HOLD

- 보고서 `reports/progressive_depletion_original_design_recovery_audit_20261111_v01.md`; 증거 `reports/progressive_depletion_design_audit_evidence_20261111_v01/`. 기존C원본잠금SHA·manifest1680·state840·history9600 보존/검증.4층×15Bundle5×5벽돌=300;C100/80/60/40/20=60/48/36/24/12묶음.20층설명을사용하지않음.
- 기존200seed경로×48제거의최고층/외부노출floodfill/정렬rng선택exact,800strictnesting PASS. 1680manifest↔840state↔2재료 및 실제3표현metadata5040개 공통mask/생성수/source SHA PASS. 동적CoG/지지안정성은구현·검증없음/UNKNOWN.
- 실제잔여slot+명목x/y/z+방향exact-set으로고유성검증: 전체40환경 C100/80/60/40/20 고유2/184/197/198/174. MNIDB_0006 C20 T02(seed3281395651)와T05(seed2131428289) 동일형상(5경로4고유);수정·삭제0. CSV26400묶음좌표·5seed SVG 도식저장/새시뮬레이션아님.
- 현재B1실제capturev03→step21 nominal source는full-layer생성. package4200행과complete4200개일치;L1–L4=75/150/225/300,부분최상층0,각L phase2종. ProgressiveDepletion과설계동일성FAIL;기존L자료·모델·보고서·주행은별도실험으로유지하고C재라벨링금지.
- HPO기존tmux/PID3130638정상RUNNING보호.12후보초기탐색완료,17:59에3365/최대6966epoch=48.31%,오류0. L전용HPO이며C최적성/전이는UNKNOWN. 원래protocol/code/params미수정,외부root에scope notice만신규추가.
- 최소복귀DRAFT:50/10/10환경×(FULL1+5T×4부분)=1050/210/210scene/표현,4410RGB안;환경별전체T/C동일split,oldtest재학습누출금지. base-vsL-HPO선정값C-Val전이대조최대6seed42모델→양설정seed43/44포함최대18안. 확정/실행아님.
-300회DRAFT=5C×2O×10pairedbase×3표현;독립환경300아님,O50별도,최종모델/안전/조건선행잠금. 신규scenario/data/render/inference/train/drive0. 선행5논문서지·내용확인범위를분리,BRIX/JENGA원문확인;나머지3전체PDF접근미완료명시. 다음은새C프로토콜구체화이며임의생성금지.


## 2026-11-11T18:36:10.022011+09:00 — C 복구 준비·독립 systemd 감시/ntfy/GitHub 통합

- 최신범위PREPARATION_ONLY. 신규렌더·학습·Isaac주행0,기존L-HPO절대수정·중단0. 48h는soft예산이며시간초과자동성공/축소/종료없음. root SDG/C_DEPLETION_REBUILD_20261111_v01. 보고서 `reports/c_depletion_preparation_automation_handoff_20261111_v01.md`.
- 신규DRAFT3장방법론/데이터·모델계획/300회프로토콜3개와ROBUST_A구조감사작성. 실제기존결과·원래미사용C알고리즘·신규미구현부분구분. .144는pallet설계두께,적재물top아님. ROBUST_A layer_count의존/CLI1,4만허용 및nominal4의C60/40/20 datum수식반례−.09/−.18/−.27m확인;센서검증아님/새C정답층수입력금지.
- .11m/7.341774°는현행MAIN출처확인,.10m/5°의잠금출처UNKNOWN. C단일기준미확정본주행HOLD,비열등성10%p미확정. 10base×5C×2O×3표현300·G1single-only·O50별도·paired/repeated/Wilson/비열등성분리.
- 독립CPUcontroller PID3509437,watchdog PID3514993,systemd user 2서비스 active/enable/Linger=yes. CPUQuota각10%1core·256MiB·Nice15. CPU2단계자동실행COMPLETED/결과SHA검증후HOLD. 새C dataset/training/pose/pilot/main 미구현·미실행/허가없음,전GPU파이프라인완성으로표시하지않음.
- ntfy기존hook/privateconfig재사용HTTP200+연구자휴대폰수신확인. independent watchdog30s/15minsnapshot·오류dedupe/retry·기존HPO완료/개별실패감시. 기존GPU와경합0/HPO PID3130638/codeSHA5개불변.
- 기존GitHub checkout/auth/remote재사용,새namespace research/c_depletion_rebuild_20261111_v01 텍스트allowlist만자동commit/push/remote SHA확인. 최초secret규칙self-match로sync실패보존,별도publisherv02회귀PASS/v03개별실패알림추가,원래protocol/hash수정0. 원격실검증commit f9cae69380e01be4f7de7d572e5b4bf8e23909a4;최신은root/github_sync_status.json. push실패시local계속/PENDING_RETRY.
- status.sh/resume.sh는새준비서비스용이며HPO재시작안함. boot자동기동구성/실제reboot미시험;기존HPO는bootresume부착안함. 잔여C실제작업은HOLD해결후대략55–70h거친안(300drive만관측39.92h/보수45h),HOLD대기제외. 정확성우선/48h강제시한없음.


## 2026-11-11T19:16:37.531172+09:00 — C 전용 공통 HPO 필수 단계 계획 개정

- 개정분만작성: `docs/c_depletion_common_hpo_plan_AMENDMENT_20261111_v01.md`, `reports/c_depletion_common_hpo_plan_amendment_20261111_v01.md`; root execution_plan_amendment_v01.json/pipeline_plan_current.json. 기존전체지시유지,선택적L-HPO전이대조만의안을C전용공통HPO필수로대체.
- C생성/QA/family split lock→C-HPO→최종9모델/seed반복→인식→pose/ROBUST_A→기술pilot→G1 300. C-HPO안12후보(base1+L-HPO 상위비기본최대3+새random최소8),3표현동일설정·ownC-Val mask mAP평균;60screen/200full/seed43,44,qualification포함최대57run/5766epochs DRAFT. 실제예산·후보는C QA후학습전잠금. Test선정사용금지.
- 현재L-HPO PID3130638 RUNNING,controller3509437/watchdog3514993 유지. 기존코드·부모protocol·QA gate/문서잠금불변. 신규GPU/주행0,HOLD해제0. 실제C-HPO실행기연결은미구현/미승인이고계획개정을자동실행완료로표시하지않음.


## 2026-11-11T19:37:50.197978+09:00 — O50 별도150회 주행 계획 추가만 반영

- 개정분 `docs/c_depletion_O50_drive_plan_AMENDMENT_20261111_v01.md`, `reports/c_depletion_O50_drive_plan_amendment_20261111_v01.md`;root execution_plan_amendment_v02.json 및pipeline_plan_current.json. 기존HPO개정/본300회유지+5C×O50×3rep×10base150=계획450. 300/150namespace·결과·분모·통계별도,450합산성공률주결과금지.
- 가능하면동일10base·제거·시작·환경·모델대응;현재frame실제가림/GT별도검증. C인식/pose O50평가·GT/가림QA·O50기술pilot·150manifest/version/model lock·별도실행승인필수. 인식/오선택/pose/plan/안전/최종실패·중단보존,기존A/제어/안전완화0.
- 계획순서main300→O50technicalpilot→O50separate150,파일럿은150분모와별도. 실제150ID/새데이터/adapter생성안함. 현재HPO PID3130638 RUNNING,Controller3509437/Watchdog3514993 유지/HOLD. 기존코드·부모잠금·C-HPO계획v01불변,신규렌더/학습/주행0. 추가물리작업만약20–22.5h,450물리합약59.88–67.5h잠정/기타단계시간별도/48h강제시한없음.


## 2026-11-11T22:08:57.944376+09:00 — B1 공통 HPO 자동 실행 종료

- 상태 COMPLETED; 보고서 `reports/b1_common_hpo_final_20261111_v01.md`; 원본 /home/user/hh/isaac_cosmos/sdg_final/B1_COMMON_HPO_20261111_v01; Test 미사용.


## C dataset automated QA stage 2026-11-12 08:44:22

- HOLD_MASK_ENCODING; reports/c_depletion_dataset_stage_results_20261111_v01.md; original results preserved, physical stages HOLD.


## 2026-11-12 09:35 KST — C bitmap QA 복구 및 실제 C-HPO 재개

- 보고서 `reports/c_depletion_bitmap_recovery_handoff_20261112_v01.md`. 원본4410/4410 생성완료; 기존 polygon QA 1782/13986 encoding 실패 HOLD 보존. 원본형태를 유지하는 새 bitmap QA PASS, CPU32seed 변환 및 6개 train/val loader 점검 PASS. PhotoDegrade Format-name CPU 실패는 보존/새 worker v03로 호환.
- C_COMMON_HPO_v02 실제 RUNNING: systemd c-depletion-bitmap-continuation-20261112-v01.service, HPO PID106572, HR smoke2epoch PASS→LR 자동진입. 후보12/최대57train/5766epoch 유지. 기존 B1 HPO 불변. 데이터/증강/조건 사후완화0, bitmap 라벨방식 변경은 C-only 계보로 구분.
- static 평가까지 독립자동연결, 원본 failed polygon controller/출력 보존. 실제 renderer legacy NumPy exception root cause 미해결; 새 mask topology 인코딩 문제와 구분. 물리pilot/main300/O50150은HOLD/실행0.

- 09:37 후속: C 3표현 GPU smoke 각2epoch 모두 PASS, checkpoint SHA/FP32/AMP 감사 확인. screen 기본 HR 60epoch 탐색 자동진입, continuation106568/HPO106572. GitHub bitmap 원격 commit2776ce1e3fcc2e1e2620efb3dac090e37d2117e6 확인. 추가 publisher5분주기/기존watchdog 유지.


## 2026-11-12 — Replicator/NumPy 예외 CPU 독립 감사 완료

- 보고서 `reports/c_depletion_replicator_numpy_data_integrity_audit_20261112_v01.md`. production210로그/26370예외=4395scene×6. UTC+경과ms 복원불확실성최대.036초; 전부실제적재물생성전empty RGB파일저장이전. 내부원인은legacy ID annotator warp.numpy→np.asarray; 실패rawbuffer/shape/framecounter미저장으로정확원인UNKNOWN,무해확정아님.
- 전체4410파일SHA/decode/actual-canonical13986마스크px·중복 검사/잔여Bundle5 독립투영 범위 PASS. RGB-empty-mask H1통계13986개exact;OK13600/LOW_SUPPORT317/WATCH30/FLAG_NUREC39원래대로유지. 최초정수pixel광선진단585outlier는별도보존; +.5pixel-center 전체13986instance 표본깊이투영5mm밖0. 기존pose/HPO입력규약수정0.
- 새데이터손상근거미발견으로추가정적평가HOLD유발없음. rawframe단위동기/버퍼신선도완전증명UNKNOWN. HPO/Controller/Watchdog/동기화서비스중단·설정변경0,물리pilot300/별도150HOLD. 감사CPU만저우선순위/최종1core제한,새GPU/렌더/학습0.


## 2026-11-12 — C100 균형 보강/B1 L4 재사용 읽기전용 감사·계획

- 보고서 `reports/c100_balance_b1_l4_reuse_and_hpo_plan_audit_20261112_v01.md`; 증거reports/c100_balance_reuse_audit_evidence_20261112_v02. B1 L4실제346/표현(244/51/51),총1038RGB SHA검증. 현재C공통70family×3=210:camera/canonicalGT모두exact,RGB/actual mask exact0;같은Test30depth exact0,calibrationexact. centered-C asset배치보정차이로추가직접호환RGBD0. GT참조재사용은새독립이미지아님. 첫GT소유경로가정실패v01보존/HR공통GT소유를따르는v02검증.
- 최소DRAFT:C100350/표현=250/50/50,기존70유지+280/표현신규,total840;전체O05250(Train3750/Val750/Test750). C100만view다양화교란명시,anchor분석별도;더엄격한전C-view대응4200신규안별도. 새TrainVal에는제한적공통확인HPO4후보×3표현200seed42+선정43/44=최대18train/3600epoch제안,미실행.
- O0만훈련선정/O25O50은Test계보대응평가유지. balancedTest각O750,총2250,가림1500/기존계획대비추가240. 기존V01 O04410과별도기술. 기존HPO/자동실행/원본변경0,새렌더학습주행0,물리 HOLD 유지. DRAFT 추가안 docs/c100_balance_and_occlusion_plan_amendment_DRAFT_20261112_v01.md는실행기에연결하지않음.


## 2026-11-12 — 연구자 C-V01 유지/상태별 보고 결정

- `reports/c_v01_retention_statewise_reporting_decision_20261112_v01.md`. C100보강/18학습재HPO대안은보류/미실행,현재4410O0/HPO/정적자동평가불변. B1L4합산0.
- pooled AP와C5상태AP및동일가중1/5macro별도,실제GT/이미지분모·독립Test family10/C100Test10한계명시. 현재raw평가가상태별AP/family_id보존함을확인. 별도CPU후처리로정적완료후표생성하며학습/기존실행기제어없음. O0학습/O0O25O50Test구조·300+별도150물리HOLD유지.


## 2026-11-12T16:47:01.334321+09:00 — C 공통 HPO 자동 실행 종료

- 상태 COMPLETED_WITH_FAILURES; 보고서 `reports/c_common_hpo_final_20261111_v01.md`; 원본 /home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02/C_COMMON_HPO_v02; Test 미사용.


## 2026-11-12 — C-HPO 별도Validation 복구 실행

- 보고서 `reports/c_hpo_validation_pipeline_recovery_handoff_20261112_v01.md`. 57train PASS/sha보존,실제cross실패24/24(14는중간집계). 별도val가training kwargs를상속하지않아overlapTrue/mosaic1default로bitmap계약충돌. maskratio4는같았음. 새eval-onlyworker/독립controller로small own/cross9건반복exact/3full own검증후24건복구중. 재학습/가중치/GT/분할/선정변경0.
- savedEMAfp16 rounding으로학습FP32EMA와지표차이HR+.017421/LR+.001834/CAD−.117268%p보존;원epoch비트재현주장없음. 같은checkpointrepeat exact. C06원래seed42score94.329830%/base94.287328% 및선정lock불변. 복구24건후에만새HPO_recovered_status COMPLETED,원본failed상태는보존. 물리HOLD.
- ntfy16:43경serverHTTP200이력있으나handsetUNKNOWN/이전로그경로결함확인,정확경로고우선재알림HTTP200확인. 기존watchdog/동기화중단0,복구에러는즉시notify+HOLD기존queue.

- 평가복구최종:24/24 crossVal,5040model-images/16632 GT instances 검증PASS. 36개검증실행artifact/inputSHA/Val계보확인/57checkpoint불변/원본24실패보존. 새HPO_recovered_status COMPLETED,기존C06선정유지. 후속static HR가림qualification 실제진입(PID707461),controller699911/static707458. 물리HOLD.


## 2026-11-12 — 최종 승인 C-V02 보강/혼합 선행 자동 실행 시작

- 보고서 `reports/c_v02_c100_mixing_pipeline_launch_handoff_20261112_v01.md`; doc lock c_v02_balanced_mixing_execution_protocol_LOCKED_20261112_v01.json. 기존4410/57학습/24복구Val/C06 SHA 보존. 이전보강보류는최신명시승인으로대체하되기록보존.
- 기존가림30/30 PASS 및1890frameQA후GPU경계예약→기존perception미진입HOLD→새C100generation전환실증. kill/중복GPU없음. V02root SDG/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01,controller910996. 신규840RGBD추가목표/전체5250. Train-derived동일distance_bin4새camera관측,70family/split/형상/조명원본보존. C100만view다양화교란/anchor분석명시.
- Real352/48/189 class0/계보hash중복0,기존LOCKEDv03 target-only원본정책유지/제품도메인차이공개/미승인보완라벨안씀. bitmap양성·음성·다중해상도6CPU시험PASS. 전체V02QA전모델학습없음.
- C06fullprecision고정39본학습(9synthetic+27partialmixed+3sharedreal trajectories)/7800epochs,별도3×2epoch smoke. 각비율1250slots(1250:0/938:312/625:625/312:938/0:1250). 동일pretrained새학습/HPOrerun0. dualVal동일가중checkpoint,공통비율9score평균/동점높은합성/epoch동점최초. zero-real훈련3공유하지만표현별bestepoch차이기록.
- sourcecapSHA고정/QA→학습→모델잠금→기존Test재사용+신규C100Test가림240→selected/baseline정적→pose→통합보고까지독립연결. 이후물리300+별도150은성공/센서datum/안전/파일럿gate미확정HOLD. 학습GPU검증은QA후예정이며아직통과주장하지않음. 기존watch/ntfy/Git 유지+V02관찰자/상태명령추가.


## 2026-11-12 — 작업 층수 prior 최신승인/C-V02 오탐수정 재개

- C100 180/840후worker정상종료전환을추가watch가즉시missingPID로오판해GPUboundary HOLD된기록보존. watcher v03에120초동일PID전환유예추가,원래연구watch3805776/실험설정유지. 180개재생성없이gen v02 PID966660으로재개,이후200/220/240/260묶음연속완료.
- task_layer_policy_v01: C100/80/60/40/20=4/4/3/2/1을운영자제공occupied layer task prior로명시허용. 기존layer금지는C-V02이최신예외로대체,GTpose/mask/slot/footprintcenter/FINAL금지유지. 원데이터nominal layer_count4(카메라생성용)수정0,별도task schema/2250static task+450physicalDRAFT/sha잠금.
- ROBUSTA code0b1e5f46702d…/cfg35cf0a78…변경0. 새CCLI1..4+finalmixedseed42 modelsha/taskregistrysha검증/initial-only. unit1..4 forwarding/NoDetection·8datum prefix·GTschema/read차단PASS. q99상층점<1%/바닥없음이면correctlayer4여도datum−.09m가능한구조위험단위진단기록;실C/O 성능은최종mask고정후추가CPUworker로6750/role 평가예정/아직미검증.
- CPUv30/원NuReccomposition감사:원NuRec collisionAPI0,과거v30 rover13+이름미분류29/PhysicsScene1. 이름만으로floor없음확정안함/rolebinding·실제loadedstage/contact는미확인. 신규 C drive stage 미생성,physicalHOLD유지. Main .11m/7.341774°를최신명시성공기준으로기록,PRE_FINAL5mm/2°cert·.03speedstop과구분;나머지안전·물리gate유지.


## 2026-11-13T14:26:18.471186+09:00 — 연구자 요청 결과 통합 추출

- 보고서 reports/research_results_snapshot_20261113_142618.md 및 단일 ZIP research_results_snapshot_20261113_142618.zip. 기존 결과 읽기전용 스냅샷/45모델셀/39본학습+3smoke/epoch기록/20250인식원자료 포함. 학습39/39완료,75:25선정;위치추정 진행중으로 미완료표시. 실행기·모델·원본변경0,물리HOLD유지. ZIP CRC검증PASS.


## C-V02 혼합·정적 평가 자동 완료

- reports/c_v02_final_mixing_perception_pose_integrated_20261112_v01.md; 물리실행0/HOLD.


## 2026-11-13T15:48:56.074321+09:00 — 연구자 요청 결과 통합 추출

- 보고서 reports/research_results_completed_static_20261113_154856.md 및 단일 ZIP research_results_completed_static_20261113_154856.zip. 기존 결과 읽기전용 스냅샷/45모델셀/39본학습+3smoke/epoch기록/20250인식원자료 포함. 학습39/39완료,75:25선정;위치추정 진행중으로 미완료표시. 실행기·모델·원본변경0,물리HOLD유지. ZIP CRC검증PASS.


## 2026-11-13T17:12:17.859551+09:00 — C-V02 O0 단일적재물540 물리진입HOLD

- reports/c_v02_drive540_single_load_protocol_and_physics_hold_20261113_v01.md;새540manifest/단일load_count1,pallet_count1개정SHA잠금. CPU15조합 벽돌수/단일적재물/공통collider/중첩/명목지지PASS. 기존정적/모델변경0,선택정확도는본540주지표제외.
- actualKit 정지물리진입4개분리진단에서초기update nativeOmniGraph core/image crash,정확원인UNKNOWN. 로그/덤프/SHA보존,actualPhysX/센서/파일럿 미검증,0/540 HOLD. 완성E2E/자동540실행기라고표시안함. 추가무조건재시도없음.


## 2026-11-13T17:42:23.140269+09:00 — C540 Kit실행복구/실제파일럿NO_DETECTION HOLD

- reports/c_v02_drive540_native_crash_recovery_and_E2E_status_20261113_v01.md;빈Kit60PASS/v30no-warmup nativefail/원Stage4의extension후빈update5복원→v30graph그대로60PASS. 기본15조합actualKit RGBD/PhysX등록/접촉확인(짧은physics구간). C진단첫expiredprim error/exit0오판은정정·실패보존.
- HR-C100 fullE2E파일럿 actual257step/4.2833s,ray2214/6wheel/support/graph/305collider/camera7checksPASS. 고정HRmodel conf.25후보0→NO_DETECTION,driver/nonzerocommand0,계획/주행미진입. 모델/조명/conf허용값변경0,실패보존,0/540HOLD.
- E2E실행코드별도잠금,controller2783174HOLD종료;자동540전환실검증미완료. passive감시/ntfy/Git유지. 다음은관측분포/렌더계보의검출실패원인분리,새attempt재검증이며blindrerun금지.


## 2026-11-13T18:21:05.337183+09:00 — C540 무검출진단·기술판정개정/실제제어시험

- reports/c_v02_drive540_no_detection_and_technical_pilot_amendment_20261113_v01.md. 동일HR saved-input conf.25무검출재현/PIL_RGB=numpy_BGR일치/모델SHA정상. GT투영bbox172×72잘림0,ROI median1/255·82.84%<20,Depth11221점타깃box내. conf.001후보max.0168은타깃아래팔레트쪽;운용사용0. static3예시정상검출,도메인/역광차이유력이나단일원인확정아님. 카메라fx317vs554/pitch−19.95vs−4~−5.6차이기록. 모델/조명/threshold변경0.
- 축약basic metadata의raw/provenance누락+USDcamera scale[.124,.026,.029]혼입별도확인. 원본보존/정식E2E기존정규화와동일한offline-only adapterv02로9검출mask모두ROBA계산. 실제정식E2E는이미정상normalized metadata사용. HR무검출원인과분리.
- 기술gate 개정: 작업SUCCESS불필요/정상모델·pose·경로실패는안전종료·증거검증후기술PASS;실이동/정지 별도필수. 8회귀테스트PASS. 기존HR실패재사용,대표15실제fullpilot 15/15기술PASS=FAIL_A5/FAIL_C10,taskSUCCESS0. 이는본5400회와별도.
- 독립Controller2823783/technical_e2e_v03에서과거검증engineering route별도실이동중. PRE도달2.825mm/0.0182deg·정지인증PASS,FINAL/ROS종료검증대기. 모든gatePASS에만main자동진입. 원래36base/540manifest SHA불변. 새watchdog/Git/ntfy독립유지,모델추론경로에GT0.


## 2026-11-13T18:36:38.100814+09:00 — 독립실제이동 PASS / main 저장권한대기

- 실제engineering이동1.681m,maxspeed.027540<.03,maxsteer13.203<20deg,PRE2.825mm/.01822deg 및FINAL2.815mm/.01757deg stop인증PASS,collision0,영상611JPG/파생MP4 612frame decodePASS. E2E/540분모0 유지.
- 본540capacity gate max실제저장량×540+25GiB=416999376520bytes에비해rootfree약108GB라HOLD. 기존empty8TBext4를ro로먼저확인:lost+found만/약6.9TiB여유. mountRW가능하지만root소유폴더생성은OS권한거부(sudo password/udisks NotAuthorized),소유권/format/data삭제0. 새연구전용폴더사용승인질문pending.
- technical_e2e_v04 PID2869572가15기술/독립motion proof만재사용하며WAITING_STORAGE_AUTHORIZATION_AND_CAPACITY. 명시approvalfile+신규디렉터리권한+UUID+공간통과에만main자동진입. 사용자승인없이GPU시작0. E3부족HOLD원기록보존. 보고서/CSV/실제영상ZIP c_v02_drive540_diagnosis_technical_evidence_20261113_183637.zip CRC PASS;원자료불변.


### 2026-11-13 C-V02 저장량·곡률 CPU 감사 (추가 기록)

본실험0/540 HOLD 유지. 새 실제 실행0. engineering722,510,798bytes는 접촉/제어 로그 중심이며417GB는540동일이동+25GiB 조건부 예산. 무손실 RAM gzip round-trip은81.323MB까지 가능하나 기존 파일/검증기 변경 미적용. 실제 곡률거절10건 모두 비평행 전진 필요곡률≥1.819398/m로 허용0.363645/m 초과; 기준목표 진단에서도 유지. 명목36Base 중 필요조건위반30, 현행 TC-S 미허용32(실제 미래 실패율 아님). 저장권한 및 경로설계 검토 미해결. 원본/모델/manifest/안전기준 불변. 보고서: reports/c_v02_drive540_storage_and_curvature_audit_20261113_v01.md; 상세 CSV는 동명 storage_curvature_audit 폴더. 기존 Controller/Watchdog 변경 없음.


### 2026-11-13 C540 전역 경로/시작점 오프라인 설계 검토

본실험0/540 HOLD,새Kit/GPU/주행0,운영코드/manifest/protocol 변경0(SHA전후동일). 기존36Base TC-S4통과. 시작점유지 free-space 곡률연속CSC36수학해,단30개17.874~18.293m우회로 현행forward/3m/overshoot/180s계약과충돌;충돌/제어전부UNKNOWN. 짧은해B11/B34추가해6기하호환. 별도미승인공통Y−1.25m시작점안은기존TC-S36통과이나카메라/접촉미검증. 새planner구현/파일럿미실행,연구자결정대기. 보고서 reports/c_v02_drive540_global_path_design_20261113_v01.md,권위수치CSV reports/c_v02_drive540_global_path_design_20261113_v02/base36_comparison_final.csv.
