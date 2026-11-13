# C-V02 540회 경유점·전역 경로 개선안: 36 Base 오프라인 비교

2026-11-13 / 보고서 v01 / 수치 비교의 최종 산출물 v02

## 결론과 현 상태

**540회 본실험은 HOLD, 0/540이며 새 실제 주행·Kit·렌더링·모델 추론을 실행하지 않았다. 기존 planner/controller/protocol/manifest/안전 제한을 변경하지 않았다.** 새 analysis 파일은 운영 실행기와 연결되지 않은 수학적 검토용이다. 사용자 승인 전 실제 planner 구현·물리 검증·본실험 진입을 하지 않는다. 저장 승인 파일도 만들지 않았다.

기존 시작점을 그대로 두어도 장애물이 없는 평면에서는 곡률과 조향 변화율을 지키는 경로가36/36 존재한다는 구성적 예를 얻었다. 그러나30개는17.874~18.293m를 크게 돌아오는 경로여서 **현행 국소 경로 정책과 제어기 그대로 실행 가능한36개 경로를 확보한 것은 아니다.** 충돌 및 실제 제어 안전성은 전부 UNKNOWN이다.

같은 시작점을 유지하면서 비교적 짧게 개선되는 것은 B11/B34이다. 기존 통과4개를 포함해 총6개가 약1m 경로의 기하·조향 변화율 검사를 통과했다. 나머지30개는 초기 방향 기준 단조 전진 제약을 유지하는 한 단순 경유점 추가로 해결되지 않는다.

별도 미승인 시작점 대안으로 모든 Base의 world Y를 동일하게−1.25m 이동하면 기존 TC-S 계획기가36/36 통과했다. 이는 실제 실행 조건 변경을 제안하는 **counterfactual**일 뿐 manifest 수정이나 새 파일럿 실행이 아니다. 새 시작점의 센서 관측·충돌·지지 상태는 미검증이다.

## 1. 고정한 항목과 비교 범위

- 실제540개 attempt와36개 Base, 단일 적재물/팔레트, O0, 대응 관계 유지.
- steer 기반 허용 rear curvature `0.363645332585/m`, wheelbase0.7m, rear offset0.338m, nominal speed0.02m/s, steer feedforward rate cap4.3976°/s 유지. 속도 안전 정지0.03m/s 등 실제 제약을 완화하지 않았다.
- 명목 PRE=(-25.888,28.305254968739225), task heading90°; FINAL=(-25.888,29.105254968739225). 원본 scene의 평가용 설계 좌표를 CPU 진단에만 사용했다. 운용 시에는 동일 정책으로 실제 인식·ROBUST_A 예측 목표를 사용해야 하며 GT 중심·mask·slot은 제공하지 않는다.
- 이번36개 비교는 **같은 명목 목표에 대한 기하 비교**다. 15조건별 실제 RGB-D 추정 결과나 Full E2E를 대체하지 않는다. 적재율·표현마다 센서 오차가 달라질 수 있다. HR/LR/CAD 및 다섯 적재 상태에 특정한 경로 튜닝을 하지 않았다.
- FINAL까지는 PRE에서 같은 heading으로0.8m 직진하는 명목 기하이므로 기존 접근 문제는 start→PRE에 집중했다. 실제 PRE 정지 오차 이후 FINAL 재계획·충돌·도달 인증은 여전히 검증 대상이다.

기존540 manifest SHA: `92ba7c2909f78110d4fa985de17ce6863538b0110dfb3e42a7e7784f05ce19fc`

기존 protocol SHA: `fa5ef9a20d0d9172f48f25b20e7a72e3dcb2c953759eafb0a4da3e18af2630d2`

기존 TC-S planner SHA: `ca15e21b8b581cd03e545421861a86e8200628b06c96d03e73d090eed411fbe4`

위 세 원본은 분석 전후 SHA가 같다. 모델 checkpoint/학습/정적 결과도 수정하지 않았다.

## 2. 비교한 개선 설계

### A. 단순 경유점 + 기존 국소 TC-S

목표를 여러 점으로 나누더라도 각 leg와 전체 경로가 초기 방향 기준으로 계속 전진하고 같은 곡률 제한을 만족한다면, 기존 감사의 횡변위 필요조건이 전체 경로에 그대로 적용된다. 30/36은 그 조건을 위반하므로 **단순히 중간점을 넣으면 해결된다고 할 수 없다.** 기존 코드는 각 goal yaw를90°로 고정하므로 임의로 경유점 heading을 바꾸는 것도 현행 구현 그대로의 사용이 아니다.

B11/B34는 물리 필요조건은 통과하지만 TC-S 후보군이 거절했던2건이다. 이 둘은 후보군 확장으로 개선할 여지가 있으며 아래 B의 짧은 경로로 그 기하학적 가능성을 확인했다. 단순 waypoint 검색에서 실패했다고 전체 가능한 waypoint를 소진했다고 주장하지 않는다.

### B. 곡률 연속 원호–직선–원호(CSC) 자유공간 설계

rear-axle SE(2)에서 시작/끝 방향을 정확히 연결한다. 좌/우 회전의4조합과 K/LIMIT=1.0/0.8/0.6의 사전 고정12후보를 공통으로 계산한다. K는 수치 round-off 방지용1e−8 상대 여유만 두었고 제한보다 커지지 않는다. 원호 연결 시 곡률이 순간 점프하지 않도록 `0→±K→0` 선형 ramp를 각 회전에 넣었다. 직선/경로 시작/끝의 곡률은0이다.

곡률 ramp 기울기는 `a = radians(4.3976)/(0.7×0.02)` 이하로 둔다. steering δ=atan(0.7k)이므로 `|dδ/dt| =0.7|dk/ds| v_rear/(1+(0.7k)^2)`이며 rear speed≤0.02이면 기존4.3976°/s를 넘지 않는다. 이 조건은 제어기의 피드백 보정이나 실제 actuator 동작까지 보장하지 않는다.

원호 hold 길이2개와 직선 길이를 비음수로 풀어 endpoint XY/heading을 맞췄다. 각 후보를 같은 예산(max180 evaluations)으로 계산하고, endpoint XY<1e−6m 및 heading<1e−7rad인 후보 중 짧은 것을 선택했다. 이 수치 tolerance는 **오프라인 해 계산 검증값**이며 기존 로봇 성공 기준이나 안전 gate를 변경한 것이 아니다. 전역 최단경로·전역 완전성을 주장하지 않으며 공간에 장애물이 없다는 가정의 예시 구성이다.

**결과:** 기하·곡률·명목 조향 변화율36/36 통과. B10/B11/B22/B23/B34/B35는 rear 길이0.997~0.999m, 나머지30개는17.874~18.293m이다. 독립0.5mm midpoint 수치 적분으로 endpoint를 재확인했고 최대 차이는약3.6×10⁻¹²m, 샘플 기반 최대 조향 변화율은4.39168°/s였다. 전방 기어로 이동하지만30개 우회 경로는 시작 방향에 대해90° 이상 돌아가기 때문에 현행 `FORWARD_REQUIRED`의 의미와 다르다.

### C. 장애물을 고려하는 전역 state-lattice/Hybrid-A* 설계안 — 미실행

실제 사용할 개선안은 B의 큰 원호를 그대로 연결하는 것이 아니라, (x,y,yaw,curvature) 상태에서 연속 곡률 motion primitives와 기존 충돌·지지 검사를 사용하는 전역 탐색이어야 한다. 충돌 map은 정당하게 사용 가능한 환경 지도/센서 관측에서 얻고, 목표 적재물의 GT footprint·slot·pose를 운용 입력으로 쓰지 않는다. 목표 주변 보호 영역도 관측 기반이어야 한다.

거리·곡률·조향 변화율의 공통 비용/탐색 예산/동점 규칙을 사전 고정하고 모든 표현에 같은 알고리즘을 적용한다. 사후 성공률이나 표현 이름으로 탐색 조건을 바꾸지 않는다. 이 방식의 실제 경로 존재·계산시간·collision-free 여부는 이번에 확인하지 않았다.

## 3. 36 Base 전체 비교

아래 PASS는 기하학적 수치 해에 한정한다. `POLICY_CONFLICT`는 물리 안전 검증 실패라는 실제 관측 결과가 아니라, 현행 정책/제어 가드와 제안 경로가 맞지 않는다는 정적 분석이다.

| Base | existing | smooth_free_space | length_m | frozen_policy | collision_control |
| --- | --- | --- | --- | --- | --- |
| B01 | CURVATURE_REJECT | PASS | 17.903 | POLICY_CONFLICT | UNKNOWN |
| B02 | CURVATURE_REJECT | PASS | 17.879 | POLICY_CONFLICT | UNKNOWN |
| B03 | CURVATURE_REJECT | PASS | 17.874 | POLICY_CONFLICT | UNKNOWN |
| B04 | CURVATURE_REJECT | PASS | 17.890 | POLICY_CONFLICT | UNKNOWN |
| B05 | CURVATURE_REJECT | PASS | 18.097 | POLICY_CONFLICT | UNKNOWN |
| B06 | CURVATURE_REJECT | PASS | 18.078 | POLICY_CONFLICT | UNKNOWN |
| B07 | CURVATURE_REJECT | PASS | 18.074 | POLICY_CONFLICT | UNKNOWN |
| B08 | CURVATURE_REJECT | PASS | 18.086 | POLICY_CONFLICT | UNKNOWN |
| B09 | CURVATURE_REJECT | PASS | 18.293 | POLICY_CONFLICT | UNKNOWN |
| B10 | PASS | PASS | 0.999 | GEOMETRY_ONLY_COMPATIBLE | UNKNOWN |
| B11 | CURVATURE_REJECT | PASS | 0.997 | GEOMETRY_ONLY_COMPATIBLE | UNKNOWN |
| B12 | CURVATURE_REJECT | PASS | 18.284 | POLICY_CONFLICT | UNKNOWN |
| B13 | CURVATURE_REJECT | PASS | 17.904 | POLICY_CONFLICT | UNKNOWN |
| B14 | CURVATURE_REJECT | PASS | 17.878 | POLICY_CONFLICT | UNKNOWN |
| B15 | CURVATURE_REJECT | PASS | 17.878 | POLICY_CONFLICT | UNKNOWN |
| B16 | CURVATURE_REJECT | PASS | 17.904 | POLICY_CONFLICT | UNKNOWN |
| B17 | CURVATURE_REJECT | PASS | 18.096 | POLICY_CONFLICT | UNKNOWN |
| B18 | CURVATURE_REJECT | PASS | 18.077 | POLICY_CONFLICT | UNKNOWN |
| B19 | CURVATURE_REJECT | PASS | 18.077 | POLICY_CONFLICT | UNKNOWN |
| B20 | CURVATURE_REJECT | PASS | 18.096 | POLICY_CONFLICT | UNKNOWN |
| B21 | CURVATURE_REJECT | PASS | 18.292 | POLICY_CONFLICT | UNKNOWN |
| B22 | PASS | PASS | 0.999 | GEOMETRY_ONLY_COMPATIBLE | UNKNOWN |
| B23 | PASS | PASS | 0.999 | GEOMETRY_ONLY_COMPATIBLE | UNKNOWN |
| B24 | CURVATURE_REJECT | PASS | 18.292 | POLICY_CONFLICT | UNKNOWN |
| B25 | CURVATURE_REJECT | PASS | 17.890 | POLICY_CONFLICT | UNKNOWN |
| B26 | CURVATURE_REJECT | PASS | 17.874 | POLICY_CONFLICT | UNKNOWN |
| B27 | CURVATURE_REJECT | PASS | 17.879 | POLICY_CONFLICT | UNKNOWN |
| B28 | CURVATURE_REJECT | PASS | 17.903 | POLICY_CONFLICT | UNKNOWN |
| B29 | CURVATURE_REJECT | PASS | 18.086 | POLICY_CONFLICT | UNKNOWN |
| B30 | CURVATURE_REJECT | PASS | 18.074 | POLICY_CONFLICT | UNKNOWN |
| B31 | CURVATURE_REJECT | PASS | 18.078 | POLICY_CONFLICT | UNKNOWN |
| B32 | CURVATURE_REJECT | PASS | 18.097 | POLICY_CONFLICT | UNKNOWN |
| B33 | CURVATURE_REJECT | PASS | 18.284 | POLICY_CONFLICT | UNKNOWN |
| B34 | CURVATURE_REJECT | PASS | 0.997 | GEOMETRY_ONLY_COMPATIBLE | UNKNOWN |
| B35 | PASS | PASS | 0.999 | GEOMETRY_ONLY_COMPATIBLE | UNKNOWN |
| B36 | CURVATURE_REJECT | PASS | 18.293 | POLICY_CONFLICT | UNKNOWN |

기존4→수학적 후보36이 곧 본실험 진입4→36을 뜻하지 않는다. 현행 거리/방향/overshoot/timeout 정책과의 기하 호환은6개만 확인했고, 그6개도 실제 충돌·제어 검증 PASS는 아니다. 자세한 시작점·곡률·조향 변화율·bounding box·실패 이유는 `base36_comparison_final.csv`에 모두 있다.

## 4. 큰 우회 경로를 현재 실행기에 바로 넣을 수 없는 이유

1. **거리/방향 정책:** 기존 primitive는 .05<D<3m, 초기 방향에 대한 `cos(theta−theta0)>0`를 요구한다. 우회30건은 rear 길이약18m이고 초기 방향 단조성을 위반한다. 원래3m 조건은 endpoint D와 primitive L 두 곳에 있으므로, endpoint가 가까워도 길이18m를 그대로 넣을 수 없다. 한 번에 통과하도록 제한을 삭제하지 않았다.
2. **기존 follower의 GOAL_OVERSHOOT:** v19 command는 최종 goal 방향의 signed along distance<−5mm이면 중단한다. 우회30건은 경로상 이 guard를 위반하는 구간이 실제로 있다. 같은 code를 써도 대원호를 안전하게 따라간다고 가정할 수 없다. 새로 계산한30건은 이 정적 guard 검사와 충돌한다.
3. **시간 제한:** 현행 approach leg는180 sim seconds/320 wall seconds다. 우회30건은0.02m/s 기준 base path 길이만으로 약900초가 필요하다(최대921.1초, 가속·정지 제외). 따라서 timeout을 그대로 적용하면 실행되지 않는다. 제한을 늘리거나 해제하지 않았다. 이 값은 실제 wall-clock 예측이 아니다.
4. **경로 진행 추적:** 현재 follower는 전체 경로에서 rear 위치에 가장 가까운 row를 선택한다. 돌아와서 시작 근처를 지나는 경로에서 진행 인덱스가 튀거나, 다른 구간의 heading을 선택할 위험이 있어 별도 검증이 필요하다. 이번에 실제로 이런 사고가 났다고 주장하지 않는다.
5. **공간:** 후보들의 좌표 합집합은 x≈−31.59~−20.19m,y≈24.04~30.70m다. 이는 각 경로가 그 전체 폭을 쓴다는 뜻은 아니지만 기존 짧은 접근 corridor보다 넓다. 기존 support/PhysX 증거는 이 넓은 영역을 인증하지 않는다. 바닥 collider의 커다란 AABB만으로 그 안의 장애물 없는 공간을 확인할 수 없다.

**따라서 기존 시작점은 자유공간에서 기하적으로 유지 가능하지만, 실제 현장에서 기존 운용 정책까지 그대로 유지하여36개 모두 해결 가능한지는 UNKNOWN이다.** 이런 사실을 무시하고 충돌 검사 없이36/36 실행 가능으로 보고하면 안 된다.

경유점 기반의 향후 구현은 각 leg의 현행 거리·timeout·overshoot·정지 인증을 유지하면서 tangent heading/곡률 연속성, 경유점 정지 후 재계획, 진행 인덱스 등을 명시적으로 설계해야 한다. 현재 CSC 경로를 잘라 붙이는 것만으로 이 조건이 충족된다는 검증은 하지 않았다. 경유점에서 곡률을0으로 재구성하면 경로 자체도 바뀌므로 재계산이 필요하다.

## 5. 별도 시작점 재설계안 — 미승인/미적용

원래 x, yaw, 표현·적재율 pairing을 그대로 두고 모든 Base의 world Y를 공통으로 뒤로 이동하는5개 고정 후보를 계산했다. 각 후보의 시작점→같은 PRE를 기존 TC-S와 동일한24 rho/곡률/조향 변화율/거리 조건으로 검사했다.

| 공통 backward Y 이동 | 기존 TC-S 기하+rate PASS/36 |
| --- | ---: |
| 0m(현재) |4|
| 0.25m |10|
| 0.50m |20|
| 0.75m |26|
| 1.00m |34|
| 1.25m |36|

1.25m는 **시험한 grid 중 처음36개가 통과한 값**이며 최소 필요 거리나 최적 시작점이 아니다. 더 뒤에서 촬영하므로 영상 내 적재물 크기·Depth 품질·모델 검출 분포가 달라질 수 있다. 기존 무검출을 해결하는 방법으로 제시한 것이 아니고, 오히려 검출이 나빠질 수도 있다. scene/family 독립성이나 모델 선정 규칙은 바뀌지 않는다. 원본36 시작점이나540 manifest는 전혀 수정하지 않았다.

이 대안은 크게 도는 경로보다 짧은 접근 구조를 유지할 가능성이 있지만, 신규 시작점의 실제 지지/충돌/camera/PhysX 및 기술 파일럿은 승인 후 따로 필요하다. 각 Base 후보180개 세부 결과는 `base36_start_redesign_counterfactual.csv`에 있다.

## 6. 타당성 및 프로토콜 변경에 대한 제안

- **현재 시작점 유지가 우선이면:** 먼저 장애물·지지를 고려한 전역 경로 탐색과 leg 분할의 CPU 설계를 승인할지 결정해야 한다. 전역 큰 우회는 수학적으로 존재하지만 그대로 도입하기는 어렵다. runtime goal·heading/leg 정책, 진행 추적, timeout 계약까지 명시한 별도 버전이 필요하다. 물리 안전 제한 자체를 완화하는 대안으로 취급해서는 안 된다.
- **현재의 짧은 접근 제어 구조 유지가 우선이면:** 공통 시작점 backward shift를 별도 프로토콜 개정 후보로 검토할 수 있다. 본실험은 아직0회지만 시나리오와 관측 분포가 바뀌므로 원본 잠금은 보존하고 새 manifest/변경 이유/카메라 영향을 사전 기록해야 한다.
- **부분적으로만 planner 개선하면:** B11/B34의 짧은 해는 후보군 한계 개선 근거가 되지만 나머지30건을 해결하지 않는다. 이를 전체 문제 해결로 보고하지 않는다.
- 두 경우 모두36 Base 전부에 동일한 설계 규칙·예산·비용·실패 분류를 적용한다. 특정 표현만 경로를 다르게 유리하게 만들지 않는다. 실제 추정 목표에 의해 경로가 달라지는 것은 기록하되 GT 목표로 대체하지 않는다.
- 모델, C06,75:25,seed42,task layer prior,Main0.11m/7.341774°,도달5mm/2°,speed0.03m/s,충돌 기준은 유지한다. Test를 보고 모델/경로 정책을 다시 선정하지 않는다. 새 planner 선정 시 최종540 수행 결과를 tuning에 사용하지 않는 engineering QA 절차를 사전 고정한다.

**이번 단계의 권고는 본실험 HOLD 유지 및 개선안 선택의 연구자 검토다.** 본실험은 물론 운영 planner 교체·새 기술 파일럿도 시작하지 않는다.

## 7. 검증·파일·실행 경계

- CPU 진단 전용 code: `analysis/c_v02_drive540_global_path_design_20261113_v02.py`, 독립 검토 `analysis/c_v02_drive540_global_path_review_20261113_v01.py`. 실제 실행기에서 import하거나 연결하지 않았다. SciPy1.17.1은 기존 환경에 설치된 버전을 사용했고 설치/업그레이드는0이다.
- 단일 CPU core47/nice15/OMP·BLAS1thread. 수학 solver 입력은 평가용 설계 geometry이며 모델·GT를 운용 worker에 전달하지 않았다.
- v01 초안은 초기 방향 단조성 컬럼의 placeholder(False)가 있어 최종 판정에 사용하지 않았다. 원본 초안은 남겼고 v02에서 실제 경로의 cos 값을 계산했다. 수치 경로·통과 수·길이는 동일하다. 최종 비교는 v02 `base36_comparison_final.csv`와 독립 검토가 권위 자료다.
- 원본 engineering 폴더에서 `gt_geometry_eval_only.json`이라는 이름을 조회한 한 번의 읽기 명령은 파일 없음으로 실패했다. 원본을 수정하지 않았으며 실제 명목 좌표 근거는 정적으로 읽은 scene/session 코드와 기존 감사 manifest이다. 이 파일을 있는 것으로 주장하지 않는다.
- 새 CSV:36조건 최종 비교,432개 사전 후보(336개 수치해 탐색+96개 접선 조건 거절),36개 독립검토,180개 시작점 대안,36개 수학 경로(실제 주행 trace 아님). PNG도 수학 경로 도해이며 Isaac Sim 캡처가 아니다.
- 기존 controller/watchdog는 변경하지 않았고 계속 저장 승인 대기 상태다. 추가 승인파일을 만들지 않았으므로 본실험 진입조건은 충족되지 않는다. 별도 ntfy 서비스·GPU job·재개명령은 실행하지 않았다. 저장/경로 검토가 끝났다는 자동 승인도 하지 않았다.
