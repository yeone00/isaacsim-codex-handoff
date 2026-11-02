# v43 — 실제 Isaac Sim 3표현 적재 완전성 × 외부 가림 결과

2026-11-02 KST. **파일럿 RGB-D·동결 모델 추론 54/54 완료. 같은 단일 Kit 세션에서 전체 계획의 RGB-D·추론 972/972까지 완료했다. 새 로버 주행·조향·물리 play는 모두 0이다.** 이는 정적 관측 결과이며 972회 주행 성공 또는 Full E2E 완료가 아니다. HPO/AMP/Ray/훈련 작업은 실행하지 않았다.

원자료 root: `/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_OCCLUSION_20261102_v43`.

## 교수 면담에서 먼저 제시할 실측

파일럿: 3표현 × C100/C60/C20 × O0/O25/O50 × cement/red, MID 2.5m·Frontal/CENTER·site Nominal. 총18개 공통 장면 설정, 각 설정의 세 표현을 대응시켰다. 반복 표본은 없다.

|파일럿 실측|HR_Scan|LR_Scan|GeoCAD|
|---|---:|---:|---:|
|유효 새 RGB-D / 선택 행|18/18|18/18|18/18|
|동결 모델 추론 완료|18/18|18/18|18/18|
|brick_load 검출 존재|17/18|17/18|18/18|
|평균 가시영역 pixel IoU, 무검출=0|0.858409|0.901282|0.876891|
|B4 계산|17/18|17/18|18/18|
|센서 ROI 기반 B5 계산|6/18|6/18|6/18|
|기존 quintic 곡률 통과 / 평가 가능|1/6|1/6|2/6|
|smooth-S 곡률 통과 / 평가 가능|3/6|4/6|4/6|
|새 실제 PRE/FINAL·정지|NOT_RUN|NOT_RUN|NOT_RUN|

HR 무검출은 `FE2E_S007_O50_v43_HR_Scan`, LR 무검출은 `FE2E_S079_O50_v43_LR_Scan`이다. 둘을 제외하지 않았다. 검출 존재는 선택한 예측이 정답 mask와 충분히 맞는다는 뜻이 아니다.

확장972건은 거리3 × 시점3 × 조명2도 포함한다. **원래54건은 아래972건의 부분집합**이다.

|전체 정적 실측|HR_Scan|LR_Scan|GeoCAD|
|---|---:|---:|---:|
|새 RGB-D / 동결 모델 추론|324/324|324/324|324/324|
|brick_load 검출 존재|238/324|292/324|268/324|
|선택 mask의 GT IoU ≥ .50|231/324|218/324|267/324|
|선택 mask의 GT IoU ≥ .75|224/324|210/324|249/324|
|평균 pixel IoU, 무검출=0|0.677861|0.635470|0.744906|

총 무검출174/972, 추론 실행 오류0/972다. LR의 검출 수가 많아도 mask IoU는 높지 않을 수 있다는 점을 두 열이 보여 준다. 이는 **표현 + 해당 표현의 동결 M50 모델** 조합의 기술 관측이다. 표현 단독 인과효과·통계적 우열·동등성·실로봇 검증으로 해석하지 않는다. 셀당 반복1회이며972개의 독립 반복 주행 성공이 아니다.

실제 그림은 외부 root의 `pilot_actual_CxO.png`(C×O 9셀 실제 캡처), `pilot_actual_capture_contact_sheet.png`(54장), `pilot_pixel_iou.png`, `pilot_stage_counts.png`, `pilot_occlusion_measured.png`, `pilot_B5_task_datum_errors.png`, `factorial_CxO_pixel_iou.png`, `factorial_detection_vs_IoU_matching.png`다. 각 캡처 디렉터리에는 실제 추론 `detection_overlay.png`도 있다. 모의 v3 HR97/108·LR89/108·CAD80/108 수치는 사용하지 않았다.

## 가림 수준: 파일럿은 근접, 전체의 정확한 명목 수준은 미충족

기존 authoritative protocol v01→amendment v03에는 독립 외부 가림 비율이 없다. O0/O25/O50은 **v43 전향 PROPOSED 수준을 관측 전에 고정**했다. 기존 잠금 자체를 수정하거나 새로운 정식 confirmatory amendment로 부르지 않는다.

completeness는 원래 잠금의 Bundle5 제거 궤적이다. C100=300, C60=180, C20=60벽돌이며 LR은 독립 재구성 자산이다. v03의 고정 reference environment `MNIDB_0001`과 각 base 행의 기존 trajectory를 사용했다. 파일럿 cement는 FULL/T02/T02, red는 FULL/T04/T04다. 서로 다른 material의 trajectory를 임의로 통일하지 않았다. 세 표현 안에서는 membership·카메라·판 위치·재질·조명·초기 pose가 동일하다.

외부 가림은 load가 아닌 **충돌 API 없는 시각 전용 foreground panel**이다. 물리 장애물을 경로에 추가하지 않았다. live 주행을 위한 물리 가림판 인증은 아니다. 깊이1m에서 카메라를 향한 판의 오른쪽 경계를 HR의 무가림 target mask 열 분위수로 구성한 뒤, 모델 추론 전에 고정했다. 같은 world vertices를 LR/CAD에도 사용했다. 표현별로 목표·카메라·가림판을 조절하지 않았다. appearance는 고정 displayColor (.13,.20,.28), 형상은 결정적이며 seed는 부모 scene seed를 기록했다.

GT는 Replicator semantic segmentation의 load 상속 라벨 `brick_load`로 얻었다. `gt_amodal_external_only.npy`는 같은 고정 카메라에서 **외부 판을 숨긴 표적 투영**이다. 외부 판에 대해서만 amodal이며, 자기 가림 뒤의 숨은 면이나 화면 밖 픽셀을 분모에 더하지 않는다. `gt_visible.npy`는 판을 적용한 실제 보이는 표적이다. 가림률은 `count(amodal & ~visible) / count(amodal)`. 전체972건에서 visible이 baseline 밖에 생긴 픽셀0, 화면 경계에 닿은 표적0이다.

|구간|O25 실제 가림률|O50 실제 가림률|
|---|---|---|
|54 pilot|24.53–25.74%|49.45–50.73%|
|전체972 중 각324행|16.56–26.57%, 평균24.69%|21.79–51.91%, 평균48.43%|

전체의 O25 24행, O50 38행은 명목값과2%p 넘게 달랐다. **2%p는 사후 분포 설명용 구간이며, 승인된 성공 기준이나 제외 규칙이 아니다. 모든 행을 유지했다.** 따라서972건의 취득·추론 완료와 정확한25%/50% 가림 factorial 실현을 구분한다. 후자는 NOT_ESTABLISHED다.

최저 O50 사례 `FE2E_S004_O50_v43_GeoCAD`의 무가림 depth를 독립 확인했다. 판이 덮는 수평 투영은50.34%이지만 그 안의8,397표적 픽셀이 깊이1m 판보다 앞이다. ray depth로 예상한 차단21.84%, 실제21.79%가 대응한다. 근거리 사선에서 판보다 앞선 표면이 남는 것이 원인인 구체 사례다. 원자료는 `occlusion_shortfall_diagnostic.json`이다. 새로 판을 옮기거나 실패 셀을 재취득하지 않았다.

## 모델·B4/B5·planner의 실제 범위

세 모델은 `final_combined_m50_adaptation_v01/standalone_selection_v01/selected_models/FINAL_<representation>_M50_REALVAL_MASKBEST_v01.pt`다. 이번3표현 HPO보다 앞선 frozen M50이며 새로운 학습·선택·Test1200/Real Test189 재평가0이다. Test189는 역사적으로 이미 평가됐으며 미개봉이라고 하지 않는다. real 외부 검증은 red-only라는 범위도 유지한다.

|모델|검증된 SHA256|
|---|---|
|HR_Scan|`257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`|
|LR_Scan|`d58e18a87f4cafba6fd92d8bade6e2ff12ad2380db427311b072859fd2cca42f`|
|GeoCAD|`bbfb9fc8d0c421154844f7e299b6d8162b9394eb07d36a31110f593c0813ce8f`|

실제 로딩 시 세 모델 모두 task=segment, class0=brick_load, 실제 새 이미지 추론 PASS다. 환경은 torch2.7.1+cu128 / ultralytics8.4.129 / numpy2.4.6, `sdg_tools/bin/python`. 추론 조건은 기존 imgsz1280/conf.25/NMS IoU.70/mask threshold.5, highest-confidence brick_load·동률 최소 index다. GT·가림 라벨은 추론 입력에 없다. 별도 평가 코드만 GT와 예측을 비교한다. pixel precision/recall/IoU를 제공하며 AP/mAP는 계산하지 않았다. IoU≥.50/.75 열도 AP가 아니다.

B4는 predicted mask와 실제 depth를 backprojection한 점에서 동결 top-band/heading 함수를 계산했다. COMPUTED는 각도 정확도 인증이 아니다. B5는 원본 pose source SHA 및 추출 함수 AST를 확인하고, 이번54장 RGB 접촉표와 원해상도 표본에서 검토한 공통 팔레트 상면 ROI를 사용했다. polygon은 [(235,202),(251,185),(384,185),(406,202)], 기존 erosion2px/brick exclusion3px·plane gate를 그대로 적용했다. 수동 보조이며 독립 사람의 맹검 검토가 아니다.

파일럿 O0의18건에서 B5 계산됐다. 가림34건은 sensor datum gate 거절, 나머지2건은 무검출로 B5 미실행이다. 예를 들어 HR C100/O25의 near-horizontal 평면 inlier는89/581=15.32%로 기존80% gate보다 낮다. GT로 datum을 대체하거나 기준을 낮추지 않았다. **추가918건은 시점·거리가 달라 fresh ROI를 새로 검토하지 않았으므로 B5 NOT_RUN**이다. 전체 B5 분포는 COMPUTED18 / DATUM_REJECTED34 / NOT_RUN920이다. 972개 pose 결과가 완성됐다고 하지 않는다.

서명 오차는 B5가 있는 행에만 기록했다. 평가용 task-design datum (−25.888,30.509), yaw90°에 대해 pred−datum, longitudinal=+Y, left=−X, heading modulo180이다. 실제 독립 metrology는 UNKNOWN이며 C20의 residual-load 중심을 task datum으로 재정의하지 않았다. `pilot_B5_task_datum_errors.png`와 결과 CSV에 각 오차가 있다. pose가 없는 칸은 N/A이지0이 아니다.

planner에는 sensor-calibrated start와 B5 관측 중심에서 만든 기존 PRE target만 전달했다. 기존 v30 executed follower의 strict quintic을 AST로 추출했고, v36 smooth-S는 별도 OFFLINE branch로만 평가했다. 곡률 bound `.95*tan(15°)/.7 = .363645332585095 /m`을 변경하지 않았다. strict 거절 뒤의 최대곡률은 예외 하나만 제거한 **별도 진단 사본**으로 산출했으며 승인으로 바꾸지 않았다. 평가18건의 old 진단 peak 범위 .006136983–1.503940294/m다.

곡률 통과는 full planner admission이 아니다. 새 목표에 대한 전체 충돌/footprint/support 또는 live steering qualification을 수행하지 않아 전체 geometry 평가 분모0, full admission N/A다. 원래 quintic 거절과 smooth-S 곡률 결과는 CSV에서 분리한다. 물리 PRE/FINAL·실제 정지 분모0이며 성공률 N/A다.

## 실행·검증·보존

발견된 `hh_isaac51/bin/python`의 SimulationApp/Kit를 정확히1회 시작했다. 재시도0, 새 session0, observer0, driver0, ROS 시작0, timeline.play0. 파생 overlay에서 발견된 모든 OmniGraph/ActionGraph를 attach 전에 비활성화했다. 각 렌더 후 timeline stopped와 Rover world matrix 불변을 확인했다. 정적 조건 사이의 초기 pose reset은 actuator 이동이 아니다.

972개의 case_started/case_completed event와 고유 case IDs가 대응한다. 첫54 취득은 Python 시작 후34.13초, 파일럿 중간 결과 뒤 같은 세션에서 나머지를 수행했다. 시작요청→close 진입470.27초, process exit까지 약472.79초. 600초 제한 안이다. resource 표본1,221개, owner RSS 최대8,127,406,080bytes=7.56924GiB <8GiB; 전체 GPU 최대7,650MiB <26,000MiB. GPU 수치는 RAM RSS와 별도이며 다른 desktop allocation도 포함한다. 첫 점검과 종료 후 compute process 목록에서 경쟁 학습은 관측되지 않았다. 기존 다른 프로세스를 종료하지 않았다.

annotator detach/product destroy 후 close_enter1회, outer process exit0, owner PID2997859 잔존0이다. **Python close_return event와 session_result.json은 생성되지 않았다.** v30과 마찬가지로 process 정상 종료와 Python 함수 return 관측을 구분한다. 강제 종료·GPU reset·설치0이다.

|검사|판정|
|---|---|
|실행 전193개 expected SHA, 기존 v30 입력108개 추가 대조|PASS, mismatch0|
|prelock/amendment v03/geometry v02 known9 SHA 및108/432행|PASS, 전체 readiness 인증 아님|
|972 고유 case /324 scene /각3표현,54 subset /18 scene|PASS|
|paired camera/pose/membership/material/lighting/panel 좌표|PASS,324scene|
|새 캡처 입력6파일 ×972 SHA 비교|PASS,5,832건|
|972 이미지/GT shape·실제 가림 산술·추론 claim/model binding|PASS|
|972 raw camera projection/view→수치 calibration 재구성|PASS|
|원본 stage·동결 weights·등록 자산의 종료 후 SHA|PASS, 보존|
|geometry lock 자체 독립 expected SHA|UNKNOWN 유지|
|새 source compile·perception4 invocation·summary·validation|exit0|
|명목 O25/O50 전조건 정확 실현|NOT_ESTABLISHED, 실제 비율 전부 보존|
|B5 전체972 /full geometry admission /로버 주행|미완료 /NOT_RUN /NOT_RUN|

숨기지 않은 구현 결함도 있다.

1. Kit 초기 `[Error] [omni.hydra] Skipping invalid mesh V43ExternalOccluder ... invalid points buffer`가1건 있다. 초기 hidden 판에 points를 아직 넣지 않은 상태에서 attach됐기 때문이다. 이후 활성 판에는 vertices가 들어갔고 각 실제 capture의 가림 mask를 측정했다. render log 전체를 error-free PASS로 부르지 않는다. terminal/process 실패는0이며 이 renderer 오류1건은 `final_validation.json`에 원문 보존했다.
2. `camera_metadata.json`의 `calibration_sha256` 필드에 calibration 대신 depth SHA를 넣은 구현 오류가 있다. 원본 metadata와 inference 결과를 고치거나 재추론하지 않았다. 원시 projection/view에서 전체972 수치 calibration을 별도 재구성·검증했고, metadata 전체 SHA를 `calibration_provenance_supplement.json`에 결합했다.
3. calibration frame_id는 같은 카메라 baseline의 O triplet에서 공유된다. 고유 capture 식별자는 case_id와 session event다. 이를 서로 다른 카메라 calibration이나 동일 frame 재사용으로 해석하지 않는다. RGB-D는 실제 판 적용 후 새 render에서 취득했다.
4. 사전 검색의 존재하지 않는 보조 경로에서 rg exit2가 있었다. 이것은 capture/inference 시행 실패가 아니며 새로운 과학 분모로 넣지 않았다. 원본 연구 파일을 이동·실행하는 discovery는 하지 않았다.

## 파일과 재개 범위

외부 root의 주요 산출물:

- `factorial_972_locked.csv`, `scene_specs_locked.json`: 관측 전 고정한972개 계획. 초기 execution_status=NOT_RUN을 보존한다. **현재 관측 상태는 `factorial_execution_status.csv`**다.
- `pilot_54_results.csv`: 실제 관측54행만. `cumulative_actual_results.csv`: 실제972행. 원본별 파일 SHA, intended/actual occlusion, visible pixels, 단계별 미실행·실패 이유 포함.
- `perception_pose_summary.csv`: 표현×C×O×material 집계와 단계별 분모. `completeness_occlusion_interaction.csv`: 파일럿 IoU의 C×O difference-of-differences, 기술 통계만. 새로운 p-value·동등성 주장은 없다.
- `captures/<case_id>/`: 새 RGB/실측 depth/평가 GT/overlay/predicted mask/추론 결과, 가용한 sensor plane과 offline path. bulk는 Git 밖에 유지한다.
- `run_manifest.json`, `integrity_preflight.json`, `historical_108_input_integrity.json`, `known_locks.json`, `final_validation.json`, `paired_scene_checks.json`, `evaluation_integrity.json`, `actual_occlusion_distribution.json`.
- `invocation.json`, `session_events.jsonl`, `kit_stdout.log`, `process_exit.json`, `pilot_inference.log`, `cumulative_inference_batch01/02/03.log`, `post_run_nvidia_smi.txt`, `executed_new_code/`.

실제 Kit 명령은 `/home/user/anaconda3/envs/hh_isaac51/bin/python scripts/three_rep_static_session_20261102_v43.py`; 외부 supervisor가 invocation과 stdout, 실제 process exit를 저장했다. 추론은 `/home/user/anaconda3/envs/sdg_tools/bin/python scripts/three_rep_static_infer_20261102_v43.py`를 파일럿1회·미처리 행 batch3회로 수행했다. claim 파일이 있는 행은 다시 추론하지 않았다. 반복 관측/선택적 rescue가 아니다.

현재 자료만 다시 집계하는 명령은 다음과 같다. Kit·학습·주행을 시작하지 않는다.

```bash
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/three_rep_static_summary_20261102_v43.py
```

변경 파일은 새 v43 prepare/session/infer3개, summary/validate/full_plots3개, 본 보고서, latest_report, PROJECT_STATE다. 원래 USD/locks/weights/훈련 데이터/Proxy 및 기존 결과 변경0이다. 로컬 `.git`이 없으므로 stage/push/remote 변경0, GitHub 동기화 완료는 UNKNOWN이다. handoff marker는 보고서 동기화 요청만 한다.

역사 결과를 유지한다: v30 HR 실제 simulator PRE→FINAL n=1, FINAL observed 목표2.79451mm 대 task-design55.23288mm. v31 LR/v32 CAD는 old-quintic 곡률 거절로 driver·motion 전 종료했다. v35/v36의27case/55,221검사는 offline이고 v37/v38의 steering response/live policy는 HOLD다. 이번 정적 관측이 이를 해제하지 않는다.

**다음 구체 작업:** 이번 파일럿과972 정적 표를 면담에 사용하되, 전체의 실제 가림률 분포 및 B5 미완료 범위를 함께 제시한다. 후속 새 버전에서는 scene-comp GT로 공통 판을 모든 표적 표면 앞에 두는 fixture와 calibration provenance 필드를 수정하고, 새 시점의 sensor-only pallet datum 획득을 정의해야 한다. 기존972를 재라벨·재추론·성공으로 소급 변경하지 않는다. 새 Kit 세션이나 조향 시험·주행은 이번 완료 뒤 자동 실행하지 않았다.
