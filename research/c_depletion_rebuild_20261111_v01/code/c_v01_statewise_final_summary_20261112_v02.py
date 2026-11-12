"""Read-only CPU summary after static completion; no model or experiment control."""
import csv,json,time,statistics,collections,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02');out=E/'statewise_reporting_v01';out.mkdir(exist_ok=True)
while not (E/'post_hpo_static_bitmap_v01/result.json').exists():time.sleep(60)
assert json.loads((E/'post_hpo_static_bitmap_v01/result.json').read_text())['state']=='COMPLETED'
aps=list(csv.DictReader((E/'perception_eval_v01/mask_AP.csv').open()));targets=list(csv.DictReader((E/'perception_eval_v01/per_target.csv').open()));levels=['C100','C80','C60','C40','C20'];groups=collections.defaultdict(dict)
for r in aps:groups[(r['model_rep'],r['seed'],r['eval_rep'],r['O'])][r['C']]=r
rows=[];strata=[]
for key,g in groups.items():
 assert set(g)==set(['ALL']+levels)
 rr=[r for r in targets if (r['model_rep'],r['seed'],r['eval_rep'],r['O'])==key]
 assert len(rr)==210
 for c in levels:
  tr=[r for r in rr if r['C']==c];expected=10 if c=='C100' else 50;assert len(tr)==expected and len({r['family_id'] for r in tr})==10
  eligible=[r for r in tr if r['target_eligible']=='True'];hit=lambda r:r['target_detected']=='True'
  strata.append(dict(model_rep=key[0],seed=key[1],eval_rep=key[2],O=key[3],C=c,attempted_images=len(tr),independent_base_families=10,target_eligible=len(eligible),target_detected_all=sum(map(hit,tr)),target_detected_eligible=sum(map(hit,eligible)),top1_target=sum(r['top1_class']=='TARGET' for r in tr),target_GT_denominator=g[c]['target_GT_denominator'],all_GT_denominator=g[c]['all_GT_denominator'],target_mask_mAP5095=g[c]['target_mask_mAP5095'],all_mask_mAP5095=g[c]['all_mask_mAP5095']))
 z=dict(model_rep=key[0],seed=key[1],eval_rep=key[2],O=key[3],attempted_images=210,independent_base_families=10)
 for kind in ['all','target']:
  metric=kind+'_mask_mAP5095';vals=[float(g[c][metric]) if g[c][metric] else None for c in levels]
  z['pooled_'+metric]=g['ALL'][metric];z['equal_state_macro_'+metric]=sum(vals)/5 if all(v is not None and math.isfinite(v) for v in vals) else None
  z['macro_defined_states']=sum(v is not None for v in vals);z['macro_rule']='exact 1/5 per C; undefined if any state undefined'
 rows.append(z)
for name,data in [('statewise_metrics.csv',strata),('pooled_vs_equal_state_macro.csv',rows)]:
 p=out/name
 with p.open('x',newline='') as f:w=csv.DictWriter(f,list(data[0]));w.writeheader();w.writerows(data)
report=R/'reports/c_v01_final_statewise_perception_summary_20261112_v01.md'
report.write_text('# C-V01 final statewise perception summary\n\nO0 origin dataset4410=Train3150/Val630/Test630. No C100 expansion/B1 L4 combination. O25/O50 are Test-only paired evaluations, never HPO/training inputs.\n\nPer model/evaluation representation/occlusion/seed: pooled210images vs equal-state mean of5APs, C10010images and each other C50images, all10basefamilies. Raw source '+str(out)+'. Seed repetitions and paired HR/LR/CAD observations do not increase independent environment count. C100 Test has only10observations; uncertainty is limited and repeated views/shapes are not independent. Pooled AP is not an arithmetic image-weighted mean of state AP. Macro AP is explicitly equal1/5; any undefined state means undefined macro. No post-Test model/hyperparameter selection.\n\nPhysical pilot300/150 HOLD maintained.\n')
(out/'result.json').write_text(json.dumps(dict(state='COMPLETED',per_state_rows=len(strata),pooled_macro_rows=len(rows),report=str(report),physical_runs=0),indent=2))
