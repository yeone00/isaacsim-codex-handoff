"""Actual Kit/PhysX stationary qualification. NEVER publishes nonzero control or launches a drive."""
import sys,os,argparse,json,time,traceback,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));ap=argparse.ArgumentParser();ap.add_argument('--row',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();row=json.loads(a.row.read_text());O=a.output;O.mkdir(exist_ok=False);app=None;result=dict(state='HOLD',physical_drive_started=False,main_denominator=0,started=time.time())
def write(n,d):(O/n).write_text(json.dumps(d,indent=2,default=lambda v:v.tolist() if hasattr(v,'tolist') else str(v)))
try:
 from evaluation.b1_common_hpo_policy_20261111_v01 import gpu_gate
 gate=gpu_gate((os.getpid(),os.getppid()));assert gate['clear'],gate
 from isaacsim import SimulationApp
 app=SimulationApp({'headless':True,'width':640,'height':480,'renderer':'RayTracedLighting','multi_gpu':False,'extra_args':['--/app/window/enabled=false','--/metricsAssembler/operationMode=0','--/omni/replicator/captureOnPlay=false']})
 import omni.usd,omni.timeline,omni.graph.core as og,numpy as np
 from isaacsim.core.utils.extensions import enable_extension
 enable_extension('isaacsim.ros2.bridge');enable_extension('isaacsim.robot.wheeled_robots')
 from pxr import Usd,UsdGeom,UsdPhysics,PhysxSchema,UsdUtils,PhysicsSchemaTools,Gf
 from evaluation.c_v02_drive540_scene_20261113_v01 import build,TARGET
 ctx=omni.usd.get_context();tl=omni.timeline.get_timeline_interface();tl.stop();stage,construction=build(O/'prepared_C_drive.usda',row);write('scene_construction.json',construction)
 for p in stage.Traverse():
  if p.HasAPI(UsdPhysics.RigidBodyAPI):PhysxSchema.PhysxContactReportAPI.Apply(p).CreateThresholdAttr().Set(0.)
 stage.GetRootLayer().Save();ctx.open_stage(str(O/'prepared_C_drive.usda'))
 for _ in range(60):app.update()
 stage=ctx.get_stage()
 from evaluation.c_v02_loaded_stage_collider_audit_20261112_v01 import audit
 manifest=audit(stage,'ACTUAL_LOADED_ISAAC_STAGE');manifest['root_layers_sha256']={x.realPath:hashlib.sha256(Path(x.realPath).read_bytes()).hexdigest() for x in stage.GetUsedLayers() if x.realPath and Path(x.realPath).is_file() and Path(x.realPath).stat().st_size<100000000};write('actual_loaded_stage_manifest.json',manifest)
 from omni.physx import get_physx_interface,get_physx_scene_query_interface,get_physx_simulation_interface
 q=get_physx_scene_query_interface();steps=[];contacts=[]
 def onstep(dt):steps.append(float(dt))
 def oncontact(headers,data):
  for h in headers:
   contacts.append(dict(a=str(PhysicsSchemaTools.intToSdfPath(h.collider0)),b=str(PhysicsSchemaTools.intToSdfPath(h.collider1)),points=[dict(position=list(data[i].position),separation=float(data[i].separation),impulse=list(data[i].impulse)) for i in range(h.contact_data_offset,h.contact_data_offset+h.num_contact_data)]))
 sub=get_physx_interface().subscribe_physics_step_events(onstep);cs=get_physx_simulation_interface().subscribe_contact_report_events(oncontact)
 cam='/World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera';assert stage.GetPrimAtPath(cam).IsA(UsdGeom.Camera)
 def rover_pose():return list(UsdGeom.XformCache().GetLocalToWorldTransform(stage.GetPrimAtPath('/World/ENG_FE2E/Rover/base_link')).ExtractTranslation())
 before=rover_pose();tl.set_looping(False);tl.play()
 for i in range(240):app.update()
 after=rover_pose();tl.pause();write('contacts.json',contacts)
 import carb
 probes=[]
 cache=UsdGeom.XformCache()
 for path in construction['collider_paths']:
  p=stage.GetPrimAtPath(path);center=cache.GetLocalToWorldTransform(p).ExtractTranslation();hits=[]
  def hit(h):hits.append(str(h.collision));return True
  q.overlap_box(carb.Float3(.0001,.0001,.0001),carb.Float3(*center),carb.Float4(0,0,0,1),hit,False);probes.append(dict(path=path,center=list(center),registered=path in hits,hits=hits))
 write('actual_PhysX_registration.json',probes)
 wheels=[p for p in stage.Traverse() if p.HasAPI(UsdPhysics.CollisionAPI) and UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get() is not False and 'wheel' in str(p.GetPath()).lower() and p.IsA(UsdGeom.Cylinder)];assert len(wheels)==6,('wheel_count',len(wheels))
 supports=[]
 for w in wheels:
  path=str(w.GetPath());events=[c for c in contacts if path in (c['a'],c['b'])];supports.append(dict(wheel=path,contact_events=len(events),other_colliders=sorted({c['b'] if c['a']==path else c['a'] for c in events})))
 write('stationary_wheel_contacts.json',supports)
 external=[c for c in contacts if (c['a'].startswith(TARGET) or c['b'].startswith(TARGET)) and ('Rover/' in c['a'] or 'Rover/' in c['b'])]
 checks=dict(actual_PhysX_steps=len(steps)>0,all_C_colliders_registered=all(x['registered'] for x in probes),all_six_wheels_contact=all(x['contact_events']>0 for x in supports),no_rover_target_collision=not external,stationary_XY_drift_below_5mm=math.dist(before[:2],after[:2])<=.005,no_external_panel=not construction['external_panel_prim_paths'],articulation_present=any(p.HasAPI(UsdPhysics.ArticulationRootAPI) for p in stage.Traverse()),camera_present=True)
 # Acquire real robot RGB-D while paused; GT mask never sent to operational pipeline.
 import omni.replicator.core as rep
 from PIL import Image
 product=rep.create.render_product(cam,(640,480));anns={n:rep.AnnotatorRegistry.get_annotator(n) for n in ['rgb','distance_to_image_plane','camera_params']}
 for an in anns.values():an.attach(product.path)
 for _ in range(60):app.update()
 rep.orchestrator.step(rt_subframes=8,delta_time=0,pause_timeline=True)
 def arr(n):
  x=anns[n].get_data();return np.asarray(x['data'] if isinstance(x,dict) else x)
 rgb=arr('rgb')[...,:3].copy();depth=np.squeeze(arr('distance_to_image_plane')).copy();np.save(O/'front_rgb.npy',rgb);np.save(O/'front_depth.npy',depth);Image.fromarray(rgb.astype('uint8')).save(O/'front_rgb.png');raw=anns['camera_params'].get_data();mat=np.array(UsdGeom.XformCache().GetLocalToWorldTransform(stage.GetPrimAtPath(cam)),float).T;mat[:3,:3]=mat[:3,:3]@np.diag([1,-1,-1]);proj=np.array(raw['cameraProjection']).reshape(4,4);cal=dict(width=640,height=480,fx=float(proj[0,0])*320,fy=float(proj[1,1])*240,cx=320.,cy=240.,T_world_optical=mat.tolist(),depth_semantic='distance_to_image_plane',depth_unit_m=1.);write('camera_metadata.json',dict(calibration=cal));checks['RGBD_valid']=rgb.shape==(480,640,3) and depth.shape==(480,640) and int(np.count_nonzero(np.isfinite(depth)&(depth>0)))>0
 for an in anns.values():an.detach(product.path)
 product.destroy()
 result.update(state='STATIONARY_PHYSICS_PASS' if all(checks.values()) else 'HOLD',checks=checks,physics_steps=len(steps),actual_sim_seconds=sum(steps),rover_before=before,rover_after=after,unresolved_gates=['full_E2E_technical_pilot','path_control_and_stop_certification','all_representative_conditions','video_and_evaluation_GT_evidence'],physical_entry='HOLD',algorithm_formula_changed=False)
except BaseException:
 result.update(state='HOLD',traceback=traceback.format_exc())
finally:
 result['ended']=time.time();write('result.json',result)
 if app:
  try:omni.timeline.get_timeline_interface().stop()
  except Exception:pass
  app.close()
print(json.dumps(result));sys.exit(0 if result['state']=='STATIONARY_PHYSICS_PASS' else 2)
