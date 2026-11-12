"""Prepare 840 new C100 observations and immutable V02 membership. No renderer/model import."""
import csv,json,hashlib,statistics,collections,time
from pathlib import Path
S=Path('/home/user/hh/isaac_cosmos/sdg_final');B=S/'C_DEPLETION_REBUILD_20261111_v01';V=B/'C_V02_20261112_v01';D=V/'data_design_v01';D.mkdir(exist_ok=False);old=B/'data_design_v01';rows=list(csv.DictReader((old/'scene_manifest.csv').open()));full=[r for r in rows if r['C']=='C100'];train=[r for r in full if r['split']=='train'];extra=[];sources={};sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for r in full:
 values=sorted({float(x['distance_m']) for x in train if x['distance_bin']==r['distance_bin']});assert len(values)>=5
 qs=[values[round((len(values)-1)*q)] for q in [.2,.4,.6,.8,.1,.3,.5,.7,.9,0.,1.]];chosen=[]
 for d in qs:
  if abs(d-float(r['distance_m']))<.005 or any(abs(d-x)<.005 for x in chosen):continue
  chosen.append(d)
  if len(chosen)==4:break
 assert len(chosen)==4
 for i,d in enumerate(chosen,1):
  x=dict(r);x.update(scene_id=r['scene_id']+f'_OBS{i:02d}',observation_id=f'OBS{i:02d}',observation_distance_m=f'{d:.6f}',source_C_V01_scene_id=r['scene_id'],camera_policy='fixed load pose; eye_x=base_zx+base_distance-observation_distance,eye_y=base_zy,z=.6; target same original load center/nominal4height',generation_role='new_C100_RGBD_observation');extra.append(x)
for r in rows:r.update(observation_id='OBS00',observation_distance_m=r['distance_m'],source_C_V01_scene_id=r['scene_id'],camera_policy='original C-V01 unchanged',generation_role='reused_C_V01')
new=rows+extra;assert len(extra)==280 and len(new)==1750 and len({r['scene_id'] for r in new})==1750
for name,rs in [('scene_manifest.csv',new),('additional_C100_manifest.csv',extra),('pilot_manifest.csv',[next(r for r in extra if r['split']=='train')])]:
 with (D/name).open('x',newline='') as f:w=csv.DictWriter(f,list(new[0]));w.writeheader();w.writerows(rs)
for name in ['families.csv','removal_history.csv','shape_duplicates.json','design_QA.json']:(D/name).write_bytes((old/name).read_bytes())
config=json.loads((old/'capture_config.json').read_text());config['version']='C_V02_C100_observation_adapter_v01';config['scene_manifest_sha256']=sha(D/'scene_manifest.csv');config['pilot_manifest_sha256']=sha(D/'pilot_manifest.csv');config['counts']=dict(train=1250,val=250,test=250);config['C_V01_parent_manifest_sha256']=sha(old/'scene_manifest.csv');(D/'capture_config.json').write_text(json.dumps(config,indent=2))
counts=collections.Counter((r['split'],r['C']) for r in new);assert all(counts[sp,c]==n for sp,n in [('train',250),('val',50),('test',50)] for c in ['C100','C80','C60','C40','C20']);assert all(len({r['split'] for r in new if r['family_id']==fam})==1 for fam in {r['family_id'] for r in new})
(V/'execution_v01').mkdir();(V/'execution_v01/logs').mkdir();(D/'V02_design_lock.json').write_text(json.dumps(dict(status='LOCKED_OBSERVATION_DESIGN',created=time.time(),source_C_V01_manifest_sha256=sha(old/'scene_manifest.csv'),new_manifest_sha256=sha(D/'scene_manifest.csv'),additional_manifest_sha256=sha(D/'additional_C100_manifest.csv'),source_families=70,split_families=dict(train=50,val=10,test=10),additional_per_rep=280,additional_all_reps=840,target_all_reps=5250,counts={str(k):v for k,v in counts.items()},camera_condition_values_source='Train full-family distances only, within each existing distance_bin; fixed pre-inference',C100_only_observation_distribution_change_disclosed=True,existing_C_HPO_repeated=False,physical_motion_authorized=False),indent=2))
print('V02 design locked; 840 additional captures, existing4410 preserved')
