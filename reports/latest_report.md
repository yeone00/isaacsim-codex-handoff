# v31 — 같은 v30 시스템의 첫 LR pilot: 인식 통과, PRE 곡률 admission 실패

2026-11-02 KST. **LR engineering 0/1 FAIL, Kit 정확히1회 / RETRY0.** fresh RGB-D → frozen LR M50 YOLO → B4 → 공통 v28 한 reviewer ROI132/132 → B5까지 PASS. 새 LR PRE 목표의 기존 quintic 경로가 `CURVATURE_INFEASIBLE`로 거절되어 driver 시작·비영 명령·실제 PRE/FINAL은0이다. 목표 보정·controller 변경·재시도는 하지 않았다. **Kit/observer exit0, runner exit1**, zero/정지 증명은 MISSING/NOT_APPLICABLE_PRE_DRIVER다. 정지한 baseline의 quiet PASS를 접근 성공으로 세지 않는다. 과학 분모0, HPO/training PAUSED, GeoCAD0, 추가 HR0.

실행 root: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_LR_ADMISSION_20261102_v31_01`.

```text
python3 scripts/construction_site_perception_runner_20261102_v31.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_LR_ADMISSION_20261102_v31_01
python3 scripts/construction_site_perception_runner_20261102_v31.py --run --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_LR_ADMISSION_20261102_v31_01
```

## 동일 시스템과 입력 확인

v30 실제 prepared plan 입력108개·executed_code96개·raw218개의 hash가 현재 로컬과 일치했다. [HR reference integrity](construction_site_hr_reference_integrity_20261102_v31.json). v24 세 장면 manifest/parent dependency/paired common evidence를 기존 checker로 재검사했고, known9 hash 및108/432 count도 PASS다. geometry lock의 독립 expected SHA는 여전히 UNKNOWN이며 expected를 갱신하지 않았다. frozen4rep/원래 source/USD/weights/v01–v30 결과를 수정하지 않았다.

새 v31 base/link는 v27 선택·mount correction과 v30 shared visual adapter를 복사해 LR 선택 및 class `/PilotLRClass_v31`로만 연결했다. runner/session/capture/diagnostic도 새 버전이다. session은 import 연결 외 v30과 같고, perception adapter는 import·representation/model 선택 외 v28과 같다. [독립 결과/코드 비교](construction_site_runtime_summary_20261102_v31.json). controller·driver·GC·stop·TF/GID·collision·support·cleanup 정책은 원본 그대로다. generic framework나 CAD 실행은 추가하지 않았다.

| 선택 입력 | 실제 경로 | expected=observed SHA256 |
|---|---|---|
| LR normalized cement | `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_LR_Scan.usd` | `5781f72b71940938883f94a1325920a2a87ed768cba37a0000fa6fefd85256e1` |
| frozen LR M50 | `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_LR_Scan_M50_REALVAL_MASKBEST_v01.pt` | `d58e18a87f4cafba6fd92d8bade6e2ff12ad2380db427311b072859fd2cca42f` |
| v24 LR parent | `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/LR_Scan/pilot_scene.usda` | `f652f4cd1db46a661adf1431cdce538562b0cef14e2019b3a2a4b2b8f970c60d` |

새 root의 `prepared_site_drive.usda` SHA `c372314e421c411dfbc543906f153fe220766c30e4c98c3667185f24522b9996`, 실제 `attempt_0001/site_drive.usda` SHA `a5fcb28f7d62bf1dfac393759a85d80502ccc598d7f2653409fe382fafe3b758`. 둘은 copy-on-write overlay이며 원본 수정이 아니다. bulk 자료는 외부 root에만 있다. prepare 입력115개의 경로·해시, 실행 소스 snapshot과 환경/명령은 `prepare.json`, `executed_code/`, `code_versions.json`에 있다.

## Stage A와 실제 pre-driver admission

[정적 검사/변조](construction_site_instancing_checks_20261102_v31.json): instance22→322, prototype23 중 LR300 placements가1개를 공유하고 각 placement의 visible mesh는1개다. inherited HR 가지는 비활성 유지, 원래 AssetRef를 재instance하지 않았다. source stack·geometry·binding/material network의 shared property SHA `3819aa138ac56dba3e1a1b9884d26bc51facf5493084170c8a8870ab057f338c`가 LR parent와 동일하다. 실제 활성 binding은 `$VIS/Normalize/SourceAsset/Looks/material0`; native physics 활성0, static union28이다. bounds 차이 최대1.0658e−14m. instance 해제/원래 branch 재instance/잘못된 HR reference/union 비활성/native physics 활성 변조5/5 거절. 일부 malformed prim 변조는 예외로 fail-closed 거절한다. capture AST도 선택 import를 반영한 LR adapter와 계측 외 동일하다.

[HR 대비 고정 월드 검사](construction_site_fixed_scene_checks_20261102_v31.json): slot world transform300개 exact 동일, load 밖2065 active prim의 값·변환·schema·연결·관계·source stack signature 동일. root layer 및 표현별 v24 overlay 경로 이름만 대응시켜 비교했다. supplier graph/rover/actor/camera/조명/union shape28/fallback/mount/units1m/Z-up 유지다. geometry·texture 배열을300배 dump하지 않았다.

실제 Kit에서는 PhysX interior28/28/native0/safety consumer28, wheel support2214/2214·6wheel contact, parser error0, contact168/예상외·shell하중0, body/DOF·camera·graph 검사 PASS. 실제 새 RGB에서 어두운 LR 적재물과 팔레트 형상을 직접 검토했다. 이 어두운 외관을 조명·재질 보정으로 바꾸지 않았다. common mounted Plane은 frustum 밖이며 authentic AprilTag 복원 주장은 없다. 시작 전 Kit/training conflict 없었고, RustDesk GPU535MiB만 별도 관측했다.

## Fresh LR perception과 한 번의 ROI

640×480 새 mounted RGB/axial depth, actual optical calibration8/8 PASS. RGB SHA `606a28d6b92cd777aa381327be26e8f151a812e3ff9f20a039cbb1528d55a8e9`, depth NPY SHA `0601264f1c706c9a599653149c5e2e55cc0e24b29daa7cf4e5cededf6e17023e`, selected mask SHA `9a7e81db84e74aa0f634ca85ddfd39d9e73f91efea50aa8f4744c378b93968cb`. frozen LR inference1회, conf .972648263, mask7718, B4 heading89.994220915°/margin .048171748.

동일 reviewer `Codex-visual-review-v28`가 새 RGB, 새 detection overlay, count-only raw overlay를 직접 확인하고 preview1/최종1로 확정했다. polygon `[(236,197),(250,183),(384,183),(403,197)]`은 v30과 같지만 새 영상·LR exclusion mask를 검사한 뒤 선택했으며 HR annotation 파일을 입력하거나 자동 전송하지 않았다. 운영자는 표현을 알고 있으므로 완전 맹검은 아니다. B5 pose/GT/downstream 결과 열람은 최종 확정 뒤였다.

raw2275/erosion1573/brick exclusion1441/**valid132**, exclusion 잔존0. 단일 꼭짓점±1px 민감도121–143점. preview26.18초 시점에 제출 검토를 시작했고180초 창 내 최종확정했다. B5 inlier132/132, tilt .079800214°, residual p95 1.0986658e−7m, 기존 min100/RANSAC400/3mm/80%/tilt5°/covariance 기준 그대로 PASS. 작은 residual은 독립 정확도 보증이 아니다. 최종 B5 pose center=(−25.9398326593,30.4819942177), heading89.994220915°, score .072482191. 원래 `predicted_pose_targets.json`은 B4 직후 중간산출물이라 B5 NOT_EVALUATED로 남고, 실제 B5 결과는 `b5_prediction.json`/`predicted_pre_final.json`이다. 중간 status를 최종 실패로 오독하지 않는다.

## 실패 원인과 정지·종료 증거

새 LR PRE=(−25.9398326593,28.2782491865), FINAL=(−25.9398326593,29.0782491865)는 live LR 인식에서만 생성됐다. 실제 공통 stopped start XY=(−25.8879814148,27.4001350403), yaw1.5708023044rad. PRE 경로 생성 단계에서 곡률 제한을 넘었고, swept/support 경로 검사 전 거절됐다. HR 좌표·USD GT를 controller에 넣거나 목표를 옮기지 않았다.

[독립 post-exit 산술](construction_site_runtime_summary_20261102_v31.json)은 저장 baseline/목표와 같은1mm quintic sample 규칙으로 다음을 재현한다. 실제 runtime 예외가 일차 증거이며 이 계산은 실행 구제나 planner 재실행이 아니다.

| 공통 한도/산술 | HR v30 | LR v31 |
|---|---:|---:|
| 허용 곡률 0.95×tan15°/0.7 | 0.363645333/m | 동일 |
| PRE 경로 최대 절대곡률 | 0.350094192/m | 0.387170521/m |
| 첫 한도 초과 | 없음 | t=.155681818, k=.364405607/m |
| PRE target X 차이(LR−HR) | — | −5.011352mm |

이는 동일 짧은 경로의 admission margin이 작은 관측 목표 차이에 민감함을 보여준다. LR 전반의 실패율이나 geometry 단독 원인이라는 증거는 아니다. 경로가 거절됐으므로 실제 PRE/FINAL endpoint 오차·normal zero/별도≥1초 postzero quiet·측정 PRE 뒤 독립 FINAL sweep은 **NOT_RUN**이다.

Kit exit0·observer exit0·driver NOT_STARTED·runner exit1/NOT_READY. `CURVATURE_INFEASIBLE`, finalizer `MISSING_WITNESS`를 그대로 보존했다. 비영 명령0, 실제 ROS zero receipt **MISSING/NOT_APPLICABLE_PRE_DRIVER**. cleanup request·direct graph zero와 baseline quiet1.000000052초는 ROS 수신/normal stop 증명이 아니다. watchdog·강제종료·timeout0, owned PID잔존0. close_enter 기록/실제 exit0가 있으나 Python close_return checkpoint와 native close 인과는 여전히 UNKNOWN이다.

Canonical GT main(11cm/7.3417743229°), strict(5.5cm/3.6860176256°), relaxed(16.5cm/10.938473748°)는 controller의 observed-goal 5mm/2°와 별개다. 이번에는 주행 endpoint 자체가 없어 **task GT posthoc NOT_ASSESSED**다. stationary start를 완료 endpoint로 평가하거나 prediction fit을 task 성공으로 세지 않는다.

## 시간·자원 및 정직한 HR/LR 비교

owner PID2724175의 `/proc/self/statm` RSS와 PSS/private·별도 owner VRAM을 phase별 기록했다. 다음 시간은 같은 owner의 python_start 기준 wall 경과다.

| 단계 | wall s | RSS GiB | owner VRAM MiB |
|---|---:|---:|---:|
| Kit startup | 7.014 | 4.3331 | 3144 |
| scene derived | 16.525 | 4.6241 | 3183 |
| scene attached | 26.708 | 5.8479 | 3528 |
| PhysX settled | 30.817 | 6.1469 | 8719 |
| after fresh capture | 40.981 | 6.1847 | 8780 |
| pre perception admission | 63.054 | 6.1875 | 8770 |
| after B4/ROI/B5 | 105.609 | 6.1875 | 8770 |
| finally paused | 105.720 | 6.1875 | 8770 |
| close enter | 109.037 | 6.1875 | 8770 |

로그 종료는약110.23초, physics elapsed4.283333557s/257steps, 기록75행이다. phase RSS 최대6.18753GiB는 sampled 값이며 전체 기간 연속 peak라고 부르지 않는다. motion-GC scope는 진입하지 않았으므로 +768MiB/600초 gate 결과는 **NOT_ENTERED**, PASS가 아니다. pre-perception8GiB admission은 PASS. 같은8GiB/+768MiB/600초 정책을 유지했다. 원시 PSS/private/VRAM과 sourceSHA는 `phase_memory_v31.jsonl` 및 runtime 요약에 보존했다. RustDesk535MiB는 owner VRAM에 합산하지 않는다.

| 단계 | HR v30 이전 pilot | LR v31 새 pilot |
|---|---|---|
| fresh RGB-D/각 frozen M50/B4 | PASS | PASS |
| 공통 ROI/B5 | 114/114 PASS | 132/132 PASS |
| common PhysX/support | 28/native0,2214/2214 | 동일 PASS |
| PRE admission | PASS | CURVATURE_INFEASIBLE FAIL |
| 실제 PRE/FINAL observed-goal 오차 | 2.883526/2.794514mm | NOT_RUN/NOT_RUN |
| 두 normal zero/quiet certificate | PASS | NOT_RUN |
| Kit/driver/observer/runner exit | 0/0/0/0 | 0/미시작/0/1 |
| 이번 각 후보 engineering 결과 | HR1/1 PASS | LR0/1 FAIL |

두 행은 동일 common controls 아래 기술적으로 서술 비교할 수 있으나 순서·단일수동review·각 n=1 한계가 있다. estimand는 표현+표현별 frozen 모델 pipeline이다. fidelity sufficiency/동등성/비열등성/일반 신뢰도·실로봇 검증 주장을 하지 않는다. LR은 저감 acquisition의 독립 재구성이며 HR decimation이 아니다. real red-only 외부검증을 cement로 일반화하지 않는다.

## 검사·변경·다음 구체 작업

[독립 witness](construction_site_pilot_witness_20261102_v31.json): input115개·snapshot·provisional digest·가용 evidence SHA 모두 PASS, owner 잔존0, engineering_success=false. HR v30 raw218개는 종료후에도 불일치0. compile PASS, 공유instance/변조5/5·공통월드 PASS, 원래 stop CPU20/20 PASS, known9/count PASS. 최초 system Python witness는 cv2 부재로 실패했고 로그를 보존했다. 패키지 설치 없이 기존 `sdg_tools/bin/python`으로 read-only witness를 완료했다. 추가 Kit/관측/모델 실행은 아니다. frozen scientific dependencies의 권위는 바뀌지 않았다.

변경 파일은 새 scripts의 base/link/runner/session/capture/perception_adapter v31, evaluation diagnostic v31, analysis instance/fixed-world/witness/outcome v31 및 해당 reports, latest_report, PROJECT_STATE다. 새 파생 장면1개·실제 Kit root1개이고 offline scratch 재시도0. Git 저장소가 없어 `git status`는 실패했으며 add/commit/push/remote 변경은 하지 않았다.

**다음은 저장된 LR 목표가 현 공통 planner 한도를 넘은 원인과 admission margin을 오프라인에서 검토하는 별도 작업**이다. 이번 LR 실패를 고정하고 controller/목표/threshold를 구제 변경하지 않는다. LR 독립 성공 조건이 충족되지 않았으므로 이번 결과에서 GeoCAD 실행을 권고·개시하지 않는다. 이후 공통 경로 정책 변경이 필요하다면 versioned proposal로 먼저 분리하고 기존 HR/LR 결과를 소급 변경하지 않는다. pilot-only3rep DRAFT/v28 ROI rule은 그대로이며 formal scientific denominator0, HPO/training PAUSED,324/432미실행을 유지한다.
