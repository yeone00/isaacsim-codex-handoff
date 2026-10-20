# Full E2E v02 PHYSICS HOLD one-shot runner — 2026-10-20

**RUNNER_NOT_READY / physical NO-GO.** 실제 Isaac5.1 시작·관측·graph·actuator·종료 경로의 새 코드를 작성했으나, 전체 native actuator writer를 배제하는 실제 연결이 없다. 실행 가능한 CLI가 있다는 사실을 물리 runner 완성이나 GO로 해석하지 않는다. 현재 `single-physics`는 승인 계약과 native gate에서 거부되며 SimulationApp 이전에 종료한다. 이 turn에서는 Isaac/graph probe/physics/ROS/actuator/ENG001/QUAL12/432 실행0, 연구 denominator0, 물리 retry0이다.

## 1. 기존 실제 증거와 보존

사용자가 실행한 `/home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v03`의 status, events, graph_result, stage_inventory, manifest, external_v03/final_adjudication 및 대응 host v03/v04/v05·CLI v06·external v03 소스를 정적으로 확인했다. Graph-only를 다시 실행하지 않았다.

로컬 기록: PASS_GRAPH_ONLY, external child0/wrapper0/overall_success=true, eval1/Ack1/Witness1, native trigger/Ack/Witness 각각 delta1, 같은 token/epoch/thread. Wheel `[.03,.03,.03,.03]rad/s`, steering `[0,0]rad`, expected 일치. Physics/actuator/ROS/retry0. Graph manifest **37개 input SHA 일치**, status가 참조한 output SHA 일치. 이것은 physics timing·독점 writer·physical stop 인증이 아니다.

기존 실제 stopping validation의 후퇴 **34.127288744mm** 및 raw-root quiet 실패 **.002619135991m/s > .002**를 유지한다. Pose/FD/native/wheel dq가 고정된 관측으로 raw-root 실패를 지우지 않는다. 원본 one-shot session의 open floor, RuntimeRover reference, 6초 비영 곡률 profile, 정상 감속, 8초 zero 관측을 읽고 사용했다.

보존 확인은 [baseline](fe2e_v02_physics_hold_runner_20261020_v01/preservation_baseline.json)과 [결과](fe2e_v02_physics_hold_runner_20261020_v01/preservation_result.json)의 **429개 SHA PASS**다. 기존 output·source·asset·controller·protocol을 변경하지 않았다. [known locks](fe2e_v02_physics_hold_runner_20261020_v01/known_locks.json) 9개 hash/count PASS; 108/432행 유지. 이번 known-subset 검사는 새 pairing/full dependency closure 인증이 아니다. 실제 simulator stage의 동적 closure도 UNKNOWN이다. `.git`이 없어 git status는 실패했으며 staging/commit/push를 하지 않았다.

## 2. 새 실제 연결 코드

| 파일 | 구현 및 실제 연결 지점 | 검증 수준 |
|---|---|---|
| `evaluation/fe2e_v02_physics_hold_host_v01.py` | PhysicsSession, PhysicsAckermann, NoRetryOwner, raw-root terminal evaluator | compile/offline PASS; 물리 미실행 |
| `scripts/fe2e_v02_hold_one_shot_v07.py` | 실제 SimulationApp, 새 USD/override, Articulation 초기화, baseline, 단일 episode, 승인/hash gate, terminal journal | CLI/admission 검사 PASS; 물리 미실행 |
| `scripts/fe2e_v02_physics_hold_external_v01.py` | child 단1개, stdout/exit/status 보존, 외부 최종 판정 | 판정 분기 검사 PASS; child launch 미실행 |
| `analysis/test_fe2e_v02_physics_hold_runner_v01.py` | 새 gate·barrier·fault·raw COM·외부 판정 회귀검사 | 8 tests PASS |

생산 경로는 `live()`→`PhysicsSession`이다. simulator import는 live 설치 함수 안에서만 일어난다. `admission`은 simulator-free 검증이며 생산 경로에 synthetic pose/receipt 또는 `offline=True` 우회가 없다. 기존 `PhysicsIntegration`의 mock 전용 봉인을 해제하지 않았다.

**실제 step 순서:** PhysX `subscribe_physics_step_events` receipt → `app.update()` 복귀 후 정확히 receipt1/시간진행/dt 검사 → live tensor q/dq·steer·base/COM/root-origin/FD·USD pose/clearance/contact 관측 → owner admission → 동기식 impulse→Ack→execOut ScriptNode → 같은 frame/token/thread의 witness1 및 native node count 각각 delta1 → 이름으로 매핑한 wheel6 velocity/steer4 position write와 native target readback → 다음 물리 advance. 따라서 같은 acquisition frame 안의 계산·쓰기이며 **그 결과가 이미 끝난 physics step에 적용됐다고 주장하지 않는다.** 실제 callback 순서, USD sync, graph scheduling, 다음 step의 응답은 UNKNOWN이다.

기존 PhaseDispatch와 StoppingAdapter의 `.07 / KMAX / PRE_FINAL / 6sim s` profile 및 정상 BRAKING을 유지한다. Graph 입력에는 기존 gain15와 `degrees(atan2(-.7*z,abs(v)))` 변환을 사용한다. Native graph 출력을 wheel rad/s·steer rad로 직접 전달하고 middle wheel은 기존 FL/FR 복사다. Radius/drive/gain/controller/물리 topology를 고치지 않았다. Graph-only synthetic `.015/zero steer`는 실제 episode profile에 사용하지 않는다.

MOVING=APPROACH, BRAKING=DECEL, ZERO_SETTLING에서 **같은 sample의 wheel q·실측 steering·base를 먼저 latch하고 owner를 HOLD로 전환**한다. 그 step에서 legacy graph zero/steering zero를 먼저 쓰지 않는다. HOLD는 wheel-position 오차→제한된 wheel velocity feedback이며 wheel stiffness를 바꾸거나 native position drive를 추가한 것이 아니다. 8초 HOLD 관측 후 wheel zero를 명시적으로 쓰고 STOP_OBSERVING으로 봉인하여 8초 독립 정지 관측을 한다. 성공/실패 모두 단일 episode 종료이며 재개·재시도 없다.

## 3. 소유권·pause·판정의 구체적 한계

세 legacy ArticulationController의 native joint명/입력 upstream을 기존 `patch()`로 검사한 뒤 새 override에서 비활성화한다. 이후 composed stage의 활성 OG node는 Ack/impulse/witness 세 개만 허용한다. ROS bridge 활성, legacy writer 재활성화, 추가 script/graph, target readback 불일치는 실패다. 모든 실제 write 바로 앞에도 native exclusion과 epoch/thread/guard를 다시 검사한다.

이 검사는 **외부 native direct writer가 같은 값을 쓰거나 값을 복원한 경우를 탐지하지 못한다.** 설치 `Articulation` 소스는 tensor target setter/readback을 제공하지만, 조사 범위에서 모든 native writer의 producer registry나 exclusive lease를 얻는 실제 port를 찾지 못했다. 따라서 `NativeExclusionUnavailable.attest()`가 구체적인 blocker를 던진다. 이는 fake certificate가 아니라 **미연결을 나타내는 실패 port**다. 현재는 `native.attest(0)`을 SimulationApp와 play 전에 호출하므로 명령0·physics0으로 거부한다. 미래의 real port가 연결되어야 실제 stage/script/native writer inventory를 제출할 수 있다. 지금 그 inventory를 확보했다고 주장하지 않는다.

Wall watchdog는 별도 thread이고 actuator를 쓰지 않는다. 실패는 thread-safe queue로 보내고 Kit thread의 post-update 및 session pump가 `timeline.pause()`를 호출해 playing readback을 기록한다. Kit가 멎으면 REQUESTED가 전달되지 않을 수 있다. **stalled Kit emergency halt 보장은 UNKNOWN**이다. 외부 wrapper도 process kill을 physical stop으로 간주하지 않는다. 새 owner는 write 실패 때 zero를 다시 쓰지 않고 fault latch와 pause 요청만 한다. 따라서 소유권을 잃은 상태에서 두 번째 명령을 시도하지 않는다. Pause 자체는 quiet/정지 PASS가 아니다.

관측은 raw COM, COM 보정 root-origin, FD, native velocity, pose, named joint q/dq, contact headers 및 live whole-rover AABB→floor edge clearance를 보존한다. Safety/evaluation GT는 perception/pose estimation/task goal 입력으로 보내지 않는다. Contact observer는 독립 읽기이나 같은 Kit/PhysX process에 의존한다. 빈 200×200m floor 외 collider는 거부한다. 이는 ENG001 장애물 clearance/transfer 인증이 아니다.

**성공 조건:** 실제 정상 DECEL→ZERO_SETTLING latch→HOLD, 모든 owner/graph/readback/observer gate 통과, HOLD 변위≤4mm/yaw≤.005rad/wheel excursion≤.03007518767339501rad, 종료 zero target의 지속 readback, 8초 post-release 관측, 마지막 온전한1초 root-origin와 **raw COM 둘 다≤.002m/s**, FD≤.002m/s, pose span≤.002m, engineering HOLD-entry reference에 대해 long/lat 각각≤.03m와 yaw≤2°, stable control receipts≥6, pause 전달/readback, terminal_success와 외부 exit0 모두 필요하다. 이 reference는 ENG001 FINAL이 아니다. HOLD 구간 자체의 마지막1초 quiet도 요구한다. Terminal 실패는 그대로 failure다.

Measured motion/FD speed 상한 .03m/s, excursion2m, clearance .10m, dq≤1rad/s, freshness/step≤.04s, wall watchdog .1s, motion-profile wall20s, episode wall40s/sim30s 및 post-release wall20s를 넘으면 실패한다. Max-time bound가 정상 감속/물리 정지를 보장하지는 않는다. 기존 frozen terminal tolerance/quiet를 완화하지 않았다.

현재 proposed 값 K=1s⁻¹, target±.02rad/s, slew .2rad/s², signs(+1×6), 4mm/.005rad/8s는 **그대로 미승인**이다. 별도 승인본 contract 경로를 받되 숫자/sign은 후보와 일치해야 하고 runtime/signed/dynamics 승인, sign resolved 및 encoder-target sign·dynamics 근거의 실제 path/hash가 필요하다. 이를 새 evidence-backed 버전으로 작성해야 하며 원본 contract를 바꾸면 preservation gate가 실패한다. 새 승인은 아직 만들지 않았다.

남은 blocker는 세 가지다.

1. **Native actuator exclusivity 실제 연결 없음.** 가장 작은 다음 engineering 작업은 별도 새 process에서 해당 articulation의 모든 native target/effort producer를 열거·차단하거나 독점 lease를 강제하는 port를 실제 API에 연결하고, 침입 writer 차단/readback 증거를 내는 것이다. 단순 callback 목록, Python monkeypatch, 승인 boolean은 대체물이 아니다. 설치 API로 불가능하면 경계를 강제할 수 있는 native extension이 필요하다. 범용 control-system 재작성이나 graph-only 재시험은 필요하지 않다.
2. **수치/sign/HOLD 정책 근거와 별도 사용자 승인 없음.** 원본 보존한 새 contract+evidence, 정확한 runner/host/contract/output에 묶인 수동 승인 필요. Unit test나 미서명 template은 승인이 아니다.
3. **실제 physics/observer/stop 경로 미실행.** 앞선 두 gate 해결 후 별도 승인한 단일 prospective trial에서만 timing·sensor sync·HOLD/zero stop을 판정한다. Stalled Kit pause 한계도 승인자가 인지해야 하며 guaranteed halt로 바꾸어 쓰지 않는다.

## 4. CLI와 별도 수동 승인 절차 — 아래 physical 명령 실행 금지

현재 admission은 이동 없이 hash/proof/blocker를 기록하고 **의도적으로 exit1 / RUNNER_NOT_READY**다. 실제 보존 출력은 `fe2e_v02_physics_hold_runner_20261020_v01/admission_0001/`이다. 이 출력은 최종 motion-profile wall20s 명시 추가 직전의 code hash snapshot이며, 최종 코드 admission 분기는 이후 오프라인 targeted test에서도 다시 검사했다. 이전 snapshot을 수정하지 않았다.

```bash
python3 scripts/fe2e_v02_hold_one_shot_v07.py \
  --mode admission --domain 191 \
  --output reports/fe2e_v02_physics_hold_runner_20261020_v01/NEW_UNUSED_ADMISSION
```

아래는 **native binding 완료와 최종 코드 검토 후 사용자에게 별도 승인받을 단1회 physical call**이다. 이 turn에는 실행하지 않았다. 지정 output과 `.external_v01`은 보고 시점 모두 미존재다. Contract/approval 경로는 앞으로 새로 작성·서명해야 하는 파일이며 현재 존재·승인을 주장하지 않는다. 현재 코드로는 native gate 때문에 이 명령도 GO가 될 수 없다.

```bash
ROS_DOMAIN_ID=191 /usr/bin/python3 \
  /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013/scripts/fe2e_v02_physics_hold_external_v01.py \
  --domain 191 \
  --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_PHYSICS_HOLD_ONE_SHOT_20261020_v01 \
  --hold-contract /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_PHYSICS_HOLD_APPROVED_CONTRACT_20261020_v02.json \
  --approval /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_PHYSICS_HOLD_MANUAL_APPROVAL_20261020_v01.json
```

Wrapper가 `/home/user/anaconda3/envs/hh_isaac51/bin/python`과 v07 `--mode single-physics`를 child 한 개로 호출한다. 자동 retry/다음 trial 없음. Output 또는 external sidecar가 있으면 덮어쓰지 않고 실패한다. Terminal이 없거나 internal FAIL/NO-GO인데 child0인 경우도 외부 실패다. Output에 manifest/events/terminal이 남고 sidecar에 command/terminal.txt/final_adjudication.json이 남는다. Physics failure를 journal에 남긴 뒤 close하며, process exit는 외부 wrapper가 최종 확인한다.

수동 approval JSON 필수값: `scope="ONE_ENGINEERING_PHYSICS_HOLD_EPISODE_NO_RETRY"`, 실제 `approved_by`, `approved_at`, exact absolute `output`, `hold_contract_sha256`, `runner_sha256`, `host_sha256`, `accept_queued_pause_stalled_kit_unknown=true`, `approve_exact_proposed_signed_K_velocity_slew=true`. 승인본 contract의 `approval_evidence`에는 `purpose=encoder_target_sign`과 `purpose=hold_dynamics_support` 각각 실제 `path`와 `sha256`가 필요하다. Native port 연결이 코드를 변경하므로 **그 최종 코드 hash에 대해 다시 승인**해야 한다. 현재 보고서나 사용자 code-only 요청을 그 승인으로 간주하지 않는다.

## 5. 오프라인 검사와 최종 판정

[최종 검사](fe2e_v02_physics_hold_runner_20261020_v01/final_checks.json), [최종 test log](fe2e_v02_physics_hold_runner_20261020_v01/tests_final.txt), [새 code hashes](fe2e_v02_physics_hold_runner_20261020_v01/new_code_sha256.json).

- PASS: 신규4개 파일 py_compile, 새 production gate/barrier/fault/terminal에 직접 대응한8 tests. Native UNKNOWN 거부, duplicate/advanced-frame barrier 거부, write 실패 후 retry0, raw COM quiet 실패 유지, internal FAIL+child0 외부 실패, approval 없이 motion 거부, admission 무launch/명령0 및 기존 output 거부.
- PASS: 이전429SHA, graph manifest37SHA 및 graph output SHA, known9 locks hash/count.
- FAIL/거부 보존: admission exit1의 RUNNER_NOT_READY. 이것은 물리 시험 실패도 graph regression도 아니며 의도된 admission 거부다. Git status는 `.git` 부재로 실패.
- UNKNOWN: 실제 새 graph/physics timing, native 소유권, 실제 q/dq/COM/USD/contact 동기화, HOLD dynamics, post-release physical quiet, stalled Kit pause 전달. Compile/tests PASS로 GO를 발행하지 않는다.

주요 보존 SHA256:

| 항목 | SHA256 |
|---|---|
| authoritative bench USD | `224cac492d267d0403c9402484fcf84011191208fb4689e7e3fc33eadf3756fe` |
| frozen research controller | `bd1a17f3038909c1ba2ce9b66a540570fd30da29def7561aae2033ebc001d472` |
| locked drive contract | `7e6937a2c14f5be4fea4b50dc9cfb7c533a62f5a54eb3885533d2f6cb81ec551` |
| graph-only v03 graph_result | `3a9142f61709bc576a2bde856e00fa6a772c3a4c766b5228bf05672fd2361468` |
| graph-only v03 events | `3312c6914391e5fe09763c710820089ffd54b07b14b21b761724650f3a6a82e0` |

**다음 구체적 작업은 native exclusive write port를 실제로 연결할 수 있는지 확인·구현하는 code-only engineering 작업이다.** 현재 실제 runner 완성을 선언할 수 없는 정확한 이유가 그 미연결이며, 그래프 재탐색이나 generic mock test 추가로 해소되지 않는다. 그 이후에도 별도 수동 승인 없이는 물리 episode를 실행하지 않는다.
