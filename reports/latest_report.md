# Construction-site pilot v24 — 두 prepare blocker의 한정 오프라인 해결

2026-11-02. **세 행 모두 STATIC_PREPARE_PASS / LIVE_RENDER_PHYSX_NOT_TESTED / SCIENCE_HOLD**. 원래 현장·rover·camera·ROS graph·300 visual slot/transform·선택 HR/LR/GeoCAD geometry와 matched M50는 보존했다. Kit/ROS/live render/주행/학습/HPO/과학 관측0, formal science denominator0. 과거 v21 성공을 새 관측으로 재사용하지 않았다.

| 표현 | 정적 준비 | Live | 연구 상태 | 행별 오프라인 시간 |
|---|---|---|---|---|
| HR_Scan | STATIC_PREPARE_PASS (19/19) | LIVE_RENDER_PHYSX_NOT_TESTED | SCIENCE_HOLD | 15.34s |
| LR_Scan | STATIC_PREPARE_PASS (19/19) | LIVE_RENDER_PHYSX_NOT_TESTED | SCIENCE_HOLD | 9.92s |
| GeoCAD | STATIC_PREPARE_PASS (19/19) | LIVE_RENDER_PHYSX_NOT_TESTED | SCIENCE_HOLD | 11.45s |

최종 출력 root: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03`. 총 prepare 38.10초, 전체 subprocess 상한180초. [실제 경로·전체 SHA manifest](../manifests/construction_site_pilot_prepare_20261102_v24.json), [독립 검사](construction_site_pilot_prepare_checks_20261102_v24.json), [CPU/CLI·실패 기록](construction_site_pilot_validation_20261102_v24.json). manifest는 외부 root의 실제 manifest.json과 byte-identical이다.

원래 source/기존 v23 USD/잠금/weights는 덮어쓰지 않았다. v23 overlay를 sublayer로 삼는 새 USD 세 개를 만들었다. 원본 v21 runtime snapshot은 정적으로 읽었고 SimulationApp 시작 부분을 확인했으며 import/실행하지 않았다. v23 부모 checker의 실제 입력 SHA와 cross-row signature를 재검증했고 두 기존 blocker 외 실패가 없음을 확인했다. 각 행의 v23 dependency layers·v21 baseline·MDL·자산·모델 SHA도 재확인했다. 독립 expected가 없던 geometry lock 자체 인증은 여전히 UNKNOWN이며 observed SHA를 expected로 바꾸지 않았다. frozen4rep108/432 membership/pairing/seed/metric/threshold는 그대로다.

## A. 공통 union collider

원래300 box의 composed world matrix와 bounds가 v23 증거와 정확히 같은지 확인했다. 최대 cardinal-axis 오차 4.44e-16: 기존96쌍의 양의부피 겹침은 AABB 오탐이 아니다. visual brick을 삭제하거나 slot을 이동하지 않았고 collision pair filtering도 추가하지 않았다. 기존300 collider만 새 layer에서 inactive로 만들고 `/World/PilotStaticUnion_v24/Cell_0000`부터 동일한 정적 cells를 author했다. CollisionAPI enabled=true, RigidBodyAPI 없음, 선택 visual native enabled collision/rigid0이다. guide purpose는 collision을 끄는 수단이 아니다.

원래 floating point endpoint를 그대로 보존하는 **102셀 완전 동일 분해**도 `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/exact_float_union_reference.json`에 실제 생성했다. 독립49×63×7=21,609 plane-cell 검사에서 missing0/extra0, 외부 경계 XYZ 정확 일치, 부피0.28129842034715324m³, 최대 coverage1이다. 다만40셀이1µm 미만의 수치 슬리버이고 최단 edge는 약3.55e−15m였다. 이를 실제 물리 후보로 내보내지 않았다.

최종 후보는 **수치허용 내 동일 union의28셀**이다. deterministic endpoint clustering 상한10nm 중 실제 최대변위 **3.5762787176e−9m**이며, 원래 visual/slot transform에는 정규화를 적용하지 않는다. 최단 cell edge는28.499998793mm다. 원래 부피와 후보를 다시 독립 구간 비교한 실제 값은 다음과 같다.

| 검사 | 실제값 | 판단 |
|---|---:|---|
| 원래 union 부피 | 0.28129842034715324m³ | 기준 |
| 후보 union 부피 | 0.2812984218292283m³ | 수치허용 내 |
| 원래 union 중 후보 누락 | 6.2163435132e−10m³ | <1e−8m³ |
| 후보의 추가 부피 | 2.1037093710e−9m³ | <1e−8m³ |
| endpoint 경계 변위 | 3.5762787176e−9m | <1e−7m |
| 정규화 기준 missing/extra | 0 / 0 | PASS |
| 정규화 외부 경계 XYZ | 모두 정확 일치 | PASS |
| 후보 pairwise positive-volume overlap | 0 | PASS |

**raw 좌표에 대한 strict bitwise union/boundary equality는 false**이며 JSON의 해당 `pass:false`를 감추지 않았다. 이는 위 미소한 부피차·경계 변위를 뜻한다. 정확한 raw102셀 증거와 최종 수치허용28셀을 구분한다. 단순 overlap0으로 union을 인증하지 않았으며, 정규화 기준27×31×4=3,348 elementary cell 전체 coverage/외부 경계와 원래 좌표 기준21,609 cell의 양방향 부피차를 독립 검사했다. 원래 bound 기반의 과도하게 보수적인 오차상한7.09e−8m³도 기록했지만, 최종 판정은 이 상한 대신 실제 양방향 구간 적분값을 사용했다. 길이/부피 허용값은 실패 후 넓히지 않았다.

합집합 sweep은 약 0.0027초, x/y plane budget100,000·raw cells50,000·최종 cells3,000·sweep15초·독립 grid2,000,000 cells 상한을 둔다. 반복 merge로 인접 cells를 합친다. 실제 standalone에서 재개방한 cube bounds의 오차도1e−12m 미만이다. 동일 shape parameter SHA256은 `83dea433c5c3683f7faa536bd0dba2ddc5b3256b98eadd51eec79cc156547a03`. 세 행의 world cells·common scene signature·rolltainer fallback signature가 같다. 의도한 tolerance 기준 접촉은 face55/edge0/corner12로, 양의부피 겹침과 구분한다.

rover 시작 clearance와 pallet/ground/fixture surface 검사는 **hash-bound v23 SAT 결과 + union 집합 동등성 + 환경 불변**으로 이전했다. 전체382,994면 triangle loop를 반복하지 않았다. 새 허용오차는 기존 SAT의1e−7m 범위 안이다. 이는 오프라인 기하 clearance 보존 증거이며 실제 contact offset/shape cooking/내부 seam/하중/settling/wheel support 검증은 아니다. common collision은 fixed-load environmental support이며 native 적재동역학·material-contact 성능 주장을 금지한다.

## B. 공통 Plane fallback

[source 탐색 기록](construction_site_pilot_texture_search_20261102_v24.json): 알려진 assets/sdg_practice/sdg_final, depth8/12초/12,000directories/300,000files 예산으로 exact `apriltag_100.png`만 찾았다. 3,589dirs/301,431files를 읽고 file guard에 도달했다(한 directory 단위 집계로 소폭 초과), 발견0, 권한오류0. 전체 home에 없다고 주장하지 않는다. 원래 `/home/jh/Downloads/rolltainer_stl/apriltag_100.png`의 authentic image SHA·lineage는 **UNKNOWN**이다.

원래 rolltainer USD `/home/user/hh/isaac_cosmos/assets/assets/robot/rolltainer.usd` SHA `10c7df3e512e927d4d57dba475efa239522490e5d177aa88c958d0ca10d92bd5`를 검증했다. source `/World/Looks/OmniPBR`과 shader 전체 authored properties, Plane 원래 binding 및 file SHA를 `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/rolltainer_source_evidence.json`에 기록했다. reference 범위 밖 관계와 누락 image를 원래대로 복원했다고 주장하지 않는다.

세 overlay 모두 Plane `/World/ENG_FE2E/Rover/base_link/MountedRolltainer/AssetRef/rolltainer_body/Plane`을 버전 subtree `/World/PilotLooks_v24/CommonRolltainerFallback`에 직접 bind한다. **COMMON CONTROLLED FALLBACK**: `UsdPreviewSurface`, diffuseColor(.5,.5,.5), roughness.8, metallic0, texture inputs0. AprilTag를 합성하지 않았다. 원래 외관과 동등하다는 주장은 없다. 실제 composed standalone binding/output/shader가 해석되고 dangling Plane relationship은 없다. Plane geometry와 다른 활성 material binding·shader properties·texture/MDL input은 그대로다. brick 및 공통 현장 active material dependency 해결 PASS, CAD의 Proxy appearance 참조 유지 PASS. 설치 MDL search path와 실제 파일 SHA는 부모 증거와 재대조했다. 기존 steer-link의 MaterialBindingAPI 미적용 warning은 보존했고, 해당 binding은 해석됐다.

현재 renderer에서 texture가 보인다는 증거는 없다. source 안의 inactive/unbound missing texture나 remote reference를 active dependency와 혼동하지 않았으며 원래 관계·경로는 source에 남아 있다. fallback이 ROI/segmentation에 미치는 영향은 다음 실제 이미지 검토 전 UNKNOWN이다.

## 실제 산출물·검사

- HR_Scan: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/HR_Scan/pilot_scene.usda`
  SHA256 `5b928d33d614c1328d3df87a66ea188844711f6b5bf6661e0f4c40a5f24cb0b4`. 상세 검사: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/HR_Scan/prepare_check.json`.
- LR_Scan: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/LR_Scan/pilot_scene.usda`
  SHA256 `f652f4cd1db46a661adf1431cdce538562b0cef14e2019b3a2a4b2b8f970c60d`. 상세 검사: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/LR_Scan/prepare_check.json`.
- GeoCAD: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/GeoCAD/pilot_scene.usda`
  SHA256 `d806cc64179dbbe6f394bf2d05b7a13be0500375d193505b04a90a0cbe448826`. 상세 검사: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03/GeoCAD/prepare_check.json`.

최종 adapter: [v24b](../scripts/construction_site_pilot_prepare_20261102_v24b.py). 초기 실패 구현 [v24](../scripts/construction_site_pilot_prepare_20261102_v24.py)도 보존한다. [별도 checker](../analysis/construction_site_pilot_evidence_check_20261102_v24.py)는 scene/check/source/assets/models/parents 및 실제 활성 asset SHA를 검증하고 세 composed stage를 직접 다시 연다. 부모 layer hash와 새 layer 전체 authored-spec whitelist로 선택 visual·다른 scene property 보존을 증명한다. 대형 mesh arrays를 문자열로 반복 비교하지 않는다. 각행300slot/world transform/선택 reference/no mixed branch/native0/static28/Plane binding/fallback/union을 재확인했다.

실제 prepare19/19×3 PASS, 별도 composed check3/3 PASS, 변조거절12/12 PASS: cell 누락/비활성/이동, dangling Plane, fallback색 변경, visual 자산 오매핑, model 오매핑, scene SHA 변조, Proxy 분석행, 독립 union의 hole/중복overlap/추가부피. prepare CLI의 live `--run`과 Proxy 인자도 각각 exit2 거절, output 미생성. AST/compile PASS. legacy simulation/omni/Kit/ROS/model module import0이다. 오프라인 검증에는 NumPy와 pxr를 사용했다.

최종 실행 명령(오프라인 전용, 같은 output 재사용 금지):
```bash
python scripts/construction_site_pilot_prepare_20261102_v24b.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_PREPARE_20261102_v24_03
```
이미 완료된 명령의 receipt이며 재실행 지시가 아니다. 설치 Isaac5.1 env Python + omni.usd.libs standalone PYTHONPATH/LD_LIBRARY_PATH, 실제 command/USD version/source snapshot/exit는 output에 기록했다. regular conda Python으로 Kit를 실행하지 않았다. 별도 checker120초 상한/exit0, prepare180초 상한/exit0.

실패는 보존했다. `_v24_01`은 정규화의 보수적 부피 오차상한 guard에서 exit1로 중단했고 scene을 만들지 않았다. `_v24_02`는 raw102셀 exact proof와 HR USD까지 만들었으나 대형 mesh 배열 문자열 반복 비교로180초 timeout/exit124였다. root exit와 HR failure receipt를 남겼으며 해당 partial output은 후보가 아니다. `_v24_03`에서 불변 parent+전체 delta whitelist로 불필요한 대형 배열 반복을 제거하고, 실제 구간 적분으로 원래 tolerance 충족을 검증했다. 세 attempt의 소스 snapshot/실패/exit를 validation JSON에 보존했다. 실패를 denominator에서 삭제하거나 successful science run으로 세지 않는다. 기존 사용자 프로세스는 중지하지 않았고 자기 bounded subprocess는 반환했다.

[PILOT-ONLY DRAFT](../docs/construction_site_pilot_amendment_DRAFT_20261102_v24.md)는 부모 DRAFT SHA, union28/수치허용 조건과 fallback을 명시한다. 비교는 사용자 선택 HR/LR/GeoCAD의새3행이며 historical locked4rep를 개정하지 않았다. [v25 계약](../docs/construction_site_pilot_runtime_contract_20261102_v24.md)은 v23의 observation·v21 stop/TF/GID/GC/contact/timeout/retry0 정책을 유지한다.

## 다음 별도 v25 실행 단위

**HR 한 bounded live admission을 먼저** 준비한다. 아직 live wrapper CLI는 없고 v24 adapter는 launch를 지원하지 않는다. v21 runner를 그대로 재실행하면 새 stage가 무시되므로 실행하면 안 된다. 다음 구현은 verified v24 HR scene을 fresh run sublayer로 연결하고 worker에 matched HR M50/asset metadata를 전달하는 최소 연결 및 CPU 거절 검사다. Physics inventory/safety consumer는 이전 slot collider300 대신 **`/World/PilotStaticUnion_v24`의28개**를 실제로 포괄해야 하며 기존 contact 정책을 완화해서 통과시키지 않는다.

이어 한 HR session에서 먼저 motion0 상태 render/material/ROI·segmentation 검토, 실제 PhysX shape28/nativebrick0 및 safety consumer coverage·union seam/contact·rover/pallet/ground·wheel support/settling을 확인한다. 문제면 NO-GO/motion0/실패·cleanup 보존. 안전 gate가 통과한 경우에만 새 RGB-D/calibration→matched HR YOLO/M50→B4/한 reviewer 한 번 ROI B5→fresh PRE sweep/support·physical normal stop/quiet→독립 FINAL admission/sweep/support·stop/quiet를 실행한다. frozen pose CSV는 관측 대체 금지, GT는 평가/허용 calibration/safety 역할로만 식별한다.

독립 stop proof/zero readback/TF·GID·GC·contact 정책과 post-exit cleanup·PID 소멸이 확인된 clean HR exit 이후에도 LR, CAD는 각각 별도 authorization으로 한 행씩 실행한다. 매행 fresh RGB-D·ROI·matched model을 사용하고 retry0. 이 v24에서는 이 live 절차를 실행하지 않았다. HPO/training PAUSED,324/432 시작0,formal denominator0.

변경 파일: 신규 v24/v24b adapter·v24 checker·DRAFT·runtime contract·manifest·prepare checks·validation·texture-search·이 보고서, `reports/latest_report.md`, `docs/PROJECT_STATE.md`. bulk USD/상세 geometry/material inventory/로그는 위 외부 output에만 있다. 원본 locks/science artifacts/v23/source USD/weights는 보존했고 publish/push/install/upgrade0이다. 최종 미해결은 authentic 원본 texture lineage와 실제 renderer/PhysX/support/vision/주행 admission이며 정적 PASS와 구분한다.
