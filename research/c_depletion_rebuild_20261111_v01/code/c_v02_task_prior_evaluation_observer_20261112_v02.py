"""Append approved-prior baseline after existing static jobs, without changing running controllers/training.
Operational child never receives evaluation GT; parent scoring reads separate eval_gt_only after child exit.
"""
import json,time,csv,os,sys,subprocess,hashlib,collections,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from scripts.c_depletion_runtime_20261111_v01 import atomic,event,sha,locked
from scripts.c_depletion_integrations_20261112_v06 import notify
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';O=V/'task_layer_policy_v01';lock=locked(O/'observer.lock');start=time.time();policy=json.loads((O/'policy.json').read_text());taskrows=list(csv.DictReader((O/'static_task_manifest.csv').open()));tm={(r['scene_id'],r['representation'],r['occlusion']):r['task_id'] for r in taskrows};operator=json.loads((O/'operator_metadata.json').read_text())
while not (V/'final_static_pipeline_v01/result.json').exists():
 atomic(O/'observer_status.json',dict(state='WAITING_FINAL_FROZEN_MODEL_STATIC',pid=os.getpid(),updated=time.time(),physical_motion=False));time.sleep(60)
assert json.loads((V/'final_static_pipeline_v01/result.json').read_text())['state']=='COMPLETED';assert json.loads((V/'MIX_C06_20261112_v01/selection_lock.json').read_text())['status']=='LOCKED';rows=[]
try:
 for role in ['selected_mixture','synthetic_baseline']:
  root=V/(role+'_eval_v01')
  if (root/'verified_reuse.json').exists():
   atomic(O/(role+'_reuse.json'),dict(state='SKIPPED_VERIFIED',source='selected_mixture',reason='same frozen model SHA'));continue
  inputs=json.loads((root/'perception_eval_v01/pose_inputs.json').read_text());ops=[];gt=[];assert len(inputs)==6750
  for x in inputs:
   f=x['frame'];tid=tm[f['scene_id'],x['model_rep'],f['O']];task=operator[tid]
   ops.append(dict(task=task,depth=f['depth'],camera=f['camera'],predicted_mask=x['mask'],checkpoint_sha256=x['checkpoint_sha256'],prediction_available=x['top1_conf'] is not None))
   gt.append(dict(GT_pose=f['GT_eval_only_target'],rep=x['model_rep'],seed=x['seed'],C=x['C'],O=x['O'],family_id=f['family_id'],scene_id=f['scene_id'],task_id=tid,target_selected=x['top1_class']=='TARGET'))
  opfile=O/(role+'_operational_view.json');atomic(opfile,ops);gp=O/'eval_gt_only'/(role+'.json');gp.parent.mkdir(exist_ok=True);atomic(gp,gt)
  out=O/(role+'_operational_results_v01')
  if not (out/'result.json').exists():
   assert not out.exists(),'INTERRUPTED_OPERATIONAL_EVALUATION_REVIEW_REQUIRED'
   with (O/(role+'_operational_worker.log')).open('x') as log:
    cmd=['/usr/bin/taskset','-c','47','/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_v02_task_prior_pose_worker_20261112_v02.py'),'--operational-view',str(opfile),'--output',str(out)];p=subprocess.Popen(cmd,cwd=R,stdout=log,stderr=subprocess.STDOUT,env=dict(os.environ,OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'))
    event(B,'STAGE_STARTED',job='V02_TASK_PRIOR_'+role)
    while p.poll() is None:atomic(O/'observer_status.json',dict(state='RUNNING_TASK_PRIOR_RGBD_EVALUATION',role=role,pid=os.getpid(),worker_pid=p.pid,updated=time.time(),physical_motion=False));time.sleep(10)
   assert p.returncode==0,'OPERATIONAL_WORKER_FAILED'
  output=[json.loads(x) for x in (out/'operational_results.jsonl').read_text().splitlines()];assert len(output)==len(ops)==len(gt)
  # Only now evaluation GT is consumed to calculate errors; no scoring field is present in child input schema.
  scoring=json.loads(gp.read_text())
  for pred,g in zip(output,scoring):
   assert pred['task_id']==g['task_id'];r=pred['result'];pose=r.get('pose');diag=r.get('diag',{});target=g['GT_pose'];dx=pose['center_x_m']-target['center_x_m'] if pose else None;dy=pose['center_y_m']-target['center_y_m'] if pose else None;a=math.radians(target['yaw_deg']);heading=pose.get('heading_deg_180') if pose else None
   rows.append(dict(role=role,rep=g['rep'],seed=g['seed'],C=g['C'],O=g['O'],scene_id=g['scene_id'],family_id=g['family_id'],task_layer_count=pred['task_layer_count'],target_selected=g['target_selected'],computed=bool(pose),designated_target_computed=bool(pose and g['target_selected']),status=r['status'],reason=r.get('reason'),datum=pose.get('datum') if pose else diag.get('datum'),floor_status=diag.get('floor_status'),q99_load_top=diag.get('load_top_sensed_m'),XY_error_m=math.hypot(dx,dy) if pose else None,long_error_m=dx*math.cos(a)+dy*math.sin(a) if pose else None,lat_error_m=-dx*math.sin(a)+dy*math.cos(a) if pose else None,yaw_error_deg=abs((heading-target['yaw_deg']+90)%180-90) if heading is not None else None,GT_operational_input=False,approved_task_prior=True))
  assert not any(r['status']=='PIPELINE_ERROR' for r in rows if r['role']==role),'PIPELINE_ERROR_HOLD'
  event(B,'STAGE_COMPLETED',job='V02_TASK_PRIOR_'+role)
 with (O/'RGBD_task_prior_per_attempt.csv').open('x',newline='') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for key in sorted({(r['role'],r['rep'],r['C'],r['O']) for r in rows}):
  rr=[r for r in rows if (r['role'],r['rep'],r['C'],r['O'])==key];ok=[r for r in rr if r['designated_target_computed']];z=dict(zip(['role','rep','C','O'],key));z.update(attempts=len(rr),independent_families=len({r['family_id'] for r in rr}),computed=sum(r['computed'] for r in rr),target_computed=len(ok),datum_counts=dict(collections.Counter(r['datum'] for r in rr)),failure_counts=dict(collections.Counter(r['reason'] for r in rr if not r['computed'])))
  for metric in ['XY_error_m','long_error_m','lat_error_m','yaw_error_deg']:
   a=[r[metric] for r in ok if r[metric] is not None];z[metric+'_mean']=float(np.mean(a)) if a else None;z[metric+'_median']=float(np.median(a)) if a else None;z[metric+'_p90']=float(np.percentile(a,90)) if a else None
  summary.append(z)
 atomic(O/'RGBD_task_prior_summary.json',summary);atomic(O/'RGBD_task_prior_result.json',dict(state='COMPLETED',attempts=len(rows),C_states=5,occlusion_conditions=3,GT_pose_mask_slots_operational=False,task_layer_prior=True,physical_motion=False,physical_entry='HOLD'))
 report=R/'reports/c_v02_ROBUST_A_task_layer_RGBD_results_20261112_v01.md';report.write_text('# C-V02 known occupied-layer ROBUST_A RGB-D results\n\n'+json.dumps(summary,indent=2,ensure_ascii=False)+'\n\n조건:작업관리자가4/4/3/2/1층수를제공. 정답pose/mask/slots미사용;동결ROBUSTA수식/QA/성공기준불변. 실제loaded-Cstage/collider/접촉gate미완료로물리HOLD. 실패를성공처리하거나GT슬롯으로수정하지않음. 기존nominal4/센서높이추정baseline은별도원본결과.\n');notify('[IsaacSim] C-V02 task-layer pose completed','Known task-layer ROBUST_A evaluated. Physical HOLD pending loaded-stage collider/contact checks. '+str(O));atomic(O/'observer_status.json',dict(state='COMPLETED_PHYSICAL_HOLD',pid=os.getpid(),updated=time.time()))
except BaseException as ex:atomic(O/'observer_status.json',dict(state='HOLD',reason=str(ex),updated=time.time()));event(B,'HOLD',reason='Task-layer prior '+str(ex));notify('[IsaacSim] C-V02 task prior HOLD',str(ex)+' logs='+str(O),True);raise
