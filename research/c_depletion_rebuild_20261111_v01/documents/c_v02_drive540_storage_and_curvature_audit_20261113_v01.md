# C-V02 540회 저장량 및 곡률 거절 원인 감사 — 2026-11-13 v01

## 상태와 범위

**본실험 HOLD, 실제 본실험 0/540. 이번 작업은 CPU 읽기 전용 분석이며 새 렌더링·추론·학습·물리 이동을 실행하지 않았다.** 기존 Controller PID 2869572 / Watchdog PID 2881294가 살아 있으며 Controller는 `WAITING_STORAGE_AUTHORIZATION_AND_CAPACITY`이다. 저장 승인 파일은 없고 새로 작성하지 않았다. 기존 출력·모델·540개 manifest·안전 기준·경로 목표를 변경하지 않았다. 저장 승인만으로 이번 분석에서 발견된 경로 문제를 해결했다고 간주해서는 안 된다. 본실험 재개 전 연구자 검토가 필요하다.

분석 입력: `C_V02_20261112_v01/DRIVE540_20261113_v01/technical_e2e_v03/pilot_records.json`의 실제 15건, 별도 engineering 실제 이동 1건. 기존 첫 HR 무검출 파일럿은 원본 `recovery_e2e_v01` 경로 그대로 읽었다. 파일럿 15건은 기술 정상 처리 15건, 과학적 결과 무검출 5건/경로 거절 10건, 실제 E2E 작업 성공 0건이다. 별도 engineering 이동 성공을 E2E 작업 성공으로 세지 않았다.

## 1. 722.5MB의 실제 구성

별도 engineering 폴더의 apparent size는 **722,510,798 bytes =722.511MB =689.040MiB**이다. 파일별 크기·할당 크기·inode·SHA256은 `storage_files_16_runs.csv`, 디렉터리별은 `engineering_directory_totals.csv`에 있다. 16개 닫힌 run의 총 2,241개 파일을 조사했다. engineering 폴더에는 hard-link 중복이 없으며 unique-inode 합도 동일하다.

| category | files | MB_decimal | percent |
| --- | --- | --- | --- |
| endpoint_forensics | 2 | 224.870 | 31.12 |
| physics_contact_points | 1 | 190.554 | 26.37 |
| simulator_console_log | 1 | 100.603 | 13.92 |
| planner_path_sweep_support | 6 | 61.073 | 8.45 |
| timing_forensics | 3 | 48.834 | 6.76 |
| robot_state_trace | 2 | 35.661 | 4.94 |
| motion_JPEG_frames | 611 | 27.677 | 3.83 |
| controller_command_trace | 1 | 21.999 | 3.04 |
| other_required_audit | 61 | 3.762 | 0.52 |
| ROS_driver_observer | 7 | 2.624 | 0.36 |
| physics_step_trace | 1 | 1.597 | 0.22 |
| initial_RGB | 2 | 1.283 | 0.18 |
| initial_depth | 1 | 1.229 | 0.17 |
| derived_overlay_or_image | 1 | 0.393 | 0.05 |
| code_snapshots | 27 | 0.275 | 0.04 |
| run_provenance_results | 5 | 0.048 | 0.01 |
| camera_capture_evidence | 9 | 0.029 | 0.00 |

주요 단일 파일: driver_endpoint_forensics.jsonl 200.860MB, contacts.json 190.554MB, runtime.log 100.603MB, driver_timing_v18.json 37.239MB, steps.jsonl 35.657MB, leg_0/1_swept.json 각각30.382/30.399MB. 영상이 대부분이라는 설명은 맞지 않는다.

- 실제 로봇 카메라 JPG 611장 합27.677MB. 초기 RGB는 PNG+NPY 두 파일 합1.283MB, Depth NPY 1.229MB. RGB 두 형식은 같은 관측의 다른 표현이며 JPG 동영상 프레임과 초기 RGB는 시점·용도가 다르다. 원본 동등성·검증기 의존성을 확인하지 않고 하나를 삭제할 수 없다.
- 이 722.5MB 안에는 MP4가 없다. 나중에 별도 `visual_evidence_v01`에서 기존 JPG로 만든 MP4는6.085MB이다. 이를 만들지 않아도 현재 417GB 예측에서는 절감이0이다. 전 시행마다 별도로 만들 경우 약3.286GB가 추가된다. 영상 생성 여부를 전체 저장 예측과 혼동하지 않는다.
- 전체16 run에서 SHA256까지 같은 반복 파일의 추가 복사 합은41.390MB이다. 이는 동일 로그 내용을 시간상 독립적인 새 정보로 해석하면 안 된다는 의미다. 단, 여러 run의 provenance를 보존해야 하므로 무조건 삭제 가능한 용량이 아니다. `feedback.json`은 마지막 steps record와 내용이 같지만 전체 시간 이력을 대체하지 않는다.
- runtime.log 399,012줄 중 `PxShape::getMaterialFromInternalFaceIndex` 메시지383,319줄/93.472MB, 기존 cameraPrim 참조 경고7,624줄/7.081MB이다. 반복 메시지임을 확인했으나 원인·접촉 자료에 대한 영향까지 무해하다고 확정한 것은 아니다. 별도 검토 전 경고 차단이나 로그 삭제를 제안하지 않는다.

## 2. 결과별 저장량과 540회 재산정

관측 무검출5건 평균 **8.294MB/run**, 경로 거절10건 평균 **8.604MB/run**이다. 성공 E2E 및 이동 도중 실패의 실제 표본은 없다. 따라서 성공은 engineering 이동722.511MB를 대리값으로 사용하고, 이동 실패는 지속 시간 조건부 모델로만 산정했다. 물리 시뮬레이션 시간 약126.917초의 한 engineering 시험은 모든 미래 주행 길이·wall-clock 시간을 대표하지 않는다.

`S×722.510798MB + N×8.2944738MB + P×8.6035706MB + F×[8.494MB + t×(722.511−8.494)MB]`가 원본 기준 근사식이다. S/N/P/F는 성공/무검출/경로거절/이동실패 수, t는 engineering 대비 이동 로그 지속 비율이다. 실패 기본값8.494MB는 조기 종료15건 평균이다. t 모델은 실제 관측치가 아니다.

| 조건부 시나리오 | 원본 GB | +25GiB 여유 GB |
| --- | ---: | ---: |
| 전540건 engineering와 같은 이동량 |390.156|416.999|
| 전540건 무검출 |4.479|31.323|
| 전540건 경로 거절 |4.646|31.489|
| 관측 Base01 비율을 단순 반복한 계산(예측 아님) |4.590|31.434|
| 270이동+90무검출+90경로거절+90절반길이 이동실패 |229.494|256.338|
| 전540건 절반길이 이동실패 |197.373|224.217|
| 전540건 두배길이 이동실패 |775.721|802.565|

**417GB는 한 이동 시험을540배 한 값에25GiB 여유를 더한 조건부 예산이다. 실제 예상값이나 절대 상한이 아니다.** 조기 실패가 많으면 크게 줄고 이동/정체가 길어지면 초과한다. 540회의 실제 성공률을 알 수 없어 하나의 정확한 저장량을 제시할 수 없다. 현재 작은 실패량을 이유로 저장 게이트를 낮추지 않았다. 8TB 경로의 사용자 쓰기 권한·명시적 승인 미완료도 그대로다.

## 3. 저장 개선안 — 이번에는 미적용

1. **무손실 보관 압축**: engineering의 모든 파일을 RAM stream에서 gzip 압축/복원하고 원본 SHA256과 비교했다. level1=102.123MB(85.9% 절감), level6=81.323MB(88.7% 절감). 원본 파일이나 압축 archive는 만들거나 바꾸지 않았다. 같은 비율이540회에 적용된다는 조건에서 원본 대비335.010/346.241GB 절감, 여유 포함81.990/70.758GB가 된다. 압축 전 active 공간과 원본 검증 동안의 최대 공간은 별개다.
2. **검증기 호환성 선행**: 현행 technical_gate v02는 contacts.json, steps.jsonl, front_rgb.png/npy, front_depth.npy 등 실제 경로를 요구하고, 이동시 rec_robotcam JPG 존재도 검사한다. `.gz`만 남기는 것은 현행 요구와 충돌한다. 향후 별도 버전의 압축-aware verifier 또는 SHA로 검증된 복원 계층이 필요하며, 회귀검증·승인 전에는 적용 불가하다.
3. **파생 영상 선택 생성**: 원본 JPG 보존 후 대표 성공/실패만 MP4 생성 가능. 전540건 MP4 생성 대비 약3.286GB의 추가 저장 회피이나 기존417GB에서 차감할 수 없다. JPG 삭제/프레임 간격 변경은 제안 적용하지 않는다.
4. **반복 code/config 공통 보관**: immutable content-addressed blob + 시행별 SHA manifest 방식은 가능하지만 동일 파일별 검증 경로와 provenance를 만족해야 한다. 현재16건 중 모든 exact duplicate가 code만인 것은 아니므로41.390MB를 곧바로 전체 절감으로 외삽하지 않는다.
5. **반복 진단 메시지**: 접촉·명령·시각·오류 발생 횟수/시각을 잃지 않는 수집 구조 개선은 검토할 수 있다. 접촉 자료 downsample, warning 숨김, 안전 로그 생략은 현재 근거로 승인할 수 없다. 우선 무손실 압축이 정보를 보존하는 대안이다.

## 4. 곡률 거절10건의 대응 비교

모두 Base01, O0, 단일 적재물이다. 실제 초기 자세는 x≈−26.067987m,y≈27.709175m,yaw≈86.000°로 거의 동일하다. 검출 및 frozen ROBUST_A 계산은10건 모두 수행됐다. 단위는 위치 m/곡률 m⁻¹이다. 전체 시작·추정 중심·물체 heading·PRE/FINAL·datum·로그 SHA는 `curvature_rejections_10.csv`에 있다.

| representation | C | start_yaw_deg | pre_x | pre_y | nominal_center_error_m | necessary_k | candidate_min_peak_k | baseline_quintic_peak_k |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LR_Scan | C100 | 86.000330 | -25.891117 | 28.306415 | 0.003326 | 1.819399 | 2.050061 | 2.815452 |
| GeoCAD | C100 | 86.000330 | -25.890924 | 28.306415 | 0.003145 | 1.820989 | 2.051697 | 2.817977 |
| LR_Scan | C80 | 86.000330 | -25.891117 | 28.306415 | 0.003326 | 1.819398 | 2.050060 | 2.815451 |
| GeoCAD | C80 | 86.000330 | -25.890923 | 28.306415 | 0.003145 | 1.820994 | 2.051703 | 2.817986 |
| HR_Scan | C60 | 86.000330 | -25.891117 | 28.306415 | 0.003326 | 1.819401 | 2.050063 | 2.815455 |
| LR_Scan | C60 | 86.000330 | -25.891116 | 28.306415 | 0.003325 | 1.819406 | 2.050067 | 2.815463 |
| HR_Scan | C40 | 86.000330 | -25.891117 | 28.306415 | 0.003326 | 1.819399 | 2.050061 | 2.815452 |
| LR_Scan | C40 | 86.000330 | -25.891116 | 28.306415 | 0.003325 | 1.819404 | 2.050065 | 2.815460 |
| HR_Scan | C20 | 86.000330 | -25.891052 | 28.306415 | 0.003265 | 1.819933 | 2.050610 | 2.816299 |
| LR_Scan | C20 | 86.000330 | -25.891050 | 28.306415 | 0.003263 | 1.819947 | 2.050625 | 2.816322 |

허용곡률은 **0.363645332585m⁻¹** (`.95*tan(15°)/.7`) 그대로다. 전10건에서 TC-S의 고정 rho24개를 그대로 계산했다. 가장 낮은 후보 peak조차2.050060~2.051703m⁻¹, 허용의약5.64배이며, old quintic도약2.815m⁻¹이다. `curvature_candidates_1104.csv`에10실측+36기준진단×24=1,104개 후보가 있다. `rejected_candidate_*.csv`는 거절 후보의 CPU 재구성일 뿐 실제 승인된 경로나 실제 이동 trace가 아니다. 원본에는 admitted leg_0_path가 없으며 로봇은 움직이지 않았다.

### 원인 분리

- **중심 추정 오차가 주원인이라는 근거는 없다.** 추정 중심과 scene construction의 평가용 기준 중심(−25.888,30.509)의 차이는3.145~3.326mm이다. 설계 기준 중심으로 PRE를 만든 진단에서도10건 모두 아래 필요조건을 위반한다. 이 비교는 GT를 운용 입력에 제공한 재실행이 아니라 오프라인 평가용 counterfactual이다.
- **짧은 전진 거리에서의 횡방향 이동과 종료 방향 제약이 핵심이다.** 약0.6m 안에서 우측으로약0.18m 이동하며86°에서90°로 정렬해야 한다. 차체가 아니라 rear axle 기준으로 분석했다. 물체의 추정 heading은0° 부근이지만 task의 접근 yaw90°와 다르며, 기존 코드의 고정 task yaw90°를 오류라고 단정하지 않는다.
- **현재 국소 전진 조건에서는 특정 polynomial만의 문제가 아니다.** 아래 독립 필요조건 하한1.819398~1.820994m⁻¹도 허용곡률의약5배다. 이10건은 TC-S를 조금 다듬어 같은 전진 기하와 제한 안에서 해결할 수 있다는 증거가 없다. 후진·멀리 돌아오는 전역 경로까지 불가능하다는 뜻은 아니다.
- 기존 `bangbang_lb=null / UNKNOWN_NONPARALLEL`은 시작/종료 방향차약4°가 기존 하한함수의 평행조건(<1°)을 벗어나기 때문이다. null이 물리 불가능의 증명도, 단순 구현 오류의 증거도 아니다. 이번에는 방향차를 포함하는 필요조건을 별도 분석했다.

### 비평행 경로의 필요조건과 검증

초기 rear heading 좌표로 끝점 변위(X,Y), 방향차δ를 정의한다. 현행 계획기는 `cos(theta−theta0)>0`인 경로만 허용한다. u=sin(theta−theta0)이면 du/dx=k이므로 |k|≤K에서

`max(−Kx, sinδ−K(X−x)) ≤ u(x) ≤ min(Kx, sinδ+K(X−x))`.

단조 함수 `u/sqrt(1−u²)`를 적분하면 가능한 횡변위 Y의 하한·상한을 얻는다. 이 구간에 들어가기 위한 최소K를 bisection으로 계산했다. 이는 조향 변화율, 끝점 zero curvature, 장애물, 경로 길이를 고려하지 않는 **필요조건**으로, 통과한다고 충분히 실행 가능하지는 않다. 수치적분3건과 평행경로 closed-form 비교4개 검사 최대차약5×10⁻¹²로 통과했다. 새 진단 코드만 NumPy `np.trapz` 미지원으로 첫 초기화가 실패했고, `np.trapezoid`로 수정한 뒤 검사를 통과했다. 이 실패 기록도 보존했으며 기존 실험 실패에 합산하지 않는다.

## 5. 다른35개 Base에서 재발 가능성

540개 잠긴 manifest는36개 Base를15조건에 대응한다. 기존의 시작 위치·yaw와 같은 명목상 PRE를 사용해 **36개 기하 진단만** 수행했다. 새 RGB-D나 모델 추론, Full E2E 결과를 대신하지 않는다.

- 36개 중30개는 위 전진 필요조건 자체를 위반했다. 실제 Base01을 제외해도 다른35개 중29개이다.
- 현행 TC-S 고정24후보 검사에서32개는 경로 미허용,4개(B10/B22/B23/B35)는 곡률·feedforward rate 검사 통과다. 다른35개 중31개 거절이다. 통과한4개도 충돌·추론·PhysX·제어 성공을 의미하지 않는다.
- B11/B34는 필요곡률 하한≈0.302834<제한0.363645이지만, TC-S best peak≈0.403432로 거절된다. 이2개는 필요조건으로 물리 불가능이라 결론 낼 수 없고 **현행 후보군의 보수성/탐색 한계 가능성**이 남는다. 개선 가능한 경로가 실제 존재한다는 증명도 아직 없다.
- 10개 관측 중심 편차를 각36 Base에 옮긴360개 sensitivity 계산도 제공한다. 시점이 달라지면 추정 편차 자체가 달라질 수 있으므로 미래 실패율 예측이 아니다.

따라서 Base01만의 예외라고 볼 근거는 약하다. 동시에32/36을540회 예상 실패율로 보고해서도 안 된다. 환경 family10개와 공통물리배경1곳의 반복 구조도 유지한다.

## 6. v44~v48과 비교 — 분모·모델·계획기 혼합 금지

| version | scope | finding |
| --- | --- | --- |
| v44 | 972 static RGB-D inputs / paired324, old perception and B5 | Historical pose/occlusion calibration; not C-V02 physical trials |
| v45 | Historical cross-representation mixed-target audit | Different model/data/scene selection task; no pooled count |
| v46 | 319 computed old B5 poses × pred/design × two planners =1276 CPU calls | Design targets still rejected219/319; pred-fail/design-pass89 old or71 smooth |
| v47 | Same old219 cases, frame and geometric audit | Old quintic:52 local-distance +3 forward-goal +164 curvature; frame consistency~1e-14 |
| v48 | Only historical handoff instructions found | No locally verified completed v48 result; did not execute instructions |
| current_CV02 | 10 actual Base01 premotion rejections plus36 nominal CPU diagnostics | Frozen TC-S; nonparallel necessary bound and all24 rho examined |

과거에도 설계상 목표를 사용한 진단에서 경로 거절이 남았다는 정성적 공통점은 있다. v47의52건 거리초과/3건 전방조건/164건 곡률 분류는 현재10건에 합산하지 않는다. 기존 v48 handoff는 과거 지시문이며 이번에 실행하지 않았다. 현재 사용 planner SHA는 `ca15e21b8b581cd03e545421861a86e8200628b06c96d03e73d090eed411fbe4`이다.

## 7. 본실험 전 필요한 결정

1. 저장 공간 권한·위치·용량 확보는 미해결이다. 417GB는 조건부 예산이며 실패량을 근거로 임의 축소하지 않는다.
2. 연구 목적이 모델/표현 차이인 상황에서 대부분의 명목 시작기하가 같은 경로 게이트를 위반한다는 점을 연구자가 검토해야 한다. 현행 그대로 실행할 경우 정상 연구 실패로 기록할 수 있지만, 경로 기하가 인식 표현 차이를 압도할 위험이 있다.
3. 안전 곡률 완화, 시작/목표/yaw/manifest 변경은 이번에 하지 않았다. 가능한 후속안은 (a) 현행 설계를 유지하고 구조적 거절을 그대로 측정하거나, (b) 본실험 전 별도 승인된 프로토콜 개정으로 접근전략/전역계획기를 검증하는 것이다. 어느 쪽도 이번 분석에서 자동 선택하지 않는다.
4. 반복 PhysX material 메시지의 원인·접촉 증거 영향도 별도로 확인할 필요가 있다. 반복 경고가 많다는 이유만으로 안전한 무해 경고라 확정하지 않는다.
5. 기존 실제 이동·정지 검증의 PASS는 보존하되, 그것이 Base01에서 추정된 목표의 실행가능성을 증명하는 것은 아니다. 새 실제 이동·본실험은 시작하지 않는다.

## 산출물 및 재현

같은 이름의 새 분석 디렉터리에 파일별2,241행 목록, 범주·디렉터리 합계, 중복 SHA, 압축 round-trip, outcome별 저장량/540조건부 예측, 곡률10건·후보1,104건·36Base·편차360건 CSV를 보존했다. `storage_files_16_runs.csv`(약1.06MB)는 로컬 보존하며 공개 자동 동기화의1MiB 상한 때문에 제외한다. 나머지 텍스트 요약/CSV/분석 코드를 명시적으로 GitHub 동기화한다. 원본 RGB-D·JPG·MP4·모델은 게시하지 않는다.

재현 스크립트는 `analysis/c_v02_drive540_storage_audit_20261113_v01.py`, `analysis/c_v02_drive540_curvature_audit_20261113_v01.py`이다. 출력은 x모드/새 디렉터리로 생성해 기존 결과 덮어쓰기를 방지한다. 재실행 시 별도 버전 출력 경로로 변경해야 한다. CPU1개 affinity47/nice15, OMP/BLAS1thread로 실행했다. legacy GPU 모듈은 import하지 않았고 정적으로 확인한 pure-math planner만 읽어 사용했다.
