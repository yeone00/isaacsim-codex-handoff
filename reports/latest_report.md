# 3표현 pilot prepare-only v23 — 2026-11-02

**실제 파생 overlay 3개 생성·검증 완료. 최종 HR/LR/CAD 모두 BLOCKED. Kit/ROS live NOT_TESTED, research observations0, formal denominator0.** 21/23 정적 gate와 cross-row identity는 통과했지만, 동일 표준 box의 양의 부피 겹침96쌍 및 공통 rolltainer Plane의 깨진 material binding 때문에 PREPARE_PASS를 부여하지 않았다.

[기계 manifest](../manifests/construction_site_pilot_prepare_20261102_v23.json) · [최종 checker 결과](construction_site_pilot_prepare_checks_20261102_v23.json) · [8개 focused 검사](construction_site_pilot_validation_20261102_v23.json) · [정밀 geometry 증거](construction_site_pilot_geometry_detail_20261102_v23.json) · [pilot-only DRAFT](../docs/construction_site_pilot_amendment_DRAFT_20261102_v23.md) · [v24 최소 runtime 계약](../docs/construction_site_pilot_runtime_contract_20261102_v23.md)

## 최종 준비 상태

| 표현 | 파일/72 hash·mapping | standalone 구성·300 static 매핑 | 안전·활성 재질 포함 최종 | live render/PhysX/ROS | 과학 admission |
|---|---|---|---|---|---|
| HR_Scan | PASS | PREPARE_PASS (제한된 정적 항목) | **BLOCKED**: 겹침96 + binding | NOT_TESTED | HOLD |
| LR_Scan | PASS | PREPARE_PASS (제한된 정적 항목) | **BLOCKED**: 겹침96 + binding | NOT_TESTED | HOLD |
| GeoCAD | PASS | PREPARE_PASS (제한된 정적 항목) | **BLOCKED**: 겹침96 + binding | NOT_TESTED | HOLD |

cross-row collider transform·dimension·enabled state 및 고정 scene signature는 정확히 같다. 이것은 **안전한 live physics parity 인증이 아니다**. 공통 static load는 적재물 질량/동역학을 제거하는 새 조건이며 v21 HR 성공도 새 파일럿 관측으로 재사용하지 않았다. 아래 경로는 모두 실제 생성됐다. bulk USD/로그/전체 mesh inventory는 Git 밖에 있다.

## 실제 overlay와 선택

모든 asset root: `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/`. 모든 model root: `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/`. 아래 전체 SHA와 절대경로는 manifest에도 동일하게 기록했다.

### HR_Scan — BLOCKED

- Overlay: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/HR_Scan_04/pilot_scene.usda`
- Overlay SHA256: `37895379cd0ac5a9b729b526bbf7b4548e7768ad404726beaa3b64a8bb200a03`
- Asset: `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_HR_Scan.usd`
- Asset SHA256: `a3fbf6bd87d71007ae756a3288140d842d6e91135ee10d230a4ce52780d8f87c`
- Matched model: `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_HR_Scan_M50_REALVAL_MASKBEST_v01.pt`
- Model SHA256: `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`
- 실제 정적 검사: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/HR_Scan_04/prepare_check.json`
- 실행 상태·소스 snapshot·stdout: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/HR_Scan_04/`

### LR_Scan — BLOCKED

- Overlay: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/LR_Scan_03/pilot_scene.usda`
- Overlay SHA256: `dd06e774715d8c8b362954c3d9b56f230a7c40a18336acb52b104499f37df4c8`
- Asset: `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_LR_Scan.usd`
- Asset SHA256: `5781f72b71940938883f94a1325920a2a87ed768cba37a0000fa6fefd85256e1`
- Matched model: `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_LR_Scan_M50_REALVAL_MASKBEST_v01.pt`
- Model SHA256: `d58e18a87f4cafba6fd92d8bade6e2ff12ad2380db427311b072859fd2cca42f`
- 실제 정적 검사: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/LR_Scan_03/prepare_check.json`
- 실행 상태·소스 snapshot·stdout: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/LR_Scan_03/`

### GeoCAD — BLOCKED

- Overlay: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/GeoCAD_04/pilot_scene.usda`
- Overlay SHA256: `fa44819add283dd56644ff2e936539a161f9ad5b6aabf56ffe1b0f452000559d`
- Asset: `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/cement_brick_GeoCAD.usd`
- Asset SHA256: `e579f77f46debf05fca23d6bfc5c08217cc9541b3d932dee1088559cbef4699b`
- Matched model: `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_GeoCAD_M50_REALVAL_MASKBEST_v01.pt`
- Model SHA256: `bbfb9fc8d0c421154844f7e299b6d8162b9394eb07d36a31110f593c0813ce8f`
- 실제 정적 검사: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/GeoCAD_04/prepare_check.json`
- 실행 상태·소스 snapshot·stdout: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v23/GeoCAD_04/`

## 실제 구현·검증한 것

새 [prepare adapter](../scripts/construction_site_pilot_prepare_20261102_v23.py)는 `--representation {HR_Scan,LR_Scan,GeoCAD}`와 v22 manifest를 받는다. `--prepare-only`만 허용하고 `--run`/Proxy를 거절한다. 설치된 Isaac 5.1의 Python과 `omni.usd.libs` 경로를 기존 runner와 같은 방식으로 사용하되 SimulationApp/Kit/omni/ROS/model을 import하지 않는다. v22의 검사 함수를 재사용해 입력72개 SHA와 frozen108/432 exact-set·4rep pairing·geometry 모든 열 join을 확인했다. 원래 v22 hard block은 수정하지 않았다.

COW overlay는 실제 v21 `prepared_site_drive.usda`를 sublayer로 참조한다. 이 baseline SHA는 v21 `prepare.json`의 expected와 일치했다. 원본 site/stage/source/모델/잠금/기존 evidence에는 저장하지 않았다. 각 output에는 source snapshot, command, standalone 환경, per-execution 상태, 실패/exit code, 해시와 상세 검사 JSON을 보존했다.

**중요한 instance/reference 해결:** 실제 300 AssetRef를 instance-proxy-aware traversal로 찾았다. 상위 scene reference 안에서 온 HR arc는 강한 local `references=[selected]`만 써도 합성에 남는 것을 로컬로 확인했다. 초기 CAD에는 HR와 CAD mesh가 함께 나타났다. 최종 전략은 각 실제 AssetRef만 instanceable=false로 하고, 원래 하위 분기300개를 derived layer에서 active=false로 만든 다음, 같은 slot frame의 새 `PilotVisual_v23` child에 selected normalized USD만 명시적으로 참조하는 것이다. 활성 mesh prim stack이 선택 자산의 dependency layer들에서만 오는지 확인했다. 원래 HR dependency가 보존된 sublayer 안에 존재하는 것과 활성 visual 혼합을 구분한다.

원래 AssetRef300의 전체 world matrix·orientation·membership은 불변이다. 전체 rover/fixture/camera/ROS ActionGraph의 composed attributes·connections·relationship targets signature도 baseline 및 세 행 간 동일하다. Proxy는 CAD의 Looks appearance dependency로 계속 해석된다. CAD는 mesh 하나에6개 material subsets가 있으므로 root mesh의 직접 binding 없음만으로 material FAIL을 내리지 않고 face partition12면과 subset binding을 검사했다. HR/LR의 활성 binding 각각300, CAD subset binding1800을 검증했다.

모든 표현에서 native brick collision/rigid 활성0, canonical static Cube300, CollisionAPI enabled=true/RigidBodyAPI 없음이다. cube는 원래 SideStanding의 sibling이며 local dimension190×90×57mm/center(0,0,.0285)m를 사용한다. guide purpose는 렌더 구분용이며 collisionEnabled를 끄지 않는다. live safety 소비자의 실제 PhysX shape 등록은 미검증이다. 원래 visual은 선택 자산 참조로 보존하고 native HR가 포함된 기존 분기는 비활성화했다.

정적 world m/Z-up, sublayer/reference composition 및 활성 selected geometry/source mapping PASS. canonical collider와 rover 시작자세 overlap0, ground/fixture surface triangle-box SAT penetration0이다. 현장 collider mesh382,994면에 대해 load envelope/triangle broad phase 뒤 SAT를 적용했다. 이 surface 검사는 충돌 표면 침투 점검이며 mass·contact offset·friction·settling·load stability 증명이 아니다.

visual standard envelope 초과 최대값은 HR 약2.854e−9m, LR 약1.027e−9m, CAD 약1.789e−9m로 1µm 수치허용보다 작았다. geometry를 축소·이동해서 맞춘 것이 아니다. 세 표현의 unit/axis 불일치나 standard envelope 밖 실질 돌출은 발견하지 못했다.

canonical signature: `636b754bce87434d1b20d46930dc85660e35d3075dbba3e6eaec9ca26c1d627d`. 고정 scene signature: `771b8d722f05abbb29def38937fff9c7229216292f00897d8d824a7de4f37ffc`. 상세 collider matrix·bounds·native disable 기록·모든 선택 reference·활성 binding·dependency layer SHA는 각 prepare_check JSON에 있다.

## 남은 두 blocker와 bounded 해결

**1. 동일 위치·표준 치수 box의 내부 겹침96쌍.** 총 접촉 후보1782쌍은 별도 정밀 검사에서 face1304/edge424/corner54로 구분됐다. 기존 JSON의 `intended_face_contacts`는 이 접촉 후보 합계이므로 face 수1782로 해석하면 안 된다. 이들과 별도로 양의 부피 겹침96쌍이 있다. 모든 box axis는 world cardinal axis와 최대4.441e−16 오차만 있어 이96쌍은 회전된 OBB의 AABB false positive가 아니다.

예: Layer_01_A/Bundle_01_S/Brick_05와 Bundle_06_R/Brick_02의 overlap XYZ는 약(28.5,47.5,90.0)mm다. 이는 원래 slot frame에 표준 box를 놓으면 발생하며 위치 보존 검사도 PASS했다. 원래 HR mesh/native collider 자체가 같은 부피를 점유한다거나 기존 v21의 실제 접촉 실패였다고 단정하지 않는다. 두 static box의 내부 겹침이 live 접촉에서 무해하다는 증거도 없다. 따라서 동일300poses/동일치수/겹침0이라는 요구를 동시에 만족했다고 주장할 수 없다. 임의 축소·이동·collider 삭제나 실패 gate 완화는 하지 않았다.

**권고하는 다음 한정 offline 수정:** 300개 표준 box의 **외부 union envelope를 정확히 보존하는 공통 정적 union collider**를 좌표평면 분할로 겹치지 않는 cuboid cells로 생성하고, union 부피·외부 경계·rover/ground clearance가 원래300 box의 union과 같은지 검증한다. 렌더와300 slot은 그대로 둔다. 이는 “enabled box 정확히300개”를 바꾸는 별도 pilot-only physics 개정이므로 현재 overlay를 PASS로 바꾸지 않고, 새 artifact/새 DRAFT 조건으로 기록해야 한다. 이 bounded 단계가 끝나기 전 v24 Kit motion은 NO-GO다. 단순 내부 겹침을 무해하다고 간주하는 우회는 권하지 않는다.

**2. 공통 rolltainer Plane의 authored material binding 손실.** 활성 prim `/World/ENG_FE2E/Rover/base_link/MountedRolltainer/AssetRef/rolltainer_body/Plane`이 source의 `/World/Looks/OmniPBR`을 가리키지만 reference 범위를 벗어나 무시된다. 원본 rolltainer USD를 직접 열어 intended Material/Shader가 존재하고 diffuse texture가 `/home/jh/Downloads/rolltainer_stl/apriltag_100.png`인 것을 확인했다. 이 파일은 해당 경로에 없고 현재 assets root의 정확한 파일명 검색에서도 발견하지 못했다. 전체 파일시스템에 없다고 단정하지 않는다. 원래 이미지의 SHA는 UNKNOWN이다.

**다음 한정 복구:** 원래 AprilTag 이미지의 실제 파일/lineage를 회수해 SHA를 기록하고, derived 공통 material subtree에서 원래 `/World/Looks/OmniPBR`을 참조한 후 Plane을 그 local material로 bind한다. 원본 USD는 그대로 두고 세 행에 동일하게 적용한다. 원래 image를 임의의 새 tag로 대체하지 않는다. 원본 texture를 회수할 수 없다면 현 fallback appearance를 별도 protocol 조건으로 명시하고 실제 동일-view render admission으로 검증해야 하며 현재 정적 FAIL을 PASS로 바꾸지 않는다.

MDL 문제를 이론으로 무시하지 않았다. 설치 SDK의 실제 `kit/mdl/core/mdl/gltf/pbr.mdl`와 `kit/mdl/core/Base/OmniPBR.mdl`을 찾아 standalone resolver search path로 해석하고 SHA를 기록했다. 전자의 SHA는 `2c7c14d7bbf7cacea990f90e8ecc92700d8a7fe9805e44970096796e2be88b78`, 후자는 `685a82c18b381f1cd29831490e4c356e61dbeac2d86803babc115cd6a4a845db`다. 선택 brick의 활성 bound networks/texture는 실제 경로 해석 PASS다. 전체 dependency scan의 remote Grid/rolltainer texture/mitex texture 등 미해결 항목은 각 JSON에 그대로 남겼으며, 전부 활성 rendered dependency라고 단정하지 않았다. 실제 MDL compile·renderer 결과는 NOT_TESTED다.

## Pilot DRAFT 및 v24 최소 실행 계획

새 DRAFT는 정확히 HR/LR/GeoCAD, cement C100/FULL300/추가 occluder 없음/v21 site·start·seed·camera를 명시한다. estimand는 **representation + matched frozen M50 pipeline**이며 geometry-only 인과효과가 아니다. frozen FE2E_S001 exact replay도 아니다. v21 start/scene, assisted ROI, matched model/controller/stop verifier, common static load라는 변경을 선언하고 원래4rep108/432를 보존한다. occlusion 수준·효과크기·power·추가 표본계획은 만들지 않았다. cost missing은 그대로 missing이다.

두 blocker의 한정 offline 해결과 새 DRAFT 조건 고정 후에만 [runtime 계약](../docs/construction_site_pilot_runtime_contract_20261102_v23.md)의 v24 순서로 진행한다. 실제 live wrapper는 아직 없으며 가짜 실행 CLI를 제시하지 않는다. 작은 코드 연결은 session의 stage derive를 검증된 scene row로 받는 것과 HR 고정 worker의 rep/model/source metadata selector 두 곳이다. v21 rover/control/ROS/stop verifier를 다시 작성하지 않는다.

첫 bounded Kit는 HR **한 행만**: 먼저 실제 render/material과 PhysX static shape 등록/native0·consumer 가시성·support/settling/contact를 검사한다. 실패면 motion0/NO-GO와 모든 로그를 보존한다. 성공한 경우에만 fresh RGB-D→정확한 HR M50→B4/한 reviewer·한 번 time-limited ROI B5→새 목표→기존 PRE swept path/wheel support→normal stop/quiet→독립 FINAL admission/stop/quiet를 적용한다. exit/cleanup/독립 post-exit proof/PID 소멸 확인 전 다음 LR을 시작하지 않고, CAD도 같은 순서다. retry0. threshold·GID·TF·속도·steer·GC·timeout·zero/quiet 기준은 원본 계약 그대로다. GT는 perception goal/ROI 정답으로 쓰지 않는다.

## 검사·실패·보존 기록

최종 adapter/checker compile PASS, 실제72/72 SHA 및108/432 pairing/join PASS, 세 scene 각각21/23 정적 검사 PASS. read-only v23 checker는 cross-row identity PREPARE_PASS와 각 행 BLOCKED/exit2를 함께 반환했다. 모델 오매핑/scene hash 변조/Proxy 분석군/disabled collider/transform 변조/CLI Proxy·live 인자 거절 등 focused8/8 PASS. standalone 결과를 FULL READY/science PASS로 승격하지 않는다.

개발 중 최초 compile 괄호 오류, 설치 USD에 없는 `Stage.GetCompositionErrors` 호출로 HR_Scan_01 exit1, ancestor reference 혼합 발견 및 초기 비효율 triangle 검사 시도는 삭제하지 않았다. 개선 전 실행의 일부는 별도 output에서 끝까지 검사했고4회는600초 timeout으로 실패했다. 이들은 과학 관측이 아니고 최종 세 행 대신 사용하지 않는다. run별 실제 terminal/exit와 source snapshot 유무는 [개발 실행 inventory](construction_site_pilot_development_runs_20261102_v23.json)에 기록했다. Standalone 총11회 중 개발8회(API FAIL1, 600초 timeout FAIL4, 완료 BLOCKED3), 최종3회 모두 완료 BLOCKED/exit2다. 이전 wrapper가 timeout exit JSON을 남기지 못한4회에는 terminal에 관측된 TimeoutExpired/exit1을 별도 receipt와 final status로 추가 기록했다. 모든 소유 standalone worker는 종료됐고 기존 사용자 프로세스를 중지하지 않았다. 초기 snapshot 부재/작업 중 source 변경이 있었던 output은 최종 provenance로 채택하지 않았다. `git status`는 starter가 Git repo가 아니어서 실패했다. stage/commit/push/remote 변경은 없다. 탐색 중 잘못된 tail 다중파일 인자 오류도 연구시도가 아니다.

변경 파일: 새 v23 adapter·evidence checker·DRAFT/runtime 계약·manifest·검사/geometry/validation/개발 실행 inventory·이 보고서. `reports/latest_report.md`와 `docs/PROJECT_STATE.md`만 최신 상태를 갱신했다. 기존 source/USD/weights/locks/v19b–v21 raw 및 v20 FAIL0/2는 보존했다. Kit/ROS live/training/HPO/asset reconstruction/새 연구 관측0, formal denominator0. 다음 구체 작업은 위 union collider와 원래 Plane texture/binding을 **offline에서 한정 해결**하는 것이며, 현재 상태로 v24 주행을 시작하지 않는다.
