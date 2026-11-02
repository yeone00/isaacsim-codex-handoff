# v41 — 실제 HPO 자격검증 실패, Stage-1 미시작

2026-11-02 KST. **STAGE1_READY=NO.** 두 ratio의 CPU 실제 loss 입력은 PASS이나, batch64 AMP 역전파 후 비유한 gradient가 검출됐다. 독립 Ray 시험은 같은 trial/epoch/YOLO 가중치 복구까지 확인했으나 optimizer state가 비어 있어 FAIL이다. 허용된 실행 한도를 지켜 GPU 재시도0, Ray 수정검증1회 뒤 종료했다. **Full-data epoch NOT_RUN / 실제 HPO launched·running·completed·pruned·failed 모두0.** 이는 AMP의 근본적 비호환이나 데이터 손상 판정이 아니다.

| 필수 게이트 | 결과와 실제 분모 |
|---|---|
| v40 보존·입력 코드 SHA | PASS: inventory53항목(중복 포함) 시작·종료 일치, legacy source4개 expected 일치. Known locks9/hash 및108·432행 PASS. v40 QA/smoke 재실행0 |
| 새 정책 고정 | PASS: `PROSPECTIVE_BITMAP_NOAUG_v41`, 세 표현 공통. 탐색 실행은 사용자 v41 지시 범위이며 **최종 학위논문 정책 채택은 검토 대기** |
| ratio2 CPU loss | PASS: 실제 bridge2scene×3rep=6장/27instance channel, target320²·reference error0/IoU1, installed loss selector6/6·positive anchors242, seg loss **4.261906624** |
| ratio4 CPU loss | PASS: 동일6장/27channel, target160²·error0/IoU1, selector6/6·anchors242, seg loss **4.844833851** |
| ratio2 GPU batch64 | **FAIL**, attempt1/exit1, 64 DISTINCT train images·workers8·AMP·nc1·640/AdamW. finite loss와 backward 완료 후 unscaled gradient assertion. 5.034743s, peak allocated **12,060,274,688 B (11.23 GiB)** / reserved **12,312,379,392 B** |
| ratio4 GPU batch64 | **FAIL**, attempt1/exit1, 동일64장/설정. 같은 assertion, 4.844988s, peak allocated **9,522,654,208 B (8.87 GiB)** / reserved **11,368,660,992 B** |
| Ray/ASHA/TPE end-to-end | **FAIL**. 첫 API binding 실패는 trial0. 수정 adapter로 실제 engineering trial1, epoch checkpoint1개 후 의도적 SIGINT·동일 root Tuner.restore. epoch2 진입 전 optimizer 검증 실패, 최종 ERROR1/완료0, 두 번째 checkpoint0 |
| Full Train6000/Val1200 epoch | **NOT_RUN**: 앞선 필수 게이트 실패. throughput/full-val score UNKNOWN |
| 실제40-trial Stage1 | **NOT_RUN**, PID 없음·백그라운드 작업 없음. 연구 confirmatory 분모0 |

## 실제 증거와 실패의 의미

외부 ROOT는 [/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41). [기계 판정·실측](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/final_evidence.json), [최종 상태](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/status.json), [입력 SHA](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/input_hashes.json), [최종 전달 SHA](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/delivery_sha256.json). 원본 v40 전체QA7200/7200·unique7139/nonexact350/IoU<.95=31·smoke PASS1/1은 입력 증거 SHA로 보존했다. metadata short canonical hash generator UNKNOWN은 그대로다. 이번에 전량 image QA를 반복하거나 Test400/Real Test189로 선택하지 않았다. Frozen manifest SHA `2a4782911ef334fc640e9f90ee8120e48ab3c30e25da47603004978835626bf8`; records SHA `e230ae083b4608428c4c1db94e6aca78484d8c0bd81477fc4e98c71fed352009`.

CPU [ratio2](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/cpu_ratio2/status.json) / [ratio4](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/cpu_ratio4/status.json)는 canonical→letterbox→nearest reference→실제 batch→설치 loss의 `single_mask_loss` 입력을 비교했다. batch_idx는 각 TRN instance4개×3image 뒤 VAL instance5개×3image의 순서다. 원래 TRN_000661 Load02 397px→ratio2 97px/ratio4 28px, VAL_000151 Load02 707px→178px/45px이며 두 component 모두 남는다. 같은 변환 reference와 exact이지 원본 해상도와 lossless가 아니다. 새 합성 reduction fixture에서는 80px/3components→ratio2 20px/2components, ratio4 5px/2components로 홀과 홀수좌표의 작은 island 소실을 명시적으로 확인했다. bridge를 합성 사례로 대체하지 않았다.

GPU [ratio2 status](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/gpu_ratio2/status.json) / [ratio4 status](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/gpu_ratio4/status.json), `raw_gpu_ratio{2,4}.log`, `batch64_records.json` 참조. 두 재료 및 HR_Scan/LR_Scan/GeoCAD 모두 포함하고 TRN_000661도 포함한다. VAL_000151은 CPU proof에만 사용했다. GPU 입력64장의 reference error0이며 loss hook의 exact/selector assertions를 통과한 후 backward/unscale 뒤 실패했다. **OOM0/collate오류0, optimizer.step 미도달**이다. 현재 allocated/reserved는 ratio2 190,829,056/12,312,379,392 B, ratio4 174,998,016/11,368,660,992 B. 이 단일 minibatch의 메모리를 전체epoch 적합성으로 확대하지 않는다. 검사 코드가 loss/boundary 숫자를 성공 후에만 저장하여 GPU의 정확한 loss 값·selector 횟수는 UNKNOWN이다. finite loss assertion과 hook 통과는 실행 순서/traceback으로만 확인되며 수치를 복원·추정하지 않았다.

이는 제가 추가한 `all finite gradient` 검사가 GradScaler의 정상 step-skip/update 전에 중단한 **qualification adapter의 한계**를 포함한다. 이를 AMP 비호환이라고 확정하거나 batch64 PASS로 바꾸지 않았다. 직접 minibatch 시험은 trainer 전체 optimizer warmup 경로의 증명이 아니다.

Ray 설치 **2.58.0**, Ultralytics **8.4.129**, Python3.11.15/torch2.7.1+cu128/CUDA12.8/RTX5090. [첫 실패 로그](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/raw_ray_initial.log): Tuner와 ASHA 양쪽 metric/mode 지정은 실제 API에서 거절됐다(exit1/trial0). 새 [v41b adapter](../scripts/bitmap_ray_resume_v41b.py)는 Tuner에만 metric/mode를 지정하고 `ray.tune.report/get_checkpoint/Checkpoint/RunConfig`, 명시적 `TPESampler(seed42)`, ASHA epoch binding을 사용했다. [최초 실행 로그](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/raw_ray_attempt2_initial.log), [동일 root 재개 로그](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/raw_ray_attempt2_resume.log), [결과/error](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v41/ray_resume_results.json).

Engineering data는 Train9/Val6, batch6/workers2/AMP, 2epochs 예정이며 final HPO 자료와 출력 경로를 분리했다. Trial **c60cbc2a** 하나, checkpoint `ray_engineering_attempt2/trial_c60cbc2a_*/checkpoint_000000/last.pt` SHA **`feed31e5d2ac398a2487da570a1efd32f87f9744e685ed58a6113a83a81b82c1`**. 중단 전 epoch1만 실제 완료; train seg **4.78188**, CSV epoch elapsed **0.893268s**, Ray iteration **3.636154s**. pooled Val6/3rep `metrics/mAP50-95(M)` **0.00483**, val seg3.5585는 engineering 관측이며 성능결론이 아니다. 같은 trial ID, saved epoch0→start_epoch1, 저장 EMA→YOLO 가중치 exact assertion 통과 뒤 optimizer state 검사에서 중단했다. checkpoint optimizer states **0**, scaler **32768**(초기65536 대비 감소). 적어도 한 optimizer update가 overflow로 건너뛰어진 증거이며 **비어 있지 않은 optimizer 재개는 미입증**이다. EMA로 재개하는 설치 YOLO 동작이며 bitwise trajectory 동등성을 주장하지 않는다. 반복 epoch0·phantom trial은 관측되지 않았지만 epoch2 완료/두checkpoint/ASHA pruning 검증은 NOT_RUN이다. Ray driver는 trial error를 결과로 반환하여 exit0였으므로 shell 성공을 PASS로 취급하지 않았다.

## 다음 하나의 수정: AMP scaler 초기화와 optimizer update 증명

[정책 amendment](../docs/bitmap_noaug_policy_amendment_20261102_v41.md)는 기존 augmented polygon HPO와 분리된 전향 bitmap/noaug arm이며 historical M50/four-rep protocol이 아니다. square letterbox/nearest/usable class0·load_id·nonoverlap 정책과 모든 증강0을 공통 고정했다. search bounds9개/mask_ratio{2,4}, pretrained YOLO11n-seg, AdamW/640/batch64/workers8/AMP/seed42, pooled Val selector,40/max60/grace15/reduction3·GPU1/shared budget은 변경하지 않았다. 최종 논문 채택은 검토 전이다.

두 실패를 잇는 우선 수정 대상은 **첫 AMP update의 overflow와 비어 있는 optimizer state**다. 초기 scale128, step 전 loss/gradient/scaler 영속 기록, 실제 optimizer state>0 assertion, resume 시 저장 scaler 유지로 새 [minibatch v41c](../scripts/bitmap_qualify_v41c.py)와 [Ray v41c](../scripts/bitmap_ray_resume_v41c.py)를 준비했다. 이는 **compile만 PASS / 실행 NOT_RUN**이며 scale128로 해결된다고 주장하지 않는다. 기존 v41/v41b source와 실패 root를 보존했다. GPU ratio별 한 번 및 Ray 수정검증 한 번을 소진했으므로 이번 task에서 v41c 실행·새 root 재시도는 하지 않았다.

지금 실행 가능한 read-only 재검증 명령(훈련 없음):

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_evidence_v41.py
```

후속 작업에서 사용할 정확한 첫 GPU 게이트 명령열(**현재 미실행**, 기존 root에 덮어쓰지 않음):

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v41c.py init
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v41c.py cpu --ratio 2
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_qualify_v41c.py gpu --ratio 2
```

ratio2 실패 시 중단. PASS 뒤 ratio4 및 Ray2-checkpoint 재개를 새로 검증해야 하며 이후에만 full6000/1200 epoch로 진행한다. 기존 errored Ray trial을 자동 재시작하지 않는다. **지금 실행 가능한 qualified Stage1 명령은 없음**; v40 future launcher를 우회 실행하면 안 된다. 현재 살아 있는 search/supervisor PID가 없으므로 stop/resume 대상도 없다.

신규 코드6개(qualify v41/v41c, Ray v41/v41b/v41c, evidence v41), 정책문서·본보고서·latest_report·PROJECT_STATE를 작성/갱신했다. compile PASS, CPU2/2 PASS, GPU0/2 FAIL, Ray resume FAIL, full-data/HPO NOT_RUN, known subset PASS. `code_output_sha256.json`은 최종 status 갱신 전 snapshot이며 최종 현재 파일 hash는 `delivery_sha256.json`을 사용한다. 부수 rg stdout/stderr glob 조회 exit2는 파일명이 없어 발생했고 trial 실패와 별개다. Ultralytics AMP check의 yolo26n 메시지는 별도 검사 모델이며 학습모델 교체가 아니다(기존 workspace weights 파일 mtime2026-11-01 확인). 설치·업그레이드0. 원본/weights/labels/splits/USD/v39/v40 수정0, Kit/ROS/motion0, steering HOLD·15°/20° 유지. 원격 mirror 완료는 확인하지 않았으며 정상 HANDOFF_REPORT marker로 동기화를 요청한다.
