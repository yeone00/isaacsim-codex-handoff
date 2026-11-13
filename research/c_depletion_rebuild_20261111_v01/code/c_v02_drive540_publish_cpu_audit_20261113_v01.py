"""Publish only explicitly listed CPU audit text; uses existing Git lock/checkout. No experiments."""
from pathlib import Path
import sys,json,re,time,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from c_depletion_runtime_20261111_v01 import R,git,locked
O=R/'reports/c_v02_drive540_storage_curvature_audit_20261113_v01';repo=Path('/home/user/hh/isaacsim-codex-handoff')
lock=locked(repo/'.git/c_depletion_publish.lock')
assert re.search(r'github\.com[:/]yeone00/isaacsim-codex-handoff(?:\.git)?$',git(['remote','get-url','origin'],repo))
assert not git(['diff','--name-only'],repo) and not git(['diff','--cached','--name-only'],repo)
git(['fetch','origin','main'],repo);git(['merge','--ff-only','origin/main'],repo)
files=[R/'reports/c_v02_drive540_storage_and_curvature_audit_20261113_v01.md',R/'docs/PROJECT_STATE.md',R/'analysis/c_v02_drive540_storage_audit_20261113_v01.py',R/'analysis/c_v02_drive540_curvature_audit_20261113_v01.py',Path(__file__).resolve()]
files += [p for p in O.iterdir() if p.suffix in ('.csv','.json','.txt') and p.stat().st_size<1024*1024 and p.name!='github_sync_receipt.json']
base=Path('research/c_depletion_rebuild_20261111_v01');tracked=[]
for src in files:
 assert src.stat().st_size<1024*1024
 text=src.read_text()
 for pat in [r'gh[pousr]_[A-Za-z0-9_]{20,}',r'github_pat_[A-Za-z0-9_]+',r'Bearer\s+[A-Za-z0-9_.-]{16,}',r'https?://[^\s/]+:[^\s/@]+@',r'ntfy\.sh/[A-Za-z0-9_-]+']:
  assert not re.search(pat,text),'SECRET_SCAN_REJECTED'
 target=base/('code' if src.suffix=='.py' else 'documents')/src.name
 (repo/target).parent.mkdir(parents=True,exist_ok=True);(repo/target).write_text(text);tracked.append(str(target))
git(['add','--',*tracked],repo)
assert all(x in tracked for x in git(['diff','--cached','--name-only'],repo).splitlines())
if git(['diff','--cached','--name-only'],repo):git(['commit','-m','C-V02 CPU-only audit: storage budget and curvature rejections; main HOLD'],repo)
git(['push','origin','main'],repo,90);local=git(['rev-parse','HEAD'],repo);remote=git(['ls-remote','origin','refs/heads/main'],repo).split()[0];assert local==remote
receipt=dict(state='VERIFIED',local_commit=local,remote_commit=remote,files=len(tracked),time=time.time(),no_new_motion=True,excluded_file='storage_files_16_runs.csv (>1MiB; local preserved)')
(O/'github_sync_receipt.json').open('x').write(json.dumps(receipt,indent=2));print(json.dumps(receipt))
