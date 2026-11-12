# C 생성 Replicator/NumPy 예외 — CPU 데이터 정합성 감사

2026-11-12. 기존 C-HPO·Controller·Watchdog·GitHub 자동 동기화 프로세스와 학습 설정은 변경·중단하지 않았다. 신규 GPU 작업/렌더링/추론/물리 주행은 실행하지 않았다. 모든 검사와 그림 없는 텍스트 증거는 저장 파일을 읽는 CPU 감사다.

## 범위와 발생 시점

기존 본생성 210 로그의 `Replicator_instance_id_segmentation` 예외 **26,370회**를 전수 추출했다. 본생성 신규 관측 4,395건에서 각각 정확히 6회이며, 이전 파일럿 재사용 15건까지 포함한 전체 저장 관측은 4,410건이다. 26,370을 손상 이미지 수로 해석하면 안 된다.

UTC 초 단위 로그만으로 장면을 매칭하면 경계가 어긋났다. 별도 복원에서 각 로그의 UTC 초와 프로세스 경과 밀리초를 함께 사용해 시작시각의 가능한 구간을 교집합으로 계산했다. 최대 시각 불확실성 구간 폭 0.036초. 전체 예외가 불확실성까지 고려해 **각 장면의 empty 배경 RGB 파일 쓰기 이전**에 있었다. 예외 추정시각부터 empty 파일 쓰기까지 0.0585~0.9932초.

동결 capture v02의 순서는 장면 제거→reset(6 orchestrator steps 포함)→empty RGB 저장→실제 적재물 생성→reset→실제 RGB/Depth/ID mask 저장→canonical 대체→reset→canonical GT 저장이다. 따라서 확인된 예외는 적재물 생성 전 empty 구간에 위치한다. 적재물·canonical GT 저장 구간의 오류였다고 단정한 이전 초 단위 추정은 정밀 복원 결과로 대체한다. 원래 로그와 첫 추정 파일은 보존한다.

## 원인과 출력 경로

설치된 NVIDIA 원본 `OgnInstanceIdSegmentationLegacy.py`의 `compute()`에서 ID 버퍼를 `wp.array(...).numpy()`로 복사/변환하다가 예외가 발생한다. Warp `types.py`의 `numpy()`는 CPU 복사 후 `np.asarray(a)`를 호출한다. 예외는 legacy node가 `db.outputs.data`와 `idToLabels`를 갱신하기 전 발생한다. RGB annotator 또는 depth annotator 함수의 예외와 구분한다.

빈 장면의 ID 버퍼/shape/stride 상태와 관련됐을 가능성은 **가설**이다. 실패 당시 pointer, shape, strides, dtype, 전체 uint32 ID buffer, render frame/generation ID가 저장되지 않아 정확한 내부 조건은 UNKNOWN이다. 실제 NumPy는 Isaac 환경 1.26.0이며 NumPy 2 호환성 문제로 임의 진단하지 않았다. CPU 검사만으로 누락된 live GPU 버퍼를 재현하지 않았다.

## 기존 QA와 독립된 재검사

| 검사 | 범위 | 결과 및 한계 |
|---|---:|---|
| 실제 파일 SHA 재계산 | 전체 4,410 capture의 기록된 모든 RGB·Depth·camera·empty·actual/canonical mask | 원래 capture SHA와 일치 |
| 이미지·배열 재디코딩 | 4,410 | RGB/empty 640×480×3 uint8, depth 480×640 float32 및 카메라 rigid transform 검사 통과 |
| mask 이진성·픽셀 수·load 간 중복 | actual/canonical 13,986 instance pairs | 저장 metadata와 일치, load 소유 마스크 중복 없음 |
| 독립 형상 투영 | 13,986 canonical instances | 보존된 Bundle5 잔여 슬롯으로 구성한 3D box를 저장 camera로 투영. 2px 경계 여유를 둔 지지 범위 밖 GT 픽셀 0. 이 경계 여유는 감사용이며 기존 QA나 성공 기준을 바꾼 것이 아님 |
| RGB·empty·actual mask 재계산 | 기존 H1 통계 13,986개 | erosion2 픽셀 수와 stored tau 기준 visibility 수치 전체 일치. 원래 pallet ID mask 미보존으로 tau 자체는 재계산 불가 |

H1 원래 분류는 OK 13,600 / LOW_SUPPORT 317 / WATCH 30 / FLAG_NUREC_OCCLUSION 39다. 이들은 원래 H1 분석용 표시이며 모두 그대로 보존한다. 이번 감사에서 표본을 제거하거나 증강·QA threshold를 완화하지 않았다. 알려진 NuRec visibility 제한을 새롭게 해결했다고 주장하지 않는다.

첫 깊이 진단은 정수 pixel 좌표에서 광선을 복원해 585 instance에 5mm enclosure outlier를 기록했다. 이를 숨기지 않고 별도 재검토했다. 해당 585건에서 pixel center +0.5 convention을 사용하자 outlier 0이 되었고, 모든 instance 대상으로 같은 검사를 추가했다. 감사 광선 규약의 정정이며 현재 HPO·기존 위치추정 입력/알고리즘은 변경하지 않았다. 5mm는 감사용 enclosure 거리이고 운용 성공 판정 기준이 아니다.

## 판정의 범위

파일 손상·형상과 모순되는 GT·픽셀 수 불일치·RGB/mask 저장 통계 불일치는 확인되지 않았다. 시간상 예외는 empty 배경 구간에 국한됐다. 이 사실은 저장 데이터 손상으로 이어졌다는 근거를 지지하지 않지만, renderer 예외를 “완전히 무해한 경고”로 확정한 것은 아니다.

원본 frame counter와 buffer generation ID가 없으므로 모든 RGB·Depth·GT가 정확히 동일 렌더 프레임에서 나온 사실을 사후 완전 증명할 수 없다. RGB와 canonical GT는 원래 설계상 actual→canonical 별도 렌더이며 동일 camera/점유 형상 대응이지 동일 raw frame이 아니다. RGB·actual depth·actual mask의 버퍼 신선도 역시 직접 frame-ID 증명은 UNKNOWN이다. 독립 투영·깊이·저장 통계는 공간 정합성 증거이며 이 UNKNOWN을 대체하지 않는다.

확인된 데이터 결함에 근거한 추가 후속 평가 HOLD 조건은 현재 관찰되지 않았다. 기존 C-HPO 및 승인된 정적 평가 계획은 유지하고, 물리 pilot/300/별도150 HOLD는 그대로다. 향후 실제 저장 데이터 모순이 발견되면 후속 평가를 HOLD해야 하며 이번 부분 검증을 무조건 통과 증명으로 사용하면 안 된다.

## 증거와 재현

외부 root: `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02`.

- `replicator_output_audit_v01/`: 전체 SHA/배열/GT projection 검사, capture_checks.jsonl, 최초 초 단위 exception timeline. source `analysis/c_depletion_replicator_output_audit_20261112_v01.py`.
- `replicator_exception_timing_v01/`: monotonic+UTC timing.jsonl, empty_background_phase.json, source_audit.json, HPO_preservation_check.json. source `analysis/c_depletion_exception_timing_20261112_v01.py`.
- `replicator_rgb_mask_audit_v01/`: RGB/H1 재계산, H1_strata.csv. source `analysis/c_depletion_rgb_mask_consistency_20261112_v01.py`.
- `replicator_depth_outlier_review_v01/` 및 `replicator_depth_center_audit_v02/`: 첫 진단과 pixel-center 전수 재검사 모두 보존.

재현 시 이미 존재하는 출력 root에 실행하지 않는다. 새 버전/출력 경로를 사용하고 CPU affinity 1core, `nice -n 15`, `ionice -c 3`, `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`을 적용한다. 마지막 깊이 감사에서 BLAS thread 확장을 관찰해 해당 **감사 프로세스만** CPU47 한 코어로 제한했다. 기존 학습 프로세스·서비스 설정은 바꾸지 않았다.

GitHub에는 이 보고서·감사 코드·작은 요약·SHA만 동기화한다. RGB-D, 마스크 원본, 대용량 timeline/instance evidence 및 NuRec 시각자료는 로컬에 보존한다.


최종 깊이 검사: 전체 **13,986 instance, 1,790,208개 결정적 표본 depth points**의 +0.5 pixel-center 광선을 재투영했을 때 5mm Bundle5 envelope 밖 점 **0**. 전수 픽셀 깊이의 무결성을 증명하는 것이 아니라 모든 instance에 대한 표본 공간 정합성 검사다. 기존 HPO PID106572와 continuation106568, Watchdog3805776, sync109541 모두 유지됐다.
