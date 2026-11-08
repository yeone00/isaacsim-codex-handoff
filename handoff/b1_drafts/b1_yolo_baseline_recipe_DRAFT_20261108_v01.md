# B1 HR / LR / CAD YOLO-seg 공통 baseline 학습 recipe — **DRAFT v01** (2026-11-08)

> **상태: DRAFT. 잠기지 않았고 실행 승인도 없다.** 연구자가 §7의 결정 항목을 확정하면 `..._LOCKED_v01_<날짜>.md` 새 파일로 잠근다. 이 DRAFT는 수정하지 않는다.
> 학습 0, HPO 0. 모델 성능을 보고 고른 값은 없다.

## 0. 원칙

- 세 표현은 **데이터만 다르고 나머지는 모두 같다.** 같은 것: 모델 구조, 초기 가중치, 하이퍼파라미터, epoch, batch, imgsz, seed, augmentation, 평가 절차.
- 가장 먼저 쓰는 기준은 v42에서 실측 검증된 설정이다(GPU batch 64 / workers 8 / AMP / AdamW / 640 / seed 42 / no-aug). 바꾼 항목은 §3에 근거를 적는다.
- **Test(200)는 모델 선택, epoch 선택, 하이퍼파라미터 조정에 쓰지 않는다.** 학습이 끝난 뒤 고정된 checkpoint로 한 번만 평가한다.
- QA 기준(v02 LOCKED), 라벨, 원본 이미지, split은 바꾸지 않는다. Real Test189는 쓰지 않는다.

## 1. 데이터

| 항목 | 값 |
|---|---|
| 패키지 | `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_YOLO_PACKAGE_20261108_v01` (`package_checks.json` 3ff0a45e…, PASS_PACKAGE_COMPLETE) |
| data.yaml | `HR_Scan/data.yaml` 6e5d2484…, `LR_Scan/data.yaml` 9779cf1a…, `GeoCAD/data.yaml` aeb24e49… |
| split | train 1000 / val 200 / test 200 base scene. 세 표현의 장면은 같고 짝지어져 있다 |
| 라벨 | class0 `brick_load`. 공통 HR canonical polygon(같은 라벨 파일을 세 표현이 공유). 팔레트는 라벨 없음 |
| QA 열(H1) | `qa_v02_train_v01/…csv`, `qa_v02_valtest_v01/…csv`. 학습 입력에는 쓰지 않고 분석에서만 쓴다 |

## 2. 고정 학습 설정(baseline)

| 항목 | 값 | 출처 |
|---|---|---|
| 모델 / 초기 가중치 | `yolo11n-seg.pt` sha256 `55ed65c5…e152` | v40–v42와 같음 |
| trainer | Ultralytics 8.4.129 `SegmentationTrainer`(표준 polygon dataset). AMP GradScaler `init_scale=128`만 v42c 방식으로 덮어쓴다 | v42c StrictTrainer와 같은 scaler. 아래 §3-1 |
| optimizer | AdamW, lr0 0.001, lrf 0.1, momentum 0.9, weight_decay 0.0005, warmup_epochs 3 | v42 full-pilot 고정값(`bitmap_full_epoch_v42c.py`) |
| loss 가중치 | box 7.5, cls 0.5, dfl 1.5 | v42와 같음 |
| batch / nbs | 64 / 64 → **accumulate 1** | v42. GPU repro B(2026-11-08)에서 복원 후 optimizer 진행 PASS |
| workers | 8 | v42 |
| imgsz | 640(원본 640×480은 letterbox) | v42 |
| epochs | 60, `patience` 1000(조기 종료 없음) | v40 Stage-1 계획값 |
| seed / deterministic | 42 / True | v42 |
| AMP | True | v42 |
| augmentation | 모두 0: mosaic, mixup, copy_paste, fliplr, flipud, degrees, translate, scale, shear, perspective, hsv_h/s/v. close_mosaic 0, multi_scale 0 | v41 정책 `PROSPECTIVE_BITMAP_NOAUG_v41` |
| mask | overlap_mask False, mask_ratio 4 | 아래 §3-3 |
| checkpoint 선택 | `best.pt` = **val** fitness 최고(Ultralytics 기본 fitness) | test 미사용 |
| device | GPU 0(RTX 5090), 한 번에 run 하나. Isaac이나 Kit과 동시에 돌리지 않는다 | |

## 3. v42 대비 변경과 그 근거

1. **trainer와 dataset:** v42의 `BitmapTrainer`/`SearchTrainer`는 예전 cement+red `final_dataset_v03` bitmap 전용이다. B1 패키지는 표준 YOLO polygon 형식이라 Ultralytics 표준 trainer를 쓴다.
   - 대신 AMP scaler `init_scale=128`은 v42c와 같게 둔다.
   - 근거: GPU repro A(2026-11-08)가 Ultralytics 기본 scale 65536에서 AdamW step을 한 번도 하지 못했다. v42에서 실측한 gradient absmax는 약 114였다. 114 × 65536은 fp16 최대값 65504를 훨씬 넘으므로 overflow가 나서 step을 건너뛴 것으로 추정한다.
2. **epochs 60:** v40 Stage-1 계획값이다. train 1000장에 batch 64이면 epoch당 16 step이므로 총 960 step이다.
   - val 곡선이 끝까지 평평해지지 않으면 다음 단계(HPO)에서 다룬다. baseline에서는 바꾸지 않는다.
3. **mask_ratio 4:** v42 GPU 실측에서 ratio 2와 4가 모두 PASS였다. full-pilot 코드는 2였고 Ultralytics 기본값과 v42 Ray 탐색은 4였다.
   - B1 load는 작은 것이 많지만, 성능을 보고 고르지 않는다는 원칙에 따라 기본값 4를 제안한다. **연구자 결정 항목**(§7-3)이다.
4. **no-aug 정책:** v40 docstring에 원래 recipe와 다르다는 점과 명시적 수락이 필요하다는 점이 적혀 있다. 그래서 **연구자 결정 항목**(§7-2)이다.

## 4. 실행 단위와 시드

- baseline은 3표현 × seed 42로 **3 run**이다.
- 권장: seed 42, 43, 44로 **9 run**(§7-1). 세 표현 간 차이가 작을 수 있어 seed 변동을 함께 보고하기 위해서다.
- seed를 바꿀 때는 seed만 바꾼다.
- 예상 시간(실측 아님): epoch당 1000장 학습 + 200장 val로 20–40초를 예상한다. 60 epoch이면 run당 20–40분, 9 run이면 3–6시간이다. 첫 run의 실측으로 갱신한다.
- 출력: 새 root(`B1_YOLO_BASELINE_<날짜>_v01/<rep>_seed<k>`). 실패한 run도 분모에 남긴다. 재시도는 승인을 받고, 새 attempt 디렉터리에서 한다.

## 5. 평가(미리 정함)

- 주지표: mask mAP50-95(M). 보조지표: mAP50(M), box mAP50-95(B), precision, recall.
- **val**: epoch마다 기록하고, best.pt 선택에만 쓴다.
- **test**: 각 run의 best.pt로 **한 번만** 평가한다. 같은 표현의 test로 평가한다.
- 분석 보고(H1): "전체"와 "FLAG 제외"를 함께 낸다.
  - FLAG 제외는 QA v02에서 FLAG_NUREC_OCCLUSION인 load를 평가에서 빼는 load 단위 분석이다.
  - Ultralytics 기본 val로는 할 수 없어서 별도 평가 스크립트가 필요하다(미작성).
- 표현 간 비교: paired base scene을 기준으로 차이와 신뢰구간을 보고한다.
  - 미리 정한 margin이 없으면 동등성이나 비열등성을 주장하지 않는다.
- 선택 사항(§7-4): 교차 평가. 예를 들어 CAD로 학습한 모델을 HR test로 평가한다. 하려면 미리 정해 둔다.

## 6. HPO(별도 단계, baseline 뒤)

- Ray Tune + Optuna TPE + ASHA. v42c 구조를 쓰고, batch 64(accumulate 1)를 유지한다.
- GPU repro B(2026-11-08) 결과: Ray 복원 후 optimizer step 1→2, real_updates 1→2, EMA 1→2, 가중치 560 tensor 변경으로 **PASS**.
- 남은 일: Stage-1 entrypoint(`bitmap_stage1_v40.py`)는 v42 raw-state adapter에 연결되어 있지 않고, B1 polygon 데이터용이 아니다. HPO 전에 새 entrypoint를 만들고 smoke를 따로 돌려야 한다.
- HPO 목표값은 val만 쓴다. test는 HPO가 끝나고 최종 recipe를 잠근 뒤 한 번 평가한다.

## 7. 연구자 결정 항목(빈칸)

1. seed 수: 1(seed 42) / **3(42, 43, 44, 권장)** → `____`
2. augmentation: v41 no-aug 정책 유지(권장, v42와 같음) / Ultralytics 기본 aug → `____`
3. mask_ratio: **4(권장, 기본값)** / 2(v42 full-pilot) → `____`
4. 교차 평가 포함 여부 → `____`
5. epochs 60 유지 여부 → `____`
6. 사람 QA 검토(체크리스트)를 학습 전에 끝낼지, 병행할지 → `____`
