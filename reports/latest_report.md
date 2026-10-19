# Full E2E v02 wheel-position feedback HOLD 구현 — 2026-10-19

**판정: NO-GO. 분리 adapter·owner mux·최소 derived-layer patch·오프라인 검사는 구현 완료. 실제 actuator 독점·물리 안정성·정지 성공은 UNKNOWN이다.** 이번 Isaac/ROS 구동·motion·ENG001·QUAL12·432-run·자동 retry는 모두 0이며 연구 denominator는 바뀌지 않았다. 기존 선정 결정을 재검토하거나 새 문헌을 탐색하지 않았다.

## 구현과 검사

- `evaluation/fe2e_v02_wheel_hold_adapter_v01.py`: explicit wheel6/steer4 name, rad/rad/s 계약. synchronized epoch의 q/dq/steer/base를 검사하여 q unwrap 및 q_hold/steer_hold/base_hold를 한 번만 latch한다. 기준은 immutable tuple이며 갱신하지 않는다. q의 encoder→canonical sign 및 target→API sign 변환을 각각 한 번 적용한다. joint error는 modulo 최단각이 아닌 누적 unwrap 좌표 차이다. `saturate(K*error, ±limit)` 뒤 slew를 적용한다. Fault/stop zero는 slew를 우회한다.
- Freshness/future/nonfinite/단위·순서/시간역행/step gap/dq·unwrap alias/시간·변위·yaw 한계는 fail-latched zero 및 pause 요청이다. Fault/stop 후 재진입과 re-arm은 금지된다. `tick(monotonic_now)`는 샘플이 끊겼을 때 외부 주기 호출이 필요하다. 입력 epoch 표시는 생산자의 동일-step 계측을 대신 증명하지 않는다.
- `evaluation/fe2e_v02_wheel_hold_owner_v01.py`: 단일 physics-thread writer mux, derived edit-layer에서 기존 3개 articulation writer의 active=false override 함수, 명시적 DOF subset의 ArticulationAction writer를 구현했다. 원본 layer 저장·drive gain 수정·simulation import/launch는 없다.
- `evaluation/fe2e_v02_wheel_hold_contract_v01.json`: 모든 수치가 명시된 PROPOSED contract. runtime 승인·signed 정책·dynamics 인증은 false. Adapter와 mux는 runtime 미승인 시 생성부터 거부한다. offline=True는 synthetic 검사용이며 실행 승인으로 사용하면 안 된다.
- `tests/test_fe2e_v02_wheel_hold_v01.py`: **15/15 PASS**, 최종 로그 `reports/fe2e_v02_wheel_hold_offline_20261019_v02/tests.txt`. Single latch, ± correction, encoder sign, wrap boundary, name/order/units, K/limit/slew invalid, freshness/NaN/mixed epoch, gap/timeout/watchdog, 변위 guard, duplicate owner, Twist overwrite 방지, stop/re-arm 금지, patch mock, writer 실패 pause 및 disjoint subset mapping 검사다.
- `analysis/fe2e_v02_wheel_hold_offline_v01.py`: 표준 라이브러리만으로 재현. 최종 `replay.json`에 5개 synthetic sample와 wheel/steer target sequence를 저장한다. q=[0,.001,−.001,.002,0]rad에서 첫 wheel target=[0,−.001,+.001,−.002,0]rad/s, steer=[.2,.1,0,0]rad 고정. **물리 stop/safety 성공 증거가 아니다.** 최초 v01 증거(14tests)도 보존하고 writer mapping 추가 후 v02(15tests)를 생성했다.

재현 명령(새 미사용 output 경로 필요):

```bash
python3 -m unittest discover -s tests -p test_fe2e_v02_wheel_hold_v01.py -v
python3 -m analysis.fe2e_v02_wheel_hold_offline_v01 reports/fe2e_v02_wheel_hold_offline_NEW
```

## PROPOSED 수치와 검토 범위

기존 보고서의 radius r=.13300000131130219m, dt≈1/60s, nominal 잔여 long5.119679mm/lat4.580750mm/yaw .466862°를 이용한 **사전 검토 후보**다. 단일 nominal margin을 다른 fresh FINAL의 실제 margin으로 쓰지 않는다.

| 항목 | 후보·단위 | 산정/안전 조건 |
|---|---:|---|
| K_hold | 1 s⁻¹ | 이상적 즉시 추종 P계의 시정수1s, 95% 복원 약3s. 실제 cascade 안정성/유효 damping100 환산 근거 없음: UNRESOLVED |
| 각 wheel target | ±.020 rad/s | r×limit=.00266000003m/s의 rolling-equivalent. 실제 base cap .03m/s 보장값이 아님. signed HOLD 전용 승인 필요 |
| target slew | .200 rad/s² | 0→limit .1s; r×slew=.0266000003m/s². 기존 surface-command .07m/s²보다 작은 후보이나 coupled response 인증 아님 |
| base excursion guard | .004m XY | nominal 최소 위치여유4.580750mm보다 작게 남긴 budget 제안. 충분한 검출·pause stopping distance 인증은 없음 |
| yaw guard | .005rad=.286479° | nominal 잔여 .466862°보다 작은 예산 후보. terminal ±2° 변경 아님 |
| wheel excursion | .004/r=.03007518767rad | base guard와 연결한 rolling-equivalent 추가 abort. Slip 시 base pose 별도 검사 필수 |
| HOLD 시간 | 8s | 이상적 시정수8배, quiet1s 평가 여유 제안. 지난 후퇴가 약7.916667s 지속한 사실도 고려하되 8s 내 stop 보증으로 쓰지 않음 |
| freshness / max sample gap | .040s / .040s | 기존 약16.67ms의 2sample 간격33.33ms를 포함하는 후보. 실제 scheduling/transport 인증 필요 |
| wall watchdog | .100s | limit rolling-equivalent에서 .266mm에 해당. actual displacement bound가 아니며 독립 pause 감시 필요 |
| measured wheel dq bound | 1rad/s | .04×1=.04rad<π로 unwrap alias 제한. 실제 dq admission 적합성 미인증 |
| signs | wheel6 모두 +1 | 동일 API q/velocity axis 전제, actual named DOF encoder/target 방향 계측 확인 필요 |

이 값은 편의 기본값으로 adapter에 숨겨져 있지 않다. 모든 양의 유한 수치와 sign을 명시해야 한다. 테스트는 limit·slew·alias 산술 및 코드 계약만 검증했다. 실제 안정성·force·slip·검출 지연·최대정지거리는 UNRESOLVED이므로 runtime을 차단한다. Parameter sweep/통과할 때까지 조정은 하지 않는다.

## 실제 적용할 단일 owner 경로

기존 graph.json은 validation bulk **상위 디렉터리**에서 확인했고 SHA도 기존 inventory와 일치한다. 최초 attempt_0001/graph.json 읽기는 경로 오류(exit1)였으며 삭제/성공 처리하지 않았다. git status도 .git 없음(exit128)이므로 Git diff 검증은 수행 불가였다. 권한/샌드박스 오류나 보안 설정 변경은 없었다.

Source `/World/ROBOT_TASK/RuntimeRover/ActionGraph`의 writer는 `articulation_controller`(FL/FR/RL/RR wheel), `_01`(front steer), `_02`(middle wheel)이다. Derived reference `/World/ENG_FE2E/Rover`에서는 동일 suffix 3개를 별도 stronger edit-layer에서 비활성화한다. Patch는 정확한 node:type과 3개 path를 확인하며 원본 USD를 수정하지 않는다. Mock으로만 검사했고 실제 USD patch 적용은 이번 미실행이다.

APPROACH/DECEL에서는 기존 ROS Twist→Ackermann 계산을 유지하고, 기존 3개 writer 대신 단일 Python owner가 graph 출력 wheel4를 이름으로 재배열하고 middleL/R=frontL/R, front steer2와 기존 rear0를 writer에 전달한다. Legacy surface→wire .250626563945 계약을 유지한다. HOLD joint rad/s에 이 scale이나 π/180을 다시 적용하지 않는다. **이 graph-output reader/physics callback 및 전체 writer inventory 검사는 아직 구현·현장검증되지 않았으며 완성된 runtime runner라고 주장하지 않는다.**

StoppingAdapter의 첫 ZERO_SETTLING 요청을 physics thread가 처리하는 epoch에, legacy zero write **전에** fresh q6/dq6/steer4/base를 취득하고 mux.enter_hold를 호출해야 한다. Same-step handoff 실패/이미 그 epoch legacy write 발생이면 abort한다. 이후 graph 계산과 ROS Twist zero는 계속될 수 있어도 disabled legacy writer와 mux state 때문에 actuator에 도달하지 않는다. 별도 JointState subscriber는 설치하지 않았고 topic 격리만으로 ownership을 주장하지 않는다. Thread/foreign direct articulation writer는 Python mux로 차단할 수 없으므로 scene과 scripts의 독점 검증이 필수다.

Independent guard는 owner와 별도 physics observer + 외부 wall watchdog이 담당하도록 다음 runner에서 연결해야 한다. .03m/s 초과·clearance<.10m·stale·fault·guard excursion이면 fail 기록→zero 시도→자기 simulation timeline pause. 기존 독립 emergency .25m/s/2m boundary는 그대로 추가 유지하며 .03 cap을 대체하지 않는다. Callback 정지/zero write 실패에도 pause가 도달해야 한다. Pause로 멈춘 경우 성공이 아닌 실패다. Zero 자체는 물리정지 보증이 아니다.

## 실행 전 blocker — 최대 3개

1. **수치·signed HOLD 정책 미승인/미인증:** 위 후보의 gain·양방향 .020rad/s·slew·admission/guard/시간 및 sign 계약의 사전 승인과 검토 기록 필요. 현재 승인 bool을 바꾸기만 해서는 인증을 대체할 수 없다.
2. **runtime integration 및 독점성 미검증:** 실제 derived patch, 동일 physics epoch graph-output reader/entry handshake/ArticulationAction writer, 모든 외부 writer 배제, independent pause/watchdog를 단일 one-shot runner로 연결하고 검사해야 한다. 현재 제공 파일은 최소 integration building block이다.
3. **단일 실제 시험 준비와 명시적 실행 승인 부재:** 미사용 output/domain, input·environment·code hashes와 단일 episode 계획, 실제 동일 epoch 계측 및 자동 retry 없는 상태 기록을 확정한 후 다음 단계에서 사용자 승인을 받아야 한다. 이번 실행 권한은 없다.

다음 1회는 기존 열린공간/동일 mobility의 nonzero-curvature→정상감속→HOLD다. 실제 q/dq/steer/base/root COM→origin/FD/ROS receive/source/graph target/owner를 동일 epoch로 기록하고 latch 이후 max along/XY/yaw drift, raw root와 FD quiet(.002m/s,1s), max planar .03m/s, contact/clearance/guard를 평가한다. Long/lat±.030m, yaw±2°, clearance≥.10m, footprint1.68×1.61m와 기존 경로·게이트는 불변이다. Wheel q가 유지돼도 base drift 또는 raw-root quiet가 실패하면 FAIL. 이 1회는 ENG001 full-chain success가 아니며 ENG001/QUAL12/432로 자동 전이하지 않는다. 현재 실행 가능한 Isaac command는 제공하지 않는다: runner 연결이 미완료인 상태에서 기존 validation command를 재사용하면 HOLD 검증이 되지 않는다.

## 보존

기존 inventory의 PROJECT_STATE 과거 버전 항목만 제외하고 비교한 **148개 expected=observed SHA256 PASS**. 최초 workspace 전체 snapshot 대비 코드·문서 기존 파일 변경0(PROJECT_STATE append 이전). 증거는 `reports/fe2e_v02_wheel_hold_offline_20261019_v01/preservation.json`이다. PROJECT_STATE는 이 작업을 추가 기록하며 원본 protocol/threshold/controller/governor/stopping adapter/USD/기존 결과·inventory는 보존했다. 새 evidence에는 명령·Python/platform·code hashes·return code를 남겼다. 구현 PASS와 runtime NO-GO를 분리한다.
