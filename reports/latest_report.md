# B1 적벽돌 HR/LR/CAD 촬영 품질 개선

실행일: 2026-11-03 KST. **적벽돌 전용 manifest를 새로 만들고, 추가 ROI 5곳을 실제 렌더했다. 추천 3곳에서 HR/LR/CAD 동일 조건 72장을 비교하여 브릭·파레트의 과다 노출을 개선했다.** 전체 데이터 생성과 YOLO 학습은 수행하지 않았다.

추천은 **R1 기둥 통로를 기본, R5 반대 방향 통로와 R4 자재 배경을 보조**로 사용하는 것이다. 공통 촬영 제안은 **ACES(op6), ISO25, shutter50, fNumber5, dome intensity=`8000+0.05×기존값`**이다. 세 표현에 같은 식을 적용했다. 이는 기존 조명 범위를 명시적으로 변경한 새 제안이며 과거 ISO400 실험 결과를 대체하지 않는다.

작업 루트 `P`:

```text
/home/user/hh/isaac_cosmos/sdg_final/B1_RED_QUALITY_20261103_v01
```

## 1. 실행 범위와 판정

| 항목 | 실제 실행 결과 |
|---|---|
| 노출 분리 진단 | 같은 train 장면 2개 × 최초 10설정 + 후속 4설정 = 28개 HR RGB |
| ROI 탐색 | 기존 R0 + **추가 5곳**, 각 빈 환경과 실제 HR 적벽돌 렌더 |
| 상세 paired 비교 | 3 ROI × 4 train 장면 × 2촬영 설정 × 3표현 = **72 RGB** |
| 빈 환경 | 위 모든 촬영과 같은 pose/settings로 106장, 전체 RGB는 배치106+빈환경106=212장 |
| canonical/YOLO | 36개 load 마스크 저장, polygon **36/36 IoU1.0·XOR0** |
| 실제 CPU 데이터 로더 | **72 이미지·108 instance label decode PASS**, 학습 없음 |
| 새 적벽돌 manifest | **1400개 paired scene**, train1000/val200/test200, cement0 |
| 향후 전체 이미지 수 | 적벽돌 1400×3=**4200장**. 기존 두 재질 8400장 계획과 구분 |
| 보존 확인 | 입력20 SHA, 이전 준비 출력117파일, 이전 준비 코드 모두 불변 |
| 미검증 | 전체1400의 시각 품질·NuRec 가림·바닥 높이/접촉·물리 지지 |

상세72장은 독립 base scene 4개의 반복 조건이다. 노출 진단까지 포함한 서로 다른 source train scene은 6개다. 저장된 canonical36개는 노출/ROI 반복을 포함하고 byte hash는 6종이다. 이를 36개의 독립 장면 또는 메트롤로지 검증으로 세지 않는다. test/val 이미지를 촬영 조건 선택에 사용하지 않았다.

## 2. 노출·톤매핑·조명을 나눈 진단

기존 설정은 실제 renderer에서 ISO400/shutter50/fNumber5/op6이었다. 같은 geometry·camera·원본 material을 유지하고 ISO100/25/6.25, shutter200, fNumber10, dome×0.1/0.01, op0을 각각 비교했다. 후속으로 ISO100+shutter200+fNumber10, Reinhard(op2), Hable(op5)를 비교했다.

설치된 `omni.rtx.settings.core`의 `post_widgets.py`에서 **op0=Clamp, op6=ACES**를 확인했다. Clamp는 exposure adjustment를 건너뛴다는 로컬 설명과 실제 거의 흰 렌더가 일치했다. op0을 노출 개선안으로 채택하지 않았다. 파일 위치와 SHA는 `P/run_manifest.json` 및 아래 근거 기록에 남겼다.

직접 비교 결과:

- ISO100, shutter200, fNumber10 각각은 비슷한 감소 효과를 보였다. 하지만 밝은 LG5 장면에서는 파레트 clipping이 남았다.
- `B1_TRN_000005`에서 ISO25만 적용해도 실제 파레트 표면의 any-channel=255 비율이 **96.24%**였다. ISO6.25는 이를 제거했지만 덜 밝은 장면의 HR 표면이 지나치게 어두워졌다.
- 조명만 줄이는 것도 삽입된 브릭·파레트에 영향을 주었다. NuRec 배경과 Mesh가 동일한 방식으로 재조명된다고 가정하지 않았다. 같은 camera에서 빈 배경도 별도로 저장했다.
- 따라서 표현별 노출 보정 대신 **공통 ISO25 + 공통 조명 범위 압축**을 상세 paired 실험에서 확인했다. model AP·test 성능·학습 결과로 설정을 고르지 않았다.

![두 파레트 밝은 장면의 노출 후보](b1_red_brick_sdg_quality_optimization_20261103_v01/exposure_comparison_B1_TRN_000005.png)

[다른 동일 장면의 14개 조건 비교](b1_red_brick_sdg_quality_optimization_20261103_v01/exposure_comparison_B1_TRN_000027.png). 수치는 `P/analysis_v01/exposure_metrics_28.csv`에 있다. 최종 조합은 아래의 별도72장 paired 결과로 평가한다.

**첫 실행 오류 보존:** 최초 노출20장 세션은 exit0와 `PASS_CAPTURE` JSON을 남겼지만, 빈 Stage에서 instance-ID annotator가 빈 배열을 처리하며 **renderer Error120건**을 기록했다. 이 세션을 clean PASS로 취급하지 않는다. RGB·원본 로그를 보존했고, v03부터 빈 배경 촬영 중 ID annotator를 detach한 뒤 물체 생성 후 attach하도록 수정했다. 이후 ROI/후속노출/HR/LR/CAD의 **5세션은 renderer Error0**이었다. prototype 등 Warning은 삭제하지 않았다. 후속 구현은 실제 brick/pallet ID mask가 비어 있으면 실패한다.

## 3. 추가 ROI 5곳과 카메라

모든 survey에는 동일한 HR 적벽돌 `B1_TRN_000027`과 ISO25를 사용했다. source jitter를 유지했으므로 아래 실제 camera 좌표는 ROI root 원점과 다르다. yaw는 world +X 기준 반시계, 모든 survey의 camera pitch는 **−5.0845°**, 높이는 world z≈0.600m다. 640×480 및 기존 렌즈는 그대로다.

| 후보 | 실제 camera xyz(m) | yaw | 확인한 장점 / 단점 | 판단 |
|---|---|---:|---|---|
| R0 기존 | (−0.077,0.337,0.600) | +90° | 통로 확보 / 벽·천장 스캔 얼룩 | 대조군 |
| **R1_NORTH_2** | (−1.077,2.337,0.600) | +90° | 기둥·벽 배경, 비교적 단순한 앞 바닥 / 벽 얼룩·광원 잔상 | **기본 추천** |
| R2_NORTH_4 | (0.923,4.337,0.600) | +90° | 목표 색 대비 / 가까운 벽 blur·우측 청록 잔상 | 비추천 |
| R3_NORTH_7 | (−0.077,7.337,0.600) | +90° | 배경 변화 / 벽·기둥이 목표 RGB를 심하게 간섭 | **제외** |
| **R4_EAST** | (−2.663,1.077,0.600) | 0° | 벽·자재·구조가 비교적 선명 / 적색 배경 물품·전경 검은 상자·바닥 얼룩 | **clutter 보조** |
| **R5_WEST** | (1.663,0.923,0.600) | 180° | 넓은 통로·기둥·바닥 배경 / 전경 상자와 밝은 배경 광원 | **보조 추천** |

![빈 환경과 실제 HR 배치: 기존1+추가5](b1_red_brick_sdg_quality_optimization_20261103_v01/roi_empty_and_HR_6.png)

선정 구역의 root 및 **배치 검토 사각형**은 다음과 같다. 아래 범위 전체가 collision-free이거나 측정된 평탄 영역이라는 뜻은 아니다. 실제 상세 촬영은 다음 절의 네 장면에 한정된다.

| 추천 ROI | root 원점 / 회전 | world 검토 구역 |
|---|---|---|
| R1 | (−1,2,0)m / +90° | x[−3,1], y[1.1,9.7]m |
| R5 | (2,1,0)m / 180° | x[−5.7,2.9], y[−1,3]m |
| R4 | (−3,1,0)m / 0° | x[−3.9,4.7], y[−1,3]m |

local 검토 범위는 전방 X[−0.9,7.7], 횡방향 Y[−2,2]m다. 원본 camera/object에 같은 rigid root 변환을 적용한다. camera matrix, 빈 이미지, 배치 이미지, load/brick 개수 및 pallet world bbox는 각 run의 `capture_ledger.json`과 `analysis_v01/roi_metrics_6.csv`에 있다.

**중요한 NuRec annotation 제한:** R3는 RGB에서 벽 간섭이 보였지만 실제 brick instance-ID 면적이 R0와 똑같이 **16397px**였다. 따라서 ID/segmentation만으로 NuRec 체적 렌더의 가림을 충분히 반영한다고 확인할 수 없다. 이 후보를 mask 면적만 보고 통과시키지 않았다.

![제외한 R3의 RGB와 ID mask](b1_red_brick_sdg_quality_optimization_20261103_v01/R3_rejected_RGB_and_ID.png)

## 4. 추천 구역의 HR/LR/CAD 동일 조건 비교

| source train scene | 역할 | 거리 | 층/loads | 기존 광도 factor |
|---|---|---:|---|---|
| TRN_000889 | 가까운 정상 적재 | 1.356m | 4층/1 | LG1 |
| TRN_001420 | 먼 정상 적재 | 3.537m | 4층/1 | LG3 |
| TRN_001074 | 가까운 부분 적재 | 1.276m | 1층/2 | LG5 |
| TRN_001736 | 먼 부분 적재 | 3.910m | 1층/2 | LG2 |

source seed·yaw·gap·cluster·jitter·camera look-at을 유지했다. 각 ROI와 설정에서 **HR/LR/CAD camera matrix·seed·촬영 설정 exact equality 24 triplets PASS**다. 정상/부분 적재는 기존 layer/load 설정이며 새로운 O25/O50 차폐판 실험을 도입하지 않았다.

![먼 정상 적재의 동일 HR LR CAD](b1_red_brick_sdg_quality_optimization_20261103_v01/improved_FAR_FULL.png)

[가까운 정상](b1_red_brick_sdg_quality_optimization_20261103_v01/improved_NEAR_FULL.png) · [가까운 부분](b1_red_brick_sdg_quality_optimization_20261103_v01/improved_NEAR_PARTIAL.png) · [먼 부분](b1_red_brick_sdg_quality_optimization_20261103_v01/improved_FAR_PARTIAL.png) · [HR 기존/개선 대조](b1_red_brick_sdg_quality_optimization_20261103_v01/HR_baseline_vs_improved.png)

LR의 줄무늬·어두운 질감과 CAD의 비교적 균일한 표면은 원본 상태로 남겼다. 서로 같은 외관이 되도록 texture/material 또는 표현별 exposure를 바꾸지 않았다. LR은 독립 저취득 재구성이며 HR decimation이 아니다.

## 5. 정량 품질과 annotation

clipping은 **RGB 중 하나 이상이 정확히255인 픽셀 비율**이다. near-white는 세 채널 모두≥250, near-black은 세 채널 모두≤5다. HSV의 높은 색 포화도와 밝기 clipping을 구분하여 CSV에 따로 기록했다. 아래는 동일한12 ROI/scene 조건에 대한 **scene별 비율의 단순 평균**이며 통계적 우열 검정이 아니다.

| 실제 표면 ID mask | HR 기존→개선 | LR 기존→개선 | CAD 기존→개선 |
|---|---:|---:|---:|
| 브릭 clipping | 22.562% → **0%** | 18.253% → **0%** | 55.788% → **0%** |
| 파레트 clipping | 95.351% → **0%** | 95.345% → **0%** | 96.624% → **0%** |
| 전체 RGB clipping | 18.281% → 0.661% | 17.727% → 0.663% | 21.052% → 0.661% |

![동일 조건 clipping 비교](b1_red_brick_sdg_quality_optimization_20261103_v01/clipping_comparison.png)

개선36장의 실제 브릭·파레트 표면에서는 **각 장면 모두 clipping0**이었다. 공통 canonical 영역은 실제 구멍·edge·background를 포함할 수 있으므로 동일 수치로 혼동하지 않는다. 그 영역의 clipping 평균은 HR0.057%/LR0.063%/CAD0.051%, 최대는 각각0.480%/0.551%/0.427%였다.

밝은 세부를 되찾는 대신 어두운 표면 비율은 늘었다. 개선 브릭 near-black 평균은 HR7.177%/LR9.874%/CAD0.430%, 최대 HR16.281%/LR17.616%/CAD1.196%다. 구멍·그늘과 원본 질감도 포함하므로 이 값만으로 결함을 분류하지 않는다. 배경 전체 near-black은 개선 장면에서도 최대 약0.049%로 화면 전체가 검게 무너진 상태는 아니었다. 광원·밝은 배경까지 clipping0이라고 주장하지 않는다.

canonical은 기존 solid 5-brick bundle, class0 `brick_load`, pallet unlabelled, ≥100px를 유지했다. actual 표현 silhouette를 공통 GT로 대신하지 않았다. 이번 테스트의 target mask는 **1642~111031px(화면0.535~36.143%)**, target border-touch0이었다. 가까운 view의 파레트는 화면 아래에서 일부 잘릴 수 있으므로 파레트 전체 촬영 보장으로 해석하지 않는다.

same-background one-load-only denominator를 추가로 렌더한 load 가시성 비율은 **0.764432~1.0**, primary는1.0이었다. 이는 다른 load에 의한 가림 진단이며, **legacy LR far-from-environment visibility 또는 NuRec-free amodal visibility가 아니다.** R3 관찰 때문에 이 값만으로 환경 가림을 PASS로 인증할 수 없다.

노출 전후 동일 pose의 canonical은 **12/12 조건에서 byte 일치**했다. 기존 v03 polygon 함수로 변환한 **36/36 마스크 IoU1.0/XOR0**이고, 실제 Ultralytics8.4.129 CPU 로더에서 표현별24장·36instances, 총72장·108labels가 읽혔다. optimizer/augmentation 학습 검증은 아니다.

![공통 canonical와 bbox 확인](b1_red_brick_sdg_quality_optimization_20261103_v01/canonical_bbox_comparison.png)

근거: `P/analysis_v01/paired_metrics_72.csv`, `canonical_instances_36.csv`, `polygon_fidelity.csv`, `mask_exposure_invariance_12.csv`, `CPU_loader_checks.json`. smoke YAML은 `data.SMOKE_ONLY.yaml`이며 모든 원본 split은 train이다. val alias는 로더 연결용일 뿐 실제 validation 분리가 아니다. 이 smoke 패키지를 학습 데이터로 사용하면 안 된다.

## 6. 파레트 접촉·바닥·물리적 제한

모든 pallet bbox의 world z 최솟값은 약 **2.24×10⁻¹⁰m(수치상0)**다. 이는 새 Stage가 가정한 z=0 기준과 일치한다는 뜻이다. NuRec 바닥의 실제 높이·평탄도와 일치한다는 증거는 아니다. RGB에는 접촉 그림자가 약하고 떠 보이는 구도가 남는다.

이를 더 확인하려고 CAD24개의 동일 빈 배경에서 `distance_to_image_plane`과 실제 camera projection을 저장했다. **24/24 배열의 유효한 양의 finite depth 비율이0**이었다. 이 출력으로 바닥 plane을 추정할 수 없으며 임의의 floor correction을 적용하지 않았다. `NuRec_empty_depth_diagnostic_24.csv`, `paired_CAD_v01/empty_depth/`가 근거다.

따라서 **밝기·형상 식별 개선은 확인, 자연스러운 바닥 접촉 완성은 미확인**이다. collider/인공 바닥/물리 지지/로봇 주행은 추가하거나 검증하지 않았다. 추후 접촉 realism을 강화하려면 원본 제작 좌표·바닥 기준 확인 또는 별도 작업 Stage의 명시적인 support/shadow geometry 설계가 필요하다. 원본 USDZ를 수정하는 조치가 아니다.

## 7. 새 적벽돌 전용 manifest와 촬영 설정

```text
P/red_only_plan_v03/red_only_manifest_1400_v03.csv
P/red_only_plan_v03/red_only_config_v03.json
P/red_only_plan_v03/checks.json
```

기존1400개 red source seed와 split membership을 그대로 보존했다. 새 scene ID는 `B1R_` prefix이며 이전 B1 ID·원본 scene ID·source zone·기존 조명값을 별도로 남겼다. cement와 Proxy는 새 학습 asset registry 및 행에서 제외했다. 기존 cement 자산·결과는 삭제하지 않았고 다른 복수 자재 연구의 활용 가능성을 그대로 보존했다.

| 조명 factor | 기존 intensity | 새 intensity |
|---|---:|---:|
| LG1 | 8000 | 8400 |
| LG2 | 16000 | 8800 |
| LG3 | 32000 | 9600 |
| LG4 | 64000 | 11200 |
| LG5 | 96000 | 12800 |

이는 USD light intensity이며 현장에서 측정한 lux가 아니다. 광도 순서는 유지했지만 범위는 달라졌다. **새 manifest의 dome_intensity는 이미 변환된 값**이다. 다시 `8000+0.05×`를 적용하면 안 되므로 새 config의 runtime scale=1/bias=0으로 기록했다. 품질 pilot jobs는 원래 값을 입력으로 받아 변환식을 한 번 적용했다.

old source zone A_OPEN→R1, B_STRUCTURAL→R5, C_CLUTTER→R4로 매핑했다. 표현별로 ROI를 다르게 고르지 않는다. 과거 세 zone의 세계좌표·분포를 그대로 재현했다는 뜻은 아니다. 과거 visibility/replacement 열은 source 계보이며 새 B1 QA 결과로 쓰지 않는다. lens/640×480/height0.6m/거리/yaw/적층/배치/seed/GT 정의는 유지했다.

## 8. 실행 파일·추적성·다음 단계

최종 paired 렌더 명령 형태(이번에 세 표현 각각 실행 완료):

```bash
/home/user/anaconda3/envs/hh_isaac51/bin/python -u scripts/b1_red_quality_capture_20261103_v05.py \
  --config /home/user/hh/isaac_cosmos/sdg_final/B1_RED_QUALITY_20261103_v01/config.json \
  --jobs /home/user/hh/isaac_cosmos/sdg_final/B1_RED_QUALITY_20261103_v01/paired_quality_jobs.json \
  --output /home/user/hh/isaac_cosmos/sdg_final/B1_RED_QUALITY_20261103_v01/paired_HR_v01 \
  --representation HR_Scan --canonical
```

LR은 같은 v05로 `paired_LR_v01`, CAD는 depth/camera_params 저장을 추가한 v06으로 `paired_CAD_v01`에서 실행했다. geometry·settings·카메라는 동일하다. 이미 존재하는 출력에는 덮어쓰지 않고 실패한다. 각 session의 invocation/code/config/jobs SHA, events, per-case metadata, stdout과 원본 Error/Warning을 보존했다.

최종 코드:

- `scripts/b1_red_quality_capture_20261103_v05.py`: train-only, 최대64개로 제한한 RGB/canonical 품질 pilot.
- `scripts/b1_red_quality_capture_20261103_v06.py`: 같은 pilot에 빈 배경 depth 진단 추가.
- `scripts/prepare_b1_red_manifest_20261103_v03.py`: red-only1400 및 공통 설정 제안 생성.
- `scripts/finalize_b1_red_quality_20261103_v01.py`: paired/노출/annotation CSV와 실제 이미지 패널 생성.

v02~v04와 첫 오류 로그도 보존했다. legacy 모듈 top-level을 실행하지 않고 기존 geometry/annotation/polygon의 정적으로 확인한 함수만 재사용했다. `P/run_manifest.json`과 최종 checks가 원본 보존 및 실행 계보다. 이전 준비117파일과 코드, 등록입력20개의 hash가 같았다. PROJECT_STATE hash는 `d919282dee1a880b3b5ca678563697e7fb45cf0b650b494801b918a95d7f19aa`로 유지했다. 원격 동기화는 UNKNOWN이며 push하지 않았다.

다음은 **이 세 ROI와 공통 설정을 바탕으로 전체1400의 RGB/annotation 시각 QA 정책을 정하고, NuRec 가림과 바닥 접촉의 한계를 처리한 뒤 별도 대량 생성**하는 단계다. 원래 v01 capture는 ISO400/단일ROI를 hardcode하므로 새 config를 그대로 전달하면 안 된다. 이번 quality entrypoint는 train-only·64개 제한이며 production val/test 생성기는 이번 작업에서 실행하지 않았다. 아직 YOLO 학습·새 HPO·기존 평가 재실행은 하지 않는다.

**결론:** 적벽돌3표현의 highlight clipping은 이번 동일 조건 smoke에서 해결됐고, 구멍·적층·원본 질감 차이를 확인할 수 있는 공통 촬영 설정과 추천 ROI3곳을 확보했다. NuRec의 가림 annotation과 접촉 realism은 별도 제한으로 남는다. 기존 Constructionsite 평가 환경·원본 자산·기존 실험/모델·PROJECT_STATE는 유지했다.
