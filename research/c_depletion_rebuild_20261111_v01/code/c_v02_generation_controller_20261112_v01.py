"""Protect old generation, build C100 V02; only reviewed capability jobs may follow."""
import json,csv,time,os,subprocess,fcntl
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,locked
from c_depletion_integrations_20261112_v06 import notify
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';E=V/'execution_v01';OLD=B/'execution_v02';D=V/'data_design_v01';lock=locked(V/'controller.lock');jobs={};catalog=json.loads((OLD/'capture_index.json').read_text());current={}
def status(st,stage,reason=None):
 d=dict(state=st,stage=stage,current=current,controller_pid=os.getpid(),updated=time.time(),total_RGBD=5250,verified_RGBD=len(catalog),new_C100_RGBD=max(0,len(catalog)-4410),physical_motion_authorized=False,reason=reason);atomic(V/'pipeline_status.json',d);atomic(V/'jobs.json',jobs)
def run(key,cmd,out,gpu=False):
 global current
 result=Path(out)/'result.json'
 if result.exists():
  d=json.loads(result.read_text());assert d['state'] in ['PASS','PASS_CAPTURE','COMPLETED'];return
 assert not Path(out).exists(),'INTERRUPTED_REVIEW_REQUIRED:'+key
 gl=None
 if gpu:gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
 log=E/'logs'/f'{key}.log'
 with log.open('x') as f:
  p=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONUNBUFFERED='1'));current=dict(job=key,pid=p.pid,log=str(log),output=str(out));jobs[key]=dict(state='RUNNING',command=cmd,pid=p.pid);event(B,'STAGE_STARTED',job='V02_'+key)
  while p.poll() is None:status('RUNNING',key);time.sleep(5)
 if gl:gl.close()
 assert p.returncode==0 and result.exists(),'WORKER_FAILED:'+key+' '+str(log)
 assert json.loads(result.read_text())['state'] in ['PASS','PASS_CAPTURE','COMPLETED'];jobs[key].update(state='COMPLETED',result_sha256=sha(result));current={};event(B,'STAGE_COMPLETED',job='V02_'+key)
try:
 # Wait until original final capture exits and guard acquires GPU; no old worker is signalled.
 while json.loads((V/'boundary_guard_status.json').read_text())['state']!='GPU_BOUNDARY_RESERVED':status('WAITING','OLD_OCCLUSION_GENERATION');time.sleep(2)
 caps=list((OLD/'test_occlusion_v01').glob('*/result.json'));assert len(caps)==30 and all(json.loads(p.read_text())['state']=='PASS_CAPTURE' for p in caps)
 # Allow old parent to finish camera/GT QA and hit the reserved GPU boundary.
 while not (OLD/'static_frame_index.json').exists():status('WAITING','OLD_OCCLUSION_QA');time.sleep(2)
 assert len(json.loads((OLD/'static_frame_index.json').read_text()))==1890
 while json.loads((OLD/'validation_repair_v01/recovery_status.json').read_text())['state']!='HOLD':status('WAITING','OLD_EVALUATION_BOUNDARY_HOLD');time.sleep(2)
 atomic(V/'release_boundary_guard.json',dict(reason='V02 owns subsequent GPU queue',time=time.time()))
 while json.loads((V/'boundary_guard_status.json').read_text())['state']!='RELEASED_TO_V02_CONTROLLER':time.sleep(1)
 event(B,'STAGE_COMPLETED',job='V02_ORDER_HANDOFF',reason='30 old batches completed/QA; old perception blocked without kill')
 rows=list(csv.DictReader((D/'additional_C100_manifest.csv').open()))
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  for i in range(0,len(rows),20):
   rr=rows[i:i+20];key=f'C100_{rep}_{i:03d}';out=E/'capture'/key;out.parent.mkdir(exist_ok=True);mp=E/(key+'.csv')
   if not mp.exists():
    with mp.open('x',newline='') as f:w=csv.DictWriter(f,list(rr[0]));w.writeheader();w.writerows(rr)
   run(key,['/home/user/anaconda3/envs/hh_isaac51/bin/python',str(R/'scripts/c_v02_C100_capture_20261112_v01.py'),'--anchor-audit',str(B/'asset_anchor_audit_v01/asset_anchor_audit.json'),'--design',str(D),'--manifest',str(mp),'--rep',rep,'--output',str(out)],out,True)
   for p in sorted((out/'complete').glob('*.json')):
    rec=json.loads(p.read_text());assert rec['state']=='PASS_CAPTURE'
    for path,h in rec['files_sha256'].items():assert sha(path)==h
    x=dict(rep=rep,scene_id=rec['scene_id'],complete=str(p))
    if not any(q['rep']==rep and q['scene_id']==rec['scene_id'] for q in catalog):catalog.append(x)
   atomic(E/'capture_index.json',catalog)
 assert len(catalog)==5250
 run('C_V02_QA',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_v02_QA_package_20261112_v01.py'),'--root',str(E)],E/'dataset_QA_bitmap_v01')
 # Additional exact correspondence/duplicates QA must pass before training.
 cap=V/'approved_training_capabilities_v01.json';assert cap.exists(),'HOLD_TRAINING_CAPABILITY_NOT_READY';spec=json.loads(cap.read_text());assert not spec['physical_motion_authorized']
 for p,h in spec['code_sha256'].items():assert sha(p)==h,p
 for j in spec['jobs']:run(j['id'],j['command'],Path(j['output']),j.get('gpu_lock',False))
 status('HOLD_PHYSICAL_STAGES','APPROVED_STATIC_STAGES_COMPLETED');event(B,'HOLD',reason='V02 approved static stages complete; physical HOLD')
except BaseException as ex:
 status('HOLD',current.get('job','V02'),str(ex));event(B,'HOLD',reason='V02 '+str(ex)+'; root='+str(V));notify('[IsaacSim] C-V02 HOLD',str(ex)+'; root='+str(V),True);raise
