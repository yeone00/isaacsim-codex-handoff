import json
from pathlib import Path
B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01'
for name in ['pipeline_status.json','mixing_execution_v01/status.json','final_static_pipeline_v01/status.json','watchdog_status.json']:
 p=V/name
 if p.exists():
  d=json.loads(p.read_text())
  if name.endswith('status.json') and 'jobs' in d:d['jobs_count']=len(d.pop('jobs'))
  print(name,json.dumps(d,indent=2,ensure_ascii=False))
print('Physical pilot / main300 / O50 150: HOLD')
