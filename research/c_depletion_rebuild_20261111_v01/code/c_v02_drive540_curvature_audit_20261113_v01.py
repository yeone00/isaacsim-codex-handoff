"""Read-only CPU diagnostic. No runtime targets/settings changed. Nominal goals are evaluation-only."""
import csv,json,math,hashlib,importlib.util,pathlib
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1];O=R/'reports/c_v02_drive540_storage_curvature_audit_20261113_v01';D=pathlib.Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01')
src=R/'analysis/stage3_local_planner_20261109_v01.py';sp=importlib.util.spec_from_file_location('safe_pure_math_planner',src);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def write(name,rows):
 with open(O/name,'x',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def geometry(start,goal):
 s,a=m.rear_pose(start);g,b=m.rear_pose(goal);v=g-s
 return float(v@[math.cos(a),math.sin(a)]),float(v@[-math.sin(a),math.cos(a)]),m.wrap(b-a)
def envelope(X,delta,K):
 u=math.sin(delta)
 if X<=0 or abs(delta)>=math.pi/2 or abs(u)>K*X:return None
 lo=-(K*X-u)/2;hi=(K*X+u)/2
 F=lambda q:-math.sqrt(max(0,1-q*q))
 lower=-math.inf if lo<=-1 else (F(lo)-F(0))/(-K)+(F(u)-F(lo))/K
 upper=math.inf if hi>=1 else (F(hi)-F(0))/K+(F(u)-F(hi))/(-K)
 return lower,upper

def bound(start,goal):
 X,Y,d=geometry(start,goal)
 def feasible(k):
  z=envelope(X,d,k);return z is not None and z[0]-1e-12<=Y<=z[1]+1e-12
 lo=0.;hi=100.
 if not feasible(hi):return dict(X=X,Y=Y,delta_deg=math.degrees(d),necessary_k=None,necessary_bound_exceeds_limit=None)
 for _ in range(70):
  mid=(lo+hi)/2
  if feasible(mid):hi=mid
  else:lo=mid
 e=envelope(X,d,m.LIMIT)
 return dict(X=X,Y=Y,delta_deg=math.degrees(d),necessary_k=hi,necessary_bound_exceeds_limit=hi>m.LIMIT+1e-8,allowed_Y_min=None if e is None else e[0],allowed_Y_max=None if e is None else e[1])
# Independent numerical check of exact envelope integral and parallel closed-form.
checks=[]
for X,delta,K in [(.6,.07,.363645),(1.,0.,.363645),(1.,-.07,.4)]:
 e=envelope(X,delta,K);x=np.linspace(0,X,100001);u=math.sin(delta)
 l=np.maximum(-K*x,u-K*(X-x));h=np.minimum(K*x,u+K*(X-x))
 vals=[float(np.trapezoid(z/np.sqrt(1-z*z),x)) for z in (l,h)]
 assert max(abs(e[i]-vals[i]) for i in (0,1))<1e-8
 checks.append(dict(test='analytic_envelope_vs_numeric',X=X,delta=delta,error=max(abs(e[i]-vals[i]) for i in (0,1))))
start=(0.,0.,0.);goal=(1.,.05,0.);b=bound(start,goal);closed=2*math.sin(2*math.atan2(.05,1))/1
assert abs(b['necessary_k']-closed)<1e-8
checks.append(dict(test='parallel_closed_form',error=abs(b['necessary_k']-closed)))
trials=[]
def scan(start,goal,label):
 best=None;passed=0
 for rho in m.RHO_GRID:
  row=dict(case=label,rho=rho,peak_k=None,rate_deg_s=None,accepted=False,error='')
  try:
   p,meta=m.primitive(start,goal,rho);peak=float(np.max(np.abs(p[:,3])));rate=m.feedforward_steer_rate(p)
   row.update(peak_k=peak,rate_deg_s=rate,accepted=peak<=m.LIMIT and rate<=m.RATE_CAP_DEG_S)
   if row['accepted']:passed+=1
   if best is None or peak<best[0]:best=(peak,rate,rho,p)
  except ValueError as e:row['error']=str(e)
  trials.append(row)
 return dict(candidate_min_peak_k=None if best is None else best[0],candidate_rate_at_min_peak=None if best is None else best[1],best_rho=None if best is None else best[2],accepted_candidates=passed),best
records=json.load(open(D/'technical_e2e_v03/pilot_records.json'));actual=[];biases=[]
nominal=(-25.888,30.509);preoffset=2.203745031260775
for r in records:
 if 'CURVATURE_INFEASIBLE' not in r['assessment']['reason']:continue
 p=pathlib.Path(r['run_dir'])/'attempt_0001';rej=json.load(open(p/'leg_0_plan_rejected.json'));pred=json.load(open(p/'predicted_pre_final.json'));t=pred['targets'];pose=pred['pose']
 st=(rej['start'][0],rej['start'][1],rej['start'][3]);go=(t['pre_x_m'],t['pre_y_m'],math.radians(t['yaw_deg']));ideal=(nominal[0],nominal[1]-preoffset,go[2]);metrics,best=scan(st,go,r['attempt_id']);bb=bound(st,go);nb=bound(st,ideal)
 row=dict(attempt_id=r['attempt_id'],representation=r['attempt_id'].split('_',4)[3] if False else ('GeoCAD' if 'GeoCAD' in r['attempt_id'] else 'LR_Scan' if 'LR_Scan' in r['attempt_id'] else 'HR_Scan'),C=r['attempt_id'].split('_')[2],start_x=st[0],start_y=st[1],start_yaw_deg=math.degrees(st[2]),detected=True,pose_computed=True,estimated_center_x=pose['center_x_m'],estimated_center_y=pose['center_y_m'],estimated_load_heading_deg=pose['heading_deg_180'],pre_x=go[0],pre_y=go[1],final_x=t['final_x_m'],final_y=t['final_y_m'],goal_yaw_deg=t['yaw_deg'],nominal_center_error_m=math.hypot(pose['center_x_m']-nominal[0],pose['center_y_m']-nominal[1]),limit_k=m.LIMIT,baseline_quintic_peak_k=rej['baseline_peak']['peak_abs_k'],**metrics,**bb,nominal_goal_necessary_k=nb['necessary_k'],nominal_goal_bound_exceeds_limit=nb['necessary_bound_exceeds_limit'],datum=pose['datum'],run_dir=str(p),rejection_sha256=hashlib.sha256((p/'leg_0_plan_rejected.json').read_bytes()).hexdigest())
 actual.append(row);biases.append((r['attempt_id'],pose['center_x_m']-nominal[0],pose['center_y_m']-nominal[1]))
 if best:
  write('rejected_candidate_'+r['attempt_id']+'.csv',[dict(x=float(q[0]),y=float(q[1]),yaw=float(q[2]),k=float(q[3]),s=float(q[4]),admitted=False) for q in best[3][::4]])
manifest=list(csv.DictReader(open(D/'single_load_amendment_v01/attempt_manifest.csv')));bases={r['base_id']:r for r in manifest};baseout=[];sensitivity=[]
for bid,r in sorted(bases.items()):
 st=(float(r['start_x_m']),float(r['start_y_m']),math.radians(float(r['start_yaw_deg'])));go=(nominal[0],nominal[1]-preoffset,math.pi/2);metrics,_=scan(st,go,bid+'_ZERO_POSE_ERROR_DIAGNOSTIC');bb=bound(st,go)
 baseout.append(dict(base_id=bid,source_family=r['source_family'],start_x=st[0],start_y=st[1],start_yaw_deg=math.degrees(st[2]),**metrics,**bb,scope='nominal goal offline geometry only; not E2E outcome'))
 for case,dx,dy in biases:
  b=bound(st,(go[0]+dx,go[1]+dy,go[2]));sensitivity.append(dict(base_id=bid,transferred_bias_case=case,**b,scope='conditional bias transfer; actual observations unavailable'))
write('curvature_rejections_10.csv',actual);write('curvature_candidates_1104.csv',trials);write('base36_nominal_geometry.csv',baseout);write('base36_conditional_bias_sensitivity.csv',sensitivity)
summary=dict(actual_cases=len(actual),all_actual_bound_exceeds=all(r['necessary_bound_exceeds_limit'] for r in actual),actual_minimum_k_range=[min(r['necessary_k'] for r in actual),max(r['necessary_k'] for r in actual)],actual_TC_peak_range=[min(r['candidate_min_peak_k'] for r in actual),max(r['candidate_min_peak_k'] for r in actual)],nominal_center_error_range_m=[min(r['nominal_center_error_m'] for r in actual),max(r['nominal_center_error_m'] for r in actual)],base36_bound_infeasible=sum(r['necessary_bound_exceeds_limit'] for r in baseout),base36_TC_admitted=sum(r['accepted_candidates']>0 for r in baseout),base36_TC_rejected=sum(r['accepted_candidates']==0 for r in baseout),limit=m.LIMIT,checks=checks,planner_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),GPU_runs=0,new_motion=0,source_modified=False)
(O/'curvature_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
