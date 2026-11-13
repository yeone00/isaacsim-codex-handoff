# E1 540회 본실험 중간 보고 (30회) — 자동 생성

- 순항 속도 0.02 m/s, 완료 30 / 남음 510
- 경과 1.23 h, 최근 30회 평균 145.5 초/회, 남은 예상 20.61 h (완료 예상 2026-11-15 01:45)
- 저장: 압축 30개 중 검증 30개, 원본 7.15 GB → 압축 0.86 GB, 볼륨 여유 7.53 TB

| 표현 | 시도 | 성공 | 성공률 | 결과 유형 |
|---|---|---|---|---|
| HR_Scan | 10 | 4 | 0.4 | {'perception_no_detection': 6, 'success': 4} |
| LR_Scan | 10 | 4 | 0.4 | {'perception_no_detection': 6, 'success': 4} |
| GeoCAD | 10 | 4 | 0.4 | {'success': 4, 'perception_no_detection': 6} |

| 적재율 | 시도 | 성공 | 성공률 | 결과 유형 |
|---|---|---|---|---|
| C100 | 6 | 2 | 0.333 | {'perception_no_detection': 4, 'success': 2} |
| C80 | 6 | 2 | 0.333 | {'perception_no_detection': 4, 'success': 2} |
| C60 | 6 | 1 | 0.167 | {'perception_no_detection': 5, 'success': 1} |
| C40 | 6 | 4 | 0.667 | {'success': 4, 'perception_no_detection': 2} |
| C20 | 6 | 3 | 0.5 | {'success': 3, 'perception_no_detection': 3} |

- 결과 유형 전체: {'perception_no_detection': 18, 'success': 12}
- 주행 12회: 거리 {'n': 12, 'mean': 1.7962, 'median': 1.7961, 'max': 1.7972}, 최종 위치 오차(m) {'n': 12, 'mean': 0.0041, 'median': 0.004, 'max': 0.005}, 방향 오차(°) {'n': 12, 'mean': 0.0261, 'median': 0.0257, 'max': 0.0598}, MAIN band 이내 12
- 실행 시간(초): 전체 {'n': 30, 'mean': 145.4868, 'median': 51.564, 'max': 292.3672}, 주행 {'n': 12, 'mean': 287.9905, 'median': 286.6076, 'max': 292.3672}, 미주행 {'n': 18, 'mean': 50.4843, 'median': 50.565, 'max': 51.5665}

- main E1 runs only (amendment v05, new output); technical pilots and the 11 preliminary v03 runs are excluded
