"""Human status; no experiment launches."""
import argparse,json,datetime
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args()
for name in ['pipeline_status.json','watchdog_status.json','github_sync_status.json']:
 p=a.root/name
 print('\n'+name)
 if not p.exists():print('NOT_YET');continue
 d=json.loads(p.read_text());print(json.dumps(d,ensure_ascii=False,indent=2))
