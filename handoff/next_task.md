# ACTION REQUIRED 2026-10-21 — IMPLEMENT two last repairs for legacy supervised mobility ONE SHOT

This is a NEW IMPLEMENTATION TASK. The diagnosis report already exists at reports/legacy_supervised_mobility_one_shot_preparation_20261021_v01.md and MUST NOT be reproduced as the sole result. Aim: make existing MOVING Isaac/ROS path ready for a user's separate authorization to run exactly one simulator-only supervised engineering demonstration. NO physical run in this Codex turn.

Project: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013

## Source of truth
- Read AGENTS.md, docs/PROJECT_STATE.md, reports/legacy_supervised_mobility_one_shot_preparation_20261021_v01.md and observed earlier run (READ ONLY) /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_STOPPING_VALIDATION_20261019_v01/attempt_0001 with parent's run plan, graph/joint_io/isolation/steps/contacts and driver code.
- Existing valid route: /home/user/anaconda3/envs/hh_isaac51/bin/python scripts/fe2e_v02_stopping_validation_session_v01.py --output <NEW>/attempt_0001 --domain 191; ROS child scripts/fe2e_v02_stopping_validation_ros_v01.py created by session. ROS Jazzy bridged, RMW rmw_fastrtps_cpp. Previous supervisor path hardcodes existing output; NEVER execute it again.
- Frozen v07 HOLD branch STOP; no unapproved K1/wheel sign/negative wheel pulses/force position-HOLD. Earlier zero→34.127288744mm retreat and raw-root quiet FAIL .002619135991> .002 preserved. Research ENG001/QUAL12/432 gates remain HOLD.

## Do exactly these two modifications, not more audits
A. VERSIONED copy of prior legacy session/ROS child and a tiny supervisor only as needed for NEW isolated output:
   - before nonzero commands, runtime inspect composed stage existing THREE ArticulationController writers and their joint names/targetPrim/input/source wiring, all 10 named DOF articulation map, ROS bridge and publisher/subscriber/TF/driver readiness in domain191; fail closed on mismatch/unknown; once running, detect publisher/endpoint changes, lost observer, unexpected concurrent writers/actors and stale data, request existing zero/abort/pause. Maintain the previously exercised graph/ROS/driver trajectory and original exact numerical limits; avoid rewriting controller or adding gain tuning. ROS guard must recognize allowed phase transitions, supervisor zero publisher vs driver, not block intended route. No invented universal native C++ writer exclusivity certificate; declare actual scope.
   - external watch/stop interface (abort_motion/zero_request) with process liveness/termination bookkeeping, no stray ROS child. Exactly ONE new attempt, no retry, and unique output path refusal. Launch command must be REAL against scripts that exist, using actual executable Python environments.
B. Finish evaluation with independent real time-series criterion:
   - read actual raw COM/root-origin/FD planar velocities, finite/nonnan with contiguous >=1 simulated second (explicit dt/gap <=.1s), pose displacement span <=.002m, each of three velocity metrics <=.002m/s, and create explicit stop/quiet result, zero-time, signed along/lateral reverse/backward excursion. Do NOT replace raw COM with COM-adjusted origin/FD. If missing or insufficient data mark NOT_READY; preserve original fault and raw logs. Target controller input readback per three articulation nodes, all six named joint q/dq & output targets, contact/floor violation stop gate.
   - output separately MOVED / QUIET / RESEARCH_E2E (always NOT_ASSESSED by engineering-only run); no assertion that motion=terminal success or that zero target=physical stop. Final wrapper verdict must account for internal status not only OS exit code.

## Minimal safe testing / execution boundary
- This Codex task may inspect code/data, create versioned legacy_* scripts, py_compile and TEST WITHOUT LAUNCHING Isaac/ROS/physics/actuation; tests should exercise true stop evaluator and change-detection source path with saved/synthetic fixtures, including prior quiet failure.
- Do NOT execute any new simulator episode in this task. No launch of SimulationApp, no ROS driver, no publish, no actuator target, no negative HOLD pulse, no 432 runs, no novel native lease architecture, no broad unit-test infrastructure.
- Preserve USD/controller/drives/protocol/old outputs and SHA. No weakening speed cap .03 terminal zero phase, emergency >.25, 2m excursion, floor contact/clearance and raw speed .002m/s criterion.
- The user intends the NEXT TURN to be a real one-shot supervised simulator test. Do not indefinitely block with theoretical global native producer proof. If a practical code gate is truly impossible, explain the ONE precise blocking API and minimal workaround; do not simply repeat last report.

## DELIVERABLE (MUST produce NEW named report, not old report)
- reports/legacy_supervised_mobility_one_shot_implementation_20261021_v01.md:
  exact changed files and source hashes;
  realistic test outcomes; named endpoint/ROS/graph guard;
  exact **currently runnable** one-shot fresh output command with env+domain setup and child launch from verified source (prefer atomic fail-if-exists);
  human approval checklist and how to abort from separate terminal;
  zero→quiet math/result path and concise success/failure criteria;
  max 2 real blockers, no inflated SHA dumps.
- If implementation cannot honestly be completed, report truthful NOT_READY and exact last missing code, without another HOLD branch narrative.
- Append docs/PROJECT_STATE.md. Original prior reports unchanged.
- End final message with exactly:
HANDOFF_REPORT: reports/legacy_supervised_mobility_one_shot_implementation_20261021_v01.md
