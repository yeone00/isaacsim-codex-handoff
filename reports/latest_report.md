# 현장 perception → PRE → FINAL v19 — 2026-11-01

**실제 체인 완료: 두 번째 실행 ENGINEERING_RECORDED, PRE_REACHED=true, FINAL_REACHED=true.** Fresh mounted RGB-D → frozen HR YOLO → B4 → 수동 ROI 보조 B5 → 새 관측 PRE/FINAL → 실제 ROS 조향 PRE 정상 정지 → 측정 정지 자세에서 독립 FINAL 경로 검증 → 실제 FINAL 정상 정지를 완료했다. 5mm 위치·2° yaw·ZERO 이후 실제 quiet ≥1초 기준을 유지했다. 첫 실행의 TF_STALE/FINAL 미도착은 NOT_READY로 보존했다. Kit 총2회, 추가0회. HPO/training PAUSED, 연구 denominator0, HR/LR/CAD 비교·confirmatory/432 실행0.

## 실제 결과

외부 output root는 `/home/user/hh/isaac_cosmos/sdg_final/` 아래 다음 두 개다. 각각 새 `attempt_0001`만 사용했다.

| 항목 | `CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v19_01` | `CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v19_02` |
|---|---|---|
| 실행 코드 | v19 | v19b: GC 제한 지연, 완료 응답 대기 수정 |
| PRE_REACHED | **true**, 정상 BRAKE→ZERO | **true**, 정상 BRAKE→ZERO |
| PRE 위치 / yaw 오차 | 2.759mm / −0.03425° | 2.856mm / −0.03452° |
| PRE quiet | PASS, 1.000000052초 | PASS, 1.000000052초 |
| FINAL_REACHED | **false** | **true**, 정상 BRAKE→ZERO |
| FINAL 위치 / yaw 오차 | 마지막 측정 약6.95mm / 도착 미입증 | **2.894mm / −0.03435°** |
| FINAL quiet | 비상 ZERO-ONLY quiet와 구분 | **PASS, 1.000000052초** |
| 실제 pulse 누적 경로 | 1.676356m | 1.680854m |
| 실제 비영 command 기록 수 | 2344 | 2344 |
| 차단 / 정상 완료 | driver TF_STALE → TWO_LEGS_INCOMPLETE | completion_accepted=true, fault=null |
| 사후 비상 quiet | 새61샘플, ZERO-ONLY PASS | 비상 복구 없음 |
| 예기치 않은 접촉 / shell 침투·하중 | 0 / 0 | 0 / 0 |
| 별도 cleanup 요청 결합 zero10 | PASS | PASS |
| driver / observer / Kit exit | 0 / 0 / 0 | 0 / 0 / 0 |
| outer final / runner exit | NOT_READY·MISSING_WITNESS / 1 | **ENGINEERING_RECORDED / 0** |

두 번째 실행의 관측 목표는 PRE `(-25.93480444460404, 28.278040544572605)`, FINAL `(-25.93480444460404, 29.078040544572602)`m다. PRE 정지 측정 world pose는 `[-25.934833526611328, 28.275184631347656, -0.009073960594832897, 1.5701938757113014]`, FINAL 정지 측정은 `[-25.934341430664062, 29.075183868408203, -0.005458937957882881, 1.5701967482995547]`이며 순서는 `[x_m,y_m,z_m,yaw_rad]`다. 종료 직전 추가 물리 관측 pose도 `[-25.934341430664062,29.07517433166504,-0.005459004081785679,1.5701967460715578]`로 보존했다.

PRE 인증 quiet 창의 COM/root/FD 최대 속도는 각각 1.309/1.307/0.584mm/s, XY span 0.0268mm다. FINAL 인증 창은 1.834/1.834/0.801mm/s, span 0.0229mm다. 마지막 추가1초는 root 0.220mm/s·span0이다. 각 leg의 독립 certificate와 zero wheel/controller readback으로 검증했으며, 단순 이동이나 cleanup zero를 도착으로 계산하지 않았다. 기존 aggregate의 `outcomes.zero`는 첫 PRE zero를 가리키는 호환 필드이므로 FINAL 근거는 `leg_1_stop.json`·FINAL commands·outer 재검증이다.

## 짧은 offline replay와 종단 수정

README·PROTOCOL_LOCKS·최신 PROJECT_STATE·v18 보고서 및 실제 v18b `executed_code`를 확인했다. 실행 스냅샷과 로컬 소스 일치, v18_02 입력65개 불변을 확인한 뒤 저장 pose/yaw·waypoints·cross/along·signed curvature·속도를 재생했다. 원시 분석은 첫 root `cpu_regression_v19.json`의 replay 배열에 있다.

v18의 cubic 경로는 종점 yaw는 +90°지만 종점 곡률이 −0.251701/m였다. 실제 base의 측방 이동과 yaw 증가 관계를 구간별 최소제곱으로 비교하면 회전 기준점에서 base까지 전방 오프셋이 약0.339m이며, 구간별 0.333–0.340m로 일관됐다. base 위치를 회전 기준점처럼 추종하면 조향 중 base의 측방 속도를 누락한다. 기존 추종은 약20mm 측방 잔차가 쌓였다가 종단에서 반대쪽으로 빠졌다. 마지막3cm에서는 이미 약6.25mm 측방 오차였고, 최소거리8.677mm에서 normal stop이 발동하지 않았다. 최소 회전반경 약2.612m에서 남은 짧은 전진거리만으로 해결할 접근이 아니었다. 8mm/s 하한도 endpoint 통과를 계속시켰다. v18에는 정상 BRAKE 진입 자체가 없었으므로 brake hysteresis가 주원인이라는 증거는 없다.

새 v19는 같은 국소 Hermite 방식에서 rear 기준점을 사용하고, BASE XY/차체 yaw로 변환한 경로를 기존 full-rover sweep에 넘긴다. quintic의 양 끝 곡률은0이다. 목표 PRE/FINAL은 바꾸지 않았다. replay에서 산출한 engineering 오프셋0.338m, 측방/heading feedback12·6(기존2.5·3.2), 속도 `min(.02,max(.004,.12*along))`를 명시적으로 적용했다. 3mm 정상 stop trigger는 유지했고 supplier steering encoding·stiffness·KMAX·governor/StoppingAdapter는 그대로다. PRE 계획 최대곡률 약0.349/m는 실제 KMAX0.382785/m 이내이며, 새 경로 admission은 0.95*KMAX 상한을 사용한다(기존 경로의0.80 여유와 구분). CPU 모델은 오프셋0.328/0.338/0.348m에서 모두 2.80–2.85mm의 정상 제동 진입을 예측했다. 이는 물리 PASS 대신 사용하지 않았고 실제 두 실행에서 정상 PRE 정지를 확인했다.

두 번째 실행의 PRE full rover 곡선 sweep와 live wheel support48060/48060 PASS, PRE 정지 후 새 pose에서 FINAL sweep와43740/43740 PASS다. original site·공급 ROS ActionGraph·실제 GID/TF·graph/render allowance·actor cache·contact·shell 보호를 유지했다. RGB와 ROI overlay를 각 실행에서 직접 보고 해당 fresh RGB hash에 ROI/review를 결합했다. 동일 픽셀 polygon을 사용했지만 과거 RGB-D·목표·pose CSV를 재사용하지 않았다. frozen checkpoint SHA256는 기존 `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`와 일치하며 target 생성에 USD GT를 넣지 않았다.

## GC와 fault-zero 생명주기

v19 첫 시도는 매 tick allow JSON load·반복 baseline normalization을 없애고 같은 graph 비교를 cache했다. 물리 정지 상태에서 precollect/freeze하되 자동 GC는 유지했다. 그러나 새 기록 객체의 gen2 수집이 readback 구간에서 **558.984ms** 멈췄다. driver의 실제 TF age0.502374초로 guard가 차단했다. 첫 시도는 timing 해결 FAIL이며 실패를 보존했다. fault latch 후 driver exit0, 해당 비상 요청에 결합한 zero 영수증, 원래 identity/GID·graph·actor·contact 및 zero targets 확인 뒤 ZERO-ONLY 물리61샘플을 새로 관찰해 quiet PASS를 얻었다. 비영 재인가 없음.

확인된 GC 원인에 한해 마지막 v19b 시도에서 cyclic GC를 주행의 엄격한 제한 구간에만 지연했다. reference counting은 동작한다. 정지 상태 precollect 후 진입, 최대600초·RSS 증가768MiB·절대8GiB를 매 tick 검사하고 위반 시 fault 처리한다. 독립 ROS driver/observer의 실제 TF wall≤0.5초·sim≤0.1초와 identity/GID 검사는 그대로이며, 별도 프로세스 driver가 첫 시도에서 실제 stale을 차단했다. finally에서 timeline.pause 이후 GC를 반드시 복원한다. CPU 시간초과·메모리초과 예외 복원 검사를 수행했다.

실제 지연 구간297.738초, RSS 시작6,665,392,128 bytes, peak7,211,487,232 bytes(증가 약521MiB), 복원 시 자동GC=true·active=false·freeze count0다. 이번 pulse_start부터 마지막 물리 샘플까지 GC0/1/2 pause는 모두0건이다. active guard 최대52.713ms, graph 비교2.140ms, actor 증분4.745ms, physics update31.084ms, readback/직렬화33.020ms다. driver TF age 최대78.994ms·sim16.667ms, session age42.778ms였다. Startup/정지 구간의 GC는 별도이며 전체 session GC 최대258.287ms를 숨기지 않았다. **이 한 번의 engineering 통과는 미래 timing 보장이 아니다.**

GOAL_OVERSHOOT/PATH_TRACKING_ENVELOPE/OBSERVED_GOAL_NOT_REACHED 등 명시적 제한 fault를 zero-only eligibility에 추가했다. 기존 driver 종료·진짜 request-bound receipt·identity/actor/graph/contact·zero wheel/controller gate는 유지한다. identity/contact/graph fault는 여전히 거절한다. CPU eligibility 및 기존 zero identity/receipt 검사는 PASS다. 이번 실제 postfault 증거는 TF_STALE이며, 새 GOAL_OVERSHOOT eligibility의 실제 물리 발동은 NOT_TESTED다. 안전한 zero-only가 불가능하면 UNKNOWN/FAIL을 그대로 남긴다.

최종 leg의 완료 응답 대기에 leg 시작 후20초를 재사용하던 기존 코드는 실제 긴 FINAL 주행 후 대기를 건너뛸 수 있었다. v19b에서 정상 certificate 발행 후 새5초 응답 deadline으로 수정했다. 이번 driver가 정상 완료 certificate를 수락하고 exit0한 것으로 경로를 검증했다.

## 실행·검사·보존

실제 런타임은 `/home/user/anaconda3/envs/hh_isaac51/bin/python`, Isaac Sim5.1, ROS jazzy/domain191, perception `sdg_tools`다. 각 prepare/run 명령은 다음과 같고 실제 argv·환경·input hashes·스냅샷은 각 root에 보존했다.

```bash
python3 scripts/construction_site_perception_runner_20261101_v19.py --prepare-only
/home/user/anaconda3/bin/python3 scripts/construction_site_perception_runner_20261101_v19.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v19_01
python3 scripts/construction_site_perception_runner_20261101_v19b.py --prepare-only
/home/user/anaconda3/bin/python3 scripts/construction_site_perception_runner_20261101_v19b.py --run --output /home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_PERCEPTION_APPROACH_20261101_v19_02
```

CPU replay/오프셋 민감도·graph 비교·GC 예외 복원 PASS, lifecycle v19/v19b 각3개 PASS, 기존 zero identity6개·receipt5개 PASS, 신규 source compile PASS다. known-lock9 hash/count subset PASS이며 과학 전체 의존성 재인증은 아니다. v18 입력59/65개와 v19 입력70/73개 hash 불변 PASS, 양쪽 provisional digest·존재 evidence hash PASS다. v19_01 eligibility=false, v19_02=true를 보존했고 outer final은 실제 Kit 종료 후 독립 재검증했다. 양쪽 cleanup receipt는 각각 별도 request에 결합돼 있다. 강제 종료·추가 retry 없이 소유 PID가 모두 소멸했고, 최종 Kit/training process0·기존 rustdesk만 유지했다. 작업 디렉터리에 .git이 없어 stage/push는 하지 않았다.

신규 코드는 scripts의 `construction_site_perception_{runner,session}_20261101_v19.py`/`v19b.py`와 `construction_site_drive_ros_20261101_v19.py`, evaluation의 `construction_site_follower_20261101_v19.py`/`construction_site_runtime_20261101_v19.py`/`v19b.py`, analysis의 `construction_site_regression_20261101_v19.py`/`construction_site_lifecycle_test_20261101_v19.py`/`v19b.py`/`construction_site_summary_20261101_v19.py`/`construction_site_evidence_check_20261101_v19.py`다. 이 보고서, latest_report, PROJECT_STATE를 갱신했다. 원본 USD·supplier graph·model·protocol·v01–v18 source/output은 변경하지 않았다.

주요 근거는 각 root의 `actual_summary_v19.json`, `evidence_check_v19.json`, `attempt_0001/leg_{0,1}_stop.json`, raw steps/commands/contacts, fresh RGB-D/model/ROI/B4/B5, provisional/final과 exit log다. 두 번째 root의 `active_timing_v19.json`, `correction_basis_v19b.json`, `final_preservation_resources_v19.json`에 시간·수정 근거·보존 검사를 기록했다.

남은 UNKNOWN은 독립 반복 재현성, 다른 start/scene/representation에서의 타당성, 장시간 timing 일반 보장, 실제 로봇 적용이다. 이번 고정 현장 engineering chain 완료와 과학 비교 readiness는 구분한다. 다음은 이 v19b 실행 snapshot·명령·증거를 handoff 기준으로 고정하는 것이다. 추가 실행이나 HR/LR/CAD 확장은 별도 작업으로 다룬다. HPO/training은 PAUSED, 연구 분모0을 유지한다.
