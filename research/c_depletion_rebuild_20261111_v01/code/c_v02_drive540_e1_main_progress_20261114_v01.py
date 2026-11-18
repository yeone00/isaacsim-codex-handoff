"""C540 E1 main progress report (v01, 2026-11-14). CPU only, READ-ONLY on the main output. Main runs only (technical pilots never included).
Usage: progress.py <out_dir> [<label>]. Writes <out_dir>/progress_<label>.json and .csv tables:
 1 progress, 2 per representation, 3 per C, 4 failure causes, 5 distance / final position & heading error, 6 run time stats,
 7 cumulative and remaining time, 8 disk usage and archive verification."""
import json, sys, csv, statistics, shutil, time, collections
from pathlib import Path
E = Path('/home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_E1_20261114_v01'); ST = E / 'main_controller_v05_state'
lock = json.loads((E / 'main_execution_lock_FINAL_v02.json').read_text()); OUTR = Path(lock['output_root'])
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); label = sys.argv[2] if len(sys.argv) > 2 else time.strftime('%Y%m%d_%H%M')
rows = list(csv.DictReader(open(lock['manifest']))); hist = [json.loads(l) for l in open(ST / 'run_history.jsonl')] if (ST / 'run_history.jsonl').exists() else []
recs = []
for h in hist:
    run = OUTR / h['attempt']; r = json.loads((run / 'result.json').read_text()) if (run / 'result.json').exists() else {}
    ar = run.parent / (run.name + '.archive.json'); a = json.loads(ar.read_text()) if ar.exists() else None
    recs.append(dict(h, final_err_m=r.get('final_err_m'), final_heading_err_deg=r.get('final_heading_err_deg'), drive_distance_m=r.get('drive_distance_m'), band_main=r.get('band_main'),
                     detection_conf=r.get('detection_conf'), runner_wall_s=r.get('wall_s'), archive=a))
def cause(x):
    if not x['technical_pass']: return 'technical_hold'
    if x['outcome'] == 'SUCCESS': return 'success'
    rs = x['reason']
    if 'NO_DETECTION' in rs: return 'perception_no_detection'
    if rs.startswith('POSE_') or 'DATUM' in rs: return 'pose_rejected'
    if rs.startswith(('PLAN_REJECTED', 'FOOTPRINT')): return 'plan_rejected'
    if x['moved']: return 'drive_outside_band_or_failed'
    return 'other:' + rs[:40]
def rate(sub): return dict(n=len(sub), success=sum(cause(x) == 'success' for x in sub), success_rate=(sum(cause(x) == 'success' for x in sub) / len(sub)) if sub else None,
                          causes=dict(collections.Counter(cause(x) for x in sub)))
dur = [x['t_end'] - x['t_start'] for x in recs]; moved = [x for x in recs if x['moved']]
def st(v): return dict(n=len(v), mean=statistics.mean(v), median=statistics.median(v), max=max(v), min=min(v)) if v else None
recent = dur[-30:]; pace = statistics.mean(recent) if recent else None; remaining = (len(rows) - len(recs)) * pace if pace else None
busy = sum(dur); first = recs[0]['t_start'] if recs else None
arcs = [x['archive'] for x in recs if x['archive']]
du = shutil.disk_usage(OUTR)
rep = {'1_progress': dict(completed=len(recs), remaining=len(rows) - len(recs), planned=len(rows)),
       '2_per_representation': {r: rate([x for x in recs if x['rep'] == r]) for r in ('HR_Scan', 'LR_Scan', 'GeoCAD')},
       '3_per_C': {c: rate([x for x in recs if x['C'] == c]) for c in ('C100', 'C80', 'C60', 'C40', 'C20')},
       '3b_per_rep_C': {f'{r}_{c}': rate([x for x in recs if x['rep'] == r and x['C'] == c]) for r in ('HR_Scan', 'LR_Scan', 'GeoCAD') for c in ('C100', 'C80', 'C60', 'C40', 'C20')},
       '4_causes_all': dict(collections.Counter(cause(x) for x in recs)),
       '5_motion': dict(moved_runs=len(moved), drive_distance_m=st([x['drive_distance_m'] for x in moved if x['drive_distance_m'] is not None]),
                        final_position_error_m=st([x['final_err_m'] for x in moved if x['final_err_m'] is not None]),
                        final_heading_error_abs_deg=st([abs(x['final_heading_err_deg']) for x in moved if x['final_heading_err_deg'] is not None]),
                        within_main_band=sum(bool(x['band_main']) for x in moved)),
       '6_run_time_s': dict(all=st(dur), drove=st([x['t_end'] - x['t_start'] for x in moved]), not_moved=st([x['t_end'] - x['t_start'] for x in recs if not x['moved']])),
       '7_time': dict(wall_since_start_h=(time.time() - first) / 3600 if first else 0, busy_h=busy / 3600, recent30_s_per_run=pace, remaining_h=remaining / 3600 if remaining else None,
                      projected_total_h=(busy + (remaining or 0)) / 3600, eta_local=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + remaining)) if remaining else None, budget_h=36),
       '8_storage': dict(archives=len(arcs), archives_verified=sum(bool(a['verified']) for a in arcs), original_GB=sum(a['original_bytes'] for a in arcs) / 1e9,
                         archive_GB=sum(a['bytes'] for a in arcs) / 1e9, volume_free_TB=du.free / 1e12),
       'note': 'main E1 runs only; technical pilots excluded; report only, no condition changed'}
(out / f'progress_{label}.json').write_text(json.dumps(rep, indent=1, default=str))
with (out / f'progress_{label}_runs.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, ['attempt', 'rep', 'C', 'start_id', 'outcome', 'reason', 'cause', 'moved', 'technical_pass', 'detection_conf', 'drive_distance_m', 'final_err_m', 'final_heading_err_deg', 'band_main', 'run_s', 'archive_verified'])
    w.writeheader()
    for x in recs: w.writerow(dict({k: x.get(k) for k in w.fieldnames if k in x}, cause=cause(x), run_s=round(x['t_end'] - x['t_start'], 1), archive_verified=(x['archive'] or {}).get('verified')))
print(json.dumps({k: rep[k] for k in ('1_progress', '4_causes_all', '7_time', '8_storage')}, indent=1, default=str))
