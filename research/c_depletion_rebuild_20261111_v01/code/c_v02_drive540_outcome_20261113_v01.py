"""Result-file-only outcome: original Main gates plus explicit approved C540 constraints."""
from pathlib import Path
import json
from evaluation.stage4_ablation_outcome_20261110_v01 import summarize as original

def summarize(run):
 out=original(run);run=Path(run);spec=json.loads((run/'run_spec.json').read_text());out.update(C=spec['C'],load_count=1,pallet_count=1,model_seed=42,target_selection_accuracy_primary=False,task_layer_count=spec['task_layer_count'],base_id=spec['base_id'],source_family=spec['source_family'])
 if out['outcome']=='SUCCESS':
  if out.get('speed_guard_trip') or out.get('lifecycle_eligible') is not True:out.update(outcome='HOLD_SAFETY',reason='C_STRICT_LIFECYCLE_OR_SPEED_NOT_CERTIFIED')
  elif out.get('final_heading_err_deg',999)>7.341774:out.update(outcome='FAIL_F',reason='FINAL_OUTSIDE_C_APPROVED_MAIN_YAW')
 out['main_position_limit_m']=.11;out['main_yaw_limit_deg']=7.341774;return out
