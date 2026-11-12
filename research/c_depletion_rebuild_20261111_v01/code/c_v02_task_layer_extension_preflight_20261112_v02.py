import json,hashlib,csv
from pathlib import Path
V=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01');O=V/'task_layer_policy_v01';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for p,h in json.loads((O/'execution_extension_lock_v02.json').read_text())['code_sha256'].items():assert sha(p)==h,p
for p,h in json.loads((O/'input_contract_lock_v01.json').read_text())['input_sha256'].items():assert sha(p)==h,p
rows=list(csv.DictReader((O/'static_task_manifest.csv').open()));assert len(rows)==2250
