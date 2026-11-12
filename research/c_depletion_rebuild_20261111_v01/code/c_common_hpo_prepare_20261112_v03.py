"""CPU-only preparation; immutable candidate, code and train/validation manifests."""
import argparse,ast,importlib.metadata,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation.c_common_hpo_policy_20261111_v01 import *
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();O=a.root.resolve()
assert not O.exists();gate=gpu_gate();assert gate['clear'],gate
rc=json.loads(BASE_RECIPE.read_text());assert sha(BASE_RECIPE)==BASE_SHA
assert sha(rc['model']['weights'])==rc['model']['sha256']
package=Path(rc['data']['package']);assert sha(package/'package_checks.json')==rc['data']['package_checks_sha256']
import optuna
assert importlib.metadata.version('ultralytics')==rc['software']['ultralytics']
assert importlib.metadata.version('torch')==rc['software']['torch']
import importlib.util
ulroot=Path(importlib.util.find_spec('ultralytics').origin).parent
for name,h in rc['software']['ultralytics_source_sha256'].items():assert sha(ulroot/name)==h,name
for name,h in {**rc['amendment']['module'],**rc['custom_photometric']['module']}.items():assert sha(R/name)==h
study=optuna.create_study(direction='maximize',sampler=optuna.samplers.RandomSampler(seed=20261112))
legacy=S/'B1_COMMON_HPO_20261111_v01'
import csv
legacy_rows=list(csv.DictReader((legacy/'hpo_results.csv').open()));legacy_params=json.loads((legacy/'candidates.json').read_text())
ranked=sorted([x for x in legacy_rows if int(x['candidate_id'])!=0 and x['full_score']],key=lambda x:(-float(x['full_score']),int(x['candidate_id'])))
candidates=[dict(id=0,params=BASE,origin='frozen_baseline')]
for x in ranked[:3]:
 cid=int(x['candidate_id']);params=legacy_params[cid]['params'];validate_params(params)
 candidates.append(dict(id=len(candidates),params=params,origin='L-HPO full200 C%02d parameters only; no trained weights'%cid))
assert any(c['origin'].startswith('L-HPO full200 C05') for c in candidates),'MANDATORY_LEGACY_C05_MISSING'
while len(candidates)<12:
 t=study.ask();params={k:t.suggest_float(k,lo,hi,log=log) for k,(lo,hi,log) in SPACE.items()};validate_params(params)
 assert all(params!=c['params'] for c in candidates)
 candidates.append(dict(id=len(candidates),params=params,origin='Optuna RandomSampler seed20261112; pre-generated before C performance'))
manifest=dict(by_rep={});members={}
for rep in REPS:
 assert sha(package/rep/'data.yaml')==rc['data']['data_yaml_sha256'][rep]
 files={};members[rep]={}
 for split,n in [('train',1050),('val',210)]:
  images=sorted(f for f in (package/rep/'images'/split).iterdir() if f.suffix.lower() in ['.png','.jpg','.jpeg'])
  labels=sorted((package/rep/'labels'/split).glob('*.txt'));assert len(images)==len(labels)==n
  assert {f.stem for f in images}=={f.stem for f in labels}
  members[rep][split]=[f.stem for f in images]
  for f in images+labels:files[str(f)]=sha(f)
  reg=json.loads((package/'bitmap_registry.json').read_text())
  for im in images:
   for mp in reg[str(im.resolve())]['masks']:files[mp]=sha(mp)
 manifest['by_rep'][rep]=files
# Paired representations use identical scene membership.
assert all(members[r]==members[REPS[0]] for r in REPS)
sources=[R/'evaluation/c_common_hpo_policy_20261111_v01.py',*[R/'scripts'/f'c_common_hpo_{k}_20261112_v03.py' for k in ['train','crossval','controller','prepare']],R/'scripts/c_depletion_bitmap_adapter_20261112_v01.py']
for p in sources:ast.parse(p.read_text())
# Meaningful CPU policy tests: completeness, bounds, finite metric and equal weighting.
assert abs(common_score(dict(zip(REPS,[.1,.4,.7])))-.4)<1e-12
for scores in [{REPS[0]:.1},dict(zip(REPS,[.1,.2,float('nan')]))]:
 try:common_score(scores)
 except ValueError:pass
 else:raise AssertionError('INVALID_OBJECTIVE_NOT_REJECTED')
for c in candidates:validate_params(c['params'])
assert candidates[0]['params']==BASE and len(candidates)==12
assert len({json.dumps(c['params'],sort_keys=True) for c in candidates})==12
O.mkdir();(O/'logs').mkdir();(O/'runs').mkdir();(O/'attempt_history').mkdir()
atomic(O/'preflight.json',dict(state='PASS',gate=gate,software={k:importlib.metadata.version(k) for k in ['ultralytics','torch','optuna']},free_disk_bytes=__import__('shutil').disk_usage(O).free,cpu_policy_checks='PASS',paired_train_val_membership=True,source_AST=True))
atomic(O/'candidates.json',candidates);atomic(O/'train_val_inputs.json',manifest);atomic(O/'scene_membership.json',members)
atomic(O/'code_lock.json',{str(p):sha(p) for p in sources})
p=dict(status='LOCKED',created=time.time(),root=str(O),python=sys.executable,session='c_common_hpo_20261111_v01',base_recipe_sha256=BASE_SHA,code_lock_sha256=sha(O/'code_lock.json'),candidates_sha256=sha(O/'candidates.json'),train_val_inputs_sha256=sha(O/'train_val_inputs.json'),sampler='Optuna RandomSampler',sampler_seed=20261112,training_seed_screen=42,training_seeds_confirm=[42,43,44],dataset_seed='original frozen package scene membership; no resampling or new split',candidate_count=12,space=SPACE,baseline=BASE,screen_epochs=60,schedule_epochs=200,promote='top3 new complete candidates + baseline; ties lowest id',final_seed42_checkpoint='own Validation MASK mAP50-95 unrounded, strict greater; ties earliest epoch',max_training_jobs=57,max_model_epochs=5766,budget='3 smoke*2 + 36 screen*60 + 12 full*200 + 6 selected seed-repeat*200; selected full seed42 reused; no automatic retries or added candidates',objective='equal mean of all three own representation Val Mask mAP50-95; failed triplet ineligible',rng_policy='UNCHANGED v04 locked PhotoDegrade implementation: Python global random seeded per Ultralytics worker; Gaussian noise uses numpy.default_rng(random.getrandbits(32)); NOT documented per-sample (seed,epoch,index) generator. Same workers=8 and fixed run seed. No RNG repair; fresh baseline controls share implementation. Exact bitwise cross-machine reproducibility not claimed.',test_access=False,realval_access=False,validation_policy='B1 own Val200 Q1 best_val_maskmAP5095 checkpoint criterion retained; historical realval/combined checkpoints not HPO objectives and no extra realval inference; cross-rep Val secondary after immutable selection',resume_policy='verify completed outputs; interrupted attempts require --resume-interrupted and restart from same pretrained in new attempt; preserve prior attempts; no silent retry; failed baseline or qualification halts',short_training_limit='stop after60 with epochs=200 schedule; promoted runs fresh pretrained at200, not resume. Short ranking may miss late improvers.',resource_guard='one GPU job; flock; existing driving and GPU owner check; 25GiB disk reserve')
atomic(O/'protocol.json',p)
print(json.dumps(dict(root=str(O),protocol_sha256=sha(O/'protocol.json'),preflight='PASS'),indent=2))
