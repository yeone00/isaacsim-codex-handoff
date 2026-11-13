"""Result-file-only outcome: original Main gates plus explicit approved C540 constraints."""
from pathlib import Path
import json
from evaluation.stage4_ablation_outcome_20261110_v01 import summarize as original

def summarize(run):
 out=original(run);run=Path(run);spec=json.loads((run/'run_spec.json').read_text());out.update(C=spec['C'],load_count=1,pallet_count=1,model_seed=42,target_selection_accuracy_primary=False,task_layer_count=spec['task_layer_count'],base_id=spec['base_id'],source_family=spec['source_family'])
 if spec['role']=='engineering':
  at=run/'attempt_0001';ss=json.loads((at/'session_result_stage3.json').read_text());legs=json.loads((at/'legs_result.json').read_text()) if (at/'legs_result.json').exists() else []
  ok=ss.get('status_before_cleanup')=='DRIVE_COMPLETED' and ss.get('eligible') is True and out.get('executed_motion') and not out.get('speed_guard_trip') and legs and all(x.get('reached') and (x.get('stop') or {}).get('confirmed') for x in legs)
  out.update(outcome='ENGINEERING_CONTROL_PASS' if ok else 'ENGINEERING_CONTROL_FAILED',counted=False,target_source='INDEPENDENT_ENGINEERING_REFERENCE_ONLY',engineering_only=True,research_E2E_success=False)
  return out
 if out['outcome']=='SUCCESS':
  if out.get('speed_guard_trip') or out.get('lifecycle_eligible') is not True:out.update(outcome='HOLD_SAFETY',reason='C_STRICT_LIFECYCLE_OR_SPEED_NOT_CERTIFIED')
  elif out.get('final_heading_err_deg',999)>7.341774:out.update(outcome='FAIL_F',reason='FINAL_OUTSIDE_C_APPROVED_MAIN_YAW')
 out['main_position_limit_m']=.11;out['main_yaw_limit_deg']=7.341774;return out
