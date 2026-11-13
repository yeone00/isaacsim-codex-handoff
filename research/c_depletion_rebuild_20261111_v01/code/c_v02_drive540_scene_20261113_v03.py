"""C-only builder: original depletion geometry + common nominal static colliders.
Scene GT/retention is simulation construction input; never perception/pose input.
No simulator startup, no motion and no legacy top-level imports.
"""
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];S=Path('/home/user/hh/isaac_cosmos/sdg_final');B=S/'C_DEPLETION_REBUILD_20261111_v01';V=B/'C_V02_20261112_v01';D=V/'DRIVE540_20261113_v01';BASE=S/'PILOT_SITE_HR_ADMISSION_20261102_v30_03/prepared_site_drive.usda';TARGET='/World/CV02DriveScene/Load_01'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build(output,row):
 from pxr import Usd,UsdGeom,UsdPhysics,UsdLux,Gf,Sdf
 from evaluation.c_depletion_geometry_20261111_v01 import usd_functions,RGB
 cfassert int(row.get('load_count',1))==1 and int(row.get('pallet_count',1))==1
 g=json.loads((B/'data_design_v01/capture_config.json').read_text());anchor=json.loads((B/'asset_anchor_audit_v01/asset_anchor_audit.json').read_text());ar=next(x for x in anchor['checks'] if x['rep']==row['representation']);assert sha(ar['path'])==ar['sha256']
 for path,h in cfg['sources_sha256'].items():assert sha(path)==h
 assert int(row.get('load_count',1))==1 and int(row.get('pallet_count',1))==1
 g=json.loads((D/'eval_gt_only/scene_construction.json').read_text())[row['base_id']+'_'+row['C']]
 stage=Usd.Stage.CreateNew(str(output));stage.GetRootLayer().subLayerPaths=[str(BASE)];UsdGeom.SetStageMetersPerUnit(stage,1.);UsdGeom.SetStageUpAxis(stage,'Z')
 # Disable ONLY the superseded target and its historical full-load union; preserve floor/site obstacles/rover.
 for path in ['/World/ENG_FE2E/Fixture','/World/PilotStaticUnion_v24']:
  p=stage.OverridePrim(path);assert p;p.SetActive(False)
 for p in list(stage.Traverse()):
  if any(t in str(p.GetPath()).lower() for t in ['stage3occluder','occlusionpanel','occluderworld']):p.SetActive(False)
 rover=UsdGeom.Xformable(stage.GetPrimAtPath('/World/ENG_FE2E/Rover'));m=Gf.Matrix4d();m.SetRotate(Gf.Rotation(Gf.Vec3d(0,0,1),float(row['start_yaw_deg'])));m.SetTranslateOnly(Gf.Vec3d(float(row['start_x_m']),float(row['start_y_m']),-.00835194));rover.ClearXformOpOrder();rover.MakeMatrixXform().Set(m)
 target=UsdGeom.Xform.Define(stage,TARGET);UsdGeom.Xformable(target).AddTranslateOp().Set(Gf.Vec3d(-25.888,30.509,0.))
 ns=usd_functions(RGB,['create_box','create_pallet','iterate_pattern','create_actual_brick','create_actual_bundle','create_actual_load','cluster_offsets'],dict(UsdGeom=UsdGeom,UsdLux=UsdLux,Gf=Gf,stage=stage,json=json,Path=Path,math=math))
 old=ns['create_actual_brick']
 def brick(path,y,asset):
  old(path,y,asset);ref=UsdGeom.Xformable(stage.GetPrimAtPath(path+'/SideStanding/AssetRef'));assert not ref.GetOrderedXformOps();ref.AddTranslateOp().Set(Gf.Vec3d(*ar['new_instance_translation_local']))
 ns['create_actual_brick']=brick;ns['create_pallet'](TARGET+'/T11_Pallet');count=ns['create_actual_load'](TARGET,g['layer_phase'],Path(ar['path']),g['mask_by_layer_json']);assert count==int(row['expected_bricks'])
 colliders=[]
 for p in list(stage.Traverse()):
  path=str(p.GetPath())
  if path.startswith(TARGET+'/T11_Pallet/') and p.IsA(UsdGeom.Cube):UsdPhysics.CollisionAPI.Apply(p).CreateCollisionEnabledAttr().Set(True);colliders.append(path)
  if path.startswith(TARGET+'/ActualBrickLoad/') and p.GetName().startswith('Brick_'):
   cube=UsdGeom.Cube.Define(stage,path+'/CommonNominalCollider');cube.CreateSizeAttr(1.);UsdGeom.Xformable(cube).AddScaleOp().Set(Gf.Vec3f(.190,.057,.090));cube.CreateVisibilityAttr().Set('invisible');UsdPhysics.CollisionAPI.Apply(cube.GetPrim()).CreateCollisionEnabledAttr().Set(True);colliders.append(str(cube.GetPath()))
 assert len(colliders)==count+5
 # Strip every native representation-specific collision/rigid-body API under actual visual references.
 for p in Usd.PrimRange(stage.GetPrimAtPath(TARGET),Usd.TraverseInstanceProxies()):
  if p.IsInstanceProxy():continue
  if str(p.GetPath()) not in colliders and p.HasAPI(UsdPhysics.CollisionAPI):UsdPhysics.CollisionAPI(p).CreateCollisionEnabledAttr().Set(False)
  if p.HasAPI(UsdPhysics.RigidBodyAPI):UsdPhysics.RigidBodyAPI(p).CreateRigidBodyEnabledAttr().Set(False)
 # Existing lighting intensity, chosen from source Test conditions; shared across representations.
 domes=[p for p in stage.Traverse() if p.IsA(UsdLux.DomeLight)]
 for p in domes:UsdLux.DomeLight(p).CreateIntensityAttr(float(g['dome_intensity']))
 # A legacy disabled render-product node has an invalid out-of-reference camera relationship.
 # C-only explicit binding to the same actual mounted camera; actuation attributes unchanged.
 sensor_node=stage.GetPrimAtPath('/World/ENG_FE2E/Rover/ActionGraph/isaac_create_render_product')
 assert sensor_node
 sensor_node.GetRelationship('inputs:cameraPrim').SetTargets(['/World/ENG_FE2E/Rover/base_link/front_link/front_camera/front_Camera'])
 stage.GetRootLayer().Save()
 construction=dict(load_count=1,pallet_count=1,target_instance='Load_01',actual_bricks=count,expected_bricks=int(row['expected_bricks']),task_layer_count=int(row['task_layer_count']),target_path=TARGET,collider_paths=colliders,collider_count=len(colliders),pallet_collider_count=5,static_collision_policy='common nominal per-brick boxes .190x.057x.090 and actual pallet components; identical geometry across representations; fixed cargo as historical static union, no dynamic cargo stability claim',source_scene=g['scene_id'],source_mask_sha256=hashlib.sha256(g['mask_by_layer_json'].encode()).hexdigest(),source_asset=dict(path=ar['path'],sha256=ar['sha256']),source_base_sha256=sha(BASE),stage_path=str(output),stage_sha256=sha(output),source_environment_note='robot drive site is prepared v30 common site; not original static dataset camera/environment reproduction',external_panel_prim_paths=[str(p.GetPath()) for p in stage.Traverse() if any(t in str(p.GetPath()).lower() for t in ['occluder','occlusionpanel'])])
 assert not construction['external_panel_prim_paths']
 return stage,construction
