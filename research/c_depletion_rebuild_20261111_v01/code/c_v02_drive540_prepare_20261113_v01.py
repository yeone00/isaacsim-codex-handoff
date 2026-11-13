"""New O0-only 540 identity lock. No GPU imports or legacy execution."""
import csv,json,hashlib,math,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';O=V/'DRIVE540_20261113_v01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,d):(O/n).write_text(json.dumps(d,indent=2,ensure_ascii=False))
O.mkdir(exist_ok=False);(O/'logs').mkdir();(O/'eval_gt_only').mkdir();(O/'tasks').mkdir()
rows=list(csv.DictReader((V/'data_design_v01/scene_manifest.csv').open()));test=[r for r in rows if r['split']=='test' and r['observation_id']=='OBS00'];families=sorted({r['family_id'] for r in test});assert len(families)==10
sel=json.loads((V/'MIX_C06_20261112_v01/selection_lock.json').read_text());assert sel['status']=='LOCKED' and sel['ratio']=='S075_R025' and not sel['Test_used']
models={m['rep']:m for m in sel['models'] if m['seed']==42};assert len(models)==3
for m in models.values():assert sha(m['checkpoint'])==m['sha256']
reps=['HR_Scan','LR_Scan','GeoCAD'];Cs=['C100','C80','C60','C40','C20'];layers=dict(C100=4,C80=4,C60=3,C40=2,C20=1);bricks=dict(C100=300,C80=240,C60=180,C40=120,C20=60);attempts=[];geo={};bases=[]
# 36 preregistered starts: 4 lateral offsets x3 distances x3 headings.
# Physical background remains the same prepared v30 site; source-family ancestry is NOT 36 independent sites.
for i in range(36):
 base=f'C2D_B{i+1:02d}';family=families[i%10];trajectory=f'T{(i//10)%5+1:02d}';x=-25.888+[-.18,-.06,.06,.18][i%4];dist=[2.8,3.,3.2][(i//4)%3];yaw=[86.,90.,94.][i//12];start=[x,30.509-dist,yaw]
 bases.append(dict(base_id=base,source_family=family,source_split='test',source_trajectory=trajectory,start_x_m=x,start_y_m=start[1],start_yaw_deg=yaw,physical_background_id='v30_03_prepared_site_common',independent_physical_site_count=1,source_family_count=10,variant_index=i//10,environment_note='source Test ancestry retained; physical robot camera/site differ from static capture; no claim of independent site'))
 for ci,C in enumerate(Cs):
  candidates=[r for r in test if r['family_id']==family and r['C']==C and r['trajectory_id']==('FULL' if C=='C100' else trajectory)];assert len(candidates)==1,(base,C);g=candidates[0]
  geo[base+'_'+C]=g
  for ri in range(3):
   rep=reps[(ri+i+ci)%3];aid=f'{base}_{C}_{rep}_O0';tid=hashlib.sha256(aid.encode()).hexdigest()[:24];task=dict(schema='C_V02_TASK_LAYER_PRIOR_v01',task_id=tid,task_layer_count=layers[C],provider='operator_or_task_management_system');dump('tasks/'+aid+'.json',task)
   attempts.append(dict(sequence=len(attempts)+1,attempt_id=aid,base_id=base,representation=rep,C=C,O='O0',source_family=family,source_split='test',source_scene_id=g['scene_id'],trajectory_id=g['trajectory_id'],depletion_seed=g['depletion_seed'],start_x_m=x,start_y_m=start[1],start_yaw_deg=yaw,task_layer_count=layers[C],task_id=tid,task_metadata=str(O/'tasks'/f'{aid}.json'),checkpoint=models[rep]['checkpoint'],checkpoint_sha256=models[rep]['sha256'],model_seed=42,expected_bricks=bricks[C],output=str(O/'main'/aid),physical_background_id='v30_03_prepared_site_common'))
assert len(attempts)==540 and len({a['attempt_id'] for a in attempts})==540
for n,a in [('attempt_manifest.csv',attempts),('base_scenarios.csv',bases)]:
 with (O/n).open('x',newline='') as f:w=csv.DictWriter(f,list(a[0]));w.writeheader();w.writerows(a)
dump('eval_gt_only/scene_construction.json',geo)
# Evaluation construction ledger is only passed to the simulator builder, never the operational perception worker.
model_lock=V/'MIX_C06_20261112_v01/selection_lock.json'
protocol=dict(schema='C_V02_DRIVE540_O0_v01',created=time.time(),representations=reps,C=Cs,occlusion=['O0'],attempts=540,per_cell=36,paired_base_ids=36,source_Test_families=10,physical_background_sites=1,task_layer_count=layers,model_seed=42,model_selection_lock=str(model_lock),model_selection_sha256=sha(model_lock),models=models,perception=dict(imgsz=640,confidence=.25,NMS_IoU=.7,max_det=100,retina_masks=True),pose='unchanged frozen ROBUST_A + supplied occupied task-layer prior',GT_operational_input=False,success=dict(position_m=.11,yaw_deg=7.341774,completed_physical_drive=True,no_collision=True,no_safety_violation=True),arrival_certificate=dict(position_m=.005,yaw_deg=2),speed_safety_stop_mps=.03,physical_execution_authorized_by_researcher=True,gate_bypass_authorized=False,mandatory_gates=['actual_loaded_stage_inventory','registered_PhysX_colliders','wheel_support_and_stationary_contacts','actual_pallet_and_load_geometry','no_external_panel_prim','RGBD_and_model_SHA','path_and_control_safety','HR_C100_full_E2E_pilot','representative_all_C_all_rep_pilots','required_evidence_and_cleanup'],main_entry='HOLD_UNTIL_ALL_GATES_PASS',pilot_denominator=0,retries='no success-until-repeat; previous attempts preserved; safety or infrastructure unresolved => HOLD',supersedes_unexecuted=['300+150','360+180','3C_x_3O_x20'],static_O0_O25_O50_unchanged=True,D600_not_in_scope=True,estimated_main_hours=[72,81],statistics=dict(Wilson_95_per_cell=True,paired_base=True,family_cluster_uncertainty=True,noninferiority_margin=None),scene_distribution=dict(start_lateral_offsets_m=[-.18,-.06,.06,.18],approach_distances_m=[2.8,3.,3.2],start_headings_deg=[86,90,94],lighting='source Test recipe intensity shared across representations',background='prepared v30 common physical environment, not independent36environments',obstacles='original physical site obstacles preserved; legacy load collider replaced separately with C geometry'),inputs_sha256={str(V/'data_design_v01/scene_manifest.csv'):sha(V/'data_design_v01/scene_manifest.csv'),str(O/'attempt_manifest.csv'):sha(O/'attempt_manifest.csv'),str(O/'base_scenarios.csv'):sha(O/'base_scenarios.csv'),str(O/'eval_gt_only/scene_construction.json'):sha(O/'eval_gt_only/scene_construction.json')})
dump('protocol.json',protocol);(O/'protocol.sha256').write_text(sha(O/'protocol.json')+'\n');dump('pipeline_status.json',dict(state='PREPARING_PHYSICAL_ADMISSION',main_started=0,main_planned=540,physical_gate='HOLD',protocol_sha256=sha(O/'protocol.json')))
print(json.dumps(dict(root=str(O),attempts=540,protocol_sha256=sha(O/'protocol.json'))))
