# Full E2E v02 bounded writer owner 결정 — 2026-10-20

**물리 판정: BLOCKED_WITH_SPECIFIC_CAUSE.** v07의 의도된 단일 writer 경로는 구체적으로 식별했다. 그러나 현재 프로세스의 enabled extension 내부 callback/직접 tensor producer까지 열거·검토한 실제 증거는 없다. 이것을 “어떠한 C++ writer도 영원히 없음”이라는 전역 요구로 확대하지 않는다. C++ lease 프로젝트는 권고하지 않는다. **다음 한 단계는 별도 승인한 paused inventory 1회**다. 새 no-motion 진입점은 코드 검토/계약 검사까지 준비했지만 실제 host admission PASS나 SINGLE process owner 인증을 발행하지 않았다. 따라서 물리 준비 판정으로 PREPARED_FOR_PAUSED_OWNER_PREFLIGHT를 사용하지 않는다.

이번 SimulationApp/Isaac launch, graph 실행, physics.play, ROS publish, actuator write, motion/retry 모두 0. 이 HOLD branch engineering denominator=0, ENG001/QUAL12/432=0. 과거 engineering 실행 기록은 삭제하거나 0으로 재해석하지 않는다.

## 1. 실제 producer와 시작 범위

[정적 원자료](fe2e_v02_bounded_owner_20261020_v01/static_bench_inventory.json)는 기존 설치 standalone pxr로 원본을 읽기만 했다. `isaac_loaded=false`, 원본 bench SHA `224cac492d267d0403c9402484fcf84011191208fb4689e7e3fc33eadf3756fe`. 조사 subtree `/World/ROBOT_TASK/RuntimeRover`에 graph node20/joint10/script·python·behavior **속성명 후보0**. 이는 stage metadata/customData와 enabled extension의 실행 코드를 모두 인증했다는 뜻이 아니다. Used layer 경로/hash도 원자료에 있다. 전체 bench composition에는 환경/rolltainer 참조도 보이며, 이를 파생 Rover subtree의 active actor와 혼동하지 않는다.

아래 `G=/World/ENG_FE2E/Rover/ActionGraph`. 원본 prefix는 `/World/ROBOT_TASK/RuntimeRover/ActionGraph`이며 v07이 reference로 옮긴다.

| 경로/producer | 실제 입력/출력 | v07 isolated process에서의 상태 |
|---|---|---|
| G/articulation_controller | Ack execOut; wheelRotationVelocity → front L/R, rear L/R wheel velocity | patch가 명칭/연결 검증 후 derived layer SetActive(False), readback |
| G/articulation_controller_01 | Ack execOut; wheelAngles → front L/R steer position | 동일 비활성화/readback |
| G/articulation_controller_02 | Ack execOut; get_array_index0/1→make_array → middle L/R wheel velocity | 동일; array shape/index/upstream도 patch 검증 |
| G/ros2_subscribe_twist | playback tick→Twist linear/angular→multiply/absolute/ATan2→Ack | PhysicsAckermann 설치가 Ack 외 node 전부 inactive 처리; ROS subscriber 자체 실행 경로 제거 |
| ROS graph 기타 | transform publisher, camera helpers2, simulation time/render product | 같은 비활성화; 원본 scene node 자체는 보존 |
| G/ackermann_controller | 수동 입력→wheel4/steer2 산출 | ONDEMAND 계산기, actuator writer 아님 |
| G/PhysicsHoldImpulseV01→Ack→PhysicsHoldWitnessV01 | evaluate_sync 단일 token/epoch/thread receipt | PhysicsAckermann이 설치. Witness script는 host witness(key)만 호출; actuator setter 없음. 이번 재설치/평가하지 않음 |
| PhysicsSession.bind→exclusive_write→batched_writer | wheel6 velocity target + steer4 position target, disjoint named subset | 의도한 유일 Python actuator route. 초기 native gate 때문에 이번/현재 실제 미시작 |
| PhysX receipt / Kit post-update / watchdog / contacts | epoch/관측, pause queue pump, contact headers | PhysicsSession/LiveObserver가 설치할 경로. watchdog는 actuator를 쓰지 않음. stalled Kit에서 queue delivery 보장 없음 |
| legacy normalized session v07 | scripts/fe2e_v02_normalized_physics_session_v07.py:147 직접 position/velocity setter | v07 HOLD runner가 import/실행하지 않음. 그 script의 top-level simulation/contact callback도 시작하지 않음 |
| legacy stopping session/ROS child | scripts/fe2e_v02_stopping_validation_session_v01.py; stopping_validation_ros_v01.py Twist publish | HOLD runner가 시작하지 않음. 원본 ROS 진단과 새 direct writer를 혼합하지 않음 |

소스 근거: `scripts/fe2e_v02_hold_one_shot_v07.py` live/main, `evaluation/fe2e_v02_hold_runtime_integration_v01.py` patch, `evaluation/fe2e_v02_wheel_hold_owner_v01.py` deactivate_derived_writers, `evaluation/fe2e_v02_physics_hold_host_v01.py` PhysicsAckermann/PhysicsSession.attest/bind, `evaluation/fe2e_v02_hold_host_ports_v02.py:236` batched_writer. v07은 bench/reference/physics/floor를 새 USD에 만들며 원본 script를 USD reference로 실행하는 구조가 아니다. 다만 USD의 실행성 metadata/extension 동작까지 이 사실 하나로 배제할 수는 없다.

**ROS 수정 설명:** 기존 v07은 bridge를 명시적으로 disable하지 않는다. PhysicsSession.attest가 `isaacsim.ros2.bridge` 또는 `omni.isaac.ros2_bridge` enabled이면 거부한다. graph inactivity와 extension disable은 별개의 검사다. 새 paused 경로는 프로세스 안의 두 bridge extension만 `set_extension_enabled_immediate(...,False)` 후 enabled=false readback을 요구한다. 외부 ROS 설정/기존 process는 건드리지 않는다.

Installed API 근거: `/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim/exts/isaacsim.core.prims/isaacsim/core/prims/impl/articulation.py`의 set_joint_position_targets:859/925, set_joint_velocity_targets:1000/1066은 tensor view setter로 전달한다. pause_motion/resume_motion:5080–5130도 target/velocity setter 후보지만 v07이 호출하지 않는다. 이것은 callback으로 자동 실행된다는 발견이 아니다. API에 target을 마지막으로 쓴 producer identity가 반환되는 것은 확인되지 않았다. 같은 값/복원 write는 readback equality로 검출 불가다. **구체적 미확인은 실제 enabled extension 및 그 내부 callback inventory**이며 외부 임의 native 존재를 입증한 것도 아니다.

## 2. 새 bounded admission 구현과 증명 범위

새 파일만 추가했다.

- `evaluation/fe2e_v02_bounded_owner_v01.py`: stage prim/active/type/schema/attribute connection/relationship 전체의 fingerprint, source SHA, enabled extension ID 집합의 admission snapshot과 변경 시 latch하는 recheck. receipt는 항상 physical_go=false/global_native_exclusion=UNKNOWN. `attest` 메서드가 없어 native port로 끼워 넣을 수 없다.
- `scripts/fe2e_v02_paused_owner_admission_v01.py`: 별도 승인 없으면 Isaac import 전 거부. discovered interpreter, 429 preservation, bench lock 검사 후 새 derived USD만 생성. 기존 patch를 재사용해 세 writer topology 검증/비활성 readback, **모든 graph node inactive**. Ack/witness 설치나 graph evaluation도 없음. unknown script 속성/foreign rigid actor 발견 시 거부. ROS disable/readback, actual attached stage identity/paused time0 확인, full inventory와 layers/source hashes/extension IDs/session layer를 저장하고 종료.
- `analysis/fe2e_v02_bounded_static_inventory_v01.py`: 위 정적 read-only composition 조사.
- `analysis/test_fe2e_v02_bounded_owner_v01.py`: 좁은 계약 검사.

새 paused entry는 Articulation/PhysicsSession을 생성하지 않고 app.update도 호출하지 않는다. stage attach가 이 조건에서 실제로 완료되는지는 live UNKNOWN이며 identity 불일치는 fail-closed다. runtime test 없이 완료를 주장하지 않는다. Terminal은 app.close 전 저장하고 실제 process exit는 외부 관찰이 필요하다.

**양의 증명:** 코드상 명시적으로 시작하는 actor writer는 v07의 exclusive_write 한 경로이고, stage graph writer3은 정확한 topology 확인 후 inactive다. 새 paused entry 자체에는 actor writer/physics advance/graph evaluation이 없다. **증명하지 못한 것:** enabled extension 내부 callbacks/native direct writers의 부재, 임의 외부 extension의 고의적 회피. 새 contract는 이 UNKNOWN을 인정하며 owner certificate를 생성하지 않는다.

물리용 후속 bounded 정책은 reviewed extension/source hash allowlist + 활성 stage writer allowlist + 매 advance 직전/직후 및 매 write 직전 재검사 + 동일 Kit thread/epoch + target readback을 요구해야 한다. 추가 graph/ROS/script/foreign actor/미검토 extension이면 fault latch→pause request, 재명령 없음. 현재 recheck는 paused snapshot 전용이며 joint state가 변하는 물리 stage에서 그대로 쓰면 false rejection이 생긴다. 따라서 physical active-state projection을 검토하지 않은 채 연결하지 않았다. 범용 native registry나 lease를 발명하지 않았다.

## 3. pre-SimulationApp guard 처리

v07 main과 live 양쪽의 native.attest(0)가 실제 stage 생성 전 실패한다. actual stage verification이 현재 경로로는 불가능한 직접 원인이다. 두 호출과 NativeExclusionUnavailable은 **수정하지 않았다**. 강한 global native 보장이 연결되지 않았다는 설명도 유지한다.

새 진입점은 별개의 **zero-command admission**으로 분리했다. physical code에는 도달하지 않으므로 기존 물리 gate를 제거/우회하지 않는다. 향후 process-scoped 정책으로 물리 진입 조건을 바꾸려면 별도 명시 engineering authorization과 새 version/source hash가 필요하다. 이 보고서는 그 승인이 아니다.

## 4. paused 다음 단계와 남은 물리 blocker 3개

새 entry의 no-motion 구조는 준비됐으나, 실제 process owner 성립은 아직 미확인이다. 따라서 요청의 “owner 성립 시에만 ready command” 조건에 따라 **승인 가능한 owner-ready launch command는 발행하지 않는다**. 다음 검토 대상은 `scripts/fe2e_v02_paused_owner_admission_v01.py --output <새 절대경로> --approve-paused-launch`이며 실제 launcher는 `/home/user/anaconda3/envs/hh_isaac51/bin/python`이다. 후보 output `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_PAUSED_OWNER_ADMISSION_20261020_v01`은 로컬 미존재 확인했다. 이 설명은 실행 지시/실행 승인/완료 증거가 아니다. 한 번의 별도 paused admission 승인 요청에서 exact command와 source hash를 묶어야 한다.

물리 1회 전 별도 사용자 승인이 필요한 항목은 다음 세 가지다.

1. **bounded scope와 native 잔여 불확실성:** 실제 paused process inventory의 extension/metadata/callback 후보 검토, process-scoped 정책 채택 여부, 기존 global native gate의 후속 version 변경을 명시 승인. 지금 owner admission UNKNOWN.
2. **signed correction와 numeric 정책:** K=1s⁻¹, limit±.02rad/s, slew .2rad/s², hold8s/4mm/.005rad, signs(+1×6)는 후보 그대로 미승인. evidence path/hash와 새 signed contract가 필요하다. 아래 부호/동역학 근거를 가정으로 대신하지 않는다.
3. **단일 실제 시험과 pause/stop gate:** independent watchdog는 같은 Kit에 pause 전달을 의존하고 stall 시 정지 보장 UNKNOWN임을 수락해야 한다. 기존 measured speed .03m/s, clearance .10m, raw COM/root/FD quiet .002m/s 등 모든 gate 유지. 이전 후퇴34.127288744mm 및 raw root .002619135991>.002 quiet FAIL은 그대로다. engineering 한 회와 ENG001/QUAL12/432를 분리하고 자동 retry 없음.

### 부호/K/velocity/slew의 실행 가능한 근거 계획

정적 joint10은 wheel6 Y-axis/identity localRot0/1, steer4 Z-axis/identity다. wheel stiffness0/damping100, steer stiffness836.6141357421875/damping40. Radius .13300000131130219m와 locked surface→wire .2506265639450088은 기존 drive 근거다. encoder와 target의 같은 signed joint coordinate는 API와 이 정의로 대조할 수 있으나 실제 named index/actuation response 부호까지 확정하지 않는다.

먼저 기존 attempt_0001/steps.jsonl의 joint name→index, graph target, q unwrap 차분과 dq를 시간 정렬해 **각 wheel별** sign agreement/lag와 zero후 q 회복 필요량을 계산한다. 이름 없는 평균 wheel speed나 base forward 부호를 encoder-target sign으로 대체하지 않는다. 이번 broad reanalysis/재실행은 하지 않았다. 부족하면 최소 미래 물리 probe는 **한 episode 안의 짧은 저속 공통 wheel target→zero**에서 여섯 named q/dq 및 실제 target을 함께 계측하는 것. 직진 양의 excitation은 encoder-target sign만 검증하며 음의 HOLD correction 안전/수렴 인증은 아니다. 이 probe도 별도 명시 승인·사전 시간/변위 상한과 같은 stop gate가 필요하고 이번 실행0이다.

수치 사전 산술: radius×limit≈.00266m/s, limit/slew=.1s, 4mm/radius=.03007518767rad. K1의 무지연 선형 오차 시간상수1s는 계산상 값일 뿐 실제 traction/지연/포화 안정성 인증이 아니다. 34.127mm 후퇴는 wheel 회전 하나로 설명되지 않을 수 있어 q latch만으로 base hold를 보장하지 않는다. 기존 로그에서 yaw/steer/raw COM/FD와 wheel excursion을 함께 검토하고 지연/슬립이 설명되지 않으면 dynamics_certified=false 유지. 신호가 부족할 때 K나 quiet threshold를 맞추지 말고 해당 미래 단일 시험의 근거 부족/실패로 남긴다.

## 5. 결정과 검사

**권고: isolate-and-proceed-to-user-approval는 paused inventory 한 회에만 적용. 현재 HOLD physical branch는 중지 상태 유지.** native extension 개발로 확대하지 않는다. paused inventory 검토로 구체적인 process scope를 만들 수 없다면 이 HOLD branch를 멈추고 이미 실제 운동이 확인된 engineering-only legacy ROS/graph route를 별도 목적에 사용한다. 그 route는 이동 가능성 근거가 있으나 34.127mm stop regression 때문에 이 HOLD/terminal 성공의 대체 PASS가 될 수 없다. C++ native lease는 더 강한 강제 경계가 정말 필요할 때의 별도 설계 선택이며 현재 다음 작업이 아니다.

[checks](fe2e_v02_bounded_owner_20261020_v01/checks.json), [최종 검사](fe2e_v02_bounded_owner_20261020_v01/tests_final.txt), [known subset](fe2e_v02_bounded_owner_20261020_v01/known_locks.json).

- PASS: standalone USD read, Isaac loaded=false; existing429SHA mismatch0; known subset hash/count 재검사; 새4개 AST parse; focused4tests(변경 source/extension/stage fault latch, native attest 부재, no-motion entry call 금지).
- FAIL 기록 보존: 최초 AST 검사에서 dict.update를 app.update로 오인한 test1 실패는 tests.txt에 남겼다. receiver를 구분해 수정 후4 PASS. 전체 filesystem 검색 중 screenshot directory permission denied와 처음 잘못 찾은 config/joint_io 경로도 있었다. 실제 contract는 evaluation/, 실제 runtime output은 attempt_0001 아래로 구분했다. 설정 변경/권한 우회/실험 재시도 없음.
- UNKNOWN: 실제 새 paused admission, enabled extension source closure/callback ownership, physical sign/dynamics/quiet/pause stall delivery. 새 검사 PASS를 owner/physics PASS로 치환하지 않는다.

변경은 새 scripts1/evaluation1/analysis2, 본 보고서와 증거 directory, PROJECT_STATE append뿐이다. 원본 v07/host/contract/USD/controller/locked manifests/기존 결과는 보존했다. 별도 protocol/approval flags true 작성, Git staging/push 없음.
