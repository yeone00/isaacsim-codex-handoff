# C 데이터 전용 공통 HPO 계획 개정분 — 2026-11-11

이 문서는 기존 C_DEPLETION_REBUILD 지시·방법론·실행 제한을 유지하면서 HPO 부분만 개정한다. 기존 잠금이나 실행 중인 코드를 수정하지 않는다. 계획 개정이며 신규 GPU 실행 승인이 아니다. PREPARATION_ONLY/HOLD는 유지한다.

## 대체되는 내용

기존 방법론/데이터 계획에서 「L-HPO 선정값과 기본값의 C 전이 대조를 보조로 수행」하던 부분을 **새 C 데이터에서 별도의 공통 HPO를 필수 수행**하는 계획으로 대체한다. 현재 B1 L1–L4 HPO는 그대로 완료하고 예비 탐색으로 보존한다. L-HPO가 새 C에 최적이라는 가정은 하지 않는다. 다른 데이터·QA·안전·300회·통계·GT·승인 조건은 변경하지 않는다.

## 변경된 단계 순서

기존 L-HPO 완료/보존 → C 데이터 생성·QA·family 단위 Train/Val/Test 분할 및 manifest 잠금 → **C 전용 공통 HPO** → 최종 공통 설정/모델 고정 및 seed 반복 → 인식 평가 → 위치추정/ROBUST_A 검증 → 기술 파일럿 → G1 300회 주행.

현재 Controller의 `C_training_evaluation`은 상위 단계명으로 유지하며, 계획상 내부를 `C_COMMON_HPO → C_FINAL_MODEL_TRAINING → C_PERCEPTION_EVALUATION`으로 확장한다. 실행 중인 Controller/Watchdog는 재시작하거나 고치지 않는다. 실제 후속 GPU adapter는 아직 구현/승인되지 않았으며, 새 실행 버전에서 이 순서를 반영해야 한다. HPO 완료만으로 현재 HOLD가 풀리지 않는다.

## C-HPO 별도 예산안

아래는 C 데이터 QA 및 실제 처리속도 확인 후 **학습 시작 전에 고정할 DRAFT 예산**이다. 이번에 후보 생성이나 학습을 시작하지 않는다.

| 단계 | 후보·표현·seed | 예산 |
| --- | --- | --- |
| Qualification | 기본 설정,3표현,seed42,2epoch;200epoch schedule | 3run/6 model-epochs,선정 제외 |
| 초기 탐색 | 총12후보×3표현×seed42×60epoch | 36run/2160 model-epochs |
| 충분한 학습 비교 | 상위 비기본3후보+기본×3표현×200epoch | 최대12run/2400 model-epochs |
| 최종 seed 반복 | 선정 공통 설정×3표현×seed43/44×200epoch | 6run/1200 model-epochs |

총 최대57개 학습run/5766 model-epochs다. 선정된200epoch seed42 세 모델은 artifact·checkpoint 검증 후 최종 seed42 모델로 고정할 수 있어 불필요한 재학습을 피한다. 최종 모델은3표현×3seed=9개이며 seed42는 탐색과 겹친다는 선택 편향을 명시한다. 이 재사용이 허용되지 않는 조건 변화가 있으면 별도 사전 개정 없이 학습을 추가하지 않는다. 기본 설정의43/44 대조를 추가하려면 별도6run/1200epoch 예산으로 잠그며 Test 결과를 근거로 추가하지 않는다.

12후보는 기본 설정1개 + 완료된 L-HPO의200epoch 자기표현 Val 공통점수 기준 상위 비기본 후보 최대3개 + 새 Random Search 최소8개로 구성하는 안이다. L 후보가 미완료/실패/중복이면 새 random 후보로 채워 **총12개를 유지**한다. L 후보의 가중치가 아니라 파라미터만 가져온다. 모든 C 학습은 동일 pretrained에서 새로 시작하고, L-HPO나 기존 M50/B1 checkpoint를 이어 학습하지 않는다. 최종 L 결과와 C manifest 잠금 후 실제 후보 목록·출처·hash를 고정한다.

작은 예산에서 TPE 우월성을 가정하지 않고 Optuna RandomSampler를 제안한다. 별도 sampler seed는20261112, 학습 seed42/43/44, 제거 master260929와 환경×T 파생 seed는 서로 다른 역할로 기록한다. 새 후보는lr0 .0002–.003(log),weight_decay .00001–.002(log),lrf .05–.25,warmup1–5에서 생성한다. 기본값은 .001/.0005/.1/3이다. 나머지 YOLO11n-seg·AdamW·batch64·640·200epoch·mask_ratio4·v04 Moderate Augmentation·FP32 box loss·AMP·실제 photometric RNG는 기존과 동일하게 유지한다.

60epoch는200epoch 학습률 일정을 유지한 단축 비교다. 상위 후보의200epoch 비교는 다시 pretrained에서 시작한다. 단축 성능이 최종 성능을 보장하지 않으며 late improver를 놓칠 수 있다는 예산 한계를 보고한다. 실패 triplet은 세 표현 중 둘만 평균해 선정하지 않고 실패로 보존한다. 동점 후보는 사전 ID 순서(기본 우선), checkpoint 동점은 기존 strict-greater/최초epoch 규칙을 유지하는 안이다.

## 목적함수와 모델 선정

각 후보는 HR/LR/CAD에 동일 파라미터를 적용한다. 주 점수는 `(HR 자기표현 C-Val Mask mAP50–95 + LR 자기표현 C-Val Mask mAP50–95 + CAD 자기표현 C-Val Mask mAP50–95)/3`이다. C별 성능과 특정 표현의 저하를 별도 보고한다. 교차표현 Val는 보조 지표다. 세 표현의 고정 Val 전체에서 계산한 mAP는 C5개를 단순히 같은 가중치로 평균한 값과 같지 않으므로 Val의 C별 실제 분모를 공개한다. 목적함수나 층화 가중치를 바꾸려면 탐색 전에 별도 잠금이 필요하다.

새 C Test, O0/O25/O50 Test, Real Test189 및 기존 주행 성능은 후보 추가·선정·조기 종료에 사용하지 않는다. C-HPO 완료 후 공통 설정을 불변 selection lock으로 고정하고 최종 모델 lineage/checkpoint SHA를 고정한다. 이후 인식 Test와 pose/주행을 수행하며 Test 결과로 재선정하지 않는다. M50/기존 B1/L-HPO/신규 C-HPO 모델을 구분한다.

## 유지되는 HOLD와 자동화

기존 Controller/Watchdog/systemd/ntfy/GitHub 동기화는 유지한다. 현재 계획 개정 파일은 실행 허가를 부여하지 않는다. C dataset/GT QA, 분할·중복 처리 정책, ROBUST_A의 GT 비사용 호환성, 단일 성공 기준, 기술 파일럿 등 기존 gate는 전부 그대로다. 300회는10base×5C×2O×3표현이며 O50는 별도다. 48시간은 강제 종료 조건이 아니다.

향후 소요시간에는 C-HPO의 별도 예산을 추가해야 한다. 현재 L-HPO에서 측정한 약4초/epoch를 단순 적용하면5766epoch는약6.4시간이고 시작·검증·교차Val 비용은 추가된다. 신규 C 데이터 규모/처리속도가 달라 아직 정확한 ETA는 아니다. 이전 「기본 학습·전이 대조만」을 가정한 전체시간 추정은 C-HPO를 반영해 후속 갱신해야 한다.
