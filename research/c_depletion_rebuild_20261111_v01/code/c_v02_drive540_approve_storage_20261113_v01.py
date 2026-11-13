"""Manual explicit researcher authorization ONLY after dedicated volume directory is provisioned.
Does not mount, format, change ownership, delete files, or start a GPU process directly.
"""
import argparse,json,subprocess,shutil,time,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--approve-storage-for-c540',action='store_true',required=True);a=p.parse_args()
D=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01');T=D/'technical_policy_amendment_v01';s=json.loads((T/'storage_plan_v01.json').read_text());dest=Path(s['destination']);assert dest.is_dir() and os.access(dest,os.W_OK),'Dedicated directory missing or not writable; administrator must create ONLY that directory first.'
uuid=subprocess.check_output(['findmnt','--noheadings','--output','UUID','--target',str(dest)],text=True).strip();assert uuid==s['volume_uuid'],'Wrong filesystem UUID';assert shutil.disk_usage(dest).free>s['required_main_bytes_with_margin'],'Insufficient free space'
out=Path(s['approval_file']);assert not out.exists(),'Authorization already exists; controller will verify storage itself';out.write_text(json.dumps(dict(approved_by_researcher=True,approval_method='explicit manual --approve-storage-for-c540 invocation',scope='new C540 evidence directory only; no formatting/deletion/original-data migration',volume_uuid=uuid,destination=str(dest),created=time.time()),indent=2));print('Storage authorized. Independent controller checks all existing scientific/safety gates before main540. No experiment settings changed.')
