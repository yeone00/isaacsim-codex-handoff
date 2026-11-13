"""OFFLINE MATHEMATICAL DESIGN ONLY. Not an operational planner; never imported by workers.
Existing artifacts/protocol/controllers untouched. No Isaac/ROS/GPU/model imports.
"""
import pathlib,json,csv,hashlib,math,importlib.util,time
import numpy as np
from scipy.optimize import least_squares
R=pathlib.Path(__file__).resolve().parents[1];O=R/'reports/c_v02_drive540_global_path_design_20261113_v01';O.mkdir(exist_ok=False)
D=pathlib.Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01')
source=R/'analysis/stage3_local_planner_20261109_v01.py';spec=importlib.util.spec_from_file_location('pure_math_tcs',source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
base=list(csv.DictReader(open(R/'reports/c_v02_drive540_storage_curvature_audit_20261113_v01/base36_nominal_geometry.csv')))
manifest=D/'single_load_amendment_v01/attempt_manifest.csv';manifestsha=hashlib.sha256(manifest.read_bytes()).hexdigest();protocol=D/'single_load_amendment_v01/protocol.json';protocolsha=hashlib.sha256(protocol.read_bytes()).hexdigest()
K=m.LIMIT*(1-1e-8);slope=math.radians(m.RATE_CAP_DEG_S)/(m.WHEELBASE*m.V_NOMINAL)
policy=dict(scope='offline diagnostics only; not production implementation',start_unchanged=True,nominal_goal_evaluation_only=True,radius_curvature_factors=[1.,.8,.6],CSC_turn_signs=[[1,1],[-1,-1],[1,-1],[-1,1]],smooth_curvature_slope_per_m2=slope,solver_max_nfev=180,solver_endpoint_tolerance_m=1e-6,solver_heading_tolerance_rad=1e-7,path_sampling_step_m=.02,alternative_start_backshift_grid_m=[.25,.5,.75,1.,1.25],curve_limit=m.LIMIT,rate_limit_deg_s=m.RATE_CAP_DEG_S,nominal_speed_mps=m.V_NOMINAL,physical_execution=False,collision_or_control_PASS_authorized=False)
(O/'offline_design_policy.json').write_text(json.dumps(policy,indent=2));nodes,weights=np.polynomial.legendre.leggauss(32)
def write(name,rows):
 with (O/name).open('x',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def wrap(x):return math.atan2(math.sin(x),math.cos(x))
def integrate(p,L,k0,k1):
 x,y,a=p
 if L<1e-12:return np.array(p)
 q=(nodes+1)*L/2;ang=a+k0*q+.5*(k1-k0)/L*q*q
 return np.array([x+L/2*np.sum(weights*np.cos(ang)),y+L/2*np.sum(weights*np.sin(ang)),a+.5*(k0+k1)*L])
def pieces(lengths,signs,k):
 h1,straight,h2=lengths;ramp=k/slope;z=[]
 for i,h in enumerate((h1,h2)):
  a=signs[i]*k;z.extend([(ramp,0.,a),(h,a,a),(ramp,a,0.)])
  if i==0:z.append((straight,0.,0.))
 return z
def endpoint(lengths,signs,k):
 p=np.zeros(3)
 for L,k0,k1 in pieces(lengths,signs,k):p=integrate(p,L,k0,k1)
 return p

def CSC_seed(goal,sa,sb,k):
 radius=1/k;X,Y,delta=goal;ca=np.array([0.,sa*radius]);cb=np.array([X-sb*radius*math.sin(delta),Y+sb*radius*math.cos(delta)]);d=cb-ca;dist=np.linalg.norm(d);off=(sa-sb)*radius
 if dist<1e-12 or abs(off)>dist+1e-10:return None
 beta=math.atan2(d[1],d[0]);q=math.asin(max(-1,min(1,off/dist)))
 for a in [beta+q,beta+math.pi-q]:
  T=float(d@np.array([math.cos(a),math.sin(a)]))
  if T<0:continue
  a1=(sa*a)%(2*math.pi);a2=(sb*(delta-a))%(2*math.pi);heading=sa*a1+sb*a2
  return np.array([a1*radius,T,a2*radius]),heading
 return None

def sample(lengths,signs,k,st):
 rear,a=m.rear_pose(st);p=np.zeros(3);ss=0;out=[]
 for L,k0,k1 in pieces(lengths,signs,k):
  n=max(1,int(math.ceil(L/.02)))
  for i in range(n):
   f=i/n;pp=integrate(p,L*f,k0,k0+(k1-k0)*f);ca,si=math.cos(a),math.sin(a);xy=rear+np.array([ca*pp[0]-si*pp[1],si*pp[0]+ca*pp[1]]);yaw=a+pp[2];base=xy+m.OFFSET*np.array([math.cos(yaw),math.sin(yaw)])
   out.append(dict(s=ss+L*f,rear_x=xy[0],rear_y=xy[1],base_x=base[0],base_y=base[1],yaw_rad=yaw,k=k0+(k1-k0)*f))
  p=integrate(p,L,k0,k1);ss+=L
 rearend=rear+np.array([math.cos(a)*p[0]-math.sin(a)*p[1],math.sin(a)*p[0]+math.cos(a)*p[1]]);yaw=a+p[2];b=rearend+m.OFFSET*np.array([math.cos(yaw),math.sin(yaw)])
 out.append(dict(s=ss,rear_x=rearend[0],rear_y=rearend[1],base_x=b[0],base_y=b[1],yaw_rad=yaw,k=0.))
 return out
trials=[];comparison=[];allpaths=[];t0=time.time()
for r in base:
 st=(float(r['start_x']),float(r['start_y']),math.radians(float(r['start_yaw_deg'])));goal=(-25.888,30.509-2.203745031260775,math.pi/2);sr,a=m.rear_pose(st);gr,b=m.rear_pose(goal);d=gr-sr;local=np.array([d@[math.cos(a),math.sin(a)],d@[-math.sin(a),math.cos(a)],wrap(b-a)])
 found=[]
 for fac in policy['radius_curvature_factors']:
  k=fac*K
  for sa,sb in policy['CSC_turn_signs']:
   seed=CSC_seed(local,sa,sb,k)
   if seed is None:continue
   lengths,heading=seed;target=np.array([local[0],local[1],heading]);ramp=k/slope
   guess=np.maximum([lengths[0]-ramp,lengths[1],lengths[2]-ramp],1e-7)
   sol=least_squares(lambda v:endpoint(v,(sa,sb),k)-target,guess,bounds=(np.zeros(3),np.full(3,100.)),max_nfev=policy['solver_max_nfev'],xtol=1e-12,ftol=1e-12,gtol=1e-12)
   err=endpoint(sol.x,(sa,sb),k)-target;xyerr=float(np.linalg.norm(err[:2]));yawerr=abs(float(err[2]));ok=xyerr<1e-6 and yawerr<1e-7
   total=float(sum(sol.x)+4*ramp);trial=dict(base_id=r['base_id'],family=('L' if sa>0 else 'R')+'S'+('L' if sb>0 else 'R'),curvature_factor=fac,geometric_endpoint_PASS=ok,xy_error_m=xyerr,heading_error_rad=yawerr,length_m=total,hold1_m=sol.x[0],straight_m=sol.x[1],hold2_m=sol.x[2],peak_curvature=k,analytic_rate_bound_deg_s=m.RATE_CAP_DEG_S,solver_evals=sol.nfev)
   trials.append(trial)
   if ok:found.append((total,trial,sol.x,(sa,sb),k))
 if found:
  _,tr,lens,signs,k=min(found,key=lambda q:q[0]);path=sample(lens,signs,k,st)
  write(r['base_id']+'_offline_global_candidate.csv',path)
  xs=[p['base_x'] for p in path];ys=[p['base_y'] for p in path]
  new=dict(global_geometric_PASS=True,global_family=tr['family'],global_length_m=tr['length_m'],global_peak_k=k,global_rate_bound_deg_s=m.RATE_CAP_DEG_S,endpoint_error_m=tr['xy_error_m'],endpoint_yaw_error_rad=tr['heading_error_rad'],xmin=min(xs),xmax=max(xs),ymin=min(ys),ymax=max(ys),start_heading_monotonic_forward=False,collision='UNKNOWN_NOT_CHECKED',control_safety='UNKNOWN_NOT_EXECUTED',failure_reason='NONE_IN_FREE_SPACE_GEOMETRY; SITE_AND_CONTROL_UNVERIFIED')
 else:new=dict(global_geometric_PASS=False,global_family='',global_length_m=None,global_peak_k=None,global_rate_bound_deg_s=m.RATE_CAP_DEG_S,endpoint_error_m=None,endpoint_yaw_error_rad=None,xmin=None,xmax=None,ymin=None,ymax=None,start_heading_monotonic_forward=False,collision='UNKNOWN_NOT_CHECKED',control_safety='UNKNOWN_NOT_EXECUTED',failure_reason='NO_ENDPOINT_SOLUTION_IN_FROZEN_OFFLINE_CSC_SEARCH')
 comparison.append(dict(base_id=r['base_id'],source_family=r['source_family'],start_x=st[0],start_y=st[1],start_yaw_deg=float(r['start_yaw_deg']),baseline_direct_PASS=int(r['accepted_candidates'])>0,baseline_reason='PASS_GEOMETRY_RATE_ONLY' if int(r['accepted_candidates']) else 'NO_ADMITTED_TC_CANDIDATE',monotonic_waypoint_necessary_bound_fail=r['necessary_bound_exceeds_limit']=='True',**new))
 print(r['base_id'],new['global_geometric_PASS'],new['global_length_m'],flush=True)
write('base36_direct_vs_global.csv',comparison);write('global_CSC_search_trials.csv',trials)
# Start redesign is an unapproved counterfactual, distinct from current-start global routes.
shifts=[]
for shift in policy['alternative_start_backshift_grid_m']:
 for r in base:
  st=(float(r['start_x']),float(r['start_y'])-shift,math.radians(float(r['start_yaw_deg'])));go=(-25.888,30.509-2.203745031260775,math.pi/2)
  try:
   path,met=m.plan(st,go);passed=True;reason='PASS_GEOMETRY_RATE_ONLY';peak=met['peak_abs_k'];rate=met['ff_steer_rate_deg_s'];length=path[-1][4]
  except ValueError as e:passed=False;reason=str(e);peak=rate=length=None
  shifts.append(dict(base_id=r['base_id'],backshift_y_m=shift,proposed_x=st[0],proposed_y=st[1],proposed_yaw_deg=float(r['start_yaw_deg']),geometry_rate_PASS=passed,reason=reason,peak_k=peak,rate_deg_s=rate,length_m=length,approved=False,collision='UNKNOWN',sensor_view='UNKNOWN'))
 print('redesign shift',shift,'pass',sum(x['geometry_rate_PASS'] for x in shifts if x['backshift_y_m']==shift),flush=True)
write('base36_start_redesign_counterfactual.csv',shifts)
summary=dict(bases=36,baseline_admitted=sum(x['baseline_direct_PASS'] for x in comparison),monotonic_waypoint_proven_impossible=sum(x['monotonic_waypoint_necessary_bound_fail'] for x in comparison),global_geometric_success=sum(x['global_geometric_PASS'] for x in comparison),global_length_range_m=[min(x['global_length_m'] for x in comparison if x['global_geometric_PASS']),max(x['global_length_m'] for x in comparison if x['global_geometric_PASS'])],start_redesign=[dict(backshift_m=s,passes=sum(x['geometry_rate_PASS'] for x in shifts if x['backshift_y_m']==s)) for s in policy['alternative_start_backshift_grid_m']],manifest_sha_before=manifestsha,manifest_sha_after=hashlib.sha256(manifest.read_bytes()).hexdigest(),protocol_sha_before=protocolsha,protocol_sha_after=hashlib.sha256(protocol.read_bytes()).hexdigest(),planner_sha=hashlib.sha256(source.read_bytes()).hexdigest(),new_GPU_or_motion=0,operational_planner_changed=False,elapsed_s=time.time()-t0)
assert summary['manifest_sha_before']==summary['manifest_sha_after'] and summary['protocol_sha_before']==summary['protocol_sha_after']
(O/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
