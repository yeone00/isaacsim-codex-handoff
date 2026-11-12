"""CPU OpenUSD audit of original background and historical v30. Not an actual new C loaded-stage certificate."""
import sys,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from pxr import Usd
from evaluation.c_v02_loaded_stage_collider_audit_20261112_v01 import audit
S=Path('/home/user/hh/isaac_cosmos/sdg_final');V=S/'C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01';O=V/'task_layer_policy_v01';rows=[]
for name,p in [('original_NuRec',Path('/home/user/hh/isaac_cosmos/assets/assets/environment/B1_CLOSED_EV.usdz')),('historical_v30_prepared',S/'PILOT_SITE_HR_ADMISSION_20261102_v30_01/prepared_site_drive.usda')]:
 st=Usd.Stage.Open(str(p));assert st;d=audit(st);d['source']=name;d['file_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();rows.append(d)
(O/'historical_composed_stage_audit.json').write_text(json.dumps(dict(state='NEW_C_PHYSICS_HOLD',audits=rows,new_C_actual_loaded_stage_manifest='NOT_CREATED/UNKNOWN',new_C_PhysX_contact_tests='NOT_RUN',originals_changed=False),indent=2));print([(r['source'],r['collision_counts']) for r in rows])
