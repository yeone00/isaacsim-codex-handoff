"""CPU-only format bridge for previously saved short-check captures. No GT or inference changes."""
import sys,json,hashlib,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
import numpy as np
from evaluation.c_v02_task_layer_prior_20261112_v02 import estimate
from evaluation.b1_b5_adapter_20261110_v01 import _calibration
D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');I=D/'perception_diagnosis_20261113_v01';O=D/'saved_calibration_pose_adapter_v02';O.mkdir(exist_ok=False);orig=json.loads((I/'result.json').read_text());rows=[]
for r in orig['results']:
 if r['kind']!='saved_physical_robot_camera':continue
 key=r['key'];meta=json.loads(Path(r['camera']).read_text());cal=dict(meta['calibration']);derived='raw_parameters' not in meta
 if derived:
  optical=np.array(cal['T_world_optical'],float);scale=np.linalg.norm(optical[:3,:3],axis=0);assert np.all(scale>0);optical[:3,:3]/=scale;assert np.allclose(optical[:3,:3].T@optical[:3,:3],np.eye(3),atol=1e-6),'NON_ORTHOGONAL_CAMERA';cal['T_world_optical']=optical.tolist();usd=optical.copy();usd[:3,:3]=optical[:3,:3]@np.diag([1,-1,-1]);pr=np.zeros((4,4));pr[0,0]=cal['fx']/320;pr[1,1]=cal['fy']/240
  cal['provenance']=dict(calibration_sha256=hashlib.sha256(Path(r['camera']).read_bytes()).hexdigest(),camera_prim='/World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera',scope='derived parser format from recorded measured fx/fy and recorded USD extrinsics, not full raw projection')
  meta=dict(calibration=cal,raw_parameters=dict(cameraProjection=pr.tolist(),cameraViewTransform=np.linalg.inv(usd).T.tolist()),format_bridge=dict(derived=True,removed_USD_camera_scale=scale.tolist(),matches_existing_full_E2E_camera_normalization=True,GT_used=False,projection_non_fx_fy_entries='UNDEFINED_ZERO_NOT_USED_BY_FROZEN_CALIBRATION_PARSER',source=r['camera']))
 text=json.dumps(meta);c,T=_calibration(text);assert abs(c['fx']-cal['fx'])<1e-8 and abs(c['fy']-cal['fy'])<1e-8 and np.allclose(T,np.array(cal['T_world_optical']),atol=1e-12)
 (O/(key+'_camera.json')).write_text(json.dumps(meta,indent=2));mp=I/(key+'_selected_mask.npy');pose=None
 if mp.exists():
  task=dict(schema='C_V02_TASK_LAYER_PRIOR_v01',task_id=key,task_layer_count=dict(C100=4,C80=4,C60=3,C40=2,C20=1)[r['C']],provider='operator_or_task_management_system');pose=estimate(np.load(mp),np.load(r['depth']),text,task)
 row=dict(rep=r['rep'],C=r['C'],operational_detections=r['operational_detection_count'],pose_state='NOT_RUN_NO_MASK' if pose is None else pose['status'],pose_reason='' if pose is None else pose.get('reason'),derived_metadata_format=derived,mask_SHA256=hashlib.sha256(mp.read_bytes()).hexdigest() if mp.exists() else None,calibration_roundtrip_PASS=True,depth_file=r['depth'],main_denominator=0)
 (O/(key+'_pose.json')).write_text(json.dumps(dict(row=row,pose=pose),indent=2,default=str));rows.append(row);print(row['rep'],row['C'],row['pose_state'],row['pose_reason'],flush=True)
with (O/'representative_15_pose.csv').open('x',newline='') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
(O/'result.json').write_text(json.dumps(dict(state='COMPLETED_OFFLINE_POSE_FORMAT_BRIDGE',GT_used=False,source_inputs_modified=False,operational_inference_rerun=False,rows=rows,actual_full_E2E_capture_already_has_raw_parameters=True),indent=2))
