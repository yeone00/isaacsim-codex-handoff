"""C-V02 DRIVE540 E1-based start redesign: manifest DRAFT generator (v01, 2026-11-14). CPU only, no simulation.
Reads the locked single-load attempt manifest (sha-verified, never modified) and the start-candidate TC-S robustness table
(reports/c_v02_start_and_camera_validation_20261113_v01/start_candidates_tcs_robustness.csv). Keeps every row's load scene,
representation, C, task, checkpoint and lighting; replaces only the start pose with one of the admitted E1-grid starts
(3.2 m to centre, lateral {0,+-3 cm} x heading {86,90,94} deg, minus combinations not robust to +-3 cm pose error).
Start assignment is per base_id (so HR/LR/CAD and all C of a base share the start): start = admitted[(base_index) mod n].
Writes a NEW directory only. Correction B is not used (group G1 = ROBUST_A only)."""
import csv, json, hashlib, sys, collections
from pathlib import Path
R = Path(__file__).resolve().parents[1]
D = Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01')
A = D / 'single_load_amendment_v01'; OLD = A / 'attempt_manifest.csv'; OLD_SHA = '92ba7c2909f78110d4fa985de17ce6863538b0110dfb3e42a7e7784f05ce19fc'
CAND = R / 'reports/c_v02_start_and_camera_validation_20261113_v01/start_candidates_tcs_robustness.csv'
DUP = Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/data_design_v01/shape_duplicates.json')
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=False)
NEW_ROOT = '/home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_E1_20261114_v01/main'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(OLD) == OLD_SHA, 'locked manifest sha mismatch'
rows = list(csv.DictReader(open(OLD))); assert len(rows) == 540
CENTRE_X, CENTRE_Y = -25.888, 30.509
cand = list(csv.DictReader(open(CAND))); grid = [c for c in cand if float(c['start_to_centre_m']) == 3.2]; assert len(grid) == 9
admitted = [c for c in grid if c['nominal_admitted'] == 'True' and c['robust_all_pm3cm'] == 'True']
excluded = [c for c in grid if c not in admitted]
# E1 first, then the remaining admitted starts in table order
admitted.sort(key=lambda c: (not (float(c['lateral_m']) == 0 and float(c['heading_deg']) == 90),))
starts = [dict(start_id=f"S{i}", lateral_m=float(c['lateral_m']), heading_deg=float(c['heading_deg']), start_x_m=round(CENTRE_X + float(c['lateral_m']), 3),
               start_y_m=round(CENTRE_Y - 3.2, 3), nominal_peak_k=float(c['nominal_min_peak_k']), curvature_margin_frac=float(c['curvature_margin_frac']),
               robust_lateral_err_range_cm=c['robust_lateral_err_range_cm'], robust_pm5cm=c['robust_all_pm5cm'] == 'True') for i, c in enumerate(admitted)]
assert starts[0]['lateral_m'] == 0 and starts[0]['heading_deg'] == 90 and starts[0]['start_x_m'] == -25.888 and starts[0]['start_y_m'] == 27.309
bases = sorted({r['base_id'] for r in rows}); smap = {b: starts[i % len(starts)] for i, b in enumerate(bases)}
new = []
for r in rows:
    s = smap[r['base_id']]; n = dict(r)
    n.update(attempt_id=r['attempt_id'].replace('C2D_', 'C2E_', 1), start_x_m=f"{s['start_x_m']:.3f}", start_y_m=f"{s['start_y_m']:.3f}", start_yaw_deg=f"{s['heading_deg']:.1f}",
             output=f"{NEW_ROOT}/{r['attempt_id'].replace('C2D_', 'C2E_', 1)}", start_id=s['start_id'], start_lateral_m=s['lateral_m'], group='G1', pose_method='ROBUST_A',
             correction_b='off', source_attempt_id=r['attempt_id'])
    new.append(n)
with open(OUT / 'attempt_manifest_E1_draft.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, list(new[0])); w.writeheader(); w.writerows(new)
# QA
dup = json.loads(DUP.read_text()); grp = {m['scene_id']: i for i, g in enumerate(dup) for m in g['members']}
key = lambda r: (r['source_scene_id'], r['start_x_m'], r['start_yaw_deg'], r['representation'])
c = collections.Counter(key(r) for r in new)
geo = collections.Counter((grp.get(r['source_scene_id'], r['source_scene_id']), r['source_family'], r['start_x_m'], r['start_yaw_deg'], r['representation']) for r in new)
per_C = {}
for C in ['C100', 'C80', 'C60', 'C40', 'C20']:
    rc = [r for r in new if r['C'] == C]
    per_C[C] = dict(rows=len(rc), distinct_scene_ids=len({r['source_scene_id'] for r in rc}), distinct_geometries=len({grp.get(r['source_scene_id'], r['source_scene_id']) for r in rc}),
                    distinct_lighting_families=len({r['source_family'] for r in rc}), distinct_starts=len({(r['start_x_m'], r['start_yaw_deg']) for r in rc}))
pair_ok = all(len({(r['start_x_m'], r['start_yaw_deg']) for r in new if r['base_id'] == b}) == 1 for b in bases)
rep_pair = all(sorted(r['representation'] for r in new if r['base_id'] == b and r['C'] == C) == ['GeoCAD', 'HR_Scan', 'LR_Scan'] for b in bases for C in per_C)
qa = dict(schema='C540_E1_MANIFEST_DRAFT_QA_v01', locked_manifest=str(OLD), locked_manifest_sha256=OLD_SHA, locked_manifest_unchanged=sha(OLD) == OLD_SHA,
          candidate_table=str(CAND), candidate_table_sha256=sha(CAND), rows=len(new), bases=len(bases), starts_admitted=starts,
          starts_excluded=[dict(lateral_m=float(x['lateral_m']), heading_deg=float(x['heading_deg']), nominal_admitted=x['nominal_admitted'], robust_pm3cm=x['robust_all_pm3cm'],
                                curvature_margin_frac=float(x['curvature_margin_frac']), robust_lateral_err_range_cm=x['robust_lateral_err_range_cm'], reason='TC-S not robust to +-3 cm pose error') for x in excluded],
          bases_per_start=dict(collections.Counter(smap[b]['start_id'] for b in bases)), exact_duplicate_conditions=sum(v - 1 for v in c.values()),
          duplicate_geometry_lighting_start_rep=sum(v - 1 for v in geo.values()), per_C=per_C, start_shared_within_base=pair_ok, three_reps_per_base_C=rep_pair,
          correction_b='off (G1 ROBUST_A only)', changed_fields=['attempt_id', 'start_x_m', 'start_y_m', 'start_yaw_deg', 'output'], added_fields=['start_id', 'start_lateral_m', 'group', 'pose_method', 'correction_b', 'source_attempt_id'],
          manifest_sha256=sha(OUT / 'attempt_manifest_E1_draft.csv'), status='DRAFT_NOT_APPROVED_NOT_EXECUTABLE_BY_CONTROLLER_V04')
(OUT / 'manifest_draft_QA.json').write_text(json.dumps(qa, indent=1))
print(json.dumps({k: qa[k] for k in ['rows', 'bases', 'bases_per_start', 'exact_duplicate_conditions', 'duplicate_geometry_lighting_start_rep', 'per_C', 'start_shared_within_base', 'three_reps_per_base_C', 'manifest_sha256']}, indent=1))
