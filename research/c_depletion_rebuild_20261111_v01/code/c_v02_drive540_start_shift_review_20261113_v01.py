"""CPU-only conditional rigid-relocation/bounding/projection review. No Kit, models or operational code.
GT bounding boxes used only for evaluation diagnostics, never generated runtime inputs.
"""
import pathlib,json,csv,math,hashlib,itertools,collections
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1];O=R/'reports/c_v02_drive540_start_shift_review_20261113_v01';O.mkdir(exist_ok=False)
V=pathlib.Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01');D=V/'DRIVE540_20261113_v01';manifest=D/'single_load_amendment_v01/attempt_manifest.csv';protocol=D/'single_load_amendment_v01/protocol.json'
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
inputs={str(p):sha(p) for p in [manifest,protocol,V/'data_design_v01/scene_manifest.csv',R/'analysis/stage3_local_planner_20261109_v01.py',R/'evaluation/b5_robust_20261110_v01.py']}
rows=list(csv.DictReader(manifest.open()));bases={r['base_id']:r for r in rows};sources=json.load(open(D/'technical_e2e_v03/pilot_records.json'));references={};provenance=[]
def write(n,rr):
 with (O/n).open('x',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def corners(bounds):return np.array(list(itertools.product(*zip(*bounds))))
def pose_matrix(p):
 c,s=math.cos(p[3]),math.sin(p[3]);T=np.array([[c,-s,0,p[0]],[s,c,0,p[1]],[0,0,1,p[2]],[0,0,0,1]],float);return T
for r in sources:
 p=pathlib.Path(r['run_dir'])/'attempt_0001';parts=r['attempt_id'].split('_');C=parts[2];rep='HR_Scan' if 'HR_Scan' in r['attempt_id'] else 'LR_Scan' if 'LR_Scan' in r['attempt_id'] else 'GeoCAD'
 ref={n:json.load(open(p/n)) for n in ['camera_metadata.json','capture_stability.json','collision_preflight.json','eval_gt_only/gt_geometry_eval_only.json']};ref['path']=p;references[C,rep]=ref
 for n in ['camera_metadata.json','capture_stability.json','collision_preflight.json','eval_gt_only/gt_geometry_eval_only.json']:
  f=p/n;inputs[str(f)]=sha(f)
ref=references['C100','LR_Scan'];coll=ref['collision_preflight.json'];body=ref['capture_stability.json']['before'];B=pose_matrix(body);inB=np.linalg.inv(B);rover=[r for r in coll['colliders'] if '/ENG_FE2E/Rover/' in r['path'] and r.get('collision_enabled')];floor=[r for r in coll['colliders'] if r['path'] in coll['support_paths']];other=[r for r in coll['colliders'] if '/ENG_FE2E/Rover/' not in r['path'] and '/CV02DriveScene/' not in r['path'] and r['path'] not in coll['support_paths'] and r.get('collision_enabled')]
local=[]
for obj in rover:
 pts=np.c_[corners(obj['bounds']),np.ones(8)];local.append((obj['path'],(inB@pts.T).T[:,:3]))
physical=[];wheels=[];fbox=np.array(ref['eval_gt_only/gt_geometry_eval_only.json']['fixture_bbox_world']);samplepts=np.array([r['xyz'][:2] for r in coll['support_samples']])
for bid,row in sorted(bases.items()):
 for shift in [0.,1.25]:
  P=pose_matrix([float(row['start_x_m']),float(row['start_y_m'])-shift,body[2],math.radians(float(row['start_yaw_deg']))]);pts=np.concatenate([(P@np.c_[q,np.ones(len(q))].T).T[:,:3] for _,q in local]);lo,hi=pts.min(axis=0),pts.max(axis=0)
  gap=np.maximum(0,np.maximum(fbox[0,:2]-hi[:2],lo[:2]-fbox[1,:2]));targetgap=float(np.linalg.norm(gap));insideall=all(lo[0]>=r['bounds'][0][0] and hi[0]<=r['bounds'][1][0] and lo[1]>=r['bounds'][0][1] and hi[1]<=r['bounds'][1][1] for r in floor)
  physical.append(dict(base_id=bid,backshift_y_m=shift,start_x=P[0,3],start_y=P[1,3],yaw_deg=row['start_yaw_deg'],rover_collision_prims=len(rover),rigid_relocation_z_assumed_m=body[2],xmin=lo[0],xmax=hi[0],ymin=lo[1],ymax=hi[1],zmin=lo[2],zmax=hi[2],fixture_AABB_gap_xy_m=targetgap,fixture_AABB_overlap_xy=targetgap==0,within_floor_mesh_AABB_xy=insideall,nonfloor_nontarget_recorded_separate_colliders=len(other),environment_mesh_intersection='UNKNOWN_MESH_AABB_INCLUDES_FLOOR_AND_STRUCTURES',actual_wheel_support='UNKNOWN_NOT_MEASURED_AT_PROPOSED_POSE' if shift else 'ONLY_BASE01_PRIOR_ACTUAL_PROOF',physical_validity='NOT_CERTIFIED'))
  for name,q in local:
   if '_wheel_link/' not in name:continue
   center=(P@np.r_[q.mean(axis=0),1])[:3];near=float(np.min(np.linalg.norm(samplepts-center[:2],axis=1)))
   wheels.append(dict(base_id=bid,backshift_y_m=shift,wheel_path=name,center_x=center[0],center_y=center[1],nearest_Base01_saved_support_ray_distance_xy_m=near,new_raycast_or_contact=False,support_status='UNKNOWN'))
write('base36_conditional_initial_collision_bounds.csv',physical);write('base36_wheel_positions_and_support_evidence_gap.csv',wheels)
projection=[];tests=[]
for row in rows:
 C,rep=row['C'],row['representation'];ref=references[C,rep];cam=ref['camera_metadata.json']['calibration'];T=np.array(cam['T_world_optical']);pb=ref['capture_stability.json']['before'];extrinsic=np.linalg.inv(pose_matrix(pb))@T;bounds=ref['eval_gt_only/gt_geometry_eval_only.json']['load_bbox_world'];points=corners(bounds);center=np.mean(bounds,axis=0);pairs=[]
 for shift in [0.,1.25]:
  P=pose_matrix([float(row['start_x_m']),float(row['start_y_m'])-shift,pb[2],math.radians(float(row['start_yaw_deg']))]);Tc=P@extrinsic;pc=(np.linalg.inv(Tc)@np.c_[points,np.ones(8)].T).T[:,:3];uv=np.c_[cam['fx']*pc[:,0]/pc[:,2]+cam['cx'],cam['fy']*pc[:,1]/pc[:,2]+cam['cy']];lo,hi=uv.min(axis=0),uv.max(axis=0);w,h=hi-lo;cl=np.maximum(lo,[0,0]);ch=np.minimum(hi,[cam['width'],cam['height']]);clipped=max(0,ch[0]-cl[0])*max(0,ch[1]-cl[1]);optcenter=(np.linalg.inv(Tc)@np.r_[center,1])[:3]
  rr=dict(attempt_id=row['attempt_id'],base_id=row['base_id'],C=C,representation=rep,backshift_y_m=shift,camera_x=Tc[0,3],camera_y=Tc[1,3],camera_z=Tc[2,3],camera_to_load_bbox_center_range_m=float(np.linalg.norm(center-Tc[:3,3])),optical_center_depth_m=optcenter[2],depth_min_bbox_m=float(pc[:,2].min()),depth_max_bbox_m=float(pc[:,2].max()),bbox_u_min=lo[0],bbox_v_min=lo[1],bbox_u_max=hi[0],bbox_v_max=hi[1],bbox_width_px=w,bbox_height_px=h,bbox_area_px2=w*h,bbox_screen_area_fraction=w*h/(cam['width']*cam['height']),bbox_fraction_in_frame=clipped/(w*h),all_bbox_corners_in_front=bool(np.all(pc[:,2]>0)),one_pixel_lateral_scale_m=optcenter[2]/cam['fx'],GT_bbox_diagnostic_only=True,terrain_pitch_roll_unchanged_assumption=True,actual_target_visible_pixel_count='UNKNOWN',actual_occlusion='UNKNOWN',new_RGBD_observed=False)
  projection.append(rr);pairs.append(rr)
 projection[-1]['width_ratio_vs_original']=pairs[1]['bbox_width_px']/pairs[0]['bbox_width_px'];projection[-1]['height_ratio_vs_original']=pairs[1]['bbox_height_px']/pairs[0]['bbox_height_px'];projection[-1]['area_ratio_vs_original']=pairs[1]['bbox_area_px2']/pairs[0]['bbox_area_px2']
 for k in ['width_ratio_vs_original','height_ratio_vs_original','area_ratio_vs_original']:projection[-2][k]=1.
 # Rigid transform round-trip check at actual reference pose.
 Tcheck=pose_matrix(pb)@extrinsic;tests.append(float(np.max(np.abs(Tcheck-T))))
write('camera_540_old_vs_shifted_projection_1080.csv',projection)
state=[]
for C in ['C100','C80','C60','C40','C20']:
 for shift in [0.,1.25]:
  a=[r for r in projection if r['C']==C and r['backshift_y_m']==shift]
  state.append(dict(C=C,backshift_y_m=shift,observations=len(a),width_min_px=min(x['bbox_width_px'] for x in a),width_max_px=max(x['bbox_width_px'] for x in a),height_min_px=min(x['bbox_height_px'] for x in a),height_max_px=max(x['bbox_height_px'] for x in a),range_min_m=min(x['camera_to_load_bbox_center_range_m'] for x in a),range_max_m=max(x['camera_to_load_bbox_center_range_m'] for x in a),bbox_min_in_frame_fraction=min(x['bbox_fraction_in_frame'] for x in a),actual_render_or_mask=False))
write('camera_projection_summary_by_C.csv',state)
# Trace all540 membership to C-V02 scene manifest, with split checks (not reassignment).
scenes=list(csv.DictReader((V/'data_design_v01/scene_manifest.csv').open()));byid={r['scene_id']:r for r in scenes};family_splits=collections.defaultdict(set)
for r in scenes:family_splits[r['family_id']].add(r['split'])
lineage=[]
for bid,row in sorted(bases.items()):
 members=[r for r in rows if r['base_id']==bid];matched=[byid.get(r['source_scene_id']) for r in members]
 lineage.append(dict(base_id=bid,source_family=row['source_family'],manifest_source_split=row['source_split'],attempts=len(members),C_levels=len({r['C'] for r in members}),representations=len({r['representation'] for r in members}),all_source_scene_ids_found=all(x is not None for x in matched),source_scene_splits=json.dumps(sorted({x['split'] for x in matched if x})),source_family_splits=json.dumps(sorted(family_splits[row['source_family']])),not_independent_environment=True))
write('base36_Test_lineage_audit.csv',lineage)
new=[r for r in projection if r['backshift_y_m']==1.25];orig=[r for r in projection if r['backshift_y_m']==0];phys=[r for r in physical if r['backshift_y_m']==1.25]
summary=dict(scope='CPU conditional diagnostic only; not new observation or physical certification',main_HOLD=True,new_GPU_or_motion=0,candidate_backshift_m=1.25,candidate_approved=False,planned_attempts=540,bases=36,source_Test_families=len({r['source_family'] for r in rows}),all540_source_scene_memberships_Test=all(byid[r['source_scene_id']]['split']=='test' for r in rows),family_split_leaks=len([k for k in {r['source_family'] for r in rows} if len(family_splits[k])>1]),physical_snapshot_rover_colliders=len(rover),separate_static_environment_nonfloor_colliders=len(other),candidate_target_AABB_overlap_count=sum(x['fixture_AABB_overlap_xy'] for x in phys),candidate_fixture_gap_range_m=[min(x['fixture_AABB_gap_xy_m'] for x in phys),max(x['fixture_AABB_gap_xy_m'] for x in phys)],all_inside_floor_AABB=all(x['within_floor_mesh_AABB_xy'] for x in phys),new_actual_support_or_collision_checks=0,camera_transform_roundtrip_max_error=max(tests),old_center_range_m=[min(x['camera_to_load_bbox_center_range_m'] for x in orig),max(x['camera_to_load_bbox_center_range_m'] for x in orig)],new_center_range_m=[min(x['camera_to_load_bbox_center_range_m'] for x in new),max(x['camera_to_load_bbox_center_range_m'] for x in new)],projected_width_ratio_range=[min(x['width_ratio_vs_original'] for x in new),max(x['width_ratio_vs_original'] for x in new)],projected_area_ratio_range=[min(x['area_ratio_vs_original'] for x in new),max(x['area_ratio_vs_original'] for x in new)],new_bbox_min_in_frame_fraction=min(x['bbox_fraction_in_frame'] for x in new),new_one_pixel_lateral_scale_m=[min(x['one_pixel_lateral_scale_m'] for x in new),max(x['one_pixel_lateral_scale_m'] for x in new)],inputs_sha_before=inputs,inputs_sha_after={p:sha(p) for p in inputs})
assert summary['inputs_sha_before']==summary['inputs_sha_after'];assert max(tests)<1e-12
(O/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if not k.startswith('inputs_')},indent=2))
