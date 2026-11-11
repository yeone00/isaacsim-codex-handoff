"""Reuse original ntfy hook/config and existing GitHub checkout. No credentials copied/published."""
import importlib.util,json,os,re,shutil,time
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,git,locked
HOOK=Path.home()/'.claude/hooks/isaacsim/ntfy_notify.py'
def notify(title,body,high=False):
 spec=importlib.util.spec_from_file_location('existing_ntfy_hook',HOOK);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 return bool(m.send(title,body,priority='high' if high else 'default',tags='warning' if high else 'information_source'))
def publish(root):
 O=Path(root);repo=Path('/home/user/hh/isaacsim-codex-handoff');l=locked(repo/'.git/c_depletion_publish.lock')
 origin=git(['remote','get-url','origin'],repo)
 assert re.search(r'github\.com[:/]yeone00/isaacsim-codex-handoff(?:\.git)?$',origin),'UNEXPECTED_REMOTE'
 assert not git(['diff','--name-only'],repo) and not git(['diff','--cached','--name-only'],repo),'EXISTING_TRACKED_CHANGES'
 git(['fetch','origin','main'],repo);git(['merge','--ff-only','origin/main'],repo)
 dest=repo/'research/c_depletion_rebuild_20261111_v01';dest.mkdir(parents=True,exist_ok=True);items={}
 p=json.loads((O/'protocol.json').read_text())
 for name in p['public_allowlist']:
  source=Path(name);assert source.is_file() and source.stat().st_size<1024*1024
  target=dest/('code/'+source.name if source.suffix=='.py' else 'documents/'+source.name)
  items[target]=source.read_bytes()
 for name in ['protocol.json','protocol.sha256','research_gates.json','pipeline_status.json','jobs.json','experiment_manifest.csv']:
  source=O/name
  if source.exists():items[dest/'status'/name]=source.read_bytes()
 hpo=Path(p['hpo_root'])/'hpo_status.json'
 if hpo.exists():items[dest/'status/hpo_status.json']=hpo.read_bytes()
 # Secret scan every proposed text. Existing project status has already been published by its original hook.
 secret_patterns=[r'-----BEGIN .*PRIVATE KEY',r'gh[pousr]_[A-Za-z0-9_]{20,}',r'github_pat_[A-Za-z0-9_]+',r'Bearer\s+[A-Za-z0-9_.-]{16,}',r'https?://[^\s/]+:[^\s/@]+@',r'ntfy\.sh/[A-Za-z0-9_-]+']
 for data in items.values():
  text=data.decode('utf-8');assert not any(re.search(pattern,text) for pattern in secret_patterns),'PUBLIC_SECRET_SCAN_REJECTED'
 tracked=[]
 for target,data in items.items():
  target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists() or target.read_bytes()!=data:target.write_bytes(data)
  tracked.append(str(target.relative_to(repo)))
 git(['add','--',*tracked],repo)
 staged=git(['diff','--cached','--name-only'],repo)
 if staged:
  assert all(n.startswith('research/c_depletion_rebuild_20261111_v01/') for n in staged.splitlines())
  git(['commit','-m','Research preparation: C depletion protocol, gates and status'],repo)
 git(['push','origin','main'],repo,90);local=git(['rev-parse','HEAD'],repo);remote=git(['ls-remote','origin','refs/heads/main'],repo).split()[0]
 assert local==remote,'REMOTE_COMMIT_NOT_VERIFIED'
 return dict(state='VERIFIED',commit=local,remote_commit=remote,repository='yeone00/isaacsim-codex-handoff',published_files=len(tracked),time=time.time())
