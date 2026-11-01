# 현장 drive cleanup 순서 수정 v10-A — 2026-11-01

판정: 소스 수정 및 CPU 검사 PASS. v10 물리 주행 / Isaac Kit / ROS drive / prepare / HPO / training / 324·432 E2E 모두 NOT_RUN. HPO PAUSED, 연구 denominator 0.

## 수정 내용

v09 session의 모듈 본문 ROS 정상 종료 분기(line 354)는 finally(line 371)의 cleanup 요청으로 생성되는 zero_published.json을 먼저 요구했다. v10은 기존 gracefulness·physical quiet·이동·wheel response·adapter/guard 조건을 success_candidate로 보관하고, finally에서 한 번만 cleanup 요청을 보낸다. observer가 보낸 실제 영수증을 최대 3초 기다린 뒤 count≥10, v=w=0, domain 일치, 요청 이후부터 현재까지의 유한 wall_time을 검사한다. observer 종료 요청은 이 검사 뒤에 보낸다.

child/observer exit0, 강제 종료 없음, graph/native cleanup 및 Kit close 오류 없음까지 확인한 뒤 최종 성공 여부와 execution_complete.json을 기록한다. runner는 session 종료 뒤 기존 aggregate로 run_status.json을 작성한다. abort 신호는 별도로 latch하며, cleanup 도중 외부에서 바뀐 zero_request도 실패로 처리한다. cleanup이 만드는 abort marker 자체와 외부 abort를 구분한다. 사전 fault/abort/zero request는 cleanup 영수증으로 성공으로 승격되지 않는다.

v09 원본은 수정하지 않았다. v10 runner를 새로 만들어 v10 session과 helper를 prepare hash 대상에 포함했다. ROS child와 observer는 기존 v09/v02 소스를 그대로 사용하므로 ROS companion 변경은 없다. controller/guard/physics/velocity/task 수치와 480 tick 관찰은 유지했다.

## 정확한 변경 위치

- `scripts/construction_site_drive_session_20261101_v10.py:17` — `def request_abort`
- `scripts/construction_site_drive_session_20261101_v10.py:358` — `  ok=graceful`
- `scripts/construction_site_drive_session_20261101_v10.py:359` — `  success_candidate=ok`
- `scripts/construction_site_drive_session_20261101_v10.py:371` — `finally:`
- `scripts/construction_site_drive_session_20261101_v10.py:379` — ` cleanup_requested=`
- `scripts/construction_site_drive_session_20261101_v10.py:390` — ` cleanup_receipt=await`
- `scripts/construction_site_drive_session_20261101_v10.py:425` — ` owners_clean=`
- `scripts/construction_site_drive_session_20261101_v10.py:426` — ` result['status']='ENGINEERING_RECORDED' if final_success`
- `evaluation/construction_site_drive_cleanup_20261101_v10.py:7` — `def await_zero_receipt`
- `evaluation/construction_site_drive_cleanup_20261101_v10.py:30` — `def final_success`
- `scripts/construction_site_drive_runner_20261101_v10.py:54` — `  cmd=[PY`
- `scripts/construction_site_drive_runner_20261101_v10.py:33` — `  c=json.loads`

## SHA256 (로컬 실제 파일)

| 파일 | SHA256 |
|---|---|
| `scripts/construction_site_drive_session_20261101_v09.py` | `66e74ea132b4ab45a3a47d576efac470577db0438b3d44bb732e7a44ffccd59f` |
| `scripts/construction_site_drive_session_20261101_v10.py` | `8b0ce6b49c84c4da9d71e11dbb5ca38730cd81470bc3d0ab57780b05364234f1` |
| `scripts/construction_site_drive_runner_20261101_v09.py` | `8fd132a0573555b0bb37b44d36ad07ded1d16f215a81965bc93dd492731c78b4` |
| `scripts/construction_site_drive_runner_20261101_v10.py` | `ce035de1cd0c6869bae44c203fb851a1b373b3105a17379a925635553dd412f0` |
| `scripts/construction_site_drive_ros_20261101_v09.py` | `bf7931222b26f8a966ab9580c5feafed012ee770ad6054949e8650d7f27b163c` |
| `evaluation/construction_site_drive_cleanup_20261101_v10.py` | `1a03662c3712c0f1a7f0589734dbf935085bc9cf1bae55b32239427a405be052` |
| `tests/test_construction_site_drive_cleanup_20261101_v10.py` | `ab9b65cec5cd5b34e6dce8e7536761a0739a9058028613c076d2bf75c0d52022` |

## 검사와 한계

- 환경: `/home/user/anaconda3/bin/python3`, Python `3.13.5`, `Linux-6.14.0-37-generic-x86_64-with-glibc2.39`. 표준 라이브러리만 사용.
- PASS: `python3 -m unittest discover -s tests -p 'test_construction_site_drive*20261101_v*.py' -v` — 11/11 (신규 3 + 기존 lifecycle 8), 최종 0.084초, exit0.
- PASS: `python3 -m py_compile scripts/construction_site_drive_session_20261101_v10.py scripts/construction_site_drive_runner_20261101_v10.py evaluation/construction_site_drive_cleanup_20261101_v10.py tests/test_construction_site_drive_cleanup_20261101_v10.py` — exit0.
- 신규 테스트: cleanup 전 marker 부재 재현 → 요청 후 지연 receipt → 정상 최종 성공; missing/malformed/stale/future/nonzero/wrong-domain/count 오류 거절; 기존 실패 후보·abort·process/cleanup fault 성공 승격 거절; AST로 cleanup→receipt→observer stop→owner 기록→Kit close→최종 판정→serialize 순서를 확인.
- 기존 lifecycle 검사에서 실제 adapter watchdog/stop timeout 및 physical/graph quiet 실패가 유지됨을 확인. 실행형 legacy Kit/ROS 모듈 import 없음.
- 보조 `git diff --stat` 명령은 이 디렉터리가 Git repository가 아니어서 exit129 실패했다. 이후 파일 직접 diff로 검토했다. `diff -u` exit1은 예상한 소스 차이를 뜻한다. staging/commit/push 없음.
- UNKNOWN: 실제 Kit·ROS에서 새 순서가 완료되는지. CPU fixture/AST는 실제 전달·물리 정지·운영체제 프로세스 종료의 runtime 인증을 대신하지 않는다. observer receipt는 기존 observer의 10회 zero 발행 증명이며 추가 subscriber ACK를 주장하지 않는다.
- 보존: v01–v09 결과 및 historic v09 runtime 보고서를 이번 작업에서 수정하지 않았다. v09 +Y21.505355835mm, STOPPED PASS, B50mm 미도달(잔여28.496601mm), runner NOT_READY라는 역사적 판정은 그대로다. 이 수치는 사용자 제공/기존 기록 맥락이며 이번에 runtime 로그를 재검사하지 않았다.

## 변경 파일 및 다음 작업

신규 session v10, runner v10, cleanup helper v10, regression test v10, 본 새 보고서. docs/PROJECT_STATE.md에 완료 기록 추가. 위 SHA256 표에 신규/원본 경로를 구분하여 기록했다.

다음 작업은 별도 승인 범위의 A→B 50mm 실제 목표 주행이다. 이번 패치는 그 실행이나 성공을 뜻하지 않으며 runtime NOT_RUN이다.
