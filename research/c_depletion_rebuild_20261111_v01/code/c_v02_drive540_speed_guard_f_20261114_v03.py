"""C540 filtered speed guard F v03 (2026-11-14) = v02 rule (trip if instant >= 1.5 x phase ceiling or 6-tick mean >= 1.0 x phase
ceiling) with the thresholds DERIVED from the speed-phase policy's governor table (SpeedPolicy.guard_thresholds()):
  H_PRE (.075, .05) and PRE_FINAL (.045, .03) are identical to v02; 'navigation' = (1.5, 1.0) x the scaled navigation ceiling.
The tick mode is SpeedPolicy.guard_mode(along) (forward-only), which switches to a slower phase only at boundary - entry_slack_m,
i.e. where the driver is required to be in that phase (else it already raised PHASE_ENTRY_OVERSPEED).
The 6-tick buffer is NOT reset at a mode change: the slower phase's mean threshold applies to the last 6 ticks immediately.
trip_from_ticks() replays speed_guard_ticks.jsonl with protocol thresholds; a recorded mode that disagrees with the policy for the
recorded along-track distance, or a backward mode change, is itself a trip (MODE_INCONSISTENT)."""
import json
from collections import deque
from evaluation.c_v02_speed_phase_policy_20261114_v01 import ORDER
MEAN_N = 6


class FGuardPhase:
    def __init__(self, policy, n=MEAN_N):
        self.policy = policy; self.thresh = policy.guard_thresholds(); self.n = n; self.buf = deque(maxlen=n); self.trip = None; self.mode = None

    def mode_for(self, along):
        m = self.policy.guard_mode(along)
        if self.mode is not None and ORDER.index(m) < ORDER.index(self.mode): m = self.mode  # forward-only latch
        self.mode = m
        return m

    def update(self, v, mode, sim_s=None, step=None, override=None):
        if self.trip is not None: return self.trip
        inst, mean = override or self.thresh[mode]
        self.buf.append(float(v)); m = sum(self.buf) / self.n if len(self.buf) == self.n else None
        if v >= inst: self.trip = dict(rule='INSTANT', mode=mode, planar_m_s=float(v), mean6_m_s=m, sim_s=sim_s, step=step, thresholds=dict(instant=inst, mean=mean, n=self.n))
        elif m is not None and m >= mean: self.trip = dict(rule='MEAN6', mode=mode, planar_m_s=float(v), mean6_m_s=m, sim_s=sim_s, step=step, thresholds=dict(instant=inst, mean=mean, n=self.n))
        return self.trip


def trip_from_ticks(lines, policy):
    g = FGuardPhase(policy); checker = FGuardPhase(policy)
    for line in lines:
        try: r = json.loads(line) if isinstance(line, str) else line
        except ValueError: continue
        if 'along_m' in r:
            expected = checker.mode_for(r['along_m'])
            if r['mode'] != expected:
                return dict(rule='MODE_INCONSISTENT', mode=r['mode'], expected=expected, along_m=r['along_m'], sim_s=r.get('sim_s'), step=r.get('step'))
        t = g.update(r['v'], r['mode'], r.get('sim_s'), r.get('step'))
        if t: return t
    return None
