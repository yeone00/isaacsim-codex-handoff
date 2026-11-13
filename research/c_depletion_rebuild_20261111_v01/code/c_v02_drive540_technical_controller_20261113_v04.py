"""Technical failures != scientific failures. Gated 15 paired pilots + separate actual-control proof -> main540."""
import json,csv,sys,os,time,fcntl,subprocess,shutil,statistics,traceback,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));sys.path.insert(0,str(R/'scripts'))
from c_depletion_runtime_20261111_v01 import atomic,sha
from c_depletion_integrations_20261112_v06 import notify
from evaluation.c_v02_drive540_technical_gate_20261113_v02 import assess
D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');A=D/'single_load_amendment_v01';T=D/'technical_policy_amendment_v01';E=D/'technical_e2e_v04';E.mkdir(exist_ok=True);lock=open(E/'controller.lock','a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);rows=list(csv.DictReader((A/'attempt_manifest.csv').open()));cap=json.loads((E/'execution_lock.json').read_text());current={};pilots=[];main=[];engineering=None;storage_ready=False;started=time.time();jobs={r['attempt_id']:dict(state='PENDING',attempted=False,planned=True) for r in rows}
def write_jobs():atomic(E/'jobs.json',jobs)
def status(st,reason=None):
 atomic(E/'status.json',dict(state=st,controller_pid=os.getpid(),current=current,pilot_technical_pass=sum(x['assessment']['technical_pass'] for x in pilots),pilot_recorded=len(pilots),pilot_planned=15,pilot_task_success=sum(x['assessment']['task_success'] for x in pilots),engineering_motion_certified=bool(engineering and engineering['assessment']['control_motion_certified']),main_completed=len(main),main_attempted=sum(x['attempted'] for x in jobs.values()),main_success=sum(x['assessment']['task_success'] for x in main),main_scientific_failure=sum(not x['assessment']['task_success'] for x in main),main_planned=540,physical_main_entry='PASS' if len(pilots)==15 and all(x['assessment']['technical_pass'] for x in pilots) and engineering and engineering['assessment']['control_motion_certified'] and storage_ready else 'HOLD',reason=reason,updated=time.time(),elapsed_seconds=time.time()-started))
def verify():
 assert sha(A/'protocol.json')==cap['scientific_protocol_sha256'];assert sha(A/'attempt_manifest.csv')==cap['manifest_sha256'];assert sha(T/'technical_policy.json')==cap['technical_policy_sha256'];assert sha(T/'storage_plan_v01.json')==cap['storage_plan_sha256']
 for p,h in cap['code_sha256'].items():assert sha(p)==h,'CODE_SHA_CHANGED:'+p
 for p,h in cap['inputs_sha256'].items():assert sha(p)==h,'INPUT_SHA_CHANGED:'+p

def record(run,role,row,reused=False):
 result=json.loads((run/'result.json').read_text());assessment=assess(run,engineering=role=='engineering');entry=dict(role=role,attempt_id=row['attempt_id'],run_dir=str(run),reused_verified=reused,result_sha256=sha(run/'result.json'),assessment=assessment)
 ad=E/'assessments';ad.mkdir(exist_ok=True);atomic(ad/(role+'_'+row['attempt_id']+'.json'),entry)
 if role=='main':
  jobs[row['attempt_id']].update(state='COMPLETED_SCIENTIFIC_SUCCESS' if assessment['technical_pass'] and assessment['task_success'] else 'COMPLETED_SCIENTIFIC_FAILURE' if assessment['technical_pass'] else 'HOLD_TECHNICAL_OR_SAFETY',attempted=True,run_dir=str(run),result_sha256=entry['result_sha256'],outcome=result['outcome']);write_jobs()
 assert assessment['technical_pass'],'TECHNICAL_OR_SAFETY_HOLD:'+json.dumps(entry,ensure_ascii=False)[:1800]
 return entry

def run(row,role):
 global current
 verify();key=row['attempt_id'];out=E/role/key
 if (out/'result.json').exists():return record(out,role,row,True)
 assert not out.exists(),'INTERRUPTED_ATTEMPT_REVIEW_REQUIRED:'+str(out)
 storage=json.loads((T/'storage_plan_v01.json').read_text());destination=Path(storage['destination']);uuid=subprocess.check_output(['findmnt','--noheadings','--output','UUID','--target',str(destination)],text=True).strip();assert uuid==storage['volume_uuid'],'STORAGE_UNMOUNTED_OR_WRONG_VOLUME';assert shutil.disk_usage(destination).free>25*1024**3,'DISK_BELOW_25_GIB';inp=E/'input_rows';inp.mkdir(exist_ok=True);rp=inp/(role+'_'+key+'.json');atomic(rp,row)
 # Respect all GPU owners; no other job/process is terminated.
 gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
 cmd=['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_v02_drive540_e2e_runner_20261113_v03.py'),'--run-dir',str(out),'--scenario-row',str(rp),'--representation',row['representation'],'--load','L4','--occlusion','O0','--group','G1','--role',role,'--scene-id',row['source_scene_id'],'--start-xy-yaw='+','.join(str(row[k]) for k in ['start_x_m','start_y_m','start_yaw_deg']),'--cell-id',key,'--record-robotcam']
 if role=='engineering':cmd+=['--engineering-targets',str(T/'engineering_reference_targets.json'),'--engineering-targets-sha',sha(T/'engineering_reference_targets.json')]
 out.parent.mkdir(exist_ok=True);log=E/(role+'_'+key+'.log')
 with log.open('x') as f:
  p=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);current=dict(role=role,attempt_id=key,pid=p.pid,output=str(out),log=str(log));status('RUNNING_'+role.upper())
  if role=='main':jobs[key].update(state='RUNNING',attempted=True,run_dir=str(out),pid=p.pid);write_jobs()
  notify('[IsaacSim] C540 '+role+' started',key+'; scientific failure allowed only when safe termination/evidence verified.')
  while p.poll() is None:status('RUNNING_'+role.upper());time.sleep(10)
 gl.close();assert (out/'result.json').exists(),'MISSING_RESULT:'+str(out);entry=record(out,role,row);current={};return entry

def main_table():
 table=[]
 for C in ['C100','C80','C60','C40','C20']:
  for rep in ['HR_Scan','LR_Scan','GeoCAD']:
   rr=[x for x in main if x['attempt_id'].split('_')[2]==C and rep in x['attempt_id']];n=len(rr);s=sum(x['assessment']['task_success'] for x in rr);lo=hi=None
   if n:
    z=1.959963984540054;p=s/n;mid=(p+z*z/(2*n))/(1+z*z/n);half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n);lo,hi=mid-half,mid+half
   table.append(dict(C=C,representation=rep,planned=36,completed=n,success=s if n else None,scientific_failure=n-s if n else None,success_rate=s/n if n else None,Wilson95_low=lo,Wilson95_high=hi,note='paired36 bases from10 source families; nominal Wilson not cluster independence proof'))
 with (E/'main_condition_results.csv').open('w',newline='') as f:w=csv.DictWriter(f,list(table[0]));w.writeheader();w.writerows(table)
try:
 verify();write_jobs();status('TECHNICAL_PILOT_QUALIFICATION')
 # Reuse all completed immutable technical pilots and actual engineering motion proof, never repeat them.
 previous=Path(cap['reuse_execution_root']);prior=json.loads((previous/'pilot_records.json').read_text());first=next(r for r in rows if r['base_id']=='C2D_B01' and r['C']=='C100' and r['representation']=='HR_Scan')
 for entry in prior:
  row=next(r for r in rows if r['attempt_id']==entry['attempt_id']);pilots.append(record(Path(entry['run_dir']),'pilot',row,True))
 atomic(E/'pilot_records.json',pilots);assert len(pilots)==15 and all(x['assessment']['technical_pass'] for x in pilots)
 engref=json.loads((previous/'engineering_control_record.json').read_text());erow=dict(first);erow['attempt_id']=engref['attempt_id'];engineering=record(Path(engref['run_dir']),'engineering',erow,True);atomic(E/'engineering_control_record.json',engineering);assert engineering['assessment']['control_motion_certified']
 # Motion proof cannot be replaced by the safe no-detection pilots.
 paths=[Path(x['run_dir']) for x in pilots]+[Path(engineering['run_dir'])];sizes=[sum(p.stat().st_size for p in path.rglob('*') if p.is_file()) for path in paths];need=max(sizes)*540+25*1024**3
 storage=json.loads((T/'storage_plan_v01.json').read_text());destination=Path(storage['destination']);approval=Path(storage['approval_file'])
 while True:
  allowed=approval.exists() and json.loads(approval.read_text()).get('approved_by_researcher') is True
  if allowed and destination.exists() and os.access(destination,os.W_OK):
   uuid=subprocess.check_output(['findmnt','--noheadings','--output','UUID','--target',str(destination)],text=True).strip();assert uuid==storage['volume_uuid'],'WRONG_STORAGE_VOLUME'
   if shutil.disk_usage(destination).free>need:break
  status('WAITING_STORAGE_AUTHORIZATION_AND_CAPACITY','Technical and actual-motion gates PASS; needs explicit storage approval, writable dedicated directory and correct volume UUID.');time.sleep(30)
 mainpath=E/'main'
 if not mainpath.exists():mainpath.symlink_to(destination,target_is_directory=True)
 assert mainpath.is_symlink() and mainpath.resolve()==destination.resolve(),'MAIN_STORAGE_MAPPING_MISMATCH'
 proof=destination/'storage_probe.json'
 if not proof.exists():atomic(proof,dict(volume_uuid=uuid,bytes_needed=need,created=time.time(),purpose='new540 evidence only; existing data not modified'))
 storage_ready=True
 atomic(E/'storage_runtime_mapping.json',dict(volume_uuid=uuid,destination=str(destination),logical_manifest_unchanged=True,bytes_required=need,bytes_available=shutil.disk_usage(destination).free,source_storage_plan_sha256=sha(T/'storage_plan_v01.json')))

 atomic(E/'main_entry_certificate.json',dict(state='PASS_TECHNICAL15_PLUS_SEPARATE_MOTION_STOP',scientific_protocol_sha256=cap['scientific_protocol_sha256'],technical_policy_sha256=cap['technical_policy_sha256'],manifest_sha256=cap['manifest_sha256'],pilots=pilots,engineering=engineering,projected_disk_required=need,created=time.time(),GT_operational_input=False))
 notify('[IsaacSim] C540 main starting','15 technical conditions and separate actual motion/stop proof passed. Scientific failures are counted, no retries.')
 for row in rows:
  main.append(run(row,'main'));atomic(E/'main_records.json',main);main_table();status('MAIN_PROGRESS')
 status('COMPLETED540');notify('[IsaacSim] C540 complete','540 scientifically valid outcomes stored. No failures removed; technical incidents separately preserved.')
except BaseException as e:
 status('HOLD',str(e));write_jobs();main_table();atomic(E/'failure.json',dict(reason=str(e),traceback=traceback.format_exc(),current=current,pilots=pilots,engineering=engineering,main=main));notify('[IsaacSim] HOLD C540 technical system',str(e)[:900]+' Logs '+str(E)+' No threshold or model changes/retry.',high=True);raise
