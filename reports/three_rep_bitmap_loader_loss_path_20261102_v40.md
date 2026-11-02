# v40 — bitmap loader 실제 loss 연결 및 1회 GPU 학습 PASS

2026-11-02 KST. **새 bitmap loader·CPU loss·전체 Train/Val QA·6장 1 epoch GPU engineering smoke PASS. Stage-1 readiness NO / HPO NOT_LAUNCHED / trials 0.** Full-data epoch pilot NOT_RUN. Kit/ROS/robot motion 0, retry 0, research denominator 0. p-value·과학적 성능 결론 없음.

## 구현과 실제 측정

새 출력 root: `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v40` (이하 ROOT). 원본과 v39 namespace를 재사용하지 않았다. `status.json`, `sha_inventory.json`, `environment.json`, `raw_*.log`에 실제 상태·경로·SHA·환경·로그를 보존했다.

[bitmap_loader_v40.py](../scripts/bitmap_loader_v40.py)는 설치 Ultralytics **8.4.129**의 `SegmentationTrainer`를 상속한다. Dataset→collate→`batch['masks']`/`batch['batch_idx']`→설치 `v8SegmentationLoss.calculate_segmentation_loss` 경로를 사용한다. 원본 usable load마다 한 binary channel을 유지하고 load_id 순서로 bbox/class/instance를 맞춘다. 분리된 component와 hole을 polygon으로 바꾸지 않는다. class 0 brick_load, pallet 제외, metadata usable=False 제외. 중복·음수 ID, pixel 수 불일치, 비binary 값, channel overlap을 거절한다. overlap_mask=False이며 image별 instance 채널을 batch_idx로 선택한다.

공통 engineering 정책은 **증강 없음·정사각 letterbox·mask nearest**다. 640×480 원본은 640×640에 위아래 80px padding되어 두 사례 모두 원래 픽셀이 보존됐다. Mosaic/mixup/copy-paste/flip/affine/HSV/multi-scale은 사용하지 않았다. 기존 HPO augmentation recipe와 동일하지 않다. loss source `/home/user/anaconda3/envs/sdg_tools/lib/python3.11/site-packages/ultralytics/utils/loss.py:516` 이후는 mask 대신 proto를 bilinear로 target 크기에 맞춘다. 이번 full-resolution target은 640×640이고, 실제 loss boundary의 proto도 640×640이다. 향후 mask_ratio 2/4 경로는 별도 RatioDataset에서 nearest로 줄이며 lossless라고 주장하지 않는다.

| 실제 사례 (Load_02) | 기존 polygon IoU / 추가 px | 새 batch/loss target | component / 원본 px |
|---|---:|---|---:|
| TRN_000661 | 0.676320272572402 / 190 | 동일변환 reference IoU 1.0, exact | 2 / 397 |
| VAL_000151 | 0.7846836847946725 / 194 | 동일변환 reference IoU 1.0, exact | 2 / 707 |

`loss_proof.json`: 두 실제 이미지 CPU minibatch의 mask `[9,640,640]`, float32, 값 {0,1}, batch_idx `[0,0,0,0,1,1,1,1,1]`, positive anchors 81. 실제 segmentation loss **3.5717935562**, 전체 loss finite. CPU proof는 pretrained YOLO11n-seg head를 이용한 mask 경로 검사이며, 아래 GPU trainer는 nc=1 head로 실제 학습했다. 모델 계열은 동일 SegmentationModel/YOLO11n-seg다. `boundary_stress.json`은 설치 loss의 실제 instance selector가 역순 target index에서도 정확한 channel을 pixel BCE 입력에 전달함을 확인했다.

ROOT의 `*_polygon_diff.png`는 green GT/red polygon extra, `*_batch_mask.png`는 실제 batch target이다. **정렬된 overlay는 `TRN_000661_letterbox_overlay.png`, `VAL_000151_letterbox_overlay.png`**다. 초기 `*_batch_overlay.png`는 RGB를 늘린 시각화 오류가 있어 보존하되 근거로 사용하지 않는다. padding 정렬을 고쳐 새 파일을 만들고 첫 사례를 육안 확인했다. 학습 tensor에는 이 시각화 오류가 없었다.

## provenance와 전체 QA

`METADATA_SHORT_HASH_ALGORITHM_UNKNOWN` 유지. bounded grep/AST에서 original nominal 생산기의 정확한 short-hash byte 계약을 찾지 못했다. 다른 nonideal hash 함수를 authority로 사용하지 않았다. `TRN_000001 Load_01`의 선언 `d4d2a2a4976b7a4d`를 교체하지 않았고 v39 실패도 그대로다. `provenance.json`에 세 사례의 선언값·원본/v03 전체 SHA·pixel 수, legacy source expected/observed SHA를 기록했다. 세 사례 모두 **VERIFIED_FULL_FILE + VERIFIED_MASK_PIXELS + METADATA_SHORT_HASH_UNKNOWN**이다. 이는 짧은 해시 검증 PASS 또는 데이터 훼손 판정이 아니다.

`audit.jsonl`: **7,200/7,200 이미지 reference**(Train 6,000 / Val 1,200), 첫 실행 checked7200/skipped0, 55.262초. 모든 이미지 SHA, metadata SHA, scene/seed/split, load IDs, PNG SHA, binary target SHA, loader SHA와 원본 해상도 exact bitmap fidelity를 기록했다. 실제 오류·누락·overlap으로 제외한 사례 0. 재개 실행은 checked0/skipped7200, 1.575초였고 이미지/GT/metadata/code SHA를 재확인했다(`audit_invocations.jsonl`).

`fidelity.jsonl`/`fidelity_summary.json`: Train/Val **7,139 unique usable load instances** 전부 원본 polygon을 재래스터화해 비교했다. nonexact350, IoU<0.95 **31**; 이번 집계가 역사 train27+val4와 같음을 확인했다. 낮은 fidelity 사례를 제외하지 않았다. v01 원본 전체 SHA 일치 **6,653**, assembler 지정 replacement 원본 일치 **486**, 합계7,139. Audit 초기 per-case original source UNKNOWN이었던 replacement도 fidelity inventory의 지정 source root 비교로 해소했다. **짧은 metadata hash는 여전히 UNKNOWN**이며 완전한 provenance 인증을 주장하지 않는다. PNG/JSON/split/label은 수정하지 않았다.

최종 manifest expected SHA `2a4782911ef334fc640e9f90ee8120e48ab3c30e25da47603004978835626bf8` 일치. Canonical GT summary/instance CSV와 polygon fidelity lock dependency SHA도 일치. `rgb_pairing.json`: unique scene2,800 및 seed2,800, Train2000/Val400/Test400, HR_Scan/LR_Scan/GeoCAD 대응8,400개 파일 존재와 metadata scene/seed/split 일치. split 교집합0. Test1,200장은 존재/metadata 확인만 했으며 평가·선택에 사용하지 않았다. Real Test189 접근·평가·선택0; 기존 평가 이력은 유지한다. LR은 reduced-acquisition 독립 재구성이다.

`stress.json` 및 `boundary_stress.json`: disconnected/hole, 두 load ownership, ignore load/배경, empty channel, binary bounds, overlap·wrong/duplicate ID·wrong split·pixel count 거절, negative bridge, installed loss 선택 PASS. 빈 usable scene은 source에서 거절하며 이번 locked Train/Val에는 해당 scene이 없었다. `ratio_checks.json`: 2/4 각각320²/160² target이 동일 nearest reference와 exact, 해상도 변경으로 원본과 lossless 비교는 하지 않았다. Ratio 경로의 GPU/Ray 전체 trial 실행 검증은 아직 없다.

## GPU smoke — 실제 1회, 재시도 없음

[bitmap_smoke_v40.py](../scripts/bitmap_smoke_v40.py), ROOT/smoke/status.json 및 epoch/results.csv. RTX5090, 시작 시 CUDA compute process 없음·Kit 실행파일 없음 확인. Python3.11.15/torch2.7.1+cu128/CUDA12.8. 설치·업그레이드·process 종료0.

Train: TRN_000001·TRN_000661 ×3 reps=**6장**. Val: VAL_000151 ×3 reps=3장. 1 epoch, batch6/workers0/AMP False/mask_ratio1, imgsz640/AdamW/seed42, safe noaug. 이는 제한된 engineering 설정이며 frozen batch64/workers8 HPO와 같다고 주장하지 않는다. 실제 nc1 YOLO11n-seg head, 2,834,763 parameters.

- **attempt1 / epoch1 / exit0 / PASS / retry0**. train box2.70187, **seg4.32745**, cls3.84952, dfl2.28389. epoch CSV elapsed1.16326초; wrapper 학습·검증 전체3.274879초.
- peak allocated3,957,387,776bytes, reserved4,045,406,208bytes. CLI GPU memory3.77G. batch64 적합성으로 외삽하지 않는다.
- 실제 train loss 경계: mask `[24,640,640]`, float32/binary; batch_idx·각 channel pixel 수·proto/positive anchors를 status에 기록했다. CPU exact 검사와 같은 loader SHA임을 final checks에서 확인했다.
- epoch Val seg3.45772, pooled 3장 Mask mAP50-95 **0.00625**. 최종 best 재검증 값 **0.006449847824533119**는 별도 반환값이다. 이 작은 smoke 수치는 연구 성능·HPO 결과가 아니다. stock trainer가 final epoch의 새 last/best를 저장했으며 ROOT/smoke 아래에만 존재한다.

**Full-data 1 epoch pilot NOT_RUN.** 무증강 정책을 기존 frozen common recipe로 포장하지 않았으며 추가 GPU 실행을 하지 않았다.

## Stage-1 전달 및 남은 구체적 작업

[bitmap_stage1_v40.py](../scripts/bitmap_stage1_v40.py)는 나중에 승인받아 실행할 별도 entrypoint다. Ray OptunaSearch(TPE,seed42)+ASHA,40 trials/max60/grace15/reduction3, single GPU 순차, YOLO11n-seg/640/batch64/workers8/AdamW/seed42/AMP, pooled Val `metrics/mAP50-95(M)` 최대화, 기존 9개 search bounds 및 mask_ratio{2,4}를 명시했다. train/val은 전체 records.json을 사용한다. epoch last.pt를 Ray checkpoint로 저장하고 Tuner unfinished resume와 YOLO checkpoint resume를 연결한다. 기존 output은 --resume 없이는 거절하며 errored trial 자동재시도하지 않는다. Stage2 Top5×3rep×150epochs는 미실행/구현범위 밖이다.

후속 실행 명령(**이번 미실행**, 정책 수용과 실행 승인 후):

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/bitmap_stage1_v40.py --output /home/user/hh/isaac_cosmos/sdg_final/THREE_REP_BITMAP_20261102_v40/stage1_future --accept-safe-policy
# 중단 후 동일 경로: 위 명령에 --resume 추가
```

**Stage-1 readiness NO.** 구체적 미해결은 (1) 기존 recipe와 다른 safe noaug 정책의 연구용 채택 여부, (2) mask_ratio2/4 실제 loss·validation 및 batch64 VRAM 적격화, (3) Ray epoch checkpoint 재개/ASHA 종료의 runtime 검증이다. 현재 script compile/--help PASS이고 search는 실행하지 않았다. metadata short hash provenance UNKNOWN도 별도 남는다. 구현된 bitmap loader와 완료 smoke를 다시 준비 단계로 되돌릴 이유는 없다. 다음 작업은 새 namespace에서 이 세 항목을 한정 검증하는 것이며 40-trial launch는 별도 승인 범위다.

## v30 과거 조향 관측 — 새 안전한계 아님

`v30_retrospective.json`: 요청 SHA `9a77f63c3fe6c1f9e930f2bac46b3cf8505b246acecd2cc48a48747ceeae8215` 일치. named_joint_state의 q_rad/dq_rad_s,7,396 samples, sim3.050000159–126.316673255s; dt 중앙값0.016666668s/max0.033333335s. 실제 logged dq 절대 max: front_left16.856316/front_right26.355076/rear_left15.668217/rear_right11.979764 deg/s. 각 joint의 중앙·90/95/99% 및 q 차분 rate도 JSON에 보존했다. joint 누락0. sample 사이 peak·logged velocity 품질 불확실성은 남는다. 이것은 old quintic 성공 run의 retrospective 관측이며 **safe rate-abort UNDEFINED**, stationary sweep/graph 변경 승인·live 시험0, steering HOLD다.

## 변경·검사·보존

신규 코드7개: bitmap_loader / bitmap_qualification / bitmap_smoke / bitmap_fidelity_inventory / bitmap_final_checks / bitmap_boundary_tests / bitmap_stage1 각 v40.py. 본 보고서·latest_report·PROJECT_STATE 갱신. 원본 scripts·dataset·labels·locks·weights·USD·v39 status/raw/historical31은 보존했고 v39 source evidence의 4개 expected SHA 일치를 다시 확인했다. 새 코드/입력 모델/설치 loss·trainer/출력 파일 SHA는 ROOT/sha_inventory.json이다. 신규 observed SHA를 기존 expected로 승격하지 않았다.

Compile·CPU proof·synthetic/ownership·full source QA·full fidelity·RGB pairing·resume·GPU smoke PASS. short hash UNKNOWN. Future HPO runtime NOT_TESTED. 부수 metadata flat 경로 조회 head exit1은 실제 split/train 경로로 해결하고 limitations.json에 기록했다. 초기 overlay 오류도 보존·수정 기록했다. 학습 실패나 OOM은 없었으며 기존 v39 감사 실패는 지우지 않았다.

재현 명령은 위 scripts의 proof/audit/fidelity/final_checks/boundary_tests 및 smoke entrypoint다. **완료된 proof/fidelity/smoke output에는 덮어쓰기/재시도하지 않는다**. audit만 SHA 검증 후 resume 가능하다. Handoff는 이 보고서의 정상 HANDOFF_REPORT marker로 동기화 요청하며 `.git` 없는 workspace에서 원격 반영 완료는 확인하지 않았다.
