"""Independent observer, durable ntfy retry queue and bounded GitHub sync. Never kills workers."""
import argparse,json,os,shutil,subprocess,time,traceback
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,atomic,event,locked,protocol,proc_alive
from c_depletion_integrations_20261111_v01 import notify,publish
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();O=a.root;p=protocol(O);lock=locked(O/'watchdog.lock')
statefile=O/'watchdog_memory.json';mem=json.loads(statefile.read_text()) if statefile.exists() else dict(event_line=0,outbox={},last_sync=0,sync_pending=True,last_snapshot=0,last_hpo_phase=None,last_hpo_state=None,last_hpo_triplets=-1)
def enqueue(key,title,body,high=False):
 if key not in mem['outbox']:mem['outbox'][key]=dict(title=title,body=body,high=high,state='PENDING',attempts=0,next_retry=0)
def err(kind,e):
 with (O/'integration_errors.jsonl').open('a') as f:f.write(json.dumps(dict(time=time.time(),kind=kind,error=type(e).__name__,summary=str(e)[:180] if kind=='GITHUB' else type(e).__name__))+'\n')
enqueue('INDEPENDENCE_TEST','[IsaacSim] C pipeline watchdog test','C_DEPLETION_REBUILD_20261111_v01: independent local watchdog test. Existing HPO untouched. New render/train/drive remain HOLD. Check local root watchdog_status.json.')
while True:
 try:
  now=time.time();proto=protocol(O)
  lines=(O/'pipeline_events.jsonl').read_text().splitlines() if (O/'pipeline_events.jsonl').exists() else []
  for i,line in enumerate(lines[mem['event_line']:],mem['event_line']):
   try:e=json.loads(line)
   except ValueError:break
   if e['kind'] in ['STAGE_STARTED','STAGE_COMPLETED','HOLD','CONTROLLER_ERROR']:
    enqueue('EVENT_'+str(i),'[IsaacSim] '+e['kind'],f"C_DEPLETION_REBUILD_20261111_v01 {e.get('job','')} {e.get('reason',e.get('detail',''))}; logs={O/'logs'}; automatic recovery=no parameter changes",e['kind'] in ['HOLD','CONTROLLER_ERROR']);mem['sync_pending']=True
   mem['event_line']=i+1
  hp_path=Path(p['hpo_root'])/'hpo_status.json';hp=json.loads(hp_path.read_text());jobs=json.loads((Path(p['hpo_root'])/'jobs.json').read_text());cur=hp.get('current') or {};phase=cur.get('phase');hs=hp['state']
  if phase and phase!=mem['last_hpo_phase']:
   enqueue('HPO_PHASE_'+phase,'[IsaacSim] HPO stage '+phase,f"Existing L1-L4 HPO entered {phase}; controller {hp['controller_pid']}; summary {hp_path}. C dataset execution remains HOLD.");mem['last_hpo_phase']=phase;mem['sync_pending']=True
  if hs!=mem['last_hpo_state']:
   if hs in ['COMPLETED','COMPLETED_WITH_FAILURES','BLOCKED']:
    enqueue('HPO_STATE_'+hs,'[IsaacSim] HPO '+hs,f"L1-L4 HPO {hs}; failed/interrupted counts {hp.get('job_counts')}; summary={hp_path}; does NOT authorize new C runs.",hs=='BLOCKED');mem['sync_pending']=True
   mem['last_hpo_state']=hs
  triplets=hp.get('completed_training_jobs',0)//3
  if triplets!=mem['last_hpo_triplets']:mem['last_hpo_triplets']=triplets;mem['sync_pending']=True
  logged=0;max_epochs=5766 if (Path(p['hpo_root'])/'selection_lock.json').exists() and json.loads((Path(p['hpo_root'])/'selection_lock.json').read_text())['candidate_id']==0 else 6966
  for j in jobs.values():
   if j.get('kind')=='train' and j.get('state')=='COMPLETED':logged+=dict(smoke=2,screen=60).get(j['phase'],200)
  logged+=int(cur.get('epoch',0));eta_seconds=max(0,max_epochs-logged)*p['observed_training_epoch_seconds']
  warnings=[]
  if hs=='RUNNING':
   if not proc_alive(hp.get('controller_pid')):warnings.append('HPO_CONTROLLER_MISSING')
   if now-hp_path.stat().st_mtime>120:warnings.append('HPO_HEARTBEAT_STALE')
   if cur.get('output'):
    candidates=[Path(cur['output'])/'epochs.jsonl',Path(cur['output'])/'run_status.json'];fresh=max([q.stat().st_mtime for q in candidates if q.exists()] or [now])
    if now-fresh>900:warnings.append('HPO_PROGRESS_STALE_15MIN_POSSIBLE_HANG')
  pipe=json.loads((O/'pipeline_status.json').read_text()) if (O/'pipeline_status.json').exists() else {}
  if pipe and not proc_alive(pipe.get('controller_pid')):warnings.append('C_CONTROLLER_MISSING')
  free=shutil.disk_usage(O).free
  if free<25*1024**3:warnings.append('DISK_BELOW_25_GIB')
  gpu=subprocess.run(['nvidia-smi','--query-gpu=utilization.gpu,memory.used,memory.total','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10)
  for w in warnings:enqueue(w+'_'+str(int(now//1800)),'[IsaacSim] '+w,f"C preparation monitor: {w}; experiment={cur.get('key')}; log={cur.get('output')}; no process killed or parameters changed; inspect and HOLD.",True)
  for key,q in mem['outbox'].items():
   if q['state']=='DELIVERED' or now<q['next_retry']:continue
   q['attempts']+=1
   try:ok=notify(q['title'],q['body'],q['high'])
   except Exception as ex:ok=False;err('NTFY',ex)
   q['next_retry']=now+min(3600,60*2**min(q['attempts']-1,6))
   if ok:q.update(state='DELIVERED',delivered=now,receipt='existing hook returned HTTP200; handset receipt unknown')
   else:err('NTFY',RuntimeError('SEND_RETURNED_FALSE'))
  # Milestones sync within <=5min; snapshots <=30min, never a commit per heartbeat.
  sync_due=mem['sync_pending'] and now-mem['last_sync']>=300 or now-mem['last_sync']>=1800
  if sync_due:
   mem['last_sync']=now
   try:
    receipt=publish(O);atomic(O/'github_sync_status.json',receipt);mem['sync_pending']=False
   except Exception as ex:
    err('GITHUB',ex);mem['sync_pending']=True;atomic(O/'github_sync_status.json',dict(state='PENDING_RETRY',time=now,error=type(ex).__name__,reason=str(ex)[:180],local_experiments_continue=True))
  meminfo={line.split(':')[0]:line.split(':')[1].strip() for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith(('MemAvailable:','MemTotal:'))}
  process_rss={}
  for pid in [hp.get('controller_pid'),cur.get('pid'),pipe.get('controller_pid'),os.getpid()]:
   try:process_rss[str(pid)]=next(line.split(':')[1].strip() for line in Path(f'/proc/{pid}/status').read_text().splitlines() if line.startswith('VmRSS:'))
   except (OSError,StopIteration):process_rss[str(pid)]='UNKNOWN'
  status=dict(pid=os.getpid(),updated=now,pipeline=pipe.get('state'),HPO_state=hs,HPO_current=cur,HPO_logged_epochs=logged,HPO_max_planned_epochs=max_epochs,HPO_epoch_progress=logged/max_epochs,HPO_remaining_training_seconds_estimate=eta_seconds,HPO_estimate_excludes_crossval_and_startup=True,free_disk_bytes=free,gpu_csv=gpu.stdout.strip() if gpu.returncode==0 else 'UNKNOWN',loadavg=os.getloadavg(),memory=meminfo,process_RSS=process_rss,warnings=warnings,ntfy_delivered=sum(q['state']=='DELIVERED' for q in mem['outbox'].values()),ntfy_pending=sum(q['state']!='DELIVERED' for q in mem['outbox'].values()),github_sync_pending=mem['sync_pending'],new_gpu_execution=False,soft_budget_hours=48,stop_at_budget=False)
  atomic(O/'watchdog_status.json',status);atomic(statefile,mem)
  if now-mem['last_snapshot']>=900:
   with (O/'watchdog_snapshots.jsonl').open('a') as f:f.write(json.dumps(status)+'\n')
   mem['last_snapshot']=now;atomic(statefile,mem)
 except Exception as e:
  err('WATCHDOG',e)
 time.sleep(30)
