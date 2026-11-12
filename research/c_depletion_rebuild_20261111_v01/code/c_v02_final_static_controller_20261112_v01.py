"""Reuse V01 Test occlusion data; add only new C100 Test occlusions; selected and synthetic baseline."""
import json,csv,subprocess,fcntl,os,time,shutil
from pathlib import Path
import numpy as np
from PIL import Image
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,locked
from c_depletion_integrations_20261112_v06 import notify
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';E=V/'execution_v01';O=V/'final_static_pipeline_v01';O.mkdir(exist_ok=True);S=V/'MIX_C06_20261112_v01/selection_lock.json';sel=json.loads(S.read_text());frames=json.loads((B/'execution_v02/static_frame_index.json').read_text());assert len(frames)==1890;catalog={(x['rep'],x['scene_id']):x for x in json.loads((E/'capture_index.json').read_text())};test=[r for r in csv.DictReader((V/'data_design_v01/additional_C100_manifest.csv').open()) if r['split']=='test'];assert len(test)==40
# Existing frames are immutable reused references; never relabel old observations as new.
for f in frames:
 for p in [f['rgb'],f['depth'],f['camera'],*f['canonical_masks']]:assert Path(p).is_file()
def run(key,cmd,out,gpu=False):
 result=Path(out)/'result.json'
 if result.exists():assert json.loads(result.read_text())['state'] in ['PASS_CAPTURE','PASS','COMPLETED'];return
 assert not Path(out).exists(),'INTERRUPTED_REQUIRES_REVIEW:'+key
 gl=None
 if gpu:gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
 with (O/(key+'.log')).open('x') as f:
  p=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);event(B,'STAGE_STARTED',job='V02_'+key)
  while p.poll() is None:atomic(O/'status.json',dict(state='RUNNING',job=key,pid=p.pid,updated=time.time(),physical_motion=False));time.sleep(10)
 if gl:gl.close()
 assert p.returncode==0 and result.exists(),'STAGE_FAILED:'+key
 assert json.loads(result.read_text())['state'] in ['PASS_CAPTURE','PASS','COMPLETED'];event(B,'STAGE_COMPLETED',job='V02_'+key)
try:
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  for i in [0,20]:
   key=f'C100_TEST_OCCLUSION_{rep}_{i}';out=O/'occlusion'/key;out.parent.mkdir(exist_ok=True);mp=O/(key+'.csv')
   if not mp.exists():
    with mp.open('x',newline='') as f:w=csv.DictWriter(f,list(test[0]));w.writeheader();w.writerows(test[i:i+20])
   run(key,['/home/user/anaconda3/envs/hh_isaac51/bin/python',str(R/'scripts/c_v02_C100_occlusion_capture_20261112_v01.py'),'--anchor-audit',str(B/'asset_anchor_audit_v01/asset_anchor_audit.json'),'--design',str(V/'data_design_v01'),'--manifest',str(mp),'--rep',rep,'--output',str(out)],out,True)
   for row in test[i:i+20]:
    sid=row['scene_id'];rec=json.loads((out/'complete'/f'{sid}.json').read_text());basecp=Path(catalog[rep,sid]['complete']);old=json.loads(basecp.read_text());base=basecp.parents[1]
    for name,h in rec['files_sha256'].items():assert sha(name)==h
    assert json.loads((base/'camera'/f'{sid}.json').read_text())['calibration']['T_world_optical']==json.loads((out/'camera'/f'{sid}.json').read_text())['calibration']['T_world_optical']
    paths=[str(base/'masks_canonical'/f'{sid}_Load_{lid:02d}.png') for lid in range(1,int(row['load_count'])+1)]
    for lid,p in enumerate(paths,1):assert np.array_equal(np.array(Image.open(p)),np.array(Image.open(out/'masks_canonical'/f'{sid}_Load_{lid:02d}.png')))
    common=dict(rep=rep,scene_id=sid,C='C100',family_id=row['family_id'],GT_eval_only_target=old['GT_eval_only']['target'])
    frames.append(dict(**common,O='O0',rgb=str(base/'rgb'/f'{sid}.png'),depth=str(base/'depth'/f'{sid}.npy'),camera=str(base/'camera'/f'{sid}.json'),canonical_masks=paths,panel=None,measured_occlusion=0.))
    for oc in ['O25','O50']:
     z=rec['occlusion'][oc];assert z['achieved'] and z['actual_same_frame_panel'];target=np.array(Image.open(paths[0]))>0;panel=np.array(Image.open(z['panel']))>0;coverage=float((target&panel).sum()/target.sum());assert abs(coverage-z['measured'])<1e-12 and abs(coverage-z['nominal'])<=.02
     for lid,mp in enumerate(z['canonical_visible_masks']):assert np.array_equal(np.array(Image.open(mp))>0,(np.array(Image.open(paths[lid]))>0)&~panel)
     frames.append(dict(**common,O=oc,rgb=z['rgb'],depth=z['depth'],camera=z['camera'],canonical_masks=z['canonical_visible_masks'],panel=z['panel'],measured_occlusion=z['measured']))
 assert len(frames)==2250 and len({(f['rep'],f['scene_id'],f['O']) for f in frames})==2250
 for f in frames:assert f['scene_id'].startswith('CDEP_B1R_TST_')
 atomic(O/'static_frame_index.json',frames)
 for role,models in [('selected_mixture',sel['models']),('synthetic_baseline',sel['baseline_models'])]:
  root=V/(role+'_eval_v01');root.mkdir(exist_ok=True)
  atomic(root/'static_frame_index.json',frames);atomic(root/'final_C_models_lock.json',dict(status='LOCKED',models=models,selection_sha256=sha(S),role=role))
  if role=='synthetic_baseline' and [m['sha256'] for m in models]==[m['sha256'] for m in sel['models']]:
   atomic(root/'verified_reuse.json',dict(state='SKIPPED_VERIFIED',source=str(V/'selected_mixture_eval_v01'),reason='identical selected and baseline checkpoints; no duplicate inference'));continue
  run(role+'_perception',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'analysis/c_v02_perception_eval_20261112_v01.py'),'--root',str(root),'--output',str(root/'perception_eval_v01')],root/'perception_eval_v01',True)
  run(role+'_pose',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'analysis/c_v02_pose_eval_20261112_v01.py'),'--root',str(root),'--output',str(root/'pose_eval_v01')],root/'pose_eval_v01')
  assert not json.loads((root/'pose_eval_v01/result.json').read_text())['pipeline_errors']
 run('V02_integrated_report',['/usr/bin/python3',str(R/'analysis/c_v02_integrated_report_20261112_v01.py')],V/'integrated_report_v01')
 atomic(O/'result.json',dict(state='COMPLETED',Test_frames=2250,reused_V01_frames=1890,new_C100_occluded_frames=240,physical_motion=False,physical_stages='HOLD'))
except BaseException as ex:event(B,'HOLD',reason='V02 static '+str(ex));notify('[IsaacSim] C-V02 static HOLD',str(ex)+' root='+str(O),True);raise
