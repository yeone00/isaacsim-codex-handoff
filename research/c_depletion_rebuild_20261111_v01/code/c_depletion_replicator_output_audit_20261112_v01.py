"""Read-only CPU audit of all 4410 saved captures and 210 exception logs. No torch/Isaac imports."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,csv,json,re,datetime,time,collections,hashlib,math,bisect
from pathlib import Path
import cv2,numpy as np
cv2.setNumThreads(1)
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation.c_depletion_geometry_20261111_v01 import literal,GT
R=Path(__file__).resolve().parents[1];E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');O=E/'replicator_output_audit_v01';O.mkdir(exist_ok=False);started=time.time()
patterns={x:literal(GT,'PATTERN_'+x) for x in ['A','B']};manifest={x['scene_id']:x for x in csv.DictReader((E.parent/'data_design_v01/scene_manifest.csv').open())};catalog=json.loads((E/'capture_index.json').read_text());counts=collections.Counter();flags=[];records=[];logcounts=[];timeline=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rotation(yaw):
 a=np.deg2rad(yaw);return np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1.]])
def cuboids(row):
 keep={x['layer']-1:set(x['bundle_ids']) for x in json.loads(row['mask_by_layer_json'])};result=[]
 for l,phase in enumerate(row['layer_phase']):
  for bid,(cx,cy,ori) in enumerate(patterns[phase],1):
   if bid not in keep[l]:continue
   nx,ny=(2,3) if ori=='S' else (3,2)
   ctr=np.array([-.950/2+(cx+nx/2)*.095,-.855/2+(cy+ny/2)*.095,.144+l*.090+.045]);half=np.array([nx*.095/2,ny*.095/2,.045]);result.append((ctr,half))
 return result
# Timestamp every legacy compute exception; exact frame id is absent from retained logs.
for p in sorted((E/'logs').glob('capture_*.log')):
 events=[json.loads(x) for x in (E/'production'/p.stem/'events.jsonl').read_text().splitlines()];sc=[x for x in events if x['state']=='SCENE_STARTED'];begins=[x['time'] for x in sc];bad=[]
 for line in p.read_text(errors='replace').splitlines():
  if 'Assertion raised in compute - setting an array element with a sequence.' not in line:continue
  m=re.match(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)',line);assert m,line[:100]
  t=datetime.datetime.fromisoformat(m[1].replace('Z','+00:00')).timestamp();i=bisect.bisect_right(begins,t)-1
  # logger UTC is only whole-second precision, so boundary association is explicitly approximate.
  sid=sc[i]['scene_id'] if i>=0 else None
  d=dict(log=p.name,UTC_second=m[1],time=t,scene_id_approx=sid,node='Replicator_instance_id_segmentation',frame_id=None,timestamp_resolution_s=1)
  if sid:
   A=E/'production'/p.stem;ar=A/'masks_actual'/f'{sid}_Load_01.png';ca=A/'masks_canonical'/f'{sid}_Load_01.png'
   d['phase_approx']='before_actual_mask_write' if ar.exists() and t<ar.stat().st_mtime else 'between_actual_and_canonical_write' if ca.exists() and t<ca.stat().st_mtime else 'after_canonical_write_or_boundary'
  else:d['phase_approx']='startup_or_scene_boundary'
  timeline.append(d);bad.append(d)
 logcounts.append(dict(log=str(p),sha256=sha(p),exceptions=len(bad)))
with (O/'exception_timeline.jsonl').open('x') as f:
 for d in timeline:f.write(json.dumps(d)+'\n')
# Validate actual saved buffers independently of prior PASS flags.
for idx,cat in enumerate(catalog):
 cp=Path(cat['complete']);d=json.loads(cp.read_text());A=cp.parents[1];sid=d['scene_id'];row=manifest[sid];rep=d['rep'];fail=[]
 for p,h in d['files_sha256'].items():
  if sha(p)!=h:fail.append('FILE_SHA_CHANGED:'+p)
 im=cv2.imread(str(A/'rgb'/f'{sid}.png'));empty=cv2.imread(str(A/'empty'/f'{sid}.png'));depth=np.load(A/'depth'/f'{sid}.npy');cal=json.loads((A/'camera'/f'{sid}.json').read_text())['calibration'];T=np.array(cal['T_world_optical']);inv=np.linalg.inv(T)
 if im is None or im.shape!=(480,640,3) or im.dtype!=np.uint8:fail.append('RGB_INVALID')
 if empty is None or empty.shape!=(480,640,3):fail.append('EMPTY_INVALID')
 if depth.shape!=(480,640) or depth.dtype!=np.float32:fail.append('DEPTH_INVALID')
 if not np.isfinite(T).all() or abs(np.linalg.det(T[:3,:3])-1)>1e-5:fail.append('CAMERA_RIGID_INVALID')
 cubes=cuboids(row);ams=[];cms=[];s=[]
 for lid in range(1,int(row['load_count'])+1):
  am0=cv2.imread(str(A/'masks_actual'/f'{sid}_Load_{lid:02d}.png'),0);cm0=cv2.imread(str(A/'masks_canonical'/f'{sid}_Load_{lid:02d}.png'),0)
  if am0 is None or cm0 is None or am0.shape!=(480,640) or cm0.shape!=(480,640):fail.append('MASK_DECODE');continue
  if not set(np.unique(am0))<={0,255} or not set(np.unique(cm0))<={0,255}:fail.append('MASK_NONBINARY')
  am=am0>0;cm=cm0>0;ams.append(am);cms.append(cm)
  if int(am.sum())!=d['actual_mask_px'][lid-1] or int(cm.sum())!=d['canonical_mask_px'][lid-1]:fail.append('MASK_PIXEL_METADATA_MISMATCH')
  gt=d['GT_eval_only']['all_loads'][lid-1];rot=rotation(gt['yaw_deg']);origin=np.array([gt['center_x_m'],gt['center_y_m'],gt['floor_z_m']]);sil=np.zeros((480,640),np.uint8)
  for ctr,half in cubes:
   xyz=ctr+np.array([[x,y,z] for x in [-1,1] for y in [-1,1] for z in [-1,1]])*half;world=xyz@rot.T+origin;q=(np.c_[world,np.ones(8)]@inv.T)[:,:3]
   if (q[:,2]<=0).any():fail.append('GEOMETRY_BEHIND_CAMERA');continue
   uv=np.c_[cal['fx']*q[:,0]/q[:,2]+cal['cx'],cal['fy']*q[:,1]/q[:,2]+cal['cy']];hull=cv2.convexHull(np.round(uv).astype(np.int32));cv2.fillConvexPoly(sil,hull,1)
  support=cv2.dilate(sil,np.ones((5,5),np.uint8))>0
  outside=int((cm&~support).sum())
  if outside:fail.append('CANONICAL_OUTSIDE_PROJECTED_RETAINED_GEOMETRY')
  # Exhaustive validity count, deterministic spatial subsample for metric 3D containment.
  valid=am & np.isfinite(depth)&(depth>0);invalid=int((am&~valid).sum());y,x=np.where(valid);sel=np.linspace(0,max(len(x)-1,0),min(len(x),128),dtype=int);x=x[sel];y=y[sel];z=depth[y,x];points=np.c_[(x-cal['cx'])*z/cal['fx'],(y-cal['cy'])*z/cal['fy'],z];world=points@T[:3,:3].T+T[:3,3];local=(world-origin)@rot
  near=np.zeros(len(local),bool)
  for ctr,half in cubes:near|=(np.abs(local-ctr)<=half+.005).all(1)
  # This is diagnostic, not a relaxed QA criterion: pixel footprint and .005m enclosure tolerance are recorded.
  if invalid:fail.append('ACTUAL_MASK_INVALID_DEPTH_PIXELS')
  if len(near) and not near.all():counts['sampled_depth_enclosure_outlier_instances']+=1
  s.append(dict(load_id=lid,actual_pixels=int(am.sum()),canonical_pixels=int(cm.sum()),canonical_outside_projected_support_pixels=outside,actual_invalid_depth_pixels=invalid,depth_points_sampled=len(near),depth_points_outside_bundle_enclosure_5mm=int((~near).sum())))
 if ams and (np.stack(ams).sum(0)>1).any():fail.append('ACTUAL_LOAD_OVERLAP')
 if cms and (np.stack(cms).sum(0)>1).any():fail.append('CANONICAL_LOAD_OVERLAP')
 r=dict(scene_id=sid,rep=rep,complete_sha256=sha(cp),rgb_sha256=sha(A/'rgb'/f'{sid}.png'),depth_sha256=sha(A/'depth'/f'{sid}.npy'),flags=sorted(set(fail)),instances=s,RGB_empty_changed_pixels=int((np.abs(im.astype(np.int16)-empty.astype(np.int16)).max(2)>2).sum()))
 records.append(r);counts['captures_checked']+=1;counts['instance_pairs_checked']+=len(s)
 if fail:flags.append(r)
 if idx%100==0:(O/'status.json').write_text(json.dumps(dict(state='RUNNING',checked=idx+1,expected=4410,flagged_captures=len(flags),elapsed=time.time()-started)))
with (O/'capture_checks.jsonl').open('x') as f:
 for r in records:f.write(json.dumps(r)+'\n')
(O/'flags.json').write_text(json.dumps(flags,indent=2));(O/'log_counts.json').write_text(json.dumps(logcounts,indent=2))
state='REVIEW_REQUIRED' if flags else 'PASS_SAVED_ARTIFACT_CHECKS_ROOT_CAUSE_UNRESOLVED'
summary=dict(state=state,counts=dict(counts),flagged_captures=len(flags),flag_types=dict(collections.Counter(x for r in flags for x in r['flags'])),exception_count=len(timeline),exception_phase_counts=dict(collections.Counter(x['phase_approx'] for x in timeline)),logger_precision_seconds=1,exact_render_frame_or_buffer_generation_ids_saved=False,RGB_depth_gt_exact_same_frame_proof='UNKNOWN: raw render frame counters and full uint32 ID buffers were not retained',independent_geometry_check='Canonical masks must be within projected retained Bundle5 boxes, 2-pixel boundary allowance diagnostic. Actual depth sampled128points/instance enclosure +5mm diagnostic, not a changed training/success threshold.',renderer_exception_root_cause='legacy instance annotator warp numpy conversion, precise incompatible buffer/shape condition unresolved; does not independently assert harmlessness',physical_motion=0,GPU_used=False,elapsed_seconds=time.time()-started,source_sha256=sha(__file__))
(O/'result.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
