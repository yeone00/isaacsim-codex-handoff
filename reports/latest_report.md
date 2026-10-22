# B5 독립 datum 오프라인 평가 — 2026-10-22

**결론: INSUFFICIENT_DATUM — 관측 상판 후보는 확보했지만 현행 증거 계약에 부합하지 않아 B5 NOT_EVALUATED, pose/PRE/FINAL=null.** 물리 높이 부재만으로 끝낸 감사가 아니다. 저장된 RGB·metric depth·예측 mask·calibration으로 실제 평면을 계산했다. 센서 관측을 planned fixture design으로 위장하지 않았으며, 요청의 계약 변경 시 중단 조건을 적용했다.

산출물: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_B5_DATUM_OFFLINE_20261022_v01/`. 실행: `/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_b5_datum_offline_20261022_v01.py` (exit0). 동일 경로의 `roi_overlay.png`, `plane_diagnostic.png`, `candidate_floor_plane.json`, `candidate_pallet_plane.json`, `datum_diagnostics.json`, `b5_predicted_pose_targets.json`, `provenance.json` 및 정확한 ROI mask에 근거를 남겼다.

|관측 근거|바닥|노출 팔레트 상판|
|---|---:|---:|
|유효 ROI / inlier 수|62,384 / 62,384|1,810 / 1,810|
|world Z 대비 normal 기울기|0.370144°|0.079751°|
|직교 잔차 RMS / P95 (m)|5.76e−8 / 1.14e−7|4.50e−8 / 8.63e−8|
|ROI 중심 world Z (m)|−0.002026833|0.146866635|
|XY covariance 작은 고유값 (m²)|0.009899|0.003574|

RGB를 먼저 보고 GT 없이 바닥 polygon `(40,335),(600,335),(600,450),(40,450)` 및 상판 polygon `(158,269),(185,239),(444,239),(482,269)`을 기록했다. 경계 2px erosion, 예측 brick mask 3px dilation 제외 후 역투영했다. 바닥은 팔레트·brick 밖이다. 상판 ROI는 육안으로 보이는 목재 deck 양옆·앞쪽이며 overlay 재확인했다. Seed261022, RANSAC400회, normal 제한10°, inlier3mm 후 TLS 재피팅. 별도 진단 기준 ≥100점·inlier≥80%·기울기≤5°·XY 분산>1e−5m²를 두 후보 모두 통과했다. 이는 **새 연구 성공 기준이 아닌 진단 기준**이다. 추가 erosion1/2px에서도 상판 중심 높이 변화 <1e−8m였다. 외측 ROI 확장·반복 관측·depth/camera 보정의 체계 오차는 미검증이다.

바닥 평면 `n=(.002298154,−.006037599,.999979133), d=.240267997`; 상판 `n≈(0,−.001391911,.999999031), d=−.105066299` (`n·world+d=0`). 상판 ROI 중심 XY에서 바닥 외삽 Z=.000417517m, 상판−바닥=.146449118m로 명목 두께 .144m보다 2.449mm 크다. 바닥은 팔레트 아래를 직접 관측하지 않았고 두 평면도 평행하지 않으므로 floor+.144를 상판 datum으로 대입하지 않았다. 극소 잔차는 **시뮬레이터가 이미 렌더한 저장 RGB-D의 내부 평면성**이며 현실 센서의 수십 nm 정확도나 실물 팔레트 측정이 아니다.

**계약·출처:** 원본 pose SHA256 `cc95b96c3305dcbe257a40fcf16f0e68a9e58ae0d5ae43f9cbd31e80ffec0988`, production SHA256 `a3740cd82022a1686794f8da892fb376ad1a02f63c2fe8e842ac1cef864641ad` 일치 PASS. `.144m`는 두 원본 및 prior allowlist의 독립된 **설계 두께**다. 실물 metrology·이번 fixture world transform과 다르다. 원본 `mask_to_world`는 Z≥PALLET_H−.020, `side_points`는 PALLET_H+nominal4×.090−.030을 사용하며 독립 측정 방법·normal 허용오차 계약은 없다. 현재 `full_e2e_locked_pose_adapter_v01.py:6–24`는 hashed `engineering_fixture_design` / `planned_horizontal_fixture_top_world_m`만 허용한다. Sensor-observed plane은 이 형식에 해당하지 않는다. 직접 원본 호출은 legacy K/frame을 쓰며 새 datum/calibration 연결 없이는 정당하지 않다. 증거 계약 확장·원본 우회 호출·동결 함수 변경은 하지 않았다.

**검사/한계:** 입력14개 실행 전후 SHA 보존 PASS, mask29,876px PASS, 진단 계산·overlay PASS. ROI 밖 무효 depth의 matmul RuntimeWarning(exit0)은 diagnostics에 보존했으며 피팅에는 유한 양수 depth만 들어갔다. B5 계약 적합 FAIL, 체계적 datum 불확도 UNKNOWN. 기존 B4=90.157714844°/margin.001015는 그대로 보존했으며 heading gate를 전체 pose 성공으로 승격하지 않았다. B5 예측이 중단되어 GT 오차 audit도 NOT_EVALUATED; 원본 fixture/GT geometry를 로드하지 않았다. Kit·YOLO·ROS·motion·학습·432 실행0, 연구분모 변화0. 체크포인트는 재로드/재해시하지 않았고 기존 manifest hash만 참조했다. Stop regression/PUBLISHER_SET은 미해결이다.

**다음 단일 행동:** 현재 관측 상판 후보와 불확도를 증거로 받는 **새 버전 datum adapter 계약을 검토·승인**한다(동결 B4/B5 함수 유지). 추가 Kit 캡처는 필요 없다. 실물 독립 검증이 필요하다면 동일 world 기준에 연결한 팔레트 상판의 다점 높이 측량이 필요하지만, 측정값만 생겨도 현 adapter의 evidence-kind 제한은 별도 해결해야 한다. 지금 병목을 단순히 “팔레트 두께 하나 부족”으로 표현하지 않는다.
