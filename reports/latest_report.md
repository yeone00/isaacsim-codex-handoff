# 현장 perception → PRE → FINAL v16 — 2026-11-01

**전체 NOT_READY. 새 인식·PRE 안전 경로 검사는 PASS, 실제 PRE/FINAL 도착은 NO/NO다.** 누적 파일 재읽기를 제거한 v16으로 Kit 1회·ROS 주행 1회를 수행했으나 `TF_STALE`가 재발해 안전 정지했다. 요청에 결합한 cleanup receipt 및 물리 quiet·소유 프로세스 정상 종료는 PASS다. 관측된 TF 상태 반영 지연에 대한 v16b 후속 패치는 CPU 검사만 PASS이며 runtime NOT_RUN이다. 재시도0, 과학 denominator0, HPO/training PAUSED. 기존 v15의 실패를 변경하지 않았다.

## 변경과 검사

v15/v15b를 새 버전으로 복제하고 검증된 mounted camera·fresh RGB-D capture, frozen HR YOLO, B4/B5, 수동 ROI, v14 Hermite follower·legacy steering encoding·StoppingAdapter·13 collider sweep·live PhysX support를 재사용했다. 새 센서 관측 대신 이전 목표/GT를 주입하지 않았다. 초기 배치는 기존 v14b의 물리 시작 전 overlay 배치 그대로이며 실행 중 transform 변경은 없다.

- Session의 command JSONL을 byte cursor로 신규 완결 행만 읽는다. 부분 행은 다음 poll까지 보류하고 파일 교체·축소는 거절한다. controller readback도 같은 캐시를 사용한다. drive contract는 시작 때 한 번 읽는다.
- Driver의 leg별 승인 경로는 한 번 읽고 cache한다. 매 사용 시 inode·size·mtime·ctime을 비교하여 경로 변경은 거절한다. 두 번째 leg는 별도 파일이므로 새로 읽는다.
- 불변인 과거 contact를 반복 검사하지 않고 새 contact 전부를 검사한다. 원자료는 모두 보존한다. 정상 정지 인증 함수 자체는 유지하고 adapter가 ZERO_SETTLING일 때만 호출한다.
- **매 tick 전체 graph/actor 검사, endpoint/GID 고정, TF wall≤0.5초·sim 차≤0.1초, steering·속도·이동 envelope·collision·support·정지 기준은 유지했다.** EndpointGuard 원본 및 fsync 동작도 변경하지 않았다.
- 비상 `zero_request.json`은 보존한다. finally에서 별도의 `cleanup_zero_request.json`을 atomic 생성하며 고유 request ID·시각·domain을 담는다. observer는 새 요청마다 zero count를 다시 시작하고 10회 발행 후 요청 전체 SHA256·ID·시각을 영수증에 넣는다. 대기 함수는 이전 요청 영수증을 성공으로 채택하지 않고 최대3초 동안 해당 요청 영수증을 기다린다. 정상 경로의 outer finalizer도 동일 binding을 다시 검사하며 기존 모든 witness를 요구한다.

실행 전 신규 IO 회귀 **5/5**, 기존 v15 graph allow/reject **5/5**, 신규 runtime source 6개 compile PASS. IO 회귀는 부분 행·동일 파일 반복 poll의 추가 read 0byte·축소 거절·승인 경로 변경 거절·잘못된 요청/시각/domain/count/nonzero 영수증 거절·기존 TF 한계 거절을 포함한다. 실제 종료 뒤 v16b TF snapshot 회귀 **4/4**, 후속 source 4개와 summary compile PASS. 총 회귀14개 PASS. 신규 테스트가 실제 도착이나 v16b runtime 성공을 증명하지는 않는다.

## 실제 제한 실행

출력 root:
`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v16_01`

명령:
```bash
python3 scripts/construction_site_perception_runner_20261101_v16.py --prepare-only
python3 scripts/construction_site_perception_runner_20261101_v16.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v16_01
```

prepare geometry worker는 기존 hh_isaac51 pxr runtime을 사용했다. Kit은 `/home/user/anaconda3/envs/hh_isaac51/bin/python`과 설치된 Isaac Sim 5.1, ROS jazzy/domain191로 실행했다. 인식은 기존 sdg_tools 환경이다. 상세 command·Python·실행 소스 snapshot은 `code_versions.json`, `prepare.json`, `executed_code/`, 인식 패키지 버전·weight hash는 `attempt_0001/frozen_model_manifest.json`에 있다. resource/GPU/domain isolation PASS, 기존 rustdesk 보존. 의존성 설치·업그레이드 없음.

이번 새 RGB와 ROI overlay를 직접 보고 `(236,197),(251,181),(383,181),(403,197)` 수동 상면 ROI를 새 RGB SHA256에 결합했다. 자동 팔레트 검출이 아니다. 새 예측 **PRE=(-25.934669582,28.278040571), FINAL=(-25.934669582,29.078040571)m**, task yaw +90°다. 이전 목표 좌표를 재사용하지 않았다.

| 항목 | 실측/판정 |
|---|---|
| fresh capture·frozen model·B4/B5 | PASS, 수동 ROI 보조 |
| PRE curved sweep / live support | PASS / 24300/24300 |
| 비영 ROS command / 전체 adapter 행 | 406 / 407 |
| PRE 도착 / FINAL 도착 | NO / NO, FINAL plan·sweep·drive NOT_RUN |
| 마지막 base XY / yaw | (-25.928850174,27.759275436)m / 약94.326° |
| PRE 잔여 거리 | 0.518797774m |
| base 경로길이 / 순변위 | 0.362254716 / 0.361458268m |
| wheel 최대 abs dq | 0.846528649rad/s |
| unexpected contact / 주행 shell 침투·하중 event | 0 / 0 |
| 비상 정지 뒤 quiet | PASS, 연속1.000000052sim초 |
| quiet pose span / FD peak | 0m / 0m/s |
| quiet raw COM / base origin peak | 0.000233799 / 0.000229391m/s |
| PRE·FINAL 정상 stop certificate | 둘 다 없음 |
| driver 최종 zero / cleanup observer zero | 20회 / 해당 cleanup 요청에 10회 |
| cleanup receipt binding | PASS |
| driver / observer exit | 0 / 0 |
| 실제 Kit PID / exit / close log | 1379939 / 0 / 확인 |
| outer / runner exit | NOT_READY·MISSING_WITNESS / 1 |

Driver의 `adapter_state=MOVING`, `completion_accepted=false`, fault 파일의 `TF_STALE`를 그대로 보존했다. `adapter_fault=null`은 endpoint fault가 없다는 뜻이 아니다. `outcomes.zero=NOT_READY`도 유지된다. 상위 `STOPPED=PASS`는 비상 정지 뒤 quiet의 집계이며 PRE/FINAL 정상 도착·stop certificate를 뜻하지 않는다. session의 `TWO_LEGS_INCOMPLETE`, outer의 `MISSING_WITNESS`와 runner exit1을 성공으로 바꾸지 않았다.

## TF_STALE 조사: 확인된 지연과 미확인 원인

실제 fault guard 시각은 **19:57:38.424785 KST**다. guard가 읽은 status는 wall age **0.095260620초**였지만 그 안의 TF age는 **0.501729965초**, sim stamp 차는 **0.016666668초**였다. pinned GID는 동일했다. 따라서 기존 TF_STALE 차단은 유효하다.

이번 최소 계측에서 pulse tick 간격 p50 **0.089357초**, p95 **0.092792초**, max **0.420023초**다. guard 구간 p50 **0.062177초**, max **0.393329초**; app.update p50 **0.025071초**, max **0.028884초**다. 중단 직전 긴 구간은 app.update 이전 guard 구간에 있었다. 이 구간 안의 graph traversal·actor signature·forensic fsync·스케줄링 중 무엇이 지연을 일으켰는지는 **UNKNOWN**이다. 누적 파일 재읽기가 유일한 원인이라는 가설은 이번 재발로 지지되지 않는다.

또한 **실제 수신과 상태 게시 사이 지연**을 확인했다. fault snapshot의 TF는 wall `1793530657.923055`였고, status 파일 시각은 `1793530658.3295243`이었다. observer 원자료에는 다음 TF를 **1793530658.3441489**에 이미 수신한 기록이 있다. 그러나 guard 시각 **1793530658.424785**에 읽은 status에는 이전 TF가 남았다. 즉 새 TF 수신 후 약80.6ms가 지나도 driver는 이전 TF를 검사했고, 다음 수신 기록은 `1793530658.4319358`이다. 이전 TF를 검사한 안전 guard를 우회하거나 threshold를 늘리는 방식으로 해결하지 않았다.

이 증거에 맞춰 **새 v16b observer**는 on_tf에서 새 TF를 즉시 atomic status snapshot에 반영한다. endpoint 목록은 기존 주기마다 전부 재조회하고, **그 endpoint inventory의 wall_s는 TF 수신으로 갱신하지 않는다**. 새 TF가 오래된 신원 정보의 유효기간을 늘릴 수 없다. CPU 재현은 실측 시각과 같은 이전 snapshot의 TF_STALE 거절, 즉시 반영 snapshot의 동일 guard 통과, GID 변경 거절, stale endpoint/stale TF 거절 및 inventory 없는 상태 생성 금지를 확인했다. **v16b는 prepare·Kit 실행하지 않았다.** 실행된 v16과 후속 v16b를 소스/해시로 분리했다. 전체 TF_STALE 해결의 runtime 검증은 남아 있다.

## Cleanup·보존·다음 행동

원래 비상 요청 시각 `1793530658.4413543`은 변경하지 않았다. 별도 cleanup 요청은 `1793530667.53573`, ID `677327f214554cdc92215441a4c7418e`; 영수증은 `1793530667.5524633`으로 **요청 후16.733ms**이며 요청 hash `efe3c60ea3518d9c540dfcf3762d0fd955132b24a277471c14659f356991814c`와 일치한다. 이 영수증은 비상 요청에 먼저 발행한 zero를 cleanup으로 소급 채택한 것이 아니다. 전체 lifecycle 성공과 cleanup receipt PASS는 별도 판정이다.

prepare 입력 **50개 hash 불변**, v15_02 prepare의 기존 **44개 입력 보존 PASS**, provisional digest·존재 evidence hash PASS. 필수 witness 누락은 그대로 FAIL이다. 소유 driver/observer/Kit PID 소멸 확인, 남은 Kit/training/HPO 프로세스0, rustdesk 유지. 강제 종료·watchdog timeout 없음. 원본 stage·weights·locked protocol·기존 v01–v15 source/results를 수정하지 않았다. 이번은 engineering 한 세션이며 scientific lock 전수 재감사나 과학 실행은 하지 않았다. `git status`는 현재 폴더가 Git repository가 아니어서 exit128로 실패했으며 파일별 hash와 diff로 확인했다.

신규 파일: `scripts/construction_site_perception_{runner,session}_20261101_v16.py`, `scripts/construction_site_drive_ros_20261101_v16.py`, `scripts/construction_site_observer_20261101_v16.py`, `evaluation/construction_site_{io,persistence}_20261101_v16.py`, IO test·summary 각 analysis 파일. 후속 미실행 패치는 runner/session/observer v16b, `evaluation/construction_site_tf_snapshot_20261101_v16b.py`와 해당 analysis test다. 이 보고서·`reports/latest_report.md`·`docs/PROJECT_STATE.md`를 갱신했다.

증거는 root의 `measured_summary_v16.json`, `tf_stale_forensics_v16.json`, `focused_checks.json`, `followup_checks_v16b.json`, `v15_preservation.json`, `code_inventory_v16.json`, `post_run_process_check.json` 및 `attempt_0001/`의 raw steps/ROS/forensics/receipt/provisional/outer final이다. 존재 evidence hash PASS가 누락 witness나 도착 성공을 대신하지 않는다.

**다음 구체적 행동:** v16b의 즉시 TF 게시 수정으로 새 별도 output에서 fresh perception·동일 안전 admission 후 bounded PRE→FINAL 검증을 수행한다. 준비 명령은 `python3 scripts/construction_site_perception_runner_20261101_v16b.py --prepare-only`이며 이후 생성되는 prepare의 정확한 run command를 사용한다. 이번 작업에서는 정한 Kit1회·retry0 한도를 지켰다. 장기 guard 구간의 세부 원인은 추가 계측 대상으로 남으며, 현재 full approach readiness는 PASS가 아니다.
