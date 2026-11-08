# B1 QA v02 잠금 · train 적용 · val/test 생성 · YOLO 패키지 (2026-11-08)

성격: production. 학습 0, v42 GPU 재현 0. 모델 성능과 Real Test189는 사용하지 않았다.

13:40 중간 보고 뒤, 15:20에 §3, §5, §6의 결과를 추가했다.

## 1. QA v02 잠금 — 완료

- 승인 근거: 연구자 지시 "진행 상황 보고하고, 다음단계 바로 진행해"(2026-11-08). 11-06 제안값을 바꾸지 않고 채택했다.
- 규칙 문서: `docs/b1_visibility_qa_rule_LOCKED_v02_20261108.md` — sha `985d8696…4407`(PROJECT_STATE에 기록)
- 값 파일: `docs/b1_visibility_qa_thresholds_LOCKED_v02_20261108.json` — sha `021c66e9…d3e7`

| 기호 | 값 |
|---|---|
| `N_min` | 100 px |
| `T_flag` | 0.90 |
| `T_watch` | 0.95 |

틀(TEMPLATE)과 DRAFT v01은 수정하지 않았다. 사람 육안 검토는 아직 하지 않았다(잠금 문서 §3에 미실행으로 기록).

## 2. train 적용 — 완료

- 실행 스크립트: `analysis/b1_apply_visibility_qa_v02_20261108_v01.py`
  - 잠금 JSON과 입력 지표 CSV의 sha가 일치해야 실행된다.
  - 기존 출력은 덮어쓰지 않고 새 dir에 쓴다.
- 결과 파일: `…/B1_RED_PRODUCTION_TRAIN_20261106_v01/qa_v02_train_v01/b1_visibility_qa_v02.csv`(sha 86e30fa7…, 8907행)

| 표현 | OK | WATCH | FLAG | LOW_SUPPORT |
|---|---:|---:|---:|---:|
| HR | 2835 | 8 | 9 | 117 |
| LR | 2842 | 4 | 10 | 113 |
| CAD | 2834 | 5 | 10 | 120 |

- FLAG는 scene-load 10개이고 모두 보조 load다. **scene_flag=FLAG인 base scene은 0개다.**
- primary LOW_SUPPORT는 0행이다.
- 정정: 11-06 보고서의 LOW_SUPPORT 254는 침식 후 0px이라 값이 없는 행을 뺀 수였다. 규칙대로 행 단위로 세면 350이다. FLAG와 WATCH 수는 어느 쪽으로 세도 같다.

## 3. val/test 생성 — **PASS**(13:35–15:09 KST)

- driver: `scripts/run_b1_valtest_production_20261108_v01.sh`
  - train driver와 달라진 것은 root, N=400, `--splits val test` 세 가지뿐이다.
- root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_VALTEST_20261108_v01`

| 표현 | result | 장면 PASS/FAIL | load | 소요 | verify |
|---|---|---|---:|---:|---|
| HR(+canonical) | PASS_CAPTURE | 400 / 0 | 1198 | 38.9분 | **PASS** (5842034b…) |
| LR | PASS_CAPTURE | 400 / 0 | 1198 | 26.7분 | **PASS** (542dd65c…) |
| CAD | PASS_CAPTURE | 400 / 0 | 1198 | 27.9분 | **PASS** (e152c8cd…) |

- renderer `[Error]`는 0줄이다.
- pairing `crossrep_pairing_v01.json`(0c3c2f99…): **PASS.** 공통 장면 400개, load 쌍 2324개.
- FAIL이 없어서 resume은 필요 없었다. 분모는 400 × 3이다. 판정은 결과 파일로 했다.

## 4. 다음 단계용 도구 — 준비됨

- `analysis/b1_visibility_qa_metrics_20261108_v02.py`
  - train 전용이던 v01을 복사하고, 잠금 sha를 확인한 뒤에만 val/test를 허용하도록 바꿨다.
  - 지표 코드는 그대로다.
  - 동일성 확인: train capture에 v02를 다시 돌렸다. 결과 CSV가 v01 CSV(60fae522…)와 **바이트 단위로 같았다**(`cmp` IDENTICAL).
- `scripts/export_b1_yolo_20261108_v03.py`
  - 표현별로 train root와 val/test root를 함께 받는다. 중복 scene은 거부한다.
  - 라벨 정책은 v02와 같다.
  - train smoke(scratchpad): 2969 instance, 빈 라벨 0, min polygon IoU 0.966(작은 load에서 xor 최대 30px). val/test가 없으므로 PARTIAL이며 data.yaml은 만들지 않았다.
  - 중복 root 음성 대조군: 거부 확인

## 5. val/test에 QA v02 적용 — 완료(잠긴 값 그대로)

- 지표: `…/B1_RED_PRODUCTION_VALTEST_20261108_v01/analysis_valtest_qa_v01/b1_visibility_qa_metrics_v02.csv`(705531e6…, 3594행)
- 판정: `…/qa_v02_valtest_v01/b1_visibility_qa_v02.csv`(b2c0600d…)

| 표현 | OK | WATCH | FLAG | LOW_SUPPORT |
|---|---:|---:|---:|---:|
| HR | 1141 | 6 | 7 | 44 |
| LR | 1144 | 5 | 8 | 41 |
| CAD | 1141 | 7 | 6 | 44 |

- split별로는 val FLAG 11행, test FLAG 10행이다.
- FLAG는 scene-load 8개이고 모두 보조 load(Load_03/05)다. **scene_flag=FLAG인 base scene은 0개다.** primary 최소는 0.988이다.
- 가장 낮은 값은 TST_000392 Load_03(0.476 / 0.468 / 0.465)이다. 세 표현이 거의 같다.
- 경계 걸침 2건
  - VAL_000148 Load_03: HR 0.878 / LR 0.851은 FLAG이고, CAD는 0.902로 WATCH다.
  - TST_000188 Load_05: LR만 FLAG(0.871, `px_e2` 132)다. HR과 CAD는 `px_e2`가 90과 80이라 LOW_SUPPORT다. N_min 근처의 작은 load라서 생긴 차이다.
- 이 결과를 보고 임계값을 바꾸지 않았다.

## 6. YOLO 패키지 — **PASS_PACKAGE_COMPLETE**(학습 0)

- root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_YOLO_PACKAGE_20261108_v01`(symlink만 사용, 원본 복사나 수정 없음)
- 생성 스크립트: `scripts/export_b1_yolo_20261108_v03.py`, `package_checks.json` 3ff0a45e…
- 구성: 표현마다 train 1000 / val 200 / test 200 이미지이고, 같은 수의 라벨이 있다.
- 깨진 symlink는 0개다.
- 라벨
  - 4167 instance(train 2969 + val/test 1198), 빈 라벨 장면 0
  - min polygon IoU 0.960, xor 최대 30px(작은 load)
  - class0 `brick_load`, 공통 HR canonical
- `data.yaml` 3개(HR 6e5d2484…, LR 9779cf1a…, CAD aeb24e49…)
- QA FLAG는 라벨에 반영하지 않는다(H1). 분석할 때 위 두 QA CSV를 scene_id와 load_id로 붙여서 쓴다.

## 남은 순서

1. ~~val/test verify와 pairing~~ 완료
2. ~~잠긴 QA를 val/test에 적용~~ 완료
3. ~~export v03으로 data.yaml을 갖춘 패키지 생성~~ 완료
4. 다음 결정(연구자): YOLO 학습 recipe와 실행 승인, v42 GPU 재현 승인, 패널 육안 검토 여부
5. **YOLO 학습과 v42 GPU 재현은 별도 승인 전까지 하지 않는다.**
