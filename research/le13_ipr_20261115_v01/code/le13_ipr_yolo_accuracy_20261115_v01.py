"""LE13 IPR YOLO recognition-accuracy analysis v01 (2026-11-15). Implements reports/le13_ipr_yolo_accuracy_plan_LOCK_20261115_v01.md
(sha checked against <ns>/yolo_accuracy_v01/yolo_accuracy_LOCK.json). Read-only over IPR captures: detections.json, gate.json,
selected_mask.npy (prediction) and eval_gt_only/mask_{canonical,actual}.png (evaluation-only GT). No inference is re-run.
Usage: python analysis/le13_ipr_yolo_accuracy_20261115_v01.py <ns_dir>"""
import csv, json, sys, math, hashlib, random, collections
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import stats
NS = Path(sys.argv[1]); OUT = NS / 'yolo_accuracy_v01'; R = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
lock = json.loads((OUT / 'yolo_accuracy_LOCK.json').read_text()); assert sha(R / lock['plan']) == lock['plan_sha256'], 'PLAN_CHANGED_AFTER_LOCK'
man = list(csv.DictReader((NS / 'prelock/capture_manifest.csv').open())); REPS = ['HR_Scan', 'LR_Scan', 'GeoCAD']; CS = ['C100', 'C80', 'C60', 'C40', 'C20']
GX, GY = 20.5, 13.5
def jl(p):
    try: return json.loads(Path(p).read_text())
    except Exception: return None
def iou(a, b): u = (a | b).sum(); return float((a & b).sum() / u) if u else 0.
rows = []
for m in man:
    cap = NS / 'captures_v01' / m['rep'] / m['capture_id']
    det = (jl(cap / 'detections.json') or {}).get('detections', []); g = jl(cap / 'gate.json') or {}
    loads = [d for d in det if d['class_name'] == 'brick_load' and d['confidence'] >= .25]
    def dist(d): c = d.get('centroid_xy_m'); return math.hypot(c[0] - GX, c[1] - GY) if c else float('inf')
    can = np.array(Image.open(cap / 'eval_gt_only/mask_canonical.png')) > 0; act = np.array(Image.open(cap / 'eval_gt_only/mask_actual.png')) > 0
    sel = g.get('selected_detector_index'); sm = np.load(cap / 'selected_mask.npy').astype(bool) if (sel is not None and (cap / 'selected_mask.npy').exists()) else None
    selconf = next((d['confidence'] for d in det if d['index'] == sel), None) if sel is not None else None
    i_c = iou(sm, can) if sm is not None else 0.; i_a = iou(sm, act) if sm is not None else 0.
    dice = (2 * (sm & can).sum() / (sm.sum() + can.sum())) if sm is not None and (sm.sum() + can.sum()) else 0.
    rows.append(dict(capture_id=m['capture_id'], family_id=m['family_id'], C=m['C'], rep=m['rep'], start_id=m['start_id'],
                     P1_detected=int(bool(loads)), P2_iou_canonical_incl_miss=i_c, selected=int(sm is not None), S1_iou_canonical_if_selected=(i_c if sm is not None else None),
                     S2_iou_actual_incl_miss=i_a, S3_dice_canonical_incl_miss=float(dice), S4_selected_conf=selconf, S5_offtarget_fp=sum(1 for d in loads if dist(d) > 1.0),
                     S6_target_detected=int(any(dist(d) <= 1.0 for d in loads)), n_brick_load=len(loads), max_conf=max((d['confidence'] for d in loads), default=None),
                     gt_canonical_px=int(can.sum()), pred_px=int(sm.sum()) if sm is not None else 0))
with (OUT / 'yolo_captures.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); [w.writerow(r) for r in rows]
fams = sorted({r['family_id'] for r in rows}); idx = {(r['family_id'], r['C'], r['rep']): r for r in rows}
def fam_mean(rep, key):
    return [float(np.mean([idx[(f, c, rep)][key] for c in CS])) for f in fams]
famtab = [dict(family_id=f, **{f'{rep}_{k}': float(np.mean([idx[(f, c, rep)][k] for c in CS])) for rep in REPS for k in ('P1_detected', 'P2_iou_canonical_incl_miss')}) for f in fams]
with (OUT / 'yolo_family_means.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(famtab[0])); w.writeheader(); [w.writerow(r) for r in famtab]
def test(a, b, name):
    d = np.array(a) - np.array(b); n = len(d); sd = d.std(ddof=1)
    if sd == 0: t, p = 0., 1.
    else: t, p = stats.ttest_rel(a, b)
    se = sd / math.sqrt(n); q = stats.t.ppf(.975, n - 1); rng = random.Random(42); bs = sorted(float(np.mean(rng.choices(list(d), k=n))) for _ in range(10000))
    try: wp = float(stats.wilcoxon(d, zero_method='wilcox').pvalue) if np.any(d != 0) else 1.
    except ValueError: wp = None
    return dict(name=name, n_families=n, mean_a=float(np.mean(a)), mean_b=float(np.mean(b)), mean_diff=float(d.mean()), sd=float(sd), ci95=[float(d.mean() - q * se), float(d.mean() + q * se)],
                t=float(t), df=n - 1, p_raw=float(p), dz=float(d.mean() / sd) if sd else None, sens_bootstrap_ci95=[bs[249], bs[9749]], sens_wilcoxon_p=wp,
                families_a_better=int((d > 0).sum()), families_b_better=int((d < 0).sum()), ties=int((d == 0).sum()))
T = []
for key, lab in (('P1_detected', 'P1 detection rate'), ('P2_iou_canonical_incl_miss', 'P2 target-mask IoU (miss=0)')):
    for a, b in (('HR_Scan', 'LR_Scan'), ('HR_Scan', 'GeoCAD'), ('LR_Scan', 'GeoCAD')):
        x = test(fam_mean(a, key), fam_mean(b, key), f'{lab}: {a}-{b}'); x.update(metric=key, a=a, b=b); T.append(x)
ps = sorted([(t['p_raw'], i) for i, t in enumerate(T)]); run = 0.
for k, (p, i) in enumerate(ps): adj = min(1., max(run, (len(ps) - k) * p)); run = adj; T[i]['p_holm'] = adj; T[i]['significant_holm_0p05'] = adj < .05
def desc(v):
    v = [x for x in v if x is not None]
    if not v: return dict(n=0)
    a = np.array(v, float); return dict(n=len(a), mean=float(a.mean()), sd=float(a.std(ddof=1)) if len(a) > 1 else None, median=float(np.median(a)), min=float(a.min()), max=float(a.max()))
res = dict(version='LE13_IPR_YOLO_ACCURACY_v01', namespace=str(NS), plan_sha256=lock['plan_sha256'], n_captures=len(rows), primary_tests=T)
res['by_rep'] = {rep: dict(P1_detection_rate=float(np.mean([r['P1_detected'] for r in rows if r['rep'] == rep])), P2_iou_incl_miss=desc([r['P2_iou_canonical_incl_miss'] for r in rows if r['rep'] == rep]),
                           S1_iou_if_selected=desc([r['S1_iou_canonical_if_selected'] for r in rows if r['rep'] == rep]), S2_iou_actual_incl_miss=desc([r['S2_iou_actual_incl_miss'] for r in rows if r['rep'] == rep]),
                           S3_dice_incl_miss=desc([r['S3_dice_canonical_incl_miss'] for r in rows if r['rep'] == rep]), S4_selected_conf=desc([r['S4_selected_conf'] for r in rows if r['rep'] == rep]),
                           S5_offtarget_fp_total=int(sum(r['S5_offtarget_fp'] for r in rows if r['rep'] == rep)), S6_target_detected_rate=float(np.mean([r['S6_target_detected'] for r in rows if r['rep'] == rep])),
                           selected_rate=float(np.mean([r['selected'] for r in rows if r['rep'] == rep]))) for rep in REPS}
res['by_rep_C'] = {f'{rep}|{c}': dict(P1=float(np.mean([r['P1_detected'] for r in rows if r['rep'] == rep and r['C'] == c])), P2=float(np.mean([r['P2_iou_canonical_incl_miss'] for r in rows if r['rep'] == rep and r['C'] == c])),
                                      S1=desc([r['S1_iou_canonical_if_selected'] for r in rows if r['rep'] == rep and r['C'] == c]).get('mean'), S4=desc([r['S4_selected_conf'] for r in rows if r['rep'] == rep and r['C'] == c]).get('mean'),
                                      max_conf=desc([r['max_conf'] for r in rows if r['rep'] == rep and r['C'] == c]).get('mean')) for rep in REPS for c in CS}
res['by_rep_start'] = {f'{rep}|{s}': dict(P1=float(np.mean([r['P1_detected'] for r in rows if r['rep'] == rep and r['start_id'] == s])), P2=float(np.mean([r['P2_iou_canonical_incl_miss'] for r in rows if r['rep'] == rep and r['start_id'] == s])))
                       for rep in REPS for s in sorted({r['start_id'] for r in rows})}
# capture-level supportive tests for detection
Y = np.array([[idx[(f, c, rep)]['P1_detected'] for rep in REPS] for f in fams for c in CS]); k = 3; N = Y.shape[0]
Gj = Y.sum(0); Li = Y.sum(1); Q = (k - 1) * (k * (Gj ** 2).sum() - Gj.sum() ** 2) / (k * Li.sum() - (Li ** 2).sum()) if (k * Li.sum() - (Li ** 2).sum()) else 0.
mc = {}
for i, j in ((0, 1), (0, 2), (1, 2)):
    b = int(((Y[:, i] == 1) & (Y[:, j] == 0)).sum()); c_ = int(((Y[:, i] == 0) & (Y[:, j] == 1)).sum())
    mc[f'{REPS[i]}-{REPS[j]}'] = dict(only_first=b, only_second=c_, p_exact=float(stats.binomtest(b, b + c_, .5).pvalue) if b + c_ else 1.)
res['supportive_capture_level'] = dict(note='captures are not independent within family; supportive only', cochran_Q=float(Q), df=2, p=float(stats.chi2.sf(Q, 2)), mcnemar_exact=mc)
(OUT / 'yolo_stats.json').write_text(json.dumps(res, indent=1))
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4)); col = {'HR_Scan': '#2a6fb0', 'LR_Scan': '#e08a1e', 'GeoCAD': '#3a9d5d'}
    for k_, (key, lab) in enumerate((('P1', 'K1 detection rate'), ('P2', 'target-mask IoU (miss = 0)'))):
        for rep in REPS: ax[k_].plot(CS, [res['by_rep_C'][f'{rep}|{c}'][key] for c in CS], 'o-', color=col[rep], label=rep)
        ax[k_].set_title(lab); ax[k_].set_ylim(0, 1.02); ax[k_].set_xlabel('load level'); ax[k_].legend()
    fig.tight_layout(); fig.savefig(OUT / 'yolo_by_load.png', dpi=120)
except Exception as e: res['figure_error'] = repr(e)
print(json.dumps([{k: t[k] for k in ('name', 'mean_a', 'mean_b', 'mean_diff', 'ci95', 'p_raw', 'p_holm')} for t in T], indent=0))
