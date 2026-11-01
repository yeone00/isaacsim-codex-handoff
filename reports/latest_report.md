# 현장 perception → PRE → FINAL v15 — 2026-11-01

**GRAPH_CHANGED 원인 해결·실제 ROS 곡선 주행 시작. 전체 demo NOT_READY: PRE 물리 NO / FINAL 물리 NO.** 새 인식은 PASS지만 PRE 도중 `TF_STALE`로 안전 정지했다. Kit 2회 한도를 소진했고 추가 실행하지 않았다. HPO/training PAUSED, 과학 denominator0.

| 결과 | 첫 시도 v15_01 | 마지막 시도 v15_02 |
|---|---|---|
| fresh mounted RGB-D → frozen YOLO/B4/수동 ROI B5 | PASS | PASS |
| 실제 capture graph 차이 | 렌더 노드17 추가, 기존 변경/삭제0 | 동일 |
| 공급자 actuator/ROS wiring | 변경0 | capture 및 매 tick invariant PASS; graph fault 없음 |
| PRE swept collision / live wheel support | PASS / 24300/24300 | PASS / 24300/24300 |
| 비영 ROS Twist | 0 | 288회 |
| PRE / FINAL 물리 도달 | NO / NO | NO / NO |
| base 경로길이 / 순변위 | 0 / 0m | .255870 / .254318m |
| wheel dq 최대 절댓값 | 0rad/s | .984256rad/s |
| 예상 밖 contact / 주행 shell 침투·하중 event | 0 / 미주행 | 0 / 0 |
| 주행 후 quiet | NOT_TESTED | PASS, 1초·pose span0·최대속도 .0002164m/s |
| zero | cleanup 기록 보존 | driver 최종20회+observer10회; cleanup receipt 검증 FAIL |
| 실제 Kit PID / exit | 1362015 / −9 | 1365688 / 0 |
| runner exit / outer result | 1 / KIT_EXIT_NOT_ZERO | 1 / MISSING_WITNESS·NOT_READY |

## 실제 그래프 차이와 수정

첫 실제 composed stage capture 직전 **19:41:39.556684 KST**, 직후 **19:41:40.389535 KST** 원자료는 `_01/attempt_0001/graph_pre_capture.json`, `graph_post_capture.json`, 재개 첫 tick의 `graph_changed_detail.json`이다. 두 번째는 **19:44:04.888041 → 19:44:05.748963 KST**이며 별도 fresh frame이다. 원래 v14c는 미실행이었고, 이번 v15는 그 계측을 복제·확장해 실제 관측했다. 아래17개는 모두 **A(render/capture-only)**다. B/C 관측0. 정확한 input 값·connection·relationship 전체와 wall time은 각 root의 `engineering_outcome_v15.json` 및 위 snapshot에 보존했다.

| 정확한 추가 prim path | node:type |
|---|---|
| `/Orchestrator/OgnReadFabricTime` | `omni.replicator.core.ReadFabricTime` |
| `/Render/OmniverseKit/HydraTextures/Replicator_03/PostRender/SDGPipeline/Replicator_03_CameraParamsOpenCVPR` | `omni.replicator.core.CameraParamsOpenCV` |
| `/Render/OmniverseKit/HydraTextures/Replicator_03/PostRender/SDGPipeline/Replicator_03_DistanceToImagePlaneSDPostCopyToHost` | `omni.syntheticdata.SdPostRenderVarToHost` |
| `/Render/OmniverseKit/HydraTextures/Replicator_03/PostRender/SDGPipeline/Replicator_03_GpuInteropEntry` | `omni.graph.nodes.GpuInteropRenderProductEntry` |
| `/Render/OmniverseKit/HydraTextures/Replicator_03/PostRender/SDGPipeline/Replicator_03_LdrColorSDPostCopyToHost` | `omni.syntheticdata.SdPostRenderVarToHost` |
| `/Render/OmniverseKit/HydraTextures/Replicator_03/PostRender/SDGPipeline/Replicator_03_PostRenderProductCamera` | `omni.syntheticdata.SdRenderProductCamera` |
| `/Render/PostProcess/SDGPipeline/DispatchSync` | `omni.replicator.core.OgnRefTimeGate` |
| `/Render/PostProcess/SDGPipeline/PostProcessDispatcher` | `omni.syntheticdata.SdOnNewFrame` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_CameraParams` | `omni.replicator.core.CameraParams` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_CameraParamsOpenCV` | `omni.replicator.core.CameraParamsOpenCV` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_CameraParamsOpenCV_Sync` | `omni.graph.action.RationalTimeSyncGate` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_CameraParams_Sync` | `omni.graph.action.RationalTimeSyncGate` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_DistanceToImagePlaneSDhostPtr` | `omni.syntheticdata.SdRenderVarPtr` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_LdrColorSDhostPtr` | `omni.syntheticdata.SdRenderVarPtr` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_PostProcessDispatch` | `omni.syntheticdata.SdOnNewRenderProductFrame` |
| `/Render/PostProcess/SDGPipeline/Replicator_03_PostProcessRenderProductCamera` | `omni.syntheticdata.SdRenderProductCamera` |
| `/Render/Simulation/SDGPipeline/Replicator_03_RenderProductCameraPrimPath` | `omni.syntheticdata.SdSimRenderProductCamera` |

분류는 prefix만으로 하지 않았다. 추가 노드17개 모두 inputs relationship가 비어 있고, 연결은 render dispatcher/GPU interop/camera parameter 경로 안에 있다. `ReadFabricTime`에는 input/relationship가 없다. 렌더 경로 값은 실제 `/Render/OmniverseKit/HydraTextures/Replicator_03`다. 기존 모든 노드는 정확히 동일하므로 추가 노드가 공급자 actuator 입력으로 연결된 흔적도 없다.

공급자 `/World/ENG_FE2E/Rover/ActionGraph`의 `ros2_subscribe_twist`는 `rover/cmd_vel`, domain191의 `EngineeringROS2Context`, 기존 playback tick을 유지했다. linear.x → `multiply_01`(15.0) → Ackermann speed, angular.z → `multiply`(−.7)·기존 atan2 → steering 연결을 변경하지 않았다. Ackermann wheelbase .7m/invertSteering True 및 세 controller의 jointNames와 입력 연결, `inputs:targetPrim=[/World/ENG_FE2E/Rover/base_link]`, 빈 robotPath가 동일했다. 원래 expected_graph에 대한 admission도 두 번 PASS. 실제 node type/버전·input config/connection·target 관계는 snapshot에 전체 보존했다. ROS publisher/subscriber의 GID 고정 guard는 그대로다. 새로운 publisher identity를 허용하지 않았다.

작은 `evaluation/construction_site_graph_20261101_v15.py`는 **baseline 전체를 그대로 비교**하고, 실제 첫 시도에서 관측한17개 추가 노드만 exact path/type/port/config/connection/relationship로 허용한다. `DispatchSync.inputs:simTimesToWrite`의 렌더 frame schedule 값만 정규화하며 connection은 비교한다. 알 수 없는 노드나 actuator 변경은 거절한다. baseline 재설정이나 graph guard 비활성화는 없다. allow manifest는 `evaluation/construction_site_render_allow_20261101_v15.json`이며 prepare hash에 포함됐다.

## 새 인식과 실제 물리 증거

두 fresh 결과 PRE=(-25.934803317,28.278040478), FINAL=(-25.934803317,29.078040478)m. 같은 scene/rover, v14b의 physics 전 engineering startup을 유지했다. 새 영상마다 RGB와 overlay를 직접 확인하고 `(236,197),(251,181),(383,181),(403,197)` 수동 ROI를 새 RGB SHA256에 결합했다. 자동 팔레트 인식이 아니다. frozen HR model·B4/B5·+90° policy, 기존 v14 follower/legacy encoding/StoppingAdapter를 재사용했다. 목표를 v14 좌표나 GT로 대체하지 않았고 실행 중 transform 변경은 없다.

마지막 base는 (-25.916446686,27.652854919)m, yaw 약93.449°다. wheel dq와 controller target·base tensor/FD physics가 steps/adapter commands에 함께 남았다. 새 PRE 경로의 실제13 collider 곡선 sweep와 live support를 통과한 뒤에만 비영 명령을 보냈다. 전체 곡선 추종 성공은 아니다. FINAL leg은 PRE 미도달로 plan/sweep/drive 미시도다.

PRE 잔여 직선거리 **0.625455m**에서 driver `TF_STALE`가 발생했다. 해당 guard 입력의 TF wall age는 **0.502469063s > .5s**, sim stamp 차이는 약 .016667s였고 GID는 고정값과 동일했다. 그 뒤 session은 `TWO_LEGS_INCOMPLETE`를 기록했다. pulse 중 기록 간 최대 wall 간격은 **.434226s**다. TF 지연의 근본 원인은 UNKNOWN이며 단순 threshold 완화로 해결하지 않았다.

## 정지·종료·검사와 다음 작업

비상 zero 후 물리 quiet PASS와 cleanup 성공을 구분한다. 마지막 driver는 final zero20회, observer는 zero10회를 기록했다. observer zero receipt는 cleanup 요청보다 먼저 생성되어 `ZERO_RECEIPT_INVALID`이며 lifecycle 완료 인증은 FAIL이다. PRE/FINAL stop certificate가 없어서 outer `MISSING_WITNESS`도 유지했다. driver/observer exit는 모두0이지만 전체 성공을 뜻하지 않는다.

첫 close는 provisional 저장 뒤에도 멈춰, 새 runner가25초 후 **소유 Kit 자식만** TERM하고5초 뒤 KILL했다. exit−9/forced termination은 실패다. 두 번째는 `Simulation App Shutting Down` 및 실제 Kit exit0 확인 후 outer final을 썼다. 역사적 v14 −9는 그대로 실패다. 두 시도 모두 prepare 입력 hash와 존재하는 provisional evidence SHA256 재검사 PASS이며 종료신호가 원래 zero_request를 덮어쓰지 않았다. 미존재 필수 witness를 PASS로 만들지 않았다.

검사: 신규 Python compile PASS; `python3 analysis/construction_site_graph_test_20261101_v15.py`의 실제 렌더17개 추가 허용 및 actuator type/connection/target/config 변경 거절 **5개 PASS**. Kit 전 resource/GPU/domain 격리 PASS, 사용자 Kit/GUI/training 없음·rustdesk 보존. 원본 USD/rover/model/scientific data/v01–v14 source와 result는 수정하지 않았다. 추가 source는 session/runner v15·v15b, graph invariant·allow manifest, CPU replay 검사다. 본 보고서·latest·PROJECT_STATE를 갱신했다.

**다음 실제 blocker:** `.5s` TF freshness를 유지하면서 runtime 지연을 줄여야 한다. 현재 session이 매 tick 누적 command JSONL 전체를 다시 읽고 controller readback에도 전체 재독해하며, driver는 매 command path JSON 전체를 다시 읽는다. 먼저 새 버전에서 이 부분만 cursor/cache로 바꾸고 physics update/TF publish/observer receive 시각을 최소 계측하여 지연 원인을 확인한다(현재 I/O가 원인이라는 확정은 아님). emergency zero receipt는 해당 요청 시각과 결합해 별도로 고친다. 안전 한계와 GID guard를 유지한 뒤 새로운 별도 bounded 실행에서 PRE→FINAL을 완주해야 한다. 이번 두 번 뒤 추가 Kit/50mm replay/학습/대규모 실험은 없다.

증거 root:

- `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v15_01`
- `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v15_02`

각 root의 prepare/code_versions/executed_code, engineering_outcome_v15, run_status와 attempt_0001의 원본 fault/provisional/outer final을 함께 읽는다. Kit exit0만으로 runner 성공이나 PRE/FINAL 도달을 주장하지 않는다.
