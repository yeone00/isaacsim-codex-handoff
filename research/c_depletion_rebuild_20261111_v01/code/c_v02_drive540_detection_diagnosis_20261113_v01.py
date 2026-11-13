"""Offline saved-RGBD diagnosis. Original thresholds unchanged; low-conf outputs DIAGNOSTIC ONLY. No rendering/motion/training."""
import sys,json,csv,time,fcntl,hashlib,itertools,statistics,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));V=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01');D=V/'DRIVE540_20261113_v01';O=D/'perception_diagnosis_20261113_v01';O.mkdir(exist_ok=False);gl=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gl,fcntl.LOCK_EX|fcntl.LOCK_NB)
import numpy as np,cv2,torch
from PIL import Image,ImageDraw
from ultralytics import YOLO
from evaluation.c_v02_task_layer_prior_20261112_v02 import estimate as estimate_with_task_prior
# resolve actual function name without importing legacy main
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,d):
 p=O/n;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(d,indent=2,default=lambda v:v.tolist() if hasattr(v,'tolist') else str(v)))
sel=json.loads((V/'MIX_C06_20261112_v01/selection_lock.json').read_text());models={m['rep']:m for m in sel['models'] if m['seed']==42};loaded={};results=[];panels=[]
for rep,m in models.items():assert sha(m['checkpoint'])==m['sha256'];loaded[rep]=YOLO(m['checkpoint'])
def predict(im,rep,conf=.25):return loaded[rep].predict(source=im,imgsz=640,conf=conf,iou=.7,max_det=100,retina_masks=True,device=0,verbose=False)[0]
def extract(pred):
 rows=[]
 if pred.boxes is not None:
  for i,b in enumerate(pred.boxes):rows.append(dict(index=i,confidence=float(b.conf[0]),class_id=int(b.cls[0]),class_name=pred.names[int(b.cls[0])],xyxy=b.xyxy[0].cpu().tolist(),mask_area=int((pred.masks.data[i]>.5).sum()) if pred.masks is not None else None))
 return rows
registry=json.loads((V/'execution_v01/C_BITMAP_PACKAGE_v01/bitmap_registry.json').read_text());pkg=list(csv.DictReader((V/'execution_v01/C_BITMAP_PACKAGE_v01/records.csv').open()));sources=[]
full=D/'recovery_e2e_v01/pilot/C2D_B01_C100_HR_Scan_O0/attempt_0001'
for C in ['C100','C80','C60','C40','C20']:
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  capture=full if C=='C100' and rep=='HR_Scan' else D/'stationary_qualification_attempt06'/(C+'_'+rep)
  sources.append(dict(key='rover_'+C+'_'+rep,kind='saved_physical_robot_camera',rep=rep,C=C,split='technical_pilot_or_basic',rgb=str(capture/'front_rgb.png'),depth=str(capture/'front_depth.npy'),camera=str(capture/'camera_metadata.json'),capture=str(capture)))
for split in ['train','val','test']:
 r=next(r for r in pkg if r['rep']=='HR_Scan' and r['C']=='C100' and r['split']==split)
 sources.append(dict(key='static_HR_C100_'+split,kind='static_O0_reference',rep='HR_Scan',C='C100',split=split,rgb=r['image'],complete=r['complete']))
for s in sources:
 rgb=np.array(Image.open(s['rgb']).convert('RGB'));bgr=rgb[:,:,::-1].copy();key=s['key'];pred=predict(bgr,s['rep']);dets=extract(pred);r=dict(**s,RGB_sha256=sha(s['rgb']),checkpoint=models[s['rep']]['checkpoint'],checkpoint_sha256=models[s['rep']]['sha256'],operational_settings=dict(imgsz=640,conf=.25,NMS_IoU=.7,max_det=100,retina_masks=True),operational_detections=dets,operational_detection_count=len(dets),global_luminance_mean=float(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY).mean()),RGB_PNG_array_exact=None,diagnostic_low_conf_NOT_operational=False)
 Image.fromarray(cv2.cvtColor(pred.plot(),cv2.COLOR_BGR2RGB)).save(O/(key+'_operational_overlay.png'))
 if s['kind']=='saved_physical_robot_camera':
  capture=Path(s['capture']);arr=np.load(capture/'front_rgb.npy');r['RGB_PNG_array_exact']=bool(np.array_equal(rgb,arr));r['cv2_BGR_equals_RGB_reversed']=bool(np.array_equal(cv2.imread(s['rgb']),bgr));dep=np.load(s['depth']);r['depth_valid_pixels']=int(np.count_nonzero(np.isfinite(dep)&(dep>0)));r['RGB_shape']=list(rgb.shape);r['depth_shape']=list(dep.shape);r['camera_calibration']=json.loads(Path(s['camera']).read_text())['calibration']
  pose=None
  if dets:
   picked=max((x for x in dets if x['class_name']=='brick_load'),key=lambda x:(x['confidence'],-x['index']),default=None)
   if picked is not None and pred.masks is not None:
    mask=(pred.masks.data[picked['index']].cpu().numpy()>.5);mask=cv2.resize(mask.astype('uint8'),(640,480),interpolation=cv2.INTER_NEAREST).astype(bool);np.save(O/(key+'_selected_mask.npy'),mask);task=dict(schema='C_V02_TASK_LAYER_PRIOR_v01',task_id=key,task_layer_count=dict(C100=4,C80=4,C60=3,C40=2,C20=1)[s['C']],provider='operator_or_task_management_system');pose=estimate_with_task_prior(mask,dep,Path(s['camera']).read_text(),task)
  r['ROBUST_A']=pose;r['pose_state']='NOT_RUN_NO_OPERATIONAL_MASK' if pose is None else pose.get('status');r['mask_quality_GT_IoU']='NOT_COMPUTED_NO_EXACT_physical_GT_bitmap; do not use projected bbox as mask'
 else:
  mask=Image.open(registry[s['rgb']]['masks'][0]);m=np.array(mask)>0;y,x=np.where(m);r['target_GT_pixels']=int(m.sum());r['target_bbox_xyxy']=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];r['target_luminance_mean']=float(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)[m].mean());r['target_rgb_mean']=rgb[m].mean(0).tolist();r['target_frame_fraction']=float(m.mean());r['source_metadata']=json.loads(Path(s['complete']).read_text()).get('scene_id')
 if s['rep']=='HR_Scan' and (s['C']=='C100'):
  low=predict(bgr,s['rep'],.001);r['diagnostic_low_conf_NOT_operational']=True;r['low_conf_001_detections_DIAGNOSTIC_ONLY']=extract(low);Image.fromarray(cv2.cvtColor(low.plot(),cv2.COLOR_BGR2RGB)).save(O/(key+'_low_conf_DIAGNOSTIC_ONLY.png'))
  pilpred=predict(Image.fromarray(rgb),s['rep']);r['PIL_RGB_vs_numpy_BGR_same_detections']=bool(len(extract(pilpred))==len(dets) and all(abs(a['confidence']-b['confidence'])<1e-6 and np.allclose(a['xyxy'],b['xyxy'],atol=1e-4) for a,b in zip(extract(pilpred),dets)))
 dump(key+'.json',r);results.append(r);thumb=Image.open(O/(key+'_operational_overlay.png')).convert('RGB').resize((480,360));panel=Image.new('RGB',(480,390),'white');panel.paste(thumb,(0,30));ImageDraw.Draw(panel).text((8,8),key+' detections='+str(len(dets)),fill='black');panels.append(panel);print(key,'dets',len(dets),'pose',r.get('pose_state'),'low',len(r.get('low_conf_001_detections_DIAGNOSTIC_ONLY',[])),flush=True)
# HR pilot observation diagnostics use evaluation-only bbox AFTER all model calls. Never used to select/repair a mask.
r=results[0];gt=json.loads((full/'eval_gt_only/gt_geometry_eval_only.json').read_text());bb=gt['load_bbox_world'];cal=r['camera_calibration'];T=np.array(cal['T_world_optical']);points=np.array(list(itertools.product(*zip(bb[0],bb[1]))));cam=(np.column_stack([points,np.ones(8)])@np.linalg.inv(T).T)[:,:3];uv=np.column_stack([cal['fx']*cam[:,0]/cam[:,2]+cal['cx'],cal['fy']*cam[:,1]/cam[:,2]+cal['cy']]);lo=np.floor(uv.min(0)).astype(int);hi=np.ceil(uv.max(0)).astype(int);rgb=np.array(Image.open(r['rgb']).convert('RGB'));roi=(slice(max(0,lo[1]),min(480,hi[1])),slice(max(0,lo[0]),min(640,hi[0])));g=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)[roi];dep=np.load(r['depth']);X,Y=np.meshgrid(np.arange(640)+.5,np.arange(480)+.5);cp=np.stack([(X-cal['cx'])/cal['fx']*dep,(Y-cal['cy'])/cal['fy']*dep,dep,np.ones_like(dep)],-1);world=cp@T.T;inside=np.all((world[:,:,:3]>=np.array(bb[0])-.01)&(world[:,:,:3]<=np.array(bb[1])+.01),axis=2)&np.isfinite(dep)&(dep>0);r['evaluation_only_projected_bbox']=dict(xyxy=[*lo.tolist(),*hi.tolist()],width_px=int(hi[0]-lo[0]),height_px=int(hi[1]-lo[1]),clipped=bool(np.any(lo<0) or hi[0]>640 or hi[1]>480),ROI_luminance_mean=float(g.mean()),ROI_luminance_median=float(np.median(g)),ROI_fraction_below20=float((g<20).mean()),depth_points_inside_GT_3D_box_1cm_tolerance=int(inside.sum()),note='bbox diagnostic is not exact mask or operational input')
im=Image.fromarray(rgb);draw=ImageDraw.Draw(im);draw.rectangle([*lo.tolist(),*hi.tolist()],outline='yellow',width=2);im.save(O/'HR_pilot_eval_bbox_DIAGNOSTIC_ONLY.png');dump('rover_C100_HR_Scan.json',r)
cols=3;sheet=Image.new('RGB',(cols*480,((len(panels)+cols-1)//cols)*390),(220,220,220))
for i,p in enumerate(panels):sheet.paste(p,((i%cols)*480,(i//cols)*390))
sheet.save(O/'RGB_operational_comparison_contact_sheet.png');dump('result.json',dict(state='COMPLETED_OFFLINE_DIAGNOSIS',models_modified=False,thresholds_changed_operationally=False,main_counted=0,results=results))
with (O/'representative_15_inference.csv').open('x',newline='') as f:
 rows=[dict(rep=x['rep'],C=x['C'],RGBD_valid=x.get('depth_valid_pixels',0)>0,operational_detections=x['operational_detection_count'],pose_state=x.get('pose_state'),source=x['capture'],RGB_sha256=x['RGB_sha256'],checkpoint_sha256=x['checkpoint_sha256'],path_plan='NOT_RUN_OFFLINE',motion='NOT_RUN_OFFLINE',main_denominator=0) for x in results if x['kind']=='saved_physical_robot_camera'];w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
