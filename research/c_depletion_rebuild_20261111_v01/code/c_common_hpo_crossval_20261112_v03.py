"""Secondary validation only; never reads test data or influences promotion."""
import argparse,json,sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluation.c_common_hpo_policy_20261111_v01 import load_protocol,sha,atomic,gpu_gate,BASE_RECIPE
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--protocol-sha',required=True);p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--checkpoint-sha',required=True);p.add_argument('--rep',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
load_protocol(a.root,a.protocol_sha);assert sha(a.checkpoint)==a.checkpoint_sha
assert gpu_gate((os.getpid(),os.getppid()))['clear']
rc=json.loads(BASE_RECIPE.read_text());assert a.rep in rc['representations']
a.output.mkdir(parents=True,exist_ok=False)
package=Path(rc['data']['package'])/a.rep
for kind in ['images','labels']:
 d=a.output/kind/'val';d.mkdir(parents=True)
 for f in sorted((package/kind/'val').iterdir()):
  if f.suffix.lower() in (['.png','.jpg','.jpeg'] if kind=='images' else ['.txt']):(d/f.name).symlink_to(f.resolve())
view=a.output/'data.yaml';view.write_text(f'path: {a.output}\ntrain: images/val\nval: images/val\nnames:\n  0: brick_load\n')
from ultralytics import YOLO
from c_depletion_bitmap_adapter_20261112_v01 import CBitmapValidator
m=YOLO(str(a.checkpoint)).val(validator=CBitmapValidator,data=str(view),split='val',imgsz=640,batch=64,device=0,workers=8,plots=False,save_json=False,project=str(a.output),name='validation',exist_ok=False)
atomic(a.output/'result.json',dict(state='COMPLETED',validation_rep=a.rep,checkpoint=str(a.checkpoint),checkpoint_sha256=a.checkpoint_sha,mask_map5095=float(m.seg.map),box_map5095=float(m.box.map),test_used=False,secondary_only=True))
