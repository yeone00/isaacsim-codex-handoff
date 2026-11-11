"""Common HPO policy. Stdlib only; no GPU or legacy imports at module load."""
import hashlib,json,math,os,subprocess
from pathlib import Path

REPS=('HR_Scan','LR_Scan','GeoCAD')
SPACE={'lr0':(0.0002,0.003,True),'weight_decay':(0.00001,0.002,True),'lrf':(.05,.25,False),'warmup_epochs':(1.,5.,False)}
BASE={'lr0':.001,'weight_decay':.0005,'lrf':.1,'warmup_epochs':3.}
R=Path(__file__).resolve().parents[1]
S=Path('/home/user/hh/isaac_cosmos/sdg_final')
BASE_RECIPE=S/'C_DEPLETION_REBUILD_20261111_v01/execution_v02/training_recipe.json'
BASE_SHA=hashlib.sha256(BASE_RECIPE.read_bytes()).hexdigest() if BASE_RECIPE.exists() else 'C_DATASET_NOT_READY'

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def atomic(p,obj):
 p=Path(p);q=p.with_name(p.name+'.tmp.'+str(os.getpid()))
 with q.open('x') as f:json.dump(obj,f,indent=2,allow_nan=False);f.flush();os.fsync(f.fileno())
 os.replace(q,p)

def common_score(scores):
 if set(scores)!=set(REPS):raise ValueError('THREE_REPRESENTATIONS_REQUIRED')
 if not all(isinstance(x,(float,int)) and math.isfinite(x) and 0<=x<=1 for x in scores.values()):raise ValueError('INVALID_MASK_MAP')
 return sum(scores[r] for r in REPS)/3

def validate_params(params):
 if set(params)!=set(SPACE):raise ValueError('ONLY_FOUR_SEARCH_PARAMETERS_ALLOWED')
 for k,(lo,hi,_) in SPACE.items():
  if not isinstance(params[k],(int,float)) or not math.isfinite(params[k]) or not lo<=params[k]<=hi:raise ValueError('PARAMETER_OUTSIDE_FROZEN_SPACE:'+k)

def gpu_gate(allowed_pids=()):
 """Do not start if existing driving queue, Isaac, training or unknown CUDA owner exists."""
 reasons=[];owners=[]
 matrix=json.loads((R/'configs/stage4_ablation_matrix_20261110_v01.json').read_text())
 counts={}
 for phase in ['main','o50']:
  n=0
  for it in matrix[phase]:
   name=it['run_name'];a=S/'STAGE4_ABLATION_20261110_v01_run02'/name/'result.json';b=S/'STAGE4_ABLATION_20261110_v01_run01'/name/'result.json'
   if a.exists() or it['group'] in ['G0','G1'] and b.exists():n+=1
  counts[phase]={'recorded':n,'declared':len(matrix[phase])}
  if n!=len(matrix[phase]):reasons.append('DRIVING_'+phase.upper()+'_INCOMPLETE')
 for p in Path('/proc').iterdir():
  if not p.name.isdigit() or int(p.name) in {os.getpid(),*allowed_pids}:continue
  try:args=[x.decode(errors='replace') for x in (p/'cmdline').read_bytes().split(b'\0') if x]
  except (OSError,PermissionError):continue
  if not args:continue
  script=Path(args[1]).name if len(args)>1 else ''
  if 'hh_isaac51/bin/python' in args[0] or script.startswith(('stage4_ablation_batch_','stage4_ablation_drive_session_','train_b1_','b1_common_hpo_train_')):
   owners.append({'pid':int(p.name),'executable':args[0],'script':script})
 if owners:reasons.append('EXISTING_DRIVING_OR_TRAINING_PROCESS')
 q=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader'],capture_output=True,text=True,timeout=10)
 if q.returncode:reasons.append('GPU_STATUS_UNAVAILABLE')
 for line in q.stdout.splitlines():
  fields=[x.strip() for x in line.split(',')]
  if len(fields)!=3:reasons.append('UNPARSEABLE_GPU_OWNER');continue
  if int(fields[0]) not in allowed_pids and 'rustdesk' not in fields[1].lower():reasons.append('OTHER_GPU_COMPUTE_OWNER:'+fields[0])
 return {'clear':not reasons,'reasons':reasons,'owners':owners,'counts':counts,'gpu_rows':q.stdout}

def load_protocol(root,expected):
 root=Path(root);p=root/'protocol.json'
 if sha(p)!=expected:raise ValueError('HPO_PROTOCOL_SHA_MISMATCH')
 spec=json.loads(p.read_text())
 if spec['status']!='LOCKED' or spec['base_recipe_sha256']!=BASE_SHA or sha(BASE_RECIPE)!=BASE_SHA:raise ValueError('BASE_RECIPE_LOCK_CHANGED')
 if sha(root/'code_lock.json')!=spec['code_lock_sha256']:raise ValueError('CODE_LOCK_CHANGED')
 for name,h in json.loads((root/'code_lock.json').read_text()).items():
  if sha(name)!=h:raise ValueError('FROZEN_HPO_SOURCE_CHANGED:'+name)
 return spec
