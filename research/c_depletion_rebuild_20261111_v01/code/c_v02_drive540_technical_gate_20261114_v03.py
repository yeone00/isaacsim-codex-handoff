"""C540 technical gate v03 (2026-11-14) = v02 unchanged for every run, plus ONE narrowly defined normal scientific failure:
FAIL_SAFETY_ABORT (outcome v03) is accepted as a validated scientific failure only if ALL of these hold; otherwise HOLD:
  - session failure_reason starts with SPEED_GUARD_ABORT: and speed_guard_abort.json exists (the session's F guard fired);
  - postfault_quiet.json: status PASS, mode ZERO_ONLY, ROS zero receipt valid (independent physical stop + command release);
  - observer and driver exited with code 0; runner had no watchdog/forced termination; no evidence missing;
  - no collision / shell / steering / emergency / discovery / GC / actor fault reason, no perception pipeline error;
  - the v02 issues present are ONLY those that a guard abort necessarily produces (listed in EXPECTED_FROM_GUARD_ABORT).
A HOLD_SAFETY outcome (stop not verified) or any additional issue stays technical_pass=False."""
import json
from pathlib import Path
from evaluation.c_v02_drive540_technical_gate_20261113_v02 import assess as assess_v02, read
EXPECTED_FROM_GUARD_ABORT = ('SPEED_OR_DRIVER_GUARD_FAULT', 'MOTION_LIFECYCLE_NOT_CERTIFIED', 'PRE_FINAL_REACH_STOP_CERTIFICATES_NOT_PASS', 'POST_MOTION_QUIET_ZERO_RECEIPT_NOT_PASS',
                             'NOT_A_VALIDATED_SCIENTIFIC_FAILURE:FAIL_SAFETY_ABORT', 'UNCLASSIFIED_OR_PARTIAL_MOTION_TERMINATION:SPEED_GUARD_ABORT_VERIFIED_STOP')
FORBIDDEN_PREFIXES = ('EVIDENCE_MISSING', 'DETECTED_MASK', 'FROZEN_PERCEPTION', 'MODEL_SHA', 'RUN_PROVENANCE', 'PRE_DRIVE_PHYSICAL', 'CAMERA_CHECKS', 'RENDER_ADMISSION', 'INSUFFICIENT_ACTUAL_PHYSICS',
                      'RUNNER_INFRASTRUCTURE', 'CLEANUP_PROCESS', 'OBSERVER_NOT_CLEANLY', 'SAFETY_OR_STATE_FAULT', 'PERCEPTION_PIPELINE_ERROR', 'DRIVER_NOT_CLEANLY_EXITED', 'MOTION_VIDEO_FRAMES_MISSING')


def assess(run, engineering=False):
    base = assess_v02(run, engineering=engineering); run = Path(run); A = run / 'attempt_0001'; result = read(run / 'result.json') or {}
    if result.get('outcome') != 'FAIL_SAFETY_ABORT':
        base['gate_version'] = 'v03(=v02)'; return base
    ss = read(A / 'session_result_stage3.json') or {}; pq = read(A / 'postfault_quiet.json') or {}; owners = read(A / 'owned_processes.json') or {}; runner = read(run / 'runner_status.json') or {}
    checks = dict(session_guard_abort=str(ss.get('failure_reason') or '').startswith('SPEED_GUARD_ABORT:') and (A / 'speed_guard_abort.json').exists(),
                  postfault_quiet_pass=pq.get('status') == 'PASS' and pq.get('mode') == 'ZERO_ONLY', zero_receipt_valid=bool((pq.get('receipt') or {}).get('valid')),
                  owners_exit_0=all((owners.get(k) or {}).get('exit_code') == 0 for k in ('observer', 'driver')),
                  runner_clean=not (runner.get('forced_termination') or runner.get('watchdog') or runner.get('reason')),
                  no_collision=result.get('collision') is False,
                  only_expected_issues=all(i in EXPECTED_FROM_GUARD_ABORT for i in base['issues']),
                  no_forbidden_issue=not any(i.startswith(FORBIDDEN_PREFIXES) for i in base['issues']))
    ok = all(checks.values())
    base.update(gate_version='v03', safety_abort_checks=checks, v02_issues=list(base['issues']), issues=[] if ok else ['SAFETY_ABORT_NOT_VALIDATED:' + ','.join(k for k, v in checks.items() if not v)] + list(base['issues']),
                technical_pass=ok, state='PASS_TECHNICAL' if ok else 'HOLD', normal_scientific_failure=ok, control_motion_certified=False)
    return base
