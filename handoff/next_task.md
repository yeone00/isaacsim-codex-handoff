# Full E2E v02 — stopping/hold 설계 결정 (사용자 승인 후 1회 실행)

상태: READY_FOR_MANUAL_APPROVAL
대상: /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013
목적: 실제 Isaac Sim stopping validation 실패를 바탕으로, 다음 engineering 단계의 실행 가능성을 구체적으로 결정한다.

시작할 때 AGENTS.md, docs/PROJECT_STATE.md, reports/full_e2e_v02_stopping_adapter_actual_validation_20261019_v01.md 및 이전 stopping adapter 보고서를 읽어라.

확인된 관측:
- DriveContract wire_per_surface=0.250626563945 확정.
- 새 stopping adapter 실제 단일 probe의 root/FD peak=0.0228053/0.0212797m/s로 phase cap 통과.
- 첫 zero 후 34.1273mm 후퇴, 마지막 1s raw root peak=0.002619m/s로 quiet fail.
- wheel dq=0과 pose span=0이 관측됐으나 root quiet는 실패. 실제 FINAL/ENG001 주행은 미실행.
- 이전 nominal FINAL margin 5.12mm longitudinal/4.58mm lateral; 예측만으로 task success 선언 불가.

이번 작업에서:
1. 기존 로그와 현재 rover USD/ActionGraph/Articulation의 실제 actuator 제어 기능만 점검해 zero wheel velocity target, wheel hold/braking 가능성, steering target 복귀, stopped pose 유지/계측 차이를 분리하라.
2. 실제 지원되지 않는 brake 또는 비홀로노믹 position hold를 가정하지 마라. root raw speed quiet fail을 단순 수치 완화로 처리하지 마라.
3. 현재 모델을 보존하면서 적용할 수 있는 최소 변경 후보를 1개 선정하고 (a) 구현 가능한 actuator interface, (b) 제어 입력/출력, (c) fail-safe 및 latch, (d) 다음 단일 실제 시험의 GO/NO-GO 기준을 작성하라. 구현이 불가능하면 근거와 명확한 대안을 제시하라.
4. 신규 제어 알고리즘을 도입한다면 동료심사 논문 또는 공식 기술보고서의 실제 출처를 제시하고, 해당 문헌에서 무엇이 검증됐고 우리 adapter의 어떤 부분은 아직 미검증인지 구분하라.
5. 1개의 간결한 결정 보고서를 reports/full_e2e_v02_stop_hold_design_decision_20261019_v01.md 로 작성하고 docs/PROJECT_STATE.md를 갱신하라. 기존 산출물은 보존하라.

금지:
- Isaac Sim/ROS 구동·추가 calibration·재시도·ENG001·QUAL12·432-run
- frozen controller, original USD, protocol, governor 기본 파라미터 변경
- 미검증 감속거리 보증, threshold/cap 완화, 무제한 추가 분석

마지막 완료 메시지에는 확정된 결론, 다음 1개 실험 승인 조건, 실제 생성한 보고서 경로를 짧게 적어라.
보고서를 생성/갱신한 경우에 한해 최종 줄에 다음 마커를 정확히 출력하라:
HANDOFF_REPORT: reports/full_e2e_v02_stop_hold_design_decision_20261019_v01.md
