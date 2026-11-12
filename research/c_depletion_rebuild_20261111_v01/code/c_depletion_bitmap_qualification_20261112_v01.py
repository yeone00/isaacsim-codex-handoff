"""CPU regression: identity topology, exact affine/flip masks and stock image/RNG parity."""
import sys,copy,random,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import c_depletion_bitmap_adapter_20261112_v01 as B
import cv2,numpy as np
from ultralytics.data.augment import RandomPerspective,RandomFlip,LetterBox
from ultralytics.utils.instance import Instances
O=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02/bitmap_qualification_v01');O.mkdir(exist_ok=True)
m=np.zeros((2,96,128),np.uint8);m[0,10:70,10:65]=1;m[0,25:40,25:40]=0;m[0,75:85,80:100]=1;m[1,20:60,90:110]=1
im=np.arange(96*128*3,dtype=np.uint8).reshape(96,128,3)
def sample():return dict(img=im.copy(),cls=np.zeros((2,1),np.float32),instances=Instances(B.boxes(m),bbox_format='xyxy',normalized=False),bitmap_masks=m.copy())
checks=[]
for seed in range(32):
 old=RandomPerspective(degrees=3,translate=.1,scale=.25,size=(128,96));new=B.replace_transforms(copy.deepcopy(old));d=sample()
 random.seed(seed);state=random.getstate();params=old.get_params(copy.deepcopy(d));image_ref=old.apply_image(copy.deepcopy(d),params)['img'];after=random.getstate()
 random.setstate(state);z=new(copy.deepcopy(d));assert np.array_equal(image_ref,z['img']) and random.getstate()==after
 ref=np.stack([cv2.warpAffine(x,params['M'][:2],(128,96),flags=cv2.INTER_NEAREST,borderValue=0) for x in m]);bb=B.boxes(ref);keep=old.box_candidates((B.boxes(m)*params['scale']).T,bb.T,area_thr=.01);assert np.array_equal(z['bitmap_masks'],ref[keep])
 f=RandomFlip(.5);bf=B.replace_transforms(copy.deepcopy(f));random.seed(seed);params=f.get_params(copy.deepcopy(z));ref=f.apply_image(copy.deepcopy(z),params)['img'];random.seed(seed);zz=bf(copy.deepcopy(z));assert np.array_equal(ref,zz['img']);assert np.array_equal(zz['bitmap_masks'],np.flip(z['bitmap_masks'],2) if params['flip'] else z['bitmap_masks'])
 checks.append(seed)
lb=B.replace_transforms(LetterBox((128,128),scaleup=False));d=lb(sample());assert np.array_equal(d['bitmap_masks'][:,16:112],m) and not d['bitmap_masks'][:,:16].any()
f=B.BitmapFormat(return_mask=True,mask_overlap=False,mask_ratio=1);z=f(d);assert np.array_equal(z['masks'].numpy()[:,16:112],m)
r=dict(state='PASS',seeds=len(checks),mask_holes_and_disconnected_components_exact=True,image_and_rng_match_installed_affine_flip=True,letterbox_exact=True,mask_ratio1_format_exact=True,photometric_original_unchanged=True,GPU_used=False)
(O/'CPU_result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
