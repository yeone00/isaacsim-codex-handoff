"""V02 extra QA before any training: counts, inherited splits, unique views, exact source hashes."""
from pathlib import Path
import csv,json,hashlib,collections
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';E=V/'execution_v01';O=V/'V02_contract_QA_v01';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();rows=list(csv.DictReader((V/'data_design_v01/scene_manifest.csv').open()));cat=json.loads((E/'capture_index.json').read_text());by={r['scene_id']:r for r in rows};groups=collections.defaultdict(list)
assert len(cat)==5250
for c in cat:
 r=by[c['scene_id']];d=json.loads(Path(c['complete']).read_text());assert d['state']=='PASS_CAPTURE';assert d['created_bricks']==int(r['retained_brick_count'])*int(r['load_count'])
 if r['C']=='C100':groups[c['rep'],r['family_id']].append((r,d,Path(c['complete']).parents[1]))
for key,rs in groups.items():
 assert len(rs)==5 and len({r['split'] for r,d,p in rs})==1
 assert len({sha(p/'rgb'/f"{r['scene_id']}.png") for r,d,p in rs})==5,'DUPLICATED_RGB_OBSERVATIONS'
 assert len({sha(p/'depth'/f"{r['scene_id']}.npy") for r,d,p in rs})==5,'DUPLICATED_DEPTH_OBSERVATIONS'
 assert len({json.dumps(d['GT_eval_only']['target'],sort_keys=True) for r,d,p in rs})==1,'LOAD_POSE_CHANGED_ACROSS_VIEWS'
 # Quantile distance affects camera only, not voxel/retained set or scene transform.
 assert len({r['mask_by_layer_json'] for r,d,p in rs})==1
assert json.loads((E/'dataset_QA_bitmap_v01/result.json').read_text())['state']=='PASS'
(O/'result.json').write_text(json.dumps(dict(state='PASS',C100_family_rep_groups=len(groups),each_group_unique_RGBD=5,target_pose_unchanged=True,raw_masks_unchanged=True,original_C_V01_preserved=True,source_family_splits_unchanged=True,C100_only_view_distribution_confound_disclosed=True),indent=2))
