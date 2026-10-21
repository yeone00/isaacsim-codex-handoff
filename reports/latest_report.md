# 실제 건설현장 Isaac Sim 프리뷰 — 2026-10-21

새 USD를 실제 생성했다. 원본 건설현장·로버·기존 팔레트와 cement HR_Scan 벽돌 300개를 합성했다. 격리된 EngineeringFloor 벤치가 최종 환경이 아니다. **정적 장면 구성 PASS, 전체 렌더 의존성 PARTIAL, 동역학/E2E UNKNOWN**이다.

## GUI에서 열 파일 — 이 경로 하나

`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/construction_site_e2e_preview.usda`

카메라 `/World/ENG_FE2E/ConstructionPreviewCamera`와 기본 viewport의 position/target/boundCamera 및 render camera를 저장했다. 현장 안의 로버와 적재물을 함께 보는 시점이다. 두 대상의 bounding box 모서리 8개씩 모두 frustum 안이며, 현장 삼각형에 대한 카메라→각 대상 중심 시선의 차폐 교차 0개다. 실제 GUI 렌더/자동 카메라 적용은 미검증이다. GUI 조작·두 번째 SimulationApp 없이 스크린샷을 얻을 수 없어 제공하지 않는다.

## 자산과 배치

|역할|실제 prim|world origin m|
|---|---|---|
|원본 건설현장|`/World/ConstructionSite`|(0, 0, 0)|
|로버|`/World/ENG_FE2E/Rover`|(-25.88797768, 28.4708691133, -0.00835194), yaw 90°|
|팔레트·적재물|`/World/ENG_FE2E/Fixture`|(-25.888, 30.509, 0.00121562), yaw 90°|
|물리 장면|`/World/ENG_FE2E/PhysicsScene`|원본 PhysicsScene 참조|
|프리뷰 카메라|`/World/ENG_FE2E/ConstructionPreviewCamera`|(-30.5, 25.4, 2.7), target (-25.85, 29.65, 0.7)|

- 현장 원본: `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`. SHA256 `224cac492d267d0403c9402484fcf84011191208fb4689e7e3fc33eadf3756fe` 일치. 실제 현장 참조는 `/home/user/hh/isaac_cosmos/assets/assets/environment/Constructionsite_isaac.usdz`다.
- 로버: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01/attempt_0001/derived_calibration.usda`의 `/World/ENG_FE2E/Rover`만 참조. 이 로버는 지정 원본의 `/World/ROBOT_TASK/RuntimeRover`를 참조한다. 벤치 바닥·다른 배우는 가져오지 않았다.
- 적재물: `/home/user/hh/isaac_cosmos/sdg_final/DEMO_FE2E_001_HR_GEOM_v01/attempt_0001/derived_scene.usda`의 `/World/ENG_FE2E/Fixture`만 참조. 기존 FULL 300개 membership·방향·팔레트 형상을 재생성 없이 유지했다. demo의 2m 로버 시작 위치는 가져오지 않았다.
- 선택 자산: `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_HR_Scan.usd`, SHA256 `a3fbf6bd87d71007ae756a3288140d842d6e91135ee10d230a4ce52780d8f87c`. 잠긴 cement/red × HR_Scan/LR_Scan/Proxy/GeoCAD 8개 모두 hash 일치 확인, 이번 장면은 cement HR_Scan 하나만 사용한다. LR은 독립 재구성이다.
- XY/yaw는 고정 geometry v02의 FE2E_S001 nominal 위치다. 원본 로버 z=.15는 현장 바닥에서 뜨므로 **프리뷰만** 실제 site 삼각형 바닥에 맞췄다. 로버 위치 바닥 z=-.00843751, 자재 위치 z=.00121562; 로버 하단 z=-.008437512. 이 수직 보정은 연구 geometry 변경 승인이나 실행 결과가 아니다. 연구 lock/원본은 수정하지 않았다.

## 제한된 오프라인 검증

PASS: 원본 입력 hash 보존, 현장 메시 visible/inherited, 로버·자재 visible/inherited, 로버 1대/PhysicsScene 1개, 300개 AssetRef가 모두 잠긴 cement HR_Scan 참조, active graph 0개. 3개 Articulation Controller는 모두 targetPrim=`/World/ENG_FE2E/Rover/base_link`, robotPath 빈 문자열이다. 해당 그래프는 프리뷰에서 inactive다. 기존 site 로버·타깃·debug·Replicator·벤치 등은 새 layer에서만 suppress했다. 기존 현장 collision mesh와 ambient dome을 유지하고 추가 floor는 만들지 않았다.

로버/적재물 AABB의 y 간격은 0.74438584m로 서로 겹치지 않는다. 실제 PhysX contact, 바닥 기복에 대한 모든 wheel 지지, nested articulation, 이동 corridor의 .10m clearance는 인증하지 않았다. 물리 실행 없이 이 항목들을 PASS로 바꾸지 않는다.

PARTIAL: USD layer 22개와 asset dependency 411개를 수집했으나 dependency closure에 다음 unresolved가 있다. 이는 disabled source branch도 포함하는 전체 파일 의존성 검사이므로 모두 active 현장에 필요한 누락이라고 단정하지 않는다. 핵심 현장/로버/300 자재 geometry는 실제 composed 됐다.

- `/home/jh/Downloads/rolltainer_stl/apriltag_100.png`
- `/home/user/hh/isaac_cosmos/assets/assets/objects/textures/mitex_box_u0_v0_diffuse.jpg`
- `OmniPBR.mdl`
- `OmniSurface.mdl`
- `gltf/pbr.mdl`
- `https:/omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Environments/Grid/Materials/Textures/WireframeBlur_basecolor.png`
- `https:/omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Environments/Grid/Materials/Textures/WireframeBlur_blue.png`
- `https:/omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Environments/Grid/Materials/Textures/Wireframe_blue.png`
- `https:/omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/5.1/Isaac/Environments/Grid/default_environment.usd`

MDL은 standalone resolver에 Kit 검색 경로가 없는 영향일 수 있으나 GUI 해결 여부 UNKNOWN이다. 누락된 로컬 PNG/JPG의 올바른 대체 경로는 UNKNOWN이며 임의 텍스처로 바꾸지 않았다.

## 전달 파일과 재구성

- USD: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/construction_site_e2e_preview.usda` (SHA256 `faf516f5d44b2e61a59eaafff54ad6a524a5bb5c5087a5788e352e63c50b6a19`).
- Manifest: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/manifest.json` — source/22 layer hash, 8개 자산, prim·위치·bounds·카메라·controller·suppression·의존성.
- 검증: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/build_status.json`, `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/camera_geometry_checks.json`, `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/build_validation.log`.
- Builder: `/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/build_construction_site_preview_20261021_v01.py`.
- CLI: `/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/build_construction_site_preview_20261021_v01.sh`.
- 카메라 검사 코드: `/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/check_construction_site_preview_camera_20261021_v01.py` (이번 attempt_0002 대상으로 고정; 기존 검사 출력 덮어쓰기 거부).

재구성 명령: `bash scripts/build_construction_site_preview_20261021_v01.sh --output <새로운_미사용_절대경로>` (프로젝트 cwd). 확인한 Isaac bundled pxr와 native library만 사용한다. SimulationApp/omni/ROS를 import하지 않는다. 기존 output은 거부한다. 외부 원본의 위치·내용은 manifest hash와 같아야 동일 구성을 재현한다.

최초 build는 graph를 inactive로 만든 뒤 기존 prim handle을 읽어 expired-prim 오류로 실패했다. `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/build_status.json`와 `build_failure.log` 및 첫 파일을 보존했다. validity 검사 수정 후 별도 attempt_0002를 생성했다. 두 번째 build의 exit1은 unresolved 의존성에 따른 OFFLINE_PARTIAL이며 성공 exit으로 숨기지 않았다. 시뮬레이션 재시도는 없다. Python compile/bash syntax 확인 PASS; 연구 sweep·단위테스트 확장 없음.

## 바로 다음 E2E 연결 단계 — 이번에 실행하지 않음

1. 이 건설현장을 환경으로 유지한 새 engineering runner에서 실제 mounted camera `/World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera`의 fresh RGB-D → frozen YOLO → B4/B5 → predicted target을 연결한다. 평가 GT/프리뷰 배치 좌표는 perception·pose·controller 입력에 넣지 않는다. 고정 observation policy와 paired representation 조건을 유지한다.
2. 별도 승인된 motion 작업에서 기존 forward-only approach → 정지 handoff → frozen PRE/FINAL → zero/quiet 평가를 이 현장에서 연결한다. 기존 격리 stop calibration의 이동 PASS나 graph-only PASS를 건설현장 E2E PASS로 쓰지 않는다. 현재 그래프는 안전한 정적 프리뷰를 위해 꺼져 있어 이 파일 자체가 motion runner는 아니다.

직접 blocker는 legacy `PUBLISHER_SET` root cause UNKNOWN과 실제 zero-stop 34.127mm 후퇴/raw-root quiet FAIL이다. .03m long/lat, yaw2°, root+COM+FD quiet .002, clearance .10 및 frozen 성공 기준은 그대로다. K1은 STOP_HOLD_BRANCH 유지. ENG001/QUAL12/432는 진짜 단일 E2E 성공 전 HOLD이며 이번 launch/physics/ROS publish/motion/research denominator 모두 0이다. 렌더 appearance는 위 누락 의존성과 GUI 미검증이 남는다.
