# C-V02 ROBUST_A 작업 층수 prior 승인 개정 및 오탐 복구

2026-11-12 연구자의 최신 결정 반영. **C-V02는 운영자/작업관리 시스템이 잔여 적재 층수를 사전에 제공하는 조건부 자율 접근·정렬 실험**이다. 센서만으로 층수를 알아내는 완전 자율 실험으로 기술하지 않는다. 기존 C-V01·B1·Stage4·HPO/모델/오류 기록은 보존한다.

## 1. 현재 작업과 오탐 복구

추가 C100 180/840건까지 정상 저장된 뒤, 새 감시기가 완료 worker PID가 사라진 전환 구간을 즉시WORKER_MISSING으로 판단해다음GPU경계를예약했다. 실제렌더/데이터실패가아닌감시오탐이며,그로인한controller BlockingIOError/HOLD로그를삭제하지않았다. observer v03에동일missingPID120초유예를추가했다. 기존연구watchdog PID3805776과진행중worker를중단하지않았다.

이미완료된180개결과·파일SHA를재사용하고generation v02 PID966660으로재개했다. 이후200/220/240/260묶음완료와다음worker전환을확인했다. 현재정확건수는V02/pipeline_status.json 기준. 학습은전체5250QA뒤대기중이며현재재학습/중복GPU없음. 최초gen v01·observer v02·오탐HOLD기록·복구버전v03을별도보존했다.

## 2. 허용 입력 계약

| 조건 | 잔여 벽돌 | 제공 task_layer_count | 최상단 잔여 Bundle5 |
|---|---:|---:|---:|
|C100|300|4|15|
|C80|240|4|3|
|C60|180|3|6|
|C40|120|2|9|
|C20|60|1|12|

값은적재율이나완전층개수가아닌**남아있는층수**다. 같은scene/O의HR/LR/CAD에동일입력. 기존C생성manifest의nominal `layer_count=4`는카메라생성전제이며변경하지않는다. 새 `task_layer_count`를독립schema/manifest로관리하여진행중이미지생성·분할·학습에영향을주지않았다.

별도operator metadata는schema/task_id/task_layer_count/provider 4개키만허용한다. C라벨/GTpose/mask/제거slot/footprint중심/FINALpose를추가하면거부한다. task_id는opaque hash이며알고리즘은C를해석하지않고정수층수만전달받는다. static task2250행,물리task450행초안(시작좌표미확정)을저장하고SHA를잠갔다. 물리초안은실행가능한최종scenario manifest가아니다.

새C전용Stage4 perception CLI는--layer-count {1,2,3,4},SHA검증된작업registry와최종model lock을요구한다. seed42를이번시점에미리주행용으로고정하여파일럿결과로다른seed/model을고르지않도록했다. seed43/44는기존정적반복검증을유지한다. initial/ROBUST_A만허용,중간재인식은추가하지않는다. 기존M50가아닌최종혼합C-V02모델을사용하고C용640/conf.25/IoU.7/maxdet100/retina-mask설정을기록한다. 이CLI는아직물리실행하지않았다.

## 3. 원본 ROBUST_A 보존

- 원본: evaluation/b5_robust_20261110_v01.py
- SHA256: `0b1e5f46702d4af0c4d4abc4b7d1c5fe9d29cc07c9f34b4a1592990ac296ae29`
- 기존frozen config SHA256: `35cf0a78d4c73919ab2a03378341fb90433aeaeeab306a605d064d98a0cfc529`

수식·ensemble·threshold·상수·source와과거결과불변. 새wrapper는원래frozen config와code SHA를검증한뒤 `estimate_pose(mask,depth,camera,task_layer_count, config=frozen,return_diag=True)`로전달한다. .144m pallet두께와적재물상단을구분한다. 기존nominal4 및센서층수추정결과는별도diagnostic baseline으로보존하며새task-prior 기준결과와혼합하지않는다.

C-V02에서의기존“정답층수입력금지”문구는이번승인범위에서만명시적으로대체한다. 나머지GT 금지는그대로다. layer count를안다고추정성공/작업성공으로집계하지않는다.

## 4. 검증 결과와 아직 없는 성능

| 검사 | 상태 |
|---|---|
|1~4층 정확 전달|PASS, 원본API forwarding 확인|
|1~4층 원본함수 NO_DETECTION smoke|PASS, mask없음은실패그대로|
|원본source datum prefix 4층수×floor유/무8case|PASS,원본AST수식을실행|
|잘못된층수0/5/bool/string 및GT키 거절|PASS|
|evaluation GT 파일읽기차단|PASS,별도프로세스/입력schema/파일접근guard|
|C20~100 실제O0/O25/O50 성능|**PENDING**,최종고정모델prediction이아직없음|
|신규C 실제loaded-drive-stage/PhysX접촉검사|**UNKNOWN/PENDING**,물리HOLD|

단위진단에서상층점이1%미만이고floor관측이없으면,정확한layer_count=4라도q99가3층상단을택해pallet datum이.144가아닌.054m로−.09m차이날수있음을원본수식그대로확인했다. 이는합성센서단위반례이며실제C80실패관측으로집계하지않는다. 층수정보만으로불규칙최상층/가림문제가해결된다고주장하지않는다. 실제RGB-D에서분기/산출률/중심·yaw오차/거절원인을평가하고,구조적실패가확인되면원본baseline을보존한별도C수정안을제안한다. 지금수식수정0.

## 5. GT 분리와 추가 정적 평가

기존Controller/학습/혼합/주된정적작업의명령·source lock을수정하지않았다. 별도CPU observer가기존정적작업완료를기다린후**새primary known-task-layer ROBUST_A 평가**를추가한다. 따라서현재C100생성/학습과경합하지않는다.

각role의최종모델mask6750입력을부모평가프로그램이분리한다. operational view에는모델prediction mask/depth/camera/checkpointSHA/허용task metadata만있다. GTpose와C/O별평가키는별도eval_gt_only파일에두고**다른프로세스인operational worker가끝난후**부모가오차계산에만읽는다. worker는GT/complete/canonical mask/scene manifest/removal history/기존pose_inputs GT묶음읽기를거부한다. 원본bitmap을GT마스크로교체하지않는다.

최종혼합모델과합성baseline을각각평가하되동일SHA이면검증참조로중복평가를피한다. 전체계산성공률과올바른목표조건부오차를구분하며모든실패와datum/floor상태를보존한다. C5×O3×표현별시도수/산출수/XY·종횡·yaw 평균·중앙값·p90/실패유형을자동보고한다. 추가모델선정/HPO/threshold튜닝없음.

원래순서 C100→QA→C06고정학습→공통혼합비율→최종model lock→인식→위치추정의순서를유지한다. 기존priorless pose작업은별도baseline이며새정책의primary결과는추가task-prior결과파일을기준으로한다. 주요정적완료뒤task-prior작업이추가되므로그완료전primary검증완료라고표시하지않는다. 물리단계는여전히HOLD.

## 6. 물리 구성 감사와 성공 기준

CPU OpenUSD로기존NuRec B1_CLOSED_EV 및역사적v30 prepared_site_drive.usda를읽었다. 원본NuRec collision API0. 역사적prepared v30에는총42enabled collision prim(이름상rover13/미분류29)와PhysicsScene1이있다. 미분류에는Env mesh와PilotStaticUnion cell들이있으므로이름만으로floor가없다고단정할수없다. 팔레트·적재물·floor role binding과실제동작접촉은이검사로인증하지못한다. 과거v30성공기록을새C의물리완전성PASS로전이하지않는다.

**신규C composed drive stage는아직생성/실제load하지않았다.** 따라서actual loaded-stage manifest,rover/floor/pallet/load collider binding,PhysX floor-wheel·pallet-load접촉/필터/충돌검사는UNKNOWN이다. CPU composition을Isaac실측검사로포장하지않고HOLD한다. 단계별검사도구는준비했지만현재GPU생성을방해하는추가Kit/물리실험은하지않았다. 구성누락/역할미확정시실제주행진입불가.

최신연구자결정으로Main task criterion을**0.11m/7.341774° 및충돌·안전위반없음**으로명시했다. PRE/FINAL **5mm/2° 도달인증**,**0.03m/s 안전정지**는별개기록이다. .10m/5°초안과혼용하지않는다. 성공기준충돌항목은이승인으로정리하되실제floor/물리구성/ROBUSTA C호환/제어안전/기술파일럿gate는미통과상태로유지한다.

## 7. 파일·상태

Root: SDG/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/task_layer_policy_v01.
- policy.json/input_contract_lock_v01.json/static_task_manifest.csv/operator_metadata.json/physical_task_plan_DRAFT.csv
- execution_extension_lock_v02.json:원본source불변·새wrapper/CLI/worker/observer SHA
- unit_smoke_results_v02.json:단위진단이며실제성능아님
- historical_composed_stage_audit.json/new_C_loaded_stage_gate_v01.json/physical_gates_amendment_v02.json
- observer_status.json:현재WAITING_FINAL_FROZEN_MODEL_STATIC
- 실제성능완료후 RGBD_task_prior_summary.json 및 reports/c_v02_ROBUST_A_task_layer_RGBD_results_20261112_v01.md 자동생성

자동서비스 c-v02-task-prior-evaluation-20261112-v01는독립CPU/systemd로대기한다. 기존C100/모델/Watchdog/ntfy/GitHub서비스는유지한다. 최신status.sh는추가작업상태도표시한다. ntfy는기존설정/재시도경로를사용하며서버전송HTTP200과휴대폰수신여부는구분한다. 새정책/코드/요약SHA는GitHub에별도동기화한다. 원본RGB-D/NuRec/weights는게시하지않는다.
