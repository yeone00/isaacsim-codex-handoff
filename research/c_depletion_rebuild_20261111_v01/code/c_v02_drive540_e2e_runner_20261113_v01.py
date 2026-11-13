"""C540 single-load fresh-RGBD Full E2E wrapper; preserve legacy lifecycle and numerical guards."""
"""CANDIDATE v05: launches compact-history session v04 and snapshots its projection helper. Not launched. Preserves all original runtime guards and exclusive new output requirement."""
"""Stage-4 ablation runner (v04, 2026-11-11; = v03 launching session v03 (GC scope re-entry at the W pause). v03 note: = v02 launching session v02 (atomic handoff files). v02 note: v01 bug: the session received "--start-xy-yaw -25.888,..." which argparse parses as an option -> fixed by passing "--start-xy-yaw=<value>"; nothing else changed) = scripts/stage3_drive_20261110_v02.py with group/start/O25 arguments, stage-4 session,
stage-4 code snapshot list and stage-4 outcome. One physical drive (or one static panel fixture) per NEW run directory.
Groups: G0 = ORIG_v44 + single approach, G1 = ROBUST_A + single, G2 = ORIG_v44 + Correction B, G3 = ROBUST_A + Correction B.
System side only (sdg_tools Python): prepares <run>/ (never overwrites), copies the v30_03 drive contract + expected graph
(sha-checked), ROS domain probe (must be empty), code snapshot, launches ONE Kit session
(scripts/stage3_drive_session_20261110_v02.py, hh_isaac51 Python), watchdogs it (wall cap, idle cap, close watchdog),
and writes <run>/runner_status.json + <run>/result.json (evaluation/stage3_outcome_20261110_v01.summarize, result files only).
Exit code is informational; success/failure is in result.json. A failed run is never deleted or re-used."""
import argparse, hashlib, json, os, shutil, subprocess, sys, time, uuid, signal
from pathlib import Path
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R))
PY = '/home/user/anaconda3/envs/hh_isaac51/bin/python'
INSTALL = Path('/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim')
V30 = Path('/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03')
PINNED = {'prepared_site_drive.usda': '__RECORD__', 'drive_contract.json': '__RECORD__', 'expected_graph.json': '__RECORD__'}
GROUPS = {'G0': ('ORIG_v44', 'off'), 'G1': ('ROBUST_A', 'off'), 'G2': ('ORIG_v44', 'on'), 'G3': ('ROBUST_A', 'on')}
CODE = ['evaluation/c_v02_drive540_scene_20261113_v06.py','evaluation/c_v02_drive540_physx_gate_20261113_v01.py','evaluation/c_v02_drive540_mount_admission_20261113_v01.py','evaluation/c_v02_task_layer_prior_20261112_v02.py','evaluation/stage4_record_projection_20261111_v01.py', 'scripts/c_v02_drive540_e2e_session_20261113_v01.py', 'evaluation/construction_site_runtime_20261101_v19b.py', 'evaluation/construction_site_persistence_20261101_v21.py', 'scripts/c_v02_stage4_perception_task_prior_20261112_v02.py', 'scripts/stage4_ablation_drive_20261111_v05.py',
        'scripts/stage4_ablation_drive_ros_20261110_v01.py', 'evaluation/stage4_ablation_outcome_20261110_v01.py', 'evaluation/b5_robust_20261110_v01.py',
        'scripts/full_e2e_perception_worker_v01.py', 'analysis/stage3_local_planner_20261109_v01.py', 'evaluation/stage3_failure_diagnosis_20261109_v01.py',
        'evaluation/b1_b5_adapter_20261110_v01.py', 'scripts/three_rep_B5_sensor_20261102_v44.py', 'evaluation/construction_site_follower_20261101_v19.py',
        'evaluation/construction_site_stopping_adapter_20261101_v21.py', 'evaluation/construction_site_stop_certificate_20261101_v21.py',
        'scripts/construction_site_observer_20261101_v18b.py', 'scripts/construction_site_sweep_20261101_v14.py',
        'scripts/construction_site_drive_geometry_20261101_v04.py', 'scripts/construction_site_pilot_link_20261102_v27.py', 'configs/full_e2e_models_v01.json']
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p, x):
    with Path(p).open('x') as f: json.dump(x, f, indent=2, allow_nan=False, default=str)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenario-row',type=Path,required=True);ap.add_argument('--run-dir', type=Path, required=True); ap.add_argument('--mode', choices=['drive', 'fixture'], default='drive')
    ap.add_argument('--representation', choices=['HR_Scan', 'LR_Scan', 'GeoCAD'], required=True)
    ap.add_argument('--load', choices=['L1', 'L4'], required=True); ap.add_argument('--occlusion', choices=['O0', 'O25', 'O50'], required=True)
    ap.add_argument('--group', choices=sorted(GROUPS), default='G0'); ap.add_argument('--trial', type=int, default=1)
    ap.add_argument('--scene-id', required=True); ap.add_argument('--start-xy-yaw', required=True)
    ap.add_argument('--fixture-coverage', type=float, default=.5); ap.add_argument('--record-robotcam', action='store_true')
    ap.add_argument('--role', choices=['smoke', 'pilot', 'main', 'o50', 'fixture', 'diagnostic'], required=True); ap.add_argument('--cell-id', default=None)
    ap.add_argument('--panel-fixture', type=Path, default=None); ap.add_argument('--domain', type=int, default=191)  # legacy_supervised_guard_v01 pins domain 191
    ap.add_argument('--wall-cap-s', type=int, default=1500); ap.add_argument('--idle-cap-s', type=int, default=600)
    a = ap.parse_args(); run = a.run_dir
    run.mkdir(parents=True, exist_ok=False)
    status = dict(status='PREPARING', started=time.time()); t0 = time.monotonic()
    try:
        if a.occlusion in ('O25', 'O50') and a.mode == 'drive': assert a.panel_fixture and a.panel_fixture.exists(), 'PANEL_FIXTURE_MISSING'
        pose_method, corr_b = GROUPS[a.group]
        frozen = Path('/home/user/hh/isaac_cosmos/sdg_final/B5_ROBUST_20261110_v01_run01/frozen_config.json')
        pinned = {n: sha(V30 / n) for n in PINNED}
        for n in ('drive_contract.json', 'expected_graph.json'): shutil.copyfile(V30 / n, run / n); assert sha(run / n) == pinned[n]
        spec = dict(schema='stage4_ablation_run_spec_v01', cell_id=a.cell_id or f'{a.scene_id}_{a.representation}_{a.group}_t{a.trial}', role=a.role, mode=a.mode,
                    representation=a.representation, load=a.load, occlusion=a.occlusion, group=a.group, pose_method=pose_method, correction_b=corr_b, arm='improved',
                    scene_id=a.scene_id, trial=a.trial, material='red', record_robotcam=a.record_robotcam, fixture_coverage=a.fixture_coverage if a.mode == 'fixture' else None,
                    start_xy_yaw_deg=[float(x) for x in a.start_xy_yaw.split(',')], base_stage=str(V30 / 'prepared_site_drive.usda'), pinned_v30_inputs=pinned,
                    robust_A_frozen_config=str(frozen), robust_A_frozen_config_sha256=sha(frozen),
                    panel_fixture=str(a.panel_fixture) if a.panel_fixture else None, panel_fixture_sha256=sha(a.panel_fixture) if a.panel_fixture else None,
                    perception='C-V02 locked75:25 seed42; no model reselection', pose={'ORIG_v44': 'ORIG_v44 sensor auto-ROI B5 (unchanged)', 'ROBUST_A': 'Correction A b5_robust v01 frozen'}[pose_method],
                    planner='TC-S v01 (rate cap 4.3976 deg/s) all groups', controller='v19 command + v21 stopping adapter + stage4 N-leg ROS driver (v21 per-leg law), 0.03 m/s guard unchanged', ros_domain=a.domain,
                    code_sha256={c: sha(R / c) for c in CODE}, research_denominator='counted' if a.role in ('main', 'o50') else 0)
        scenario=json.loads(a.scenario_row.read_text());assert scenario['representation']==a.representation and scenario['O']=='O0' and a.group=='G1'
        spec.update(C=scenario['C'],load=scenario['C'],load_count=1,pallet_count=1,task_layer_count=int(scenario['task_layer_count']),source_family=scenario['source_family'],base_id=scenario['base_id'],checkpoint=scenario['checkpoint'],checkpoint_sha256=scenario['checkpoint_sha256'],scenario_row=str(a.scenario_row),scenario_sha256=sha(a.scenario_row))
        dump(run / 'run_spec.json', spec)
        snap = run / 'executed_code'; snap.mkdir()
        for c in CODE: shutil.copyfile(R / c, snap / Path(c).name)
        env = dict(os.environ, ROS_DOMAIN_ID=str(a.domain), ROS_DISTRO='jazzy', RMW_IMPLEMENTATION='rmw_fastrtps_cpp')
        env['LD_LIBRARY_PATH'] = env.get('LD_LIBRARY_PATH', '') + ':' + str(INSTALL / 'exts/isaacsim.ros2.bridge/jazzy/lib')
        env.pop('PYTHONPATH', None)
        if a.mode == 'drive':
            probe = ['/bin/bash', '-c', 'source /opt/ros/jazzy/setup.bash && exec "$@"', 'probe', '/usr/bin/python3', str(R / 'scripts/legacy_supervised_observer_v02.py'), '--output', str(run / 'domain_probe'), '--probe-only']
            with (run / 'probe.log').open('x') as f: r = subprocess.run(probe, env=env, stdout=f, stderr=subprocess.STDOUT, timeout=30)
            assert r.returncode == 0, 'DISCOVERY_TIMEOUT:ROS_DOMAIN_NOT_EMPTY'
        gpu = subprocess.run(['nvidia-smi', '--query-compute-apps=pid,process_name,used_memory', '--format=csv,noheader'], capture_output=True, text=True, timeout=10)
        status['gpu_before'] = gpu.stdout
        nonce = uuid.uuid4().hex; env['V10C_RUN_NONCE'] = nonce
        cmd = [PY, str(R / 'scripts/c_v02_drive540_e2e_session_20261113_v01.py'), '--output', str(run / 'attempt_0001'), '--domain', str(a.domain), '--mode', a.mode,
               '--representation', a.representation, '--load', a.load, '--occlusion', a.occlusion, '--pose-method', pose_method, '--correction-b', corr_b,
               '--start-xy-yaw=' + a.start_xy_yaw, '--fixture-coverage', str(a.fixture_coverage), '--base-stage', str(V30 / 'prepared_site_drive.usda')]
        cmd+=['--scenario-row',str(a.scenario_row)]
        if a.panel_fixture and a.mode == 'drive': cmd += ['--panel-fixture', str(a.panel_fixture)]
        if a.record_robotcam: cmd += ['--record-robotcam']
        status.update(status='LAUNCHED', command=cmd, nonce=nonce)
        with (run / 'runtime.log').open('x') as f:
            child = subprocess.Popen(cmd, env=env, cwd=R, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
            def abort(*_):
                status['supervisor_abort'] = True; at = run / 'attempt_0001'
                if at.exists(): (at / 'abort_motion').touch()
            signal.signal(signal.SIGTERM, abort); signal.signal(signal.SIGINT, abort)
            started = time.monotonic(); close_seen = None
            while child.poll() is None:
                at = run / 'attempt_0001'
                if (at / 'execution_provisional.json').exists() and close_seen is None: close_seen = time.monotonic()
                newest = (run / 'runtime.log').stat().st_mtime
                if at.exists():
                    for q in list(at.iterdir()):
                        try: newest = max(newest, q.stat().st_mtime)
                        except OSError: pass  # atomic .tmp files vanish between listing and stat (run03 runner bug)
                reason = ('KIT_CLOSE_HANG' if close_seen is not None and time.monotonic() - close_seen > 40 else
                          'HANG:RUN_WALL_CAP' if time.monotonic() - started > a.wall_cap_s else
                          'HANG:NO_FILE_PROGRESS' if time.time() - newest > a.idle_cap_s else None)
                if reason:
                    status.setdefault('watchdog', reason)
                    if reason != 'KIT_CLOSE_HANG': abort(); time.sleep(20)
                    try:
                        with (run / 'watchdog_ps.txt').open('w') as pf: subprocess.run(['ps', '-o', 'pid,etime,stat,wchan:32,cmd', '-g', str(child.pid)], stdout=pf, stderr=subprocess.STDOUT, timeout=10)
                    except Exception: pass
                    os.killpg(child.pid, signal.SIGTERM)
                    try: child.wait(timeout=10)
                    except subprocess.TimeoutExpired: os.killpg(child.pid, signal.SIGKILL); child.wait(timeout=10)
                    status['forced_termination'] = reason != 'KIT_CLOSE_HANG'; status['close_watchdog'] = reason == 'KIT_CLOSE_HANG'
                    break
                time.sleep(.5)
        status.update(status='EXITED', exit_code=child.returncode, close_log_confirmed='Simulation App Shutting Down' in (run / 'runtime.log').read_text(errors='replace'))
        if status.get('forced_termination'): status['reason'] = status['watchdog']
    except Exception as exc:
        status.update(status='RUNNER_FAILED', reason=str(exc))
    status['wall_s'] = time.monotonic() - t0; status['ended'] = time.time()
    dump(run / 'runner_status.json', status)
    try:
        from evaluation.stage4_ablation_outcome_20261110_v01 import summarize
        res = summarize(run) if a.mode == 'drive' else dict(mode='fixture', fixture=json.loads((run / 'attempt_0001/stage4_panel_fixture.json').read_text()) if (run / 'attempt_0001/stage4_panel_fixture.json').exists() else None)
    except Exception as exc:
        res = dict(outcome='INFRA_MISSING_RESULT', category='E', reason='SUMMARIZE_EXCEPTION:' + repr(exc))
    dump(run / 'result.json', res); print(json.dumps({k: res.get(k) for k in ('cell_id', 'outcome', 'category', 'reason', 'final_err_m', 'pose_err_xy_m', 'b_decision', 'executed_motion')} if a.mode == 'drive' else {'fixture': (res.get('fixture') or {}).get('status')}), flush=True)
    return 0

if __name__ == '__main__': raise SystemExit(main())
