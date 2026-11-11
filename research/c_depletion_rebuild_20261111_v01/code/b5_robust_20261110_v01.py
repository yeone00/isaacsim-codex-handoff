"""Boundary-insensitive B5 pallet/load pose estimator, b5_robust v01 (2026-11-10). ENGINEERING / OFFLINE candidate.

Does NOT replace or modify the frozen B5 (scripts/three_rep_B5_sensor_20261102_v44.py + evaluation/full_e2e_locked_core_v01.py);
both must be reported separately. Pure CPU (numpy + cv2). No GT, no GT panel mask, no simulator.

Method family: RGB-D point-cloud geometric correction after the DL instance mask, i.e. detection -> point-cloud geometric
matching -> pose (structure inspired by Tsiogas et al. 2021, IROS, DOI 10.1109/IROS51168.2021.9636270; the specific
sub-techniques below are this module's own choices, not claimed to be from that paper). Matching is only against the KNOWN
COMMON design model (pallet 1.1x1.1x0.144, load footprint 0.950x0.855, layer 0.090) - no representation-specific shape, no GT mesh.

Failure reason codes (status, reason): NO_DETECTION/{ORIGINAL_SELECTED_PREDICTION_ABSENT, EMPTY_ORIGINAL_MASK};
DEPTH_INSUFFICIENT/{NO_VALID_MASK_DEPTH, insufficient_3d_points, insufficient_side_points}; DATUM_REJECTED/{SHAPE_MISMATCH,
FOOTPRINT_INCONSISTENT_EXTENT, EMPTY_PERTURBED_MASK}; PIPELINE_ERROR/EXCEPTION_<type>.

Inputs (sensor + task metadata only): instance mask (bool HxW), depth (distance_to_image_plane, m), camera_metadata (same JSON
as v44: calibration + raw_parameters cameraProjection/cameraViewTransform), layer_count (task metadata), nominal dimensions
(LOAD 0.950 x 0.855, layer 0.090, pallet 1.1 x 1.1 x 0.144 from the locked core constants).

Root cause addressed (analysis/b5_flip_diagnostic_20261110_v01.py): the frozen b5_fit_candidate anchors EVERY axis on a
"visible face" = 2%/98% quantile of side points on the side whose sign is sign(dot(to_camera, axis)); for the lateral axis
of a near head-on view that dot product is ~0 (|view| < .01), so a sub-degree heading change flips the anchor between the
left and the right silhouette (centre jumps by observed_width - 0.855 ~ 5 cm); additionally the 0/90 long/short candidate
is chosen by a near-tie residual score (score difference ~1e-3), which swaps LOAD_X/LOAD_Y (another 4.75 cm).

Algorithm (per axis of a rectilinear footprint):
  1 foreground: depth-gap clustering of mask depths (gap .05 m as B1ADAPT A3) but keeping the FARTHEST cluster that holds
    >= 25% of the largest (an occluder that bleeds into the mask is in front of the target); height band between the sensed
    pallet top and the load top.
  2 datum fallback order: (a) load top sensed from the mask (q99 z) minus layer_count*0.090 when consistent with (b) a sensed
    floor plane (+0.144) within 3 cm; (b) sensed floor + 0.144 when inconsistent (top occluded / wrong); (c) load-top only if no
    floor is observable (B1 scenes have no floor depth; a "floor" fitted on the pallet top is rejected). No design-prior floor.
  3 depth-continuous region growth (<= grow_px around the mask, vertical-face heights only, |d depth| < continuity_m) so the
    support ends at true depth silhouettes instead of mask boundary pixels; horizontal-plane clustering of the vertical-face
    points removes slivers of neighbouring loads.
  4 heading: rectilinear Hough on vertical-face points (mod 90), refined by a line fit to the sensed pallet front face
    (clean 1.1 m cuboid) or, if no pallet face, the load face.
  5 per axis, in priority order:
      PALLET_FACE      the pallet's vertical face below/in front of a visible load face: centre = face -/+ 0.55 (square
                       pallet => no long/short ambiguity, independent of brick stagger and of mask boundaries)
      PALLET_MIDPOINT  pallet face seen over its full 1.10 +- 0.03 m width on the other axis: centre = its midpoint
      FACE             visible load face (dense plane peak on the camera side): MEDIAN plane position -/+ half dimension
      MIDPOINT         edge-on axis, both depth silhouettes free: midpoint (no dimension used)
      EDGE_LO/EDGE_HI  one silhouette occlusion-truncated: free end +- half dimension
      MIDPOINT_BOTH_TRUNCATED  low-confidence fallback
    truncation = support-boundary pixels whose neighbourhood holds a CLOSER non-target surface above pallet level, the image
    border, or a depth-continuous surface beyond the growth radius (treated as UNKNOWN, never as an edge).
  6 long/short hypotheses (axis1=LOAD_X vs axis2=LOAD_X) scored on observed full extents, truncated extents / top extents as
    lower bounds and the load-face-to-pallet-face offset ((1.1-dim)/2); near-tie -> the two hypothesis centres are averaged
    (bounded 2.4 cm instead of a 4.75 cm flip) and flagged AXIS_AMBIGUOUS_HEDGED.
  7 optional mask-perturbation ensemble (median of centres over erode/orig/dilate masks); frozen v01 config: OFF.
Output: same schema as the frozen B5 result: dict(status, reason, pose={center_x_m, center_y_m, heading_deg_180, ...}).
"""
import hashlib, json, math
import numpy as np, cv2

VERSION = 'b5_robust_20261110_v01'
LOAD_X, LOAD_Y, SIDE_H, PALLET_H, PALLET_XY = 0.950, 0.855, 0.090, 0.144, 1.100  # == full_e2e_locked_core_v01 constants (asserted in tests)

DEFAULT_CONFIG = dict(
    version=VERSION,
    depth_gap_m=0.05,            # A3 foreground clustering gap (same value as B1ADAPT_v01)
    cluster_policy='farthest_major', cluster_major_frac=0.25,
    top_quantile=0.99,           # load top = q99 of foreground z
    floor_consistency_m=0.03,    # load-top datum vs sensed-floor datum agreement
    floor_below_load_m=0.10,     # a sensed floor must lie >= this below the lowest load points (else it is a pallet/load surface)
    band_low_above_pallet_m=0.015,
    band_high_above_top_m=0.02,
    side_below_top_m=0.02,       # vertical-face points: z <= load_top - this
    grow_px=6, continuity_m=0.05,
    hough_coarse_deg=1.0, hough_fine_deg=0.1, hough_bin_m=0.01,
    face_min_pts=40, face_min_frac=0.10, face_near_end_m=0.10, face_inlier_m=0.015,
    edge_quantile=0.005, end_window_m=0.03, trunc_frac=0.30, occluder_gap_m=0.05, occluder_radius_px=3,
    hyp_sigma_m=0.02, hyp_lower_bound_tol_m=0.02, hyp_ambiguous_margin=1.0,
    max_extent_over_m=0.30,      # reject footprint if any observed extent > nominal long side + this (mask spans >1 object)
    min_points=30,
    heading_refine_iters=2, heading_refine_max_deg=3.0, heading_refine_source='pallet_then_load',
    use_pallet=True, pallet_z_margin_m=0.02, pallet_min_pts=40, pallet_offset_min_m=0.03, pallet_offset_max_m=0.20, pallet_offset_sigma_m=0.015, pallet_full_width_tol_m=0.03, pallet_lateral_margin_m=0.35,
    component_min_px=150, component_min_frac=0.10, component_cell_m=0.02, top_max_dist_from_side_m=0.75, face_axis_min_full_extent_m=0.40,
    ensemble=None,               # optional ('ero1', 'orig', 'dil1'): median centre over perturbed masks
)


def config_sha(cfg):
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ geometry helpers
def calibration(camera_metadata):
    """Same recovery as v44 estimate(): fx/fy from cameraProjection, T_world_optical from cameraViewTransform."""
    raw = camera_metadata if isinstance(camera_metadata, dict) else json.loads(camera_metadata)
    cal = dict(raw['calibration']); pr = np.array(raw['raw_parameters']['cameraProjection'], float).reshape(4, 4)
    vw = np.array(raw['raw_parameters']['cameraViewTransform'], float).reshape(4, 4)
    T = np.linalg.inv(vw).T; T[:3, :3] = T[:3, :3] @ np.diag([1, -1, -1])
    W, H = int(cal['width']), int(cal['height'])
    return dict(fx=float(pr[0, 0] * W / 2), fy=float(pr[1, 1] * H / 2), cx=float(cal['cx']), cy=float(cal['cy']), W=W, H=H,
                depth_unit_m=float(cal.get('depth_unit_m', 1.0))), T


def world_map(depth, cal, T):
    v, u = np.indices(depth.shape); valid = np.isfinite(depth) & (depth > 0)
    z = np.where(valid, depth, 0).astype(float) * cal['depth_unit_m']
    opt = np.stack([(u - cal['cx']) * z / cal['fx'], (v - cal['cy']) * z / cal['fy'], z], -1)
    world = opt @ T[:3, :3].T + T[:3, 3]; world[~valid] = np.nan
    return world, valid


def depth_gap_cluster(mask, depth, gap, policy='largest', major_frac=0.25):
    """Split mask depths at sorted-depth gaps > gap. policy 'largest' = B1ADAPT A3 (largest cluster); 'farthest_major' =
    the farthest cluster holding >= major_frac of the largest (an occluder bleeding into the mask is in FRONT of the target)."""
    valid = mask & np.isfinite(depth) & (depth > 0)
    if not valid.any(): return valid
    d = depth[valid].astype(float); o = np.sort(d); cuts = np.where(np.diff(o) > gap)[0]
    edges = np.r_[o[0] - 1, (o[cuts] + o[cuts + 1]) / 2, o[-1] + 1]; idx = np.digitize(d, edges[1:-1])
    cnt = np.bincount(idx, minlength=len(edges) - 1)
    if policy == 'farthest_major': keep = int(np.nonzero(cnt >= major_frac * cnt.max())[0].max())
    else: keep = int(np.argmax(cnt))
    out = np.zeros_like(mask); vv, uu = np.nonzero(valid); sel = idx == keep; out[vv[sel], uu[sel]] = True
    return out


def sensed_floor_z(world, valid, mask, xy_ref):
    """v44-style floor: bottom 40% image rows, non-mask, 1 cm height mode + plane fit gates. Returns z at xy_ref or None."""
    H = valid.shape[0]; rows = np.zeros_like(valid); rows[int(.6 * H):] = True
    g = world[valid & rows & ~mask]
    if len(g) < 100: return None, 'GROUND_SUPPORT_MISSING'
    bins = np.floor(g[:, 2] / .01).astype(int); vals, cnt = np.unique(bins, return_counts=True); mode = vals[np.argmax(cnt)] * .01 + .005
    q = g[abs(g[:, 2] - mode) < .01]
    if len(q) < 100: return None, 'GROUND_SUPPORT_MISSING'
    n = np.array([0., 0., 1.]); d = -np.median(q[:, 2]); inl = abs(q @ n + d) < .003
    for _ in range(3):
        if inl.sum() < 3: return None, 'GROUND_PLANE_GATE_REJECTED'
        p = q[inl]; c = p.mean(0); _, _, vh = np.linalg.svd(p - c, full_matrices=False); n = vh[-1]; n = n if n[2] >= 0 else -n; d = -float(n @ c); inl = abs(q @ n + d) < .003
    p = q[inl]; tilt = math.degrees(math.acos(min(1., abs(n[2])))); res = abs(p @ n + d)
    eig = np.linalg.eigvalsh(np.cov(p[:, :2].T)) if len(p) >= 3 else [0, 0]
    if not (len(p) >= 100 and inl.mean() >= .8 and tilt <= 5 and eig[0] > 1e-5 and np.quantile(res, .95) <= .003): return None, 'GROUND_PLANE_GATE_REJECTED'
    return float(-(n[0] * xy_ref[0] + n[1] * xy_ref[1] + d) / n[2]), 'SENSED_FLOOR_OK'


def grow_support(seed, cand, depth, steps, tol):
    """Depth-continuous 8-neighbour growth of `seed` into `cand` for `steps` iterations."""
    sup = seed.copy(); H, W = sup.shape; d = np.where(np.isfinite(depth), depth, np.inf).astype(float)
    for _ in range(steps):
        front = cv2.dilate(sup.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & cand & ~sup
        if not front.any(): break
        ok = np.zeros_like(sup)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0: continue
                ss = np.zeros_like(sup); ds = np.full_like(d, np.inf)
                ys, yd = slice(max(dy, 0), H + min(dy, 0)), slice(max(-dy, 0), H + min(-dy, 0))
                xs, xd = slice(max(dx, 0), W + min(dx, 0)), slice(max(-dx, 0), W + min(-dx, 0))
                ss[yd, xd] = sup[ys, xs]; ds[yd, xd] = d[ys, xs]
                with np.errstate(invalid='ignore'): ok |= front & ss & (np.abs(ds - d) < tol)
        if not ok.any(): break
        sup |= ok
    return sup


def pallet_faces(world, valid, mask, sup, pallet_top, axes, dlo, dhi, cfg):
    """For each footprint axis: the pallet's camera-side vertical face (z in pallet body, below the load, 0.02-0.20 m in
    front of the load's camera-side boundary). Returns per axis None or dict(pos, n, other_lo/hi/mid, full_width)."""
    vv, uu = np.nonzero(sup); H, W = sup.shape; h = vv.max() - vv.min() + 1; w = uu.max() - uu.min() + 1
    win = np.zeros_like(sup); win[vv.min():min(H, vv.max() + int(.8 * h) + 5), max(0, uu.min() - int(.3 * w)):min(W, uu.max() + int(.3 * w) + 1)] = True
    zz = world[..., 2]
    with np.errstate(invalid='ignore'):
        sel = win & valid & ~mask & (zz >= pallet_top - PALLET_H + cfg['pallet_z_margin_m']) & (zz <= pallet_top - cfg['pallet_z_margin_m']) & (np.nan_to_num(world[..., 2]) == zz)
    Q = world[sel][:, :2] if sel.any() else np.zeros((0, 2))
    out = [None, None]
    if len(Q) < cfg['pallet_min_pts']: return out
    for k, ax in enumerate(axes):
        if ax['face'] is None: continue  # a pallet face is only searched where the load face on this axis is visible
        a = np.array(ax['axis']); b = np.array(axes[1 - k]['axis']); s = ax['cam_side']; near = ax['face']['pos']
        pa = Q @ a; pb = Q @ b; ob = axes[1 - k]
        off = s * (pa - near); inwin = (off >= cfg['pallet_offset_min_m']) & (off <= cfg['pallet_offset_max_m']) & (pb >= ob['lo'] - cfg['pallet_lateral_margin_m']) & (pb <= ob['hi'] + cfg['pallet_lateral_margin_m'])
        if inwin.sum() < cfg['pallet_min_pts']: continue
        q = pa[inwin]; hist = np.bincount(((q - q.min()) / .01).astype(int)); h3 = np.convolve(hist, np.ones(3), 'same'); i = int(np.argmax(h3))
        if h3[i] < cfg['pallet_min_pts']: continue
        peak = q.min() + (i + .5) * .01; inl = np.abs(q - peak) <= cfg['face_inlier_m']
        if inl.sum() < cfg['pallet_min_pts']: continue
        qb = pb[inwin][inl]; blo, bhi = np.quantile(qb, [cfg['edge_quantile'], 1 - cfg['edge_quantile']])
        out[k] = dict(pos=float(np.median(q[inl])), n=int(inl.sum()), _xy=Q[inwin][inl], offset_from_load_m=float(s * (np.median(q[inl]) - near)), other_lo=float(blo), other_hi=float(bhi),
                      other_mid=float(.5 * (blo + bhi)), full_width=bool(abs((bhi - blo) - PALLET_XY) <= cfg['pallet_full_width_tol_m']))
    return out


def keep_major_components(sup, world, cfg):
    """Cluster the support in the horizontal plane (occupancy grid, cell=component_cell_m, 8-connected after a 1-cell
    dilation) and keep clusters holding >= max(min_px, frac*largest) points. Removes slivers of neighbouring loads /
    background inside a mask, keeps grazing faces (continuous in XY) and panel-split parts of the same load (large)."""
    vv, uu = np.nonzero(sup); xy = world[vv, uu, :2]; cell = cfg['component_cell_m']
    ij = np.floor((xy - xy.min(0)) / cell).astype(int) + 1; G = np.zeros(ij.max(0) + 2, np.uint8); G[ij[:, 0], ij[:, 1]] = 1
    n, lab = cv2.connectedComponents(cv2.dilate(G, np.ones((3, 3), np.uint8)), connectivity=8)
    if n <= 2: return sup, 1
    pl = lab[ij[:, 0], ij[:, 1]]; cnt = np.bincount(pl, minlength=n); cnt[0] = 0
    keep = cnt >= max(cfg['component_min_px'], cfg['component_min_frac'] * cnt.max()); sel = keep[pl]
    out = np.zeros_like(sup); out[vv[sel], uu[sel]] = True
    return out, int(keep.sum())


def hough_heading(xy, cfg):
    """Rectilinear Hough: theta (mod 90) maximising face-plane concentration on both axes."""
    def score(th):
        r = math.radians(th); s = 0
        for a in (np.array([math.cos(r), math.sin(r)]), np.array([-math.sin(r), math.cos(r)])):
            p = xy @ a; h = np.bincount(((p - p.min()) / cfg['hough_bin_m']).astype(int)); h2 = h[:-1] + h[1:] if len(h) > 1 else h
            s += h2.max()
        return s
    grid = np.arange(0, 90, cfg['hough_coarse_deg']); sc = np.array([score(t) for t in grid]); t0 = grid[int(np.argmax(sc))]
    fine = np.arange(t0 - cfg['hough_coarse_deg'], t0 + cfg['hough_coarse_deg'] + 1e-9, cfg['hough_fine_deg']); sf = np.array([score(t) for t in fine])
    best = fine[sf == sf.max()]; return float(np.mean(best) % 90), int(sf.max())


# ------------------------------------------------------------------------------------------------ core (single mask)
def _estimate_single(mask, depth, cal, T, layer_count, cfg, world=None, valid=None):
    if world is None: world, valid = world_map(depth, cal, T)
    fg = depth_gap_cluster(mask, depth, cfg['depth_gap_m'], cfg['cluster_policy'], cfg['cluster_major_frac'])
    if fg.sum() < cfg['min_points']: return None, 'NO_VALID_MASK_DEPTH', {}
    z = world[fg][:, 2]; load_top_s = float(np.quantile(z, cfg['top_quantile'])); ref_xy = np.nanmedian(world[fg][:, :2], 0)
    pallet_ld = load_top_s - layer_count * SIDE_H; floor, floor_reason = sensed_floor_z(world, valid, cv2.dilate(mask.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool), ref_xy)
    z_low = float(np.quantile(z, 0.01))
    if floor is not None and floor > z_low - cfg['floor_below_load_m']:  # e.g. B1: 'floor' seeds are the pallet top (no floor depth)
        floor, floor_reason = None, 'FLOOR_CANDIDATE_NOT_BELOW_LOAD(%.3f)' % floor
    diag = dict(load_top_sensed_m=load_top_s, floor_z_m=floor, floor_status=floor_reason, load_z_q01_m=z_low)
    if floor is not None and abs(floor + PALLET_H - pallet_ld) > cfg['floor_consistency_m']:
        pallet_top = floor + PALLET_H; load_top = pallet_top + layer_count * SIDE_H; datum = 'SENSED_FLOOR_PLUS_PALLET_H(load top inconsistent)'
    else:
        pallet_top = pallet_ld; load_top = load_top_s; datum = 'SENSED_LOAD_TOP_MINUS_LAYERS' + ('(floor-consistent)' if floor is not None else '(no floor observed)')
    diag.update(pallet_top_m=pallet_top, load_top_m=load_top, datum=datum)
    zz = world[..., 2]
    with np.errstate(invalid='ignore'):
        band = valid & (zz >= pallet_top + cfg['band_low_above_pallet_m']) & (zz <= load_top + cfg['band_high_above_top_m'])
    dfg = depth[fg]; dlo, dhi = float(dfg.min()) - 0.10, float(dfg.max()) + 0.10
    with np.errstate(invalid='ignore'):
        vert = zz <= load_top - cfg['side_below_top_m']  # growth only on vertical-face heights (never across top surfaces)
        cand = band & vert & (depth >= dlo) & (depth <= dhi) & cv2.dilate(fg.astype(np.uint8), np.ones((2 * cfg['grow_px'] + 1,) * 2, np.uint8)).astype(bool)
    seed = fg & band
    if seed.sum() < cfg['min_points']: return None, 'insufficient_3d_points', diag
    sup = grow_support(seed, cand, depth, cfg['grow_px'], cfg['continuity_m'])
    with np.errstate(invalid='ignore'):
        is_side = sup & (zz <= load_top - cfg['side_below_top_m'])
    if is_side.sum() < cfg['min_points']: return None, 'insufficient_side_points', diag
    side_sup, ncomp = keep_major_components(is_side, world, cfg)  # clusters on vertical-face points (top surfaces bridge gaps)
    med = np.median(world[side_sup][:, :2], 0); top_sup = sup & ~is_side
    if top_sup.any():
        tv, tu = np.nonzero(top_sup); far = np.linalg.norm(world[tv, tu, :2] - med, axis=1) > cfg['top_max_dist_from_side_m']; top_sup[tv[far], tu[far]] = False
    sup = side_sup | top_sup
    if sup.sum() < cfg['min_points']: return None, 'insufficient_3d_points', diag
    P = world[sup]; side = P[P[:, 2] <= load_top - cfg['side_below_top_m']]
    diag.update(n_seed=int(seed.sum()), n_support=int(sup.sum()), n_components_kept=ncomp, n_side=len(side), n_top=int(len(P) - len(side)))
    if len(side) < cfg['min_points']: return None, 'insufficient_side_points', diag
    theta, hscore = hough_heading(side[:, :2], cfg)
    # occlusion / truncation evidence on support boundary pixels
    ker = np.ones((2 * cfg['occluder_radius_px'] + 1,) * 2, np.uint8)
    boundary = sup & ~cv2.erode(sup.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    with np.errstate(invalid='ignore'):
        occ_src = valid & ~sup & ~fg & (zz > pallet_top + 0.02)  # target-cluster pixels (e.g. staggered bricks) are never occluders; other mask pixels (bled-in panel) can be
    dmin_out = cv2.erode(np.where(occ_src, depth, 1e6).astype(np.float32), ker)
    # depth-continuous surface in the height band just beyond the support (growth stopped by the radius / component pruning)
    with np.errstate(invalid='ignore'):
        cand_free = band & vert & (depth >= dlo) & (depth <= dhi)
    cont_src = grow_support(sup, cand_free, depth, 1, cfg['continuity_m']) & ~sup
    cont_near = cv2.dilate(cont_src.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    H, W = depth.shape; vv, uu = np.nonzero(boundary)
    border = (uu <= 1) | (uu >= W - 2) | (vv <= 1) | (vv >= H - 2)
    occluded = dmin_out[vv, uu] < depth[vv, uu] - cfg['occluder_gap_m']
    trunc_b = border | occluded | cont_near[vv, uu]; bxy = world[vv, uu, :2]
    if cfg.get('debug'): diag['_debug'] = dict(sup=sup, fg=fg, vv=vv, uu=uu, border=border, occluded=occluded, cont=cont_near[vv, uu])
    cam = T[:2, 3]

    def build_axes(theta):
        axes = []
        for k in range(2):
            r = math.radians(theta + 90 * k); a = np.array([math.cos(r), math.sin(r)])
            ps = side[:, :2] @ a; lo, hi = np.quantile(ps, cfg['edge_quantile']), np.quantile(ps, 1 - cfg['edge_quantile'])
            ca = float(cam @ a); s = 1.0 if ca >= 0.5 * (lo + hi) else -1.0  # camera side along this axis
            pb = bxy @ a; ends = {}
            for name, e in (('lo', lo), ('hi', hi)):
                sel = np.abs(pb - e) <= cfg['end_window_m']
                frac = float(trunc_b[sel].mean()) if sel.any() else 1.0
                ends[name] = dict(pos=float(e), n_boundary=int(sel.sum()), trunc_frac=frac, truncated=bool(frac > cfg['trunc_frac']))
            # visible face perpendicular to this axis: dense plane peak near the camera-side end, camera outside the extent
            h = np.bincount(((ps - ps.min()) / 0.01).astype(int)); h3 = np.convolve(h, np.ones(3), 'same'); i = int(np.argmax(h3))
            peak = ps.min() + (i + .5) * 0.01; near_end = hi if s > 0 else lo
            cam_outside = (ca > hi) if s > 0 else (ca < lo)
            face = None
            if cam_outside and h3[i] >= max(cfg['face_min_pts'], cfg['face_min_frac'] * len(ps)) and abs(peak - near_end) <= cfg['face_near_end_m']:
                inl = np.abs(ps - peak) <= cfg['face_inlier_m']; face = dict(pos=float(np.median(ps[inl])), n=int(inl.sum()), _xy=side[inl, :2])
            top_pts = P[P[:, 2] > load_top - cfg['side_below_top_m']]
            top_ext = float(np.ptp(np.quantile(top_pts[:, :2] @ a, [cfg['edge_quantile'], 1 - cfg['edge_quantile']]))) if len(top_pts) >= cfg['min_points'] else 0.
            axes.append(dict(top_extent_m=top_ext, axis=a.tolist(), theta=(theta + 90 * k) % 180, lo=float(lo), hi=float(hi), cam_proj=ca, cam_side=s, face=face, ends=ends))
        # pallet front-face evidence (square 1.1 m pallet: no long/short ambiguity; sensed, no pallet mask)
        pal = pallet_faces(world, valid, mask, sup, pallet_top, axes, dlo, dhi, cfg) if cfg['use_pallet'] else [None, None]
        for k in range(2): axes[k]['pallet'] = pal[k]
        return axes

    theta0 = theta; axes = build_axes(theta)
    for _ in range(cfg['heading_refine_iters']):  # refine heading on the best plane (pallet face preferred: clean cuboid)
        src = cfg['heading_refine_source']; cands = []
        if src in ('pallet', 'both', 'pallet_then_load'): cands += [(2 * len(ax['pallet']['_xy']), ax['pallet']['_xy'], k) for k, ax in enumerate(axes) if ax['pallet'] is not None and len(ax['pallet']['_xy']) >= cfg['pallet_min_pts']]
        if src in ('load', 'both') or (src == 'pallet_then_load' and not cands): cands += [(len(ax['face']['_xy']), ax['face']['_xy'], k) for k, ax in enumerate(axes) if ax['face'] is not None]
        if not cands: break
        _, xy, k = max(cands, key=lambda c: c[0]); xy = xy - xy.mean(0); _, _, vh = np.linalg.svd(xy, full_matrices=False)
        d = vh[0]; t_line = math.degrees(math.atan2(d[1], d[0]))  # face line runs along the OTHER axis (theta + 90(k+1))
        t_new = (t_line - 90 * (k + 1)) % 90; dt = ((t_new - theta) + 45) % 90 - 45
        if abs(dt) > cfg['heading_refine_max_deg'] or abs(dt) < 1e-3: break
        theta = (theta + dt) % 90; axes = build_axes(theta)
    diag['theta_hough_mod90'] = theta0
    # long/short hypotheses
    hyps = []
    for hh in range(2):
        dims = (LOAD_X, LOAD_Y) if hh == 0 else (LOAD_Y, LOAD_X); cen = 0; score = 0.; modes = []
        for k, ax in enumerate(axes):
            half = dims[k] / 2; s = ax['cam_side']; lo_e, hi_e = ax['ends']['lo'], ax['ends']['hi']
            far = lo_e if s > 0 else hi_e; near = hi_e if s > 0 else lo_e
            pf = ax['pallet']; po = axes[1 - k]['pallet']
            if pf is not None and ax['face'] is not None:  # load-face to pallet-face offset = (1.1 - dim)/2
                score += ((s * (pf['pos'] - ax['face']['pos']) - (PALLET_XY - dims[k]) / 2) / cfg['pallet_offset_sigma_m']) ** 2
            if pf is not None:
                c = pf['pos'] - s * PALLET_XY / 2; mode = 'PALLET_FACE'; ext = 0.; full = False
            elif po is not None and po['full_width']:
                c = po['other_mid']; mode = 'PALLET_MIDPOINT'; ext = 0.; full = False
            elif ax['face'] is not None:
                c = ax['face']['pos'] - s * half; mode = 'FACE'
                other_face = axes[1 - k]['face'] is not None  # far end lies on the other (non-grazing) visible face
                ext = abs(far['pos'] - ax['face']['pos']); full = (not far['truncated']) and other_face and ext >= cfg['face_axis_min_full_extent_m']
            elif not lo_e['truncated'] and not hi_e['truncated']:
                c = 0.5 * (lo_e['pos'] + hi_e['pos']); mode = 'MIDPOINT'; ext = hi_e['pos'] - lo_e['pos']; full = True
            elif not lo_e['truncated']:
                c = lo_e['pos'] + half; mode = 'EDGE_LO'; ext = hi_e['pos'] - lo_e['pos']; full = False
            elif not hi_e['truncated']:
                c = hi_e['pos'] - half; mode = 'EDGE_HI'; ext = hi_e['pos'] - lo_e['pos']; full = False
            else:
                c = 0.5 * (lo_e['pos'] + hi_e['pos']); mode = 'MIDPOINT_BOTH_TRUNCATED'; ext = hi_e['pos'] - lo_e['pos']; full = False
            if mode.startswith('PALLET'):
                lo_e2, hi_e2 = lo_e, hi_e; ext = hi_e2['pos'] - lo_e2['pos']; full = (not lo_e2['truncated'] and not hi_e2['truncated'] and ax['face'] is None)
            if full: score += ((ext - dims[k]) / cfg['hyp_sigma_m']) ** 2
            else: score += (max(0., ext - dims[k] - cfg['hyp_lower_bound_tol_m']) / cfg['hyp_sigma_m']) ** 2
            score += (max(0., ax['top_extent_m'] - dims[k] - cfg['hyp_lower_bound_tol_m']) / cfg['hyp_sigma_m']) ** 2  # top face: lower bound
            cen = cen + c * np.array(ax['axis']); modes.append(dict(mode=mode, extent_m=float(ext), extent_full=bool(full), centre_coord=float(c)))
        hyps.append(dict(center=cen, score=float(score), modes=modes, long_axis_theta=(theta + 90 * hh) % 180))
    best = 0 if hyps[0]['score'] <= hyps[1]['score'] else 1; margin = abs(hyps[0]['score'] - hyps[1]['score'])
    ambiguous = margin < cfg['hyp_ambiguous_margin']
    center = 0.5 * (hyps[0]['center'] + hyps[1]['center']) if ambiguous else hyps[best]['center']
    maxext = max(ax['hi'] - ax['lo'] for ax in axes)
    diag.update(theta_mod90=theta, hough_score=hscore, axes=[{k: ({kk: vv for kk, vv in v.items() if kk != '_xy'} if isinstance(v, dict) else v) for k, v in ax.items()} for ax in axes], hyps=[dict(score=h['score'], modes=h['modes'], long_axis_theta=h['long_axis_theta']) for h in hyps],
                hyp_best=best, hyp_margin=margin, ambiguous=ambiguous, max_extent_m=float(maxext))
    if maxext > LOAD_X + cfg['max_extent_over_m']: return None, 'FOOTPRINT_INCONSISTENT_EXTENT', diag
    pose = dict(center_x_m=float(center[0]), center_y_m=float(center[1]), heading_deg_180=float(hyps[best]['long_axis_theta']),
                b2_heading_deg=float(theta), b4_flip_used=bool(best == 1), b4_score_margin=float(margin), b5_center_flip_90=bool(best == 1),
                b5_score=float(hyps[best]['score']), b5_inside_rate=float('nan'), n_points=int(len(P)), n_top_points=int(len(P) - len(side)), n_side_points=int(len(side)),
                axis_modes='|'.join(m['mode'] for m in hyps[best]['modes']), axis_ambiguous_hedged=bool(ambiguous), datum=datum, pallet_top_m=float(pallet_top))
    return pose, None, diag


def _perturb(mask, kind):
    m = mask.astype(np.uint8); k = np.ones((3, 3), np.uint8)
    if kind == 'orig': return mask
    if kind.startswith('ero'): return cv2.erode(m, k, iterations=int(kind[3:])).astype(bool)
    if kind.startswith('dil'): return cv2.dilate(m, k, iterations=int(kind[3:])).astype(bool)
    raise ValueError(kind)


def estimate_pose(mask, depth, camera_metadata, layer_count, config=None, return_diag=False):
    """Safe wrapper: never raises; any exception -> status 'PIPELINE_ERROR' with the exception as reason code."""
    try:
        return _estimate_pose(mask, depth, camera_metadata, layer_count, config, return_diag)
    except Exception as e:  # recorded failure, never silently dropped
        cfg = dict(DEFAULT_CONFIG, **(config or {}))
        return dict(status='PIPELINE_ERROR', reason=f'EXCEPTION_{type(e).__name__}: {e}'[:200], pose=None, GT_input=False, variant=VERSION, config_sha256=config_sha(cfg))


def _estimate_pose(mask, depth, camera_metadata, layer_count, config=None, return_diag=False):
    """IMPORTABLE ENTRY POINT.
    mask: bool HxW (selected instance mask, or None); depth: float HxW distance_to_image_plane [m];
    camera_metadata: dict or JSON text in the v44 camera_metadata.json format; layer_count: int (task metadata).
    Returns dict(status in {'B5_COMPUTED','NO_DETECTION','DEPTH_INSUFFICIENT','DATUM_REJECTED'}, reason, pose|None, variant,
    config_sha256[, diag]). pose has the frozen-B5 keys (center_x_m, center_y_m, heading_deg_180, ...)."""
    cfg = dict(DEFAULT_CONFIG, **(config or {})); out = dict(status='DATUM_REJECTED', reason='NOT_EVALUATED', pose=None, GT_input=False, variant=VERSION, config_sha256=config_sha(cfg))
    if mask is None or not np.asarray(mask).any():
        out.update(status='NO_DETECTION', reason='ORIGINAL_SELECTED_PREDICTION_ABSENT' if mask is None else 'EMPTY_ORIGINAL_MASK'); return out
    mask = np.asarray(mask).astype(bool); depth = np.asarray(depth)
    cal, T = calibration(camera_metadata)
    if mask.shape != depth.shape or depth.shape != (cal['H'], cal['W']): out.update(status='DATUM_REJECTED', reason='SHAPE_MISMATCH'); return out
    world, valid = world_map(depth, cal, T)
    members = list(cfg['ensemble']) if cfg['ensemble'] else ['orig']; results = {}
    for kind in members:
        m = _perturb(mask, kind)
        if not m.any(): results[kind] = (None, 'EMPTY_PERTURBED_MASK', {}); continue
        results[kind] = _estimate_single(m, depth, cal, T, int(layer_count), cfg, world, valid)
    base_pose, base_reason, base_diag = results.get('orig', next(iter(results.values())))
    ok = {k: r[0] for k, r in results.items() if r[0] is not None}
    if base_pose is None and not ok:
        st = 'DEPTH_INSUFFICIENT' if (base_reason or '').startswith(('insufficient', 'NO_VALID')) else 'DATUM_REJECTED'
        out.update(status=st, reason=base_reason)
        if return_diag: out['diag'] = base_diag
        return out
    if base_pose is None:  # orig failed but perturbed members computed: use them (recorded)
        base_pose = dict(next(iter(ok.values()))); base_reason = 'ORIG_MEMBER_FAILED_' + str(base_reason)
    pose = dict(base_pose)
    if len(ok) >= 2:
        cx = np.median([p['center_x_m'] for p in ok.values()]); cy = np.median([p['center_y_m'] for p in ok.values()])
        pose.update(center_x_m=float(cx), center_y_m=float(cy))
    pose['ensemble_members_computed'] = sorted(ok); pose['ensemble_spread_m'] = float(max(math.hypot(p['center_x_m'] - pose['center_x_m'], p['center_y_m'] - pose['center_y_m']) for p in ok.values()))
    out.update(status='B5_COMPUTED', reason=base_reason or 'B5_ROBUST_V01_COMPUTED', pose=pose)
    if return_diag: out['diag'] = base_diag
    return out
