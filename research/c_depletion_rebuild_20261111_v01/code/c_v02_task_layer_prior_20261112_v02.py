"""Approved operator occupied-layer prior only. Frozen ROBUST_A mathematics/config unchanged."""
import json,hashlib,builtins,io,contextlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ROBUST_CODE=R/'evaluation/b5_robust_20261110_v01.py';ROBUST_SHA='0b1e5f46702d4af0c4d4abc4b7d1c5fe9d29cc07c9f34b4a1592990ac296ae29'
FROZEN=Path('/home/user/hh/isaac_cosmos/sdg_final/B5_ROBUST_20261110_v01_run01/frozen_config.json');CONFIG_SHA='35cf0a78d4c73919ab2a03378341fb90433aeaeeab306a605d064d98a0cfc529'
MAPPING={'C100':4,'C80':4,'C60':3,'C40':2,'C20':1};TASK_KEYS={'schema','task_id','task_layer_count','provider'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate_task(task):
 if set(task)!=TASK_KEYS or task['schema']!='C_V02_TASK_LAYER_PRIOR_v01':raise ValueError('TASK_METADATA_SCHEMA_REJECTED')
 if type(task['task_layer_count']) is not int or task['task_layer_count'] not in [1,2,3,4]:raise ValueError('TASK_LAYER_COUNT_OUTSIDE_1_TO_4')
 if task['provider']!='operator_or_task_management_system':raise ValueError('UNAPPROVED_PRIOR_PROVIDER')
 return task['task_layer_count']
@contextlib.contextmanager
def deny_evaluation_GT_reads():
 oldopen,oldio=builtins.open,io.open;opened=[]
 def guard(fn):
  def wrapped(file,*a,**kw):
   if isinstance(file,(str,Path)):
    path=str(file);low=path.lower();mode=str(a[0] if a else kw.get('mode','r'))
    if 'r' in mode or '+' in mode:
     if any(x in low for x in ['/eval_gt_only/','/masks_canonical/','/evaluation_gt/','/ground_truth/','/canonical_gt/','/complete/','pose_inputs.json','static_frame_index.json','scene_manifest.csv','retention','removal_history']):raise PermissionError('EVALUATION_GT_FILE_ACCESS_DENIED:'+path)
     opened.append(path)
   return fn(file,*a,**kw)
  return wrapped
 builtins.open,io.open=guard(oldopen),guard(oldio)
 try:yield opened
 finally:builtins.open,io.open=oldopen,oldio

def estimate(mask,depth,camera_metadata,task):
 layer=validate_task(task);assert sha(ROBUST_CODE)==ROBUST_SHA,'FROZEN_ROBUST_A_CODE_CHANGED'
 from evaluation import b5_robust_20261110_v01 as rb
 cfgfile=json.loads(FROZEN.read_text());cfg=cfgfile['config'];assert cfgfile['estimator_code_sha256']==ROBUST_SHA and cfgfile['config_sha256']==CONFIG_SHA and rb.config_sha(dict(rb.DEFAULT_CONFIG,**cfg))==CONFIG_SHA
 with deny_evaluation_GT_reads() as reads:
  out=rb.estimate_pose(mask,depth,camera_metadata,layer,config=cfg,return_diag=True)
 out['task_metadata']=dict(task);out['task_prior_is_known_occupied_layer_count']=True;out['GT_pose_mask_slots_used']=False;out['operational_read_audit']=reads;out['robust_code_sha256']=ROBUST_SHA;out['robust_frozen_config_sha256']=CONFIG_SHA;out['variant']='ROBUST_A_FROZEN_TASK_LAYER_PRIOR_C_V02_v01'
 return out
