"""Passive 540 HOLD/error monitor and original GitHub+ntfy integrations. No worker launch."""
from pathlib import Path
import json,time,sys,hashlib,os
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from c_depletion_runtime_20261111_v01 import atomic
from c_depletion_integrations_20261113_v16 import notify,publish
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');D=B/'C_V02_20261112_v01/DRIVE540_20261113_v01';A=D/'single_load_amendment_v01';last='';notified=False;last_recovery_state=None
while True:
 try:
  status=json.loads((D/'pipeline_status.json').read_text());cpu=json.loads((A/'CPU_scene_QA_v01/result.json').read_text());summary=dict(active_protocol=json.loads((D/'active_physical_protocol.json').read_text()),protocol=json.loads((A/'protocol.json').read_text()),pipeline={k:status.get(k) for k in ['state','controller_pid','current','completed_stationary_qualifications','main_completed','main_planned','physical_gate','reason']},CPU_geometry_state=cpu['state'],CPU_conditions=[{k:r[k] for k in ['C','rep','checks','load_count','pallet_count','brick_count','collider_geometry_sha256']} for r in cpu['results']],infrastructure_failures=json.loads((D/'infrastructure_failure_inventory_v01.json').read_text()),actual_single_load_perception='NOT_RUN',actual_PhysX='HOLD_NATIVE_KIT_CRASH_UNRESOLVED',main_completed=0,physical_main_entry='HOLD',monitor_pid=os.getpid())
  recovery=D/'recovery_e2e_v01/status.json'
  if recovery.exists():
   rs=json.loads(recovery.read_text());summary['recovery_e2e_status']={k:v for k,v in rs.items() if k!='updated'};summary['actual_PhysX']='BASIC_KIT_RGBD_REGISTRATION_CONTACTS_RECOVERED; full motion gates remain';summary['actual_single_load_perception']='PENDING full E2E pilot';summary['main_completed']=rs['main_completed'];summary['physical_main_entry']=rs['physical_main_entry']
   if last_recovery_state!=rs['state']:
    accepted=notify('[IsaacSim] C540 recovery '+rs['state'],str(rs.get('reason') or rs.get('current'))[:850]+' status '+str(recovery),high=rs['state']=='HOLD');last_recovery_state=rs['state'] if accepted else last_recovery_state
  recovered=D/'recovery_evidence_v01/drive540_crash_recovery_summary_20261113_v01.json'
  if recovered.exists():
   rr=json.loads(recovered.read_text());summary['verified_recovery_result']=rr;summary['actual_single_load_perception']=rr['perception_status'];summary['actual_PhysX']='HR strict pre-drive admission PASS; remaining full motion gates NOT_RUN'
  data=json.dumps(summary,sort_keys=True);fingerprint=hashlib.sha256(data.encode()).hexdigest()
  if not notified and not recovery.exists():
   accepted=notify('[IsaacSim] HOLD C-V02 single-load 540','Single load/pallet manifest540 locked; CPU15 conditions PASS. Actual Kit qualification native OmniGraph crash, four preserved diagnostic attempts. Main0/540; no auto retry. Log '+str(D/'logs'),high=True)
   atomic(D/'ntfy_status.json',dict(server_accepted=accepted,phone_receipt='UNKNOWN',time=time.time(),event='single_load540_physics_HOLD'));notified=accepted
  if fingerprint!=last:
   atomic(D/'drive540_single_load_public_summary_20261113_v01.json',summary)
   result=publish(B);atomic(D/'github_sync_status.json',result);last=fingerprint
  atomic(D/'monitor_status.json',dict(state='MONITORING_PHYSICAL_HOLD',pid=os.getpid(),updated=time.time(),main_completed=0,next_automatic_GPU_job='See recovery_e2e_v01/status.json; physical main remains gated',ntfy_server_accepted=notified))
 except BaseException as e:
  atomic(D/'monitor_integration_error.json',dict(state='PENDING_RETRY',error=type(e).__name__+':'+str(e),time=time.time(),local_experiments_affected=False))
 time.sleep(60)
