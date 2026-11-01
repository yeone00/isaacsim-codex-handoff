# Kit 종료 경계 결과 저장 수정 v10C — 2026-11-01

**SOURCE PATCH PASS / CPU 36 tests PASS / compile PASS / Kit NOT_RUN.** ROS 주행·prepare geometry worker·학습·HPO·물리 재시도 없음. HPO/GPU training PAUSED, 공식 연구 denominator 0. CPU 검사는 실제 Kit runtime을 인증하지 않는다.

## 역사적 v10B 결과 보존

원래 B_REACHED YES, MOVED YES, STOPPED PASS, runner FAIL(exit1)이다. 실제 final XY=(-25.887977600097656,28.52072525024414)m, 순변위49.858093262mm, 원래 B 오차0.143863045mm(기준5mm). ROS nonzero Twist74, driver/observer/Kit exit0. 이번 결과 저장 수정과 물리 성공은 별개다.

증거 root: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_TARGET_DRIVE_20261101_v10B_01`. 해당 run_status는 FAILED, Kit exit_code0, execution_complete 부재를 기록한다. 원시 파일 수정 없음. run_status SHA256 `8c9793cdcbef06a5446833d9356148bcecfdc501c1b11b1819c2f4c1f1529487`.

v10B runner/session은 실제 executed_code snapshot과 각각 byte/hash 일치했다. runner SHA256 `4a6b00573c66033dd748af1ee21a25e34cb254a0603a7ff56428a4c7f5f8dd0d`, session SHA256 `7e635d1d2610c04d71f16ec9ce7597c236e5a2b242a623d76c2ea3366eb551f4`. steps854행·commands95행, 원시 final XY 및 receipt/owned exits를 확인했다. CPU helper로 원시 stop을 읽기 전용 재계산: confirmed=True, 저장된 최종 stop_quiet_result와 outcomes 동일. 이는 historical run 재분류가 아니다.

v10B는 app.close 뒤 최종 집계·serialize에 의존했다. 실제 로그에는 Simulation App Shutting Down이 있고 결과 파일은 없다. close 뒤 어느 Python 명령이 실행됐는지는 trace가 없어 UNKNOWN이다. collision/geometry/TF/GID/navigation 재감사나 변경은 하지 않았다.

## 변경 내용과 소유권

새 session은 기존 주행·target·guard·emergency zero 및 cleanup 순서를 그대로 계승한다. 실제 정지 판정, zero 요청/receipt, observer/driver 종료, stream 종료와 metrics 저장 후 기존 final_success 조건을 계산한다. result.status는 NOT_READY인 채로 execution_provisional.json에 PROVISIONAL envelope를 쓴다. provisional은 최종 PASS가 아니다. 그 다음 단일 소유 helper가 app.close를 한 번 호출한다. 정상 반환 뒤에는 로컬 exit code만 정하며 최종 저장을 하지 않는다. close 예외가 반환되면 별도 fault 파일을 남긴다. 반환하지 않는 close에서도 provisional은 이미 존재한다.

증거 파일 fsync → provisional 임시 파일 flush/fsync → 같은 파일시스템 hard-link로 atomic no-clobber 게시 → directory fsync 순서다. 기존 파일은 교체하지 않는다. 전체 증거가 없으면 실패 provisional도 보존하며 outer 판정은 NOT_READY다. 저장 I/O 자체가 실패하면 성공으로 승격하지 않는다.

provisional에는 schema, 고유 runner nonce, Kit PID, 절대 output 경로, session source SHA256, wall time, close 요청 의도, eligibility, critical result, 필수 증거12개 hash와 canonical body SHA256를 기록한다. SHA256는 무결성/provenance 결합이며 비밀키 전자서명은 아니다. nonce/PID/source 기대값은 외부 runner가 소유한다.

외부 runner는 Popen poll/wait로 실제 Kit child 종료를 확인한 뒤에만 finalize를 호출한다. Kit exit0와 별도로 해당 신규 runtime.log의 shutdown 문구도 요구한다. ROS child exit0만으로 Kit 종료를 판정하지 않는다. shutdown 문구와 close 요청 의도는 정확한 내부 instruction trace나 framework release 완료 인증은 아니다. 실제 v10C 종료 경계 검증은 NOT_RUN/UNKNOWN이다.

outer 검증: provisional schema/digest/provenance·필수 evidence hash, 동일 원래 B와5mm, raw 최종 pose 오차, confirmed_stop 재계산(물리 quiet ≥1초·속도≤.002m/s·span≤.002m 및 graph/controller zero), 저장 outcome과의 일치, BRAKING→ZERO_SETTLING, driver completion/adapter_fault/hard_trigger 명시 필드, corridor/support admission, 기존 contact 안전 조건, cleanup zero count≥10/domain191/v=w=0/요청 이후 receipt, ROS owner exit0, 기존 final_success eligibility/오류 조건. fault witness 부재뿐 아니라 명시적인 정상 driver 필드를 요구한다. timeout·signal/supervisor abort·강제 종료는 별도 latch로 성공을 금지한다.

검증이 끝난 outer만 attempt_0001/execution_complete.json을 atomic 작성하고 기존 aggregate를 통해 top-level run_status.json을 atomic 작성한다. 누락/변조/모순/비정상 exit/timeout/fault는 NOT_READY 또는 runner FAILED/exit1이며 기록을 덮어쓰지 않는다. 두 JSON은 각각 atomic이며 한 트랜잭션은 아니다. 사이에 outer crash가 나면 run_status 부재는 미완료로 남는다. 자동 재시도는 추가하지 않았다.

새 기본 output namespace는 CONSTRUCTION_SITE_RESULT_PERSISTENCE_20261101_v10C_01이며 prepare는 exist_ok=False다. 기존 status/attempt 재사용을 거부한다. correction-recheck는 v10C에서 거부한다. future run용 source snapshot/code_versions 및 prepare input hashes에 v10C를 포함했다. 기존 v10B ROS driver/target/guard를 재사용하며 원본은 수정하지 않았다.

## 변경 파일 / SHA256

| 신규 파일 | SHA256 |
|---|---|
| `scripts/construction_site_drive_runner_20261101_v10C.py` | `5d4ab00c593f9750160037ef969b08f7ff1a81802fcd20c0b10d33bed291633e` |
| `scripts/construction_site_drive_session_20261101_v10C.py` | `9d93ca9c1081e767e3074dc76522118003cd1e5c3ca4d263d41477a8dee08ed7` |
| `evaluation/construction_site_persistence_20261101_v10C.py` | `aa952bce559e87eb1c4dbcc92b32786ae8c47827cec46088ebd8761ffa2d3eae` |
| `tests/test_construction_site_persistence_20261101_v10C.py` | `23e774163c89bdbab974f81b98458e34f90ced0d564e156a511ca0bd3a48b977` |

추가 문서 변경: 본 보고서, reports/latest_report.md, docs/PROJECT_STATE.md(append). 기존 보고서·raw evidence·잠금·USD·weights·legacy source 보존.

v10B 대비 diff 요약:
- runner: +18/−5행. 외부 종료 검증·최종화·atomic 저장·신규 output/source provenance.
- session: +5/−6행. close 뒤 저장 제거, close 전 eligibility/provisional로 이동. 주행 본문 변경 없음.

## CPU 검증

- 신규23/23 PASS: os._exit(0)으로 반환하지 않는 mock close→durable provisional→실제 CPU child wait→외부 최종화, 유효 결과, provisional 누락/손상, hash 변경, provenance 불일치, Kit crash/nonzero/종료 미확인, shutdown 로그 누락, timeout, receipt/물리 정지 누락, 속도 실패, target 모순, driver fault/명시 필드 누락, observer exit 실패, 외부 abort, close 예외, 기존 final 덮어쓰기 거부, source 소유권 연결.
- 기존 cleanup/lifecycle11/11 PASS, target/phase2/2 PASS. 합계36/36.
- 신규 Python4개 py_compile PASS. executable Kit/ROS entrypoint를 import하거나 실행하지 않았다. CPU subprocess는 mock close 시험 전용이다.
- git diff --stat는 이 디렉터리가 Git repository가 아니어서 FAIL. 파일간 diff로 검토했으며 diff exit1은 차이 존재를 뜻한다. staging/commit/push 없음.

실행한 검사 명령:

```bash
python3 -m unittest discover -s tests -p 'test_construction_site_persistence_20261101_v10C.py' -v
python3 -m unittest discover -s tests -p 'test_construction_site_drive*20261101_v*.py' -v
python3 -m unittest discover -s tests -p 'test_construction_site_target_20261101_v10B.py' -v
python3 -m py_compile scripts/construction_site_drive_runner_20261101_v10C.py scripts/construction_site_drive_session_20261101_v10C.py evaluation/construction_site_persistence_20261101_v10C.py tests/test_construction_site_persistence_20261101_v10C.py
```

## 미해결과 다음 행동

v10C 실제 Kit 종료·runner exit0 확인은 NOT_RUN/UNKNOWN. CPU mock은 설치된 SimulationApp.close의 종료 동작을 인증하지 않는다. 별도 bounded runtime confirmation 1회가 다음 검증 후보이며 이번 작업에서 시작하지 않았다. 이후에는 의미 있는 장거리 A-to-B와 fresh RGB-D→YOLO→B4/B5 및 task E2E로 engineering을 진행하는 것이 목적이다. 50mm 반복 물리 입증은 수행하지 않았다. Perception/task E2E는 미검증, HPO/training PAUSED, 공식 연구 denominator0.
