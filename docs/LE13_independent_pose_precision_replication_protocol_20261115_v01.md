# L_E13 independent pose precision replication — 2026-11-15 v01

**STATUS: PLAN LOCK CANDIDATE / NOT RUN. This file is not experimental evidence.**

## Purpose
Independently determine whether the exploratory HR-Scan smaller pose error observed in the completed L_E13 540-drive study replicates on **new held-out scene families**. Avoid reusing E1/L_E13 trial B01-B36, training scenes or selected C-V03 training imagery as new test observations.

## Prospective experiment
- L_E13 within `Constructionsite_isaac.usdz`, frozen original weights (before C-V03 retraining), frozen ROBUST_A, calibration, camera/exposure/lighting, nominal geometries, and GT convention.
- Identify **36 previously unused, provenance-disjoint source scene families**. If not available, report INDEPENDENCE_NOT_ESTABLISHED instead of fabricating new families or reusing old ones.
- For each family, generate 5 fixed depletion load states C100/C80/C60/C40/C20, and render 3 representations HR_Scan/LR_Scan/GeoCAD. **36 × 5 × 3 = 540 new static RGB-D captures**, not full 540 physical rover drives.
- Each same-family/load triplet must have identical camera position, yaw, lighting, stage, depletion history and GT; vary only representation and its already-frozen associated model. Store all hashes, seed, original source ID and camera pose.
- Primary precision analysis uses **K1 first-view captures only**. Never substitute K2 recovery capture into the paired pose-error comparison. Independently report K1 detection and pose-completion rates for the full intended denominator.
- Record all missing observations, infrastructure failure, and GT alignment issues. Never exclude B10-like failures because they are large. Do not change threshold/model based on new observations.

## Precommitted statistical analysis
1. Primary metric is horizontal GT pose error in mm on K1 valid poses. Match three representations within family×load, then calculate HR−LR and HR−GeoCAD differences.
2. Aggregate paired differences across the 5 loads **within each genuinely independent family**; family, not individual image, is the inferential unit.
3. For two prespecified comparisons: two-sided paired t-test on family means, 95% CI, Holm multiple-comparison correction (alpha 0.05). Also family-block bootstrap and sign test as sensitivity analyses; clearly distinguish exploratory components.
4. A claim that HR is statistically superior to **both** comparators requires both adjusted p<0.05 and both mean differences negative; report effect size in millimeters and engineering relevance relative to camera calibration/110 mm task criterion. No equivalence claim without a prespecified engineering margin.
5. Include family counts, matched K1 triplets, missing rates, residual K1 pose error distribution, signed x/y and yaw error. Report all outcomes, favorable or not.
6. Keep completed original 532/540 drive-success results separate: this study evaluates pose precision, not new driving task success.

## Immediate Codex task
Audit full previous source IDs (training, validation, old 540), freeze an actually disjoint 36-family manifest with hashes before first capture, adapt the existing Isaac Sim static RGB-D capture and ROBUST_A pipeline rather than building a second navigation pipeline, render 540 static triplet-matched captures, and run the frozen family-level inference. Preserve all original artifacts, prepare traceable result CSV/figures, and report PASS/NOT_RUN/INDEPENDENCE_NOT_ESTABLISHED truthfully.

This document was prepared from existing L_E13 results; it cannot establish independence or statistical significance of future captures without execution.
