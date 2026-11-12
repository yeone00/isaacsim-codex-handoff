"""CPU observer for new V02 stages; durable ntfy retry queue, no worker signals or GPU computation."""
import json,time,os,shutil,subprocess
from pathlib import Path
from c_depletion_runtime_20261111_v01 import atomic,locked
from c_depletion_integrations_20261112_v06 import notify
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';lock=locked(V/'watchdog.lock');mp=V/'watchdog_memory.json';mem=json.loads(mp.read_text()) if mp.exists() else dict(last=None,outbox={})
while True:
 try:
  p=json.loads((V/'pipeline_status.json').read_text());mix=V/'mixing_execution_v01/status.json';m=json.loads(mix.read_text()) if mix.exists() else {};static=V/'final_static_pipeline_v01/status.json';s=json.loads(static.read_text()) if static.exists() else {};active=s if s.get('state')=='RUNNING' else m if m else p;state=active.get('state');cur=active.get('current',{});key=str((state,p.get('stage'),cur.get('job'),active.get('reason')))
  if key!=mem['last']:
   mem['last']=key;high=str(state).startswith('HOLD');title='[IsaacSim] C-V02 '+str(state);body='stage='+str(p.get('stage'))+' job='+str(cur.get('job'))+' reason='+str(active.get('reason'))+' logs='+str(cur.get('log',V/'controller.log'))+'; physical HOLD'
   # Render mini-batches are recorded locally, not all notified. Failures and stage/mixed-model transitions are.
   if high or not str(p.get('stage','')).startswith('C100_') or cur.get('job'):mem['outbox'][key]=dict(state='PENDING',title=title,body=body,high=high,attempts=0,next_retry=0)
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
  atomic(V/'watchdog_status.json',dict(pid=os.getpid(),updated=time.time(),pipeline=p,current_mixing=m if not m.get('jobs') else {k:v for k,v in m.items() if k!='jobs'},current_epoch=epoch,current_static=s,GPU=gpu,free_disk_bytes=shutil.disk_usage(V).free,ntfy_pending=sum(x['state']!='DELIVERED' for x in mem['outbox'].values()),physical_motion=False));atomic(mp,mem)
 except Exception as ex:atomic(V/'watchdog_last_error.json',dict(time=time.time(),error=str(ex)))
 time.sleep(30)
