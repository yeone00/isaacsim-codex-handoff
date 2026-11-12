"""CPU re-decode saved RGB/empty/actual mask and recompute original H1 photometric statistics."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,collections
from pathlib import Path
import cv2,numpy as np
cv2.setNumThreads(1)
E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');O=E/'replicator_rgb_mask_audit_v01';O.mkdir(exist_ok=False);counts=collections.Counter();errors=[];rows=[];cross=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
for c in json.loads((E/'capture_index.json').read_text()):
 p=Path(c['complete']);r=json.loads(p.read_text());A=p.parents[1];sid=r['scene_id'];I=cv2.imread(str(A/'rgb'/f'{sid}.png'));bg=cv2.imread(str(A/'empty'/f'{sid}.png'));diff=np.abs(I.astype(np.int16)-bg.astype(np.int16)).max(2)
 for q in r['visibility_QA']:
  lid=q['load_id'];m=cv2.imread(str(A/'masks_actual'/f'{sid}_Load_{lid:02d}.png'),0)>0;me=cv2.erode(m.astype('uint8'),cross,iterations=2,borderType=cv2.BORDER_CONSTANT,borderValue=0)>0;n=int(me.sum());v=float((diff[me]>q['tau']).mean()) if n else None
  if n!=q['px_e2'] or ((v is None)!=(q['vis_hard_e2'] is None)) or (v is not None and abs(v-q['vis_hard_e2'])>1e-12):errors.append(dict(scene_id=sid,rep=r['rep'],load_id=lid,reason='RGB_EMPTY_MASK_H1_STATISTIC_MISMATCH'))
  counts[q['category']]+=1;rows.append(dict(scene_id=sid,rep=r['rep'],load_id=lid,eroded_mask_pixels=n,stored_tau=q['tau'],visibility=v,category=q['category'],H1_keep=True))
(O/'rows.json').write_text(json.dumps(rows));d=dict(state='PASS_STORED_RGB_MASK_STATISTICS' if not errors else 'REVIEW_REQUIRED',captures=4410,instance_statistics_recomputed=len(rows),errors=errors,original_H1_categories_preserved=dict(counts),limitation='Stored tau reused because original per-frame pallet ID mask was not retained; does not certify absolute visibility or eliminate all temporally stale frames. Original H1 flags remain analysis-only; no sample removal/threshold changes.')
(O/'result.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2))
