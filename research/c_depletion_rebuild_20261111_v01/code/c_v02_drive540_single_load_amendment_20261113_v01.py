"""Researcher-approved single-target amendment; preserves original540 manifest/protocol."""
import pathlib,csv,json,hashlib,time,collections
R=pathlib.Path(__file__).resolve().parents[1];D=pathlib.Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
A=D/'single_load_amendment_v01';A.mkdir(exist_ok=False);rows=list(csv.DictReader((D/'attempt_manifest.csv').open()))
for r in rows:r.update(load_count=1,pallet_count=1,target_instance='Load_01',target_semantics='unique placed approach target; not inference-selected identity',target_selection_accuracy_primary=False)
p=A/'attempt_manifest.csv'
with p.open('x',newline='') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
pairs=collections.defaultdict(list)
for r in rows:pairs[(r['base_id'],r['C'])].append(r)
assert len(rows)==540 and len(pairs)==180
for rr in pairs.values():
 assert {r['representation'] for r in rr}=={'HR_Scan','LR_Scan','GeoCAD'}
 assert len({(r['start_x_m'],r['start_y_m'],r['start_yaw_deg'],r['task_layer_count'],r['trajectory_id'],r['source_family']) for r in rr})==1
assert all(n==36 for n in collections.Counter((r['C'],r['representation']) for r in rows).values())
protocol=json.loads((D/'protocol.json').read_text());protocol.update(schema='C_V02_DRIVE540_SINGLE_LOAD_O0_amendment_v01',parent_protocol_sha256=sha(D/'protocol.json'),parent_manifest_sha256=sha(D/'attempt_manifest.csv'),load_count=1,pallet_count=1,target_instance='Load_01',target_identity_definition='sole scene-placed approach target; first generated ID is not nearest/selected object',primary_metrics=['single_load_detection','instance_mask_quality','RGBD_pose_computation_and_error','path_plan_success','physical_approach_alignment_success','final_XY_yaw_error','stage_failure_and_task_success'],excluded_primary_metrics=['multi_load_target_selection_accuracy'],prediction_mask_rule='highest-confidence operational detection among duplicate/false masks; incorrect mask classified as detection/segmentation/pose failure',static_multi_load_results_unchanged=True,static_OTHER_LOAD_is_auxiliary_only=True,main_entry='HOLD_UNTIL_SINGLE_LOAD_PHYSICS_SAFETY_AND_E2E_PILOTS_PASS',attempt_manifest=str(p),attempt_manifest_sha256=sha(p),created=time.time())
(A/'protocol.json').write_text(json.dumps(protocol,indent=2,ensure_ascii=False));(A/'protocol.sha256').write_text(sha(A/'protocol.json')+'\n');(A/'manifest_QA.json').write_text(json.dumps(dict(state='PASS_MANIFEST_ONLY',attempts=540,paired_base_C=180,cells=15,per_cell=36,source_families=10,load_count=1,pallet_count=1,GT_operational_input=False,actual_loaded_PhysX='HOLD_CRASH_UNRESOLVED',main_started=0),indent=2))
(D/'active_physical_protocol.json').write_text(json.dumps(dict(protocol=str(A/'protocol.json'),sha256=sha(A/'protocol.json'),manifest=str(p),manifest_sha256=sha(p),main_entry='HOLD',main_started=0),indent=2))
s=(R/'evaluation/c_v02_drive540_scene_20261113_v02.py').read_text().replace("TARGET='/World/CV02DriveTarget'","TARGET='/World/CV02DriveScene/Load_01'")
s=s.replace("g=json.loads", "assert int(row.get('load_count',1))==1 and int(row.get('pallet_count',1))==1\n g=json.loads")
s=s.replace("construction=dict(actual_bricks=count,", "construction=dict(load_count=1,pallet_count=1,target_instance='Load_01',actual_bricks=count,")
(R/'evaluation/c_v02_drive540_scene_20261113_v03.py').write_text(s)
print(json.dumps(dict(root=str(A),protocol_sha256=sha(A/'protocol.json'),manifest_sha256=sha(p))))
