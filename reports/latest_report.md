# v30 — 공유 HR visual 복원, 원래 메모리 한도 안에서 실제 PRE·FINAL 성공

2026-11-02 KST. **새 HR engineering 1/1 PASS, Kit 1회 / retry0.** fresh RGB-D → frozen HR YOLO/B4 → 검토 ROI114점/B5 → 실제 PRE → 독립 zero/quiet → 독립 FINAL 경로 검증 → 실제 FINAL → 독립 zero/quiet를 완료했다. Kit/driver/observer exit0, watchdog/강제종료0. [독립 witness](construction_site_pilot_witness_20261102_v30.json)의 engineering success=true다. **과학 분모0, HR/LR/GeoCAD 비교 pilot은 아직 미완료**, LR/CAD 실행0, HPO/training PAUSED.

## 구체적인 수정과 정적 증거

v23은 각 AssetRef를 uninstance하고 inherited HR 가지를 active=false로 격리한 뒤 선택 asset을 PilotVisual에 참조했다. v24 union28·공통 material fallback과 v26 mount correction은 유지했다. 새 v30은 **AssetRef의 instanceable=false 및 기존 비활성 HR 가지를 유지**하고, 선택 HR asset reference와 native physics=false를 `/PilotHRClass_v30` 공통 class에 작성했다. 각 기존 `PilotVisual_v23` root는 이 class를 내부 참조하는 instance다. class는 abstract라 추가 렌더 배치가 아니다. 새 per-instance descendant override는 작성하지 않았다. 기존 약한 하위 override가 무시되어도 공통 class에서 physics=false가 적용된다.

[instance 검증·변조거절](construction_site_instancing_checks_20261102_v30.json): 기존 pilot instance22 → **322**, 총 prototype23, **선택 HR placement300 / 실제 공유 prototype1 / 각 Mesh1**. instance-proxy-aware mesh321 유지. 동일300slot/월드변환, material binding, geometry value source layer/속성 stack과 선택 source SHA를 검사했다. 전체 visual 속성/mesh array/material network는 공유 소스당 한 번 비교해 SHA `85fed37557b4cdfeeadc9d284a604eb18de146120c18cb1a831f93ab772718b3` 전후 동일; 300배 대형 문자열 dump 없음. 최대 world-bound 수치차1.0658e−14m(명시적1nm 산술허용), 원래1µm envelope 정책보다 작다. 기존 HR 가지 혼합0/native enabled0, 공통 static union28/변환·graph·외부physics·units/Z-up 유지. instance toggle/원래 AssetRef 재instance/다른 asset reference/union collider 비활성/prototype native 활성 **5/5 거절**. 원래 branch 재instance 변조는 null-prim 예외로 fail-closed 거절한다. capture는 계측을 제거한 AST가 v28과 동일하다.

선택 asset `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_HR_Scan.usd`, SHA `a3fbf6bd87d71007ae756a3288140d842d6e91135ee10d230a4ce52780d8f87c`. 새 채택 scene은 외부 `PILOT_SITE_HR_ADMISSION_20261102_v30_03/prepared_site_drive.usda`, SHA `72fda3227219a7f39fea4a3393d3adb036bf6e8eb029adaa4292a62f50bd396f`다. 원래 v24/v26/v28 USD는 수정하지 않았다. runtime overlay는 같은 root의 `attempt_0001/site_drive.usda`; 정확한 두 경로·실행 scene SHA는 [runtime 요약](construction_site_runtime_summary_20261102_v30.json)에 있다.

## 실제 한 번의 측정

Kit output root: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03`. 실제 명령:

```text
python3 scripts/construction_site_perception_runner_20261102_v30.py --run --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03
```

발견된 `hh_isaac51/bin/python`의 SimulationApp/Kit를 사용했다. owner **PID1995923**의 `/proc/self/statm` RSS, `smaps_rollup` PSS/private와 별도 `nvidia-smi` owner 행을 기록했다. YOLO/B4/B5는 원래 별도 worker이고 RAM 합산/메모리 이전0. 각 checkpoint에 wall time·PID·실행 session/diagnostic SHA·GC 및 작은 stage inventory를 기록했으며 source 전체는 prepared108개 hash와 snapshot으로 고정했다. motion tick 내부 추가 계측0. 아래는 **동일 PID의 실제 phase 측정**이다.

| 동일 owner 단계 | 경과 s | RAM RSS GiB | PSS GiB | private RAM GiB | owner GPU MiB |
|---|---:|---:|---:|---:|---:|
| python_start | 0.000 | 0.0228 | 0.0203 | 0.0202 | N/A |
| kit_startup | 7.206 | 4.3002 | 4.2249 | 4.2043 | 3271 |
| before_derive | 7.608 | 4.3400 | 4.2647 | 4.2441 | 3313 |
| scene_derived | 16.979 | 4.5870 | 4.5117 | 4.4911 | 3313 |
| scene_attached | 27.161 | 5.7962 | 5.7209 | 5.7003 | 3602 |
| after_physx_settling | 31.271 | 6.1118 | 6.0360 | 6.0150 | 8796 |
| before_capture | 39.939 | 6.1124 | 6.0366 | 6.0156 | 8739 |
| capture_warmup_complete | 40.488 | 6.1122 | 6.0364 | 6.0155 | 8739 |
| capture_annotators_attached | 40.643 | 6.1124 | 6.0366 | 6.0156 | 8739 |
| capture_render_complete | 41.078 | 6.1406 | 6.0648 | 6.0439 | 8797 |
| after_capture | 41.301 | 6.1474 | 6.0716 | 6.0506 | 8797 |
| pre_perception_memory_admission | 71.221 | 6.1503 | 6.0744 | 6.0534 | 8787 |
| after_B4_ROI_B5 | 97.941 | 6.1503 | 6.0744 | 6.0534 | 8787 |
| pre_drive | 111.577 | 6.1936 | 6.1178 | 6.0968 | 8787 |
| finally_paused | 452.120 | 6.7270 | 6.6511 | 6.6301 | 8786 |
| kit_close_enter | 462.714 | 6.7516 | 6.6763 | 6.6556 | 8786 |

원시 `phase_memory_v30.jsonl`은 run root에 있으며 witness에도 수록했다. GPU 값은 **VRAM MiB이며 RAM RSS가 아니다**. RustDesk PID953930의535MiB는 owner 수치에서 제외하고 원시 행은 보존했다. GPU 초기값과 PhysX settling 사이 증가는 실제 scene/render 초기화와 겹치므로 PhysX 단독 소비로 단정하지 않는다. RAM은 scene-derived→attached +1.2092GiB, attached→settled +0.3156GiB, capture 전→후 +0.0351GiB, worker 전→후0이다. annotator3개 attach/product와 render 완료를 따로 기록했으며 명시적 detach/destroy는 기존대로 없음이다.

| 별도 run의 비교 기준 | v28 기존 deinstance pilot | v30 공유 visual 후보 |
|---|---:|---:|
| motion-GC 진입 owner RSS | 20.7964GiB | 6.1936GiB |
| 같은 scope peak RSS | 20.7964GiB / 즉시 거절 | 6.7268GiB |
| scope 증가 | 0 / 주행 전 실패 | 572481536bytes (약546MiB) |
| 절대8GiB / 증가768MiB / 600초 | absolute FAIL | 모두 PASS / 340.191초 |
| 실제 PRE·FINAL | NOT_RUN | 각각 PASS |

위 두 run 차이는 같은 run의 phase growth가 아니다. **동일 geometry/material·physics를 보존한 공유 복원 뒤 약14.60GiB 낮은 admission RSS와 실제 주행 성공이 관측됐다.** de-instancing이 주요 메모리 증가와 연관됐다는 강한 실측 근거이며 renderer 내부 allocation별 인과 분해/반복성 증명은 아니다. 이번 동일 run에서는 scene/render 초기화가 capture보다 큰 RAM 증가 구간이다. 20GiB가 HR의 불가피한 물리적 필요라는 증거는 없고, 8GiB 정책 상향 제안도 필요하지 않다. 원래8GiB/+768MiB/600초 guard, warning·contact·TF/GID guard 변경0. worker 전에도8GiB admission을 추가 확인했다.

## 실제 관측·물리·정지와 종료

| 항목 | 판정과 수치 |
|---|---|
| fresh 관측 | 새640×480 RGB/axial depth, calibration8/8, 유효depth290691, capture 중 정지·graph 보존 PASS. RGB SHA `f3da809a00fb9fb104a06137d9039771007e9131ea03e29f95ac42dd9671f9a8` |
| frozen HR 인식 | matched HR M50 SHA `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`, YOLO1회 conf .7917593/mask7710, B4/B5 PASS. 학습/GT input0 |
| ROI/B5 | 새 RGB와 preview overlay 직접 검토, v28 공통180초 규칙·preview1/final1·polygon [(236,197),(250,183),(384,183),(403,197)]. 유효114/114, brick exclusion 잔존0, tilt .079800°, residual p95 1.04394e−7m. 좌표는 이전과 같지만 새 영상/마스크/검토/hash에 결합, 자동 재사용·B5 후 재제출0 |
| 실제 물리 | parser Error0, PhysX interior28/28·region native0·safety consumer28, wheel support2214/2214·6wheel contact, body/DOF·camera/graph PASS. contact50708·예상외/shell 하중0 |
| 새 목표/경로 | PRE=(−25.9348213,28.2780404), FINAL=(−25.9348213,29.0780404). PRE swept/live support48060/48060. 측정 PRE 정지 뒤 독립 FINAL swept/live support43740/43740 PASS |
| PRE 실제 도달 | 오차2.883526mm / yaw−.0378203°, normal zero 뒤 quiet1.000000052초; 독립 raw replay 및 저장 certificate 일치 PASS |
| FINAL 실제 도달 | 오차2.794514mm / yaw−.0397224°, normal zero 뒤 새 quiet1.000000052초; 독립 raw replay/certificate 일치 PASS. 같은 호출의 BRAKING→ZERO 실제 event를 기존v21 방식으로 인증 |
| ROS/cleanup | 비영 publish2350, driver/session endpoint92090/7341행 독립 replay 실패0. driver completion_accepted=true, 요청에 결합된 cleanup ROSzero10·receipt valid=true. 이번에는 실제 driver가 존재함 |
| 종료 | observer0/driver0/Kit0/runner0, owned PID잔존0, timeout/watchdog/terminate/kill0. GC paused restore PASS |

**close 진입은 기록됐지만 Python `kit_close_return` checkpoint는 없다.** `Simulation App Shutting Down` 뒤 실제 owner exit0와 outer finalizer의 증거 검증이 있다. 따라서 프로세스 정상 종료 PASS와 Python 함수 반환 미관측을 구분한다. 10초 간격 traceback 예약 파일은0bytes이며 dump가 발동한 증거가 없다. close_enter에 Python thread/GC callback 목록을 기록했지만 native callback 호출·C++ blocking stack은 UNKNOWN이다. 로컬 SimulationApp.close는 Replicator stop/wait → stage close → framework shutdown 순서이며 파일 SHA를 runtime 요약에 기록했다. 이번 run에서는 annotator explicit detach가 없어도 종료됐으므로 이를 v28 hang의 특정 원인으로 확정하지 않는다. v28의 −9/watchdog 실패는 그대로이며, 종료 원인 규명/일반 재현성은 미해결이다. 임의 cleanup 변경·timeout 확대0.

## 검증·보존·다음 작업

known9 SHA/108·432 count PASS, inherited v24 dependency/paired manifest checker PASS, 정적 composition/변조5/5·capture AST·compile PASS, 원래v21 stop20/20 PASS. [독립 witness](construction_site_pilot_witness_20261102_v30.json)는 prepared108개·executed snapshot·provisional digest·증거 hash 모두 PASS, 실제 두 정지/ROS receipt/GC 한도/owned 종료를 재검증했다. [v28 원시185파일 보존](construction_site_preservation_20261102_v30.json) mismatch0. [fixed-world 보강 검사](construction_site_fixed_scene_checks_20261102_v30.json)도 PASS: load 밖2065 active prim의 월드변환·schema·속성 source stack·연결/관계 signature가 기존 v28과 동일하다.

개발 실패도 보존했다. offline `_v30_01`은 anonymous layer 확장자/API 오류, `_02`는 exact BBox 비교 거절이었다. 실제 수치차를 기록하고1nm 산술 허용으로 해결했다. `_03`은 scene 검증/저장·corridor 완료 후 MANIFEST re-export 누락으로 plan 작성만 실패했고, 소스를 고친 뒤 기존 scene을 재작성하지 않고 `construction_site_prepare_finish_20261102_v30.py`로 prepared plan을 완료했다. **채택 instanced 후보1개·Kit root1개**이나, 요청의 scene 수 제한과 별개로 실패 offline scratch root2개에 기존형 파생 USD가 생성된 점은 범위 초과로 기록한다. 삭제/은폐하지 않았다. 추가 Kit/구제/재시도0.

변경: 새 v30 link·runner·session·capture·diagnostic, 제한된 offline probe/check/prepare-finish·witness 분석과 v30 reports, latest/PROJECT_STATE. bulk USD/RGB/depth는 외부 root에만 있다. 기존v19–v29 source/results·weights·locks·원본stage 변경0. v20 0/2 FAIL, v21 old-site1/1, v25–v28 FAIL, v29 Kit0 이력 불변. 이번은 HR engineering1/1일 뿐 표현 간 성능·동등성·실로봇 타당성 주장이 아니다.

**다음 구체 작업은 새 pilot-only DRAFT의 동일 공통조건·공유 visual 방식·matched frozen 모델을 적용한 LR 한 행의 별도 bounded admission이다.** 이번 작업에서는 LR/GeoCAD Kit·training·324/432를 실행하지 않았다. HR/LR/GeoCAD 실제 비교 완료로 부르지 않는다.
