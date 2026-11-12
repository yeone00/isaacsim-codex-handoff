"""CPU observer for new V02 stages; durable ntfy retry queue, no worker signals or GPU computation."""
import json,time,os,shutil,subprocess,threading,fcntl
from pathlib import Path
from c_depletion_runtime_20261111_v01 import atomic,locked,proc_alive,sha
from c_depletion_integrations_20261112_v06 import notify
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';lock=locked(V/'watchdog.lock');mp=V/'watchdog_memory.json';mem=json.loads(mp.read_text()) if mp.exists() else dict(last=None,outbox={})
def reserve_next_GPU_boundary(reason):
 g=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(g,fcntl.LOCK_EX);atomic(V/'watchdog_GPU_HOLD.json',dict(state='HOLD_GPU_BOUNDARY',reason=reason,time=time.time()))
 while not (V/'clear_watchdog_GPU_HOLD.json').exists():time.sleep(10)
 g.close()
hold_thread=None
while True:
 try:
  p=json.loads((V/'pipeline_status.json').read_text());mix=V/'mixing_execution_v01/status.json';m=json.loads(mix.read_text()) if mix.exists() else {};static=V/'final_static_pipeline_v01/status.json';s=json.loads(static.read_text()) if static.exists() else {};active=s if s.get('state')=='RUNNING' else m if m else p;state=active.get('state');cur=active.get('current',{});key=str((state,p.get('stage'),cur.get('job'),active.get('reason')))
  if key!=mem['last']:
   mem['last']=key;high=str(state).startswith('HOLD');title='[IsaacSim] C-V02 '+str(state);body='stage='+str(p.get('stage'))+' job='+str(cur.get('job'))+' reason='+str(active.get('reason'))+' logs='+str(cur.get('log',V/'controller.log'))+'; physical HOLD'
   # Render mini-batches are recorded locally, not all notified. Failures and stage/mixed-model transitions are.
   if high or not str(p.get('stage','')).startswith('C100_') or cur.get('job'):mem['outbox'][key]=dict(state='PENDING',title=title,body=body,high=high,attempts=0,next_retry=0)
  warnings=[]
  if p.get('state') in ['RUNNING','WAITING']:
   if not proc_alive(p.get('controller_pid')):warnings.append('CONTROLLER_MISSING')
   if time.time()-p.get('updated',0)>120:warnings.append('CONTROLLER_HEARTBEAT_STALE')
  if cur.get('pid') and active.get('state') in ['RUNNING','RUNNING_FINAL_STATIC']:
   if not proc_alive(cur['pid']):warnings.append('WORKER_MISSING')
   log=Path(cur.get('log','/notexistent'))
   if log.exists() and time.time()-log.stat().st_mtime>1800:warnings.append('WORKER_LOG_STALE_30MIN')
   ep=Path(cur.get('output','/notexistent'))/'epochs.jsonl'
   if ep.exists() and time.time()-ep.stat().st_mtime>900:warnings.append('TRAIN_EPOCH_STALE_15MIN')
  if shutil.disk_usage(V).free<25*1024**3:warnings.append('DISK_BELOW_25_GIB')
  for specname in ['approved_training_capabilities_v01.json','approved_final_static_capabilities_v01.json']:
   for code,h in json.loads((V/specname).read_text())['code_sha256'].items():
    if sha(code)!=h:warnings.append('FROZEN_SOURCE_CHANGED:'+code)
  for reason in warnings:
   mem['outbox'].setdefault('GUARD_'+reason,dict(state='PENDING',title='[IsaacSim] C-V02 safety HOLD',body=reason+' logs='+str(V)+'; active worker not killed; next GPU boundary reserved',high=True,attempts=0,next_retry=0))
  if warnings and hold_thread is None:
   atomic(V/'watchdog_HOLD_request.json',dict(reasons=warnings,time=time.time()));hold_thread=threading.Thread(target=reserve_next_GPU_boundary,args=(';'.join(warnings),),daemon=True);hold_thread.start()
  for k,item in mem['outbox'].items():
   if item['state']=='DELIVERED' or time.time()<item['next_retry']:continue
   item['attempts']+=1
   if notify(item['title'],item['body'],item['high']):item.update(state='DELIVERED',server_HTTP=200,handset_receipt='UNKNOWN',time=time.time())
   else:item['next_retry']=time.time()+min(900,30*2**min(5,item['attempts']))
  epoch=None
  if cur.get('output'):
   f=Path(cur['output'])/'epochs.jsonl'
   if f.exists():
    lines=f.read_text().splitlines()
    if lines:epoch=json.loads(lines[-1]).get('epoch')
  gpu=subprocess.run(['nvidia-smi','--query-gpu=utilization.gpu,memory.used,memory.total','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10).stdout.strip()
  atomic(V/'watchdog_status.json',dict(pid=os.getpid(),updated=time.time(),pipeline=p,current_mixing=m if not m.get('jobs') else {k:v for k,v in m.items() if k!='jobs'},current_epoch=epoch,current_static=s,GPU=gpu,free_disk_bytes=shutil.disk_usage(V).free,ntfy_pending=sum(x['state']!='DELIVERED' for x in mem['outbox'].values()),physical_motion=False,warnings=warnings));atomic(mp,mem)
 except Exception as ex:atomic(V/'watchdog_last_error.json',dict(time=time.time(),error=str(ex)))
 time.sleep(30)
