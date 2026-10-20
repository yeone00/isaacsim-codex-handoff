# Full E2E v02 HOLD runtime integration — offline 구현

작성일 2026-10-20 (Asia/Seoul). 요청된 보고서 파일명의 20261019를 유지했다.

**GO/NO-GO: 실제 실행 NO-GO. 새 dependency-injected integration의 단위/mock 계약 12/12 PASS. 실제 host 설치·actuator 독점·pause 전달·물리 HOLD 안정성은 UNKNOWN.** Isaac Sim/ROS/physics launch, ENG001, QUAL12, 432, retry/sweep 모두 0이다. 연구 denominator 및 기존 실패 결과는 바뀌지 않았다. 후보 선정/알고리즘 재탐색/기존 감사 재수행은 하지 않았다.

## 새 구현 파일

- `evaluation/fe2e_v02_hold_runtime_integration_v01.py`: 정확한 derived writer inventory와 jointNames/upstream/index/array 연결을 검사하는 별도 edit-layer patch, Ackermann graph-output reader, 이름 기반 DOF snapshot mapping, physics-thread callback, 독립 physics observer와 wall watchdog/pause port. simulator/ROS import나 launch 부작용은 없다.
- `scripts/fe2e_v02_hold_one_shot_v01.py`: 미사용 output만 생성하는 one-shot 기록/실패 종료 인터페이스. 입력·자기 코드 SHA, 명령, Python/platform, 계측 목록, append event, terminal status, nonzero 실패 exit를 제공한다. 재사용/자동 retry를 거부한다. actor 함수는 전달해도 호출되지 않는다. 현재 CLI는 launch runner가 아닌 **봉인된 준비/거부 인터페이스**다.
- `analysis/test_fe2e_v02_hold_runtime_integration_v01.py`: 새 synthetic port 계약 검사. 기존 adapter/owner는 정적으로 확인한 simulator-free 모듈만 사용했다. legacy session은 읽기만 했고 import/실행하지 않았다.

`RUNTIME_APPROVED=False`, 기존 numeric contract의 승인 3항목 false를 유지했다. 새 PhysicsIntegration은 offline mock 생성만 허용하며 실제 runtime 생성은 항상 거부한다. bool을 승인으로 바꾸는 작업은 이번 범위에 포함되지 않는다. K=1, ±.020rad/s, slew=.2, base .004m 등 기존 PROPOSED 수치는 변경하거나 인증하지 않았다.

## 정적 계약 근거와 연결 순서

읽은 실제 근거:

- `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01/graph.json`
- `scripts/fe2e_v02_stopping_validation_session_v01.py`의 scene/reference 및 graph 출력 취득 코드
- 기존 wheel HOLD adapter/owner/contract 및 20261019 구현 보고서

원본 reference는 `/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd`의 `/World/ROBOT_TASK/RuntimeRover`이며 derived rover는 `/World/ENG_FE2E/Rover`다. 실제 현재 열린 stage의 재검증은 하지 않았다. graph snapshot hash와 관련 노드 전체 속성/연결은 `reports/fe2e_v02_hold_runtime_integration_20261020_v01/graph_contract.json`에 남겼다.

| 원본 graph suffix | 이름/입력 연결 | derived patch 경로 |
|---|---|---|
| articulation_controller | front_left, front_right, rear_left, rear_right wheel / Ackermann wheelRotationVelocity | /World/ENG_FE2E/Rover/ActionGraph/articulation_controller |
| articulation_controller_01 | front_left, front_right steer / Ackermann wheelAngles | /World/ENG_FE2E/Rover/ActionGraph/articulation_controller_01 |
| articulation_controller_02 | middle_left, middle_right wheel / make_array(get_array_index 0, get_array_index_01 1) | /World/ENG_FE2E/Rover/ActionGraph/articulation_controller_02 |

Joint 이름은 코드에서 `_wheel_joint`, `_steer_joint`까지 정확히 검사한다. Patch는 TraverseAll inventory exact-set, 별도 edit target, node type 및 위 연결을 검사한 뒤 active=false override만 작성한다. 원본/root layer 저장은 없다. 실제 USD에서 patch를 적용하거나 export하지 않았으며 mock stage 검사만 했다. 전체 stage에 다른 articulation writer가 있으면 보수적으로 거부한다. drive gain/controller 변경은 없다.

APPROACH/DECEL에서는 host가 완료한 graph epoch token을 reader에 전달해야 한다. wheel4는 FL/FR/RL/RR, middle은 FL/FR 복제, front steer2와 rear steer0를 이름으로 wheel6/steer4에 매핑한다. native rad/s, rad를 그대로 전달하며 HOLD에 surface→wire scale 또는 각도 변환을 추가하지 않는다. 기존 ROS Twist→Ackermann 계산 및 surface→wire 계약 자체는 이번 코드 밖의 보존 대상이다.

Callback은 독립 observer의 같은 epoch 확인 → 외부 exclusivity/pause receipt 확인 → fresh synchronized sample 검사 → PRE_WRITE_SNAPSHOT 기록 → owner write 순서다. 첫 ZERO_SETTLING은 같은 callback에서 `enter_hold`로 immutable q/steer/base latch를 만든 뒤 첫 zero target을 적용한다. 이미 같은 epoch에 approach write가 발생한 경우 중복 epoch로 거부한다. HOLD 이후 graph target을 읽거나 재전달하지 않고 HOLD adapter target만 같은 mux로 적용한다. 별도 validation adapter가 매 epoch의 sample 순서/단위/유한성/freshness를 검사하며 실제 HOLD adapter history는 별도로 유지한다.

Receipt는 epoch, graph_disabled, direct_writers_excluded, single_callback, pause_installed가 모두 정확히 일치해야 한다. UNKNOWN/누락/직접 writer 신고/중복 owner/thread/시간 역행/sample 누락은 failure와 pause 요청으로 이어진다. 이 receipt는 host attestation 인터페이스이며 **Python dict가 외부/native writer의 부재를 증명하지 않는다**. 실제 관측/설치 검증을 구현한 host가 없으므로 runtime 봉인을 유지한다.

IndependentGuard는 owner와 별도 observer에서 raw COM→origin planar 및 FD planar, clearance, contact, 2m emergency boundary를 검사한다. .03m/s, .10m 제한을 유지한다. 별도 thread의 monotonic wall watchdog은 physics callback/write 없이도 pause port를 호출한다. owner latch drift guard(.004m/.005rad)는 기존 adapter가 담당한다. 실제 raw/FD 계산·contact/clearance 공급 및 별도 observer 등록은 host 책임이며 mock 값만 검사했다. Wall pause가 thread에서 실제 timeline까지 전달되는지, physics hang에서도 전달되는지는 UNKNOWN이다. pause port 예외도 안전정지 성공으로 취급하지 않는다. Zero는 안전정지 보장이 아니며 pause 종료는 FAIL이다.

## 오프라인 검사와 보존

명령: `python3 -m unittest analysis.test_fe2e_v02_hold_runtime_integration_v01 -v`

**12/12 PASS, exit0.** 이름/배열 mapping, latch-before-write 및 HOLD graph 차단, missing/mixed/NaN sample, direct writer·pause 미설치 receipt 거부, 중복 epoch/graph barrier, 다른 thread, 독립 속도/clearance/contact/boundary guard, physics 진행 없는 wall timeout pause, write 실패 pause, runtime gate/one-shot actor 미호출·재사용 금지·실패 상태, snapshot 이름 재정렬, exact inventory patch를 검사했다. 후속 코드 변경에 맞춘 재검사까지 모두 exit0이며 최초 로그도 보존했다. 실물 안정성이나 실물 독점성 PASS로 해석하지 않는다.

증거 디렉터리: `reports/fe2e_v02_hold_runtime_integration_20261020_v01/`

- `tests.txt`, `tests_final.txt`, `tests_final_v02.txt`: 각 단계 로그, 최종 12tests PASS.
- `execution.json`: 검사 명령/exit, 환경, 새 코드·기존 contract SHA, 실행 금지 상태.
- `preservation.json`: 기존 148개 expected=observed SHA PASS; PROJECT_STATE append 직전 기존 파일 변경0.
- `before.json`: 이번 작업 시작 시 workspace SHA snapshot.

기존 protocol/controller/USD/결과/inventory/adapter/owner/contract는 수정하지 않았다. PROJECT_STATE에 이번 결과만 추가했다. 새 code·report·evidence는 별도 경로다. Git stage/push/publish는 수행하지 않았다.

## 남은 blocker — 3개

1. **실제 host 연결과 독점성:** post-physics atomic acquisition, Ackermann completion barrier, 단일 callback 등록, live USD patch/readback, 모든 script/native direct writer inventory·배제 및 callback/thread 소유권 증거가 필요하다. 현재는 테스트 가능한 injected port 구현이며 실제 Isaac callback 등록은 미구현이다.
2. **독립 pause와 수치/물리 검증:** 별도 observer/wall thread의 실제 pause 전달 설치·hang/write failure 시 전달, raw root COM→origin/FD 및 drift·clearance 계측, joint sign, signed HOLD와 PROPOSED 수치의 사전 검토/승인·안정성 검증이 필요하다. Mock PASS는 이를 인증하지 않는다.
3. **단일 실행 승인 및 host runner 확정:** 실제 발견된 Isaac launcher의 정확한 경로/명령·버전, unused output/domain, 전체 input/code hash, 한 episode 계획과 실패 상태 보존을 확정하고 사용자 명시 실행 승인을 받아야 한다. 새 인터페이스에는 simulator launcher나 ROS command가 없으며 승인된 실제 시험 명령도 아직 UNKNOWN이다.

## 단일 실제 시험 사전조건 및 다음 행동

다음 행동은 별도 허용 범위에서 blocker 1·2의 host binding을 구현하고, scene/callback/direct writer/pause 설치 증거를 검토하는 것이다. 그 뒤 새 unused output·isolated domain과 **정확한 실제 launcher 명령**을 보고 사용자에게 단일 실행 승인을 받아야 한다. 이번 작업은 해당 승인을 요청하거나 추정하지 않는다.

준비 인터페이스 명령 형식(이번 턴 실행하지 않음): `python3 scripts/fe2e_v02_hold_one_shot_v01.py --output <UNUSED_OUTPUT> --input evaluation/fe2e_v02_wheel_hold_contract_v01.json`. 현재는 metadata 작성 후 FAILED/exit1로 끝나며 simulation을 시작할 수 없다. 실제 host runner를 대체하는 명령이 아니다.

향후 승인 대상 한 회는 기존 열린 공간·동일 mobility에서 nonzero curvature→DECEL→첫 ZERO_SETTLING latch→HOLD다. 각 epoch의 q/dq/steer/base, raw COM/root·origin·FD, source/receive/graph target/owner와 latch-before-zero 순서를 기록해야 한다. HOLD 최대 along/XY/yaw drift와 raw-root·FD quiet(.002m/s, 1s), max planar .03m/s, clearance≥.10m 및 contact/guard를 평가한다. quiet·drift의 실제 산출/성공 판정기는 이번 one-shot interface에 구현하지 않았으며 계측 schema만 준비했다. Long/lat±.030m, yaw±2°, footprint1.68×1.61m와 기존 경로/정책은 불변이다. 계측 누락·terminal error·pause는 실패로 남기고 자동 재시도하지 않는다. ENG001/QUAL12/432로 자동 전이하지 않는다.
