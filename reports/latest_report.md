# 건설현장 전방 RGB-D → 동결 YOLO → B4/B5 단일 스모크 — 2026-10-22

**FAIL: 실제 Kit 1회가 캡처 이전 단위 assertion에서 중단됐다. 재시도0.** host exit0와 내부 FAIL을 구분한다. 실제 센서 RGB/깊이 미생성, YOLO 현장 추론0, B4/B5·target 미계산이다. NO_DETECTION이나 OUT_OF_FOV 결과로 해석하면 안 된다. Preview 사진을 센서 증거로 대체하지 않았다.

## 실행과 입증된 blocker

실행 명령: `python3 scripts/run_construction_site_front_once_20261022_v01.py`.
실제 runtime: `/home/user/anaconda3/envs/hh_isaac51/bin/python`, Isaac5.1 base.python.kit, headless RayTracedLighting. PYTHONPATH 제거, EULA YES. process gate 기존 Isaac/GUI0; exclusive 새 output에서 Kit launch1. ROS extension0·active OmniGraph0 검사 통과, timeline play/physics.play/명령/이동0. 새 USD 생성·기존 USD 저장 없음. 기존 LIT USD를 열고 session edit target만 선택했다.

`construction_site_front_rgbd_capture_20261022_v01.py:27`의 `assert units == 1.`가 실패했다. 이전 캡처 코드의 단위 가정을 새 최상위 LIT stage에 적용하기 전에 오프라인으로 확인하지 않은 구현 실수다. stage open 이후 render product/annotator 생성 전에 중단됐으므로 캡처 완료 race나 YOLO 의존성 실패가 아니다.

실패 후 SimulationApp 없이 bundled pxr로 읽은 실제 결과:

|파일|metersPerUnit|upAxis|근거|
|---|---:|---|---|
|최상위 LIT USD|0.01|Y|두 metadata 미작성, 실제 API fallback|
|원래 preview attempt_0002 USD|1.0|Z|두 metadata authored|
|원본 recovery USD|1.0|Z|두 metadata authored|

LIT/runtime-fixed/visible 상위 layer에는 units가 없고 아래 preview에는 1.0이 있지만, 실제 최상위 stage API 결과는 0.01이다. 하위 layer에 값이 있다는 사실만으로 최상위 stage 단위를 인증할 수 없다. `offline_unit_evidence.json`, `source_coordinate_evidence.json`에 exact path와 layer 정보를 보존했다. 이 결과는 이전 visual PASS를 취소하지 않지만 metric RGB-D 인증을 대신할 수 없음을 보여준다. 카메라 prim은 실제 존재한다. mounted camera의 시선·stack 가시성은 **UNKNOWN**이다.

내부 `kit_internal_result.json`: FAIL/AssertionError. `runtime_host_result.json`: EXITED0/returncode0. wrapper도 exit0를 반환했으므로 **wrapper의 종료 코드 전달 결함**도 기록한다. 결과 판단은 내부 JSON이 우선이며 이 작업을 PASS로 해석하지 않는다. `kit_shutdown.json` 부재로 app.close Python return UNKNOWN; log는 shutdown을 기록하고 host는 종료했다. Native crash를 입증한 결과는 아니다. 재실행·자동 retry 없음.

## 실제 동결 모델과 수치 규약

- 체크포인트: `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_HR_Scan_M50_REALVAL_MASKBEST_v01.pt`.
- SHA256 expected=observed: `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`.
- representation: HR_Scan, 기존 M50 RealAdapted selection, epoch25. 현 fixture cement HR_Scan에 맞춰 선택했고 모델 비교/튜닝하지 않았다. selection summary는 Real Val48 Mask mAP50-95 기반이다. 그 historical summary의 Test sealed 문구는 당시 기록이며, 현재 Real Test189는 이미 평가 완료라는 연구 상태를 바꾸지 않는다.
- 실패 후 기존 sdg_tools 환경에서 체크포인트를 실제 로드해 `SegmentationModel`, task segment, **class0=brick_load** 확인. 학습·predict 호출 없음. torch2.7.1+cu128, ultralytics8.4.129. 상세 manifest 저장.
- 기존 실제 worker v02와 같은 예정 추론: sensor640×480, YOLO imgsz1280/conf.25/iou.70, RGB→BGR ndarray 변환, mask>.5 후 nearest640×480. 최고 confidence brick_load, tie detector index 선택, GT association/fallback 없음. detection.conf=null, mask area/valid depth=미측정(0으로 성능 평가하지 않음).
- 실제 카메라 prim: `/World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera`. exterior preview camera 사용 안 함. 동일 render product의 rgb/distance_to_image_plane/camera_params, stopped timeline의 delta_time0 step을 쓰도록 구현했지만 이번에는 해당 지점 미도달이다.
- 보정 규약: optical right/down/forward, column-vector T_world_optical, world metres. projection[0,0]×320, projection[1,1]×240, principal point320/240; renderer view와 USD scale 제거 transform 비교. 이번 intrinsic/extrinsic/depth 단위의 실제 sensor 검증은 NOT_RUN이다.
- 동결 pose 원본 `/home/user/eval_step25_pose_final_locked_v01.py` SHA `cc95b96c3305dcbe257a40fcf16f0e68a9e58ae0d5ae43f9cbd31e80ffec0988` 일치. 정적 추출 core와 기존 adapter를 읽었다. B4 top band20mm, quantile.01/.99, overshoot weight4, gate.014116, 최소점30; heading world XY degrees modulo180. B5 camera-facing side fit, nominal4층, side90mm/top exclusion30mm, face quantile.02/.98, load.950×.855m, pallet plane.144m. adapter는 별도 근거가 있는 world pallet-top datum을 요구한다. 현장 USD fixture 높이/pose를 대신 주입하지 않았다.
- 기존 target 생성은 B5 world XY에서 지정 local−X outward 방향으로 PRE2.203745031260775m/FINAL1.403745031260775m, task yaw는 동결 task 축이다. B4 heading으로 task 축을 돌리지 않는다. 이번에는 target 생성·controller 입력 없음.
- B5 datum의 현장용 독립 근거는 아직 확보되지 않았다. 이는 미실행 단계의 제한이며, 이번 실제 중단 원인은 좌표계 metadata assertion이다. 새 코드의 센서 기반 B4 단독 경로도 NOT_RUN이며 전체 동결 B4/B5 PASS가 아니다.

## 실제 산출물과 누락

외부 새 output: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v01/`.

|산출물|존재/의미|
|---|---|
|front_rgb.png / front_rgb.npy|없음 — 캡처 미도달|
|front_depth.npy|없음 — 캡처 미도달|
|camera_metadata.json|있음 — NOT_CAPTURED 및 실제 오프라인 stage 단위, sensor calibration null|
|detection_overlay.png|없음 — 추론 미실행|
|frozen_model_manifest.json|있음 — 실제 checkpoint hash/class 로드 확인, inference0|
|predicted_pose_targets.json|있음 — CAPTURE_FAILED, traceback, pose/targets null|
|runtime.log / runtime_host_result.json|있음 — 실제 Kit log와 host0|
|kit_internal_result.json|있음 — 내부 FAIL|
|launch_ledger.json / preservation_check.json|있음 — gate/명령 입력·code hash/보존|
|offline_unit_evidence.json / source_coordinate_evidence.json|있음 — 실패 후 read-only 좌표계 확인|
|final_evidence.json|있음 — exact filename 존재 여부와 SHA|

**실제 센서 thumbnail reference: 없음.** 존재하지 않는 thumbnail이나 이전 exterior PNG를 첨부하지 않는다. Pose/target/error/clearance는 전부 NOT_EVALUATED, stack line-of-sight UNKNOWN이다. 실패 evidence를 정상 검출0이나 invalid depth 측정으로 바꾸지 않는다.

## 보존·검사·다음 행동

known-lock 도구9개 hash/count PASS(108/432 포함, 이번 pairing 재감사 아님). LIT manifest가 고정한 source hash 및 LIT USD·checkpoint·pose 원본을 실행 전/후 재검증 PASS; exact 목록과 수는 launch ledger/preservation JSON에 있다. 원본·prior outputs·weights/protocol/threshold/조명/300 membership 수정 없음. 새 Python3개 compile PASS. 이번 환경에서 `git status`는 not a git repository로 실패했고 staging/push/remote 변경은 없다. 과학 패키지 설치/업데이트 없음.

변경: 신규 capture/infer/host 스크립트3개(`scripts/*construction_site_front*20261022_v01.py`), 이 보고서, PROJECT_STATE append. 외부에는 이번 실패 실행 evidence만 추가했다. 실행한 소스는 실패 당시 hash와 함께 보존하고 수정·재실행하지 않았다.

**다음 구체 행동 하나:** 별도 후속 단일 센싱 실행을 준비할 때, 기존 LIT를 열되 session layer에 원래 preview/recovery로 입증된 `metersPerUnit=1.0`, `upAxis=Z`를 명시하고 render 전 readback을 검사한다. 원본 파일·geometry·카메라 pose는 그대로 보존한다. 동시에 host가 internal FAIL이면 nonzero로 종료하도록 수정해야 한다. 이번에는 이를 실행하지 않았으며, 현재 v01 명령 재사용은 exclusive output에서 거부된다. sensing·pose가 성공하지 않았으므로 approach/motion 연결을 다음 단계로 주장하지 않는다.

전체 exercise는 engineering-only이며 preview Dome2500/Rect6000을 frozen research lighting으로 승인하지 않는다. Full E2E 성공·실제 robot 배포 검증 없음. 기존34.127mm stop regression/quiet FAIL, ROS PUBLISHER_SET blocker, ENG001/QUAL12/432 HOLD 유지. 연구 분모 기여0.
