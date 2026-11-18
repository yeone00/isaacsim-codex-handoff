"""C540 E1 main unattended reporter / passive watchdog (v01, 2026-11-14). Starts no GPU job and changes nothing in the experiment.
Every 60 s: reads <W>/main_started.json (written by the autostart), the controller state dir and the systemd unit state.
 - at completed >= 30/100/180/270/360/450/540: builds a progress report (main runs only, technical pilots excluded) -> reports/*.md + *.json,
   commits ONLY those files to the handoff repo and pushes (no force), ntfy;
 - if the controller unit is no longer active and status != MAIN_COMPLETE: ntfy once with the HOLD/stop reason (controller already sends HOLD);
 - after 540: final report (per representation / C success, failure types, run time, position/heading error), push, exit."""
import json, time, subprocess, statistics, collections, csv, shutil
from pathlib import Path
R = Path('/home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013'); W = Path('/home/user/hh/isaac_cosmos/sdg_final/C_V02_SPEED_CANDIDATES_20261114_v01')
G = Path('/home/user/hh/isaacsim-codex-handoff'); MS = (30, 100, 180, 270, 360, 450, 540); SENT = W / 'reporter_state.json'
def notify(t, m, tag):
    subprocess.run(['python3', '-c', "import sys;sys.path.insert(0,'/home/user/.claude/hooks/isaacsim');import ntfy_notify as n;n.send(sys.argv[1],sys.argv[2],4,sys.argv[3])", t, m, tag], capture_output=True)
def cause(x):
    if not x.get('technical_pass', True): return 'technical_hold'
    o = x['outcome']; rs = x['reason']
    if o == 'SUCCESS': return 'success'
    if o == 'FAIL_SAFETY_ABORT': return 'safety_abort_verified_stop'
    if 'NO_DETECTION' in rs: return 'perception_no_detection'
    if rs.startswith('POSE_') or 'DATUM' in rs: return 'pose_rejected'
    if rs.startswith(('PLAN_REJECTED', 'FOOTPRINT')): return 'plan_rejected'
    if x.get('moved'): return 'drive_failure_or_outside_band'
    return 'other:' + rs[:40]
def stats(v): return dict(n=len(v), mean=round(statistics.mean(v), 4), median=round(statistics.median(v), 4), max=round(max(v), 4)) if v else None
def build(info, label, final=False):
    lock = json.loads(Path(info['lock']).read_text()); ST = Path(info['state_dir']); OUT = Path(info['output_root'])
    hist = [json.loads(l) for l in open(ST / 'run_history.jsonl')] if (ST / 'run_history.jsonl').exists() else []
    recs = []
    for h in hist:
        run = OUT / h['attempt']; r = json.loads((run / 'result.json').read_text()) if (run / 'result.json').exists() else {}
        ar = run.parent / (run.name + '.archive.json'); a = json.loads(ar.read_text()) if ar.exists() else None
        recs.append(dict(h, final_err_m=r.get('final_err_m'), heading=r.get('final_heading_err_deg'), dist=r.get('drive_distance_m'), band=r.get('band_main'), run_s=h['t_end'] - h['t_start'], archive=a))
    def rate(sub): n = len(sub); s = sum(cause(x) == 'success' for x in sub); return dict(n=n, success=s, success_rate=round(s / n, 3) if n else None, causes=dict(collections.Counter(cause(x) for x in sub)))
    moved = [x for x in recs if x['moved']]; dur = [x['run_s'] for x in recs]; pace = statistics.mean(dur[-30:]) if dur else None; remaining = (lock['rows'] - len(recs)) * pace if pace else 0
    arcs = [x['archive'] for x in recs if x['archive']]
    rep = {'cruise_m_s': lock.get('cruise_m_s', .02), 'completed': len(recs), 'remaining': lock['rows'] - len(recs),
           'per_representation': {k: rate([x for x in recs if x['rep'] == k]) for k in ('HR_Scan', 'LR_Scan', 'GeoCAD')},
           'per_C': {c: rate([x for x in recs if x['C'] == c]) for c in ('C100', 'C80', 'C60', 'C40', 'C20')},
           'per_rep_C': {f'{k}_{c}': rate([x for x in recs if x['rep'] == k and x['C'] == c]) for k in ('HR_Scan', 'LR_Scan', 'GeoCAD') for c in ('C100', 'C80', 'C60', 'C40', 'C20')},
           'causes': dict(collections.Counter(cause(x) for x in recs)),
           'motion': dict(moved=len(moved), distance_m=stats([x['dist'] for x in moved if x['dist']]), final_position_error_m=stats([x['final_err_m'] for x in moved if x['final_err_m'] is not None]),
                          final_heading_error_deg=stats([abs(x['heading']) for x in moved if x['heading'] is not None]), within_main_band=sum(bool(x['band']) for x in moved)),
           'run_time_s': dict(all=stats(dur), drove=stats([x['run_s'] for x in moved]), not_moved=stats([x['run_s'] for x in recs if not x['moved']])),
           'time': dict(elapsed_h=round((time.time() - recs[0]['t_start']) / 3600, 2) if recs else 0, busy_h=round(sum(dur) / 3600, 2), recent30_s_per_run=round(pace, 1) if pace else None,
                        remaining_h=round(remaining / 3600, 2), eta=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + remaining))),
           'storage': dict(archives=len(arcs), verified=sum(bool(a['verified']) for a in arcs), original_GB=round(sum(a['original_bytes'] for a in arcs) / 1e9, 2), archive_GB=round(sum(a['bytes'] for a in arcs) / 1e9, 2),
                           volume_free_TB=round(shutil.disk_usage(OUT).free / 1e12, 2)),
           'note': 'main E1 runs only (amendment v05, new output); technical pilots and the 11 preliminary v03 runs are excluded'}
    name = f"c_v02_drive540_main_{'final_results' if final else 'progress_%03d' % label}_20261114_v01"
    rp = R / 'reports'; (rp / (name + '.json')).write_text(json.dumps(rep, indent=1, default=str))
    L = [f"# E1 540회 본실험 {'최종 결과' if final else f'중간 보고 ({label}회)'} — 자동 생성", '',
         f"- 순항 속도 {rep['cruise_m_s']} m/s, 완료 {rep['completed']} / 남음 {rep['remaining']}",
         f"- 경과 {rep['time']['elapsed_h']} h, 최근 30회 평균 {rep['time']['recent30_s_per_run']} 초/회, 남은 예상 {rep['time']['remaining_h']} h (완료 예상 {rep['time']['eta']})",
         f"- 저장: 압축 {rep['storage']['archives']}개 중 검증 {rep['storage']['verified']}개, 원본 {rep['storage']['original_GB']} GB → 압축 {rep['storage']['archive_GB']} GB, 볼륨 여유 {rep['storage']['volume_free_TB']} TB", '',
         '| 표현 | 시도 | 성공 | 성공률 | 결과 유형 |', '|---|---|---|---|---|']
    for k, v in rep['per_representation'].items(): L.append(f"| {k} | {v['n']} | {v['success']} | {v['success_rate']} | {v['causes']} |")
    L += ['', '| 적재율 | 시도 | 성공 | 성공률 | 결과 유형 |', '|---|---|---|---|---|']
    for k, v in rep['per_C'].items(): L.append(f"| {k} | {v['n']} | {v['success']} | {v['success_rate']} | {v['causes']} |")
    L += ['', f"- 결과 유형 전체: {rep['causes']}", f"- 주행 {rep['motion']['moved']}회: 거리 {rep['motion']['distance_m']}, 최종 위치 오차(m) {rep['motion']['final_position_error_m']}, 방향 오차(°) {rep['motion']['final_heading_error_deg']}, MAIN band 이내 {rep['motion']['within_main_band']}",
          f"- 실행 시간(초): 전체 {rep['run_time_s']['all']}, 주행 {rep['run_time_s']['drove']}, 미주행 {rep['run_time_s']['not_moved']}", '', f"- {rep['note']}"]
    (rp / (name + '.md')).write_text('\n'.join(L) + '\n')
    try:
        subprocess.run(['git', 'pull', '--ff-only', '-q'], cwd=G, timeout=120)
        for ext in ('.md', '.json'): shutil.copy(rp / (name + ext), G / 'reports' / (name + ext))
        subprocess.run(['git', 'add', f'reports/{name}.md', f'reports/{name}.json'], cwd=G, check=True)
        subprocess.run(['git', 'commit', '-q', '-m', f'C-V02 E1 main540 {"final results" if final else "progress %d" % label} (auto)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'], cwd=G, check=True)
        subprocess.run(['git', 'push', '-q', 'origin', 'main'], cwd=G, check=True, timeout=120); pushed = True
    except Exception: pushed = False
    notify(f"C540 main {'FINAL' if final else label}", f"{rep['completed']}/540, causes {rep['causes']}, ETA {rep['time']['eta']}, github {'ok' if pushed else 'FAILED'}", 'bar_chart')
    return pushed
sent = json.loads(SENT.read_text()) if SENT.exists() else dict(milestones=[], stop_notified=False, final=False)
while True:
    try:
        if (W / 'main_started.json').exists():
            info = json.loads((W / 'main_started.json').read_text()); ST = Path(info['state_dir'])
            stt = json.loads((ST / 'status.json').read_text()) if (ST / 'status.json').exists() else {}
            done = sum(1 for _ in open(ST / 'run_history.jsonl')) if (ST / 'run_history.jsonl').exists() else 0
            for m in MS[:-1]:
                if done >= m and m not in sent['milestones']: build(info, m); sent['milestones'].append(m)
            if stt.get('state') == 'MAIN_COMPLETE' and not sent['final']:
                build(info, 540, final=True); sent['final'] = True; SENT.write_text(json.dumps(sent)); break
            active = subprocess.run(['systemctl', '--user', 'is-active', info['unit']], capture_output=True, text=True).stdout.strip()
            if active != 'active' and stt.get('state') != 'MAIN_COMPLETE' and not sent['stop_notified']:
                notify('C540 main controller stopped', f"state={stt.get('state')} reason={str(stt.get('reason'))[:150]} completed={done}", 'warning'); sent['stop_notified'] = True
            SENT.write_text(json.dumps(sent))
    except Exception as e:
        (W / 'reporter_errors.log').open('a').write(time.strftime('%F %T ') + repr(e) + '\n')
    time.sleep(60)
