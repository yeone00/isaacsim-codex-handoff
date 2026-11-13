"""Independent CPU review of mathematical proposals, no runtime code imported/changed."""
import pathlib,csv,json,math,hashlib
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1];O=R/'reports/c_v02_drive540_global_path_design_20261113_v02'
def read(n):return list(csv.DictReader(open(O/n)))
def write(n,rows):
 with (O/n).open('x',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
comp=read('base36_direct_vs_global.csv');trials=read('global_CSC_search_trials.csv');policy=json.load(open(O/'offline_design_policy.json'));q=policy['smooth_curvature_slope_per_m2'];checks=[]
for r in comp:
 p=read(r['base_id']+'_offline_global_candidate.csv');a=np.array([[float(x[z]) for z in ['s','rear_x','rear_y','base_x','base_y','yaw_rad','k']] for x in p]);k=float(r['global_peak_k']);t=next(x for x in trials if x['base_id']==r['base_id'] and x['family']==r['global_family'] and abs(float(x['length_m'])-float(r['global_length_m']))<1e-8 and x['geometric_endpoint_PASS']=='True');sa=1 if t['family'][0]=='L' else -1;sb=1 if t['family'][-1]=='L' else -1;ramp=k/q;pieces=[]
 for i,sign in enumerate([sa,sb]):
  pieces += [(ramp,0.,sign*k),(float(t['hold1_m'] if i==0 else t['hold2_m']),sign*k,sign*k),(ramp,sign*k,0.)]
  if i==0:pieces.append((float(t['straight_m']),0.,0.))
 # Independent midpoint quadrature at <=0.5mm, no use of Gauss-Legendre solver.
 xy=a[0,1:3].copy();theta=a[0,5]
 for L,k0,k1 in pieces:
  n=max(1,math.ceil(L/.0005));ds=L/n;x=(np.arange(n)+.5)*ds
  th=theta+k0*x+.5*(k1-k0)/L*x*x if L>0 else np.full(n,theta)
  xy+=np.array([np.cos(th).sum(),np.sin(th).sum()])*ds;theta+=.5*(k0+k1)*L
 endpoint_error=float(np.linalg.norm(xy-a[-1,1:3]));assert endpoint_error<1e-6
 rate=float(np.max(np.abs(np.diff(np.arctan(.7*a[:,6]))/np.diff(a[:,0]))*.02)*180/math.pi)
 peak=float(np.max(np.abs(a[:,6])));assert peak<=policy['curve_limit']+1e-10 and rate<=policy['rate_limit_deg_s']+1e-8
 base_length=float(np.sum(np.linalg.norm(np.diff(a[:,3:5],axis=0),axis=1)));mincos=float(np.min(np.cos(a[:,5]-a[0,5])));monotonic=mincos>0
 # Existing pure follower's along-goal guard, inspected source: no commands executed.
 goal=a[-1,3:5];ga=a[-1,5];along=(goal[0]-a[:,3])*math.cos(ga)+(goal[1]-a[:,4])*math.sin(ga);overshoot=bool(np.any(along<-.005));timeout=base_length/.02>180
 checks.append(dict(base_id=r['base_id'],independent_midpoint_endpoint_error_m=endpoint_error,peak_k=peak,finite_difference_rate_deg_s=rate,analytic_rate_bound_deg_s=policy['rate_limit_deg_s'],max_virtual_steer_deg=math.degrees(math.atan(.7*peak)),min_initial_heading_cos=mincos,monotonic_initial_heading=monotonic,existing_GOAL_OVERSHOOT_guard_would_trigger=overshoot,reference_base_path_length_m=base_length,nominal_02mps_minimum_travel_s=base_length/.02,exceeds_180s_approach_timeout=timeout,rear_path_length_le3m=float(r['global_length_m'])<=3,geometry_and_rate_only_PASS=True,collision_PASS='UNKNOWN',physical_control_PASS='UNKNOWN',frozen_policy_compatible_geometry_only=monotonic and not overshoot and not timeout and float(r['global_length_m'])<=3))
write('base36_independent_review.csv',checks)
summary=dict(bases=36,independent_geometric_rate_PASS=36,strict_frozen_local_policy_compatible=sum(x['frozen_policy_compatible_geometry_only'] for x in checks),overshoot_guard_conflicts=sum(x['existing_GOAL_OVERSHOOT_guard_would_trigger'] for x in checks),timeout_conflicts=sum(x['exceeds_180s_approach_timeout'] for x in checks),minimum_time_range_s=[min(x['nominal_02mps_minimum_travel_s'] for x in checks),max(x['nominal_02mps_minimum_travel_s'] for x in checks)],max_independent_integration_error_m=max(x['independent_midpoint_endpoint_error_m'] for x in checks),max_rate_deg_s=max(x['finite_difference_rate_deg_s'] for x in checks),all_collision_and_control_UNKNOWN=True,original_artifacts_changed=False,new_physics=0)
(O/'independent_review_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
# Standard scientific visualization, offline design paths only; not simulation imagery.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(1,3,figsize=(15,4.8))
for ax,bid in zip(axs[:2],['C2D_B01','C2D_B11']):
 pp=read(bid+'_offline_global_candidate.csv');x=[float(z['base_x']) for z in pp];y=[float(z['base_y']) for z in pp]
 ax.plot(x,y,label='Offline proposed path');ax.plot(x[0],y[0],'go',label='Locked start');ax.plot(x[-1],y[-1],'rx',label='Nominal PRE (diagnosis only)');ax.set_aspect('equal');ax.set_title(bid+' free-space geometry');ax.set_xlabel('World X (m)');ax.set_ylabel('World Y (m)');ax.legend(fontsize=7);ax.grid()
ss=read('base36_start_redesign_counterfactual.csv');shifts=[.25,.5,.75,1.,1.25];count=[sum(x['geometry_rate_PASS']=='True' and float(x['backshift_y_m'])==s for x in ss) for s in shifts];axs[2].plot([0]+shifts,[4]+count,'o-');axs[2].set_ylim(0,38);axs[2].set_xlabel('Unapproved common backward shift in world Y (m)');axs[2].set_ylabel('TC-S geometry + rate pass / 36');axs[2].grid();axs[2].set_title('Separate start redesign alternative')
fig.suptitle('CPU design only: collision / physical control NOT validated');fig.tight_layout();fig.savefig(O/'offline_path_proposals.png',dpi=160);plt.close(fig)
