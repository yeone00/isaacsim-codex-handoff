"""C540 technical gate v04 (2026-11-14) = v03 unchanged for every run, plus ONE more narrowly defined normal scientific failure for the
multi-view protocol (session v07 / outcome v05): a controlled MULTIVIEW_* stop (no gated detection in K1-K3, or the OBS->FINAL plan rejected,
or K2/K3 pose failure) after a CERTIFIED observation leg is accepted only if ALL hold; otherwise HOLD:
  - outcome v05 = FAIL_A / FAIL_B / FAIL_C with multiview_stop.stop_verified (postfault_quiet PASS ZERO_ONLY, ROS zero receipt valid,
    observer+driver exit 0, no collision); session failure_reason starts with MULTIVIEW_;
  - exactly one leg recorded (the observation leg), reached (5 mm / 2 deg) with a confirmed stop certificate;
  - multiview.json exists and the capture evidence (front_rgb.npy, camera_metadata.json, perception_result.json) exists for every capture made;
  - runner clean, no speed-guard trip; a driver_guard_fault.json is allowed ONLY with reason ABORT_DURING_VALIDATION (the driver saw the
    session's controlled abort while paused at the certified OBS stop); no forbidden issue; v02 issues limited to what such a stop produces."""
import json
from pathlib import Path
from evaluation.c_v02_drive540_technical_gate_20261114_v03 import assess as assess_v03, FORBIDDEN_PREFIXES
from evaluation.c_v02_drive540_technical_gate_20261113_v02 import read
EXPECTED_FROM_MV_STOP = ('MOTION_LIFECYCLE_NOT_CERTIFIED', 'PRE_FINAL_REACH_STOP_CERTIFICATES_NOT_PASS', 'POST_MOTION_QUIET_ZERO_RECEIPT_NOT_PASS')


def assess(run, engineering=False):
    base = assess_v03(run, engineering=engineering); run = Path(run); A = run / 'attempt_0001'; result = read(run / 'result.json') or {}
    ss = read(A / 'session_result_stage3.json') or {}; fr = str(ss.get('failure_reason') or '')
    if not fr.startswith('MULTIVIEW_') or result.get('outcome') not in ('FAIL_A', 'FAIL_B', 'FAIL_C'):
        base['gate_version'] = 'v04(=v03)'; return base
    legs = read(A / 'legs_result.json') or []; mv = read(A / 'multiview.json') or {}; runner = read(run / 'runner_status.json') or {}
    caps = [c for c in mv.get('captures', []) if c.get('k', 1) > 1]
    checks = dict(stop_verified=bool((result.get('multiview_stop') or {}).get('stop_verified')),
                  obs_leg_certified=len(legs) == 1 and bool(legs[0].get('reached')) and bool((legs[0].get('stop') or {}).get('confirmed')),
                  multiview_evidence=bool(mv) and bool(caps) and all(all((A / ('mv%d' % c['k']) / n).exists() for n in ('front_rgb.npy', 'camera_metadata.json', 'perception_result.json')) for c in caps),
                  runner_clean=not (runner.get('forced_termination') or runner.get('watchdog') or runner.get('reason')),
                  no_guard_fault=not result.get('speed_guard_trip') and (not (A / 'driver_guard_fault.json').exists() or (read(A / 'driver_guard_fault.json') or {}).get('reason') == 'ABORT_DURING_VALIDATION'),
                  no_collision=result.get('collision') is False,
                  only_expected_issues=all(i in EXPECTED_FROM_MV_STOP or (i == 'SPEED_OR_DRIVER_GUARD_FAULT' and not result.get('speed_guard_trip') and (read(A / 'driver_guard_fault.json') or {}).get('reason') == 'ABORT_DURING_VALIDATION') or i.startswith('NOT_A_VALIDATED_SCIENTIFIC_FAILURE:') or i.startswith('UNCLASSIFIED_OR_PARTIAL_MOTION_TERMINATION:MULTIVIEW_') for i in base['issues']),
                  no_forbidden_issue=not any(i.startswith(FORBIDDEN_PREFIXES) for i in base['issues']))
    ok = all(checks.values())
    base.update(gate_version='v04', multiview_stop_checks=checks, v03_issues=list(base['issues']), issues=[] if ok else ['MULTIVIEW_STOP_NOT_VALIDATED:' + ','.join(k for k, v in checks.items() if not v)] + list(base['issues']),
                technical_pass=ok, state='PASS_TECHNICAL' if ok else 'HOLD', normal_scientific_failure=ok, control_motion_certified=ok)
    return base
