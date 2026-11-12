"""CPU report: statewise/pooled/equal-C AP, family-clustered uncertainty, pose and model lineage."""
import json,csv,collections,statistics,random,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];B=Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01');V=B/'C_V02_20261112_v01';O=V/'integrated_report_v01';O.mkdir(exist_ok=False);sel=json.loads((V/'MIX_C06_20261112_v01/selection_lock.json').read_text());summary=[];bootstrap=[];levels=['C100','C80','C60','C40','C20']
def table(name,rows):
 if not rows:return
 with (O/name).open('x',newline='') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
for role in ['selected_mixture','synthetic_baseline']:
 root=V/(role+'_eval_v01')
 if (root/'verified_reuse.json').exists():root=V/'selected_mixture_eval_v01'
 ap=list(csv.DictReader((root/'perception_eval_v01/mask_AP.csv').open()));rows=list(csv.DictReader((root/'perception_eval_v01/per_target.csv').open()));groups=collections.defaultdict(dict)
 for a in [z for z in ap if not z['C'].startswith('ANCHOR_')]:groups[a['model_rep'],a['seed'],a['eval_rep'],a['O']][a['C']]=a
 for key,g in groups.items():
  assert set(g)==set(['ALL']+levels)
  r=dict(role=role,model_rep=key[0],seed=key[1],eval_rep=key[2],O=key[3],attempted_images=250,independent_base_families=10)
  for metric in ['target_mask_mAP50','target_mask_mAP5095','all_mask_mAP50','all_mask_mAP5095']:
   vals=[float(g[c][metric]) if g[c][metric] else None for c in levels];r['pooled_'+metric]=g['ALL'][metric];r['equal_C_macro_'+metric]=sum(vals)/5 if all(x is not None for x in vals) else None
  summary.append(r)
 for rep in ['HR_Scan','LR_Scan','GeoCAD']:
  for oc in ['O0','O25','O50']:
   for c in levels:
    rr=[r for r in rows if r['model_rep']==rep and r['eval_rep']==rep and r['O']==oc and r['C']==c];assert len(rr)==150 # 50images x3 seeds, still only10 families
    fam=collections.defaultdict(list)
    for r in rr:fam[r['family_id']].append(r)
    assert len(fam)==10
    for metric in ['target_detected','top1_target','top1_target_iou']:
     def value(r):return float(r['target_detected']=='True') if metric=='target_detected' else float(r['top1_class']=='TARGET') if metric=='top1_target' else float(r['top1_target_iou'])
     vals=[statistics.mean(value(r) for r in fr) for fr in fam.values()];rng=random.Random(20261112);b=sorted(statistics.mean(rng.choices(vals,k=10)) for i in range(2000));bootstrap.append(dict(role=role,rep=rep,O=oc,C=c,metric=metric,mean=statistics.mean(vals),CI95_low=b[49],CI95_high=b[1949],independent_families=10,observations_per_seed=50,seeds=3,uncertainty='family-cluster percentile bootstrap; seed dependence retained within family; seed SD separate'))
 table(role+'_state_AP.csv',ap)
table('pooled_vs_equal_state_macro.csv',summary);table('family_cluster_uncertainty.csv',bootstrap)
report=R/'reports/c_v02_final_mixing_perception_pose_integrated_20261112_v01.md'
report.write_text('# C-V02 균형 데이터·혼합 비율·정적 평가 통합 결과\n\n'+json.dumps(dict(selected_ratio=sel['ratio'],scores=sel['scores'],training_trajectories=39,source_C_HPO_repeated=False,O0_dataset=5250,O0_train=3750,O0_val=750,O0_test=750,occluded_Test=1500,Test_total=2250,independent_source_families=70,independent_Test_families=10,physical_runs=0,physical_stages='HOLD'),indent=2,ensure_ascii=False)+'\n\n표/조건별분모/cluster불확실성: '+str(O)+'. AP는pooled와각C동일1/5macro를구분한다. Test50행/상태/표현은10family×5relatedobservations이며독립50환경아님. C100만카메라거리관측이다양해진교란을명시하며원래anchor관측의대응비교와추가view결과를분리해해석한다.\n\nRoboflow는기존target-only라벨·다른포장대형블록제품/현장도메인이며원래unwrapped red brick과동일재료실세계일반화/로봇배포검증이아니다. Real Test189이전노출보존/새blind주장없음. Test로모델재선정하지않는다. 위치추정실패는조건부오차평균에서제외하고전체시도성공률과구분한다. ROBUST_A .144m site-prior는현장인증UNKNOWN,GT C/slot/pose운용입력없음. 안전/성공판정/기술파일럿미확정으로본300/별도150HOLD유지.\n')
(O/'result.json').write_text(json.dumps(dict(state='COMPLETED',report=str(report),physical_stages='HOLD'),indent=2))
with (R/'docs/PROJECT_STATE.md').open('a') as f:f.write('\n\n## C-V02 혼합·정적 평가 자동 완료\n\n- reports/c_v02_final_mixing_perception_pose_integrated_20261112_v01.md; 물리실행0/HOLD.\n')
