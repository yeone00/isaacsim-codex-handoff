# C-V02 O0 단일 적재물 540회 프로토콜 및 실제 물리 진입 검사

기록 시각: 2026-11-13T17:12:17.859126+09:00

## 현재 결론

- 최종 설계 HR/LR/CAD × C100/C80/C60/C40/C20 × O0 ×36=540. 주행 시작0, 성공/실패/성공률은 아직 산출할 수 없음. 인프라 정지검증4건은 본실험 분모0.
- 새 root `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01`. 기존 원본C-V01/C-V02/학습39/HPO57/정적O0O25O50/checkpoint 수정·재학습·재선정 없음. 기존300+150/360+180/3C×3O×20은 실행대상에서 제외한 과거안.
- 단일 적재물 개정본 `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/single_load_amendment_v01/attempt_manifest.csv` 540행. 원본540 manifest는 load_count 키가 없었음. 참조한 정적 원천 행의 load_count는 다중일 수 있으나 새 물리 builder는 해당값을 읽어 클러스터를 만들지 않고 적재물1개/팔레트1개만 생성함. 이 차이를 명시적으로 잠금.
- 개정본 프로토콜 SHA256 `fa5ef9a20d0d9172f48f25b20e7a72e3dcb2c953759eafb0a4da3e18af2630d2`.
- 개정본 manifest SHA256 `92ba7c2909f78110d4fa985de17ce6863538b0110dfb3e42a7e7784f05ce19fc`.

## 단일 적재물 계약과 지표

모든 행에 load_count=1, pallet_count=1, target_instance=Load_01 명시. Load_01은 장면에 배치된 유일한 접근 대상이며 첫 생성 ID를 로봇의 선택 결과나 nearest 판정으로 설명하지 않음. 운영 인식은 최고confidence 마스크 처리규칙만 유지. 잘못된 마스크/배경 오검출은 검출·분할·위치추정 실패로 분리. 다중 목표 선택 정확도는 본540 주요지표에서 제외.

주요지표: 단일 적재물 검출, instance mask 품질, RGBD 계산 성공/XY·종횡·yaw오차, 계획/실제이동/정렬/정지 성공, 단계별실패, 작업성공률. 기존 정적 OTHER_LOAD/top1은 다중 적재물의 지정Load_01과선택마스크 일치에 관한 보조분석 그대로보존. GT는sim장면생성/평가전용이며운용prior는층수4/4/3/2/1만허용.

최종C06/75:25/seed42 모델3개 SHA 잠금 유지. imgsz640/conf.25/NMS.7/maxdet100/retinamasks. 기존 ROBUST_A 수식·설정 변경 없음. 새로운 직접높이추정/D600 미적용.

## 540 시나리오 manifest 검증

36base ×5C ×3rep, 고유attempt540, 대응base×C180,15셀각36 PASS. 같은base/C 3표현의 시작자세/제거경로/층수/family 동일. 표현순서를base와C에따라회전. 10Test원천family 계보를기록하며 기존물리배경은prepared v30 공통1개현장이다. 36개 독립현장으로주장하지않음. 원천staticcamera환경의완전재현이아니라 새로버탑재카메라 주행장면이다.

시작점은타깃중심(-25.888,30.509) 기준 x오프셋−.18/−.06/.06/.18m,거리2.8/3.0/3.2m,heading86/90/94deg 조합36. **좌표잠금은가능성/안전통과의뜻이아님**. 각시작점 실제바닥/장애물/가시성/경로검증은아직필요. 결과를보고성공위주로교체하지않음. 현재기술진입실패중이므로본manifest시도는전부PENDING/HOLD.

## 생성한 실제 USD 장면의 CPU 검사

`/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/single_load_amendment_v01/CPU_scene_QA_v01/result.json`:15조합 CPU_PASS. 각장면에서활성적재물1/팔레트1,Load_02+추가ID0,패널0,벽돌300/240/180/120/60개. brick공통명목box .190×.057×.090m 및실제pallet5부품 collisionAPI. 표현별동일C의충돌형상hash동일PASS,box중첩0,명목층별하부지지누락0.

과거고정28full-load union은새C장면에서비활성,새잔여벽돌별명목충돌체와팔레트충돌체로대체. 바닥·로버·배경장애물은보존. 고정cargo/static충돌모델이며동적벽돌붕괴/적재안정성검증이아님. CPU검사는actualloadedPhysX/접촉/안전/모션PASS를대체하지않음.

## 실제 Isaac Sim 실행: 실패를 보존한 HOLD

새 systemd controller가전역GPUlock하에hh_isaac51 실제Kit를실행했으나초기장면update에서native크래시.4개서로다른진단attempt/코드/로그보존:

1. v01 cache attach:첫app.update에서OmniGraph core/image plugin nativecrash.
2. v02 savedstage open:같은 nativecrash,연결API변경만으로해결되지않음.
3. v03 legacy disabled renderproduct node의깨진camera관계명시보정:같은 nativecrash. 깨진관계존재는CPU확인했지만크래시원인으로확정할수없음.
4. v04 단일Load_01 +이미disabled된ROS camera helper/renderproduct3노드만진단격리:같은 nativecrash. 로버actuator/TF/원본카메라 geometry는보존. 이sensorgraph분리판은본실험채택완료가아닌진단후보.

덤프스택은libomni.graph.core 및libomni.graph.image.core,Python app.update를가리킨다. **정확한native원인은UNKNOWN**. OOM이나모델인식실패로단정하지않음. 결과JSON이없으므로성공으로처리하지않고컨트롤러가HOLD/ntfy. 추가무조건재시도금지. GPUreset/패키지변경/기존프로세스kill없음.

`/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/infrastructure_failure_inventory_v01.json`에4로그SHA. 첫덤프/py-stack은기존Kit data내03aaeee1-a407-448a-592a1fb7-1a9193d6 파일. helper자동텍스트변환의별도v03 SyntaxError는CPU임포트실패로보존,수정v04문법/15장면CPU검증PASS;실험실패와구분.

## 실제검증 여부 / 본실험 진입

|항목|상태|
|---|---|
|540 단일 적재물 manifest·15셀 분모·모델잠금|PASS|
|15조합 단일적재물/팔레트/벽돌/명목 지지·중첩·공통충돌체 CPU검사|PASS_CPU_ONLY|
|actual loaded-drive-stage/PhysX등록·6차륜접촉|NOT_VERIFIED: nativecrash가실행을차단|
|새 단일 장면의 신선RGBD/인식/ROBUST_A|NOT_RUN: buffers생성전종료|
|경로·제어·정지·충돌·속도 안전/비상정지|NOT_VERIFIED|
|HR-C100 Full E2E 기술파일럿 및대표15조합|NOT_RUN|
|영상/GT/trace 필수증거저장|NOT_VERIFIED; USD와로그는보존|
|540 본실험|0/540,HOLD|

Main .11m/7.341774deg 및실제이동/충돌·안전위반없음 유지. PRE/FINAL5mm2deg/stop.03mps 별도. 아직예정540을실패540이나성공0%로계산하지않음. Wilson/대응분석/cluster는실제결과가쌓인후산출. `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/single_load_amendment_v01/condition_results_PENDING.csv`에15셀planned36/attempted0/비율NA 기록.

## 다음 구체 작업

nativegraphcrash를재현최소scene와원래validatedv30환경간차이로분리하고,distinct근거있는수정판만새output에서검증. 실제loadedstage·접촉·RGBD를확인한뒤인식/추정/계획/제어/정지/영상/GT운용분리FullE2E adapter를완성·동결해야한다. 현재stationary controller는본540을실행하는완성controller가아님. 본주행이나기술파일럿이자동진행중이라고주장하지않음.

상태명령: `bash /home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/DRIVE540_20261113_v01/status.sh`. 기존실패서비스v01-v04를같은출력으로재시작하지말것. 안전한재개는원인별새진단버전/새attempt경로와전역GPUlock필수. 본540의정상주행예상72~81시간은현재추가안전검증시간을포함하지않음.

기존Controller/Watchdog/ntfy/Git동기화는보존하며새프로토콜과HOLD도텍스트로동기화. ntfy서버접수와휴대폰실제수신은구분하여integration상태에기록.
