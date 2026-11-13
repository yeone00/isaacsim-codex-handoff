"""Safety regression against actual failed pilot plus clearly separated mutated fixtures."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from evaluation.c_v02_drive540_technical_gate_20261113_v02 import assess
D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');P=D/'recovery_e2e_v01/pilot/C2D_B01_C100_HR_Scan_O0';O=D/'technical_policy_amendment_v01/validator_regression_v01';O.mkdir(exist_ok=False);rows=[]
def clone(name):
 t=O/name;t.mkdir();(t/'attempt_0001').mkdir()
 for parent in [P,P/'attempt_0001']:
  out=t if parent==P else t/'attempt_0001'
  for p in parent.iterdir():
   if p.is_file(): (out/p.name).symlink_to(p)
 return t

def mutate(p,fn):
 data=json.loads(p.read_text());p.unlink();fn(data);p.write_text(json.dumps(data))
base=assess(P);assert base['technical_pass'] and not base['task_success'] and not base['control_motion_certified'];rows.append(dict(case='actual_NO_DETECTION_is_normal_failure_not_control_pass',PASS=True))
assert not assess(P,engineering=True)['technical_pass'];rows.append(dict(case='no_motion_cannot_certify_engineering_control',PASS=True))
for name,rel,fn in [('speed_guard','result.json',lambda x:x.update(speed_guard_trip=True)),('camera_invalid','attempt_0001/camera_metadata.json',lambda x:x['checks'].update(renderer_optical_world_match=False)),('pipeline_error','attempt_0001/perception_result.json',lambda x:x.update(pose_status='PIPELINE_ERROR')),('model_sha','attempt_0001/frozen_model_manifest.json',lambda x:x.update(observed_sha256='bad')),('zero_readback','attempt_0001/runtime_summary.json',lambda x:x.update(nonzero_commands=1))]:
 t=clone(name);mutate(t/rel,fn);result=assess(t);assert not result['technical_pass'],name;rows.append(dict(case=name,PASS=True,issues=result['issues']))
t=clone('missing_RGB');(t/'attempt_0001/front_rgb.png').unlink();assert not assess(t)['technical_pass'];rows.append(dict(case='missing_evidence',PASS=True))
(O/'result.json').write_text(json.dumps(dict(state='PASS',tests=rows,main_denominator=0,real_artifacts_modified=False),indent=2));print('PASS',len(rows),'safety gate regressions')
