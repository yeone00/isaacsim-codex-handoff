"""Independent CPU preparation controller; after gates it remains HOLD and never starts new GPU work."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,locked,protocol,proc_alive
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();O=a.root;p=protocol(O);lock=locked(O/'controller.lock');global_lock=locked('/tmp/c_depletion_rebuild_controller.lock')
jobs=json.loads((O/'jobs.json').read_text()) if (O/'jobs.json').exists() else {};start=time.time()
def status(state,current=None,reason=None):
 atomic(O/'pipeline_status.json',dict(state=state,updated=time.time(),controller_pid=os.getpid(),watchdog_pid=(json.loads((O/'watchdog_status.json').read_text()).get('pid') if (O/'watchdog_status.json').exists() else None),current=current,reason=reason,completed=[k for k,j in jobs.items() if j['state'] in ['COMPLETED','SKIPPED_VERIFIED']],pending_stages=['C_dataset','C_training_evaluation','C_pose_ROBUST_A_validation','technical_pilot','main_300'],scope='PREPARATION_ONLY',new_gpu_jobs_started=0,soft_budget_hours=48,stop_at_budget=False,elapsed_seconds=time.time()-start))
try:
 event(O,'CONTROLLER_STARTED',pid=os.getpid(),scope='PREPARATION_ONLY');status('RUNNING')
 for job in ['stage0_existing_evidence','preparation_document_gates']:
  old=jobs.get(job)
  if old and old['state'] in ['COMPLETED','SKIPPED_VERIFIED']:
   result=Path(old['output'])/'result.json';assert sha(result)==old['result_sha256'] and json.loads(result.read_text())['state']=='COMPLETED'
   old['state']='SKIPPED_VERIFIED';atomic(O/'jobs.json',jobs);event(O,'JOB_SKIPPED_VERIFIED',job=job);continue
  if old:
   if proc_alive(old.get('pid')):raise RuntimeError('PREVIOUS_WORKER_ALIVE')
   old['state']='INTERRUPTED';atomic(O/'jobs.json',jobs);raise RuntimeError('INTERRUPTED_REQUIRES_REVIEW_NO_AUTORETRY')
  out=O/'jobs'/f'{job}_a01';cmd=[sys.executable,str(R/'scripts/c_depletion_stage_runner_20261111_v01.py'),'--root',str(O),'--job',job,'--output',str(out)]
  with (O/'logs'/f'{job}_a01.log').open('x') as f:
   child=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,cwd=R)
   jobs[job]=dict(state='RUNNING',pid=child.pid,output=str(out),command=cmd,started=time.time(),attempt=1);atomic(O/'jobs.json',jobs);status('RUNNING',job);event(O,'STAGE_STARTED',job=job,pid=child.pid)
   while child.poll() is None:time.sleep(2);status('RUNNING',job)
  q=out/'result.json';assert child.returncode==0 and q.is_file() and json.loads(q.read_text())['state']=='COMPLETED'
  jobs[job].update(state='COMPLETED',result_sha256=sha(q),ended=time.time());atomic(O/'jobs.json',jobs);event(O,'STAGE_COMPLETED',job=job)
 gates=json.loads((O/'research_gates.json').read_text());event(O,'HOLD',reason='NEW_GPU_NOT_AUTHORIZED_AND_UNRESOLVED_RESEARCH_GATES',gates=gates)
 while True:status('HOLD',reason='Preparation verified; new render/training/drive forbidden by latest instruction; success threshold and C geometry/GT/pose gates unresolved.');time.sleep(30)
except BaseException as e:
 event(O,'CONTROLLER_ERROR',error=type(e).__name__,detail=str(e));status('HOLD',reason=str(e));raise
