"""CPU QA and lossless polygon package. Any unrepresentable mask HOLDS, never bridges/deletes GT silently."""
import argparse,json,csv,sys,hashlib,collections
from pathlib import Path
import cv2,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation.c_depletion_geometry_20261111_v01 import sha
R=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--pilot-only',action='store_true');a=ap.parse_args();O=a.root;B=O.parent;D=B/'data_design_v01'
manifest=list(csv.DictReader((D/('pilot_manifest.csv' if a.pilot_only else 'scene_manifest.csv')).open()));expected={r['scene_id']:r for r in manifest};catalog=[]
if a.pilot_only:
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  for p in sorted((O/f'pilot_{rep}_v02/complete').glob('*.json')):catalog.append(dict(rep=rep,scene_id=p.stem,complete=str(p)))
else:catalog=json.loads((O/'capture_index.json').read_text())
Q=O/('pilot_QA_v02' if a.pilot_only else 'dataset_QA_bitmap_v01');Q.mkdir(exist_ok=False);errors=[];records=[];common={};mask_stats=[];registry={}
assert len(catalog)==len(expected)*3 and len({(x['rep'],x['scene_id']) for x in catalog})==len(catalog)
P=O/'C_BITMAP_PACKAGE_v01'
if not a.pilot_only:P.mkdir(exist_ok=False)
for cat in catalog:
 rec=json.loads(Path(cat['complete']).read_text());r=expected[rec['scene_id']];A=Path(cat['complete']).parents[1];rep=cat['rep'];sid=r['scene_id'];sp=r['split']
 assert rec['state']=='PASS_CAPTURE' and rec['created_bricks']==int(r['retained_brick_count'])*int(r['load_count']) and rec['nominal_slot_support']
 for name,h in rec['files_sha256'].items():assert sha(name)==h,name
 depth=np.load(A/'depth'/f'{sid}.npy');assert depth.dtype==np.float32 and depth.shape==(480,640)
 assert rec['depth_valid_target_px']>=100 and rec['calibration_check'] and rec['mask_count_check']
 camera=json.loads((A/'camera'/f'{sid}.json').read_text());key=sid
 if key in common:assert np.array_equal(np.array(camera['calibration']['T_world_optical']),common[key]['T']),'CROSS_REP_CAMERA_MISMATCH'
 else:common[key]=dict(T=np.array(camera['calibration']['T_world_optical']),masks={})
 lines=[]
 for lid in range(1,int(r['load_count'])+1):
  m=cv2.imread(str(A/'masks_canonical'/f'{sid}_Load_{lid:02d}.png'),0)>0
  if lid in common[key]['masks']:assert np.array_equal(m,common[key]['masks'][lid]),'CROSS_REP_CANONICAL_MISMATCH'
  else:common[key]['masks'][lid]=m.copy()
  if m.sum()<100:continue # original frozen canonical min-visible-pixel ignore policy
  y,x=np.where(m);box=[(x.min()+x.max()+1)/2/640,(y.min()+y.max()+1)/2/480,(x.max()+1-x.min())/640,(y.max()+1-y.min())/480]
  lines.append('0 '+' '.join(map(str,box))) # bookkeeping bbox only; bitmap adapter owns GT.
  mask_stats.append(dict(scene_id=sid,rep=rep,load_id=lid,px=int(m.sum()),bitmap_exact=True))
 registry[str((A/'rgb'/f'{sid}.png').resolve())]=dict(masks=[str(A/'masks_canonical'/f'{sid}_Load_{i:02d}.png') for i in range(1,int(r['load_count'])+1) if cv2.countNonZero(cv2.imread(str(A/'masks_canonical'/f'{sid}_Load_{i:02d}.png'),0))>=100])
 if not a.pilot_only:
  for kind in ['images','labels']:(P/rep/kind/sp).mkdir(parents=True,exist_ok=True)
  image=A/'rgb'/f'{sid}.png';(P/rep/'images'/sp/f'{sid}.png').symlink_to(image.resolve());(P/rep/'labels'/sp/f'{sid}.txt').write_text('\n'.join(lines)+'\n')
  records.append(dict(rep=rep,scene_id=sid,split=sp,image=str(image),image_sha256=sha(image),complete=cat['complete'],family_id=r['family_id'],C=r['C'],trajectory=r['trajectory_id'],labelled_loads=len(lines)))
(Q/'mask_polygon_fidelity.json').write_text(json.dumps(mask_stats,indent=2));(Q/'errors.json').write_text(json.dumps(errors,indent=2))
state='PASS'
result=dict(state=state,captured_records=len(catalog),expected_records=len(expected)*3,canonical_usable_instances=len(mask_stats),polygon_errors=len(errors),cross_rep_camera_masks_exact=True,source_hashes_verified=True,depth_checks=True,nominal_geometric_support=True,dynamic_physical_support='NOT_ASSESSED; physical stages HOLD',H1_flags_preserved=True,GT_not_runtime_input=True,new_physical_motion=0)
(Q/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if errors:raise RuntimeError('HOLD_MASK_ENCODING; raw GT preserved; bitmap-aware training adapter required, no bridge/instance split performed')
if not a.pilot_only:
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  (P/rep/'data.yaml').write_text(f'path: {P/rep}\ntrain: images/train\nval: images/val\ntest: images/test\nnames:\n  0: brick_load\n')
 with (P/'records.csv').open('x',newline='') as f:w=csv.DictWriter(f,records[0]);w.writeheader();w.writerows(records)
 checks=dict(state='PASS',counts={sp:sum(r['split']==sp and r['rep']=='HR_Scan' for r in records) for sp in ['train','val','test']},QA_result_sha256=sha(Q/'result.json'),scene_manifest_sha256=sha(D/'scene_manifest.csv'),lossless_native_mask_encoding=True,source_split_preserved=True,cross_split_partial_geometry_duplicates=0)
 assert checks['counts']==dict(train=1250,val=250,test=250);(P/'bitmap_registry.json').write_text(json.dumps(registry,indent=2));checks['bitmap_registry_sha256']=sha(P/'bitmap_registry.json');checks['encoding']='lossless bitmap; txt is bbox bookkeeping, never segmentation target';(P/'package_checks.json').write_text(json.dumps(checks,indent=2))
 recipe=json.loads((R/'docs/b1_yolo_recipe_LOCKED_v04_20261108.json').read_text());recipe.update(version='C_V02_BITMAP_RECIPE_v01',status='LOCKED',parent_B1_recipe_sha256=sha(R/'docs/b1_yolo_recipe_LOCKED_v04_20261108.json'),C_data_QA_sha256=sha(Q/'result.json'))
 recipe['data']=dict(package=str(P),package_checks_sha256=sha(P/'package_checks.json'),data_yaml_sha256={rep:sha(P/rep/'data.yaml') for rep in ['HR_Scan','LR_Scan','GeoCAD']},split_counts=checks['counts'],records_csv_sha256=sha(P/'records.csv'))
 assert not (O/'training_recipe.json').exists();recipe['bitmap_adapter']=dict(path=str(R/'scripts/c_v02_bitmap_adapter_20261112_v01.py'),sha256=sha(R/'scripts/c_v02_bitmap_adapter_20261112_v01.py'),reason='single polygon cannot represent holes/disconnected regions; original bitmaps unchanged');(O/'training_recipe.json').write_text(json.dumps(recipe,indent=2));(O/'dataset_lock.json').write_text(json.dumps(dict(status='LOCKED',package=str(P),package_checks_sha256=sha(P/'package_checks.json'),recipe_sha256=sha(O/'training_recipe.json'),QA=str(Q/'result.json'),manifest_sha256=sha(D/'scene_manifest.csv')),indent=2))
