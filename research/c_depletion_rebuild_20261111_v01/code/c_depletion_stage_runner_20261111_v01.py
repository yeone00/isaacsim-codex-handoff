"""Actual CPU verification stages only. Future GPU stage adapters deliberately absent."""
import argparse,ast,json,sys,time,xml.etree.ElementTree as ET
from pathlib import Path
from c_depletion_runtime_20261111_v01 import R,sha,atomic,protocol
a=argparse.ArgumentParser();a.add_argument('--root',type=Path,required=True);a.add_argument('--job',choices=['stage0_existing_evidence','preparation_document_gates'],required=True);a.add_argument('--output',type=Path,required=True);o=a.parse_args();p=protocol(o.root);o.output.mkdir(exist_ok=False)
checks={};started=time.time()
try:
 if o.job=='stage0_existing_evidence':
  E=R/'reports/progressive_depletion_design_audit_evidence_20261111_v01'
  prior=json.loads((E/'audit_result.json').read_text());assert prior['state']=='PASS'
  n=0
  for path,h in json.loads((E/'inputs_sha256.json').read_text()).items():
   if '/B1_COMMON_HPO_' in path:continue
   assert sha(path)==h,path;n+=1
  pair=json.loads((E/'manifest_to_trajectory_pairing.json').read_text());assert pair['state']=='PASS'
  checks=dict(immutable_inputs=n,prior_200_histories_pass=True,manifest_to_rep_metadata=True,known_duplicate_retained='MNIDB_0006 C20 T02/T05; not silently reseeded')
 else:
  for name,h in p['preparation_documents'].items():assert sha(name)==h,name
  critical=json.loads((o.root/'research_gates.json').read_text())
  assert critical['success_threshold']['status']=='UNRESOLVED' and critical['new_gpu_authorization']['status']=='NOT_AUTHORIZED'
  assert p['main_runs']==300 and p['main_group']=='G1_ROBUST_A_single_observation'
  assert p['soft_budget_hours']==48 and not p['stop_at_budget']
  ET.parse(R/'reports/progressive_depletion_design_audit_evidence_20261111_v01/existing_first_environment_5seed_top_slots.svg')
  checks=dict(documents_hash_verified=True,main_denominator=300,scope='PREPARATION_ONLY',research_hold_is_required=True,no_gpu_stage_adapter=True)
 atomic(o.output/'result.json',dict(state='COMPLETED',job=o.job,checks=checks,started=started,ended=time.time(),new_render=0,new_training=0,new_drive=0))
except BaseException as e:
 atomic(o.output/'result.json',dict(state='FAILED',job=o.job,error=type(e).__name__,started=started,ended=time.time()));raise
