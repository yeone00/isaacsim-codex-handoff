"""Build operator task metadata separately from evaluation GT. No start pose/FINAL/slot fields."""
from pathlib import Path
import json,csv,hashlib,time,collections
R=Path(__file__).resolve().parents[1];import sys;sys.path.insert(0,str(R))
from evaluation.c_v02_task_layer_prior_20261112_v01 import MAPPING,ROBUST_SHA,CONFIG_SHA,validate_task
V=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01');O=V/'task_layer_policy_v01';O.mkdir(exist_ok=False);rows=[r for r in csv.DictReader((V/'data_design_v01/scene_manifest.csv').open()) if r['split']=='test'];tasks=[];op={}
for r in rows:
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  for oc in ['O0','O25','O50']:
   key='|'.join([r['scene_id'],rep,oc]);tid=hashlib.sha256(key.encode()).hexdigest()[:24];t=dict(schema='C_V02_TASK_LAYER_PRIOR_v01',task_id=tid,task_layer_count=MAPPING[r['C']],provider='operator_or_task_management_system');validate_task(t);tasks.append(dict(scene_id=r['scene_id'],representation=rep,occlusion=oc,task_id=tid,task_layer_count=t['task_layer_count']));op[tid]=t
assert len(tasks)==2250
with (O/'static_task_manifest.csv').open('x',newline='') as f:w=csv.DictWriter(f,list(tasks[0]));w.writeheader();w.writerows(tasks)
(O/'operator_metadata.json').write_text(json.dumps(op,indent=2))
# Physical metadata proposal only: source family matched, start pose/collider/controller gates unresolved.
plan=[]
for r in rows:
 if r['C']=='C100' and r['observation_id']!='OBS00':continue
 if r['C']!='C100' and r['trajectory_id']!='T01':continue
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  for oc in ['O0','O25','O50']:plan.append(dict(source_scene_id=r['scene_id'],base_family_id=r['family_id'],rep=rep,O=oc,task_layer_count=MAPPING[r['C']],physical_entry='HOLD',physical_start_pose='UNRESOLVED'))
assert len(plan)==450
with (O/'physical_task_plan_DRAFT.csv').open('x',newline='') as f:w=csv.DictWriter(f,list(plan[0]));w.writeheader();w.writerows(plan)
policy=dict(status='LOCKED_TASK_PRIOR_CONTRACT',created=time.time(),mapping=MAPPING,meaning='occupied remaining layers supplied in advance by operator/task management, not sensor inferred',allowed_operational_prior='task_layer_count only',GT_pose_mask_slots_footprint_FINAL_forbidden=True,ROBUST_A_formula_unchanged=True,robust_code_sha256=ROBUST_SHA,robust_config_sha256=CONFIG_SHA,task_success=dict(XY_m=.11,yaw_deg=7.341774,collision_safety_violation=False),arrival_certification=dict(PRE_FINAL_position_m=.005,PRE_FINAL_yaw_deg=2),speed_safety_stop_mps=.03,physical_motion_authorized=False,physical_scene_start_positions_not_locked=True,Test_for_model_ratio_selection=False,priorless_static_methods='retained as separately labelled diagnostic baselines',static_performance='PENDING final frozen model predictions',actual_loaded_physical_stage_audit='UNKNOWN/PENDING; no new drive stage loaded')
(O/'policy.json').write_text(json.dumps(policy,indent=2));print('task prior2250 +physicalDRAFT450 metadata locked')
