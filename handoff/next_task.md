# NEXT 2026-10-22 — ACTUAL CONSTRUCTION-SITE RGB-D -> FROZEN YOLO -> B4/B5 POSE (ONE ENGINEERING SMOKE)

## Status and non-negotiable context
Just completed: reports/construction_site_lit_preview_render_20261022_v01.md.
Usable, truly rendered source scene, not a mock:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/construction_site_e2e_lit.usda
Actual headless PNG:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/static_preview.png
HEADLESS_VISUAL_PASS (robot frame/body/wheels, 300 cement HR_Scan bricks+wooden pallet, construction-site floor/columns/windows clearly visible), Kit load/capture PASS, host EXITED0. GUI lifecycle still UNKNOWN. Actual lighting is preview-only Dome2500 + new RectLight6000; do not silently treat this as frozen SDG/evaluation lighting. Single rover, single physics scene, render product active, stale calibration consumer fixed, camera actual preview position and rover/brick pose locked. Preserve originals and prior outputs/hashes.
User is exhausted by dozens of pointless camera/graph mock validations. Move the RESEARCH forward instead of making more proof-of-concept USD preview variants.

Research objective: test whether 3D asset representation strategies (HR_Scan/LR_Scan/Proxy/GeoCAD, cement/red bricks) affect synthetic->real perception and downstream robot pose/approach alignment. Current visible fixture is **cement HR_Scan 300 bricks nominal** only. Real robot front mounted camera:
 /World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera
 Existing trained YOLO11-seg and frozen inference checkpoint(s), synthetic RGB-D annotators distance_to_image_plane, frozen B4/B5 pose+target logic are in research project assets/scripts. Reuse ACTUAL source & checkpoint, NEVER mocked detections, never pass fixture GT world pose to estimation/planning.
Do not assume the exterior preview camera is the on-robot perception camera. A pretty scene photo is not perception evidence.

## ONE SUBSTANTIVE CODEx JOB

1. Inspect real project frozen model paths (e.g. M50_R50 RealAdapted if appropriate) and real camera prim/annotator and B4/B5 implementation and their expected inputs. Read only needed code/report/manifest; no broad audit, no literature search. Identify and document exact existing model checkpoint hash and which trained model representation it belongs to, resolution, class IDs and B4/B5 numerical conventions. If source absent do not invent.
2. Build ONE minimal engineering-only on-robot vision smoke runner to OPEN THE EXISTING **LIT site USD** (or its fresh one-off derived run layer if absolutely required) in Isaac Sim5.1 and render a FRESH image from the actual mounted front camera, simultaneously REAL metric depth (distance_to_image_plane), and camera calibration/intrinsics/extrinsics metadata. Use existing correct annotators/ROS-independent pipeline. No physics.play, no ROS, no articulation movement, no training, no automatic retries.
3. Run real frozen YOLO11 segmentation on FRESH on-rover RGB and then REAL depth-assisted B4/B5 predicted 3D/approach/target (or honestly output NO_DETECTION/INVALID_DEPTH/OUT_OF_FOV with actual sensor evidence). Save overlay RGB and B4/B5 computed target data when possible. Explicitly report detection.conf, segmentation mask area, depth valid pixels, predicted pose frame and predicted target, estimated clearances only if actually evaluated. Avoid calling camera viewport photo a sensor frame. Never use known GT stack position/pose or source USD target as estimator/controller input; GT for offline error evaluation only after predictions frozen. Use existing checkpoint, not a new default untrained model.
4. Confirm mounted camera line-of-sight to stack FROM ACTUAL CAPTURE, not bbox-only. If object is outside FOV, negative result is meaningful; do not fake inference success. If orientation/location must change only to get sensible initial perception, do so only in a NEW engineering derivative with documented approved source-grounded start transformation and NO research GT leakage; preferably return honest OUT_OF_FOV instead of geometry edits. No multiple repeated test variants or parameter sweeping.
5. Execute at most ONE no-motion actual Kit run, only if no GUI/Isaac process is already running (process gate), using existing workstation Python/Isaac5.1 and confirmed model weights; finish actual PNG/NPY/JSON captures before shutdown (the previous file existence race was solved). If cannot run due absent checkpoint/dependency, DO NOT pretend PASS or create ten wrappers; produce precise missing file/module and a small ready-to-execute script. Distinguish an internal exception from host exit0 and hold no-retry after crash.
6. Save actual artifacts to NEW unused run output directory:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v01/
 at minimum front_rgb.png, front_depth.npy, camera_metadata.json, detection_overlay.png when detection succeeds, frozen_model_manifest.json, predicted_pose_targets.json (with status and failure reason), runtime result and log. No manipulation of prior USDs. Script output's exact names must match report and verify existence.
7. Report
 reports/construction_site_front_rgbd_pose_smoke_20261022_v01.md
 with exact results, actual sensor frame thumbnail reference, whether YOLO inference ran, mask, B4/B5 pose and errors, honest fail states, actual host/Kit status and scientific limits. Append docs/PROJECT_STATE.md. Provide ONE concrete next step directly toward building single engineering E2E site rover approach ONLY if sensing and pose succeed. Otherwise focus on ONE proven blocker (e.g., mounted camera cannot see stack) with precise correction, not more separate research architecture projects.

## Safety and research locks
- Workstation GUI should not be asked to run Script Editor; do not launch Kit alongside GUI; no ROS publish, wheels, physics.play, robot motion, persistent controls; no A*/new K1 controller, no QUAL12, no 432 benchmark, research denominator remains0. Previous terminal stop drift34.127mm and raw-root quiet failure, and ROS discovery PUBLISHER_SET blocker remain; do not claim E2E motion success.
- Source asset representation, camera/material hashes, prior scene and model checkpoints, fixed thresholds/hypotheses/protocol unmodified. Do not use GT in perception. Light in lit USD for visual preview does NOT automatically authorize lighting change of frozen study scenes; classify this entire exercise engineering-only until protocol alignment.
- Save partial output if no detection and close simulator. Do not auto retry to force a success. Absolutely no further GUI click-by-click testing requested from user.

Final marker ONLY if report exists:
HANDOFF_REPORT: reports/construction_site_front_rgbd_pose_smoke_20261022_v01.md
