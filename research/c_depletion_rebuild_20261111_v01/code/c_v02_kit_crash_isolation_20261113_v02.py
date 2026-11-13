"""Small actual Kit isolations; every case new process/output. No control/motion commands."""
import argparse,sys,json,time,traceback,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--stage',type=Path);p.add_argument('--graphs-off',action='store_true');p.add_argument('--bridge',action='store_true');a=p.parse_args();O=a.output;O.mkdir(exist_ok=False);app=None;result=dict(state='RUNNING',stage=str(a.stage),graphs_off_diagnostic=a.graphs_off,bridge=a.bridge,started=time.time(),pid=os.getpid(),motion_commands=0)
def mark(phase,**kw):
 result.update(phase=phase,**kw);(O/'progress.json').write_text(json.dumps(result,indent=2));print('DIAG_PHASE',phase,flush=True)
try:
 from isaacsim import SimulationApp
 app=SimulationApp({'headless':True,'width':640,'height':480,'renderer':'RayTracedLighting','multi_gpu':False,'extra_args':['--/app/window/enabled=false','--/metricsAssembler/operationMode=0']});mark('app_created')
 import omni.usd,omni.timeline
 from pxr import Usd,Sdf
 ctx=omni.usd.get_context();omni.timeline.get_timeline_interface().stop()
 if a.bridge:
  from isaacsim.core.utils.extensions import enable_extension
  enable_extension('isaacsim.ros2.bridge');enable_extension('isaacsim.robot.wheeled_robots')
  mark('bridge_enabled')
 if a.stage:
  stage=Usd.Stage.CreateNew(str(O/'diagnostic_copy.usda'));stage.GetRootLayer().subLayerPaths=[str(a.stage)]
  removed=[]
  if a.graphs_off:
   paths=[str(prim.GetPath()) for prim in stage.Traverse() if prim.GetTypeName() in ['OmniGraph','ComputeGraph'] or prim.GetName()=='ActionGraph']
   for path in paths:removed.append(path);stage.GetPrimAtPath(path).SetActive(False)
  stage.GetRootLayer().Save();mark('stage_prepared',diagnostic_graphs_disabled=removed)
  ctx.open_stage(str(O/'diagnostic_copy.usda'));mark('stage_open_called')
 else:ctx.new_stage();mark('empty_stage_created')
 for i in range(60):
  mark('before_update',update_index=i);app.update();mark('after_update',update_index=i)
 result.update(state='PASS_60_UPDATES',ended=time.time());(O/'result.json').write_text(json.dumps(result,indent=2))
except BaseException:
 result.update(state='FAILED_PYTHON',traceback=traceback.format_exc(),ended=time.time());(O/'result.json').write_text(json.dumps(result,indent=2));raise
finally:
 if app:mark('before_close');app.close()
print('DIAG_DONE',flush=True)
