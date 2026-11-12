"""Wait for final existing capture, reserve GPU boundary; never signal/kill workers."""
import json,time,fcntl,os
from pathlib import Path
from c_depletion_runtime_20261111_v01 import atomic,event,locked
E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');B=E.parent;O=B/'C_V02_20261112_v01';O.mkdir(exist_ok=True);lock=locked(O/'boundary_guard.lock')
while True:
 p=E/'post_hpo_static_recovered_v01/progress.json';r=json.loads(p.read_text()) if p.exists() else {};done=list((E/'test_occlusion_v01').glob('*/result.json'))
 atomic(O/'boundary_guard_status.json',dict(state='WAIT_FINAL_CAPTURE',pid=os.getpid(),completed_batches=len(done),current=r,updated=time.time()))
 if r.get('stage')=='C_TEST_OCCLUSION_CDEP_B1R_TST_000058_GeoCAD' or len(done)==30:break
 time.sleep(1)
gpu=open('/tmp/b1_common_hpo_gpu_0.lock','a');fcntl.flock(gpu,fcntl.LOCK_EX)
atomic(O/'boundary_guard_status.json',dict(state='GPU_BOUNDARY_RESERVED',pid=os.getpid(),completed_batches=len(list((E/'test_occlusion_v01').glob('*/result.json'))),updated=time.time(),reason='User changed order: C100 V02 and mixing before perception; original processes not signaled'))
event(B,'HOLD',reason='Authorized evaluation boundary reserved after final capture; C-V02 and mixing precede perception. '+str(O))
while not (O/'release_boundary_guard.json').exists():time.sleep(2)
gpu.close();atomic(O/'boundary_guard_status.json',dict(state='RELEASED_TO_V02_CONTROLLER',pid=os.getpid(),updated=time.time()))
