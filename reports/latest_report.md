# PUBLISHER_SET 집중 진단 — 2026-10-21

**ROOT_CAUSE_UNKNOWN / 진단 보강 완료 / runtime 미실행.** 실제 v01 attempt의 모든 JSON·JSONL·stdout 로그를 읽었다. `execution_complete.json`은 session v01:153 → guard v01:23, discovery에서 PUBLISHER_SET이며 motion_attempts=0이다. driver도 wall_s=1792548135.0291867에 같은 오류를 기록했다. 그러나 정확한 실패 입력 `names`는 저장되지 않았다. observer는 ros_status.json을 0.1초마다 교체하며 ros_observed.jsonl에는 TF273행·cmd_vel30행뿐이고 endpoint 이력이 없다. 남은 ros_status.json의 wall_s=1792548135.3445156은 driver fault보다 0.3153289초 늦다. 그 최종 snapshot의 names는 `["eng_smoke_observer"]`, namespace `/`, 조회 topic `/rover/cmd_vel`, type `geometry_msgs/msg/Twist`, GID `[1,15,113,9,77,162,171,17,0,0,0,0,0,0,21,3]`이며 저장 TF시각 기준 v01 discovery 검사를 통과한다(ready=False). 이는 실패 snapshot 재현이 아니다. isolation snapshot의 publisher=[]와 허용 TF1/subscriber2도 이후 discovery의 정당성을 증명하지 않는다. 실패한 AND 조건에서 확정 가능한 것은 이름 중복 또는 허용집합 밖 이름 중 적어도 하나뿐이다. namespace/type/GID 자체는 해당 assertion 다음 줄에서 검사되므로 단독으로 그 오류를 설명하지 못한다. 외부 publisher 이름·GID나 합법적 중복 endpoint였다는 주장은 UNKNOWN이다. 기존 출력은 PROCESS_EXIT_CODE=1, internal_status=NOT_READY, MOVED=NO, QUIET=PASS(정지 baseline), zero=NOT_READY, RESEARCH_E2E=NOT_ASSESSED로 유지한다. 과거34.127288744mm 후퇴/QUIET FAIL도 그대로다.

새 파일은 `evaluation/legacy_supervised_guard_v02.py`, `scripts/legacy_supervised_{session,ros,observer,one_shot,offline_checks}_v02.py`, `scripts/legacy_supervised_sources_v02.json`, 이 보고서와 checks JSON이다. session/driver는 검증 **직전** 별도 `session_endpoint_forensics.jsonl`/`driver_endpoint_forensics.jsonl`에 정확한 snapshot·names·phase·wall/sim·이전 pinned identity를 append/flush/fsync한다. observer v02는 각 endpoint의 실제 조회 topic을 명시한다. 허용 node/cardinality/GID 정책은 v01을 상속하여 그대로 유지하며, 같은 node의 distinct GID 둘도 계속 거부한다. 근거 없는 endpoint 병합/허용 확장은 하지 않았다. topic 일치, 이미 관측한 observer 소실, driver 최초 등장과 등장 후 소실(소실은 zero만 허용), active 이후 discovery 회귀도 fail closed다. 기존 graph/physics/controller/감속/abort/threshold 경로는 바꾸지 않았다. 새 wrapper는 v02 경로와 17-entry SHA manifest를 사용하며 원래 v01 pin도 검증한다. [검사 증거](legacy_supervised_publisher_set_hotfix_20261021_v01_checks.json): 집중18개·기존21개·compile6개 PASS, 기존 manifest11개 SHA PASS, 실제 기존 출력37파일의 전후 SHA/파일집합 동일 PASS. 실제 실패 자료와 최종 snapshot의 비재현성, distinct-GID 중복/foreign node·publisher/topic/type/namespace/GID 교체/stale·소실/정상 phase 전이/오류 전 forensic 보존을 검사했다. 최초 fixture 예상 오류명 불일치는 FAIL로 기록 후 foreign endpoint 추가 fixture로 수정했다. Git status는 저장소가 아니므로 FAIL이며 stage/commit 없음. 원인 해결 여부·runtime admission·MOVED/QUIET 성공은 UNKNOWN이다. 다음은 사용자가 별도로 승인할 때만 아래 **한 번의 진단 보강 simulator-only 시도**이며, 원인 해결 완료로 취급하지 않는다. 미사용 output과 console 경로를 고정하고 충돌 시 중단한다. 외부 publisher가 포착되면 계속 차단하고 그 identity의 domain 격리/매칭을 먼저 해결한다. 자동 retry/sweep, HOLD K1/direct signed pulse, Full E2E/QUAL12/432는 실행하지 않으며 연구분모0이다.

별도 사용자 승인 후 사용할 단일 명령(이번 세션 미실행):

```bash
(
  cd /home/user/hh/IsaacSim_Codex_Starter_20261013/isaacsim_asset_representation_20261013 || exit 1
  set -o noclobber
  exec 3> /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_HOTFIX_20261021_v02.console.log || exit 1
  export ROS_DOMAIN_ID=191 RMW_IMPLEMENTATION=rmw_fastrtps_cpp ROS_DISTRO=jazzy
  export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}:/home/user/anaconda3/envs/hh_isaac51/lib/python3.11/site-packages/isaacsim/exts/isaacsim.ros2.bridge/jazzy/lib"
  /usr/bin/python3 scripts/legacy_supervised_one_shot_v02.py --output /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_HOTFIX_20261021_v02 >&3 2>&1
  run_rc=$?
  printf '\nPROCESS_EXIT_CODE=%s\n' "$run_rc" >&3
  cat /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_HOTFIX_20261021_v02.console.log
  exit "$run_rc"
)
```

감독자는 실행 중 새 root의 `runtime_stdout.log`와 옆 `.console.log`를 확인한다. wrapper의 simulator launcher는 기존 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, ROS child는 source된 Jazzy `/usr/bin/python3`이며 domain191 빈-domain probe와 atomic root mkdir를 유지한다. wrapper는 runtime argv/env/input hashes, OS child exit, supervisor_complete.json internal_status, attempt execution_complete.json/outcomes를 수집한다. 종료 코드0만으로 성공 판정하지 않는다. 준비할 사용자 중단 명령(새 attempt가 있을 때 파일 요청만 수행):

```bash
test -d /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_HOTFIX_20261021_v02/attempt_0001 && touch /home/user/hh/isaac_cosmos/sdg_final/FE2E_V02_LEGACY_SUPERVISED_HOTFIX_20261021_v02/attempt_0001/abort_motion
```

Ctrl-C도 기존 abort/zero 요청 경로를 사용한다. 프로세스 종료는 물리 quiet 증거가 아니다. 새 시도도 MOVED/QUIET/RESEARCH_E2E를 각각 판정하고, 실패 출력은 삭제하거나 재시도하지 않는다.
