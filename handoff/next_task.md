# HOTFIX ONLY — 2026-10-21 supervised legacy mobility run blocked at ROS discovery PUBLISHER_SET

User actually launched ONE supervised simulator-only attempt at:
 /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01
Prior output MUST NEVER be deleted, overwritten, retried, or reclassified as movement success.
External wrapper: PROCESS_EXIT_CODE=1; supervisor_complete.json internal_status NOT_READY, MOVED=NO, QUIET=PASS (stationary baseline only), zero=NOT_READY. execution_complete.json: motion_attempts=0, failure_reason=PUBLISHER_SET, traceback at scripts/legacy_supervised_session_v01.py:153 and evaluation/legacy_supervised_guard_v01.py:23.
Observed passing attempt_0001/isolation_check.json: pass true, TF publisher exactly one expected node, cmd_publishers empty during isolation, cmd_subscribers exactly observer and OG rover Twist subscriber, nodes the expected three names. This does NOT prove the later discovery publisher set was correct. The failing line is:
 assert len(names)==len(set(names)) and set(names)<=({OB,DR} if phase!='isolated' else set()), 'PUBLISHER_SET'
Hence actual failure could be repeated node name, unexpected node, bad prefix/namespacing, or snapshot format. DO NOT GUESS WHICH; inspect real attempt files.

## JOB: ONLY resolve this ONE root cause with evidence and minimum repair
1) Read actual files and source:
 scripts/legacy_supervised_session_v01.py
 scripts/legacy_supervised_ros_v01.py
 scripts/legacy_supervised_observer_v01.py
 evaluation/legacy_supervised_guard_v01.py
 reports/legacy_supervised_mobility_one_shot_implementation_20261021_v01.md
 all relevant JSON status snapshots/logs under existing attempt_0001 (read-only); do not demand a fresh run to diagnose a stored snapshot.
 Trace the exact values of the 'names' list at failed discovery. Identify precisely whether the check rejected an unexpected publisher identity or erroneously treated multiple GIDs/endpoints of an allowed node as spoofing. Report node, namespace, topic/type, GID where present and phase, with a compact excerpt (NOT 300MB logs). If not stored, label ROOT_CAUSE_UNKNOWN and add pre-failure forensic event in new source rather than fabricating cause.
2) Make a SMALL versioned correction or diagnostics only (v02 guard/session/ROS/observer as actually needed). Publisher validation must still reject foreign node/GID replacement, unexpected extra publishers, topic/type/namespace mismatch, stale or vanished observer, driver discovery-phase transitions and conflicting ROS nodes. Prefer per-topic per-GID endpoint identity and expected cardinality rather than collapsing legitimate discovery endpoints by node name. Do not just delete the assertion, set always-true, or weaken the frozen control safety boundaries. Distinguish allowed driver initial appearance from a publisher disappearing after active stage.
3) Regression tests MUST include the saved actual v01 discovery failure data when available, duplicate same-node endpoints with distinct GID, foreign node, unexpected topic/type, GID swap and valid isolated->discovery->active->zero phase transitions; deterministic offline tests and compile, no actual Sim/ROS activity. Preserve all previous sources, USD, contracts and actual attempt logs. Version the entrypoint and pinned source manifest if changed; leave old pinned manifest untouched.
4) Provide EXACT single NEW output command to launch same historical ROS/graph/physics mobility path ONCE after user's separate physical-simulator approval. Ensure no stale output collision, source/hashes and domain191 environment. Keep user-controlled abort instruction and stdout/exit/internal status collection. No automatic retry/sweep; no HOLD K1; no direct signed pulse; previous 34.127mm stop regression remains failure and new MOVED/QUIET/E2E distinct.
5) If actual incident is a genuinely unexpected ROS publisher, DO NOT make it allowed. Report exact publisher and safest minimal next action (e.g. isolate domain or instrument matching). A real foreign publisher must block the physical run, not be hidden to get MOVED=YES.

## Scope boundaries
No Isaac/SimulationApp, physics.play, ROS node creation/publish, actuator command or robot movement in THIS Codex session; no another broad ownership audit / graph-only / paused inventory; no unrelated edits. Exactly one focused diagnostic/fix. The existing full-e2e results are not research denominator. Existing v01 output must remain immutable.
Write new report:
 reports/legacy_supervised_publisher_set_hotfix_20261021_v01.md
Append docs/PROJECT_STATE.md and report actual root cause confirmed vs hypothesized, files/targeted tests, new one-shot command OR named blocker in two paragraphs.
If report exists, final line:
HANDOFF_REPORT: reports/legacy_supervised_publisher_set_hotfix_20261021_v01.md
