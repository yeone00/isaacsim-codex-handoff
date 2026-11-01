# 정상 정지 전이·인증 계약 v21 — 2026-11-01 실행 / 2026-11-02 보고 완료

**정지 계약 수정 PASS, 새 PRE→FINAL 실구동 1/1 성공, 재시도 0.** 두 leg 모두 실제 정상 정지·zero·독립 post-zero quiet 인증 후 Kit/driver/observer exit0 및 외부 `ENGINEERING_RECORDED`/runner0을 확인했다. HPO/training **PAUSED**, scientific denominator **0**. HR/LR/CAD 과학 실험·학습·자산/인식/항법 재구성은 시작하지 않았다. 역사적 v19b 성공과 v20 **실패 0/2**는 그대로 보존한다.

## 1. 먼저 수행한 정확한 오프라인 재현

[재현 JSON](construction_site_stop_replay_20261101_v21.json), [원시 출력](construction_site_stop_replay_20261101_v21.log), [읽기 전용 도구](../analysis/construction_site_stop_replay_20261101_v21.py). v20 최초/추가 baseline 인덱스와 두 실패 raw 인덱스의 **1,072개 SHA 항목 불일치 0**을 확인했다. 기존 adapter는 실행 snapshot에 없으므로 경로를 추측하지 않고, 추가 인덱스가 동결한 실제 transitive source를 사용했다. 확인 logic은 저장 snapshot과 일치하는 기존 v09다. simulator/ROS를 시작하지 않고 각 FINAL 시작부터 최초 ZERO까지 원래 governor 상태를 순서대로 재계산했다. 코드 import 전 관련 CPU module을 정적으로 읽었다.

| 원자료 | 재현 호출 수 | 첫 정상 정지 전이 sim초 / step | 호출 전 surface command → 반환 surface command(m/s) | 기존 verifier |
|---|---:|---|---|---|
| v19b `v19_02` | 1109 | 123.066673085 / 7381: MOVING→BRAKING | .003573693367 → .000073693184 | 원래 PASS |
| v19b 다음 호출 | 위에 포함 | 123.116673088 / 7384: BRAKING→ZERO_SETTLING | .000073693184 → 0 | 위와 같음 |
| v20_01 | 1114 | 123.983339800 / 7436: MOVING→ZERO_SETTLING 반환 | .002804366825 → 0 | 원래 FAIL |
| v20_02 | 1114 | 123.483339773 / 7406: MOVING→ZERO_SETTLING 반환 | .003280314790 → 0 | 원래 FAIL |

세 재현의 기존 adapter **전체 반환 dictionary 불일치 0**. 해시 검사 포함 재현은 약 3.58초였다. v19b의 첫 BRAKING wire 출력은 .000018469470m/s였고 다음 호출은 wire 0이었다. 이는 요청/출력값이며 실측 기체 속도와 구별한다.

v20 두 호출도 내부에서 먼저 정상 요청에 의해 BRAKING이 되고, governor에 요청 0을 넣어 기존 감속을 계산한다. 직전 출력이 한 호출의 감속량 안에 있어 그 호출 출력이 바로 0이 되고 ZERO_SETTLING으로 바뀐다. 기존 interface는 최종 state만 반환하므로 중간 전이가 숨는다. **유한 시간의 별도 비영 제동 명령은 이 두 호출에 없다.** 내부 제동 계산·전이와 실제 발행된 zero 한 개를 구별한다. 과거 로그에 BRAKING 행을 만들거나 과거 정지 인증을 보충하지 않았다.

## 2. 수정 범위와 독립 인증

[새 adapter](../evaluation/construction_site_stopping_adapter_20261101_v21.py)는 기존 동작을 보존하면서 각 실제 state 대입에 `transition()`을 사용한다. 한 update의 입력, update_id, 시작 state, 순서 ordinal·before·after·cause를 반환한다. 전이는 해당 command의 실제 source step/sim time에 결합되며 가상의 시각·지속시간·추가 ROS 명령을 만들지 않는다. 한 호출의 MOVING→BRAKING→ZERO도 두 사건으로 기록하지만 발행 출력은 그 호출의 실제 출력 하나다. governor/이득/감속/steering/follower 변경은 없다.

[새 verifier](../evaluation/construction_site_stop_certificate_20261101_v21.py)는 event를 신뢰만 하지 않는다. 명령별 실제 저장 입력으로 adapter를 처음부터 재실행하여 반환 dictionary·event·발행 wire와 대조한다. 정상 stop 요청이 실제 목표 3mm 이내 측정에서 발생하고 유지돼야 하며, 정상 request→BRAKING→governor zero 순서가 정확해야 한다. initial zero, fault latch, 가짜 event, 틀린 시간/순서는 거절한다. 실제 비영 BRAKING 출력이 있을 때만 그 수를 기록하며 immediate-zero 경우 그 수는 0일 수 있다.

계속 요구하는 증거는 다음과 같다.

- raw physics step와 feedback pose/속도/시간의 결합, 실제 이동 및 비영 명령.
- 정상 요청·실제 zero wire, graph wheel target와 두 wheel controller의 zero readback.
- ZERO 이후 새 연속 quiet ≥1초, 시간 간격 ≤.1초, COM/origin/FD 속도 각각 ≤2mm/s, pose span ≤2mm.
- 실제 측정 종점의 거리 ≤5mm·yaw ≤2°. 기존 3mm stop trigger도 유지.
- fresh observer/TF 및 허용 ROS publisher 이름·namespace·type·GID pin. 원래 독립 driver/session guard가 두 leg 전체에서 계속 동작하고, 인증도 저장된 endpoint snapshot을 재검사.
- PRE/FINAL 분리, FINAL 첫 명령보다 앞선 PRE 정지 인증, 각 leg 별 독립 quiet와 endpoint. fault/cleanup quiet는 정상 정지로 인정하지 않음.
- 원래 curved full-rover collision/support·contact·speed/steering·GC/RSS·프로세스 종료·cleanup receipt·provisional/hash gate.

기존 시작에서 첫 command가 바로 앞 `fresh_capture` 측정을 참조하는 사실을 archived regression에서 확인했다. 첫 호출이며 정상 stop 요청이 없는 경우만 이 원래 시작을 허용한다. 이후 fault/cleanup phase는 거절한다. 최종 outer 재검증은 각 leg certificate의 실제 end 시점까지 명령과 physics를 다시 대조하고, FINAL zero 뒤 나머지 모든 command도 zero인지 확인한다. 종료 후 추가 quiet와 cleanup은 기존 별도 검사를 유지한다. 종점 yaw도 저장된 요약 scalar 대신 raw pose에서 재계산한다.

런타임 연결은 새 driver/session/runner 및 persistence v21 파일로만 변경했다. 원래 supplier graph·원본 site/USD·engineering 시작·v19 follower·fresh RGB-D/HR YOLO/B4/수동 ROI B5 경로를 유지했다. 소스 diff는 호출 기록·인증 연결 및 그에 필요한 per-leg 시간창에 국한된다.

## 3. CPU 검증과 실행 전 gate

[최종 CPU log](construction_site_stop_cpu_20261101_v21_final.log): **20/20 PASS**. v19b 두 호출 BRAKING→ZERO와 v20 한 호출 내부 BRAKING→ZERO, 제동 사건/zero/request 누락, 역순, 위조 사건·시간, endpoint/yaw 초과, contact/fault·fault cleanup, stale endpoint·변경 GID, 비영 readback, 부족한 quiet, PRE/FINAL 분리·순서·leg 혼합을 검사했다. 세 archived 실행의 양 leg 물리 자료를 **후보 계약의 CPU fixture**로 검사했으며 역사 판정을 변경하지 않았다. old/new adapter의 기존 반환 필드도 전부 일치했다. 이 후보 fixture를 실제 새 run raw나 인증 파일로 저장하지 않았다.

기존 GC3·identity6·I/O/receipt5 및 supplier/render graph5 검사도 PASS([GC](construction_site_gc_cpu_20261101_v21.log), [identity](construction_site_identity_cpu_20261101_v21.log), [I/O](construction_site_io_cpu_20261101_v21.log), [graph](construction_site_graph_cpu_20261101_v21.log)). 신규 source memory compile PASS. [known-lock 검사](construction_site_known_locks_20261101_v21.json)의 알려진 9개 hash/count subset PASS이며 전체 과학 readiness는 인증하지 않는다.

[실행 전 audit](construction_site_prelaunch_audit_20261101_v21.json): 과거 1,072항목·새 prepared inputs·v19b 공통 입력 불일치 0, GPU는 기존 rustdesk만, Kit/training 점유 0. baseline 두 sidecar도 일치. Isaac Sim5.1의 실제 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, perception `sdg_tools`, ROS jazzy/domain191/`rmw_fastrtps_cpp` 유지. 원래 engineering start XY (−25.88797768,27.4)m, seed261022, 수동 ROI 정책, 5mm/2도/quiet·TF .5wall/.1sim·GC600초/증가768MiB/절대8GiB를 유지했다. 전체 renderer dependency closure와 미기록 과거 환경의 완전 소급 인증은 v20과 같이 UNKNOWN이다.

오프라인 개발 실패도 보존한다. 최초 replay는 존재하지 않는 executed adapter snapshot 경로 조회로 실패했고(재실행도 같은 오류), 동결된 transitive source의 실제 경로로 해결했다. 확장 archived 검사 첫 두 판은 시작 phase 제한과 PRE 인증 뒤 자료까지 포함한 잘못된 fixture 시간창 때문에 실패하여 로그 v02/v03을 보존했다. 후속 v04 및 최종은 20/20 PASS다. persistence 변경 직후 compile은 들여쓰기 오류 1회로 실패했고 실행 전에 수정·재검사했다. 비Git 디렉터리의 git status, 탐색 중 존재하지 않는 후보 파일 조회도 성공 검사로 계산하지 않았다. 이들은 Kit 시도나 연구 denominator가 아니다.

## 4. 새 engineering 실행

새 root는 `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_STOP_LIFECYCLE_20261101_v21_01`, 새 Kit PID1587403 및 `attempt_0001` 한 번이다. [runner 출력](construction_site_runner_20261101_v21.log), [독립 증거·환경·인증](construction_site_stop_proof_20261101_v21.json), [물리 속도/조향](construction_site_motion_bounds_20261101_v21.json), [보존 인덱스](construction_site_final_audit_20261101_v21.json)를 저장했다. 실행 명령은 다음과 같다.

```bash
python3 scripts/construction_site_perception_runner_20261101_v21.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_STOP_LIFECYCLE_20261101_v21_01
/home/user/anaconda3/bin/python3 scripts/construction_site_perception_runner_20261101_v21.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_STOP_LIFECYCLE_20261101_v21_01
```

CPU 재현은 `python3 analysis/construction_site_stop_replay_20261101_v21.py`, 회귀검사는 `python3 analysis/construction_site_stop_test_20261101_v21.py`로 먼저 수행했다. 이 도구들의 기존 출력 경로는 exclusive-create이므로 이 기록을 덮어쓰는 재실행을 하지 않는다. 실제 실행 중 새 RGB를 직접 열어 팔레트 top polygon `[(236,197),(251,181),(383,181),(403,197)]`을 지정하고, 새 overlay도 직접 검토한 뒤 현재 RGB/overlay SHA와 `manual_roi.json`/`roi_review.json`을 결합했다. 이전 pose/target/depth를 복사하지 않았다.

fresh HR YOLO confidence .719590545, B4 heading90.011093°, B5 `COMPUTED`, center(−25.934830108,30.481785554)m였다. 새 PRE/FINAL은 각각(−25.934830108,28.278040523), (−25.934830108,29.078040523)m다. task yaw90°의 기존 역할과 B4 heading을 구별하고 USD GT를 commanded target으로 넣지 않았다. 새 RGB SHA `b0c90f49f2630b45b69f79573085e8f293a8b27f9ef5a14f7e9647dfcd286e30`; depth SHA `d17d0fe06e507a7718ba90723be945a07151b2a627f278d7a0bc918548be3e3d`. 고정 장면에서 depth 내용 hash가 v20과 같은 사실은 동일 관측 copy의 증거도 새 획득의 단독 증거도 아니다. 새 Kit/capture annotator 실행과 capture 결과·RGB·inference/ROI hash 결합을 함께 근거로 한다. **수동 ROI 보조 B5**이며 완전 자율 pallet 인식으로 주장하지 않는다.

| 실제 새 증거 | PRE | FINAL |
|---|---:|---:|
| 실제 도달 및 정상 stop certificate | PASS | PASS |
| 실측 종점 거리 | 2.723096mm | 2.887923mm |
| 실측 yaw 오차 | −.037820° | −.039664° |
| 정상 stop 요청 sim초 | 67.183336837 | 123.883339794 |
| 첫 정상 ZERO sim초 | 67.233336840 | 123.883339794 |
| 새 quiet 창 sim초 | 67.250003507–68.250003560 | 123.916673129–124.916673182 |
| quiet coverage | 1.000000052초 | 1.000000052초 |
| quiet root / FD peak | .546573 / 1.029968mm/s | 1.356805 / 1.258850mm/s |
| quiet pose span | .009726mm | .022888mm |
| full-rover curve sweep / live wheel support | PASS / 48060개 PASS | PASS / 43740개 PASS |
| 별도 비영 BRAKING command 수 | 1 | **0** |

PRE는 update1250/step4029에서 surface .000448656230m/s를 반환한 BRAKING, update1251/step4032에서 zero라는 두 호출이었다. **FINAL은 update1112/step7430 한 호출**에서 ordinal0 `MOVING→BRAKING/NORMAL_STOP_REQUEST`, ordinal1 `BRAKING→ZERO_SETTLING/GOVERNOR_NORMAL_OUTPUT_ZERO`를 모두 기록했다. governor 요청·surface/wire 출력은 0이며 정상 output 감속률은 −.052070690m/s²다. 별도 비영 제동 명령이나 지속시간을 만들지 않았다. 즉, 두 종류의 실제 전이 경로를 이번 한 PRE→FINAL에서 각각 직접 검증했다. FINAL 인증은 PRE quiet를 재사용하지 않았다.

실제 pulse base 누적 경로 **1.680723306m**, 순변위1.675680130m, 비영 command2361개였다. 6개 실제 wheel 모두 q span12.5639–12.5658rad 및 비영 dq를 기록했고 peak1.356681rad/s였다. 물리 planar peak .029738332m/s로 기존 .03m/s 차단선 아래, 실측 steer peak15.714018°로 기존20° 물리 guard 아래였다. pulse 기록7,210샘플의 sim120.166673초/wall324.914397초는 중간 PRE 정지·FINAL 검사도 포함하며 순수 이동시간으로 쓰지 않는다. 모든 pose/q/dq·wire·graph/controller readback·contacts는 원자료에 보존했다. 정지 RGB-D 외의 실제 주행 영상은 새로 생성하지 않았다.

[독립 post-exit 증거 검사](construction_site_stop_proof_20261101_v21.json)에서 driver endpoint88,812행, session7,375행을 **원래 guard로 처음부터 재생**, 두 leg에 걸친 publisher/GID pin·TF·순서 오류0이었다. 두 stop certificate도 raw physics와 실제 command로 다시 계산해 저장 certificate와 **정확히 일치**했다. post-exit CPU verifier는 PRE .09845초/FINAL .09158초였다. 실제 실행 driver TF wall age 최대328.103ms, session308.305ms, driver sim age16.667ms로 원래 .5wall/.1sim 한도를 유지했고 TF/GID fault0이다. 검증 추가 후의 이 관측 시간을 v19b의 더 짧은 latency나 일반적인 timing 보장으로 바꾸어 해석하지 않는다.

접촉 원자료50,918건 중 예상 밖 접촉·주행 shell 침투/하중 **0**. GC 제한 scope329.710084wall초, guard 관측 peak RSS7,181,115,392bytes/증가577,691,648bytes로 기존 한도 이내, paused 복원 후 automatic GC=true·active=false·freeze0이다. fault ZERO-ONLY recovery 샘플0이며 cleanup quiet를 정상 도착에 사용하지 않았다. driver는 `completion_accepted=true`, 정상 zero20회 후 exit0; 별도 cleanup 요청ID/hash/time 결합 zero10 receipt PASS. driver1590146/observer1588393/Kit1587403 모두 exit0·PID 소멸, 강제 종료·추가 Kit·자동 retry0이다. provisional eligible=true·digest/evidence hash PASS 후 outer가 `ENGINEERING_RECORDED`를 확정했고 runner도0이다.

실제 환경은 kernel6.14.0-37-generic, RTX5090/driver570.172.08, Kit/perception Python3.11.15, ROS Python3.12.3이다. 실제 inference versions는 torch2.7.1+cu128/ultralytics8.4.129/numpy2.4.6이며 설치·upgrade0. 상세 binary SHA·GPU UUID·source/prepare manifest SHA는 독립 proof JSON에 있다. `code_versions.json` SHA는 `f9b83d037ed2686aa35b18090a9aea75aea71434a0306cb9e1229b063abf6992`, prepare manifest SHA는 `f2b407bb45d679d7168c5cf1099d033a52daacaa3028cf5efcef9d7a865cd523`이다. 원본 scene SHA는 기존 `865bb3fd13189bfc4d9e51124828cc646b209ddb06ca5e3412b0e0ef232fd978`과 일치한다.

## 5. 보존, 변경 파일과 최종 결정

최종 audit는 과거1,072항목 불일치0, 신규 prepared84개 불일치0, v19b 공통 입력 불일치0 및 새 run186파일 hash를 기록했다. 실행 Python snapshot80개를 보존했다. [2026-11-02 이어서 완료한 보존 검사](construction_site_resume_preservation_20261102_v21.json)는 이 hash들을 다시 확인하고 재개 후 추가 Kit0을 기록한다. HPO/training 프로세스0, 기존 rustdesk 보존. 과거 v19b `ENGINEERING_RECORDED`와 **v20 두 runner exit1/FAIL 0/2**를 수정하지 않았다.

새 runtime 파일은 `scripts/construction_site_drive_ros_20261101_v21.py`, `construction_site_perception_session_20261101_v21.py`, `construction_site_perception_runner_20261101_v21.py`와 `evaluation/construction_site_stopping_adapter_20261101_v21.py`, `construction_site_stop_certificate_20261101_v21.py`, `construction_site_persistence_20261101_v21.py`다. 새 analysis 파일은 replay/test/audit/proof 및 기존 분석을 별도 출력에 연결한 summary/evidence_check v21 총6개다. 이 보고서·보조 JSON/log·`reports/latest_report.md`·`docs/PROJECT_STATE.md`를 작성/갱신했다. 원본/기존 source·locks·weights·USD·v01–v20 결과를 보존했고 bulk data는 외부 run root에 둔다. Git stage/push·외부 publish0이다.

| 결정 항목 | 판정 |
|---|---|
| stop-certificate interface 수정 검증 | **PASS**: 정확한 replay·CPU20·실제 두 전이 형태·outer 독립 재검증 |
| 새 PRE 물리 도달 | **YES**, 2.723096mm |
| 새 FINAL 물리 도달 | **YES**, 2.887923mm |
| 정상 stop·zero·각 leg 새 quiet | **PASS / PASS** |
| 새 v21 실제 engineering denominator | **1/1**, retry0; v20은 그대로0/2 |
| 다음 scientific pilot ready? | **아직 NOT_READY**: engineering stop gate는 통과, 공통 조건의 작은 과학 pilot admission 명세/명령은 미작성 |
| HPO / 정식 과학 denominator | **PAUSED / 0** |

새 계약의 offline 결정성과 이번 bounded 실제 작동은 입증했다. 수정 버전의 실구동은1회이므로 장기 반복 성공률·다른 장면·실로봇 재현성을 인증하지 않는다. scientific readiness 전체와 renderer dependency closure의 UNKNOWN도 남는다. 새로운 관찰 실패 blocker는 없으며 이번 범위의 정지 불일치는 해결됐다.

다음 구체 작업은 **실험 실행 전에**, 동결된 HR_Scan/LR_Scan/Proxy/GeoCAD별 checkpoint·asset과 paired scenario를 매핑하고 RGB-D 획득·관측/ROI 도움·B4/B5·controller·정지/안전·timeout·실패 denominator가 공통인 작은 scientific pilot admission 명세와 명령을 작성하는 것이다. LR은 reduced acquisition 조건의 독립 재구성으로 유지하고 CAD=GeoCAD/Proxy를 혼동하지 않는다. representation×load completeness×occlusion의 수준·표본 수를 이번 결과로 새로 잠그거나 tuning하지 않는다. Real Test189는 recipe locking 후 이미 평가된 자료이며 tuning 재사용0; real external validation은 red-only로 cement·실로봇 배포에 일반화하지 않는다. 이번 작업에서 HR/LR/CAD 실행·training·432 confirmatory는 시작하지 않았다.
