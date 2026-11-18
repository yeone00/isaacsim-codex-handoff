"""C540 result-file-only outcome v03 (2026-11-14) = v02 with the speed rule replaced by filtered guard F, plus FAIL_SAFETY_ABORT.
- speed_guard_trip := F trip over the recorded 'pulse' ticks (single tick >= 0.045 or 6-tick mean >= 0.03); the old single-tick >= 0.03
  event is still reported as raw_single_tick_ge_0p03 (information only).
- A session that ended with SPEED_GUARD_ABORT is:
    FAIL_SAFETY_ABORT (category S)  only if the zero recovery verified the stop: postfault_quiet status PASS, ROS zero receipt valid,
                                    driver and observer exit 0, no collision / unexpected-contact reason;
    HOLD_SAFETY                     otherwise (stop not independently verified).
- Every other rule (SUCCESS definition, main band 0.11 m / 7.341774 deg, categories) is unchanged from v02."""
from pathlib import Path
import json
from evaluation.stage4_ablation_outcome_20261110_v01 import summarize as original
from evaluation.c_v02_drive540_speed_guard_f_20261114_v01 import trip_from_steps


def _load(p):
    p = Path(p)
    try: return json.loads(p.read_text()) if p.exists() else None
    except ValueError: return None


def summarize(run):
    out = original(run); run = Path(run); A = run / 'attempt_0001'; spec = json.loads((run / 'run_spec.json').read_text())
    out.update(C=spec['C'], load_count=1, pallet_count=1, model_seed=42, target_selection_accuracy_primary=False, task_layer_count=spec['task_layer_count'], base_id=spec['base_id'], source_family=spec['source_family'])
    out['raw_single_tick_ge_0p03'] = out.get('speed_guard_trip_at')
    sg = (_load(A / 'runtime_opt_stats.json') or {}).get('speed_guard') or {}
    thr = dict(instant=sg.get('instant', .045), mean=sg.get('mean', .03), n=sg.get('n', 6))
    trip = trip_from_steps(open(A / 'steps.jsonl')) if (A / 'steps.jsonl').exists() else None   # result rule always uses the PROTOCOL thresholds
    session_trip = sg.get('trip')
    out.update(speed_guard_rule='F(instant>=0.045 or mean6>=0.03)', speed_guard_trip=trip is not None, speed_guard_trip_at=trip, session_guard_thresholds=thr,
               session_guard_test_override=bool(sg.get('test_override')), session_guard_trip=session_trip)
    ss = _load(A / 'session_result_stage3.json') or {}
    if str(ss.get('failure_reason') or '').startswith('SPEED_GUARD_ABORT:'):
        pq = _load(A / 'postfault_quiet.json') or {}; owners = _load(A / 'owned_processes.json') or {}
        receipt_ok = bool((pq.get('receipt') or {}).get('valid'))
        exits_ok = all((owners.get(k) or {}).get('exit_code') == 0 for k in ('observer', 'driver'))
        no_collision = not out.get('collision') and not str(out.get('reason') or '').startswith(('COLLISION', 'SHELL_FLOOR'))
        verified = pq.get('status') == 'PASS' and pq.get('mode') == 'ZERO_ONLY' and receipt_ok and exits_ok and no_collision
        out['safety_abort'] = dict(session_trip=session_trip, postfault_quiet=pq.get('status'), receipt_valid=receipt_ok, owners_exit_0=exits_ok, no_collision=no_collision, stop_verified=verified)
        if verified: out.update(outcome='FAIL_SAFETY_ABORT', category='S', reason='SPEED_GUARD_ABORT_VERIFIED_STOP')
        else: out.update(outcome='HOLD_SAFETY', category='S', reason='SPEED_GUARD_ABORT_STOP_NOT_VERIFIED')
        out['main_position_limit_m'] = .11; out['main_yaw_limit_deg'] = 7.341774
        return out
    if spec['role'] == 'engineering':
        legs = _load(A / 'legs_result.json') or []   # identical to v02
        ok = ss.get('status_before_cleanup') == 'DRIVE_COMPLETED' and ss.get('eligible') is True and out.get('executed_motion') and not out.get('speed_guard_trip') and legs and all(x.get('reached') and (x.get('stop') or {}).get('confirmed') for x in legs)
        out.update(outcome='ENGINEERING_CONTROL_PASS' if ok else 'ENGINEERING_CONTROL_FAILED', counted=False, target_source='INDEPENDENT_ENGINEERING_REFERENCE_ONLY', engineering_only=True, research_E2E_success=False)
        return out
    if out['outcome'] == 'SUCCESS':
        if out.get('speed_guard_trip') or out.get('lifecycle_eligible') is not True: out.update(outcome='HOLD_SAFETY', reason='C_STRICT_LIFECYCLE_OR_SPEED_NOT_CERTIFIED')
        elif out.get('final_heading_err_deg', 999) > 7.341774: out.update(outcome='FAIL_F', reason='FINAL_OUTSIDE_C_APPROVED_MAIN_YAW')
    out['main_position_limit_m'] = .11; out['main_yaw_limit_deg'] = 7.341774
    return out
