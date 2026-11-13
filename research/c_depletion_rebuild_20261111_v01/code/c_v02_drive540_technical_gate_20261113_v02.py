"""Result-file-only scientific/technical distinction. No simulation or model imports."""
from pathlib import Path
import json

def read(p):
 p=Path(p)
 return json.loads(p.read_text()) if p.exists() else None

def assess(run,engineering=False):
 run=Path(run);A=run/'attempt_0001';result=read(run/'result.json') or {};session=read(A/'session_result_stage3.json') or {};runner=read(run/'runner_status.json') or {};physical=read(A/'pilot_physical_admission.json') or {};cam=read(A/'camera_metadata.json') or {};render=read(A/'render_auto_admission.json') or {};runtime=read(A/'runtime_summary.json') or {};owners=read(A/'owned_processes.json') or {};perc=read(A/'perception_result.json') or {};quiet=read(A/'stop_quiet_result.json') or {};cleanup=read(A/'cleanup_zero_classification.json') or {};reason=str(session.get('failure_reason') or result.get('reason') or '');issues=[]
 required=['C_scene_construction.json','actual_loaded_C_stage_manifest.json','pilot_physx_C.json','support_admission.json','camera_metadata.json','front_rgb.png','front_rgb.npy','front_depth.npy','perception_result.json','frozen_model_manifest.json','detections.json','runtime_summary.json','steps.jsonl','contacts.json','owned_processes.json','session_result_stage3.json']
 issues+=['EVIDENCE_MISSING:'+n for n in required if not (A/n).exists()]
 if perc.get('perception_status')=='DETECTED' and not (A/'selected_mask.npy').exists():issues.append('DETECTED_MASK_EVIDENCE_MISSING')
 model=read(A/'frozen_model_manifest.json') or {};spec=read(run/'run_spec.json') or {}
 if model.get('imgsz')!=640 or model.get('conf')!=.25 or model.get('iou')!=.7:issues.append('FROZEN_PERCEPTION_SETTINGS_MISMATCH')
 if model.get('observed_sha256')!=spec.get('checkpoint_sha256'):issues.append('MODEL_SHA_PROVENANCE_MISMATCH')
 if not (run/'run_spec.json').exists() or not (run/'runner_status.json').exists():issues.append('RUN_PROVENANCE_MISSING')
 if not physical.get('pass'):issues.append('PRE_DRIVE_PHYSICAL_ADMISSION_NOT_PASS')
 if not cam.get('checks') or not all(cam['checks'].values()):issues.append('CAMERA_CHECKS_NOT_PASS')
 if not render.get('pass'):issues.append('RENDER_ADMISSION_NOT_PASS')
 if (runtime.get('physics') or {}).get('steps',0)<120:issues.append('INSUFFICIENT_ACTUAL_PHYSICS_STEPS')
 if runner.get('forced_termination') or runner.get('watchdog') or runner.get('reason'):issues.append('RUNNER_INFRASTRUCTURE_FAULT')
 if session.get('process_failure') or session.get('cleanup_graph_zero_error'):issues.append('CLEANUP_PROCESS_OR_GRAPH_ZERO_FAILURE')
 if not owners.get('observer') or owners['observer'].get('exit_code')!=0:issues.append('OBSERVER_NOT_CLEANLY_EXITED')
 if result.get('speed_guard_trip') or (A/'driver_guard_fault.json').exists():issues.append('SPEED_OR_DRIVER_GUARD_FAULT')
 if reason.startswith(('COLLISION','MEASURED_STEERING','GRAPH_STEERING','EMERGENCY_','STATIONARY_','SHELL_FLOOR','DISCOVERY_','ISOLATION_','GC_MEMORY_','ACTOR_','ROS_')):issues.append('SAFETY_OR_STATE_FAULT:'+reason)
 if perc.get('status') in ('INTERNAL_EXCEPTION','PIPELINE_ERROR') or perc.get('pose_status')=='PIPELINE_ERROR' or 'PIPELINE_ERROR' in reason:issues.append('PERCEPTION_PIPELINE_ERROR')
 moved=bool(result.get('executed_motion'));driver=owners.get('driver');nonzero=runtime.get('nonzero_commands',0);no_motion=not moved and nonzero==0 and driver is None
 normal_failure=False
 if no_motion and (reason.startswith('PERCEPTION_NO_DETECTION:') or reason.startswith('POSE_') or reason.startswith('PLAN_REJECTED:') or reason.startswith('FOOTPRINT_CLEARANCE_FAIL:')):
  if quiet.get('QUIET')!='PASS':issues.append('NO_MOTION_FAILURE_NOT_QUIET')
  if cleanup.get('status')!='NOT_APPLICABLE_PRE_DRIVER':issues.append('PRE_DRIVER_CLEANUP_NOT_CERTIFIED')
  # Abort marker is intentionally authored by cleanup; evaluate actual graph readback instead.
  last=None
  sp=A/'steps.jsonl'
  if sp.exists():
   with sp.open() as f:
    for line in f:
     if line.strip():last=json.loads(line)
  if last is None or last.get('graph_wheel_target_rad_s') is None or any(abs(x)>1e-12 for x in last['graph_wheel_target_rad_s']):issues.append('PRE_DRIVER_GRAPH_ZERO_NOT_VERIFIED')
  normal_failure=True
 elif moved:
  legs=read(A/'legs_result.json') or [];n=session.get('n_legs');receipt=session.get('cleanup_receipt') or {}
  if session.get('status_before_cleanup')!='DRIVE_COMPLETED' or not session.get('eligible'):issues.append('MOTION_LIFECYCLE_NOT_CERTIFIED')
  if not legs or len(legs)!=n or not all(x.get('reached') and (x.get('stop') or {}).get('confirmed') for x in legs):issues.append('PRE_FINAL_REACH_STOP_CERTIFICATES_NOT_PASS')
  if quiet.get('QUIET')!='PASS' or not receipt.get('valid'):issues.append('POST_MOTION_QUIET_ZERO_RECEIPT_NOT_PASS')
  if not driver or driver.get('exit_code')!=0:issues.append('DRIVER_NOT_CLEANLY_EXITED')
  if not list((A/'rec_robotcam').glob('*.jpg')):issues.append('MOTION_VIDEO_FRAMES_MISSING')
  normal_failure=result.get('outcome')=='FAIL_F' and reason=='FINAL_OUTSIDE_MAIN_BAND'
 else:issues.append('UNCLASSIFIED_OR_PARTIAL_MOTION_TERMINATION:'+reason)
 if engineering and not moved:issues.append('ENGINEERING_ACTUAL_MOTION_REQUIRED')
 if not engineering and result.get('outcome')!='SUCCESS' and not normal_failure:issues.append('NOT_A_VALIDATED_SCIENTIFIC_FAILURE:'+str(result.get('outcome')))
 return dict(state='PASS_TECHNICAL' if not issues else 'HOLD',technical_pass=not issues,task_success=(result.get('outcome')=='SUCCESS') and not engineering,scientific_outcome=result.get('outcome'),reason=reason,normal_scientific_failure=normal_failure,actual_motion=moved,control_motion_certified=moved and not issues,engineering_only=engineering,issues=issues,run_dir=str(run),GT_operational_input=False)
