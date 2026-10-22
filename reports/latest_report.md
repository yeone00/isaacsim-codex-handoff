# 전면 RGB-D·동결 YOLO 단일 스모크 수정 결과 — 2026-10-22

**실제 센서 캡처·YOLO 실행 PASS. Kit 정확히 1회, 재시도0. B4 heading 계산 완료, B5/전체 pose/target은 NOT_EVALUATED·null.** 기존 v01은 캡처 이전 assertion FAIL이며 그대로 보존했다.

## 실제 결과와 위치

새 실행 경로: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v02/` (이하 RUN). 실행 명령: `python3 scripts/run_construction_site_front_once_20261022_v02.py`.

|항목|실측 결과|
|---|---|
|front_rgb.png / front_rgb.npy|640×480 RGB, 저장·PNG 재개봉 검증 PASS|
|front_depth.npy|480×640 float32, distance_to_image_plane, 미터|
|전체 유효 깊이|288,630 pixels; 0.570293–4.205339m|
|YOLO11-seg|fresh RGB에 동결 모델 predict 정확히1회; class0 brick_load 1개|
|confidence / mask|0.8027858734 / 29,876 pixels, 모두 유효 깊이|
|B4 heading|90.15771484375° (world XY, modulo180)|
|B4 gate|margin .0010150169 < frozen .014116, 90° flip 미사용|
|B5 / pose / PRE·FINAL targets|독립 physical pallet datum 부재로 NOT_EVALUATED / null / null|
|Kit 내부 / child exit / wrapper exit|PASS / 0 / 0, inference exit0, 최종 host gate PASS|

RUN의 `front_rgb.png`, `front_depth.npy`, `camera_metadata.json`, `frozen_model_manifest.json`, `detection_overlay.png`, `detections.json`, `predicted_pose_targets.json`, `kit_internal_result.json`, `runtime_host_result.json`, `host_gate_result.json`, `runtime.log`, `inference.log`가 실제 존재한다. `final_evidence.json`에 파일별 크기·SHA256, 코드 해시와 최종 검증을 기록했다.

Fresh overlay를 직접 확인했다. 전면 영상 중앙에 벽돌 적층이 가림 없이 들어오고 팔레트는 그 아래 보인다. 배경은 바닥·창문이다. 따라서 이번 관측은 NO_DETECTION/OUT_OF_FOV가 아니다. 마스크 유효 깊이 min/median/max는 .995580/1.058167/3.257009m이며, 배경 혼입 가능성을 배제하거나 pose 정확도를 인증하지 않는다. GT 오차·clearance는 NOT_EVALUATED다.

## 메타데이터 수정과 실행 전 검증

기존 LIT 입력은 `CONSTRUCTION_SITE_E2E_LIT_20261022_v01/construction_site_e2e_lit.usda`, SHA256 `4e0ad262a0ce2a733e86e82e2ba69aa0eee42bb87c33086925117956bbddade8`이다. v01의 실제 `offline_unit_evidence.json` 및 recovery/preview 근거는 원래 좌표 의미1m/Z와 LIT root fallback .01m/Y를 구분한다.

새 RUN/`stage_metrics_1m_z.usda`는 기존 LIT sublayer 하나와 **root metersPerUnit=1, upAxis="Z"만** 작성했다. SHA256 `424cb17b104d7a68a4c264216e38b9823f371524a8704e07fb4eec8b08d1e264`; 실행 전 read-only mode0444로 고정했다. 원본 저장·100배 scale·회전 보정은 없다. root/session stage metadata 의미는 [OpenUSD UsdGeom 문서](https://openusd.org/release/user_guides/schemas/usdGeom/overview.html)와 [UsdStage API](https://openusd.org/release/api/class_usd_stage.html)를 확인했다. 설치 버전 API는 직접 확인해 적용했다.

Bundled pxr 오프라인 `offline_preflight.json` PASS: 최상위 composed1m/Z·두 root metadata authored, root prim spec0, 원본/파생 실제 prim membership·type·기여 source prim stack 일치, 입력hash 일치, 300 nonempty fixture meshes, 단일 rover, active /Render 및 기존 product 접근, active OmniGraph0. 따라서 mesh/xform/camera/light/300 membership opinion은 동일하다.

실제 전면 카메라 `/World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera`의 active/loaded/Camera schema·mount·perspective·양수 focal/aperture·clipping(.01,10000000)·유한 비퇴화 변환·scale 제거 후 no-shear를 검사했다. 위치는 (-25.888,29.009,.5970774262)m이다. Replicator 설치 소스에서 rgb/distance_to_image_plane/camera_params 등록 및 synchronous step(delta_time0, wait_for_render)을 확인했고, Python 구문·실제 inference module import도 통과했다.

**오프라인 실패도 보존:** 첫 preflight는 큰 메쉬 속성 직렬화 후 번들 Stage에 `GetCompositionErrors`가 없어 AttributeError로 exit1했다. Kit launch0인 시점이었다. `offline_attempt1_failure.json`에 남겼고 API 호환 v03에서 root prim spec0 + 실제 prim stack/membership 비교로 대체해 PASS했다. 최초 snapshot 비교 boolean은 저장되지 않아 인증 근거로 사용하지 않는다. 이 정적 검사 실패를 Kit 실패나 센서 음성 결과로 바꾸지 않았다.

Checkpoint SHA256 `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`, pose 원본 SHA256 `cc95b96c3305dcbe257a40fcf16f0e68a9e58ae0d5ae43f9cbd31e80ffec0988`를 확인하고 sdg_tools에서 실제 모델 로드·segment/class0 brick_load를 검증했다. 추론은 기존 imgsz1280/conf.25/iou.70, mask>.5 nearest resize, 최고 confidence/tie index 규약을 유지했다. GT association·fixture pose 주입은 없다.

## 단일 런타임과 종료 판정

`launch_ledger.json`의 기존 Isaac/GUI process0 이후 Isaac5.1 base.python.kit headless RayTracedLighting을 한 번 실행했다. 동일 전면 render product에서 RGB·axial depth·camera_params를 얻었다. timeline time0, stopped, ROS extension0, physics.play/명령/운동0. 카메라 변환 전후 일치, renderer view와 optical 변환 일치, metersPerSceneUnit1.0, 실제 fx=fy317.0431201px, cx320/cy240 확인.

PNG/NPY를 동기 저장한 뒤 다시 열어 완전성을 확인하고 Kit를 닫았다. async viewport capture future를 사용하지 않으므로 저장 future 미완료 shutdown 경로가 없다. 로그는 약17.277초에 shutdown을 기록한다. `app.close()` 뒤 Python marker는 없어 close의 Python return은 UNKNOWN이지만, child exit0 및 이미 저장된 내부 capture PASS와 host/inference 결과는 확인했다. 기존 material binding/fabric 경고와 unknown projection→pinhole fallback 경고는 로그에 보존했으며 실제 cameraModel=pinhole과 projection/calibration 교차 검증은 PASS했다.

호스트는 child exit만으로 성공 처리하지 않고 **내부 PASS·child0·inference0 모두** 요구한다. 내부 FAIL/UNKNOWN 또는 inference 실패면 wrapper1이다. child0/internalFAIL, missing internal, child failure, inference failure, 성공 판정 사례를 검사했다. 이번 실측은 모두 성공해 wrapper0이며, 이번 런에서 내부 실패를 인위적으로 유발하거나 Kit를 재실행하지 않았다.

B4는 fresh mask/depth 역투영 점에 기존 추출 core의 top-band/heading 함수만 적용했다. B5 vertical filter/독립 datum 입력은 적용하지 않았다. 전체 B4/B5 pose pipeline PASS·목표 접근 readiness로 해석하지 않는다.

## 보존과 다음 행동

입력27개 실행 전후 hash PASS, v01 기존 산출물·스크립트14개 hash 보존 PASS, known-lock9개 hash/count PASS(이번 pairing 재감사 아님). 원본·v01·weights·protocol·threshold·카메라·조명은 수정하지 않았다. 과학 패키지 설치/학습/preview 재렌더/ROS/움직임/QUAL12/432 없음, 연구분모0.

변경 파일: 신규 `scripts/construction_site_front_rgbd_capture_20261022_v02.py`, `scripts/construction_site_front_infer_20261022_v02.py`, `scripts/run_construction_site_front_once_20261022_v02.py`, `scripts/preflight_construction_site_front_20261022_v02.py`(실패 보존), API 호환 `scripts/preflight_construction_site_front_20261022_v03.py`, `scripts/check_construction_site_front_camera_20261022_v02.py`, 본 보고서와 PROJECT_STATE append. 외부 RUN에는 실제 센서/추론/상태/검증 증거만 추가했다.

다음 구체 행동은 실제 RGB-D·overlay를 검토하고 독립 pallet datum의 물리적 근거를 확보하는 것이다. 확보 전 B5 target 생성·motion으로 진행하지 않는다. 이번 관측은 engineering-only이며 frozen 연구 lighting/confirmatory/real robot 배포 검증을 대신하지 않는다.
