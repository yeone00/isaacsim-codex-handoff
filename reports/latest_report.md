# 기존 construction site 원래 B 목표 주행 v10-B — 2026-11-01

실제 Kit 1회·ROS 저속 episode 1회·재시도 0회. **B_REACHED YES, MOVED YES, STOPPED PASS, 전체 runner FAIL(exit1)**. HPO/training PAUSED, 연구 denominator 0. v09의 미도달 및 cleanup 순서 실패 기록은 수정하지 않았다.

## 실제 측정

| 항목 | 결과 |
|---|---|
| NONZERO Twist | 74회 |
| initial XY world m | [-25.887977600097656, 28.470867156982422] |
| final XY world m | [-25.887977600097656, 28.52072525024414] |
| ORIGINAL B world m | [-25.88797768, 28.520869113267] |
| 실제 순변위 | 49.858093262mm |
| 원래 B까지 최종 거리 | 0.143863045mm |
| B_REACHED | YES, 사전 선언 Euclidean 5mm 이내 |
| MOVED / STOPPED | YES / PASS |
| 최종 quiet | sim 16.266667515039444–17.266667567193508, 1.0000000521540642 physical초 |
| zero receipt | count10, v=w=0, domain191, 요청 이후 실제 wall timestamp 확인 |
| 종료 | driver0 / observer0 / Kit0 / runner1 |
| runner | FAIL: execution_complete.json 없음 |
| safety | 예상 밖 접촉 0; 주행 shell 1920 points, 최소 separation 0.08201577514410019m, 최대 impulse 0.0Ns |
| faults | driver adapter_fault=None, hard_trigger=None; completion_accepted=True |

정지 증거는 live PhysX/SimulationManager 물리 시간 및 위치 표본이다. graph wheel target과 wheel controller zero를 포함한 stop_confirmed.json도 존재한다. 최종 quiet 기준은 기존 속도≤.002m/s, pose span≤.002m, ≥1초 유지다. 최종 quiet 상세: `{"status": "PASS", "criteria": {"coverage_s": 1.0, "max_dt_s": 0.1, "span_m": 0.002, "speed_m_s": 0.002}, "start_sim_s": 16.266667515039444, "end_sim_s": 17.266667567193508, "coverage_s": 1.0000000521540642, "max_dt_s": 0.01666666753590107, "max_raw_COM_m_s": 0.0006907683005902118, "max_root_origin_m_s": 0.0006844824186411379, "max_FD_m_s": 0.0, "pose_span_m": 0.0}`. 최대 planar 속도 0.021711930243831726m/s로 기존 .03m/s pulse cap 미만이다. collision preflight 및 support admission PASS. 원본 supplier Action Graph·/rover/cmd_vel·wheel controllers 경로이며 native fallback은 새 경로에서 명시적으로 금지했다.

## 최소 확장과 제한

새 runner/session/ROS v10B 및 evaluation target helper를 추가했다. live world base pose를 engineering 제어 입력으로 명시 사용한다. 연구 perception 입력/GT 없는 Full E2E 검증이 아니다. 원래 B는 고정했고 +Y remaining≤3mm이면 기존 StoppingAdapter BRAKING을 latch한다. 이동 요청 .02m/s 및 기존 governor/감속/속도·yaw·접촉·endpoint guard는 보존했다. 기존 40mm diagnostic travel abort는 이 50mm 목표와 양립하지 않아 새 버전에서 65mm 유한 한계로 변경했다. 기존 corridor가 -50~+150mm를 검사하므로 이 한계는 검사 범위 안이다. 새 planner·robot·floor·원본 USD 변경·teleport·base pose 직접 설정 없음. 기존 derive가 실행별 overlay를 생성하는 경로를 그대로 사용했다.

v09의 시작 포함20wall초 대신 startup8초, 이동60wall초 및10sim초, 정지20wall초를 선언했다. stale feedback .5초·supervisor abort는 중복 step 대기보다 먼저 zero+abort한다. 기존 adapter의8sim초 정지 timeout과 독립 물리 quiet 조건도 유지했다. session 전체 active85wall초/22sim초, child 전체95wall초, runner180초 abort/210초 소유 process 강제종료 backstop을 유지했다. timeout은 성공으로 승격하지 않는다. 실제 driver 완료 wall 25.49363174199243초, normal brake sim 7.900000412017107, zero sim 8.150000425055623다.

## 실제 드러난 최종 저장 실패

v10-A corrected cleanup 순서를 계승해 zero_request→observer zero receipt→observer stop→owned process exit 기록까지 실행됐다. receipt wall 1793519989.493466, request wall 1793519989.489242; 두 ROS child exit0이다. 그 뒤 runtime.log의 `Simulation App Shutting Down`, Kit exit0이 있으나 app.close 뒤의 최종 집계/serialize에 도달한 증거가 없고 execution_complete.json이 없다. 따라서 메모리 안 cleanup_receipt.valid 및 session 최종 candidate는 UNKNOWN이다. 실제 파일의 receipt 필드는 독립적으로 재확인했다. runner 원시 기본 MOVED NO/STOPPED NOT_TESTED는 결과 파일 load 이전 기본값이며 실제 steps/stop evidence와 구분한다. 원시 run_status.json은 수정하지 않았다.

로컬 SimulationApp.close 소스 `.../isaacsim/exts/isaacsim.simulation_app/isaacsim/simulation_app/simulation_app.py:763`은 shutdown_and_release_framework()를 호출한다. 이 런타임에서는 close 이후 저장에 의존할 수 없다는 증거다. CPU fixture는 이 Kit 종료 동작을 인증하지 못했다. 카메라/재질의 reference scope warning도 runtime.log에 남아 있으며 이번 작업에서 원본을 수정하지 않았다.

다음 구체적 조치는 **별도 새 버전에서 close 이전 provisional 결과를 저장하고, Kit가 종료된 뒤 외부 runner가 exit code와 receipt/child 증거를 검증해 최종 결과를 작성**하는 것이다. 이번 single-session 예산은 소진했으며 재실행/원시 결과 사후 PASS 변경은 하지 않았다.

## 검사·파일·재현

- PASS: 새 실행 소스 py_compile; 기존 cleanup/lifecycle CPU11/11 및 신규 target/phase 검사2/2. legacy 실행 모듈 import 없이 검사했다.
- PASS: prepare corridor 및 resource gate(Kit/training 없음; 기존 rustdesk535MiB만 GPU 사용). 실행 후 prepare 입력 21개 hash 모두 동일. 전체 연구 lock/asset dependency closure 재감사 주장은 아니다.
- 실제 실행: prepare exit0, Kit exit0, runner exit1. 실제 이동/도달/정지 PASS와 전체 FAIL을 분리한다.
- 신규 코드: scripts/construction_site_drive_runner_20261101_v10B.py, scripts/construction_site_drive_session_20261101_v10B.py, scripts/construction_site_drive_ros_20261101_v10B.py, evaluation/construction_site_target_20261101_v10B.py, tests/test_construction_site_target_20261101_v10B.py.
- 문서: 본 보고서, latest_report.md, docs/PROJECT_STATE.md. 기존 v01–v10-A 소스/보고서 보존, staging/push 없음.

```bash
python3 -m py_compile scripts/construction_site_drive*20261101_v10B.py evaluation/construction_site_target_20261101_v10B.py
python3 -m unittest discover -s tests -p 'test_construction_site_drive*20261101_v*.py' -v
python3 -m unittest discover -s tests -p 'test_construction_site_target_20261101_v10B.py' -v
python3 scripts/construction_site_drive_runner_20261101_v10B.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_TARGET_DRIVE_20261101_v10B_01
python3 scripts/construction_site_drive_runner_20261101_v10B.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_TARGET_DRIVE_20261101_v10B_01
```

증거 root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_TARGET_DRIVE_20261101_v10B_01`. prepare.json 입력 hash/command, code_versions.json 환경/hash, executed_code snapshot, runtime.log, run_status.json, measurement_summary.json, attempt_0001의 원시 steps(854행)/physics_steps/adapter_commands(95행)/contacts/support/stop_confirmed/stop_quiet_result/zero_request/zero_published/owned_processes를 보존한다. execution_complete.json 부재 자체가 실패 증거다. diff exit1은 예상 소스 차이이며 테스트 실패가 아니다.

YOLO/B4/B5·HPO·B300·324/432 E2E 미실행. engineering world pose feedback 성과를 연구/실물 로봇 validation으로 일반화하지 않는다.
