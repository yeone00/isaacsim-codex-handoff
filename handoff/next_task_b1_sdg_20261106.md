# NEXT TASK (B1 SDG track) — 2026-11-06 · Claude Code 작성 DRAFT

> 이 파일은 **B1 합성데이터 트랙** 전용 지시서다. 로봇 트랙 `handoff/next_task.md`(v48, 미실행)는 그대로 유효하며, 이 파일이 그것을 대체하지 않는다.
> 두 트랙은 같은 연구 repo와 `docs/PROJECT_STATE.md`를 공유한다. 한 번에 한 세션만 쓴다.

## 현재 상태(2026-11-06 기준)

- 승인된 결정: `docs/b1_production_decisions_20261106_v01.md`
  - FLAG 처리 **H1**: 모든 장면 유지, FLAG 열만 기록
  - 구성 **C1**: 같은 세션에서 RGB와 빈 배경 렌더, HR은 canonical 포함
- 실행 중: train 1000장면 × HR/LR/CAD 생성
  - root: `/home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_TRAIN_20261106_v01`
  - driver: `scripts/run_b1_train_production_20261106_v01.sh`
  - 판정: 표현별 `verify_*_v01.json`과 `crossrep_pairing_v01.json`. exit code로는 판정하지 않는다.
- QA 규칙
  - 측정 정의: `docs/b1_visibility_qa_rule_DRAFT_20261105_v01.md`
  - 잠금 틀: `docs/b1_visibility_qa_rule_v02_LOCK_TEMPLATE_20261106.md`, `docs/b1_visibility_qa_thresholds_v02_TEMPLATE_20261106.json`
  - 임계값은 아직 없다.
- 준비된 도구(pilot으로 smoke PASS)
  - `analysis/b1_train_visibility_qa_20261106_v01.py`: train 전용, 임계값 미적용
  - `scripts/export_b1_yolo_20261106_v02.py`
    - 공통 HR canonical label, class0 `brick_load`, 100px 이상
    - train·val·test가 모두 있어야 data.yaml을 만든다.
- 최신 보고서: `reports/b1_nurec_visibility_3rep_and_production_pilot_20261105.md`

## 다음 순서(각 단계는 연구자 승인 후)

1. train 생성 결과를 확인한다.
   - 3개 verify와 pairing이 모두 PASS여야 다음 단계로 간다.
   - FAIL이면 멈추고 보고한다. 재시도는 `RESUME=1`로만 하고, 실패 기록은 보존한다.
2. train QA 지표를 계산한다.
   - 분포와 임계값 격자 표를 연구자에게 보고한다.
   - 연구자가 `N_min`, `T_flag`, `T_watch`를 고른다.
   - 고른 값을 LOCKED v02 새 파일로 잠그고 SHA를 기록한다.
3. 잠긴 QA를 train에 적용해 `b1_visibility_qa_v02.csv`를 만든다.
4. val/test(200+200) × 3표현을 같은 v03 엔트리포인트와 검증기로 생성한다. 같은 규칙을 적용한다.
5. YOLO export v02로 패키지를 만든다(data.yaml 생성).
   - **YOLO 학습은 별도 승인 전까지 하지 않는다.**

## 금지·주의

- 원본 USD, 브릭, `red_only_manifest_1400_v03.csv`(sha 56c8acbb…), split을 변경하지 않는다.
- 기존 출력을 덮어쓰지 않는다.
- val/test QA 분포는 v02 잠금 전에 열지 않는다. 모델 성능으로 임계값을 정하지 않는다. Real Test189를 쓰지 않는다.
- matte나 그림자 합성은 보류한다. 바닥 접촉 그림자 약함은 알려진 제한이다.
- PROJECT_STATE가 append로 SHA가 바뀌었다. 그래서 이 문서를 hash-gate하는 구 스크립트는 멈춘다. 기대 해시를 수정하지 말고, 제외 처리한 새 버전을 쓴다.
- Isaac 실행 중에는 GPU를 쓰는 다른 작업(로봇 트랙 Kit 포함)을 동시에 띄우지 않는다.
