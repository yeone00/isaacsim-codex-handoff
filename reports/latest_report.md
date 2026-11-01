# 3개 표현 HPO 착수 결과 — 요청일 2026-10-29 / 실제 실행일 2026-11-01 KST

**Stage-1: NOT_LAUNCHED / 신규 HPO trials 0. 실제 GPU 1-epoch engineering smoke: PASS(exit 0).**

HPO를 시작하려고 실제 데이터 구성과 학습 smoke까지 수행했다. 그러나 Nominal **train과 val**의 분리된 마스크 조각 사이에 인공 polygon 연결선이 실제로 존재한다. 이번 사용자의 “오염된 train/val로 학습하지 말 것” 조건 때문에 전체 HPO는 시작하지 않았다. 과거 라벨 잠금의 허용 판단을 이번 QA PASS로 대체하지 않았다. HPO 완료·실행 중이라는 주장은 하지 않는다.

## 실제 데이터와 보존

새 namespace를 `mkdir(exist_ok=False)`로 생성했다. 기존 경로를 삭제하거나 재사용하지 않았다.

`/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261029_v01/`

| 항목 | 실제 위치 / 내용 |
|---|---|
| Nominal 최종 manifest | `/home/user/hh/isaac_cosmos/sdg_final/nominal_visibility_replacement_v02/strict_reselection_v03/final_manifest_v03/final_experiment_base_manifest_2800_v03.csv` |
| Manifest SHA256 | `2a4782911ef334fc640e9f90ee8120e48ab3c30e25da47603004978835626bf8` — 원본 assembler/converter의 expected와 실제 일치 |
| RGB | `/home/user/hh/isaac_cosmos/sdg_final/final_dataset_v03/rgb_iso400_v02/{HR_Scan,LR_Scan,GeoCAD}/images/{train,val,test}` |
| train/val 기존 구성 | `/home/user/hh/isaac_cosmos/sdg_final/final_dataset_v03/yolo/dataset_size_curve_v01/datasets/{HR,LR,GeoCAD}/N2000/` |
| canonical mask | `/home/user/hh/isaac_cosmos/sdg_final/final_dataset_v03/canonical_gt/masks/{train,val}` |
| 기존 polygon | `/home/user/hh/isaac_cosmos/sdg_final/final_dataset_v03/yolo/base_canonical_v03/labels/{train,val}` |
| 새 HPO 후보 config | 새 namespace의 `pooled/data.yaml` — **라벨 QA 차단 상태, 학습 금지** |
| 입력 추적 | `input_manifest.csv`, `input_sha256_inventory.csv` — 7,200개 image/label 경로와 SHA256 |

| 표현 | train | val | test membership만 확인 | train cement/red | val cement/red | test cement/red |
|---|---:|---:|---:|---|---|---|
| HR_Scan | 2000 | 400 | 400 | 1000/1000 | 200/200 | 200/200 |
| LR_Scan | 2000 | 400 | 400 | 1000/1000 | 200/200 | 200/200 |
| GeoCAD | 2000 | 400 | 400 | 1000/1000 | 200/200 | 200/200 |

각 표현의 scene ID exact-set이 최종 manifest와 일치한다. train/val/test scene ID 교집합 0, 중복 0. 3개 표현 모두 train/val 누락 image/label 0, 클래스 0·좌표 유한성·범위·polygon 최소 길이와 metadata의 usable load 수 일치 PASS. 모든 개발 라벨은 canonical 라벨 bytes와 일치했다. test는 파일명 membership만 점검했고 평가·점수 선택에는 사용하지 않았다. Real Test189는 접근하지 않았다. Depletion 표본은 라벨 QA만 수행했으며 학습·검증 선택에 넣지 않았다.

새 풀은 동일한 train 2,000개 장면을 세 표현 모두 포함한 **6,000 images**, 동일 val 400개 장면의 **1,200 images**다. 이미지 원본을 참조하고 라벨은 새 namespace에 작은 텍스트 사본으로 저장했다. 원본 cache/라벨을 쓰지 않도록 구분했다. Proxy 0, test key 없음. LR은 독립 재구성 표현이라는 정의를 유지한다.

## 작은 실제 라벨 검사

고정 표본은 split별 cement/red의 첫 scene ID: train `TRN_000002`, `TRN_000001`; val `VAL_000003`, `VAL_000001`. 여기에 기존 fidelity CSV가 지목한 split별 최저-IoU 분리 조각 1개를 추가했다. 이는 모델 선택용 표본이 아니다. RGB와 canonical mask를 3개 표현 모두 겹쳐 본 12개 영상에서 위치 대응은 육안상 일치했다. 증거: `qa/rgb_mask_contact.jpg`. 전체 데이터의 pixel alignment를 인증한 것은 아니다.

`brick_load`는 **물리적 적재물 하나당 class 0의 polygon 한 줄**이다. 장면에 여러 load가 있어 여러 줄인 것은 정상이며, 분리된 가시 조각을 서로 다른 객체로 늘리면 안 된다. 7,200개 개발 image/label에 대해 이 줄 수 계약을 metadata와 대조했다.

| 실제 표본 | source 조각 수 | 원래 정수좌표 반올림 복원 IoU | 원본에 없는 추가 픽셀 |
|---|---:|---:|---:|
| train TRN_000661 Load_02 | 2 | 0.676320 | 190 |
| val VAL_000151 Load_02 | 2 | 0.784684 | 194 |
| depletion NDP_E007_C_T03_C20 Load_01 | 2 | 0.999815 | 13 |
| depletion NDP_E002_C_T01_C40 Load_01 | 1 | 1.0 | 0 |

실제 PNG 재개봉·polygon 재래스터화로 확인했다. train 표본의 두 조각 사이 긴 인공 선을 overlay에서도 확인했다. 따라서 문제는 held-out depletion에만 있지 않다. 기존 audit의 train27+val4=31개 IoU<0.95 기록도 실제 CSV hash 검증 후 확인했다. **0.95는 기존 진단값을 기술한 것이며 새 합격 기준이나 비열등성 margin이 아니다.**

원본 정수좌표 반올림 이외에 설치된 Ultralytics의 int32 절삭 방식도 별도 계산했다. 위 train/val 표본의 직접 raster IoU는 각각 0.628333/0.727371이었다. 이 추가 진단은 원본 해상도에서 float64 좌표를 직접 절삭한 결과이며, 실제 loader의 float32·1,000점 resampling·letterbox/augmentation·mask_ratio 전체를 재현한 최종 학습 target 수치는 아니다. 단순 경계 양자화와 별개로, 반올림에서도 인공 연결선은 남는다. 표본의 세부 값·mask/label hashes는 `qa_results.json`, `depletion_disconnected_qa.json`에 있다.

기존 depletion fidelity CSV에는 C20의 multi-contour 사례 2개, C40은 0개다. 따라서 존재하지 않는 C40 분리 표본을 만들어내지 않고 실제 C40 단일 연결 표본을 검사했다. 최초 preflight가 빈 C40 후보에 `min()`을 호출하여 exit1로 실패한 사실을 `preflight_attempt_0001_failure.json`에 보존했다. 그 뒤 새 `qa_finish` 코드로 후보 없음 자체를 기록하고 QA를 완료했다. 전체 namespace 생성 스크립트를 다시 실행하거나 실패를 삭제하지 않았다.

## 원본 잠금과 이번 판단의 차이

`YOLO_BASE_CANONICAL_V03_LOCK.json`은 secondary disconnected fragments의 오차를 허용하고 기존 polygon을 유지하도록 기록되어 있다. 이 내용도 그대로 보존했다. 해당 lock SHA256은 `7176aaf3c4166ca620a3482ef83a36ba9903f9ec8253915017e5c28d016c8526`이다(자체 observed hash, 독립 인증용 expected는 아님).

의존 fidelity CSV SHA256 `d55b055f6dee04545075330b262e097abb9e89cc48ee8b308376213b8dfbe338`, summary JSON hash 및 전체 canonical labels tree SHA256 `d86e85dbb0033da01e8f16e17814acf11b40ef77474571b5872c17cd3f6942a2`는 lock expected와 일치했다. 라벨 tree는 smoke 후에도 재검증했다. 기존 최소 bridge 대안 감사도 정적으로 읽었으며 worst IoU 0.676320이 남아 있어 이미 시도된 대안을 새 해결책이라고 주장하지 않는다.

이번 사용자 조건은 오염된 개발 라벨을 수정하라는 것이므로 **과거 허용 lock을 변경하지 않고 새 연구 실행을 차단**했다. 새 labels는 아직 수정본이 아니며 staged 사본이다.

**다음 단일 repair:** 새 데이터 경로에서 canonical instance bitmap을 보존하는 mask 입력/변환 경로를 구현하고, 이미지와 동일한 공간 augmentation을 적용해 loader가 생성한 최종 target을 검증한다. 분리 조각은 같은 physical instance로 유지하고 인공 bridge를 만들지 않는다. 원본 polygon·sample membership·seed·test를 바꾸지 않는다. 이 repair와 새 loader target QA를 마친 뒤 동일 GPU smoke를 새 attempt에서 수행하고 Stage‑1을 시작한다. 현재 stock polygon 경로에 그대로 연결하면 수정이 완료된 것이 아니다.

## 실제 배포 HPO protocol 확인

원본: `/home/user/hh/isaac_cosmos/scripts/training/run_common_hpo_stage1_v01.py`, `prepare_common_hpo_pool_v01.py`, `run_common_hpo_stage2_v01.py`. 기존 `final_dataset_v03/yolo/hpo_common_v01/stage1_hpo.log`의 2026-09-28 실제 실행에는 SearchGenerator/AsyncHyperBandScheduler/40 trials가 기록되어 있다. 이것은 **과거 4-rep 기록**이며 신규 trial 증거가 아니다.

설치된 `ultralytics/utils/tuner.py`, `callbacks/raytune.py`와 Ray `optuna_search.py`도 직접 읽었다. 실제 프레임워크는 **Ray Tune OptunaSearch(TPESampler 기본) + ASHA**, Optuna SuccessiveHalvingPruner가 아니다. Epoch별 `on_fit_epoch_end`가 metric과 `epoch+1`을 보고한다. ASHA time_attr=`epoch`, reduction_factor=3, max_t=60, grace=15다.

| 조건 | 원본에서 확인 / 새 연구 적용 결정 |
|---|---|
| Stage‑1 | 40 trials, 최대60 epochs, grace15, ASHA reduction3 |
| 공통 모델 | 기존 `/home/user/yolo11n-seg.pt` pretrained YOLO11n-seg |
| 고정 학습 | imgsz640, batch64, workers8, AdamW, training seed42, deterministic=True, AMP, patience1000, GPU 1개/trial |
| 선택 지표 | pooled val `metrics/mAP50-95(M)` 최대화 |
| 후속 Stage‑2 | Top5 × **3** representations ×150 epochs, seed42; 각 표현 val mask AP의 산술평균 |
| 후속 | multiseed/capacity는 HPO 선정 뒤 수행, 이번에 실행하지 않음 |

Search space는 원본 그대로: lr0 loguniform[1e-4,5e-3], lrf loguniform[0.01,0.20], momentum uniform[0.85,0.98], weight_decay loguniform[1e-6,1e-3], warmup_epochs uniform[0,5], box uniform[4,12], cls uniform[0.2,1.0], dfl uniform[0.5,3.0], mask_ratio choice{2,4}.

원본 pool은 2,000/400개의 장면마다 4개 표현 중 하나만 배정(500/100 per rep)했다. 새 결정은 요청의 paired full train2000/val400을 따라 세 표현 전체를 포함한다. 따라서 epoch당 images/compute가 과거와 달라지며, 과거 4-rep trial과 동일 예산 성능 비교로 해석하지 않는다. representation/material에 같은 수의 영상을 넣되 pooled AP는 각 표현 AP의 산술평균과 같다고 주장하지 않는다. Stage‑2에서 별도 평균을 쓴다.

원본은 training seed42만 명시했고 Optuna sampler seed는 미지정이었다(설치 Ray 기본 None). 새 실행에서는 **TPESampler seed42를 명시**하는 결정을 기록한다. 이를 과거 sampler seed가42였다는 증거로 소급하지 않는다. 이 설정을 반영한 HPO launcher와 재개 경로는 라벨 repair 후 구성해야 하며, 현재 실행 가능한 HPO command가 검증됐다고 주장하지 않는다.

## 실제 학습 실행과 환경

환경: `/home/user/anaconda3/envs/sdg_tools/bin/python`, Python3.11.15, torch2.7.1+cu128, Ultralytics8.4.129, Ray2.58.0, Optuna5.0.0, NVIDIA RTX5090(약32GB), driver570.172.08. CUDA availability와 실제 모델 학습 PASS. 패키지 설치/업그레이드 0.

기존 hh_isaac51 GUI 프로세스 PID955077이 GPU 약3.4GB를 사용하고 있었으며 종료하거나 조작하지 않았다. Isaac/ROS/robot motion은 새로 실행하지 않았다. B5도 재실행하지 않았다.

실제 실행 command(repository cwd):

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python -u scripts/three_rep_hpo_smoke_20261029_v01.py > /home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261029_v01/smoke.log 2>&1
```

실제 PID **958823**, terminal session **61199**, **이미 정상 종료(exit0)**. 고정 train/val 각2 scenes ×3 reps=각6 images, val15 instances. 1 epoch, imgsz640, batch6, workers2, AdamW, seed42, AMP, GPU0. 고정 표본은 기존 integer-round fidelity1.0/단일 연결 사례만 썼으며, 앞서 설명한 stock loader 양자화 한계는 남는다. 전체 HPO 라벨 QA가 PASS라는 뜻은 아니다.

`smoke/attempt_0001/results.csv`의 epoch1 mask mAP50‑95는0.00967, 마지막 best.pt 재검증의 정밀값은 **0.009547528222070929**다. 반환 metric은 `smoke_status.json`에 기록했다. loss/gradient 학습 및 validation 경로가 실행됐음을 확인하는 수치이며 학술 모델 성능이나 HPO 선택 결과가 아니다. `save=False`에도 마지막 epoch의 best/last.pt가 실제 생성되어 새 namespace 안에 보존됐다.

확인 파일: `smoke.log`, `smoke_status.json`, `smoke/attempt_0001/results.csv`, `smoke/attempt_0001/args.yaml`, `smoke/attempt_0001/weights/{best,last}.pt`. 원본 pretrained 모델과 소스 observed SHA는 `source_code_hashes.json`에 있다. 코드 hashes는 관측 inventory이며 독립 expected가 없는 원본의 무변경을 인증하는 기준으로 오용하지 않는다.

## 진행 확인 / 중지 / 재개

**현재 running HPO PID/session/database 없음.** `launch_status.json`의 NOT_LAUNCHED/trials_created0이 최종 상태다. 완료된 smoke PID에 kill을 보내지 않는다. 실행 중인 다른 프로세스도 중지하지 않는다.

```bash
cat /home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261029_v01/launch_status.json
cat /home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261029_v01/smoke_status.json
tail -n 20 /home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261029_v01/smoke.log
```

stop/resume: **대상 없음(N/A)**. 무제한 background HPO는 시작하지 않았다. tmux binary `/usr/bin/tmux`는 확인했으나 기존 tmux session은 없었다. 설치 Ultralytics의 Tuner.can_restore/restore 경로는 정적으로 확인했지만 실제 새 HPO의 stop/resume는 미검증이다. 실행 가능한 command나 재개 성공을 꾸며 제시하지 않는다. namespace를 다시 만드는 preflight command는 이미 존재하므로 의도적으로 실패해야 한다. smoke runner도 기존 status가 있으면 덮어쓰기/재시도를 거부한다.

## 결과 및 다음 순서

PASS: 최종 manifest expected SHA,2800 rows, split counts,3-rep pairing,누락/누수0,metadata별 instance 계약,legacy labels expected tree,소량 RGB-mask 대응,GPU 실제1epoch 학습·검증.

FAIL: Nominal train/val polygon의 artificial bridges. 첫 QA의 C40 빈 후보 처리 exit1은 보존 후 새 QA 코드로 해결.

UNKNOWN/NOT_RUN: corrected bitmap loader 및 최종 target 일치, 전체 HPO40 trials, Optuna sampler 고정/실제 세션 재개, Stage‑2/최종 모델/새 평가. 논문 chapter3 v7 원문은 이번 작업에서 발견·수정하지 않았으며 사용자가 제시한 방향만 적용했다.

다음 구체적 작업은 위 **canonical instance bitmap을 보존하는 새 label/loader 경로 repair 하나**다. 완료 후 Stage‑1 → Top5 Stage‑2 → multiseed/capacity → 최종3-rep weights → Nominal+depletion+3×3 cross-evaluation → real+scale-model → pose+900 B300 →324 fresh-observation E2E 순서다.900/324는 이번 사용자의 새 계획 수치이며 과거 B300/432 잠금 manifest를 변경하거나 새 실험이 잠겼다는 뜻이 아니다. Real 외부 검증 red-only와 Test189의 이미 평가된 이력을 유지한다.

변경: repository의 신규 `scripts/three_rep_hpo_{preflight,qa_finish,smoke}_20261029_v01.py`, 본 보고서, `docs/PROJECT_STATE.md` append 및 외부 새 namespace. 원본 데이터·코드·잠금·과거4-rep 결과·기존 보고서를 덮어쓰지 않았다. Git repository가 아니어서 `git status`는 fatal로 종료됐으며 이를 숨기지 않는다. git add/push/remotes 작업0.
