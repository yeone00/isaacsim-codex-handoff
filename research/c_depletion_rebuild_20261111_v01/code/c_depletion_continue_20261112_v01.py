"""Resume verified C bitmap pipeline, preserve failed polygon attempt. No physical launch."""
import json,os,sys,time,subprocess,fcntl,traceback
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,locked
E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');B=E.parent;H=E/'C_COMMON_HPO_v02';lock=locked('/tmp/c_depletion_static_execution.lock');started=time.time()
spec=json.loads((E/'bitmap_execution_amendment_v01.json').read_text())
for p,h in spec['code_sha256'].items():assert sha(p)==h,p
assert not spec['physical_motion_authorized']
current={}
def status(state,stage,reason=None):
 d=dict(state=state,stage=stage,controller_pid=os.getpid(),current=current,reason=reason,updated=time.time(),generated_RGBD=4410,declared_RGBD=4410,completed_jobs=210,failed_jobs=1,prior_failure_preserved='C_DATASET_QA_PACKAGE',physical_motion_authorized=False,physical_runs_started=0,elapsed_seconds=time.time()-started)
 if (H/'hpo_status.json').exists():d['C_HPO']=json.loads((H/'hpo_status.json').read_text())
 atomic(E/'production_status.json',d)
def run(key,cmd,out,result):
 global current
 marker=E/(key+'_completion_v01.json')
 if marker.exists():
  m=json.loads(marker.read_text());assert sha(result)==m['result_sha256'];return
 log=E/'logs'/(key+'_attempt_v01.log');assert not log.exists(),'INTERRUPTED_ATTEMPT_REVIEW_REQUIRED'
 with log.open('x') as f:
  child=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONUNBUFFERED='1'));current=dict(job=key,pid=child.pid,output=str(out),log=str(log));event(B,'STAGE_STARTED',job=key,pid=child.pid)
  while child.poll() is None:status('RUNNING',key);time.sleep(10)
 assert child.returncode==0,'WORKER_EXIT_'+str(child.returncode)
 d=json.loads(result.read_text());assert d['state']=='COMPLETED',d.get('state');atomic(marker,dict(state='COMPLETED',result_file=str(result),result_sha256=sha(result)));event(B,'STAGE_COMPLETED',job=key);current={}
try:
 assert json.loads((E/'dataset_QA_bitmap_v01/result.json').read_text())['state']=='PASS'
 assert json.loads((E/'bitmap_qualification_v01/CPU_result.json').read_text())['state']=='PASS'
 assert json.loads((E/'bitmap_qualification_v01/dataset_CPU_result.json').read_text())['state']=='PASS'
 # Prepared lock verifies every train/val bitmap as well as image and bookkeeping bbox.
 ph=sha(H/'protocol.json');run('C_COMMON_HPO_BITMAP',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_common_hpo_controller_20261112_v03.py'),'--root',str(H),'--protocol-sha',ph],H,H/'hpo_status.json')
 out=E/'post_hpo_static_bitmap_v01';run('C_STATIC_AFTER_HPO_BITMAP',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_depletion_post_hpo_static_20261112_v02.py'),'--root',str(E),'--output',str(out)],out,out/'result.json')
 status('HOLD_PHYSICAL_STAGES','STATIC_STAGES_COMPLETED','Physical success/site datum/safety gates unresolved; zero physical runs');event(B,'HOLD',reason='Static completed; physical pilot/300/150 remain HOLD')
except BaseException as ex:
 status('HOLD',current.get('job','BITMAP_CONTINUATION'),str(ex));event(B,'HOLD',job=current.get('job','BITMAP_CONTINUATION'),reason=str(ex));raise
