"""Predeclared C candidate: sensor-inferred occupied height, common DESIGN support prior.
No C/retained slots/GT pose input. Not the frozen ROBUST_A; not physical qualification.
"""
import numpy as np
from evaluation import b5_robust_20261110_v01 as rb
VERSION='C_ROBUST_SENSOR_HEIGHT_SITE_PRIOR_v01'
SITE_SUPPORT_TOP_Z=.144  # common B1 design floor0 + pallet thickness; NOT an observed/real-surveyed floor
def estimate(mask,depth,camera_metadata):
 out=dict(version=VERSION,status='DATUM_REJECTED',reason=None,pose=None,GT_input=False,uses_design_support_prior=True,design_support_top_z_m=SITE_SUPPORT_TOP_Z,physical_site_datum_certified=False)
 if mask is None or not mask.any():out.update(status='NO_DETECTION',reason='NO_SELECTED_MASK');return out
 cal,T=rb.calibration(camera_metadata);world,valid=rb.world_map(depth,cal,T);cfg=rb.DEFAULT_CONFIG
 fg=rb.depth_gap_cluster(mask,depth,cfg['depth_gap_m'],cfg['cluster_policy'],cfg['cluster_major_frac']);z=world[fg&valid,2]
 if len(z)<cfg['min_points']:out.update(status='DEPTH_INSUFFICIENT',reason='INSUFFICIENT_SENSOR_HEIGHT_POINTS');return out
 top=float(np.quantile(z,.99));n=int(round((top-SITE_SUPPORT_TOP_Z)/.09));out.update(sensed_top_z_m=top,inferred_layer_hypothesis=n)
 if not 1<=n<=4:out['reason']='SENSOR_HEIGHT_OUTSIDE_NOMINAL_1_TO_4';return out
 result=rb.estimate_pose(mask,depth,camera_metadata,n)
 out.update(result);out.update(version=VERSION,GT_input=False,uses_design_support_prior=True,design_support_top_z_m=SITE_SUPPORT_TOP_Z,inferred_layer_hypothesis=n,sensed_top_z_m=top,physical_site_datum_certified=False)
 return out
