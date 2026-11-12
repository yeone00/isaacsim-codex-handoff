"""Static C pose evaluation. All operational inputs exclude GT/C/retained slots.
Nominal4 baselines and NEW sensor-height/common-site-prior candidate are reported distinctly.
"""
import argparse,json,sys,time,csv,math,collections
from pathlib import Path
import numpy as np,cv2
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from evaluation import b1_b5_adapter_20261110_v01 as old
from evaluation import b5_robust_20261110_v01 as rb
from evaluation.c_depletion_robust_sensed_height_20261111_v01 import estimate as sensed
from evaluation.c_depletion_geometry_20261111_v01 import sha
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();O=a.output;O.mkdir(exist_ok=False);started=time.time();inputs=json.loads((a.root/'perception_eval_v01/pose_inputs.json').read_text());rows=[]
for idx,x in enumerate(inputs):
 frame=x['frame'];depth=np.load(frame['depth']);rgb=cv2.imread(frame['rgb'])[:,:,::-1].copy();mask=np.load(x['mask'])['mask'] if x['top1_conf'] is not None else None
 meta=json.loads(Path(frame['camera']).read_text());meta['calibration'].setdefault('provenance',dict(camera_prim='/World/CDepletion/Camera',calibration_sha256=sha(frame['camera']),convention='optical_right_down_forward_world_m_column'));meta['calibration'].setdefault('frame_id',0);meta['calibration'].setdefault('sim_time',0.);text=json.dumps(meta)
 methods=[('ORIG_v44',lambda:old.run_orig_v44(str(idx),rgb,depth,text,mask)[0]),('B1ADAPT_SENSEDTOP_NOMINAL4',lambda:old.run_b1adapt_v01(depth,text,mask,4,'SENSEDTOP')),('B1ADAPT_PRIORTOP_NOMINAL4',lambda:old.run_b1adapt_v01(depth,text,mask,4,'PRIORTOP')),('ROBUST_A_FROZEN_NOMINAL4',lambda:rb.estimate_pose(mask,depth,text,4)),('C_ROBUST_SENSOR_HEIGHT_SITE_PRIOR_v01',lambda:sensed(mask,depth,text))]
 for name,fn in methods:
  error=None
  try:result=fn()
  except Exception as e:result=dict(status='PIPELINE_ERROR',reason=type(e).__name__,pose=None);error=str(e)
  pose=result.get('pose');gt=frame['GT_eval_only_target'];heading=pose.get('heading_deg_180') if pose else None;dx=pose['center_x_m']-gt['center_x_m'] if pose else None;dy=pose['center_y_m']-gt['center_y_m'] if pose else None;angle=math.radians(gt['yaw_deg']);long=dx*math.cos(angle)+dy*math.sin(angle) if pose else None;lat=-dx*math.sin(angle)+dy*math.cos(angle) if pose else None
  rows.append(dict(model_rep=x['model_rep'],seed=x['seed'],C=x['C'],O=x['O'],scene_id=x['scene_id'],family_id=x['family_id'],method=name,target_selected=x['top1_class']=='TARGET',computed=bool(pose),designated_target_computed=bool(pose and x['top1_class']=='TARGET'),status=result.get('status'),reason=result.get('reason'),error=error,XY_error_m=math.hypot(dx,dy) if pose else None,long_error_m=long,lat_error_m=lat,yaw_mod180_error_deg=abs((heading-gt['yaw_deg']+90)%180-90) if heading is not None else None,sensor_inferred_layers=result.get('inferred_layer_hypothesis'),GT_operational_input=False,layer_policy='sensor inferred with common design support prior' if name.startswith('C_ROBUST') else 'nominal4 common prior (no actual C layer provided)'))
  with (O/'pose_records.jsonl').open('a') as f:f.write(json.dumps(dict(input_index=idx,method=name,pose_result=result,mask=x['mask'],depth=frame['depth'],camera=frame['camera'],GT_role='error_scoring_only_after_operational_method',checkpoint_sha256=x['checkpoint_sha256']),default=lambda v:v.tolist() if hasattr(v,'tolist') else str(v))+'\n')
 if idx%20==0:
  print('pose inputs',idx+1,'of',len(inputs),'wall',round(time.time()-started),flush=True)
  with (O/'progress.json').open('w') as f:json.dump(dict(processed=idx+1,total=len(inputs),updated=time.time()),f)
with (O/'per_attempt.csv').open('x',newline='') as f:w=csv.DictWriter(f,rows[0]);w.writeheader();w.writerows(rows)
summary=[]
for key in sorted({(r['model_rep'],r['C'],r['O'],r['method']) for r in rows}):
 rr=[r for r in rows if (r['model_rep'],r['C'],r['O'],r['method'])==key];ok=[r for r in rr if r['designated_target_computed']];s=dict(zip(['rep','C','O','method'],key));s.update(attempts=len(rr),target_selected=sum(r['target_selected'] for r in rr),computed=sum(r['computed'] for r in rr),designated_target_computed=len(ok),failures=dict(collections.Counter(r['reason'] for r in rr if not r['computed'])))
 for metric in ['XY_error_m','long_error_m','lat_error_m','yaw_mod180_error_deg']:
  vv=[r[metric] for r in ok if r[metric] is not None];s[metric+'_mean']=float(np.mean(vv)) if vv else None;s[metric+'_median']=float(np.median(vv)) if vv else None;s[metric+'_p90']=float(np.percentile(vv,90)) if vv else None
 summary.append(s)
errors=sum(r['status']=='PIPELINE_ERROR' for r in rows)
(O/'summary.json').write_text(json.dumps(summary,indent=2));(O/'result.json').write_text(json.dumps(dict(state='COMPLETED' if not errors else 'HOLD_PIPELINE_ERRORS',attempt_rows=len(rows),pose_inputs=len(inputs),GT_operational_input=False,failed_cases_excluded_from_error_mean=True,actual_occupied_C_layers_not_provided=True,new_candidate_uses_common_design_site_support_prior=True,physical_site_datum_certification='UNKNOWN',physical_stages='HOLD',pipeline_errors=errors,elapsed_seconds=time.time()-started),indent=2))
