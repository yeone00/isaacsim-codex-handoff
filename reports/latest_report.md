# Test 평가 준비: B1 Synthetic Test + Roboflow Real Test189 (2026-11-08)

성격: 준비와 프로토콜 잠금 후보 작성 단계다.
- **test 이미지 추론 0회**(B1 test, Real Test189 모두). 학습 0, HPO 0, checkpoint 변경 0, threshold 조정 0.
- 데이터, 라벨, manifest, 기존 결과는 변경하지 않았다.
- 사람 QA 최종 검토는 **PENDING**이다.

평가 A(B1 합성 Test)와 평가 B(Real Test189)는 목적이 다르다.
- A: 합성 B1 안에서 val 결과(같은 표현 우세, CAD→LR 저하)가 독립 test에서 재현되는지 본다.
- B: 합성 데이터로만 학습한 모델이 실제 사진 한 세트에서 어떻게 동작하는지 보는 외부 점검이다.

두 평가는 GT 정의도 다르다(§3). 그래서 결과를 하나의 표로 합치지 않는다.

## 요약 — 6개 보고 항목

| # | 항목 | 결과 |
|---|---|---|
| 1 | B1 Synthetic Test 준비 | **준비 완료.** 200 장면 × 3 표현 = 600장, GT 605개, capture와 pairing 검증 PASS, QA v02 test 1815행. 평가 코드는 val과 같은 v01이고 test는 LOCKED 문서 없이는 거부된다. |
| 2 | Real Test189 데이터·GT | 189장, 972×1296. 파일 목록 sha가 기존 lock과 일치한다. 빨강 점토 블록 팔레트 **1개**만 있고 시멘트는 없다. 분할 누출 0. 라벨은 **SAM2.1 자동 mask**(Roboflow bbox를 prompt로 사용)이고 **수동 QA 기록이 없다.** |
| 3 | B1 모델과 클래스·라벨 호환 | **형식은 호환된다**(YOLO-seg polygon, class 0 `brick_load`, 팔레트 제외). 변환이 필요 없다. **정의 차이가 있다.** 실제 라벨은 이미지당 대상 load 1개만 표시하고 배경 벽돌 더미는 표시하지 않는다. 벽돌 형태(비닐 포장 중공 블록 vs 낱장 벽돌)도 다르다. |
| 4 | LOCKED 프로토콜·명령 | 두 개의 **LOCK CANDIDATE**(json + md)를 작성했고 preflight PASS. 승인하면 LOCKED JSON을 만들고 `scripts/run_test_evals_20261108_v01.sh` 한 번으로 A → B를 실행한다. |
| 5 | 실행 전 해결할 문제 | (a) Test189 GT 수동 QA 기록 없음, (b) 라벨 정의 차이(FP 처리), (c) 얼굴이 있는 실제 사진의 그림 취급, (d) 후보를 LOCKED로 확정하는 연구자 승인. 자세한 내용은 §5. |
| 6 | 최종 판단 | **A는 승인 즉시 실행 가능하다.** **B는 기술적으로 실행 가능하다.** 단, (a)·(b) 제한을 받아들인다는 연구자 결정이 필요하다. 이 제한이 결과 해석에 큰 영향을 주므로 승인 시 명시해 주기를 권한다. |

## 1. 평가 A: B1 Synthetic Test 준비 상태

**데이터(추론 없이 파일만 확인)**
- root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_VALTEST_20261108_v01`(val과 함께 생성됨)
- manifest `red_only_manifest_1400_v03.csv`(sha `56c8acbb…`)에서 test 200 장면을 고정했다.
  - L1 45 / L2 50 / L3 54 / L4 51
  - D1 57 / D2 46 / D3 48 / D4 49
- 표현별 RGB test 200장씩, 누락 0. `verify_{rep}_v01.json`은 passed=True(val+test 400 장면, load 1198개)다. `crossrep_pairing_v01.json`도 passed=True.
- GT: HR canonical mask 605개(모두 ≥100px). QA v02 test 1815행 = 605 × 3.
  - FLAG: HR 3, LR 4, CAD 3
  - LOW_SUPPORT: 25 / 23 / 26
  - WATCH: 5 / 4 / 5
- 파일 목록 inventory(1405줄, sha `3911b8e2…`): `reports/test_eval_protocols_20261108_v01/b1_test_inventory.tsv`
- B1 test는 지금까지 어디에도 쓰지 않았다.
  - 학습 data.yaml에는 train/val만 있다.
  - 평가 코드는 LOCKED 문서 없이 test를 거부한다.
  - test 평가 출력도 없다.

**평가 방식**
- val과 같은 코드(`eval_b1_yolo_20261108_v01.py`, sha `0de45618…`)와 같은 설정을 쓴다.
  - GT ≥100px, <100px IGNORE, imgsz 640, conf 0.001, NMS 0.7, max_det 100, retina mask
  - 작동점 conf 0.25 / IoU 0.5, FLAG 포함과 제외
  - 층: L1–L4, 주/부, 크기, 실제 가림, QA, ROI, 거리
  - 장면 bootstrap 1000회
- 3-seed 요약은 val 때 쓴 `b1_three_seed_summary_20261108_v01.py`로 한다(seed t 구간 포함).
- **재현 기준을 미리 고정했다**(후보 문서 §4)
  - R1: 같은 표현 우세. 6개 비교 모두 3 seed 같은 부호이고 CI가 0을 포함하지 않아야 한다.
  - R2: CAD→LR이 최저 칸이고 LR 이미지에서 CAD − LR < 0이 재현되어야 한다.
  - R3: 일반화 순서는 기술만 한다.

## 2. 평가 B: Roboflow Real Test189 확인 결과

**위치와 기존 기록**
- 데이터: `/home/user/hh/isaac_cosmos/real_benchmark/cvut_pallets_bricks_original_v01/yolo_real_v01/`
  - data.yaml의 class는 `0: brick_load`
  - train 352(양성 287 + 음성 65) / val 48 / test 189
- 기존 평가: `/home/user/hh/isaac_cosmos/sdg_final/real_test189_eight_model_common_eval_v01/`
  - lock sha `58dda07b…`, 2026-10-05 개봉
  - 모델 8개: Combined 합성 전용 4개 + M50 실제 적응 4개

**검증 1 — 경로, 개수, 해상도, 라벨 형식**
- 이미지 189장. 라벨 txt 189개이고 각 파일에 polygon이 정확히 1줄이다.
- 해상도는 모두 972×1296(세로)이다. EXIF 회전 정보는 없다. annotation 사본에 회전이 이미 적용돼 있다.
- 정렬한 파일명 목록의 sha `f51a9b39…`가 기존 lock의 `test_filename_list_sha256`와 **일치**한다. 같은 189장이다.
- 이미지와 라벨 내용 sha inventory는 `c5d9fb3c…`(`real_test189_inventory.tsv`)다.

**검증 2 — 내용(189장 전부 GT 겹침 contact sheet로 육안 확인)**
- 모든 프레임이 **같은 현장에 있는 같은 빨강 점토 중공 블록 팔레트 1개**다. 비닐로 감겨 있고 제조사 인쇄가 있다. 지게차 포크 높이에서 찍었고 포크 끝이 보인다.
- **시멘트 벽돌은 보이지 않았다.** 다른 객체는 사람(얼굴이 식별되는 프레임 포함), 건물, 나무, 그리고 **라벨 없는 배경 벽돌·팔레트 더미**(visual block A1)다.
- metadata
  - macro scene은 모두 A
  - visual block A1 98 / A2 91
  - near-visual group은 21개(그룹 없음 29장)
  - real_tier는 모두 R_STRICT
- 따라서 189장은 사실상 대상 1개를 여러 거리와 각도에서 찍은 연속 프레임에 가깝다. **유효 표본 크기는 189보다 훨씬 작다.**

**검증 3 — 분할 보존, 중복, 누출**
- source group: test는 A만, train은 B 261 + D 26, val은 C 48이다.
- final source group, source_group_v03, near-visual group, visual block, macro scene 모두 **test와 train/val에 걸친 그룹이 0개**다.
- yolo 파일 간 정확 중복 hash는 0이다.
- Roboflow 원래 split과는 다르다. 이 test 189장은 원래 train 129 / valid 40 / test 20에서 왔다. 프로젝트에서 group 기준으로 다시 나눈 것이다(`split_v03`).
- **B1 모델은 실제 데이터를 학습이나 선택에 전혀 쓰지 않았다.** 따라서 B1 모델 기준으로는 누출 경로가 없다.

**검증 4·5 — 클래스, 인스턴스 정의, 라벨 종류**

| 항목 | B1(학습 라벨) | Real Test189 |
|---|---|---|
| 클래스 | 0 `brick_load` | 0 `brick_load`(이름과 id 같음) |
| 라벨 종류 | instance segmentation(canonical mask → polygon) | instance segmentation polygon(YOLO-seg). 원본 Roboflow는 bbox였고 SAM2.1로 mask를 만들었다 |
| 인스턴스 단위 | 팔레트 위 벽돌 적재 1더미 = 1 instance, 화면의 **모든** load(≥100px) | 이미지의 **대상 팔레트 1개만**. 배경 더미는 라벨 없음 |
| mask 범위 | 보이는 벽돌, 팔레트 제외 | 보이는 적재물(비닐 포함), 팔레트·사람·배경 제외 |
| 외형 | 낱장 벽돌(190×90×57mm) 75–300개, 포장 없음, 합성 렌더 | 대형 중공 블록, 비닐 포장과 인쇄, 실제 카메라 |
| 해상도 | 640×480 가로 | 972×1296 세로 |
| 장면 | B1 합성 현장, 여러 load, L1–L4 적재율 | 실제 현장 1곳, 가득 찬 팔레트 1개 |

- **형식은 그대로 호환된다.** polygon을 원해상도로 래스터화하는 것 말고는 변환이 없고, 임의 라벨 변환도 하지 않는다.
- **정의상 차이 두 가지가 결과에 영향을 준다.**
  - (i) 배경 더미를 맞게 찾아도 FP가 된다. 그래서 precision과 AP가 낮아질 수 있다. 이를 `fp_far`로 따로 보고하도록 했다. IGNORE 영역을 만들면 라벨 변경이 되므로 만들지 않는다.
  - (ii) 대상 외형이 B1과 크게 다르다.

**검증 6 — 기존 사용 이력과 이번 평가의 한계**
- Test189는 2026-10-05에 기존 8개 모델 평가로 이미 개봉됐다. "미개봉 test"가 아니다(AGENTS.md).
- 기존 M50 모델은 Test189로 선택되지 않았다(lock: selection/threshold/retraining from test 모두 false).
- 이번 B1 모델은 Test189와 무관하게 이미 고정돼 있다(checkpoint sha 고정, 실제 데이터 미사용). 따라서 이번 평가는 B1 모델에 대해 새로운 외부 점검이다.
- 다만 데이터는 연구자가 이미 본 적이 있다. GT는 SAM2.1 자동 생성이고 수동 QA 기록이 없다. 대상도 하나뿐이다.
- 기존 Combined 합성 전용 모델(YOLO11m, imgsz 1280)은 Test189에서 mask mAP50-95가 HR 0, LR 0, Proxy 0.0026, GeoCAD 0이었다. 예측이 아예 없는 이미지가 많았다(prediction_count_sanity_audit). **이번 합성 전용 B1 모델도 바닥 수준일 가능성이 있다.** 그래서 바닥 규칙을 미리 고정했다(§4).

## 3. 두 평가의 차이(결과 비교 시 반영)

| | A: B1 Synthetic Test | B: Real Test189 |
|---|---|---|
| 목적 | val 결과의 독립 재현(표현 효과) | 합성 전용 모델의 실제 사진 일반화 점검 |
| 이미지 | 합성 600장(200 장면 × 3 표현), 표현마다 다른 렌더 | 실제 189장, 한 세트를 9개 모델이 공유 |
| GT | HR canonical, 모든 load ≥100px, <100px IGNORE, FLAG 부분집합 | 대상 load 1개, IGNORE 없음 |
| 쌍대 단위 | 같은 장면 구성(표현별 렌더), base-scene bootstrap | 같은 실제 이미지, near-visual cluster bootstrap |
| 표현 효과의 의미 | 학습 표현 × 평가 표현 3×3 | 학습 표현만(평가 이미지는 실제) |
| 층 | L1–L4, 주/부, 크기, 가림, 거리 | visual block, GT 면적(거리 대용)만 |

## 4. 잠금 후보 프로토콜과 실행 명령

**파일(신규)**
- `docs/b1_synthetic_test_eval_protocol_LOCK_CANDIDATE_v01_20261108.{json,md}`
- `docs/real_test189_b1_eval_protocol_LOCK_CANDIDATE_v01_20261108.{json,md}`
- inventory: `reports/test_eval_protocols_20261108_v01/`
  - `b1_test_inventory.tsv`(sha `e3b37204…`)
  - `real_test189_inventory.tsv`(`1abd8746…`)
  - `checkpoints.tsv`(`177d696a…`)
- 코드
  - `analysis/eval_real_test189_b1_20261108_v01.py`(`f8271995…`)
  - `analysis/real_test189_b1_summary_20261108_v01.py`(`6832d7ca…`)
  - `scripts/preflight_test_eval_20261108_v01.py`(`1fd374d1…`)
  - `scripts/run_test_evals_20261108_v01.sh`(`6f5f6854…`)

**고정한 내용(두 평가 공통)**
- checkpoint 9개의 sha(집합 sha `2e9a02ec…`)
  - HR `27ba2931…` / `415b80d6…` / `f7394559…`
  - LR `0f6222d2…` / `151a6401…` / `66d44137…`
  - CAD `bdf634af…` / `a74c307b…` / `2c9739bf…`
- 추론: imgsz 640, conf 0.001, NMS 0.7, max_det 100, retina mask
- 작동점 conf 0.25 / IoU 0.5(조정 없음)
- 주 지표 mask mAP50-95(COCO 101점), 보조 지표 mAP50/75, P, R, pixel IoU, 전경 IoU
- seed별 결과, 3 seed 평균과 SD, 쌍대 bootstrap 1000회(seed 20261108), seed t 구간
- 금지: 결과로 재선정, 학습, HPO, 데이터 수정, 반복 실행

**평가별로 고정한 내용**
- A: 데이터 inventory sha `3911b8e2…`, manifest와 QA csv sha, FLAG 포함/제외, 층 7종, **재현 기준 R1–R3**
- B
  - 파일 목록 sha `f51a9b39…`(기존 lock과 같음), inventory sha `c5d9fb3c…`
  - GT 래스터화 규칙, IGNORE 없음, fp_far 별도 보고
  - 층: visual block, GT 면적 3구간(GT만 보고 정함, n 152 / 20 / 17)
  - 주 CI는 near-visual **cluster bootstrap**
  - **바닥 규칙:** 모든 표현의 seed 평균 mAP50 < 0.05이면 표현 비교는 기술만 한다.
  - 그림 선택 규칙(최저 3, 최고 3, 무작위 3)

**승인 절차와 강제 장치**
1. 연구자가 두 후보를 승인한다.
2. 후보 JSON에 `status: LOCKED`와 `approval{approved_by, approved_at, candidate_path, candidate_sha256}`만 더한 `..._LOCKED_v01_20261108.json`을 만든다.
3. `scripts/preflight_test_eval_20261108_v01.py --check <LOCKED 2개> --require-locked`가 다음을 확인한다.
   - 데이터와 checkpoint의 현재 sha
   - 후보와 LOCKED가 status/approval 말고는 같은지
4. 실행: `scripts/run_test_evals_20261108_v01.sh`(1회, 약 25–35분 예상)
   - 출력 root `/home/user/hh/isaac_cosmos/sdg_final/B1_TEST_EVAL_20261108_v01`가 이미 있으면 거부한다.
   - 코드 sha가 lock과 다르면 거부한다.
   - A 평가 → A 요약 → B 평가 → B 요약 순서이고, 결과 파일이 있는지로 완료를 판정한다.

**확인한 거부 동작(실행 없이 확인)**
- 지금 driver를 실행하면 `REFUSE: LOCKED protocol files missing`(exit 3)이 난다. 출력 폴더는 생기지 않는다.
- 실제 평가 코드
  - test에 lock이 없으면 거부한다.
  - 후보 lock으로 전체 실행하면 거부한다.
  - 후보 lock으로 `--preflight-only`를 하면 9개 sha와 데이터 sha가 일치한다(추론 없음).
- preflight `--require-locked`는 후보 상태에서 FAIL이다. 의도한 동작이다.

**엔지니어링 smoke(test 아님)**
- 실제 평가 코드를 **실제 val 48장**(source group C, test와 분리)에 SMOKE 모델(B1 HR 3 epoch 짧은 시험 checkpoint)로 실행했다. 본 모델 9개는 실제 데이터에 한 번도 적용하지 않았다.
  - `/home/user/hh/isaac_cosmos/sdg_final/REAL_EVAL_SMOKE_REALVAL_20261108_v01`: 그림 글자가 밝은 하늘에 묻혀 보이지 않아 v02에서 검은 머리띠로 고쳤다. 보존했다.
  - `/home/user/hh/isaac_cosmos/sdg_final/REAL_EVAL_SMOKE_REALVAL_20261108_v02`: 파이프라인 동작, 출력 파일 전체, 그림 9장, 요약 스크립트까지 확인했다.
- smoke 수치(3 epoch 모델, 의미 없음): mAP50-95 0.01, 작동점 검출 0.

## 5. 실행 전에 해결하거나 결정할 문제

1. **Test189 GT 품질(가장 중요).**
   - test mask는 Roboflow bbox → SAM2.1 자동 생성이고 수동 경계 QA 기록이 없다. polygon fidelity(0.99)는 SAM raster와의 일치일 뿐 사람 판정이 아니다.
   - 선택지
     - (a) 그대로 사용하고 "SAM 기반 GT, 수동 QA 미확인"으로 표기한다. 기존 결과와 같은 GT이므로 연결성이 유지된다. **권장.**
     - (b) 실행 전에 사람이 GT를 표본 검토한다. 단, 라벨을 수정하면 새 GT 버전이 되고 기존 결과와의 비교가 끊긴다.
2. **라벨 정의 차이.** 이미지당 대상 1개만 라벨이 있고 배경 더미는 없다. 사전 고정한 대로 IGNORE 없이 FP로 세고 `fp_far`를 따로 보고한다. 연구자가 이 방식에 동의해야 한다.
3. **외형과 domain 차이, 바닥 효과.** 비닐 포장 중공 블록은 B1 낱장 벽돌과 다르다. 기존 합성 전용 모델도 약 0이었다. 바닥이면 표현 비교는 결론을 내지 못하고, 이는 미리 고정한 규칙대로 보고한다.
4. **대상 1개, 현장 1곳.** 189장은 독립 표본이 아니다. 실제 일반화나 로봇 배치에 대한 주장으로 넓히지 않는다.
5. **개인정보.** 일부 프레임에 얼굴이 식별되는 사람이 있다. RGB 그림은 출력 root(Git 밖)에만 저장하고 GitHub에 올리지 않는다. 보고서에는 수치와 경로만 적는다. CVUT/Roboflow 데이터의 재배포 권한도 확인되지 않았다.
6. **B1 test의 사람 QA PENDING.** FLAG / LOW_SUPPORT 판정은 사람 승인 전이다. 결과에 제한으로 표기한다.
7. **기존 label cache.** `yolo_real_v01/labels/test.cache`(2026-10-05, 기존 Ultralytics 평가가 만든 파일)가 있다. 이번 코드는 Ultralytics val과 cache를 쓰지 않으며 데이터 폴더에 아무것도 쓰지 않는다. 기존 파일도 건드리지 않았다.
8. **후보를 LOCKED로 확정하는 연구자 승인.**

## 6. 기존 연구 결과와의 연결

| 구분 | 모델 | 실제 데이터 사용 | Test189 결과 |
|---|---|---|---|
| 합성 전용(기존) | Combined YOLO11m, imgsz 1280, HPO R5, 4 표현 | 없음 | mAP50-95 ≈ 0(HR 0, LR 0, Proxy 0.0026, CAD 0) |
| 실제 적응(기존) | M50: Combined 초기값 + 실제 train(B+D, 증강 991 pool) 50% 혼합, 실제 val C로 epoch 선택 | 있음 | 0.985–0.988(표현 차이 0.003 이내) |
| 합성 전용(이번 B1) | YOLO11n-seg, imgsz 640, recipe v03, 3 표현 × 3 seed | 없음 | 미실행(승인 대기) |

- **합성 전용 모델의 실제 일반화**는 기존 Combined와 이번 B1이 같은 질문에 답한다. 다만 구조(11m vs 11n), 해상도(1280 vs 640), 합성 데이터(Combined vs B1), 평가 코드(Ultralytics val, max_det 300 vs COCO 101점, max_det 100)가 달라서 수치를 그대로 비교하면 안 된다.
- **실제 적응 모델의 성능**(0.985 이상)은 실제 train / val을 쓴 결과다. B1 합성 전용 결과와 비교하면 "실제 데이터 적응의 효과"가 섞인다. 표현 효과로 읽으면 안 된다.
- **에셋 표현의 영향**은 같은 branch 안에서만 읽는다. B1 9개 모델끼리, 같은 189장의 쌍대 비교로만 본다.
- **모델, 해상도, 데이터, 프로토콜 차이**는 이번 설계로 분리되지 않는다. 기존 결과와의 비교는 기술 통계로만 한다(lock에 명시).
- **v43–v47(위치추정, 경로계획)과의 연결**
  - v43–v47은 M50 실제 적응 모델과 합성 건설현장 장면을 쓴 인식 → pose → planner 분석이다. B1 모델은 그 파이프라인에 들어간 적이 없다. 그러므로 Test189 결과를 v43–v47의 pose나 경로 성능으로 옮길 수 없다.
  - 연결 가능한 부분은 두 가지다.
    - (i) B1 합성 전용 모델이 Test189에서 바닥이면, 실제 배치 전에 실제 데이터 적응(M50 같은 단계)이 필요하다는 기존 결론을 다시 확인하게 된다.
    - (ii) v45의 "CAD 모델 우세"는 M50 계열에서 선택 mask IoU로 얻은 결과다. B1 합성과 실제 결과로는 이를 직접 검증할 수 없다(통합 보고서 §8).
  - 이번 단계에서 로봇 주행이나 위치추정 실험은 하지 않았다.

## 7. 최종 판단

- **평가 A(B1 Synthetic Test): 실행 가능.** 데이터, GT, 코드, checkpoint, 통계, 재현 기준이 모두 고정됐고 preflight PASS다. 남은 것은 LOCKED 승인뿐이다.
- **평가 B(Real Test189): 조건부 실행 가능.**
  - 형식은 호환되고 데이터 무결성(기존 lock과 같은 189장, 누출 0)도 확인했다. 코드 smoke도 PASS다.
  - 실행 전에 연구자가 세 가지를 명시적으로 받아들여야 한다.
    - §5-1: SAM 기반 GT, 수동 QA 기록 없음
    - §5-2: 배경 더미를 FP로 처리
    - §5-5: 그림은 Git 밖에 저장
  - 결과는 "물체 1개, 현장 1곳의 외부 점검"으로 해석을 제한한다.
- 승인 메시지에 두 프로토콜 승인과 §5-1·2 처리 방식(권장: 그대로 사용)을 함께 적어 주면, LOCKED JSON 생성 → preflight → 1회 실행으로 진행한다.

## 파일

- 신규
  - `docs/*_LOCK_CANDIDATE_v01_20261108.{json,md}` 4개
  - `analysis/eval_real_test189_b1_20261108_v01.py`
  - `analysis/real_test189_b1_summary_20261108_v01.py`
  - `scripts/preflight_test_eval_20261108_v01.py`
  - `scripts/run_test_evals_20261108_v01.sh`
  - `reports/test_eval_protocols_20261108_v01/`(inventory 3개)
- 외부 root(Git 밖): `REAL_EVAL_SMOKE_REALVAL_20261108_v01`, `REAL_EVAL_SMOKE_REALVAL_20261108_v02`(실제 val smoke 출력과 그림)
- 변경 없음: 기존 데이터, 라벨, 모델, val 결과, 기존 Test189 평가 폴더
