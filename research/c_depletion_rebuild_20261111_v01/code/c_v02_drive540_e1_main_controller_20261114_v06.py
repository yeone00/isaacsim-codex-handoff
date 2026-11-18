"""Controller v06 (2026-11-14) = v05 with defaults runner v06 (session v05: filtered speed guard F + verified-stop safety abort) and technical
gate v03 (FAIL_SAFETY_ABORT accepted only with independently verified stop); milestone counts add safety_abort. Everything else identical to v05."""
"""C540 E1 main controller (v05, 2026-11-14). NOT STARTED for main540 until the researcher authorizes the exact lock. Separate from Codex
technical controller v04; never touches v04 files except checking that v04's storage_authorization.json does NOT exist.

Runs the locked manifest sequentially (one Isaac session at a time) with the locked runner + runtime flags. Before EVERY run it re-checks:
manifest/amendment/code SHA, researcher authorization bound to this lock SHA, v04 authorization absent, no competing GPU process,
output volume UUID / free space / writability, no unresolved HOLD. Then:
  - technical HOLD (stop everything, notify): technical gate not PASS, graph-cache shadow mismatch, missing result, archive verify failure;
  - normal scientific failures (no detection, pose/plan rejection, safe drive outside band) are recorded and the run continues;
  - no retries; a run dir that exists without result.json is a HOLD (never re-run automatically);
  - graceful stop: create <state_dir>/STOP_REQUEST -> stops before the next run (status STOPPED_BY_REQUEST); restart resumes;
  - after a HOLD, restart refuses until <state_dir>/hold_resolution_<attempt>.json exists (researcher decision; the HOLD run stays recorded);
  - after each run: tar.zst archive next to the original (original kept) + SHA-256 + full restore verification (every file's SHA-256);
  - milestones (lock['milestones']): milestone_NNN.json + notification with counts per representation, drive ratio, recent pace, ETA,
    projected total and budget risk. Report only: nothing is skipped or changed for schedule reasons.
Lock keys: manifest, manifest_sha256, rows, amendment, amendment_sha256, code_sha256, runtime_flags, output_root, volume_uuid,
min_free_bytes, milestones, state_dir; optional (mock tests only): runner_script, assess_module, notify(bool), budget_h."""
import argparse, csv, hashlib, importlib, json, os, shutil, subprocess, sys, tarfile, time, collections, statistics
from pathlib import Path
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R))
V04 = Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01')
PY = '/home/user/anaconda3/envs/sdg_tools/bin/python'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
ap = argparse.ArgumentParser(); ap.add_argument('--lock', type=Path, required=True); ap.add_argument('--dry-run', action='store_true'); a = ap.parse_args()
lock = json.loads(a.lock.read_text()); LOCK_SHA = sha(a.lock)
ST = Path(lock['state_dir']); ST.mkdir(parents=True, exist_ok=True); LOG = ST / 'controller.log'
RUNNER = R / lock.get('runner_script', 'scripts/c_v02_drive540_e2e_runner_20261114_v06.py')
ASSESS = importlib.import_module(lock.get('assess_module', 'evaluation.c_v02_drive540_technical_gate_20261114_v03')).assess
NOTIFY = lock.get('notify', True); BUDGET_H = lock.get('budget_h', 36.)
def log(m):
    with LOG.open('a') as f: f.write(time.strftime('%Y-%m-%dT%H:%M:%S ') + m + '\n')
def notify(t, m, tag):
    log('NOTIFY ' + t + ' | ' + m)
    if NOTIFY: subprocess.run(['python3', '-c', "import sys;sys.path.insert(0,'/home/user/.claude/hooks/isaacsim');import ntfy_notify as n;n.send(sys.argv[1],sys.argv[2],4,sys.argv[3])", t, m, tag], capture_output=True)
def status(state, **kw):
    tmp = ST / 'status.json.tmp'; tmp.write_text(json.dumps(dict(state=state, updated=time.time(), lock_sha256=LOCK_SHA, **kw), indent=1)); os.replace(tmp, ST / 'status.json')
def hold(reason, attempt=None, blocking=False):
    # blocking holds (a specific run failed technically / incomplete / archive) require hold_resolution_<attempt>.json before restart;
    # gate holds (e.g. missing authorization, competing process) are recorded in last_hold.json and simply re-checked on restart.
    rec = json.dumps(dict(reason=reason, attempt=attempt, blocking=blocking, time=time.time()), indent=1)
    (ST / 'last_hold.json').write_text(rec)
    if blocking: (ST / 'hold.json').write_text(rec)
    status('HOLD', reason=reason, attempt=attempt); log('HOLD ' + reason); notify('C540 E1 main HOLD', reason[:200], 'warning'); sys.exit(2)
def competing():
    out = []
    for l in subprocess.run(['ps', '-eo', 'pid=,stat=,args='], capture_output=True, text=True).stdout.splitlines():
        f = l.split(None, 3)
        if len(f) < 3: continue
        exe = f[2]; args = ' '.join(f[2:])
        if 'python' in exe and any(k in args for k in ('c_v02_drive540_e2e_session', 'c_v03_rover_domain_capture', 'c_v03_rover_domain_train')): out.append(l)
        if exe.endswith('bash') and len(f) > 3 and f[3].split()[0].endswith('run_render_full.sh') and not f[1].startswith('T'): out.append(l)
    return out
def gates():
    g = {}
    g['manifest_sha'] = sha(lock['manifest']) == lock['manifest_sha256']
    g['amendment_sha'] = sha(lock['amendment']) == lock['amendment_sha256']
    g['code_sha'] = all(sha(R / c) == h for c, h in lock['code_sha256'].items()) and str(Path(__file__).resolve().relative_to(R)) in lock['code_sha256']
    auth = ST / 'main_authorization_v06.json'
    g['researcher_authorization'] = auth.exists() and json.loads(auth.read_text()).get('lock_sha256') == LOCK_SHA
    g['v04_storage_authorization_absent'] = not (V04 / 'technical_policy_amendment_v01/storage_authorization.json').exists()
    g['no_competing_process'] = not competing()
    out = Path(lock['output_root']); base = out if out.exists() else out.parent
    uuid = subprocess.run(['findmnt', '-no', 'UUID', '--target', str(base)], capture_output=True, text=True).stdout.strip()
    g['volume_uuid'] = uuid == lock['volume_uuid']; g['free_space'] = shutil.disk_usage(base).free > lock['min_free_bytes']
    g['output_writable'] = os.access(base, os.W_OK)
    hj = ST / 'hold.json'
    g['no_unresolved_hold'] = not hj.exists() or (ST / ('hold_resolution_%s.json' % json.loads(hj.read_text()).get('attempt'))).exists()
    return g
def archive(run):
    arc = run.parent / (run.name + '.tar.zst')
    subprocess.run(['bash', '-c', f'tar -C "{run.parent}" -cf - "{run.name}" | zstd -3 -T4 -q -o "{arc}"'], check=True)
    orig = {str(p.relative_to(run.parent)): sha(p) for p in run.rglob('*') if p.is_file()}
    proc = subprocess.Popen(['zstd', '-dc', str(arc)], stdout=subprocess.PIPE); rest = {}
    with tarfile.open(fileobj=proc.stdout, mode='r|') as tf:
        for m in tf:
            if m.isfile():
                h = hashlib.sha256(); f = tf.extractfile(m)
                for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
                rest[m.name] = h.hexdigest()
    proc.wait()
    return dict(archive=str(arc), sha256=sha(arc), bytes=arc.stat().st_size, original_bytes=sum((run.parent / k).stat().st_size for k in orig),
                files=len(orig), restored_files=len(rest), verified=proc.returncode == 0 and rest == orig)
rows = list(csv.DictReader(open(lock['manifest']))); assert len(rows) == lock['rows'], 'ROW_COUNT'
g = gates(); log('GATES ' + json.dumps(g))
if a.dry_run:
    print(json.dumps(dict(gates=g, rows=len(rows), lock_sha256=LOCK_SHA, would_run=[r['attempt_id'] for r in rows[:3]]), indent=1)); sys.exit(0)
if not all(g.values()): hold('START_GATES_FAILED:' + ','.join(k for k, v in g.items() if not v))
if (ST / 'STOP_REQUEST').exists(): (ST / 'STOP_REQUEST').rename(ST / ('STOP_REQUEST_consumed_%d' % time.time()))
hist = [json.loads(l) for l in open(ST / 'run_history.jsonl')] if (ST / 'run_history.jsonl').exists() else []
MILESTONES = tuple(lock.get('milestones', (30, 100, 180, 270, 360, 450)))
t_first = hist[0]['t_start'] if hist else time.time()
def cls(h):
    if not h.get('technical_pass', True): return 'technical_hold'
    if h['outcome'] == 'FAIL_SAFETY_ABORT': return 'safety_abort_verified_stop'
    if h['outcome'] == 'SUCCESS' or h['moved']: return 'drove'
    if 'NO_DETECTION' in h['reason']: return 'no_detection'
    if h['reason'].startswith(('PLAN_REJECTED', 'FOOTPRINT')): return 'plan_rejected'
    if h['reason'].startswith('POSE_'): return 'pose_rejected'
    return 'other_normal_failure'
def milestone(n):
    busy = sum(h['t_end'] - h['t_start'] for h in hist); recent = hist[-30:]
    pace = statistics.mean(h['t_end'] - h['t_start'] for h in recent)
    per = {rep: dict(collections.Counter(cls(h) for h in hist if h['rep'] == rep)) for rep in ('HR_Scan', 'LR_Scan', 'GeoCAD')}
    drive = sum(cls(h) == 'drove' for h in hist) / len(hist)
    remaining = (len(rows) - n) * pace; total = busy + remaining
    rep = dict(completed=n, planned=len(rows), wall_since_first_start_h=(time.time() - t_first) / 3600, busy_run_time_h=busy / 3600, per_rep=per, drive_ratio=drive,
               recent30_s_per_run=pace, remaining_h=remaining / 3600, eta_local=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + remaining)),
               projected_total_h=total / 3600, budget_h=BUDGET_H, over_budget_risk=('HIGH' if total > BUDGET_H * 3600 else 'MEDIUM' if total > .92 * BUDGET_H * 3600 else 'LOW'),
               technical_holds=sum(cls(h) == 'technical_hold' for h in hist),
               note='report only: no condition is skipped or changed; schedule change or sample reduction needs separate researcher approval')
    (ST / f'milestone_{n:03d}.json').write_text(json.dumps(rep, indent=1)); log('MILESTONE ' + json.dumps(rep))
    notify(f'C540 E1 main {n}/{len(rows)}', f"drive {drive:.0%}, {pace:.0f} s/run, ETA {rep['eta_local']} (total {total/3600:.1f} h, {BUDGET_H:.0f} h risk {rep['over_budget_risk']})", 'hourglass')
done = 0
for r in rows:
    run = Path(lock['output_root']) / r['attempt_id']
    if run.exists():
        if not (run / 'result.json').exists(): hold('INCOMPLETE_RUN_DIR:' + str(run), attempt=r['attempt_id'], blocking=True)
        done += 1; continue
    if (ST / 'STOP_REQUEST').exists():
        status('STOPPED_BY_REQUEST', completed=done, planned=len(rows)); log('STOPPED_BY_REQUEST at %d' % done); notify('C540 E1 main stopped by request', f'{done}/{len(rows)}', 'pause_button'); sys.exit(0)
    g = gates()
    if not all(g.values()): hold('PER_RUN_GATES_FAILED:' + ','.join(k for k, v in g.items() if not v), attempt=r['attempt_id'])
    rowf = ST / 'rows' / (r['attempt_id'] + '.json'); rowf.parent.mkdir(exist_ok=True)
    if not rowf.exists(): rowf.write_text(json.dumps(dict(r, output=str(run)), indent=1))
    cmd = [PY, str(RUNNER), '--run-dir', str(run), '--scenario-row', str(rowf), '--representation', r['representation'], '--load', 'L4', '--occlusion', 'O0', '--group', 'G1',
           '--role', 'main', '--scene-id', r['source_scene_id'], '--start-xy-yaw=' + ','.join(r[k] for k in ('start_x_m', 'start_y_m', 'start_yaw_deg')), '--cell-id', r['attempt_id'],
           '--record-robotcam'] + lock['runtime_flags']
    status('RUNNING', attempt=r['attempt_id'], completed=done, planned=len(rows)); log('START ' + r['attempt_id']); t0 = time.time()
    (ST / 'runner_logs').mkdir(exist_ok=True)
    rl = ST / 'runner_logs' / (r['attempt_id'] + '.log')
    if rl.exists(): rl = ST / 'runner_logs' / ('%s.%d.log' % (r['attempt_id'], time.time()))  # researcher-approved re-run after quarantine keeps the old log
    with rl.open('x') as f:
        rc = subprocess.run(cmd, cwd=R, stdout=f, stderr=subprocess.STDOUT).returncode
    res = json.loads((run / 'result.json').read_text()) if (run / 'result.json').exists() else {}
    try: asmt = ASSESS(run)
    except Exception as e: asmt = dict(technical_pass=False, issues=['ASSESS_EXCEPTION:' + repr(e)])
    (run.parent / (run.name + '.technical_assessment.json')).write_text(json.dumps(asmt, indent=1, default=str))
    opt = json.loads((run / 'attempt_0001/runtime_opt_stats.json').read_text()) if (run / 'attempt_0001/runtime_opt_stats.json').exists() else {}
    shadow_bad = bool((opt.get('graph_cache_stats') or {}).get('shadow_mismatch')) or 'GRAPH_CACHE' in str(res.get('reason'))
    log('END %s rc=%s outcome=%s reason=%s technical_pass=%s' % (r['attempt_id'], rc, res.get('outcome'), res.get('reason'), asmt.get('technical_pass')))
    h = dict(attempt=r['attempt_id'], rep=r['representation'], C=r['C'], start_id=r.get('start_id'), outcome=res.get('outcome'), reason=str(res.get('reason')), moved=bool(res.get('executed_motion')),
             technical_pass=bool(asmt.get('technical_pass')), t_start=t0, t_end=time.time())
    hist.append(h)
    with (ST / 'run_history.jsonl').open('a') as hf: hf.write(json.dumps(h) + '\n')
    if not asmt.get('technical_pass') or shadow_bad or res.get('outcome') in (None, 'INFRA_MISSING_RESULT'): hold('TECHNICAL_HOLD:' + r['attempt_id'] + ':' + str(asmt.get('issues')), attempt=r['attempt_id'], blocking=True)
    ai = archive(run); (run.parent / (run.name + '.archive.json')).write_text(json.dumps(ai, indent=1))
    if not ai['verified']: hold('ARCHIVE_VERIFY_FAILED:' + r['attempt_id'], attempt=r['attempt_id'], blocking=True)
    done += 1
    if done in MILESTONES: milestone(done)
status('MAIN_COMPLETE', completed=done, planned=len(rows)); log('ALL DONE'); notify('C540 E1 main COMPLETE', f'{done}/{len(rows)}', 'checkered_flag')
