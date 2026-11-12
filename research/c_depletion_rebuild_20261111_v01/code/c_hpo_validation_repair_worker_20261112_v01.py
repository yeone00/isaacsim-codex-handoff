"""Evaluation only: frozen bitmap GT + native training-validation inference context; no train/optimizer."""
import os,sys,argparse,json,hashlib,time,types
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.insert(0,str(Path(__file__).resolve().parent))
from evaluation.c_common_hpo_policy_20261111_v01 import sha,atomic,gpu_gate,BASE_RECIPE
p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--checkpoint-sha',required=True);p.add_argument('--rep',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--limit',type=int,default=0);a=p.parse_args();assert sha(a.checkpoint)==a.checkpoint_sha;assert gpu_gate((os.getpid(),os.getppid()))['clear'];O=a.output;O.mkdir(parents=True,exist_ok=False);rc=json.loads(BASE_RECIPE.read_text());P=Path(rc['data']['package']);assert a.rep in rc['representations']
from ultralytics import YOLO
from ultralytics.cfg import get_cfg
from ultralytics.utils.torch_utils import init_seeds
from ultralytics.data.build import build_dataloader
import torch,numpy as np,cv2
import c_depletion_bitmap_adapter_20261112_v01 as BM
# Preserve training validation preprocessing: no random augmentation; rect mode and doubled val batch.
kw=dict(rc['train_args']);kw.update(task='segment',mode='val',batch=128,rect=True,augment=False,conf=.001,iou=.7,max_det=300,save_json=False,plots=False,project=str(O),name='validation',exist_ok=False)
cfg=get_cfg(overrides=kw);init_seeds(42,deterministic=True)
V=O/'dataset/images/val';V.mkdir(parents=True);images=sorted((P/a.rep/'images/val').glob('*.png'));assert len(images)==210
if a.limit:images=images[:a.limit]
for f in images:(V/f.name).symlink_to(f.resolve())
# Train alias points only to the same val view; no Test images, labels or inference in this worker.
view=O/'data.yaml';view.write_text(f'path: {O}/dataset\ntrain: images/val\nval: images/val\nnames:\n  0: brick_load\n');cfg.data=str(view)
data=dict(train=str(V),val=str(V),names={0:'brick_load'},nc=1,channels=3)
model=YOLO(str(a.checkpoint)).model.to('cuda:0').float().eval();model.args=cfg
# No loss/gradient calculation is needed for metrics. This only removes training-only validation loss work.
model.loss=types.MethodType(lambda self,batch,preds:(None,{}),model)
owner=types.SimpleNamespace(args=cfg,model=model,data=data)
ds=BM.dataset(owner,str(V),mode='val',batch=128)
assert not ds.augment and cfg.mask_ratio==4 and not cfg.overlap_mask and ds.rect
reg=json.loads((P/'bitmap_registry.json').read_text());mask_audit=[]
for i,f in enumerate(ds.im_files):
 raw=BM.read_masks(reg[str(Path(f).resolve())]['masks']);d=ds.get_image_and_label(i)
 assert np.array_equal(raw,d['bitmap_masks']),'RAW_BITMAP_ALTERED'
 assert len(raw)==len(d['cls'])==len(d['instances'])
 mask_audit.append(dict(image=str(Path(f).resolve()),image_sha256=sha(Path(f).resolve()),masks=[dict(path=m,sha256=sha(m),pixels=int((cv2.imread(m,0)>0).sum())) for m in reg[str(Path(f).resolve())]['masks']]))
loader=build_dataloader(ds,batch=128,workers=8,shuffle=False,rank=-1)
val=BM.CBitmapValidator(loader,save_dir=O/'validation',args=cfg)
trainer=types.SimpleNamespace(device=torch.device('cuda:0'),data=data,amp=True,ema=types.SimpleNamespace(ema=model),model=model,args=cfg,loss_items={},stopper=types.SimpleNamespace(possible_stop=False),epoch=0,epochs=2,world_size=1,label_loss_items=lambda loss,prefix='val':{})
started=time.time()
with torch.inference_mode():val(trainer=trainer)
assert sha(a.checkpoint)==a.checkpoint_sha
atomic(O/'mask_input_audit.json',dict(images=mask_audit,instances=sum(len(z['masks']) for z in mask_audit),Test_used=False,raw_pixels_and_instance_ownership_preserved=True))
atomic(O/'result.json',dict(state='COMPLETED',validation_rep=a.rep,checkpoint=str(a.checkpoint),checkpoint_sha256=a.checkpoint_sha,mask_map5095=float(val.metrics.seg.map),mask_map50=float(val.metrics.seg.map50),box_map5095=float(val.metrics.box.map),images=len(ds),instances=sum(len(z['masks']) for z in mask_audit),Test_used=False,secondary_only=True,training_performed=False,settings=dict(mask_ratio=4,overlap_mask=False,augment=False,rect=True,validation_batch=128,training_batch_unchanged=64,conf=.001,iou=.7,max_det=300,inference_precision='native training validation float32 EMA weights with CUDA autocast16; loaded checkpoint float16 EMA rounded when originally saved',fuse=False,bitmap_source=BM.__file__,transforms=[type(x).__name__ for x in ds.transforms.transforms]),elapsed_seconds=time.time()-started))
