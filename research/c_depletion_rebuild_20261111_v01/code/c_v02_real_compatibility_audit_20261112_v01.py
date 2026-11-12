"""CPU source/label/split audit. Does not revise original target-only Roboflow annotations."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import json,hashlib,re,collections
import cv2,numpy as np
cv2.setNumThreads(1)
R=Path(__file__).resolve().parents[1];S=Path('/home/user/hh/isaac_cosmos');REAL=S/'real_benchmark/cvut_pallets_bricks_original_v01/yolo_real_v01';V=S/'sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01';O=V/'real_compatibility_audit_v01';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();rows=[];errors=[];filegroups=collections.defaultdict(set);pixelgroups=collections.defaultdict(set);sourcegroups=collections.defaultdict(set)
for sp,n in [('train',352),('val',48),('test',189)]:
 fs=sorted(p for p in (REAL/'images'/sp).iterdir() if p.suffix.lower() in ['.jpg','.png','.jpeg']);assert len(fs)==n
 for p in fs:
  im=cv2.imread(str(p));assert im is not None;h,w=im.shape[:2];lab=REAL/'labels'/sp/(p.stem+'.txt');assert lab.exists();ph=hashlib.sha256(im.tobytes()).hexdigest();filegroups[sha(p)].add(sp);pixelgroups[ph].add(sp);m=re.match(r'CVUT_(\d+)_[AB]_',p.name);source=m[1] if m else p.stem;sourcegroups[source].add(sp);num=0
  if sp!='test':
   for line in lab.read_text().splitlines():
    if not line.strip():continue
    z=list(map(float,line.split()));coords=np.array(z[1:]);num+=1
    if z[0]!=0 or len(coords)<6 or len(coords)%2 or not np.isfinite(coords).all() or (coords<0).any() or (coords>1).any():errors.append(dict(image=str(p),reason='CLASS_OR_POLYGON_INVALID'))
  rows.append(dict(split=sp,image=str(p),image_sha256=sha(p),decoded_pixel_sha256=ph,label=str(lab),label_sha256=sha(lab),source_frame_id=source,shape=[h,w],instances=num if sp!='test' else None))
for name,g in [('file',filegroups),('decoded_pixel',pixelgroups),('source_frame',sourcegroups)]:
 for k,v in g.items():
  if len(v)>1:errors.append(dict(kind=name,key=k,splits=sorted(v),reason='CROSS_SPLIT_LEAKAGE'))
parent=R/'docs/b1_mixing_experiment_protocol_LOCKED_v03_20261108.json';lock=json.loads(parent.read_text());assert lock['status']=='LOCKED'
result=dict(state='PASS_WITH_DISCLOSED_ANNOTATION_DOMAIN_LIMITATIONS' if not errors else 'HOLD',counts={sp:sum(r['split']==sp for r in rows) for sp in ['train','val','test']},class_id=0,class_name='brick_load',original_target_only_annotation_preserved=True,known_unlabelled_other_loads_and_merged_instances=True,supplementary_unapproved_labels_not_used=True,annotation_policy_authority=str(parent),authority_sha256=sha(parent),material_limit=lock['material_limitation'],real_Test_previously_evaluated=True,real_Test_not_fresh_blind=True,Test_labels_only_hashed_not_used_for_model_selection=True,errors=errors)
(O/'inventory.json').write_text(json.dumps(rows,indent=2));(O/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
