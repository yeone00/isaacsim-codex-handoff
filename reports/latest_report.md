# 연구 결과 통합 스냅샷 — 2026-11-13T14:26:18.471186+09:00

현재 C-V02 결과와 이 저장소의 기존 연구 보고서·집계표를 한 ZIP에 보존한 읽기 전용 추출본입니다. 서로 다른 실험 버전과 분모를 합산하지 않습니다. 파일 작성 중에도 원래 실험은 계속 실행되므로 파일별 캡처 시점은 조금 다릅니다. 원본·학습·실행기 변경 없음.

## 현재 완료와 미완료

- C-V01 4,410장 보존, C-V02 추가 C100 840장 및 전체 5,250장 검증 완료.
- C-V02 표현별 Train 1,250 / Validation 250 / Test 250, 각 C 상태 250/50/50. 기본 환경 계보 총70, Train50/Val10/Test10. 반복 관측은 독립 환경이 아님. C100만 추가 시점 관측이라는 교란 한계 유지.
- C06 고정 본 학습39/39 완료, 별도 smoke3건. 45개 논리 모델 셀은 real-only3개 학습 궤적 공유를 포함하므로 45회 독립 학습이 아님. 모두 200epoch, 기존 HPO57건 재실행 아님.
- 선정 공통 비율 S075_R025, Validation 점수 95.327405%. 합성/실사 Validation 동일 가중 및3표현×3seed 평균. Test 선정 사용 없음. 75:25와50:50의 작은 수치차는 통계적 우월성 증명이 아님.
- 선정 모델 인식 평가20250/20250 model-images 완료(2250 프레임×9모델). 자기표현 위치추정 입력6750건. 현재 단계 {'state': 'RUNNING', 'job': 'selected_mixture_pose', 'pid': 2489543, 'updated': 1794547539.9433594, 'physical_motion': False}; 위치추정 완료로 표시하지 않음.
- 합성 전용 baseline, 층수 prior ROBUST_A 후속 평가 및 전체 통합 결론은 완료 여부를 첨부 상태에서 확인. 물리 주행0회/HOLD.

## 위치추정 이후 남은 순서

1. 선정 모델 위치추정 완료 및 실패/조건부 오차 집계, 합성 전용 baseline 인식·위치추정 대응 비교.
2. task_layer_count(C100/80/60/40/20=4/4/3/2/1)만 허용하는 ROBUST_A 별도 평가. 층수는 운영자 작업 prior이며 GT pose/mask/slot/FINAL 입력 금지. 기존 nominal-layer 방법과 구분.
3. 적재율×가림×표현의 오차 전파·실패 분해·통계 불확실성·최종 정적 보고서. 10개 Test 기본환경의 반복관측 구조 유지.
4. 신규 실제 loaded stage collider/바닥/팔레트/적재물/로버 구성, PhysX 접촉, 경로·조향·속도·정지 안전 검증.
5. 진입 조건/승인 충족 후 기술 파일럿. 현재 HOLD이며 이 파일은 실행 승인이 아님.
6. 별도 본실험 O0/O25 300회, O50 강건성150회. 분모·통계 별도, 실패 보존, 450개 독립 장면 주장 금지.
7. 실패/오차 전파/구축 부담 분석 및 논문3·4장 결과 통합.

Main 성공허용값0.11m/7.341774도 및 충돌·안전 위반 없음. PRE/FINAL5mm/2도 도달인증과0.03m/s 안전정지는 별도. 현재 물리 gate와 승인/HOLD 유지.

## ZIP 내용과 지표 해석

- current/CSV: 45개 checkpoint/원래SHA/epoch/두 Validation 점수, 비율 및 표현별3seed 요약,39개 본학습+3smoke 실행정보, epoch별 상세 기록.
- selected_mixture_eval_v01: 완료 인식평가 AP와20250행 대상별 원자료. AP의 all/target GT 분모와 attempted_images를 원본 그대로 보존. mAP값은0~1 단위.
- derived/target_condition_summary.csv: seed/표현/가림/C별 파생 집계. 검출=운용confidence 통과 후보의 target IoU>=0.5, 전체시도 분모; eligible 수 별도. oracle IoU와Top1 IoU 구분. 이 평균에 실패가 포함되며 위치추정 조건부 오차와 혼동 금지.
- snapshots: 프로토콜/선정lock/QA/상태/partial pose 산출물 중 존재하는 CSV·JSON. 미완료 pose 파일은 progress snapshot이며 완료 판정 근거 아님.
- historical_reports: 기존 연구 Markdown 및 CSV 표를 버전 그대로 포함. 과거 B1·C-V01·Stage1~4는 신규 C-V02 결과와 섞지 않음. historical 문서의 당시 상태는 현재 상태가 아님.
- source_inventory.csv: 각 원본 절대경로, ZIP내 경로, 복사한 바이트의 SHA256. 대용량 RGBD/이미지/weights는 복사하지 않고 경로·SHA로 참조. 비공개 ntfy 설정은 포함하지 않음.

실사 Test189는 과거 평가 이력이 있는 재사용 검증이며 신규 blind Test 아님. 알려진 원본 라벨 정책/제품 도메인 차이/v04 RNG 문서 불일치/Replicator 예외의 미해명 부분은 기존 감사 보고서 그대로 유지.
