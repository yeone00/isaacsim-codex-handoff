"""Audited pure functions from original depletion builder. No legacy module imports/top-level execution."""
import ast,collections,hashlib,json,random
from pathlib import Path
BUILDER=Path('/home/user/hh/isaac_cosmos/scripts/build_nonideal_depletion_manifest_v01.py')
CANON=Path('/home/user/nonideal_matched_canonical_gt_production_v03.py')
RGB=Path('/home/user/nonideal_depletion_b2b_production_rgb_v01.py')
GT=Path('/home/user/nonideal_depletion_canonical_gt_production_v01.py')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def literal(path,name):
 for n in ast.parse(Path(path).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name:return ast.literal_eval(n.value)
 raise KeyError(name)
def pure_original():
 ns=dict(hashlib=hashlib,json=json,random=random,deque=collections.deque,MASTER_DEPLETION_SEED=260929,N_LAYERS=4,BUNDLES_PER_LAYER=15,BRICKS_PER_BUNDLE=5,GRID_NX=10,GRID_NY=9,ALL_GRID_CELLS={(x,y) for x in range(10) for y in range(9)},CHECKPOINTS=dict(C100=60,C80=48,C60=36,C40=24,C20=12),PARTIAL_CHECKPOINTS={48:'C80',36:'C60',24:'C40',12:'C20'})
 ns['PATTERNS']={p:literal(CANON,'PATTERN_'+p) for p in ['A','B']}
 names={'stable_int_seed','bundle_cells','make_bundle_records','full_state','clone_state','state_count','highest_nonempty_layer','layer_cells','exterior_empty_cells','bundle_is_externally_exposed','removal_candidates','generate_trajectory','mask_by_layer_json','retained_bundle_ids_json','layer_retained_counts_json'}
 nodes=[n for n in ast.parse(BUILDER.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(nodes)==len(names)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(BUILDER),'exec'),ns)
 ns['BUNDLES']={p:ns['make_bundle_records'](p) for p in ['A','B']};return ns
def usd_functions(path,names,namespace):
 """Whitelisted definitions/constants only, never legacy imports/main/side effects."""
 allowed={'WIDTH','HEIGHT','SIDE_Y','SIDE_H','CELL','LOAD_X','LOAD_Y','PALLET_X','PALLET_Y','PALLET_H','BOTTOM_H','TOP_H','RUNNER_H','RUNNER_W','PATTERN_A','PATTERN_B','BUNDLE_X','BUNDLE_Y','BUNDLE_Z','CAMERA_HEIGHT','FOCAL_LENGTH','H_APERTURE','V_APERTURE'}
 nodes=[]
 for n in ast.parse(Path(path).read_text()).body:
  if isinstance(n,ast.FunctionDef) and n.name in names:nodes.append(n)
  elif isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in allowed:nodes.append(n)
 assert {n.name for n in nodes if isinstance(n,ast.FunctionDef)}==set(names)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace);return namespace
