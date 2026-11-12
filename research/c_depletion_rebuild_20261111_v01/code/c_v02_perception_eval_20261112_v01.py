"""Post-selection C Test only. Reuses original Stage1 AP/matching functions verbatim.
No model/candidate selection, training or motion. Saves runtime Top1 mask separately from GT scoring.
"""
import argparse,ast,csv,json,sys,time
from pathlib import Path
import numpy as np,torch,cv2
from ultralytics import YOLO
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from evaluation.c_depletion_geometry_20261111_v01 import sha
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();O=a.output;O.mkdir(exist_ok=False);started=time.time()
from evaluation.b1_common_hpo_policy_20261111_v01 import gpu_gate
import os
assert gpu_gate((os.getpid(),os.getppid()))['clear']
models=json.loads((a.root/'final_C_models_lock.json').read_text())['models'];frames=json.loads((a.root/'static_frame_index.json').read_text());assert len(models)==9 and len(frames)==2250
THR=np.round(np.arange(.5,.96,.05),2);dev='cuda:0'
ns=dict(np=np,torch=torch,THR=THR,dev=dev)
source=R/'analysis/b1_occlusion_eval_20261109_v01.py';nodes=[n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in ['ious','match','ap101']];assert len(nodes)==3;exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
ious,match,ap101=ns['ious'],ns['match'],ns['ap101'];rows=[];cache={};predictions=[]
for model in models:
 assert sha(model['checkpoint'])==model['sha256'];net=YOLO(model['checkpoint']);mk=f"{model['rep']}_s{model['seed']}"
 for er in ['HR_Scan','LR_Scan','GeoCAD']:
  for oc in ['O0','O25','O50']:
   items=[f for f in frames if f['rep']==er and f['O']==oc];assert len(items)==250
   for b in range(0,len(items),16):
    chunk=items[b:b+16]
    for frame,res in zip(chunk,net.predict([f['rgb'] for f in chunk],imgsz=640,conf=.001,iou=.7,max_det=100,retina_masks=True,device=0,verbose=False)):
     G=[cv2.imread(p,0)>0 for p in frame['canonical_masks']];P=cv2.imread(frame['panel'],0)>0 if frame['panel'] else np.zeros((480,640),bool)
     pm=res.masks.data.cpu().numpy().astype(bool) if res.masks is not None else np.zeros((0,480,640),bool);scores=res.boxes.conf.cpu().numpy() if res.boxes is not None else np.zeros(0)
     iou=ious(list(pm),G);use=np.array([g.sum()>=100 for g in G]);target=np.zeros(len(G),bool);target[0]=True;op=scores>=.25;best=float(iou[op,0].max()) if op.any() else 0.;selected=int(np.argmax(np.where(op,scores,-1))) if op.any() else None
     if selected is None:t1=0.;tc='NO_DETECTION';conf=None;onpanel=None
     else:
      t1=float(iou[selected,0]);other=float(iou[selected,1:].max()) if len(G)>1 else 0.;onpanel=float((pm[selected]&P).sum()/max(1,pm[selected].sum()));tc='TARGET' if t1>=.5 else 'OTHER_LOAD' if other>=.5 else 'PANEL' if onpanel>=.5 else 'POOR_TARGET_MASK' if t1>=.1 else 'BACKGROUND';conf=float(scores[selected])
     key=(mk,er,oc,frame['scene_id']);cache[key]=dict(scores=scores,all=match(scores,iou,use,~use),target=match(scores,iou,use&target,~(use&target)),npos_all=int(use.sum()),npos_target=int(use[0]),C=frame['C'])
     row=dict(model_rep=model['rep'],seed=model['seed'],eval_rep=er,own=model['rep']==er,O=oc,C=frame['C'],scene_id=frame['scene_id'],family_id=frame['family_id'],target_gt_px=int(G[0].sum()),target_eligible=bool(use[0]),target_detected=bool(op.any() and (iou[op,0]>=.5).any()),oracle_target_iou=best,top1_target_iou=t1,top1_class=tc,top1_conf=conf,predictions_operational=int(op.sum()),actual_occlusion=frame['measured_occlusion'])
     rows.append(row)
     if model['rep']==er:
      folder=O/'selected_masks'/mk/oc;folder.mkdir(parents=True,exist_ok=True);mp=folder/f"{frame['scene_id']}.npz"
      np.savez_compressed(mp,mask=pm[selected] if selected is not None else np.zeros((480,640),bool))
      predictions.append(dict(**row,mask=str(mp),frame=frame,checkpoint_sha256=model['sha256'],runtime_selection='highest confidence >=.25; no GT selection'))
    print(mk,er,oc,'images',min(b+16,len(items)),'wall',round(time.time()-started),flush=True)
 del net;torch.cuda.empty_cache()
aps=[]
for model in models:
 mk=f"{model['rep']}_s{model['seed']}"
 for er in ['HR_Scan','LR_Scan','GeoCAD']:
  for oc in ['O0','O25','O50']:
   for level in ['ALL','C100','C80','C60','C40','C20','ANCHOR_ALL','ANCHOR_C100','ANCHOR_C80','ANCHOR_C60','ANCHOR_C40','ANCHOR_C20']:
    ks=[k for k,c in cache.items() if k[:3]==(mk,er,oc) and ((level.replace('ANCHOR_','')=='ALL' or c['C']==level.replace('ANCHOR_','')) and (not level.startswith('ANCHOR_') or '_OBS' not in k[3]))];out=dict(model_rep=model['rep'],seed=model['seed'],eval_rep=er,O=oc,C=level,attempted_images=len(ks))
    for which in ['all','target']:
     n=sum(cache[k]['npos_'+which] for k in ks);ss=np.concatenate([cache[k]['scores'] for k in ks]) if ks else np.zeros(0);ap=[ap101(ss,np.concatenate([cache[k][which][t] for k in ks]),n) for t in range(10)] if ks else [float('nan')]*10
     out[which+'_GT_denominator']=n;out[which+'_mask_mAP5095']=float(np.mean(ap)) if n else None;out[which+'_mask_mAP50']=float(ap[0]) if n else None
    aps.append(out)
for name,rr in [('per_target.csv',rows),('mask_AP.csv',aps)]:
 with (O/name).open('x',newline='') as f:w=csv.DictWriter(f,rr[0]);w.writeheader();w.writerows(rr)
(O/'pose_inputs.json').write_text(json.dumps(predictions,indent=1));(O/'result.json').write_text(json.dumps(dict(state='COMPLETED',attempted_model_images=len(rows),expected_model_images=20250,models=9,own_pose_inputs=len(predictions),selection_locked_before_Test=True,Test_used_for_selection=False,metric_source_sha256=sha(source),elapsed_seconds=time.time()-started),indent=2));assert len(rows)==20250 and len(predictions)==6750
