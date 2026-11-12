"""Independent CPU report after ratio selection, no model changes or extra inference."""
import time,json,csv,statistics
from pathlib import Path
V=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01');P=V/'mixing_execution_v01/models_by_ratio.json'
while not P.exists():time.sleep(60)
a=json.loads(P.read_text());rows=[]
for ratio,models in a.items():
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  rr=[m for m in models if m['rep']==rep];assert len(rr)==3
  z=dict(ratio=ratio,rep=rep,seeds='42/43/44',n_training_seeds=3)
  for metric in ['combined_validation','synthetic_validation','real_validation']:
   vals=[m[metric] for m in rr];z[metric+'_mean']=statistics.mean(vals);z[metric+'_sd']=statistics.stdev(vals)
  rows.append(z)
p=V/'ratio_seed_summary_v01.csv'
with p.open('x',newline='') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
(V/'ratio_seed_summary_notes_v01.json').write_text(json.dumps(dict(state='COMPLETED',rows=15,real_only_training_trajectories=3,real_only_rep_checkpoint_may_differ=True,mean_SD='over3training seeds within each representation; not9independent real-only trainings',Test_used=False),indent=2))
