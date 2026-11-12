"""C-only bitmap instances. Frozen v04 image transforms/RNG, full masks before mask_ratio=4.
No contour bridging, instance splitting, hole filling, or change to installed Ultralytics.
"""
import json,copy
from pathlib import Path
import cv2,numpy as np,torch
from ultralytics.data.dataset import YOLODataset
from ultralytics.data.augment import RandomPerspective,RandomFlip,LetterBox,Format,Compose
from ultralytics.utils.instance import Instances
from ultralytics.models.yolo.segment.val import SegmentationValidator
from ultralytics.utils.torch_utils import unwrap_model
PACKAGE=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/execution_v01/C_BITMAP_PACKAGE_v01')
def boxes(ms):
 out=[]
 for m in ms:
  y,x=np.where(m);out.append([x.min(),y.min(),x.max()+1,y.max()+1] if len(x) else [0,0,0,0])
 return np.asarray(out,dtype=np.float32).reshape(-1,4)
def read_masks(paths,shape=None):
 ms=[]
 for p in paths:
  m=cv2.imread(str(p),0);assert m is not None and set(np.unique(m))<={0,255}
  m=(m>0).astype('uint8')
  if shape and m.shape!=shape:m=cv2.resize(m,shape[::-1],interpolation=cv2.INTER_NEAREST)
  ms.append(m)
 return np.stack(ms)
class BitmapPerspective(RandomPerspective):
 def apply_instances(self,labels,params=None):
  old=labels['instances'];old.convert_bbox('xyxy');old.denormalize(*params['orig_shape'][::-1]);b1=old.bboxes.copy()*params['scale']
  ms=labels['bitmap_masks'];M=params['M'];size=params['size']
  warp=cv2.warpPerspective if self.perspective else cv2.warpAffine
  ms=np.stack([warp(m,M if self.perspective else M[:2],size,flags=cv2.INTER_NEAREST,borderValue=0) for m in ms]) if len(ms) else np.zeros((0,size[1],size[0]),np.uint8)
  bb=boxes(ms);keep=self.box_candidates(b1.T,bb.T,area_thr=.01)
  labels['bitmap_masks']=ms[keep];labels['cls']=labels['cls'][keep]
  labels['instances']=Instances(bb[keep],bbox_format='xyxy',normalized=False)
  return labels
class BitmapFlip(RandomFlip):
 def apply_instances(self,labels,params=None):
  labels=super().apply_instances(labels,params)
  if params['flip']:labels['bitmap_masks']=np.flip(labels['bitmap_masks'],axis=1 if params['direction']=='vertical' else 2).copy()
  return labels
class BitmapLetterBox(LetterBox):
 def apply_instances(self,labels,params=None):
  labels=super().apply_instances(labels,params);p=params
  labels['bitmap_masks']=np.stack([cv2.copyMakeBorder(cv2.resize(m,p['new_unpad'],interpolation=cv2.INTER_NEAREST),p['top'],p['bottom'],p['left'],p['right'],cv2.BORDER_CONSTANT,value=0) for m in labels['bitmap_masks']]) if len(labels['bitmap_masks']) else np.zeros((0,labels['img'].shape[0],labels['img'].shape[1]),np.uint8)
  return labels
class BitmapFormat(Format):
 def get_params(self,labels):
  ms=labels.pop('bitmap_masks');inst=labels['instances'];inst.bitmap_masks=ms
  return super().get_params(labels)
 def _format_segments(self,instances,cls,w,h):
  assert not self.mask_overlap,'Frozen nonoverlap policy required'
  ms=instances.bitmap_masks
  # Match frozen polygon2mask final cv2.resize semantics; only polygon rasterization is removed.
  masks=np.stack([cv2.resize(m,(w//self.mask_ratio,h//self.mask_ratio)) for m in ms])
  return masks,instances,cls

def replace_transforms(t):
 if isinstance(t,Compose):t.transforms=[replace_transforms(x) for x in t.transforms]
 else:
  if type(t) in {RandomPerspective,RandomFlip,LetterBox,Format}:
   cls={RandomPerspective:BitmapPerspective,RandomFlip:BitmapFlip,LetterBox:BitmapLetterBox,Format:BitmapFormat}[type(t)];q=cls.__new__(cls);q.__dict__=copy.deepcopy(t.__dict__);t=q
  # Installed v8 pipeline uses pre_transform inside mix transforms, all frozen probabilities zero.
  for name in ['pre_transform']:
   if getattr(t,name,None) is not None:setattr(t,name,replace_transforms(getattr(t,name)))
 return t
class CBitmapDataset(YOLODataset):
 def get_labels(self):
  registry=json.loads((PACKAGE/'bitmap_registry.json').read_text());self.bitmap_paths={};labels=[]
  for f in self.im_files:
   real=str(Path(f).resolve());r=registry[real];self.bitmap_paths[real]=r['masks'];h,w=cv2.imread(real).shape[:2];ms=read_masks(r['masks']) if r['masks'] else np.zeros((0,h,w),np.uint8);bb=boxes(ms);bb[:,[0,2]]/=w;bb[:,[1,3]]/=h
   # xyxy labels, no dummy polygon is a training target.
   labels.append(dict(im_file=f,shape=(h,w),cls=np.zeros((len(ms),1),np.float32),bboxes=bb,segments=[],keypoints=None,normalized=True,bbox_format='xyxy'))
  return labels
 def get_image_and_label(self,index):
  d=super().get_image_and_label(index);paths=self.bitmap_paths[str(Path(d['im_file']).resolve())];d['bitmap_masks']=read_masks(paths,d['img'].shape[:2]) if paths else np.zeros((0,*d['img'].shape[:2]),np.uint8);return d
 def build_transforms(self,hyp=None):
  assert all(getattr(hyp,k)==0 for k in ['mosaic','mixup','cutmix','copy_paste']) and not hyp.overlap_mask
  return replace_transforms(super().build_transforms(hyp))
def dataset(owner,img_path,mode='train',batch=None,validation=False):
 gs=int(max(unwrap_model(owner.model).stride.max() if getattr(owner,'model',None) is not None and hasattr(unwrap_model(owner.model),'stride') else 0,32)) if not validation else int(owner.stride)
 return CBitmapDataset(img_path=img_path,imgsz=owner.args.imgsz,batch_size=batch,augment=mode=='train',hyp=owner.args,rect=mode=='val' if not validation else owner.args.rect,cache=False,single_cls=owner.args.single_cls,stride=gs,pad=0.0 if mode=='train' else .5,prefix=f'{mode}: ',task='segment',classes=owner.args.classes,data=owner.data,fraction=owner.args.fraction if mode=='train' else 1.)
class CBitmapValidator(SegmentationValidator):
 def build_dataset(self,img_path,mode='val',batch=None):return dataset(self,img_path,mode,batch,True)

BitmapFormat.__name__="Format" # preserve original PhotoDegrade insertion contract
