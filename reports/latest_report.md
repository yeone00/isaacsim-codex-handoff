# 건설현장 프리뷰 가시성 수정 — 2026-10-22

새 정적 프리뷰 파일을 생성했다. **기하 검증 PASS / 실제 GUI_VISUAL UNKNOWN**이다. 이전 사용자 GUI 화면은 실패 증거이며 이전 frustum PASS로 이를 뒤집지 않는다. 이번에도 GUI를 관찰하거나 렌더한 것은 아니므로 실제 가시성 해결 완료라고 판정하지 않는다.

## 열 파일 하나

`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_VISIBLE_20261022_v01/construction_site_e2e_visible.usda`

새 파일에서 기본 카메라는 `/World/ENG_FE2E/ConstructionPreviewCamera`다. 팔레트가 화면 왼쪽, 로버가 오른쪽에 크게 배치되고 실제 원본 현장이 배경으로 남도록 옆에서 내려다보는 구도로 수정했다. 노드 확장·F·속성 수정·반복 재시작은 요청하지 않는다. 원본이나 이전 파일의 저장은 필요 없다.

## 확인된 원인과 아직 확정할 수 없는 원인

**확정된 결함:** 기존 팔레트 투영 폭/높이는 14.46%/14.76%로 이번 실용 기준 15%에 미달했다. 무텍스처 흰 DomeLight는 intensity=2500, exposure=0, color=(1,1,1)로 합성되어 있었다. 밝은 흰 배경과 높은 조명 에너지가 씻겨 보이는 현상에 기여할 수 있다. 새 프리뷰에서 가까운 측면 구도와 intensity=350, color=(.65,.72,.85)를 적용했다. 이 조도는 프리뷰 선택값이며 광도 보정이나 렌더로 검증한 최적값이 아니다.

**GUI 불일치의 단일 근본 원인은 UNKNOWN이다.** 기존 파일의 실제 authored/composed 카메라는 eye=(-30.5,25.4,2.7), 월드 -Z look=(.70354,.64302,-.30260), +Y up=(.22336,.20415,.95312)이며 요청한 표적 방향과 일치한다. `/World`, `/World/ENG_FE2E`의 상위 변환은 identity다. 기존 카메라의 실제 월드 행렬로 계산해도 로버 전체는 약197×204px, 팔레트는117×75px(810×506 기준)이다. 따라서 '현장 전체가250px/로버 없음' 화면을 잘못된 정적 카메라 방향으로 설명할 수 없다. GUI 세션의 다른 카메라 상태·레이어/렌더 상태가 적용됐을 가능성은 가설이다. GUI의 카메라 이름 표시는 사용자 증거로 인정하며 '카메라 미선택'으로 단정하지 않는다.

기존 root `cameraSettings:boundCamera`와 RenderSettings camera 관계는 올바른 prim을 가리켰다. 로컬 Isaac 5.1 `omni.kit.viewport.menubar.camera.../camera_menu_container.py`의 `__ensure_valid_camera`도 root boundCamera 키를 읽는다. 새 파일은 이 키, Perspective position/target, DefaultViewport boundCamera와 실제 RenderSettings camera를 함께 기록했다. 이 메타데이터는 현재 열린 GUI 세션에 강제 적용했다는 뜻은 아니다.

## 실제 합성 형상 확인

인스턴스 proxy를 포함한 순회와 points·purpose·inherited visibility를 확인했다. 모든 대상/조상은 active/loaded이고 visibility 차단은 없다. instance 내부로 들어가지 않는 이전의 단순 mesh count를 근거로 삼지 않았다.

|대상|월드 AABB 최소 m|최대 m|확인|
|---|---|---|---|
|현장|(-35.923,-12.030,-3.760)|(41.678,37.613,8.791)|실제 mesh1, material subset410|
|로버|(-26.584,27.727,-.00844)|(-25.192,29.215,1.565)|mesh20, render/default/proxy visible19, material subset528|
|팔레트+벽돌|(-26.438,29.959,.00122)|(-25.338,31.059,.50522)|실제 nonempty visible brick mesh300, material300, 기존 팔레트Cube5|

로버 본체는 `/World/ENG_FE2E/Rover/base_link/visuals/gl_shell/mesh`이고 실제 points607638개, purpose=default, visibility=inherited다. 본체 AABB는 (-26.2515,27.9299,.06885)~(-25.5245,29.0119,.52415)이다. 로버 전체 bbox만으로 본체 크기를 대체하지 않고 따로 투영했다. guide collision mesh는 렌더 메시 수에서 제외했다. 로버의 보이지 않는 debug Cube도 별도로 확인했다.

기존 rolltainer Plane의 `/World/Looks/OmniPBR` binding은 reference 범위 밖이라 무시되는 warning이 실제로 있다. 다른 rolltainer 본체/rover body의 geometry는 정상 합성되므로 이것을 로버 전체 소실의 원인이라고 하지 않는다. site는 mesh 직접 binding 대신410개 subset material을 사용한다. 전체411개 dependency 목록은 반복하지 않았다. 기존 unresolved MDL/일부 texture의 GUI 해석과 실제 shading은 UNKNOWN이며 임의 텍스처/가짜 proxy 형상으로 대체하지 않았다.

로버/Fixture의 XY/yaw/z, site transform, 바닥·collision, 원본 형상·팔레트300 membership은 변경하지 않았다. 두 대상 y AABB 간격은 .74439m다. 새 preview-only 물체 pose도 도입하지 않았다. 단일 로버/PhysicsScene, active OmniGraph0을 재확인했다. 물리 contact/주행 가능성은 검사 범위가 아니다.

## 수정된 실제 카메라 검증

카메라 eye=(-29.35,29.4,2.6), target=(-25.888,29.4,.65). 명시적인 SetLookAt 역행렬 하나와 resetXformStack을 사용한다. 실제 월드/view/projection 행렬과 -Z/+Y 축, authored opOrder·전체 camera attrs는 manifest에 보존했다. Perspective, focalLength24, aperture36×22.5, clipping .05~250m, shutter open/close0, exposure0이다. time-sampled camera ops는 없다. RenderSettings1600×1000과 기본 viewport camera 모두 동일한 실제 카메라를 참조한다.

|대상|투영 폭×높이 비율|810×506 화면 예상 bbox|화면 중심 (u,v)|카메라 깊이 m|
|---|---|---|---|---|
|로버 전체|35.69%×55.84%|289×283px|(.704,.485)|2.918~4.903|
|로버 본체|20.70%×20.21%|168×102px|약(.660,.584)|모든 corner frame 안|
|팔레트+300벽돌|23.21%×26.76%|188×135px|(.306,.600)|3.565~4.771|

USD row-vector/world inverse 및 실제 projection matrix로 AABB8 corners를 투영했다. 가로·세로15% 초과, 중심/모든 corners 화면 안, near/far clip 여유 PASS다. 픽셀은 명시된 가상 해상도 기준 근사이며 GUI 실측이 아니다. 현장 실제 삼각형과 카메라→각 대상 중심 segment 교차0/0이다. 이는 전체 표면 가림이나 로버 자체가림/재질 렌더 PASS를 보장하지 않는다. 단일 detail 구도로 두 대상이 기준을 만족하므로 사용자에게 여러 후보 파일/카메라를 요구하지 않는다.

## 파일·실행·보존

- Builder: `scripts/build_construction_site_visible_20261022_v01.py`, bundled pxr launcher `.sh`.
- 본체 확인: `scripts/check_construction_site_visible_body_20261022_v01.py`.
- 실행: `bash scripts/build_construction_site_visible_20261022_v01.sh` (프로젝트 cwd). 새 output mkdir(exist_ok=False)에 해당하는 사전 충돌거부; 이 경로는 이제 사용됐으므로 재실행하면 실패해야 한다.
- 실제 런타임: `/home/user/anaconda3/envs/hh_isaac51/bin/python` + Isaac 5.1 `omni.usd.libs-1.0.1+69cbf6ad.lx64.r.cp311`; SimulationApp/omni/ROS import 없음.
- 증거: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_VISIBLE_20261022_v01/manifest.json`, `body_geometry_check.json`, `build_status.json`, `build_validation.log`. 명령/원본 hashes/코드 hash/환경과 실제 행렬·투영·mesh/material count를 기록했다.
- 새 USD SHA256: `828cc1d00509298473ebc65fd67bd02834c05b87683ab6002af08e65fc8547bc`.
- 이전 USD SHA256: `faf516f5d44b2e61a59eaafff54ad6a524a5bb5c5087a5788e352e63c50b6a19` 일치.
- cement HR_Scan SHA256: `a3fbf6bd87d71007ae756a3288140d842d6e91135ee10d230a4ce52780d8f87c` 일치.

Builder exit0, checks11개 PASS, 본체 별도 check exit0, Python compile/bash syntax PASS. old composed used-layer hashes는 수정 전후 모두 일치했다. 새 output은 생성 전 없었고 기존 원본·v01/attempt0002·과거 실패를 덮어쓰지 않았다. 잠금/성공기준/실험 결과 변경 없음. 현장 GUI 스크린샷·로컬 렌더는 생성하지 않았다. 기존 GUI 조작/추가 Isaac launch/physics.play/ROS/actuation/training/432=0, 연구 denominator0.

다음 구체적 단계는 위 새 USD 하나를 기존 GUI에서 여는 것이다. GUI_VISUAL은 실제 관찰 전 UNKNOWN이다. 프리뷰가 사용 가능한 것이 확인된 뒤에만 실제 on-rover front RGB-D→frozen YOLO→B4/B5로 이어간다. Forward-only approach는 후속 별도 작업이며 기존 physical stop FAIL/ROS guard 문제를 유지한다. 새 graph/ROS/HOLD 프로젝트나 benchmark를 실행하지 않았다.
