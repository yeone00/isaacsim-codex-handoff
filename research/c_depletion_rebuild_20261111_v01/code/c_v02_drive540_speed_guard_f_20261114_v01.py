"""C540 filtered speed guard F (v01, 2026-11-14). Shared by session v05 (run abort) and outcome v03 (result rule).
Signal: the same per-tick base planar speed as before ('planar_m_s', root velocity at the base origin), 'pulse' phase only.
Trip if (a) any single tick >= INSTANT (0.045 m/s = 1.5 x the 0.03 ceiling) or (b) the mean of the last MEAN_N=6 pulse ticks (0.1 s)
>= MEAN (0.03 m/s). The driver governor's own per-tick 0.03 command cut, steering bounds, tracking/emergency envelopes and contact
checks are unchanged and independent of this guard. Thresholds are overridable ONLY for non-main technical tests (runner enforces)."""
from collections import deque
INSTANT, MEAN, MEAN_N = .045, .03, 6


class FGuard:
    def __init__(self, instant=INSTANT, mean=MEAN, n=MEAN_N):
        self.instant, self.mean, self.n = instant, mean, n; self.buf = deque(maxlen=n); self.trip = None

    def reset(self): self.buf.clear()

    def update(self, v, sim_s=None, step=None):
        if self.trip is not None: return self.trip
        self.buf.append(float(v))
        m = sum(self.buf) / len(self.buf) if len(self.buf) == self.n else None
        if v >= self.instant: self.trip = dict(rule='INSTANT', planar_m_s=float(v), mean6_m_s=m, sim_s=sim_s, step=step, thresholds=dict(instant=self.instant, mean=self.mean, n=self.n))
        elif m is not None and m >= self.mean: self.trip = dict(rule='MEAN6', planar_m_s=float(v), mean6_m_s=m, sim_s=sim_s, step=step, thresholds=dict(instant=self.instant, mean=self.mean, n=self.n))
        return self.trip


def trip_from_steps(lines, instant=INSTANT, mean=MEAN, n=MEAN_N):
    """Replays recorded steps.jsonl lines: every 'pulse' tick in order, one continuous window (identical to session v05, which never resets it)."""
    import json
    g = FGuard(instant, mean, n)
    for line in lines:
        try: r = json.loads(line)
        except ValueError: continue
        if r.get('phase') == 'pulse':
            t = g.update(float(r.get('planar_m_s') or 0.), r.get('sim_s'), r.get('step'))
            if t: return t
    return None
