# G0–G3 본 주행 120셀 결과·버전 분리·메모리 개선 후보 (2026-11-11)

## 실행 상태와 해석 범위

보고서 생성 2026-11-11T11:32:29+09:00, 검증 snapshot `snapshot_20261111T113224`. **본 주행 선언120셀 모두 종료 결과를 확보했다.** 종료 결과는 코드 사본·session/runner 종료·실제 steps 로그·모든 leg 도달/정지 인증·quiet·최종 오차로 재계산했다. verifier는 원본 summarize의 판정식을 그대로 쓰고 큰 trace만 스트리밍으로 읽는다. 저장 outcome과의 불일치 및 malformed/nonmonotonic trace는 0건이다. 단, 저장 인증을 모든 실행에 대해 독립 재연산한 것은 아니며 후보 회귀검사에서는 별도33개 인증을 재연산했다.

본120셀과 파일럿12개, O50 12개, 중복된 수정 재실행을 구분한다. 이 snapshot의 O50 운영 결과는 0/12이며 **본120 분모에 더하지 않는다**. 기존 shell은 main 뒤 o50를 자동 진행한다. 본120 완료가 GPU 비점유를 뜻하지 않으며 새 Kit/ROS/주행·재촬영은 실행하지 않았다. 기존 프로세스와 알림은 중지·재시작·수정하지 않았다.

기존 실행기는 run01의 G0/G1을 재사용하고 G2/G3를 run02에서 재실행했다. 따라서 원본 첫 시도120셀과 운영 선택120셀은 **버전이 섞인 이력표**이며, 단일 버전 실험으로 합쳐 효과를 검정하지 않는다. 아래 실제 버전별 원본 결과와 같은 버전의 짝이 맞는 비교를 따로 제시한다. 원본 G3 메모리 실패6건은 그대로 유지된다. 시간상 순서·실행 환경 차이와 재실행 선택이 있으므로 보정 효과에 대한 확증 실험이 아니다.

## 정확한 실험군과 고정 조건

| 군 | 초기/재인식 위치 추정 | 접근 순서 |
| --- | --- | --- |
| G0 | ORIG_v44 | PRE→FINAL |
| G1 | ROBUST_A | PRE→FINAL |
| G2 | ORIG_v44 | W→재인식→PRE′→FINAL′ |
| G3 | ROBUST_A | W→재인식→PRE′→FINAL′ |

ORIG_v44는 동결 센서 자동 ROI B5다. A는 b5_robust v01(frozen config SHA35cf0a78…c529, code SHA0b1e5f46…ae29)로 센서 floor/load-top datum·depth region growth·팔레트 수직면·edge-on midpoint·축 모호성 중심 평균을 사용한다. 적재 단수는 task metadata이며 GT 중심/pose는 입력하지 않는다. B는 PRE_init보다0.80m 뒤 W에서 기존v21 인증 정지 후 같은 RenderProduct로 재촬영하고, 초기 mask centroid와0.30m 이내 재식별·초기 pose와0.25m 이내 gate를 적용해 재추정값으로 대체한다. 가림판은 모든 군에서 초기 촬영 후 제거돼 B의 재관측은 가림 없는 조건이다.

자기 표현 M50 모델을 사용한다. 앞서 집계한 B1 recipe v03/v04 모델과 별도 계보다. 공통 HR 현장 stage에서 HR/LR/GeoCAD 벽돌 외형을 바꾼 red 실험이며 cement나 실제 로봇 배치로 일반화하지 않는다. LR은 별도 축소 취득 재구성으로 HR decimation이 아니다. Proxy/과거432설계는 이번120셀에 포함되지 않으며 그 프로토콜을 바꾸지 않았다.

설계10조건(4시작×L4×O0, 4시작×L4×O25, S1/S2×L1×O0)×3표현×4군×1회다. 독립 물리 현장10개나 seed120개가 아니다. 각 군30셀, 표현×군10셀 분모를 유지한다. 성공은 predicted 입력·실제0.10m 이상 이동·모든 leg5mm/2도와v21인증·QUIET PASS·무충돌·설계 FINAL11cm/7.34177도 이내다. 속도 guard.03m/s, 조향·곡률·tracking·정지 판정은 유지했다.

matrix SHA `6bc3fb4edeb6812a00ae32776bc093616fe1038fd95a3166841beb99a610a0c7`. 실행별 Scene/군/표현/model path·SHA/B5 코드/start/success 기준은 `snapshot_20261111T113224/execution_provenance.csv`에 있다. 촬영 전에 실패한 경우 configured model과 실제 inference manifest 존재를 구분했다.

## 실제 버전별 결과 — 병합하지 않음

| 버전 | 표현 | 군 | 실제 실행수 | 성공 | 원본 outcomes |
| --- | --- | --- | --- | --- | --- |
| run01 | ALL | G0 | 10 | 0 | {'FAIL_B': 10} |
| run01 | ALL | G1 | 9 | 8 | {'SUCCESS': 8, 'FAIL_E': 1} |
| run01 | ALL | G2 | 9 | 0 | {'FAIL_B': 9} |
| run01 | ALL | G3 | 10 | 4 | {'FAIL_E': 6, 'SUCCESS': 4} |
| run01 | HR_Scan | G0 | 4 | 0 | {'FAIL_B': 4} |
| run01 | HR_Scan | G1 | 3 | 3 | {'SUCCESS': 3} |
| run01 | HR_Scan | G2 | 3 | 0 | {'FAIL_B': 3} |
| run01 | HR_Scan | G3 | 4 | 2 | {'FAIL_E': 2, 'SUCCESS': 2} |
| run01 | LR_Scan | G0 | 3 | 0 | {'FAIL_B': 3} |
| run01 | LR_Scan | G1 | 3 | 3 | {'SUCCESS': 3} |
| run01 | LR_Scan | G2 | 3 | 0 | {'FAIL_B': 3} |
| run01 | LR_Scan | G3 | 3 | 1 | {'FAIL_E': 2, 'SUCCESS': 1} |
| run01 | GeoCAD | G0 | 3 | 0 | {'FAIL_B': 3} |
| run01 | GeoCAD | G1 | 3 | 2 | {'SUCCESS': 2, 'FAIL_E': 1} |
| run01 | GeoCAD | G2 | 3 | 0 | {'FAIL_B': 3} |
| run01 | GeoCAD | G3 | 3 | 1 | {'FAIL_E': 2, 'SUCCESS': 1} |
| run02 | ALL | G0 | 20 | 0 | {'FAIL_B': 18, 'FAIL_A': 2} |
| run02 | ALL | G1 | 21 | 17 | {'SUCCESS': 17, 'FAIL_A': 3, 'FAIL_D': 1} |
| run02 | ALL | G2 | 30 | 0 | {'FAIL_A': 2, 'FAIL_B': 28} |
| run02 | ALL | G3 | 30 | 24 | {'FAIL_D': 4, 'SUCCESS': 24, 'FAIL_A': 2} |
| run02 | HR_Scan | G0 | 6 | 0 | {'FAIL_B': 5, 'FAIL_A': 1} |
| run02 | HR_Scan | G1 | 7 | 4 | {'FAIL_A': 2, 'SUCCESS': 4, 'FAIL_D': 1} |
| run02 | HR_Scan | G2 | 10 | 0 | {'FAIL_A': 1, 'FAIL_B': 9} |
| run02 | HR_Scan | G3 | 10 | 8 | {'FAIL_D': 1, 'SUCCESS': 8, 'FAIL_A': 1} |
| run02 | LR_Scan | G0 | 7 | 0 | {'FAIL_B': 7} |
| run02 | LR_Scan | G1 | 7 | 7 | {'SUCCESS': 7} |
| run02 | LR_Scan | G2 | 10 | 0 | {'FAIL_B': 10} |
| run02 | LR_Scan | G3 | 10 | 9 | {'SUCCESS': 9, 'FAIL_D': 1} |
| run02 | GeoCAD | G0 | 7 | 0 | {'FAIL_B': 6, 'FAIL_A': 1} |
| run02 | GeoCAD | G1 | 7 | 6 | {'SUCCESS': 6, 'FAIL_A': 1} |
| run02 | GeoCAD | G2 | 10 | 0 | {'FAIL_B': 9, 'FAIL_A': 1} |
| run02 | GeoCAD | G3 | 10 | 7 | {'FAIL_D': 2, 'SUCCESS': 7, 'FAIL_A': 1} |

run01은 runner v03/session v02(atomic handoff), run02는 runner v04/session v03(W GC 구간 재설정)다. G0/G1은 B 경로를 사용하지 않지만 코드 버전·실행시각을 감추지 않았다. run02에 없는 G0/G1을 성공·실패0으로 채워넣지 않는다. 버전별 actual count와120 계획 ledger의 count는 용도가 다르다.

## 선언120셀의 보존 이력표(효과 검정용 단일 버전 코호트 아님)
### 최초 시도 — 원본 실패 유지

| 군 | 기록/계획 | 성공 | 실패 |
| --- | --- | --- | --- |
| G0 | 30/30 | 0 | {'FAIL_B': 28, 'FAIL_A': 2} |
| G1 | 30/30 | 25 | {'FAIL_E': 1, 'FAIL_A': 3, 'FAIL_D': 1} |
| G2 | 30/30 | 0 | {'FAIL_B': 28, 'FAIL_A': 2} |
| G3 | 30/30 | 18 | {'FAIL_E': 6, 'FAIL_D': 4, 'FAIL_A': 2} |

### 기존 실행기가 선택한 운영 결과 — 재실행 사용 표시

| 군 | 기록/계획 | 성공 | 실패 |
| --- | --- | --- | --- |
| G0 | 30/30 | 0 | {'FAIL_B': 28, 'FAIL_A': 2} |
| G1 | 30/30 | 25 | {'FAIL_E': 1, 'FAIL_A': 3, 'FAIL_D': 1} |
| G2 | 30/30 | 0 | {'FAIL_B': 28, 'FAIL_A': 2} |
| G3 | 30/30 | 24 | {'FAIL_D': 4, 'FAIL_A': 2} |

두 표를 별도120회 독립 표본으로 더하지 않는다. 같은 cell의 원본과 수정 시도는 대응 이력이다. CSV에는 모든 실제 실행을 빠짐없이 남겼다.

## 단계별 통과·오차·비용(운영 이력 참고)

분모는 군당 전체30이다. 오차/시간 중앙값 뒤 괄호는 수치가 기록된 조건부 표본 수다. 실패를0오차로 넣지 않았다. 최종 오차는 모든 leg 끝점이 기록된 경우에만 존재한다. 전체 성공률과 조건부 오차는 다른 지표다.

| 표현 | 군 | N | 검출 | pose | 초기계획 | 실제이동 | 작업성공 | 초기XY mm(n) | FINAL mm(n) | heading °(n) | drive sim s(n) | wall s(n) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ALL | G0 | 30 | 28 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 50.083 (30) |
| ALL | G1 | 30 | 26 | 26 | 26 | 26 | 25 | 5.244 (26) | 5.079 (25) | 0.047 (25) | 149.325 (26) | 479.189 (30) |
| ALL | G2 | 30 | 28 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 50.085 (30) |
| ALL | G3 | 30 | 28 | 28 | 28 | 28 | 24 | 5.244 (28) | 3.892 (24) | 0.041 (24) | 163.708 (28) | 539.290 (30) |
| HR_Scan | G0 | 10 | 9 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 50.585 (10) |
| HR_Scan | G1 | 10 | 8 | 8 | 8 | 8 | 7 | 5.430 (8) | 5.096 (7) | 0.046 (7) | 147.092 (8) | 468.920 (10) |
| HR_Scan | G2 | 10 | 9 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 50.330 (10) |
| HR_Scan | G3 | 10 | 9 | 9 | 9 | 9 | 8 | 5.617 (9) | 4.266 (8) | 0.051 (8) | 162.967 (9) | 534.541 (10) |
| LR_Scan | G0 | 10 | 10 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 50.830 (10) |
| LR_Scan | G1 | 10 | 10 | 10 | 10 | 10 | 10 | 5.645 (10) | 5.724 (10) | 0.044 (10) | 149.367 (10) | 480.931 (10) |
| LR_Scan | G2 | 10 | 10 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 50.830 (10) |
| LR_Scan | G3 | 10 | 10 | 10 | 10 | 10 | 9 | 5.640 (10) | 4.084 (9) | 0.035 (9) | 164.683 (10) | 539.781 (10) |
| GeoCAD | G0 | 10 | 9 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 49.579 (10) |
| GeoCAD | G1 | 10 | 8 | 8 | 8 | 8 | 8 | 4.674 (8) | 4.585 (8) | 0.058 (8) | 149.275 (8) | 484.187 (10) |
| GeoCAD | G2 | 10 | 9 | 0 | 0 | 0 | 0 | NA (0) | NA (0) | NA (0) | NA (0) | 49.831 (10) |
| GeoCAD | G3 | 10 | 9 | 9 | 9 | 9 | 7 | 4.666 (9) | 3.389 (7) | 0.040 (7) | 163.783 (9) | 532.782 (10) |

## 같은 run02 버전에서 짝이 맞는 효과 비교

원본120셀이 모두 확보된 뒤에만 계산했다. 같은 scene/표현에서 필요한 군이 모두 있는 pair만 사용한 **명시적 보조 분석**이다. 나머지 셀과 실패를 원본 이력에서 삭제하지 않았다. 결측 버전 구조 때문에 이 표가 원래 계획한10조건×3표현 전체 비교를 대체하지 않는다. bootstrap10000/seed20261110은 조건 단위로 resample하며 한 조건의 표현들을 함께 유지한다. pooled p는 조건 평균의 부호 검정이고30표현-조건을 독립으로 본 McNemar가 아니다. p는 다중비교 보정 전 탐색값이며 상호작용은 별도 sign test다. 비유의를 동등성·비열등성으로 해석하지 않는다.

| 표현 | 대비 | 조건수 | paired표현셀 | 성공률차 | bootstrap95% | +/−/동률 조건 | 탐색 p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HR_Scan | G1-G0 | 6 | 6 | 0.500 | [0.1667, 0.8333] | [3, 0, 3] | 0.25000 |
| HR_Scan | G2-G0 | 6 | 6 | 0.000 | [0.0, 0.0] | [0, 0, 6] | 1.00000 |
| HR_Scan | G3-G1 | 7 | 7 | 0.143 | [0.0, 0.4286] | [1, 0, 6] | 1.00000 |
| HR_Scan | G3-G0 | 6 | 6 | 0.667 | [0.3333, 1.0] | [4, 0, 2] | 0.12500 |
| HR_Scan | interaction | 6 | 6 | 0.167 | [0.0, 0.5] | [1, 0, 5] | 1.00000 |
| LR_Scan | G1-G0 | 7 | 7 | 1.000 | [1.0, 1.0] | [7, 0, 0] | 0.01562 |
| LR_Scan | G2-G0 | 7 | 7 | 0.000 | [0.0, 0.0] | [0, 0, 7] | 1.00000 |
| LR_Scan | G3-G1 | 7 | 7 | -0.143 | [-0.4286, 0.0] | [0, 1, 6] | 1.00000 |
| LR_Scan | G3-G0 | 7 | 7 | 0.857 | [0.5714, 1.0] | [6, 0, 1] | 0.03125 |
| LR_Scan | interaction | 7 | 7 | -0.143 | [-0.4286, 0.0] | [0, 1, 6] | 1.00000 |
| GeoCAD | G1-G0 | 7 | 7 | 0.857 | [0.5714, 1.0] | [6, 0, 1] | 0.03125 |
| GeoCAD | G2-G0 | 7 | 7 | 0.000 | [0.0, 0.0] | [0, 0, 7] | 1.00000 |
| GeoCAD | G3-G1 | 7 | 7 | -0.286 | [-0.575, 0.0] | [0, 2, 5] | 0.50000 |
| GeoCAD | G3-G0 | 7 | 7 | 0.571 | [0.1429, 0.8571] | [4, 0, 3] | 0.12500 |
| GeoCAD | interaction | 7 | 7 | -0.286 | [-0.575, 0.0] | [0, 2, 5] | 0.50000 |
| ALL | G1-G0 | 7 | 20 | 0.800 | [0.6, 0.9524] | [7, 0, 0] | 0.01562 |
| ALL | G2-G0 | 7 | 20 | 0.000 | [0.0, 0.0] | [0, 0, 7] | 1.00000 |
| ALL | G3-G1 | 7 | 21 | -0.095 | [-0.3333, 0.0952] | [1, 2, 4] | 1.00000 |
| ALL | G3-G0 | 7 | 20 | 0.700 | [0.4, 0.9524] | [6, 0, 1] | 0.03125 |
| ALL | interaction | 7 | 20 | -0.100 | [-0.3333, 0.1053] | [1, 2, 4] | 1.00000 |

G0→G1은 초기 B5 계산 병목이 줄어드는 방향이며, G0→G2는 초기 pose를 통과하지 못해 중간 재인식에 도달할 수 없었다. G1→G3는 conditional pose 오차 변화와 추가 중간 정지 실패·비용을 함께 봐야 한다. 성공한 재인식 표본만으로 전체 작업 성공률 향상을 주장하지 않는다.

## 재인식 조건부 변화와 추가 비용

| 표현 | n | 초기XY mm | 재관측XY mm | paired변화 mm | 감소 | 증가 | 재관측 wall s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ALL | 24 | 4.691 | 3.498 | -1.314 | 21 | 3 | 17.027 |
| HR_Scan | 8 | 5.430 | 3.798 | -1.635 | 7 | 1 | 17.007 |
| LR_Scan | 9 | 5.245 | 3.638 | -1.768 | 7 | 2 | 17.060 |
| GeoCAD | 7 | 4.309 | 3.167 | -1.181 | 7 | 0 | 17.039 |

같은 run02 버전·같은 조건에서 G1/G3가 모두 성공한 쌍의 추가 비용과 최종 오차 변화(성공 조건부):

| 표현 | 성공paired n | wall추가 s 중앙 | drive추가 sim s 중앙 | FINAL오차변화 mm 중앙 | heading변화 ° 중앙 |
| --- | --- | --- | --- | --- | --- |
| ALL | 14 | 60.119 | 15.417 | -1.807 | 0.000 |
| HR_Scan | 4 | 60.618 | 15.550 | -1.700 | 0.004 |
| LR_Scan | 6 | 65.626 | 15.375 | -11.621 | -0.014 |
| GeoCAD | 4 | 55.621 | 14.967 | -0.541 | 0.033 |

차이는 G3−G1이다. wall 시간은 호스트 부하와 프로세스 기동도 포함하며 simulation 시간과 구분한다. 둘 다 성공한 쌍만의 비용이므로 전체 평균 작업 비용으로 일반화하지 않는다.
G3 B 결정: {'B_CORRECTED': 24, 'NOT_REACHED': 6}. G2는 초기 추정 거부/미검출로 재관측에 도달하지 못했다. 센서 촬영·재식별·pose·계획 거부는 원본 decision/reason을 CSV에서 구분했다.
## 저장 RGB-D 전체 조건의 B5 대조

G1의30개 계획 cell에서 같은 저장 sensor input에 ORIG와A를 각각 CPU로 재실행했다. 원래 촬영 실패는 재현 불가로 남겼다. GT/새추론/새촬영은 사용하지 않았다. 입력 SHA는 전후 불변이며 기존 status/reason과 중심 좌표가 exact 일치했다.

| 구분 | 건수 |
| --- | --- |
| CPU 재실행 | 29 |
| 원본 촬영 실패 | 1 |
| 아직 terminal 없음 | 0 |
| ORIG datum 거부 | 26 |
| 양쪽 미검출 | 3 |
| ROBUST_A 계산 | 26 |

마스크가 있는 재현 입력에서는 팔레트 높이 후보가 관측됐지만, 5×5 침식 후 지지점이 100개 미만으로 줄어 모두 거부됐다. 팔레트 윗면이 전혀 보이지 않는다고 단정하지 않고, 새 시점의 얇은 띠와 기존 ROI 조건이 겹친 결과로 해석한다. calibration checks 통과와 오프라인 재현은 정합성·시작점 전달 오류가 필수 원인이 아님을 뒷받침하지만 독립 실측 정확도 인증은 아니다. 기존 G0/G2 실패는 수정하지 않았다. 자세한 사례·입력 SHA·후보 지지점은 reports/stage4_pose_failure_detail_20261111_v01/snapshot_20261111T113026/cases.json에있다.
## 실패 원인·시작점·가림 조건

| 버전 | 군 | outcome | 원문 reason | 세부원인 | 건수 |
| --- | --- | --- | --- | --- | --- |
| run01 | G0 | FAIL_B | POSE_NO_CONNECTED_PALLET_SURFACE_PASSED_UNCHANGED_PLANE_GATES: | None | 10 |
| run01 | G2 | FAIL_B | POSE_NO_CONNECTED_PALLET_SURFACE_PASSED_UNCHANGED_PLANE_GATES: | None | 9 |
| run01 | G3 | FAIL_E | GC_MEMORY_BOUND | None | 6 |
| run01 | G1 | FAIL_E | CAPTURE_BUFFERS_INVALID | None | 1 |
| run02 | G3 | FAIL_D | GOAL_OVERSHOOT | None | 4 |
| run02 | G1 | FAIL_A | PERCEPTION_NO_DETECTION: | None | 3 |
| run02 | G2 | FAIL_A | PERCEPTION_NO_DETECTION: | None | 2 |
| run02 | G2 | FAIL_B | POSE_NO_CONNECTED_PALLET_SURFACE_PASSED_UNCHANGED_PLANE_GATES: | None | 28 |
| run02 | G0 | FAIL_B | POSE_NO_CONNECTED_PALLET_SURFACE_PASSED_UNCHANGED_PLANE_GATES: | None | 18 |
| run02 | G1 | FAIL_D | LEGS_INCOMPLETE | SPEED_GUARD_0.03 | 1 |
| run02 | G3 | FAIL_A | PERCEPTION_NO_DETECTION: | None | 2 |
| run02 | G0 | FAIL_A | PERCEPTION_NO_DETECTION: | None | 2 |


| 조건(운영 이력) | G0 | G1 | G2 | G3 |
| --- | --- | --- | --- | --- |
| S1_L4_O0 | 0/3 | 2/3 | 0/3 | 3/3 |
| S2_L4_O0 | 0/3 | 3/3 | 0/3 | 3/3 |
| S3_L4_O0 | 0/3 | 3/3 | 0/3 | 3/3 |
| S4_L4_O0 | 0/3 | 3/3 | 0/3 | 3/3 |
| S1_L4_O25 | 0/3 | 3/3 | 0/3 | 2/3 |
| S2_L4_O25 | 0/3 | 1/3 | 0/3 | 1/3 |
| S3_L4_O25 | 0/3 | 2/3 | 0/3 | 3/3 |
| S4_L4_O25 | 0/3 | 2/3 | 0/3 | 0/3 |
| S1_L1_O0 | 0/3 | 3/3 | 0/3 | 3/3 |
| S2_L1_O0 | 0/3 | 3/3 | 0/3 | 3/3 |

G1의 LEGS_INCOMPLETE 1건은 저장 trace에서 순간속도 .03056994m/s로 기존 .03 guard 작동이 확인돼 SPEED_GUARD_0.03을 별도 기록한다. 단순 통신 오류라고 재분류하지 않는다. G3의 아래4건은 W 접근 중 GOAL_OVERSHOOT이며 재인식 호출 전 실패다. 감독 종료 후 driver_guard_fault의 SUPERVISOR_ABORT를 최초 원인으로 바꿔 쓰지 않았다.

4건 모두 W 최근접 거리3.06–3.70mm가 기존 normal-stop 요청 반경3mm 밖이었다. normal_stop 요청0회 상태로 최소속도.004m/s 전진을 계속하다 along<−5mm에서 중단됐다. 25mm tracking envelope와3mm 종단 요청 조건의 차이가 드러난 사례다. 단순 속도 초과나 재식별 실패가 아니다. 제어 기준·성공 문턱을 바꾸지 않았고 해당 실패를 유지했다.

| 실행 | 최근접 mm | 횡잔차 mm | 최종 along mm | 정상감속 요청수 |
| --- | --- | --- | --- | --- |
| main_S1_L4_O25_GeoCAD_G3_t1 | 3.265 | 3.265 | -5.063 | 0 |
| main_S4_L4_O25_HR_Scan_G3_t1 | 3.059 | 3.059 | -5.029 | 0 |
| main_S4_L4_O25_GeoCAD_G3_t1 | 3.700 | 3.700 | -5.026 | 0 |
| main_S4_L4_O25_LR_Scan_G3_t1 | 3.148 | 3.146 | -5.009 | 0 |

## 원본 G3 메모리6건과 이미 실행된 GC 수정 묶음

원본 실패는8GiB CPU RSS 절대 한도 초과가 아니라 구간기준+768MiB 증가 guard 초과였다. RSS는Kit 자신의 resident memory로 CUDA VRAM이나 인식 subprocess와 합산하지 않는다. W 재설정 수정은8GiB/768MiB/600초 값은 유지하지만 기준점을 다시 잡으므로 전체 주행 증가량 의미가 달라진다. gc.collect 전후 RSS가 같았던 기록도 있어 누수가 제거됐다는 증거는 아니다.

| 원본 cell | 원본 outcome | 원본peak GiB | 원본증가 MiB | run02별도 outcome | 새결과검증 | 새FINAL mm |
| --- | --- | --- | --- | --- | --- | --- |
| main_S2_L4_O0_GeoCAD_G3_t1 | FAIL_E | 6.852 | 769.500 | SUCCESS | True | 3.389 |
| main_S2_L4_O0_HR_Scan_G3_t1 | FAIL_E | 6.961 | 768.688 | SUCCESS | True | 4.592 |
| main_S2_L4_O0_LR_Scan_G3_t1 | FAIL_E | 6.995 | 769.219 | SUCCESS | True | 4.222 |
| main_S3_L4_O0_GeoCAD_G3_t1 | FAIL_E | 6.827 | 768.449 | SUCCESS | True | 2.936 |
| main_S3_L4_O0_HR_Scan_G3_t1 | FAIL_E | 6.984 | 768.605 | SUCCESS | True | 3.940 |
| main_S3_L4_O0_LR_Scan_G3_t1 | FAIL_E | 6.882 | 768.508 | SUCCESS | True | 4.111 |

## 새 메모리 개선 후보 — 아직 실제 실행 안 함

`evaluation/stage4_record_projection_20261111_v01.py`와 새 session `stage4_ablation_drive_session_20261111_v04.py`, runner `stage4_ablation_drive_20261111_v05.py`를 별도 생성했다. 기존 feedback·steps.jsonl에는 전체 row를 먼저 기록한 뒤, 메모리 history에는 인증/quiet/outcomes/기존 session이 읽는14개 필드만 보관한다. 기록 수나 시간을 잘라 버리지 않고 원본 데이터도 손실시키지 않는다. 전역 GC/메모리 한도·controller·perception·physics는 바꾸지 않았다. 실행 중 코드와 설정은 불변이다.

검증: 13개 기존 실행, 정지 인증33개가 full-history와 compact-history에서 전체 반환값까지 일치했고 저장 인증과도 일치했다. 전체 quiet/outcomes 동일, 잘못된 측정 binding을 넣은33개 거부 검사도 동일했다. AST 비교상 session 변경은 helper import와 기록 보관 호출뿐이다. 이는 **OFFLINE PASS**이며 새 런타임 적합성 승인이 아니다.

실제 기록5000개를 읽는 별도 CPU 프로세스 비교에서 tracemalloc 보유량은 73.23→30.20MiB(58.76% 감소), 종료RSS는 206.96→97.81MiB였다. **Kit/CUDA 전체 메모리 감소율이 아니다.** JSON 재역직렬화 객체는 live 객체의 문자열/키 공유와도 다를 수 있어 실제 절감량의 예측치로 쓰지 않는다. JSONLTail.rows·TIMING.rows·native 할당은 여전히 남는다. native/RenderProduct/CUDA 누수는 미입증이다. 기존 재촬영은 같은 product를 사용하고 모델은 별도 process에서 로드하므로 중복 적재를 원인으로 단정하지 않았다.

후속 실행은 기존 main 및o50 프로세스·ROS191·GPU 비점유 확인 후 별도 smoke1회부터 해야 한다. 이후 원본6cell 대응 재실행을 새 namespace로 구분하고 기존 실패와 섞지 않는다. 이번에는 이 후보의 새 주행/메모리 runtime 검증을 실행하지 않았다.

## 논문용 시각자료

새 Kit 없이 실제 저장JPG를 MP4로 패키징했다. 출력은 **공개 GitHub 업로드 금지, 로컬 전용** `/home/user/hh/isaac_cosmos/sdg_final/STAGE4_PAPER_MEDIA_20261111_v02`다. 원본배경 사람 형상이 포함될 수 있다. MP4는실제기록, 경로그림은로그재구성으로 명시했다.

| 실행 | 자료 | frame수 | 디코드 확인 | 결과 |
| --- | --- | --- | --- | --- |
| main_S1_L4_O0_HR_Scan_G1_t1 | /home/user/hh/isaac_cosmos/sdg_final/STAGE4_PAPER_MEDIA_20261111_v02/main_S1_L4_O0_HR_Scan_G1_t1_ACTUAL_ROBOTCAM_5FPS.mp4 | 721 | 721 | SUCCESS |
| main_S1_L4_O0_HR_Scan_G3_t1 | /home/user/hh/isaac_cosmos/sdg_final/STAGE4_PAPER_MEDIA_20261111_v02/main_S1_L4_O0_HR_Scan_G3_t1_ACTUAL_ROBOTCAM_5FPS.mp4 | 784 | 784 | SUCCESS |
| main_S1_L4_O0_LR_Scan_G1_t1 | /home/user/hh/isaac_cosmos/sdg_final/STAGE4_PAPER_MEDIA_20261111_v02/main_S1_L4_O0_LR_Scan_G1_t1_ACTUAL_ROBOTCAM_5FPS.mp4 | 719 | 719 | SUCCESS |
| main_S1_L4_O0_LR_Scan_G3_t1 | /home/user/hh/isaac_cosmos/sdg_final/STAGE4_PAPER_MEDIA_20261111_v02/main_S1_L4_O0_LR_Scan_G3_t1_ACTUAL_ROBOTCAM_5FPS.mp4 | 785 | 785 | SUCCESS |
| main_S1_L4_O0_GeoCAD_G1_t1 | NO_RECORDED_FRAMES | NA | NA | FAIL_E |
| main_S1_L4_O0_GeoCAD_G3_t1 | /home/user/hh/isaac_cosmos/sdg_final/STAGE4_PAPER_MEDIA_20261111_v02/main_S1_L4_O0_GeoCAD_G3_t1_ACTUAL_ROBOTCAM_5FPS.mp4 | 789 | 789 | SUCCESS |

MP4 5개는 기록된 JPG를 5 FPS로 연결한 자료이며 새 실험이 아니다. 원본 파일명의 정확한 sim time을 영상에 표시했다. leg 전환에 0.217초 간격이 있어 정확한 wall-time 녹화라고 부르지 않는다. 첫 export는 모든 간격을 0.2초로 가정해 실패했다. v01/FAILED.json과 로그를 보존한 뒤 v02에서 명목 5 FPS로 표기했다. 모든 MP4를 다시 디코드해 원본 프레임 수와 일치함을 확인했다.

26개 패널(누락 안내 1개 포함)과 contact sheet 1개에 실제 RGB·mask·주행 중·마지막 저장 프레임을 모았다. CAD G1 촬영 실패를 가상의 이미지로 채우지 않았다. HR G1/G3와 CAD G3 실패의 경로·속도 PNG 3개는 **로그 재구성이며 실제 top-down 카메라가 아님**을 그림에 표시했다. 외부 시점의 로봇 몸체 캡처와 독립 top-down 렌더는 없다. Stage3 main에는 초기 RGB/overlay가 각각 72개 있지만 주행 MP4 증거는 찾지 못했다.

## 미완료·다음 행동

본 120셀 종료 검증, 버전별 비교, 기존 메모리 실패 6건의 대응 비교, 저장 영상 패키징을 완료했다. O50는 이 snapshot에서 미완료일 수 있으며 본 120과 별도 후속 기록이 필요하다. 새 후보의 실제 Kit 메모리 검증, 후보 버전의 6셀 재실행, 외부 카메라 영상은 NOT_RUN이다. 기존 프로세스를 중복 실행하지 않고 자원 확보 후의 별도 단계로 남겼다. 비유의를 동등성으로 해석하지 않고 같은 현장·반복·표현을 독립 표본으로 부풀리지 않는다.

Git 초기화·push·remotes 변경은 하지 않았다. 이 텍스트 보고서만 handoff 동기화 대상이며 raw 영상·이미지·process dump는 제외한다. 원격 반영 완료는 UNKNOWN이다.

증거: snapshot의all_executions/group_metrics/failure_and_B_decisions/reobservation_error_changes/scene_groups/effects_success/execution_provenance CSV, verified_executions의입력SHA·코드SHA·판정재계산. raw실험파일은읽기전용으로보존했다. 새코드는analysis/와evaluation/,scripts/의별도버전파일에있으며실행중v03/v04파일을수정하지않았다.


## 최종 검사·실패 기록과 안전한 다음 명령

2026-11-11T11:34:27+09:00: 기록된 입력 파일 fingerprint 10130개가 검증 이후 불변이었다. 실행 중 사용한 batch v04 / runner v04 / session v03 / perception v01의 SHA는 첫 인수인계 snapshot과 동일하다. 새 코드 12개 AST parse PASS. 본120셀·실제 main139시도·pilot12시도(합계151개 검증 기록)를 구분하며, 불일치0이다.

O50와 main은 별도다. 새 후보 preflight의 exit2/HOLD는 오류 은폐가 아니라 기존 batch·Kit·GPU 점유와 미완료 큐 때문에 추가 실행하지 말라는 의도된 결과였다. 이후에도 다음 읽기 전용 점검을 먼저 사용한다. 이 점검은 주행을 시작하지 않는다.

```text
python3 scripts/stage4_projection_preflight_20261111_v01.py
```

구체적인 별도 smoke 명령은 `reports/stage4_projection_preflight_20261111_v01.json`의 candidate_command_NOT_EXECUTED에 기록했다. 아직 실행하지 않았다. main/O50의 결과와 process/ROS191/GPU 비점유를 다시 확인해야 하며, preflight 통과만으로 실제 Kit 메모리 검증이 된 것은 아니다.

Bootstrap에서 [0,0] 또는 [1,1]이 나온 셀은 관측한 짝의 값이 모두 같아 생긴 퇴화 구간이다. 모집단 불확실성이 없거나 두 방법이 동등하다는 뜻이 아니다. 편의 선택된 조건의 재표집과 동일 현장이라는 범위를 유지한다.

추가 실패 그림은 비공개 media 폴더의 `failure_diagnostics/`에 있다. G1 속도 guard의 원본60Hz 로그, CAD G3의 W 감속 요청 원을 비켜간 궤적, CAD 실패 직전 마지막 실제 저장 프레임을 분리했다. 이 그림도 새로운 Isaac 렌더가 아니다.

이번 작업의 첫 MP4 export는 촬영 간격 가정으로 FAILED(exit1)였고 새 v02에서 수정했다. 보고서 생성 첫 호출도 itertools import 누락으로 FAILED(exit1)여서 이전 snapshot의 REPORT_FAILED_attempt.txt와 부분 provenance CSV를 보존한 뒤 새 snapshot에서 성공했다. 보고서 수정 중 apply_patch의 context 불일치 1건도 파일 변경 없이 실패했다. ffmpeg 및 imageio_ffmpeg 경로를 찾지 못한 탐색(exit2)은 보존하며 패키지 설치 없이 기존 OpenCV encoder로 작성·재디코드 검증했다. 이 감사 명령 실패를 연구 주행 분모와 섞지 않는다.
