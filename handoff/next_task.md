# NEXT TASK — v09 ONE REAL CONSTRUCTION-SITE A→B DRIVE AND CLEAN SHUTDOWN

USER DECISION: Stop proliferating validation code. The existing supplier robot ROS2 Action Graph and actual original construction-site USD already achieved a physical ROS-driven +21.970748901mm forward movement, correct zero and last-1s quiet PASS in v08. It failed overall only because a later wall watchdog entered FAULT_LATCHED and top-level status was stale. The latest v09 code patched normal-stop lifecycle and status aggregation; CPU tests 8/8 + compile PASS but v09 runtime NOT_TESTED. Now execute ONE actual experiment using v09, not another theory/audit-only task. HPO stays PAUSED.

READ: local reports/construction_site_drive_lifecycle_fix_20261101_v09.md and reports/latest_report.md, inspect new v09 CLI source, minimal tests and actual output schemas. Do not confuse v09 offline PASS with physical run PASS. Source:
scripts/construction_site_drive_runner_20261101_v09.py
scripts/construction_site_drive_session_20261101_v09.py
scripts/construction_site_drive_ros_20261101_v09.py
evaluation/construction_site_drive_lifecycle_20261101_v09.py

USE original real site and rover scene, correct 1m/Z active Render, actual pallet and HR cement bricks. Reuse original /rover/cmd_vel ROS2 ActionGraph, existing 3 articulation controllers, tested physics clock, RaycastHit support 2214/2214, shell 9/9, nonpenetrating contact, 0.10m short corridor and ROS endpoint GID guard. NO new EngineeringFloor, new controller, robot teleport, HPO or broad audit. No other concurrent Isaac GUI/Kit/training; never kill user processes.

ONE ACTUAL KIT SESSION if free:
1. Run fresh v09 prepare using its actual CLI and a NEW unused output directory (e.g. /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v09_runtime_01/), then launch once. Do not overwrite v01-v08 or offline v09 outputs. Record real physical time.
2. Publish through existing supplier ROS /rover/cmd_vel a controlled short low-speed forward toward a nearby A→B engineering waypoint in the *previously checked safe corridor*. IMPORTANT v08 generated 21.97mm in 2 seconds, not the full 50mm planned point. If v09 code still enforces a fixed 2s pulse, don't incorrectly claim 50mm waypoint reached; either demonstrate the actual shorter destination (measured and labeled) or use a tested bounded closed-loop target within VERIFIED corridor and elapsed wall watchdog budget. Don't extend past 0.10m obstacle corridor/speed caps blindly.
3. Confirm actual world base pose displacement and wheel q/dq, not only command publishes, then normal BRAKING→ZERO_SETTLING, >=1 real physical-second quiet, graph zero, no physical collision, and v09 child/runner clean exit without late FAULT_LATCHED. Do not call v09 PASS if watchdog or other genuine fault occurs. Preserve existing true 20wall-second hard watchdog and frozen strict study metrics. If timings are insufficient to complete before watchdog, report that precise conflict and fix the lifecycle ordering safely, rather than disable safeguards or falsely pass.
4. Report separate, clear truth values: actual MOVED, distance to the declared B waypoint, STOPPED, clean lifecycle/runner exit, physical safety, research denominator 0. Endpoint A→B reached is NOT identical to simple movement achieved. If any run fails, identify the one real cause and use already-working code, not a new planner.
5. If v09 fails before movement due a proven regressions or source bug, perform only a focused code fix; avoid further repeated heavy tests. No uncontrolled automatic retries. Keep user progress/report brief.
6. Save report reports/construction_site_drive_v09_runtime_20261101_v01.md, latest_report mirror and PROJECT_STATE update. Keep original USD, frozen guard, all previous reports, checkpoints immutable. Do NOT start YOLO/B4/B5, 324-run, HPO yet.

If report created, finish with:
HANDOFF_REPORT: reports/construction_site_drive_v09_runtime_20261101_v01.md
