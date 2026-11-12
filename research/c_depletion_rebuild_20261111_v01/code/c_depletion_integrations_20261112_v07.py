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
 public_files=list(p['public_allowlist'])
 active=O/'active_execution.json'
 if active.exists():
  active_spec=json.loads(active.read_text());E=Path(active_spec['root']);auth=E/active_spec['authorization_file'];assert sha(auth)==active_spec['authorization_sha256']
  approved=json.loads(auth.read_text());assert approved['physical_motion_authorized'] is False
  public_files.extend([str(auth),str(active),str(E/'production_status.json'),str(O/'data_design_v01/design_QA.json')])
  public_files.extend(approved['code_sha256'])
  capability=E/'static_evaluation_capabilities_v01.json'
  if capability.exists():public_files.extend(json.loads(capability.read_text())['code_sha256'])
  for f in ['C_COMMON_HPO_v01/selection_lock.json','C_COMMON_HPO_v01/final_summary.json','final_C_models_lock.json','occlusion_qualification_QA_v01.json','static_pipeline_v01/result.json']:
   if (E/f).exists():public_files.append(str(E/f))
  for name in ['c_depletion_dataset_stage_results_20261111_v01.md','c_common_hpo_final_20261111_v01.md','c_depletion_static_pipeline_results_20261111_v01.md','c_depletion_generation_execution_handoff_20261111_v01.md']:
   if (R/'reports'/name).exists():public_files.append(str(R/'reports'/name))

  for f in ['static_evaluation_capabilities_v01.json','C_COMMON_HPO_v01/hpo_status.json','dataset_QA_v01/result.json']:
   if (E/f).exists():public_files.append(str(E/f))
 amendment=O/'execution_v02/bitmap_execution_amendment_v01.json'
 if amendment.exists():
  E=amendment.parent;am=json.loads(amendment.read_text());assert not am['physical_motion_authorized']
  public_files.extend(am['code_sha256']);public_files.append(str(amendment))
  for f in ['dataset_QA_bitmap_v01/result.json','bitmap_qualification_v01/CPU_result.json','bitmap_qualification_v01/dataset_CPU_result.json','C_COMMON_HPO_v02/protocol.json','C_COMMON_HPO_v02/candidates.json','C_COMMON_HPO_v02/hpo_status.json','C_COMMON_HPO_v02/selection_lock.json','C_COMMON_HPO_v02/final_summary.json','static_evaluation_capabilities_bitmap_v01.json']:
   if (E/f).exists():public_files.append(str(E/f))
  report=R/'reports/c_depletion_bitmap_recovery_handoff_20261112_v01.md'
  if report.exists():public_files.append(str(report))
 audit=O/'execution_v02/replicator_audit_handoff_v01.json'
 if audit.exists():
  ad=json.loads(audit.read_text());public_files.append(str(audit));public_files.extend(ad['public_text_files'])
 public_files.extend([str(R/'scripts/c_depletion_integrations_20261111_v04.py'),str(R/'scripts/c_depletion_watchdog_20261111_v04.py'),str(O/'runtime_amendment_v04.json'),str(R/'scripts/c_depletion_integrations_20261111_v05.py'),str(R/'scripts/c_depletion_watchdog_20261111_v05.py'),str(O/'runtime_amendment_v05.json')])
 for name in public_files+[str(R/'scripts/c_depletion_integrations_20261111_v02.py'),str(R/'scripts/c_depletion_watchdog_20261111_v02.py'),str(O/'runtime_amendment_v02.json'),str(R/'scripts/c_depletion_integrations_20261111_v03.py'),str(R/'scripts/c_depletion_watchdog_20261111_v03.py'),str(O/'runtime_amendment_v03.json')]:
  source=Path(name);assert source.is_file() and source.stat().st_size<1024*1024
  target=dest/('code/'+source.name if source.suffix=='.py' else 'documents/'+source.name)
  items[target]=source.read_bytes()
 for name in ['protocol.json','protocol.sha256','research_gates.json','pipeline_status.json','jobs.json','experiment_manifest.csv','integration_errors.jsonl']:
  source=O/name
  if source.exists():items[dest/'status'/name]=source.read_bytes()
 hpo=Path(p['hpo_root'])/'hpo_status.json'
 if hpo.exists():items[dest/'status/hpo_status.json']=hpo.read_bytes()
 # Secret scan every proposed text. Existing project status has already been published by its original hook.
 secret_patterns=[r'(?m)^-----BEGIN [A-Z ]*PRIVATE KEY-----$',r'gh[pousr]_[A-Za-z0-9_]{20,}',r'github_pat_[A-Za-z0-9_]+',r'Bearer\s+[A-Za-z0-9_.-]{16,}',r'https?://[^\s/]+:[^\s/@]+@',r'ntfy\.sh/[A-Za-z0-9_-]+']
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
