# NEXT 2026-11-01 — PRESERVE SUCCESSFUL SITE DRIVE; FIX POST-ZERO LIFECYCLE OFFLINE

The user's priority is functioning construction-site A-to-B mobility, not endless inspections. v08 finally achieved REAL physical ROS driving/stop. Read reports/latest_report.md and local reports/construction_site_single_rover_mobility_20261101_v08.md. DO NOT relitigate solved geometry/raycast/TF/ROS discovery.

OBSERVED v08 (DO NOT CHANGE HISTORICAL REPORT):
- One physical run in original site; /rover/cmd_vel, original supplied ActionGraph, 45 nonzero Twist publishes in one episode, physical base +0.021970748901m forward +Y; wheel dq max .362895578rad/s and final dq0. Postzero last 1s raw root/COM/FD stationary PASS, contact PASS, postzero backward excursion from peak .00003623963m, no collision. Native fallback NOT used, no teleport. Thus engineering physical MOVED YES and STOPPED PASS, but waypoint .05m not reached, no full E2E, research denominator0. HPO/training PAUSED.
- ROS discovery guard PASS in .4603s. The previous run's anonymous GID is still UNKNOWN; never claim to have mapped it.
- v08 overall adapter/runner NOT_READY exit1 despite real movement+stop. After MOVING -> BRAKING/NORMAL_DECELERATION at sim6.43333 -> ZERO_SETTLING at sim6.683333682, it went FAULT_LATCHED/EMERGENCY_ZERO at sim8.383333771, about1.7sim sec after first zero. Existing ROS child 20s wall watchdog and session 20s abort/stop are suspect; verify source and timestamps, do not assert cause without testing. Zero commands after fault, so fault must be preserved, not silently converted to PASS.
- Root run_status.json top-level stale MOVED NO / STOPPED NOT_TESTED while nested outcomes MOVED YES / QUIET PASS and measurements demonstrate actual movement/stop. Fix new aggregation code, NOT old historical output.
- Original stage USD, ROS ActionGraph/frozen guard and all v01-v08 code/results must remain untouched.

THIS ONE CODEX TASK:
1. Inspect focused portions only of v08 session/ROS/runner lifecycle/termination and v08 adapter_commands.jsonl, run_status.json, stop_quiet_result.json, execution_complete.json; determine real wall timer trigger vs actual safety fault. Do not create new architecture, physics validator, new scene or alternate controllers.
2. Produce small versioned v09 code derived from v08 that marks successful basic mobility lifecycle only after witnessed nonzero actual base displacement, normal deceleration, zero, >=1s physical quiet hold, proper graph zero and physical safety; terminate owned child gracefully BEFORE normal session cleanup erroneously latches an emergency fault. Genuine motion timeout, lost command, collision, faulty stop or watchdog BEFORE confirmed stop MUST continue to fail; preserve emergency-zero. Do not disable watchdog or rewrite frozen research thresholds.
3. Fix top-level runner status aggregation to match verified measured nested MOVED/STOPPED outcomes. Keep adapter fault field separately if present and do not convert genuine faults to PASS just because rover moved.
4. Run focused source-level and CPU-only tests for (a) normal zero+quiet success, (b) real active-motion watchdog failure, (c) safety/stop failure, (d) correct nested status aggregation. Compile. NO Isaac Kit/ROS physical rerun in this task; last v08 movement milestone already evidenced. Explicitly report v09 runtime NOT_TESTED.
5. New concise report reports/construction_site_drive_lifecycle_fix_20261101_v09.md plus latest_report/PROJECT_STATE as appropriate. Preserve all historical artifacts, source USD, benchmarks, training weights. HPO stays PAUSED, engineering research denominator0.
6. After v09 code is ready, suggest separate future one-shot waypoint A-to-B runtime test using EXISTING ROS graph and existing engineering field/corridor, then fresh YOLO/B4/B5 and final experiments. No large extra checks, new USD, full E2E 324, B300 or HPO now.

Finish marker only if report exists:
HANDOFF_REPORT: reports/construction_site_drive_lifecycle_fix_20261101_v09.md
