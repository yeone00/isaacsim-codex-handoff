# 센서 관측 pallet datum adapter v02 — 2026-10-22

**실제 결과: B5 COMPUTED, 단일 offline engineering 호출1/재시도0/exit0.** 저장된 front RGB-D·검출 mask와 수동 ROI 상판 평면만 사용했다. 새 계약은 **PROPOSED engineering semimanual 전용**이며 frozen confirmatory 승인·자율 perception·연구 E2E 성공을 뜻하지 않는다.

산출물: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_B5_SENSOR_ADAPTER_20261022_v02/`. `adapter_evidence_v02.json`, `contract_validation.json`, `b5_prediction.json`, `predicted_pre_final.json`, `source_hash_manifest.json`, `completion.json`, `post_execution_verification.json` 존재·파일0444. 실행 명령: `/home/user/anaconda3/envs/sdg_tools/bin/python analysis/construction_site_b5_sensor_adapter_20261022_v02.py`.

|항목|실제 값|
|---|---:|
|관측 anchor world XY (m)|−25.8346946456, 30.0307131705|
|계산된 상판 world Z (m)|0.14686663495932334|
|B5 중심 world XY (m)|−25.8358191200, 30.4337574128|
|B4 heading (mod180)|90.15771484375°|
|B4 margin / flip|0.001015016867 / false (threshold .014116)|
|B5 score / inside rate|0.073290312617 / 0.985579663973|
|유효점 / top / side|29,819 / 4,470 / 24,504|
|B5 center 90° 후보 선택|true; heading은 원본대로 B4 값 유지|
|PRE world XY (m)|−25.8358191200, 28.2300123815|
|FINAL world XY (m)|−25.8358191200, 29.0300123815|

기존 YOLO confidence .8027858734는 검출 신뢰도다. Pose confidence는 정의되지 않았다. 원본 B5의 실패 gate는 3D/top/side 각각30점 미만이며 side 부족 시 q70 fallback이 있다. 이번에는 모두 통과했다. 원본에는 score/inside-rate 합격 threshold가 없으므로 새 threshold를 만들거나 pose 정확도 PASS로 해석하지 않았다. B4 margin은 flip 선택 규칙이며 전체 pose gate가 아니다.

**좌표·수식 근거:** frozen source `/home/user/eval_step25_pose_final_locked_v01.py`의 `PALLET_H=.144`(157행), `camera_basis`(398행)의 eye Z=.600 및 target Z=PALLET_H+layers×SIDE_H/2, `mask_to_world`(498행)의 `Z>=PALLET_H-.020`, `side_points`(918행)의 `Z<=PALLET_H+layers*.090-.030`를 확인했다. 즉 .144는 원래 floor Z=0 설정에서 설계 두께와 절대 상판 Z가 같았던 값이며 일반 world 높이가 아니다. 함수는 datum 인자를 노출하지 않는다. 새 v02는 기존 calibrated camera adapter의 **입력 좌표 평행이동** `z′=z_world−z_anchor+.144`를 재사용한다. 따라서 두 filter는 world에서 각각 `Z>=z_anchor−.020`, `Z<=z_anchor+.360−.030`과 동치다. XY·normal 회전·원본 전역 상수·B4/B5 식은 변경하지 않았다. Camera basis도 같은 Z 이동을 쓰며 B5는 그 forward XY를 사용한다.

`n·world+d=0`에서 JSON의 normal·d·관측 centroid XY를 읽어 `z_anchor=−(nx*xa+ny*ya+d)/nz`로 계산했다. .146866635를 상수로 넣지 않았다. 상판 normal≈(4.923e−9,−.001391911,.999999031), d=−.1050662992m, tilt=.079750625°. Inlier1810/1810, XY extent1.069291×.252661m, 관측 Z span .351871mm, 잔차 RMS4.50e−8m/P958.63e−8m다. 이는 anchor에서 수평 datum으로 근사한 것이며 전체 기울어진 평면을 flatten하지 않았다.

**계약·검사:** evidence kind=`sensor_observed_pallet_top_plane_world_v01`. RGB/depth/calibration·checkpoint·ROI mask·plane·run ID·이전 provenance와 파일 SHA를 연결하고 frame/Z-up/미터, 유한 값, +Z unit normal, slope≤5°, inlier≥100/ratio≥.8, P95≤3mm, XY covariance>1e−5m²를 검사했다. 이 수치는 이전 진단을 이은 **제안 engineering admission 기준**이며 연구 승인값이 아니다. 잘못된 kind/hash/수치·출처변경은 거부한다. 부정 사례7개 거부 PASS(평면변경4개는 먼저 provenance mismatch에서 차단; 각 geometry branch의 독립 coverage는 미확보). 원본9개 함수 및 모든 추출 상수 AST 일치 PASS, 평행이동 filter 동치·synthetic side/fallback spot 검사 PASS. 원본 pose SHA `cc95b96c3305dcbe257a40fcf16f0e68a9e58ae0d5ae43f9cbd31e80ffec0988`, production SHA `a3740cd82022a1686794f8da892fb376ad1a02f63c2fe8e842ac1cef864641ad`, HR checkpoint SHA `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca` 실제 일치. 전체 입력50파일 전후 보존 PASS, compile2 PASS, known-lock9 hash/count PASS(이번 pairing 재감사 아님). 기존 capture manifest의 자기 자신 항목은 작성 전 empty hash이므로 자기 인증에서 제외했으며 입력 데이터 항목은 기존 datum provenance와 교차 일치한다. expected hash를 수정하지 않았다.

예측 JSON을0444로 먼저 고정한 후 기존 target generator를 적용했다. PRE/FINAL은 prelock 거리2.2037450313/1.4037450313m 및 amendment chain through v03·geometry v02 workspace의 task yaw+90°/local_-X 정책이며 추정 heading을 task yaw로 대체하지 않았다. 관련 실제 lock 내용·hash를 사후 검증 JSON에 남겼다. GT 비교는 독립적으로 정당화된 현재 scene GT 없이 수행하지 않았다.

**한계:** ROI는 RGB 육안 polygon·erosion·검출 mask 제외를 사용한 수동 선택이다. Brick mask에도 배경 혼입 가능성이 있다. 상판은 한 anchor의 높이이며 floor와 비평행하다. floor 외삽 대비 .146449118m와 설계 .144m 차2.449mm는 절대 센서 오차가 아니다. 렌더 depth의 극소 잔차는 물리 센서 정확도가 아니며 scale/calibration 체계 불확도와 world 위치 정확도는 UNKNOWN이다. Clearance·로봇 성공 NOT_EVALUATED. Kit/새 capture/YOLO inference/ROS/physics/motion/432 모두0, 연구분모 기여0. 기존 stop regression/PUBLISHER_SET 미해결도 유지한다.

변경: 신규 `evaluation/full_e2e_sensor_datum_adapter_v02.py`, `analysis/construction_site_b5_sensor_adapter_20261022_v02.py`, 본 보고서, PROJECT_STATE append. Frozen 원본·v01 adapter·이전 출력은 보존했다. `.git` 부재로 Git status는 실패했으며 staging/push 없음; 존재하지 않는 task config 탐색도 실패했으나 실제 lock에서 정책을 확인했다.

**다음 단일 engineering 단계:** 저장 RGB-D에서 노출 목재 상판 ROI를 자동으로 분리하는 별도 후보를 구현하고, 이번 고정 수동 ROI와 비교하여 datum 자동 추출 가능성을 평가한다. 이 결과나 코딩만으로 protocol 승인을 대신하지 않는다.
