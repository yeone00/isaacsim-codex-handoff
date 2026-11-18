"""C540 cruise-speed candidate validation + automatic selection + main540 autostart (v01, 2026-11-14). Researcher pre-approved (final instruction):
order 0.035 -> 0.03 -> fallback 0.02 (A+B validated). Pre-registered PASS rule per candidate, evaluated run by run (first failure stops the candidate,
no retries): four technical runs (counted=false) with runner v07 --cruise-m-s c:
  E1 GeoCAD C100, S1 GeoCAD C100, S6 GeoCAD C100, E1 LR C40 (run-11 condition);
each must be: gate v03 technical_pass, outcome SUCCESS, F (phase thresholds) not tripped, band_main, final error <= 0.01 m, both legs reached with stop
certificates, H_PRE 6-tick mean max <= 0.045 (0.9 x ceiling) and PRE_FINAL 6-tick mean max <= 0.027; TC-S offline nominal 7/7 starts admitted (done).
Then: writes amendment v05 FINAL (chosen speed) + execution lock FINAL_v04, runs the matching approve script (pre-approved by the researcher),
dry-runs the controller and, only if every gate is true, starts it with systemd-run (unit c-v02-drive540-e1-main-v07). Never touches v04/v05 outputs."""
import json, hashlib, subprocess, sys, time, statistics
from pathlib import Path
R = Path('/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013'); sys.path.insert(0, str(R))
PY = '/home/user/anaconda3/envs/sdg_tools/bin/python'; S = Path('/home/user/hh/isaac_cosmos/sdg_final')
E = S / 'C_V02_DRIVE540_E1_20261114_v01'; W = S / 'C_V02_SPEED_CANDIDATES_20261114_v01'; W.mkdir(exist_ok=True); LOG = W / 'autostart.log'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(m):
    with LOG.open('a') as f: f.write(time.strftime('%Y-%m-%dT%H:%M:%S ') + m + '\n')
def notify(t, m, tag='white_check_mark'):
    subprocess.run(['python3', '-c', "import sys;sys.path.insert(0,'/home/user/.claude/hooks/isaacsim');import ntfy_notify as n;n.send(sys.argv[1],sys.argv[2],4,sys.argv[3])", t, m, tag], capture_output=True)
FLAGS = ['--profile-steps', '--opt-contact-compact', '--opt-graph-cache', '--opt-fsync-batch', '15', '--opt-leg-start-pacing-s', '0.5', '--pace-period-s', '0.042', '--record-robotcam']
G = S / 'C_V02_E1_GRID_PILOT_20261114_v01/input_rows'; V = S / 'C_V02_SPEED_GUARD_VALID_20261114_v01/input_rows'
TESTS = [('E1_GeoCAD_C100', V / 'T1_GeoCAD_C100.json'), ('S1_GeoCAD_C100', G / 'S1.json'), ('S6_GeoCAD_C100', G / 'S6.json'), ('E1_LR_C40', V / 'T2_LR_C40.json')]
def competing():
    return subprocess.run(['python3', str(S / 'C_V02_E1_GRID_PILOT_20261114_v01/check_competing.py')], capture_output=True).returncode != 0
def guard_means(A):
    from collections import deque
    buf = deque(maxlen=6); mx = {'H_PRE': 0., 'PRE_FINAL': 0.}
    p = A / 'speed_guard_ticks.jsonl'
    if not p.exists(): return mx
    for l in open(p):
        r = json.loads(l); buf.append(r['v'])
        if len(buf) == 6: mx[r['mode']] = max(mx[r['mode']], sum(buf) / 6)
    return mx
def run_test(c, name, row):
    rw = json.loads(row.read_text()); run = W / f'v{int(c*1000):03d}' / name
    if competing(): return dict(name=name, PASS=False, why='COMPETING_PROCESS')
    xyz = ','.join(rw[k] for k in ('start_x_m', 'start_y_m', 'start_yaw_deg'))
    cmd = [PY, str(R / 'scripts/c_v02_drive540_e2e_runner_20261114_v07.py'), '--run-dir', str(run), '--scenario-row', str(row), '--representation', rw['representation'], '--load', 'L4',
           '--occlusion', 'O0', '--group', 'G1', '--role', 'pilot', '--scene-id', rw['source_scene_id'], f'--start-xy-yaw={xyz}', '--cell-id', f'SPC_{int(c*1000)}_{name}', '--cruise-m-s', str(c)] + FLAGS
    log('START %s %s' % (c, name)); run.parent.mkdir(parents=True, exist_ok=True)
    with open(str(run) + '.log', 'x') as f: subprocess.run(cmd, cwd=R, stdout=f, stderr=subprocess.STDOUT)
    from evaluation.c_v02_drive540_technical_gate_20261114_v03 import assess
    res = json.loads((run / 'result.json').read_text()) if (run / 'result.json').exists() else {}
    g = assess(run); gm = guard_means(run / 'attempt_0001')
    chk = dict(technical_pass=g['technical_pass'], success=res.get('outcome') == 'SUCCESS', no_F_trip=res.get('speed_guard_trip') is False, band_main=res.get('band_main') is True,
               final_err_le_1cm=(res.get('final_err_m') or 9) <= .01, legs=res.get('leg_reached') == [True, True] and res.get('stop_certificates') == [True, True],
               H_PRE_mean6_margin=gm['H_PRE'] <= .045, PRE_FINAL_mean6_margin=gm['PRE_FINAL'] <= .027)
    out = dict(name=name, cruise=c, checks=chk, PASS=all(chk.values()), outcome=res.get('outcome'), reason=res.get('reason'), wall_s=res.get('wall_s'), drive_sim_s=res.get('drive_sim_s'),
               final_err_m=res.get('final_err_m'), max_planar=res.get('max_pulse_planar_m_s'), mean6_max=gm, issues=g['issues'][:4])
    log('END %s %s PASS=%s %s' % (c, name, out['PASS'], json.dumps(out, default=str)[:400])); return out
results = {}; chosen = None
for c in (.035, .03):
    results[str(c)] = []
    for name, row in TESTS:
        o = run_test(c, name, row); results[str(c)].append(o)
        if not o['PASS']: break
    ok = len(results[str(c)]) == len(TESTS) and all(o['PASS'] for o in results[str(c)])
    log('CANDIDATE %s %s' % (c, 'PASS' if ok else 'FAIL'))
    if ok: chosen = c; break
if chosen is None: chosen = .02
sel = dict(chosen_cruise_m_s=chosen, rule='0.035 if PASS else 0.03 if PASS else 0.02 (A+B validated)', results=results, tcs_offline=json.loads((S / 'C_V02_SPEED_GUARD_VALID_20261114_v01/tcs_speed_candidates.json').read_text()), time=time.time())
(W / 'speed_selection.json').write_text(json.dumps(sel, indent=1, default=str)); log('CHOSEN %s' % chosen)
notify('C540 cruise speed selected', f'{chosen} m/s (0.035/0.03 candidates validated in order)', 'racing_car')
# ---- final protocol + lock ----
v4 = json.loads((E / 'protocol_amendment_E1_v04_CANDIDATE.json').read_text())
fast = chosen > .02
am = dict(v4, schema='C540_E1_AMENDMENT_v05_FINAL', status='FINAL_PREAPPROVED_BY_RESEARCHER_INSTRUCTION_20261114', supersedes=str(E / 'protocol_amendment_E1_v04_CANDIDATE.json'), supersedes_sha256=sha(E / 'protocol_amendment_E1_v04_CANDIDATE.json'),
          cruise_speed=dict(chosen_m_s=chosen, selection=str(W / 'speed_selection.json'), selection_sha256=sha(W / 'speed_selection.json'),
                            control=('follower v20 vmax=%.3f; governor H_PRE (ceiling .05, ref .035) until 0.1667 m before each leg goal, then latched PRE_FINAL (unchanged final approach); F guard v02 H_PRE .075/.05, PRE_FINAL .045/.03; TC-S steer-rate admission evaluated at the cruise speed' % chosen)
                            if fast else 'follower v19 0.02 m/s, PRE_FINAL throughout, F guard v01 (.045/.03) — A+B validated configuration'),
          applies_to='all 540 runs identically (HR/LR/CAD x C100-C20 x 36)')
amp = E / 'protocol_amendment_E1_v05_FINAL.json'; amp.write_text(json.dumps(am, indent=1, default=str))
cand = json.loads((E / 'main_execution_lock_FINAL_v03_CANDIDATE.json').read_text())
ctrl = 'scripts/c_v02_drive540_e1_main_controller_20261114_v07.py' if fast else 'scripts/c_v02_drive540_e1_main_controller_20261114_v06.py'
appr = 'scripts/c_v02_drive540_e1_main_approve_20261114_v07.py' if fast else 'scripts/c_v02_drive540_e1_main_approve_20261114_v06.py'
files = set(cand['code_sha256'])
if fast:
    files -= {'scripts/c_v02_drive540_e2e_session_20261114_v05.py', 'scripts/c_v02_drive540_e2e_runner_20261114_v06.py', 'scripts/c_v02_drive540_e1_main_controller_20261114_v06.py', 'scripts/c_v02_drive540_e1_main_approve_20261114_v06.py', 'evaluation/c_v02_drive540_outcome_20261114_v03.py'}
    files |= {'scripts/c_v02_drive540_e2e_session_20261114_v06.py', 'scripts/c_v02_drive540_e2e_runner_20261114_v07.py', 'scripts/stage4_ablation_drive_ros_20261114_v02.py', 'evaluation/construction_site_follower_20261114_v20.py',
              'evaluation/c_v02_drive540_speed_guard_f_20261114_v02.py', 'evaluation/c_v02_drive540_outcome_20261114_v03.py', 'evaluation/c_v02_drive540_outcome_20261114_v04.py', ctrl, appr}
lock = dict(cand, schema='C540_E1_MAIN_EXECUTION_LOCK_FINAL_v04', status='FINAL_PREAPPROVED', amendment=str(amp), amendment_sha256=sha(amp), code_sha256={f: sha(R / f) for f in sorted(files)},
            runtime_flags=cand['runtime_flags'] + (['--cruise-m-s', str(chosen)] if fast else []), output_root=cand['output_root'] if not fast else cand['output_root'].replace('E1_main_v04_protocol', 'E1_main_v05_protocol'),
            state_dir=str(E / ('main_controller_v07_state' if fast else 'main_controller_v06_state')), controller=ctrl, cruise_m_s=chosen)
lp = E / 'main_execution_lock_FINAL_v04.json'; lp.write_text(json.dumps(lock, indent=1)); log('LOCK %s %s' % (lp, sha(lp)))
ap = subprocess.run([PY, str(R / appr), '--approve-e1-main540-v07' if fast else '--approve-e1-main540-v06', '--lock', str(lp)], cwd=R, capture_output=True, text=True); log('APPROVE rc=%s %s %s' % (ap.returncode, ap.stdout.strip(), ap.stderr.strip()[-300:]))
dr = subprocess.run([PY, str(R / ctrl), '--lock', str(lp), '--dry-run'], cwd=R, capture_output=True, text=True)
try: gates = json.loads(dr.stdout)['gates']
except Exception: gates = {'dry_run_parse': False}
log('DRYRUN ' + json.dumps(gates))
if ap.returncode != 0 or not all(gates.values()):
    log('NOT STARTED: approval or gates failed'); notify('C540 main NOT started', 'approval/dry-run gate failed: ' + ','.join(k for k, v in gates.items() if not v), 'warning'); sys.exit(2)
unit = 'c-v02-drive540-e1-main-v07'
st = subprocess.run(['systemd-run', '--user', f'--unit={unit}', '-p', 'Restart=no', f'--working-directory={R}', PY, '-u', str(R / ctrl), '--lock', str(lp)], capture_output=True, text=True)
log('START_MAIN rc=%s %s %s' % (st.returncode, st.stdout.strip(), st.stderr.strip()))
(W / 'main_started.json').write_text(json.dumps(dict(unit=unit, lock=str(lp), lock_sha256=sha(lp), cruise_m_s=chosen, controller=ctrl, state_dir=lock['state_dir'], output_root=lock['output_root'], time=time.time()), indent=1))
notify('C540 E1 main540 STARTED', f'cruise {chosen} m/s, unit {unit}', 'rocket')
