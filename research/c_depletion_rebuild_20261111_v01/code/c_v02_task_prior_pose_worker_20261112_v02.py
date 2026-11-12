"""CPU operational estimator replay. Input view contains sensors/model masks/task metadata only; GT forbidden."""
import os
for k in ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS']:os.environ[k]='1'
import argparse,json,sys,time
from pathlib import Path
import numpy as np,cv2
cv2.setNumThreads(1)
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from evaluation.c_v02_task_layer_prior_20261112_v02 import estimate,deny_evaluation_GT_reads,validate_task
p=argparse.ArgumentParser();p.add_argument('--operational-view',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--layer-count',type=int,choices=[1,2,3,4],help='optional assertion for single-count engineering views; full task manifest supplies per-attempt values');a=p.parse_args();a.output.mkdir(exist_ok=False);entries=json.loads(a.operational_view.read_text());records=[]
for i,x in enumerate(entries):
 assert set(x)=={'task','depth','camera','predicted_mask','checkpoint_sha256','prediction_available'},'OPERATIONAL_INPUT_SCHEMA_REJECTED';n=validate_task(x['task'])
 if a.layer_count is not None:assert n==a.layer_count
 assert len(x['checkpoint_sha256'])==64
 with deny_evaluation_GT_reads() as reads:
  d=np.load(x['depth']);m=np.load(x['predicted_mask'])['mask'] if x['prediction_available'] else None;camera=Path(x['camera']).read_text();result=estimate(m,d,camera,x['task'])
 records.append(dict(task_id=x['task']['task_id'],task_layer_count=n,result=result,checkpoint_sha256=x['checkpoint_sha256'],input_read_audit=reads))
 if i%20==0:(a.output/'progress.json').write_text(json.dumps(dict(processed=i+1,total=len(entries),updated=time.time())))
with (a.output/'operational_results.jsonl').open('x') as f:
 for x in records:f.write(json.dumps(x,default=lambda v:v.tolist() if hasattr(v,'tolist') else str(v))+'\n')
(a.output/'result.json').write_text(json.dumps(dict(state='COMPLETED',attempts=len(records),GT_operational_input=False,approved_layer_prior=True,task_layers=sorted({r['task_layer_count'] for r in records}),physical_motion=False),indent=2))
