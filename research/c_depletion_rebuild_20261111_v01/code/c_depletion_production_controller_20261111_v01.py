"""Approved static C pipeline, independent of Codex. Physical pilot/450 drives have no launch path."""
import argparse,csv,json,sys,time,os,subprocess,fcntl,shutil
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,locked,proc_alive
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();O=a.root;B=O.parent;D=B/'data_design_v01';lock=locked('/tmp/c_depletion_static_execution.lock')
p=json.loads((O/'production_authorization_v01.json').read_text());assert p['data_training_static_authorized'] and not p['physical_motion_authorized']
for path,h in p['code_sha256'].items():assert sha(path)==h,path
J=O/'production_jobs.json';jobs=json.loads(J.read_text()) if J.exists() else {};catalog={};manifest=list(csv.DictReader((D/'scene_manifest.csv').open()));started=time.time();current={}
def status(state,stage,reason=None):
 summary=dict(state=state,stage=stage,controller_pid=os.getpid(),current=current,reason=reason,updated=time.time(),generated_RGBD=len(catalog),declared_RGBD=4410,completed_jobs=sum(j['state']=='COMPLETED' for j in jobs.values()),failed_jobs=sum(j['state']=='FAILED' for j in jobs.values()),physical_motion_authorized=False,physical_runs_started=0,elapsed_seconds=time.time()-started)
 h=O/'C_COMMON_HPO_v01/hpo_status.json'
 if h.exists():summary['C_HPO']=json.loads(h.read_text())
 atomic(O/'production_status.json',summary);atomic(J,jobs)
def verify_records(output,expected_count=None):
 result=Path(output)/'result.json';d=json.loads(result.read_text());assert d['state']=='PASS_CAPTURE'
 rr=[]
 for q in sorted((Path(output)/'complete').glob('*.json')):
  r=json.loads(q.read_text());assert r['state']=='PASS_CAPTURE'
  for name,h in r['files_sha256'].items():assert sha(name)==h,name
  assert r['calibration_check'] and r['mask_count_check'] and r['nominal_slot_support']
  rr.append(dict(rep=r['rep'],scene_id=r['scene_id'],complete=str(q)))
 assert len(rr)==d['completed']==d['declared']
 if expected_count is not None:assert len(rr)==expected_count
 return rr
def run(key,cmd,out,kind='CPU'):
 global current
 old=jobs.get(key)
 if old:
  if old['state']=='COMPLETED':
   assert sha(old['result_file'])==old['result_sha256'];return old
  if proc_alive(old.get('pid')):raise RuntimeError('WORKER_STILL_ALIVE:'+key)
  old['state']='INTERRUPTED' if old['state']=='RUNNING' else old['state'];atomic(J,jobs);raise RuntimeError('HOLD_PREVIOUS_ATTEMPT_REQUIRES_REVIEW:'+key)
 if shutil.disk_usage(O).free<25*1024**3:raise RuntimeError('DISK_BELOW_25_GIB')
 gpu=None
 if kind=='CAPTURE':gpu=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gpu,fcntl.LOCK_EX|fcntl.LOCK_NB)
 with (O/'logs'/f'{key}.log').open('x') as log:
  child=subprocess.Popen(cmd,cwd=R,stdout=log,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONUNBUFFERED='1'))
  jobs[key]=dict(state='RUNNING',pid=child.pid,command=cmd,output=str(out),started=time.time(),attempt=1,kind=kind);current=dict(job=key,pid=child.pid,output=str(out),log=str(O/'logs'/f'{key}.log'));status('RUNNING',key);event(B,'STAGE_STARTED',job=key,pid=child.pid)
  while child.poll() is None:time.sleep(10);status('RUNNING',key)
 if gpu:gpu.close()
 jobs[key].update(exit_code=child.returncode,ended=time.time())
 if child.returncode!=0:jobs[key]['state']='FAILED';status('HOLD',key,'WORKER_EXIT_NONZERO');raise RuntimeError('WORKER_FAILED:'+key)
 result=Path(out)/('hpo_status.json' if kind=='HPO' else 'result.json')
 assert result.exists(),'MISSING_RESULT:'+str(result)
 d=json.loads(result.read_text());assert d['state'] in ['PASS_CAPTURE','PASS','COMPLETED'],'RESULT_NOT_VERIFIED:'+str(d.get('state'))
 jobs[key].update(state='COMPLETED',result_file=str(result),result_sha256=sha(result));current={};status('RUNNING',key);event(B,'STAGE_COMPLETED',job=key)
 return jobs[key]
try:
 assert json.loads((O/'pilot_done_v02.json').read_text())['state']=='COMPLETED'
 assert json.loads((O/'pilot_QA_v02/result.json').read_text())['state']=='PASS'
 # Reuse the 15 exact pilot captures in their predeclared train family, no duplicate render.
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  for r in verify_records(O/f'pilot_{rep}_v02',5):catalog[r['rep'],r['scene_id']]=r
 for family in sorted({r['family_id'] for r in manifest}):
  for rep in ['HR_Scan','LR_Scan','GeoCAD']:
   rr=[r for r in manifest if r['family_id']==family and (rep,r['scene_id']) not in catalog]
   if not rr:continue
   key='capture_'+family+'_'+rep;out=O/'production'/key
   if key in jobs and jobs[key]['state']=='COMPLETED':
    for x in verify_records(out):catalog[x['rep'],x['scene_id']]=x
    continue
   mf=O/'job_manifests'/f'{key}.csv';mf.parent.mkdir(exist_ok=True)
   with mf.open('x',newline='') as f:w=csv.DictWriter(f,list(rr[0]));w.writeheader();w.writerows(rr)
   cmd=['/home/user/anaconda3/envs/hh_isaac51/bin/python',str(R/'scripts/c_depletion_rgbd_capture_20261111_v02.py'),'--anchor-audit',str(B/'asset_anchor_audit_v01/asset_anchor_audit.json'),'--design',str(D),'--manifest',str(mf),'--rep',rep,'--output',str(out)]
   out.parent.mkdir(exist_ok=True);run(key,cmd,out,'CAPTURE')
   for x in verify_records(out,len(rr)):catalog[x['rep'],x['scene_id']]=x
   atomic(O/'capture_index.json',list(catalog.values()));status('RUNNING','C_DATASET_PRODUCTION')
 assert len(catalog)==4410;atomic(O/'capture_index.json',list(catalog.values()))
 run('C_DATASET_QA_PACKAGE',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_depletion_dataset_QA_package_20261111_v01.py'),'--root',str(O)],O/'dataset_QA_v01')
 dl=json.loads((O/'dataset_lock.json').read_text());assert dl['status']=='LOCKED'
 H=O/'C_COMMON_HPO_v01'
 if not H.exists():
  prepare=['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_common_hpo_prepare_20261111_v01.py'),'--root',str(H)]
  with (O/'logs/C_HPO_prepare.log').open('x') as log:ret=subprocess.run(prepare,cwd=R,stdout=log,stderr=subprocess.STDOUT)
  assert ret.returncode==0,'C_HPO_PREPARE_FAILED'
 hsha=sha(H/'protocol.json')
 run('C_COMMON_HPO',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_common_hpo_controller_20261111_v01.py'),'--root',str(H),'--protocol-sha',hsha],H,'HPO')
 # Static post-HPO workers must have a separate reviewed immutable capability lock.
 cap=O/'static_evaluation_capabilities_v01.json'
 if not cap.exists():raise RuntimeError('HOLD_STATIC_EVALUATION_ADAPTERS_NOT_REGISTERED')
 spec=json.loads(cap.read_text());assert spec['physical_motion_authorized'] is False
 for name,h in spec['code_sha256'].items():assert sha(name)==h
 for j in spec['jobs']:run(j['id'],j['command'],Path(j['output']),j.get('kind','CPU'))
 status('HOLD_PHYSICAL_STAGES','STATIC_STAGES_COMPLETED','Success rule, ROBUST_A validation and physical entry gates must be finalized; 300+150 not launched.');event(B,'HOLD',reason='Static stages completed; physical pilot/450 drives remain prohibited pending gates')
except BaseException as ex:
 for j in jobs.values():
  if j['state']=='RUNNING' and not proc_alive(j.get('pid')):j['state']='FAILED'
 status('HOLD',current.get('job','C_PIPELINE'),str(ex));event(B,'HOLD',job=current.get('job','C_PIPELINE'),reason=str(ex));raise
