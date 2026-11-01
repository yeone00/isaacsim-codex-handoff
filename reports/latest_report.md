# 현장 perception → PRE → FINAL v18 — 2026-11-01

**전체 NOT_READY. PRE 도착 NO, FINAL 도착 NO.** 새 계측·ZERO-ONLY 정지 복구를 구현하고 실제 Kit 2회를 수행했다. 첫 실행에서 TF_STALE 직전 actor 검사 0.488초의 CPU 지연을 특정했고, 실제 비상 zero 이후 새 물리 샘플로 quiet PASS를 입증했다. 변경 통지 기반 actor 검사로 수정한 두 번째 실행은 TF_STALE 없이 0.887m 이동했으나 기존 follower의 GOAL_OVERSHOOT로 종료했다. 두 번째 실행의 주행 후 quiet는 FAIL/미입증이다. 추가 Kit 0회이며 허용된 첫 실행+원인이 확인된 수정 실행 1회의 한도를 모두 사용했다. HPO/training PAUSED, 연구 denominator0, confirmatory/432 실행0.

## 실제 실행과 관측

README, PROJECT_STATE 최신 v17, PROTOCOL_LOCKS, v17 보고서와 실제 v16b/v16/v15 소스를 읽고 진행했다. 실제 런타임은 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, Isaac Sim 5.1, ROS jazzy/domain191이며 perception은 기존 sdg_tools 환경이다. 설치·업그레이드 없음. 두 번 모두 다른 Kit/training·GPU 작업 부재와 domain isolation을 확인한 뒤 실행했다. 기존 rustdesk는 보존했다.

출력 root는 다음 두 개이며, 각각 `attempt_0001` 한 번만 사용했다.

- `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v18_01`: 새 v18 계측·정지 복구, 전체 actor 순회 유지.
- `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v18_02`: 새 v18b actor 증분 계산·GC/세부 IO 계측.

실행 명령은 각 root의 `prepare.json`, `code_versions.json`, `run_status.json`에도 보존했다.

```bash
python3 scripts/construction_site_perception_runner_20261101_v18.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v18_01
/home/user/anaconda3/bin/python3 scripts/construction_site_perception_runner_20261101_v18.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v18_01
python3 scripts/construction_site_perception_runner_20261101_v18b.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v18_02
/home/user/anaconda3/bin/python3 scripts/construction_site_perception_runner_20261101_v18b.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v18_02
```

각 실행에서 새 640×480 RGB-D, frozen HR YOLO, B4, 수동 ROI B5를 수행했다. 새 RGB와 overlay를 각각 직접 보고 `(236,197),(251,181),(383,181),(403,197)`의 팔레트 상면 ROI와 review를 이번 영상 hash에 결합했다. 같은 좌표의 과거 목표 재사용이 아니며 자동 팔레트 인식으로 주장하지 않는다. USD GT를 목표 생성에 넣지 않았다. checkpoint observed SHA256는 frozen `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`와 일치한다.

| 항목 | 실행 01: v18 | 실행 02: v18b |
|---|---|---|
| YOLO confidence | 0.656553984 | 0.698806345 |
| 관측 PRE XY(m) | −25.934824241, 28.278040457 | −25.934672961, 28.278040587 |
| 관측 FINAL XY(m) | −25.934824241, 29.078040457 | −25.934672961, 29.078040587 |
| PRE 곡선 collider sweep / live support | PASS / 24300/24300 | PASS / 24300/24300 |
| 실제 ROS 비영 발행 | 740 | 1097 |
| 실제 base 누적 경로 / 순변위(m) | 0.680531296 / 0.678295977 | 0.886907620 / 0.883784257 |
| Wheel peak abs dq(rad/s) | 2.202980757 | 1.123795033 |
| 실제 PRE 도착·정상 stop | NO | NO |
| 측정 PRE 최소 거리(m) | 0.201452729 | 0.008677044 |
| FINAL 경로 독립 검사 / 실제 도착 | NOT_RUN / NO | NOT_RUN / NO |
| 실제 차단 원인 | TF_STALE | GOAL_OVERSHOOT |
| Unexpected contact / drive shell 침투·하중 event | 0 / 0 | 0 / 0 |
| Fault 이후 새 물리 quiet | PASS, ZERO-ONLY 70 samples | 미입증, 새 samples0 / 최종 QUIET FAIL |
| 별도 cleanup 요청에 결합한 zero 영수증 | PASS | PASS |
| Driver / observer / Kit exit | 0 / 0 / 0 | 0 / 0 / 0 |
| Outer final / runner exit | NOT_READY·MISSING_WITNESS / 1 | NOT_READY·MISSING_WITNESS / 1 |

PRE 성공에는 기존 5mm 위치·2° yaw 및 물리 stop 증명이 필요하다. 두 번째 실행의 최소 거리 8.68mm도 이 조건을 만족하지 않는다. 두 실행 모두 PRE/FINAL 정상 stop certificate가 없으며 provisional eligibility=false다. Kit exit0을 task 성공이나 runner 성공으로 바꾸지 않았다.

## 지연 계측과 확인된 원인

새 timing helper는 `time.monotonic_ns()`의 구간 시작·종료와 가능한 구간의 `thread_time_ns()` CPU 시간을 메모리 배열에 저장하고 exit 때 JSON으로 flush한다. 파일 안의 단위·열 정의도 기록했다. 기존 forensic 기록과 fsync는 제거하지 않았다. TF stamp, wall timestamp, freshness 0.5초 wall / 0.1초 sim도 변경하지 않았다. 가짜 heartbeat가 없다.

세분화한 항목은 graph fingerprint 순회·비교, actor 검사, 새 contacts/support 처리, endpoint snapshot read 및 실제 identity/TF 검사, forensic open/JSON 직렬화/write/flush/fsync/close, physics app.update, update 이후 readback/직렬화가 포함된 구간, tick 전체 및 tick 사이 기타 작업이다. v18b의 전체 pre-update guard와 내부 구간의 차이에는 observer/driver 상태 확인·파일 존재 검사 등 짧은 기타 작업과 계측 비용이 포함된다. 각 구간 시작·종료를 보존해 미계측 잔여 시간을 원인으로 감추지 않는다. Observer는 callback 실제 수신 MONOTONIC 시각과 해당 TF의 atomic replace가 반환한 완료 시각을 따로 기록한다. Endpoint inventory의 wall_s는 TF 수신으로 갱신하지 않는다. Driver의 ROS snapshot read도 별도 계측한다.

실행01 fault 직전 MONOTONIC ns 구간:

| 구간 | 시작 → 종료(ns) | wall / thread CPU |
|---|---|---|
| graph 순회 | 156383149080857 → 156383156958972 | 7.878 / 7.878ms |
| actor 전체 검사 | 156383158165076 → 156383646352688 | **488.188 / 487.891ms** |
| endpoint snapshot read | 156383646463110 → 156383646573012 | 0.110 / 0.110ms |
| 실제 endpoint 검사(직렬화·fsync 포함), TF_STALE | 156383646613125 → 156383647573725 | 0.961 / 0.343ms |

이 실행의 graph 순회 최대10.554ms, session fsync 최대7.225ms, TF 수신→atomic publication 완료 최대0.724ms였다. fault 구간의 실제 긴 CPU 지연은 actor 검사 안에서 발생했다. 이 구간을 OS 대기나 observer 게시 지연으로 해석할 근거는 없다. 다만 첫 실행에는 GC callback이 없어 **actor 내부의 어느 세부 연산/GC가 488ms를 썼는지는 UNKNOWN**이다. v17도 같은 내부 원인이었다고 소급 확정하지 않는다.

실행02는 actor 검사를 바꾼 뒤 driver TF age 최대0.484270573초, sim 차이 최대0.016666668초로 이번 bounded 구간의 TF 검사를 통과했다. 그러나 timing stall 자체가 완전히 해결된 것은 아니다.

| 실행02 계측 | p50 | 최대 |
|---|---:|---:|
| actor 증분 검사 | 1.195ms | 53.274ms |
| graph 순회 | 8.020ms | 10.891ms |
| graph 비교 | 1.203ms | 449.714ms |
| 전체 pre-update guard | 11.870ms | 460.266ms |
| session forensic fsync | 0.707ms | 6.896ms |
| TF 수신→atomic publication 완료 | 0.232ms | 0.609ms |
| driver ROS snapshot read | 0.051ms | 0.351ms |

최장 guard `156744701304971 → 156745161571031ns` 안에 GC generation2가 `156744708972981 → 156745157420895ns`, wall448.448ms/threadCPU448.402ms로 정확히 포함됐다. 이는 graph 비교 구간 내부의 실제 Python 전체 GC 지연이다. **두 번째 실행의 긴 stall에는 GC가 관여했다는 직접 증거가 있다.** 첫 actor 지연도 GC였다는 주장은 여전히 추정에 머문다. `.484s < .5s`였다는 단일 결과로 앞으로의 freshness 안전 여유가 충분하다고 주장하지 않는다. GC 비활성화·timeout 연장·위조 TF는 적용하지 않았다.

전체 app.update 최대422.904ms는 startup 등 모든 phase를 포함한 값이다. 실제 pulse app.update 최대29.463ms이며 분리해 해석해야 한다. tick 사이 최대46.270초도 멈춘 fresh capture·수동 검토·경로 검사를 포함하므로 active guard stall로 해석하지 않는다. 원시 구간은 `session_timing_v18.json`, `observer_timing_v18.json`, `driver_timing_v18.json`, 집계는 각 root의 `timing_summary_v18.json`에 보존했다.

## 변경 계산의 안전 범위

실행02의 `ActorCache`는 USD `ObjectsChanged` 통지를 사용한다. 기존 prim에 변경이 있으면 그 prim에 **원래 actor_signature 함수 자체**를 적용해 schema, enabled 속성, 모든 관계 및 script hook을 다시 검사한다. 속성명별 무시 allowlist는 없다. prim 추가·삭제·resync 또는 알 수 없는 traversal 변경은 전체 순회로 되돌린다. 검사 중 재변경·알 수 없는 traversal 상태는 실패한다. 변경 통지 객체를 유지하고 초기 cache와 전체 signature의 일치도 확인한다.

원래 graph 전체 순회와 v15 baseline/정확한 render allowance 비교는 매 tick 유지했다. 원래 supplier ROS/Ackermann/3 controller, endpoint identity·GID pin, curved follower, steering adapter, collider/바퀴 support와 contact 보호를 유지했다. Actor 계산 최적화로 unknown actuator나 script hook을 허용하지 않는다. 실제 실행에서는 전체 rebuild5회, 변경 prim 검사53075회를 수행했다.

독립 CPU USD 검사 15개에서 rigid/collision/joint enabled, schema 제거, type 변경, 관계, 새 속성, physics transform, prim 생성·삭제·비활성·재활성, script hook 거절 및 제거를 검사했다. 각 단계 cache 결과를 원래 전체 순회와 대조했다. 저장 현장 stage도 exact match다. 정지된 저장 stage에서 full 검사15회의 p50 38.037ms, 변경 없는 cache 검사100회의 p50 0.391µs였다. 이 offline 수치를 live 변경 prim 처리 시간과 혼동하지 않는다.

## ZERO-ONLY 물리 정지와 한계

fault가 나면 abort latch와 실제 ROS zero 요청을 남기고 timeline을 우선 pause한다. 복구는 비영 motion driver가 exit0으로 끝나고 실제 observer zero 발행 영수증이 **그 비상 요청에 결합**된 것을 확인한 뒤에만 가능하다. 원래 graph/actor·observer·endpoint inventory freshness·GID/identity·새 contact·shell 검사를 유지하고, graph의 wheel velocity output이0인지 확인하며 controller velocity/effort 입력도0으로 유지한다. 이 모드에서 motion driver 재시작·비영 명령 승인은 없다.

TF_STALE/TF_SIM_STALE만은 해당 fault를 그대로 보존하면서 별도 identity-only zero 검사를 적용한다. snapshot timestamp를 바꾸지 않으며 이 함수는 motion authority를 반환하지 않는다. 외부 publisher·GID 변경·오래된 endpoint inventory·script/actor 변화·contact 등은 계속 거절한다. contact나 신원 문제 때문에 안전한 zero-only step을 확인할 수 없으면 물리를 재개하지 않는다. 기존 steering position을 포함한 공급 graph 자체를 재설계하지 않았다.

실행01은 비상 요청1793535526.1915338, 그 요청에 결합한 zero10 영수증1793535526.2001193 이후, 새 ZERO-ONLY 첫 샘플1793535527.0803006부터70 samples를 측정했다. 마지막 연속1.000000052sim초에서 max raw COM1.836mm/s, origin1.837mm/s, FD0.801mm/s, XY span0.0173mm로 기존 ≤2mm/s·≤2mm quiet 기준 PASS다. 모든 복구 샘플의 graph wheel output 및 두 wheel controller velocity target0도 확인했다. 과거 주행 샘플이나 paused stage를 quiet로 계산하지 않았다.

별도 cleanup 요청은 실행01 ID `dd20ed5076004a5181805ccc709b75d4`, 실행02 ID `2fa617e781ef4775956ef7213c109b46`이며, 각각 자체 request hash/ID/domain/time/zero/count10 영수증과 결합해 PASS다. 응답 지연은15.393ms /14.440ms다. 첫 비상 영수증을 cleanup 영수증으로 재사용하지 않았다. `stop_proof_v18.json`에 실제 관측 ROS zero, target readback 및 프로세스 소멸 검사를 보존했다.

실행02 GOAL_OVERSHOOT는 이번 보수적 recovery whitelist 밖이어서 `FAULT_NOT_SAFE_FOR_ZERO_RECOVERY`, 새 recovery samples0이다. ROS zero20 및 cleanup zero10·정상 종료는 확인됐지만 실제 주행 후 물리 quiet 증거는 없다. 마지막 주행1초의 span7.232mm/속도11.424mm/s로 최종 QUIET FAIL을 보존했다. 이 결과는 최종 물리 정지 실패의 직접 측정이라기보다 **정지 관찰을 확보하지 못한 실패**이며, 실제 최종 정지는 UNKNOWN이다.

## 두 번째 실행의 PRE 차단과 남은 작업

관측 PRE는 (−25.934672961,28.278040587)m이다. 저장된 모든 pulse pose를 원래 follower로 다시 계산했을 때 가장 가까운 step3528의 위치오차8.677mm, cross-track−8.649mm이며 stop=false다. 원래 follower는 거리≤3mm에서 normal stop을 요청하는데 어떤 측정 pulse pose도 이 조건에 들어오지 않았다. 마지막 step3576에서는 진행 방향 overshoot5.079mm로 기존 `along < −.005` 보호가 GOAL_OVERSHOOT를 발생시켰다. 최종 위치오차10.416mm다. 실제 driver도 normal_stop_requested_sim_s=null, adapter MOVING, completion_accepted=false다.

따라서 PRE 안정 도착으로 인정하거나 FINAL 경로·주행을 승인할 근거가 없다. 기준을8.68mm 이상으로 넓히거나 관측 목표를 바꾸지 않았다. 다음 구체적 작업은 저장 궤적의 측방 잔차와 전진 follower terminal 제동 가능성을 먼저 CPU에서 검증하는 것, 전체 GC의 motion 중 긴 동기 pause를 안전한 생명주기로 관리할 방법을 검증하는 것, overshoot처럼 zero-only 정지가 가능한 fault도 신원·충돌 검사 아래 정지 관찰로 연결할 수 있는지 검증하는 것이다. 이 작업에서는 추가 정책 변경·세 번째 Kit 실행을 하지 않았다.

## 검사·보존·변경 파일

- CPU: 신규 timing/zero gate v18 6개, v18b 6개, 기존 TF4+IO5+graph5, actor cache15개 PASS. 총41개 검사 결과를 얻었다. 외부 신원/GID 변경, stale inventory, zero owner 부재는 zero-only에서도 거절했다.
- CPU actor test 첫 시도는 USD API `RigidBodyAPI.Remove` 호출이 없어 FAIL했다. 새 테스트에서 `prim.RemoveAPI`로 고친 두 번째 시도는 PASS다. 첫 실패 log `actor_cache_cpu_stdout_v18b.log`와 후속 `..._02.log` 모두 실행01 root에 남겼다. 이 CPU 실패를 Kit 실행이나 연구 분모에 넣지 않았다.
- 신규 scripts/evaluation/analysis v18 계열 compile PASS, saved trajectory follower replay·GC 포함관계·cleanup binding 검사 PASS. Runtime PRE/FINAL success는 FAIL/미달성으로 구분한다.
- known-lock9 hash/count subset PASS. 전체 과학 pairing/dependency 재감사나 research readiness 인증은 아니다.
- prepare 입력 실행01 59개/실행02 65개, 기존 v17 54개/v16 50개/v15_02 44개 SHA256 불변 PASS. 각 실행 provisional digest 및 존재 evidence hash PASS, eligibility=false 실패 보존.
- driver·observer·Kit 소유 PID 전부 소멸, watchdog/강제 종료 없음. 최종 Kit/training process0, GPU에는 기존 rustdesk만 남았다. 원본 stage·weights·protocol·이전 실행 소스/결과/보고서를 수정하지 않았다.

신규 runnable source는 `scripts/construction_site_perception_{runner,session}_20261101_v18.py`와 `v18b.py`, `scripts/construction_site_{observer,drive_ros}_20261101_v18.py`와 `v18b.py`의8개다. 신규 evaluation은 `construction_site_timing_20261101_v18.py`, `construction_site_timing_20261101_v18b.py`, `construction_site_actor_cache_20261101_v18b.py`의3개다. 신규 analysis는 timing test v18/v18b, actor_cache_test v18b, timing_summary/failure_replay/stop_proof v18의6개다. 실행 source snapshot은 각 root `executed_code/`에 있다. 이 보고서와 `reports/latest_report.md`, `docs/PROJECT_STATE.md`를 갱신했다.

주요 추가 증거는 실행01 `fault_attribution_v18.json`, `actor_cache_cpu_v18b.json`, 실행02 `failure_replay_v18.json`, `known_locks_v18.json`, `final_resources_v18.json`, 양쪽 `measured_summary_v16.json`(기존 요약 도구 이름 유지), `timing_summary_v18.json`, `stop_proof_v18.json`이다. 모든 RGB-D·model/ROI/review·prediction·path/support·raw step/contact·forensic·zero request/receipt·provisional/final·종료 log를 외부 root에 보존했다. 연구 representation/샘플/threshold/seed/관측 정책 변경이나 real-robot 검증 주장은 없다.
