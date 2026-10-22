# 건설현장 runtime prim / 크래시 수정 — 2026-10-22

새 USD의 runtime namespace 수정과 실제 Kit 로드/viewport RenderProduct 확인은 PASS다. **전체 smoke는 캡처 파일 즉시 확인 AssertionError로 FAIL**, host exit는 0이다. 성공 exit가 내부 실패를 덮지 않도록 별도 판정했다. 실제 저장된 headless 이미지는 매우 어두워 **HEADLESS_VISUAL FAIL**, 사용자 GUI 가시성은 **GUI_VISUAL UNKNOWN**이다. 재실행하지 않았다. 이전 사용자 GUI의 `Aborted (core dumped)`는 **CRASHED**로 유지한다.

## 전달 파일과 범위

최종 USD:
`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_RUNTIME_FIX_20261022_v01/construction_site_e2e_runtime_fixed.usda`

최종 SHA256: `97da3867a2297f2f90d10ce120280c06e4b1cc71833e51d7862e8399794c3ab6`.

- 최종 builder: `scripts/build_construction_site_runtime_fix_20261022_v02.py`, launcher `.sh`. 기존 visible/preview builder는 수정하지 않았다. 새 builder v01 실패도 보존했다.
- 최종 offline 검사: `scripts/check_construction_site_runtime_fix_20261022_v02.py`.
- 한 번의 Kit 검사/host launcher: `scripts/check_construction_site_kit_load_20261022_v01.py`, `scripts/run_construction_site_kit_once_20261022_v01.py`.
- 원본·이전 output·프로토콜·controller·체크포인트 변경 없음. 카메라 위치/target/asset pose/조명 변경 없음. 신규 바닥 없음. physics.play/ROS/actuation/ENG001/QUAL12/432=0, 연구 분모0.

## 확인된 작성 결함과 수정

실제 bundled `pxr`로 원본 parent site, calibrated derived reference, preview/visible USD를 합성해 확인했다. 이전 보고서의 기하 PASS는 runtime namespace/GUI PASS가 아니며 이번 사용자 관측이 결함을 확정한다.

1. `scripts/build_construction_site_preview_20261021_v01.py:38-39`의 pseudo-root children 중 World 외 전부 `SetActive(False)` 루프가 `/Render`를 껐다. 실제 authored opinion은 `CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/construction_site_e2e_preview.usda`의 `/Render active=false`다. 원본 recovery USD는 active=true다. visible v01은 이를 그대로 상속했다.
2. 같은 builder의 35–37행 World children 일괄 비활성화가 `/World/Rover_Calibration active=false`를 작성했다. 원본 recovery USD는 이 루트에 `rover_base_camera_51_SUCCESS.usd` reference를 갖고 활성이다. 원본에 `/World/Rover_Calibration/rover_base`도 실제 존재/활성이다. 따라서 이전 합성에서 부모 비활성은 **로컬 확인된 사실**이다. 다만 사용자의 native expired-prim 예외를 던진 정확한 C++ 호출/보관된 handle은 확보하지 못했다. 비활성 부모가 발견됐다는 이유로 전체 native stack 원인을 확정하지 않는다.
3. 원본 `/Render/OmniverseKit/HydraTextures`에는 viewport 제품과 Replicator, Replicator_01, Replicator_02가 있다. viewport와 _01/_02의 `camera`는 옛 calibration RoverFrontCamera 경로, Replicator는 꺼진 `/World/RobotCameraFixed`를 가리킨다. `/Render/OmniverseGlobalRenderSettings.products`는 이 제품과 이미 없는 Step16D 조명 캘리브레이션 제품들도 예약한다. 이것은 **확인된 stale consumer**다. `/Replicator/SDGPipeline/OgnGetPrims_01.inputs:pathPattern`도 옛 camera 경로지만 `/Replicator` 자체는 계속 inactive다. source 속성 조사에서 별도 calibration Python script hook은 확인하지 못했으며, 모든 외부 GUI callback 부재를 증명한 것은 아니다.

새 layer는 `/Render`, `/Render/OmniverseKit`, `/Render/OmniverseKit/HydraTextures`만 활성화하고 viewport 제품의 camera를 현재 detail preview camera에 재연결한다. 오래된 Replicator 제품3개는 개별 inactive, global/preview RenderSettings.products는 viewport 하나로 한정한다. 옛 renderer 설정을 통째로 활성화하거나 전부 지우지 않았다.

Calibration 루트와 rover_base는 활성 namespace로 유지한다. 루트의 GroundPlane/Cube/Camera와 rover_base의 모든 직계 자식(링크·바퀴·joints·Looks)은 새 layer에서 개별 inactive다. 따라서 이 namespace에서 활성 prim은 컨테이너2개뿐이며 geometry/camera/physics API/graph가 없다. 두 번째 로버나 옛 controller를 활성화하지 않았다. 임의의 가짜 로버/대체 형상/카메라 alias도 만들지 않았다. 현재 로버의 후방 camera만 추가 inactive로 하여 실제 front camera와 detail camera 두 개를 유지했다.

다른 억제 root도 원본/preview/fixed 활성 상태를 조사했다. `/Replicator`는 옛 SDG graph 때문에 계속 inactive, `/World/ROBOT_TASK`는 기존 RuntimeRover/PhysicsScene 중복 방지를 위해 계속 inactive다. `/World/TestSetup`, `/World/RobotCameraFixed`, `/World/SDGTarget_Mitex`, `/World/ROBOT_TASK_TARGET`, `/World/RobotTaskDebug` 등 옛 실험 root는 일괄 복구하지 않았다. 전체 실제 root 목록과 각 layer active opinion은 output의 `authored_active_diagnostics.json`에 있다.

## 합성 readback과 형상

|경로|이전 composed|수정 composed|새 layer authored|
|---|---|---|---|
|/Render|false|true|true|
|/Render/OmniverseKit 및 HydraTextures|부모 비활성으로 없음|true|true|
|viewport RenderProduct|부모 비활성으로 없음|true|상위 true, camera 재연결|
|/World|true|true|새 active opinion 없음|
|/World/Rover_Calibration|false|true|true|
|/World/Rover_Calibration/rover_base|부모 비활성으로 없음|true, 빈 형상 컨테이너|true|
|/World/ROBOT_TASK|false|false|기존 false 유지|
|/World/ROBOT_TASK/RuntimeRover|부모 비활성으로 없음|없음|추가 없음|
|/World/ENG_FE2E 및 Rover/Fixture|true|true|기존 상태 유지|

Rover/Fixture/site bounds, visible/nonempty mesh와 material/subset 집계는 수정 전후 정확히 같다. 활성 geometry rover1, PhysicsScene1, OmniGraph0, RenderProduct1, camera2다. Fixture 실제 visible/nonempty mesh300, cement HR_Scan reference 및 300 membership의 기존 layer와 hash를 보존했다. camera world=(-29.35,29.399999999999995,2.6000000000000028), target=(-25.888,29.4,.65). 부동소수점 오차 허용1e-10로 확인했다.

- `/World/ConstructionSite`: bbox `[[-35.922999532751746, -12.03000091842822, -3.76000491489485], [41.678000472232675, 37.613003106975654, 8.791001771608157]]`, visible mesh 1, nonempty mesh 1, material subset 410, bound mesh 0.
- `/World/ENG_FE2E/Rover`: bbox `[[-26.58353353126272, 27.727124082005997, -0.00843751199999998], [-25.19242182873728, 29.214614144527538, 1.564688323444346]]`, visible mesh 19, nonempty mesh 20, material subset 528, bound mesh 9.
- `/World/ENG_FE2E/Fixture`: bbox `[[-26.43800001192093, 29.95899998807907, 0.0012156202235174187], [-25.337999988079073, 31.05900001192093, 0.5052156203391005]]`, visible mesh 300, nonempty mesh 300, material subset 0, bound mesh 300.

## 보존한 입력과 검증 실패 이력

원본 parent: `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`.
Calibrated rover reference: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01/attempt_0001/derived_calibration.usda`의 `/World/ENG_FE2E/Rover`; 원본 RuntimeRover를 참조한다. Fixture reference는 `DEMO_FE2E_001_HR_GEOM_v01/attempt_0001/derived_scene.usda`의 기존 Fixture다.

이전 visible manifest의 input_layer_hashes를 실제 파일과 대조했고 현재 source used-layer 전체 hash도 Kit 종료 뒤 다시 일치했다. 전체 path/hash는 `manifest.json.source_hashes`, `.prior_hash_inventory_verified`에 보존했다. 주요 값:

- `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_VISIBLE_20261022_v01/construction_site_e2e_visible.usda`: `828cc1d00509298473ebc65fd67bd02834c05b87683ab6002af08e65fc8547bc`
- `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/construction_site_e2e_preview.usda`: `faf516f5d44b2e61a59eaafff54ad6a524a5bb5c5087a5788e352e63c50b6a19`
- `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`: `224cac492d267d0403c9402484fcf84011191208fb4689e7e3fc33eadf3756fe`
- `/home/user/hh/isaac_cosmos/assets/assets/objects/cement_brick_HR_Scan.usd`: `55716ba771ba02b0d07492a60ab9ea3d38925dc1353ac980b4bd5d7d3a113157`
- `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_HR_Scan.usd`: `a3fbf6bd87d71007ae756a3288140d842d6e91135ee10d230a4ce52780d8f87c`
- `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01/attempt_0001/derived_calibration.usda`: `ccd37e6493813884f49c66d7ae94419e0009293bb33954e0a241d23c775910f2`

처음 새 builder v01은 USD를 생성했으나 front camera 이름을 RoverFrontCamera로 가정하고 camera world float를 exact equality로 비교하여 exit1/FAILED다. 별도 v01 검사에서 실제 rear camera가 남아 있음도 확인했다. 초기 후보는 `failed_offline_candidate.usda`로 byte 보존했고 원래 manifest/build_status/offline_check 실패를 그대로 남겼다. 최종 새 USD에 rear camera만 비활성화했으며, 최종 builder v02와 offline_check_v02는 실제 front_Camera 경로/float tolerance/카메라2개를 확인한다. 최종 offline17 checks PASS이며 geometry/material 집계는 동일하다. Kit는 이 최종 파일에 대해서만 한 번 실행했다. 오류를 지우거나 실패를 PASS로 덮어쓰지 않았다.

## 실제 한 번의 no-motion Kit 검사와 종료

명령: `python3 scripts/run_construction_site_kit_once_20261022_v01.py`.
Host gate는 `/proc`의 comm/cmdline에서 Kit/Isaac/SimulationApp 프로세스를 확인했고 실행 전 해당 프로세스0이다. ledger의 exclusive create로 같은 output 재시도는 거부한다.

실제 runtime: `/home/user/anaconda3/envs/hh_isaac51/bin/python`, Isaac 5.1 `isaacsim.exp.base.python.kit`/SimulationApp. 이전 offline 실행은 Isaac `omni.usd.libs-1.0.1+69cbf6ad.lx64.r.cp311` PYTHONPATH와 bin/conda lib를 지정했다. 과학 패키지 설치/업데이트 없음.

실제 Kit readback (`kit_load_result.json`): exact final stage, `/Render active=true`, calibration active=true, viewport render_product_path=`/Render/OmniverseKit/HydraTextures/omni_kit_widget_viewport_ViewportTexture_0`, 실제 RenderProduct valid/active, camera 현재 detail 경로 및 위 world position. 활성 ROS extension은 빈 목록, timeline_playing=false, physics.play 호출0, active OmniGraph0. original/derived USD 저장은 하지 않았고 runtime edit target은 session layer다.

Native `Failed to define UsdPrim`, `UsdExpiredPrimAccessError`, terminate/core dump는 이번 log에 없다. 원본 rolltainer material binding이 reference scope 밖이라 무시되는 기존 warning, fabric의 `/World/ENG_FE2E/Rover/rear_right_wheel_link/collisions/mesh_0` non-existent path warning은 실제 log에 남아 있다. 이 warning을 성공으로 숨기거나 새 trial로 고치지 않았다.

**정확한 내부 실패:** `check_construction_site_kit_load_20261022_v01.py:35`, `task.result(); assert (OUT/'static_preview.png').is_file()` → AssertionError. Capture future 이후 파일 기록 시점이 달라 즉시 존재 assertion이 실패했을 가능성이 있으나 원인을 확정하지 않는다. `kit_failure.json`에 stack 보존. finally의 `app.close()` 이후 host returncode=0/EXITED이고 `[15.209s] Simulation App Shutting Down`이다. `kit_shutdown.json`은 생성되지 않았으므로 app.close의 Python return 확인은 UNKNOWN이다. 전체 smoke는 내부 FAIL로 집계하며 host exit0만으로 PASS라 하지 않는다. 이번 실행은 CRASHED로 판정할 native/signal 증거가 없다. 사용자 이전 GUI core dump는 별도로 CRASHED다. 재시도0/추가 launch0.

## 실제 이미지와 남은 제약

종료 뒤 `static_preview.png`가 실제 저장돼 직접 열어 확인했다(1000×625). 좌측 pallet/벽돌 덩어리와 우측 로버/rolltainer 윤곽 및 현장 구조는 보이지만 전체가 매우 어둡고 로버/자재 식별성이 불충분하다. **HEADLESS_VISUAL FAIL_DARK_INSUFFICIENT_IDENTIFIABILITY**, **GUI_VISUAL UNKNOWN**이다. bbox를 visual PASS로 바꾸지 않았다. 조명·노출·오래된 per-product renderer 속성 및 GUI 환경 차이의 기여도는 이번 한 번으로 분리되지 않았다. 원본 renderer 제품에는 invertColorCorrection/invertToneMap 등 과거 속성도 있으며 이번에는 카메라 consumer 경로만 고쳤다. 임의 노출/조도 sweep이나 또 다른 카메라 변경은 하지 않았다.

최종 이미지 SHA256: `4f2aabda24be8ff8be2d10199a5068234c161721b6c920b1867eec349dc9a083`.

정확한 남은 blocker는 실용적인 밝기/식별성 미확보다. 런타임 namespace 결함은 실제 로드에서 복구 확인했지만 모든 GUI callback/재오픈 lifecycle의 무크래시 보장은 아니다. 다음 사용자 동작이 필요하면 **위 최종 USD 하나를 GUI에서 한 번 열기**로 제한한다. 추가 스크립트 편집/스크린샷 반복은 요구하지 않는다. 후속 조명/색관리 수리는 실제 이미지와 runtime renderer 설정에 근거한 별도 범위이며 이번에는 허용한 단일 load 뒤 재실행하지 않았다.

## 변경 파일과 검사

새 builder v01/v02와 launcher2, offline checker v01/v02, 단일 Kit checker/host launcher, 이 보고서 추가; docs/PROJECT_STATE.md append. Bulk USD/PNG/log/hash JSON은 위 외부 output에만 있다. compile4 및 bash syntax PASS, offline 최종17 checks PASS, prior layers/최종 USD post-Kit SHA 보존 PASS, runtime load/product PASS, capture smoke FAIL, host EXITED0, headless visual FAIL, GUI UNKNOWN. cwd에 Git metadata가 없어 `git status --short`는 not a git repository로 실패했다. staging/push/remote 변경 없음.
