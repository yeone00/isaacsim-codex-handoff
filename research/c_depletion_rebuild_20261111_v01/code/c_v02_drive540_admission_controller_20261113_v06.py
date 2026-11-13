"""Independent GPU-exclusive actual stationary qualifications; HOLD before any unvalidated motion."""
import sys,json,time,os,subprocess,fcntl,csv,hashlib,traceback
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from c_depletion_runtime_20261111_v01 import atomic,sha
from c_depletion_integrations_20261112_v06 import notify
D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');lock=open(D/'controller.lock','a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);protocol=json.loads((D/'protocol.json').read_text());assert sha(D/'protocol.json')==(D/'protocol.sha256').read_text().strip();rows=list(csv.DictReader((D/'single_load_amendment_v01/attempt_manifest.csv').open()));current={};completed=[]
def state(st,reason=None):atomic(D/'pipeline_status.json',dict(state=st,controller_pid=os.getpid(),current=current,completed_stationary_qualifications=completed,main_completed=0,main_planned=540,physical_gate='HOLD',reason=reason,updated=time.time()))
try:
 for C in ['C100','C80','C60','C40','C20']:
  for rep in ['HR_Scan','LR_Scan','GeoCAD']:
   row=next(r for r in rows if r['base_id']=='C2D_B01' and r['C']==C and r['representation']==rep);key=C+'_'+rep;job=D/'stationary_qualification_attempt06'/key;job.parent.mkdir(exist_ok=True);rp=job/'result.json'
   if rp.exists():
    assert json.loads(rp.read_text())['state']=='STATIONARY_PHYSICS_PASS','PREVIOUS_FAILED_QUALIFICATION_REVIEW_REQUIRED:'+key
    completed.append(key);continue
   assert not job.exists(),'INTERRUPTED_JOB_REVIEW_REQUIRED:'+key
   rowpath=D/'stationary_qualification_attempt06'/(key+'.input.json');atomic(rowpath,row)
   gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
   env=dict(os.environ,ROS_DOMAIN_ID='191',ROS_DISTRO='jazzy',RMW_IMPLEMENTATION='rmw_fastrtps_cpp',PYTHONUNBUFFERED='1');env.pop('PYTHONPATH',None);env['LD_LIBRARY_PATH']=env.get('LD_LIBRARY_PATH','')+':/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim/exts/isaacsim.ros2.bridge/jazzy/lib'
   cmd=['/home/user/anaconda3/envs/hh_isaac51/bin/python',str(R/'scripts/c_v02_drive540_physical_admission_20261113_v06.py'),'--row',str(rowpath),'--output',str(job)]
   log=D/'logs'/(key+'_attempt06.log')
   with log.open('x') as f:
    p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,cwd=R,env=env);current=dict(job=key,pid=p.pid,log=str(log),command=cmd);state('RUNNING_STATIONARY_PHYSICS');notify('[IsaacSim] C-V02 540 qualification',key+' actual Kit/PhysX stationary test started. Main runs remain HOLD.')
    while p.poll() is None:
     state('RUNNING_STATIONARY_PHYSICS');time.sleep(10)
   gl.close();assert rp.exists(),'MISSING_QUALIFICATION_RESULT:'+key;result=json.loads(rp.read_text());assert p.returncode==0 and result['state']=='STATIONARY_PHYSICS_PASS','QUALIFICATION_HOLD:'+key+' '+str(result.get('checks',result.get('traceback')))
   completed.append(key);current={};state('STATIONARY_QUALIFICATION_PROGRESS')
 state('HOLD_FULL_E2E_PILOT_REQUIRED','Stationary qualifications complete. Full E2E adapter/control/GT/video admission must be validated before main540.');notify('[IsaacSim] HOLD C-V02 540','Stationary15 qualifications completed; physical main not started; full E2E technical pilot gate remains. '+str(D))
except BaseException as e:
 state('HOLD',str(e));atomic(D/'controller_failure.json',dict(reason=str(e),traceback=traceback.format_exc(),current=current,main_started=0));notify('[IsaacSim] HOLD C-V02 540',str(e)[:650]+' Log '+str(current.get('log'))+' Automatic retry: no, preserved failed evidence.');raise
