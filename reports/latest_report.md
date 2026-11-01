# v28 HR pilot — ROI 가능, fresh B5 통과; 메모리 gate에서 주행 전 실패

2026-11-02 (Asia/Seoul). **정당한 팔레트 ROI는 가능했다. 새 HR RGB-D → frozen YOLO/B4 → 수동 ROI113점 → B5/새 PRE·FINAL 목표 생성까지 PASS. 실제 PRE/FINAL 주행은 모두 NOT_RUN.** Kit 정확히1회/RETRY0, engineering **0/1 FAIL**이다. 주행 전 기존 `GC_MEMORY_BOUND`가 중단시켰고, 이후 정상 Kit close도 실패하여 기존 runner watchdog이 강제 종료했다. 성공·clean exit로 해석하지 않는다. LR/CAD0, science denominator0, HPO/training PAUSED.

## 짧은 오프라인 진단과 공통 reviewer 규칙

v27 raw의 RGB/array/depth/YOLO mask/calibration/ROI/mask SHA를 기존 witness index와 대조했다. 모든 입력·원본 보존 PASS. 실제 RGB와 확대영상 및 마스크를 직접 검토했다. 기존 polygon `[(237,196),(250,183),(384,183),(401,196)]`은 vertex 순서가 정상인 convex 사각형이다. 높이13px, raw2102 → 2px erosion1415 → 3px brick exclusion1328 → 유효87로 재현됐다. 깊이 결측이 아니라 대부분의 ROI가 적재물에 가려지고 그 주변까지 제외되는 설계다.

보이는 팔레트 좌우 상면과 앞 모서리 안쪽을 따르는 후보 `[(236,197),(250,183),(384,183),(403,197)]`는 높이14px, raw2275/eroded1573/excluded1460/**valid113**, 제외영역 잔존0이다. 앞선 ROI를 y197까지 1px 넓히기만 하면101점이며 여유는1점이다. 최종 후보는13점 여유지만 견고하지 않다. 좌우 경계·앞 경계를 각각 ±1px 바꾼 9개 diagnostic에서92–139점, 안쪽 변경 시98·92로100 아래가 된다. y198 후보 등은 경계 밖 위험 때문에 최종 선택하지 않았다. 자동 최적 polygon 탐색·GT mask·USD target/pose 사용0. 가림 내부를 가로지르는 raw 사각형에서 brick은 원래 exclusion으로 제거하며 **잔존 픽셀을 상면에서 확인**했다. 수직 앞면·바닥을 점 확보에 사용하지 않았다. 2px erosion이 앞 모서리와 잔존점 사이 여유를 제공한다.

[오프라인 결과](construction_site_roi_regression_20261102_v28.json), [별도 원래 fit diagnostic](construction_site_roi_plane_diagnostic_20261102_v28.json). 새 pure-fit 코드를 만들지 않고 정적으로 읽은 v27 `fit` AST만 추출해 saved depth를 검사했다. 기존 RANSAC400/3mm·inlier100/80%·tilt5°·covariance 조건 그대로113/113 PASS, tilt .079800°, p95 residual1.047e−7m. 저장 관측 diagnostic이며 v27의 실패를 구제하거나 fresh observation으로 대체하지 않는다. v21의 알려진 ROI는 실제 raw에서 확인했으나 새 run에 자동 복사하지 않았다.

[PILOT ONLY 공통 절차 v28](../docs/construction_site_roi_review_rule_PILOT_20261102_v28.md)을 기록·적용했다. **기존 one-shot 앞에180초의 사전 preview window를 추가한 observation-policy 변경**이며 frozen scientific lock 수정이 아니다. HR/LR/CAD에 동일 적용한다. RGB·동일 axial depth·YOLO exclusion만으로 raw polygon/잔존점 overlay와 count를 보며, plane/GT/target/downstream 성공·representation 표시는 없다. Reviewer가 시각적으로 정당한 ROI를 한 window 안에서 검토한 뒤 한 번만 확정하며 B5 후 재제출0. Reviewer code `Codex-visual-review-v28`; 운영자는 HR임을 알고 있으므로 완전한 이중맹검은 주장하지 않는다. 암호학적 인간 신원 인증도 아니다.

## 실제 새 Kit 결과

외부 root: `/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v28_01`, raw `attempt_0001`. fresh RGB SHA `d1b5e670ea9a5def7043db1640c6f9e69735b4f0bf00ebce9d14e893cf409bbe`. 아래 prepare는 offline이고 run만 Kit1회다.

```text
python3 scripts/construction_site_perception_runner_20261102_v28.py --prepare-only --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v28_01
python3 scripts/construction_site_perception_runner_20261102_v28.py --run --output /home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v28_01
```

| 항목 | 실제 판정 |
|---|---|
| Camera | PASS, fresh640×480 RGB/axial depth·유효290691·calibration8/8·정지capture·원래 graph. 새 full RGB와 확대영상을 직접 검토. Plane offscreen 분류 유지 |
| Frozen HR M50 / B4 | PASS, 새 inference1회, conf .7014451, mask/depth7718, heading90.011093°·margin .0664386562. weights/recipe 불변 |
| ROI | 새 frame 직접검토 후 preview1개·최종제출1개,113점. 제출전 raw overlay를 표시·직접 확인. 좌표가 diagnostic과 같지만 새 영상에서 독립적으로 재검토했으며 자동 재사용0. RGB/array/depth/mask/overlay·preview SHA, reviewer, window·final 시각, shape, count, exclusion proof 기록 |
| B5 | PASS, 평면113/113·tilt .079800°·p95 1.047e−7m. locked pose COMPUTED, B5 inside_rate .9906603. fresh PRE=(-25.9346695,28.2780359), FINAL=(-25.9346695,29.0780359). **목표 생성과 목표 도달을 구분** |
| Physical admission | PASS, parser Error0, 실제 PhysX28/native0·consumer28, stationary support2214/2214·6wheel contact. 실제 contact168/예상외·shell load0 |
| PRE 경로 admission | 전체 rover sweep PASS, PhysX live support48060/48060. 실제 주행 trajectory 검증이나 PRE 도달 아님 |
| 실제 PRE / FINAL / normal stop | **모두 NOT_RUN**. driver 시작 전 차단, 비영 adapter/ROS 명령0. FINAL은 측정 PRE가 없어 독립 재계획·sweep NOT_RUN. baseline quiet1초는 접근 stop 아님 |
| TF/GID·GC | capture graph/물리 불변 PASS. active driver endpoint/TF/GID 검증 NOT_RUN. 기존 GC guard **FAIL**: RSS22,329,970,688 bytes=20.7964GiB, 절대상한8GiB 초과. 증가량0이며768MiB 증가한도 위반이 아니라 절대한도 위반. scope .00258s, GC는 paused cleanup에서 복구됨 |
| zero / 종료 | ROSzero receipt MISSING/valid=false, NOT_APPLICABLE_PRE_DRIVER. 요청·직접graphzero만 존재. observer exit0/driver NOT_STARTED. Kit close watchdog25초 초과→terminate 후5초 대기→kill, Kit exit−9·runner exit1/FAILED·finalizer KIT_EXIT_NOT_ZERO. 정상 shutdown 증거없음. watchdog 종료를 숨기거나 정상 exit로 바꾸지 않음. owned Kit/observer 잔존0 |

**첫 중단 원인은 `GC_MEMORY_BOUND` 하나이며, 후속 cleanup의 Kit close 실패는 별도 infrastructure 실패다.** `motion_gc.enter()` 직후 첫 `tick()`에서 발생했고 isolation/driver 생성 이전이다. 이번 run의 메모리 사용 원인은 아직 UNKNOWN이다. ROI·detector·geometry/model 실패로 돌리지 않으며 메모리 한도를 올리지 않았다. 추가 Kit/annotation/재추론/구제0.

## 검증과 보존

[독립 witness](construction_site_pilot_witness_20261102_v28.json)는 입력·executed snapshot·provisional digest·가용 evidence hash 모두 PASS, owned PID 소멸, contact·실제28shape·113점 재계산 및 PRE/FINAL NOT_RUN을 확인했다. engineering success=false, zero receipt=false, GC한도 충족=false가 명시돼 있다. Endpoint replay0행을 PASS로 취급하지 않는다. 대형 sweep/support는 외부 raw에 보존하고 report에는 경로/SHA/요약만 둔다. 초기 verbose witness도 외부 `witness_full_development_v28.json`에 보존했다.

집중 ROI14/14 + [소스·시각거절5/5](construction_site_source_checks_20261102_v28.json), compile PASS, 기존 v21 stop20/20 PASS, [known9 SHA 및108/432행](construction_site_known_locks_20261102_v28.json) PASS. 테스트는 old87 REJECT, valid113 INPUT PASS, brick/image-edge/교차vertex/시각적으로 부적절한 pallet-edge 거절, final후preview/재제출·late·변조·RGB mismatch 거절, preview target생성0, 원래 B5 fit AST 동일을 포함한다. 시각적 pallet-edge 적절성은 reviewer 책임이고 preview가 자동 semantic/GT edge 판별을 한다고 주장하지 않는다.

[실행전](construction_site_preservation_20261102_v28_pre.json)·[실행후](construction_site_preservation_20261102_v28_post.json) v27 전체 원시 index와 prepared 입력 mismatch0. v26 mount fix·v24 HR scene·28cell·v21 driver/event-aware stop·min100·B4/B5·5mm/2°/quiet1s·contact/graph/TF/GID/GC 한도를 보존했다. 이전 v27 **0/1 FAIL**, v20 **0/2 FAIL**, v21 **1/1 engineering success** 그대로다. 이번 v28은 exploratory engineering0/1이며 formal sample0, scientific equivalence/confirmatory 성공 주장없음.

변경 파일: 새 `scripts/construction_site_roi_review_20261102_v28.py`와 v28 adapter/session/runner. Adapter는 기존 B5 전 provenance 검증·window 시작만 추가, session은 adapter 경로만 변경, runner는 새 경로·source hash 포함만 변경했다. 새 ROI regression/source-check/independent-witness 분석과 pilot rule·v28 reports, latest/PROJECT_STATE 갱신. legacy 원본·USD·weights·locks 변경0, scene/light/YOLO training0, LR/CAD0, push/설치/외부 메시지0.

다음 구체 작업은 **기존 메모리 한도를 유지하면서 pre-driver admission 완료 시 RSS가20.8GiB인 원인을 좁히고, 동일 실패 후 close 지연 로그를 확인하는 별도 bounded 진단**이다. 이번 v28에서는 더 실행하지 않는다. 독립 clean HR PRE/FINAL 성공 전 LR/CAD 진행하지 않는다.
