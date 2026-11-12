"""Review all depth diagnostic outlier instances, compare pixel-center convention and boundary."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,csv,collections
from pathlib import Path
import numpy as np,cv2
cv2.setNumThreads(1)
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation.c_depletion_geometry_20261111_v01 import literal,GT
E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');O=E/'replicator_depth_outlier_review_v01';O.mkdir(exist_ok=False);pat={p:literal(GT,'PATTERN_'+p) for p in ['A','B']};manifest={r['scene_id']:r for r in csv.DictReader((E.parent/'data_design_v01/scene_manifest.csv').open())};cat={(r['rep'],r['scene_id']):r for r in json.loads((E/'capture_index.json').read_text())};rows=[];tot=collections.Counter()
for line in (E/'replicator_output_audit_v01/capture_checks.jsonl').read_text().splitlines():
 r=json.loads(line);bad=[s['load_id'] for s in r['instances'] if s['depth_points_outside_bundle_enclosure_5mm']]
 if not bad:continue
 cp=Path(cat[r['rep'],r['scene_id']]['complete']);d=json.loads(cp.read_text());A=cp.parents[1];sid=r['scene_id'];mrow=manifest[sid];cal=json.loads((A/'camera'/f'{sid}.json').read_text())['calibration'];T=np.array(cal['T_world_optical']);dep=np.load(A/'depth'/f'{sid}.npy');keep={k['layer']-1:set(k['bundle_ids']) for k in json.loads(mrow['mask_by_layer_json'])};cubes=[]
 for l,ph in enumerate(mrow['layer_phase']):
  for bid,(cx,cy,ori) in enumerate(pat[ph],1):
   if bid not in keep[l]:continue
   nx,ny=(2,3) if ori=='S' else (3,2);cubes.append((np.array([-.475+(cx+nx/2)*.095,-.4275+(cy+ny/2)*.095,.144+l*.09+.045]),np.array([nx*.095/2,ny*.095/2,.045])))
 for lid in bad:
  mask=cv2.imread(str(A/'masks_actual'/f'{sid}_Load_{lid:02d}.png'),0)>0;inner=cv2.erode(mask.astype('uint8'),cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)),iterations=2,borderType=cv2.BORDER_CONSTANT,borderValue=0)>0;y,x=np.where(mask&np.isfinite(dep)&(dep>0));sel=np.linspace(0,len(x)-1,min(len(x),128),dtype=int);x=x[sel];y=y[sel];z=dep[y,x];g=d['GT_eval_only']['all_loads'][lid-1];a=np.deg2rad(g['yaw_deg']);rot=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1.]]);origin=np.array([g['center_x_m'],g['center_y_m'],g['floor_z_m']]);res=dict(scene_id=sid,rep=r['rep'],load_id=lid,sampled=len(x))
  for offset in [0.,.5]:
   p=np.c_[(x+offset-cal['cx'])*z/cal['fx'],(y+offset-cal['cy'])*z/cal['fy'],z];local=(p@T[:3,:3].T+T[:3,3]-origin)@rot;distance=np.full(len(x),np.inf)
   for ctr,half in cubes:distance=np.minimum(distance,np.maximum(np.abs(local-ctr)-half,0).max(1))
   outside=distance>.005;inter=inner[y,x];key='integer_pixel' if offset==0 else 'half_pixel_center';res[key]=dict(outside=int(outside.sum()),interior_outside=int((outside&inter).sum()),boundary_outside=int((outside&~inter).sum()),max_outside_m=float(distance.max()),outlier_depth_range=[float(z[outside].min()),float(z[outside].max())] if outside.any() else None)
   tot[key+'_outlier_points']+=int(outside.sum());tot[key+'_interior_outlier_points']+=int((outside&inter).sum());tot[key+'_instances_with_interior_outlier']+=int((outside&inter).any())
  rows.append(res)
(O/'instances.json').write_text(json.dumps(rows,indent=2));result=dict(state='DIAGNOSTIC_REVIEW',instances_reviewed=len(rows),counts=dict(tot),interpretation='Diagnostic tolerance5mm unchanged; boundary-vs-interior and integer-vs-half-pixel interpretations reported separately. No data filtering or model changes.')
(O/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
