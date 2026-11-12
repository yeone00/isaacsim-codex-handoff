"""CPU contract + frozen-source datum-prefix tests. No GT oracle or new inference."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='1'
import sys,json,ast,hashlib
from pathlib import Path
import numpy as np,cv2
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from evaluation import c_v02_task_layer_prior_20261112_v02 as task
from evaluation import b5_robust_20261110_v01 as rb
V=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01');O=V/'task_layer_policy_v01';unit=[]
for n in [1,2,3,4]:
 t=dict(schema='C_V02_TASK_LAYER_PRIOR_v01',task_id='unit'+str(n),task_layer_count=n,provider='operator_or_task_management_system');assert task.validate_task(t)==n;calls=[];old=rb.estimate_pose
 def fake(mask,depth,camera,layer_count,**kw):calls.append(layer_count);return dict(status='UNIT_FAKE',pose=None)
 rb.estimate_pose=fake
 try:assert task.estimate(None,None,'{}',t)['task_metadata']==t and calls==[n]
 finally:rb.estimate_pose=old
 out=task.estimate(None,np.zeros((480,640),np.float32),'{}',t);assert out['status']=='NO_DETECTION';unit.append(dict(layer_count=n,forwarding_exact=True,frozen_no_detection_smoke=out['status']))
for bad in [0,5,True,'4']:
 try:task.validate_task(dict(schema='C_V02_TASK_LAYER_PRIOR_v01',task_id='bad',task_layer_count=bad,provider='operator_or_task_management_system'))
 except ValueError:pass
 else:raise AssertionError('invalid layer accepted')
t=dict(schema='C_V02_TASK_LAYER_PRIOR_v01',task_id='badGT',task_layer_count=4,provider='operator_or_task_management_system',GT_pose=[0,0,0])
try:task.validate_task(t)
except ValueError:pass
else:raise AssertionError('GT metadata accepted')
try:
 with task.deny_evaluation_GT_reads():open('/tmp/eval_gt_only/forbidden.json')
except PermissionError:pass
else:raise AssertionError('GT read not blocked')
# Execute the actual unchanged source prefix through datum decision only; no copied formula or pose-success claim.
source=task.ROBUST_CODE.read_text();tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_estimate_single');prefix=[]
for node in fn.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='zz' for t in node.targets):break
 prefix.append(node)
probe=ast.FunctionDef(name='datum_probe',args=fn.args,body=prefix+[ast.Return(value=ast.Name(id='diag',ctx=ast.Load()))],decorator_list=[]);mod=ast.fix_missing_locations(ast.Module(body=[probe],type_ignores=[]));cfg=json.loads(task.FROZEN.read_text())['config'];cases=[]
for n in [1,2,3,4]:
 for floor in [None,0.]:
  world=np.zeros((25,40,3));world[:,:,2]=.144+n*.09;mask=np.ones((25,40),bool);ns=dict(np=np,cv2=cv2,SIDE_H=.09,PALLET_H=.144,depth_gap_cluster=lambda m,*args:m,sensed_floor_z=lambda *args:(floor,'UNIT_FLOOR' if floor is not None else 'UNIT_NO_FLOOR'))
  exec(compile(mod,str(task.ROBUST_CODE),'exec'),ns);d=ns['datum_probe'](mask,np.ones(mask.shape),{},None,n,cfg,world=world,valid=mask);assert abs(d['pallet_top_m']-.144)<1e-9;cases.append(dict(layer_count=n,floor_observed=floor is not None,diag=d))
# Sparse top visibility counterexample: correct4 prior, fewer than1% top-layer points, no floor.
world=np.zeros((25,40,3));world[:,:,2]=.144+3*.09;world[0,0,2]=.144+4*.09;ns=dict(np=np,cv2=cv2,SIDE_H=.09,PALLET_H=.144,depth_gap_cluster=lambda m,*args:m,sensed_floor_z=lambda *args:(None,'UNIT_NO_FLOOR'));exec(compile(mod,str(task.ROBUST_CODE),'exec'),ns);risk=ns['datum_probe'](mask,np.ones(mask.shape),{},None,4,cfg,world=world,valid=mask);assert abs(risk['pallet_top_m']-.054)<1e-9
result=dict(state='PASS_CONTRACT_AND_FROZEN_PREFIX_TESTS',layer_forwarding=unit,datum_prefix_cases=cases,sparse_top_no_floor_structural_risk=risk,structural_risk_is_NOT_real_RGBD_success_or_failure=True,GT_key_rejection=True,GT_read_guard=True,actual_C_O_performance='PENDING selected model RGBD',robust_original_sha256=task.sha(task.ROBUST_CODE),frozen_config_sha256=task.CONFIG_SHA,GT_oracle_masks_used=False,GPU_used=False)
(O/'unit_smoke_results_v02.json').write_text(json.dumps(result,indent=2));print('1..4 forwarding/no-detection,8datum cases,GT separation PASS; sparse top/no-floor risk demonstrated')
