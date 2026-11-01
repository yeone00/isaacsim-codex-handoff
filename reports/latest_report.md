# v25 HR pilot admission — BLOCKED / motion0

2026-11-02 (Asia/Seoul). **새 v24 HR 장면에서 Kit 정확히 1회, RETRY0. Engineering 성공 0/1, 비영 명령0, PRE/FINAL 미시작.** 원인은 이번 연결에서 추가한 renderer semantic annotator와 기존 graph 허용 목록의 충돌이다. 기존 guard가 정상 거절했으며 완화하거나 두 번째 Kit를 실행하지 않았다. 그와 별개로 기존 v21에도 존재하는 PhysX schema 오류 10건을 발견하여 다음 admission의 독립 blocker로 남겼다. HPO/training PAUSED, formal science denominator0, LR/CAD/324/432 실행0.

실제 raw root: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v25_05` (약13MiB). `attempt_0001/`에 새 stage/RGB/depth/calibration/renderer semantic buffer/PhysX support/contact/physics clock/ROS 관찰/cleanup 요청/exit 증거가 있다. `_01`–`_04`는 **Kit를 시작하지 않은 offline prepare 실패**이며 삭제하지 않았다. 숫자05가 다섯 번째 Kit 시도를 뜻하지 않는다.

| 독립 항목 | 결과와 한계 |
|---|---|
| HR 장면·모델 선택 | PASS. HR scene SHA `5b928d33d614c1328d3df87a66ea188844711f6b5bf6661e0f4c40a5f24cb0b4`, HR M50 SHA `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca` 재확인. 모델 실행은 안 됨. |
| 정적 full composition | PASS. 실제300 visual slot/선택 HR reference/transform, enabled static28/native enabled0, 공통 Plane binding과 union을 기존 독립 checker로 재검사. 부모·참조 dependency hashes도 검사. |
| 실제 열린 stage와 safety consumer | 새 run layer가 HR v24 scene을 직접 sublayer로 사용. live `collision_preflight.json`의 전체 collider inventory가 union28을 포함. 이 inventory는 USD 기반이며 cooked shapes 증거가 아님. |
| 원래 rover/graph | PASS 범위: graph exact comparison, 허용 delta 밖 actor exact comparison, live graph admission. 허용 범위는 hash-bound v24 load/union 및 Plane의 단일 재질 binding. 원래 graph/actor/TF 검사를 끄지 않음. |
| LIVE_RENDER_MATERIAL | 새640×480 RGB-D 획득 PASS, calibration8/8 PASS, valid depth290,691px. **전체 material admission은 INCONCLUSIVE/NO-GO**. 아래 영상 검토 참조. |
| 실제 PhysX28/native0 | **NOT_RUN / UNKNOWN**. overlap query 구현은 있으나 capture graph guard에서 그 호출보다 먼저 중단. offline CollisionAPI28을 등록28로 바꾸어 주장하지 않음. |
| 실제 휠 지지·shell | PASS 범위: stationary PhysX support2,214/2,214, 실제6wheel contact, corrected-ray certificate, shell gap/contact gate. union seam·native shape 부재·동적 하중을 인증하지 않음. |
| PhysX parser 진단 | **BLOCKED**. nested articulation roots 및 mounted rolltainer 하위 rigid body의 missing xformstack reset10건. v21 baseline에도 같은 종류10건이 있음. 기존 성공을 근거로 무해 처리하지 않음. |
| HR fresh YOLO/B4/B5/ROI | **NOT_RUN**. 새 RGB-D는 생성했지만 worker 시작 전 차단. 새 ROI·과거 ROI·predicted targets·GT pose 입력0. |
| PRE_REACHED / FINAL_REACHED | 둘 다 NOT_RUN. curved sweep/leg별 live support/물리 주행/개별 stop certificate 미생성. |
| 정상 stop / quiet | 정상 PRE/FINAL stop 없음. baseline quiet만1.000000052sim초 PASS, 측정 pose span0, COM peak0.000969488mm/s, origin peak0.000991107mm/s, FD0. 이를 post-command stop 성공으로 세지 않음. |
| 실제 base/wheel motion | 비영 command0, pulse path0, baseline 측정75행. 6wheel q span0/peak dq0. 초기 settling 구간 전체의 wheel tensor 측정은 없으므로 모든 중력 settling 변위0이라고 하지 않음. |
| contact | 저장168 events, 기존 정책상 unexpected0. 통과한 것은 관측된 stationary rover/ground 접촉 범위. union seam/contact behavior 전체는 UNKNOWN. |
| zero cleanup | 요청·abort·직접 graph zero backstop 경로 실행. **ROS zero receipt MISSING / 인증FAIL**. isolation 전 중단되어 원래 observer는 zero publisher를 만들지 않았음. isolation을 허위 생성하거나 publisher guard를 완화하지 않음. |
| exit / 독립 witness | Kit0, observer0, driver NOT_STARTED, runner1, outer NOT_READY/MISSING_WITNESS. 강제종료0, Kit/observer PID 소멸, 잔여 Kit/training0, 기존 RustDesk 보존. 독립 verdict BLOCKED. |

## 구현과 실제 실패 지점

실제 실행 소스는 `scripts/construction_site_perception_runner_20261102_v25.py`, `construction_site_perception_session_20261102_v25.py`, `construction_site_perception_adapter_20261102_v25.py`, `construction_site_pilot_link_20261102_v25.py`다. 원래 v21 runner/session/driver는 executed_code snapshot과 byte 일치를 먼저 확인하고 수정하지 않았다. v25 원본도 실실행 후 변경하지 않았다. raw root의 `executed_code/`, `prepare.json`, `code_versions.json`이 실행 코드·입력·환경을 묶는다.

실행 명령은 다음의 **완료된 실패 receipt**다. 재실행 지시가 아니다.

```text
python scripts/construction_site_perception_runner_20261102_v25.py --run --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v25_05
```

runner가 실제 `/home/user/anaconda3/envs/hh_isaac51/bin/python`으로 v25 session을 실행했다. 기존 Jazzy/FastRTPS/domain191 empty probe 및 Kit/training/GPU resource 검사를 통과했다. 시작 시 GPU에는 RustDesk만 있었다. SimulationApp renderer/초기화·outer900/930초·close25초 상한과 기존 controller/stop/TF .5wall/.1sim/GID/contact/steer/GC·RSS 정책을 보존했다. motion 단계·MotionGC.enter·driver isolation 이전 중단이므로 이 정책들의 이번 주행 성능을 검증했다는 뜻은 아니다.

새 root에 world 단위1m·Z up을 명시했다. USD stage metadata는 sublayer에서 자동으로 계승되지 않으므로 반드시 필요한 연결이다. rover start/parent·camera transform과 supplier graph는 기존 v21 baseline에서 계승하며 다시 배치하지 않았다. 과거 capture/ROI/goal/success를 복사하지 않았다.

이번에 추가한 `semantic_segmentation` annotator가 실제 `/Render/PostProcess/SDGPipeline/Replicator_03_instance_segmentation_fast_Sync`를 만들었다. `check_capture_graph`가 `UNKNOWN_GRAPH_NODE`로 거절했다. 기존 actuation graph를 변경했다고 확인된 사건은 아니지만, 허용되지 않은 render graph 추가를 안전상 통과시킬 수 없었다. 이때 capture 파일은 완성됐으나 `physx_gate`, runtime render review, perception worker는 호출 전이었다. 자동 retry0을 지켰다.

## 실제 영상의 제한된 사후 검토

새 RGB SHA `c696ab5f8303fc71831655161aeff01052394bb75c165d39938c9496e380bf90`. 직접 연 영상에서 원래 공사현장과 pallet, 매우 어두운 적재물이 보인다. intended HR material 품질을 이 영상만으로 확정하지 않는다. mounted rolltainer Plane은 front frame에 보이지 않으므로 공통 회색 fallback의 실제 가시 외관·ROI 영향도 인증하지 못했다. 원래 AprilTag 복원·동등 appearance 주장은 없다.

Renderer semantic buffer는 실제 생성됐지만 labels는 BACKGROUND/UNLABELLED뿐이다. HR object segmentation PASS가 아니다. 보이는 pallet top은 있으나 새 ROI 승인·B5를 발급하지 않았다. [사후 검토](construction_site_pilot_render_review_20261102_v25.json)는 runtime admission 허가가 아니며 새 run에서 재사용할 수 없다.

## 오프라인 검증과 실패 보존

- [HR focused regression](construction_site_pilot_regression_20261102_v25.json) 14/14 PASS: exact scene/model/composition300/28/native0, collider consumer28, original graph, missing/disabled cell 및 ROS graph mutation 거절, worker parameter binding, v21 stop 연결, gate 순서, 새 output·stale target 없음, one-attempt/error lifecycle 및 input hashes. [실제 로그](construction_site_pilot_regression_20261102_v25.log).
- 기존 `analysis/construction_site_stop_test_20261101_v21.py` 20/20 PASS/exit0/26.082초. 역사적 반환·정상 stop event·거절 counterexample 재검증이며 새 pilot 성공이 아니다. 최초 stdout은 이번 terminal 기록이며 별도 raw log를 꾸며 만들지 않았다.
- [known lock subset](construction_site_known_locks_20261102_v25.json) 9 SHA 및108/432 row counts PASS. prelock v01→amendment through v03/geometry v02 보존. geometry lock 자체의 독립 expected hash는 UNKNOWN 유지. frozen science pairing/membership/seed/metrics/threshold를 수정하지 않았다.
- offline `_01`: root stage metric assert; `_02`/`_03`: exact actor guard가 의도한 Plane material binding 차이1건을 포착; `_04`: 설치 USD에 없는 `Stage.GetCompositionErrors` 호출로 실패. `_05` 이전에 root metadata 명시·Plane 한 관계만 exact 허용·지원되는 used-layer 검사로 해결했다. [검증·실패 목록](construction_site_pilot_validation_20261102_v25.json). guard 거절과 API 오류를 삭제하지 않았다.
- [최종 integrity](construction_site_pilot_integrity_20261102_v25.json): 실행 입력 hashes·snapshot·provisional digest·기존 evidence hashes 모두 PASS, HR scene 원본 SHA 불변, process absence PASS. [독립 witness 및 raw hash index](construction_site_pilot_witness_20261102_v25.json), [간략 출력](construction_site_pilot_witness_20261102_v25.log). Kit exit0과 engineering 실패를 별도로 보존했다.

## 실행 후 오프라인 수정 및 다음 한 작업

추가 annotator를 제거하여 v21의 실제 capture 함수와 **pinned pilot SOURCE metadata 외 AST exact 일치**하는 v25b adapter를 만들었다. v25b runner/session은 이를 연결하며 원래 graph checker·v21 event-aware stop verifier·28셀 overlap gate·render review를 유지한다. segmentation은 기존 frozen YOLO mask 경로이며, renderer semantic admission을 얻었다고 하지 않는다. v25b는 새 버전 소스일 뿐 **추가 Kit/prepare/worker 실행0**이다. [첫 correction 검사](construction_site_pilot_offline_fix_20261102_v25.json), [최종 compile·진단 gate 검사](construction_site_pilot_offline_fix_20261102_v25_v02.json).

또한 v25b에는 owned runtime log의 PhysX schema Error를 capture·motion 전에 NO-GO로 기록하는 gate를 추가했다. 저장 v25/v21 로그에 대한 offline replay가 각각10건을 거절했다. 이는 robot/graph를 고치거나 예외를 허용한 것이 아니다. **v25b도 현재 LIVE_BLOCKED**이며 실행 준비 완료라고 하지 않는다.

다음 작업은 HR에서 보존된 rolltainer physics schema 오류가 실제 활성 articulation/shape에 미치는 영향을 오프라인으로 판정하고, root/rover 보존 조건 안에서 해결할 수 있는지 결정하는 것이다. 이후 별도 한 HR admission에서 material/fallback의 가시 검토와 실제28/native0 shape 등록부터 다시 인증해야 한다. 기존 실패 root는 재사용하지 않는다. 이번 task에 추가 Kit는 없다.

실제 clean HR PRE→FINAL 성공 이후에만 LR/CAD를 각각 같은 physical scene/controller·공통 reviewer/ROI 규칙·표현별 frozen model·fresh RGB-D와 별도 새 scene/output의 한 trial로 제안한다. 그때도 각 표현의 render/PhysX를 새로 확인한다. 이번0/1 engineering 실패는 표현 비교나 reliability 추정, scientific 실패 관측, Real Test189 재평가가 아니다. LR은 저감 acquisition 독립 재구성이며 HR decimation이 아니다. red-only real validation을 cement·실로봇 배포로 확대하지 않는다.

변경: 신규 v25 link/runner/session/adapter, offline 수정 v25b runner/session/adapter, 신규 regression/witness 분석 스크립트, 위 reports·검사 JSON/로그, pilot-only DRAFT, `reports/latest_report.md`, `docs/PROJECT_STATE.md`. bulk USD/RGB/depth·기존 weights는 외부 원위치. 원래 USD/rover/graph/checkpoint/v24 세 overlay/v20 실패/v21 성공/과학 locks는 보존했으며 install/upgrade/training/push/remote 변경0이다.
