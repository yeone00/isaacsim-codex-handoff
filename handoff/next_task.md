# CRITICAL 2026-10-22 — FIX CONFIRMED DEACTIVATED RUNTIME PRIMS + ISAAC CRASH IN CONSTRUCTION-SITE USD

This is a REAL observed GUI crash fix, NOT a camera redesign, academic research audit, generic mock unit test, another graph-only run, or another repeated manual screenshot exercise.

## Existing CURRENT user's direct Isaac GUI observations (authoritative)
Opened:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_VISIBLE_20261022_v01/construction_site_e2e_visible.usda
GUI Script Editor READBACK:
 STAGE is exact above path
 /World/ENG_FE2E/Rover exists=true, active=true, loaded=true, visibility=inherited
 /World/ENG_FE2E/Fixture exists=true, active=true, loaded=true, visibility=inherited
 /World/ENG_FE2E/ConstructionPreviewCamera exists=true, active=true, loaded=true
 Camera world position (-29.35,29.4,2.6), viewport bound camera path correct.
 Live world bounds are EXACTLY what the old offline report expected:
  Rover (-26.58353,27.72712,-.00844) to (-25.19242,29.21461,1.56469)
  Fixture (-26.438,29.959,.00121562) to (-25.338,31.059,.50522)
 Yet site is visibly rendered as distant washed-out image, rover/pallet not identifiable. Previous v01/v02 USD camera tests do NOT establish actual viewport visibility.
 READBACK of namespace BEFORE change:
   /Render EXISTS TRUE but ACTIVE FALSE
   /Render/OmniverseKit, /Render/OmniverseKit/HydraTextures and intended viewport RenderProduct all missing
   while vp.render_product_path is /Render/OmniverseKit/HydraTextures/omni_kit_widget_viewport_ViewportTexture_0.
 Native error when switching to /OmniverseKit_Persp:
   [Error] omni.usd: Failed to define UsdPrim </Render/OmniverseKit>
 THIS IS A REAL VERIFIED BAD AUTHORING: disabling /Render prevented normal viewport child RenderProduct creation. Fix in derived USD base, not ephemeral GUI session.
 User manually used TEMPORARY SESSION EDIT TARGET to SetActive(True) on /Render; then observed
    RENDER ACTIVE: True
    RENDER PRODUCT VALID: True
 THIS confirms that /Render was a real blocker. Camera position still matched after fix. BUT:
   [Error] omni.usd: Failed to define UsdPrim </World/Rover_Calibration/rover_base>
   terminate called after throwing pxrInternal_v0_24__pxrReserved__::UsdExpiredPrimAccessError: Used null prim
   Aborted (core dumped).
 The GUI process is now CRASHED / STOPPED. This second problem has NOT yet been conclusively localized: /World/Rover_Calibration ancestor might be inactive, absent, or a runtime script retaining an invalid prim; investigate rather than claiming it is definitely inactive.

## MANDATORY WORK IN ONE CODEX TURN
1. READ real USD and builder source, report
 reports/construction_site_visible_preview_fix_20261022_v01.md,
 original parent site and calibrated derived references, and prior source layer hashes.
 Use installed bundled USD pxr (Isaac conda/omni.usd.libs) for actual loaded stage composition; inspect layer stack's authored active opinions at:
    /Render
    /Render/OmniverseKit and descendants
    /World/Rover_Calibration
    /World/Rover_Calibration/rover_base
    /World/ROBOT_TASK/RuntimeRover
    /World/ENG_FE2E/Rover and Fixture
 and ancestry. Find exactly which NEW preview builder suppress() or SetActive(False) authored the bad inactive /Render, inspect suppression of Rover_Calibration parent. Identify other ACTIVE runtime namespace roots that have accidentally been marked inactive without indiscriminate enabling every prim. Keep original USD entirely immutable.
2. FIX the existing versioned BUILDER in a NEW VERSION, writing a NEW output USD:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_RUNTIME_FIX_20261022_v01/construction_site_e2e_runtime_fixed.usda
 - Never disable /Render or its necessary runtime namespace ancestors. Ensure composed active readback True, enable legitimate viewport RenderProduct creation.
 - Solve Rover_Calibration crash without duplicating rover, replacing research geometry, or enabling old unwanted controllers. If older calibration scripts still refer to /World/Rover_Calibration/rover_base, avoid authored inactive ancestor and remove/disable only specific obsolete writer hooks in a verified safe way, or refactor child aliases/consumer path if genuinely required; do NOT blindly turn on a second active rover, fake success or hide crash.
 - Keep /World/ConstructionSite visible, single intended Rover, single PhysicsScene, Fixture cement HR_Scan 300 actual visible brick meshes, one intended rover front camera and detail preview camera, inactive Actuator ActionGraph during preview, no duplicate floor, original site/rover/assets/hashes unchanged.
 - No camera location/asset pose fiddling unless actual evidence says necessary. Camera world pose (-29.35,29.4,2.6) / target (-25.888,29.4,.65) already geometry-validated, avoid rerunning camera-only redesign cycle.
3. VALIDATE the actual runtime issue, not just static frustum:
  - offline composition hard assert /Render active True and accurate runtime namespace ancestors (record composed active + authored active opinions for /World/Rover_Calibration);
  - check site+rover+fixture bounds/material mesh and root lifecycle;
  - assert no old renderer/calibration actor incorrectly activated.
  - Since user's Isaac GUI CRASHED, and ONLY if process detection confirms NO existing Isaac GUI process, you MAY run EXACTLY ONE non-moving Isaac5.1 Kit/SimulationApp no-physics no-ROS loading smoke of NEW USD and viewport RenderProduct creation with short log collection and camera readback. No ROS bridge, no physics.play, no actuator, no robot movement, no rendering research denominator, no retry. If safe no-physics single live load cannot be done, report precise reason; do not invent GUI success.
  - Prefer capture one actual static render of construction site+rover+Fixture if safe headless viewport capture already exists; if not possible, report GUI_VISUAL_UNKNOWN, but do not claim VISUAL_PASS from bbox alone. Explicitly record host exit/terminal crash status; a core dump must be classified CRASHED.
  - If a second runtime error appears, report the exact path/stack and do not silently make a third trial or series of output variants.
4. If a patch fails, do NOT deliver generic plan/report alone; deliver a concrete corrected USD or explain a specific unresolved engine constraint backed by output. Preserve prior files. New builder can fail closed if real dependencies missing. Do not let a supposed PASS conceal active /Render=False or expired prim crash.

## Strict scope/limits
This is a static PREVIEW repair. No GUI manual script editing, no requests for another dozen screenshots. No Isaac GUI load while other GUI is active; user GUI has reportedly crashed, still check process before any standalone launch. No ROS publish, no physics.play, no robot actuation, no new HOLD/driver/safety controls, no ENG001/QUAL12/432, no automatic retry/sweep. Keep first robotics results and controller/protocol science intact. No original layer edits or overwriting old output.

## Deliverables
- New actual USD in fresh output, versioned builder and short runtime checks, optional one headless no-motion result.
- reports/construction_site_runtime_prim_crash_fix_20261022_v01.md:
  1. /Render deactivation precise source/fix and /World/Rover_Calibration failure evidence (confirmed vs possible);
  2. exact new USD absolute path, authored active diagnostics, geometry/prim uniqueness;
  3. one real no-motion Kit load/RenderProduct result if performed and shutdown status;
  4. if visual preview unverified, accurately UNKNOWN; precise remaining blocker and ONE next user GUI open at most.
- Append docs/PROJECT_STATE.md and preserve source hashes. Final marker only if report actually exists:
HANDOFF_REPORT: reports/construction_site_runtime_prim_crash_fix_20261022_v01.md
