"""Read-only byte/inode/hash/log/gzip-roundtrip audit. Writes new CSV/JSON only. Never changes source results."""
from pathlib import Path
import sys,json,csv,os,hashlib,zlib,time,collections,re,statistics,datetime
R=Path(__file__).resolve().parents[1];D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');O=R/'reports/c_v02_drive540_storage_curvature_audit_20261113_v01';O.mkdir(exist_ok=False)
def csvout(name,rows):
 rows=list(rows)
 if not rows:return
 keys=list(dict.fromkeys(k for x in rows for k in x))
 with (O/name).open('x',newline='') as f:w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
def category(p):
 n=p.name;s=str(p)
 if 'executed_code' in p.parts:return 'code_snapshots'
 if n in ['drive_contract.json','expected_graph.json','run_spec.json','runner_status.json','result.json']:return 'run_provenance_results'
 if n=='runtime.log':return 'simulator_console_log'
 if n=='contacts.json':return 'physics_contact_points'
 if 'endpoint_forensics' in n:return 'endpoint_forensics'
 if n in ['steps.jsonl','feedback.json']:return 'robot_state_trace'
 if 'timing' in n:return 'timing_forensics'
 if n in ['physics_steps.jsonl']:return 'physics_step_trace'
 if n.startswith('leg_') and ('swept' in n or 'support' in n or 'path' in n):return 'planner_path_sweep_support'
 if n=='adapter_commands.jsonl':return 'controller_command_trace'
 if n.startswith('ros_') or n.startswith('driver_') or 'observer' in n:return 'ROS_driver_observer'
 if p.suffix.lower() in ['.jpg','.jpeg']:return 'motion_JPEG_frames'
 if p.suffix.lower()=='.mp4':return 'derived_MP4'
 if n=='front_depth.npy':return 'initial_depth'
 if n.startswith('front_rgb.'):return 'initial_RGB'
 if p.suffix.lower()=='.npy' and any(x in n for x in ['mask','roi']):return 'predicted_masks_ROI'
 if any(x in n for x in ['camera','calibration','capture']):return 'camera_capture_evidence'
 if p.suffix.lower() in ['.png','.jpg']:return 'derived_overlay_or_image'
 return 'other_required_audit'
prior=json.loads((D/'technical_e2e_v03/pilot_records.json').read_text());runs=[dict(run_id=x['attempt_id'],role='scientific_pilot',path=Path(x['run_dir']),outcome=x['assessment']['scientific_outcome']) for x in prior];eng=D/'technical_e2e_v03/engineering/ENGINEERING_HISTORICAL_ROUTE_HR_C100';runs.append(dict(run_id=eng.name,role='engineering_motion_proxy_not_E2E_success',path=eng,outcome='ENGINEERING_CONTROL_PASS'))
files=[];sha_groups=collections.defaultdict(list);runstats=[];start=time.time()
for run in runs:
 root=run['path'];rr=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  st=p.stat();h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  after=p.stat();assert (st.st_size,st.st_mtime_ns)==(after.st_size,after.st_mtime_ns),'SOURCE_CHANGED_DURING_READ:'+str(p)
  row=dict(run_id=run['run_id'],role=run['role'],outcome=run['outcome'],relative_path=str(p.relative_to(root)),source_path=str(p),category=category(p),bytes=st.st_size,allocated_bytes=st.st_blocks*512,MB_decimal=st.st_size/1e6,MiB=st.st_size/2**20,sha256=h.hexdigest(),device=st.st_dev,inode=st.st_ino,mtime_ns=st.st_mtime_ns);files.append(row);rr.append(row);sha_groups[(st.st_size,h.hexdigest())].append(row)
 total=sum(x['bytes'] for x in rr);unique_inode=sum(v['bytes'] for v in {(x['device'],x['inode']):x for x in rr}.values());result=json.loads((root/'result.json').read_text());runner=json.loads((root/'runner_status.json').read_text());rt=json.loads((root/'attempt_0001/runtime_summary.json').read_text());runstats.append(dict(run_id=run['run_id'],role=run['role'],outcome=run['outcome'],bytes=total,MB_decimal=total/1e6,MiB=total/2**20,unique_inode_bytes=unique_inode,allocated_bytes=sum(x['allocated_bytes'] for x in rr),files=len(rr),runner_wall_seconds=runner.get('wall_s'),drive_sim_seconds=result.get('drive_sim_s'),physics_sim_seconds=rt.get('physics_sim_s'),nonzero_commands=rt.get('nonzero_commands'),JPEG_frames=len(list((root/'attempt_0001/rec_robotcam').glob('*.jpg')))))
 print(run['run_id'],total,flush=True)
csvout('storage_files_16_runs.csv',files);csvout('storage_runs.csv',runstats)
agg=[]
for role in ['engineering_motion_proxy_not_E2E_success','scientific_pilot']:
 selected=[x for x in files if x['role']==role];total=sum(x['bytes'] for x in selected)
 for cat in sorted({x['category'] for x in selected}):
  a=[x for x in selected if x['category']==cat];b=sum(x['bytes'] for x in a);agg.append(dict(role=role,category=cat,files=len(a),bytes=b,MB_decimal=b/1e6,percent=b/total*100))
csvout('storage_category_totals.csv',agg)
dirs=collections.defaultdict(lambda:[0,0])
for x in files:
 if x['role']!='engineering_motion_proxy_not_E2E_success':continue
 rel=Path(x['relative_path']);key=str(rel.parent);dirs[key][0]+=x['bytes'];dirs[key][1]+=1
a=[dict(directory=k,files=v[1],bytes=v[0],MB_decimal=v[0]/1e6) for k,v in dirs.items()];csvout('engineering_directory_totals.csv',sorted(a,key=lambda x:-x['bytes']))
dup=[]
for (size,h),a in sha_groups.items():
 if len(a)>1:dup.append(dict(bytes_per_copy=size,sha256=h,copies=len(a),avoidable_duplicate_bytes_if_shared_immutable=(len(a)-1)*size,paths=json.dumps([x['source_path'] for x in a])))
csvout('exact_byte_duplicate_groups.csv',sorted(dup,key=lambda x:-x['avoidable_duplicate_bytes_if_shared_immutable']))
# Byte-exact gzip feasibility tests, in RAM streams only; do not produce/delete source archives.
compression=[]
for x in [r for r in files if r['role']=='engineering_motion_proxy_not_E2E_success']:
 p=Path(x['source_path']);st=p.stat()
 for level in [1,6]:
  compressor=zlib.compressobj(level,zlib.DEFLATED,31);decompressor=zlib.decompressobj(31);original=hashlib.sha256();roundtrip=hashlib.sha256();compressed=0;t=time.monotonic()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):
    original.update(b);c=compressor.compress(b);compressed+=len(c)
    if c:roundtrip.update(decompressor.decompress(c))
  c=compressor.flush();compressed+=len(c);roundtrip.update(decompressor.decompress(c));roundtrip.update(decompressor.flush());assert original.digest()==roundtrip.digest() and original.hexdigest()==x['sha256'];assert (st.st_size,st.st_mtime_ns)==(p.stat().st_size,p.stat().st_mtime_ns)
  compression.append(dict(relative_path=x['relative_path'],category=x['category'],bytes=x['bytes'],gzip_level=level,gzip_bytes=compressed,ratio=compressed/x['bytes'] if x['bytes'] else None,bytes_saved=x['bytes']-compressed,CPU_seconds=time.monotonic()-t,roundtrip_SHA256_PASS=True,original_unchanged=True))
csvout('lossless_gzip_stream_benchmarks.csv',compression)
# Repeated console messages: byte redundancy vs timestamped scientific data are distinguished.
log=eng/'runtime.log';counts=collections.Counter();bytecounts=collections.Counter();line_count=0
with log.open(errors='replace') as f:
 for line in f:
  line_count+=1
  if 'PxShape::getMaterialFromInternalFaceIndex' in line:key='PhysX_PxShape_getMaterialFromInternalFaceIndex_warning'
  elif 'relationship target' in line and 'cameraPrim' in line:key='legacy_disabled_cameraPrim_out_of_reference_warning'
  else:key='OTHER'
  counts[key]+=1;bytecounts[key]+=len(line.encode())
csvout('engineering_console_message_categories.csv',[dict(message=k,lines=v,approx_bytes=bytecounts[k],all_lines=line_count) for k,v in counts.items()])
# Verify logical overlap of latest feedback and final step, without discarding either.
last=None
with (eng/'attempt_0001/steps.jsonl').open() as f:
 for l in f:
  if l.strip():last=json.loads(l)
feedback=json.loads((eng/'attempt_0001/feedback.json').read_text());logical=dict(feedback_exactly_equals_final_step=feedback==last,note='latest snapshot duplicates one record, not the entire time history; both live consumers and offline validators use these paths')
# Outcome-stratified observations and conditional forecasts; no E2E success or motion-failure sample exists yet.
no=[r for r in runstats if r['outcome']=='FAIL_A'];rej=[r for r in runstats if r['outcome']=='FAIL_C'];motion=next(r for r in runstats if r['role']=='engineering_motion_proxy_not_E2E_success');M=motion['bytes'];A=statistics.mean(x['bytes'] for x in no);C=statistics.mean(x['bytes'] for x in rej);fixed=statistics.mean(x['bytes'] for x in runstats if x['role']=='scientific_pilot');dynamic=max(0,M-fixed);scenarios=[]
def scen(name,n_success,n_no,n_rej,n_fail,fail_fraction=1.):
 assert n_success+n_no+n_rej+n_fail==540;fail=fixed+fail_fraction*dynamic;total=n_success*M+n_no*A+n_rej*C+n_fail*fail;scenarios.append(dict(scenario=name,success_proxy_count=n_success,no_detection_count=n_no,path_reject_count=n_rej,motion_failure_proxy_count=n_fail,motion_failure_duration_fraction_of_proxy=fail_fraction,raw_bytes=total,raw_GB_decimal=total/1e9,raw_GiB=total/2**30,with_25GiB_margin_bytes=total+25*2**30,with_25GiB_margin_GB_decimal=(total+25*2**30)/1e9,not_a_prediction_of_success_rate=True,success_storage_is_engineering_proxy_not_observed_E2E_success=True,motion_failure_storage_is_unobserved_duration_model=True))
scen('all540_full_motion_proxy_conservative_budget',540,0,0,0);scen('all540_no_detection_conditional',0,540,0,0);scen('all540_path_rejection_conditional',0,0,540,0);scen('repeat_observed_Base01_mix_NOT_FORECAST',0,180,360,0);scen('illustrative_mixed_270_motion_90_each_failure_type',270,90,90,90,.5)
for frac in [.25,.5,1.,2.]:scen('all540_motion_failure_duration_model_'+str(frac),0,0,0,540,frac)
csvout('storage_540_conditional_scenarios.csv',scenarios)
# Per-outcome size summaries.
outcomes=[dict(outcome='NO_DETECTION',measured_n=len(no),mean_bytes=A,min_bytes=min(r['bytes'] for r in no),max_bytes=max(r['bytes'] for r in no),evidence='actual full pilots, one shared Base01'),dict(outcome='PATH_REJECT',measured_n=len(rej),mean_bytes=C,min_bytes=min(r['bytes'] for r in rej),max_bytes=max(r['bytes'] for r in rej),evidence='actual full pilots, one shared Base01'),dict(outcome='SUCCESSFUL_FULL_E2E',measured_n=0,mean_bytes=None,min_bytes=None,max_bytes=None,evidence='NOT_OBSERVED; engineering control storage surrogate '+str(M)+' bytes'),dict(outcome='MOTION_FAILURE',measured_n=0,mean_bytes=None,min_bytes=None,max_bytes=None,evidence='NOT_OBSERVED; duration scenarios only')];csvout('storage_outcome_evidence.csv',outcomes)
# Derived video was generated once outside the motion run; do not add it to the historical417GB twice.
visual=[dict(path=str(p),bytes=p.stat().st_size,category=category(p)) for p in (D/'visual_evidence_v01').glob('*') if p.is_file()];csvout('derived_video_and_visuals_outside_original_run.csv',visual)
# Current format paths are mandatory; compression test is a proposal, not applied.
summary=dict(state='READ_ONLY_STORAGE_AUDIT_COMPLETED',created=datetime.datetime.now().astimezone().isoformat(),files=len(files),engineering_bytes=M,engineering_MB_decimal=M/1e6,engineering_MiB=M/2**20,no_detection_mean_bytes=A,path_reject_mean_bytes=C,old_projection_bytes=M*540+25*2**30,old_projection_GB_decimal=(M*540+25*2**30)/1e9,old_projection_GiB=(M*540+25*2**30)/2**30,engineer_unique_inode_bytes=motion['unique_inode_bytes'],exact_duplicates_all_16_avoidable_bytes=sum(x['avoidable_duplicate_bytes_if_shared_immutable'] for x in dup),gzip_engineering=[dict(level=l,bytes=sum(x['gzip_bytes'] for x in compression if x['gzip_level']==l),saved_bytes=sum(x['bytes_saved'] for x in compression if x['gzip_level']==l),CPU_seconds=sum(x['CPU_seconds'] for x in compression if x['gzip_level']==l),all540_with_25GiB_GB=(sum(x['gzip_bytes'] for x in compression if x['gzip_level']==l)*540+25*2**30)/1e9) for l in [1,6]],logical_overlap=logical,sources_modified=False,source_file_hashes_and_mtime_checked=True,compression_applied=False,GPU_execution=0,new_motion=0,elapsed_seconds=time.time()-start)
(O/'storage_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
