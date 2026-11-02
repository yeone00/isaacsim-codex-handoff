# v32 — 세 번째 GeoCAD pilot: 인식 성공, 동일 PRE 곡률 admission 실패

2026-11-02 KST. **GeoCAD exploratory pilot 0/1 FAIL, Kit 1회·retry0.** 새 RGB-D→matched frozen GeoCAD M50→B4→직접 검토 ROI138/138→B5까지 PASS했으나, 원래 quintic PRE 최대곡률 **0.366967770/m > 공통 0.363645333/m**으로 `CURVATURE_INFEASIBLE`에 거절됐다. driver·비영 명령·PRE/FINAL 주행은 시작하지 않았다. 기존 LR 실패를 구제하거나 공통 planner를 변경하지 않았다. 과학 confirmatory 분모0, HPO/training PAUSED, 324/432 미실행이다.

## 입력·파생·사전 검사

새 외부 root는 `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_GEOCAD_ADMISSION_20261102_v32_01`이다. 준비된 `prepared_site_drive.usda` 하나와 실행 overlay `attempt_0001/site_drive.usda`를 작성했다. 별도 scratch scene·두 번째 Kit root·HR/LR 재실행은 없다. 정확한 scene SHA와 저장자료 곡률 산술은 [runtime summary](construction_site_runtime_summary_20261102_v32.json), 실행 입력·스냅샷·명령·환경은 root의 `prepare.json`, `code_versions.json`, `executed_code/`에 있다.

아래 입력을 실제 hash로 확인했고 v24 manifest dependency/pairing checker도 통과했다.

| GeoCAD 입력 | 경로 | SHA256 |
|---|---|---|
| normalized cement | `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_GeoCAD.usd` | e579f77f46debf05fca23d6bfc5c08217cc9541b3d932dee1088559cbef4699b |
| frozen matched M50 | `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_GeoCAD_M50_REALVAL_MASKBEST_v01.pt` | bbfb9fc8d0c421154844f7e299b6d8162b9394eb07d36a31110f593c0813ce8f |
| v24 parent | `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/GeoCAD/pilot_scene.usda` | d806cc64179dbbe6f394bf2d05b7a13be0500375d193505b04a90a0cbe448826 |

[공유 visual 검사](construction_site_instancing_checks_20261102_v32.json) PASS: 실제 선택 placement300/prototype1, 전체 instance322, 선택 mesh1/배치, native enabled0, union28, 이전 visual과 bound 차0m. GeoCAD mesh의 여섯 material subset(back/bottom/front/left/right/top)을 실제로 검사했다. 전체 face를 중복 없이 덮고 각각 활성 material에 bind된다. root-mesh 직접 binding을 가정하지 않았다. Proxy USD/packaged appearance 의존성은 유지하며 Proxy 비교군 추가가 아니다. inherited HR branch 혼합0, per-instance 대형 geometry 복제0, visual 속성 digest 전후 동일. 변조5/5 거절, capture AST 동일 PASS.

[공통 월드](construction_site_fixed_scene_checks_20261102_v32.json)는 HR v30 대비 load 밖2065 active prim의 transform/schema/속성 source stack/관계/연결 signature와300 slot transform exact 일치다. 원래 rover/start/camera/illumination/supplier graph, static28 safety consumers, mounted rolltainer fallback과 inactive mount API correction을 보존했다. [코드 parity·보존](construction_site_parity_20261102_v32.json): session/capture/adapter/runner는 버전·표현명 정규화 후 v31과 정확히 같다. 원래 target 생성+90°/local_-X, quintic 경로, rear offset.338m, .95×tan15°/.7 곡률 한도, speed.02m/s, steering, TF/GID, GC8GiB/+768MiB/600s, PRE/FINAL5mm/2° 및 quiet≥1s 정책 변경0. 안전 gate 완화·horizon 연장·목표 이동·과거 pose 입력0.

실제 명령은 `python3 scripts/construction_site_perception_runner_20261102_v32.py --run`이며 기본 root는 위 경로다. 실제 Kit launcher는 기존 `hh_isaac51/bin/python`, perception worker는 기존 `sdg_tools/bin/python`, ROS Jazzy/domain191이다. 설치·업그레이드 없음.

## 새 관측·실패·종료

Fresh640×480 RGB/axial depth/calibration8/8 PASS. RGB SHA `8468a038d485436fd16611efab511a653b1a2ee2ffcdde4d882b30e1d8f4b0b3`, depth SHA `b70fadfd84dd6ab6c161e93553564da6a63c2da8ab9a93c2bf29260daf58390e`. frozen GeoCAD inference1회 conf.959305346/mask7703, B4 heading89.453897834°/margin.008906575.

동일 reviewer `Codex-visual-review-v28`가 새 RGB, 새 detection overlay, count-only raw ROI overlay를 직접 보고 preview1/최종1로 확정했다. polygon [(236,197),(250,183),(384,183),(403,197)]은 보이는 팔레트 상면에 근거해 선택했고, 이전 annotation을 입력하지 않았다. 제외영역을 건너는 중앙은 새 YOLO mask로 제거됐다. raw2275/erosion1573/brick exclusion1435/valid138, exclusion 잔존0. window 개시 약21.47초에 preview,180초 내 final. B5/목표 열람은 final 뒤였다. 운영자가 표현을 아니 완전 맹검은 아니다.

B5 inlier138/138, tilt.079799336°, p95 residual1.08570e−7m, 기존 RANSAC400/3mm/100점/80%/tilt5°/covariance gate PASS. 잔차는 독립 정확도 증명이 아니다. 새 B5 center=(−25.9367052594,30.4783510578), heading89.453897834°이며 실제 목표는 `predicted_pre_final.json`에 있다. 중간 B4 JSON의 B5 NOT_EVALUATED를 최종 실패로 읽지 않는다.

PRE 경로 생성에서 곡률 초과로 sweep/driver 전에 거절됐다. 저장 baseline과 새 목표에 대한 독립1mm sample quintic 산술도 같은 실패를 재현하며 runtime 예외가 일차 증거다. 대체 경로 탐색·구현·실행은 하지 않았다. 실제 PhysX28/native0/consumer28, stationary support2214/2214·6wheel contact, parser Error0·예상외/shell하중 contact0, graph/capture guard PASS. 이는 정적 적재 support 범위이며 native 적재 동역학 검증은 아니다.

Kit exit0/observer exit0/driver NOT_STARTED/runner exit1·NOT_READY, `MISSING_WITNESS` 보존. ROS zero receipt **MISSING/NOT_APPLICABLE_PRE_DRIVER**다. cleanup request/direct graph zero/baseline quiet는 정상 접근 정지 인증을 대체하지 않는다. PRE/FINAL, 두 normal zero/quiet certificate, 측정 PRE 뒤 FINAL sweep은 모두 NOT_RUN. watchdog/강제종료/timeout0, owned PID잔존0. close-enter는 기록됐으나 Python close-return checkpoint는 없으므로 native 반환 인과는 UNKNOWN이다.

Owner PID2740591 phase RSS는 startup4.3412→derived4.6378→attached5.6841→settled6.0097→capture후6.0447→worker전후6.0536GiB, sampled 최대6.05355GiB다. owner VRAM은 settled8843MiB/capture후8844MiB/worker후8834MiB이며 RustDesk535MiB는 별도다. PSS/private/wall/sourceSHA 원시는 `phase_memory_v32.jsonl` 및 witness에 있다. pre-perception8GiB admission PASS, motion GC scope는 NOT_ENTERED이며 +768MiB/600초 PASS로 세지 않는다. 연속 peak 측정 주장은 하지 않는다.

## 동일 정책 아래 세 행

각각 frozen representation-matched M50와 해당 normalized cement asset을 사용했다. HR/LR의 정확한 path/hash·원시 증거는 [v30](construction_site_pilot_hr_admission_20261102_v30.md), [v31](construction_site_pilot_lr_admission_20261102_v31.md)에 보존된다.

| 표현/모델 | 새 RGB-D·YOLO/B4/B5·ROI | B5 center XY(m) | PRE 최대곡률(/m), bound .363645333 | 실제 이동·정지·결과 | phase 최대 RSS / owner VRAM | Kit/driver/observer/runner |
|---|---|---|---|---|---|---|
| HR_Scan / HR M50 v30 | 모두 PASS,114/114 | −25.9348213,30.4817854 | .350094192 PASS | PRE2.883526mm/FINAL2.794514mm, 각 normal zero/quiet PASS;1/1 | 6.7516GiB / settled8796MiB | 0/0/0/0 |
| LR_Scan / LR M50 v31 | 모두 PASS,132/132 | −25.9398327,30.4819942 | .387170521 FAIL | CURVATURE_INFEASIBLE, motion0, PRE/FINAL NOT_RUN;0/1 | 6.18753GiB / settled8719MiB | 0/미시작/0/1 |
| GeoCAD / GeoCAD M50 v32 | 모두 PASS,138/138 | −25.9367053,30.4783511 | .366967770 FAIL | CURVATURE_INFEASIBLE, motion0, PRE/FINAL NOT_RUN;0/1 | 6.05355GiB / settled8843MiB | 0/미시작/0/1 |

공통 물리는 세 행 모두28/native0·support2214/2214·six-wheel/graph/contact gate PASS다. HR만 주행 support·두 독립 정지까지 검증됐다. 실패는 pipeline의 실제 기술 결과이며 missing-at-random이나 일반적인 표현 열등성으로 취급하지 않는다. posthoc GT prediction error는 이번 비교에서 별도 검증 산출물이 없어 UNKNOWN; LR/CAD task GT endpoint error는 주행이 없어 NOT_ASSESSED다. HR observed-goal endpoint 오차도 canonical GT task 오차와 다르다. 각 n=1/순차 실행/수동 review로 통계결론·동등성·비열등성·충분한 신뢰도를 주장할 수 없다. LR은 독립 저감 acquisition 재구성이며 HR decimation이 아니다. red-only real 검증을 cement·실로봇 배포로 일반화하지 않는다.

## 검사·변경·다음 작업

[독립 witness](construction_site_pilot_witness_20261102_v32.json): 실행 입력/snapshot/provisional digest/가용 evidence hash PASS, engineering_success=false, owner잔존0. HR v30 raw218와 LR v31 raw192은 종료후 hash 보존 여부를 runtime summary에 기록했다(각각 불일치0). known9/count108/432 PASS, inherited v24 dependency/pairing PASS, compile PASS, stopping adapter CPU8/8 PASS. 실패 run은 denominator에서 삭제하지 않았다. 원래 full event-aware v21 verifier는 실행 코드와 독립 witness가 그대로 사용하며 두 leg가 없으므로 certificate를 만들지 않는다.

새 scripts base/link/runner/session/capture/adapter v32, evaluation diagnostics v32, analysis instance/fixed-world/witness/outcome v32, 해당 reports와 latest/PROJECT_STATE를 작성·갱신했다. bulk USD/RGB/depth는 외부 root에 있다. 기존 outputs/source stage/weights/locks/controller/planner/supplier graph는 보존했다.

**다음 별도 작업으로 공통 planner robustness 연구를 권고한다.** LR target X는 HR보다−5.011352mm이고 CAD는 그 사이인데, 현 짧은 quintic admission margin은 세 관측 중 둘을 거절했다. 이는 목표와 planner 조합의 민감도이며 geometry 단독 인과 증거가 아니다. prospective versioned 연구에서 lateral 수mm 변화에 대한 곡률 민감도를 진단하고 동일 steering/장애물/full sweep/support 조건에서 대체 경로 존재 여부를 검증해야 한다. 대체 경로의 물리적 존재는 현재 UNKNOWN이다. 새 정책은 세 표현 모두에 전향 적용하고 fresh trials 또는 명확히 표시한 offline replay로 평가해야 한다. v31/v32 실패의 소급 성공 전환·LR 선택적 수정은 금지하며 v32에는 새 planner 구현/실행이 없다. 사용자 v32의 명시적 지시에 따라 과거 LR 성공 후 CAD 진행이라는 권고만 대체했고, 실패기록과 안전 gate는 바꾸지 않았다.
