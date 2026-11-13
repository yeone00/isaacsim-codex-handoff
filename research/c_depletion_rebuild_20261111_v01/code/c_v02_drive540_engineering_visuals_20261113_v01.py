"""Derived actual-video/trajectory artifacts, never counted E2E success. Original JPEG/trace untouched."""
from pathlib import Path
import json,csv,math,bisect
import cv2,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');P=D/'technical_e2e_v03/engineering/ENGINEERING_HISTORICAL_ROUTE_HR_C100';O=D/'visual_evidence_v01';frames=sorted((P/'attempt_0001/rec_robotcam').glob('*.jpg'));times=[float(p.stem.split('_')[1]) for p in frames];fps=5.;output=O/'engineering_actual_robot_camera.mp4';assert not output.exists();im=cv2.imread(str(frames[0]));h,w=im.shape[:2];writer=cv2.VideoWriter(str(output),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h));assert writer.isOpened();mapping=[]
for i in range(int(math.ceil((times[-1]-times[0])*fps))+1):
 t=times[0]+i/fps;j=max(0,min(len(frames)-1,bisect.bisect_right(times,t)-1));writer.write(cv2.imread(str(frames[j])));mapping.append(dict(output_frame=i,display_sim_s=t,source=str(frames[j])))
writer.release();cap=cv2.VideoCapture(str(output));ok,_=cap.read();n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));cap.release();assert ok and n==len(mapping)
(O/'MP4_encoding_validation.json').write_text(json.dumps(dict(state='PASS_DECODE',codec='mp4v',fps=fps,encoded_frames=n,timebase='simulation time; source-frame hold at constant5fps',source_mapping=mapping,original_JPEGs_unchanged=True,E2E_or_main_counted=False,ffmpeg_CLI='unavailable; no package installed; existing OpenCV encoder used'),indent=2))
rows=[]
with (P/'attempt_0001/steps.jsonl').open() as f:
 for l in f:
  x=json.loads(l)
  if x['phase'] in ['pulse','zero_stop']:rows.append(dict(sim_s=x['sim_s'],x_m=x['pose'][0],y_m=x['pose'][1],yaw_rad=x['pose'][3],planar_mps=x['planar_m_s']))
with (O/'engineering_actual_trajectory.csv').open('x',newline='') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
goals=json.loads((P/'attempt_0001/live_goals.json').read_text())['goals'];fig,axes=plt.subplots(1,2,figsize=(10,4));axes[0].plot([x['x_m'] for x in rows],[x['y_m'] for x in rows]);axes[0].scatter([x[0] for x in goals],[x[1] for x in goals],c=['orange','green'],marker='x',label='Engineering PRE / FINAL');axes[0].set(xlabel='World X (m)',ylabel='World Y (m)',title='Reconstructed from actual physics trace');axes[0].axis('equal');axes[0].legend(fontsize=8);axes[1].plot([x['sim_s'] for x in rows],[x['planar_mps'] for x in rows]);axes[1].axhline(.03,color='red',linestyle='--',label='Safety stop threshold');axes[1].set(xlabel='Simulation time (s)',ylabel='Measured speed (m/s)');axes[1].legend();fig.suptitle('Independent engineering control — excluded from E2E and main540');fig.tight_layout();fig.savefig(O/'engineering_trajectory_and_speed.png',dpi=180);plt.close(fig);print('MP4 decode PASS',n,'frames; actual trace plot saved')
