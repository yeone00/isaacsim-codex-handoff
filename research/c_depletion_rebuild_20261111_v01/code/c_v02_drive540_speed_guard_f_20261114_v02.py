"""C540 filtered speed guard F v02 (2026-11-14) = v01 with per-tick thresholds tied to the driver's governor phase:
PRE_FINAL (final approach, and the whole drive at cruise 0.02): instant 0.045 / 6-tick mean 0.03 (= v01, ceiling 0.03).
H_PRE cruise segment (only when cruise > 0.02 and along-track distance to the leg goal > switch): instant 0.075 / mean 0.05 (= 1.5x and 1.0x the
H_PRE governor ceiling 0.05). The session records every pulse tick's thresholds in speed_guard_ticks.jsonl; the result rule replays that file."""
from collections import deque
THRESH = {'PRE_FINAL': (.045, .03), 'H_PRE': (.075, .05)}
MEAN_N = 6


class FGuardPhase:
    def __init__(self, n=MEAN_N): self.n = n; self.buf = deque(maxlen=n); self.trip = None

    def update(self, v, mode, sim_s=None, step=None, override=None):
        if self.trip is not None: return self.trip
        inst, mean = override or THRESH[mode]
        self.buf.append(float(v)); m = sum(self.buf) / self.n if len(self.buf) == self.n else None
        if v >= inst: self.trip = dict(rule='INSTANT', mode=mode, planar_m_s=float(v), mean6_m_s=m, sim_s=sim_s, step=step, thresholds=dict(instant=inst, mean=mean, n=self.n))
        elif m is not None and m >= mean: self.trip = dict(rule='MEAN6', mode=mode, planar_m_s=float(v), mean6_m_s=m, sim_s=sim_s, step=step, thresholds=dict(instant=inst, mean=mean, n=self.n))
        return self.trip


def trip_from_ticks(lines):
    """Replays speed_guard_ticks.jsonl with the PROTOCOL thresholds of each tick's recorded mode (test overrides ignored)."""
    import json
    g = FGuardPhase()
    for line in lines:
        try: r = json.loads(line)
        except ValueError: continue
        t = g.update(r['v'], r['mode'], r.get('sim_s'), r.get('step'))
        if t: return t
    return None
