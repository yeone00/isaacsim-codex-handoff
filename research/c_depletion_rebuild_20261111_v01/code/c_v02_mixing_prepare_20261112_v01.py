"""After V02 QA: lock equal1250 mixtures and original real polygon-to-bitmap inputs; no training."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='1'
import csv,json,random,hashlib,collections
from pathlib import Path
import cv2,numpy as np
cv2.setNumThreads(1)
R=Path(__file__).resolve().parents[1];S=Path('/home/user/hh/isaac_cosmos/sdg_final');B=S/'C_DEPLETION_REBUILD_20261111_v01';V=B/'C_V02_20261112_v01';E=V/'execution_v01';M=V/'MIX_C06_20261112_v01';M.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert json.loads((E/'dataset_QA_bitmap_v01/result.json').read_text())['state']=='PASS';assert json.loads((V/'real_compatibility_audit_v01/result.json').read_text())['state']=='PASS_WITH_DISCLOSED_ANNOTATION_DOMAIN_LIMITATIONS';P=E/'C_BITMAP_PACKAGE_v01';reg=json.loads((P/'bitmap_registry.json').read_text());inventory=json.loads((V/'real_compatibility_audit_v01/inventory.json').read_text());real=[r for r in inventory if r['split']=='train'];rv=[r for r in inventory if r['split']=='val'];assert len(real)==352 and len(rv)==48
for r in real+rv:
 assert sha(r['image'])==r['image_sha256'] and sha(r['label'])==r['label_sha256'];h,w=r['shape'];paths=[]
 for i,line in enumerate(Path(r['label']).read_text().splitlines()):
  if not line.strip():continue
  z=list(map(float,line.split()));assert z[0]==0;xy=np.array(z[1:]).reshape(-1,2)*[w,h];m=np.zeros((h,w),np.uint8);cv2.fillPoly(m,[xy.astype(np.int32)],255);assert m.any();p=M/'real_bitmap_GT'/r['split']/(Path(r['image']).stem+f'_Load_{i+1:02d}.png');p.parent.mkdir(parents=True,exist_ok=True);cv2.imwrite(str(p),m);paths.append(str(p))
 reg[str(Path(r['image']).resolve())]=dict(masks=paths,shape=[h,w],source_label=r['label'],original_instance_order=True)
(M/'bitmap_registry.json').write_text(json.dumps(reg,indent=2));(M/'manifests').mkdir();rows=list(csv.DictReader((V/'data_design_v01/scene_manifest.csv').open()));levels=['C100','C80','C60','C40','C20'];buckets={c:sorted([r['scene_id'] for r in rows if r['split']=='train' and r['C']==c]) for c in levels};rng=random.Random(20261112)
for c in levels:rng.shuffle(buckets[c]);assert len(buckets[c])==250
syn_order=[buckets[c][i] for i in range(250) for c in levels];rng.shuffle(real);recipes=[]
for name,ns,nr in [('S100_R000',1250,0),('S075_R025',938,312),('S050_R050',625,625),('S025_R075',312,938),('S000_R100',0,1250)]:
 rr=[dict(source='synthetic',key=x,copy=0) for x in syn_order[:ns]]+[dict(source='real',key=real[i%352]['image'],copy=i//352) for i in range(nr)];assert len(rr)==1250
 with (M/'manifests'/(name+'.csv')).open('x',newline='') as f:w=csv.DictWriter(f,list(rr[0]));w.writeheader();w.writerows(rr)
 recipes.append(dict(ratio=name,synthetic=ns,synthetic_C_counts=dict(collections.Counter(next(x['C'] for x in rows if x['scene_id']==r['key']) for r in rr if r['source']=='synthetic')),real=nr,real_unique=min(nr,352),real_repeated_entries=max(0,nr-352),real_max_copies=(nr+351)//352 if nr else 0,manifest_sha256=sha(M/'manifests'/(name+'.csv'))))
sel=json.loads((B/'execution_v02/C_COMMON_HPO_v02/selection_lock.json').read_text());protocol=dict(status='LOCKED',C06=sel['params'],source_selection_sha256=sha(B/'execution_v02/C_COMMON_HPO_v02/selection_lock.json'),ratios=recipes,training_seeds=[42,43,44],sampling_seed=20261112,pretrained_only=True,epochs=200,train_samples=1250,source_real_train_unique=352,source_real_val=48,annotation_policy='original target-only Roboflow labels from accepted B1 LOCKED v03; no label repair; different product/site domain',checkpoint_rule='each representation: max .5*own C-V02 Val Mask mAP5095 + .5*realVal Mask mAP5095; strict greater, ties earliest epoch',real_only_rule='three seed trajectories shared; evaluate all3 C Val domains and save per-rep balanced checkpoint (may differ by epoch); no redundant real-only training',common_ratio_rule='maximum equal mean of balanced checkpoint scores over3 reps x3 seeds; exact ties prefer higher synthetic fraction in fixed ratio order; Test never used',physical_motion_authorized=False,max_unique_train_jobs=39,max_model_epochs=7800,nominal_rep_ratio_seed_cells=45,synthetic_baseline_reuse=9)
(M/'protocol.json').write_text(json.dumps(protocol,indent=2));(M/'result.json').write_text(json.dumps(dict(state='COMPLETED',ratios=recipes,unique_training_jobs=39),indent=2));print('MIX locked39 unique train jobs; no HPO repeated')
