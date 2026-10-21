# IMMEDIATE PRIORITY 2026-10-21: ACTUAL CONSTRUCTION-SITE ISAAC SIM SCENE. Deliver it, not another audit.

IMPORTANT: The user is frustrated because they have repeatedly been asked to open USD files, screenshot graph nodes, and run Codex mock probes. Stop that cycle. This task does not request user screenshots or repetitive property inspection. First deliver a usable derived USD scene that is VISIBLY the construction site, with rover and construction material together. Be honest about what cannot be run. NO research sweeps.

Project cwd: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
Isaac Sim conda: /home/user/anaconda3/envs/hh_isaac51/bin/python
Known authoritative source scene:
 /home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd
This contains /World/ConstructionSite and /World/ROBOT_TASK/RuntimeRover (CONFIRMED by GUI screenshots). Also /World/TestSetup, /World/SDGTarget_Mitex, etc. Existing isolated engineering stop bench:
 /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_IMPL_20261021_v01/attempt_0001/derived_calibration.usda
has /World/ENG_FE2E/Rover, EngineeringFloor, PhysicsScene but NO constructed site: THIS IS NOT THE MAIN RESEARCH ENVIRONMENT. Do NOT use this as final study scene or ask user to reopen it. The GUI screenshots confirmed derived bench all 3 Articulation Controller targetPrim=/World/ENG_FE2E/Rover/base_link and correct 4 wheel / 2 steer / 2 middle wheel named joints. Original source contains first controller old robotPath=/rover, but derived runtime patched it; do not edit original USD.
Other existing evidence: real graph-only v03 PASS, legacy mobility prior actual motion PASS but zero-stop 34.127mm retreat & raw-root quiet failure; latest ROS guard v02 still root cause UNKNOWN, do not claim fixed. STOP_HOLD_BRANCH for experimental K1 controller. ENG001 research gates, QUAL12/432 forbidden until true single successful E2E. Frozen 0.03m long/lat, 2 deg yaw, root+COM+FD quiet .002, clearance .10 etc unchanged.

## ONE JOB, complete end-to-end locally where feasible
A. Discover *existing verified* site and material/load USD assets, frozen representation variants/cement-red asset entries, their real prim paths, placement and references from project files, manifests, and scene hierarchy. Limit to files relevant to the scene; do not launch broad literature or inventory audit. Inspect source USD composition using the available pxr from standalone Isaac python/environment; do not assume imported pxr works in arbitrary python. No path guessing, no substitution of random cubes as study materials.
B. CREATE ONE new versioned, immutable source-preserving derived USD at a NEW output dir:
 /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_PREVIEW_20261021_v01/
 Compose/reference the actual /World/ConstructionSite and its correct ground/collision/lighting, working /World/ENG_FE2E/Rover rover reference and appropriate existing site material pallet/brick stack (single verified nominal representative asset; document which representation). Existing site USD already contains rover: avoid duplicate robot, duplicate PhysicsScene, floors, shadows/actors; isolate runtime rover via override and suppress site source rover *in derived composition only*, or reuse existing site rover after carefully patching prim routes. Keep an actual construction-site camera view framing all 3: SITE + ROVER + CONSTRUCTION MATERIAL. Place rover on physical floor and load in realistic reach/access geometry, collision-safe by source bounds. Preserve target distances/geometry and origin layers; don't silently change research data.
 For scene assembly methods, prefer simple USD sublayers/reference/overrides over new ROS control logic. All source USD, frozen controller and scene data must be unchanged, and material assets must resolve via real paths/hashes.
C. DELIVER executable, standalone code or CLI that reconstructs preview deterministically from those verified sources, plus concise manifest with site, rover, material prims and world positions, USD dependencies, screenshot if possible. Give user ONE unambiguous GUI open path; do not require screenshot or extra GUI steps. Since user already has Isaac Sim GUI running, NEVER launch a second concurrent SimulationApp. If safe, use the existing command-line USD-only composition and USD checks without simulation. If preview screenshot cannot be captured without interacting with user's running GUI, report screenshot unavailable, but still deliver usable USD and camera prim to open.
D. Make at most one limited SOURCE-DRIVEN VALIDATION of: derived USD exists, compositions resolve, site geometry present and not hidden, rover visible at floor, actual material present, exactly one active rover and physics scene, graph controller paths correct, no extra ROS publishers/motion. No long unit-test jungle. If full preview impossible because required asset/reference missing, report the exact missing asset/path and produce best honest partial scene, not generic NOT_READY report.
E. Also include a SHORT second-step roadmap (without executing motion): how to bring frozen YOLO RGB-D / B4-B5 and forward-only approach into THIS construction scene; distinguish a real construction-site engineering E2E run from prior isolated stop calibration. State any genuine blocker, especially legacy PUBLISHER_SET and actual stopping failure. No experiments, no autonomous movement, no ROS publish, no ENG001/QUAL12/432. DO NOT start further HOLD algorithms, native ownership projects, paused writer audits or graph-only probes.

## Permissions and constraints
This task authorizes you to create new scene/build scripts, perform OFFLINE USD validation, and prepare GUI-ready scene, not to actuate the rover or conduct new simulation episodes. Do not launch Isaac/SimulationApp in parallel to an open GUI. If underlying USD APIs demand app runtime, use safe no-motion offline builder only, or mark a precise unresolved source issue. Preserve all original source/USD/protocols and earlier reports. Never use target/ground truth from perception to drive rover.

## Mandatory output artifacts
1. Actual new preview USD (not merely proposed path), with saved camera/viewpoint showing active construction site, rover, and verified stacked material.
2. Build script and small manifest, and absolute paths in report.
3. A SMALL new report:
 reports/construction_site_isaac_preview_20261021_v01.md
 Outline exactly what can now be opened/seen in the GUI; asset identity, prim paths, geometry/physics sanity and remaining direct-to-E2E blocker. If incomplete, precise missing file/connection; do NOT fabricate completed scene.
4. docs/PROJECT_STATE.md append, existing files immutable.
Final message last line if created:
HANDOFF_REPORT: reports/construction_site_isaac_preview_20261021_v01.md

EXECUTE scene composition now if local tools allow. Do not stop after a plan, literature search, design audit, or repeated report of legacy publisher guard. User wants an actual construction-site USD, not instructions to manually click through many screens.
