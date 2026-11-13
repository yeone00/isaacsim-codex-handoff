"""CPU-only composition geometry check: not actual PhysX admission."""
import sys,pathlib,json,csv,time,collections,hashlib,itertools,math
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from evaluation.c_v02_drive540_scene_20261113_v03 import build,TARGET
from pxr import Usd,UsdGeom,UsdPhysics
D=pathlib.Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');A=D/'single_load_amendment_v01';O=A/'CPU_scene_QA_v01';O.mkdir(exist_ok=False);rows=list(csv.DictReader((A/'attempt_manifest.csv').open()));results=[];signatures={}
for C in ['C100','C80','C60','C40','C20']:
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  row=next(r for r in rows if r['base_id']=='C2D_B01' and r['C']==C and r['representation']==rep);stage,construction=build(O/(C+'_'+rep+'.usda'),row);cache=UsdGeom.BBoxCache(Usd.TimeCode.Default(),['default','render','proxy'],False,True);xf=UsdGeom.XformCache();active=[p for p in stage.Traverse()];loads=[p for p in active if p.GetName()=='ActualBrickLoad'];pallets=[p for p in active if p.GetName()=='T11_Pallet'];extra=[str(p.GetPath()) for p in active if p.GetName().startswith('Load_') and p.GetName()!='Load_01'];bricks=[p for p in active if str(p.GetPath()).startswith(TARGET+'/ActualBrickLoad') and p.GetName().startswith('Brick_')];boxes=[];sig=[]
  for path in construction['collider_paths']:
   p=stage.GetPrimAtPath(path);bb=cache.ComputeWorldBound(p).ComputeAlignedBox();lo=list(bb.GetMin());hi=list(bb.GetMax());sig.append([path.replace(TARGET,''),[round(v,7) for v in lo],[round(v,7) for v in hi]])
   if 'CommonNominalCollider' in path:boxes.append((path,lo,hi))
  overlap=[];unsupported=[]
  for i,(p,lo,hi) in enumerate(boxes):
   for q,lo2,hi2 in boxes[i+1:]:
    pen=[min(hi[k],hi2[k])-max(lo[k],lo2[k]) for k in range(3)]
    if min(pen)>1e-6:overlap.append(dict(a=p,b=q,penetration=pen))
   if abs(lo[2]-.144)>1e-6:
    supported=any(abs(lo[2]-h[2])<1e-6 and min(hi[0],h[0])-max(lo[0],l[0])>1e-6 and min(hi[1],h[1])-max(lo[1],l[1])>1e-6 for q,l,h in boxes if q!=p)
    if not supported:unsupported.append(p)
  signature=hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest();signatures.setdefault(C,[]).append(signature)
  checks=dict(single_load=len(loads)==1,single_pallet=len(pallets)==1,no_extra_Load_ids=not extra,correct_brick_count=len(bricks)==int(row['expected_bricks']),correct_common_collider_count=len(construction['collider_paths'])==int(row['expected_bricks'])+5,no_solid_box_overlap=not overlap,nominal_support_below_every_brick=not unsupported,no_external_panel=not construction['external_panel_prim_paths'])
  result=dict(C=C,rep=rep,state='PASS_CPU_COMPOSITION' if all(checks.values()) else 'FAIL_CPU_COMPOSITION',checks=checks,load_count=len(loads),pallet_count=len(pallets),brick_count=len(bricks),overlap_cases=overlap[:10],unsupported_bricks=unsupported[:10],collider_geometry_sha256=signature,actual_PhysX_pass=False,construction=construction);results.append(result);(O/(C+'_'+rep+'.json')).write_text(json.dumps(result,indent=2));print(C,rep,result['state'],len(overlap),len(unsupported),flush=True)
passed=all(r['state']=='PASS_CPU_COMPOSITION' for r in results) and all(len(set(s))==1 for s in signatures.values());(O/'result.json').write_text(json.dumps(dict(state='PASS_CPU_GEOMETRY_ONLY' if passed else 'HOLD',conditions=15,results=results,common_representation_colliders=all(len(set(s))==1 for s in signatures.values()),actual_PhysX_admission='HOLD',main_started=0),indent=2));assert passed
