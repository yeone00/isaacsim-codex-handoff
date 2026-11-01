# 현장 perception → PRE → FINAL v17 — 2026-11-01

**전체 NOT_READY. 실제 PRE 도착 NO, FINAL 도착 NO.** 기존 v16b를 수정 없이 새 출력에서 Kit 1회 실행했다. 새 RGB-D·YOLO·B4·수동 ROI B5와 PRE 경로 안전 검사는 PASS였지만 실측 경로 약0.680m 뒤 TF_STALE로 차단됐다. PRE 잔여0.201629488m이며 FINAL 경로 검사·주행은 NOT_RUN이다. Cleanup 영수증과 소유 프로세스 정상 종료는 PASS, 주행 후 물리 quiet 인증은 FAIL이다. 원인이 특정된 국소 소프트웨어 수정이 없어 추가 Kit 실행을 하지 않았다. Retry0, HPO/training PAUSED, 연구 denominator0, 대규모 과학 실행0.

## 재사용과 실행 전 검사

README·PROJECT_STATE의 최신 v16 기록·PROTOCOL_LOCKS·v16 보고서와 v16b runner/session/observer를 읽었다. v16b 즉시 TF snapshot, 기존 v16 driver의 알려진 steering adapter, v14 curved follower, v15 graph invariant, 기존 EndpointGuard/StoppingAdapter 및 충돌·속도·정지 한계를 그대로 사용했다. 새 runner나 follower를 만들지 않았고 실행 소스 수정0이다. TF wall≤0.5초/sim차≤0.1초, ROS identity/GID, 매 tick graph/actor 검사 및 fsync를 유지했다.

- `python3 -m py_compile`: runner/session/observer v16b, driver v16, TF helper v16b, IO helper v16의 6개 PASS.
- `analysis/construction_site_tf_snapshot_test_20261101_v16b.py`: 4/4 PASS.
- `analysis/construction_site_io_test_20261101_v16.py`: 5/5 PASS.
- `analysis/construction_site_graph_test_20261101_v15.py`: allow/reject 5개 PASS.
- prepare geometry/corridor PASS, resource/GPU/domain isolation PASS. 설치·업그레이드 없음.

새 외부 출력 root:
`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v17_01`

정확한 명령:
```bash
python3 scripts/construction_site_perception_runner_20261101_v16b.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v17_01
/home/user/anaconda3/bin/python3 scripts/construction_site_perception_runner_20261101_v16b.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v17_01
```

실제 Kit Python은 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, Isaac Sim5.1, ROS jazzy/domain191이다. Perception은 기존 sdg_tools Python이다. 초기 overlay 배치는 v14b 그대로이며 실행 중 teleport/원본 USD 변경은 없다. `prepare.json`, `code_versions.json`, `executed_code/`가 입력 경로·hash·환경·실행 command와 source snapshot을 보존한다. v16b라는 소스 버전과 v17이라는 실행/보고서 버전을 구분한다.

## 새 관측과 실제 결과

새640×480 RGB를 직접 확인하고 팔레트 상면 ROI `(236,197),(251,181),(383,181),(403,197)`를 지정했다. 새 overlay도 직접 보고 RGB/overlay SHA256에 결합한 review를 기록했다. 같은 픽셀 좌표를 쓰더라도 이번 새 영상 검토 후 지정한 annotation이며 과거 목표를 주입하지 않았다. 자동 팔레트 인식이 아닌 수동 ROI 보조 B5다.

Frozen HR YOLO checkpoint observed SHA256는 잠금값 `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`와 일치했다. 새 RGB SHA256는 `b8a89272423695b16d283701d4559ccc3d66235c7373e7aa82f8bcbb88d8520f`, 검출 confidence0.724332094다. 새 예측은 PRE=(-25.934899827,28.278040409), FINAL=(-25.934899827,29.078040409)m, yaw+90°다. 인식·목표 생성의 GT 입력은 없다.

| 항목 | 결과 |
|---|---|
| Fresh RGB-D / frozen YOLO / B4 / manual ROI B5 | PASS |
| PRE actual collider curved sweep / live PhysX support | PASS / 24300/24300 |
| PRE 최대 계획 곡률 | 0.269020205/m, 기존 steering feasibility gate 통과 |
| ROS 비영 발행 / adapter 행 | 741 / 743 |
| 실측 base 경로 / 순변위 | 0.679993402 / 0.678219185m |
| 마지막 XY / yaw | (-25.938789368,28.076448441)m / 92.3607565° |
| PRE 도착 / 잔여거리 | NO / 0.201629488m |
| FINAL 도착 / 독립 FINAL 검사 | NO / NOT_RUN |
| Wheel 최대 abs dq | 1.521160603rad/s |
| Unexpected contact / drive shell 침투·하중 event | 0 / 0 |
| PRE·FINAL 정상 stop certificate | 둘 다 없음 |
| 주행 후 physical quiet | FAIL, 정지 관찰 확보 못함 |
| Driver 최종 zero / cleanup observer zero | 20 / 요청 결합10회 |
| Cleanup receipt binding | PASS |
| Driver / observer / Kit exit | 0 / 0 / 0 |
| Outer / runner exit | NOT_READY·MISSING_WITNESS / 1 |

비상 zero와 timeline pause를 목표 도착 또는 물리 quiet 성공으로 계산하지 않았다. Session이 guard fault에서 timeline을 pause했고 이후 exception 경로의 tick도 stale TF로 즉시 거절돼 추가 물리 정지 관찰이 없다. `quiet`가 검사한 마지막1.000000052sim초는 여전히 주행 구간으로 span0.019044534m, 최대origin속도0.025114650m/s다. 따라서 안전 차단·zero 발행·종료는 확인되지만 실제 postfault quiet/최종 정지는 입증되지 않았다. Driver는 MOVING/completion_accepted=false로 끝났다. 정상 PRE stop 이전이므로 FINAL을 승인하지 않았다.

## TF_STALE 재발과 실제 시각

Driver fault wall `1793534545.6670182` (21:02:25.667 KST). Session도 같은 시점에 TF_STALE로 거절했다. 다음은 원시 forensic의 실제 수신·snapshot 기록·검사 시각이다. 단위는 Unix wall초다.

| 사건 | 시각 / 차이 |
|---|---|
| 직전 TF 수신 | 1793534545.0741835 |
| 위 TF 즉시 snapshot 기록 시작 | 1793534545.0741966, 수신 후13.1µs |
| Session 위 snapshot 검사 | 1793534545.1438527 |
| 마지막 실제 TF 수신 | 1793534545.1638134, sim41.516668831 |
| 마지막 완료 step 기록 | 1793534545.1709049 |
| Fault snapshot의 endpoint inventory 시각 | 1793534545.5801053 |
| Session 다음 guard 검사 | 1793534545.6649926, TF age0.501179218초 |
| Driver 최종 guard 검사 | 1793534545.6658301, TF age0.502016783초 |

v16b의 즉시 게시가 직전 실제 snapshot에서 확인됐다. 이번 fault snapshot은 그 뒤의 주기 inventory 게시로 덮여 `tf_snapshot_write_wall_s`가 없으므로 **마지막 TF의 정확한 atomic replace 완료/게시 시각은 UNKNOWN**이다. Inventory 시각은 실제 저장된 값이며 atomic replace 완료 시각으로 바꾸어 부르지 않는다. 마지막 수신 TF가 fault snapshot에 들어 있고, observer raw log에는 그 이후 새 TF 수신이 없다. v16처럼 이미 수신한 더 새 TF가 driver snapshot에 빠져 있었다는 증거는 없다.

확인된 지연은 **마지막 step 기록→다음 session guard 검사 사이0.494087696초**이며 새 app.update 이전 구간이다. 해당 구간 내부 graph traversal/actor signature/OS scheduling 등의 분해 계측은 없어 원인 UNKNOWN이다. 전체 pulse의 guard duration p50 0.062704325초/max0.464979410초, app.update p50 0.025537014초/max0.029932976초다. Fault가 발생한 미완료 tick의 전체 duration은 완료 step 통계에 들어 있지 않으므로 max값으로 fault 구간 전체를 설명하지 않는다. Driver의 TF sim 차이는 최대0.016666668초였으나 wall freshness 거절은 유효하다.

이 증거로 게시 patch가 전체 freshness 문제를 해결했다고 할 수 없다. 마지막 신규 TF 수신 부재 및 pre-endpoint 검사 진입 지연은 확인됐지만 세부 원인이 특정되지 않아 안전 threshold·graph 검사·fsync·신원 검사 변경이나 추측성 패치를 하지 않았다. 이해된 소프트웨어 수정에만 허용된 추가1회 Kit 조건이 성립하지 않으므로 추가 실행0이다.

## Cleanup·보존·남은 조치

원래 비상 요청 `1793534545.6661675` 보존. 별도 cleanup 요청 `1793534545.728555`, ID `e08d469d540e4013888db467003adb4c`; 영수증 `1793534545.7407072`로 요청후12.152ms다. 요청 hash `6daf922f78bdae66e40b0b12c7d46eb5c8040a10f488b1d5197071290edc8a23`/ID/domain/count10/zero 값 binding PASS. 이 발행 증거는 물리 quiet를 대신하지 않는다.

Kit PID1456759, observer1457749, driver1459321 모두 소멸 확인. 남은 Kit/training/HPO process0, 기존 rustdesk GPU process 보존. 강제 종료·watchdog timeout 없음. 이번 prepare 입력 전부 hash 불변, 기존 v16 prepare50개 및 v15_02 prepare44개 입력 hash 불변 PASS. Provisional digest와 존재 evidence hash PASS, eligibility=false 및 missing witness 실패는 그대로 보존했다. 원본 USD·weights·protocol·이전 결과 변경0. 이번은 engineering 실행이며 과학 lock 전체 재감사나 과학 성공 증거가 아니다.

증거: 새 root의 `evidence_v17.json`, `measured_summary_v16.json`(기존 read-only summary 도구의 출력명 유지), `prepare.json`, `run_status.json`, `runtime.log`, `executed_code/`; attempt의 raw RGB-D·ROI/review·model manifest·predicted targets·leg_0 sweep/support/path·steps·TF/endpoint forensics·guard fault·zero request/receipt·owned processes·provisional/final. 새 출력은 이전 출력을 덮어쓰지 않았다.

변경 파일은 이 보고서, `reports/latest_report.md`, `docs/PROJECT_STATE.md`다. 실행 코드 변경0. 다음 구체적 조치는 **기존 pre-endpoint guard 내부 graph/actor/forensic 구간별 시작·종료 시각과 observer의 실제 atomic publication 완료 시각을 새 버전에서 계측하는 것**이다. 추가 실주행 전 stale fault 이후 postfault quiet를 확보할 수 있는 안전 정지 관찰 lifecycle도 별도로 검증해야 한다. 현재 PRE/FINAL 완료와 physical final quiet는 미달성이다.
