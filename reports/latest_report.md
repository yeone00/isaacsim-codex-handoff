# 축소모형 실제 영상 증강·HR/LR/CAD 동결모델 비교 — 독립 v01

2026-11-02 KST. [GitHub Issue #1](https://github.com/yeone00/isaacsim-codex-handoff/issues/1)의 명세를 읽고 실제 실행했다. **실제 영상9개 → 1초간격 원본136프레임 → 원본포함10종 입력1,360장 → 세 모델4,080건 추론 완료, 실패0**이다. 합성 영상이나 v45 영상으로 실제 촬영을 대체하지 않았다. GT가 없어 정확도/GT IoU/AP/mAP는 NOT_ESTABLISHED다.

독립 결과 root: `/home/user/hh/isaac_cosmos/sdg_final/SCALE_MODEL_REAL_VIDEO/results/SCALE_MODEL_ROBUSTNESS_20261102_v01`. v45 외부 root/코드/보고서/latest_report를 수정하지 않았다. v45 보호파일10,493개의 크기·mtime과 핵심SHA 확인 PASS다. PROJECT_STATE에는 이번 독립작업 기록만 추가하며 과거기록을 보존했다.

## 입력·전달 코드 통합

사용자 전달3개 파일은 `/home/user/Downloads/scale_model_codex/`에서 발견했다. 원문은 불변으로 두고 새 `scripts/scale_model_codex_20261102_v01/`에 그대로 보존했으며 원문대비SHA를 대조했다. 원래 모듈은 정적검토 후 import시 실행하지 않는 main guard를 확인했고, 새 통합wrapper에서 `image_variant` 함수와 VARIANTS를 사용했다. Python 구문검사 PASS, 환경추가설치/업그레이드0이다.

입력은 지정된 raw_videos의9개 MP4다. 모두30FPS, decoded512×910 portrait다. reported frame count와 sequential 실제decode수는9/9 exact다. 영상별 metadata에는 orientation meta/auto, SHA, 실제decode수와 추출수가 있다. 원래영상은 종료시SHA 재검증했다.

|video|fps|decoded|sampled|width|height|sha256|
|---|---|---|---|---|---|---|
|IMG_0074.mp4|30.0|822|28|512.0|910.0|d751570ad535d6b05e5fe77e7bbd7abe9bfeee8b0a3b1eb2ec849492d2d9042e|
|IMG_0075.mp4|30.0|597|20|512.0|910.0|c59989009827439b4623f4b8e3b564398410f0936c519e71f23633970624ef2c|
|IMG_0076.mp4|30.0|362|13|512.0|910.0|46c36d57fe812907d69f1a9958bf111e9e3c73d09d2f3397abd701d3127cfe0c|
|IMG_0077.mp4|30.0|455|16|512.0|910.0|043fcf4f99d5a1f61492d7c7de48760466baa708c8e13d4ab3ccfcc23ae212a1|
|IMG_0078.mp4|30.0|434|15|512.0|910.0|a0866f9e924a825c6f92cd7778027965a2321db164dad89c4dcac2f8ab612687|
|IMG_0079.mp4|30.0|283|10|512.0|910.0|26c69811a30f93b9c4b01ee95ad26ff8454021188da32bca4bcda60b7f034e42|
|IMG_0080.mp4|30.0|450|15|512.0|910.0|56dc5e1c556932eeeabfc9adb4c2e864c07308b906c1fa437528c699ad886a18|
|IMG_0081.mp4|30.0|274|10|512.0|910.0|616db7abca3aa65404e53f84dfd3fb78e53af692f1cc2bfe8d28af3f7fff3d53|
|IMG_0082.mp4|30.0|256|9|512.0|910.0|a6ec8fea29a0c84ba06841a69c024c870468e3ab4817513f413ce15f4b990103|

1초간격은 fps30에서 frame index0,30,60,…이며 끝의1초미만 구간도 해당 index가 존재하면 포함했다. 원본 parent_frame_id를 모든파생입력에 유지했다. `frames.csv`는136행, `annotation_frame_list.csv`도136행이다. 실제촬영9편은동일물체/촬영환경을공유할수있어9개독립배포환경이라고하지않는다.

고정 증강: original, brightness0.70/1.30, contrast0.80/1.20(중심127.5), Gaussian noiseσ5/10(8bit·clip), Gaussian blur3×3/5×5, JPEG quality60. JPEG는변환후losslessPNG로저장했다. 모든원본/variant별SHA와seed는 `augmented_manifest.csv`, 원문image_variant 두번실행 exact·PNG roundtrip exact·shape 유지1,360검사는 `augmentation_QA.csv`다. 원본136장과 추가광도변형1,224장을 구분한다. 새실제촬영1,360장이라고하지않는다.

원본품질은Laplacian variance/평균밝기/암부·포화비율과1초이웃sample correlation,128×128 optical-flow median을 계산했다. 이웃sample 평균correlation은영상별약.537–.618이다. 이는실제회전/물체변화/카메라움직임이함께반영된 기술값이며 카메라흔들림만분리한추정치가아니다. blur variance도GT가아닌영상지표다. 명목시점·조명·가림을새요인라벨로만들거나 인과효과를주장하지않았다.

## 실제 추론·smoke gate

먼저각영상의첫sample1개,총9parent×10variant×3모델=270건smoke를실행했다. 오류0/PASS후나머지3,810건을추론해총4,080고유key를완료했다. smoke270은최종집계에한번만포함했다. 새training/HPO/threshold선택/IsaacKit/ROS/로봇/조향0이다. smoke원본9장은HR3/LR4/CAD2검출이며smoke완료를성능PASS로부르지않는다.

RGB프레임을OpenCV BGR ndarray로전달, class0=brick_load/nc1/segment확인, imgsz1280/conf.25/NMSIoU.70/maskthreshold>.5, device0, highest-confidence class0/동률최소index 고정이다. 모델세개는동일1,360개파일SHA를공유한다. 재학습/모델재선택/Test1200/RealTest189접근0이다.

통합시차이: 전달코드의 `retina_masks=True` 및 `>=.5` 대신 기존v43와같은 `retina_masks=False`·threshold>.5후nearest resize를관측전policy에명시했다. 전달코드원문은그대로보존했다. portrait letterbox padding을명시적으로제거하지않는기존nearest-resize방식은작은공간왜곡이가능하다. **이번GT없는검출률은이마스크픽셀변환과분리되지만, 향후사람GT IoU평가전에는원해상도retina 또는정확한unletterbox계약을별도버전으로검증해야한다.** 두방식을동일mask조건으로소급합치지않는다.

모델SHA/원본경로는 `policy_locked.json`에고정했고실행전후일치했다:

- HR_Scan: `257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca`
- LR_Scan: `d58e18a87f4cafba6fd92d8bade6e2ff12ad2380db427311b072859fd2cca42f`
- GeoCAD: `bbfb9fc8d0c421154844f7e299b6d8162b9394eb07d36a31110f593c0813ce8f`

실행환경은기존sdg_tools Python3.11.15/torch2.7.1+cu128/ultralytics8.4.129/numpy2.4.6/OpenCV5.0.0이다. smoke5.747초, full추가61.809초(모델로딩·skip확인포함), full최대RSS1.70360GiB,torchpeakallocated582,363,136bytes이다. torch할당은전체GPU사용량이아니다. 기존GUI프로세스를정지하지않았다. 실제smoke/full/analysisprocess exit0을 `process_exit_receipts.json`에기록했다.

## 측정 결과

아래는각variant의136개parent에서generic brick_load검출이존재한수다. GT일치성공수나accuracy가아니다.

|variant|HR_Scan|LR_Scan|GeoCAD|
|---|---|---|---|
|blur_3|36|25|34|
|blur_5|17|14|18|
|bright_070|49|58|45|
|bright_130|50|43|56|
|contrast_080|48|60|44|
|contrast_120|46|43|43|
|jpeg_60|38|30|20|
|noise_05|4|2|12|
|noise_10|13|26|0|
|original|46|50|40|

원본검출률은HR46/136=33.82%,LR50/136=36.76%,CAD40/136=29.41%다. 검출된집합의조건부평균confidence는HR.7331/LR.8260/CAD.7459이며서로다른검출집합이므로accuracy로비교하지않는다. 이외부영상의검출빈도순서와v45 simulationIoU순서를같은척도로읽지않는다.

sigma5→10에서일부모델검출수가단조감소하지않는현상도실측대로보존했다. 임의threshold나가장좋은증강을선택해새baseline으로승격하지않았다. 원래RGB외부관측은original행만이며증강은영상품질강건성진단이다. generic검출이틀린경우를사람GT없이정답으로셀수없다.

`summary.csv`에는30개모델×variant셀의exact분모/검출률/조건부confidence/원본대비변화가있다. pooled parent검출률과9영상동일비중검출률을따로제공했다. 원본동일비중률은HR.26866/LR.33983/CAD.25239로,긴영상가중pooled률과다르다. 변화량은같은영상내paired차이를9개영상에같은비중으로평균했다. source video를재표집한10,000회bootstrap(seed20261102)구간은탐색적이며9편의촬영종속성을해결하지않는다. 증강child를독립촬영으로재표집하지않았다. formalp값/인과우열/동등성/실로봇검증주장0이다.

`same_frame_model_comparisons.csv`는동일원본/variant에서모델간both/only-first/only-second/neither및영상단위paired차이를기록한다. `per_video_summary.csv`와 `time_block_summary.csv`는영상및5초구간별분모다. `prediction_self_consistency_NOT_GT.csv`는동일모델의original예측과variant예측사이self-IoU이며**GT IoU가아니다**. 양쪽무검출이면undefined로두었다.

그림: `detection_robustness.png`, `conditional_confidence.png`, `original_model_comparison_contact_sheet.jpg`, `augmentation_model_contact_sheet.jpg`, `smoke_model_contact_sheet.jpg`, `input_video_first_frames.png`. 각추론의overlay와선택mask PNG는 `predictions/<model>/<variant>/<frame_id>/`에있다.

## GT·실패·재개 한계

현지입력에사람GT가없어GT프레임0이며 `per_frame.csv`의mask_iou와summary의mean_iou/ΔIoU는공란이다. GT를자동예측으로대체하지않았다. AP/mAP는구현/보고하지않았다. annotation list는사람이원본RGB에가시벽돌load(팔레트/배경제외)를표시하기위한대기목록이지완료GT가아니다. 여러load가확인되면별도instance정의·target규칙이필요하다. first/midcontactsheet에서는빨강적재모형1개씩관측됐지만전체영상의독립instance annotation인증은없다. 시멘트재질·실로봇외부검증으로확장하지않는다.

실제pipeline실패0/4,080,decode실패0/9,augmentation검사실패0/1,360이다. 넓은초기파일검색에서존재하지않는/mnt/data·접근불가system폴더로rgexit2가있었고,결과파일생성중상태확인ls에서아직없는gate파일로exit2가있었다. 이들은추론실패와분리한discovery/status조회오류다. 설치돼있지않은ffprobe에의존하지않고OpenCVmetadata/실제decode를사용했다.

각추론은claim/resultJSON을개별저장하며완료PASS만재개시skip한다. 실패기록이있으면자동재시도로덮지않고중단한다. augmentationprepare는비어있지않은root를덮지않는다. 최초제공코드의전체완료후일괄CSV방식에개별checkpoint를추가했다. 현재추가재실행은필요없다.

## 파일·검사·다음 작업

변경파일은새원문보존3개, `scripts/scale_model_integrated_20261102_v01.py`, `analysis/scale_model_results_20261102_v01.py`, 본보고서와PROJECT_STATE의새독립기록이다. 원래v45/latest_report/handoff/next_task.md는불변이다. 전체입력·weights·증강SHA대조/3모델입력exactpairing/4,080고유key/모든셀136분모검사PASS. sourceSHA는아래와같고실행snapshot은외부root/source에있다.

- `scale_model_integrated_20261102_v01.py`: `3a07223b0d12be65fcecc7974c61c75c268443a21f601b6fa125b247330746cf`
- `scale_model_results_20261102_v01.py`: `c458c798af8c0f8f3fe8aed74c660d4ce52a64020e9431537d11705fe1171324`
- `scale_model_video_robustness.py`: `6501f057e90c1137107e2a76fd988d8edfbdfcfd0db6452477814cd5b1083102`

실제명령(모두기존`/home/user/anaconda3/envs/sdg_tools/bin/python`):

```text
scripts/scale_model_integrated_20261102_v01.py prepare
scripts/scale_model_integrated_20261102_v01.py smoke
scripts/scale_model_integrated_20261102_v01.py full
analysis/scale_model_results_20261102_v01.py
```

판정: 코드통합/영상추출/증강/동결모델비교/그림/보존 **PASS 실제완료**. accuracy/GT IoU/materialsemantic/AP/mAP **NOT_ESTABLISHED**. 다음구체작업은원본annotationlist에사람GT를작성하고,mask좌표계검증을갖춘별도평가버전으로IoU를추가하는것이다. 이번작업이새학습이나robotqualification을승인하지않는다. Issue댓글/원격push는하지않았고원격보고서sync완료는UNKNOWN이다.
