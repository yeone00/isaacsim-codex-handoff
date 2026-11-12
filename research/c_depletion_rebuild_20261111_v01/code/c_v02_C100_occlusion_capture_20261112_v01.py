"""v03: adds independently measured O25/O50 RGB-D + actual panel and visible canonical GT; no motion."""
"""v02: new C-only instance-centre compensation from exact mesh-vertex audit; v01 failure preserved."""
"""C partial-load RGB-D/GT capture adapter. Fresh Kit, no physics playback or robot motion.
Audited original retained-bundle functions, B1 frozen camera/photometry. No legacy top-level imports.
"""
import argparse,csv,json,sys,os,time,traceback,math,resource
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation.c_depletion_geometry_20261111_v01 import sha,usd_functions,RGB,GT
ap=argparse.ArgumentParser();ap.add_argument('--anchor-audit',type=Path,required=True);ap.add_argument('--design',type=Path,required=True);ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--rep',choices=['HR_Scan','LR_Scan','GeoCAD'],required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
C=json.loads((a.design/'capture_config.json').read_text());RC=json.loads(Path(C['red_config']).read_text());QC=json.loads(Path(C['quality_config']).read_text())
for p,h in C['sources_sha256'].items():assert sha(p)==h,p
assert sha(C['background'])==C['background_sha256']
for q in C['assets'].values():assert sha(q['path'])==q['sha256']
anchor=json.loads(a.anchor_audit.read_text());assert anchor['state']=='PASS_CENTERED_ENCLOSURE_GEOMETRY';anchor_rep=next(r for r in anchor['checks'] if r['rep']==a.rep);assert sha(anchor_rep['path'])==anchor_rep['sha256'];rows=list(csv.DictReader(a.manifest.open()));assert rows
O=a.output;O.mkdir(exist_ok=False);app=None;results=[];started=time.time()
def dump(n,x):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=1,default=lambda v:v.tolist() if hasattr(v,'tolist') else str(v)))
def event(st,**kw):
 with (O/'events.jsonl').open('a') as f:f.write(json.dumps(dict(time=time.time(),state=st,pid=os.getpid(),**kw))+'\n')
event('STARTED',rep=a.rep,scenes=len(rows),manifest_sha256=sha(a.manifest),code_sha256=sha(__file__))
try:
 from evaluation.b1_common_hpo_policy_20261111_v01 import gpu_gate
 g=gpu_gate((os.getpid(),os.getppid()));assert g['clear'],g
 from isaacsim import SimulationApp
 app=SimulationApp({'headless':True,'width':640,'height':480,'renderer':'RayTracedLighting','multi_gpu':False,'extra_args':['--/app/window/enabled=false','--/app/livestream/enabled=false','--/UJITSO/geometry=true','--/omni/replicator/captureOnPlay=false','--/exts/omni.kit.scripting.allowed=false','--/metricsAssembler/operationMode=0']})
 import numpy as np,omni.usd,omni.timeline,omni.kit.app,omni.replicator.core as rep,carb.settings
 from PIL import Image
 from scipy import ndimage as nd
 from pxr import Usd,UsdGeom,UsdLux,UsdShade,Sdf,Gf,Vt,Semantics
 tl=omni.timeline.get_timeline_interface();tl.stop();ctx=omni.usd.get_context();ctx.new_stage();stage=ctx.get_stage();stage.GetRootLayer().subLayerPaths=[C['background']];stage.SetEditTarget(stage.GetRootLayer());UsdGeom.SetStageUpAxis(stage,'Z');UsdGeom.SetStageMetersPerUnit(stage,1.);stage.GetRootLayer().SetPermissionToSave(False)
 root='/World/CDepletion';xf=UsdGeom.Xformable(UsdGeom.Xform.Define(stage,root));tr=xf.AddTranslateOp();rz=xf.AddRotateZOp();scene=root+'/Scene';cc=C['camera']
 cam=UsdGeom.Camera.Define(stage,root+'/Camera');cam.CreateFocalLengthAttr(cc['focal_length_mm']);cam.CreateHorizontalApertureAttr(cc['h_aperture_mm']);cam.CreateVerticalApertureAttr(cc['v_aperture_mm']);cam.CreateClippingRangeAttr((.05,1000.));camop=UsdGeom.Xformable(cam).MakeMatrixXform();dome=UsdLux.DomeLight.Define(stage,root+'/Dome');dome.CreateExposureAttr(0);dome.CreateColorAttr((1,1,1))
 volumes=[p for p in stage.Traverse() if p.GetAttribute('omni:nurec:isNuRecVolume').IsValid() and p.GetAttribute('omni:nurec:isNuRecVolume').Get()];assert len(volumes)==1;nu=UsdGeom.Imageable(volumes[0])
 sett=carb.settings.get_settings()
 for k,v in Sdf.Layer.FindOrOpen(C['background']).customLayerData.get('renderSettings',{}).items():sett.set('/'+k.replace(':','/'),v)
 ph=C['photometric']
 for k,v in {'/rtx/rendermode':'RaytracedLighting','/rtx/post/aa/op':2,'/rtx/post/aa/autoExposureMode':2,'/rtx/post/aa/exposure':1.,'/rtx/post/histogram/enabled':False,'/rtx/scenedb/skipMostLights':False,'/app/viewport/grid/enabled':False,'/rtx/post/tonemap/op':ph['op'],'/rtx/post/tonemap/filmIso':ph['filmIso'],'/rtx/post/tonemap/cameraShutter':ph['cameraShutter'],'/rtx/post/tonemap/fNumber':ph['fNumber']}.items():sett.set(k,v)
 ns=usd_functions(RGB,['create_box','create_pallet','iterate_pattern','create_actual_brick','create_actual_bundle','create_actual_load','cluster_offsets'],dict(UsdGeom=UsdGeom,UsdLux=UsdLux,Gf=Gf,stage=stage,json=json,Path=Path,math=math))
 original_brick=ns['create_actual_brick']
 def centered_brick(path,local_y,asset_path):
  original_brick(path,local_y,asset_path)
  ref=stage.GetPrimAtPath(path+'/SideStanding/AssetRef');refxf=UsdGeom.Xformable(ref)
  assert not refxf.GetOrderedXformOps(),'UNEXPECTED_REFERENCED_ROOT_XFORM'
  refxf.AddTranslateOp().Set(Gf.Vec3d(*anchor_rep['new_instance_translation_local']))
 ns['create_actual_brick']=centered_brick
 camera_ns=usd_functions(C['camera_source'],['set_camera'],dict(Gf=Gf,camera_matrix_op=camop))
 original_set_camera=camera_ns['set_camera']
 def set_observation_camera(row):
  if row.get('observation_id','OBS00')=='OBS00':return original_set_camera(row)
  zx,zy,base,dist=map(float,[row['zone_anchor_x_m'],row['zone_anchor_y_m'],row['distance_m'],row['observation_distance_m']])
  eye=Gf.Vec3d(zx+base-dist,zy,.600);target=Gf.Vec3d(zx+base,zy,.144+4*.090/2)
  view=Gf.Matrix4d();view.SetLookAt(eye,target,Gf.Vec3d(0,0,1));camop.Set(view.GetInverse())
 camera_ns['set_camera']=set_observation_camera

 cn=usd_functions(GT,['create_box','apply_class_semantics','iterate_pattern','parse_retention_mask','create_canonical_bundle','create_canonical_load'],dict(UsdGeom=UsdGeom,Gf=Gf,Semantics=Semantics,stage=stage,json=json))
 assert ns['PATTERN_A']==cn['PATTERN_A'] and ns['PATTERN_B']==cn['PATTERN_B']
 product=rep.create.render_product(str(cam.GetPath()),(640,480));anns={n:rep.AnnotatorRegistry.get_annotator(n) for n in ['rgb','instance_id_segmentation','distance_to_image_plane','camera_params']}
 for an in anns.values():an.attach(product.path)
 def updates(n):
  for _ in range(n):assert not tl.is_playing();app.update()
 def reset():
  updates(16);ctx.reset_renderer_accumulation();updates(4)
  for _ in range(6):rep.orchestrator.step(rt_subframes=8,delta_time=0,pause_timeline=True);assert not tl.is_playing()
  assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024<=8*1024**3,'CPU_RSS_8_GIB_LIMIT'
 def pixels(name):
  d=anns[name].get_data();return d['data'] if isinstance(d,dict) and 'data' in d else d
 def image(path,array):path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(array).save(path)
 def rgb():x=np.asarray(pixels('rgb'))[:,:,:3].astype('uint8');assert x.shape==(480,640,3);return x.copy()
 def masks():
  d=anns['instance_id_segmentation'].get_data();ar=np.squeeze(np.asarray(d['data']));mapping=d['info'].get('idToLabels',{})
  def one(needle):
   ids=[int(k) for k,v in mapping.items() if needle in str(v)];return np.isin(ar,ids),len(ids)
  return one
 em=omni.kit.app.get_app().get_extension_manager();assert not [e['id'] for e in em.get_extensions() if 'ros' in e['id'].lower() and em.is_extension_enabled(e['id'])];updates(70)
 for row in rows:
  sid=row['scene_id'];rec=dict(scene_id=sid,family_id=row['family_id'],split=row['split'],C=row['C'],rep=a.rep,trajectory=row['trajectory_id'],depletion_seed=row['depletion_seed'],target_instance='Load_01',observation_id=row.get('observation_id','OBS00'),observation_distance_m=row.get('observation_distance_m',row['distance_m']),source_C_V01_scene_id=row.get('source_C_V01_scene_id'),started=time.time());event('SCENE_STARTED',scene_id=sid)
  try:
   tr.Set(Gf.Vec3d(float(row['roi_origin_x_m']),float(row['roi_origin_y_m']),float(row['roi_origin_z_m'])));rz.Set(float(row['roi_yaw_deg']));camera_ns['set_camera'](row);dome.CreateIntensityAttr(float(row['dome_intensity']));nu.MakeVisible()
   if stage.GetPrimAtPath(scene):stage.RemovePrim(scene)
   updates(8);reset();empty=rgb();image(O/'empty'/f'{sid}.png',empty)
   UsdGeom.Xform.Define(stage,scene);offsets=ns['cluster_offsets'](int(row['load_count']),float(row['pallet_gap_m']));created=0;paths=[]
   for lid,(dx,dy) in enumerate(offsets,1):
    lr=scene+f'/Load_{lid:02d}';load=UsdGeom.Xform.Define(stage,lr);lx=UsdGeom.Xformable(load.GetPrim());lx.AddTranslateOp().Set(Gf.Vec3d(float(row['zone_anchor_x_m'])+float(row['distance_m'])+dx,float(row['zone_anchor_y_m'])+dy,0.));lx.AddRotateZOp().Set(float(row['physical_yaw_deg']));ns['create_pallet'](lr+'/T11_Pallet');created+=ns['create_actual_load'](lr,row['layer_phase'],Path(C['assets']['red__'+a.rep]['path']),row['mask_by_layer_json']);paths.append(lr)
   expected=int(row['retained_brick_count'])*int(row['load_count']);assert created==expected
   for _ in range(3000):
    _,fl,tf=ctx.get_stage_loading_status()
    if not(fl or tf):break
    updates(1)
   else:raise RuntimeError('STAGE_LOADING_TIMEOUT')
   reset();tries=0
   while not masks()('/Load_01/ActualBrickLoad/')[0].any() and tries<5:tries+=1;updates(60);reset()
   # Exact source vertices were CPU-audited for all3 reps. USD BBoxCache bounds can inflate
   # rotated bounds and were the unsuitable v01 test; do not relax the numerical tolerance.
   rawdims=np.array(anchor_rep['raw_dimensions']);dims=rawdims[[0,2,1]]
   envelope=dict(source_mesh_sha256=anchor_rep['sha256'],raw_mesh_center=anchor_rep['raw_mesh_center'],instance_translation=anchor_rep['new_instance_translation_local'],centered_dimensions=dims.tolist(),expected_dimensions=[.190,.057,.090],tolerance_m=1e-6,pass_=bool(np.max(abs(dims-[.190,.057,.090]))<=1e-6),meaning='exact mesh vertex normalization and centered instance placement; static enclosure support, no dynamic stability claim')
   assert envelope['pass_'],'EXACT_ASSET_DIMENSIONS_FAILED'
   I=rgb();dep=np.squeeze(np.asarray(pixels('distance_to_image_plane'))).astype(np.float32).copy();assert dep.shape==(480,640)
   actual=[];get=masks();pallet=get('/T11_Pallet')[0]
   for lid in range(1,len(paths)+1):
    m,n=get(f'/Load_{lid:02d}/ActualBrickLoad/');assert n==int(row['retained_brick_count']),('ACTUAL_INSTANCE_COUNT_MISMATCH',n,row['retained_brick_count']);actual.append(m.copy());image(O/'masks_actual'/f'{sid}_Load_{lid:02d}.png',m.astype('uint8')*255)
   assert actual[0].any() and pallet.any(),'ACTUAL_INSTANCE_MASK_EMPTY'
   image(O/'rgb'/f'{sid}.png',I);(O/'depth').mkdir(exist_ok=True);np.save(O/'depth'/f'{sid}.npy',dep)
   par={k:(np.asarray(v).tolist() if hasattr(v,'shape') else v) for k,v in anns['camera_params'].get_data().items()};pr=np.array(par['cameraProjection'],float).reshape(4,4);view=np.array(par['cameraViewTransform'],float).reshape(4,4);T=np.linalg.inv(view).T;T[:3,:3]=T[:3,:3]@np.diag([1,-1,-1]);M=np.array(UsdGeom.XformCache().GetLocalToWorldTransform(cam.GetPrim())).T;M[:3,:3]=M[:3,:3]@np.diag([1,-1,-1]);fx=pr[0,0]*320;fy=pr[1,1]*240
   assert np.max(abs(T-M))<1e-4 and abs(fx-fy)<.01*fx,'CAMERA_REGISTRATION_FAILED'
   dump('camera/'+sid+'.json',dict(calibration=dict(width=640,height=480,fx=fx,fy=fy,cx=320.,cy=240.,T_world_optical=T.tolist(),depth_semantic='distance_to_image_plane',depth_unit_m=1.),raw_parameters=par))
   gtpose=[]
   for lr in paths:
    mat=UsdGeom.XformCache().GetLocalToWorldTransform(stage.GetPrimAtPath(lr));tt=mat.ExtractTranslation();axis=mat.TransformDir(Gf.Vec3d(1,0,0));gtpose.append(dict(center_x_m=tt[0],center_y_m=tt[1],floor_z_m=tt[2],pallet_top_z_m=tt[2]+.144,yaw_deg=math.degrees(math.atan2(axis[1],axis[0]))))
   canon_counts=[]
   for lr in paths:stage.GetPrimAtPath(lr+'/ActualBrickLoad').SetActive(False);canon_counts.append(cn['create_canonical_load'](lr,row))
   reset();get=masks();canon=[]
   for lid in range(1,len(paths)+1):
    m,n=get(f'/Load_{lid:02d}/CanonicalBrickGT/');assert n==int(row['retained_bundle_count']),'CANONICAL_INSTANCE_COUNT_MISMATCH';canon.append(m.copy());image(O/'masks_canonical'/f'{sid}_Load_{lid:02d}.png',m.astype('uint8')*255)
   assert canon[0].sum()>=100,'PRIMARY_CANONICAL_UNDER_100PX'
   valid=np.isfinite(dep)&(dep>0);assert (valid&actual[0]).sum()>=100,'TARGET_DEPTH_UNDER_100PX'
   union=np.any(actual,0)|pallet;diff=np.abs(I.astype(np.int16)-empty.astype(np.int16)).max(2);background=~nd.binary_dilation(union,iterations=15);assert background.any();tau=max(int(np.percentile(diff[background],99.9)),2);qa=[]
   for lid,m in enumerate(actual,1):
    me=nd.binary_erosion(m,iterations=2);n=int(me.sum());v=float((diff[me]>tau).mean()) if n else None;cat='LOW_SUPPORT' if n<100 else 'FLAG_NUREC_OCCLUSION' if v<.90 else 'WATCH' if v<.95 else 'OK';qa.append(dict(load_id=lid,px_e2=n,tau=tau,vis_hard_e2=v,category=cat,H1_keep=True))
   maskrows=json.loads(row['mask_by_layer_json']);occupied={x['layer']:x['bundle_ids'] for x in maskrows};top=max(l for l,ids in occupied.items() if ids);assert all(len(occupied[l])==15 for l in range(1,top)),'NOMINAL_SUPPORT_HOLE'
   rec.update(state='PASS_CAPTURE',expected_bricks=expected,created_bricks=created,asset_envelope=envelope,actual_mask_px=[int(m.sum()) for m in actual],canonical_mask_px=[int(m.sum()) for m in canon],canonical_bundle_counts=canon_counts,depth_valid_target_px=int((valid&actual[0]).sum()),calibration_check=True,load_retries=tries,nominal_slot_support=True,dynamic_support='NOT_ASSESSED_STATIC_DATA_CAPTURE',visibility_QA=qa,GT_eval_only=dict(target=gtpose[0],all_loads=gtpose,retention=json.loads(row['mask_by_layer_json']),occupied_layers=int(row['occupied_layers_eval_only'])),mask_count_check=True)
   files=[O/'rgb'/f'{sid}.png',O/'depth'/f'{sid}.npy',O/'camera'/f'{sid}.json',O/'empty'/f'{sid}.png']+[O/'masks_canonical'/f'{sid}_Load_{i:02d}.png' for i in range(1,len(paths)+1)]+[O/'masks_actual'/f'{sid}_Load_{i:02d}.png' for i in range(1,len(paths)+1)]
   # Actual visibility pass. GT is used ONLY for fixture construction and evaluation.
   for lr in paths:stage.GetPrimAtPath(lr+'/CanonicalBrickGT').SetActive(False);stage.GetPrimAtPath(lr+'/ActualBrickLoad').SetActive(True)
   reset();occroot='/World/CDepletionOccluder';occ={};C0=canon[0];yy,xx=np.where(C0);side='left' if int(row['scene_seed'])%2==0 else 'right'
   cameraM=UsdGeom.XformCache().GetLocalToWorldTransform(cam.GetPrim());invM=cameraM.GetInverse()
   b=UsdGeom.BBoxCache(Usd.TimeCode.Default(),['default','render']).ComputeWorldBound(stage.GetPrimAtPath(paths[0])).ComputeAlignedRange()
   near=min(-invM.Transform(Gf.Vec3d(x,y,z))[2] for x in [b.GetMin()[0],b.GetMax()[0]] for y in [b.GetMin()[1],b.GetMax()[1]] for z in [b.GetMin()[2],b.GetMax()[2]])
   zp=.85*near;assert .05<zp<near
   material=UsdShade.Material.Define(stage,root+'/PanelMaterial');shader=UsdShade.Shader.Define(stage,root+'/PanelMaterial/Shader');shader.CreateIdAttr('UsdPreviewSurface');shader.CreateInput('diffuseColor',Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(.45,.45,.45));shader.CreateInput('roughness',Sdf.ValueTypeNames.Float).Set(.9);shader.CreateInput('metallic',Sdf.ValueTypeNames.Float).Set(0.);material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(),'surface')
   columns=C0.sum(0).astype(float)
   if side=='right':columns=columns[::-1]
   cdf=np.cumsum(columns)/columns.sum()
   for oname,target in [('O25',.25),('O50',.5)]:
    adjusted=target;history=[]
    for iteration in range(3):
     j=int(np.searchsorted(cdf,min(max(adjusted,1e-4),1-1e-4)));prev=cdf[j-1] if j else 0.;boundary=j+(adjusted-prev)/max(cdf[j]-prev,1e-9)
     if side=='right':boundary=640-boundary
     xlo,xhi=(float(xx.min()-6),boundary) if side=='left' else (boundary,float(xx.max()+1+6));ylo,yhi=float(yy.min()-6),float(yy.max()+1+6)
     if stage.GetPrimAtPath(occroot):stage.RemovePrim(occroot)
     mesh=UsdGeom.Mesh.Define(stage,occroot+'/Panel');points=[cameraM.Transform(Gf.Vec3d((u-320)/fx*zp,-(v-240)/fy*zp,-zp)) for u,v in [(xlo,ylo),(xhi,ylo),(xhi,yhi),(xlo,yhi)]]
     mesh.CreatePointsAttr(Vt.Vec3fArray([Gf.Vec3f(*q) for q in points]));mesh.CreateExtentAttr(UsdGeom.PointBased.ComputeExtent(Vt.Vec3fArray([Gf.Vec3f(*q) for q in points])));mesh.CreateFaceVertexCountsAttr([4]);mesh.CreateFaceVertexIndicesAttr([0,1,2,3]);mesh.CreateDoubleSidedAttr(True);UsdShade.MaterialBindingAPI.Apply(mesh.GetPrim()).Bind(material);reset()
     panel=masks()('/CDepletionOccluder/Panel')[0];coverage=float((C0&panel).sum()/C0.sum());history.append(dict(iteration=iteration,adjusted=adjusted,measured=coverage,panel_pixels=int(panel.sum())))
     if abs(coverage-target)<=.005 or iteration==2:break
     adjusted=min(max(adjusted+target-coverage,.01),.99)
    assert panel.any() and abs(coverage-target)<=.02,('OCCLUSION_NOT_ACHIEVED',oname,coverage)
    out=O/'occlusion'/oname;image(out/'rgb'/f'{sid}.png',rgb());(out/'depth').mkdir(parents=True,exist_ok=True);dp=out/'depth'/f'{sid}.npy';np.save(dp,np.squeeze(np.asarray(pixels('distance_to_image_plane'))).astype(np.float32));pp=out/'masks'/f'{sid}_panel.png';image(pp,panel.astype('uint8')*255);files.extend([out/'rgb'/f'{sid}.png',dp,pp]);cm=[]
    for lid,baseGT in enumerate(canon,1):
     mp=out/'masks'/f'{sid}_Load_{lid:02d}.png';image(mp,(baseGT&~panel).astype('uint8')*255);files.append(mp);cm.append(str(mp))
    occ[oname]=dict(nominal=target,measured=coverage,achieved=True,refinement=history,panel=str(pp),canonical_visible_masks=cm,rgb=str(out/'rgb'/f'{sid}.png'),depth=str(dp),camera=str(O/'camera'/f'{sid}.json'),panel_world_corners=[list(q) for q in points],panel_below_design_floor=bool(min(q[2] for q in points)<float(row['roi_origin_z_m'])-.01),GT_role='fixture_and_evaluation_only_no_pose_input',actual_same_frame_panel=True)
   if stage.GetPrimAtPath(occroot):stage.RemovePrim(occroot)
   rec['occlusion']=occ
   rec['files_sha256']={str(f):sha(f) for f in files}
  except Exception:rec.update(state='FAILED',traceback=traceback.format_exc());dump('complete/'+sid+'.json',rec);results.append(rec);event('SCENE_FAILED',scene_id=sid);raise
  rec['ended']=time.time();dump('complete/'+sid+'.json',rec);results.append(rec);event('SCENE_COMPLETED',scene_id=sid)
 dump('result.json',dict(state='PASS_CAPTURE',rep=a.rep,declared=len(rows),completed=len(results),failed=0,manifest_sha256=sha(a.manifest),code_sha256=sha(__file__),elapsed_seconds=time.time()-started,physics_play=0,robot_motion=0))
 for an in anns.values():an.detach(product.path)
 product.destroy();ctx.close_stage()
except BaseException:
 dump('failure.json',dict(state='FAILED',traceback=traceback.format_exc(),declared=len(rows),completed=sum(r.get('state')=='PASS_CAPTURE' for r in results),attempted=len(results)));event('FAILED');raise
finally:
 if app:app.close()
