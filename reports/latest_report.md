# v27 HR admission: 새 live perception 시도, ROI 점 수 부족으로 실패

2026-11-02 (Asia/Seoul). **Kit 1회 / RETRY0. HR의 새 YOLO/B4 관측은 얻었지만, 유효한 전체 HR pilot 관측은 아니다.** 새 수동 ROI의 팔레트 점 87개가 기존 최소100개에 미달하여 `PERCEPTION_FAIL`로 종료했다. PRE/FINAL 모두 NOT_RUN, 비영 주행0. 어두운 외관이나 offscreen Plane을 실패 원인으로 삼지 않았다. LR/CAD 미실행, pilot-only amendment DRAFT, formal science denominator0, HPO/training PAUSED.

| 판정 | 결과와 범위 |
|---|---|
| CAMERA_CAPTURE_PASS | PASS: 새640×480 RGB/axial depth, 유효290,691픽셀, calibration8/8, optical transform·정지 capture·원래 graph PASS |
| Render/material admission | 한 reviewer가 새 RGB를 직접 확인, 적재물과 팔레트 상면 구분 가능. 활성 asset/MDL/texture dependency 확인. 전체 renderer closure UNKNOWN은 유지하며 photometric fidelity나 원본 동등성을 인증하지 않음 |
| 공통 Plane | NOT_VISIBLE/OUT_OF_SCOPE: composed bounds 전체가 optical 오른쪽 frustum 밖. near=.01m/far=10,000,000m도 검사. frontal pallet ROI 가림 불가. 공통 gray binding 검증 유지, in-frame material PASS 주장 없음. authentic AprilTag MISSING |
| 실제 physics | parser error0, PhysX interior28/28·region28 unique union28/native0·consumer28 PASS, stationary support2214/2214·6wheel contact, contacts168/예상외0 |
| 새 frozen HR YOLO/B4 | brick_load 1개/conf .7122505903, mask/depth7717/7717, B4 heading90.011093°·margin .0664386562. 실제 새 센서 관측이며 GT·이전 pose 입력0 |
| 수동 ROI-assisted B5 | **FAIL 입력 gate.** 새 polygon [[237,196],[250,183],[384,183],[401,196]], 2px erosion/3px brick exclusion 후87점. inlier87/87, tilt .079804°, p95 residual1.147e−7m, 작은 XY covariance eigenvalue .00504m²는 통과하나 **87<100**. B5 pose/targets 생성 전 중단 |
| PRE / FINAL | 둘 다 NOT_RUN. driver 미시작, actual curved sweep/normal leg stop/독립 FINAL proof NOT_RUN. 유효 pilot 성공0/1 시도, formal science 표본으로 미등록 |
| zero / exit | zero request 및 직접 graph zero 수행, 실제 ROS receipt MISSING/valid=false·NOT_APPLICABLE_PRE_DRIVER. Kit0/observer0/runner1, NOT_READY/MISSING_WITNESS. 강제종료·timeout0, 소유 PID 잔존0. baseline quiet1초·aggregate STOPPED=PASS는 접근 정지 성공이 아님 |

저장 v26의 객관 진단은 [offline evidence](construction_site_hr_offline_evidence_20261102_v27.json)에 있다. 성공한 v21과 width/height/fx/fy/cx/cy/optical transform이 정확히 같다. 두 RGB 전체 평균 휘도는118.6656/118.7224, 직접 검토한 load 사각형(x247:383,y135:195)의 평균10.5258/10.5128·중앙값4.353/4.353, 팔레트 사각형 평균33.0961/33.1050이다. RGB 평균 채널 절대차 .37372/255, 최대33으로 bitwise 동일하지 않다. 두 depth 모두290,691픽셀 유효하며 공통 유효영역 abs차 중앙값·95백분위0, 최대 .429513m. 국소 geometry 차이를 전체 렌더 고장으로 해석하지 않았다. v24는 visual reference replacement와 공통 union/fallback의 파생 pilot scene, v26은 disabled mount API만 추가 제거한 scene이다. v21 원본 scene과 완전히 같은 실험이 아니며 start/camera geometry는 일치하고 새 light/brightness 수정은 없다.

별도 외부 `PILOT_HR_OFFLINE_DIAGNOSTIC_20261102_v27_01`에서 v26 저장 RGB에 동일 M50 recipe(imgsz1280/conf.25/IoU.70/mask.5)를 정확히1회 적용했다. brick_load conf.6880520582, 마스크7714픽셀·valid depth7714, B4 계산 PASS. detector mask 내 luma 중앙4.1404/95백분위24.9399, 최소0/최대126.7892다. 이는 실제 RGB의 검출된 노출영역 수이며 semantic GT의 brick pixel census가 아니다. semantic annotator는 추가하지 않았다. 수동 ROI는 시각적으로 가능했지만 offline B5는 실행하지 않았다. 이 diagnostic은 fresh 과학 관측이나 v27 capture로 대체되지 않는다.

HR 활성 material은 `PilotVisual_v23/Normalize/SourceAsset/Looks/material0`의 `gltf/pbr.mdl::gltf_material`, texture lookup은 같은 MDL의 `gltf_texture_lookup`이다. SDK MDL SHA `2c7c14d7bbf7cacea990f90e8ecc92700d8a7fe9805e44970096796e2be88b78`과 v24 active dependency를 재검사했다. 실제 USDZ member `SubUSDs/textures/brick_gray_mid_texture0.png`를 읽고 hash를 남겼다([texture evidence](construction_site_hr_texture_20261102_v27.json)). 활성 재질은 unlit shader가 아니며 emissive_strength10000만 authored되어도 MDL default emissive_factor0이면 자체 발광하지 않는다. 텍스처 미해결이나 fatal shader failure의 구체 증거는 없고 임의 밝기·조명 보정0이다. resolved asset과 외관 관측이 renderer 전체 정합성 증명을 뜻하지는 않는다.

[좁은 결정 규칙](../docs/construction_site_hr_admission_rule_20261102_v27.md)은 camera capture, perception validity, material unknown을 구분한다. v26 당시 NO-GO/미주행 결과는 소급 수정하지 않았다. 새 v27 runner/session/adapter/link는 v26 derived-only mount fix·v25b capture를 유지하고 offscreen frustum 분류, fatal shader/RGB-D rejection, task PERCEPTION_FAIL 명시만 추가했다. v21 driver/event-aware stop/verifier·model·ROS·graph/TF/GID·PhysX·contact·sweep·GC·5mm/2도·quiet≥1초 기준은 그대로다. 실행된 source는 이후 수정하지 않았다.

실제 명령은 아래 두 단계이며 첫 prepare는 offline, 두 번째가 유일한 Kit다. 이미 사용한 root에 재실행하면 거절된다.

```text
python3 scripts/construction_site_perception_runner_20261102_v27.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v27_01
python3 scripts/construction_site_perception_runner_20261102_v27.py --run --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v27_01
```

raw: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v27_01/attempt_0001`. 실제 derived scene SHA `0a4e245c065e492c510720fd91beb67bcc4e01680d08745701bdd2535b12c523`, fresh RGB SHA `cc1af4c6dfba0ca6fe1c4b9e4157f48ecbee9ef8727dc0808c4ce84502b0f45c`. ROI는 새 영상을 보고 새로 지정했고 old v21 ROI/pose를 복사하지 않았다. 시각 검토 뒤 선택한 더 좁은 다각형이 기존 pixel-exclusion 뒤 최소 점 수를 확보하지 못했다. 이번 실패는 HR 모델의 detection failure나 재질 고장을 증명하지 않으며, 수동 ROI protocol의 현재 한 사례 실패다. 실패 후 ROI 변경·추가 inference·재시도·GT 구제0이다.

검사: compile PASS, 실행 전 [집중 CPU28/28](construction_site_pilot_regression_20261102_v27.json), v21 stop20/20, known9 SHA 및108/432행 PASS. 새 valid/invalid RGB-D·depth0·fatal shader·in-frustum Plane 분기의 실제 함수 호출 회귀5/5는 **실행 종료 후** 추가 확인했다([결과](construction_site_hr_admission_test_20261102_v27.json)); fake app/read-only USD를 쓰며 추가 Kit는 없다. [독립 witness](construction_site_pilot_witness_20261102_v27.json)는 raw 전체 hash index·실제 physics/관측/cleanup·입력 SHA·executed snapshots·provisional digest·available evidence hash PASS를 확인한다. [보존 검사](construction_site_preservation_20261102_v27.json): v26 raw154개 hash 불일치0, v24 manifest/parents/세 scene/material dependency 재검사 PASS. 기존 v19–v26·v20 FAIL0/2·v21 성공1/1·frozen4rep·원본USD/weights는 그대로다.

변경 파일: 새 `scripts/construction_site_{perception_runner,perception_session,perception_adapter,pilot_link}_20261102_v27.py`, 새 offline/geometry/regression/admission_test/witness 분석 코드, v27 결정 규칙·reports, latest와 PROJECT_STATE. bulk 센서/scene은 외부 root에 남겼고 설치/학습/LR/CAD/432/Git push0이다. 이번 원시 실패·worker exit1·runner exit1은 삭제하거나 성공 분모에서 숨기지 않는다.

**남은 실제 blocker는 새 수동 pallet ROI의 유효 점 수87<100이다.** 다음 구체 작업은 이 실패 RGB/overlay/mask에서 기존 ROI 선택 절차의 점 확보 가능성과 경계 불확실성을 offline 검토하는 것이다. 이 실행을 구제하거나 재시도하지 않는다. 새 live 재시도는 별도 bounded 작업으로 결정해야 하며, 독립 clean HR PRE/FINAL 성공 전 LR/CAD는 권고하지 않는다.
