# 현장 단일 로버 v04 — 물리 시계 PASS, 기울어진 바퀴 지지 검사에서 구동 전 중단

2026-11-01 KST. **실제 Kit 한 세션에서 시계와 baseline 정지는 확인했지만 forward+stop 목표는 달성하지 못했다.** 비영 명령 0, MOVED NO, 주행 후 STOPPED NOT_TESTED. 연구 denominator 0, HPO PAUSED 유지. 재시도·두 번째 Kit 없음.

| 항목 | 실제 결과 |
|---|---|
| Kit / drive attempts / nonzero commands | 1 / 0 / 0 |
| 물리 clock / stationary quiet | PASS / PASS |
| MOVED / STOPPED | NO / NOT_TESTED — postzero 검증 없음 |
| shell 관측 접촉점 비침투·무충격 | PASS, 정지 기록 범위 한정 |
| 여섯 바퀴 contact | 관측됨; 실제 swept PhysX 지지 인증 NOT_TESTED |
| 내부 판정 / native host exit / runner exit | NOT_READY / 0 / 1(정상화된 실패) |
| 단일 남은 기술 제약 | 정착 후 기울어진 바퀴 지지를 실제 PhysX raycast로 인증하지 못함 |

## 시계 BEFORE / AFTER

v03 원본 steps195개·runtime_summary·run_status·ros_status를 직접 읽었다. runtime_summary는 attempt 내부가 아니라 v03 출력 root에 있었다. v03 baseline은 `timeline.get_current_time()`을 사용했고 timeline start/end timecode0, 기본 looping play였다. timeline 범위 **0.000000160808~0.033333656689초, 역행78회**, TF stamp6.283333661초였다. v03에는 독립 물리 step 기록이 없으므로 과거 물리 진행 자체를 확정하지 않는다.

설치된 Isaac Sim **5.1.0**의 실제 Python 소스와 `.pyi`를 확인했다(`installed_api_evidence.json`). v04는 **SimulationManager.get_simulation_time()**을 baseline·FD·endpoint/TF 비교·pulse/postzero 시간의 기준으로 사용한다. PhysX 실제 step callback의 횟수·각 dt·누적 dt, native step count, raw timeline·play/loop 상태, 기존 graph simulationTime·TF stamp를 별도로 저장했다. wall time과 i×dt를 simulation time으로 사용하지 않았다.

새 runtime overlay만 start0/end120초·loopingFalse로 설정했다. 원본 USD와 graph·physics dt·controller는 그대로다. 물리 timestamp는 **6.283333661035초**, 실제 callback **377 steps**, 마지막 dt **0.016666667536초**이며 native physics step 수도377이다. native 시간과 실제 callback dt 누적값 차이 **0초**, step count 차이0, 기존 graph timestamp와 native 차이0이다. telemetry195행의 물리 시각3.050000159070→6.283333661035초, 역행0; raw timeline3.016666823998→6.250000325963초, 역행0; TF와 native 최대 차이 .033333336068초로 기존 .1초 기준 이내다.

baseline 마지막30행 시간차 **0.483333358541초 > .4초**. 마지막 정지창 coverage **1.000000052154초**, COM peak .000388869344m/s, root-origin .000394139814m/s, FD0, pose span0으로 모두 기존 .002 기준 PASS다. 이 값은 **비영 명령 이전 stationary 상태**이며 주행 후 정지 성공을 뜻하지 않는다. raw timeline과 물리 시계가 서로 다른 위상임을 직접 확인했다. 다만 range와 source를 함께 수정했으므로 v03 원인이 looping 하나였다는 분리 인과 증명은 아니다.

## shell과 바퀴 — 확보한 물리 증거

`contacts.json`은 pair뿐 아니라 각 접촉점의 world 위치, normal, separation(m), impulse(Ns), phase와 물리 step을 저장한다. 총168 events, shell24 events/144 points다. shell 최소 separation **.078864306211m**, 최대 impulse **0Ns**, normal Z .999986469746이다. 예시 world contact(-25.9086914,28.4468822,-.008502685)m는 floor 근처지만 shell에 대한 separation은 양수였다. 따라서 단순 pair count를 shell 침투/끌림으로 해석하지 않는다.

정착 후 collider inventory의 shell world Z는 **[.065561256826,.527515326354]m**다. 원본 현장 mesh를 읽어 같은 shell XY의 수직 triangle 교차9점을 계산했으며 최소 하단 gap **.070647280933m**, 9/9 양수다. 이는 **저장 기하의 offline 교차**이며 live PhysX raycast로 표기하지 않는다. 관측된 shell 접촉은 모두 settling0~.383333353초에 발생했고 baseline 접촉점은 없다. 기록된 점은 비침투·무하중이며 정지 상태 간격도 양수다. **주행 중 dragging/안전은 NOT_TESTED**다.

여섯 바퀴 모두 각24 contact events를 기록했다. 전후4바퀴에는 최대10.4266/16.5298/20.7066/12.0553Ns impulse가 있었고 middle2바퀴는 최대0Ns였다. 따라서 여섯 pair를 모두 하중 지지로 승격하지 않는다. 전체 swept support 표본의 실제 PhysX 검사는 도달하지 못했다.

## 정확한 중단 원인과 실행 후 수정

offline 준비는 collision별 .10m clearance와 기존 ROS 세 controller graph admission PASS였다. 실제 baseline 후 다시 계산한 `collision_preflight.json`에는 **장애물 overlap0건**이다. 실패7개는 여섯 바퀴 각각 `tilted_support_requires_stationary_PhysX` + 그 결과 `no_enabled_ground_supports`다. 기존 알고리즘은 cylinder 축의 world Z 성분 절댓값>.0001이면 표본을 만들지 않았다. 실제 tensor base orientation은 roll **.137956685°**, pitch **-.260161107°**였고 수평 축 가정이 깨졌다. 이는 통로 장애물이나 실제 wheel unsupported 확정이 아니다.

**이번 구현은 이 analytic 실패를 shell 진단·live raycast보다 먼저 assert하는 순서를 유지한 탓에, 안전 확인 후 같은 세션에서 주행할 기회를 놓쳤다.** 원시 failure_reason `NO_SAFE_CORRIDOR`는 보존하지만 원인은 위 support 처리 한계로 특정한다. 임의로 guard를 통과시키거나 재실행하지 않았다.

실행 종료 뒤 실행 당시 v04 코드3개를 외부 `executed_code/`에 그대로 보존했고 hash가 prepare manifest와 일치함을 확인했다. 이어 repository v04 geometry에는 기울어진 cylinder의 각 axle 단면에서 실제 최하단 radial tread를 계산하는 식을 추가했다. 표본 높이는 개별 world Z로 비교하며 기존10mm support tolerance, 5mm travel 간격, yaw±2°, .10m clearance를 유지한다. session도 shell 진단과 live support 자료를 저장한 뒤 최종 admission을 판단하도록 순서를 수정했다. controller/graph/원본 collider 변경 없음.

**이 실행 후 수정본은 static 검증만 PASS, 실제 runtime NOT_TESTED다.** consumed prepare의 입력 hash는 이 수정본과 달라 재사용 실행이 차단된다. 실행 결과를 수정본의 성공으로 재해석하지 않는다.

## 보존·검사와 다음 행동

- 새 코드: `scripts/construction_site_drive_{runner,session,geometry,geometry_checks,evidence}_20261101_v04.py` 총5개. 변경 문서: 이 보고서, `reports/latest_report.md` 동일 내용, `docs/PROJECT_STATE.md` 추가 기록.
- compile5 PASS. enabled high collider의 높이 분리/실제10m 충돌/disabled 상태 회귀 PASS. .2° tilted wheel369 support samples PASS, 바닥 제거 시 지원 실패 검출 PASS. 이는 synthetic offline 검사다.
- source/reused input46개 재검증 PASS, v03 prepared inputs49개 보존 PASS. source USD, v01-v03 코드/출력·고정 controller/threshold 변경 없음. 실행 당시 코드와 실행 후 수정본 hash는 `final_verification.json`에 구분했다.
- Kit 내부 NOT_READY인데 native exit0인 현상을 다시 관측했다. 새 runner는 internal status를 읽어 **exit1**로 반환했다. 성공 처리하지 않았다. post-run 선택적 Euler 계산의 inline SyntaxError/exit1도 verification에 남기고 read-only 계산만 바로잡았다.
- 실제 명령: `python3 scripts/construction_site_drive_runner_20261101_v04.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v04/prepare_0001`. 로컬 hh_isaac51 Python/Kit 사용. 사전 Kit·훈련 프로세스0, GPU는 기존 rustdesk535MiB. 사용자 프로세스 종료 없음.
- 증거 root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v04`. 실제 실행은 `prepare_0001/attempt_0001/`; 핵심 파일은 `physics_steps.jsonl`, `steps.jsonl`, `baseline_quiet.json`, `collision_preflight.json`, `contacts.json`, `runtime_summary.json`, `execution_complete.json`, 상위 `run_status.json`, root `stationary_evidence_analysis.json`, `final_verification.json`이다. 초기 prepare와 최종 prepare는 offline이며 Kit은 최종 prepare에서 정확히1회였다.

**다음 구체적 행동은 새 별도 실행 기회에서 수정된 tilted-tread 표본의 live PhysX 지지 인증을 마치고, 안전하면 같은 세션에서 단일 forward+stop을 수행하는 것이다.** 이번 허용량 한 세션은 소진했으므로 추가 launch하지 않았다. 34.127288744mm 역드리프트 문제는 해결되지 않았고 이번에는 postzero reverse drift·target 오차를 측정할 주행이 없었다. HPO/YOLO training/B4/B5/B300/324/432/QUAL12/preview/GT perception 입력 없음, 연구분모0이다.
