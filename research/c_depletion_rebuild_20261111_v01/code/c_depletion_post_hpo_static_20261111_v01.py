"""After immutable C selection: O25/O50 static capture, perception and pose evaluation. No driving."""
import argparse,csv,json,os,sys,subprocess,time,fcntl
from pathlib import Path
import numpy as np
from PIL import Image
from c_depletion_runtime_20261111_v01 import R,sha,atomic,event,proc_alive
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();E=a.root;O=a.output;B=E.parent;O.mkdir(exist_ok=True);started=time.time();registry=E/'static_evaluation_capabilities_v01.json';cap=json.loads(registry.read_text())
assert cap['physical_motion_authorized'] is False
for p,h in cap['code_sha256'].items():assert sha(p)==h,p
H=E/'C_COMMON_HPO_v01';assert json.loads((H/'hpo_status.json').read_text())['state']=='COMPLETED';selection=json.loads((H/'selection_lock.json').read_text());cid=selection['candidate_id'];hjobs=json.loads((H/'jobs.json').read_text());models=[]
for rep in ['HR_Scan','LR_Scan','GeoCAD']:
 for seed in [42,43,44]:
  phase='full' if seed==42 else 'baseline_control' if cid==0 else 'final';j=hjobs[f'{phase}_C{cid:02d}_{rep}_s{seed}'];assert j['state']=='COMPLETED';best=j['best'];assert sha(best['checkpoint'])==best['sha256']
  models.append(dict(rep=rep,seed=seed,checkpoint=best['checkpoint'],sha256=best['sha256'],candidate_id=cid,params=selection['params'],best_epoch=best['epoch']))
lock=dict(status='LOCKED',models=models,selection_sha256=sha(H/'selection_lock.json'),test_used_for_selection=False,source='C dataset common HPO; not old B1/M50')
mf=E/'final_C_models_lock.json'
if mf.exists():assert json.loads(mf.read_text())==lock
else:atomic(mf,lock)
manifest=[r for r in csv.DictReader((B/'data_design_v01/scene_manifest.csv').open()) if r['split']=='test'];assert len(manifest)==210
base_index={(r['rep'],r['scene_id']):r for r in json.loads((E/'capture_index.json').read_text())};frames=[]
def run(key,cmd,out,gpu=False):
 result=Path(out)/'result.json'
 if result.exists():
  d=json.loads(result.read_text());assert d['state'] in ['PASS_CAPTURE','COMPLETED'];return
 assert not Path(out).exists(),'INTERRUPTED_STATIC_JOB_REQUIRES_REVIEW:'+key
 gl=None
 if gpu:gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
 event(B,'STAGE_STARTED',job=key)
 with (E/'logs'/f'{key}.log').open('x') as f:
  child=subprocess.Popen(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONUNBUFFERED='1'))
  print('STATIC_STAGE_STARTED',key,child.pid,flush=True);heartbeat=0
  while child.poll() is None:
   atomic(O/'progress.json',dict(stage=key,worker_pid=child.pid,updated=time.time(),physical_motion=False));time.sleep(10)
   heartbeat+=1
   if heartbeat%6==0:print('STATIC_STAGE_ALIVE',key,child.pid,round(time.time()-started),flush=True)
 if gl:gl.close()
 assert child.returncode==0 and result.exists(),'STATIC_JOB_EXIT_OR_RESULT_FAILURE:'+key
 assert json.loads(result.read_text())['state'] in ['PASS_CAPTURE','COMPLETED'],'STATIC_QA_FAILED:'+key
 event(B,'STAGE_COMPLETED',job=key)
# Train-family-only implementation qualification precedes any C Test occlusion generation.
qual=[]
for rep in ['HR_Scan','LR_Scan','GeoCAD']:
 out=E/'occlusion_qualification_v01'/rep;out.parent.mkdir(exist_ok=True)
 run('C_OCCLUSION_QUALIFICATION_'+rep,['/home/user/anaconda3/envs/hh_isaac51/bin/python',str(R/'scripts/c_depletion_rgbd_capture_20261111_v03.py'),'--anchor-audit',str(B/'asset_anchor_audit_v01/asset_anchor_audit.json'),'--design',str(B/'data_design_v01'),'--manifest',str(B/'data_design_v01/pilot_manifest.csv'),'--rep',rep,'--output',str(out)],out,True)
 for cp in (out/'complete').glob('*.json'):
  rec=json.loads(cp.read_text());assert rec['state']=='PASS_CAPTURE'
  for name,h in rec['files_sha256'].items():assert sha(name)==h
  for oc,z in rec['occlusion'].items():
   gt=np.array(Image.open(out/'masks_canonical'/f'{cp.stem}_Load_01.png'))>0;panel=np.array(Image.open(z['panel']))>0;cov=float((gt&panel).sum()/gt.sum());assert abs(cov-z['nominal'])<=.02 and abs(cov-z['measured'])<1e-12
   qual.append(dict(rep=rep,C=rec['C'],O=oc,measured=cov))
assert len(qual)==30;atomic(E/'occlusion_qualification_QA_v01.json',dict(state='PASS',cases=qual,raw_RGBD_frames=45,source_split='train only',no_model_selection=True))
for family in sorted({r['family_id'] for r in manifest}):
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  rr=[r for r in manifest if r['family_id']==family];key='C_TEST_OCCLUSION_'+family+'_'+rep;out=E/'test_occlusion_v01'/key;out.parent.mkdir(exist_ok=True);mp=E/'job_manifests'/f'{key}.csv'
  if not mp.exists():
   with mp.open('x',newline='') as f:w=csv.DictWriter(f,list(rr[0]));w.writeheader();w.writerows(rr)
  run(key,['/home/user/anaconda3/envs/hh_isaac51/bin/python',str(R/'scripts/c_depletion_rgbd_capture_20261111_v03.py'),'--anchor-audit',str(B/'asset_anchor_audit_v01/asset_anchor_audit.json'),'--design',str(B/'data_design_v01'),'--manifest',str(mp),'--rep',rep,'--output',str(out)],out,True)
  for r in rr:
   sid=r['scene_id'];orig=Path(base_index[rep,sid]['complete']);old=json.loads(orig.read_text());base=orig.parents[1];new=json.loads((out/'complete'/f'{sid}.json').read_text());assert new['state']=='PASS_CAPTURE'
   for name,h in new['files_sha256'].items():assert sha(name)==h
   oldT=json.loads((base/'camera'/f'{sid}.json').read_text())['calibration']['T_world_optical'];newT=json.loads((out/'camera'/f'{sid}.json').read_text())['calibration']['T_world_optical'];assert np.array_equal(np.array(oldT),np.array(newT)),'OCCLUSION_CAMERA_CHANGED'
   for lid in range(1,int(r['load_count'])+1):assert np.array_equal(np.array(Image.open(base/'masks_canonical'/f'{sid}_Load_{lid:02d}.png')),np.array(Image.open(out/'masks_canonical'/f'{sid}_Load_{lid:02d}.png'))),'OCCLUSION_REFERENCE_GT_CHANGED'
   gt=old['GT_eval_only']['target'];common=dict(rep=rep,scene_id=sid,C=r['C'],family_id=family,GT_eval_only_target=gt)
   frames.append(dict(**common,O='O0',rgb=str(base/'rgb'/f'{sid}.png'),depth=str(base/'depth'/f'{sid}.npy'),camera=str(base/'camera'/f'{sid}.json'),canonical_masks=[str(base/'masks_canonical'/f'{sid}_Load_{i:02d}.png') for i in range(1,int(r['load_count'])+1)],panel=None,measured_occlusion=0.))
   for oc in ['O25','O50']:
    z=new['occlusion'][oc];assert z['achieved'] and z['actual_same_frame_panel'];target=np.array(Image.open(base/'masks_canonical'/f'{sid}_Load_01.png'))>0;panel=np.array(Image.open(z['panel']))>0;assert abs(float((target&panel).sum()/target.sum())-z['measured'])<1e-12
    for lid,mp in enumerate(z['canonical_visible_masks'],1):assert np.array_equal(np.array(Image.open(mp))>0,(np.array(Image.open(base/'masks_canonical'/f'{sid}_Load_{lid:02d}.png'))>0)&~panel),'OCCLUSION_VISIBLE_GT_MISMATCH'
    frames.append(dict(**common,O=oc,rgb=z['rgb'],depth=z['depth'],camera=z['camera'],canonical_masks=z['canonical_visible_masks'],panel=z['panel'],measured_occlusion=z['measured']))
assert len(frames)==1890;atomic(E/'static_frame_index.json',frames)
run('C_PERCEPTION_TEST',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'analysis/c_depletion_perception_eval_20261111_v01.py'),'--root',str(E),'--output',str(E/'perception_eval_v01')],E/'perception_eval_v01',True)
run('C_POSE_STATIC',['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'analysis/c_depletion_pose_eval_20261111_v01.py'),'--root',str(E),'--output',str(E/'pose_eval_v01')],E/'pose_eval_v01')
pose=json.loads((E/'pose_eval_v01/result.json').read_text());assert not pose['pipeline_errors']
atomic(O/'result.json',dict(state='COMPLETED',models=9,test_frames=1890,perception=str(E/'perception_eval_v01/result.json'),pose=str(E/'pose_eval_v01/result.json'),physical_stages='HOLD',physical_runs=0,physical_site_datum_certification='UNKNOWN',elapsed_seconds=time.time()-started))
summary=dict(dataset_QA=json.loads((E/'dataset_QA_v01/result.json').read_text()),HPO=json.loads((H/'final_summary.json').read_text()),perception=json.loads((E/'perception_eval_v01/result.json').read_text()),pose=pose)
report=R/'reports/c_depletion_static_pipeline_results_20261111_v01.md'
report.write_text('# C 데이터·공통 HPO·인식/pose 정적 평가 자동 결과\n\n'+json.dumps(summary,indent=2,ensure_ascii=False)+'\n\n원본 지표: '+str(E/'perception_eval_v01/mask_AP.csv')+' / '+str(E/'perception_eval_v01/per_target.csv')+' / '+str(E/'pose_eval_v01/summary.json')+'\n\nC_ROBUST 후보는 sensor 높이와 공통 design support=.144m prior를 사용하며 GT잔여층/slot/pose를 입력하지 않았다. 실제현장 datum 인증 및 물리충돌/정지/성공 기준 검증은 UNKNOWN/HOLD. 신규 물리 주행0, 예정300/별도150의 결과가 아니다. seed42는 탐색 중복이며3seed SD는 환경독립성을 증명하지 않는다. 데이터는70 source families이고 C/Test210행은10 families의관련상태다.\n')
with (R/'docs/PROJECT_STATE.md').open('a') as f:f.write('\n\n## '+time.strftime('%Y-%m-%d %H:%M:%S')+' — C 정적 파이프라인 자동 완료\n\n- 보고서 `reports/c_depletion_static_pipeline_results_20261111_v01.md`; 데이터/HPO/인식/pose 원본 '+str(E)+'. 물리pilot/300/150은별도gate미충족으로HOLD/실행0.\n')
