# 기존 USDZ 환경4종 실제 시각화 및 대체 가능성 검토

2026-11-03 KST. **네 에셋 모두 현재 PC의 Isaac Sim5.1에서 실제로 렌더링됐다. 그러나 네 파일 모두 Mesh/Collider가0개라 지금 상태로 물리 주행 환경을 대체할 수는 없다.** 우선 검토 추천은 **B1_CLOSED_EV**, 등급은 **B(조건부 대체 가능)**다. 넓은 통로·공사 구획·기둥·자재가 실제 이미지에서 관측된다는 근거이며, 주행 공간·작업 성공·권리 허가가 인증됐다는 뜻은 아니다.

## 1. 실행 범위와 실제 산출물

- 원본 경로: `/home/user/hh/isaac_cosmos/assets/assets/environment/`.
- 정적 Kit 2세션, 에셋4×(첫6시점+보완12시점)=**72장**, 별도 Mesh 렌더 대조군2장, 총74개960×600 PNG를 저장·decode 확인했다. 4개 비교패널2장과 환경별6시점패널도 만들었다.
- 기존 연구 Stage를 열어 바꾸지 않았다. 각 에셋은 **새 anonymous Stage의 subLayer**로 읽고 새 SessionLayer에 카메라/조명만 추가했다. USD 저장0, 로버 삽입/주행0, 팔레트 삽입0, Physics play0, ROS0, YOLO 추론/학습0, 기존 연구 재실행0이다.
- 원본5개USDZ+PROJECT_STATE+기존출처보고서 총7파일 시작/종료SHA 불변PASS. 기존 연구 코드·기존 결과를 수정하지 않았다. PROJECT_STATE와 latest_report도 갱신하지 않았다.
- 실제 실행/카메라transform·시점별품질·설정·종료코드는 companion 폴더의 `run_manifest.json`, `capture_results.json`, `detail_capture_v02/capture_results.json`, `session_events.jsonl`, `kit_stdout.log`, `process_exit.json`에 있다.

| 환경 | bytes | SHA256 |
|---|---|---|
| 5F_CLOSED_EV | 86326118 | `892ca7c846bbf2b48399176350185a50fb95bee8997fc1ec57ae50337c822b81` |
| 5F_OPEN_EV | 129619954 | `e597ce4c9af6f1c41f9f9c0a8cbc5d3145cc02ea9266d36ebf9557768c873dca` |
| B1_CLOSED_EV | 271964190 | `de908a9e91ab433556db57d2e584422801a3e93f3d469b6bf2c324ecb9e0586d` |
| Jeonju_122151 | 286042665 | `618d0e3d2587ab2f4f0f42cc24e0db46fcf848026b1285832c50157737aea611` |

## 2. 네 환경 대표 비교 이미지

아래는 **각 원본 NuRec에서 실제로 렌더링한 이미지**다. 생성형 이미지·다른 배경·가짜 바닥으로 대체하지 않았다.

![4개 환경 로봇 높이 후보 비교](alternative_environment_asset_review_20261103_v01/four_environment_comparison.png)

카메라는 원본 좌표(0,0,z=.65m)에 배치하고 방향을 달리했다. z=.65는 대략적인 낮은 카메라 시점용 설정이다. **원본 바닥 높이를 독립 측정하지 않았으므로 실제 지면에서 .65m라는 metrology 인증은 아니다.** 기존 로버 카메라의 정확한 mount/extrinsics를 이식한 실험도 아니다. 8방향 및z1.5m 보완뷰를 모두 보존했다.

![4개 전체 crop 조감도](alternative_environment_asset_review_20261103_v01/four_environment_overviews.png)

전체 조감도는 원본 neural crop bounding box에 맞춰 잡았다. 큰 외곽 범위·빈 공간 때문에 유효 재구성 부분이 작게 보인다. **회색 격자는 Isaac viewport의 편집용 guide이며 원본 바닥 Mesh/Collider가 아니다.** 보완 촬영에서는 grid를숨겼다. crop 전체모습은 유지하고 별도 가까운 조감도를 추가했다. crop를 실제 사용 가능한 면적·층높이로 해석하지 않는다.

## 3. 환경별 실제 공간 관측

### 5F_CLOSED_EV

승강기 폐문, 창, 석고보드/콘크리트 벽과 짧은 전실, 바닥의 거친 표면가 실제 화면에서 보인다. 짧은 전실/복도; 넓은 접근·회전 공간과 Far시점 확보 미검증. 장애물/벽체: 폐문 승강기·측면 벽·모서리·좌측 개구부. 자재 배치 후보: 전실 바닥이 후보로 보이나 1.1m 팔레트와 로버 통과 동시 확보 미검증. 품질 한계: 창 과노출, 캡처 범위 밖/근접 시 blur; 외곽/하부 crop는 실제 바닥이 아님.

[원본 전체 조감도](alternative_environment_asset_review_20261103_v01/images/5F_CLOSED_EV__overview.png) · [로봇 높이 후보 시점](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_CLOSED_EV__camera_z0p65_S.png) · [바닥](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_CLOSED_EV__floor_near_origin.png) · [장애물](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_CLOSED_EV__camera_z0p65_W.png) · [배치공간 관측](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_CLOSED_EV__standing_z1p50_S.png)

![5F_CLOSED_EV의 실제 렌더6시점](alternative_environment_asset_review_20261103_v01/5F_CLOSED_EV_review_panel.png)
### 5F_OPEN_EV

5F_CLOSED와 유사한 전실, 열린 승강기 개구와 내부 모습; 개구 가장자리 잔상/반투명 왜곡가 실제 화면에서 보인다. 승강기 인계/문 앞 인식의 조건부 후보; 동일형상·정합은 미검증. 장애물/벽체: 승강기 문틀·문턱·벽과 모서리; 애니메이션/물리 Door는 없음. 자재 배치 후보: 문 앞 단거리 배치 후보; 문턱/승강기 내부 지지 구조 미검증. 품질 한계: 열린 개구부의 잔상·반투명 왜곡, crop Z가11.94m로 사용 가능한 단층 높이를 뜻하지 않음.

[원본 전체 조감도](alternative_environment_asset_review_20261103_v01/images/5F_OPEN_EV__overview.png) · [로봇 높이 후보 시점](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_OPEN_EV__camera_z0p65_SW.png) · [바닥](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_OPEN_EV__floor_near_origin.png) · [장애물](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_OPEN_EV__camera_z0p65_W.png) · [배치공간 관측](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/5F_OPEN_EV__standing_z1p50_S.png)

![5F_OPEN_EV의 실제 렌더6시점](alternative_environment_asset_review_20261103_v01/5F_OPEN_EV_review_panel.png)
### B1_CLOSED_EV

지하층으로 보이는 넓은 공사 통로, 기둥, 천장 배관/덕트, 임시 비닐 구획, 콘·안내판·소화기·자재가 실제 화면에서 보인다. 네 에셋 중 운반 접근/장애물 맥락의 우선 후보; 실제 폭/회전반경/전 구간 연결성 미측정. 장애물/벽체: 기둥·비닐 구획·콘·안내판·자재; 사람 모양 흐림/잔상도 보여 동적 장애물로 인증할 수 없음. 자재 배치 후보: N방향 통로 옆 빈 바닥이 후보; 배치와 swept clearances는 미검증. 품질 한계: 이동체로 의심되는 흐림/잔상과 재구성 구멍;66×124m crop를 가용 면적으로 사용하면 안 됨.

[원본 전체 조감도](alternative_environment_asset_review_20261103_v01/images/B1_CLOSED_EV__overview.png) · [로봇 높이 후보 시점](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/B1_CLOSED_EV__camera_z0p65_N.png) · [바닥](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/B1_CLOSED_EV__floor_near_origin.png) · [장애물](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/B1_CLOSED_EV__camera_z0p65_W.png) · [배치공간 관측](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/B1_CLOSED_EV__standing_z1p50_S.png)

![B1_CLOSED_EV의 실제 렌더6시점](alternative_environment_asset_review_20261103_v01/B1_CLOSED_EV_review_panel.png)
### Jeonju_122151

노출 콘크리트 벽과 열린 승강기, 청색 문/분전함, 공사 안내물이 있는 전실가 실제 화면에서 보인다. 승강기 주변 단거리 관측/인계 후보; crop 밖/넓은 이동 구역 품질은 미검증. 장애물/벽체: 문틀·노출벽·모서리·청색 문; 문턱의 지지/높이 미측정. 자재 배치 후보: 전실 일부 바닥이 후보; 물체를 실제 배치하지 않았으며 통로 여유 미검증. 품질 한계: 큰 crop61×129m 대비 origin 주변 관측 위주; 벽/개구 가까이 view-dependent blur.

[원본 전체 조감도](alternative_environment_asset_review_20261103_v01/images/Jeonju_122151__overview.png) · [로봇 높이 후보 시점](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/Jeonju_122151__camera_z0p65_SW.png) · [바닥](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/Jeonju_122151__floor_near_origin.png) · [장애물](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/Jeonju_122151__camera_z0p65_W.png) · [배치공간 관측](alternative_environment_asset_review_20261103_v01/detail_capture_v02/images/Jeonju_122151__standing_z1p50_S.png)

![Jeonju_122151의 실제 렌더6시점](alternative_environment_asset_review_20261103_v01/Jeonju_122151_review_panel.png)


5F_CLOSED와5F_OPEN은 비슷한 전실로 보이며 승강기 문 상태의 차이가 화면에 나타난다. 다만 두 파일의 metric 정합·완전한 동일 공간이라는 판정은 하지 않았다. open파일의 문/개구에는 잔상·반투명 왜곡이 관측되므로 ‘열려 보인다’는 사실을 로봇이 안전하게 통과할 수 있다는 뜻으로 사용하지 않는다. 승강기 움직임/문 opening joint는 없으며 정적 재구성이다.

B1의 N방향에는 사람 형상처럼 보이는 흐림/잔상이 있어 실제 고정 장애물이나 동적 사람 검증으로 사용할 수 없다. Jeonju는 열린 승강기와 노출 콘크리트 전실을 확인했지만 이름만으로 건물·층·권리자를 확정하지 않았다. 어느 이미지에도 팔레트를 합성 배치하거나 ‘이곳이충분하다’는 clearance 상자를 그리지 않았다.

## 4. USD 구조·물리 활용 가능성

| 환경 | 형식 | 원본Mesh/Collider | crop XYZ 크기(m) | 렌더 | 권리 |
|---|---|---|---|---|---|
| 5F_CLOSED_EV | NuRec | 0 / 0 | 9.92 × 15.91 × 5.07 | PASS | UNKNOWN |
| 5F_OPEN_EV | NuRec | 0 / 0 | 14.40 × 36.36 × 11.94 | PASS | UNKNOWN |
| B1_CLOSED_EV | NuRec | 0 / 0 | 65.90 × 124.03 × 8.80 | PASS | UNKNOWN |
| Jeonju_122151 | NuRec | 0 / 0 | 61.10 × 128.57 × 12.53 | PASS | UNKNOWN |

원본 네 파일은 전부 metersPerUnit=1, Z-up, composed prim5개이며 대체로다음 구조다.

```text
USDZ/default.usda → gauss.usda
/World
  /gauss                         [Xform]
    /gauss                       [Volume]
      /density_field             [OmniNuRecFieldAsset]
      /emissive_color_field      [OmniNuRecFieldAsset]
           filePath → Jeonju_*.nurec
```

**확인됨:** 네 파일 각각 Mesh0 / CollisionAPI0 / RigidBodyAPI0 / PhysicsScene0 / Camera0 /Light0. 외곽Volume의extent/crop와nurecfield만으로 영상이 나타난다. 바닥 Geometry와 벽체 Collider가 없다. 바닥의평탄도·경사·마찰·지지·문턱·최소통로폭은 UNKNOWN이다. 실제 사진 같은 바닥이 보여도 바퀴가놓이는 물리표면은아니다.

기존 Constructionsite는 Mesh1·CollisionAPI 적용prim1이 확인된다. 이것도원본환경전체의groundsupport/벽충돌·모든 paired조건의성공을인증한다는뜻은아니다. 이번에는기존 환경을다시렌더하거나주행검증하지않았다. 전수숫자·Prim계층·API·crop·멤버는 `USD_structure_and_collision.csv`, `USD_structure_details.json`에있다.

**물리화에 필요한 작업:** 실제측량/확인된모델에정합한바닥·벽·기둥·문틀·문턱·장애물geometry를새버전에작성하고Collider/마찰/지지/전체로봇sweptfootprint를검증해야한다. 단순히보이지않는Plane하나를넣으면모든문제가지원되는것처럼보일수있으므로이번에는추가하지않았다. 물리shape와neural appearance의정합이깨지면시각상빈곳에서충돌하거나보이는벽을관통한다.

## 5. NuRec 지원 및 렌더링 확인

실제 실행은기존 `/home/user/anaconda3/envs/hh_isaac51/bin/python`의SimulationApp,IsaacSim5.1,RTX5090,driver570.172.08,RayTracedLighting,singleGPU다. `--/UJITSO/geometry=true`,원본 renderSettings를적용했다. timeline은모든update/capture중stopped로확인했고원본을save하지않았다. 카메라/ReviewFillLight는임시layer에만추가했다. 소스에있는neural조명표현은일반Mesh의물리적re-lighting과같다고가정하지않는다.

첫 세션25 PNG와보완 세션49 PNG를각각저장했고process exit는둘다0. 각 asset별 분리 로그에서 `Failed to create nrend renderer`0건이다. 실제 이미지 내용도확인해단순 PNG 파일 존재만으로렌더PASS라하지않았다. close_called는있고app.close_returned이벤트는없으므로정상process종료와Pythonclose복귀를구분한다.

공식 [IsaacSim5.1 Neural Volume Rendering](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/assets/usd_assets_nurec.html)은NuRec시각화와추가collisionplane사용예를설명한다. [공식저장소issue635](https://github.com/isaac-sim/IsaacSim/issues/635)에는5.1/Blackwell및particle/volume지원문제기록이있다.이를사전점검했지만,**이번로컬네파일은실제렌더에성공했으므로그issue를그대로적용해실패라고판정하지않았다.** 반대로이성공을모든NuRec버전·다른GPU·센서지원보증으로일반화하지않는다.

첫bbox기반촬영중일부crop-min+1m카메라는실제공간아래/밖을보아blur·빈영역이나왔다. 이결과를삭제하지않고initial24 contact sheet와raw이미지에남겼다. 보완촬영은같은원본에원점주변z.65/yaw8방향,z1.5N/S,바닥·가까운조감도12뷰를정적으로추가한것이다. 이시점탐색은실험모델선택이나HPO가아니다. 원본 정점/mesh를가정해임의이미지로대체하지않았다.

## 6. 기존 환경과 비교

| 평가항목 | 기존 환경 | 대안과 차이 |
|---|---|---|
| 현장 적합성 | 넓은 콘크리트 건설현장Mesh 배경 | 실제 공사 전실/통로 NuRec; B1이 운반 맥락에 가장 유리 |
| 이동 가능 공간 | 기존 배치/잠금·과거 주행 기록 존재, 전 조건 경로 성공 아님 | B1 통로 유력, 나머지 작은 승강기 전실 중심 |
| 자재 적재 공간 | 기존 fixture/팔레트 배치와 좌표 존재 | 빈 바닥 후보는 보이나1.1m pallet+rover여유 미검증 |
| 카메라 환경 | 동결 HR/LR/CAD 모델과 원래RGB-D 정책 | view-dependent blur/holes, window exposure, baked appearance |
| 물리 시뮬레이션 | 환경Mesh1/CollisionAPI1 확인; 과거 전체task success와 구분 | Mesh0/Collider0/RigidBody0/PhysicsScene0 |
| 환경 수정 비용 | 기존 fixtures/robot/lighting pipeline | 높음: staticphysics map+neural alignment+sensor/lighting정합 |
| 연구 재현성 | 기존protocol/seed/geometry/modelhash 보존 | 새 workspace/scene hash와 관측정책 잠금 필요 |
| 라이선스 | upstream 미확정, CGTrader 후보 No-AI 여부 미해결 | 네 파일 모두 제작자·원URL·연구권리UNKNOWN |

특히현재 설계 중심(-25.888,30.509)m는5F_CLOSED/5F_OPEN/Jeonju의crop XY밖이다. B1에서는bbox안이지만실제표면·빈공간안이라는증거는아니다. **기존로버/팔레트/목표물의절대world좌표를그대로복사하는것은유효한이식이아니다.** 로봇과팔레트모델·상대fixture치수·물리상수는재사용가능성이있지만새workspace의검증된frame/지지/충돌조건에새로결합해야한다.

## 7. A/B/C 평가와 추천

- A(즉시대체유력): **0개**. 네 파일 모두물리Geometry와사용권리확인이부족하다.
- B(조건부대체가능): **4개**. 실제RGB공간은확인됐으며독립Geometry/Collision/센서정합/권리확보가필요하다.
- C(대체부적합확정): **0개**. 현재자료만으로영구사용불가나모든경로부재를증명하지않았다. 모든에셋의활용성을낙관한다는뜻은아니며사용목적은다르다.

| 환경 | 평가 | 확인한 장점 | 미검증/제약 | 추천순위 |
|---|---|---|---|---|
| 5F_CLOSED_EV | B: 조건부 | 승강기 폐문, 창, 석고보드/콘크리트 벽과 짧은 전실, 바닥의 거친 표면 | 짧은 전실/복도; 넓은 접근·회전 공간과 Far시점 확보 미검증 | 2 |
| 5F_OPEN_EV | B: 조건부 | 5F_CLOSED와 유사한 전실, 열린 승강기 개구와 내부 모습; 개구 가장자리 잔상/반투명 왜곡 | 승강기 인계/문 앞 인식의 조건부 후보; 동일형상·정합은 미검증 | 3 |
| B1_CLOSED_EV | B: 조건부 | 지하층으로 보이는 넓은 공사 통로, 기둥, 천장 배관/덕트, 임시 비닐 구획, 콘·안내판·소화기·자재 | 네 에셋 중 운반 접근/장애물 맥락의 우선 후보; 실제 폭/회전반경/전 구간 연결성 미측정 | 1 |
| Jeonju_122151 | B: 조건부 | 노출 콘크리트 벽과 열린 승강기, 청색 문/분전함, 공사 안내물이 있는 전실 | 승강기 주변 단거리 관측/인계 후보; crop 밖/넓은 이동 구역 품질은 미검증 | 4 |

**가장 적합한 우선 후보:B1_CLOSED_EV.** 현재건설자재운반연구와가장가까운통로·기둥·공사구획·현장자재가동시에보이고,작은승강기전실보다접근/적재구역후보를설계할여지가있어보인다. 이것은영상에근거한조건부우선순위이며통로폭이나팔레트1.1m배치가능성을실측확정한결과가아니다. 후속검토는B1의품질좋은부분한구역에서측량/정합geometry와workspace를먼저확보하는것이타당하다.5F두종은승강기앞단거리전달/인식장면이라는연구질문에더적합할수있다.

## 8. HR/LR/CAD 연구 영향 — 재실험은 하지 않음

1. **배치와 좌표:** 로봇·팔레트 모델과 상대 치수는 재사용할 수 있다. 하지만 새 task-design center, 접근면, 관측 pose와 paired base scenario를 별도로 정해야 한다. 기존 geometry lock을 덮어쓰지 않고 새 환경 버전과 원래 결과를 분리한다. HR/LR/GeoCAD는 같은 조건과 관측 정책으로 대응시킨다. LR은 저감 취득 조건의 독립 재구성이며 HR decimation으로 대체하지 않는다.

2. **경로와 주행:** 기존 rear offset .338m, wheelbase .7m, steering15°, 보수 곡률 상한 .363645332585095/m을 무단 변경하지 않는다. 이 상한에 대응하는 반경은 약2.75m다. 좁은 전실에서는 접근 공간을 특히 확인해야 하지만, 이것만으로 모든 경로가 불가능하다고 판정할 수는 없다. v47의 local planner/bracket 거절도 배경 교체만으로 해결됐다고 말할 수 없다. 새 occupancy·swept geometry·support·stopped handoff 검증이 필요하며 이번에는 경로 탐색이나 주행을 하지 않았다.

3. **카메라와 조명:** 기존 mount/extrinsics는 검증된 로봇 모델에서 재사용하되, 새 world base TF 및 실제 바닥 frame에 정합해야 한다. NuRec의 빛과 그림자는 촬영된 모습이므로 새로 넣은 벽돌의 조명·그림자·occlusion과 맞지 않을 수 있다. RGB 렌더 성공은 depth 정확도, semantics, 가시성 또는 B5 평면 추정의 보증이 아니다. 별도 RGB-D 관측 계약과 바닥·벽체 depth 정합 검증이 필요하다.

4. **SDG와 YOLO:** 새 환경의 성능을 주장하려면 새 조건의 fresh paired 데이터를 준비해야 한다. 기존 SDG는 원래 환경 자료로 보존한다. 재학습이 반드시 필요한지는 아직 알 수 없다. 먼저 동결 모델과 전향 검증용 GT로 도메인 변화 영향을 평가하고, 필요할 때 별도 학습·validation 설계를 한다. Test189를 모델 선택이나 튜닝에 재사용하지 않는다. 이번 데이터 재생성·추론·훈련은 모두0이다.

5. **기존 결과의 사용 범위:** 원래 IoU·검출/B5 수율·위치오차·planner 거절·거리/가림/조명 효과·collision/support·물리 PRE/FINAL을 새 환경의 성능으로 옮겨 주장할 수 없다. 원래 결과는 그대로 유지하고 새 환경에서는 해당 항목을 재검증해야 한다. 같은 RGB를 다시 분석한 자료를 독립 관측으로 늘리지 않는다. 실물 red-only 검증을 cement나 새 현장의 실제 주행 검증으로 확대하지 않는다.

6. **실구동 게이트:** 사람 ROI 검토 PENDING, 역사 v44 사전 검토 FAIL, v38 승인된 실측 steering abort 규칙 HOLD는 그대로다. 이번 정적 촬영 성공은 새 주행이나 정지 조향의 허가가 아니다.

## 9. 출처·라이선스

네 파일은 앞선 [출처 조사](construction_environment_usd_provenance_audit.md)에서 확인한 assets.zip/assets.z01→assets_full.zip 묶음에 들어 있다. 그러나 **제작자·원 다운로드 URL·학술/ML/논문 그림 사용 권한은 모두 UNKNOWN**이다.

`Jeonju`·`EV`라는 이름, 한국어 안내문, NuRec 기술만으로 고레로보틱스 소유나 제작이라고 판정하지 않았다. NVIDIA의 NuRec 기술 라이선스와 촬영된 콘텐츠의 권리는 별개다. 기존 Constructionsite를 이 파일들로 바꾸더라도 출처·권리 문제가 자동으로 해결되지 않는다.

묶음 전달자나 촬영·재구성 담당자에게 소유권, 촬영 장소와 동의, 정확한 파일 버전, 연구·합성데이터·ML 활용, 논문 이미지 공개 및 수정·공유 범위를 확인해야 한다. 이번 이미지는 내부 검토 자료이며 논문 게재 권한 확인을 대신하지 않는다.

## 10. 결론과다음단계

**실제 모습 확보 PASS / 물리 주행 준비 미충족 / 권리UNKNOWN.** B1_CLOSED_EV를조건부 1순위로추천하며,새 연구 환경으로즉시채택/기존실험교체하지않는다. 다음구체단계는B1의검토구역에대한권리와실측/정합floor·wallgeometry를확보하고,원하는거리/시점·팔레트/로버경로가그검증구역안에들어가는지새버전으로설계하는것이다.

변경은새보고서와신규이미지/검사로그/CSV/JSON/실행코드snapshot뿐이다. 원본 USD/기존 Stage/실험 결과/PROJECT_STATE 불변. 두실제Kitprocess종료0,source SHA7/7 PASS,PNG74/74decodePASS. 도중연구실패를지우거나physics성공으로표시한항목0. 초기바닥밖시점·blur·빈crop영역은실제자료로보존했다. 원격 push/publish는수행하지않았다.
