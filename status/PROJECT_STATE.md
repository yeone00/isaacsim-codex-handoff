# PROJECT_STATE — 2026-10-13 (Asia/Seoul)

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
