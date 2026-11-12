# C-V02 C100 보강·C06 고정 혼합 실험 자동 실행 인수인계

2026-11-12 최신 연구자 지시를 적용했다. 기존 C100 보강 보류 결정은 이번 신규 승인으로 대체되지만 과거 결정/감사/DRAFT는 보존했다. 신규 root: `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01`.

## 실제 실행 및 기존 작업 보호

기존 C-V01 4410 관측, C-HPO 57학습, 복구crossVal24, C06 lock/원본checkpoint를 보존했다. 기존Test가림30/30묶음 PASS_CAPTURE/1890frame manifest/camera·GT·coverage QA가 완료됐다. 마지막GeoCAD생성종료후에만전역GPUlock을예약하여예정된C-V01perception진입이BlockingIOError로HOLD된기록을보존했다. 이는연구자순서변경에따른의도적진입차단이며생성실패가아니다. 실행중worker에kill/SIGSTOP/재시작을하지않았다. C-V01perception/pose는시작하지않았으며이후발견되는기존결과도삭제하지않는다.

새generationcontroller(systemd)는경계HOLD를확인한뒤GPU예약을인계받아C100본생성을실제시작했다. 첫20관측PASS_CAPTURE및다음묶음자동전환확인. 이후시각의실제건수는V02/pipeline_status.json을기준으로한다. 부분생성만으로전체QA/학습완료를주장하지않는다.

## C100 추가 관측과 QA

| 표현별 상태 | Train | Val | Test |
|---|---:|---:|---:|
| 기존C100 |50|10|10|
| 추가C100 |200|40|40|
| 최종C100 |250|50|50|
| C80/60/40/20 각각 |250|50|50|
| 최종전체 |1250|250|250|

신규840관측/전체5250,세표현합계Train3750/Val750/Test750. 기존4410은파일참조로재사용하고새관측만별도폴더에저장한다.70기본family와split50/10/10유지,원본제거이력/Bundle5점유/300벽돌형상/에셋SHA/중심배치보정/팔레트/조명/렌더러/센서고정. 각family에원래OBS00+4개새camera-distance 관측을만든다. 거리값은**기존Train의같은distance_bin 분포에서만**사전선택한4개의서로다른값이며Test성능/GT오차로조건을고르지않았다.

카메라만local eye_x=zone_x+원래배치거리−새관측거리로옮기고기존적재물중심/nominal4높이(.324m)를보도록한다. 높이.6m/광학640×480/ISO25/shutter50/f5는유지. load의world pose는변경하지않는다. 단순복사/색증강이아닌새RGB-D렌더관측이다. HR/LR/CAD는같은sceneID/조건을공유한다. 20관측이하freshKit묶음,기존8GiBCPU RSS안전검사보존.

C100만다양한camera거리/시점을갖는교란을명시한다. 거리구간·조명분포및family별관측수는C_observation_distribution_audit_v01.csv에저장했다. 최종AP에는기존동일카메라anchor-only와전체V02를별도집계하며,보강효과를순수적재율효과/실사동일재료일반화로단정하지않는다.

QA는모든5250의sourceSHA/실제brick수/원본bitmap·Depth·camera·표현간canonical exact 대응을재검증하고,새C100각family×rep의5RGB/Depth해시고유성과targetpose불변도별도검사한다. 기존mask구멍·분리영역은그대로,정답slot/pose는운용알고리즘에제공하지않는다. 전체QA/분할잠금전학습진입없음.

## 실사 자료 감사 및 한계

Roboflow원본Train352/Val48/Test189. 파일SHA·decoded pixel SHA·CVUT frame ID의split교차중복0,Train/Val class0 polygon형식검사PASS. Test는누수검사용hash/계보만확인하고새모델선정에는사용하지않는다. 기존Real Test189은B1분석에서이미노출되었으며새독립blind Test가아니다.

실사원본은target-only이고미라벨주변적재물/병합GT의알려진제약이있다. 기존연구자가승인한LOCKED mixing protocol v03(원본라벨그대로,보완라벨검토중단)을따른다. 미승인labels_v02초안을섞지않는다. 제품도작은unwrapped red bricks와포장된대형천공clay blocks의도메인차이가있다. 따라서호환성판정은**기존명시적라벨정책을유지하는전이·적응실험**범위의PASS_WITH_DISCLOSED_LIMITATIONS이지완전히동일한물체/완전annotation보증이아니다.

원본실사polygon은그자체를변경하지않고원본해상도bitmap으로rasterize하여instance순서/소유권을보존한다. C bitmap을polygon으로변환하지않는다. 모델입력리사이즈/nearest bitmap변환과mask_ratio4는같은로더에서처리한다. 무라벨음성도0instance로정상지원한다. CPU에서양성/구멍/분리/음성×640×480/1296×972총6조합변환검사PASS. 실사원본/라벨/SHA는별도보존.

## C06 고정·1250개 혼합 manifest·학습 수

HPO57건은반복하지않는다. 기존selection_lock의C06 **전체정밀도값**을읽어고정한다(사용자표시는반올림값).

- lr0 .000888131352250591
- weight_decay .0008730658008775225
- lrf .13119036537141066
- warmup_epochs 4.486041867303101

동일pretrained SHA55ed65c56c91713d23e8402371c6c49a6fd84f257f7dce452e8d70e41dcbe152에서새학습. YOLO11n-seg/200epoch/batch64/640/AdamW/v04PhotoDegrade/FP32box·AMP/scaler128유지. 새C-V02에서도수학적으로최적이라고주장하지않는다.

| 혼합비 | 합성slot | 실사slot | 실사고유수 | 실사추가반복slot | 고유본학습 |
|---|---:|---:|---:|---:|---:|
|100:0|1250|0|0|0|9|
|75:25|938|312|312|0|9|
|50:50|625|625|352|273|9|
|25:75|312|938|352|586|9|
|0:100|0|1250|352|898|3|
|합계|||||**39**|

실제분율75.04:24.96/24.96:75.04를기록한다. sampling seed20261112,학습seed42/43/44는별개. 합성은상태별round-robin선택으로표현간같은scene membership을사용한다. 실사는고정순열prefix/cycle로반복하고매load시원래온라인증강을적용한다. 반복이항상서로다른증강결과이거나독립실사사진이라고주장하지않는다. 모든비율1250slot고정.

합성전용9개를먼저훈련하고100:0혼합조건에그대로재사용한다. 0:100은동일실사학습궤적을seed별1회만훈련하되각표현의합성Val에서동일선정규칙으로checkpoint를저장하므로선정epoch/SHA는표현별로달라질수있다. 학습궤적3개를9개독립실험이라고세지않는다. 본39×200=7800epoch와별도2epoch GPU smoke3개(6epoch)는분모를구분한다.

## 사전 모델·비율 선정 규칙

매epoch의primary checkpoint score는 .5×자기표현C-V02 Val Mask mAP50–95 + .5×실사Val Mask mAP50–95. 원래원본SegmentationValidator matching/mAP공식을사용한다. 비트맵GT와native FP32EMA/autocast16평가경로,Valrect/pad/mask_ratio4/overlapFalse를공통적용한다. 학습증강은Validation에서적용하지않는다. 실사Val은48장그대로이며증강/반복하지않는다. real-Val dataloader는별도로workers0으로만들어기존반복DataLoader shutdown HANG을피한다.

checkpoint는unrounded score strict greater,동점earliest epoch. 0:100은3합성Val+실사Val을측정해표현별같은공식으로best를저장한다. 합성own-Val best는보조checkpoint로도보존하지만ratio primary와혼동하지않는다.

공통비율은5비율의3표현×3seed balanced checkpoint score를동일가중평균한최고값으로선정한다. 정확동점시고정순서100:0→75:25→50:50→25:75→0:100(합성비중높은쪽). 특정표현에유리하도록사후선택하지않는다. 별도CPU보고가표현별3seed평균/SD를작성한다. 과거B1 50:50을최적으로가정하지않고Test에따라재선정하지않는다. 최종9checkpoint와baseline9checkpoint를SHA고정한뒤정적평가한다.

## 후속 평가·안전

기존V01Test frame1890(630O0+1260가림)은source/camera/GT/coverage QA가끝난참조로재사용한다. 신규C100Test120O0에대해O25/O50각120,총240만추가생성한다. 최종Test2250=표현당250×3O×3표현,각상태50관측이지만독립family는10개다. C100추가camera조건의coverage/GT는새frame에서검증한다.

고정혼합9모델과C-V02합성baseline9모델의전체cross표현·O0/O25/O50·C5조건mAP50/50–95/목표검출/IoU/Top1/실패분류를집계한다. 같은SHA선정baseline이면중복inference를SKIPPED_VERIFIED로참조한다. pooled/동일C macro/anchor-only를분리하고seed변동성과familycluster bootstrap 불확실성을기록한다. 이후같은selected masks로기존B5/두B1ADAPT/frozen ROBUST_A/센서높이후보를구분해정적pose평가한다. 실패를조건부오차평균에혼합하지않는다.

물리pilot/본300/별도O50150은HOLD. .11m/7.34° vs.10m/5°출처충돌,실제floor/pallet .144site datum 인증,센서기반ROBUSTA·충돌/속도/조향/정지·파일럿gate가해결되지않았으며물리진입명령을새capability에넣지않았다. 논문3/4장용통합보고는정적완료후자동작성하되물리미실행을명시한다.

## 독립 실행과 검증 범위

현재source generation v01이systemd아래실행중이며원래Watchdog/ntfy/GitHub서비스를중단하지않았다. 새V02감시기는heartbeat/PID/로그/epoch/disk/고정source SHA를감시하고알림실패queue재시도한다. GPU연구작업은flock1개씩,threshold/source경고는현재worker를kill하지않고다음GPU경계에서HOLD하도록구성했다. 새로운server/topic/credentials는만들지않았다.

이미실제로검증한전환은**기존30묶음완료·QA→예정인식진입차단→C100첫묶음→다음묶음자동전환**이다. 새학습GPU smoke와본학습·최종평가는전체C-V02 QA후자동수행되며이번시점에완료했다고표시하지않는다. 새source AST/6개bitmap CPU변환/실사계보검사는PASS. 실패는새attempt와HOLD로남기며자동batch/QA/성공기준변경없음.

capability `approved_training_capabilities_v01.json`/`approved_final_static_capabilities_v01.json`에단계명령·코드SHA고정,신규생성source inventory도별도보관. source immutable부모를수정하지않는다. 안전재개용generation v02는systemd다음시작용으로등록했지만현재v01작업은재시작하지않았다. 중단된출력이있으면검토전재학습/덮어쓰기없음. 재부팅실험은수행하지않았다.

명령: 상위root `status.sh`, `resume.sh`. 실제상태는V02/pipeline_status.json, mixing_execution_v01/status.json, watchdog_status.json 우선. Git에는보고서/핵심코드/요약/경로·SHA만게시하고원본RGB-D/NuRec/weights는로컬보존.

## 계산 예산

이전B1혼합39개PASS의실측평균886.16초/200epoch(1000slot)를참고했다. 새1250slot/bitmap·dualVal/0real추가Val비용을고려해**본학습약12~18 GPU시간**,초기실측전보수적계획으로둔다. 추가C100은현재20관측묶음약167초평균,42묶음약2시간이며진행량에따라갱신한다. 추가Test가림240관측과최종두모델군인식·pose·통합보고는그뒤별도이며정적전체예산은아직미실측이다. 48시간종료/분모축소/성공누락없음.


추가검증:원래57개primarycheckpoint SHA재확인불변/기존perceptionoutput미생성/30가림완료/두capability SHA일치. 현재PID910996/원래Watch3805776 모두실행유지. 새ratio선정에seed42/43/44를모두사용하므로그Val평균을선정과독립적인3seed확증이라고주장하지않는다.

70기본family는동일B1_CLOSED_EV현장안의source조건계보이지70개독립실제현장이아니다. Test독립성도같은현장내10조건계보범위로해석한다. 새seed평균/SD도새독립현장검증이아니다.
