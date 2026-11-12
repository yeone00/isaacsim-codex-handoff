# C-HPO 평가 파이프라인 복구 — 학습/가중치 불변

2026-11-12. 학습57/57은 모두 PASS이며 재학습0. 원래교차Validation은14건이최종수가아니라24/24가실패했다. 원본명령/traceback/checkpoint SHA를 `validation_repair_v01/original_failure_audit.csv` 및 `failed_original_jobs.json`에기록했다. 원본HPO jobs/status/실패로그를덮어쓰지않았다.

## 정확한 실패 원인

Ultralytics Model.load는 checkpoint training args 중imgsz/data/task/single_cls만 overrides로보존한다. 별도Model.val 호출이bitmap필수kwargs를명시하지않아defaults mosaic=1,overlap_mask=True를받았다. bitmap build_transforms의고정계약(혼합증강0/비중첩)에걸려AssertionError가발생했다. mask_ratio default4는이미같았으며문제의원인이아니다. augment=False이므로실제로mosaic augmentation을수행하다실패한것이아니라,평가loader생성시정적config계약충돌이었다. rect는Model.val 기본True로이미참이었다.

설정 assertion을제거하거나GT를polygon으로우회하지않았다. 학습source/weights/분할/선정규칙/후보값/마스크를수정하지않았다.

## 새 evaluator의 경로

원래bitmap module을그대로사용한다. Val는augment=False,mask_ratio4,overlap_mask=False,rectTrue. train전용mosaic/mixup/cutmix/copy_paste는0. 학습중Validation의실제batch는training64의2배인128이므로새평가도128을사용한다. 학습batch를변경한것이아니다. conf.001/NMS IoU.7/maxdet300와설치된SegmentationValidator의mAP/GT matching 로직을유지한다.

학습Validation은FP32 EMA 모델에autocast16을사용한다. 별도AutoBackend의fuse/FP16 weights변환차이를피하기위해읽기전용trainer-shaped validation context로같은native validator를호출한다. optimizer/backward/model.train 호출없음. 지표에필요없는validation loss만빈작업으로대체했다. GT 원본bitmap/인스턴스소유권은그대로이고mask_ratio4의동일최종downsample만수행한다. 원본GT를연결하거나구멍을채우지않는다.

## 검증 및 재현성 한계

3표현각12개Val의own평가2회,순환cross평가1회:9개소규모작업. 동일checkpoint/동일입력/설정의mask 및box mAP 반복값이정확히일치했다. full own-Val210장×3표현도별도수행했다. 입력audit에각RGB/bitmap SHA와픽셀수/인스턴스목록을저장했다. worker는Val view만연결하며Test RGB/GT 배열접근없음.

학습중epoch 원래EMA는FP32였으나동결checkpoint저장시EMA가FP16으로반올림된다. 실제saved_EMA_precision_audit.json에서세표현saved dtype float16 및원래epoch EMA 절대합fingerprint차이를확인했다. 따라서원래학습epoch unrounded mAP를비트단위복원할수있다고주장하지않는다. **동일checkpoint반복은exact**,학습당시FP32EMA와savedcheckpoint지표차이는다음과같이보존한다. 이차이를맞추기위해threshold/선정/모델을수정하지않았다.

| 표현 | 학습 epoch Mask mAP | saved checkpoint 재평가 | 차이(%p) |
|---|---:|---:|---:|
|HR_Scan|94.282263%|94.299684%|+0.017421|
|LR_Scan|93.184880%|93.186714%|+0.001834|
|GeoCAD|95.522348%|95.405081%|-0.117268|

## 선정과 완료 판정

원래selection_lock의candidate C06을보존한다. objective는seed42,200epoch own-Val Mask mAP의HR/LR/CAD동일가중평균이다. cross-Val는잠금상보조지표이며복구결과로후보를다시선정하지않는다. Test성능미사용. C06의원래full score94.329830%,baseline94.287328%,차이+0.042503%p. 이는seed42선정비교이며3seed일반화개선확정이아니다. baseline43/44는이번57학습예산에없으므로baseline3seed개선이라고주장하지않는다.

공통설정:lr0=.000888131352250591,weight_decay=.0008730658008775225,lrf=.13119036537141066,warmup_epochs=4.486041867303101. optimizer/기타동결조건불변.

원래24attempt 실패는영구보존한다. 복구24건과checkpoint SHA를검증한뒤에만새 `validation_repair_v01/HPO_recovered_status.json`을COMPLETED로기록한다. 원래 `C_COMMON_HPO_v02/hpo_status.json`의COMPLETED_WITH_FAILURES는그실행기록이므로덮어쓰지않는다. 현재운용상태는상위production_status와새recovered status를본다.

## 독립 후속 실행 및 알림

평가전용service `c-hpo-validation-repair-20261112-v01.service`;controller가GPU전역lock으로worker를하나씩실행하고완료artifact/체크포인트불변성을확인한다. 원래Controller는이미실패종료한상태를보존했고기존Watchdog/ntfy/GitHub서비스는중단하지않았다. 학습재개명령없음. resume.sh는현재복구service를중복없이start한다. interrupted attempt를무조건성공/재시도로처리하지않는다.

복구성공후별도source `c_depletion_post_hpo_static_20261112_v03.py`가훈련용가림구현점검→Test가림생성→인식/pose정적평가로이어진다. 모델계보/원래Test/판정기준/GT운용입력제한은불변. 새capability파일에SHA를기록했고완료판정을원래실패status대신복구검증결과에연결했다. pooled/상태별/macro CPU보고관찰자도recovered정적완료root를기다리는별도service로등록했으며기존보고프로세스를중단하지않았다. 물리pilot/본300/별도150은HOLD유지.

첫실패ntfy서버전송은16:43경HTTP200로그가있으나handset수신UNKNOWN. 기존경고가이전C_COMMON_HPO_v01경로를가리킨결함을확인했다. 이번복구중정확한v02로그경로를포함한고우선순위알림을기존hook으로전송해HTTP200을확인했고receipt를보존했다. 신규오류는복구controller가정확한로그경로로즉시notify하고HOLD event를기존watchdog의재시도queue에도보낸다. 새서버/topic/인증생성없음. AI가실행중이아닌시간의이채팅선제메시지는불가능하며로컬ntfy가담당한다. 서버전송과휴대폰수신을구분한다.

## 코드·원본 식별

- 수정 전 evaluator SHA256 `033f3e278253a7181a398d631d4323165b0cccff7841a5b875654c7a94dcebb8`
- 새 evaluator SHA256 `a622913f13d2385e50914928f186590da28278ec7730f70aa0baa134d07a59d0`
- 기존bitmap loader SHA256 `8dd6f00730f0de9634831929eb18fe38d2df57a66423101c4f7aec4d23e2090d`
- 원래selection lock SHA256 `8b1df58783bb693ee2f3a4c36a186a6d05ddc74da246b532f091875e562f4fdf`
- 57개 checkpoint 경로·SHA: `validation_repair_v01/training_inventory_before.json`;복구완료후모두재검증. 재사용모델C00 seed42×3및C06 seed42/43/44×3의자기표현외24평가. 모든GT원본·학습결과불변.
