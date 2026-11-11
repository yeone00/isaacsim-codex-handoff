# C RGB-D 데이터와 모델 계획 (DRAFT, 신규 생성 미실행)

권위 자료는 `reports/progressive_depletion_original_design_recovery_audit_20261111_v01.md`와 거기서 검증한 원본 제거 lock/manifest/history다. 기존 B1_CLOSED_EV.usdz 및 광학·렌더·에셋·visibility QA의 실제 경로와 SHA를 원래 B1 설정에서 고정한다. B1의 `step21` complete-layer builder는 그대로 C builder가 될 수 없다. 새로운 version adapter에만 잔여 mask를 전달하고, RGB/Depth/canonical/visible GT 모두 같은 잔여 슬롯을 사용하도록 추가 구현해야 한다. 아직 C adapter·그 QA·dataset lock이 없다.

분할 예시는50/10/10 base families × [공유FULL1+5T×4부분] =1050/210/210 scenes/표현, 총4410 RGB다. 이는 아직 확정된 sample membership가 아니다. 기존1000/200/200과학습 update수가 같지 않다는 한계도 기록한다. 동일family의 경로·C·O·표현은 같은split에 귀속한다. 단일 B1 배경 공유를 독립현장 검증이라고 부르지 않는다. 원래 평가용1680test를 새train에 재사용하지 않는다. 동일 C100 템플릿은 의도된 공통 물체이고, 동일배치/시점까지 겹친 입력 누수와 구분한다. partial geometry 중복 처리 정책과 family 정의가 확정되기 전 HOLD다.

O0는panel없음이며NuRec/자기가림까지0이라는뜻이아니다. O25/O50는목표canonical visible mask 대비 실제 panel 차폐를 측정하며, 기존 panel fixture의 threshold/MARGIN/refine/achieve/저장규칙을 임의 완화하지 않는다. 과거 G1 감사에서 fixture시점의빈 panel mask가저장된사실을새자료에서는명시적으로방지한다. 새 C GT에는 제거된묶음이없어야하고각표현/가림별aligned RGB·Depth·target/all-instance·panel mask 및 calibration을 실제 저장해야한다.

QA에는 brick수·slot·phase·strict nesting·세표현pairedgeometry·sourcehash·depth유효성·projection·target ID·mask GT·가림률·지지/부유/중첩/충돌·visibility·split누수가포함된다. 최고층제거와아래층완전유지는명목support증거일뿐CoG/접촉물리증명이아니다. visual static생성기에는실제동적지지검사가없어추가구현/검증필수다. 검사마다샘플분모·검사수·FAIL/UNKNOWN을보존하고전부통과한manifest만최종잠금한다.

재사용은L4의배치·시점·광학·환경·pixel/depth/GT까지새조건과일치하고새split누수가없을때만한다. 기존B1package에는필요한새C전체depth/GT가없으므로형상만일치한다고C100전체재사용PASS를주지않는다. 원본은읽고새root에경로/hash참조만둔다.

P0: C기본증강3표현×seed42=3모델. P1: 잠근Test의5C×3O×3표현인식/target선택및pose평가. P2:43/44까지총9기본모델,seed42중복과분산보고. 선택된L-HPO설정대조는Val에서먼저별도최대3모델(seed42)을더할수있고두설정을3seed로비교하면총최대18이다. 선정설정이기본과같으면중복학습하지않는다. 기존48개무조건재학습/혼합비율재탐색은P3별도다.

과거Stage1 evaluator의AP/IoU/Top1/OTHER_LOAD/PANEL/BACKGROUND/NO_DETECTION정의를재사용할수있으나하드코딩된B1 Test200/manifest/model-lock/path를새C용명시적입력으로바꾼별도version이필요하다. Stage2도geometry/GT/eval-only역할·분모·조건부오차를분리한새adapter가필요하다. 원본script를바로새자료에실행하지않는다.

모든후속GPU작업은현재PREPARATION_ONLY범위밖이다. 기존HPO종료는새작업실행허가가아니며,입력/알고리즘/QA/성공규칙을확정하고별도승인된version에서만가능하다.
