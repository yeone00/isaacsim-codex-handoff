"""Stdlib-only preparation runtime and durable integrations. No GPU or simulator imports."""
import fcntl,hashlib,json,os,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=Path('/home/user/hh/isaac_cosmos/sdg_final')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atomic(p,x):
 p=Path(p);q=p.with_name(p.name+'.tmp.'+str(os.getpid()))
 with q.open('x') as f:json.dump(x,f,indent=2,ensure_ascii=False,allow_nan=False);f.flush();os.fsync(f.fileno())
 os.replace(q,p)
def event(root,kind,**kw):
 row=dict(time=time.time(),kind=kind,**kw)
 with (Path(root)/'pipeline_events.jsonl').open('a') as f:
  fcntl.flock(f,fcntl.LOCK_EX);f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
 return row
def locked(path):
 f=open(path,'a');fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);return f
def protocol(root):
 root=Path(root);p=json.loads((root/'protocol.json').read_text());expected=(root/'protocol.sha256').read_text().strip()
 if sha(root/'protocol.json')!=expected:raise ValueError('PROTOCOL_HASH_MISMATCH')
 for name,h in p['code_sha256'].items():
  if sha(name)!=h:raise ValueError('CODE_SHA_MISMATCH:'+name)
 for name,h in p.get('evidence_sha256',{}).items():
  if sha(name)!=h:raise ValueError('EVIDENCE_SHA_MISMATCH:'+name)
 if p.get('research_gates_sha256') and sha(root/'research_gates.json')!=p['research_gates_sha256']:raise ValueError('GATES_SHA_MISMATCH')
 if p['execution_scope']!='PREPARATION_ONLY' or p['new_gpu_execution_authorized'] is not False:raise ValueError('SCOPE_NOT_AUTHORIZED_BY_THIS_RUNTIME')
 return p
def proc_alive(pid):
 if not isinstance(pid,int):return False
 try:return Path(f'/proc/{pid}/stat').read_text().split()[2]!='Z'
 except OSError:return False
def git(args,repo,timeout=45):
 p=subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=True,timeout=timeout,env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10'))
 if p.returncode:raise RuntimeError('GIT_'+args[0]+'_EXIT_'+str(p.returncode))
 return p.stdout.strip()
