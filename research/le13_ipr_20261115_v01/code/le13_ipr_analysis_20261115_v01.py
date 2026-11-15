"""LE13 IPR analysis v01 (2026-11-15) — implements reports/le13_ipr_analysis_plan_LOCK_20261115_v01.md exactly (sha checked against PRELOCK).
Reads result files only (capture complete records for GT, perception_result/gate/pose_ROBUST_A for predictions). K1 only.
Outputs: per-capture CSV, family-level CSV, stats JSON, figure.
Usage: python analysis/le13_ipr_analysis_20261115_v01.py <ns_dir> <out_dir>"""
import csv, json, sys, math, hashlib, random, collections
from pathlib import Path
import numpy as np
from scipy import stats
NS, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True); P = NS / 'prelock'
R = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
lock = json.loads((P / 'PRELOCK.json').read_text())
assert sha(R / 'reports/le13_ipr_analysis_plan_LOCK_20261115_v01.md') == lock['analysis_plan_sha256'], 'ANALYSIS_PLAN_CHANGED_AFTER_LOCK'
for n, h in lock['files'].items(): assert sha(P / n) == h, n
man = list(csv.DictReader((P / 'capture_manifest.csv').open())); REPS = ['HR_Scan', 'LR_Scan', 'GeoCAD']; CS = ['C100', 'C80', 'C60', 'C40', 'C20']
def jl(p):
    try: return json.loads(Path(p).read_text())
    except Exception: return None
rows = []
for m in man:
    cid = m['capture_id']; C = NS / 'captures_v01' / m['rep']; cap = C / cid; comp = jl(C / 'complete' / f'{cid}.json') or {}
    rec = dict(capture_id=cid, family_id=m['family_id'], source_scene_id=m['source_scene_id'], C=m['C'], rep=m['rep'], start_id=m['start_id'], dome=m['dome_intensity'],
               capture_state=comp.get('state'), status=None, detected=False, detection_conf=None, n_brick_load=None, gate_selected=None, pose_status=None, axis_modes=None,
               err_xy_mm=None, err_x_mm=None, err_y_mm=None, yaw_err_deg=None, yaw_err_mod90_deg=None, pred_x=None, pred_y=None, pred_heading_deg=None, vis_hard_e2=(comp.get('qa') or {}).get('vis_hard_e2'))
    if comp.get('state') != 'PASS_CAPTURE': rec['status'] = 'CAPTURE_FAILED'; rows.append(rec); continue
    pr = jl(cap / 'perception_result.json'); g = jl(cap / 'gate.json'); po = jl(cap / 'pose_ROBUST_A.json')
    if pr is None: rec['status'] = 'INFERENCE_MISSING'; rows.append(rec); continue
    nb = (pr.get('gate') or {}).get('n_brick_load'); rec.update(n_brick_load=nb, detected=bool(nb), gate_selected=(g or {}).get('selected_detector_index'), detection_conf=pr.get('detection_conf'))
    gt = comp['GT_eval_only']['target']
    if not nb: rec['status'] = 'NO_DETECTION'
    elif rec['gate_selected'] is None: rec['status'] = 'GATE_REJECTED'
    elif not po or not po.get('pose') or po.get('status') != 'B5_COMPUTED': rec.update(status='POSE_FAILED', pose_status=(po or {}).get('status'))
    else:
        p = po['pose']; dx = p['center_x_m'] - gt['center_x_m']; dy = p['center_y_m'] - gt['center_y_m']; h = float(p['heading_deg_180'])
        rec.update(status='VALID', pose_status=po['status'], axis_modes=p.get('axis_modes'), pred_x=p['center_x_m'], pred_y=p['center_y_m'], pred_heading_deg=h,
                   err_x_mm=dx * 1000, err_y_mm=dy * 1000, err_xy_mm=math.hypot(dx, dy) * 1000,
                   yaw_err_deg=((h - gt['yaw_deg'] + 90) % 180) - 90, yaw_err_mod90_deg=((h - gt['yaw_deg'] + 45) % 90) - 45)
    rows.append(rec)
with (OUT / 'ipr_k1_captures.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); [w.writerow(r) for r in rows]
def desc(v):
    v = [x for x in v if x is not None]
    if not v: return dict(n=0)
    a = np.array(v, float); return dict(n=len(a), mean=float(a.mean()), sd=float(a.std(ddof=1)) if len(a) > 1 else None, median=float(np.median(a)), p90=float(np.percentile(a, 90)), min=float(a.min()), max=float(a.max()))
res = dict(version='LE13_IPR_ANALYSIS_v01', plan_sha256=lock['analysis_plan_sha256'], prelock_files=lock['files'], n_intended=len(man))
res['by_rep'] = {rep: dict(intended=sum(r['rep'] == rep for r in rows), status=dict(collections.Counter(r['status'] for r in rows if r['rep'] == rep)),
                           K1_detection_rate=sum(r['detected'] for r in rows if r['rep'] == rep) / sum(r['rep'] == rep for r in rows),
                           K1_pose_completion_rate=sum(r['status'] == 'VALID' for r in rows if r['rep'] == rep) / sum(r['rep'] == rep for r in rows),
                           err_xy_mm=desc([r['err_xy_mm'] for r in rows if r['rep'] == rep]), err_x_mm=desc([r['err_x_mm'] for r in rows if r['rep'] == rep]),
                           err_y_mm=desc([r['err_y_mm'] for r in rows if r['rep'] == rep]), yaw_err_deg=desc([r['yaw_err_deg'] for r in rows if r['rep'] == rep]),
                           abs_yaw_err_deg=desc([abs(r['yaw_err_deg']) for r in rows if r['rep'] == rep and r['yaw_err_deg'] is not None]),
                           conf=desc([r['detection_conf'] for r in rows if r['rep'] == rep]), axis_modes=dict(collections.Counter(r['axis_modes'] for r in rows if r['rep'] == rep and r['axis_modes'])))
                 for rep in REPS}
res['by_rep_C'] = {f'{rep}|{c}': dict(valid=sum(r['status'] == 'VALID' for r in rows if r['rep'] == rep and r['C'] == c), err_xy_mm=desc([r['err_xy_mm'] for r in rows if r['rep'] == rep and r['C'] == c]),
                                      conf=desc([r['detection_conf'] for r in rows if r['rep'] == rep and r['C'] == c])) for rep in REPS for c in CS}
# matched triplets
idx = {(r['family_id'], r['C'], r['rep']): r for r in rows}
fams = sorted({r['family_id'] for r in rows}); trip = []
for f in fams:
    for c in CS:
        t = [idx.get((f, c, rep)) for rep in REPS]
        if all(x and x['status'] == 'VALID' for x in t):
            trip.append(dict(family_id=f, C=c, start_id=t[0]['start_id'], e_HR=t[0]['err_xy_mm'], e_LR=t[1]['err_xy_mm'], e_CAD=t[2]['err_xy_mm'],
                             d_HR_LR=t[0]['err_xy_mm'] - t[1]['err_xy_mm'], d_HR_CAD=t[0]['err_xy_mm'] - t[2]['err_xy_mm']))
with (OUT / 'ipr_matched_triplets.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(trip[0]) if trip else ['family_id']); w.writeheader(); [w.writerow(t) for t in trip]
famrows = []
for f in fams:
    tt = [t for t in trip if t['family_id'] == f]
    if tt: famrows.append(dict(family_id=f, n_loads=len(tt), mean_d_HR_LR=float(np.mean([t['d_HR_LR'] for t in tt])), mean_d_HR_CAD=float(np.mean([t['d_HR_CAD'] for t in tt])),
                                mean_e_HR=float(np.mean([t['e_HR'] for t in tt])), mean_e_LR=float(np.mean([t['e_LR'] for t in tt])), mean_e_CAD=float(np.mean([t['e_CAD'] for t in tt]))))
with (OUT / 'ipr_family_means.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(famrows[0]) if famrows else ['family_id']); w.writeheader(); [w.writerow(t) for t in famrows]
res['matching'] = dict(families=len(fams), families_included=len(famrows), matched_triplets=len(trip), intended_triplets=len(fams) * 5,
                       triplet_missing_rate=1 - len(trip) / (len(fams) * 5), loads_per_family=dict(collections.Counter(fr['n_loads'] for fr in famrows)))
def test(vals, name):
    a = np.array(vals, float); n = len(a)
    if n < 2: return dict(name=name, n=n, state='INSUFFICIENT')
    t, p = stats.ttest_1samp(a, 0.0); se = a.std(ddof=1) / math.sqrt(n); q = stats.t.ppf(.975, n - 1)
    rng = random.Random(42); bs = sorted(float(np.mean(rng.choices(list(a), k=n))) for _ in range(10000))
    npos = int((a > 0).sum()); nneg = int((a < 0).sum()); sp = stats.binomtest(npos, npos + nneg, .5).pvalue if npos + nneg else None
    return dict(name=name, n_families=n, mean_mm=float(a.mean()), sd_mm=float(a.std(ddof=1)), se_mm=float(se), ci95_mm=[float(a.mean() - q * se), float(a.mean() + q * se)],
                t=float(t), df=n - 1, p_raw=float(p), dz=float(a.mean() / a.std(ddof=1)) if a.std(ddof=1) > 0 else None,
                sens_bootstrap_ci95_mm=[bs[249], bs[9749]], sens_sign_test=dict(n_pos=npos, n_neg=nneg, p=sp), sens_median_mm=float(np.median(a)))
T = [test([f['mean_d_HR_LR'] for f in famrows], 'HR-LR'), test([f['mean_d_HR_CAD'] for f in famrows], 'HR-GeoCAD')]
ps = sorted([(t['p_raw'], i) for i, t in enumerate(T) if 'p_raw' in t]); m = len(ps); run = 0.
for k, (p, i) in enumerate(ps):
    adj = min(1., max(run, (m - k) * p)); run = adj; T[i]['p_holm'] = adj; T[i]['significant_holm_0p05'] = adj < .05
res['primary_tests'] = T
res['HR_superior_to_both'] = bool(all(t.get('significant_holm_0p05') and t['mean_mm'] < 0 for t in T))
# exploratory
res['exploratory'] = dict(
    by_C={c: dict(d_HR_LR=desc([t['d_HR_LR'] for t in trip if t['C'] == c]), d_HR_CAD=desc([t['d_HR_CAD'] for t in trip if t['C'] == c])) for c in CS},
    by_start={s: dict(d_HR_LR=desc([t['d_HR_LR'] for t in trip if t['start_id'] == s]), d_HR_CAD=desc([t['d_HR_CAD'] for t in trip if t['start_id'] == s])) for s in sorted({t['start_id'] for t in trip})},
    excl_abs_err_gt_50mm=dict(note='EXPLORATORY ONLY; primary analysis excludes nothing',
                              tests=[test([float(np.mean([t[k] for t in trip if t['family_id'] == f and max(t['e_HR'], t['e_LR'], t['e_CAD']) <= 50])) for f in fams
                                           if any(t['family_id'] == f and max(t['e_HR'], t['e_LR'], t['e_CAD']) <= 50 for t in trip)], nm) for k, nm in (('d_HR_LR', 'HR-LR'), ('d_HR_CAD', 'HR-GeoCAD'))]),
    large_errors=[{k: r[k] for k in ('capture_id', 'err_xy_mm', 'axis_modes', 'detection_conf')} for r in rows if r['err_xy_mm'] is not None and r['err_xy_mm'] > 50])
res['engineering_reference'] = dict(task_position_band_mm=110, note='differences compared with the 110 mm task band and the ~3.4 mm common robot-frame bias seen in the original 540')
(OUT / 'ipr_stats.json').write_text(json.dumps(res, indent=1))
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for k, (key, nm) in enumerate((('mean_d_HR_LR', 'HR − LR'), ('mean_d_HR_CAD', 'HR − GeoCAD'))):
        v = [f[key] for f in famrows]; ax[k].axhline(0, color='#888', lw=1); ax[k].plot(range(1, len(v) + 1), v, 'o', color='#2a6fb0')
        t = T[k]; ax[k].axhspan(t['ci95_mm'][0], t['ci95_mm'][1], color='#2a6fb0', alpha=.15); ax[k].set_title(f"{nm}: mean {t['mean_mm']:.3f} mm, Holm p={t['p_holm']:.3g}")
        ax[k].set_xlabel('family'); ax[k].set_ylabel('family mean paired difference (mm)')
    fig.tight_layout(); fig.savefig(OUT / 'ipr_family_differences.png', dpi=120)
except Exception as e:
    res['figure_error'] = repr(e)
print(json.dumps(dict(matching=res['matching'], tests=[{k: t.get(k) for k in ('name', 'n_families', 'mean_mm', 'ci95_mm', 'p_raw', 'p_holm')} for t in T], HR_superior_to_both=res['HR_superior_to_both']), indent=1))
