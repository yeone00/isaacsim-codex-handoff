"""Independent passive technical/main monitor, ntfy, verified GitHub queue. No GPU job/parameter control."""
import json,time,sys,os,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from c_depletion_runtime_20261111_v01 import atomic
from c_depletion_integrations_20261113_v18 import notify,publish
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');D=B/'C_V02_20261112_v01/DRIVE540_20261113_v01';E=D/'technical_e2e_v03';last_publish='';notified=set();last_publish_time=0
while True:
 try:
  s=json.loads((E/'status.json').read_text());warnings=[];now=time.time();pid=s.get('controller_pid');state=s['state'];cur=s.get('current',{})
  if state.startswith(('RUNNING','PILOT','MAIN','TECHNICAL')) and pid and not Path('/proc',str(pid)).exists():warnings.append('CONTROLLER_LOST')
  if state.startswith('RUNNING'):
   if now-s['updated']>120:warnings.append('CONTROLLER_HEARTBEAT_STALE')
   output=Path(cur.get('output','/nonexistent'));activity=[output/'runtime.log',output/'attempt_0001/feedback.json',output/'attempt_0001/driver_status.json',output/'attempt_0001/steps.jsonl'];recent=max([p.stat().st_mtime for p in activity if p.exists()]+[s['updated']]);
   if now-recent>600:warnings.append('WORKER_NO_ACTIVITY_600S')
  for message in warnings+(['HOLD:'+str(s.get('reason'))] if state=='HOLD' else []):
   if message not in notified:
    accepted=notify('[IsaacSim] C540 technical alert',message[:900]+' status '+str(E/'status.json'),high=True)
    if accepted:notified.add(message)
  summary=dict(status={k:v for k,v in s.items() if k not in ['updated','elapsed_seconds']},technical_policy=json.loads((D/'technical_policy_amendment_v01/technical_policy.json').read_text()),execution_lock_sha256=hashlib.sha256((E/'execution_lock.json').read_bytes()).hexdigest(),watchdog_warnings=warnings,physical_main_criteria='all15 technical handling PASS + separate actual motion/stop PASS + evidence and disk; task success is NOT required',raw_RGBD_checkpoints_published=False)
  if (E/'pilot_records.json').exists():summary['pilot_records']=json.loads((E/'pilot_records.json').read_text())
  if (E/'engineering_control_record.json').exists():summary['engineering_control_record']=json.loads((E/'engineering_control_record.json').read_text())
  data=json.dumps(summary,sort_keys=True);fingerprint=hashlib.sha256(data.encode()).hexdigest()
  if fingerprint!=last_publish and now-last_publish_time>=120:
   atomic(D/'drive540_technical_execution_summary_20261113_v01.json',summary);(D/'drive540_technical_policy_20261113_v01.json').write_bytes((D/'technical_policy_amendment_v01/technical_policy.json').read_bytes());(D/'drive540_offline_representative_15_pose_20261113_v01.csv').write_bytes((D/'saved_calibration_pose_adapter_v02/representative_15_pose.csv').read_bytes());result=publish(B);atomic(E/'github_sync_status.json',result);last_publish=fingerprint;last_publish_time=now
  atomic(E/'watchdog_status.json',dict(state='MONITORING',pid=os.getpid(),updated=now,current=s,warning=warnings,notification_event_count=len(notified),GPU=subprocess.run(['nvidia-smi','--query-gpu=utilization.gpu,memory.used','--format=csv,noheader,nounits'],capture_output=True,text=True).stdout.strip()))
 except BaseException as exc:
  atomic(E/'watchdog_error.json',dict(state='PENDING_RETRY',error=repr(exc),time=time.time(),research_processes_not_interrupted=True))
 time.sleep(30)
