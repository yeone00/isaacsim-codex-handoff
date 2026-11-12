"""Read-only USD composition/live-stage inspector. Never applies physics APIs or advances simulation."""
import hashlib
from pathlib import Path
def audit(stage,mode='CPU_COMPOSITION_ONLY'):
 from pxr import Usd,UsdPhysics
 roles={r:[] for r in ['rover','floor','pallet','load','other']};rigid=[];scenes=[]
 for p in Usd.PrimRange(stage.GetPseudoRoot(),Usd.TraverseInstanceProxies()):
  path=str(p.GetPath());low=path.lower()
  if p.IsA(UsdPhysics.Scene):scenes.append(path)
  if p.HasAPI(UsdPhysics.RigidBodyAPI):rigid.append(path)
  if not p.HasAPI(UsdPhysics.CollisionAPI):continue
  enabled=UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get()
  if enabled is False:continue
  role='rover' if any(x in low for x in ['rover','robot']) else 'pallet' if 'pallet' in low else 'load' if any(x in low for x in ['brick','bundle','load']) else 'floor' if any(x in low for x in ['floor','ground']) else 'other';roles[role].append(path)
 missing=[r for r in ['rover','floor','pallet','load'] if not roles[r]]
 return dict(scope=mode,stage_identifier=stage.GetRootLayer().identifier,root_layer_sha256=hashlib.sha256(stage.GetRootLayer().ExportToString().encode()).hexdigest(),used_layers=[x.identifier for x in stage.GetUsedLayers()],enabled_collision_prims=roles,collision_counts={k:len(v) for k,v in roles.items()},rigid_body_prims=rigid,physics_scenes=scenes,missing_required_roles=missing,state='HOLD' if missing or not scenes or mode!='ACTUAL_LOADED_ISAAC_STAGE' else 'STRUCTURE_ONLY_PASS_CONTACT_TESTS_PENDING',actual_loaded_Isaac_stage=mode=='ACTUAL_LOADED_ISAAC_STAGE',contacts_or_PhysX_steps='NOT_RUN',collision_free_motion_certified=False,physical_entry='HOLD')
