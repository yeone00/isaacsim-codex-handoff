# B1 / Jeonju 학습용 합성데이터 재생성 준비

조사·실행일: 2026-11-03 KST. **기준 환경은 `B1_CLOSED_EV.usdz`로 선정했다. 별도 Stage 구성, HR/LR/GeoCAD 18장 렌더, 공통 canonical annotation, YOLO 변환 및 CPU 로더 연결까지 실행했다.** 전체 8,400장 생성과 학습은 수행하지 않았다. 실행 경로는 준비됐지만, 기존 ISO400 조명을 그대로 이식했을 때 나타난 하이라이트 포화와 새 배경의 전체 가시성 검사는 미해결이다. 따라서 상태는 **소규모 연결 검증 PASS / 대량 생성 품질 미승인**이다.

기존 `Constructionsite_isaac.usdz`는 평가용으로 유지했다. 원본 USDZ·브릭·기존 코드·평가 Stage·PROJECT_STATE는 변경하지 않았다. 검사 대상 20개 입력 SHA256이 작업 전 기록과 일치한다. 물리 재생·로봇 이동·ROS·학습·optimizer update는 모두 0이다.

## 1. 환경 선정과 사용 범위

| 항목 | B1_CLOSED_EV | Jeonju_122151 |
|---|---|---|
| 실제 렌더에서 확인한 구역 | 길게 열린 통로, 반복 기둥, 가림막, 현장 물품 | 엘리베이터·콘크리트 전실 중심 |
| 이번 작업 적합성 | 여러 파레트와 거리 변화에 사용할 통로가 비교적 명확 | 선택 가능한 전실 배경은 있으나 이번 목적에서는 B1 통로가 편리 |
| 결정 | **학습용 기준으로 선정** | 대안으로 보존, 이번 브릭 smoke는 수행하지 않음 |

두 파일의 렌더에서 확인한 구역은 다르다. 같은 건물의 일부인지, 동일 스캔의 다른 crop인지까지 증명하지 않았다. 선정에는 완전한 동일성 증명이 필요하지 않다. 이전 실제 렌더와 구조 검사는 [환경 비교 보고서](alternative_environment_asset_review_20261103.md)에 있다.

두 환경은 NuRec Volume 기반이며 이전 구조 검사에서 Mesh/Collision/Rigidbody가 없었다. 이번 용도는 정적 RGB와 annotation 생성이다. **화면에 보이는 바닥을 물리적으로 주행 가능한 바닥으로 인증한 것이 아니다.** NuRec의 외관은 Mesh와 동일하게 재조명되지 않으며 스캔에 포함된 사람·물체 잔상도 배경 특성이다. 제작자·이용 권한은 여전히 UNKNOWN이며 [출처 조사](construction_environment_usd_provenance_audit.md)의 결론을 사용 가능 승인으로 바꾸지 않는다.

원본 경로:

```text
/home/user/hh/isaac_cosmos/assets/assets/environment/B1_CLOSED_EV.usdz
/home/user/hh/isaac_cosmos/assets/assets/environment/Jeonju_122151.usdz
```

B1 SHA256: `de908a9e91ab433556db57d2e584422801a3e93f3d469b6bf2c324ecb9e0586d`.

## 2. ROI, 좌표계 및 새 Stage

작업 루트:

```text
/home/user/hh/isaac_cosmos/sdg_final/B1_SYNTHETIC_REGEN_PREP_20261103_v01
```

이하 `P`는 위 경로다. 새 Stage는 `P/smoke_HR_Scan_v01/preview_stage.usda`이며 LR·GeoCAD에도 별도 preview가 있다. B1과 정규화 브릭을 참조한다. 기존 평가 Stage는 참조하거나 수정하지 않는다. Preview는 첫 번째 red 장면 `B1_TRN_000027`을 저장했으며 카메라는 `/World/B1Training/Camera`다.

| 정의 | 값 / 확인 범위 |
|---|---|
| 작업 root | `/World/B1Training`, 원점 world `(0,0,0)m`, Z축 회전 +90° |
| 좌표 대응 | local +X → world +Y, local +Y → world −X |
| 사용 ROI | **world x=[−2.0,+2.0], y=[−0.9,+7.7]m** |
| 바닥 기준 | world z=0m, 시각적 임시 기준. 측량한 평탄도·높이 아님 |
| 카메라 | local 높이 0.600m, 원점 주변 기존 jitter, 주 목표 방향으로 조준 |
| 주 파레트 위치 | local `(jitter_x + distance, jitter_y, 0)` |
| 복수 파레트 | 기존 `cluster_offsets` 그대로, 최대 5개 |
| 전체 manifest 기하 검사 | 회전된 1.1×1.1m 파레트 footprint **2800/2800이 선언 ROI 안** |

ROI 검사는 배치 사각형의 범위 검사다. 벽과의 교차, 실제 support, NuRec 표면과의 접촉을 검증하지 않는다. 인공 바닥이나 collider는 추가하지 않았다. 카메라와 물체에 같은 root 변환을 적용했으며, 평가용 rover 시작 자세와 연결하지 않는다.

![실제 ROI 카메라와 브릭 배치](synthetic_dataset_regeneration_plan_b1_jeonju_20261103_v01/roi_and_placement.png)

왼쪽은 물체 없는 실제 B1 렌더, 오른쪽은 기존 브릭/파레트를 배치한 실제 렌더다. ROI 전체가 한 카메라에 모두 보인다는 뜻은 아니다. 수치 ROI와 각 장면의 카메라 world matrix는 config/ledger에 별도로 기록했다.

## 3. 기존 파이프라인 연결과 변경점

초기 placeholder 개발 설정 대신 실제 최종 nominal v03 manifest와 production 코드를 사용했다.

| 단계 | 재사용한 실제 근거와 동작 |
|---|---|
| 표본·split | `final_experiment_base_manifest_2800_v03.csv`, SHA `2a4782911ef334fc640e9f90ee8120e48ab3c30e25da47603004978835626bf8` |
| RGB 배치/카메라 | `/home/user/step21_b2b_production_rgb_iso400_v02.py`의 순수 함수·상수만 AST로 추출 |
| 브릭 | `_normalized/{red,cement}_brick_{HR_Scan,LR_Scan,GeoCAD}.usd`, v43 기록의 자산 해시 대조 |
| canonical | `/home/user/nonideal_canonical_nominal_replay_v02.py`의 solid 5-brick bundle 패턴, load별 하나의 instance |
| YOLO 변환 | `/home/user/canonical_gt_to_yolo_seg_v03.py`의 기존 contour 연결/직렬화 함수 |
| 학습 설정 | `FINAL_MODEL_DEVELOPMENT_LOCK_v01.json`, HPO_R5 JSON 및 최종 HR `args.yaml` |

레거시 Python 모듈의 top-level을 import하거나 실행하지 않았다. 기존 코드의 실행 부작용을 피하고 정적으로 읽은 함수만 새 Stage에 연결했다. 원본 hash와 사용한 함수는 새 코드와 `run_manifest.json`에 기록했다.

유지한 항목:

- paired scene seed, material, load/layer 수, A/B 적층, yaw, 거리, gap, jitter, LG1–LG5, split membership.
- RGB 640×480, focal 18.14756mm, aperture 20.955/15.291mm, 높이 0.6m, rt_subframes=8, 준비 5회+capture 1회.
- ISO400, shutter50, fNumber5, tonemap6. 물리 시간은 진행하지 않는다.
- 정규화 브릭 190×90×57mm에 기존 rotateX −90° 적용: 배치 footprint 190×57mm, 층 높이 90mm. 75 bricks/layer, 파레트 1.1×1.1×0.144m. 실제 생성 개수 검사 통과.
- annotation class0 `brick_load`, 파레트 unlabelled, canonical mask 100px 이상 조건. bbox는 같은 마스크에서 파생한다.
- 공통 canonical은 개별 HR/LR/CAD의 실제 표면 silhouette와 다를 수 있는 **기존 정의**다. 기존 GT 파일을 가져다 붙이지 않고 새 B1 카메라에서 다시 렌더했다.
- polygon은 RETR_EXTERNAL/CHAIN_APPROX_SIMPLE, 단순화 없음, 분리 contour는 기존 최소 bridge로 연결, 정규화 좌표 소수점 6자리. bitmap master도 보존.

명시적으로 바뀐 항목:

- 학습 배경 B1, 새 `B1_` scene ID, 새 출력 경로.
- 기존 A_OPEN/B_STRUCTURAL/C_CLUTTER의 **서로 다른 공간 anchor를 하나의 B1 ROI로 통합**했다. 기존 zone은 `source_zone`으로 남겼다. 따라서 과거 세 공간의 분포까지 재현했다고 주장하지 않는다.
- 기존 jitter를 ROI의 local anchor로 사용했다. 원본 zone anchor 및 과거 visibility/replacement 열은 계보 기록이다. **기존 배경에서 얻은 visibility 수치는 B1의 유효성 판정에 사용하지 않는다.**
- 현재 요청의 HR/LR/CAD 3종을 실행했다. Proxy는 8개 자산 registry에 보존했으며 생성하지 않았다. LR은 저취득 조건에서 독립 재구성한 표현이며 HR decimation이 아니다.

## 4. 실제 실행 결과

smoke는 deterministic train 4개·val 2개 scene을 선택했다. red/cement, 1/2 loads, A/B 패턴을 포함하며 test RGB는 열거나 렌더하지 않았다.

| 검사 | 실제 결과 |
|---|---|
| B1 + HR/LR/GeoCAD import·RGB capture | **각 6/6, 총 18장 PASS** |
| smoke load/brick 생성 수 | 각 표현 8 loads, 기대 brick 수와 일치 |
| 새 공통 canonical | 6 scenes, **8개 load 마스크**, primary 6/6 ≥100px |
| YOLO export | `yolo_smoke_v02`, 각 표현 train4/val2/test0 |
| polygon과 bitmap 일치 | **8/8 IoU=1.0, XOR=0**. 전체 데이터에 일반화하지 않음 |
| 실제 Ultralytics CPU 로더 | **18/18 이미지·class·segmentation mask decode PASS** |
| 학습 recipe API 검증 | `get_cfg` PASS, 학습/optimizer step 0 |
| 2800개 배치 범위 | footprint ROI 내부 2800, 외부 0 |
| 원본 보존 | 등록한 입력 **20/20 SHA 일치** |
| 대량 렌더/전체 가시성/학습 | **NOT_RUN** |

![실제 동일 장면 HR LR CAD 비교](synthetic_dataset_regeneration_plan_b1_jeonju_20261103_v01/matched_three_rep_camera_panel.png)

![실제 RGB 위 공통 canonical mask와 bbox](synthetic_dataset_regeneration_plan_b1_jeonju_20261103_v01/canonical_mask_bbox_overlay.png)

18개 RGB에서 공유하는 마스크는 8개다. 표현별로 연결된 총 24개 instance label을 24회의 독립 관측으로 세지 않는다.

**첫 실패도 보존했다.** Isaac runtime와 기본 Python에는 ultralytics가 없어 import probe가 실패했다. 설치하지 않고 기존 `sdg_tools` 환경을 찾았다. 최초 exporter는 새 metadata 병합의 중복 key로 실패했으며 `yolo_smoke_v01`을 보존했다. 새 adapter의 병합을 수정하여 `yolo_smoke_v02`가 통과했다. RGB를 다시 생성하거나 실패 출력을 덮지 않았다. `failed_attempts.json`에 기록했다.

## 5. 즉시 실행 가능 여부와 남은 품질 문제

**Stage 구성·브릭 배치·annotation export·YOLO 입력 연결은 실행 가능하다. 완성된 학습 데이터셋이라고 부를 단계는 아니다.**

1. **하이라이트 포화:** 기존 조명값을 그대로 유지한 결과, `B1_TRN_000033` cement의 공통 목표 마스크 안에서 RGB 세 채널 모두 ≥250인 비율이 HR 95.315%, LR 79.622%, CAD 97.818%다. CAD `B1_VAL_000058` red도 75.876%다. 이는 새 성공 기준이 아닌 진단 수치다. 흰 영역의 세부 정보가 약하므로 자연스러운 합성 또는 인식 학습 품질을 PASS로 확정하지 않는다. 원본 material이나 frozen 조명값을 몰래 수정하지 않았다. 전체 수치는 `photometric_smoke_18.csv`에 있다.
2. **새 배경의 전체 QA:** 기존 v03 배경의 primary visibility≥0.5 선별 이력을 B1에 승계할 수 없다. 이번 adapter는 ≥100px mask와 생성 수를 확인하지만, isolated denominator를 통한 visibility ratio, 전체 2800개의 벽·기둥 간섭 및 sparse 배경 품질은 검사하지 않았다. 기존 가시성 조건을 유지하는 새 B1 QA를 전체 생성과 함께 수행해야 한다. sample을 조용히 삭제·교체해서는 안 된다.
3. **시각적 접촉:** z=0은 임시 기준이고 NuRec에는 지원 Mesh가 없다. 일부 시점에서는 파레트가 떠 보이거나 그림자 접촉이 부자연스러울 수 있다. 정적 RGB 배치와 물리 support 검증을 구분한다.
4. **권한:** B1/Jeonju의 출처·라이선스는 UNKNOWN이다. 데이터·논문 이미지를 공개할 권한은 이 기술 smoke로 확인되지 않는다.

다음 품질 조치는 **train 장면만 사용한 공통 photometric 설정 검토 → 필요하면 새 배경 전용 설정을 별도 버전으로 명시 → 동일한 3표현 smoke 재확인**이다. 표현별로 다른 노출을 맞추거나 test/Real Test189 성능으로 설정을 고르면 안 된다. 기존 ISO400 recipe에서 설정이 달라지면 변경 사실을 기록해야 하며 이번 작업에서 승인·확정된 것으로 취급하지 않는다. 원본 에셋의 material 교체나 새 방법론 도입은 하지 않았다.

## 6. 데이터 구성과 YOLO 학습 연결

계획된 새 B1 데이터는 paired base 2800개, 표현별 train2000/val400/test400, 총 **8400 RGB**다. 같은 base scene은 표현 사이에서 동일 split에 놓인다. 새 B1 internal test이며 기존 Constructionsite 시뮬레이션 평가와 별개다. 기존 Real Test189는 이미 평가된 자료이고 설정 선택에 재사용하지 않는다. 실제 외부 검증은 red-only 범위를 유지한다.

`P/yolo_smoke_v02/{HR_Scan,LR_Scan,GeoCAD}/data.yaml`은 실제 CPU 로더가 읽었다. 정사각 letterbox 후 image/mask 텐서까지 확인했으며 GPU 학습·증강 통과를 의미하지 않는다. 각 이미지와 공통 label은 새 출력에 symlink로 연결한다. 원본 브릭·기존 RGB/GT는 복사하거나 변경하지 않는다.

학습 adapter는 기존 polygon YOLO11m-seg/HPO_R5 설정을 불러온다. 초기 가중치 `/home/user/yolo11m-seg.pt`, imgsz640, epochs150, AdamW, seed42, AMP, 기존 mosaic/HSV 등 증강을 유지한다. 새 HPO를 수행하지 않는다. 설정 API를 확인한 현재 training runtime은 `sdg_tools`, ultralytics **8.4.129**다. 역사적 전체 환경과의 완전한 bitwise 재현을 주장하지 않는다.

요청 batch64와 과거 freeze에 기록된 실제 physical batch32의 차이는 `training_command_plan.json`에 남겼다. 새 adapter는 64로 명시하며 조용히 낮추지 않는다. GPU 메모리·실제 training step qualification은 미실행이다. v40–42의 별도 bitmap/noaug 경로 및 v42 resume qualification 실패는 해결했다고 간주하지 않고, 이번에는 실제 완료 이력이 있는 기존 polygon 경로를 사용했다.

## 7. 실행 파일과 다음 단계

새 코드:

- `scripts/prepare_b1_sdg_regeneration_20261103_v01.py`: 입력 hash/lock 확인, paired manifest·ROI·recipe 생성.
- `scripts/b1_sdg_capture_20261103_v01.py`: 새 Stage RGB와 선택적 공통 canonical, scene별 완료 ledger/resume.
- `scripts/export_b1_yolo_20261103_v01.py`: 공통 canonical→기존 polygon·bbox·YOLO 패키지.
- `scripts/check_b1_sdg_preparation_20261103_v01.py`: 입력 보존·2800 footprint·실제 CPU loader 검사.
- `scripts/train_b1_historical_recipe_20261103_v01.py`: 기본은 설정 dry-run, 별도 실행 flag가 있어야 학습.
- `scripts/visualize_b1_sdg_preparation_20261103_v01.py`: 실제 렌더 기반 비교 패널과 annotation overlay.

이미 수행한 연결 검사는 아래 명령으로 만든 새 결과에 기록되어 있다. 같은 output에 재실행하면 덮어쓰지 않고 실패하도록 구성했다.

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python scripts/check_b1_sdg_preparation_20261103_v01.py \
  --prep /home/user/hh/isaac_cosmos/sdg_final/B1_SYNTHETIC_REGEN_PREP_20261103_v01 \
  --dataset /home/user/hh/isaac_cosmos/sdg_final/B1_SYNTHETIC_REGEN_PREP_20261103_v01/yolo_smoke_v02 \
  --output /home/user/hh/isaac_cosmos/sdg_final/B1_SYNTHETIC_REGEN_PREP_20261103_v01/loader_checks_v01
```

**향후 전체 생성 명령 형태** — 이번에는 실행하지 않았고 위 품질 문제 해결 후 새 출력명으로 사용한다. 아래는 HR 예시다. LR_Scan/GeoCAD도 같은 config/manifest로 각각 fresh Kit에서 실행하며 `--canonical`은 HR 공통 pass에만 붙인다. 동시 GPU 실행을 전제하지 않는다.

```bash
/home/user/anaconda3/envs/hh_isaac51/bin/python -u scripts/b1_sdg_capture_20261103_v01.py \
  --config /home/user/hh/isaac_cosmos/sdg_final/B1_SYNTHETIC_REGEN_PREP_20261103_v01/config.json \
  --output /home/user/hh/isaac_cosmos/sdg_final/B1_SYNTHETIC_REGEN_PREP_20261103_v01/production_HR_Scan_future_v01 \
  --representation HR_Scan --mode production --canonical --allow-production
```

`--allow-production`은 실수 방지용 실행 flag이며 품질 승인이나 권한 확인을 대신하지 않는다. 중단된 **동일 실행**에는 `--resume`을 추가할 수 있고 config/representation hash 확인 후 완료 scene을 건너뛴다. 전체 생성 전 위에서 지적한 visibility QA를 연결해야 한다.

순서는 **노출·접촉 검토 및 B1 QA 연결 → 세 표현 전체 RGB/공통 GT 생성 → 2800 pairing·가시성·polygon fidelity 검사 → exporter로 새 YOLO 패키지 → training adapter dry-run → 별도 GPU qualification과 YOLO 재학습**이다. Exporter는 `--config`, HR/LR/CAD 세 `--runs`, 새 `--output`을 받는다. Training adapter는 `--prep`, 완성된 `--dataset`, 새 `--output`을 받으며 기본은 학습하지 않는다. `--execute-training`은 전체 2000/400/400 패키지가 확인되어야 실행된다. 현재 smoke 데이터에는 학습 실행을 허용하지 않는다.

## 8. 보존과 인수인계

핵심 증거는 `P/run_manifest.json`, `source_authority_checks.json`, `preflight_v01/roi_footprint_preflight_2800.csv`, `loader_checks_v01/checks.json`, `yolo_smoke_v02/package_checks.json`, `polygon_fidelity.csv`, `bbox_instances.csv`, `training_dryrun_v01/training_command_plan.json`이다. 각 capture의 `invocation.json`, `status.jsonl`, `capture_ledger.json`, `used_layer_sha256.json` 및 stdout을 보존했다. 새 코드의 SHA도 manifest에 있다.

PROJECT_STATE SHA256은 작업 전후 `d919282dee1a880b3b5ca678563697e7fb45cf0b650b494801b918a95d7f19aa`로 동일하다. 보고서와 새 코드·새 이미지/Stage/JSON만 생성했다. 작업 디렉터리에 Git 저장소가 확인되지 않아 remote sync는 UNKNOWN이며 push하지 않았다.

**최종 판단:** B1 통로 ROI가 이번 학습 배경의 기준이다. 기존 배치·canonical·YOLO 흐름은 실제로 연결됐고 18장 smoke로 실행 증거를 확보했다. 다만 밝은 조건의 디테일 손실과 전체 새 배경 QA가 남아 있으므로, 대량 생성·YOLO 재학습 준비가 무조건 완료됐다고 보고하지 않는다. 기존 평가 환경과 기존 결과는 그대로 유지한다.
