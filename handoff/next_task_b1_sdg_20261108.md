# NEXT TASK (B1 SDG track) — 2026-11-08 · Claude Code 작성

> 이 파일은 `next_task_b1_sdg_20261106.md` 이후의 B1 트랙 상태다. 11-06 파일은 이력으로 남겨 둔다.
> 로봇 트랙 `handoff/next_task.md`(v48)와는 별개다. 두 트랙은 같은 연구 repo와 `docs/PROJECT_STATE.md`를 공유하며, 한 번에 한 세션만 쓴다.

## 완료(2026-11-08까지, 결과 파일 검증)

- train 1000 / val 200 / test 200 × HR / LR / CAD 생성
  - 각 표현의 verify PASS, crossrep pairing PASS, FAIL 0
  - roots: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_TRAIN_20261106_v01`, `…/B1_RED_PRODUCTION_VALTEST_20261108_v01`
- QA v02 **LOCKED**: N_min 100, T_flag 0.90, T_watch 0.95
  - 규칙 문서 sha `985d8696…4407`, 값 파일 sha `021c66e9…d3e7`
  - 사본: `handoff/b1_locked_docs/`
  - train과 val/test 모두 적용했다. scene_flag=FLAG인 base scene은 0개이고, FLAG는 보조 load만 해당한다(train 10, val/test 8 scene-load).
- YOLO 패키지: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_YOLO_PACKAGE_20261108_v01`
  - PASS_PACKAGE_COMPLETE, data.yaml 3개, 4167 instance
- 보고서: `reports/b1_qa_v02_lock_and_valtest_20261108.md`

## 현재 지시(연구자, 2026-11-08)

1. v42 GPU 재현 실험 2개(승인됨)
   - (a) 실제 gradient accumulation 조건에서 optimizer step이 정상적으로 증가하는지
   - (b) Ray checkpoint 복원 후 optimizer step이 추가로 증가하고 가중치가 갱신되는지
   - 판정은 로그와 checkpoint로 한다.
   - 실패하면 원인만 분석한다. 임의로 설정을 바꾸거나 재시도를 반복하지 않는다.
2. 사람 QA 검토용 패널과 체크리스트 준비
   - 포함할 것: 모든 FLAG, VAL_000148, TST_000188, LOW_SUPPORT 표본, 정상 primary 표본
   - 승인 칸은 비워 둔다. AI 검토를 사람 검토로 치지 않는다.
3. HR / LR / CAD 공통 YOLO 학습 recipe 작성
   - baseline을 고정 설정으로 먼저 하고, HPO는 별도 단계로 둔다.
   - Test는 모델 선정이나 하이퍼파라미터 조정에 쓰지 않는다.
   - **학습과 HPO는 아직 시작하지 않는다.**

## 금지·주의

- 원본 USD, 브릭, manifest(sha 56c8acbb…), split, QA 기준, 라벨, 기존 출력을 변경하지 않는다.
- Real Test189는 쓰지 않는다. 실패 로그는 보존한다.
