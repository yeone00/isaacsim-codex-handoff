"""C540 auto-resume supervisor v04 (2026-11-14 20:4x) = v03 plus ONE narrow class SAFE_STOPPED_ADAPTER_CAP_FAULT, added after
L13_C2E_B12_C20_GeoCAD_O0: the stopping adapter latched MEASURED_PHASE_CAP_EXCEEDED on a single-tick measured-speed spike in H_PRE/PRE_FINAL
(0.0193 -> 0.0307 m/s vs ceiling 0.030; commanded wheel 0.012 m/s) and zeroed the rover. Accepted ONLY if: exactly one adapter fault transition
and it is MEASURED_PHASE_CAP_EXCEEDED in H_PRE/PRE_FINAL; the faulting tick's planar speed <= 1.25 x the unchanged phase ceiling and the
previous tick was below the ceiling (isolated spike, not a runaway); collision false; stop_quiet QUIET PASS; cleanup zero VERIFIED_ROS_ZERO;
observer+driver exit 0; no speed-guard trip; at most 3 such resolutions in the whole main (a 4th -> safety stop, systematic).
Recorded as-is (FAIL_D in the denominator, counted as failure), no re-run; thresholds/pipeline unchanged. All other faults as v03.
(v03 text follows)
C540 auto-resume supervisor v03 (2026-11-14) = v02 classification rules, re-targeted to the L_E13 main (lock LE13_FINAL_v05, controller v07,
unit c-v02-drive540-le13-main-v07, state main_controller_v07_state, reporter c-v02-drive540-le13-reporter). Researcher instruction 2026-11-14:
recoverable technical problems are resolved and resumed automatically without approval; real safety problems still stop safely.
v02 text follows:
C540 E1 main auto-resume supervisor (v02, 2026-11-14). v02 adds class SAFE_STOPPED_HANDOFF_RACE: after motion, the locked driver
read a leg handoff file that the session had just unlinked (exists()->read TOCTOU, FileNotFoundError in driver_guard_fault.json) while the
rover was paused between legs; accepted ONLY if collision false, stop_quiet QUIET PASS, cleanup zero VERIFIED_ROS_ZERO, every reached leg has a
stop certificate, no speed-guard trip. Recorded as-is (FAIL_D in the denominator), no re-run. All other post-motion faults still stop.
(v01 text follows)
Researcher standing instruction (2026-11-14 ~11:01): "앞으로는 중단될 일 없게 해. 중단되어야 하더라도 자동 재개. 스크립트 입력 없이 자동 실행".
Changes nothing in the locked pipeline (controller/runner/session/lock untouched). Every 60 s, if the controller unit is not active:
  - MAIN_COMPLETE or STOP_REQUEST present -> do nothing (exit on complete).
  - non-blocking gate HOLD / controller crash -> restart (start gates are re-checked by the controller itself).
  - blocking HOLD on attempt A -> classify from A's own result/technical assessment:
      INFRA (no motion: executed_motion false, distance 0/None, no collision, no driver admitted) or ARCHIVE_VERIFY_FAILED
        -> write hold_resolution_A.json (RECORD_AS_FAIL_E_INFRA_AND_CONTINUE_NO_RERUN, decided_by auto-resume v01), restart.
      INCOMPLETE run dir (no result.json) with no driver admission/commands -> rename dir to A.incomplete_<ts> (kept, not deleted),
        write resolution, restart (the attempt runs once more; a 2nd incomplete for the same attempt -> SAFETY_STOP).
      anything involving motion with a technical failure, collision, HOLD_SAFETY, stop-certificate / unrecovered control /
        unknown safety -> NOT resumed (researcher's predefined safety stop conditions); ntfy once.
  - consecutive auto-resumes without a technical-PASS run in between: >=3 -> 20 min cool-down before restart; >=6 -> stop + ntfy
    (pipeline evidently broken; continuing would turn remaining rows into FAIL_E).
Every action is logged to <state>/auto_resume.log and auto_resume_actions.jsonl."""
import json, time, subprocess, sys
from pathlib import Path
R = Path('/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013')
D = Path('/home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_LE13_20261114_v01'); ST = D / 'main_controller_v07_state'
L = D / 'main_execution_lock_LE13_FINAL_v05.json'; W = Path('/home/user/hh/isaac_cosmos/sdg_final/C_V02_SPEED_CANDIDATES_20261114_v01')
PY = '/home/user/anaconda3/envs/sdg_tools/bin/python'; CTRL = 'scripts/c_v02_drive540_le13_main_controller_20261114_v07.py'
UNIT = 'c-v02-drive540-le13-main-v07'; OUT = Path(json.loads(L.read_text())['output_root'])
SAFETY_WORDS = ('COLLISION', 'STOP_CERT', 'HOLD_SAFETY', 'UNRECOVERED', 'SAFETY_UNKNOWN', 'QUIET', 'ZERO_RECOVERY', 'NOT_STOPPED')
AS = ST / 'auto_resume_state.json'
def log(m):
    with (ST / 'auto_resume.log').open('a') as f: f.write(time.strftime('%FT%T ') + m + '\n')
def act(**k):
    k['time'] = time.strftime('%FT%T')
    with (ST / 'auto_resume_actions.jsonl').open('a') as f: f.write(json.dumps(k) + '\n')
def notify(t, m, tag):
    subprocess.run(['python3', '-c', "import sys;sys.path.insert(0,'/home/user/.claude/hooks/isaacsim');import ntfy_notify as n;n.send(sys.argv[1],sys.argv[2],4,sys.argv[3])", t, m, tag], capture_output=True)
def jl(p):
    try: return json.loads(Path(p).read_text())
    except Exception: return {}
def active(): return subprocess.run(['systemctl', '--user', 'is-active', UNIT], capture_output=True, text=True).stdout.strip() in ('active', 'activating')
CEIL = {'H_PRE': .05, 'PRE_FINAL': .03}
def cap_fault(a, res, sq, cz):
    try: rows = [json.loads(l) for l in open(a / 'adapter_commands.jsonl')]
    except Exception: return None
    tr = [(i, t) for i, r in enumerate(rows) for t in ((r.get('adapter') or {}).get('transitions') or []) if t.get('after') == 'FAULT_LATCHED']
    if len(tr) != 1 or tr[0][1].get('cause') != 'MEASURED_PHASE_CAP_EXCEEDED' or tr[0][0] == 0: return None
    i = tr[0][0]; ui = rows[i]['adapter'].get('update_input') or {}; ph = ui.get('phase'); c = CEIL.get(ph)
    prev = (rows[i - 1].get('adapter') or {}).get('update_input') or {}
    own = jl(a / 'owned_processes.json'); n_prev = sum(1 for p in ST.glob('hold_resolution_*.json') if jl(p).get('kind') == 'SAFE_STOPPED_ADAPTER_CAP_FAULT')
    ok = (c and ui.get('planar', 9) <= 1.25 * c and prev.get('planar', 9) < c and res.get('collision') is False and sq.get('QUIET') == 'PASS'
          and cz.get('status') == 'VERIFIED_ROS_ZERO' and not res.get('speed_guard_trip') and all((own.get(k) or {}).get('exit_code') == 0 for k in ('observer', 'driver')))
    if not ok: return None
    if n_prev >= 3: return 'SAFETY', 'adapter cap fault recurring (4th): systematic, needs researcher'
    return 'SAFE_STOPPED_ADAPTER_CAP_FAULT', f"single-tick speed spike {ui.get('planar'):.4f} m/s (prev {prev.get('planar'):.4f}) > {ph} ceiling {c}; adapter zeroed, quiet PASS, ROS zero verified, no collision"
def classify(attempt, reason):
    run = OUT / attempt
    if reason.startswith('ARCHIVE_VERIFY_FAILED'): return 'ARCHIVE', 'archive verification failed; original run dir kept'
    if reason.startswith('INCOMPLETE_RUN_DIR'):
        a = run / 'attempt_0001'
        if any((a / f).exists() for f in ('driver_admitted.json', 'adapter_commands.jsonl', 'driver_ready.json')): return 'SAFETY', 'incomplete run after driver admission: motion/safety state unknown'
        return 'INCOMPLETE_NO_DRIVER', 'incomplete run, driver never admitted (no motion possible)'
    res = jl(run / 'result.json'); asmt = jl(OUT / (attempt + '.technical_assessment.json'))
    txt = json.dumps([res.get('outcome'), res.get('reason'), asmt.get('issues'), reason]).upper()
    a = run / 'attempt_0001'; gf = jl(a / 'driver_guard_fault.json'); sq = jl(a / 'stop_quiet_result.json'); cz = jl(a / 'cleanup_zero_classification.json')
    race = 'No such file or directory' in str(gf.get('reason')) and any(k in str(gf.get('reason')) for k in ('leg_validation_pause.json', 'next_leg_', '_stop.json', '_path.json'))
    if (race and res.get('collision') is False and sq.get('QUIET') == 'PASS' and cz.get('status') == 'VERIFIED_ROS_ZERO' and not res.get('speed_guard_trip')
            and res.get('stop_certificates') and all(res['stop_certificates']) and len(res['stop_certificates']) == sum(bool(x) for x in res.get('leg_reached') or [])):
        return 'SAFE_STOPPED_HANDOFF_RACE', 'driver handoff-file race while paused between legs; quiet PASS, ROS zero verified, no collision: ' + str(gf.get('reason'))[-60:]
    cap = cap_fault(a, res, sq, cz)
    if cap: return cap
    if res.get('collision') is True or any(w in txt for w in SAFETY_WORDS): return 'SAFETY', 'safety-related: ' + txt[:200]
    moved = res.get('executed_motion') or asmt.get('actual_motion') or (res.get('drive_distance_m') or 0) > 0
    if moved: return 'SAFETY', 'technical failure after motion: ' + txt[:200]
    if (run / 'attempt_0001' / 'driver_admitted.json').exists() and res.get('executed_motion') is None: return 'SAFETY', 'driver admitted but motion flag unknown'
    return 'INFRA', 'no motion, no collision: ' + str(res.get('reason'))[:120]
def restart(why):
    subprocess.run(['systemctl', '--user', 'reset-failed', UNIT], capture_output=True)
    dry = subprocess.run([PY, CTRL, '--lock', str(L), '--dry-run'], cwd=R, capture_output=True, text=True)
    try: g = json.loads(dry.stdout)['gates']
    except Exception: g = {'dry_run_parse': False}
    if not all(g.values()):
        log('DRY_RUN_GATES_FAIL ' + json.dumps(g)); act(action='dry_run_fail', gates=g); return False
    r = subprocess.run(['systemd-run', '--user', '--unit=' + UNIT, '-p', 'Restart=no', '--working-directory=' + str(R), PY, '-u', CTRL, '--lock', str(L)], capture_output=True, text=True)
    ok = r.returncode == 0
    p = D / 'reporter_state.json'
    if ok and p.exists():
        s = jl(p); s['stop_notified'] = False; p.write_text(json.dumps(s))
    log(f'RESTART ok={ok} {why} {r.stderr.strip()[:200]}'); act(action='restart', ok=ok, why=why)
    notify('C540 main auto-resumed' if ok else 'C540 main auto-resume FAILED', why[:200], 'repeat' if ok else 'warning')
    return ok
s = jl(AS) or dict(consecutive=0, last_pass_count=0, stopped=False, notified_attempt=None, incomplete_seen=[])
log('SUPERVISOR START')
while True:
    try:
        stt = jl(ST / 'status.json'); hist = [json.loads(l) for l in open(ST / 'run_history.jsonl')] if (ST / 'run_history.jsonl').exists() else []
        npass = sum(bool(h.get('technical_pass')) for h in hist)
        if npass > s['last_pass_count']: s['consecutive'] = 0; s['last_pass_count'] = npass
        if stt.get('state') == 'MAIN_COMPLETE': log('MAIN_COMPLETE, supervisor exit'); AS.write_text(json.dumps(s)); break
        if not active() and not (ST / 'STOP_REQUEST').exists() and not s['stopped']:
            hj = ST / 'hold.json'; hold = jl(hj) if hj.exists() else {}
            attempt = hold.get('attempt'); reason = str(hold.get('reason', ''))
            unresolved = bool(attempt) and not (ST / f'hold_resolution_{attempt}.json').exists()
            if s['consecutive'] >= 6:
                s['stopped'] = True; log('STOP: 6 consecutive auto-resumes without a technical PASS')
                notify('C540 main STOPPED (auto-resume limit)', '6 consecutive infra holds without a technical PASS; pipeline needs inspection', 'warning')
            elif unresolved:
                kind, why = classify(attempt, reason)
                if kind == 'SAFETY' or (kind == 'INCOMPLETE_NO_DRIVER' and attempt in s['incomplete_seen']):
                    if s['notified_attempt'] != attempt:
                        log(f'NO_AUTO_RESUME {attempt} {kind} {why}'); act(action='no_resume', attempt=attempt, kind=kind, why=why)
                        notify('C540 main HOLD needs researcher (safety)', f'{attempt}: {why}'[:250], 'rotating_light'); s['notified_attempt'] = attempt
                else:
                    if s['consecutive'] >= 3 and time.time() - hold.get('time', 0) < 1200: pass  # cool-down
                    else:
                        if kind == 'INCOMPLETE_NO_DRIVER':
                            q = OUT / f'{attempt}.incomplete_{int(time.time())}'; (OUT / attempt).rename(q); s['incomplete_seen'].append(attempt)
                            dec = 'QUARANTINE_INCOMPLETE_NO_DRIVER_AND_RUN_ONCE_MORE'; why += f' -> kept at {q.name}'
                        else: dec = 'RECORD_AS_IS_IN_DENOMINATOR_AND_CONTINUE_NO_RERUN' if kind in ('SAFE_STOPPED_HANDOFF_RACE', 'SAFE_STOPPED_ADAPTER_CAP_FAULT') else 'RECORD_AS_FAIL_E_INFRA_AND_CONTINUE_NO_RERUN'
                        (ST / f'hold_resolution_{attempt}.json').write_text(json.dumps(dict(attempt=attempt, decision=dec, kind=kind, evidence=why, hold_reason=reason[:500],
                            decided_by='auto-resume supervisor v04 under researcher standing instruction 2026-11-14 (auto-resume without script input)', time=time.strftime('%FT%T')), indent=1))
                        act(action='resolve', attempt=attempt, kind=kind, decision=dec, why=why); log(f'RESOLVED {attempt} {kind} {dec}')
                        s['consecutive'] += 1; restart(f'{attempt} {kind}: {why}')
            else:
                # resolved hold, gate hold or crash: controller re-checks gates; space retries 5 min apart
                if time.time() - s.get('last_try', 0) > 300:
                    s['last_try'] = time.time()
                    if stt.get('state') != 'HOLD': s['consecutive'] += 1  # crash counts; plain gate holds just retry every 5 min
                    restart(f"state={stt.get('state')} reason={str(stt.get('reason'))[:120]}")
        AS.write_text(json.dumps(s))
    except Exception as e:
        log('ERROR ' + repr(e))
    time.sleep(60)
