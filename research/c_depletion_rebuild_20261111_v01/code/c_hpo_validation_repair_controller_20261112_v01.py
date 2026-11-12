"""Independent evaluation-only recovery. Original failed attempts and 57 training artifacts untouched."""
import json,os,time,sys,subprocess,fcntl,traceback,statistics,hashlib
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,locked
from c_depletion_integrations_20261112_v06 import notify
E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');H=E/'C_COMMON_HPO_v02';O=E/'validation_repair_v01';B=E.parent;PY='/home/user/anaconda3/envs/sdg_tools/bin/python';lock=locked('/tmp/c_depletion_static_execution.lock');spec=json.loads((O/'authorization_v01.json').read_text())
for p,h in spec['code_sha256'].items():assert sha(p)==h,p
original=json.loads((H/'jobs.json').read_text());sel=json.loads((H/'selection_lock.json').read_text());cid=sel['candidate_id'];inventory=json.loads((O/'training_inventory_before.json').read_text());jobs={};current={};start=time.time()
def verify_weights():
 for r in inventory:assert sha(r['checkpoint'])==r['sha256'],'ORIGINAL_CHECKPOINT_CHANGED'
def status(state,stage,reason=None):
 d=dict(state=state,stage=stage,current=current,controller_pid=os.getpid(),updated=time.time(),training_complete=57,original_crossval_failures=24,completed_evaluations=sum(j['state']=='COMPLETED' for j in jobs.values()),reason=reason,physical_motion_authorized=False,physical_runs=0)
 atomic(O/'recovery_status.json',d);atomic(O/'repair_jobs.json',jobs)
 hp=json.loads((O/'HPO_recovered_status.json').read_text()) if (O/'HPO_recovered_status.json').exists() else dict(state=state,current=current,completed_training_jobs=57,job_counts=dict(COMPLETED=sum(j['state']=='COMPLETED' for j in jobs.values()),FAILED=sum(j['state']=='FAILED' for j in jobs.values())),recovery_root=str(O),original_failed_attempts_preserved=24)
 atomic(E/'production_status.json',dict(state=state,stage=stage,controller_pid=os.getpid(),current=current,reason=reason,updated=time.time(),generated_RGBD=4410,declared_RGBD=4410,physical_motion_authorized=False,physical_runs_started=0,C_HPO=hp,original_HPO_status_preserved=str(H/'hpo_status.json')))
def evaluate(key,source,target,seed,limit=0,existing=None):
 global current
 phase='full' if seed==42 else 'baseline_control' if source[0]==0 else 'final';j=original[f'{phase}_C{source[0]:02d}_{source[1]}_s{seed}'];b=j['best'];out=Path(existing) if existing else O/'runs'/key;out.parent.mkdir(exist_ok=True)
 if (out/'result.json').exists():
  z=json.loads((out/'result.json').read_text());assert z['state']=='COMPLETED' and z['checkpoint_sha256']==b['sha256'] and z['validation_rep']==target and z['images']==(limit or 210)
  jobs[key]=dict(state='COMPLETED',output=str(out),result_sha256=sha(out/'result.json'),reused_verified=True);return z
 assert not out.exists(),'INTERRUPTED_ATTEMPT_REQUIRES_REVIEW:'+key
 log=O/(key+'.log');gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
 cmd=[PY,str(R/'scripts/c_hpo_validation_repair_worker_20261112_v01.py'),'--checkpoint',b['checkpoint'],'--checkpoint-sha',b['sha256'],'--rep',target,'--output',str(out)]
 if limit:cmd+=['--limit',str(limit)]
 with log.open('x') as f:
  child=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);current=dict(job=key,pid=child.pid,output=str(out),log=str(log));jobs[key]=dict(state='RUNNING',command=cmd,checkpoint_sha256=b['sha256'],pid=child.pid,output=str(out));status('RUNNING','VALIDATION_REPAIR')
  while child.poll() is None:time.sleep(5);status('RUNNING','VALIDATION_REPAIR')
 gl.close();assert child.returncode==0,'EVALUATION_FAILED:'+key+' log='+str(log)
 z=json.loads((out/'result.json').read_text());assert z['state']=='COMPLETED' and z['checkpoint_sha256']==b['sha256'] and not z['Test_used'];jobs[key].update(state='COMPLETED',result_sha256=sha(out/'result.json'));current={};return z
try:
 verify_weights();event(B,'STAGE_STARTED',job='VALIDATION_REPAIR',reason=str(O))
 reps=['HR_Scan','LR_Scan','GeoCAD'];qualification=[]
 for i,rep in enumerate(reps):
  one=evaluate('smoke_'+rep+'_own_1',(cid,rep),rep,42,12,existing=O/'smoke_HR_own_a01' if rep=='HR_Scan' else None);two=evaluate('smoke_'+rep+'_own_2',(cid,rep),rep,42,12)
  assert one['mask_map5095']==two['mask_map5095'] and one['box_map5095']==two['box_map5095'],'NONDETERMINISTIC_REPEAT'
  cross=evaluate('smoke_'+rep+'_to_'+reps[(i+1)%3],(cid,rep),reps[(i+1)%3],42,12)
  qualification.append(dict(rep=rep,same_checkpoint_repeat_exact=True,own=one,cross=cross))
 # Full own-val comparison uses checkpoint-native metrics, never changes frozen epoch-based selection.
 own=[]
 for rep in reps:
  z=evaluate('own_full_'+rep,(cid,rep),rep,42,existing=O/'own_HR_full_a01' if rep=='HR_Scan' else None);ref=original[f'full_C{cid:02d}_{rep}_s42']['mask_map5095'];own.append(dict(rep=rep,training_epoch_metric=ref,checkpoint_revalidation_metric=z['mask_map5095'],difference=z['mask_map5095']-ref,checkpoint=z['checkpoint'],checkpoint_sha256=z['checkpoint_sha256']))
 atomic(O/'qualification.json',dict(state='PASS_CHECKPOINT_REPRODUCTION_AND_BITMAP_CONTRACT',cases=qualification,own_full_comparison=own,epoch_exact_reproduction='Not claimed: saved EMA is FP16, training validation used FP32 EMA under autocast. Original precision provenance and metric differences preserved; no threshold/selection change.',test_access=False))
 recovered=[]
 for key,j in original.items():
  if j['kind']!='crossval':continue
  if j['state']=='COMPLETED':
   p=Path(j['output'])/'result.json';z=json.loads(p.read_text());assert sha(j['checkpoint'])==j['checkpoint_sha256'];recovered.append(dict(original_job=key,reused=True,result=z));continue
  z=evaluate('repair_'+key,(j['candidate_id'],j['source_rep']),j['rep'],j['seed']);recovered.append(dict(original_job=key,original_attempt_state=j['state'],repaired=True,result=z))
 assert len(recovered)==24 and all(r['result']['state']=='COMPLETED' for r in recovered)
 verify_weights();assert json.loads((H/'selection_lock.json').read_text())==sel
 summary=dict(state='COMPLETED',training_jobs=57,validated_original_checkpoints=57,original_crossval_failed_attempts_preserved=24,crossval_completed=24,selection=sel,selection_changed=False,crossval_is_secondary_not_selection=True,own_full_comparison=own,original_summary=json.loads((H/'final_summary.json').read_text()),recovered_crossval=recovered,test_used_for_selection=False,checkpoint_files_unchanged=True)
 atomic(O/'final_summary.json',summary);atomic(O/'HPO_recovered_status.json',dict(state='COMPLETED',controller_pid=os.getpid(),completed_training_jobs=57,crossval_completed=24,current={},recovery_root=str(O),original_failed_attempts_preserved=24,selection=sel,updated=time.time()))
 event(B,'STAGE_COMPLETED',job='C_HPO_VALIDATION_RECOVERED',reason=str(O));notify('[IsaacSim] C-HPO validation recovered','57 trainings preserved; cross-validation 24/24 verified; static evaluation starts next. Logs: '+str(O)+'; physical HOLD.')
 out=E/'post_hpo_static_recovered_v01';cmd=[PY,str(R/'scripts/c_depletion_post_hpo_static_20261112_v03.py'),'--root',str(E),'--output',str(out)]
 with (O/'post_static.log').open('x') as f:
  child=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);current=dict(job='C_STATIC_AFTER_VALIDATION_REPAIR',pid=child.pid,output=str(out),log=str(O/'post_static.log'))
  while child.poll() is None:status('RUNNING','C_STATIC_AFTER_VALIDATION_REPAIR');time.sleep(10)
 assert child.returncode==0,'STATIC_EVALUATION_FAILED:'+str(O/'post_static.log')
 status('HOLD_PHYSICAL_STAGES','STATIC_STAGES_COMPLETED','Physical success/datum/safety gates unresolved');event(B,'HOLD',reason='Static completed; physical HOLD')
except BaseException as ex:
 if current and current.get('job') in jobs:jobs[current['job']]['state']='FAILED'
 status('HOLD',current.get('job','VALIDATION_REPAIR'),str(ex));event(B,'HOLD',reason='Evaluation recovery: '+str(ex)+'; logs='+str(O));notify('[IsaacSim] Evaluation recovery HOLD',str(ex)+'; logs='+str(O),True);raise
