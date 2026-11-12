"""Independent 39 unique fixed-C06 training trajectories, common ratio selection, then static stages."""
import json,os,time,subprocess,fcntl,statistics
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,locked
from c_depletion_integrations_20261112_v06 import notify
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';M=V/'MIX_C06_20261112_v01';O=V/'mixing_execution_v01';O.mkdir(exist_ok=True);lock=locked(O/'controller.lock');P=json.loads((M/'protocol.json').read_text());jobs={};start=time.time();current={}
def status(st,reason=None):atomic(O/'status.json',dict(state=st,current=current,controller_pid=os.getpid(),updated=time.time(),jobs=jobs,elapsed_seconds=time.time()-start,training_complete=sum(j['state']=='COMPLETED' and j.get('smoke') is False for j in jobs.values()),training_planned=39,physical_motion=False,reason=reason))
def train(ratio,rep,seed,smoke=False):
 global current
 key=('SMOKE_' if smoke else '')+ratio+'_'+rep+'_s'+str(seed);out=O/'runs'/key;out.parent.mkdir(exist_ok=True);result=out/'run_status.json'
 if result.exists():
  d=json.loads(result.read_text());assert d['state']=='PASS' and all(d['checks'].values());jobs[key]=dict(state='COMPLETED',smoke=smoke,output=str(out));return d
 assert not out.exists(),'INTERRUPTED_TRAINING_REVIEW_REQUIRED:'+key
 gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB);log=O/(key+'.log');cmd=['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_v02_mixed_train_20261112_v01.py'),'--ratio',ratio,'--rep',rep,'--seed',str(seed),'--output',str(out)]
 if smoke:cmd+=['--smoke']
 with log.open('x') as f:
  p=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT);current=dict(job=key,pid=p.pid,log=str(log),output=str(out));jobs[key]=dict(state='RUNNING',smoke=smoke,command=cmd,output=str(out));event(B,'STAGE_STARTED',job='V02_'+key)
  while p.poll() is None:status('RUNNING');time.sleep(10)
 gl.close();assert p.returncode==0,'TRAIN_EXIT_FAILURE:'+key+' '+str(log);d=json.loads(result.read_text());assert d['state']=='PASS' and all(d['checks'].values()),d
 for bb in d['best_balanced'].values():assert sha(bb['checkpoint'])==bb['sha256']
 jobs[key].update(state='COMPLETED',result_sha256=sha(result));current={};event(B,'STAGE_COMPLETED',job='V02_'+key);return d
try:
 for ratio in ['S100_R000','S050_R050','S000_R100']:train(ratio,'HR_Scan',42,True)
 all_models={};reps=['HR_Scan','LR_Scan','GeoCAD']
 for recipe in P['ratios']:
  ratio=recipe['ratio'];all_models[ratio]=[]
  for seed in [42,43,44]:
   for rep in (['HR_Scan'] if ratio=='S000_R100' else reps):
    d=train(ratio,rep,seed)
    for target,b in d['best_balanced'].items():all_models[ratio].append(dict(rep=target,seed=seed,checkpoint=b['checkpoint'],sha256=b['sha256'],combined_validation=b['score'],synthetic_validation=b['synthetic_val'],real_validation=b['real_val'],best_epoch=b['epoch'],ratio=ratio))
  assert len(all_models[ratio])==9
 scores={r:statistics.mean(x['combined_validation'] for x in a) for r,a in all_models.items()};order=[r['ratio'] for r in P['ratios']];best=min(order,key=lambda r:(-scores[r],order.index(r)));selection=dict(status='LOCKED',ratio=best,score=scores[best],scores=scores,models=all_models[best],baseline_models=all_models['S100_R000'],protocol_sha256=sha(M/'protocol.json'),Test_used=False,training_trajectories=39,zero_real_trajectories_shared=True)
 for a in all_models.values():
  for m in a:assert sha(m['checkpoint'])==m['sha256']
 atomic(M/'selection_lock.json',selection);atomic(O/'models_by_ratio.json',all_models);status('COMPLETED_TRAINING_VALIDATION');notify('[IsaacSim] C-V02 mixing completed','39 unique training trajectories complete; common ratio '+best+' locked from Validation only. Static evaluation next; physical HOLD.')
 cap=json.loads((V/'approved_final_static_capabilities_v01.json').read_text());assert not cap['physical_motion_authorized']
 for p,h in cap['code_sha256'].items():assert sha(p)==h
 for j in cap['jobs']:
  with (O/(j['id']+'.log')).open('x') as f:
   p=subprocess.Popen(j['command'],cwd=R,stdout=f,stderr=subprocess.STDOUT);current=dict(job=j['id'],pid=p.pid,log=str(O/(j['id']+'.log')))
   while p.poll() is None:status('RUNNING_FINAL_STATIC');time.sleep(10)
  assert p.returncode==0,'STATIC_FAILURE:'+j['id']
 atomic(O/'result.json',dict(state='COMPLETED',training_jobs=39,selected_ratio=best,physical_stages='HOLD'));status('HOLD_PHYSICAL_STAGES');event(B,'HOLD',reason='V02 all static stages complete; physical pilot/300/150 HOLD')
except BaseException as ex:
 status('HOLD',str(ex));event(B,'HOLD',reason='V02 mixing '+str(ex)+' root='+str(O));notify('[IsaacSim] C-V02 mixing HOLD',str(ex)+' root='+str(O),True);raise
