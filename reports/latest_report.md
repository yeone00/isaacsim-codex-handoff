# v46 — 인식 → B5 위치 → 접근 플래너의 실제 저장자료 분석

2026-11-02 KST. **오프라인 실행 완료.** 원본 RGB-D 972장(324 대응 장면×3표현)을 연결하고, 기존 v44 B5 계산319건에서 old strict-quintic 및 frozen v36 smooth-S를 재실행했다. 예측 목표와 설계 목표를 비교한 플래너 호출은 319×2목표×2플래너=1,276회다. 새로운 B5 추정·모델 추론·학습·HPO·Kit·physics·조향·로버 주행은 모두0이다. 이는 319회 로봇 작업 검증이 아니다.

**HUMAN_REVIEW_GATE=PENDING / POSITION_ESTIMATES=EXPLORATORY_UNVALIDATED / HUMAN_REVIEW_HOLD.** v44의 `HUMAN_REVIEW_BEFORE_ROLLOUT=FAIL`, v45 추가918 `NOT_RUN`을 그대로 유지한다. 원래 값은 수정하지 않았다. 사람 서명0건이며 검토 패키지 생성이나 AI의 그림 가독성 확인을 사람 검토로 세지 않는다.

관측된 핵심은, 마스크 품질과 B5 위치·플래너 판정이 일대일로 이어지지 않는다는 점이다. 공통 B5 장면은79개이며 전체 B5 계산 수83/133/103을 불균형한 채 순위로 해석하지 않았다. 같은 시작점에서 설계 목표로 바꿔도 old 219/319, smooth 219/319가 실패한다. 이 부분은 단순 마스크 문제로 설명할 수 없는 planner/task geometry 제약을 드러낸다. 반대로 설계 목표는 통과하지만 예측 목표가 실패한 old 89, smooth 71건은 **이 고정 오프라인 코드에서 목표 좌표 차이에 민감한 사례**다. 동역학 인과효과나 실제 로봇 성공의 증명은 아니다.

## 입력 계보와 보존

새 외부 root: `/home/user/hh/isaac_cosmos/sdg_final/PERCEPTION_TO_ROBOT_20261102_v46`. v43/v44/v45 원본은 읽기만 했다. 보고서명에 causal audit가 들어가지만, segmentation→pose 상관은 관찰적 탐색 분석이고 terminal-target 치환만 통제된 오프라인 계산이다.

- v43 original972는 실제 RGB-D 정적 capture이며972 robot runs가 아니다. exact scene_id324×render3, base_scenario_id108×O3을 유지했다. 카메라 수치T·seed·range·view·material·C·lighting·trajectory를 대응 검사했다. actual occlusion은 표현별 실측값을 그대로 보존했고 명목O로 대체하지 않았다. 원래 잘못된 metadata calibration SHA 필드는 수정하지 않고 corrected calibration의 원시 projection/view 복원 계보를 연결했다.
- v45 cross2916=972 같은 이미지×3모델. diagonal972의 모델/이미지 SHA·mask pixel diff0·IoU 차<1e−12를 재확인했다. off-diagonal1944는 **mask 결과만** 있다. `v46_cross_model_mask_sources_2916.csv`에 예측 result/candidate masks/선택mask 경로·SHA·후보 confidence/GT IoU를 연결했다. 2916 pose 결과를 만들거나 추정하지 않았다. 선택은 최고confidence/동률최소index였으며 GT best-instance는 평가 진단이다.
- v44 existing972=계산319/ROI datum거절479/무검출174/source unavailable0. v45b54=계산51/거절1/무검출2, 같은 원본54장의 재분석이다. **319+51=370 독립관측으로 합치지 않았다.** v45b918 NOT_RUN을 유지했다. v44의 별도 corrected occluder 새54장은 이번 original972 분석의 분모에 섞지 않았다.
- 3그룹 HR_Scan/LR_Scan/GeoCAD만 비교했다. LR은 저감 취득 조건의 독립 재구성이며 HR decimation이 아니다. Proxy의 과거 잠금·기록은 보존했다.
- expected SHA 10,721건(기존 v45 inventory10,525+v43 preflight193+3모델) 대조 PASS. 추가 v30/v36/v38 source authority 대조 1019 PASS, 독립 expected 없는 15건 UNKNOWN. 원본3 root 전체와 실행 source를 포함한 27930파일의 시작/종료 SHA 불변 PASS. expected를 갱신하여 맞춘 항목0이다.
- known9 protocol SHA 및108/432 count PASS. 실제 읽은 prelock v01→amendment v02/v03→geometry v02의 JSON 내용은 `authority_content_read.json`; geometry lock 자체 독립 expected는 UNKNOWN이다. frozen 모델3개 SHA는 `run_manifest.json`과 `input_expected_sha_checks.csv`에 있다.

`v46_case_lineage_972.csv`는 exact case/scene/render/model·camera/scene seed·실측 가림·이미지/depth/model/calibration/result SHA·v44/v45 상태를 포함한다. SHA inventory로 고정하며 무검출/거절/NOT_RUN을0mm로 채우지 않았다.

## 단계별 수율과 계산된 사례만의 오차 — HUMAN_REVIEW_HOLD

| representation | selected | detected | mask_iou_ge50 | B5_computed | datum_rejected | no_detection |
| --- | --- | --- | --- | --- | --- | --- |
| GeoCAD | 324 | 268 | 267 | 103 | 165 | 56 |
| HR_Scan | 324 | 238 | 231 | 83 | 155 | 86 |
| LR_Scan | 324 | 292 | 218 | 133 | 159 | 32 |

원래 diagonal unconditional IoU(무검출0)는 HR .677861/LR .635470/CAD .744906, v45 equal-domain mean은 HR .614619/LR .538966/CAD .707187이다. 이는 geometry와 해당 matched frozen model이 함께 달라진 조합이며 표현 단독 효과는 분리되지 않는다. 같은 이미지에서 모델만 달리한 v45는 mask 비교까지만 가능하고 B5 비교로 확대 해석하지 않았다.

세 표현 모두 검출218/324, 모두 mask IoU≥.5인 장면173/324다. 아래 오차 표의 분모는 전체324가 아니라 **각 표현에서 계산된 사례만**이다. 단독 표현별 조건부 분포를 우열 순위로 사용하지 않는다.

| representation | n_computed_only | v44_center_error_norm_mm_median | v44_center_error_norm_mm_p90 | v44_center_error_norm_mm_p95 | abs_yaw_error_deg_median | abs_yaw_error_deg_p90 | abs_yaw_error_deg_p95 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GeoCAD | 103 | 93.395890 | 371.807453 | 415.732064 | 1.365112 | 82.997261 | 89.998986 |
| HR_Scan | 83 | 88.179419 | 404.213417 | 433.887045 | 1.061836 | 89.740131 | 89.960363 |
| LR_Scan | 133 | 219.746089 | 2202.443377 | 2234.775508 | 29.390469 | 70.482672 | 89.641352 |

XY 기준은 원래 authored task-design center(−25.888,30.509)m, pred−datum이다. longitudinal=+Y, left=−X, XY norm은mm. 독립 실물 metrology·사람 검증 중심이 아니다. B4/B5 yaw 오차는90° 기준 modulo180(−90≤e<90)이며 PRE/FINAL의 고정 +90° 방향 yaw와 구분했다. 단일 class `brick_load`이므로 red/cement semantic 분류 정확도를 주장하지 않는다.

계산되었어도 평가 대상 mask와 맞지 않는 사례를 따로 집계했다. LR 계산133건 중49건은IoU<.5이며 그중17건은IoU0이다. LR의 많은 계산 수에는 잘못된 물체/영역을 사용했을 가능성이 있는 결과가 포함된다. 이는 사람의 ROI 정체성 검증을 대신하지 않는다.

| representation | evaluation_match | n | median_XY_mm | p95_XY_mm | human_review_status |
| --- | --- | --- | --- | --- | --- |
| GeoCAD | IoU_lt_0.5 | 0 |  |  | HUMAN_REVIEW_HOLD |
| GeoCAD | IoU_ge_0.5 | 103 | 93.395890 | 415.732064 | HUMAN_REVIEW_HOLD |
| GeoCAD | IoU_eq_zero | 0 |  |  | HUMAN_REVIEW_HOLD |
| HR_Scan | IoU_lt_0.5 | 5 | 197.347698 | 295.619488 | HUMAN_REVIEW_HOLD |
| HR_Scan | IoU_ge_0.5 | 78 | 86.007438 | 439.331325 | HUMAN_REVIEW_HOLD |
| HR_Scan | IoU_eq_zero | 0 |  |  | HUMAN_REVIEW_HOLD |
| LR_Scan | IoU_lt_0.5 | 49 | 1283.947090 | 2235.428856 | HUMAN_REVIEW_HOLD |
| LR_Scan | IoU_ge_0.5 | 84 | 81.153032 | 411.563734 | HUMAN_REVIEW_HOLD |
| LR_Scan | IoU_eq_zero | 17 | 2202.444422 | 2235.428856 | HUMAN_REVIEW_HOLD |

거리·view·material·C·명목O의 전체 yield와 conditional signed long/left/yaw·XY median/p90/p95는 `v46_pose_yield_and_errors.csv`, absolute yaw 및 actual occlusion 기술 구간(0–10/10–30/30–60%, 사후 시각화용이며 제외 기준 아님)은 `v46_conditional_robust_errors.csv`에 있다. 원래 B5 `n_points/n_top_points/n_side_points`, inside rate, score, ROI count/inlier 비율은 `v46_computed_support_and_errors_319.csv`에 수록했다.

## 대응 3표현 위치 비교 — HUMAN_REVIEW_HOLD

all-three B5 computed **79 scene triplets /47 base clusters**. 모두검출 조건을 더해도79, 모두IoU≥.5까지 요구하면 **69 triplets /46 clusters**다. 전체 검출218 또는 IoU≥.5 173을 위치오차 분모로 사용하지 않았다. 긴형식 `v46_matched_pose_triplets.csv`는237행=79×3이고, `v46_matched_pose_triplets_wide79.csv`는79행이다.

| subset | representation | n | XY_median_mm | abs_yaw_median_deg | human_review_status |
| --- | --- | --- | --- | --- | --- |
| all_computed | GeoCAD | 79 | 85.890157 | 1.174698 | HUMAN_REVIEW_HOLD |
| all_computed | HR_Scan | 79 | 85.200573 | 0.351547 | HUMAN_REVIEW_HOLD |
| all_computed | LR_Scan | 79 | 90.506628 | 0.663193 | HUMAN_REVIEW_HOLD |
| all_computed_IoU50 | GeoCAD | 69 | 79.339202 | 0.547951 | HUMAN_REVIEW_HOLD |
| all_computed_IoU50 | HR_Scan | 69 | 73.761024 | 0.308297 | HUMAN_REVIEW_HOLD |
| all_computed_IoU50 | LR_Scan | 69 | 84.739887 | 0.509377 | HUMAN_REVIEW_HOLD |

아래는 **사례별 오차 차이의 중앙값(a−b)**다. 표현별 중앙값을 먼저 뺀 값과는 다르다. 동일 base_scenario_id 내 O3을 함께 재표집한 percentile bootstrap 2,000회/95% CI, 고정seed26110246. 선택된 computed subset에 조건부인 탐색 CI이며 다중비교 확증·일반화·동등성/비열등성 판정이 아니다.

| subset | rep_a | rep_b | triplets | base_clusters | median_paired_delta | ci95_lo | ci95_hi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_three_computed | HR_Scan | LR_Scan | 79 | 47 | 0.230690 | -0.264881 | 0.769035 |
| all_three_computed | HR_Scan | GeoCAD | 79 | 47 | -0.852098 | -2.293257 | -0.342927 |
| all_three_computed | LR_Scan | GeoCAD | 79 | 47 | -0.616487 | -1.436388 | 0.011759 |
| computed_and_all_iou_ge50 | HR_Scan | LR_Scan | 69 | 46 | 0.305429 | -0.009343 | 0.897440 |
| computed_and_all_iou_ge50 | HR_Scan | GeoCAD | 69 | 46 | -1.005683 | -2.811179 | -0.394716 |
| computed_and_all_iou_ge50 | LR_Scan | GeoCAD | 69 | 46 | -1.023021 | -1.650652 | -0.333597 |

signed modulo180 yaw의 같은 paired CI는 `v46_matched_pose_paired_CI.csv`, absolute yaw 오차 차이의 별도 CI는 `v46_matched_abs_yaw_CI.csv`(seed26110247)다. CI가0을 포함한다는 이유로 동등성을 주장하지 않는다. mask 품질 선택을 추가하면 분석 대상 자체가 달라진다.

전체324의 paired categorical availability:

| rep_a | rep_b | denominator | both_computed | a_only | b_only | neither | human_review_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HR_Scan | LR_Scan | 324 | 82 | 1 | 51 | 190 | HUMAN_REVIEW_HOLD |
| HR_Scan | GeoCAD | 324 | 80 | 3 | 23 | 218 | HUMAN_REVIEW_HOLD |
| LR_Scan | GeoCAD | 324 | 99 | 34 | 4 | 187 | HUMAN_REVIEW_HOLD |

각 장면의 세 상태(COMPUTED/REJECTED/MISS)는 `v46_availability_all324.csv`에 모두 남겼다. LR의 추가 계산 사례에 false-load ROI/큰 오차가 포함될 수 있으므로 계산 수가 많다는 사실을 위치 품질로 해석하지 않는다.

## 마스크 → 위치 연관과 반례 — EXPLORATORY / HUMAN_REVIEW_HOLD

319 computed에서 원래 IoU·confidence·유효 depth support·ROI count/inlier count/ratio·range·actual occlusion과 XY norm의 Spearman을 계산했다. base cluster bootstrap2,000회/95% CI이며, 이는 검출/ROI가 통과한 표본으로 조건화된 상관이다. 원인 기여·센서 절대 정확도·픽셀 IoU의mm 환산으로 해석하지 않는다.

| representation | n | rho | ci95_lo | ci95_hi |
| --- | --- | --- | --- | --- |
| ALL | 319 | -0.541063 | -0.661264 | -0.414536 |
| GeoCAD | 103 | -0.313173 | -0.501448 | -0.086708 |
| HR_Scan | 83 | -0.223941 | -0.421698 | -0.026503 |
| LR_Scan | 133 | -0.783874 | -0.867578 | -0.659134 |

다른 변수의 결과는 `v46_spearman_cluster_CI.csv`, 원래319행+confidence·depth/ROI·range/view/material/C/actualO·signed long/left/yaw·norm은 `v46_mask_vs_pose_scatter.csv`와 support 보강표다. `selected_instance_correctness`는 평가 GT IoU≥.5 matching이라는 운영 정의이며 사람의 물체 정체성 검증이 아니다.

높은IoU(≥.8) 중 큰 위치오차 상위 사례와 낮은IoU(<.5) 중 작은 오차 사례를 관측 후 진단용으로 추렸다. small은 이 subset 내 상대적 표현이며 로봇 허용오차 통과라는 뜻이 아니다.

| case_id | pixel_iou | v44_center_error_norm_mm | v44_yaw_error_deg | selection |
| --- | --- | --- | --- | --- |
| FE2E_S097_O50_v43_HR_Scan | 0.941452 | 498.704740 | 0.083931 | IoU>=.8; largest XY error |
| FE2E_S045_O50_v43_HR_Scan | 0.857672 | 489.962286 | -29.999962 | IoU>=.8; largest XY error |
| FE2E_S098_O50_v43_GeoCAD | 0.900787 | 479.465826 | 0.168350 | IoU>=.8; largest XY error |
| FE2E_S039_O0_v43_HR_Scan | 0.308154 | 79.583083 | -0.022987 | IoU<.5; smallest XY error |
| FE2E_S046_O25_v43_LR_Scan | 0.471091 | 107.359343 | 0.222862 | IoU<.5; smallest XY error |
| FE2E_S046_O50_v43_HR_Scan | 0.494590 | 109.779376 | 27.166515 | IoU<.5; smallest XY error |

이 반례는 B5 datum/고정치수/visible-face/잘못된 ROI/heading·depth 지원을 함께 검토할 이유다. 어느 하나를 독립 원인으로 확정하지 않았다. `v46_mask_vs_pose_scatter.png`, `v46_stratified_pose_errors.png`는 실제 CSV로 그렸고 HUMAN_REVIEW_HOLD를 표시했다.

## 위치 → 플래너: 재현과 설계목표 치환 — HUMAN_REVIEW_HOLD

v30 실제 executed follower `plan`만 AST로 추출하여 legacy module import를 피했다. frozen v36은 pure CPU 함수다. 시작 base pose는 같은 calibrated optical T와 기존 camera offset .5381308867332306m/.00002232m에서 복원했다. rear offset .338m, wheelbase .7m, steering15°, curvature bound .95×tan15°/.7=**.363645332585095/m**, PRE=center−2.203745031260775×(+Y), goal yaw+90°를 유지했다. B5 heading을 goal yaw로 쓰지 않았다.

`PREDICTED_TARGET`: 실제 저장 B5 center로 기존 PRE 생성. `DESIGN_TARGET_ORACLE_OFFLINE`: 같은 case/start/planner에 terminal center만 원래 design center로 치환한다. design/GT는 이 오프라인 평가 분기에만 쓰고 sensor/B5/driver 입력으로 넣지 않았다. 이름의 oracle은 목표 치환 진단이며 독립 물리 GT·항상 도달 가능한 목표라는 뜻이 아니다.

**역사 재현 PASS:** old11/319, smooth29/319, 319개 각각의 두 상태/reason을 모두 재현했다. old 진단은 curvature 예외 하나만 제거한 별도 사본으로 거절 이후 후보 kmax를 계산했으며 승인으로 바꾸지 않았다. smooth primitive의 sample kmax와 conservative upper를 구분했다. LOCAL_PATH_DISTANCE, FORWARD_GOAL_REQUIRED, bracket/forward/curvature/이름 없는 assertion을 그대로 reason으로 남겼다. 계산값이 없는 열은 blank이며0곡률로 채우지 않았다.

| planner | representation | denominator | predicted_pass | oracle_pass | both_pass | pred_fail_oracle_pass | pred_pass_oracle_fail | both_fail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| old | ALL | 319 | 11 | 100 | 11 | 89 | 0 | 219 |
| old | GeoCAD | 103 | 4 | 36 | 4 | 32 | 0 | 67 |
| old | HR_Scan | 83 | 4 | 30 | 4 | 26 | 0 | 53 |
| old | LR_Scan | 133 | 3 | 34 | 3 | 31 | 0 | 99 |
| smooth | ALL | 319 | 29 | 100 | 29 | 71 | 0 | 219 |
| smooth | GeoCAD | 103 | 8 | 36 | 8 | 28 | 0 | 67 |
| smooth | HR_Scan | 83 | 11 | 30 | 11 | 19 | 0 | 53 |
| smooth | LR_Scan | 133 | 10 | 34 | 10 | 24 | 0 | 99 |

both_fail은 고정 planner/search 범위·시작/목표 geometry 제약이 남는 경우다. oracle만 pass이면 예측 중심 차이에 의한 이 코드의 pass→fail 전환을 관측한 것이다. predicted만 pass이면 잘못된/다른 목표가 오히려 곡률을 낮출 수 있으므로 곡률 pass 자체가 정확한 작업을 뜻하지 않는다. 다른 안전한 경로가 존재하지 않는다는 증명도 아니다.

각319건의 start/goal, rear local distance·forward projection, strict reason, sampled/upper curvature, 후보 arc length·수학 endpoint residual, paired transition은 `v46_planner_predicted_vs_oracle_319.csv`. endpoint residual은 경로 생성 수학값이며 실제 로버 endpoint가 아니다. 목표별 이유 분포는 `v46_planner_reason_counts.csv`에 있다.

**전체 swept collision/footprint/support = NOT_EVALUATED.** 기존 v35 checker는 nominal saved stage3개와 해당 rover collider13개·instance-aware steering·floor triangle을 연다. v43은 stopped 렌더 장면의 표현/C/O/카메라 변경 capture이며, 사례별 authoritative occupancy/변환된 obstacle·articulated footprint/support binding이 인증된 입력으로 저장되어 있지 않다. v35 nominal PASS를 이319건에 이식하지 않았다. 따라서 full offline geometry 평가 분모0, admission N/A, actual PRE/FINAL0, both stops0, robot success rate N/A다. `v46_task_funnel.csv`에서 이 단계들을 분리했다.

![오프라인 단계 비교](/home/user/hh/isaac_cosmos/sdg_final/PERCEPTION_TO_ROBOT_20261102_v46/v46_task_funnel_comparative.png)

## 사람 검토 패키지와 실구동 판단

`review/`에 **v45b pilot54 전체 + v44 curated24 = 78사례**를 준비했다. original RGB, 원 depth symlink(원본 경로/SHA), 원래 또는 거절된 후보 ROI, selected inlier mask, depth heatmap, plane normal·residual histogram, B5 estimate/design overlay와 case별 evidence.json, 기본 contact sheet13장이 있다. 최초 curation의 무검출7개 패널/접촉표/checklist는 `review/initial_package_before_curated_refinement/`와 기존 사례 폴더에 추가 보존했다(기본78사례와 별도). 거절된 후보는 diagnostic only로 표시했고 selected/accepted ROI로 바꾸지 않았다. plane이 없는 miss/reject는 원인·빈 residual로 표시했다. 중심 overlay는z=.144m로 투영한 평가 표시이며 metrology가 아니다. curated는표현/거리/view/C/O/상태를 넓게 포함하고 심한 outlier를 더한 진단 선택으로 통계표본을 추가하지 않는다.

`review/human_review_checklist.csv`의 `approve_reject_needs_revision`, notes, reviewer, signed_at는 **전부 빈칸**이다. 독립 file SHA는 `review/file_sha256.json`. 사람이 각 원영상·ROI의 pallet 정체성·깊이/평면/오염을 검토해 서명하기 전에는319 검증완료나 신규918/2916 B5 확대를 주장하지 않는다. optional cross-model54 B5 진단도 이번에는 실행하지 않았다.

`MOTION_BLOCKER_DECISION.md`는1페이지 후속 결정이다. v38의 단일 정책 진입 blocker인 **승인된 실측 조향속도 중단 규칙**이 확인되지 않았다. policy_check가 요구하는 stationary yaw/tracking tolerance의 authority, native sole writer·zero/braking·복원·지지/충돌은 여전히별도미검증이다. configured286.48°/s·명령15°·계산요구rate를 허용 실측속도로 대신하지 않았다. 정책을 기록할 위치, 승인 후 최소 정지 검증, 동일 조건3표현 pilot 제안은 있지만 **실행0**이며 추가live 명시승인 없이는 시작하지 않는다.

역사 v30 HR simulator1회: perceived 목표2.79451mm 대비 design55.23288mm. v31LR/v32CAD는이동전old곡률거절. v35 27offline/v36 55,221CPU검사는물리주행이아니다. 현재v46은기존물리결과를추가하지않는다.

## 실행·검사·실패·변경 범위

주 실행:

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python -u analysis/three_rep_perception_pose_planner_20261102_v46.py
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/three_rep_perception_pose_supplement_20261102_v46.py
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/three_rep_perception_pose_report_20261102_v46.py
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/three_rep_perception_pose_finalize_20261102_v46.py
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/verify_known_locks.py --out /home/user/hh/isaac_cosmos/sdg_final/PERCEPTION_TO_ROBOT_20261102_v46/known_locks_v46.json
```

완료 phase는 integrity/linkage/planners/review/final_verify 각각 status JSON에 PASS를 저장했다. 부분 planner50건마다 CSV checkpoint를 남겼다. 중단 후 `--resume`은완료PASS phase를건너뛰며 원본을변경하지않는다. `run_manifest.json`, source snapshots, input/output SHA, `execution.log`, supplement/report 실행기록에환경·command·seed·코드SHA를기록했다. 경로가이미있는초기실행은거부한다.

보존된 구현/점검 실패: 부수검색1회가존재하지않는v35분석파일경로로rg exit2를냈다. authority inventory 첫parser가expected없는observed-only행에서KeyError/exit1이었다(`source_authority_attempt01_FAILED.json`). 새parser는expected없는15건을UNKNOWN으로남겼고expected1,019건PASS를확인했다. 이는모델/로봇시행이아니며319분모에서빼거나성공으로꾸미지않았다. main scatter의 B5 support count 일부 보강열은원래pose field명을잘못참조해blank였으므로, supplement에서실제`n_points/n_top_points/n_side_points`로별도보강표를생성했다. 기존B5값변경0. 초기 curated24에 무검출7건이 포함된 것을 확인해 최종 기본 checklist는 계산/거절24건으로 보강했다. 초기 checklist·접촉표와 무검출 패널7개는 별도 보존했다. 첫 보강 helper는 AST에서 같은 변수명을 가진 다른 loop를 선택해 NameError/exit1이었으며(`review_refine.log`), 새v03이 정확한 image loop만 선택해7개 패널을 추가하고 기본78사례 접촉표를 재생성했다. 추정/추론 재실행은0이다.

PASS: 972계보/324paired/2916mask-source/319상태재현/79·69matched/cluster CI/수율·실측그림/78검토패널/원본SHA보존. PENDING: 사람서명. UNKNOWN: 독립물리metrology·geometry lock 자체expected·실제 actuator소유/응답·remote sync. NOT_EVALUATED: 이장면의fullgeometry. NOT_RUN: 신규B5추정·새모델추론·훈련/HPO·Kit/physics/ROS/driver/조향/로버이동.

새코드6개(analysis main/supplement/report/finalize/review refine02·03), 본보고서, latest_report, PROJECT_STATE 및외부v46산출물을작성했다. 원본v30–v45보고서/weights/USD/GT/splits/media는수정하지않았다. 별도축소모형영상9편/136parent/4080inference의기존PROJECT_STATE기록과보고서는독립증거로보존했고재실행0이다. Git이없는로컬workstation에서는stage/push/remote완료를주장하지않으며동기화UNKNOWN이다. handoff marker는보고서sync요청이며실험승인이아니다.

다음구체행동은78사례의사람ROI/inlier검토·서명이다. 검토된datum/ROI정책을고정한뒤에만별도B5확대범위를정한다. 실구동은별도의승인된조향중단정책과완성된one-shot검증소스가필요하다. 비유의성을동등성으로해석하지않고, 이미평가된RealTest189를모델선택에재사용하지않았으며red-only외부검증을cement/실로봇배포로일반화하지않았다.

최종 패키지 검사: 972/319/79·69 및 기본 검토78(54+24), 사람 결정칸 전체 공백, old11/smooth29, expected10,721건 종료 재대조 PASS. curated24는 계산11/거절13이다. 별도 보존한 최초 무검출 패널7개를 기본24의 계산/거절 수로 세지 않았다. 독립 depth heatmap 생성에서 무한 깊이를 표시용 수로 바꾸는 곱셈에 RuntimeWarning1건이 발생했으며 finalize.log에 보존했다. 표시값은0–6m로clip하고 비유한/0이하 깊이는black처리했으므로 이 경고를 센서/pose 수정이나 실패 사례 삭제로 해결하지 않았다. 원depth는그대로다.
