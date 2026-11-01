# v19b 기준선 동결 및 독립 재현성 v20 — 2026-11-01

**실제 Kit 시도 정확히 2회, 독립 전체 성공 0/2, 추가 실행0. 두 실행 모두 FAIL / NOT_READY / runner exit1이다.** 새 RGB-D → frozen HR YOLO → B4 → **수동 이미지 ROI 보조 B5** → 새 PRE/FINAL 추정 → 실제 ROS PRE 정상 정지는 두 번 통과했다. FINAL에서는 정상 stop 요청 시 `MOVING → ZERO_SETTLING`으로 같은 update 안에서 전환돼, 기존 독립 인증에 필요한 별도 `BRAKING` 기록이 없었다. FINAL 인증·완료 응답 없이 종료됐으며 cleanup/fault quiet를 도착 성공으로 계산하지 않았다.

과거 v19b(`v19_02`) 성공은 **이전 engineering 참고 1회**로 보존하며 이번 반복 수에 포함하지 않는다. 첫 v19 실패도 그대로 실패다. HPO/training **PAUSED**, scientific denominator **0**, 학습·자산 생성·HR/LR/CAD 비교·324/432 formal 실행0. 과학 pilot 준비 완료를 선언하지 않는다.

## A. 먼저 동결한 기준선

[최초 해시 인덱스](../construction_site_v19b_success_baseline_20261101_v20.json)와 [추가 의존성 인덱스 v02](../construction_site_v19b_success_baseline_20261101_v20_v02.json)를 새 파일로 작성하고 각 `.sha256` sidecar를 저장했다. v02는 최초 인덱스를 해시로 참조한다. **최초 인덱스를 덮어쓰거나 역사적 v19_02 기록을 수정하지 않았다.** 인덱스 및 sidecar는 읽기 전용으로 설정했다. 내용 SHA 검사가 보존 근거이며 읽기 전용 권한 자체를 보안상 불변성 보증으로 해석하지 않는다.

최초 인덱스는 준비 입력73개, 실행 Python snapshot69개, v19_02 raw 파일 전체, PRE/FINAL 개별 인증, steps/ROS Twist/wheel/contact/quiet/exit/provisional 증거, HR checkpoint, 환경 entry, seed/설정을 참조한다. Python 원문은 import 없이 메모리 compile 검사했다. 추가 인덱스는 USD 의존성27 layers와 materialized archive/texture, v07 provenance42항목, transitive local code/config, 두 conda 환경 package metadata를 포함한다. 최초268개+추가456개 파일 항목이며 중복 참조가 있다. 과거 expected가 없는 항목은 현재 observed hash만 기록했으며 소급 PASS를 만들지 않았다.

실제 진입은 기존 `scripts/construction_site_perception_runner_20261101_v19b.py`와 `construction_site_perception_session_20261101_v19b.py`다. session source SHA256는 `9b2da203e7c4506b7c96fcd1e6942d95553db72c3b9fc4dc9a3344b064f5a5c8`. 모델은 `FINAL_HR_Scan_M50_REALVAL_MASKBEST_v01.pt`, SHA256 `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`다. Python `/home/user/anaconda3/envs/hh_isaac51/bin/python`, Isaac Sim5.1, perception `sdg_tools`, ROS jazzy/domain191/`rmw_fastrtps_cpp`를 유지했다. 실제 argv·Python version은 각 `code_versions.json`, inference library version은 `frozen_model_manifest.json`에 있다.

원래 1m/Z construction site의 `stage_metrics_1m_z.usda`, 원래 rover, supplier graph 원본 `construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`, v14b engineering startup overlay(초기 XY −25.88797768, 27.4m), HR cement nominal load를 유지했다. camera·render allowlist·ROS/GID guard·follower·full-rover collision/support 기준을 변경하지 않았다. 목표는 perception에서 산출하고 USD GT를 commanded target으로 넣지 않았다. geometry는 기존 safety 역할로 구분된다.

PRE/FINAL 위치5mm·yaw2°·ZERO 뒤 quiet≥1초, quiet 속도/XY span 각2mm/s·2mm, TF wall≤0.5초/sim≤0.1초 및 GID gate를 유지했다. stop trigger3mm, 기존 제어 이득/후방 기준 offset0.338m, GC600초/RSS증가768MiB/절대8GiB 제한도 변경하지 않았다. B5 RANSAC seed261022 유지, 다른 명시적 seed 부재는 UNKNOWN으로 기록했다.

정적 `pxr.UsdUtils.ComputeAllDependencies` 검사에는 material resolver 없는 SDK MDL(`OmniPBR.mdl`, `OmniSurface.mdl`, `gltf/pbr.mdl`), remote Grid 경로와 로컬 `apriltag_100.png`, `mitex_box_u0_v0_diffuse.jpg` 등의 미해결 참조가 남는다. 정확한 경로는 [closure JSON](construction_site_usd_closure_20261101_v20.json), 경고는 동명 `.log`에 있다. 이 검사는 비활성/reference metadata까지 포함한다. 참조 파일을 새로 만들거나 stage를 바꾸지 않았으며 materialized 입력의 drift는 없었다. **전체 렌더 자산 closure 및 미기록 과거 환경의 완전 소급 인증은 UNKNOWN**이다. 실제 두 실행의 capture/calibration/graph 및 safety gate 결과와 구분한다. missing Python snapshot·모델·실행 필수 prepared input은 없었다.

[재현 명령 README](../construction_site_reproduction_20261101_v20.md)에 정확한 prepare/run 명령과 fresh ROI 절차를 저장했다. pose CSV·이전 목표 재생이 아니라 기존 capture/inference entry를 실행한다.

## B. 독립 실제 실행 두 번

두 root는 `/home/user/hh/isaac_cosmos/sdg_final/` 아래 각각 다음과 같다. root마다 새 runner/Kit/physics 초기화와 `attempt_0001` 한 번만 사용했다.

- `CONSTRUCTION_SITE_REPRODUCIBILITY_20261101_v20_01`
- `CONSTRUCTION_SITE_REPRODUCIBILITY_20261101_v20_02`

각 실행 직전 기존 인덱스724개 항목의 SHA256 및 새 prepare와 역사적 prepare의 파일 내용 hash가 일치했다. output 경로만 달랐다. GUI/Kit/training 없음, GPU rustdesk만 존재, ROS domain probe PASS 후 launch했다. 첫 실패 뒤 새 ZERO-ONLY 정지·접촉0·소유 PID 소멸을 확인해 두 번째를 허용했다. unrelated process 중지·GPU reset·강제 종료0. 두 실행 사이 runtime code/GC/ROI 정책/모델/초기 배치/기준 변경0.

| 항목 | v20_01 | v20_02 |
|---|---:|---:|
| fresh capture / real YOLO / B4 | PASS / PASS / 계산 완료 | PASS / PASS / 계산 완료 |
| YOLO confidence | 0.693538 | 0.718262 |
| B5 / fresh RGB+ROI overlay 직접 시각 검토 | COMPUTED / 승인 | COMPUTED / 승인 |
| PRE 추정 XY(m) | −25.934824241, 28.278040457 | −25.934825707, 28.278040474 |
| FINAL 추정 XY(m) | −25.934824241, 29.078040457 | −25.934825707, 29.078040474 |
| PRE_REACHED / FINAL_REACHED(인증 기준) | true / **false** | true / **false** |
| PRE 위치오차 / yaw오차 | 2.682323mm / −0.037579° | 2.772089mm / −0.013001° |
| PRE post-zero quiet | 1.000000052초 PASS | 1.000000052초 PASS |
| FINAL 독립 stop certificate | **누락 / FAIL** | **누락 / FAIL** |
| PRE / FINAL live support | 48060 / 43740 PASS | 48060 / 43740 PASS |
| 실제 pulse 누적 경로 | 1.682034207m | 1.682042363m |
| pulse 기록 sim / wall 기간* | 126.833340 / 314.493228초 | 126.400007 / 306.942939초 |
| nonzero command 기록 | 2363 | 2353 |
| 실제 wheel peak | 1.572852rad/s | 1.450511rad/s |
| driver TF wall 최대 | 60.709ms | 49.504ms |
| session TF wall 최대 | 121.238ms | 116.312ms |
| driver TF sim 최대 | 16.667ms | 16.667ms |
| 예상 밖 contact / shell 침투·하중 | 0 / 0 | 0 / 0 |
| 별도 fault ZERO-ONLY quiet | 새61샘플 / PASS | 새61샘플 / PASS |
| cleanup 요청 결합 zero10 | PASS | PASS |
| driver / observer / Kit exit | 0 / 0 / 0 | 0 / 0 / 0 |
| outer / runner exit | NOT_READY / **1** | NOT_READY / **1** |

\* `pulse_start`부터 마지막 `phase=pulse` 샘플까지이며 중간 PRE 정지/FINAL 검사와 실패 대기 구간을 포함한다. 순수 이동시간이나 성공 소요시간이 아니다. 정확한 sim/wall timestamps는 원자료와 summary에 있다.

두 번 모두 새 `front_rgb.png`와 새 `roi_overlay.png`를 도구로 직접 열어 확인한 뒤, 현재 RGB/overlay SHA에 `manual_roi.json`/`roi_review.json` 승인을 결합했다. 현재 영상에서 노출된 pallet top이 같은 위치임을 확인해 polygon `[(236,197),(251,181),(383,181),(403,197)]`을 각각 사용했다. 기존 2px erosion·brick exclusion3px 유지. 승인자는 이번 작업의 Codex 시각 검토이며 연구자의 추가 현장 annotation 검증을 대체한다고 주장하지 않는다. **assisted B5이며 완전 자율 pallet 인식이 아니다.**

새 RGB SHA256는 순서대로 `6f77b4245686231a5c289c8d6aa41ed3018e2746c3363b92775a72620a06155d`, `7b4333d784758489e966fd1378ac948732bf90fee844f87bb9548723fdec27f9`다. depth는 둘 다 `d17d0fe06e507a7718ba90723be945a07151b2a627f278d7a0bc918548be3e3d`로 일치한다. 고정 장면/초기 관측의 동일 depth 내용 자체를 stale 또는 독립성 증명으로 해석하지 않는다. 각 새 Kit PID(1548314/1559236), 새 output, capture에서 render product 생성·orchestrator step·annotator 새 buffer 저장, capture PASS 및 별도 시각 검토·실제 inference 기록을 함께 근거로 사용했다. 이전 pose/targets/depth 파일을 copy하는 경로는 실행하지 않았다.

`predicted_pose_targets.json`은 B4 직후의 중간 결과라 B5_NOT_EVALUATED를 기록한다. 이후 수동 ROI datum으로 계산된 최종 B5는 별도 `b5_prediction.json`에서 COMPUTED다. B4 heading은 둘 다90.011093°, B5 center는 각각 (−25.934824241,30.481785488), (−25.934825707,30.481785505)m다. `predicted_pre_final.json`과 B5 최종 기록을 사용했으며 중간 파일을 성공처럼 수정하지 않았다.

## 실패의 직접 근거와 안전 정지 구분

v20_01 FINAL 첫 ZERO는 sim123.983339800초/source step7436, v20_02는 sim123.483339773초/step7406이다. 두 leg1 command 배열에 `BRAKING`은 **0개**, `ZERO_SETTLING`은 각각141개다. 정상 stop 요청 update에서 governor의 출력이 바로0이 됐고 `NORMAL_DECELERATION`으로 ZERO가 기록됐다. 반면 역사적 v19b FINAL에는 sim123.066673085초 BRAKING(출력0.000073693m/s) 다음 sim123.116673088초 ZERO라는 두 기록이 존재한다.

고정 `StoppingAdapter.update`는 normal stop 때 내부 상태를 BRAKING으로 바꾼 뒤 같은 호출에서 출력이0이면 ZERO_SETTLING으로 다시 바꾸고 최종 상태만 반환한다. `confirmed_stop`은 command 배열의 별도 BRAKING 존재 및 BRAKING→ZERO 순서를 요구한다. 따라서 이번 두 배열은 quiet 여부와 관계없이 인증에서 거절된다. driver는 ZERO 뒤7sim초에서 certificate 미수신 상태로 exit0/`completion_accepted=false`; session은 `TWO_LEGS_INCOMPLETE`, outer는 `MISSING_WITNESS`로 실패했다. 이는 **저장 증거와 정적 코드로 특정한 상태 전이/인증 불일치**이며 제어를 변경해 검증한 해결책은 아니다.

최종 측정은 각각 FINAL 잔여2.978442mm/yaw−0.032799°, 2.851582mm/−0.018149°였다. 그러나 이 측정 phase는 `fault_zero_only`이고 FINAL 독립 인증이 없다. **FINAL 정상 도착 PASS로 재분류하지 않는다.** fault 뒤 새61물리샘플의 quiet1.000000052초는 안전 정지 증거만이다. quiet root 최대속도1.011301/0.548719mm/s, span0.013351/0.007629mm였다. 기존 aggregate `outcomes.zero`는 PRE 첫 ZERO를 가리키므로 FINAL 근거로 쓰지 않는다.

GC 제한 구간은317.790467/310.173294wall초, peak RSS7,248,240,640/7,221,178,368bytes, 증가584,306,688/577,949,696bytes로 기존 제한 이내다. finally의 paused 복원에서 automatic GC=true, active=false, freeze count0이다. TF/GID fault 기록은 양쪽0이며 graph 변경/접촉 fault도 없었다. 전체 session startup/정지 GC 시간은 각 `actual_summary_v19.json`의 timing에 보존돼 있고, 이번 실패를 GC로 돌리지 않았다.

기존 capture는 정지 RGB-D만 보존한다. 실제 주행 영상 capture가 없어 optional 동영상은 생성하지 않았다. 새로운 frame capture를 제어 loop에 넣거나 pose 기반 가짜 애니메이션을 만들지 않았다.

## 검사·보존 및 다음 gate

[통합 원자료 인덱스/요약](construction_site_reproducibility_summary_20261101_v20.json)은 각 root174개 파일(총348개)의 SHA, 두 실행별 fresh vision/B4/B5/ROI·목표·stop·Twist/base/wheel·시간·TF·GC·contact·exit를 기록한다. 각 root의 `actual_summary_v19.json`, `evidence_check_v19.json`, `leg_0_stop.json`, raw steps/commands/contacts, provisional/final 및 runtime log도 보존했다. `leg_1_stop.json`과 FINAL `stop_confirmed.json`은 양쪽 누락이며 이를 새로 조작해 만들지 않았다.

최종 [보존 검사](construction_site_final_preservation_20261101_v20.json): 기준선+신규 raw **1072개 hash 항목 불일치0**, 역사적/신규 snapshot 각각69개 일치, prepared73개씩 일치, provisional digest·기록된 evidence hash PASS. known-lock9 hash/count subset PASS([검사](construction_site_known_locks_20261101_v20.json)); 과학 전체 readiness 인증은 아니다. source compile PASS, ROI/hash binding PASS. Kit/training0, 소유 driver/observer/Kit PID 모두 소멸, rustdesk 보존. 누락된 FINAL 인증과 전체 렌더 의존성 closure는 각각 FAIL/UNKNOWN으로 남겼다. 초반 capture 파일 생성 전 확인의 `ls`/`tail` 비존재와 읽기 검색 무일치는 점검 과정의 비정상 exit로 남아 있으며 Kit 반복을 추가/삭제하는 근거로 쓰지 않았다.

변경·추가 파일은 root baseline JSON2개와 SHA sidecar2개, reproduction README, 신규 offline analysis helper3개(`freeze`, `baseline_complete`, `reproducibility_summary`), 본 보고서와 보조 JSON/log, `reports/latest_report.md`, `docs/PROJECT_STATE.md`다. v01–v19 소스·output·과거 보고서·원본 USD·weights·locks는 보존했다. 두 runner exit1도 그대로 남겼다. Git stage/push·외부 publish는 하지 않았다.

**다음 권고는 별도 좁은 offline lifecycle 작업이다.** 기존 v19b 성공과 v20 실패의 정상 stop update를 재생하여 같은 호출 내 MOVING→BRAKING→ZERO 전이를 명시적으로 관측·검증할 방법을 검토한다. 정지 속도·위치·yaw·quiet·GID/TF/접촉 기준을 낮추거나 BRAKING 검사를 무조건 삭제하지 않는다. 새 버전 후보의 전이 기록/인증 일관성과 fault 거절을 CPU에서 먼저 확인하고, 그 뒤 별도 허가된 bounded engineering 확인을 제안한다. 이번 작업에서는 수정·세 번째 Kit·v21 sweep을 시작하지 않았다.

그 gate를 통과하기 전에는 fixed-condition 과학 pilot을 보류한다. 이후 별도 **작은 cross-representation pilot/admission**에서 독립 HR/LR/CAD inference checkpoint 및 자산 경로를 명시하고 비교할 수 있다. LR은 reduced acquisition 조건에서 **독립 재구성**한 scan이며 HR mesh decimation이 아니다. CAD는 GeoCAD 자산/모델과 명시적으로 연결해야 하며 Proxy와 혼동하지 않는다. 현재 protocol의 HR_Scan/LR_Scan/Proxy/GeoCAD membership을 임의로 축소하거나 다시 설계하지 않는다.

향후 축은 **representation × load completeness × occlusion**으로 검토하되 수치 수준·표본 수·합의를 새로 만들지 않는다. paired base scenario/seed·장면/start pose·camera/calibration·RGB-D 획득·관측 정책·frozen recipe/checkpoint 선택 규칙·ROI 도움 수준/검토 기준·B4/B5·controller·collision·TF/GID·stop/quiet·timeout·metric/실패 denominator를 표현 간 동등하게 고정해야 한다. 수동 ROI 보조를 사용할 경우 이를 공통 protocol로 사전 명시하고 fully autonomous 결과와 구분한다. Real Test189는 recipe locking 후 이미 평가됐으므로 tuning에 재사용하지 않는다. real external validation은 red-only이며 cement·실로봇 deployment로 일반화하지 않는다. 이번 0/2는 engineering 원시 빈도이며 정식 성능·동등성·비열등성 주장으로 확장하지 않는다.
