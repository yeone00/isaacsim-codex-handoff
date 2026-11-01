# 현장 drive v09 — post-zero 종료 수명주기 수정 (offline)

2026-11-01 KST. **v09 코드·CPU 검사 PASS, runtime NOT_TESTED.** Kit/ROS 실행·추가 물리 주행·prepare/새 USD 생성은 하지 않았다. v08의 실제 ROS 이동 +Y 0.021970748901m와 물리 정지 PASS, 전체 NOT_READY/runner exit1을 그대로 보존한다. .05m waypoint 도달이나 Full E2E 성공으로 해석하지 않는다. HPO/training PAUSED, 연구 denominator 0.

## 원인 범위와 실제 시각

원자료 root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v08/`. `adapter_commands.jsonl`, `run_status.json`, `stop_quiet_result.json`, `execution_complete.json` 및 discovery/pulse/driver 완료 기록을 직접 읽었다.

- 정상 감속 sim6.433333669 → 첫 zero sim6.683333682 → 최초 fault sim8.383333771, reason EMERGENCY_ZERO.
- 최초 fault wall1793516952.7942958은 pulse 시작 후 **19.873876572초**, 첫 discovery 관측 후 **20.276896477초**다. discovery의 wait_s를 합친 child 경과 추정은 **20.334500880초**다. 최초 fault의 feedback age는 **0.001709461초**다.
- v08 ROS child는 discovery를 포함한 wallstart 기준 `>20`을 emergency로 넣는다. 따라서 이 시각에는 **child wall watchdog 조건이 실제로 참**이며, session의 pulse 기준 20초 조건은 아직 거짓이다. Session은 루프 종료 시 무조건 abort/zero를 요청하는 별도 경로도 갖는다. Adapter 정지 관찰 timeout 8sim초는 이 최초 fault에서 아직 해당하지 않는다.
- 과거 로그는 hard 조건의 세부 trigger를 저장하지 않았다. watchdog은 source와 시각으로 설명되는 실제 활성 조건이지만, 그 순간 abort 파일도 동시에 존재했는지는 **UNKNOWN**이다. stale feedback이나 새로운 충돌을 원인으로 주장하지 않는다. 기존 cleanup이 덮어쓴 zero_request는 최초 abort 시각 증거가 아니다.

## 작은 변경과 완료 조건

v08에서 파생한 새 runner/session/ROS v09 3개와 순수 Python helper 1개만 실행 경로에 추가했다. 원래 graph·guard·adapter/controller·물리 안전 검사와 연구 threshold는 수정하지 않았다.

Session은 pulse 이후 실제 base 변위(기존 MOVED 기준 >.002m), nonzero 명령, BRAKING→ZERO_SETTLING 순서, fault 부재, zero 이후 연속 **최소1sim초**의 기존 raw COM/origin/FD·pose quiet 검사(.002m/s, .002m span, 최대 sample 간격 .1s), 해당 창의 graph wheel 및 두 wheel controller velocity zero를 함께 확인한다. 기존 contact/endpoint/clock/envelope 검사를 통과한 tick에서만 `stop_confirmed.json`을 쓴다. Baseline quiet나 바퀴 회전만으로는 완료하지 않는다.

Child는 기존 guard와 20wall초 watchdog·feedback age·abort 검사를 먼저 적용한 뒤, fresh certificate와 자기 ZERO_SETTLING 상태가 맞을 때만 정상 완료를 수락한다. Final zero20회를 발행하고 실제 소유 child가 exit0한 것을 session이 확인한 뒤 기존 480tick 정지 관찰과 cleanup으로 진행한다. 이 후속 관찰에서도 안전/quiet 실패는 NOT_READY다. 완료 확인 전에 발생한 watchdog·lost/stale command·안전/정지 실패는 emergency-zero와 실패를 유지한다. Watchdog/adapter stop timeout을 늘리거나 제거하지 않았다. Cleanup graph zero 오류도 NOT_READY로 남긴다.

새 ROS 로그에는 각 command의 hard_trigger/wall_elapsed_s, 최초 hard trigger의 wall/sim 시각, adapter_fault, completion_accepted를 기록한다. 새 prepare hash 입력에 helper도 포함했다. 기존 native fallback 코드는 변경·실행하지 않았다.

Runner 최상위 MOVED/STOPPED는 nested 측정 결과를 반영하고 adapter_fault를 별도로 보존한다. 이동·quiet PASS여도 fault나 process 실패, nested NOT_READY를 전체 PASS로 올리지 않는다. v08 자료의 offline 집계는 **MOVED YES / STOPPED PASS / NOT_READY / FAULT_LATCHED_REASON_UNRECORDED**다. 역사 파일은 갱신하지 않았다.

## 검사와 보존

**PASS:** CPU unittest 8개 — 정상 zero+quiet 완료, 실제 adapter 정상감속, active watchdog emergency latch, stop-observation timeout, safety/quiet/graph 실패, base 비이동·감속 누락 거절, 완료보다 fault 우선, nested 집계 및 source 연결 검사. 새 Python 파일5개 py_compile PASS. 테스트 최초 실행은 fixture의 wall_s 누락으로 4 errors/exit1이었으며 fixture 보완 뒤 8/8 PASS다. 이 실패를 runtime 실패나 성공으로 재분류하지 않는다.

v08 telemetry의 읽기 전용 prefix 재생에서 최초 완료 조건 충족은 **sim7.733333737 / wall1793516949.429641**, 최초 fault보다 **3.364654779wall초 앞**이다. 최종 fault까지 포함한 전체 재생은 완료 거절로 유지했다. 이는 과거 자료에 대한 offline 결과이며 v09 child handshake/runtime 성공 증거가 아니다.

v08 소스3개·역사 보고서·frozen guard·v08 JSON/command 원자료 등 **49파일의 작업 전후 SHA256 동일 PASS**. 전체 v01–v08 데이터나 USD dependency closure를 새로 전수 감사한 것은 아니다. 원본 USD·benchmarks·weights·기존 결과에 쓰기 작업 없음. 실제 코드 SHA/시각/집계/검사 범위는 [검사 증거 JSON](construction_site_drive_lifecycle_checks_20261101_v09.json)에 기록했다.

검사 명령 (system Python, 과학 패키지 설치 없음):
```bash
python3 -m unittest discover -s tests -p 'test_construction_site_drive_lifecycle_20261101_v09.py' -v
python3 -m py_compile scripts/construction_site_drive_runner_20261101_v09.py scripts/construction_site_drive_session_20261101_v09.py scripts/construction_site_drive_ros_20261101_v09.py evaluation/construction_site_drive_lifecycle_20261101_v09.py tests/test_construction_site_drive_lifecycle_20261101_v09.py
```

변경 파일: `scripts/construction_site_drive_{runner,session,ros}_20261101_v09.py`, `evaluation/construction_site_drive_lifecycle_20261101_v09.py`, `tests/test_construction_site_drive_lifecycle_20261101_v09.py`, 이 보고서·검사 JSON, `reports/latest_report.md`, `docs/PROJECT_STATE.md`.

## 다음 별도 작업

**v09 runtime NOT_TESTED**, 실제 handshake·실시간 처리 여유·정상 종료는 다음 한 번의 실행에서 확인해야 한다. 기존 engineering field/corridor와 기존 ROS graph를 사용하는 별도 one-shot waypoint A→B 시험을 제안한다. 새 unused output에 명령→graph→wheel→실제 base 변위→정상 감속→zero→quiet→child 종료를 기록하고 목표 도달과 기본 이동/정지를 구분한다. 이번 작업은 그 실행을 시작하지 않았다. 이후 fresh RGB-D→YOLO→B4/B5 연결과 최종 실험을 단계적으로 진행한다. 지금은 HPO·B300·Full E2E324/432·대규모 추가 검사 없음. v07 익명 GID는 계속 UNKNOWN이다.
