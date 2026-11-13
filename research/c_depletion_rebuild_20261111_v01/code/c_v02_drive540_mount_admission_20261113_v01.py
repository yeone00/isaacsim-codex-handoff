"""Narrow inactive-mount schema correction; no simulation, no transform edits."""
import hashlib,json
from pathlib import Path
from pxr import Usd,UsdGeom,UsdPhysics,Sdf
BASE='/World/ENG_FE2E/Rover/base_link'
MOUNT=BASE+'/MountedRolltainer/AssetRef'
BODY=MOUNT+'/rolltainer_body'
BODIES={BODY}|{MOUNT+'/'+c+'/'+n for c,ns in {'caster_fr':['rolltainer_link_01','rolltainer_wheel_01'],'caster_fl':['rolltainer_link_02','rolltainer_wheel_02'],'caster_rr':['rolltainer_link_03','rolltainer_wheel_03'],'caster_rl':['rolltainer_link_04','rolltainer_wheel_04']}.items() for n in ns}
REMOVED={'PhysicsRigidBodyAPI','PhysxRigidBodyAPI','PhysicsArticulationRootAPI','PhysxArticulationAPI'}
def digest(data):return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
def fingerprint(stage):
 """Transforms and all authored physical values/relationships, plus active set."""
 rows={}
 for p in stage.Traverse():
  name=str(p.GetPath());x=UsdGeom.Xformable(p)
  attrs={a.GetName():str(a.Get()) for a in p.GetAttributes() if a.IsAuthored() and a.GetName().startswith(('physics:','physx','xformOp'))}
  rel={r.GetName():list(map(str,r.GetTargets())) for r in p.GetRelationships() if r.GetName().startswith('physics:') and r.IsAuthored()}
  if attrs or rel or name.startswith(BASE):
   rows[name]={'type':p.GetTypeName(),'attrs':attrs,'rel':rel,'world':str(x.ComputeLocalToWorldTransform(Usd.TimeCode.Default())) if x else None,'apis':[a for a in p.GetAppliedSchemas() if not (name in BODIES and a in REMOVED)]}
 return rows

def verify_source(stage):
 found={str(p.GetPath()) for p in stage.Traverse() if str(p.GetPath()).startswith(MOUNT+'/') and p.HasAPI(UsdPhysics.RigidBodyAPI)}
 assert found==BODIES,('INACTIVE_BODY_SET_CHANGED',sorted(found))
 for name in sorted(BODIES):
  p=stage.GetPrimAtPath(name)
  assert UsdPhysics.RigidBodyAPI(p).GetRigidBodyEnabledAttr().Get() is False,('ACTIVE_MOUNT_BODY',name)
  assert not UsdGeom.Xformable(p).GetResetXformStack(),('ALTERED_MOUNT_XFORM_STACK',name)
  assert not p.GetAttribute('physics:rigidBodyEnabled').GetTimeSamples(),'ANIMATED_BODY_ENABLE'
 colliders=[];joints=[]
 for p in stage.Traverse():
  name=str(p.GetPath())
  if name.startswith(MOUNT+'/') and p.HasAPI(UsdPhysics.CollisionAPI):
   assert UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get() is False,('ACTIVE_MOUNT_COLLIDER',name)
   assert not p.GetAttribute('physics:collisionEnabled').GetTimeSamples(),'ANIMATED_COLLISION'
   colliders.append(name)
  if p.IsA(UsdPhysics.Joint):
   targets=[str(t) for r in ('physics:body0','physics:body1') for t in p.GetRelationship(r).GetTargets()]
   if name.startswith(MOUNT+'/') or any(t.startswith(MOUNT+'/') for t in targets):
    joints.append(name)
    assert UsdPhysics.Joint(p).GetJointEnabledAttr().Get() is False,('ACTIVE_MOUNT_JOINT',name)
 assert len(colliders)==10,('MOUNT_COLLIDER_MEMBERSHIP',colliders)
 assert stage.GetPrimAtPath(BODY).HasAPI(UsdPhysics.ArticulationRootAPI),'SOURCE_ROOT_MISSING'
 return {'disabled_bodies':sorted(BODIES),'disabled_colliders':sorted(colliders),'active_mount_joints':joints}

def correct(stage):
 proof=verify_source(stage);before=fingerprint(stage)
 changes={}
 for name in sorted(BODIES):
  p=stage.GetPrimAtPath(name)
  # Token deletion also works when standalone USD has not loaded PhysX plugins.
  tokens=['PhysicsRigidBodyAPI','PhysxRigidBodyAPI']
  if name==BODY:tokens+=['PhysicsArticulationRootAPI','PhysxArticulationAPI']
  p.SetMetadata('apiSchemas',Sdf.TokenListOp.Create(deletedItems=tokens))
  changes[name]=tokens
 after=fingerprint(stage)
 if before!=after:
  delta={k:{'before':before.get(k),'after':after.get(k)} for k in before.keys()|after.keys() if before.get(k)!=after.get(k)}
  raise AssertionError('TRANSFORM_OR_EFFECTIVE_PHYSICS_CHANGED:'+json.dumps(delta))
 assert not any(stage.GetPrimAtPath(n).HasAPI(UsdPhysics.RigidBodyAPI) for n in BODIES)
 assert not stage.GetPrimAtPath(BODY).HasAPI(UsdPhysics.ArticulationRootAPI)
 # No active articulated topology is changed: no joint points into mount.
 proof.update(pass_offline=True,removed_schema_tokens=changes,invariant_sha256=digest(before),all_authored_physics_and_world_transforms_equal=True,reset_added=False)
 return proof

def assess(stage,errors,live=None):
 """Parser messages remain evidence; topology and live invariants decide admission."""
 issues=[]
 for p in stage.Traverse():
  name=str(p.GetPath())
  if name in BODIES and p.HasAPI(UsdPhysics.RigidBodyAPI):issues.append('MOUNT_SCHEMA_NOT_CORRECTED:'+name)
  if p.HasAPI(UsdPhysics.ArticulationRootAPI):
   q=p.GetParent()
   while q and not q.IsPseudoRoot():
    if q.HasAPI(UsdPhysics.ArticulationRootAPI):issues.append('NESTED_ARTICULATION:'+name)
    q=q.GetParent()
  if name.startswith(MOUNT+'/') and p.HasAPI(UsdPhysics.CollisionAPI) and UsdPhysics.CollisionAPI(p).GetCollisionEnabledAttr().Get():issues.append('MOUNT_COLLIDER_ENABLED:'+name)
 # No warning allowlist: an error after the correction is an unresolved parser condition.
 if errors:issues.append('UNRESOLVED_PARSER_CONDITION')
 if live is not None:
  required=('body_joint_identity','camera_base_invariant','supplier_graph','wheel_support','registered_C_common_colliders','safety_consumer_C_colliders','unexpected_contacts_clear')
  issues += ['LIVE_INVARIANT_NOT_PASS:'+k for k in required if live.get(k) is not True]
 return {'pass':not issues,'issues':issues,'errors':errors,'live':live,'basis':'inactive source proof + corrected topology + explicit live physical invariants; historical success grants no exemption'}

def cleanup_classification(driver_started,receipt):
 if receipt.get('valid') is True:return {'status':'VERIFIED_ROS_ZERO','approach_success':False}
 return {'status':'MISSING' if driver_started else 'NOT_APPLICABLE_PRE_DRIVER','ros_zero_receipt':'MISSING','approach_success':False,'reason':'request and direct graph zero do not establish ROS publication or consumption'}
