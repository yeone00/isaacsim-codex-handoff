# Full E2E v02 — Graph-only v03 REAL PASS. Finish one-shot PHYSICS HOLD engineering runner.

상태: READY_FOR_MANUAL_APPROVAL_FOR_CODE_ONLY. One-shot physical motion is NOT approved by this file.
Date: 2026-10-20.
Project: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013

## What is already proven (DO NOT REPEAT)
User ran ONE REAL Isaac5.1 graph-only preflight:
 /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_GRAPH_ONLY_PREFLIGHT_20261020_v03
 + .external_v03/final_adjudication.json
Verified observed status PASS_GRAPH_ONLY, wrapper overall_success=true, process exit0, graph_evaluations=1, actual Ack compute=1, Witness=1, native trigger/Ack/Witness delta1 each, same token/epoch/thread, four wheel outputs [.03,.03,.03,.03]rad/s, two steering [0,0]rad, expected match, physics_callbacks=0, actuator_writes=0, ros_publishes=0, retry0. This establishes the Ackermann execution graph, not actual physical control or stop.
Review status.json, events.jsonl, graph_result.json, stage_inventory.json, external adjudication, and corresponding source at start; preserve outputs.
There is NO reason to run more graph-only probes, rewrite OnImpulse, re-audit relative OG exec paths, or tune synthetic inputs.

## Core objective: finish executable ONE isolated simulator physics test path
The user needs one actual engineering mobility calibration: in the existing open-floor bench, nonzero curvature → normal DECEL → ZERO_SETTLING latch → wheel-position HOLD → validated stop; one episode only, no ENG001/QUAL12/432. NOT an endless additional abstraction design.
Consult AGENTS.md, docs/PROJECT_STATE.md, old actual physical stopping validation and measured reverse 34.127mm, latest hold owner/adapter/numeric contract, new v02 host port/binding, v03/v04/v05 graph code, actual graph/rover USD and original one-shot scripts. Preserve immutable research controller, USD, protocols and thresholds.

Deliver actual code, not yet another mock-only report:
1) Produce one **concrete versioned Isaac5.1 physical runner** using the existing proven graph execution mechanism at simulation physics steps. Separate 'graph-only proven' from 'same-physics-step timing actual physical path UNKNOWN'. Use actual step/session callback, synchronize graph completion witness, acquire wheel q/dq+steer+base with explicit frame/epoch, implement owner APPROACH→DECEL→HOLD latch-before-write. No fake receipts, no synthetic poses in actual runner. Original robot motion command profile from existing measured test, no broad rewriting of control system.
2) Establish exclusive actuator ownership with actual stage/script/native writer inventory, disabled legacy ArticulationControllers, explicit single writer and target readback, protect against foreign writers. If exclusion cannot be evidenced, fail closed with a specific recorded blocker and do not issue wheel commands. Do not satisfy condition merely by toggling an approval boolean. The graph-only witness result is not an ownership certificate.
3) Bind actual independent observer (raw COM/root-origin/FD, joint q/dq, pose, contact/clearance, speed), independent watchdog to Kit-thread pause queue, terminal journal, no retry, max motion/speed/excursion/stop envelope and failure exit. Do not assert guaranteed emergency halt under stalled Kit. Stop failure stays failure. Uphold frozen terminal limits and current proposed/unapproved HOLD K/sign/velocity/slew; parameter approval requires explicit evidence/user signoff.
4) Make the exact one-shot entrypoint and CLI with new exclusive unused output + external final adjudication. Provide two explicit modes only if technically necessary: admission/verification (no movement) and SINGLE actual physics episode (gated). CLI MUST NOT silently move robot without separately granted permission. Offline regressions only where they directly exercise the new runner's wires and failure paths. Do not prioritize adding generic mocks/test counts instead of completing the running path.
5) One prospective trial ONLY; do not execute now. Explicit precise success/failure and required approvals. Report residual blockers max three. If actual runner cannot be completed with current host/API, say RUNNER_NOT_READY with exact missing real connection and smallest next engineering step; never claim GO based on green unit tests.

## Execution boundaries FOR THIS CODEX TURN
READ, EDIT, and offline unit-test only. NO Isaac/SimulationApp launch, ROS publish, physics.play, actuator commands, motion, ENG001, QUAL12, 432-run, automated retries, experiments, sweeping gains, relaxing acceptance gates. Keep native named joint topology and previously recorded reverse+raw-root quiet failure. Keep previous evidence and hash inventory intact.

## Exit artifacts
- Versioned actual runner/host binding modifications and actual executable CLI, code compile/targeted tests. Distinguish production physical path from preflight/mock branches.
- reports/full_e2e_v02_physics_hold_one_shot_runner_20261020_v01.md: 1) which actual connections are now complete, 2) what remains runtime UNKNOWN, 3) owner/pause guarantees and concrete blockers (<=3), 4) exact single physical trial call command (DO NOT execute) with manual approval protocol and exclusive output, 5) GO/NO-GO and preservation hashes.
- Append docs/PROJECT_STATE.md; no modification to frozen assets/controller/protocol.
- LAST line of final message ONLY if actual report exists:
HANDOFF_REPORT: reports/full_e2e_v02_physics_hold_one_shot_runner_20261020_v01.md
