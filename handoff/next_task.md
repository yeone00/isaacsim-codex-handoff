# NEXT TASK v10-B: ACTUAL 50mm TARGET DRIVING IN EXISTING CONSTRUCTION SITE

The previous v10-A task is COMPLETE: new source files were created and CPU tests 11/11 passed. Do not repeat v10-A, recheck the old v09 report only, or submit the same old HANDOFF_REPORT. The user wants the existing rover to ACTUALLY reach planned point B, stop, and finish normally.

First read local reports/construction_site_drive_cleanup_patch_20261101_v10.md and reports/latest_report.md, then inspect the working scripts/construction_site_drive_runner_20261101_v10.py and scripts/construction_site_drive_session_20261101_v10.py. v10 cleanup now requests zero, checks the observer receipt and process exits, then decides final status. This change is not yet tested in actual Kit.

Previous actual runtime v09: with original supplied ROS2 /rover/cmd_vel Action Graph in existing real construction site, one 2s fixed pulse physically moved 21.505356mm in +Y and stopped safely. Driver/observer/Kit exited 0. Its overall runner failed due to cleanup proof being checked before its creation, which v10-A fixed in source. Do not rewrite that historical record.

Declared ORIGINAL target:
A=(-25.887977600098,28.470867156982) world meters.
B=(-25.887977680000,28.520869113267) world meters.
Distance roughly 50mm +Y. The old fixed pulse stopped 28.496601mm short. It did NOT reach B. The previously used coarse +/-30mm diagnostic tolerance cannot be treated as evidence of reaching this particular point.

Required focused implementation and execution:
1) Make the smallest versioned extension of the existing v10 ROS drive to use actual live world base position as feedback and move toward fixed B along the previously cleared straight route. Do not create a new planner, USD, robot, teleoperation infrastructure, synthetic floor, or safety framework. Do not teleport or directly set base pose. Keep original ROS Twist topic, supplier Action Graph, wheel controllers, and safe limits. Explicitly declare a modest engineering position tolerance meaningfully narrower than 28.5mm, a braking/zero criterion, and a finite bound on travel. Measure actual final world distance to B, not commanded distance.
2) Inspect the source timing. The v09 driver's 20-second wall watchdog covers startup and left only ~1.9s after a 2s sim pulse and normal quiet. For a longer physical motion, use a coherent finite per-phase timeout with mandatory emergency zero, preserving genuine collision, command freshness, and physical-stop safety. Do not simply remove watchdog protection or speed limits to force arrival.
3) Use the v10-A corrected cleanup ordering in the new execution path. Focused compile/CPU test first. If no other user Kit/GUI/training is active, run ONE new real Isaac Sim Kit session in the existing original site. Run a single low-speed supervised drive episode, monitor contact/corridor and base pose, brake and zero, then check >=1 physical sim-second quiet, zero acknowledgement, ROS child exit and runner final status. Stop safely on any genuine obstacle, contact or controller fault. Never terminate the user's unrelated processes.
4) Preserve original scene, frozen controller/guard and v01-v10-A reports and code. New output directory must be unused and unique, e.g. /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_TARGET_DRIVE_20261101_v10B_01.
5) Report separate factual results: NONZERO Twist count; initial/final XY; distance to ORIGINAL B; B_REACHED YES/NO using the declared tighter engineering tolerance; MOVED YES/NO; STOPPED PASS/FAIL/NOT_TESTED; cleanup receipt; runner PASS/FAIL; collision safety and any faults. Engineering only, research denominator0. HPO/training PAUSED. No YOLO/B4/B5, HPO, B300, or full 324/432 E2E.
6) Produce NEW report reports/construction_site_target_drive_20261101_v10B.md; update latest_report and PROJECT_STATE. If unable to run, explain the concrete technical blocker and mark NOT_RUN, rather than substituting another v09 reread.

Expected final marker after the NEW report exists:
HANDOFF_REPORT: reports/construction_site_target_drive_20261101_v10B.md
