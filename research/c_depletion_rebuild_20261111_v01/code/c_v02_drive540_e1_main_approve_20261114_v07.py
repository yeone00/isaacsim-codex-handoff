"""Researcher-only authorization for the E1 main controller v07 (v07 = v06 approve script with v07 file names) (2026-11-14). Run ONLY by the researcher, explicitly, after approving
the E1 protocol amendment, the manifest, and the validated runtime-option lock. Creates main_authorization_v07.json bound to the lock SHA.
Does not start anything, never touches Codex v04 files (and refuses if v04's storage authorization exists)."""
import argparse, hashlib, json, time
from pathlib import Path
E1 = Path('/home/user/hh/isaac_cosmos/sdg_final/C_V02_DRIVE540_E1_20261114_v01')
V04 = Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01')
p = argparse.ArgumentParser(); p.add_argument('--approve-e1-main540-v07', action='store_true', required=True); p.add_argument('--lock', type=Path, required=True); a = p.parse_args()
assert not (V04 / 'technical_policy_amendment_v01/storage_authorization.json').exists(), 'v04 storage authorization exists: resolve before E1 main'
lock = json.loads(a.lock.read_text()); assert lock.get('schema', '').startswith('C540_E1_MAIN_EXECUTION_LOCK_FINAL'), 'only a FINAL lock can be authorized'
assert 'runner_script' not in lock and 'assess_module' not in lock and lock.get('notify', True), 'mock/test keys present'
out = Path(lock['state_dir']) / 'main_authorization_v07.json'; out.parent.mkdir(parents=True, exist_ok=True); assert not out.exists(), 'authorization already exists'
out.write_text(json.dumps(dict(approved_by_researcher=True, method='explicit --approve-e1-main540-v07', lock=str(a.lock), lock_sha256=hashlib.sha256(a.lock.read_bytes()).hexdigest(),
                               manifest_sha256=lock['manifest_sha256'], amendment_sha256=lock['amendment_sha256'], runtime_flags=lock['runtime_flags'], created=time.time()), indent=1))
print('E1 main540 authorized for this lock only. Start controller v07 separately.')
