"""C540 v01: original Stage4 safety/control/ROS/stop law retained; single C scene, known task-layer prior and fixed mixed seed42 model. No Correction B or panels. Pilot-gated."""
"""CANDIDATE v04: compact in-memory history only AFTER full feedback/trace persistence. Not active; requires offline validation before a separate execution. No guard changes."""
"""Stage-4 ablation single physical drive session (v03, 2026-11-11; v02 + GC-scope lifecycle fix for Correction B: at the certified W stop
(timeline paused, driver in its validated zero pause) the v19b MotionGC deferred-GC scope is CLOSED (restore + gc.collect) and a NEW
scope is opened (enter) before motion resumes. Bound VALUES unchanged (768 MiB growth, 600 s, 8 GiB absolute per scope). Evidence:
main run01 G3 6x GC_MEMORY_BOUND at growth 760-770 MiB after 455-470 s; growth rate 1.63-1.72 MiB/s identical in G1 and G3
(retained per-tick records/commands), i.e. B only lengthens the scope. Single-approach groups are unaffected (code path only in B).)
v02 header: v01 + ATOMIC publication (tmp + fsync + os.link, persistence_v21.atomic_new)
of every driver handoff file: leg_<k>_path.json, leg_<k>_stop.json, leg_validation_pause.json, next_leg_<k>.json; reported
non-atomic JSON handoff at a stop transition (speed-guard investigation, reg_HR_Scan_L4_O0_baseline_r1). Nothing else changed.)
v01 header follows: = scripts/stage3_drive_session_20261110_v02.py with ONLY:
  1. group switches: --pose-method ORIG_v44 (A off) | ROBUST_A (Correction A, frozen b5_robust v01) and --correction-b on/off.
     Planner fixed to TC-S v01 (stage-3 'improved' arm, rate cap 4.3976 deg/s); v19 `command`, v21 adapter/certificate, ROS driver
     (N-leg generalisation scripts/stage4_ablation_drive_ros_20261110_v01.py), 0.03 m/s speed guard, tracking envelope, steering
     bounds, emergency envelope, contact/support/clearance checks: UNCHANGED.
  2. start pose: --start-xy-yaw is AUTHORED on /World/ENG_FE2E/Rover xformOp:transform in the per-run overlay (same op the v21
     prepared stage used to set the v30 start; z unchanged -0.00835194); start validity 2 cm / 1 deg unchanged.
  3. occlusion O25/O50 from a locked B1-v02-rule fixture (GT = fixture placement only); panel visible during the INITIAL capture
     only, removed + verified before motion in every group (re-observation captures are panel-free in every group).
  4. Correction B: legs W -> PRE' -> FINAL'. W = point on the straight chord start->PRE_init at y = PRE_init_y - 0.80 m, yaw 90.
     At the certified W stop (same v21 certificate): timeline pause barrier, re-capture with the UNCHANGED render product
     (same annotators, same checks: camera static, pose/sim-time static, capture-graph invariant, render admission, RSS),
     re-detection + re-identification + pose (stage4 perception worker, mode reobs), PRE'/FINAL' from the re-estimate, TC-S replan
     from the CURRENT pose. Declared fallbacks: B_FALLBACK_NO_W (start->W not admissible -> single approach),
     B_FALLBACK_REOBS (re-detection/re-identification/pose failed -> initial PRE/FINAL), B_FALLBACK_PLAN (W->PRE' rejected ->
     W->PRE_init). FINAL target always comes from the same estimate as the PRE actually used.
  5. stop certificate: unchanged v21 confirmed_stop; legs >= 1 are presented to it with leg label 1 and previous_end = previous
     leg end (pure relabel; every criterion identical).
  6. optional in-session robot-camera recording (--record-robotcam): reads the EXISTING rgb annotator of the capture render
     product every REC_EVERY ticks during motion (no new render product / graph node); per-tick graph invariant still enforced.
  7. fixture mode generalised: --fixture-coverage (B1 v02 rule; .25 or .50) at the requested start.
"""
import argparse,os,json,math,time,hashlib,subprocess,traceback,sys,signal,uuid
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));sys.path.insert(1,str(R/'scripts'));sys.path.insert(2,str(R/'analysis'))
from evaluation.construction_site_persistence_20261101_v21 import persist_before_close, atomic_new
from evaluation.construction_site_stop_certificate_20261101_v21 import confirmed_stop
from evaluation.construction_site_drive_cleanup_20261101_v10 import final_success
from evaluation.construction_site_io_20261101_v16 import JSONLTail, await_cleanup_receipt
from evaluation.legacy_supervised_guard_v02 import DOF, quiet, outcomes, graph_signature, validate_graph, actor_signature
from evaluation.construction_site_timing_20261101_v18b import TIMING, EndpointGuard, install_forensic_timing, identity_only_zero_check
install_forensic_timing()
import gc
from evaluation.stage4_record_projection_20261111_v01 import project_record
_gc_start={}
def gc_event(phase,info):
 gen=info['generation']
 if phase=='start':_gc_start[gen]=(time.monotonic_ns(),time.thread_time_ns())
 elif gen in _gc_start:
  start,cpu=_gc_start.pop(gen);TIMING.rows.append(('gc_generation_'+str(gen),start,time.monotonic_ns(),time.thread_time_ns()-cpu,True))
gc.callbacks.append(gc_event)
from evaluation.construction_site_runtime_20261101_v19b import MotionGC, eligible_fault
motion_gc=MotionGC()
from evaluation.construction_site_diagnostics_20261102_v30 import checkpoint,traced_close
p=argparse.ArgumentParser()
p.add_argument('--scenario-row',type=Path,required=True);p.add_argument('--output',required=True);p.add_argument('--domain',type=int,required=True)
p.add_argument('--mode',choices=['drive','fixture'],default='drive')
p.add_argument('--representation',choices=['HR_Scan','LR_Scan','GeoCAD'],required=True)
p.add_argument('--load',choices=['L1','L4'],required=True);p.add_argument('--occlusion',choices=['O0','O25','O50'],required=True)
p.add_argument('--arm',choices=['improved'],default='improved')
p.add_argument('--pose-method',choices=['ORIG_v44','ROBUST_A'],default='ORIG_v44');p.add_argument('--correction-b',choices=['on','off'],default='off')
p.add_argument('--fixture-coverage',type=float,default=.5);p.add_argument('--record-robotcam',action='store_true');p.add_argument('--wp-back-m',type=float,default=.80)
p.add_argument('--base-stage',required=True);p.add_argument('--panel-fixture',default=None)
p.add_argument('--start-xy-yaw',default='-25.88797768,27.40014,90.0')
a=p.parse_args();O=Path(a.output);O.mkdir(exist_ok=False);EV=O/'eval_gt_only';EV.mkdir()
START_LOCK=[float(x) for x in a.start_xy_yaw.split(',')]
CORR_B=a.correction_b=='on';REC_EVERY=12;recorder=None;rec_stats={'frames':0,'errors':0,'seconds':0.,'max_s':0.}
def emit(n,d):
 with (O/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x))
def emit_ev(n,d):
 with (EV/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x))
def emit_atomic(n,d):
 atomic_new(O/n,json.loads(json.dumps(d,allow_nan=False,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x))))
def snap(n,d):
 t=O/(n+'.tmp');t.write_text(json.dumps(d,allow_nan=False));t.replace(O/n)
def stage3_event(kind,**kw):
 with (O/'stage3_events.jsonl').open('a') as f:f.write(json.dumps(dict(event=kind,wall_s=time.time(),**kw),default=str)+'\n')
command_tail=JSONLTail(O/'adapter_commands.jsonl');checked_contacts=0
drive_contract=json.loads((O.parent/'drive_contract.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fresh_tf_status(status,now,sim):
 return bool(status and status.get('tf') and status.get('tf_count',0)>=3 and 0<=now-status['wall_s']<=.5 and 0<=now-status['tf']['wall_received']<=.5 and abs(status['tf']['stamp_s']-sim)<=.1)
signal_aborted=False
def request_abort(*_):
 global signal_aborted
 signal_aborted=True
 (O/'abort_motion').touch()
 snap('signal_abort.json',{'domain':a.domain,'time':time.time(),'signal':True})
 if not (O/'zero_request.json').exists():snap('zero_request.json',{'domain':a.domain,'time':time.time(),'signal':True})
signal.signal(signal.SIGTERM,request_abort);signal.signal(signal.SIGINT,request_abort)

LOAD='/World/CV02DriveScene/Load_01/ActualBrickLoad';FIXTURE='/World/CV02DriveScene/Load_01'
PANEL_ROOT='/World/Stage3OccluderWorld';PANEL=PANEL_ROOT+'/Panel';CLASS='/Stage3BrickClass_v01'
CAMERA='/World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera'
RED={k:'/home/user/hh/isaac_cosmos/assets/assets/objects/_normalized/red_brick_%s.usd'%k for k in ('HR_Scan','LR_Scan','GeoCAD')}
MANIFEST=R/'manifests/construction_site_pilot_prepare_20261102_v24.json'
SCENARIO=json.loads(a.scenario_row.read_text());assert SCENARIO['representation']==a.representation and SCENARIO['O']=='O0' and int(SCENARIO['load_count'])==1 and int(SCENARIO['pallet_count'])==1
assert a.occlusion=='O0' and not CORR_B and a.mode=='drive'
LAYER_COUNT=int(SCENARIO['task_layer_count'])

def discovery_check(guard,st,now,sim,out,started):
 unknown=[x for x in st['cmd_publishers'] if x['node']=='_NODE_NAME_UNKNOWN_' or x['namespace']=='_NODE_NAMESPACE_UNKNOWN_']
 with (out/'discovery_wait.jsonl').open('a') as f:
  f.write(json.dumps({'wall_s':now,'wait_s':time.monotonic()-started,'sim_s':sim,'snapshot':st,'unknown':unknown})+'\n')
 prior=getattr(guard,'startup_unknown_gids',set())
 if unknown:
  gids={tuple(x['gid']) for x in unknown}
  assert not prior or gids==prior,'DISCOVERY_UNKNOWN_GID_CHANGED'
  guard.startup_unknown_gids=gids
  assert time.monotonic()-started<5.,'DISCOVERY_METADATA_TIMEOUT'
  assert 0<=now-st['wall_s']<=.5 and st['tf'] and 0<=now-st['tf']['wall_received']<=.5 and abs(st['tf']['stamp_s']-sim)<=.1,'DISCOVERY_TF_STALE'
  assert len(unknown)==1 and len(st['cmd_publishers'])<=2,'UNTRUSTED_DISCOVERY_SET'
  assert all(x['node'] in ('eng_smoke_observer','v02_stopping_single_validation','_NODE_NAME_UNKNOWN_') for x in st['cmd_publishers']),'UNTRUSTED_DISCOVERY_PUBLISHER'
  return False
 if prior:
  assert all(any(tuple(x['gid'])==gid and x['node']=='v02_stopping_single_validation' and x['namespace']=='/' for x in st['cmd_publishers']) for gid in prior),'UNKNOWN_GID_NOT_RESOLVED_TO_DRIVER'
 return guard.check(st,'discovery',now,sim)

def derive_stage3(path):
 from evaluation.c_v02_drive540_scene_20261113_v06 import build
 stage,proof=build(path,SCENARIO)
 emit('C_scene_construction.json',proof)
 # Exact original graph; no ROS/camera/TF/actuator node removed.
 from pxr import Usd
 ref=Usd.Stage.Open(a.base_stage)
 validate_graph(graph_signature(stage),json.loads((O.parent/'expected_graph.json').read_text()))
 assert graph_signature(stage)==graph_signature(ref),'C_SUPPLIER_GRAPH_DELTA'
 bindings=[str(q.GetPath()) for q in stage.Traverse() if 'IsaacArticulationController' in str(q.GetAttribute('node:type').Get())]
 assert len(bindings)==3
 return stage,bindings

app=observer=child=art=stream=None;timeline=None;result={'scope':'stage3_v02','research_denominator':'counted_by_runner','status':'FAILED','motion_attempts':0,'retry':0,'mode':a.mode,'arm':a.arm};phase='bootstrap';active_path=None;endpoint_guard=EndpointGuard(O/"session_endpoint_forensics.jsonl");native_mode=False;discovery_started=None;admitted=False;graph_lock=None;records=[];step=0;contacts=[];guard_center=None;started_wall=time.monotonic();last=None;success_candidate=False;cleanup_receipt={'valid':False};stage3_stage='bootstrap'
checkpoint(O,'python_start')
try:
 assert os.environ['ROS_DOMAIN_ID']==str(a.domain)
 bench='/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_robot_task_controller_perturbation35mm_2p5deg_v01.usd';assert sha(bench)=='224cac492d267d0403c9402484fcf84011191208fb4689e7e3fc33eadf3756fe'
 from isaacsim import SimulationApp
 app=SimulationApp({'headless':True,'width':640,'height':480,'renderer':'RayTracedLighting','extra_args':['--/app/window/enabled=false','--/app/livestream/enabled=false','--/metricsAssembler/operationMode=0']})
 checkpoint(O,'kit_startup');stage3_event('kit_started')
 import numpy as np,omni.usd,omni.timeline,carb
 import omni.graph.core as og
 from pxr import Usd,UsdGeom,UsdPhysics,PhysxSchema,Sdf,Gf,UsdUtils,PhysicsSchemaTools
 from isaacsim.core.utils.extensions import enable_extension
 enable_extension('isaacsim.ros2.bridge');enable_extension('isaacsim.robot.wheeled_robots')
 for _ in range(5):app.update()
 timeline=omni.timeline.get_timeline_interface();timeline.stop();ctx=omni.usd.get_context()
 from evaluation.c_v02_drive540_physx_gate_20261113_v01 import physx_gate
 from construction_site_drive_geometry_20261101_v04 import corridor,ROVER
 stage3_stage='derive'
 stage,bindings=derive_stage3(O/'site_drive.usda')
 checkpoint(O,'scene_derived',stage)
 GP='/World/ENG_FE2E/Rover/ActionGraph';BASE='/World/ENG_FE2E/Rover/base_link'
 for pp in stage.Traverse():
  if pp.HasAPI(UsdPhysics.RigidBodyAPI):PhysxSchema.PhysxContactReportAPI.Apply(pp).CreateThresholdAttr().Set(0.)
 clearance=corridor(stage);emit('initial_corridor.json',clearance);assert clearance['status']=='PASS','NO_SAFE_CORRIDOR'
 allowed_support=set(clearance['support_paths'])
 stage.GetRootLayer().Save();carb.settings.get_settings().set('/physics/updateToUsd',True);ctx.attach_stage_with_callback(UsdUtils.StageCache.Get().Insert(stage).ToLongInt())
 for _ in range(10):app.update()
 stage=ctx.get_stage()
 expected_graph=json.loads((O.parent/'expected_graph.json').read_text())
 from evaluation.construction_site_actor_cache_20261101_v18b import ActorCache
 actor_cache=ActorCache(stage)
 graph_lock=graph_signature(stage);validate_graph(graph_lock,expected_graph);actor_lock=actor_signature(stage)
 assert actor_cache.check()==actor_lock,'INITIAL_CACHE_MISMATCH'
 emit('graph_admission.json',{'pass':True,'signature':graph_lock,'scope':'composed OmniGraph nodes/config/connections and observed ROS endpoints; not native C++ exclusivity'})
 def pose():
  m=UsdGeom.XformCache().GetLocalToWorldTransform(stage.GetPrimAtPath(BASE));t=m.ExtractTranslation();f=m.TransformDir(Gf.Vec3d(1,0,0));return [float(t[0]),float(t[1]),float(t[2]),math.atan2(float(f[1]),float(f[0]))]
 def ros(argv,name):
  log=(O/name).open('x');return subprocess.Popen(['/bin/bash','-c','source /opt/ros/jazzy/setup.bash && exec "$@"','child']+argv,cwd=R,env=dict(os.environ),stdout=log,stderr=subprocess.STDOUT)
 if a.mode=='drive':observer=ros(['/usr/bin/python3',str(R/'scripts/construction_site_observer_20261101_v18b.py'),'--output',str(O)],'observer_stdout.log')
 from omni.physx import get_physx_simulation_interface,get_physx_interface,get_physx_scene_query_interface
 from isaacsim.core.simulation_manager import SimulationManager
 physics={'steps':0,'elapsed_s':0.,'last_dt_s':None}
 clock_stream=(O/'physics_steps.jsonl').open('x')
 def physics_step(dt):
  assert math.isfinite(dt) and dt>0,'INVALID_ACTUAL_PHYSICS_DT'
  physics['steps']+=1;physics['elapsed_s']+=dt;physics['last_dt_s']=dt
  clock_stream.write(json.dumps(dict(physics,timeline_s=timeline.get_current_time(),manager_sim_s=SimulationManager.get_simulation_time(),manager_steps=SimulationManager.get_num_physics_steps(),playing=timeline.is_playing(),looping=timeline.is_looping()))+'\n');clock_stream.flush()
 physics_subscription=get_physx_interface().subscribe_physics_step_events(physics_step)
 def sim_time():return float(SimulationManager.get_simulation_time())
 emit('clock_configuration.json',{'source':'SimulationManager.get_simulation_time; independently checked actual PhysX callbacks dt sum and step count','before':{'start_s':timeline.get_start_time(),'end_s':timeline.get_end_time(),'looping':timeline.is_looping(),'stage_start':stage.GetStartTimeCode(),'stage_end':stage.GetEndTimeCode()},'after':{'start_s':0.,'end_s':480.,'looping':False}})
 stage.SetStartTimeCode(0.);stage.SetEndTimeCode(480.*stage.GetTimeCodesPerSecond());stage.GetRootLayer().Save()
 timeline.set_start_time(0.);timeline.set_end_time(480.);timeline.set_looping(False)
 def contact_cb(headers,data):
  for h in headers:
   c0=str(PhysicsSchemaTools.intToSdfPath(h.collider0));c1=str(PhysicsSchemaTools.intToSdfPath(h.collider1));points=[]
   for i in range(h.contact_data_offset,h.contact_data_offset+h.num_contact_data):
    d=data[i];points.append({'position':[float(v) for v in d.position],'normal':[float(v) for v in d.normal],'separation_m':float(d.separation),'impulse_Ns':[float(v) for v in d.impulse]})
   contacts.append({'sim_s':sim_time(),'timeline_s':timeline.get_current_time(),'physics_step':physics['steps'],'phase':phase,'collider0':c0,'collider1':c1,'num_points':int(h.num_contact_data),'points':points})
 subscription=get_physx_simulation_interface().subscribe_contact_report_events(contact_cb)
 stream=(O/'steps.jsonl').open('x');com_local=None
 def graph_array(name):
  value=og.Controller.attribute(GP+'/ackermann_controller.outputs:'+name).get()
  return [] if value is None else list(value)
 def tick():
  global step,last,checked_contacts,_last_tick_end
  motion_gc.check()
  before=time.monotonic();tick_wall_start=time.time();guard_start_ns=time.monotonic_ns()
  if '_last_tick_end' in globals():TIMING.rows.append(('between_ticks_other',_last_tick_end,time.monotonic_ns(),None,True))
  try:
   current_graph=TIMING.call('graph_fingerprint_traversal',graph_signature,stage)
   from evaluation.construction_site_runtime_20261101_v19b import check_graph
   try:TIMING.call('graph_fingerprint_comparison',check_graph,graph_lock,current_graph)
   except AssertionError:
    snap('graph_changed_detail.json',{'phase':phase,'wall_s':time.time(),'added':sorted(set(current_graph)-set(graph_lock)),'removed':sorted(set(graph_lock)-set(current_graph))})
    raise
   assert TIMING.call('actor_signature_incremental',actor_cache.check)==actor_lock,'ACTOR_CHANGED'
   assert observer is None or observer.poll() is None,'OBSERVER_LOST'
   if admitted:
    st=TIMING.call('endpoint_snapshot_read',lambda:json.loads((O/'ros_status.json').read_text()))
    mode=('zero' if (O/'calibration_ros_complete.json').exists() else 'active') if phase=='pulse' else ('zero' if phase in ('zero_stop','exception_zero') else 'discovery')
    (identity_only_zero_check(endpoint_guard,st,time.time(),sim_time()) if phase=='fault_zero_only' else discovery_check(endpoint_guard,st,time.time(),sim_time(),O,discovery_started) if mode=='discovery' and discovery_started is not None else endpoint_guard.check(st,mode,time.time(),sim_time()))
    if phase=='pulse':
     assert child is not None and (child.poll() is None or (O/'calibration_ros_complete.json').exists()),'DRIVER_DIED'
     ds=json.loads((O/'driver_status.json').read_text())
     if not (O/'calibration_ros_complete.json').exists():assert time.time()-ds['wall_s']<=.5,'DRIVER_STALE'
   contact_start=time.monotonic_ns()
   for c in contacts[checked_contacts:]:
    assert all(x.startswith('/World/ENG_FE2E/Rover/') or x in allowed_support for x in (c['collider0'],c['collider1'])),'COLLISION:UNEXPECTED_CONTACT'
   if phase in ('pulse','zero_stop','fault_zero_only'):
    for c in contacts[checked_contacts:]:
     if c['phase'] in ('pulse','zero_stop','fault_zero_only') and ('gl_shell' in c['collider0'] or 'gl_shell' in c['collider1']):
      assert all(d['separation_m']>=0 and sum(v*v for v in d['impulse_Ns'])==0 for d in c['points']),'SHELL_FLOOR_PENETRATION_OR_LOAD_DURING_DRIVE'
   checked_contacts=len(contacts)
   TIMING.rows.append(('contacts_support',contact_start,time.monotonic_ns(),None,True))
   if phase=='fault_zero_only':
    assert child is not None and child.poll()==0,'ZERO_RECOVERY_DRIVER_NOT_EXITED'
    for node in bindings:
     for key in ('velocityCommand','effortCommand'):
      attr=og.Controller.attribute(node+'.inputs:'+key);value=attr.get()
      if value is not None:attr.set([0.]*len(value))
    assert all(float(x)==0 for x in graph_array('wheelRotationVelocity')),'ZERO_RECOVERY_GRAPH_NONZERO'
   if (O/'zero_request.json').exists():(O/'abort_motion').touch()
  except Exception:
   TIMING.rows.append(('preupdate_guard',guard_start_ns,time.monotonic_ns(),None,False))
   (O/'abort_motion').touch()
   if not (O/'zero_request.json').exists():emit('zero_request.json',{'domain':a.domain,'time':time.time(),'guard_fault':True})
   timeline.pause();raise
  TIMING.rows.append(('preupdate_guard',guard_start_ns,time.monotonic_ns(),None,True))
  other_start=time.monotonic_ns()
  guard_end=time.time();previous_physics=physics['steps'];TIMING.call('physics_app_update',app.update);update_end=time.time();step+=1;t=sim_time();p=pose()
  status=json.loads((O/'ros_status.json').read_text()) if (O/'ros_status.json').exists() else {}
  clock={'timeline_s':timeline.get_current_time(),'physics_sim_s':t,'physics_steps':physics['steps'],'callback_elapsed_s':physics['elapsed_s'],'last_physics_dt_s':physics['last_dt_s'],'manager_steps':int(SimulationManager.get_num_physics_steps()),'tick_timing':{'guard_end_wall_s':guard_end,'update_end_wall_s':update_end,'guard_duration_s':guard_end-tick_wall_start,'update_duration_s':update_end-guard_end,'tf_wall_received':status.get('tf',{}).get('wall_received') if status.get('tf') else None},'physics_steps_this_update':physics['steps']-previous_physics,'playing':timeline.is_playing(),'looping':timeline.is_looping(),'tf_stamp_s':status.get('tf',{}).get('stamp_s') if status.get('tf') else None,'graph_sim_s':None if native_mode else og.Controller.attribute(GP+'/isaac_read_simulation_time.outputs:simulationTime').get()}
  if art is not None:
   assert physics['steps']>previous_physics,'PHYSICS_STEP_NOT_ADVANCING'
   assert abs(t-physics['elapsed_s'])<.05,'PHYSICS_CLOCK_CALLBACK_MISMATCH'
   assert last is None or t>last['sim_s'],'PHYSICS_TIME_NOT_MONOTONIC'
  if art is not None:
   raw=np.array(art._physics_view.get_root_transforms())[0];vel=np.array(art._physics_view.get_root_velocities())[0];cm=UsdGeom.XformCache().GetLocalToWorldTransform(stage.GetPrimAtPath(BASE));rot=np.array(cm)[:3,:3].T;originv=vel[:3]-np.cross(vel[3:6],rot@com_local);q=np.array(art.get_joint_positions())[0];dq=np.array(art.get_joint_velocities())[0];vf=float(originv[0]*math.cos(p[3])+originv[1]*math.sin(p[3]));speed=float(np.linalg.norm(originv[:2]));fd=None
   if last is not None and t>last['sim_s']:fd=[(p[i]-last['pose'][i])/(t-last['sim_s']) for i in range(3)]
   r={'clock':clock,'step':step,'sim_s':t,'wall_s':time.time(),'phase':phase,'pose':p,'tensor_root_pose_xyzw':raw.tolist(),'tensor_COM_velocity':vel.tolist(),'base_origin_v':originv.tolist(),'forward_m_s':vf,'planar_m_s':speed,'fd_velocity':fd,'q_rad':q.tolist(),'dq_rad_s':dq.tolist(),'native_published_velocity':list(UsdPhysics.RigidBodyAPI(stage.GetPrimAtPath(BASE)).GetVelocityAttr().Get()),'wheel_surface_m_s':float(np.mean(dq[active]))*drive_contract['wheel_radius_m'],'graph_wheel_target_rad_s':[] if native_mode else graph_array('wheelRotationVelocity'),'graph_steer_target_rad':[] if native_mode else graph_array('wheelAngles'),'measurement_note':'tensor post-update COM->origin correction; native velocity and FD retained'}
   if phase in ('pulse','zero_stop','fault_zero_only'):
    assert all(abs(q[i])<=math.radians(20) for i,n in enumerate(names) if n.endswith('_steer_joint')),'MEASURED_STEERING_BOUND'
    assert all(abs(v)<=math.radians(20) for v in r['graph_steer_target_rad']),'GRAPH_STEERING_BOUND'
   r['controller_inputs']={}
   for node in ([] if native_mode else bindings):
    data={}
    for key in ('jointNames','positionCommand','velocityCommand','effortCommand'):
     val=og.Controller.attribute(node+'.inputs:'+key).get()
     data[key]=None if val is None else ([str(x) for x in val] if key=='jointNames' else [float(x) for x in val])
    assert data['jointNames']==list(stage.GetPrimAtPath(node).GetAttribute('inputs:jointNames').Get()),'CONTROLLER_NAMES_MISMATCH'
    r['controller_inputs'][node]=data
   if phase in ('pulse','zero_stop') and (O/'adapter_commands.jsonl').exists():
    lines=command_tail.poll()
    if lines and t-lines[0]['sim_s']>.1:
     for node,data in r['controller_inputs'].items():
      key='positionCommand' if node.endswith('_01') else 'velocityCommand'
      assert data[key] is not None and len(data[key])==len(data['jointNames']),'CONTROLLER_READBACK_MISSING'
   actions=art.get_applied_actions()
   assert actions is not None,'TARGET_READBACK_UNAVAILABLE'
   position_targets=np.array(actions.joint_positions)[0];velocity_targets=np.array(actions.joint_velocities)[0]
   assert len(position_targets)==10 and len(velocity_targets)==10,'TARGET_MAP_INVALID'
   r['physics_named_targets']={name:{'position_rad':float(position_targets[i]),'velocity_rad_s':float(velocity_targets[i])} for i,name in enumerate(names)}
   r['named_joint_state']={name:{'q_rad':float(q[i]),'dq_rad_s':float(dq[i])} for i,name in enumerate(names)}
   snap('feedback.json',r);stream.write(json.dumps(r)+'\n');stream.flush();records.append(project_record(r));last=r
   if phase in ['pulse','zero_stop'] and (math.hypot(p[0]-guard_center[0],p[1]-guard_center[1])>3.2 or speed>.25):
    (O/'abort_motion').touch();timeline.pause();raise RuntimeError('EMERGENCY_PAUSE_ENVELOPE')
   if phase in ('pulse','zero_stop') and active_path is not None:
    from evaluation.construction_site_follower_20261101_v19 import command as tracking_check
    try:tracking_check(p,active_path)
    except Exception:
     (O/'abort_motion').touch();timeline.pause();raise
   if phase=='pulse' and (speed>=.03 or math.hypot(p[0]-guard_center[0],p[1]-guard_center[1])>=3.1):(O/'abort_motion').touch()
   if recorder is not None and phase in ('pulse','zero_stop') and step%REC_EVERY==0:recorder(step,t)
  TIMING.rows.append(('post_guard_update_readback_serialization',other_start,time.monotonic_ns(),None,True))
  TIMING.rows.append(('tick_other_and_total',int(before*1e9),time.monotonic_ns(),None,True))
  _last_tick_end=time.monotonic_ns()
  time.sleep(max(0.,1/60-(time.monotonic()-before)))
 from evaluation.c_v02_loaded_stage_collider_audit_20261112_v01 import audit as audit_loaded_C
 emit('actual_loaded_C_stage_manifest.json',audit_loaded_C(stage,'ACTUAL_LOADED_ISAAC_STAGE'))
 checkpoint(O,'scene_attached',stage)
 stage3_stage='settle'
 phase='settling';timeline.play(start_timecode=0,end_timecode=480.*stage.GetTimeCodesPerSecond(),looping=False)
 for _ in range(180):tick()
 from isaacsim.core.prims import Articulation
 art=Articulation(prim_paths_expr=BASE,name='calibration_reader_only',reset_xform_properties=False);art.initialize();names=list(art.dof_names);active=[i for i,n in enumerate(names) if n.endswith('_wheel_joint')];assert names==DOF,'NAMED_DOF_MAP_MISMATCH';com_local=np.array(art._physics_view.get_coms())[0,0,:3]
 emit('joint_io.json',{'dof_names':names,'body_names':list(art.body_names),'active':active,'COM_local':com_local.tolist(),'read_only_articulation':True})
 checkpoint(O,'after_physx_settling',stage)
 phase='baseline'
 for _ in range(75):tick()
 settled=pose();guard_center=settled[:2];assert records[-1]['sim_s']-records[-30]['sim_s']>.4,'CLOCK_NOT_ADVANCING';basequiet=quiet(records)['status']=='PASS';emit('baseline_quiet.json',quiet(records))
 # NEW start validity: settled rover within 2 cm / 1 deg of the locked common start (fail-closed HOLD).
 start_err=math.hypot(settled[0]-START_LOCK[0],settled[1]-START_LOCK[1]);start_yaw_err=math.degrees(math.atan2(math.sin(settled[3]-math.radians(START_LOCK[2])),math.cos(settled[3]-math.radians(START_LOCK[2]))))
 emit('start_validity.json',{'settled':settled,'locked_start_xy_yaw_deg':START_LOCK,'xy_error_m':start_err,'yaw_error_deg':start_yaw_err,'tolerance':{'xy_m':.02,'yaw_deg':1.},'baseline_quiet':basequiet,'pass':start_err<=.02 and abs(start_yaw_err)<=1.})
 assert start_err<=.02 and abs(start_yaw_err)<=1.,'START_POSE_INVALID'
 stage3_stage='safety_preflight'
 clearance=corridor(stage);emit('collision_preflight.json',clearance)
 query=get_physx_scene_query_interface();support_checks=[]
 shell=stage.GetPrimAtPath(BASE+'/collisions/gl_shell/mesh')
 shellbox=UsdGeom.BBoxCache(Usd.TimeCode.Default(),['default','render','proxy','guide'],False,True).ComputeWorldBound(shell).ComputeAlignedBox()
 lo=list(shellbox.GetMin());hi=list(shellbox.GetMax());shell_rays=[]
 winding=[]
 for sitepath in sorted(allowed_support):
  mesh=UsdGeom.Mesh(stage.GetPrimAtPath(sitepath));mat=UsdGeom.XformCache().GetLocalToWorldTransform(mesh.GetPrim())
  ids=mesh.GetFaceVertexIndicesAttr().Get();counts=mesh.GetFaceVertexCountsAttr().Get();pts=mesh.GetPointsAttr().Get();offsets=[0]
  for n in counts:offsets.append(offsets[-1]+n)
  faces=sorted({h['face'] for ss in clearance['support_samples'] for h in ss['hits'] if h['site']==sitepath})
  for face in faces:
   vs=[mat.Transform(Gf.Vec3d(pts[i])) for i in ids[offsets[face]:offsets[face+1]]];normal=Gf.Cross(vs[1]-vs[0],vs[2]-vs[0]);normal.Normalize()
   winding.append({'composed_path':sitepath,'face':face,'world_normal_from_indices':list(normal)})
 def raw_ray(label,origin,length,both):
  raw=[]
  def callback(hit):
   hit={k:getattr(hit,k,None) for k in ('collision','position','normal','distance','rigid_body','face_index')};path=str(hit.get('collision',''))
   raw.append({'path':path,'position':[float(v) for v in hit['position']] if hit.get('position') is not None else None,'normal':[float(v) for v in hit['normal']] if hit.get('normal') is not None else None,'distance':float(hit.get('distance',0)),'accepted':path in allowed_support})
   return True
  returned=query.raycast_all(tuple(origin),(0.,0.,-1.),length,callback,both)
  return {'label':label,'origin':list(origin),'length_m':length,'bothSides':both,'return_bool':bool(returned),'hits_before_filter':raw}
 representatives=[ss for ss in clearance['support_samples'] if ss['travel']==0 and ss['yaw_deg']==0 and ss['axle_fraction']==0]
 debug=[]
 for ss in representatives:
  x,y,z=ss['xyz']
  for both in (False,True):debug.append(raw_ray(ss['rover'],[x,y,z+.04],.08,both))
 for both in (False,True):debug.append(raw_ray('control_site_floor_center',[(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,hi[2]+.5],hi[2]+1.,both))
 backface_proven=any(w['world_normal_from_indices'][2]<-.9 for w in winding) and any(not any(h['accepted'] for h in aa['hits_before_filter']) and any(h['accepted'] for h in bb['hits_before_filter']) for aa,bb in zip(debug[::2],debug[1::2]))
 emit('raycast_raw_diagnosis.json',{'rays':debug,'winding':winding,'allowed_composed_paths':sorted(allowed_support),'backface_proven':backface_proven})
 for x in (lo[0],(lo[0]+hi[0])/2,hi[0]):
  for y in (lo[1],(lo[1]+hi[1])/2,hi[1]):
   rr=raw_ray('shell',[x,y,hi[2]+.1],hi[2]-lo[2]+.3,backface_proven)
   hits=[{'collider':h['path'],'position':h['position'],'normal':h['normal']} for h in rr['hits_before_filter'] if h['accepted']]
   shell_rays.append({'xy':[x,y],'hits':hits,'minimum_gap_m':min((lo[2]-h['position'][2] for h in hits),default=None),'return_bool':rr['return_bool']})
 shell_contacts=[c for c in contacts if 'gl_shell' in c['collider0'] or 'gl_shell' in c['collider1']]
 shell_points=[d for c in shell_contacts if c['phase']=='baseline' for d in c['points']]
 shell_safe=all(v['minimum_gap_m'] is not None and v['minimum_gap_m']>0 for v in shell_rays) and all(d['separation_m']>=0 and math.sqrt(sum(v*v for v in d['impulse_Ns']))==0 for d in shell_points)
 emit('shell_contact_diagnosis.json',{'pass':shell_safe,'bounds_world':[lo,hi],'floor_rays':shell_rays,'all_shell_events':len(shell_contacts),'baseline_points':len(shell_points)})
 for sample in clearance['support_samples']:
  x,y,z=sample['xyz'];hits=[]
  def support_hit(hit):
   collider=str(hit.collision);pos=hit.position
   if collider in allowed_support and pos is not None:hits.append({'collider':collider,'position':[float(v) for v in pos],'distance':float(hit.distance)})
   return True
  query.raycast_all((x,y,z+.04),(0.,0.,-1.),.08,support_hit,backface_proven)
  good=[h for h in hits if abs(h['position'][2]-z)<=.01]
  support_checks.append({'rover':sample['rover'],'xyz':sample['xyz'],'hits':hits,'pass':bool(good)})
 wheel_paths=set(s['rover'] for s in clearance['support_samples'])
 contacted={w for w in wheel_paths if any((c['collider0']==w and c['collider1'] in allowed_support) or (c['collider1']==w and c['collider0'] in allowed_support) for c in contacts)}
 support_ok=all(c['pass'] for c in support_checks) and contacted==wheel_paths
 emit('stationary_PhysX_support.json',{'pass':support_ok,'checks_failed':[c for c in support_checks if not c['pass']][:20],'n_checks':len(support_checks),'wheel_paths':sorted(wheel_paths),'contacted_wheels':sorted(contacted)})
 strict_support_ok=support_ok;strict_shell_safe=shell_safe
 if not support_ok or not shell_safe:
  meshtri=[]
  for sitepath in sorted(allowed_support):
   mesh=UsdGeom.Mesh(stage.GetPrimAtPath(sitepath));mat=UsdGeom.XformCache().GetLocalToWorldTransform(mesh.GetPrim());vs=[mat.Transform(Gf.Vec3d(v)) for v in mesh.GetPointsAttr().Get()];ids=mesh.GetFaceVertexIndicesAttr().Get();off=0
   for n in mesh.GetFaceVertexCountsAttr().Get():
    poly=[vs[i] for i in ids[off:off+n]];off+=n
    for k in range(1,n-1):
     tri=(poly[0],poly[k],poly[k+1])
     if all(min(v[i] for v in tri)<=hi[i]+.2 and max(v[i] for v in tri)>=lo[i]-.2 for i in (0,1)):meshtri.append(tri)
  def floor_z(x,y):
   zs=[]
   for aa,bb,cc in meshtri:
    den=(bb[1]-cc[1])*(aa[0]-cc[0])+(cc[0]-bb[0])*(aa[1]-cc[1])
    if abs(den)<1e-12:continue
    u=((bb[1]-cc[1])*(x-cc[0])+(cc[0]-bb[0])*(y-cc[1]))/den;v=((cc[1]-aa[1])*(x-cc[0])+(aa[0]-cc[0])*(y-cc[1]))/den
    if min(u,v,1-u-v)>=-1e-8:
     z=float(u*aa[2]+v*bb[2]+(1-u-v)*cc[2])
     if -.03<=z<=.02:zs.append(z)
   return max(zs) if zs else None
  gaps=[lo[2]-z if (z:=floor_z(x,y)) is not None else None for x in (lo[0],(lo[0]+hi[0])/2,hi[0]) for y in (lo[1],(lo[1]+hi[1])/2,hi[1])]
  wheel_evidence=[]
  for w in sorted(wheel_paths):
   events=[c for c in contacts if (c['collider0']==w and c['collider1'] in allowed_support) or (c['collider1']==w and c['collider0'] in allowed_support)]
   points=[d for c in events for d in c['points']];grounded=[d for d in points if (z:=floor_z(*d['position'][:2])) is not None and abs(d['position'][2]-z)<=.01 and abs(d['normal'][2])>.9]
   wheel_evidence.append({'wheel':w,'points':len(points),'grounded_up_normal_points':len(grounded),'max_impulse_Ns':max((math.sqrt(sum(v*v for v in d['impulse_Ns'])) for d in grounded),default=0.),'minimum_separation_m':min((d['separation_m'] for d in points),default=None),'pass':bool(grounded) and all(d['separation_m']>=-.01 for d in points)})
  window=[r for r in records if r['sim_s']>=records[-1]['sim_s']-1.01];zspan=max(r['pose'][2] for r in window)-min(r['pose'][2] for r in window)
  shell_no_load=all(d['separation_m']>=0 and sum(v*v for v in d['impulse_Ns'])==0 for c in shell_contacts for d in c['points'])
  independent=clearance['status']=='PASS' and all(w['pass'] for w in wheel_evidence) and sum(w['max_impulse_Ns']>0 for w in wheel_evidence)>=3 and zspan<=.002 and all(g is not None and g>0 for g in gaps) and shell_no_load
  emit('independent_engineering_support.json',{'pass':independent,'strict_ray_certificate':strict_support_ok,'strict_shell_rays':strict_shell_safe,'wheels':wheel_evidence,'shell_mesh_gaps_m':gaps,'shell_nonpenetrating_unloaded':shell_no_load,'stationary_z_span_m':zspan,'criterion':'identical to v30 session independent support proof'})
  support_ok=independent;shell_safe=independent
 emit('support_admission.json',{'pass':support_ok and shell_safe,'mode':'corrected_raycast' if strict_support_ok and strict_shell_safe else 'independent_contact_mesh_stationary'})
 assert clearance['status']=='PASS',('COLLIDER_SUPPORT_OR_CLEARANCE_FAILED:'+str(clearance['failure']))
 assert support_ok,'STATIONARY_PHYSX_SUPPORT_FAILED'
 assert shell_safe,'SHELL_FLOOR_PENETRATION_OR_LOAD'
 physics_errors=[line for line in (O.parent/'runtime.log').read_text(errors='replace').splitlines() if '[Error]' in line and '[omni.physicsschema.plugin]' in line]
 from evaluation.c_v02_drive540_mount_admission_20261113_v01 import assess
 diagnostic=assess(stage,physics_errors)
 emit('pilot_physics_diagnostics.json',diagnostic)
 assert diagnostic['pass'],'PILOT_PHYSICS_INVARIANT_NO_GO'
 from evaluation.construction_site_pause_20261101_v12 import pause_barrier
 emit('pause_barrier.json',pause_barrier(app,timeline,sim_time))
 emit('graph_pre_capture.json',{'wall_s':time.time(),'sim_s':sim_time(),'signature':graph_signature(stage)})
 checkpoint(O,'before_capture',stage)
 # ---------------- capture (same render path as capture v30; GT masks to eval_gt_only/ only) ----------------
 stage3_stage='capture'
 phase='fresh_capture';capture_start=pose();capture_physics=sim_time()
 import omni.replicator.core as rep
 from PIL import Image
 assert not timeline.is_playing()
 units=UsdGeom.GetStageMetersPerUnit(stage);assert abs(units-1.)<1e-9 and UsdGeom.GetStageUpAxis(stage)=='Z'
 cp=stage.GetPrimAtPath(CAMERA);assert cp.IsA(UsdGeom.Camera) and cp.IsActive()
 class NoExternalPanel:
  def Get(self):return 'invisible'
  def Set(self,value):assert value=='invisible','EXTERNAL_PANEL_FORBIDDEN'
 panel_vis=NoExternalPanel()
 for _ in range(120):
  assert not timeline.is_playing();app.update()
 # Drive mode: EXACTLY the v30 annotator set (rgb, depth, camera_params) so the unchanged v15 capture-graph allow-list applies;
 # the semantic annotator (GT masks) adds render-graph nodes and is attached ONLY in the motionless fixture mode.
 product=rep.create.render_product(CAMERA,(640,480));rgb_ann=rep.AnnotatorRegistry.get_annotator('rgb');depth_ann=rep.AnnotatorRegistry.get_annotator('distance_to_image_plane');params_ann=rep.AnnotatorRegistry.get_annotator('camera_params');sem_ann=rep.AnnotatorRegistry.get_annotator('semantic_segmentation') if a.mode=='fixture' else None
 for ann in [x for x in (rgb_ann,depth_ann,params_ann,sem_ann) if x is not None]:ann.attach(product.path)
 before_camera=UsdGeom.XformCache().GetLocalToWorldTransform(cp)
 def render():
  for _ in range(30):app.update()
  rep.orchestrator.step(rt_subframes=8,pause_timeline=False,delta_time=0.)
  assert not timeline.is_playing()
  rgb_data=rgb_ann.get_data();depth_data=depth_ann.get_data();params=params_ann.get_data()
  rgb=np.asarray(rgb_data['data'] if isinstance(rgb_data,dict) else rgb_data)[...,:3].copy();depth=np.asarray(depth_data['data'] if isinstance(depth_data,dict) else depth_data).copy()
  if sem_ann is None:return rgb,depth,params,None,None,None
  sd=sem_ann.get_data();labels=sd['info']['idToLabels'];arr=np.asarray(sd['data'])
  def lab(needle):
   ids=[int(i) for i,l in labels.items() if needle in str(l)];return np.isin(arr,ids)
  return rgb,depth,params,lab('stage3_brick_load'),lab('stage3_panel'),labels
 def serial(v):
  if hasattr(v,'tolist'):return v.tolist()
  if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
  if isinstance(v,(list,tuple)):return [serial(x) for x in v]
  return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)
 def calibration(params,frame):
  cm=UsdGeom.XformCache().GetLocalToWorldTransform(cp);camera=UsdGeom.Camera(cp)
  world=np.array(cm,dtype=float).T;rotation=world[:3,:3].copy();scale=np.linalg.norm(rotation,axis=0);rotation=rotation/scale
  assert np.allclose(rotation.T@rotation,np.eye(3),atol=1e-6),'CAMERA_SHEAR'
  optical=np.eye(4);optical[:3,:3]=rotation@np.diag([1,-1,-1]);optical[:3,3]=world[:3,3]*units
  return cm,camera,scale,optical
 panel_log={'occlusion':a.occlusion,'panel_prim':PANEL,'collision_api':False,'events':[]}
 if a.occlusion in ('O25','O50'):
  assert panel_vis.Get()=='invisible'
  rgb_absent,_,_,_,_,_=render();Image.fromarray(rgb_absent).save(EV/'rgb_panel_absent_eval_only.png')
  panel_vis.Set('inherited');panel_log['events'].append({'action':'panel_visible','wall_s':time.time(),'sim_s':sim_time()})
 rgb,depth,params,visible,panel_mask,labels=render()
 cm=UsdGeom.XformCache().GetLocalToWorldTransform(cp)
 if not np.allclose(np.array(before_camera),np.array(cm),atol=1e-10) or timeline.is_playing():raise RuntimeError('Camera moved or timeline playing')
 assert rgb.shape==(480,640,3) and depth.shape==(480,640),'CAPTURE_BUFFERS_INVALID'
 np.save(O/'front_depth.npy',depth,allow_pickle=False);np.save(O/'front_rgb.npy',rgb,allow_pickle=False);Image.fromarray(rgb).save(O/'front_rgb.png');Image.open(O/'front_rgb.png').verify()
 if visible is not None:np.save(EV/'gt_target_mask_visible.npy',visible);np.save(EV/'gt_panel_mask.npy',panel_mask)
 emit('camera_params_raw.json',serial(params))
 cm,camera,scale,optical=calibration(params,1)
 focal=camera.GetFocalLengthAttr().Get();ha=camera.GetHorizontalApertureAttr().Get();va=camera.GetVerticalApertureAttr().Get();sim_now=timeline.get_current_time()
 emit('capture_calibration_evidence.json',{'usd_camera_focal_aperture':[focal,ha,va],'usd_camera_world_matrix_row':serial(cm),'optical_world_matrix_column':serial(optical),'removed_camera_transform_scale':serial(scale),'stage_meters_per_unit':units,'annotator':'distance_to_image_plane','depth_unit_m':1.,'same_render_product':str(product.path),'completed_render_step':1,'timeline_time':sim_now,'rgb_shape':list(rgb.shape),'depth_shape':list(depth.shape)})
 cal={'width':640,'height':480,'fx':float(np.array(params['cameraProjection']).reshape(4,4)[0,0])*320,'fy':float(np.array(params['cameraProjection']).reshape(4,4)[1,1])*240,'cx':320.,'cy':240.,'depth_semantic':'distance_to_image_plane','depth_unit_m':1.,'T_world_optical':serial(optical),'frame_id':1,'sim_time':sim_now,'provenance':{'camera_prim':CAMERA,'calibration_sha256':sha(O/'capture_calibration_evidence.json'),'convention':'optical_right_down_forward_world_m_column'}}
 renderer_view=np.array(params['cameraViewTransform']).reshape(4,4);renderer_world=np.linalg.inv(renderer_view).T;renderer_opt=renderer_world.copy();renderer_opt[:3,:3]=renderer_world[:3,:3]@np.diag([1,-1,-1])
 checks={'projection_fx_positive':cal['fx']>0,'projection_fy_positive':cal['fy']>0,'resolution_match':list(params['renderProductResolution'])==[640,480],'stage_unit_match':bool(np.isclose(float(params['metersPerSceneUnit']),units,atol=1e-9)),'renderer_optical_world_match':bool(np.allclose(renderer_opt,optical,atol=1e-8)),'synchronous_one_render_product':True,'timeline_stopped':not timeline.is_playing()}
 emit('camera_metadata.json',{'calibration':cal,'checks':checks,'raw_parameters':serial(params),'depth_valid_pixels':int(np.count_nonzero(np.isfinite(depth)&(depth>0))),'physics_play_calls':0,'source_usd':str(O/'site_drive.usda')})
 assert all(checks.values()),checks
 if a.occlusion in ('O25','O50'):
  panel_vis.Set('invisible');panel_log['events'].append({'action':'panel_hidden_before_motion','wall_s':time.time(),'sim_s':sim_time()})
  rgb_after,_,_,_,_,_=render();Image.fromarray(rgb_after).save(EV/'rgb_after_panel_removal_eval_only.png')
  fx=json.loads(Path(a.panel_fixture).read_text());u0,v0,u1,v1=[int(round(x)) for x in fx['panel_screen_rect']]
  roi=(slice(max(0,v0+2),min(480,v1-2)),slice(max(0,u0+2),min(640,u1-2)))
  d_on=float(np.abs(rgb[roi].astype(float)-rgb_absent[roi].astype(float)).mean());d_after=float(np.abs(rgb_after[roi].astype(float)-rgb_absent[roi].astype(float)).mean())
  panel_log.update(panel_rect_px=[u0,v0,u1,v1],rgb_mean_abs_diff_panel_on_vs_absent=d_on,rgb_mean_abs_diff_after_removal_vs_absent=d_after,
                   measured_occlusion_eval_only=fx['coverage'],occlusion_definition='B1 v02 primary: |canonical HR target mask & rendered panel| / |canonical| from the locked fixture (shared by HR/LR/CAD)')
  assert d_on>10.,'PANEL_NOT_RENDERED_DURING_CAPTURE'
  assert d_after<3. and panel_vis.Get()=='invisible','PANEL_NOT_REMOVED_BEFORE_MOTION'
 panel_log['panel_visibility_before_motion']=panel_vis.Get();emit('panel_removed.json',panel_log)
 # Evaluation-only GT geometry (never read by perception/planner/controller).
 bb=UsdGeom.BBoxCache(Usd.TimeCode.Default(),['default','render'],False,True)
 lb=bb.ComputeWorldBound(stage.GetPrimAtPath(LOAD)).ComputeAlignedRange();fb=bb.ComputeWorldBound(stage.GetPrimAtPath(FIXTURE)).ComputeAlignedRange()
 emit_ev('gt_geometry_eval_only.json',{'design_center_xy':[-25.888,30.509],'design_task_yaw_deg':90.,'canonical_final_xy':[-25.888,30.509-1.403745031260775],'canonical_pre_xy':[-25.888,30.509-2.203745031260775],'load_bbox_world':[list(lb.GetMin()),list(lb.GetMax())],'fixture_bbox_world':[list(fb.GetMin()),list(fb.GetMax())],'fixture_children':[str(c.GetPath()) for c in stage.GetPrimAtPath(FIXTURE).GetChildren()],'semantic_labels':serial(labels) if labels else None,'target_visible_px':int(visible.sum()) if visible is not None else None})
 emit('capture_internal_result.json',{'status':'PASS','capture':'PASS','timeline_playing':timeline.is_playing(),'capture_count':1,'files_complete_before_shutdown':True})
 checkpoint(O,'after_capture',stage)
 if a.mode=='fixture':
  # ---------- B1 rule (scripts/b1_occlusion_capture_20261109_v02.py): plane perpendicular to optical axis at .85*near depth of
  # the load (pallet+bricks) bbox; screen rectangle from one side (seed parity) to the canonical-mask column-CDF target; vertical
  # extent = canonical bbox +-6 px; <=2 secant refinements on the RENDERED panel mask coverage (tol .5 pp). GT = fixture setup only.
  assert a.representation=='HR_Scan' and a.load=='L4' and a.occlusion=='O0','FIXTURE_REQUIRES_HR_L4_O0'
  assert a.fixture_coverage in (.25,.5),'FIXTURE_COVERAGE_NOT_DECLARED'
  C=visible.copy();yy,xx=np.where(C);assert C.sum()>=100,'CANONICAL_TOO_SMALL'
  # Camera prim carries a NON-UNIFORM xform scale; use the scale-free optical matrix (x right, y down, z forward, metres).
  OPT=np.array(cal['T_world_optical'],float);OPTi=np.linalg.inv(OPT);M=OPT;W,H=640,480;FX=cal['fx'];FY=cal['fy'];CX,CY=320.,240.
  corners=[np.array([x,y,z,1.]) for x in (fb.GetMin()[0],fb.GetMax()[0]) for y in (fb.GetMin()[1],fb.GetMax()[1]) for z in (fb.GetMin()[2],fb.GetMax()[2])]
  near=float(min((OPTi@c)[2] for c in corners));z_p=.85*near;assert .05<z_p<near,'PANEL_NOT_IN_FRONT'
  seed=4004945975;side='left' if seed%2==0 else 'right'
  def xstar(C,t,side):
   cols=C.sum(axis=0).astype(float);tot=cols.sum()
   if side=='right':cols=cols[::-1]
   cdf=np.cumsum(cols)/tot;t=min(max(t,1e-4),1-1e-4);i=int(np.searchsorted(cdf,t));prev=cdf[i-1] if i>0 else 0.
   x=i+(t-prev)/max(cdf[i]-prev,1e-9);return x if side=='left' else W-x
  y_lo,y_hi=float(yy.min()-6),float(yy.max()+1+6);t=float(a.fixture_coverage);t_adj=t;hist=[]
  for it in range(3):
   xs=xstar(C,t_adj,side);x_lo,x_hi=(float(xx.min()-6),xs) if side=='left' else (xs,float(xx.max()+1+6))
   pts=[(OPT@np.array([(u-CX)/FX*z_p,(v-CY)/FY*z_p,z_p,1.]))[:3] for (u,v) in [(x_lo,y_lo),(x_hi,y_lo),(x_hi,y_hi),(x_lo,y_hi)]]
   from pxr import Vt
   UsdGeom.Mesh(stage.GetPrimAtPath(PANEL)).GetPointsAttr().Set(Vt.Vec3fArray([Gf.Vec3f(*[float(v) for v in q]) for q in pts]));UsdGeom.Mesh(stage.GetPrimAtPath(PANEL)).GetExtentAttr().Set(UsdGeom.PointBased.ComputeExtent(Vt.Vec3fArray([Gf.Vec3f(*[float(v) for v in q]) for q in pts])))
   panel_vis.Set('inherited');frgb,_,_,fvis,P,_=render();panel_vis.Set('invisible')
   cov=float((C&P).sum()/C.sum());hist.append({'iter':it,'t_adj':t_adj,'x_star':xs,'panel_px':int(P.sum()),'canonical_coverage':cov,'visible_occlusion':float(1-(fvis&C).sum()/C.sum())})
   if abs(cov-t)<=.005 or it==2:break
   t_adj=min(max(t_adj+(t-cov),.01),.99)
  Image.fromarray(frgb).save(O/'fixture_panel_rgb.png')
  fixture={'status':'FIXTURE_READY' if P.sum()>0 and abs(cov-t)<=.02 else 'FIXTURE_NOT_ACHIEVED','rule':'B1 occlusion v02 (PANEL_DEPTH_FRAC .85, MARGIN 6, TOL_REFINE .005, MAX_REFINE 2, ACHIEVE_PP .02, side=seed parity)','nominal':t,'coverage':cov,'achieved':abs(cov-t)<=.02,'refine':hist,'side':side,'scenario_seed':seed,'base_scenario':'stage4 start %s (red C100)'%START_LOCK,'start_xy_yaw_deg':START_LOCK,'panel_depth_m':z_p,'target_near_depth_m':near,'panel_world_corners':[[float(c) for c in q] for q in pts],'panel_screen_rect':[x_lo,y_lo,x_hi,y_hi],'panel_world_min_z':min(float(q[2]) for q in pts),'canonical_px':int(C.sum()),'canonical_source':'HR_Scan L4 O0 GT visible target mask at the settled locked start (fixture setup only; shared by HR/LR/CAD)','appearance':'UsdPreviewSurface diffuse .45 grey, roughness .9, metallic 0','collision_api':False,'T_world_optical':OPT.tolist(),'settled_start':settled,'GT_role':'fixture_setup_only_no_perception_inputs'}
  emit('stage4_panel_fixture.json',fixture);result.update(status='FIXTURE_RECORDED' if fixture['status']=='FIXTURE_READY' else 'FIXTURE_FAILED',fixture=fixture['status'])
  raise SystemExit(0)
 from evaluation.construction_site_graph_20261101_v15 import check as check_capture_graph
 check_capture_graph(graph_lock,graph_signature(stage))
 emit('graph_capture_invariant.json',{'pass':True,'actuation_unchanged':True,'wall_s':time.time()})
 emit('capture_stability.json',{'before':capture_start,'after':pose(),'physical_before':capture_physics,'physical_after':sim_time()})
 assert math.dist(capture_start[:3],pose()[:3])<.0001 and abs(sim_time()-capture_physics)<1e-9,'CAPTURE_PHYSICAL_MOVEMENT'
 physx_gate(stage,query,clearance,O)
 expected_bodies=['base_link','front_left_steer_link','front_right_steer_link','middle_left_wheel_link','middle_right_wheel_link','rear_left_steer_link','rear_right_steer_link','front_left_wheel_link','front_right_wheel_link','rear_left_wheel_link','rear_right_wheel_link']
 live={'body_joint_identity':list(art.body_names)==expected_bodies and names==DOF,'camera_base_invariant':math.dist(capture_start[:3],pose()[:3])<.0001,'supplier_graph':check_capture_graph(graph_lock,graph_signature(stage)) is True,'wheel_support':bool(support_ok and shell_safe),'registered_C_common_colliders':json.loads((O/'pilot_physx_C.json').read_text())['pass'] is True,'safety_consumer_C_colliders':len(json.loads((O/'pilot_physx_C.json').read_text())['safety_consumer_cells'])==int(SCENARIO['expected_bricks'])+5,'unexpected_contacts_clear':all(c['collider0'] in allowed_support or c['collider1'] in allowed_support for c in contacts)}
 diagnostic=assess(stage,physics_errors,live)
 emit('pilot_physical_admission.json',diagnostic)
 assert diagnostic['pass'],'PILOT_PHYSICAL_ADMISSION_NO_GO'
 # Automatic render admission (v27 render_review checks without the human wait).
 import itertools
 box=UsdGeom.BBoxCache(Usd.TimeCode.Default(),['default','render','proxy','guide'],False,True).ComputeWorldBound(stage.GetPrimAtPath('/World/ENG_FE2E/Rover/base_link/MountedRolltainer/AssetRef/rolltainer_body/Plane')).ComputeAlignedBox()
 corners=np.array(list(itertools.product(*zip(box.GetMin(),box.GetMax()))));optc=np.column_stack([corners,np.ones(8)])@np.linalg.inv(np.array(cal['T_world_optical'])).T;x_,y_,z_=optc[:,:3].T
 nearc,farc=UsdGeom.Camera(cp).GetClippingRangeAttr().Get()
 planes={'near':z_-nearc,'far':farc-z_,'left':cal['fx']*x_+cal['cx']*z_,'right':(640-cal['cx'])*z_-cal['fx']*x_,'top':cal['fy']*y_+cal['cy']*z_,'bottom':(480-cal['cy'])*z_-cal['fy']*y_}
 outside_planes=[k for k,v in planes.items() if bool(np.all(v<0))]
 fatal=[line for line in (O.parent/'runtime.log').read_text(errors='replace').splitlines() if any(t in line.lower() for t in ['failed to compile','failed to load texture','failed to resolve','mdl compiler error'])]
 emit('render_auto_admission.json',{'plane_outside_frustum':outside_planes,'depth_valid_pixels':int(np.count_nonzero(np.isfinite(depth)&(depth>0))),'fatal_shader_lines':fatal[:20],'human_review':False,'pass':bool(outside_planes) and not fatal and all(checks.values())})
 assert outside_planes,'PLANE_MAY_ENTER_ANALYSIS_ROI';assert not fatal,'ACTIVE_RENDER_SHADER_FAILURE'
 checkpoint(O,'pre_perception_memory_admission',stage)
 from evaluation.construction_site_runtime_20261101_v19b import rss as owner_rss
 assert owner_rss()<=8*1024**3,'GC_MEMORY_BOUND_PRE_PERCEPTION'
 # ---------------- perception + pose (sensor-only subprocess) ----------------
 stage3_stage='perception'
 command=['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_v02_stage4_perception_task_prior_20261112_v02.py'),'--capture',str(O),'--representation',a.representation,'--layer-count',str(LAYER_COUNT),'--pose-method',a.pose_method,'--mode','initial']
 PARENT=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01')
 registry=PARENT/'DRIVE540_20261113_v01/single_load_amendment_v01/operator_task_registry.json';models=PARENT/'MIX_C06_20261112_v01/selection_lock.json'
 command+=['--task-metadata',SCENARIO['task_metadata'],'--task-registry',str(registry),'--task-registry-sha',sha(registry),'--model-lock',str(models),'--model-lock-sha',sha(models)]
 emit('perception_command.json',{'argv':command,'GT_input':False,'gt_dir_not_passed':str(EV),'input_contract':'single-load known occupied task layer only; no construction or GT files passed'})
 with (O/'perception.log').open('x') as log:
  worker=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=300)
 checkpoint(O,'after_perception',stage,{'worker_exit':worker.returncode})
 perc=json.loads((O/'perception_result.json').read_text())
 if perc['status']!='TARGETS_READY':raise RuntimeError(('PERCEPTION_NO_DETECTION' if perc['status']=='NO_DETECTION' else 'POSE_'+str(perc.get('pose_reason') or perc['status']) if perc['status']=='POSE_FAILED' else 'PERCEPTION_EXCEPTION')+':'+str(perc.get('failure_reason','')))
 if a.record_robotcam:
  (O/'rec_robotcam').mkdir()
  def recorder(rstep,rsim):
   t0=time.monotonic()
   try:
    d=rgb_ann.get_data();arr=np.asarray(d['data'] if isinstance(d,dict) else d)
    if arr.ndim==3 and arr.shape[0]==480:Image.fromarray(arr[...,:3].copy()).save(O/'rec_robotcam'/('%06d_%09.3f.jpg'%(rstep,rsim)),quality=85);rec_stats['frames']+=1
   except Exception as exc:rec_stats['errors']+=1;rec_stats['last_error']=repr(exc)
   dt=time.monotonic()-t0;rec_stats['seconds']+=dt;rec_stats['max_s']=max(rec_stats['max_s'],dt)
 targets=json.loads((O/'predicted_pre_final.json').read_text())['targets']
 pre=[targets['pre_x_m'],targets['pre_y_m']];final=[targets['final_x_m'],targets['final_y_m']]
 # ---------------- planning (TC-S, all groups) + swept clearance + live support ----------------
 stage3_stage='planning'
 from stage3_local_planner_20261109_v01 import plan as plan_tcs, feedforward_steer_rate, baseline_quintic_peak, bangbang_lower_bound, classify_rejection
 from construction_site_sweep_20261101_v14 import swept_corridor
 def admit_path(label,goal,out_name,source):
  current=pose();start3=(current[0],current[1],current[3]);goal3=(*goal,math.pi/2);info={'arm':a.arm,'label':label,'start':current,'goal':goal}
  try:
   path,metrics=plan_tcs(start3,goal3);info.update(planner='stage3_local_planner_20261109_v01.plan (TC-S)',tcs_metrics={k:v for k,v in metrics.items() if k!='rho_trials'})
  except ValueError as exc:
   info.update(reason=str(exc),baseline_peak=baseline_quintic_peak(start3,goal3),bangbang_lb=bangbang_lower_bound(start3,goal3),classification=classify_rejection(start3,goal3,str(exc)));emit(label+'_plan_rejected.json',info)
   raise RuntimeError('PLAN_REJECTED:'+str(exc))
  info.update(peak_abs_k=max(abs(q[3]) for q in path),ff_steer_rate_deg_s=feedforward_steer_rate(path),n_rows=len(path))
  route=swept_corridor(stage,path);emit(label+'_swept.json',route)
  if route['status']!='PASS':emit(label+'_plan_rejected.json',dict(info,reason='FOOTPRINT_CLEARANCE_FAIL',sweep_failure=route['failure']));raise RuntimeError('FOOTPRINT_CLEARANCE_FAIL:'+label+':'+str(route['failure']))
  checks=[]
  for sample in route['support_samples']:
   xx,yy,zz=sample['xyz'];hits=[]
   def hit(h):
    if str(h.collision) in allowed_support and abs(float(h.position[2])-zz)<=.01:hits.append(str(h.collision))
    return True
   query.raycast_all((xx,yy,zz+.04),(0.,0.,-1.),.08,hit,backface_proven)
   if not hits:checks.append(sample)
  emit(label+'_live_support.json',{'pass':not checks,'count':len(route['support_samples']),'failed':checks[:20]})
  if checks:raise RuntimeError('FOOTPRINT_CLEARANCE_FAIL:'+label+'_CURVED_LIVE_SUPPORT_FAILED')
  emit_atomic(out_name,{'path':path,'goal':goal,'start':current,'source':str(source),'source_sha256':sha(source),'kinematic_max_curvature':max(abs(q[3]) for q in path),'admission':info})
  return path
 from evaluation.stage4_ablation_b_logic_20261110_v01 import waypoint, b_decision, is_plan_fallback, leg_kind, certificate_leg_label, leg_bounds
 PRED0=O/'predicted_pre_final.json';pre_init,final_init=pre,final
 b_log={'enabled_requested':CORR_B,'pose_method':a.pose_method,'events':[],'decision':None,'wp_rule':'W on straight chord start->PRE_init at y=PRE_init_y-%.2f m, yaw 90 deg'%a.wp_back_m}
 if CORR_B:
  st0=pose();b_log.update(start=st0)
  try:
   try:W,lam=waypoint(st0[:2],pre_init,a.wp_back_m);b_log.update(W=W,chord_fraction=lam)
   except ValueError as exc:raise RuntimeError('PLAN_REJECTED:'+str(exc))
   active_path=admit_path('leg_0_W',W,'leg_0_path.json',PRED0);goals=[W,None,None]
  except RuntimeError as exc:
   if not is_plan_fallback(exc):raise
   b_log['events'].append({'event':'B_FALLBACK_NO_W','reason':str(exc)});b_log['decision']='B_FALLBACK_NO_W';CORR_B=False;emit('correction_b.json',b_log)
 if not CORR_B:
  active_path=admit_path('leg_0',pre,'leg_0_path.json',PRED0);goals=[pre,final]
 n_legs=len(goals);bounds_sim,bounds_wall,driver_total_wall=leg_bounds(n_legs)
 emit('observed_route_admission.json',{'start':settled,'PRE':pre,'FINAL':final,'goals_initial':goals,'n_legs':n_legs,'correction_b':CORR_B,'pose_method':a.pose_method,'motion_authorized':True,'manual_ROI_review':None,'automatic_sensor_ROI':True,'arm':a.arm,'sequential_corridor':'leg 0 sweep now; each later leg planned and swept after the previous certified stop'})
 emit('live_goals.json',{'goals':goals,'n_legs':n_legs,'source_sha256':sha(PRED0),'tolerance_m':.005,'speed_cap_request_m_s':.02,'leg_sim_bounds_s':bounds_sim,'leg_wall_bounds_s':bounds_wall,'driver_total_wall_s':driver_total_wall,'note':'goals of legs >0 may be replanned after the previous certified stop'})
 checkpoint(O,'pre_drive',stage)
 if a.mode!='drive':raise RuntimeError('MODE_NOT_DRIVE')
 def reobserve():
  """Correction B at the certified W stop (timeline paused): unchanged capture path + checks, re-detect/re-identify/pose, replan."""
  global active_path
  RD=O/'reobs';RD.mkdir();t_start=time.time();ev={'W_stop_pose':pose(),'sim_s':sim_time(),'wall_s':t_start}
  assert not timeline.is_playing(),'REOBS_TIMELINE_PLAYING'
  cam_before=UsdGeom.XformCache().GetLocalToWorldTransform(cp);p_before=pose();s_before=sim_time()
  rgb2,depth2,params2,_,_,_=render()
  if not np.allclose(np.array(cam_before),np.array(UsdGeom.XformCache().GetLocalToWorldTransform(cp)),atol=1e-10) or timeline.is_playing():raise RuntimeError('CAPTURE_REOBS_CAMERA_MOVED_OR_PLAYING')
  assert rgb2.shape==(480,640,3) and depth2.shape==(480,640),'CAPTURE_REOBS_BUFFERS_INVALID'
  np.save(RD/'front_depth.npy',depth2,allow_pickle=False);np.save(RD/'front_rgb.npy',rgb2,allow_pickle=False);Image.fromarray(rgb2).save(RD/'front_rgb.png');Image.open(RD/'front_rgb.png').verify()
  with (RD/'camera_params_raw.json').open('x') as f:json.dump(serial(params2),f,indent=2)
  cm2,camera2,scale2,optical2=calibration(params2,2)
  with (RD/'capture_calibration_evidence.json').open('x') as f:json.dump({'usd_camera_focal_aperture':[camera2.GetFocalLengthAttr().Get(),camera2.GetHorizontalApertureAttr().Get(),camera2.GetVerticalApertureAttr().Get()],'usd_camera_world_matrix_row':serial(cm2),'optical_world_matrix_column':serial(optical2),'removed_camera_transform_scale':serial(scale2),'stage_meters_per_unit':units,'annotator':'distance_to_image_plane','depth_unit_m':1.,'same_render_product':str(product.path),'completed_render_step':2,'timeline_time':timeline.get_current_time()},f,indent=2)
  cal2={'width':640,'height':480,'fx':float(np.array(params2['cameraProjection']).reshape(4,4)[0,0])*320,'fy':float(np.array(params2['cameraProjection']).reshape(4,4)[1,1])*240,'cx':320.,'cy':240.,'depth_semantic':'distance_to_image_plane','depth_unit_m':1.,'T_world_optical':serial(optical2),'frame_id':2,'sim_time':timeline.get_current_time(),'provenance':{'camera_prim':CAMERA,'calibration_sha256':sha(RD/'capture_calibration_evidence.json'),'convention':'optical_right_down_forward_world_m_column'}}
  rv=np.array(params2['cameraViewTransform']).reshape(4,4);rw=np.linalg.inv(rv).T;ro=rw.copy();ro[:3,:3]=rw[:3,:3]@np.diag([1,-1,-1])
  checks2={'projection_fx_positive':cal2['fx']>0,'projection_fy_positive':cal2['fy']>0,'resolution_match':list(params2['renderProductResolution'])==[640,480],'stage_unit_match':bool(np.isclose(float(params2['metersPerSceneUnit']),units,atol=1e-9)),'renderer_optical_world_match':bool(np.allclose(ro,optical2,atol=1e-8)),'synchronous_one_render_product':True,'timeline_stopped':not timeline.is_playing()}
  with (RD/'camera_metadata.json').open('x') as f:json.dump({'calibration':cal2,'checks':checks2,'raw_parameters':serial(params2),'depth_valid_pixels':int(np.count_nonzero(np.isfinite(depth2)&(depth2>0))),'physics_play_calls':0,'source_usd':str(O/'site_drive.usda'),'capture':'reobservation_at_W'},f,indent=2)
  assert all(checks2.values()),('CAPTURE_REOBS_CHECKS',checks2)
  check_capture_graph(graph_lock,graph_signature(stage))
  assert math.dist(p_before[:3],pose()[:3])<.0001 and abs(sim_time()-s_before)<1e-9,'CAPTURE_REOBS_PHYSICAL_MOVEMENT'
  box2=UsdGeom.BBoxCache(Usd.TimeCode.Default(),['default','render','proxy','guide'],False,True).ComputeWorldBound(stage.GetPrimAtPath('/World/ENG_FE2E/Rover/base_link/MountedRolltainer/AssetRef/rolltainer_body/Plane')).ComputeAlignedBox()
  corners2=np.array(list(itertools.product(*zip(box2.GetMin(),box2.GetMax()))))
  optc2=np.column_stack([corners2,np.ones(8)])@np.linalg.inv(np.array(cal2['T_world_optical'])).T;x2,y2,z2=optc2[:,:3].T
  planes2={'near':z2-nearc,'far':farc-z2,'left':cal2['fx']*x2+cal2['cx']*z2,'right':(640-cal2['cx'])*z2-cal2['fx']*x2,'top':cal2['fy']*y2+cal2['cy']*z2,'bottom':(480-cal2['cy'])*z2-cal2['fy']*y2}
  outside2=[k for k,v in planes2.items() if bool(np.all(v<0))]
  emit('reobs_render_admission.json',{'plane_outside_frustum':outside2,'graph_capture_invariant':True,'checks':checks2,'panel_visibility':panel_vis.Get(),'pass':bool(outside2) and all(checks2.values())})
  assert outside2,'PLANE_MAY_ENTER_ANALYSIS_ROI';assert panel_vis.Get()=='invisible','PANEL_NOT_REMOVED_BEFORE_MOTION'
  assert owner_rss()<=8*1024**3,'GC_MEMORY_BOUND_PRE_REOBS_PERCEPTION'
  command=['/home/user/anaconda3/envs/sdg_tools/bin/python',str(R/'scripts/c_v02_stage4_perception_task_prior_20261112_v02.py'),'--capture',str(RD),'--representation',a.representation,'--layer-count',str(LAYER_COUNT),'--pose-method',a.pose_method,'--mode','reobs','--reference',str(O)]
  emit('reobs_perception_command.json',{'argv':command,'GT_input':False})
  perc2=None
  try:
   with (RD/'perception.log').open('x') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=30)
   perc2=json.loads((RD/'perception_result.json').read_text())
  except Exception as exc:ev['worker_error']=repr(exc)
  ev['perception_status']=None if perc2 is None else perc2.get('status');ev['reid']=None if perc2 is None else perc2.get('reid')
  reobs_status=None if perc2 is None else perc2.get('status');plan_error=None
  if reobs_status=='TARGETS_READY':
   t2=perc2['targets'];pre_c=[t2['pre_x_m'],t2['pre_y_m']];fin_c=[t2['final_x_m'],t2['final_y_m']];ev.update(PRE_corrected=pre_c,FINAL_corrected=fin_c,center_reobs=perc2['predicted_center_xy'])
   try:active_path=admit_path('leg_1_corrected',pre_c,'leg_1_path.json',RD/'predicted_pre_final.json');goals[1],goals[2]=pre_c,fin_c
   except RuntimeError as exc:plan_error=str(exc);ev['corrected_plan_rejection']=plan_error
  decision=b_decision(reobs_status,plan_error)
  if decision!='B_CORRECTED':
   active_path=admit_path('leg_1_fallback',pre_init,'leg_1_path.json',PRED0);goals[1],goals[2]=pre_init,final_init
  ev.update(decision=decision,PRE_used=goals[1],FINAL_used=goals[2],PRE_initial=pre_init,FINAL_initial=final_init,duration_wall_s=time.time()-t_start)
  b_log['decision']=decision;b_log['events'].append(dict(ev,event=decision));emit('correction_b.json',b_log)
 # ---------------- ROS driving (unchanged v30 sequence, N legs) ----------------
 stage3_stage='ros_isolation'
 motion_gc.enter()
 timeline.play()
 deadline=time.monotonic()+8;status=None
 while time.monotonic()<deadline:
  tick()
  if (O/'ros_status.json').exists():
   status=json.loads((O/'ros_status.json').read_text())
   if fresh_tf_status(status,time.time(),sim_time()):break
 assert fresh_tf_status(status,time.time(),sim_time()),'NO_FRESH_TARGET_TF'
 tf=status['tf'];others=[x for x in status['cmd_subscribers'] if x['node']!='eng_smoke_observer'];good=str(status['domain'])==str(a.domain) and len(status['tf_publishers'])==1 and len(others)==1 and not status['cmd_publishers'] and status['commands']==0 and math.hypot(tf['x_m']-settled[0],tf['y_m']-settled[1])<.002 and abs(tf['stamp_s']-sim_time())<.1
 emit('isolation_check.json',{'pass':good,'status':status,'expected_prim':BASE});assert good,'ISOLATION_FAILED'
 endpoint_guard.check(status,'isolated',time.time(),sim_time())
 admitted=True
 emit('isolation_verified.json',{'pass':True,'domain':a.domain,'target':BASE,'verified_before_nonzero':True})
 emit('settling.json',{'pose':settled,'quiet':basequiet,'baseline_sim_s':records[-1]['sim_s']})
 discovery_started=time.monotonic()
 child=ros(['/usr/bin/python3',str(R/'scripts/stage4_ablation_drive_ros_20261110_v01.py'),'--output',str(O)],'calibration_ros_stdout.log')
 ros_ready=False;ros_failure=None
 deadline=time.monotonic()+5
 try:
  while time.monotonic()<deadline:
   tick()
   st=json.loads((O/'ros_status.json').read_text())
   if discovery_check(endpoint_guard,st,time.time(),sim_time(),O,discovery_started) and (O/'driver_ready.json').exists():ros_ready=True;break
   if (O/'driver_guard_fault.json').exists():raise RuntimeError('ROS_CHILD_DISCOVERY_FAILED')
 except Exception as exc:ros_failure=str(exc)
 emit('discovery_result.json',{'admitted':ros_ready,'failure':ros_failure,'wait_s':time.monotonic()-discovery_started,'final_snapshot':st})
 assert ros_ready,'DISCOVERY_TIMEOUT:ROS_REQUIRED_NO_NATIVE_FALLBACK:'+str(ros_failure)
 result['driving_mode']='ROS';emit('driver_admitted.json',{'pass':True,'domain':a.domain,'wall_s':time.time()})
 stage3_stage='drive_leg_0'
 phase='pulse';emit('pulse_start.json',{'sim_s':sim_time(),'wall_s':time.time(),'source':'fresh observed targets; automatic sensor ROI; n_legs=%d'%n_legs})
 result['motion_attempts']=1;leg_results=[];leg_start=sim_time();leg_wall=time.monotonic();cert_last_eval={}
 while child.poll() is None and not (O/'abort_motion').exists():
  tick()
  leg=len(leg_results)
  assert sim_time()-leg_start<(bounds_sim[min(leg,n_legs-1)]+12.),'MOVE_SIM_TIMEOUT:LEG_SIM_TIMEOUT'
  assert time.monotonic()-leg_wall<bounds_wall[min(leg,n_legs-1)],'PHASE_WALL_TIMEOUT:LEG_WALL_TIMEOUT'
  if (O/'adapter_commands.jsonl').exists():
   commands=command_tail.poll()
   segment=[x for x in commands if x.get('leg')==leg]
   # stage-3 v02 timing fix retained: evaluate the unchanged certificate only >=1.0 s sim after the first ZERO_SETTLING command, then every 0.1 s sim.
   zero_cmd=next((x for x in segment if x['adapter']['state']=='ZERO_SETTLING'),None)
   due=zero_cmd is not None and segment[-1]['adapter']['state']=='ZERO_SETTLING' and records[-1]['sim_s']-zero_cmd['sim_s']>=1.0 and records[-1]['sim_s']-cert_last_eval.get(leg,-1e9)>=.1
   if due:cert_last_eval[leg]=records[-1]['sim_s']
   cert_leg=certificate_leg_label(leg)  # pure relabel for the unchanged 2-leg certificate (criteria identical)
   cert=confirmed_stop(records,[dict(x,leg=cert_leg) for x in segment],safety_ok=not (O/'driver_guard_fault.json').exists(),drive=drive_contract,goal=goals[leg],leg=cert_leg,previous_end=leg_results[leg-1]['stop']['end_sim_s'] if leg>=1 else None) if due else {'confirmed':False}
   if cert['confirmed'] and leg<n_legs:
    goal=goals[leg];terminal=pose();error=math.dist(terminal[:2],goal);yaw=math.degrees(math.atan2(math.sin(terminal[3]-math.pi/2),math.cos(terminal[3]-math.pi/2)))
    entry={'leg':leg,'goal':goal,'pose':terminal,'distance_m':error,'yaw_error_deg':yaw,'reached':error<=.005 and abs(yaw)<=2,'stop':cert,'sim_s':sim_time(),'certificate_leg_label':cert_leg,'kind':leg_kind(leg,n_legs,CORR_B)}
    emit_atomic('leg_'+str(leg)+'_stop.json',entry);leg_results.append(entry);snap('legs_result.json',leg_results)
    assert entry['reached'],'OBSERVED_GOAL_NOT_REACHED'
    if leg<n_legs-1:
     emit_atomic('leg_validation_pause.json',{'leg':leg+1,'wall_s':time.time()})
     timeline.pause()
     emit('leg_%d_pause_barrier.json'%leg,pause_barrier(app,timeline,sim_time))
     if CORR_B and leg==0:
      stage3_stage='reobservation';rs0=owner_rss();motion_gc.restore();gc.collect();rs1=owner_rss()
      b_log['gc_rescope']={'rss_before_collect':rs0,'rss_after_collect':rs1,'scope1':motion_gc.events[-1]}
      reobserve()
      motion_gc.enter();b_log['gc_rescope']['scope2_base']=motion_gc.base;emit_atomic('gc_rescope_at_W.json',b_log['gc_rescope'])
     else:
      stage3_stage='planning_leg_%d'%(leg+1)
      active_path=admit_path('leg_%d'%(leg+1),goals[leg+1],'leg_%d_path.json'%(leg+1),(O/'reobs'/'predicted_pre_final.json') if (CORR_B and b_log.get('decision')=='B_CORRECTED') else PRED0)
     stage3_stage='drive_leg_%d'%(leg+1)
     timeline.play()
     deadline=time.monotonic()+5
     while time.monotonic()<deadline:
      app.update();time.sleep(.02)
      status=json.loads((O/'ros_status.json').read_text())
      if fresh_tf_status(status,time.time(),sim_time()):break
     assert fresh_tf_status(status,time.time(),sim_time()),'TF_STALE:LEG_RESUME_TF_STALE'
     tick()
     (O/'leg_validation_pause.json').unlink()
     emit_atomic('next_leg_%d.json'%(leg+1),{'leg':leg+1,'previous_stop_sha256':sha(O/('leg_%d_stop.json'%leg))});leg_start=sim_time();leg_wall=time.monotonic()
    else:
     snap('stop_confirmed.json',dict(cert,wall_s=time.time()));phase='zero_stop'
     completion_deadline=time.monotonic()+5.
     while child.poll() is None and time.monotonic()<completion_deadline:tick()
     break
 assert child.poll()==0 and len(leg_results)==n_legs,'LEGS_INCOMPLETE'
 for _ in range(75):tick()
 commands=command_tail.poll()
 outcome=outcomes(records,commands);emit('stop_quiet_result.json',outcome)
 driver_result=json.loads((O/'calibration_ros_complete.json').read_text())
 success_candidate=all(x['reached'] for x in leg_results) and driver_result['completion_accepted'] and outcome['QUIET']=='PASS'
 result.update(outcomes=outcome,driver_result=driver_result,legs=leg_results,n_legs=n_legs,lifecycle_confirmed=success_candidate,base_stop_confirmed=outcome['QUIET']=='PASS',status='DRIVE_COMPLETED')

except SystemExit:
 pass
except Exception as exc:
 result.update(status='NOT_READY',failure_reason=str(exc),failure_stage=stage3_stage,traceback=traceback.format_exc())
 if O.exists():(O/'abort_motion').touch()
 if observer is not None and (O/'isolation_verified.json').exists() and not (O/'zero_request.json').exists():emit('zero_request.json',{'domain':a.domain,'time':time.time(),'exception':True})
 if app is not None and timeline is not None and child is not None:
  recovery_start=len(records)
  try:
   child.wait(timeout=3)
   assert child.poll()==0,'ZERO_RECOVERY_DRIVER_EXIT'
   req=json.loads((O/'zero_request.json').read_text())
   receipt=await_cleanup_receipt(O,a.domain,req,observer,timeout_s=3.)
   assert receipt['valid'],'ZERO_RECOVERY_RECEIPT_MISSING'
   assert eligible_fault(str(exc)),'FAULT_NOT_SAFE_FOR_ZERO_RECOVERY'
   phase='fault_zero_only'
   identity_only_zero_check(endpoint_guard,json.loads((O/'ros_status.json').read_text()),time.time(),sim_time())
   for node in bindings:
    for key in ('velocityCommand','effortCommand'):
     attr=og.Controller.attribute(node+'.inputs:'+key);value=attr.get()
     if value is not None:attr.set([0.]*len(value))
   timeline.pause()
   for _ in range(3):TIMING.call('zero_paused_update',app.update)
   assert all(float(x)==0 for x in graph_array('wheelRotationVelocity')),'ZERO_RECOVERY_GRAPH_NONZERO'
   timeline.play()
   deadline=time.monotonic()+20
   while time.monotonic()<deadline:
    tick()
    if quiet(records[recovery_start:])['status']=='PASS':break
   emit('postfault_quiet.json',dict(quiet(records[recovery_start:]),mode='ZERO_ONLY',new_records=len(records)-recovery_start,receipt=receipt))
  except Exception as recovery_error:
   timeline.pause()
   emit('postfault_quiet.json',{'status':'NOT_READY','reason':str(recovery_error),'new_records':len(records)-recovery_start,'mode':'ZERO_ONLY'})

finally:
 success_candidate=success_candidate and not signal_aborted and not (O/'abort_motion').exists() and not (O/'zero_request.json').exists()
 if result.get('status') not in ('FIXTURE_RECORDED','FIXTURE_FAILED'):result['status_before_cleanup']=result.get('status');result['status']='NOT_READY'
 (O/'abort_motion').touch()
 cleanup_requested=time.time()
 cleanup_request={'domain':a.domain,'time':cleanup_requested,'cleanup':True,'request_id':uuid.uuid4().hex}
 atomic_new(O/'cleanup_zero_request.json',cleanup_request)
 if not (O/'zero_request.json').exists():snap('zero_request.json',cleanup_request)
 if timeline is not None:timeline.pause()
 motion_gc.restore()
 checkpoint(O,'finally_paused',resources={'driver_started':child is not None})
 emit('gc_lifecycle_v19.json',{'events':motion_gc.events,'active':motion_gc.active})
 if app is not None:
  try:
   for node in (bindings if 'bindings' in globals() else []):
    for key in ('velocityCommand','effortCommand'):
     attr=og.Controller.attribute(node+'.inputs:'+key);value=attr.get()
     if value is not None:attr.set([0.]*len(value))
  except Exception as exc:result.update(cleanup_graph_zero_error=str(exc))
 cleanup_receipt=await_cleanup_receipt(O,a.domain,cleanup_request,observer,timeout_s=3.) if observer is not None else {'valid':False,'reason':'NO_OBSERVER_FIXTURE_MODE'}
 result['cleanup_receipt']=cleanup_receipt
 from evaluation.construction_site_mount_invariant_20261102_v26 import cleanup_classification
 emit('cleanup_zero_classification.json',cleanup_classification(child is not None,cleanup_receipt))
 if child is not None and child.poll() is None:
  try:child.wait(timeout=3)
  except subprocess.TimeoutExpired:
   result['process_failure']=True;child.terminate()
   try:child.wait(timeout=5)
   except subprocess.TimeoutExpired:child.kill();child.wait(timeout=3)
 if observer is not None:
  (O/'stop_observer').touch()
  try:observer.wait(timeout=3)
  except subprocess.TimeoutExpired:
   result['process_failure']=True;observer.terminate()
   try:observer.wait(timeout=5)
   except subprocess.TimeoutExpired:observer.kill();observer.wait(timeout=3)
 if (child is not None and child.poll()!=0) or (observer is not None and observer.poll()!=0):result.update(process_failure=True)
 emit('owned_processes.json',{'observer':None if observer is None else {'pid':observer.pid,'exit_code':observer.poll()},'driver':None if child is None else {'pid':child.pid,'exit_code':child.poll()}})
 commands=[]
 try:commands=[json.loads(line) for line in (O/'adapter_commands.jsonl').read_text().splitlines()]
 except (OSError,ValueError):pass
 if 'outcomes' not in result:
  outcome=outcomes(records,commands) if records else {'MOVED':'NO','QUIET':'NOT_TESTED'};emit('stop_quiet_result.json',outcome);result['outcomes']=outcome
 if stream is not None:stream.close()
 emit('contacts.json',contacts)
 if 'physics' in globals():
  clock_stream.close();emit('runtime_summary.json',{'physics':physics,'physics_sim_s':sim_time(),'manager_steps':int(SimulationManager.get_num_physics_steps()),'records':len(records),'clock_first':records[0]['clock'] if records else None,'clock_last':records[-1]['clock'] if records else None,'nonzero_commands':sum(c['wire_v']!=0 or c['wire_z']!=0 for c in commands),'outcomes':result['outcomes']})
 try:
  cr=json.loads((O/'zero_request.json').read_text())
  external_abort=cr.get('cleanup') is not True or cr.get('time')!=cleanup_requested
 except (OSError,ValueError,AttributeError):external_abort=True
 owners_clean=child is not None and child.poll()==0 and observer is not None and observer.poll()==0
 eligible=final_success(success_candidate,cleanup_receipt,owners_clean,external_abort or signal_aborted or (O/'driver_guard_fault.json').exists(),result) if a.mode=='drive' else False
 result['eligible']=bool(eligible)
 if 'actor_cache' in globals():emit('actor_cache_stats.json',{'rebuilds':actor_cache.rebuilds,'prim_checks':actor_cache.prim_checks})
 result['robotcam_recording']=dict(rec_stats,enabled=bool(a.record_robotcam),every_ticks=REC_EVERY);result['group']={'pose_method':a.pose_method,'correction_b':a.correction_b,'start_xy_yaw_deg':START_LOCK};result['correction_b']=globals().get('b_log')
 emit('session_result_stage3.json',{k:v for k,v in result.items() if k not in ('traceback',)}|{'traceback':result.get('traceback')})
 TIMING.flush(O/'session_timing_v18.json')
 persist_before_close(O,result,eligible,os.environ['V10C_RUN_NONCE'],__file__,(lambda:traced_close(O,app.close)) if app is not None else lambda:None)

raise SystemExit(0 if eligible else 1)
