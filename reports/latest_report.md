# HR/LR/CAD 소규모 과학 파일럿 admission v22 — 2026-11-02

**현재 실행 readiness: 세 표현 모두 BLOCKED. Kit 실행 0, 과학 denominator 0, HPO/training PAUSED.** 실제 자산·동결 모델은 세 표현 모두 확보됐다. 막힌 것은 모델 부재가 아니라 **3표현/변경된 현장 제어·수동 ROI 정책의 명시적 개정과, 실제 300개 슬롯을 매핑하는 최소 adapter·공통 물리 overlay의 미구현**이다. 기존 v21을 또 반복하는 작업은 필요하지 않다.

산출물: [구체 후보 manifest](../manifests/construction_site_pilot_candidate_20261102_v22.json), [명령·adapter 계약](../docs/construction_site_pilot_commands_20261102_v22.md), [실행 가능한 offline checker](../scripts/construction_site_pilot_admission_20261102_v22.py), [실제 검사 결과](construction_site_pilot_admission_checks_20261102_v22.json), [scene/asset inventory](construction_site_scene_inventory_20261102_v22.json), [known locks](construction_site_known_locks_20261102_v22.json). 후보는 실행 가능한 검사를 제공하지만 미구현 live runner를 실행 가능하다고 표시하지 않는다.

## 1. 로컬 근거와 readiness

README, PROJECT_STATE 전체, PROTOCOL_LOCKS, 실제 prelock v01/amendment v02/v03/geometry v02, registry와 CSV, v21 소스·raw calibration/graph/corridor, 자산 characterization·cost benchmark를 읽었다. known 9개 SHA/count PASS. 별도 checker에서 **72개 unique 입력 파일 SHA 72/72 PASS**, base108/execution432/geometry108/432 uniqueness·4rep exact-set 및 모든 CSV 열 join PASS. geometry의 중복 열은 `_geometry`를 사용하므로 legacy task yaw0을 geometry yaw90으로 오독하지 않았다. geometry lock 자체 독립 expected SHA는 여전히 UNKNOWN; 이번 observed inventory를 과거 authoritative expected로 승격하지 않았다.

| 표현 | 실제 자산/모델 | 현재 현장 통합 | 판정 |
|---|---|---|---|
| HR_Scan | cement/red normalized USD·matched M50 SHA PASS | 현장 cement 300개 HR reference; v21 fresh RGB-D→실제 PRE/FINAL 완료 1회 | **BLOCKED**: 새 pilot 정책/overlay에 대한 HR 행은 미실행, HR 성공 재사용 불가 |
| LR_Scan | cement/red normalized USD·matched M50 SHA PASS | 원본 자산 존재; 현재 현장 슬롯은 HR 고정. LR 원본 collider0 | **BLOCKED**: 새 scene mapping/worker 인자·물리 통제 미구현 |
| GeoCAD (=CAD) | cement/red normalized USD·matched M50 SHA PASS | 원본 자산 존재; 현장 GeoCAD mapping 없음. 원본 collider0 | **BLOCKED**: LR과 같은 구현 gate |

v21 ENGINEERING_RECORDED와 독립 post-Kit proof는 [v21 보고서](construction_site_stop_lifecycle_20261101_v21.md)에 보존돼 있다. 새 corrected implementation **engineering 1/1**, historical v19b 성공, v20 **0/2 VERIFIED FAIL**은 별개다. 1/1은 일반 신뢰성·반복 성공률이 아니다. 이번 파일럿 수행수0, 정식 과학 분모0. 이전 engineering/실패를 새 과학 성능표에 넣거나 빼서 유리하게 만들지 않는다.

## 2. 실제 자산, 유래, 모델 및 비용

자산 root는 `/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/`이다. 실제 파일명은 `{cement,red}_brick_{HR_Scan,LR_Scan,GeoCAD,Proxy}.usd`이며 8개 전부 registry expected SHA와 일치한다. 전체 절대경로·SHA와 referenced source layer SHA는 inventory/manifest에 있다. 파일명 동일 source와 normalized wrapper를 경로 전체로 구분했다.

| 표현 | cement normalized SHA256 | red normalized SHA256 |
|---|---|---|
| HR | a3fbf6bd87d71007ae756a3288140d842d6e91135ee10d230a4ce52780d8f87c | 886a191cd74959dbb963206f3b173afee37a3b4e4e0159831bc48ab40fbabad4 |
| LR | 5781f72b71940938883f94a1325920a2a87ed768cba37a0000fa6fefd85256e1 | 9cf5d46621f5c8c1bc0ef76ac99584cdb0907008bab5ae8f290c4b2a359808e1 |
| CAD | e579f77f46debf05fca23d6bfc5c08217cc9541b3d932dee1088559cbef4699b | 104a55f4cd98c439ed3d7c739e13052c94056834dfd41ed3076803dd9e45020a |
| legacy Proxy | a86a29dd9cfe5fad48734df3f6f0fc91afaff628c0c0f08b4aa99f4a20e677be | 0750b615c32f242fb0031c0456b5251b42a53720c899e41bcf0999e890b694d8 |

HR은 높은 acquisition 입력의 재구성, LR은 reduced-resolution acquisition 입력을 같은 pipeline으로 **독립 재구성**한 것이다. HR mesh decimation이 아니다. `_asset_audit/brick_asset_characterization_FINAL_8ASSET_v03.csv`는 이 유래를 명시한다. LR source preprocessing benchmark에는 원영상 cement1280×720/30fps/1873frames/62.433초, red1234×720/30fps/2199frames/73.3초와 재현 LR640×360/5fps/313·367frames가 기록돼 있다. 이는 **입력 저감 재현 benchmark**이며 당시 독립 reconstruction 전체 로그나 원래 실제 human acquisition 비용의 대체물이 아니다. 원본 reconstruction tool/version·설정·측정자 노동시간의 완전 lineage는 이번 근거에서 UNKNOWN이다.

GeoCAD는 실측 치수 기반 script CAD이다. cement `build_geocad_v03.py`, red 최종 `rebuild_red_geocad_v06.py`; 오래된 red v03을 고르지 않는다. red에는 실제 구멍/홈 geometry가 있고 Proxy는 photographed face textures를 입힌 cuboid이다. CAD는 Proxy라는 이름 변경이 아니다. 다만 **GeoCAD composed layers가 Proxy USD를 appearance 의존성으로 참조**한다. Proxy를 분석군에서 제외해도 그 dependency 파일을 삭제/비활성화하면 안 된다.

동결 모델 root는 `/home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/`, 파일명 `FINAL_<representation>_M50_REALVAL_MASKBEST_v01.pt`이다.

| 표현 | matched checkpoint SHA256 |
|---|---|
| HR_Scan | 257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca |
| LR_Scan | d58e18a87f4cafba6fd92d8bade6e2ff12ad2380db427311b072859fd2cca42f |
| GeoCAD | bbfb9fc8d0c421154844f7e299b6d8162b9394eb07d36a31110f593c0813ce8f |
| legacy Proxy | 870cd7a66e7c26bc8fdab89df51a0a0ed04df53e7e68cf1f946c593dfcf7f74e |

prelock의 `perception_models_frozen`/`implementation_guardrails`는 representation-matched M50을 규정한다. 공통 HR 모델은 공정성 기본값이 아니다. 모델마다 mask/confidence/유효 depth·B4/B5·목표가 달라질 수 있고, 비교 대상은 **표현+해당 동결 인식 모델의 전체 전략**이다. 순수 geometry causal effect로 해석하지 않는다. 공유 모델을 비교하려면 별도 estimand/새 protocol이 필요하다. 새 HPO 최종 3weights는 준비됐다고 가정하지 않으며 이 pilot에 필요하지 않다.

공통 estimator는 `/home/user/eval_step25_pose_final_locked_v01.py` SHA `cc95b96c3305dcbe257a40fcf16f0e68a9e58ae0d5ae43f9cbd31e80ffec0988`, B4 Gated Top MinAreaRect/B5 Camera-Facing Side Fit, frozen gate .014116이다. v21의 v13 worker는 HR key·metadata를 hard-code하고 B5를 새 영상의 수동 pallet ROI 평면으로 보조한다. layer_count4와 seed261022도 명시적이다. 이 도움·prior를 전 표현 동일하게 선언해야 한다. GT pallet-top을 대신 넣지 않는다.

### 기록된 비용과 결측

| 항목 | 실제 기록 | 한계/결측 |
|---|---|---|
| HR/LR elapsed | characterization: HR120분/LR30분, 두 재료 모두 APPROX_REPORTED | timed compute가 아니며 active/passive 모두 PENDING |
| acquisition workload | 원영상 해상도/fps/frames/길이/크기/SHA, LR 저감 비율·preprocessing wall/CPU | 실제 촬영 준비·재촬영·사람 분·재구성 원 run 로그 미확보 |
| CAD 재현 compute | GeoCAD benchmark 3회/재료: cement wall평균 .898590초, red .898861초; CPU·geometry_match 기록 | 실측·스크립트 작성·수정·appearance 노동시간 아님 |
| geometry/size | cement HR512696/LR468612/CAD12 triangles; red HR623272/LR613600/CAD972 | polygon 수만으로 fidelity 순위/정확도 결론 불가 |
| dependency footprint | cement HR37.770/LR33.264/CAD8.928MiB, red HR43.212/LR42.122/CAD5.245MiB | wrapper 약 .001MiB만 비용으로 쓰지 않음; shared dependency 중복과 tex payload 구분 |
| fidelity/physics | size/pivot PASS, texture resolution/payload·mesh/material 수 기록 | scan-to-real 오차/동일 view render fidelity 정량 점수·전체 renderer closure UNKNOWN |

CAD 노동시간·HR/LR active/passive compute가 누락됐다고 0으로 채우지 않는다. 기존 비용을 reference로 붙이고 파일럿에서는 새 capture/inference/B4/B5/planning/verification/전체 wall·sim·RSS·review 시간을 측정한다. 비용 결측은 파일럿 launch blocker가 아니라 향후 cost–performance 결론 제한이다.

## 3. 최소 paired matrix와 실제 불일치

질문은 “동일 v21 controller·독립 verifier와 동일한 관측/도움 규칙을 실제 HR/LR/CAD에 적용할 수 있는가?”이다. 최소 **한 base × 세 표현, 각 1 planned execution**, 반복·검정력·성능 우열/동등성 검정은 제안하지 않는다.

| 새 실행 ID suffix | material/completeness/occlusion | scene/seed/start | 변화 |
|---|---|---|---|
| HR_Scan | cement/C100 300개 4층/FULL, 추가 occluder 없음 | 공통 site,261022, XY(−25.88797768,27.4), yaw90° | 실제 HR asset+HR M50 |
| LR_Scan | 동일 | 동일 | 실제 LR asset+LR M50 |
| GeoCAD | 동일 | 동일 | 실제 CAD asset+CAD M50 |

base ID `PILOT_SITE_CEMENT_C100_CLEAR_20261102_v22`; 각 output 절대경로/300개 prim 경로는 manifest에 열거했다. 아직 디렉터리를 만들지 않았다. 고정 순서 HR→LR→CAD는 feasibility용이며 order bias를 성능 효과와 혼동하지 않는다. 이후 본 연구 representation×load completeness×occlusion으로 확대하려면 별도 수준·분석 잠금이 필요하다.

기존 frozen nominal/unobstructed 대응 근거는 `FE2E_S001`이다: cement/C100/FULL/300/Near1.5m/Frontal0/Nominal/seed2379027709, geometry v02 start(−25.88797768,28.4708691133), target(−25.888,30.509), yaw90°. 이 행은 confirmatory membership=true이므로 새 pilot ID에서 성능 자료로 소모하지 않는다. **v21 start Y27.4, seed261022, site 조명은 S001과 다르다.** v21 actual camera Y27.939685994이므로 target XY거리 약2.5693m이며 frozen Near1.5나 Mid2.5와 동일하지 않다. 그러므로 이 제안은 기존 현장 nominal fixture의 **새 paired 파생 pilot**이며 frozen S001 exact replay가 아니다. 일반화 범위는 cement 한 조건뿐이다.

available C100/C60/C20·FULL/T01–T05·paired seeds는 locked CSV에 존재한다. 생산 source `/home/user/nonideal_depletion_b2b_production_rgb_v01.py`와 registry mapping, frozen depletion membership은 확인했지만 v21 worker는 layer_count4/현장 full fixture만 지원한다. 기존 manifests에는 completeness/distance/view/lighting이 있고 **독립 occlusion factor/가림률 수준은 없다**. 추가 occluder 없음과 self-occlusion0은 다른 말이다. 모든 표현에서 실제 가시율은 posthoc 측정, self-occlusion 차이는 표현의 관측 효과로 기록한다. C60/C20이나 occlusion 확장을 현재 실행 가능하다고 표시하지 않는다.

standalone USD 합성 검사로 현장 `/World/ENG_FE2E/Fixture/ActualBrickLoad`의 HR AssetRef300, 사용 layer25를 확인했다. source stage는 `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v02/stage_metrics_1m_z.usda`; lit/runtime-fixed layer를 거쳐 기존 DEMO fixture를 참조한다. fixture root transform은 회전90°/translation(−25.888,30.509,.00121562)이다. native 인스턴스 내부 collider는300개다. plain Traverse에서0을 반환하는 것은 instance proxy 미포함 때문이며 물리 collider 없음으로 결론 내리지 않았다. source asset은 cement HR collider1, 나머지7 asset collider0이다.

따라서 **참조만 바꾸는 native scene은 공통 physics가 아니다.** geometry 크기 정규화가 collider·mass·settling 동등성을 보장하지 않는다. 권고안은 pilot-only 새 overlay에서 세 표현 모두 native brick rigid/collision을 끄고 기존300슬롯·190×90×57mm canonical 정적 box와 보수적 exclusion envelope를 공통 적용하는 것이다. scene/rover/원본 asset은 손대지 않는다. 이는 material contact·적재물 동역학을 평가하지 않는 **고정 적재물의 인식→비접촉 접근** 비교로 한정한다. 형상을 억지로 동일하다고 주장하지 않고, visible scan/CAD geometry·texture는 그대로 둔다. 이 변경은 아직 미승인/미구현이며 safety 서명과 명시적 개정 없이는 실행 금지다. native 물리까지 연구하려면 그것을 표현 전략의 일부로 유지한 별도 설계가 필요하다.

## 4. 관측·제어·정지·기록 계약

[명령 guide](../docs/construction_site_pilot_commands_20261102_v22.md)에 adapter의 구체 patch 지점·frame convention·ROI·timeout·원시 artifact·lifecycle을 적었다. fresh mounted 640×480 RGB+distance_to_image_plane depth 한 render product, 매 실행 실제 calibration/optical transform, 단일 inference, matched M50/B4/B5를 사용한다. fx=fy317.0431201195는 실제 v21 reference이며 새 T_world_optical을 복사하지 않는다. PRE/FINAL은 새 B5 중심에서 공통 offset2.2037450313/1.4037450313m, task yaw90/local−X로 생성한다. B4는 기록용 heading이며 task axis를 회전시키지 않는다. USD GT는 sensor pose calibration·안전 map의 허용 role과 posthoc evaluation에만 식별하여 쓰고 B5 center·ROI·controller goal 정답으로 주지 않는다.

manual ROI는 **명시적 human-assisted/nonautonomous**이다. 세 표현에 동일 reviewer/익명 image code/한 번 polygon 제출/시간 제한, GT·모델명·이전 ROI·성공 결과 비공개, 실제 새 RGB와 overlay SHA 결합 검토를 요구한다. 외관으로 표현이 짐작되는 blind 한계는 기록한다. 미검출/ROI 실패 시 더 많은 도움·재시도·threshold 변경을 허용하지 않는다.

v21 graph/publisher/GID/TF, rear-reference follower와 base_link evaluation의 구분, 원래 collision/support/path/speed·steering·memory/GC bounds, PRE stop 후 독립 FINAL admission, 실제 wire replay·physics stop verifier를 모두 유지한다. **engineering trigger3mm, endpoint5mm/2°, quiet≥1초**는 perception target 도달 인증이다. 이를 canonical task success threshold로 바꾸지 않는다. canonical GT posthoc main11cm/7.3417743229°, strict5.5cm/3.6860176256°, relaxed16.5cm/10.938473748°는 기존 정의 그대로 별도 보고한다. GT 중심에 대해 잘못 생성된 목표에 정확히 정지할 수 있으므로 두 결과는 반드시 나눈다.

pilot 출력은 다음과 같다.

- 단계별 capture/calibration·detection(confidence/mask/depth count)·B4 validity/heading·B5 validity/center·target generation·route admission 결과와 최초 실패원인.
- B4 modulo180 heading error, B5 XY·longitudinal/lateral 오차를 **GT posthoc 전용**으로 측정. invalid pose는 결측 원인과 함께 남기고 유효표본에서만 구한 평균을 전체 성능처럼 표시하지 않음.
- PRE/FINAL 각각 실제 이동·base_link endpoint 거리/yaw·wire zero/quiet·certificate, canonical terminal error와 기존 세 task bands.
- unexpected contact·침투/하중·안전 fault·timeout·TF/GID/graph fault·강제종료·exit code·독립 attestation 결과.
- 단계/전체 wall와 sim 시간, inference/pose/계획/검증 비용, reviewer active time, RSS 및 기존 asset 제작비 reference/결측.

예정행3/실제시도수/검증완료수/성공수를 함께 보고한다. detection/pose/ROI/target/route rejection/물리 미도달/접촉은 task failure; sensor bootstrap/process crash·증거 hash/독립 certificate 누락·외부 verifier/exit 실패는 infrastructure/attestation failure로 별도 표시한다. 동시에 발생하면 두 flag를 보존한다. **시작된 모든 행은 전체 시도 분모에 남고**, 인프라 실패를 지워 성공률을 높이지 않는다. 시작 전 BLOCKED는 미시도로 별도 집계한다. 타당한 inference가 있었더라도 attestation 실패를 VERIFIED success로 세지 않는다. 파일럿은 정식 confirmatory 분모에 합치지 않는다.

## 5. 3 대 4 개정 권고 — 기존 잠금 변경 없음

10월29일 요청을 기록한 [three_rep_hpo_start 보고서](three_rep_hpo_start_20261029_v01.md)와 PROJECT_STATE의 “향후 HR/LR/GeoCAD, Proxy 제외”가 확인됐다. 이 후의 4rep 언급은 frozen protocol 기록이며 이를 뒤집는 새로운 4rep 연구 결정 근거는 찾지 못했다. **의도된 후보는 HR/LR/CAD**다. 다만 이 결정이 Full E2E frozen matrix에 이미 반영됐다는 뜻은 아니다.

권고: 다음 미사용 artifact 번호로 별도 pilot amendment를 작성하고 parent SHA를 명시한다. `v04`라는 전역 버전 하나를 모든 artifact에 강제로 붙이지 않는다. 아래는 제안이며 이번에 어떤 lock도 갱신하지 않았다.

| 영향 artifact/section | 필요한 versioned 변경 |
|---|---|
| prelock `confirmatory_design`/representation factor·pairing·confirmatory count, `perception_models_frozen`, `analysis_precommitment`, `implementation_guardrails` | 후보3rep/matched 모델/추론·도움·실패정책 명시; pilot namespace와 정식 matrix 분리 |
| amendment v03 `scientific_factors_unchanged`/`representation_runs`/primary model 및 task-policy 관련 기존 controller 규정 | 더는 unchanged라 부르지 않음. v21 follower/stop verifier, 현장 start/조명·수동ROI·공통 정적 물리 정책을 pilot 범위로 명시 |
| scenario_manifest_v01 execution432 + SCENARIO_MANIFEST_LOCK | 새 3rep 실행행렬·행수·SHA·pairing exact-set; 기존432 불변. base108을 재사용한다면 membership/seed 그대로 parent 참조 |
| initial_geometry_v02 geometry432 + INITIAL_GEOMETRY_LOCK | 새 실행 geometry join/metadata 및 pilot 고유 geometry/start 정의. geometry108/workspace는 같을 때만 hash 참조; 바뀌면 각각 새 버전 |
| asset registry/model mapping 및 downstream config/runner/results schema | execution eligibility3rep와 appearance dependency 구분. 8asset 원본 registry는 그대로 보존 가능; 새 pilot mapping만 별도 생성 |
| 연구 method/results/analysis contrast·표·비용 항목 | 연구 대상3rep·representation+matched model estimand·human assistance·physics/분모·과거4rep 연구와 구분 |

세 표현으로 base108을 그대로 유지하면 수학적으로324행이지만 **324 설계를 승인·생성·실행한 것은 아니다**. 추후 completeness×occlusion 새 축은 기존 distance/view interaction 계획과 다르므로 별도 방법론 개정 대상이다. 이번 목적을 큰 행렬/검정력 결정으로 확장하지 않는다. 접근 가능한 `Downloads/TOC 수정본.docx`는 EUI/건물용도 연구 목차여서 본 연구 method/results 근거가 아니었다. 관련 최신 논문 원고는 확인하지 못했다. starter에 기록된 Real Test189는 recipe locking 뒤 이미 평가됐으며 미개봉이라 하지 않고 tuning에 사용하지 않았다. 실제 외부 검증 red-only를 cement/실로봇 배포로 일반화하지 않는다.

## 6. 진짜 blocker와 다음 단일 작업

1. **문서 gate:** 3rep 후보, v21 controller/현재 start·수동 ROI·matched M50·pilot-only 공통 정적 physics를 parent locks와 구분한 좁은 서면 amendment가 필요하다. 이는 기존 사용자3rep 의도를 다시 묻기 위한 gate가 아니라 기존 잠금과 달라지는 실행 조건을 구체적으로 남기는 gate다.
2. **작은 실행 adapter gate:** 300개 실제 slot reference 교체와 공통 물리 overlay, representation 인자 worker, 동일 reviewer 규칙·per-run raw/status를 연결하고 standalone USD에서 slot/transform/활성 재질·collider·graph·camera/safety를 비교해야 한다. Kit/학습 없이 할 수 있는 다음 구현이다. HR/LR/CAD 세 행 모두 같은 새 adapter를 써야 한다.

**다음 단일 action:** 위 두 조건을 한 번에 검토할 수 있도록 *pilot-only amendment + 최소 parameterized adapter/derived overlay의 prepare-only 산출물*을 새 버전으로 구현·검사한다. 그 static admission이 통과한 뒤 별도 허용된 작은 파일럿으로 전환한다. 이번에는 Kit 승인 요청이나 이전 v21 주행 재시도를 하지 않았다. 새 자산/학습/HPO를 준비하는 것은 다음 action이 아니다.

inactive texture reference 자체는 blocker로 넣지 않았다. 전체 renderer closure는 UNKNOWN이지만 v21 HR은 실제 렌더/인식 성공했다. LR/CAD의 활성 material binding·texture closure는 prepare-only에서 어떤 visible prim에 연결되는지 확인할 대상이다. 빠진 경로가 현재 활성 rendering에 영향을 주는 증거가 있을 때만 해당 행을 차단한다. Proxy appearance 의존성은 보존한다.

## 7. 검사·실패 기록·변경 파일

PASS: checker AST와 정상 BLOCKED·변조 hash/누락 input 거절을 CPU로 확인했다（`construction_site_pilot_checker_validation_20261102_v22.json`）。known9 subset, 입력72 SHA, 108/432 four-rep pairing 및 geometry 모든 열 join; standalone USD scene300 refs/instance collider300 및 자산8개 확인. CPU checker가 **12개 미구현 runtime contract로 BLOCKED/exit2** 반환하는 것은 예상 admission 거절이다. 런타임/과학 readiness PASS가 아니다.

탐색 중 nonexistent scene-provider/glob 조회 exit2, 넓은 파일명 검색의 Documents permission denied, standalone USD 첫 인라인 코드 괄호 오류 exit1은 있었다. 기존 파일은 수정하지 않았고 잘못된 인라인 코드를 수정한 뒤 standalone read-only 합성을 완료했다. plain traversal collider0의 제한은 inventory에 보존하고 instance-proxy300 결과로 명시했다. 이것들은 Kit/과학 시도가 아니다. 관련 논문 파일명 검색은 exhaustive filesystem 권한 인증이 아니다.

신규: 본 보고서, candidate manifest, command guide, stdlib checker, known-lock/scene/admission/checker 검증 JSON. 갱신: `reports/latest_report.md`, `docs/PROJECT_STATE.md`. source USD·weights·원본 rover/scene·모든 frozen scientific manifests/locks·v19/v20/v21 code/raw/snapshots는 수정하지 않았다. package 설치/학습/Kit/ROS/process 종료/Git stage·push0. **engineering corrected 1/1, science denominator0 유지.**
