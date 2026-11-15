"""LE13 IPR pre-capture lock v02 (2026-11-15) = v01 with ONE correction (amendment A1, decided BEFORE any v02 capture/inference):
the B1 red manifest dome_intensity is ALREADY the C-V02-mapped value (e.g. B1R_TST_000001: red 11200 = C-V02 dome 11200, B1 original 64000),
so v01 applied the mapping twice (8420-8640). v02 uses the red dome value unchanged = the C-V02 / drive lighting convention.
Family selection, trajectories, starts, tasks, cameras, analysis plan: unchanged. v01 outputs preserved and reported as a disclosed deviation.
(v01 text follows)
LE13 independent pose-precision replication (IPR) — pre-capture lock v01 (2026-11-15).
Implements docs/LE13_independent_pose_precision_replication_protocol_20261115_v01.md (handoff repo). Read-only over prior artifacts.
1. Source-ID audit: candidate families = B1 red TEST scenes with layer_count 4 (the same source pool the C-V02 test families came from).
   Excluded: the 10 C-V02 test families (used by the old 540 / E1 drives), all C-V02 train/val families (model training / selection;
   C-V03 used train + val families). Every candidate is checked by exact-string search for zero occurrence in the C-V02 / depletion /
   drive / C-V03 namespaces. Selection rule (fixed before capture): sort eligible scene_id ascending, take the first 36.
2. Family construction (same algorithms as C-V02, nothing tuned): environment id IPR_<scene_id>; layer phase = source layer_phase;
   effective dome = 8000 + 0.05 * source dome (C-V02 mapping); ONE seeded depletion trajectory T01 with the C-V02 4-layer audited
   algorithm and master seed 260929 -> C100/C80/C60/C40/C20 (60/48/36/24/12 bundles); start pose = the 7 LE13 drive start poses
   assigned cyclically by family order (S0..S6); K1 camera pose/intrinsics = the exact LE13 drive K1 camera of that start (recorded
   T_world_optical, identical across all drive runs of that start); gate centre = the drive's own gate argument for that start.
3. Task metadata (operator occupied-layer prior, C-V02 mapping C100/C80->4, C60->3, C40->2, C20->1) in a NEW locked registry.
Writes <ns>/prelock/{family_selection.csv, capture_manifest.csv, task_registry.json, tasks/*.json, start_cameras.json, PRELOCK.json}.
Usage: python analysis/le13_ipr_prelock_20261115_v01.py <namespace_dir>"""
import csv, json, sys, hashlib, subprocess, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation.c_depletion_geometry_20261111_v01 import pure_original
NS = Path(sys.argv[1]); P = NS / 'prelock'; P.mkdir(parents=True, exist_ok=True); (P / 'tasks').mkdir(exist_ok=True)
S = Path('/home/user/hh/isaac_cosmos/sdg_final'); V = S / 'C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01'
RED = S / 'B1_RED_QUALITY_20261103_v01/red_only_plan_v03/red_only_manifest_1400_v03.csv'
DRIVE_OUT = Path('/media/user/1997fec1-5a55-49af-a41b-e2095924fd81/isaac_research/C_V02_DRIVE540_20261113_v01/LE13_main_v01')
DRIVE_MAN = S / 'C_V02_DRIVE540_LE13_20261114_v01/attempt_manifest_LE13_v01.csv'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
red = list(csv.DictReader(RED.open())); fam = list(csv.DictReader((V / 'data_design_v01/families.csv').open()))
used_src = {f['source_scene_id'] for f in fam}
cand = sorted(r['scene_id'] for r in red if r['split'] == 'test' and r['layer_count'] == '4')
NAMESPACES = [S / 'C_DEPLETION_REBUILD_20261111_v01', S / 'C_V02_DRIVE540_LE13_20261114_v01', S / 'C_V02_DRIVE540_E1_20261114_v01', S / 'C_V03_ROVER_DOMAIN_20261113_v01',
              S / 'C_V03_SITE_INDEP_CAPTURE_20261113_v01_run01', S / 'C_V02_LE13_PILOT_20261114_v01', S / 'C_V02_SITE_LOCATION_STUDY_20261114_v01', S / 'C_V02_MULTIVIEW_STUDY_20261114_v01']
audit = []
for s in cand:
    hits = []
    for ns in NAMESPACES:
        if not ns.exists(): continue
        r = subprocess.run(['grep', '-rl', '--include=*.csv', '--include=*.json', '--include=*.jsonl', '-F', s + '"', str(ns)], capture_output=True, text=True)
        r2 = subprocess.run(['grep', '-rl', '--include=*.csv', '--include=*.json', '--include=*.jsonl', '-F', s + ',', str(ns)], capture_output=True, text=True)
        r3 = subprocess.run(['grep', '-rl', '--include=*.csv', '--include=*.json', '--include=*.jsonl', '-F', s + '_', str(ns)], capture_output=True, text=True)
        n = len(set((r.stdout + r2.stdout + r3.stdout).split()))
        if n: hits.append(f'{ns.name}:{n}')
    audit.append(dict(scene_id=s, in_C_V02_families=s in used_src, namespace_hits=';'.join(hits), eligible=(s not in used_src and not hits)))
elig = [a['scene_id'] for a in audit if a['eligible']]
state = 'PASS' if len(elig) >= 36 else 'INDEPENDENCE_NOT_ESTABLISHED'
sel = elig[:36]
with (P / 'source_audit.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(audit[0])); w.writeheader(); [w.writerow(a) for a in audit]
if state != 'PASS':
    (P / 'PRELOCK.json').write_text(json.dumps(dict(state=state, eligible=len(elig)), indent=1)); print(state, len(elig)); sys.exit(2)
# start cameras from the drive (exact recorded K1 camera per start id)
dm = list(csv.DictReader(DRIVE_MAN.open())); starts = {}
for r in dm:
    sid = r['start_id']
    if sid in starts: continue
    A = DRIVE_OUT / r['attempt_id'] / 'attempt_0001'
    cm = json.loads((A / 'camera_metadata.json').read_text()); pc = json.loads((A / 'perception_command.json').read_text())
    gate = next(x for x in pc['argv'] if x.startswith('--gate-center='))
    starts[sid] = dict(start_xy_yaw=[float(r['start_x_m']), float(r['start_y_m']), float(r['start_yaw_deg'])], T_world_optical=cm['calibration']['T_world_optical'],
                       fx=cm['calibration']['fx'], fy=cm['calibration']['fy'], raw_focal=cm['raw_parameters']['cameraFocalLength'], raw_haperture=cm['raw_parameters']['cameraAperture'][0],
                       gate_arg=gate, source_attempt=r['attempt_id'])
(P / 'start_cameras.json').write_text(json.dumps(starts, indent=1))
SIDS = sorted(starts)
ns = pure_original(); redby = {r['scene_id']: r for r in red}
fams, rows, registry = [], [], {}
MAP = {'C100': 4, 'C80': 4, 'C60': 3, 'C40': 2, 'C20': 1}
for i, s in enumerate(sel):
    src = redby[s]; env = 'IPR_' + s; ph = src['layer_phase']; assert ph in ('ABAB', 'BABA')
    seed, snaps, hist = ns['generate_trajectory'](env, 1, ph); dome = float(src['dome_intensity']); st = SIDS[i % len(SIDS)]
    fams.append(dict(family_id=f'F{i + 1:02d}', source_scene_id=s, source_split='test', environment_id=env, layer_phase=ph, source_dome=src['dome_intensity'], effective_dome=dome,
                     trajectory='T01', depletion_seed=seed, start_id=st))
    for c in ('C100', 'C80', 'C60', 'C40', 'C20'):
        stt = snaps[c]; mask = ns['mask_by_layer_json'](stt, ph); nb = ns['state_count'](stt)
        task = dict(schema='C_V02_TASK_LAYER_PRIOR_v01', task_id=f'IPR_F{i + 1:02d}_{c}', task_layer_count=MAP[c], provider='operator_or_task_management_system')
        registry[task['task_id']] = task; (P / 'tasks' / f"{task['task_id']}.json").write_text(json.dumps(task, indent=1))
        for rep in ('HR_Scan', 'LR_Scan', 'GeoCAD'):
            rows.append(dict(capture_id=f"IPR_F{i + 1:02d}_{c}_{rep}", family_id=f'F{i + 1:02d}', source_scene_id=s, C=c, rep=rep, layer_phase=ph, layer_count=4,
                             mask_by_layer_json=mask, retained_bundle_count=nb, retained_brick_count=5 * nb, occupied_layers_eval_only=ns['highest_nonempty_layer'](stt),
                             dome_intensity=dome, start_id=st, task_id=task['task_id'], task_layer_count=MAP[c], depletion_seed=seed,
                             load_center_x_m=20.5, load_center_y_m=13.5, load_yaw_deg=0.0))
with (P / 'family_selection.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(fams[0])); w.writeheader(); [w.writerow(x) for x in fams]
with (P / 'capture_manifest.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); [w.writerow(x) for x in rows]
(P / 'task_registry.json').write_text(json.dumps(registry, indent=1, sort_keys=True))
plan = Path(__file__).resolve().parents[1] / 'reports/le13_ipr_analysis_plan_LOCK_20261115_v01.md'
lock = dict(state='PRELOCK_PASS', amendment='A1: dome = red manifest value (already C-V02-mapped); v01 double-mapped (8420-8640); primary result = v02 decided before v02 capture', version='v02', created='2026-11-15', protocol='docs/LE13_independent_pose_precision_replication_protocol_20261115_v01.md (handoff repo)',
            candidates=len(cand), eligible=len(elig), selected=len(sel), selection_rule='eligible sorted ascending, first 36', excluded_C_V02_families=sorted(used_src & set(cand)),
            families_per_start=dict(collections.Counter(f['start_id'] for f in fams)), captures=len(rows),
            files={n: sha(P / n) for n in ('source_audit.csv', 'family_selection.csv', 'capture_manifest.csv', 'task_registry.json', 'start_cameras.json')},
            analysis_plan=str(plan), analysis_plan_sha256=sha(plan) if plan.exists() else None, code_sha256=sha(__file__),
            frozen=dict(model_lock=str(V / 'MIX_C06_20261112_v01/selection_lock.json'), model_lock_sha256=sha(V / 'MIX_C06_20261112_v01/selection_lock.json'),
                        perception='scripts/c_v02_stage4_perception_task_prior_20261114_v03.py', perception_sha256=sha(Path(__file__).resolve().parents[1] / 'scripts/c_v02_stage4_perception_task_prior_20261114_v03.py'),
                        robust_code_sha256='0b1e5f46702d4af0c4d4abc4b7d1c5fe9d29cc07c9f34b4a1592990ac296ae29', robust_config_sha256='35cf0a78d4c73919ab2a03378341fb90433aeaeeab306a605d064d98a0cfc529'))
(P / 'PRELOCK.json').write_text(json.dumps(lock, indent=1)); print(json.dumps({k: lock[k] for k in ('state', 'candidates', 'eligible', 'selected', 'captures', 'families_per_start', 'analysis_plan_sha256')}))
