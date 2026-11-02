# v42 — AMP 실제 갱신 PASS, Ray 복원 후 optimizer 진행 미입증으로 full epoch 중단

2026-11-02 KST. **STAGE1_READY=NO / STAGE1_TECHNICAL_READY=NO.** v41c의 초기 scaler128은 두 mask ratio에서 첫 실제 AdamW update를 통과했다. Ray는 같은 trial로 epoch2를 완료하고 raw optimizer/model/EMA/scaler/scheduler를 정확히 복원했다. 다만 epoch2에서 optimizer step이 증가하지 않아 요청한 재개 후 학습 진행 증명을 충족하지 못했다. **추가 실행 없이 중단: full Train6000/Val1200 epoch NOT_RUN, HPO launched/completed/pruned/errored 모두0.** 이것은 AMP 비호환 또는 optimizer 복원 손상이라는 결론이 아니다.

## 실제 실행·게이트

새 ROOT: `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v42`. 기존 v39/v40/v41 output 및 원본 소스는 덮어쓰지 않았다. 정책 `PROSPECTIVE_BITMAP_NOAUG_v41`, class0 brick_load, HR_Scan/LR_Scan/GeoCAD 및 red/cement 공통 square letterbox/nearest bitmap/noaug 유지. GPU batch64/workers8/AMP/AdamW/640/seed42 유지. full pilot mask_ratio=2를 실행 전 코드에 고정했고, 실제 실행은 하지 않았다.

| 관문 | 판정 | 실제 증거 |
|---|---|---|
| 입력/보존·새 namespace | PASS | init exit0, 기존 inventory/records/manifest/코드 및 previous provenance 총64개 참조 expected=observed. 7200 records, Train2000×3/Val400×3 pairing 검사. GPU compute 경쟁작업 없음, Kit executable 없음, 수동 process 목록에서도 ROS 작업 미관측 |
| ratio2 CPU preflight | PASS | 기존 v41c 필수6이미지/2scene×3rep canonical nearest reference 및 실제 loss selector exact. exit0 |
| ratio2 GPU 한 번 | PASS | 첫 step에서 state290/step1/파라미터290개 변경/finite weights |
| ratio4 CPU preflight | PASS | ratio4의 올바른160² reference exact 및 실제 loss selector. exit0 |
| ratio4 GPU 한 번 | PASS | 첫 step에서 state290/step1/파라미터290개 변경/finite weights |
| Ray 동일 trial 복원·2 checkpoints | PASS | trial `f2db5f54`, Tuner.restore, epoch0→start_epoch1, model/EMA/optimizer/scaler/scheduler exact assertions, checkpoint2개 |
| Ray 복원 뒤 실제 optimizer 진행 | **FAIL (미입증)** | epoch2 완료에도 optimizer step1→1 / 모든 AdamW state tensor 동일 / scaler growth_tracker1→1. 따라서 통합 Ray 관문 FAIL |
| 전체6000/1200 1 epoch | **NOT_RUN** | train0/6000, val0/1200; loss/metric/VRAM/walltime 측정 없음 |
| Stage1 40 trials | **NOT_RUN** | launched/completed/pruned/errored0. 별도 engineering trial1개를 HPO trial로 합산하지 않음 |

## AMP 실측

각 GPU는 distinct64 이미지·두 재료·세 표현이며 실행 attempt1/exit0. v42 사본은 기존 v41c의 비유한 gradient assertion을 제거하고 최대12 step 한정으로 정상 scaler.step/skip/update를 허용했다. 실제 두 실행은 첫 step에 성공하여 추가 step·overflow skip·재시도는 모두0이다. 초기 scale128 외 optimizer/loss/데이터 설정은 유지했다. 가중치 tensor 전체 finite 검사, optimizer step counter, 전후 파라미터 비교를 함께 수행했다.

| mask_ratio | 상태 / attempt / exit | train seg loss | 첫 성공 step / AdamW counter / state수 | 변경 tensor수 | scaler / skip수 | 단일step images/s | gate wall초 | peak allocated / reserved bytes |
|---|---|---:|---|---:|---|---:|---:|---|
| 2 | PASS / 1 / 0 | 3.261194944 | 1 / 1.0 / 290 | 290 | 128→128 / 0 | 51.969 | 5.365702 | 12070773760 / 12322865152 |
| 4 | PASS / 1 / 0 | 3.416858912 | 1 / 1.0 / 290 | 290 | 128→128 / 0 | 55.660 | 5.175161 | 9537396736 / 11377049600 |

ratio2/4 비유한 gradient tensor0/0, finite gradient absmax 113.875/114.75. 전체 loss vector/항목별 loss, 현재 allocated/reserved, 정확한 canonical pixel/instance selector 증거는 각 `gpu_ratio*/status.json`에 보존했다. images/s는 단일 forward/backward/update 측정이며 데이터 전체 학습 throughput으로 외삽하지 않는다. CPU seg loss는 ratio2 4.261906623840332, ratio4 4.844833850860596이다.

## Ray의 성공 범위와 실패 원인 한 가지

prepared v41c adapter의 새 v42 사본에서 raw float32 optimizer·live model·EMA·scaler·scheduler·실제 update counter를 `raw_state.pt`로 별도 저장하고 정확히 복원했다. 설치 Ultralytics의 last.pt는 optimizer를 fp16으로 직렬화하며 마지막 final_eval에서 strip할 수 있으므로 Ray report 전에 복사하고 raw 상태를 별도로 보존했다. raw 복원을 사용해 model/EMA와 AdamW `step`, `exp_avg`, `exp_avg_sq`를 tensor별 exact 비교했다. Scaler/scheduler도 state_dict exact 비교 PASS. last.pt checkpoint hash는 복원 직전 시작 callback에서 첫 저장 hash와 같았다. 두 번째 raw checkpoint hash 변경만을 optimizer 진행으로 해석하지 않았다.

| 완료 epoch | AdamW state수 / counter | scaler / growth_tracker | scheduler last_epoch / step_count | raw checkpoint SHA256 |
|---|---|---|---|---|
| 1 | 290 / 1.0 | 128.0 / 1 | 0 / 2 | `1bc6a06b06d818d04d5a845395729dbc7f32a8936d4fe3f226bc4f2a9750e6cf` |
| 2 | 290 / 1.0 | 128.0 / 1 | 1 / 3 | `fde130bf888d081cce5fb65a75f697c8bf58cf894c07ddf91cb7305cd4a9eaba` |

last.pt epoch1 SHA `6cda7db72052f0c32e0d76217718f00b90830df805f5300662fc7b560ed090dc`, epoch2 SHA `112b62c469fafcd978f250a687918c141995f88f4aedd33a17e2450b770ad797`. checkpoint 디렉터리는 `ray_engineering/trial_f2db5f54_*/checkpoint_000000` 및 `checkpoint_000001`. `ray_interrupt.json`에 첫 checkpoint 뒤 의도한 driver SIGINT를 기록했고 start driver/restore driver 모두 exit0이었다. 기존 errored v41 trial을 재실행하지 않았다. 실제 새 engineering trial은1개이며 같은 ID로 training_iteration1→2, start_epoch1→epoch2, epoch0 반복/phantom 새 trial 없음. 첫 구간 wall 21.619초(중단 정리 포함), 복원 구간 wall 12.180초. Ray 자체 보고 누적 iteration 시간8.810478초. scheduler는0→1로 진행했다. ASHA pruning은 **NOT_DEMONSTRATED**이며 두 epoch 완료를 pruning 증명으로 부르지 않는다.

고정 engineering Train9/Val6의 metric selector는 `metrics/mAP50-95(M)`이며 epoch1/2 pooled 값은 둘 다0.00060(보고 반올림)이다. Val seg46.71218 역시 engineering 관측으로 기록하며 과학적 성능·비열등성 결론이나 모델 선택에 쓰지 않는다.

**정확한 원인:** tiny Ray 시험은 batch6, 설치 trainer 기본 nbs64, Train9이므로 epoch당2 minibatch다. resume 때 `accumulate=round(64/6)=11`로 시작하고 마지막 epoch라 warmup이 끝난다. epoch2의 global batch index ni=2,3, 지역 `last_opt_step=-1`에서 차이는3,4로11보다 작다. 따라서 optimizer_step을 호출하지 않는다. checkpoint 두 개의 모든 AdamW state tensor가 동일하고 scaler growth_tracker도1→1인 증거와 일치한다. 손상된 optimizer state가 원인이 아니라 **작은 시험 구성과 gradient accumulation의 조합**이 재개 후 update 증명을 막았다. 누적 gradient/last_opt_step 자체의 연속성도 저장하지 않았으므로 bitwise 학습 trajectory 동등성은 주장하지 않는다.

**다음 정확한 패치 한 가지:** 후속 새 버전 tiny trial의 train subset을 이미 검증한 `batch64_records.json`의64개 distinct 이미지로 바꾸고 `batch=64, workers=8`을 사용한다. 구체적으로 `selected = json.loads((ROOT/'batch64_records.json').read_text()) + [r for r in rr if r['scene_id'] in valids]` 및 trial kw의 `batch=64, workers=8`로 바꾸면 nbs64에서 accumulate1로 두 epoch 각각 실제 update를 할 수 있다. report assertion에 `resumed epoch optimizer_step > saved optimizer_step`를 추가한다. 이는 후속 새 engineering 시험의 수정 제안이며 **이번 v42 trial을 수정·재실행하지 않았다**. 성공을 미리 보장하지 않는다.

## 파일·명령·환경·보존

신규 코드: `scripts/bitmap_qualify_v42c.py`, `scripts/bitmap_ray_resume_v42c.py`, `scripts/bitmap_full_epoch_v42c.py`. 마지막 파일은 조건부 1 epoch 경로를 준비하고 compile만 했으며 실행0이다. 코드의 full pilot hyperparameters는 lr0=.001/lrf=.1/momentum=.9/weight_decay=.0005/warmup_epochs3/box7.5/cls.5/dfl1.5, batch64/workers8/ratio2로 고정되어 있고 성능에 따라 선택하지 않았다. 실제 Stage1 entrypoint `bitmap_stage1_v40.py`는 여전히 v42 raw optimizer/scaler adapter로 연결되지 않았으므로 이를 실행하면 안 된다. technical readiness를 YES로 올리지 않았다.

실제 명령은 아래이며 `command_*.json`에 절대 Python 경로·return code·start/end, `raw_*.stdout.log`와 `raw_*.stderr.log`에 원문을 보존했다.

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v42c.py init
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v42c.py cpu --ratio 2
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v42c.py gpu --ratio 2
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v42c.py cpu --ratio 4
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v42c.py gpu --ratio 4
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_ray_resume_v42c.py
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_ray_resume_v42c.py --resume
```

Python3.11.15 / Ultralytics8.4.129 / Ray2.58.0 / torch2.7.1+cu128 / CUDA12.8 / RTX5090 / driver570.172.08. `environment.json`, `environment_versions.json`, GPU 전후 snapshot, input_hashes.json, previous_provenance.json, preservation_checks.json, ray_gate.json, status.json, delivery_sha256.json을 ROOT에 기록했다. 로그의 Ultralytics upgrade 알림은 설치/업그레이드 실행이 아니다. 설치0, OOM0, terminal exception0, 의도 SIGINT1, Ray trial ERROR0; 이와 별개로 필수 optimizer 진행 관문은 FAIL로 보존했다. 사전/사후 입력 SHA64참조 일치, 새 세 코드 py_compile PASS. v40 전체7200 QA 재실행0, METADATA_SHORT_HASH_ALGORITHM_UNKNOWN 유지. 기존 v39/v41 실제 실패와 원본 source/weights/labels/splits/USD 보존.

Full pilot의 과학적 단위는 실행할 경우 Train2000 paired scene×3=6000 이미지, Val400×3=1200 이미지다. 이번에는 해당 실행0이며 n6000 독립 scene 또는 최종 benchmark 성능을 주장하지 않는다. Test1200/Real Test189 접근·선택·평가0(Real Test189 기존 평가 이력은 유지). Kit0/ROS0/motion0/asset retune0, steering HOLD, v30 physical n1/v31-v32 curvature FAIL/v35-v36 offline/v40 QA 완료는 불변. 연구 confirmatory 분모0. 보고서·latest_report·PROJECT_STATE를 갱신하고 정상 HANDOFF_REPORT marker로 동기화를 요청한다. 원격 반영 완료는 로컬에서 확인하지 않았다.
