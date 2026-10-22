# URGENT 2026-10-22 — FIX ACTUAL GUI VISIBILITY of construction-site preview (not another theoretical frustum PASS)

This replaces the earlier RGB-D/YOLO task for ONE targeted GUI preview repair. The user's ACTUAL Isaac Sim 5.1 screenshot of existing preview contradicts the offline camera check:
- Open file: /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/attempt_0002/construction_site_e2e_preview.usda
- GUI viewport toolbar explicitly says "ConstructionPreviewCamera".
- Render shows a SMALL, distant, OVEREXPOSED construction site only against large white background, approx 250px wide in ~810px viewport. NO identifiable rover, pallet or cement bricks.
- Stage shows /World/ConstructionSite and collapsed /World/ENG_FE2E (not visibly marked inactive). The intended preview was an actual close, recognizable SITE + ROVER + PALLET/300 CEMENT BRICKS together.
- This is NOT a successful preview! Do not tell user to manually expand nodes, press F multiple times, send more screenshots, tweak attributes, or restart numerous times.
- Current Isaac GUI IS OPEN on workstation; DO NOT launch another concurrent SimulationApp, ROS, physics or motion. Original scene open UI marked * in earlier screenshots: do not save changes into any original/old USD.

Previous report: reports/construction_site_isaac_preview_20261021_v01.md
Previous preview builder scripts/build_construction_site_preview_20261021_v01.py
Previous derived preview manifest JSON and camera_geometry_checks.json in attempt_0002.
It claims camera at (-30.5,25.4,2.7) target (-25.85,29.65,0.7), rover (-25.88797768,28.4708691133,-.00835194) and fixture (-25.888,30.509,.00121562), one active rover and a 300-brick cement HR_Scan pallet. That claim was OFFLINE ONLY. Investigate why it does not render as intended in the actual user's GUI.

## DO THE WORK — ONE REAL VISUAL PREVIEW FIX, not a diagnostic report only

1. Inspect actual existing preview USD via USD/PXR (use known Isaac bundled pxr environment, not an arbitrary python with missing pxr):
  - Camera authored XformOps, opOrder, composed local-to-world transform, orientation, look axis (-Z) and up (+Y); actual frustum/matrix, focalLength, aperture, clipping planes, shutter, camera prim relationships, DefaultViewport metadata, geometry visibility.
  - Recompute projected image locations AND approximate on-screen pixel extents of rover and Fixture from authored world bounding boxes using USD convention and camera world transform; validate expected "large enough" and CENTERED. Do not conflate offline theoretical requested target with camera actual authored pose.
  - Composition for /World/ENG_FE2E/Rover and Fixture: active/inherited visibility from ancestors; loaded payload, material, geometry descendants counts, size, USD BBoxCache world ranges, 300 brick actual mesh/reference instances, whether relationships refer to suppressed legacy actors, bad references or offset transforms. A nominal reference count isn't evidence meshes are visible. Report site/rover/fixture bbox, camera clipping and actual relative positions.
  - Identify and FIX root cause of why user can see only distant site: wrong view camera orientation/authoring, unbound viewport camera, clipping, hidden/failed geometry, incorrect site-frame placement, or missing texture/lighting. Confirm with real composed USD data; categorize unverified branches as hypotheses.
  - Do not rebuild entire research scene, guess new random assets, change frozen scientific poses or change old 300-brick membership. If fixing site placement genuinely requires a NEW preview-only visual pose, state exactly why and keep scientific geometry unchanged in source.

2. Produce ONE NEW versioned corrected preview file in UNUSED output path:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_VISIBLE_20261022_v01/construction_site_e2e_visible.usda
 (if path exists, fail without overwrite and report collision).
 Make GUI default view a REAL authored close camera in which the rover BODY and pallet/brick stack are both visually sizable (~at least several tens of pixels each) while recognizable real construction environment forms background. Provide overview camera separately if useful. Camera frame should use actual USD camera axes, explicit composed world xform and projection, not only settings target. Preserve all ORIGINAL source and v01 preview USD untouched. Keep original floor/collision and one robot/PhysicsScene, inactive action graph; no ROS/motion.

3. Validation must address failure: project actual composed world-bounds corners for rover and pallet to image-space under actual corrected authored Camera Xform. Require projected centers inside frame with >15% image width/height (practical but avoid false precision; report actual ratios), no near/far clip issues, physically plausible bounds and visible descendants. If can't make both fit at a recognizable size, create a second "robot + pallet detail" camera with explicit default selected. Catch white/washed material only if relevant and source-backed. Avoid repeating full 411 dependency list unless one missing active material directly explains invisible body.
 The GUI is open so do not auto-launch another SimulationApp. You may optionally use a LOCAL NON-SIM rendering preview only if it is already available; do not claim screenshots verified by GUI unless actually observed. A USD validator can PASS geometric checks but GUI_VISUAL remains UNKNOWN until opened.

4. Output NEW builder patch/script if needed, small manifest (camera world matrix, image projection, material/mesh count, geometry bbox and source hash), report:
 reports/construction_site_visible_preview_fix_20261022_v01.md
 State exact diagnosed cause and what changed, new actual file path, what is visually expected, what remains unknown; do not label GUI visually PASS without evidence. If the true issue is failed USD geometry references, repair with existing REAL files/prim paths, not fake proxy cubes.

5. Keep next study flow after fixing user-visible scene: real on-rover front RGB-D + frozen YOLO + B4/B5; forward-only approach later subject to existing physical stop and ROS guard failure. Do NOT do these until preview is usable, do NOT new graph/ROS/HOLD project, audits, 432-run. Limit code-only action to scene repair, no physics.play, no actuation, no parallel Isaac launch. User should only have to open ONE newly created file once, not repeat screenshots for many proposed variants.

## Important provenance
Actual report before fix recorded v01 preview USD SHA faf516f5d44b2e61a59eaafff54ad6a524a5bb5c5087a5788e352e63c50b6a19 and 300 asset refs. Asset is cement_brick_HR_Scan.usd source hash a3fbf6bd87d71007ae756a3288140d842d6e91135ee10d230a4ce52780d8f87c. Preserve.
PROJECT_STATE append, old data untouched, no benchmark results.
Last line after NEW report:
HANDOFF_REPORT: reports/construction_site_visible_preview_fix_20261022_v01.md
