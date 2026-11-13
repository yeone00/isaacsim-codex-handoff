"""C-only actual PhysX registration and safety-consumer proof, replacing historical full-load28union inventory only."""
import json
from pathlib import Path
def physx_gate(stage,query,clearance,out):
 import carb
 from pxr import Usd,UsdGeom,UsdPhysics
 proof=json.loads((out/'C_scene_construction.json').read_text());expected=set(proof['collider_paths']);seen={x['path'] for x in clearance['colliders']};assert expected<=seen,'C_SAFETY_CONSUMER_MISSED_COLLIDERS';cache=UsdGeom.XformCache();checks=[]
 for path in sorted(expected):
  center=cache.GetLocalToWorldTransform(stage.GetPrimAtPath(path)).ExtractTranslation();hits=[]
  def hit(h):hits.append(str(h.collision));return True
  query.overlap_box(carb.Float3(.0001,.0001,.0001),carb.Float3(*center),carb.Float4(0,0,0,1),hit,False);checks.append(dict(path=path,actual_registered=path in hits,hits=hits))
 prefix=proof['target_path'];enabled={str(p.GetPath()) for p in Usd.PrimRange(stage.GetPrimAtPath(prefix),Usd.TraverseInstanceProxies()) if p.HasAPI(UsdPhysics.CollisionAPI) and UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get() is not False};assert enabled==expected,'C_UNEXPECTED_NATIVE_COLLIDER'
 passed=all(x['actual_registered'] for x in checks);(out/'pilot_physx_C.json').write_text(json.dumps(dict(pass_=passed,checks=checks,safety_consumer_cells=sorted(seen&expected),expected_count=len(expected),scope='actual PhysX interior overlap probes + exact common collider membership; no actuation guard relaxation'),indent=2).replace('"pass_"','"pass"'));assert passed,'C_PHYSX_REGISTRATION_FAILED'
