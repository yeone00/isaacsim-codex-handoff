# L_E13 540회 본실험 최종 결과 — 자동 생성

- 위치 L_E13, 속도 정책 PHASED (일반 이동 상한 0.5 m/s, 최종 정지 SQRT), 다중 시점 최대 3회 촬영
- 완료 540 / 540, 경과 28.4 h, 최근 30회 평균 152.0 초/회, 완료 예상 2026-11-15 17:08
- 다중 시점 작동 10회 (K2 검출 10, K3 검출 0), 평균 촬영 1.019회, 추가 시간 {'n': 10, 'mean': 3.2291, 'median': 3.2018, 'max': 3.3116}
- 저장: 압축 535개 중 검증 535개, 볼륨 여유 7.37 TB

| 구분 | 시도 | 성공 | 성공률 | 초기 검출률 | 다중시점 추가 검출 | 최종 검출률 | 주행 성공률 | 결과 유형 |
|---|---|---|---|---|---|---|---|---|
| HR_Scan | 180 | 178 | 0.989 | 0.944 | 10 | 1.0 | 0.994 | {'success': 178, 'technical_hold': 1, 'drive_failure_or_outside_band': 1} |
| LR_Scan | 180 | 177 | 0.983 | 0.994 | 0 | 0.994 | 0.989 | {'success': 177, 'drive_failure_or_outside_band': 1, 'technical_hold': 2} |
| GeoCAD | 180 | 177 | 0.983 | 1.0 | 0 | 1.0 | 0.983 | {'success': 177, 'drive_failure_or_outside_band': 1, 'technical_hold': 2} |
| C100 | 108 | 108 | 1.0 | 0.907 | 10 | 1.0 | 1.0 | {'success': 108} |
| C80 | 108 | 106 | 0.981 | 0.991 | 0 | 0.991 | 1.0 | {'success': 106, 'technical_hold': 2} |
| C60 | 108 | 108 | 1.0 | 1.0 | 0 | 1.0 | 1.0 | {'success': 108} |
| C40 | 108 | 108 | 1.0 | 1.0 | 0 | 1.0 | 1.0 | {'success': 108} |
| C20 | 108 | 102 | 0.944 | 1.0 | 0 | 1.0 | 0.944 | {'success': 102, 'drive_failure_or_outside_band': 3, 'technical_hold': 3} |
| 전체 | 540 | 532 | 0.985 | 0.98 | 10 | 0.998 | 0.989 | {'success': 532, 'technical_hold': 5, 'drive_failure_or_outside_band': 3} |

- 위치추정 오차(m): {'n': 539, 'mean': 0.0047, 'median': 0.0037, 'max': 0.2118}
- 주행 538회: 최고 속도 {'n': 538, 'mean': 0.3833, 'median': 0.3746, 'max': 0.4395}, 최종 위치 오차(m) {'n': 536, 'mean': 0.0053, 'median': 0.0042, 'max': 0.2146}, 방향 오차(°) {'n': 536, 'mean': 0.0443, 'median': 0.0365, 'max': 0.5259}
- 실행 시간(초): 전체 {'n': 540, 'mean': 154.6576, 'median': 154.8143, 'max': 325.3892}, 주행 {'n': 538, 'mean': 155.0166, 'median': 154.8147, 'max': 325.3892}

- 조건 균형: 조건 수 15, 조건별 회수 [36], 각 20회 정확히 포함: False
- 처음 540행과 전체 540행의 분포 차이(최대 절대 비율 차): base 0.0, start 0.0, C 0.0, rep 0.0, task_layers 0.0
- first 540 manifest rows = bases ['C2D_B01', '...']; bases are disjoint between the first 300 and the remaining 240 rows, so scene membership differs by construction; C and representation are exactly balanced

- 세부 표(표현×적재율)는 같은 이름의 .json에 있습니다.
- L_E13 main (amendment v06); E1 54 runs and pilots excluded
