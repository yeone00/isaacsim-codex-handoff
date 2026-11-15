"""LE13 IPR frozen K1 inference runner v01 (2026-11-15). For every capture of one representation in the prelock manifest, runs the
UNCHANGED drive perception (scripts/c_v02_stage4_perception_task_prior_20261114_v03.py: frozen C-V02 seed42 model, conf 0.25,
task-region gate with the drive's own gate argument for that start, ROBUST_A with the operator layer prior) in a SEPARATE process
per capture (one YOLO model per process). Never passes GT. Skips captures already inferred; records per-capture status.
Usage: python scripts/le13_ipr_k1_inference_20261115_v01.py <ns_dir> <rep>"""
import csv, json, sys, subprocess, hashlib, time
from pathlib import Path
R = Path(__file__).resolve().parents[1]
NS, REP = Path(sys.argv[1]), sys.argv[2]; P = NS / 'prelock'; C = NS / 'captures_v01' / REP
V = Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01'); ML = V / 'MIX_C06_20261112_v01/selection_lock.json'
PY = '/home/user/anaconda3/envs/sdg_tools/bin/python'; PERC = R / 'scripts/c_v02_stage4_perception_task_prior_20261114_v03.py'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
lock = json.loads((P / 'PRELOCK.json').read_text()); assert sha(ML) == lock['frozen']['model_lock_sha256'] and sha(PERC) == lock['frozen']['perception_sha256'], 'FROZEN_ARTIFACT_CHANGED'
REG = P / 'task_registry.json'; assert sha(REG) == lock['files']['task_registry.json']
starts = json.loads((P / 'start_cameras.json').read_text())
rows = [r for r in csv.DictReader((P / 'capture_manifest.csv').open()) if r['rep'] == REP]
log = (NS / 'inference_v01'); log.mkdir(exist_ok=True); st_path = log / f'status_{REP}.jsonl'
for r in rows:
    cid = r['capture_id']; cap = C / cid; comp = C / 'complete' / f'{cid}.json'
    if (cap / 'perception_result.json').exists(): continue
    rec = dict(capture_id=cid, rep=REP, time=time.time())
    if not comp.exists() or json.loads(comp.read_text()).get('state') != 'PASS_CAPTURE':
        rec.update(status='CAPTURE_MISSING_OR_FAILED')
    else:
        cmd = [PY, str(PERC), '--capture', str(cap), '--representation', REP, '--layer-count', r['task_layer_count'], '--pose-method', 'ROBUST_A', '--mode', 'initial',
               starts[r['start_id']]['gate_arg'], '--task-metadata', str(P / 'tasks' / f"{r['task_id']}.json"), '--task-registry', str(REG), '--task-registry-sha', sha(REG),
               '--model-lock', str(ML), '--model-lock-sha', sha(ML)]
        p = subprocess.run(cmd, cwd=R, capture_output=True, text=True, timeout=600)
        (cap / 'inference_stdout.log').write_text(p.stdout[-20000:] + '\n--- stderr ---\n' + p.stderr[-20000:])
        (cap / 'inference_command.json').write_text(json.dumps(dict(argv=cmd, GT_input=False), indent=1))
        rec.update(status='RAN', rc=p.returncode)
    with st_path.open('a') as f: f.write(json.dumps(rec) + '\n')
print('done', REP)
