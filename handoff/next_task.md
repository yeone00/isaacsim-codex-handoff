# v16: Perception-based PRE and FINAL approach

Read the latest v15 report. Investigate and address the TF_STALE issue while preserving the existing freshness and safety checks. Avoid repeatedly reading growing logs on each tick if unnecessary. Correct the zero-receipt ordering so the receipt belongs to its cleanup request. Reuse the existing validated camera, inference, steering, and collision-checking code. After focused tests, conduct a bounded integrated run toward newly inferred PRE and FINAL goals if the path is safe. Record measured arrival, stop, cleanup, and process outcomes honestly. Do not repeat unrelated analysis or scientific trials. Save a new v16 report and update latest_report and PROJECT_STATE.

HANDOFF_REPORT: reports/construction_site_perception_approach_20261101_v16.md
