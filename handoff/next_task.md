# ACTIVE NEW TASK v10-A — EDIT SOURCE CODE, NOT v09 LOG RECHECK — 2026-11-01

CRITICAL: The previous Codex completion was WRONG TASK. It only reread previously completed /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v09_runtime_01/ and appended "identical request received" to the SAME old v09 report. It made NO SOURCE CODE EDIT. The user did NOT ask for a v09 repeat. This current task is **SOURCE CODE PATCH ONLY**, NO Isaac Kit, no physical driving, no new preliminary audits. Do NOT treat prior v09 runtime data as completion of this v10-A task.

MANDATORY COMPLETION CONDITIONS:
(A) Create a new **different** versioned Python source file at scripts/construction_site_drive_session_20261101_v10.py derived from v09, with actual execution ordering fix.
(B) Make any absolutely necessary minimal companion edits if runner/ROS imports need v10 session. Preserve v09 original source and all v01-v09 results.
(C) Add small regression test reproducing missing cleanup marker before cleanup and proving a normal stop+cleanup receipt finalizes correctly; ensure missing receipt and real faults still fail. Run CPU tests/compile.
(D) Write a **NEW** report reports/construction_site_drive_cleanup_patch_20261101_v10.md showing old/new source SHA256, exact changed method/line, test outcomes. Do NOT reuse, append or report the historic file reports/construction_site_drive_v09_runtime_20261101_v01.md as your deliverable.
(E) No launch of Isaac Kit, ROS drive, HPO, training or full 324 E2E here. The user wants fix and then separately A→B 50mm real target driving, but THIS task only changes code. No status of physical v10 drive may be PASS; mark NOT_RUN.

KNOWN BUG, NOT AN OPEN RESEARCH QUESTION:
Source scripts/construction_site_drive_session_20261101_v09.py: near line354 evaluates ok requiring (O/'zero_published.json').exists() before its finally cleanup near line371 sends zero_request.json to observer which only then creates zero_published.json. In real v09, physical rover moved +21.505355835mm along +Y, zero and stationary quiet PASS, child/observer/Kit exit0, but runner exit1 because it checked the marker too early. Real timestamps show cleanup request preceded receipt by about 0.0073741 wall seconds. No genuine watchdog/fault in that run.
Fix v10 execution order in an idempotent and bounded way: normal child completion+physical quiet certificate -> request cleanup observer zero -> await actual observer zero_published receipt and verify zero content/response & owner processes cleanly terminated -> evaluate final success predicate -> serialize run_status/report. Ensure genuine abort/fault paths still zero and FAIL. Avoid double cleanup or deadlock in finally; make sure signal handling and false markers cannot upgrade failures. Preserve existing guard/physics/velocity/task thresholds; do not simply remove the marker condition or force success.
Minimal scope is important: inspect v09 original source code and adjacent runner/ROS imports first, implement the fix, CPU test. Do NOT rerun entire project hash inventory, create fake failure reports, or revisit geometry/ROS discovery, all already succeeded.

Scientific boundaries: Original rover USD with supplier ROS /rover/cmd_vel ActionGraph is working. Historical v09: MOVED YES, STOPPED PASS, planned original B50mm NOT REACHED (remaining28.496601mm), runner NOT_READY. Do not rewrite history or call source patch runtime-success. HPO PAUSED; research denominator0.

If and ONLY if the new Python source and new report exist, finish:
HANDOFF_REPORT: reports/construction_site_drive_cleanup_patch_20261101_v10.md

Otherwise explicitly state why no source could be modified, never report "v09 already finished" as a legitimate resolution.
