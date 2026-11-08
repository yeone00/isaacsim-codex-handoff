# B1 NuRec 가시도 QA 규칙 v02 — **LOCKED** (2026-11-08)

> **상태: LOCKED.** 이 파일은 `docs/b1_visibility_qa_rule_v02_LOCK_TEMPLATE_20261106.md`(sha `830c6f7b…a731`)를 복사해 칸을 채운 것이다. 틀 파일과 DRAFT v01은 수정하지 않았다.
> 기계가 읽는 값은 `docs/b1_visibility_qa_thresholds_LOCKED_v02_20261108.json`에 있다.
> 잠근 뒤에는 값을 바꾸지 않는다. 바꾸려면 v03 amendment로 하고 변경 사유를 남긴다.

## 0. 기반 문서(변경 없이 상속)

| 문서 | SHA256 |
|---|---|
| `docs/b1_visibility_qa_rule_DRAFT_20261105_v01.md` (측정 정의 §2, 범주 구조 §3) | `b0f48fd2f29ce7c1176f86a8732062dfcea45c8016957f62c9407b97717299bd` |
| `docs/b1_production_decisions_20261106_v01.md` (H1, C1 승인) | `cfa15a815c009b6565740f3b45c62f7a66cdb7e87cc7de922cef1a22c4ec7eb7` |
| `analysis/b1_train_visibility_qa_20261106_v01.py` (train 지표 계산) | `ea54419f4273f7c62ede40c950724003cedb5244f8ef62dd0dbfd7dc8f8767fa` |

## 1. v01 대비 확정 사항(이미 승인됨)

- **FLAG 처리 H1:** 장면을 삭제하거나 대체하지 않는다. FLAG 열만 기록한다. 분석은 "전체"와 "FLAG 제외"를 함께 보고한다.
- **생성 구성 C1:** 같은 세션에서 I와 E만 렌더하고 O는 렌더하지 않는다. 그래서 production에서 `vis_soft_e2`는 **NOT_COMPUTED**이며, 판정에는 `vis_hard_e2`만 쓴다.
- 측정 정의는 v01 §2와 같다.
  - τ: 99.9 pct, 최소 2, 물체 mask를 15px 팽창한 영역 밖에서 계산
  - 침식: 2px
  - 사용 mask: 실제 표현 load mask

## 2. 임계값(train 결과로만 결정)

| 기호 | 값 | 의미 |
|---|---|---|
| `N_min` | **100** px | `px_e2`가 이 값보다 작으면 LOW_SUPPORT(판정 불가) |
| `T_flag` | **0.90** | `vis_hard_e2`가 이 값보다 작으면 FLAG_NUREC_OCCLUSION |
| `T_watch` | **0.95** | `T_flag ≤ vis_hard_e2 < T_watch`이면 WATCH |

세 값 모두 v01 §4 후보 격자 안에 있다(`T_watch`는 0.95, `T_flag`는 0.90, `N_min`은 100).

## 3. 결정에 사용한 증거

- train capture root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_TRAIN_20261106_v01`
  - 결과 검증 3개 PASS 여부: **PASS**
    - `verify_HR_Scan_v01.json` e5e93094…
    - `verify_LR_Scan_v01.json` 2707bf80…
    - `verify_GeoCAD_v01.json` 8b7ba4b7…
  - pairing PASS 여부: **PASS** (`crossrep_pairing_v01.json` 1624cf1a…, 1000장면, load 쌍 5756개, 위반 0)
- QA 지표 출력 dir: `…/B1_RED_PRODUCTION_TRAIN_20261106_v01/analysis_train_qa_v01/`
  - `b1_visibility_qa_train_metrics_v01.csv` SHA256: `60fae5227ea3baac7b2a0fdca7790931b3fdc07bf9e2ab3402adbb1f72262407`(8907행)
  - `threshold_grid_train_v01.csv` SHA256: `f25b207d51c20bf9d90135e486d94e2ba4891f03e3886079f92c02e3b4da01ec`
  - 근거 집계: `reports/b1_train_production_qa_20261106_v01/threshold_evidence.json` SHA256 `24df4b7dbee6a69800607864baf5278cf0ddb8fb086c8740bcac9bf4cf5055c4`
- train 분포 요약(`vis_hard_e2` 0 / 0.1 / 1 / 5 pct)

  | 표현 | 0 | 0.1 | 1 | 5 | primary Load_01 최소 |
  |---|---:|---:|---:|---:|---:|
  | HR | 0.354 | 0.720 | 0.984 | 0.999 | 0.990 |
  | LR | 0.358 | 0.733 | 0.983 | 0.998 | 0.988 |
  | CAD | 0.387 | 0.742 | 0.974 | 0.998 | 0.995 |

- `px_e2` 분포(전체): 0 / 0.1 / 1 / 5 / 50 pct = 0 / 0 / 1 / 164 / 5313. primary `px_e2`의 최소는 2646이다.
- 표현 간 spread(세 표현 max−min)
  - 크기 100–200px: max 0.102
  - 200–500px: max 0.043
  - 1000px 이상: p99 0.011
- 양성 대조군 R3(진단 pilot, train 장면 TRN_000027)의 `vis_hard_e2`
  - 진단 값: 0.815 / 0.814 / 0.826 (HR/LR/CAD)
  - production에서는 R3 ROI를 쓰지 않으므로 참고로만 쓴다.
- 육안 검토(train 범위만)
  - 검토 장면 목록: **미실행.** 패널 6개는 `reports/b1_train_production_qa_20261106_v01/panel_*.png`에 있다.
  - 검토자: 없음
  - 날짜: 없음
  - AI 판독(R1_NORTH_2 반투명 floater 가림)은 육안 검토로 치지 않는다.

**쓰지 않은 정보:** val/test의 QA 분포(아직 생성 전), 모델 성능(AP/mAP 등), Real Test189.

## 4. 결정 근거

- `N_min = 100`을 고른 이유
  - 기존 canonical 라벨 규칙(canonical_px ≥ 100)과 같은 수준이다.
  - 200을 써도 FLAG scene-load는 10개로 같고, LOW_SUPPORT만 254에서 396행으로 늘어난다.
  - 100–200px에서는 표현 간 spread가 최대 0.10이다. 이 크기대의 FLAG/WATCH는 해석할 때 주의한다.
- `T_flag = 0.90`을 고른 이유
  - R3 대조군(0.814–0.826)을 0.07 이상 여유를 두고 FLAG로 잡는다. 0.80이면 R3를 놓친다.
  - 0.95면 경계 걸침이 5개다. 0.90이면 1개다(TRN_000926 Load_03: 0.927 / 0.861 / 0.864).
- `T_watch = 0.95`를 고른 이유
  - 0.90–0.95 구간을 보고용으로만 따로 표시한다.
  - 0.95 근처의 경계 걸침이 이 구간에 들어간다.
- 선택한 값에서 train FLAG 수
  - 29행, scene-load 10개, base scene 10개이며 모두 보조 load(Load_03/05)다.
  - 표현별로는 HR 9 / LR 10 / CAD 10이다.
  - FLAG scene-load: TRN_000236/3, 000266/3, 000334/3, 000391/3, 000612/3, 000688/5, 000919/3, 000926/3, 000934/3, 001773/5
  - **primary 기준 base-scene FLAG: 0**
  - WATCH: HR 8 / LR 4 / CAD 5
- 선택한 값에서 train LOW_SUPPORT 수
  - HR 117 / LR 113 / CAD 120(합계 350행)
  - 이 중 primary는 0이다.
  - 보고서(2026-11-06)의 254행과 다른 이유
    - 근거 스크립트는 `vis_hard_e2`가 계산되는 행(`px_e2` > 0)이 세 표현에 모두 있는 scene-load만 셌다.
    - 침식 후 0px이 되어 값이 없는 행은 거기서 빠졌다.
    - 그런 행도 규칙상 LOW_SUPPORT이므로 전체 행 기준은 350이다(`threshold_grid_train_v01.csv`와 같다).
    - FLAG와 WATCH 수는 어느 기준으로 세도 같다.

## 5. 적용 규칙(v01 §3 구조 그대로)

1. load 단위 판정 순서: `px_e2 < N_min` → LOW_SUPPORT, `vis_hard_e2 < T_flag` → FLAG_NUREC_OCCLUSION, `vis_hard_e2 < T_watch` → WATCH, 그 외 → OK.
2. base scene 단위: HR/LR/CAD 중 **하나라도** Load_01이 FLAG면 `scene_flag=FLAG`이고, 세 표현 모두에 같은 표시를 붙인다. 그 외는 `scene_flag=OK`다.
3. 출력 파일 `b1_visibility_qa_v02.csv`의 열:
   - scene_id, representation, load_id
   - px, px_e2, tau
   - vis_hard_e2, vis_soft_e2(NOT_COMPUTED)
   - category, scene_flag
4. 적용 순서:
   1. 잠금(§7 기록)
   2. train에 적용
   3. val/test 생성
   4. 같은 규칙으로 val/test에 적용
5. 라벨(YOLO)은 바꾸지 않는다. FLAG는 분석용 별도 열이다(H1).

## 6. 알려진 제한(v01 §6 상속)

- 바닥 접촉 그림자가 약하다(matte FAIL, 보류).
- NuRec depth는 무효다.
- E는 세션 간 비트 단위로 같지 않다.
- C1에서는 soft 지표가 없다. 반투명 가림은 hard 지표에서 과소 또는 과대 평가될 수 있으며, 그 정도는 UNKNOWN이다.
- 공통 canonical label은 NuRec 가림을 반영하지 않는다. 그래서 FLAG load에서는 RGB에서 가려진 부분까지 라벨에 포함된다.

## 7. 잠금 기록

- 잠금 일시: 2026-11-08
- 승인자(연구자)
  - 2026-11-08 지시: "진행 상황 보고하고, 다음단계 바로 진행해"
  - 이 지시는 `reports/b1_train_production_qa_20261106.md`의 제안값(0.90 / 0.95 / 100)과 "승인하면 잠금" 질문에 대한 응답이다. 제안값을 바꾸지 않고 그대로 채택했다.
- 이 LOCKED 파일 SHA256: 파일이 자기 해시를 담을 수 없으므로 PROJECT_STATE 2026-11-08 항목에 기록한다.
- thresholds JSON SHA256: `021c66e9810ec35f08eaa31c6e292729f973993dbb630f03fd43f7f3741bd3e7`
- 이 잠금이 기록된 PROJECT_STATE 항목 날짜: 2026-11-08
