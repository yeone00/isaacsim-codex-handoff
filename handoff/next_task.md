# NEXT 2026-10-22 — REAL CONSTRUCTION SITE VISUAL: FIX DARKNESS AND CAPTURE SMOKE

User has already spent hours repeatedly opening USDs, taking screenshots and running manual GUI Script Editor. No more manual diagnostics; DO NOT ask user to operate camera controls or take screenshots. Deliver real render evidence and ONE ready-to-open USD.

## Latest reliable facts (read full report)
reports/construction_site_runtime_prim_crash_fix_20261022_v01.md
Current stage: /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_RUNTIME_FIX_20261022_v01/construction_site_e2e_runtime_fixed.usda
- CONFIRMED FIXED: /Render active and viewport RenderProduct valid, /World/Rover_Calibration active empty container, stale cameras removed from active renderer, actual Isaac Sim5.1 Kit loaded and ended host exit0 WITHOUT prior native core dump, 1 real rover, 300 real cement HR_Scan brick meshes and pallet, proper scene bounds/camera. Preserve.
- Actual saved headless image static_preview.png (look for file inside above output folder) shows left brick pallet, right rover outline and site but is TOO DARK for practical identification. HEADLESS_VISUAL FAIL, GUI_VISUAL UNKNOWN.
- Prior renderer detail preview light blue-ish DomeLight intensity=350 color=(.65,.72,.85), down from original 2500. Renderer still has possible old tone/correction settings. Need check actual settings and image before choosing exact fix.
- Latest single Kit smoke internal failure: scripts/check_construction_site_kit_load_20261022_v01.py immediately asserted PNG existence after screenshot capture future, but PNG was generated later. Do not count host exit0 as capture success. Fix asynchronous capture completion/wait, properly check image file and record output.
- Exact camera position (-29.35,29.4,2.6) target (-25.888,29.4,.65) is geometry tested. DO NOT change camera or object pose or repeat offline frustum/PXR matrix audit.
- Existing original source files, historical attempted USDs, scripts, checkpoints and frozen experiment parameters must remain IMMUTABLE.

## ONE CONCRETE EXECUTION REQUEST
1. Inspect old real dark PNG quantitatively (luminance distribution, nonzero masks), and inspect in image viewer or local image-processing library, plus the actual active DomeLight/environment/exposure/tone/color settings read from USD/Kit and prior functioning site render settings. Diagnose darkness instead of asserting root cause without checking.
2. Build exactly ONE NEW versioned derived scene (do not overwrite):
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/construction_site_e2e_lit.usda
 Change only necessary preview display lighting, material resolving or color/exposure settings, chosen from evidence. Preserve 1 rover, 300 cement HR Scan meshes, site, preview camera and on-robot camera, /Render active, Rover_Calibration namespace active/empty, one physics scene, graph inactive, existing bounds/placement and science locks. Do not add surrogate materials that defeat real asset fidelity study.
3. If no other Isaac GUI/process is running (user previous GUI crashed, but verify actual process list), conduct exactly ONE NO-PHYSICS NO-ROS NO-MOTION Isaac Sim5.1 Kit loading and STATIC RENDER of new scene. Fix capture future synchronization: wait for saved nonempty PNG and verify before close (no naive immediate is_file assert). Record host exit and internal return separately. No automatic second render if fail.
4. Actually INSPECT output PNG for practical visibility (rover BODY, brick STACK and pallet, site background). Save output PNG, if useful an offline before-after composite; quantify exposure with p10/p50/p90 luminance and clipping. Classify HEADLESS_VISUAL_PASS only if visually recognizable, not merely because camera bounds or code tests pass. Distinguish GUI_VISUAL_UNKNOWN until real GUI observed.
5. Generate concise report:
 reports/construction_site_lit_preview_render_20261022_v01.md
 Include specific cause evidence, modifications, absolute verified USD and PNG paths, honest runtime/capture/visual results and any blocker, input hashes and future one-file GUI-open instruction. Append docs/PROJECT_STATE.md; preserve previous failures and outputs. If still dark, report actual cause candidate from runtime settings and FAIL, rather than another design-audit project.

SCOPE: no robotics controller, ROS publisher, physical motion, physics.play, new HOLD graph, dataset training, ENG001/QUAL12/432-run, experiment denominator adjustment. No GUI manual operations or new unsupported runtime promises.

Output final marker only when report exists:
HANDOFF_REPORT: reports/construction_site_lit_preview_render_20261022_v01.md
