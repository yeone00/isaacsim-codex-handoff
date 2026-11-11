# C 전용 공통 HPO 단계 추가 — 계획 개정 기록

기존 C_DEPLETION_REBUILD 지시문 전체는 유지한다. 현재 L1–L4 HPO는 중단/수정 없이 완료 후 예비 탐색으로 보존한다. 기존 「L-HPO 설정의 C 전이 보조 대조」 대신 **C 데이터 QA·Train/Val/Test 잠금 이후 C 전용 공통 HPO를 필수 단계로 추가**했다.

변경 순서: C dataset/QA/split lock → C-HPO → 최종 공통 설정/9모델 고정 및 seed 반복 → 인식 평가 → 위치추정/ROBUST_A → 기술 파일럿 → G1 300회.

계획 상세는 `docs/c_depletion_common_hpo_plan_AMENDMENT_20261111_v01.md`다. 별도 DRAFT 예산은12후보(기본1+L-HPO 상위 비기본 최대3+새random 최소8),3표현공통seed42·60epoch screening,상위3+base200epoch,선정설정seed43/44다. qualification 포함최대57run/5766 model-epochs. 최종seed42는선정된완료200epoch checkpoint를검증해재사용하고,최종3seed9모델을확보한다. 모든실제학습은공통pretrained에서시작하며 L 모델 가중치는이식하지않는다.

목적함수는세표현자기표현C-Val Mask mAP50–95의동등가중평균이다. L상위설정은초기후보일뿐최적가정없음. Test/O50/RealTest189를선정·후보추가·조기종료에사용하지않는다. 샘플분할·모든seed역할·실제v04 RNG/FP32/AMP·고정kwargs·동점규칙을잠근다. 예산/실제후보는C QA후학습전에고정하며이번에는생성하지않았다.

실행범위는 PREPARATION_ONLY/HOLD 그대로다. 신규 GPU·물리주행0. Controller/Watchdog·ntfy·GitHub연동과현재HPO의코드/프로토콜/결과를수정하지않는다. 현재runtime의 `C_training_evaluation`은상위단계명이고추가한내부단계는계획JSON에기록한다. 아직실제C-HPO adapter가구현/연결됐다고주장하지않는다. 실제후속GPU실행은별도승인과새버전이필요하다.
