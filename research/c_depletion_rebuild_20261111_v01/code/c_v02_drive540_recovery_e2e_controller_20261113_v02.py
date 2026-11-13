"""Independent gated actual Full E2E pilots then approved540. Never bypass a physics/safety/evidence failure."""
import json,csv,sys,os,time,fcntl,subprocess,shutil,statistics,traceback,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from c_depletion_runtime_20261111_v01 import atomic,sha
from c_depletion_integrations_20261112_v06 import notify
D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');A=D/'single_load_amendment_v01';E=D/'recovery_e2e_v02';E.mkdir(exist_ok=True);lock=open(E/'controller.lock','a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);rows=list(csv.DictReader((A/'attempt_manifest.csv').open()));cap=json.loads((E/'execution_lock.json').read_text());current={};pilot_results=[];main_results=[]
def status(st,reason=None):atomic(E/'status.json',dict(state=st,controller_pid=os.getpid(),current=current,pilot_completed=len(pilot_results),pilot_planned=15,main_completed=len(main_results),main_planned=540,main_success=sum(x['outcome']=='SUCCESS' for x in main_results),main_failure=sum(x['outcome']!='SUCCESS' for x in main_results),physical_main_entry='PASS' if len(pilot_results)==15 and all(x['outcome']=='SUCCESS' for x in pilot_results) else 'HOLD',reason=reason,updated=time.time()))
def verify():
 assert sha(A/'protocol.json')==cap['protocol_sha256'];assert sha(A/'attempt_manifest.csv')==cap['manifest_sha256']
 for p,h in cap['code_sha256'].items():assert sha(p)==h,'EXECUTION_CODE_CHANGED:'+p
 for p,h in cap['models_sha256'].items():assert sha(p)==h,'CHECKPOINT_CHANGED:'+p

def run(row,role):
 global current
 verify();key=row['attempt_id'];out=E/role/key;rp=out/'result.json'
 if rp.exists():
  result=json.loads(rp.read_text());assert (out/'runner_status.json').exists();assert not result['outcome'].startswith(('HOLD','INFRA')),'PREVIOUS_HOLD_REQUIRES_REVIEW:'+str(out)
  if role=='pilot':assert result['outcome']=='SUCCESS','PREVIOUS_FAILED_PILOT_REQUIRES_REVIEW:'+str(out)
  return result
 assert not out.exists(),'INTERRUPTED_OUTPUT_REVIEW_REQUIRED:'+str(out)
 assert shutil.disk_usage(D).free>25*1024**3,'DISK_BELOW_25_GIB'
 inp=E/'input_rows';inp.mkdir(exist_ok=True);rowpath=inp/(role+'_'+key+'.json');atomic(rowpath,row)
 gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
 argv=['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_v02_drive540_e2e_runner_20261113_v02.py'),'--run-dir',str(out),'--scenario-row',str(rowpath),'--representation',row['representation'],'--load','L4','--occlusion','O0','--group','G1','--role',role,'--scene-id',row['source_scene_id'],'--start-xy-yaw='+','.join(row[k] for k in ['start_x_m','start_y_m','start_yaw_deg']),'--cell-id',key,'--record-robotcam'];out.parent.mkdir(exist_ok=True);log=E/(role+'_'+key+'.log')
 with log.open('x') as f:
  p=subprocess.Popen(argv,cwd=R,stdout=f,stderr=subprocess.STDOUT);current=dict(role=role,attempt_id=key,pid=p.pid,output=str(out),log=str(log));notify('[IsaacSim] C540 '+role+' started',key+' fresh RGBD/pose/path/physics. Main denominator excludes pilots.')
  while p.poll() is None:status('RUNNING_'+role.upper());time.sleep(10)
 gl.close();assert rp.exists(),'RUN_RESULT_MISSING:'+str(out);result=json.loads(rp.read_text());result['artifact_path']=str(out);result['result_sha256']=sha(rp)
 assert not result['outcome'].startswith(('HOLD','INFRA')),'SAFETY_OR_INFRA_HOLD:'+json.dumps(result,default=str)[:1600]
 if role=='pilot':
  assert result['outcome']=='SUCCESS','TECHNICAL_PILOT_NOT_PASS:'+str(out)+' '+str(result.get('reason'))
  at=out/'attempt_0001'
  for f in ['actual_loaded_C_stage_manifest.json','pilot_physx_C.json','support_admission.json','camera_metadata.json','perception_result.json','selected_mask.npy','live_goals.json','steps.jsonl','legs_result.json','owned_processes.json']:assert (at/f).exists(),'PILOT_EVIDENCE_MISSING:'+f
  assert len(list((at/'rec_robotcam').glob('*.jpg')))>0,'PILOT_VIDEO_FRAMES_MISSING'
 current={};return result
try:
 verify();status('WAITING_STATIONARY_QUALIFICATIONS')
 for _ in range(360):
  p=json.loads((D/'pipeline_status.json').read_text());count=len(p.get('completed_stationary_qualifications',[]))
  if count==15:break
  assert p['state']!='HOLD','STATIONARY_QUALIFICATION_HOLD:'+str(p.get('reason'));time.sleep(10)
 else:raise RuntimeError('STATIONARY_QUALIFICATION_WAIT_TIMEOUT')
 for C in ['C100','C80','C60','C40','C20']:
  for rep in ['HR_Scan','LR_Scan','GeoCAD']:
   row=next(r for r in rows if r['base_id']=='C2D_B01' and r['C']==C and r['representation']==rep);pilot_results.append(run(row,'pilot'));atomic(E/'pilot_results.json',pilot_results);status('PILOT_PROGRESS')
 assert len(pilot_results)==15 and all(x['outcome']=='SUCCESS' for x in pilot_results),'ALL_15_TECHNICAL_PILOTS_MUST_PASS'
 # All pilot gates verified above. Locked trial IDs, pairing and numeric criteria remain unchanged.
 sizes=[sum(p.stat().st_size for p in Path(x['artifact_path']).rglob('*') if p.is_file()) for x in pilot_results];required=max(sizes)*540+25*1024**3;assert shutil.disk_usage(D).free>required,'INSUFFICIENT_PROJECTED_MAIN_DISK_CAPACITY:'+str(required)
 atomic(E/'main_entry_certificate.json',dict(state='PASS_15_PILOTS_AND_EVIDENCE',protocol_sha256=cap['protocol_sha256'],manifest_sha256=cap['manifest_sha256'],pilot_results=[dict(path=x['artifact_path'],sha256=x['result_sha256']) for x in pilot_results],GT_operational_input=False,created=time.time(),required_free_disk_bytes=required))
 notify('[IsaacSim] C540 main started','15 full E2E pilots passed; frozen O0/single-load540 begins. All planned attempts retained.')
 for row in rows:
  main_results.append(run(row,'main'));atomic(E/'main_results.json',main_results);status('MAIN_PROGRESS')
 status('COMPLETED_MAIN540');notify('[IsaacSim] C540 completed','540 outcomes recorded. Success '+str(sum(x['outcome']=='SUCCESS' for x in main_results))+'; all failures preserved.')
except BaseException as e:
 status('HOLD',str(e));atomic(E/'failure.json',dict(state='HOLD',reason=str(e),traceback=traceback.format_exc(),current=current,pilot_results=pilot_results,main_results=main_results));notify('[IsaacSim] HOLD C540 recovery',str(e)[:900]+' Evidence '+str(E)+'; no automatic parameter changes/retry.',high=True);raise
