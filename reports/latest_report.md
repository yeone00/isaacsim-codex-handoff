# Real 라벨 보완(R1) 초안 · 사람 검토 패키지 · 평가 정의 일관성 · manifest / 프로토콜 v02 (2026-11-08)

성격: 준비 단계다.
- **39개 본 학습 0, HPO 0, B1 test / Real Test189 추론 0. GPU 학습 0.**
- SAM2.1로 train/val 초안 mask를 만들었다(test는 읽지 않음).
- 원본 Roboflow(CVUT) 이미지·라벨, 기존 split, baseline 9개는 변경하지 않았다. 원본 라벨 폴더 전체 hash가 전후 같다.
- **사람 검토는 PENDING이다.** 자동 초안과 AI 판정은 승인된 라벨이 아니다.

## 요약

| 항목 | 상태 |
|---|---|
| 보완이 필요한 이미지 | **AI 선별로 확인된 79장**(train 58, val 21) + AI 판정이 엇갈린 1장(0415) = Tier A 80장. **정확한 최종 수는 400장 전체를 사람이 검토한 뒤 확정한다**(PENDING). 자동 선별은 음성 65장 중 15장을 놓쳤으므로 Tier B 320장에서 더 나올 수 있다. |
| 초안 | SAM2.1 Base, AI가 확인한 후보 box 기반. **63장, 102개 instance.** Tier A 중 17장은 초안이 없어 사람이 직접 그려야 한다. 초안은 적재 더미의 일부만 덮는 경우가 많아 수정이 필요하다. |
| 저장 | `/home/user/hh/isaac_cosmos/real_benchmark/cvut_real_labels_v02_20261108/`(새 폴더, Git 밖) |
| 사람 검토 패키지 | contact sheet 34장(400장 전부), Tier A 원해상도 겹침 80장, 체크리스트 2개(400행 + 102행, 판정 칸은 비어 있고 PENDING), 검토 가이드 |
| 평가 정의 | Test189은 GT를 바꾸지 않는다. **T-AP / A-AP(독립 보완 GT) / T-ignore / target-centric** 네 관점으로 나눠 평가하도록 설계했다. 주 지표 규칙도 고정했다(§2). |
| manifest / 프로토콜 | 막 목록 v02(구성은 v01과 같고 실제 라벨만 labels_v02), 프로토콜 후보 v02, trainer v07(라벨 승인 게이트), 확정 도구 2개 |
| recipe v04 | 후보는 그대로 유효하다(sha 3f00ab20…, 모듈 sha 일치). `scripts/finalize_lock_20261108_v01.py`로 승인 즉시 LOCKED를 만들 수 있다. |
| 39개 학습 | **준비 완료, 사람 라벨 검토 대기.** 남은 차단 항목: labels_v02 사람 검토 → 확정 → 프로토콜 v02와 recipe v04 LOCKED |

## 1. 실제 라벨 보완(R1)

### 1.1 전체 검토 절차(400장 전부)

| 단계 | 대상 | 방식 |
|---|---|---|
| 0 자동 선별(완료) | 400장 | 색 선별 후보 147개 → AI crop 판정에서 벽돌 102개, 음성 65장 전수 육안 확인 |
| 1 초안(완료) | 후보가 있는 63장 | SAM2.1 box prompt(후보 box를 25% 확장). 원본 대상 영역 제거, 겹치는 초안 병합, 410 px 미만 제거 |
| 2 Tier A 사람 검토(PENDING) | 80장 | 원해상도 겹침으로 초안마다 ACCEPT / EDIT / REJECT / SPLIT, 누락 적재물 추가, 원본 polygon 병합 여부 확인 |
| 3 Tier B 사람 검토(PENDING) | 320장 | contact sheet로 전부 한 번씩 본다. 놓친 적재물이 있으면 Tier A 방식으로 처리 |
| 4 2인 독립 검토(권장) | 400장 | 불일치만 협의하고 기록을 남긴다 |
| 5 확정(PENDING) | — | `scripts/finalize_real_labels_v02_20261108_v01.py`. 체크리스트가 모두 REVIEWED가 아니면 거부한다(지금 실행하면 502행 미완료로 거부, 아무것도 쓰지 않음). 결과: `labels_v02/`, `change_log_final.csv`, `APPROVAL.json`(label set sha, 검토자) |

**라벨 기준(B1 all-load와 같게, `REVIEW_GUIDE.md`)**
- 보이는 팔레트 위 벽돌 적재물을 모두 라벨한다. 팔레트 1개분 = 1 instance다.
- 나란히 놓였거나 2단으로 쌓인 경우 각각 라벨한다. 구분이 안 되면 `GROUP`으로 표시한다.
- 비닐 포장은 포함하고 팔레트는 제외한다.
- 크기 기준은 ≥ 약 410 px(972×1296)이다. B1의 100 px(640×480)에 해당한다. 그보다 작으면 라벨하지 않고 기록만 한다.
- 잘렸거나 가려진 부분은 보이는 부분만 그린다. 빈 팔레트와 낱장 벽돌은 라벨하지 않는다.
- **인접 적재물 병합 확인**: 원본 polygon마다 R2(OK / MERGED_WITH_NEIGHBOUR / BOUNDARY_ERROR / NOT_A_LOAD)를 판정한다. 알려진 사례는 0715이고, 400장 전부에서 확인한다.

### 1.2 초안 결과(`draft_summary.json`)

| | 이미지 | 초안 있는 이미지 | 초안 instance |
|---|---|---|---|
| train | 352 | 42 | 69 |
| val | 48 | 21 | 33 |
| 합계 | 400 | 63 | 102 |

- 초안 면적은 2,819–103,141 px(중앙값 9,599 px)로, 410 px 기준으로 빠진 초안은 없다. 그래도 실제 적재 더미보다 작게 잡히는 경우가 많다. 예를 들어 0403, 0405는 여러 팔레트 더미의 일부만 덮고, 0389는 큰 더미를 놓치고 작은 것만 잡았다. 그러니 **초안은 검토 출발점일 뿐이다.**
- **초안이 없는 Tier A 17장**: 음성 14장, 양성 3장(0715 병합, 0770, 0779). 어둡거나 작은 적재물이라 색 선별이 놓쳤다.
- **AI 판정 불일치 1장(0415)**: crop 판정은 벽돌이었고 전체 이미지 육안 판정은 없음이었다. 사람이 결정한다.
- 원본 라벨 줄은 초안 파일 첫 줄에 바이트 단위로 그대로 복사했다(검사 포함).

### 1.3 산출물

- 새 폴더 `/home/user/hh/isaac_cosmos/real_benchmark/cvut_real_labels_v02_20261108/`
  - `labels_v02_draft/{train,val}/`(400 파일)
  - `draft_instances.csv`, `change_log.csv`(이미지마다 status PENDING_HUMAN_REVIEW)
  - `README_STATUS.md`(DRAFT, 학습과 평가에 사용 금지)
  - `review_pack_v01/`(sheets 34, per_image 80, 체크리스트)
  - 사람 얼굴이 있으므로 **GitHub에 올리지 않는다.**
- Git용 텍스트(이미지 없음, 파일명만): `reports/real_labels_v02_review_20261108_v01/`
  - `REVIEW_GUIDE.md`
  - `review_checklist_images.csv`, `review_checklist_drafts.csv`
  - `change_log.csv`, `draft_summary.json`, `pack_summary.json`
- AI 후보 판정 기록: `reports/real_label_conflict_audit_20261108_v01/ai_colour_candidate_classification.csv`
- 코드
  - `scripts/build_real_labels_v02_draft_20261108_v01.py`
  - `scripts/build_real_label_review_pack_20261108_v01.py`
  - `scripts/finalize_real_labels_v02_20261108_v01.py`

## 2. 평가 라벨 정의 일관성

### 2.1 문제
- B1(학습과 평가)과 보완 후 real train/val은 **all-load** 정의다.
- 기존 Test189 GT는 **target-only**다(이미지당 대상 1개). visual block A1(98장)에는 라벨 없는 배경 더미가 있다.
- GT는 바꾸지 않는다.

### 2.2 네 가지 평가 관점

| 관점 | GT | 배경 load 예측 처리 | 측정하는 것 |
|---|---|---|---|
| **T-AP** | 원본 target-only(변경 없음) | FP | 기존 정의, 기존 결과와 비교 가능 |
| **A-AP** | **Test189-A**(별도 보완 GT, 원본 옆 새 폴더) | 맞으면 TP, 놓치면 FN | B1·학습 정의와 같은 all-load 성능 |
| **T-ignore** | 원본 대상 + Test189-A의 비대상 load를 무시 영역으로 | TP도 FP도 아님 | 대상 성능, 배경 정책에 중립 |
| **target-centric** | 원본 대상 | 무관 | 이미지마다 대상 검출(conf ≥ 0.25, IoU ≥ 0.5)과 대상 pixel IoU |

### 2.3 혼합 비율 비교에 생기는 편향
- **T-AP만 쓰면** 배경 적재물까지 찾는 모델이 FP로 감점된다.
  - labels_v02로 학습한 모델(실제 비중이 클수록 all-load 신호가 강함)과 합성 비중이 큰 모델(B1 all-load)이 모두 불리하다.
  - 원본 라벨 시절에는 오히려 target-only 정책을 배운 실제 위주 모델이 유리했다. 즉 T-AP의 편향 방향은 **학습 라벨 정책에 따라 바뀐다.** 비율 효과로 해석하면 안 된다.
- **A-AP만 쓰면** 멀고 작은 배경 더미의 recall이 크게 작용한다. 작은 물체에 강한 모델(해상도, 실제 데이터 양)이 유리하다. 대상 1개만 중요한 작업 관점과는 다르다.
- **T-ignore와 target-centric**은 배경 정책에 중립이다. 대신 배경 적재물 인식 능력은 평가하지 않는다.
- **real val 선정(A 정의)**은 all-load 쪽으로 checkpoint를 고른다. Test189 T-AP와 같이 쓰면 정의 불일치로 실제 위주 모델이 체계적으로 감점될 수 있다.
- **결론**: 비율 비교의 주 지표는 정의가 학습과 같은 **A-AP**(Test189-A가 승인되면)로 한다. 그렇지 않으면 정책 중립적인 **target-centric**을 쓴다. T-AP는 기존 결과와의 연결용 보조 지표다. 네 관점을 모두 보고하고, 관점에 따라 순위가 바뀌면 그 사실을 결과로 보고한다. 이 규칙은 프로토콜 v02 후보에 미리 고정했다.

### 2.4 Test189-A(보완 GT) 구축 절차(설계만, 실행 안 함)
1. **모델 예측 차단**
   - 구축하는 동안 B1, 혼합, 기존 M50 등 **어떤 학습 모델의 Test189 추론도 하지 않는다.**
   - 기존 Test189 예측 산출물(`real_test189_eight_model_common_eval_v01/runs`)도 검토자에게 주지 않는다.
2. **초안**
   - 원본 대상 polygon은 그대로 둔다.
   - 비대상 적재물은 사람이 직접 박스를 그리고 SAM2.1이 mask를 제안한다(범용 분할기이고 평가 대상 모델이 아님).
   - 색 선별 같은 비학습 자동 후보는 쓸 수 있지만 사람 판정이 필요하다.
3. **검수**
   - 검토자 2명이 독립으로 R1/R2를 판정하고 불일치만 협의한다. train/val과 같은 가이드를 쓴다.
   - 대상 polygon의 병합 오류는 기록만 한다. 원본은 고치지 않는다.
4. **확정**
   - `labels_test189A/` + `APPROVAL_test189A.json`(sha, 검토자, 날짜)을 만든다. 원본 `yolo_real_v01/labels/test`는 변경하지 않는다.
   - Test189-A sha는 **test 실행 전에** test LOCK v02에 고정한다.
5. **순서**: Test189-A 승인과 LOCK이 끝난 뒤에만 모델 추론을 한다. 승인이 늦어지면 Test189-A 없이 target-centric을 주 지표로 하는 규칙을 그대로 적용한다.

## 3. checkpoint 규칙(연구자 채택)

- **Q2(혼합 비율)와 Q3–Q5**
  - 모든 혼합 모델(100:0과 0:100 포함)에 **best_combined**를 쓴다.
  - 0.5 × (B1 자기 표현 val + real val **labels_v02**) mask mAP50-95가 최대인 epoch, 동점이면 이른 epoch다.
  - 최종 잠금은 real val 라벨 승인 뒤에 한다.
- **Q1(증강 효과)**: 기존 baseline과 같은 **B1 val best**로 양쪽을 비교한다.
- 서로 다른 규칙의 결과를 같은 비교로 다루지 않는다. 보조 checkpoint는 별도 표로 보고하고, test 결과로 다시 고르지 않는다(프로토콜 후보 v02의 `checkpoint_rule`).

## 4. manifest · 프로토콜 · recipe

- **막 목록 v02**
  - 경로: `reports/mixing_design_20261108_v02/manifests/A1000_*_v02.csv` + 요약
  - 생성: `scripts/build_mixing_manifests_20261108_v02.py`
  - 구성(포함 이미지, 순서, 반복)은 v01 A1000과 같다.
  - 합성 1000 / 750 / 500 / 250 / 0, 실제 항목 0 / 250 / 500 / 750 / 1000, 실제 고유 0 / 250 / 352 / 352 / 352, 최대 반복 — / 1 / 2 / 3 / 3
  - 실제 양성 / 음성은 labels_v02 승인 후 다시 계산한다. 초안 기준으로는 50:50에서 양성 441 / 음성 59다(원본 기준 407 / 93).
- **실제 라벨용 데이터 view와 trainer**
  - `scripts/b1_real_labels_v02_view_20261108_v01.py`: labels_v02 + `APPROVAL.json` sha가 맞아야 통과한다. draft는 SMOKE에서만 허용한다.
  - `scripts/train_b1_yolo_20261108_v07.py`: v06 + 라벨 게이트 + 프로토콜 LOCKED v02 요구 + 라벨 hash 전후 비교
  - 정적 검사와 게이트 동작을 확인했다(draft를 비SMOKE로 쓰면 거부, SMOKE로 쓰면 1000 = 500 + 500 구성). **GPU smoke는 아직 하지 않았다**(v06 smoke PASS 이후 바뀐 것은 데이터 view뿐이다). 승인된 라벨이 나오면 3 epoch smoke 1회를 권한다.
- **프로토콜 후보 v02**: `docs/b1_mixing_experiment_protocol_LOCK_CANDIDATE_v02_20261108.{json,md}`(sha ad6baa88…). status는 LOCK_CANDIDATE_PENDING_LABEL_REVIEW이고 labels_v02 sha는 TBD다.
- **recipe v04**: 후보 그대로다. 증강 검증과 smoke로 확인한 내용이다.
  - 승인 시: `python scripts/finalize_lock_20261108_v01.py --candidate docs/b1_yolo_recipe_LOCK_CANDIDATE_v04_20261108.json --approved-by "<연구자>"`
  - 이 도구는 status와 approval 말고 다른 내용이 바뀌면 거부한다.

## 5. 39개 학습 준비 상태와 남은 순서

1. **[PENDING · 사람]** labels_v02 검토: Tier A 80장(편집), Tier B 320장(확인), 가능하면 2인
2. `finalize_real_labels_v02` 실행 → `labels_v02` + `APPROVAL.json`
3. 프로토콜 v02에 label sha와 실제 양성 / 음성 수를 채운다 → 연구자 승인 → LOCKED. recipe v04도 LOCKED.
4. trainer v07 3 epoch smoke(승인된 라벨, 50:50 HR seed 42)
5. 39 run(증강 100:0 9 → 혼합 27 → 실제만 3), 약 10시간. PASS일 때만 진행한다.
6. val 평가(B1 val 3×3, real val A/T)
7. (별도) Test189-A 구축과 승인 → test LOCK v02 → test 1회

- B1 test와 Test189은 이번에 실행하지 않았다.
- 사람 QA(B1 FLAG, real labels_v02, Test189-A)는 모두 PENDING이다.

## 파일

- 신규 코드
  - `scripts/build_real_labels_v02_draft_20261108_v01.py`
  - `scripts/build_real_label_review_pack_20261108_v01.py`
  - `scripts/finalize_real_labels_v02_20261108_v01.py`
  - `scripts/finalize_lock_20261108_v01.py`
  - `scripts/build_mixing_manifests_20261108_v02.py`
  - `scripts/b1_real_labels_v02_view_20261108_v01.py`
  - `scripts/train_b1_yolo_20261108_v07.py`
- 신규 문서: `docs/b1_mixing_experiment_protocol_LOCK_CANDIDATE_v02_20261108.{json,md}`
- 첨부
  - `reports/real_labels_v02_review_20261108_v01/`(가이드, 체크리스트, 변경 이력, 텍스트만)
  - `reports/mixing_design_20261108_v02/manifests/`
  - `reports/real_label_conflict_audit_20261108_v01/ai_colour_candidate_classification.csv`
- Git 밖: `/home/user/hh/isaac_cosmos/real_benchmark/cvut_real_labels_v02_20261108/`(초안 라벨, 검토 이미지)
- 변경 없음: `yolo_real_v01` 이미지·라벨(전체 hash 전후 동일), split, baseline 9개, recipe v01–v03, v04 후보, 기존 막 목록 v01, 프로토콜 후보 v01, Test LOCK 후보
