# 현장 drive v09 실제 1회 — 이동·정지·정상 child 종료, 전체 runner NOT_READY

2026-11-01 KST. **실제 Kit 세션 1회 / ROS 주행 episode 1회 / 재시도 0회. MOVED YES, STOPPED PASS, 물리 안전 PASS.** 실제 world base 순변위 **21.505356mm**. v09 normal-stop handshake와 driver·observer·Kit 종료는 정상이며 FAULT_LATCHED·watchdog trigger는 없다. 그러나 성공 판정의 cleanup 증거 요구 순서 오류로 **전체 NOT_READY / runner exit1**이다. v09 전체 PASS로 올리지 않았다. HPO/training PAUSED, 연구 denominator **0**.

## A→B와 실제 목적지

새 prepare의 기존 B는 world XY `(-25.887977680000, 28.520869113267)m`, 약50mm 전방이다. 코드의 고정2초 pulse·surface 요청 .02m/s·yaw0을 변경하지 않았다. 폐루프 목표 추종이나 pulse 연장은 하지 않았다.

- 시작 A world XY: `(-25.887977600098, 28.470867156982)m`.
- 실제 정지 목적지 **B′(사후 측정한 짧은 목적지)**: `(-25.887975692749, 28.492372512817)m`.
- world ΔX / ΔY: `0.000001907349 / +0.021505355835m`.
- **계획 B까지 남은 Euclidean 거리 28.496601mm. 50mm 계획 위치 자체 도달: NO.** 실제 짧은 A→B′ 이동·정지: YES. B′는 사전 목표를 바꿔 성공으로 만든 점이 아니다.
- 기존 engineering target.pass는 TRUE(±30mm/±2°), long error −28.494644mm, yaw error .000299971°. 이 넓은 진단 허용창 통과를 50mm 실이동 또는 연구 정밀 FINAL 도달이라고 부르지 않는다. 동결 연구 metric은 변경하지 않았다.

## 실제 물리·정지·종료의 분리 판정

| 항목 | 실제 관측 / 판정 |
|---|---|
| 구동 경로 | 기존 supplier ROS `/rover/cmd_vel` → 기존 ActionGraph → 기존 3 articulation controllers → PhysX; ROS admission PASS, native fallback 미실행 |
| MOVED | YES, world base 순변위 21.505356mm; 비영 publish45회 |
| wheel 반응 | peak abs dq 0.362895578rad/s; peak abs Δq 0.164466966rad; 최종 abs dq0 |
| 속도 | base 최대 planar 0.020390048m/s; 기존 .03m/s pulse abort 이하 |
| 정상 감속 | BRAKING sim6.516667007 → ZERO_SETTLING/zero sim6.766667020 |
| 첫 stop 인증 | sim7.800000407, zero 이후 최소1 physical sim초 quiet 및 graph/controller zero 확인 |
| 최종 STOPPED | PASS; sim14.883334110–15.883334162, 1.000000052 physical초 |
| 최종 quiet 속도 | COM 0.000209952051, origin 0.000215435673, FD0m/s; pose span0m |
| graph zero | quiet 창 wheel targets 및 두 wheel controller velocity 배열0; driver final zero20회, cleanup observer zero10회 |
| child lifecycle | completion_accepted TRUE, ZERO_SETTLING, adapter_fault NULL, hard_trigger NULL; wall 18.104778060초에 완료 |
| hard watchdog | 실제20wall초 유지; child 완료 시 약1.895222초 여유, timeout 연장·해제 없음 |
| 정상 process 종료 | driver0 / observer0 / Kit0; 강제종료·사용자 process 중지 없음 |
| 전체 runner | **FAIL/NOT_READY, exit1**; 아래 판정 순서 오류 |
| 연구 denominator | 0; Full E2E/autonomy NOT_YET_VALIDATED |

Physical 시간은 SimulationManager 및 실제 PhysX callback953회·dt합 **15.883334162초**, manager step953과 일치한다. 최종 관측 KST **2026-11-01T16:29:01.857321+09:00**, pulse wall 시작 **2026-11-01T16:28:10.608674+09:00**. 최종 quiet는 단순 wall sleep이나 frozen pose 재생이 아닌 live 물리 표본이다. Child 완료 후 기존480tick 정지 관찰도 수행했다.

## 안전과 원본 보존

fresh prepare/corridor PASS, 실제 support **2214/2214**, shell rays **9/9**, 여섯 wheel contact 확인. 기존 .10m clearance와 속도·yaw·위치 envelope 및 ROS endpoint GID guard를 유지했다. 허용 rover/support 밖 접촉 **0**, 주행·정지 shell point1398개 최소 separation **+0.082015775m**, 최대 impulse **0Ns**. 물리 접촉 안전 PASS이며 장애물 충돌이나 shell 침투/하중은 관측되지 않았다.

기존 `stage_metrics_1m_z.usda`의 실제 construction site·pallet·HR cement brick scene과 동일 rover를 새 overlay로 구성했다. Geometry source의 1m/Z·active Render assert와 기존 graph validation을 통과했다. 새 floor·controller·teleport·HPO·YOLO/B4/B5·연구 실험 없음. 원본 USD와 기존 v01–v08/offline v09 결과는 쓰기 대상으로 사용하지 않았다. Prepare가 기록한14개 입력 SHA256은 실행 후 모두 동일 PASS, 실행 코드 snapshot과 hash를 새 output에 보존했다. 이는 원본 전체 USD dependency closure나49/53파일의 새 전수감사 주장이 아니다.

## 전체 FAIL의 한 원인: cleanup marker를 cleanup 전에 요구

`scripts/construction_site_drive_session_20261101_v09.py:354`의 `ok`에는 `(O/'zero_published.json').exists()`가 포함된다. 이 파일은 observer가 `zero_request.json`을 받은 뒤 생성한다. 정상 handshake 경로에서는 요청을 보내지 않고, 뒤의 `finally` cleanup(:371)에서 처음 요청한다. 따라서 정상 이동·quiet·child 종료 후에도 해당 성공 predicate는 아직 FALSE다.

실제 마지막 sample wall **1793518141.8573213**, cleanup 요청 **1793518141.8685927**, observer marker **1793518141.8759668** 순이다. `lifecycle_confirmed=true`, 최종 confirmed_stop 재평가 TRUE, 비영45·wheel 반응·quiet·zero 측정·driver state·fault 부재는 모두 충족했고, marker만 평가 뒤 생성됐다. Native Kit exit0과 내부 NOT_READY를 받은 wrapper는 exit1로 보존한다. 후처리로 원시 status를 PASS로 변경하지 않았다.

이는 v08의 late watchdog fault가 재발한 것이 아니다. v09 child 정상 완료는 이번에 실제 입증됐지만 전체 집계는 여전히 실패다. `abort_motion`/`zero_request`의 최종 존재는 정상 child 종료 후 cleanup이 남긴 것이며 active fault 증거가 아니다. CPU8/8 PASS가 이 process 간 파일 생성 순서를 검증하지 못했다.

다음 구체적 조치는 **정상 child 종료 후 cleanup-zero receipt를 확인한 다음 최종 성공 집계를 수행하도록 순서 한 곳을 수정**하는 것이다. active watchdog/endpoint/contact/quiet 검사를 우회하거나 marker 조건을 단순 삭제하는 방향은 아니다. 이번에는 수정 코드·추가 planner·새 validation 체계·재실행을 만들지 않았다. 명시된 실제1회 예산은 소진했다.

## 명령·산출물·검사

```bash
python3 scripts/construction_site_drive_runner_20261101_v09.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v09_runtime_01
python3 scripts/construction_site_drive_runner_20261101_v09.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v09_runtime_01
python3 -m unittest discover -s tests -p test_construction_site_drive_lifecycle_20261101_v09.py -v
```

prepare exit0, CPU8/8 PASS, 실제 물리 이동·정지·안전 PASS, 정상 driver lifecycle PASS, 전체 runtime FAIL/NOT_READY다. 재실행0. 종료 후 Kit/drive/training process0, GPU compute는 기존 rustdesk535MiB만 남았다. `.git` 없는 경로여서 git status exit128; stage/push 없음.

외부 evidence root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v09_runtime_01`. `prepare.json`, `code_versions.json`, `executed_code/`, `measurement_summary.json`, `run_status.json`, `runtime.log`와 `attempt_0001/`의 `steps.jsonl`, `physics_steps.jsonl`, `adapter_commands.jsonl`, endpoint forensic JSONL, `stop_confirmed.json`, `calibration_ros_complete.json`, `zero_request.json`, `zero_published.json`, `contacts.json`, `stop_quiet_result.json`, `owned_processes.json`, `execution_complete.json`을 보존한다. 새 runtime 출력만 생성했으며 코드 변경0. 보고서·latest mirror·PROJECT_STATE를 갱신했다.
