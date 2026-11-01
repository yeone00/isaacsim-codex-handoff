# 현장 단일 로버 v06 — 레이캐스트 수정 PASS, 이동 FAIL(TF_STALE)

2026-11-01 KST. **MOVED NO / 실제 변위 0m / 비영 명령 0 / 주행 후 STOPPED NOT_TESTED**. 사용자의 첫 실제 이동 목표를 달성하지 못했다. 바퀴 회전도 관측 최대 dq=0rad/s다. 연구 denominator=0, HPO·GPU training PAUSED, Full E2E NOT_YET_VALIDATED.

| 항목 | 실제 결과 |
|---|---|
| Kit 세션 / 측정 주행 시도 / 진단 수정 재확인 | 2 / 0 / 1 |
| 첫 진단 | FAIL, RaycastHit dict 접근 예외 후 독립 지지 계산 지연; supervisor 제한 시간 종료, child -9 / runner 1 |
| 수정 재확인 | NOT_READY, TF_STALE; native child 0 / runner 1 |
| 수정 재확인 실제 물리 | 378 steps / 6.300000328571s |
| 첫 진단 마지막 저장 물리 | 257 steps / 4.283333556727s; 종료 시 최종 summary 없음 |
| 최초 비영 명령 / commanded speed / ROS driver | 없음 / 발행 없음 / 미생성 |
| base signed forward / net XY / 최대 forward | 0 / 0 / 0m |
| 명령 후 ROS zero / 정지 hold | NOT_TESTED / NOT_TESTED |
| 기존 보수적 장애물 sweep | PASS, 0.10m 여유·±2°·기존 이동 envelope 유지 |
| 실제 support ray | **2,214/2,214 PASS**, 여섯 wheel contact 경로 일치 |
| shell ray | **9/9 PASS**, 최소 gap 70.647287mm |
| shell 실제 contact | 144점, 최소 separation +78.864306mm, 최대 impulse 0Ns |
| baseline quiet | PASS; 주행 후 정지 판정으로 사용하지 않음 |
| 최종 연구용 인증 | NOT_YET_VALIDATED |

레이캐스트 결함은 실제 API 사용 오류였다. 설치된 `omni.physx`의 `raycast_all` callback은 dict가 아니라 `RaycastHit` 객체를 준다. 기존 `hit.get(...)` 및 `hit[...]` 사용은 AttributeError를 냈다. 첫 v06 계측도 같은 잘못된 dict 접근을 남겨 실패했으며, runtime.log의 예외와 첫 코드 snapshot을 보존했다. 이 실패를 바닥 부재로 해석하지 않는다. 설치된 pyi의 `RaycastHit`, `SceneQueryHitLocation`, `SceneQueryHitObject`를 확인한 후 `.collision`, `.position`, `.normal`, `.distance`, `.rigid_body` 속성 접근으로 고쳤다. callback은 True를 반환해 traversal을 계속한다.

수정 재확인에서는 현재 여섯 바퀴 중심 tread XY에서 각각 단면/양면 2개씩, shell 중심의 알려진 site floor 대조 ray 2개, **총 14개 bounded raw ray**를 저장했다. 원점·방향·길이·반환 bool·모든 필터 전 hit·normal·distance·rigidBody·collisionEnabled·수락/거절 이유·callback 미호출 여부가 `raycast_raw_diagnosis.json`에 있다. 14개 모두 bool True 및 callback 2회였다. 대표 전륜 ray origin=(-26.172473673,28.820257187,0.033963821), direction=(0,0,-1), length=.08m에서 실제 바닥 hit Z=-.006157368m, distance=.040121187m가 수락됐다. ray 원점이 wheel 내부인 self hit(distance0)는 별도 거절되고 바닥 hit는 계속 수집된다.

실제 수락 경로는 composed site mesh `/World/ConstructionSite/Env/cb5ce5926fdd4ce2b8f8f548239dcfaf/cb5ce5926fdd4ce2b8f8f548239dcfaf`이다. 원본 usdz의 `/World/Env/...` alias와 구분했다. 관련 10개 face의 world winding normal Z≈+.999987, orientation=rightHanded, doubleSided=False, collisionEnabled=True를 기록했다. 기본 bothSides=False에서도 모두 맞았고 양면 비교 결과도 같으므로 **path filter·ray 방향/길이·winding은 이번 실패 원인이 아니다**. 원본 mesh나 sidedness를 바꾸지 않았다. 독립 contact+mesh fallback은 수정 재확인에서 사용하지 않았다. ray 검증 성공이 주행 성공이나 연구용 인증을 의미하지 않는다.

최종 중단은 session isolation admission의 **TF_STALE**이다. 긴 정적 support 계산 후 기존 대기 조건은 `tf_count>=3`인 과거 TF를 즉시 채택했다. 실제 guard 입력의 TF wall age는 **7.206363678s**, observer status age는 0.028938055s, TF↔physics 차이는 0.016666668s였다. 즉 observer가 죽었다거나 ROS topic이 없었다는 증거가 아니라, 갱신된 status 안의 오래된 TF를 신선한 TF처럼 채택한 admission 결함이다. endpoint 원본은 `session_endpoint_forensics.jsonl`에 보존했다. 예외 뒤 물리를 120 update 더 진행하며 TF가 갱신됐지만 drive branch로 복귀하지 않았다. PUBLISHER_SET은 NOT_TESTED이며 성공/실패를 주장하지 않는다.

종료 후 **같은 기존 대기 루프가 guard와 동일한 .5s wall/.1s sim 신선도에 도달한 TF만 채택하도록 최소 수정**했다. frozen guard와 시간 기준은 바꾸지 않았다. 실제 stale snapshot 거절·fresh snapshot 수락·sim .2s stale 거절 및 compile PASS. 이 마지막 TF 대기 수정은 **runtime NOT_TESTED**다. 실행 당시 두 코드 snapshot과 SHA를 attempt별로 보존하고 `code_versions.json` 및 `post_run_static_revision.json`으로 현재 코드와 구분했다. 추가 Kit launch는 하지 않았다.

공급자 graph는 기존 BENCH `/World/ROBOT_TASK/RuntimeRover/ActionGraph` reference를 새 overlay에서 재사용했다. derived subscribe node는 namespace 빈 문자열/topicName=`rover/cmd_vel`이며 실제 endpoint는 `/rover/cmd_vel`이다. 기존 세 articulation controller의 targetPrim은 모두 `/World/ENG_FE2E/Rover/base_link`다. ROS2 Bridge 및 Wheeled Robots startup을 runtime log에서 확인했다. 설치 환경은 Isaac Sim5.1/hh_isaac51, ROS Jazzy/domain191이며 공급자 안내의 Humble을 새로 설치하지 않았다. 기존 linear.x×15 및 drive contract를 바꾸지 않았다. **Twist 도착→physical wheel→base 이동은 이번에도 미검증**이다.

첫 진단에서는 callback 오류를 확인한 뒤 해당 세션의 `abort_motion`을 설정해 비영 명령을 차단하고, 소유 observer에만 종료 marker를 썼다. 독립 mesh 지지 계산이 오래 걸려 기존 supervisor의 180s abort/210s 종료 경로에 도달했고 child -9로 끝났다. 최종 contacts/execution_complete가 없는 불완전 실패도 그대로 남겼다. 사용자 기존 프로세스 중지·GPU reset 없음. 수정 재확인에서는 정상 observer exit0, driver null, timeline pause 및 graph velocity/effort zero cleanup이 기록됐다. ROS zero 발행 증거는 없으므로 cleanup 요청을 STOPPED로 부르지 않는다.

실행 명령:
```bash
python3 scripts/construction_site_drive_runner_20261101_v06.py --prepare-only
python3 scripts/construction_site_drive_runner_20261101_v06.py --run
python3 scripts/construction_site_drive_runner_20261101_v06.py --run --correction-recheck
```

새 외부 출력은 `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_SINGLE_ROVER_MOBILITY_20261101_v06`다. 두 세션 모두 시작 전 active Kit/training 없음, GPU compute는 기존 rustdesk535MiB만 있었다. 종료 후 Kit/runner/session 프로세스 없음. 첫 prepare 및 correction 전 실제 input hash gate PASS. 종료 후 원본 stage·원본 controller scene·기존 v04 코드 5개 총7개 SHA 보존 PASS; 새로운 v06 코드 수정은 별도 version manifest에 기록했다. 이전 v01–v05 출력/원본 stage/체크포인트/잠금/연구 threshold 수정 없음.

변경 파일: 새 `scripts/construction_site_drive_runner_20261101_v06.py`, `scripts/construction_site_drive_session_20261101_v06.py`, 이 보고서, `reports/latest_report.md`, `docs/PROJECT_STATE.md`. 검사는 prepare corridor/graph, typed-hit callback AST spot check, fresh-TF 회귀3개, py_compile PASS다. summary 생성기의 첫 괄호 SyntaxError(exit1)는 runtime과 별개로 수정 후 재실행했으며 기록에서 숨기지 않는다. 프로세스 확인 rg exit1은 일치 프로세스 없음이다.

증거는 외부 root의 `prepare.json`, `correction_prepare.json`, 두 runtime log/run_status, `measurement_summary.json`, `final_verification.json`, `code_versions.json`, `post_run_static_revision.json`; attempt_0002의 raw rays/support/shell/graph/endpoint/contacts/physics_steps/steps/root_trajectory/runtime_summary/execution_complete다. 실제 q/dq·base world pose는 steps.jsonl에 있다. 첫 세션 실패와 수정 재확인 실패를 합격이나 연구 분모에서 숨기지 않았다(별도 engineering 세션2, research0).

다음 구체적 행동은 **수정된 fresh-TF 대기로 새 미사용 출력에서 기존 ROS 경로의 짧은 pulse→측정 zero/stop 한 번을 실제 검증**하는 것이다. 현재 주행 지지 장애는 해소됐고, 남은 입증 대상은 ROS admission과 실제 구동이다. 이번에는 추가 재시도·HPO·B4/B5·Full E2E·EngineeringFloor·새 planner·스크린샷·teleport를 하지 않았다.
