# 현장 단일 로버 v05 — 실제 Kit 1회, PhysX 허용 바닥 hit 미확보로 이동 실패

2026-11-01 KST. 수정된 v04 코드 그대로 새 v05 출력에서 실제 실행했다. **MOVED NO / STOPPED NOT_TESTED / 비영 명령 0**. 이동 목표 미달이며 준비나 정지 결과를 이동 성공으로 판정하지 않는다. 연구 denominator 0, HPO PAUSED.

| 항목 | 실제 결과 |
|---|---|
| Kit / drive / retry | 1 / 0 / 0 |
| 최초 비영 명령·시각 | 없음 |
| base 순변위 / 첫 기록 대비 최대 XY 이동 | 0.000000000000 / 0.000000000000 m |
| 물리 시간 | 377 steps / 6.283333661035 s, dt .016666667536 s |
| 물리 시각 역행 | 0 |
| 통로 / graph admission | PASS / PASS |
| 여섯 바퀴 접촉 | 6/6 관측; 매 순간 모든 바퀴 하중 지지를 의미하지 않음 |
| 실제 PhysX support | FAIL: 2,214 표본 중 허용 바닥 hit 저장 0, 통과 0 |
| shell ray | 9/9 허용 바닥 hit 저장 없음, gap UNKNOWN |
| 내부 / Kit native exit / runner exit | NOT_READY / 0 / 1 |
| ROS driver admission | NOT_TESTED: 지지 검사에서 먼저 중단, driver 미생성 |
| 명령 후 zero / stop hold / 목표 오차 | NOT_TESTED / NOT_TESTED / NOT_ASSESSED |

정확한 실패는 `STATIONARY_PHYSX_SUPPORT_FAILED`(session line177)다. 이전 tilted-axis 표본0 문제는 이번에 재현되지 않았고, 2,214 표본이 생성되어 analytic per-collider corridor PASS 후 실제 query까지 도달했다. 그러나 wheel 및 shell 콜백이 허용 support path와 일치하는 hit만 저장하므로, **현재 빈 hits는 query 자체가 아무것도 맞히지 않았는지, 다른 path의 hit가 필터됐는지 구분할 수 없다.** 실제 지면 부재나 위험 침투가 확정된 것은 아니다. query 반환 bool·필터 전 hit는 UNKNOWN이다. 정상 지지를 인증하지 못한 상태에서 안전 검사를 우회하지 않았다. 두 번째 launch·native 이동 branch 없음.

shell contact는 144점, 최소 separation 0.078864306211m, 최대 impulse 0.000000000000Ns다. baseline shell 점0, world bounds 하단 .065561256826m이며 실제 shell ray gap은 UNKNOWN이다. 정지 접촉 기록에 침투·하중 증거는 없으나 동적 dragging은 NOT_TESTED다. baseline quiet PASS(최종1.000000052s, COM peak .000388869344m/s, origin .000394139814m/s, FD0)는 주행 후 정지 검증이 아니다. 이 strict quiet는 기존 코드에 남아 있었고 이번 실행에서는 통과해 중단 원인이 아니었다. 기존 task 30mm/2° 판정은 도달하지 않았다. 연구 protocol은 변경하지 않았다.

ROS observer만 실행되어 정상 exit0, driver는 null이다. endpoint/publisher 원본은 `ros_status.json` 및 observer 출력에 보존했다(파일 목록은 출력 폴더 참조). ROS publisher 오류는 관측되지 않았으며 admission 성공도 주장하지 않는다. cleanup zero request wall timestamp 1793513989.2622912은 요청 기록이며 실제 ROS zero 발행 증거가 아니다. timeline pause와 graph velocity/effort zero cleanup을 수행했고 command 이후 hold는 없었다. 원래 첫 비영 명령은 존재하지 않으므로 재구성하지 않았다.

**최소 수정 제안 1개:** 다음 버전에서 두 raycast callback의 필터 **이전** 원시 hit(collider path·position·normal·distance)와 `raycast_all` 반환 bool을 함께 저장한다. 허용 support 필터와 충돌 안전 기준은 유지한다. 설치된 binding은 `bothSides=False` 기본값을 명시하지만 이번 증거로 winding 원인을 단정하거나 양면 query를 해결책으로 확정하지 않는다. 현재 코드는 수정하지 않았다. 이 한 가지 계측 수정 후의 단일 실행이 다음 구체적 행동이며 이번에는 추가 실행하지 않았다.

실제 명령:
```bash
python3 scripts/construction_site_drive_runner_20261101_v04.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v05
python3 scripts/construction_site_drive_runner_20261101_v04.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v05
```

사전 Kit/HPO 없음, GPU compute는 기존 rustdesk535MiB만 있었다. prepare PASS 후 기존 hh_isaac51 Python/Isaac Sim5.1 runtime을 정확히 한 번 실행했다. 새 출력 `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v05`. 원본 scene `stage_metrics_1m_z.usda`와 고정 controller/guard/기존 결과 보존 검사 PASS(51 inputs). 기존 v04 실행 당시 코드와 수정 후 코드는 아래처럼 구분한다. 이번 실행5개 SHA는 이전 `post_run_static_revision_code`와 모두 일치한다.

| 파일 | 원래 v04 Kit 실행 SHA256 | 이번 수정본 SHA256 |
|---|---|---|
| construction_site_drive_evidence_20261101_v04.py | UNKNOWN — 당시 실행 snapshot 없음 | 9f296f052947a855f140d5d93de85384de4757ccd479bcae695a7d2b41411562 |
| construction_site_drive_geometry_20261101_v04.py | 4c356e2ef9fdb508a984a140af991a06275f28c9a1295a46ebef292281bc92f3 | aa8fad4b175043b118b3fd44eebbbc1010dcf443e9fce2e978d8aa8adf1e78a9 |
| construction_site_drive_geometry_checks_20261101_v04.py | UNKNOWN — 당시 실행 snapshot 없음 | 804fc4d0eb1c3bedc9b5c7365306dbdd996525b51597c00313068d34eab41e85 |
| construction_site_drive_runner_20261101_v04.py | 437048058f963a564befeaa48aef5c89cd60a12cbd4b033bc7432567a81c7ef8 | 437048058f963a564befeaa48aef5c89cd60a12cbd4b033bc7432567a81c7ef8 |
| construction_site_drive_session_20261101_v04.py | a2b6982c33ad42727cb5372b23fd76df49f5cc8ca0979991498b6a6d3716db22 | bbffd26cebc667a2c8999a351e6f79917865f1c1b05957bcd6e3469ce90a4e4c |

증거: `prepare.json`, `provenance.json`, `run_status.json`, `measurement_summary.json`, `runtime.log`; attempt 내부 `physics_steps.jsonl`, `steps.jsonl`, 새 `root_trajectory.csv`, `collision_preflight.json`, `stationary_PhysX_support.json`, `shell_contact_diagnosis.json`, `contacts.json`, `runtime_summary.json`, `execution_complete.json`, `zero_request.json`, `owned_processes.json`. 렌더/clip은 생성하지 않았다. 이동 전 physics195개 telemetry를 보존했으며 terminal 실패를 분모에서 숨기지 않았다(별도 engineering attempt1, 연구분모0).

변경 파일은 이 보고서, latest_report mirror, PROJECT_STATE 추가 기록이며 코드 변경0이다. terminal 검사 중 runtime.log 생성 전 tail 1회 exit1도 있었으나 재실행을 유발하지 않았다. Full E2E·training·HPO·B300·Qual12·432·새 scene·EngineeringFloor·teleport 없음. 최종 논문용 perception→pose→approach/align 및 strict task 성공은 별도 미검증이다.
