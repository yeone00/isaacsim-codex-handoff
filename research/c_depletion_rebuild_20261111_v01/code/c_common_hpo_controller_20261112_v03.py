"""Independent sequential HPO controller. No torch imports; detached tmux owns lifetime.
Fresh pretrained workers only. Interrupted attempts are retained, never passed as completed.
"""
import argparse,csv,datetime,fcntl,json,math,os,shutil,subprocess,sys,time,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation.c_common_hpo_policy_20261111_v01 import REPS,R,sha,atomic,common_score,gpu_gate,load_protocol
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--protocol-sha',required=True);ap.add_argument('--resume-interrupted',action='store_true');a=ap.parse_args()
O=a.root.resolve();P=load_protocol(O,a.protocol_sha);PY=P['python'];START=time.time();jobs={};CURRENT={};LAST_SNAPSHOT=0
lock=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
rootlock=open(O/'controller.lock','a');fcntl.flock(rootlock,fcntl.LOCK_EX|fcntl.LOCK_NB)
JOBFILE=O/'jobs.json'
if JOBFILE.exists():jobs=json.loads(JOBFILE.read_text())
C=json.loads((O/'candidates.json').read_text())
def now():return datetime.datetime.now().astimezone().isoformat()
def error(kind,detail):
 with (O/'hpo_errors.log').open('a') as f:f.write(json.dumps(dict(time=now(),kind=kind,detail=detail),default=str)+'\n')
def score(cid,phase):
 ss={}
 for rep in REPS:
  j=jobs.get(f'{phase}_C{cid:02d}_{rep}_s42',{})
  if j.get('state')!='COMPLETED':return None
  ss[rep]=j['mask_map5095']
 return common_score(ss)
def valid_train(j):
 try:
  out=Path(j['output']);s=json.loads((out/'run_status.json').read_text());au=json.loads((out/'audit.json').read_text());b=s['best']
  expected={'smoke':2,'screen':60}.get(j['phase'],200)
  assert s['state']=='PASS' and all(s['checks'].values())
  assert len(au['epochs'])==expected and au['epochs'][-1]['epoch']==expected
  assert sha(b['checkpoint'])==b['sha256'] and math.isfinite(b['val_mask_map5095'])
  assert s['hpo_protocol_sha256']==a.protocol_sha and s['candidate_id']==j['candidate_id'] and s['seed']==j['seed'] and s['rep']==j['rep']
  assert (out/'train/results.csv').is_file() and s['train_kwargs']['epochs']==200 and s['train_kwargs']['batch']==64
  return s
 except Exception:return None
def publish(state='RUNNING',reason=None):
 global LAST_SNAPSHOT
 cand=[]
 for c in C:
  cid=c['id'];jj=[jobs.get(f'screen_C{cid:02d}_{r}_s42',{}) for r in REPS];states=[j.get('state','PENDING') for j in jj]
  st='COMPLETED' if all(x=='COMPLETED' for x in states) else 'FAILED' if any(x in ['FAILED','INTERRUPTED'] for x in states) else 'RUNNING' if 'RUNNING' in states else 'PENDING'
  cand.append(dict(candidate_id=cid,state=st,screen_score=score(cid,'screen'),full_score=score(cid,'full'),**c['params']))
 bests=[(c['full_score'],c['candidate_id']) for c in cand if c['full_score'] is not None]
 if not bests:bests=[(c['screen_score'],c['candidate_id']) for c in cand if c['screen_score'] is not None]
 best=max(bests,key=lambda t:(t[0],-t[1])) if bests else None
 current=dict(CURRENT)
 if current.get('output'):
  ep=Path(current['output'])/'epochs.jsonl'
  try:
   lines=ep.read_text().splitlines();e=json.loads(lines[-1]);current.update(epoch=e['epoch'],latest_validation_mask_map5095=e['val_extra']['mask_map5095'])
  except (OSError,IndexError,ValueError):current['epoch']=0
 stat=dict(state=state,reason=reason,updated=now(),controller_pid=os.getpid(),session=P['session'],total_candidates=len(C),candidate_counts={s:sum(c['state']==s for c in cand) for s in ['COMPLETED','RUNNING','PENDING','FAILED']},current=current,best_candidate=best,best_score_phase='full' if any(c['full_score'] is not None for c in cand) else 'screen',completed_training_jobs=sum(j.get('state')=='COMPLETED' and j.get('kind')=='train' for j in jobs.values()),job_counts={s:sum(j.get('state')==s for j in jobs.values()) for s in ['COMPLETED','RUNNING','FAILED','INTERRUPTED']},max_training_jobs=57,max_model_epochs=5766,wall_seconds_this_controller=time.time()-START,test_used=False,recovery='--resume-interrupted explicitly restarts interrupted attempts from pretrained in a new attempt directory; completed verified jobs skipped')
 atomic(O/'jobs.json',jobs);atomic(O/'hpo_status.json',stat)
 with (O/'hpo_results.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,cand[0]);w.writeheader();w.writerows(cand)
 (O/'hpo_progress.md').write_text('# B1 common HPO\n\n'+json.dumps(stat,indent=2)+'\n\nRead hpo_results.csv and jobs.json for full history.\n')
 if time.time()-LAST_SNAPSHOT>=900:
  with (O/'status_snapshots.jsonl').open('a') as f:f.write(json.dumps(stat)+'\n')
  LAST_SNAPSHOT=time.time()
def resource_gate():
 g=gpu_gate((os.getpid(),))
 if not g['clear']:raise RuntimeError('RESOURCE_GATE:'+json.dumps(g))
 if shutil.disk_usage(O).free<25*1024**3:raise RuntimeError('DISK_BELOW_25_GIB')
def run_job(key,kind,meta,command_builder):
 global CURRENT
 old=jobs.get(key)
 if old:
  if old['state']=='COMPLETED':
   if kind=='train':assert valid_train(old),'COMPLETED_ARTIFACT_INVALID:'+key
   else:assert sha(Path(old['output'])/'result.json')==old['result_sha256']
   return old
  if old['state']=='FAILED':return old
  if old['state'] in ['RUNNING','INTERRUPTED']:
   pid=old.get('pid')
   if pid and Path(f'/proc/{pid}').exists():raise RuntimeError('PRIOR_WORKER_STILL_ALIVE:'+str(pid))
   old['state']='INTERRUPTED';error('INTERRUPTED',old);publish()
   if not a.resume_interrupted:raise RuntimeError('EXPLICIT_RESUME_INTERRUPTED_REQUIRED:'+key)
   atomic(O/'attempt_history'/f'{key}_a{old["attempt"]:02d}.json',old)
 attempt=old.get('attempt',0)+1 if old else 1
 out=O/'runs'/f'{key}_a{attempt:02d}';assert not out.exists()
 resource_gate();cmd=command_builder(out)
 j=dict(key=key,kind=kind,state='RUNNING',attempt=attempt,output=str(out),started=time.time(),command=cmd,**meta)
 j['fingerprint']=__import__('hashlib').sha256(json.dumps(dict(key=key,protocol=a.protocol_sha,meta=meta),sort_keys=True).encode()).hexdigest()
 jobs[key]=j;log=O/'logs'/f'{key}_a{attempt:02d}.log'
 with log.open('x') as f:
  proc=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,cwd=R,env=dict(os.environ,PYTHONUNBUFFERED='1'))
  j['pid']=proc.pid;CURRENT=dict(key=key,pid=proc.pid,output=str(out),**meta);publish()
  while proc.poll() is None:time.sleep(10);publish()
 j.update(exit_code=proc.returncode,ended=time.time(),elapsed_seconds=time.time()-j['started'],log=str(log))
 if kind=='train':
  s=valid_train(j) if proc.returncode==0 else None
  if s:j.update(state='COMPLETED',mask_map5095=s['best']['val_mask_map5095'],best=s['best'],run_status_sha256=sha(out/'run_status.json'))
  else:j.update(state='FAILED',failure='TRAINING_EXIT_OR_AUDIT_FAILURE')
 else:
  try:
   result=json.loads((out/'result.json').read_text());assert proc.returncode==0 and result['state']=='COMPLETED' and math.isfinite(result['mask_map5095'])
   j.update(state='COMPLETED',mask_map5095=result['mask_map5095'],result_sha256=sha(out/'result.json'))
  except Exception:j.update(state='FAILED',failure='VALIDATION_EXIT_OR_RESULT_FAILURE')
 if j['state']=='FAILED':error(j['failure'],j)
 CURRENT={};publish();return j
def train(phase,cid,rep,seed):
 key=f'{phase}_C{cid:02d}_{rep}_s{seed}'
 return run_job(key,'train',dict(phase=phase,candidate_id=cid,rep=rep,seed=seed),lambda out:[PY,str(R/'scripts/c_common_hpo_train_20261112_v03.py'),'--root',str(O),'--protocol-sha',a.protocol_sha,'--candidate',str(cid),'--rep',rep,'--seed',str(seed),'--phase',phase,'--output',str(out)])
def freeze(path,obj):
 if path.exists():assert json.loads(path.read_text())==obj,'SELECTION_ALREADY_FROZEN_DIFFERENT'
 else:atomic(path,obj)
try:
 publish();resource_gate()
 for rep in REPS:
  assert train('smoke',0,rep,42)['state']=='COMPLETED','QUALIFICATION_FAILED'
 for c in C:
  for rep in REPS:
   j=train('screen',c['id'],rep,42)
   if c['id']==0 and j['state']!='COMPLETED':raise RuntimeError('BASELINE_SCREEN_FAILED')
 eligible=[c['id'] for c in C[1:] if score(c['id'],'screen') is not None]
 assert len(eligible)>=3,'INSUFFICIENT_ELIGIBLE_CANDIDATES'
 promoted=[0]+sorted(eligible,key=lambda cid:(-score(cid,'screen'),cid))[:3]
 freeze(O/'promotion_lock.json',dict(candidate_ids=promoted,rule='baseline plus top3 complete screen triplets; ties earliest candidate id',protocol_sha256=a.protocol_sha))
 for cid in promoted:
  for rep in REPS:
   j=train('full',cid,rep,42)
   if cid==0 and j['state']!='COMPLETED':raise RuntimeError('BASELINE_FULL_FAILED')
 eligible=[cid for cid in promoted if score(cid,'full') is not None];assert eligible
 selected=min(eligible,key=lambda cid:(-score(cid,'full'),cid))
 freeze(O/'selection_lock.json',dict(candidate_id=selected,params=C[selected]['params'],score=score(selected,'full'),rule='200epoch own-validation mask-only mean; ties lowest candidate id; no Test',protocol_sha256=a.protocol_sha))
 for cid in [selected]:
  for seed in [43,44]:
   for rep in REPS:
    j=train('baseline_control' if cid==0 else 'final',cid,rep,seed)
    if j['state']!='COMPLETED':error('SEED_STABILITY_FAILURE_PRESERVED',j)
 # Own-val metrics already available. Cross representation metrics are secondary only, after selection.
 for cid in sorted({0,selected}):
  for seed in [42,43,44]:
   phase='full' if seed==42 else 'baseline_control' if cid==0 else 'final'
   for source in REPS:
    j=jobs.get(f'{phase}_C{cid:02d}_{source}_s{seed}',{})
    if j.get('state')!='COMPLETED':continue
    for target in REPS:
     if target==source:continue
     key=f'crossval_C{cid:02d}_{source}_s{seed}_to_{target}';b=j['best']
     run_job(key,'crossval',dict(candidate_id=cid,rep=target,source_rep=source,seed=seed,phase='secondary_validation'),lambda out,b=b,target=target:[PY,str(R/'scripts/c_common_hpo_crossval_20261112_v03.py'),'--root',str(O),'--protocol-sha',a.protocol_sha,'--checkpoint',b['checkpoint'],'--checkpoint-sha',b['sha256'],'--rep',target,'--output',str(out)])
 # CPU-only final analysis, no AI invocation.
 import statistics
 summary=[]
 for cid in sorted({0,selected}):
  for rep in REPS:
   jj=[j for j in jobs.values() if j.get('kind')=='train' and j.get('candidate_id')==cid and j.get('rep')==rep and j.get('phase') in ['full','final','baseline_control'] and j.get('state')=='COMPLETED']
   vals=[j['mask_map5095'] for j in jj];summary.append(dict(candidate_id=cid,rep=rep,n=len(vals),mean=statistics.mean(vals) if vals else None,sd=statistics.stdev(vals) if len(vals)>1 else None,seed_metrics={str(j['seed']):j['mask_map5095'] for j in jj}))
 result=dict(selection=json.loads((O/'selection_lock.json').read_text()),seed_summary=summary,total_worker_wall_seconds=sum(j.get('elapsed_seconds',0) for j in jobs.values()),failed_jobs=[k for k,j in jobs.items() if j.get('state')!='COMPLETED'],test_used=False,seed42_selection_bias=True,rng_policy=P['rng_policy'])
 atomic(O/'final_summary.json',result)
 state='COMPLETED_WITH_FAILURES' if result['failed_jobs'] else 'COMPLETED';publish(state)
 report=R/'reports/c_common_hpo_final_20261111_v01.md'
 report.write_text('# C 데이터 전용 공통 HPO 최종 자동 집계\n\n'+json.dumps(result,indent=2,ensure_ascii=False)+'\n\n전체 후보: '+str(O/'hpo_results.csv')+'\n교차표현 Validation: '+str(O/'jobs.json')+'\n기존 모델·Test·Stage4 결과는 변경하지 않음. seed42는 탐색과 중복되어 선택 편향 가능. RNG는 기존 worker Python random/getrandbits 구현 유지. 독립 blind Test 미실행.\n')
 with (R/'docs/PROJECT_STATE.md').open('a') as f:f.write('\n\n## '+now()+' — C 공통 HPO 자동 실행 종료\n\n- 상태 '+state+'; 보고서 `reports/c_common_hpo_final_20261111_v01.md`; 원본 '+str(O)+'; Test 미사용.\n')
except BaseException as e:
 error('CONTROLLER_BLOCKED',dict(error=repr(e),traceback=traceback.format_exc()));publish('BLOCKED',repr(e));raise
