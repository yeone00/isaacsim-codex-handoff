# 제3장 방법론 수정안 — Progressive Depletion 복구 (DRAFT)

## 실제 수행 범위와 신규 연구의 구분

기존 B1은 red brick, HR_Scan/LR_Scan/GeoCAD, 완전층 L1–L4(75/150/225/300개)의 별도 실험이다. 기존 48개 모델·Stage1/2·Stage3/4·현재 L-HPO를 이 설계의 결과로 보존한다. LR은 저취득 조건에서 독립 재구성한 에셋이며 HR 감면 mesh가 아니다. Real Test189는 잠금 후 이미 평가됐고 신규 설정 선정에 사용할 수 없다. 실제 외부 검증은 red-only이며 cement 또는 실물로봇 주행 검증으로 확대하지 않는다.

원래 Progressive Depletion은 실제 구현돼 있었으나 B1 생성 경로에서는 사용되지 않았다. 신규 C 연구의 RGB-D·GT·학습·위치추정·300회 주행은 아직 수행되지 않았다. 아래 문장은 연구설계 설명이며 결과 서술이 아니다.

## 적재 구조와 점진적 제거

팔레트 하나는4층, 각층15개 Bundle5(75개 벽돌), 합60묶음/300개다. Pattern A/B의 층별 배치를 유지한다. C100에서 시작해 최고 비어 있지 않은 층의 외부 노출 Bundle5 중 seed로 한 묶음을 선택한다. 외부 노출은10×9 footprint 격자에서 외곽 또는 외부연결 빈 공간에 인접하는 것으로 정의된다. 후보는 매 제거 후 다시 계산한다.12묶음마다 C80/C60/C40/C20을 저장한다. 잔여 벽돌 수는300/240/180/120/60이며 각 단계는 이전 상태의 엄격한 부분집합이다. 같은 경로를 세 표현에 공통 적용한다.

원본 master260929와 환경ID·T01–T05로 파생되는 경로 seed는 모델 학습seed42/43/44 및 HPO sampler20261111과 구분한다. 동일 환경의 C100은 공유FULL1개이며 경로별 고유 형상5개로 세지 않는다. 기존 C20 MNIDB_0006 T02/T05 중복은 보존하고 고유 형상4개로 보고한다. 제거 이력의 다름이 잔여 형상의 다름을 보장하지 않는다.

## 대응 및 분할

동일 base scenario family의 모든 경로·C·가림·표현은 같은 split에 속한다. 단일 B1 현장을 유지하므로 train/test가 독립 물리 현장이라는 주장은 할 수 없다. 여기서 environment family는 단순 stage 파일명이 아니라 원천 배치·시작/카메라·조명·경로 계보를 공유하는 묶음을 뜻하는 안이며, 최종 정의는 잠금 전 확정한다. 파일명/seed만 다르게 해 독립 표본으로 세지 않는다.

누수는 원천family, 입력hash, 픽셀/Depth/GT, partial occupancy 및 world placement를 구분해 검사한다. C100은 원래 동일한 두 A/B 템플릿이므로 모든 split의 nominal shape를 서로 다르게 만들 수 없다. 이 의도된 공통 템플릿과 사실상 동일 장면의 누수를 구분해야 한다. partial shape 중복이 발생하면 숨기거나 성공할 때까지 seed를 바꾸지 않고 사전 중복 처리 정책을 확정한다. 그 전에는 데이터 QA HOLD다.

## 인식과 모델 선정

P0는 세 표현에 같은 기본 YOLO11n-seg pretrained·AdamW·batch64·640·200epochs·v04 Moderate Augmentation·FP32 box loss/AMP를 적용한다. 추가 탐색 전 기본 lr0=.001,lrf=.1,wd=.0005,warmup3을 유지한다. 실제 v04 RNG는 UL worker에서 seed된 Python random 및 getrandbits 기반 noise generator이며 문서의 per-sample generator와 다르다. 기존 구현은 수정하지 않고 동일 기본 대조군에 적용한다.

현재 L-HPO 선정 설정의 C 전이성은 별도 Train/Val에서 기본 설정과 대조한다. Test/O50/RealTest189는 선정·조기 종료·튜닝에 사용하지 않는다. 자기표현 Validation Mask mAP50–95와 동점 최초epoch 규칙을 사용하고, 공통 설정 비교는 세 표현 동등 가중 평균으로 한다. M50/기존B1/신규C 모델 계보와 checkpoint SHA를 분리한다. seed42만 끝났다면3seed 완료로 표시하지 않는다. P2는43/44 반복과 평균/표본SD다.

## 위치추정과 GT 역할

ORIG_v44, B1ADAPT SENSEDTOP, B1ADAPT PRIORTOP, ROBUST_A를 서로 다른 방법으로 기록한다. GT는 annotation·평가·명시적으로 허용된 fixture QA에만 둔다. GT 잔여Bundle·C정답·정답pose를 운용 인식/pose/controller 입력에 전달하지 않는다. 기존 ROBUST_A의 actual layer_count 입력 의존성은 별도 구조 감사 및 새 C RGB-D 검증 전 미해결이다. 고정 팔레트 두께 .144m는 물체 설계정보이며 적재물 상면의 world z가 아니다.

## 물리 주행과 통계

10base×5C×O0/O25×3표현=300실행, G1 ROBUST_A single observation만 사용한다. G2/G3 재인식은 제외하고 O50는 별도다. 동일base에서 경로·시작·카메라·조명을 대응시킨다.300독립장면으로 해석하지 않고 base/환경의 반복측정 구조를 유지한다. 실제 GT입력 없는 fresh RGB-D FullE2E와 충돌 없는 FINAL·PRE/FINAL 정지인증·QUIET·기존 속도/조향/충돌조건이 필요하다.

과거 성공 기준 .11m/7.34177432289679°와 신규 언급 .10m/5°는 아직 C본실험의 단일 기준으로 확정되지 않았다. 최종 기준 미확정 상태에서는 본주행 금지다. Wilson 구간은 각 분모에 대한 기술적 이항구간으로 제시하되 관련 시행을 독립으로 가정한 효과검정으로 대체하지 않는다. 표현 간 비교는 같은base의 paired outcome과 환경cluster를 고려한다. 비열등성10%p는 미확정이므로 검정/주장하지 않는다. 비유의 차이는 동등성의 증거가 아니다.

48시간은 소요 예산 추정값이지 종료·분모축소·성공처리 조건이 아니다. 모든 실패·중단·HOLD를 버전별로 보존한다. 현재 실행 허가는 준비/기존HPO 감시에 한정되며 신규 GPU작업은 별도 승인 전 시작하지 않는다.
