# Paused 증거 이후 단일 물리시험 admission 결정

검토일 2026-10-21 KST. 요청의 20261020 파일명을 유지한다. **STOP_HOLD_BRANCH.** Paused inventory는 완료되었다. 추가 graph-only/paused 실행이나 전역 native registry 개발을 다음 단계로 요구하지 않는다. 현재 자료로 v07의 K=1 양방향 HOLD를 단일 engineering 시험에 수용할 근거는 부족하다. 새 physical admission 코드/승인 JSON/실행 CLI를 발행하지 않았고 frozen v07 guard를 보존했다. 이는 simulator-only 시험에 대한 결정이며 실제 로봇 검증과 관계없다.

## 실제 증거와 좁은 owner 검토

원자료 root: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_PAUSED_OWNER_ADMISSION_20261020_v01`. `execution_complete.json`, `manifest.json`, `before_inventory.json`, `stage_inventory.json`을 직접 읽었다. [작은 검사 기록](full_e2e_v02_post_paused_owner_physics_admission_20261020_v01_checks.json)에 입력 hash와 집계를 보존했다. 대형 geometry/attribute 원자료는 복제하지 않았다.

193→204 prim, 삭제0, 추가11은 viewport camera/render 경로다. 이전 active17개가 inactive가 되었고 원래 inactive3개를 포함한 graph node20개가 모두 inactive다. ActionGraph container active는 child writer 실행의 증거가 아니다. 원본 articulation_controller, _01, _02 및 Twist subscriber 모두 inactive다. 두 ROS bridge는 before/after 모두 false. script/python/behavior 속성 후보와 scripting applied schema는 0이다. 16 layers 중 파일이 있는15개의 기록 SHA를 현재 파일과 대조해 모두 일치했다. Session layer에는 독립 파일 hash가 없다. 이 과정에서 원본을 수정하지 않았다.

아래 설치 경로의 공통 root `I=/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim`. **rover에 자동 연결되는 actuator callback의 confirmed present 항목은 없다.** 일반 callback 등록과 rover actuator writer를 구분했다.

| 후보 / 판정 범위 | 직접 확인한 source 또는 runtime 사실 | 판정 |
|---|---|---|
| 기존 graph3 writer / ROS 입력 | 위 실제 stage20 inactive, bridge2 false | 해당 recorded process의 실행 경로 absent 확인 |
| `isaacsim.robot.wheeled_robots` | `I/exts/isaacsim.robot.wheeled_robots/isaacsim/robot/wheeled_robots/impl/extension.py:25`: startup은 native interface acquire, shutdown은 release. Python startup에는 rover 검색·Articulation 생성·actuator subscription 없음 | Python 자동 rover writer absent; native 내부 producer는 UNKNOWN |
| `isaacsim.cortex.behaviors`, deprecated sample_behaviors | 각 `config/extension.toml`의 python.module과 해당 `__init__.py`: behavior library/이전 이름 경고. Framework `cortex_world.py` 경로도 표적 검색했으며 이 rover 선택/자동 callback 시작 근거 없음 | 이 module startup에서 자동 rover writer absent. 명시적인 world/behavior 생성 가능성을 실행 중 writer로 세지 않음 |
| `omni.kit.scripting` | `I/extscache/omni.kit.scripting-107.3.2+107.3.2/omni/kit/scripting/scripts/extension.py:29–34`, `script_manager.py:63–71`: timeline/stage subscription을 자동 설치. `:277–295` OmniScriptingAPI prim에서 scripts 적용, `:125–136` 생성된 instance의 on_update 호출 | 일반 callback 등록 present(source); 실제 prim script 연결0이므로 이 stage에서 연결된 behavior writer absent. 살아 있는 callback 객체 목록 자체는 미기록 |
| `omni.graph.scriptnode` | `I/extscache/omni.graph.scriptnode-1.50.0+107.3.0/omni/graph/scriptnode/_impl/extension.py:145–176`: attach/setting callback은 scriptnode 검사·graph enable 상태 관리 | 일반 callback 등록 present(source), 독립 actuator writer 아님. Paused stage에는 활성 scriptnode 없음 |
| `isaacsim.replicator.behavior` | `I/exts/isaacsim.replicator.behavior/isaacsim/replicator/behavior/extension.py:20`: startup pass. Scripting에 붙은 behavior도 원자료에서 없음 | 자동 rover writer absent |
| `omni.physx.tensors` / `omni.physics.tensors` | 실제 `I/extscache/omni.physx.tensors-107.3.26+107.3.3.lx64.r.cp311.u353/config/extension.toml:27`은 native plugin 로드. target API 제공과 producer 실행은 별개 | rover에 연결된 writer 확인 근거 없음; native 내부 callback ownership UNKNOWN |

301개를 wholesale 감사하지 않았다. 위 absent 판정은 표의 특정 시작 경로/기록 stage에만 해당하며 모든 native callback 부재 인증이 아니다. `callbacks='none installed by this entry'`도 extension callback 부재를 뜻하지 않는다. `shutdown_completion=UNKNOWN_EXTERNAL_EXIT_REQUIRED`를 유지하며 외부 exit0 확인을 주장하지 않는다.

## 과거 named wheel 증거로 해결된 부분과 남은 부분

원자료: `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01/{graph.json,attempt_0001/joint_io.json,attempt_0001/steps.jsonl}`. Graph 명칭/배열 순서로 FL,FR,RL,RR target을 대응했고 middle L/R은 index0/1 복사임을 확인했다. `joint_io.json`의 이름→DOF index로 q/dq를 읽었다. pulse의 연속 sample 중 이전 sample의 네 graph target이 모두 >0.1 rad/s인303쌍만 집계했다. 지연 fitting이나 gain 선택 기준이 아니다.

| wheel | DOF index | 누적 Δq rad | Δq>1e−5 / Δq<−1e−5 sample쌍 |
|---|---:|---:|---:|
| front_left | 6 | +0.501991 | 303 / 0 |
| front_right | 7 | +0.564997 | 303 / 0 |
| middle_left | 2 | +0.512821 | 303 / 0 |
| middle_right | 3 | +0.503467 | 302 / 0 |
| rear_left | 8 | +0.513910 | 303 / 0 |
| rear_right | 9 | +0.555260 | 303 / 0 |

관측 범위에서 양의 target→양의 encoder 이동은 여섯 이름 모두 지지된다. 그러나 모든 wheel의 해당 구간 순간 dq 최소값은 음수도 포함한다(세부값 checks). 음의 graph wheel target sample은 전체 로그에서0이다. 따라서 전 구간 dq sign agreement, 음의 target 응답, 새 direct setter의 동특성까지 인증하지 않는다. Zero 뒤 자연 후퇴는 음의 명령 응답 시험이 아니다.

추가 코드 사실: `evaluation/fe2e_v02_wheel_hold_adapter_v01.py:106–113,149–151`은 encoder에 sign을 곱하고 API target에 다시 같은 sign을 곱한다. 대칭 saturation에서 두 sign은 복원 방향상 상쇄된다. +1×6을 기계적 부호 인증으로 채택하거나 sign을 바꿔 지연/슬립 문제를 고쳤다고 해석할 수 없다. 기존 파일은 수정하지 않았다.

K=1 s⁻¹, ±.02 rad/s, slew .2 rad/s²는 여전히 **시험 후보**다. radius×limit≈.00266 m/s는 wheel surface 산술이며 base cap 보증이 아니다. 과거 로그에는 이 K와 steering latch의 closed-loop HOLD가 없다. 이전 후퇴34.127288744 mm와 raw-root .002619135991 m/s > .002 quiet 실패를 유지한다.

## 실행 결정과 다음 한 단계

실제 blocker는 두 가지다.

1. **HOLD 응답 근거 부족:** 여섯 named joint의 양·음 direct target readback→다음 q/dq/시간 응답과 제한된 position restoration을 함께 관측한 기록이 없다. K=1 안정성/복원 여유를 historical forward graph 로그만으로 판정할 수 없다.
2. **현재 실행 가능한 bounded 경로 없음:** `evaluation/fe2e_v02_bounded_owner_v01.py`는 paused 전체 attribute fingerprint라 physics 중 변하는 pose/q에 그대로 적용할 수 없다. Frozen `PhysicsSession.step()`은 advance 전 safe projection을 재확인하는 별도 bounded 구현이 아니며 v07은 native.attest에서 launch 전 차단된다. 이번 STOP 분기에서는 새 계약 설계를 계속하거나 이 guard를 우회하지 않는다. 이것은 범용 C++ lease가 필요하다는 결론이 아니다.

가장 작은 빠진 측정은 **한 episode의 동기화된 named wheel target-readback/q/dq/시간 응답 기록**이다. 향후 별도 승인한다면 기존 이동 경로를 쓰는 감독형 비연구 demo의 저속 이동→정상감속→zero 구간에서 이를 수집할 수 있다. 단, 음의 target과 실제 HOLD 복원까지 평가하려면 별도 사전 명시된 bounded signed segment가 필요하며 forward demo만으로 채워졌다고 하지 않는다. 시간/변위/명령 한계와 stop 시점을 먼저 고정하고 이상 응답 시 pause·종료, retry0으로 해야 한다. 이번에 그 segment 또는 실행을 승인/구현했다고 주장하지 않는다.

**권고하는 다음 행동은 기존 알려진 mobility engineering 경로의 감독형 simulator demo 1회에 대한 별도 요청이다.** 알려진 경로는 `scripts/fe2e_v02_stopping_validation_session_v01.py` + `scripts/fe2e_v02_stopping_validation_ros_v01.py`이며 실제 동일 attempt 증거가 있다. 별도 요청 시 그 demo의 최종 source/contract hashes, 미사용 output, 정확한 명령을 고정하고 명시적 사용자 승인을 받아야 한다. 현재 HOLD 물리 CLI는 제공하지 않는다. Demo 이동 성공은 frozen terminal stop PASS가 아니다. Root+COM+FD quiet .002, clearance/speed gate 및 independent watchdog의 stalled-Kit pause 전달 보장 UNKNOWN을 유지한다. Threshold 완화·sleep 판정으로 치환하지 않는다. Full E2E/QUAL12/432는 HOLD다.

## 보존과 검사

PASS: 기존 preservation429 SHA 불일치0, paused manifest source5 불일치0, recorded file layers15 불일치0, prim path/active 차분 및 historical named303쌍 집계 완료. Frozen runner SHA `77dc13092bc3e27b34f9f95b37ffc432aa58e99b6b53a3382479a6622e8b65a0`, host SHA `a4a3c1f41725cb55d37c76578eca4df10bc544e2750828c595c8d1cc43a6328e`, HOLD contract SHA `230662b8ecd38655fac0ed2df6e466c26a5dac876ae32b3f09b577b4277f46b8`. 이것은 새 물리 승인 대상 hash 묶음이 아니다.

FAIL/기록: tensor config의 처음 추정한 build suffix 경로 읽기는 실패했다. rg로 실제 설치 경로를 찾아 확인했다. 실험 attempt는 아니다. UNKNOWN: native ownership/음의 target·closed-loop HOLD 동특성/실제 one-shot stop/외부 shutdown. Protocol/432 pairing readiness를 이번 표적 검사 PASS로 대체하지 않았다.

변경 파일은 본 보고서, 작은 checks JSON, `docs/PROJECT_STATE.md` append뿐이다. 새 admission code는 STOP 선택에 따라 추가하지 않았다. Isaac/SimulationApp/graph 실행/physics/ROS publish/actuator/retry=0, 이번 engineering·research denominator 기여0. 기존 결과·원본 USD/controller/protocol·v07·수치 contract·이전 실패를 보존했다. Git stage/push 및 package 설치 없음.


## 2026-10-21 요청 재확인 — 최종 실행 결정 유지

동일 이름의 보고서와 checks가 이미 존재하여 덮어쓰지 않고 이 절만 추가했다. 이번 turn에서 실제 paused JSON 네 파일과 manifest를 다시 읽고 기존 checks의 입력21개 SHA를 대조했다(불일치0). 보존429개 및 file-layer15개도 직접 재계산하여 불일치0, prim 추가11/삭제0/graph20 inactive를 확인했다. Historical steps와 named DOF를 다시 읽어 303 pulse sample쌍의 위 여섯 순증가 값 및 negative-target row0을 재현했다. v07 runner/host, bounded_owner, paused entry, adapter와 표의 주요 extension startup/subscription source를 정적으로 읽었다. 이 검사는 새 runtime inventory 실행이 아니다.

**최종 결정: STOP_HOLD_BRANCH.** Native 잔여 UNKNOWN 자체를 범용 lease 개발 요구로 바꾸지 않는다. 구체적인 HOLD 응답 근거가 부족하므로 지금 새 process-scoped 물리 entry를 구현해도 시험 준비 완료가 되지 않는다. 기존 paused fingerprint를 물리 safe projection으로 간주하거나 v07 native guard를 approval flag로 대체하지 않는다. 새로운 코드·contract·physics CLI·approval artifact를 추가하지 않았다.

빠진 최소 측정은 여섯 named joint의 실제 signed target readback→다음 q/dq/시간 및 복원 응답을 묶은 **한 episode 기록**이다. 다음 작업은 알려진 mobility 경로의 감독형 simulator demo를 별도 요청하여, 필요 signed segment를 포함할지 먼저 정하고 최종 source/contract hash·정확한 명령·미사용 output·시간/변위/명령 상한을 고정한 뒤 한 번만 명시 승인받는 것이다. 현재 forward 이동 demo만으로 양방향 HOLD가 인증되지는 않는다. 이번에는 승인 질문이나 실행을 하지 않는다. Root+COM+FD quiet와 기존 speed/clearance/terminal 기준, stalled Kit의 pause 전달 한계, 실패 denominator 및 retry0 규칙은 유지한다. Full E2E/QUAL12/432 HOLD.

이번 turn 변경: 이 보고서와 PROJECT_STATE의 append뿐. PASS는 위 정적 원자료 대조 범위이며 native ownership/negative-target HOLD dynamics/외부 exit는 UNKNOWN이다. 새 Isaac·physics·graph 평가·ROS 발행·actuator·retry0, engineering/research denominator 기여0. 기존 checks·source·USD·controller·protocol·실패 결과는 수정하지 않았다.
