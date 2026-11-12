"""CPU positive/holey/disconnected/negative mask augmentation contract."""
import sys,copy,random,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import c_v02_bitmap_adapter_20261112_v01 as B
import numpy as np,cv2
from ultralytics.utils.instance import Instances
from ultralytics.data.augment import RandomPerspective,LetterBox,RandomFlip
V=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01');checks=[]
for n in [0,1,2]:
 for h,w in [(480,640),(1296,972)]:
  ms=np.zeros((n,h,w),np.uint8)
  for i in range(n):ms[i,20+i*60:150+i*60,50:200]=1;ms[i,50+i*60:80+i*60,80:100]=0;ms[i,200+i*60:220+i*60,250:280]=1
  labels=dict(img=np.zeros((h,w,3),np.uint8),cls=np.zeros((n,1),np.float32),instances=Instances(B.boxes(ms),bbox_format='xyxy',normalized=False),bitmap_masks=ms.copy())
  for t in [B.replace_transforms(RandomPerspective(degrees=3,translate=.1,scale=.25,size=(640,640))),B.replace_transforms(RandomFlip(.5)),B.replace_transforms(LetterBox((640,640)))]:labels=t(labels)
  z=B.BitmapFormat(return_mask=True,mask_overlap=False,mask_ratio=4)(labels);assert z['masks'].shape[0]==z['cls'].shape[0]==z['bboxes'].shape[0];checks.append(dict(instances=n,shape=[h,w],result='PASS'))
(V/'bitmap_CPU_qualification_v01.json').write_text(json.dumps(dict(state='PASS',cases=checks,GPU_used=False),indent=2));print('bitmap6positive/negative/resolution checks PASS')
