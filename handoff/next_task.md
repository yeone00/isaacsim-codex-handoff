# NEXT — Construction-site perception/pose smoke, NOT flat-floor controls or another USD audit (2026-10-21)

Previous task COMPLETED: actual new preview at
/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/construction_site_e2e_preview.usda
Report reports/construction_site_isaac_preview_20261021_v01.md.
User has the Isaac Sim 5.1 GUI open on workstation; do NOT start a second SimulationApp while GUI runs. Do not request new screenshots or repeated property inspection.

## Actual known state
- Source site /World/ConstructionSite, rover /World/ENG_FE2E/Rover, cement HR_Scan FULL 300 bricks and pallet /World/ENG_FE2E/Fixture, one PhysicsScene; real mounted front Camera and preview Camera.
- Composition static PASS, camera frustum checked offline, active graph0 (purposely DISABLED preview), ROS publish/motion0.
- OFFLINE_PARTIAL specifically missing deps some MDLs/grid URL and local apriltag PNG/mitex JPG, many may be inactive branch. GUI visual status is not yet known. Original USD/assets immutability required.
- Old isolated actual ROS/graph mobility can move rover but zero→stop moved backward34.127mm, quiet failed. Legacy PUBLISHER_SET issue root-cause unknown. New K1 HOLD branch STOP. These are honest downstream blockers; do not misrepresent scene preview as motion readiness.
- Research core: asset-representation performance comparison in CONSTRUCTION SITE. Path frozen RGB-D → YOLO model → B4/B5 depth pose → approach-target determination → actual motion/stop. Ground-truth only for evaluation, never perception/controller input. Freeze controller and scientific locks; QUAL12/432 prohibited until valid one-shot E2E.

## Single substantive deliverable
Prepare (do not run without explicit approval) ONE reproducible and MINIMAL **real construction-site RGB-D perception + B4/B5 pose smoke** using this exact existing scene and front robot camera. The next work must establish whether the actual site scene and study sensor/data/model path function. Do not spend this turn making a new robot controller/ROS safety framework, another graph-only witness or another scene with cubes.

A. Inspect only necessary script/model/camera/source refs and actual pinned frozen weights/shape, existing RGB-D extraction and B4/B5 modules; identify actual paths (no guessed weights), create a small live runner or GUI-safe Python script for ONE engineering frame/short sensor capture from the actual derived scene, real camera RGB plus distance_to_image_plane depth, frozen YOLO11-seg, B4/B5 predicted target, and source timestamps. No offline pre-filled prediction or GT-derived target. If there is no reachable model, report exact blocker.
B. First deal with scene asset appearance pragmatically: via USD analysis identify which missing deps are truly reachable from currently active mesh/shading; either fix ONLY genuinely required active materials with correct existing assets/Kit paths on a NEW derived layer, or keep OFFLINE_PARTIAL and explain what specific appearance might be wrong. Do not download random replacements or touch originals. Avoid repeating wholesale 411-dependency closure.
C. Camera: confirm robot actual front camera is attached to existing robot and sees material in its real frustum. Note preview camera visibility is NOT same as front sensor camera visibility; if front sensor FOV is wrong, adjust ONLY preview-specific initial rover pose/camera or target placement in a NEW scene version and document transform; no GT shortcuts. Do not silently assume object is visible because preview camera sees it.
D. Deliver one NEW versioned sensor-smoke script plus exact one-shot CLI/launch procedure and outputs (frame RGB, depth NPY/metadata, actual inference mask/conf, predicted B4/B5 pose/target or honest NO_DETECTION) and a concise two-page report. If user GUI is still running, do NOT launch new Isaac process; prepare then request GUI closure only before a future explicit one-shot live smoke. Can optionally create a no-motion offline USD camera projection check now. Do not call external ROS bridge or move wheels in this task.
E. No more than 2 true blockers. Keep failures as failures; do not create 15 preparatory wrappers. Source/hash and existing frozen assets stay untouched. Need a meaningful engine-based sensor capture NEXT, not a new audit/safety architecture.

## Authorized now
Inspect/reuse code, produce a NEW small derived USD only if needed, scripts and offline checks, report. NO parallel SimulationApp launch, no physics.play, ROS publish, wheel actuation, physical rover run, automatic retries, QUAL12/432, research denominator change. Do not ask the user to operate GUI in multiple steps.

## Outputs
- reports/construction_site_rgbd_pose_smoke_preparation_20261021_v01.md
- Real script/config with one precise valid executable command (no ungrounded names), independent unused output, frozen model manifest and error/abort behavior. If not implementable due actual missing dependency, specific file+small correction.
- docs/PROJECT_STATE.md append. Preserve all sources/outputs.
- final marker only if report exists:
HANDOFF_REPORT: reports/construction_site_rgbd_pose_smoke_preparation_20261021_v01.md
