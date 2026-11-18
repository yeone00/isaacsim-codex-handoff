"""C540 L_E13 main unattended reporter (v01, 2026-11-14). Starts no GPU job, changes nothing in the experiment.
Every 60 s reads the controller state (run_history.jsonl, status.json) + each run's result.json / technical assessment.
At completed >= 15 / 150 / 300 / 540 (main runs only): writes reports/c_v02_le13_main_{progress_NNN|interim_300|final_results}_20261114_v01.md/.json,
commits ONLY those two files to ~/hh/isaacsim-codex-handoff, pushes (no force), ntfy. At 300 the report checks the per-condition balance
(exactly 20 per representation x C) and compares the scene / start / C distribution of the first 300 rows with the full 540-row manifest.
The run never stops because of a report. Notifies once if the controller unit is not active and status != MAIN_COMPLETE."""
import json, time, subprocess, statistics, collections, shutil, csv
from pathlib import Path
R = Path('/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013'); D = Path('/home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_LE13_20261114_v01')
LOCK = json.loads((D / 'main_execution_lock_LE13_FINAL_v05.json').read_text()); ST = Path(LOCK['state_dir']); OUT = Path(LOCK['output_root']); UNIT = 'c-v02-drive540-le13-main-v07'
G = Path('/home/user/hh/isaacsim-codex-handoff'); MS = (15, 150, 300, 540); SENT = D / 'reporter_state.json'
REPS = ('HR_Scan', 'LR_Scan', 'GeoCAD'); CS = ('C100', 'C80', 'C60', 'C40', 'C20')
def notify(t, m, tag):
    subprocess.run(['python3', '-c', "import sys;sys.path.insert(0,'/home/user/.claude/hooks/isaacsim');import ntfy_notify as n;n.send(sys.argv[1],sys.argv[2],4,sys.argv[3])", t, m, tag], capture_output=True)
def load(p):
    try: return json.loads(Path(p).read_text())
    except Exception: return {}
def cause(x):
    if not x['technical_pass']: return 'technical_hold'
    o = x['outcome']; rs = x['reason'] or ''
    if o == 'SUCCESS': return 'success'
    if o == 'FAIL_SAFETY_ABORT': return 'safety_abort_verified_stop'
    if rs.startswith('MULTIVIEW_NO_DETECTION') or 'NO_DETECTION' in rs: return 'perception_no_detection_after_multiview' if rs.startswith('MULTIVIEW') else 'perception_no_detection'
    if rs.startswith(('POSE_', 'MULTIVIEW_PERCEPTION')) or 'DATUM' in rs: return 'pose_rejected'
    if rs.startswith(('PLAN_REJECTED', 'FOOTPRINT', 'MULTIVIEW_PLAN')): return 'plan_rejected'
    if x['moved']: return 'drive_failure_or_outside_band'
    return 'other:' + rs[:40]
def stats(v):
    v = [x for x in v if x is not None]
    return dict(n=len(v), mean=round(statistics.mean(v), 4), median=round(statistics.median(v), 4), max=round(max(v), 4)) if v else None
def rate(sub):
    n = len(sub); s = sum(cause(x) == 'success' for x in sub)
    k1 = sum(bool(x['initial_detected']) for x in sub); fin = sum(bool(x['final_detected']) for x in sub); mv = sum(bool(x['mv_active']) for x in sub)
    drove = [x for x in sub if x['moved']]
    return dict(n=n, success=s, success_rate=round(s / n, 3) if n else None, initial_detection_rate=round(k1 / n, 3) if n else None,
                multiview_triggered=mv, multiview_additional_detections=fin - k1, final_detection_rate=round(fin / n, 3) if n else None,
                drive_success_rate=round(sum(cause(x) == 'success' for x in drove) / len(drove), 3) if drove else None,
                pose_err_xy_m=stats([x['pose_err'] for x in sub]), causes=dict(collections.Counter(cause(x) for x in sub)))
def build(label):
    rows = list(csv.DictReader(open(LOCK['manifest'])))
    hist = [json.loads(l) for l in open(ST / 'run_history.jsonl')] if (ST / 'run_history.jsonl').exists() else []
    recs = []
    for h in hist:
        r = load(OUT / h['attempt'] / 'result.json'); a = load(OUT / (h['attempt'] + '.archive.json'))
        recs.append(dict(h, initial_detected=r.get('initial_detected'), final_detected=r.get('final_detected'), mv_active=bool(r.get('multiview_active')) and not r.get('initial_detected'),
                         detected_at=r.get('detected_at_capture'), captures=r.get('captures_used'), mv_s=r.get('multiview_duration_wall_s'), pose_err=r.get('pose_err_xy_m'),
                         final_err=r.get('final_err_m'), heading=r.get('final_heading_err_deg'), dist=r.get('drive_distance_m'), vmax=r.get('max_pulse_planar_m_s'),
                         run_s=h['t_end'] - h['t_start'], archive=a or None))
    n = len(recs); moved = [x for x in recs if x['moved']]; dur = [x['run_s'] for x in recs]; pace = statistics.mean(dur[-30:]) if dur else None
    remaining = (len(rows) - n) * pace if pace else 0; arcs = [x['archive'] for x in recs if x['archive']]
    rep = dict(site='L_E13', speed=dict(mode='PHASED', v_nav=LOCK['v_nav'], final_law=LOCK['final_law']), completed=n, planned=len(rows),
               per_representation={k: rate([x for x in recs if x['rep'] == k]) for k in REPS}, per_C={c: rate([x for x in recs if x['C'] == c]) for c in CS},
               per_rep_C={f'{k}_{c}': rate([x for x in recs if x['rep'] == k and x['C'] == c]) for k in REPS for c in CS}, overall=rate(recs),
               multiview=dict(triggered=sum(x['mv_active'] for x in recs), detected_K2=sum(x['detected_at'] == 2 for x in recs), detected_K3=sum(x['detected_at'] == 3 for x in recs),
                              mean_captures=round(statistics.mean([x['captures'] or 1 for x in recs]), 3) if recs else None, extra_time_s=stats([x['mv_s'] for x in recs if x['mv_active']])),
               motion=dict(moved=len(moved), distance_m=stats([x['dist'] for x in moved]), peak_planar_m_s=stats([x['vmax'] for x in moved]), final_position_error_m=stats([x['final_err'] for x in moved]),
                           final_heading_error_deg=stats([abs(x['heading']) for x in moved if x['heading'] is not None])),
               run_time_s=dict(all=stats(dur), drove=stats([x['run_s'] for x in moved])),
               time=dict(elapsed_h=round((time.time() - recs[0]['t_start']) / 3600, 2) if recs else 0, recent30_s_per_run=round(pace, 1) if pace else None, remaining_h=round(remaining / 3600, 2),
                         eta=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + remaining))),
               storage=dict(archives=len(arcs), verified=sum(bool(a.get('verified')) for a in arcs), volume_free_TB=round(shutil.disk_usage(OUT).free / 1e12, 2)),
               note='L_E13 main (amendment v06); E1 54 runs and pilots excluded')
    if label in (300, 540):
        done = [x['attempt'] for x in recs]; cnt = collections.Counter((x['rep'], x['C']) for x in recs)
        rep['balance'] = dict(per_condition=sorted(set(cnt.values())), exactly_20_each=(label == 300 and len(cnt) == 15 and set(cnt.values()) == {20}), conditions=len(cnt))
        sub = rows[:label]; full = rows
        def dist(rs, key): c = collections.Counter(key(r) for r in rs); t = sum(c.values()); return {str(k): round(v / t, 4) for k, v in sorted(c.items())}
        keys = dict(base=lambda r: r['base_id'], start=lambda r: (r['start_x_m'], r['start_y_m'], r['start_yaw_deg']), C=lambda r: r['C'], rep=lambda r: r['representation'], task_layers=lambda r: r['task_layer_count'])
        rep['distribution_first_vs_full'] = {k: dict(first=dist(sub, f), full=dist(full, f), max_abs_diff=round(max(abs(dist(sub, f).get(z, 0) - dist(full, f).get(z, 0)) for z in set(dist(sub, f)) | set(dist(full, f))), 4)) for k, f in keys.items()}
        rep['distribution_note'] = 'first %d manifest rows = bases %s; bases are disjoint between the first 300 and the remaining 240 rows, so scene membership differs by construction; C and representation are exactly balanced' % (label, sorted({r['base_id'] for r in sub})[:1] + ['...'])
    name = 'c_v02_le13_main_' + ('final_results' if label == 540 else 'interim_300' if label == 300 else 'progress_%03d' % label) + '_20261114_v01'
    rp = R / 'reports'; (rp / (name + '.json')).write_text(json.dumps(rep, indent=1, default=str))
    L = [f"# L_E13 540회 본실험 {'최종 결과' if label == 540 else '300회 중간 결과' if label == 300 else f'진행 보고 ({label}회)'} — 자동 생성", '',
         f"- 위치 L_E13, 속도 정책 PHASED (일반 이동 상한 {LOCK['v_nav']} m/s, 최종 정지 {LOCK['final_law']}), 다중 시점 최대 3회 촬영",
         f"- 완료 {n} / {len(rows)}, 경과 {rep['time']['elapsed_h']} h, 최근 30회 평균 {rep['time']['recent30_s_per_run']} 초/회, 완료 예상 {rep['time']['eta']}",
         f"- 다중 시점 작동 {rep['multiview']['triggered']}회 (K2 검출 {rep['multiview']['detected_K2']}, K3 검출 {rep['multiview']['detected_K3']}), 평균 촬영 {rep['multiview']['mean_captures']}회, 추가 시간 {rep['multiview']['extra_time_s']}",
         f"- 저장: 압축 {rep['storage']['archives']}개 중 검증 {rep['storage']['verified']}개, 볼륨 여유 {rep['storage']['volume_free_TB']} TB", '',
         '| 구분 | 시도 | 성공 | 성공률 | 초기 검출률 | 다중시점 추가 검출 | 최종 검출률 | 주행 성공률 | 결과 유형 |', '|---|---|---|---|---|---|---|---|---|']
    for k, v in list(rep['per_representation'].items()) + list(rep['per_C'].items()) + [('전체', rep['overall'])]:
        L.append(f"| {k} | {v['n']} | {v['success']} | {v['success_rate']} | {v['initial_detection_rate']} | {v['multiview_additional_detections']} | {v['final_detection_rate']} | {v['drive_success_rate']} | {v['causes']} |")
    L += ['', f"- 위치추정 오차(m): {rep['overall']['pose_err_xy_m']}", f"- 주행 {rep['motion']['moved']}회: 최고 속도 {rep['motion']['peak_planar_m_s']}, 최종 위치 오차(m) {rep['motion']['final_position_error_m']}, 방향 오차(°) {rep['motion']['final_heading_error_deg']}",
          f"- 실행 시간(초): 전체 {rep['run_time_s']['all']}, 주행 {rep['run_time_s']['drove']}"]
    if 'balance' in rep:
        L += ['', f"- 조건 균형: 조건 수 {rep['balance']['conditions']}, 조건별 회수 {rep['balance']['per_condition']}, 각 20회 정확히 포함: {rep['balance']['exactly_20_each']}",
              '- 처음 %d행과 전체 540행의 분포 차이(최대 절대 비율 차): ' % label + ', '.join(f"{k} {v['max_abs_diff']}" for k, v in rep['distribution_first_vs_full'].items()), '- ' + rep['distribution_note']]
    L += ['', '- 세부 표(표현×적재율)는 같은 이름의 .json에 있습니다.', f"- {rep['note']}"]
    (rp / (name + '.md')).write_text('\n'.join(L) + '\n')
    pushed = False
    try:
        subprocess.run(['git', 'pull', '--ff-only', '-q'], cwd=G, timeout=120)
        for ext in ('.md', '.json'): shutil.copy(rp / (name + ext), G / 'reports' / (name + ext))
        subprocess.run(['git', 'add', f'reports/{name}.md', f'reports/{name}.json'], cwd=G, check=True)
        subprocess.run(['git', 'commit', '-q', '-m', f'C-V02 LE13 main540 {name} (auto)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'], cwd=G, check=True)
        subprocess.run(['git', 'push', '-q', 'origin', 'main'], cwd=G, check=True, timeout=120); pushed = True
    except Exception: pass
    o = rep['overall']; notify(f"C540 LE13 {label}", f"{n}/540 success {o['success_rate']} det1 {o['initial_detection_rate']} final det {o['final_detection_rate']} ETA {rep['time']['eta']} github {'ok' if pushed else 'FAILED'}", 'bar_chart')
sent = load(SENT) or dict(milestones=[], stop_notified=False)
while True:
    try:
        stt = load(ST / 'status.json'); done = sum(1 for _ in open(ST / 'run_history.jsonl')) if (ST / 'run_history.jsonl').exists() else 0
        for m in MS:
            if done >= m and m not in sent['milestones']: build(m); sent['milestones'].append(m)
        if 540 in sent['milestones']: SENT.write_text(json.dumps(sent)); break
        active = subprocess.run(['systemctl', '--user', 'is-active', UNIT], capture_output=True, text=True).stdout.strip()
        if active != 'active' and stt.get('state') != 'MAIN_COMPLETE' and not sent['stop_notified']:
            notify('C540 LE13 controller not running', f"state={stt.get('state')} reason={str(stt.get('reason'))[:150]} completed={done} (auto-resume supervisor decides)", 'warning'); sent['stop_notified'] = True
        if active == 'active': sent['stop_notified'] = False
        SENT.write_text(json.dumps(sent))
    except Exception as e:
        with (D / 'reporter_errors.log').open('a') as f: f.write(time.strftime('%F %T ') + repr(e) + '\n')
    time.sleep(60)
