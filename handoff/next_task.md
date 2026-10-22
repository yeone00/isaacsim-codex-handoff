# NEXT — 2026-10-22: SENSOR-OBSERVED PALLET DATUM ADAPTER v02 + ONE OFFLINE B5 ENGINEERING RESULT

## Current scientifically grounded state
Read reports/construction_site_b5_datum_offline_20261022_v01.md AND reports/construction_site_front_rgbd_pose_smoke_fix_20261022_v02.md. Source report latest confirms:
- Previously captured ACTUAL mounted front camera RGB 640×480, metric depth, frozen HR_Scan YOLO brick_load detection conf0.8027858734, mask29876, B4 heading90.157714844°, gate margin0.001015 < .014116 PASS.
- SAVED output, don't recapture or rerun:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v02/
- Real OBSERVED plane analysis from same RGB-D, not fixture GT:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_B5_DATUM_OFFLINE_20261022_v01/
  ROI overlay, exact masks, candidate_floor_plane.json, candidate_pallet_plane.json, datum_diagnostics.json, provenance.json.
- Observed pallet-top candidate 1810 ROI inliers, near-horizontal normal slope .079751deg, top center world Z .146866635m; floor 62384 inliers, top-minus-extrapolated floor .146449118m, vs separately sourced NOMINAL pallet thickness .144m (+2.449mm). This does NOT prove absolute 2.449mm sensor error; floor is observed outside pallet, planes nonparallel and calibration systematic uncertainty UNKNOWN. RANSAC near-zero residuals reflect synthetic rendered depth, not actual physical measurement accuracy.
- ROI polygons were manually selected using fresh RGB and explicitly saved. So sensor-derived B5, IF computed, is ENGINEERING SEMI-MANUAL evidence, NOT autonomous perception or research E2E success.
- frozen pose source /home/user/eval_step25_pose_final_locked_v01.py SHA cc95b96c3305dcbe257a40fcf16f0e68a9e58ae0d5ae43f9cbd31e80ffec0988; production SHA a3740cd82022a1686794f8da892fb376ad1a02f63c2fe8e842ac1cef864641ad. Current full_e2e_locked_pose_adapter_v01.py only accepts hashed engineering_fixture_design / planned_horizontal_fixture_top_world_m. Do NOT lie or relabel this OBSERVED plane as engineering_fixture_design or edit the frozen source.
- original frozen B5 formula includes Z>=PALLET_H-.020, side fit Z criteria PALLET_H+4*.090-.030 and needs datum scalar. Approx original source scalar .144 is a design thickness, not necessarily world absolute top Z. MUST resolve actual frame/definition from source, not quietly conflate floor-relative thickness, world Z or local Z.

## ONE SUBSTANTIVE JOB, NOT ANOTHER HOLD-ONLY PAPER
Develop a NEW separate engineering-only V02 adapter contract accepting independently sensor-observed horizontal PALLET TOP datum and execute ONE OFFLINE TEST using preexisting files, if physically and code-contract justified. This is a deliberate PROPOSED NEW adapter and must NOT be declared approved for frozen confirmatory evaluation without independent study/protocol signoff.

1. INSPECT current v01 adapter and locked B4/B5 source entrypoints & exact frame/unit conventions, including how PALLET_H is consumed and whether immutable original B5 functions can accept a datum parameter. Record only relevant source snippets/hashes. Determine whether sensor plane predicted top Z can be passed without modifying B5 equations; an adapter may convert observed (normal,d,anchor x/y) to scalar world Z if same frame and horizontal tolerance is satisfied. Document conversion precisely, including uncertainty and reference anchor; NEVER hardcode .146866635 as a new generic constant; read plane JSON and compute.
2. NEW v02 evidence type must be explicit, e.g. sensor_observed_pallet_top_plane_world_v01 (not engineering_fixture_design); fields: source-run IDs/hashes, RGB/depth/camera calibration, ROI mask hash, plane coeff & center/normal/frame/unit, fit inlier count/ratio/residual and support extent, datum plane anchor XY, how scalar pallet top world Z is derived, manual ROI disclosure, sensor scale uncertainty UNKNOWN, independent from fixture pose/GT. Reject invalid frame/up axis, nonfinite values, opposing normals, unsupported slope, weak support, wrong model hash, provenance mismatch, source changes.
3. Carefully reuse original frozen B4/B5 ALGORITHMS unchanged. If they expose a parameterized function, call it with converted datum. If they rely on a hardcoded module-level PALLET_H, do NOT mutate original module/global constant; either implement an explicitly versioned engineering-only adapter of the *same mathematical function* with equivalence spot tests/transparent diff, or if not feasible return a precise named code-contract blocker. Do not silently loosen threshold or use planned_fixture design fake evidence. Preserve original source hashes and previous v01 adapter.
4. Use only SAVED observations; perform ONE OFFLINE engineering B5 invocation, calculate pose and task PRE/FINAL only if B5 gates pass, otherwise save actual failure diagnostic instead of another generic NOT_EVALUATED. Run without Isaac Sim, YOLO model inference, ROS, physics or rover actuation. No repeats/sweeps to force success.
5. Critically evaluate the practical geometry: top Z is at one observed anchor; fitted plane slightly nonparallel, world position accuracy unknown; pallet/brick mask segmentation and ROI were semimanual; a B5 result may be informative but is not autonomous validation. B4 orientation gate is NOT a full pose gate. If pose computed, freeze predictions first; only AFTERWARD separate GT comparison if grounded, not as estimator input. Do not declare collision clearance or robot success without real motion.
6. Save new unused immutable output:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_B5_SENSOR_ADAPTER_20261022_v02/
  adapter_evidence_v02.json, contract_validation.json, b5_prediction.json, predicted_pre_final.json or explicit invalid reasons, source_hash_manifest.json and optional comparison overlay; keep source data unchanged.
7. Write concise factual report:
 reports/construction_site_b5_sensor_adapter_20261022_v02.md
 with real execution result (B5 computed or exactly why not), numeric outputs/confidence/gates if produced, manual ROI and unknown calibration limits, and ONE practical next engineering step. Append docs/PROJECT_STATE.md. No more than one-page executive summary unless evidence requires detail. Do NOT label science protocol approved by coding changes alone.

## HARD RULES
- No Isaac Kit launch, no new capture, no YOLO inference, no ROS, no motion/physics, no controller/A* modifications, no 432/QUAL12/ENG001, no sample inclusion in research denominator.
- Don't edit original USD, original camera/model/checkpoint, frozen B4/B5 source, old adapter, prior outputs or success gates. Don't manufacture a GT-derived pallet Z or brick pose. Preserve hashes.
- No additional GUI clicks or multi-step user manual diagnostics.
- If the existing mathematical code CANNOT be legally wrapped under immutable science locks, state specific boundary and prepare adapter proposal with a concrete path forward; no silent hack. But try hard to provide ACTUAL B5 engineering offline output, not just yet another contract essay.

Final line only if new report exists:
HANDOFF_REPORT: reports/construction_site_b5_sensor_adapter_20261022_v02.md
