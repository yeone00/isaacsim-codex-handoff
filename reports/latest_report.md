# 현장 perception→approach 통합 첫 실행 v11 — 2026-11-01

**전체 FAIL / NOT_READY. 실제 Kit 1회, 재시도 0. 새 RGB-D 캡처 시작 전 assertion으로 중단했다. YOLO·B4·B5·PRE/FINAL·주행은 미도달이다.** HPO/training PAUSED, 연구 denominator 0. 과거 v10B 이동 성공이나 이전 영상의 B5 결과를 이번 성과로 대입하지 않았다.

## 실제 실패와 범위

출력: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v11_01`. `attempt_0001/execution_provisional.json`에 실제 traceback, `runtime.log`와 `run_status.json`에 종료를 보존했다.

session v11:266의 `timeline.pause()` 직후 adapter:22가 `assert not timeline.is_playing()`을 검사했으나 playing 상태여서 실패했다. pause 요청이 즉시 관측 상태로 바뀐다고 가정한 새 통합 코드의 오류다. 이번 세션은 render product 생성·RGB/depth 저장 전에 종료됐다. 예외 문자열은 빈 문자열이지만 traceback은 AssertionError 및 해당 위치를 명시한다. 이를 경로 충돌이나 센서 검출 실패로 바꾸어 해석하지 않는다.

기존 v10C 패치를 다시 작성하지 않았고 기존 persistence helper를 그대로 호출했다. 새 runner/session은 v10C 기반이며 캡처·관측 기반 경로 admission을 driver 생성 이전에 삽입했다. adapter는 기존 v02 capture/inference와 기존 상판 RANSAC/TLS fit 및 frozen pose namespace를 재사용하는 코드다. 단, 실제 perception 실행까지 도달하지 않았으므로 동작 인증은 아니다. 새 source에는 관측 경로와 수동 ROI 검토가 완료되지 않으면 중단하는 gate가 있다. 기존 v10B 동작 본문 및 prepare의 original_B 메타데이터는 계승되어 있지만 이번에는 해당 본문·ROS driver를 실행하지 않았다. 따라서 이 코드는 임의 관측 목표를 따라가는 완성된 일반 주행기라는 주장을 하지 않는다.

## 단계별 결과

| 단계 | 실제 결과 |
|---|---|
| 새 mounted RGB-D | FAIL, render·저장 전 pause assertion |
| Frozen HR YOLO segmentation | NOT_RUN, model predict 호출 0 |
| B4 heading | NOT_RUN |
| B5 수동 영상 ROI 보조 | NOT_RUN |
| 자동 pallet ROI/detection | 미구현, 자동 E2E 아님 |
| 같은 새 관측의 PRE/FINAL | NOT_COMPUTED |
| 관측 목표 corridor/footprint | NOT_EVALUATED |
| PRE 실제 이동 / FINAL 도착 | NOT_ATTEMPTED / NOT_ATTEMPTED |
| 무구동 baseline quiet | PASS, 주행 후 정지 인증과 구분 |
| cleanup zero receipt | FAIL/MISSING, ROS driver 없음 |
| close 전 provisional | 실제 생성, digest/source/존재 evidence hash PASS |
| 실제 Kit 종료 / outer 최종 파일 | Kit exit0, shutdown 로그, final 파일 생성 |
| v10C 전체 성공 판정 | NOT_READY / MISSING_WITNESS, runner exit1 |

`stage_outcomes.json`과 `independent_verification.json`은 원시 run_status를 고치지 않은 독립 요약이다. top-level MOVED/STOPPED NOT_TESTED와 원시 무구동 MOVED NO/QUIET PASS를 구분한다.

## 물리·안전 실측

- SimulationManager/PhysX: 257 steps, 4.283333556727s. 물리 rows 75개(articulation 초기화 전 settling은 physics callback 파일에 별도 기록).
- 측정 initial/final base XY 모두 `[-25.887977600097656, 28.470867156982422]`m. 기록 구간 순변위 및 최대 XY 변위 **0m**. 구동 이동 성과가 아니다.
- 기록 wheel peak abs dq **0rad/s**, 최종 모든 joint dq 0. nonzero Twist **0**, driver 생성 **0**, observer 관측 command 수 **0**.
- 기존 짧은 전방 baseline corridor PASS. 실제 strict PhysX support **2214/2214 PASS**, 6바퀴 접촉 및 shell floor ray 검사 PASS. 이 baseline corridor를 새 관측 PRE/FINAL의 안전성으로 쓰지 않는다.
- 예상 밖 접촉 **0**. baseline shell contact point가 없어 최소 contact separation은 null/UNKNOWN이며 양수 실측값을 꾸미지 않는다. shell ray gap 검사는 PASS다.
- baseline quiet 3.283333504573–4.283333556727s, coverage1.000000052154s, FD0/XY span0m, max COM .000388869344m/s, max origin .000394139814m/s. 주행 후 zero/quiet는 NOT_TESTED.
- cleanup pause/graph zero 요청 및 observer exit0; driver null. `zero_published.json` 없음. observer isolation admission 이전 예외라 cleanup receipt 계약이 충족되지 않았다. zero 명령 전달/물리 정지를 full completion으로 승격하지 않는다.
- 실행 전 Kit/training 없음, GPU compute는 기존 rustdesk535MiB뿐. 실행 후 Kit/training 검출0. 사용자 프로세스 중지·GPU reset·원본 stage/robot pose 직접 설정 없음.

## 수동 ROI·좌표·경로 연결 상태

미실행 adapter의 ROI polygon은 이전 RGB 육안 annotation `(158,269),(185,239),(444,239),(482,269)`의 이전 정의를 따른다. erosion2px, 예측 brick mask dilation3px 제외다. 새 영상에 실제 맞는지 확인한 적이 없으며 **이번 ROI provenance·mask·상판 평면은 생성되지 않았다**. 자동 pallet detection으로 부르지 않는다.

계획된 변환은 axial depth z(m)에 대해 `opt=[(u-cx)z/fx,(v-cy)z/fy,z]`, `world=R*opt+t`, 관측 상판 `n·world+d=0`의 centroid XY에서 `z_anchor=-(nx*xa+ny*ya+d)/nz`, frozen B5에 들어갈 Z만 `z_world-z_anchor+.144`로 옮긴다. capture는 renderer projection과 optical right/down/forward extrinsic을 교차 확인하는 기존 코드를 따른다. 이번 실제 intrinsics/extrinsics/frame/depth/mask/B4/B5 파일은 **없다**. 값 UNKNOWN을 옛 calibration으로 메우지 않는다.

PRE/FINAL은 기존 +90°/local_-X target policy와 추정 center로 산출하도록 연결했지만 미실행이다. 원본 task policy는 유지했고 GT target을 공급하지 않았다. 예전 B5/PRE/FINAL 및 고정 50mm B는 이번 목표로 사용하지 않았다. 관측 estimated target 및 original 대비 오차는 UNKNOWN/NOT_EVALUATED, 사후 USD GT 평가도 하지 않았다.

v10B는 +Y forward·travel65mm 한계의 특수 구동기다. 기존 `structured_path_follower_v01.py`는 `Goal behind; no reverse fallback`을 명시하고, 기존 reuse planner는 전진/반경2.8m/budget30s 방식이다. 예전 full-chain demo에는 FINAL을150mm 바꾸는 별도 정책과 다른 footprint 검사도 있어 사용자 조건에 그대로 맞지 않는다. 이번에는 새 관측도 없으므로 뒤쪽 목표/장애물 문제를 확정하거나 segmented path 존재/부재를 주장하지 않는다. 기존 follower를 실행하거나 새 planner를 만들지 않았다.

## v10C 첫 실제 종료 경계

Kit PID1182547, exit0, runtime shutdown 로그 `[49.903s] Simulation App Shutting Down`. provisional wall timestamp1793521240.1201334. close 호출 전 helper가 PROVISIONAL을 쓰는 소스 순서, runtime에서 해당 파일 존재, 실제 child 종료 후 outer의 `execution_complete.json` 및 `run_status.json` 생성까지 확인했다. provisional digest/source/evidence8개 hash PASS. 모든 evidence12개가 충족된 성공 run의 persistence 인증은 아니다.

필수 witness 중 `adapter_commands.jsonl`, `stop_confirmed.json`, `zero_published.json`, `calibration_ros_complete.json` 4개가 없다. 실제 미주행/receipt 미확보를 그대로 반영해 외부 verifier가 `MISSING_WITNESS`로 성공을 거절했다. final NOT_READY/runner1은 보존하며 누락 파일을 가짜로 만들거나 성공 조건을 완화하지 않았다. v10C 물리 quiet/driver/receipt를 모두 포함한 성공 경계는 여전히 미검증이다.

## 파일·검사·보존

신규 source:
- `scripts/construction_site_perception_adapter_20261101_v11.py`: `b80ffafc72d74575df2c6991b21219eda5ebdd4e0590a014b6066e66b13ed92f`
- `scripts/construction_site_perception_runner_20261101_v11.py`: `96cd15c710b89125d454e927331ba33237dd66bddca269909127b80a0009eb0f`
- `scripts/construction_site_perception_session_20261101_v11.py`: `9a23082f4e931037ce3c738c855c488624ae68532856c56f9092c38ad93519c5`

문서 변경: 본 보고서, latest_report mirror, PROJECT_STATE append. 보조 검사 보고서 `reports/known_locks_perception_20261101_v11.json`. 외부 root에 prepare/corridor/source snapshot/code_versions/runtime/attempt 원자료 및 독립 요약을 보존했다.

- PASS: 신규3파일 py_compile. 별도 Kit import 없이 원본 plane fit 함수와 새 adapter fit 함수 AST 동치 확인.
- PASS: prepare geometry worker/graph/baseline corridor. **prepare의 motion_allowed는 기존 짧은 baseline corridor 판정뿐이며 관측 목표 실행 허가가 아니다.**
- PASS: known-lock9개 SHA 및 해당108/432 row counts. 이번에는 전체 pairing/asset closure 재감사하지 않았고 연구 readiness 인증 아님.
- PASS: 원본 stage SHA `424cb17b104d7a68a4c264216e38b9823f371524a8704e07fb4eec8b08d1e264` 및 원본 참조 포함25개 입력 전후 보존. prepare source/config27개 전후 hash 일치. v10C 원본 helper/runner/session 포함 이전 코드 수정0.
- FAIL: 실제 통합 capture entry 및 전체 runner. CPU compile/AST PASS를 runtime PASS로 대체하지 않음. 새 geometry generalization/YOLO/B4/B5 runtime NOT_TESTED.
- 이번 신규 YOLO 모델 로드 전 실패했으므로 모델 runtime/hash admission도 미도달이다. frozen checkpoint 파일 변경·훈련 없음.

실제 명령:
```bash
python3 -m py_compile scripts/construction_site_perception*20261101_v11.py
python3 scripts/verify_known_locks.py --out reports/known_locks_perception_20261101_v11.json
python3 scripts/construction_site_perception_runner_20261101_v11.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v11_01
python3 scripts/construction_site_perception_runner_20261101_v11.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v11_01
```

## 다음 단일 수정

**새 버전에서 pause 요청과 capture 진입 사이에 bounded Kit update barrier를 넣어 실제 `is_playing()==False`와 physics time 안정화를 확인하고 나서 capture를 호출한다.** pause assertion을 삭제하거나 timeline stop/reset으로 대체하지 않는다. 설치된 timeline의 controller `commit()`은 pending state 적용 API지만 ITimeline과 Timeline 객체 API를 혼동하지 않도록 실제 반환 타입을 확인해야 한다. 가장 직접적인 후속 수정은 `pause()` 뒤 최대2wall초 `app.update()`로 상태 반영을 기다리고 timeout이면 중단하는 것이다. 이번 세션에서 수정·재실행하지 않았으며 추가 launch는0이다. 이 수정만으로 이후 ROI/경로/driver 연결이 검증된다는 뜻은 아니다.

학습/HPO/B300/324/432/Qual12·자산 비교·외부 배포·push 없음. **FIRST INTEGRATED PERCEPTION-TO-ROBOT SUCCESS 아님. 연구 denominator0.**
