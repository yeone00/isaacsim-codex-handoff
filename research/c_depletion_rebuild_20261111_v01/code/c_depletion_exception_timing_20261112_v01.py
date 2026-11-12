"""Refine UTC second precision with monotonic millisecond log times; CPU only."""
from pathlib import Path
import json,re,datetime,bisect,collections,time
E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');O=E/'replicator_exception_timing_v01';O.mkdir(exist_ok=False);rows=[];bounds=[]
pat=re.compile(r'^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) \[([\d,]+)ms\]')
for p in sorted((E/'logs').glob('capture_*.log')):
 parsed=[]
 for line in p.read_text(errors='replace').splitlines():
  m=pat.match(line)
  if not m:continue
  t=datetime.datetime.fromisoformat(m[1].replace('Z','+00:00')).timestamp();u=int(m[2].replace(',',''))/1000;parsed.append((t,u,line))
 lo=max(t-u for t,u,line in parsed);hi=min(t+1-u for t,u,line in parsed);assert hi>=lo,'Inconsistent wall vs monotonic clock';origin=(lo+hi)/2
 bounds.append(dict(log=p.name,origin_low=lo,origin_high=hi,uncertainty_seconds=hi-lo))
 A=E/'production'/p.stem;ev=[json.loads(x) for x in (A/'events.jsonl').read_text().splitlines()];starts=[x for x in ev if x['state']=='SCENE_STARTED'];beg=[x['time'] for x in starts]
 for t,u,line in parsed:
  if 'Assertion raised in compute - setting an array element with a sequence.' not in line:continue
  at=origin+u;i=bisect.bisect_right(beg,at)-1;sid=starts[i]['scene_id'] if i>=0 else None
  if sid:
   rgb=A/'rgb'/f'{sid}.png';act=A/'masks_actual'/f'{sid}_Load_01.png';can=A/'masks_canonical'/f'{sid}_Load_01.png';dep=A/'depth'/f'{sid}.npy'
   phase='before_actual_mask_file' if at<act.stat().st_mtime else 'after_actual_mask_before_RGB_file' if at<rgb.stat().st_mtime else 'after_RGB_before_canonical_file' if at<can.stat().st_mtime else 'after_canonical_file'
   # State transition/capture subframes not logged; phase uses file-write times, not exact render stage.
   rr=dict(log=p.name,scene_id=sid,time_estimate=at,time_uncertainty_s=hi-lo,phase_by_file_writes=phase,delta_to_rgb_file_s=at-rgb.stat().st_mtime,delta_to_depth_file_s=at-dep.stat().st_mtime,delta_to_canonical_file_s=at-can.stat().st_mtime)
  else:rr=dict(log=p.name,scene_id=None,time_estimate=at,time_uncertainty_s=hi-lo,phase_by_file_writes='startup')
  rows.append(rr)
with (O/'timing.jsonl').open('x') as f:
 for r in rows:f.write(json.dumps(r)+'\n')
c=collections.Counter((r['log'],r['scene_id']) for r in rows)
d=dict(state='TIMING_RECONSTRUCTION_COMPLETED',exceptions=len(rows),per_scene_exception_count_histogram=dict(collections.Counter(c.values())),phase_by_file_writes=dict(collections.Counter(r['phase_by_file_writes'] for r in rows)),max_time_uncertainty_s=max(x['uncertainty_seconds'] for x in bounds),bounds=bounds,limitation='Clock interval inferred from whole-second wall stamps and millisecond elapsed; no raw render frame IDs or output-buffer generation IDs. File write sequence does not establish exact render stage or buffer freshness.')
(O/'result.json').write_text(json.dumps(d,indent=2));print(json.dumps({k:v for k,v in d.items() if k!='bounds'},indent=2))
