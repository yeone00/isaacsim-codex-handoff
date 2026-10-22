# IMMEDIATE REPAIR 2026-10-22 — PREVENTABLE STAGE-METADATA FAIL, THEN REAL FRONT-CAMERA RGB-D/YOLO SINGLE SMOKE

User is understandably furious about repeated expensive headless Kit launches that fail before any sensor capture due to assumptions we could and MUST have checked offline first. STOP creating multiple audit phases and withholding real sensor evidence. In THIS ONE CODEX TURN: correct the preventable stage metrics issue, PRE-FLIGHT ALL OTHER STATIC ASSUMPTIONS before Kit launch, and if genuinely ready run exactly one no-motion real on-rover sensor/inference smoke.

## Grounded exact evidence
Read reports/construction_site_front_rgbd_pose_smoke_20261022_v01.md and source scripts/outputs. Previous v01 produced:
- ERROR in scripts/construction_site_front_rgbd_capture_20261022_v01.py line27: assert units == 1.0.
- Stage opened: /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/construction_site_e2e_lit.usda
- LIT top-level composition reports UsdGeom.GetStageMetersPerUnit = 0.01m and GetStageUpAxis = Y, because top-level LIT/runtime-fixed/visible layer DOES NOT author stage metrics. Base recovery and original preview attempt_0002 authored metersPerUnit=1.0 and upAxis=Z. Correct meaning of scene world positions/geometry is 1m/Z.
- Old Kit launched one time, aborted BEFORE creating annotators or capture, internal FAIL yet host/wrapper exit0. No RGB, depth, inference or B4/B5 outputs. DO NOT pretend NO_DETECTION/OUT_OF_FOV.
- Frozen existing model checkpoint: /home/user/hh/isaac_cosmos/sdg_final/final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_HR_Scan_M50_REALVAL_MASKBEST_v01.pt; SHA256 257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca; class0 brick_load; YOLO11 seg actual loaded in sdg_tools env. Locked B4/B5 source /home/user/eval_step25_pose_final_locked_v01.py SHA cc95b96c3305dcbe257a40fcf16f0e68a9e58ae0d5ae43f9cbd31e80ffec0988. Existing on-robot front camera /World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera, not preview camera.
- Lighting preview scene has real render visual PASS, robot + 300 cement HR_Scan bricks + pallet visible in EXTERIOR camera, not yet proven from FRONT camera. GUI lifecycle unknown. Do not touch original/preview old outputs.

## REQUIRED ACTION (one joined job, no incremental back-and-forth)

A. Fix stage-unit metadata at root CAUSE with a completely new immutable working input OR a stage session-layer override, whichever reliably yields active composed stage 1.0/Z in Isaac Kit. Prefer writing a NEW thin/derived USD layer with BOTH:
  metersPerUnit = 1.0
  upAxis = "Z"
authoring stage root metadata explicitly, while referencing/sublayering existing lit site with same authored composition and without changing original source USD, rover, scene mesh xforms, camera, light, or 300-brick membership. Validate composed result via bundled pxr offline.
  Alternatively session-only override allowed via actual OpenUSD API:
  with Usd.EditContext(stage, Usd.EditTarget(stage.GetSessionLayer())):
      assert UsdGeom.SetStageMetersPerUnit(stage, 1.0)
      assert UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
  then re-read UsdGeom.GetStageMetersPerUnit(stage), GetStageUpAxis(stage). NOTE stage metadata in a SUBLAYER is insufficient; explicitly read stage composed results at top-level. Treat incorrect return as preflight FAIL. The root-layer approach is preferable if any session behavior ambiguous.
  Do NOT scale model by 100, rotate stage or call reference transform correction: the source coordinates are already in 1m/Z. This is metadata correction ONLY.
  OpenUSD evidence: https://openusd.org/release/user_guides/schemas/usdGeom/overview.html and https://openusd.org/release/api/class_usd_stage.html — stage metrics and root/session layer authoring.

B. BEFORE ONE KIT LAUNCH run a fast offline preflight, on REAL target scene and script configuration, fail with exact concise issue, NOT another generic stage:
  - exact intended stage composed 1.0m/Z and BOTH metrics authored
  - front camera Prim is active, loaded, is UsdGeom.Camera, correctly mounted, with valid projection/clipping and nondegenerate world pose
  - correct robot and fixture shapes, 300 bricks, single rover, /Render active and intended headless render product accessible
  - actual checkpoint exists, SHA matches and can load in installed inference environment (already loaded in previous report); pose source exists SHA matches
  - imported code/module/annotator ID names and effective output destinations can be resolved enough to avoid preventable static assertions; no arbitrary zero-frame/float equality checks.
  - B5 requires an INDEPENDENT physical pallet datum, which remains unproven; this is not a blocker for taking RGB-D and doing YOLO/B4, so treat full B5 as NOT_EVALUATED instead of killing the smoke. Never inject fixture/world pose as B5's input.
  - ensure output path is new UNUSED version, e.g. /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_FRONT_RGBD_POSE_SMOKE_20261022_v02 ; old v01 failed output cannot be reused or overwritten.
  - confirm no running Isaac GUI/Kit before launch. No other instance while GUI open.

C. Correct actual live sensor runner:
  - Use full LIT site scene but corrected 1m/Z, on-rover FRONT camera (not exterior preview camera), one RGB+meter depth distance_to_image_plane+camera_params capture with existing live Isaac5.1 replicator/annotator implementation (no fake data).
  - Await asynchronous capture file writes and verify complete PNG/NPY/JSON before closing Kit. The previous async-capture race is already fixed; retain that logic.
  - Run REAL frozen checkpoint YOLO11-seg on FRESH captured RGB, mask->depth pose B4, then B5 only if genuine independent datum is available. Never use fixture GT poses or root authored transform in model inference.
  - If no detection/invalid depth/camera front misses brick stack, SAVE FRESH RGB and depth and report accurate reason, not another failure from an unnecessary assert; record line-of-sight from live image. Failure cases count useful sensor smoke evidence.
  - Do not change camera/object pose, lighting, controller, physics/protocol.
  - No physics.play, ROS/OmniGraph actuation, robot movement, repeated launches, automatic retries, research denominator count.

D. HOST/INTERNAL STATUS bug MUST be fixed: failure in Kit Python result JSON must yield NONZERO wrapper/host status, even if SimulationApp clean shutdown returns host exit0. A separate host gate may inspect internal result after child exit and exit with nonzero. On failures preserve evidence and don't call it PASS. Avoid throwing an early assertion that prevents saving sensor negatives.

E. After offline preflight PASS, DO EXACTLY ONE ACTUAL Kit5.1 no-motion runtime session, IF no other Kit running. Save in new output:
  front_rgb.png, front_depth.npy, camera_metadata.json, frozen_model_manifest.json, detection_overlay.png (if inference), predicted_pose_targets.json (status & reason), internal/host result and preserved logs. If GT B5 datum unavailable still provide B4 status and image.
  There should be no more "we ran Kit then realized a stage metadata assumption" — preflight the stage metrics without Kit before launch.
  If preflight exposes hard true blocker, resolve in this SAME task when source-derived and safe, THEN single launch; do not stop at creating a preparatory report. If truly impossible, report exact missing module and no Kit run.

F. Deliver concise actual results, NOT another giant audit:
  reports/construction_site_front_rgbd_pose_smoke_fix_20261022_v02.md
  exact new run paths, metadata correction provenance and preflight evidence, whether front RGB/depth actually saved, detection+confidence, B4/B5 target or honest null, Kit internal outcome and host propagation. Append docs/PROJECT_STATE.md; preserve v01 failed evidence/hashes.
  Output final marker exactly once only if report exists:
HANDOFF_REPORT: reports/construction_site_front_rgbd_pose_smoke_fix_20261022_v02.md

## Do not repeat previous waste
No camera/lighting preview variants, no additional renders solely for appearance, no new control algorithms, no generic 100-check test suite, no asset/model training, no QUAL12/432, no motion/ROS, no re-running v01 path, no requests for screenshots/manual user prim property work. The user wants the first real front-camera RGB-D and model output, even if model misses. Finish that if at all technically possible.
