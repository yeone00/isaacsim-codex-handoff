"""C540 result-file-only outcome v05 (2026-11-14) for session v07 = outcome v04 rules with:
- site relocation: the evaluation-only design centre / canonical PRE / FINAL are shifted by run_spec['site_offset'] (default 0,0 = v04);
  SUCCESS definition, MAIN band (0.11 m / 7.341774 deg), 5 mm / 2 deg leg rule and categories are unchanged.
- speed guard: replays speed_guard_ticks.jsonl with guard F v03 for the run's recorded speed policy, PER LEG (the session resets the guard at
  each leg start); MODE_INCONSISTENT counts as a trip.
- multi-view: perception funnel = K1/K2/K3 (multiview.json); reported initial / additional / final detection; the counted pose error is the one of
  the capture that produced the driven target.
- controlled multi-view stops (session failure_reason MULTIVIEW_*): if the zero recovery verified the stop (postfault_quiet PASS ZERO_ONLY, ROS zero
  receipt valid, observer+driver exit 0, no collision) -> FAIL_A (MULTIVIEW_NO_DETECTION) / FAIL_C (MULTIVIEW_PLAN_REJECTED) / FAIL_B (other
  MULTIVIEW_PERCEPTION_*); otherwise HOLD_SAFETY.
- SPEED_GUARD_ABORT handling identical to v03/v04 (FAIL_SAFETY_ABORT only with verified stop, else HOLD_SAFETY)."""
from pathlib import Path
import json, math
import evaluation.stage4_ablation_outcome_20261110_v01 as base
from evaluation.c_v02_speed_phase_policy_20261114_v01 import SpeedPolicy
from evaluation.c_v02_drive540_speed_guard_f_20261114_v03 import trip_from_ticks

D0 = (-25.888, 30.509); FIN_BACK = 1.403745031260775; PRE_BACK = 2.203745031260775


def _load(p):
    p = Path(p)
    try: return json.loads(p.read_text()) if p.exists() else None
    except ValueError: return None


def _verified_stop(A, out):
    pq = _load(A / 'postfault_quiet.json') or {}; owners = _load(A / 'owned_processes.json') or {}
    receipt_ok = bool((pq.get('receipt') or {}).get('valid')); exits_ok = all((owners.get(k) or {}).get('exit_code') == 0 for k in ('observer', 'driver'))
    no_collision = not out.get('collision') and not str(out.get('reason') or '').startswith(('COLLISION', 'SHELL_FLOOR'))
    ok = pq.get('status') == 'PASS' and pq.get('mode') == 'ZERO_ONLY' and receipt_ok and exits_ok and no_collision
    return ok, dict(postfault_quiet=pq.get('status'), receipt_valid=receipt_ok, owners_exit_0=exits_ok, no_collision=no_collision, stop_verified=ok)


def summarize(run):
    run = Path(run); A = run / 'attempt_0001'; spec = json.loads((run / 'run_spec.json').read_text())
    off = spec.get('site_offset') or [0., 0.]; dc = (D0[0] + off[0], D0[1] + off[1])
    saved = (base.DESIGN_CENTER, base.CANON_FINAL)
    base.DESIGN_CENTER = dc; base.CANON_FINAL = (dc[0], dc[1] - FIN_BACK)
    try: out = base.summarize(run)
    finally: base.DESIGN_CENTER, base.CANON_FINAL = saved
    out.update(site_offset=off, design_center_eval_only=list(dc))
    out.update(C=spec['C'], load_count=1, pallet_count=1, model_seed=42, target_selection_accuracy_primary=False, task_layer_count=spec['task_layer_count'], base_id=spec['base_id'], source_family=spec['source_family'])
    out['raw_single_tick_ge_0p03'] = out.get('speed_guard_trip_at')
    sg = (_load(A / 'runtime_opt_stats.json') or {}).get('speed_guard') or {}
    pol = SpeedPolicy.from_dict(sg['speed_policy']) if sg.get('speed_policy') else SpeedPolicy(mode='LEGACY_V02', cruise=sg.get('cruise_m_s', .02))
    trip = None
    if (A / 'speed_guard_ticks.jsonl').exists():
        legs = {}
        for line in open(A / 'speed_guard_ticks.jsonl'):
            try: r = json.loads(line)
            except ValueError: continue
            legs.setdefault(r.get('leg', 0), []).append(r)
        for k in sorted(legs):
            trip = trip_from_ticks(legs[k], pol)
            if trip: trip['leg'] = k; break
    out.update(speed_guard_rule='F_v03_policy_phase_per_leg', speed_policy=pol.to_dict(), speed_policy_sha256=pol.sha256(), speed_guard_trip=trip is not None, speed_guard_trip_at=trip,
               session_guard_trip=sg.get('trip'), max_pulse_planar_m_s=out.get('max_pulse_planar_m_s'))
    # multi-view funnel
    mv = _load(A / 'multiview.json'); caps = (mv or {}).get('captures') or []
    k1 = out.get('perception_status') == 'DETECTED'
    det_k = (mv or {}).get('detected_at') if (mv or {}).get('obs_stop_pose') else (1 if k1 else None)  # observation leg driven -> the K2/K3 capture drove the target
    out.update(multiview_active=bool(mv and len(caps) > 1 or (mv or {}).get('obs_stop_pose')), multiview_forced=bool((mv or {}).get('forced')),
               initial_detected=k1, detected_at_capture=det_k, captures_used=len(caps) if (mv or {}).get('obs_stop_pose') else 1,
               capture_confs=[c.get('conf') for c in caps] if caps else [out.get('detection_conf')], final_detected=det_k is not None,
               multiview_duration_wall_s=(mv or {}).get('duration_wall_s'))
    if det_k in (2, 3):
        e = base.pose_err(A / f'mv{det_k}' / 'pose_ROBUST_A.json')
        if e.get('center'):
            dx = e['center'][0] - dc[0]; dy = e['center'][1] - dc[1]
            out.update(pred_center_x=e['center'][0], pred_center_y=e['center'][1], pose_err_lat_m=dx, pose_err_long_m=dy, pose_err_xy_m=math.hypot(dx, dy), pose_source=f'K{det_k}')
        pr = _load(A / f'mv{det_k}' / 'perception_result.json') or {}; out['detection_conf'] = pr.get('detection_conf')
    ss = _load(A / 'session_result_stage3.json') or {}; fr = str(ss.get('failure_reason') or '')
    out['main_position_limit_m'] = .11; out['main_yaw_limit_deg'] = 7.341774
    if fr.startswith('SPEED_GUARD_ABORT:'):
        ok, info = _verified_stop(A, out); out['safety_abort'] = dict(info, session_trip=sg.get('trip'))
        out.update(outcome='FAIL_SAFETY_ABORT', category='S', reason='SPEED_GUARD_ABORT_VERIFIED_STOP') if ok else out.update(outcome='HOLD_SAFETY', category='S', reason='SPEED_GUARD_ABORT_STOP_NOT_VERIFIED')
        return out
    if fr.startswith('MULTIVIEW_'):
        ok, info = _verified_stop(A, out); out['multiview_stop'] = info
        cat = 'A' if fr.startswith('MULTIVIEW_NO_DETECTION') else 'C' if fr.startswith('MULTIVIEW_PLAN_REJECTED') else 'B'
        out.update(outcome='FAIL_' + cat, category=cat, reason=fr) if ok else out.update(outcome='HOLD_SAFETY', category=cat, reason='MULTIVIEW_STOP_NOT_VERIFIED:' + fr)
        return out
    if spec['role'] == 'engineering':
        legs = _load(A / 'legs_result.json') or []
        ok = ss.get('status_before_cleanup') == 'DRIVE_COMPLETED' and ss.get('eligible') is True and out.get('executed_motion') and not out.get('speed_guard_trip') and legs and all(x.get('reached') and (x.get('stop') or {}).get('confirmed') for x in legs)
        out.update(outcome='ENGINEERING_CONTROL_PASS' if ok else 'ENGINEERING_CONTROL_FAILED', counted=False, engineering_only=True, research_E2E_success=False)
        return out
    if out['outcome'] == 'SUCCESS':
        if out.get('speed_guard_trip') or out.get('lifecycle_eligible') is not True: out.update(outcome='HOLD_SAFETY', reason='C_STRICT_LIFECYCLE_OR_SPEED_NOT_CERTIFIED')
        elif out.get('final_heading_err_deg', 999) > 7.341774: out.update(outcome='FAIL_F', reason='FINAL_OUTSIDE_C_APPROVED_MAIN_YAW')
    return out
