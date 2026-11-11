# G1 HR/LR/CAD 주행 성능 차이 원인 감사 (2026-11-11)

## 결론과 범위

HR7/10·LR10/10·CAD8/10은 기존 결과 그대로다. **현재 자료만으로 에셋 표현 자체의 우열을 뜻하지 않는다.** HR의3실패는 O25에서 인식2건과 속도 안전장치1건으로 나뉜다. CAD의2실패는 O25 인식1건과 O0 촬영1건이다. LR은 이10조건에서 모두 성공했지만10개 독립 현장이나 충분한 반복 표본이 아니다.

본 주행·O50가 종료되고 GPU가 비었음을 확인한 뒤 저장 이미지에서만 별도 추론 진단을 했다. 새 주행/렌더/학습은0이다. HPO는 이 진단 중 실행하지 않았으며, 진단 결과를 B1 HPO의 후보 선정에 사용하지 않는다. M50와 B1 증강 모델을 구분한다.

## HR 실패3건과 동일 조건 비교

| Scene | 표현 | 버전 | 시작 x,y,yaw | 원본 결과 | 원인 | conf | pose XY m | 초기계획 | 속도 최대 m/s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S2_L4_O25 | HR_Scan | run02 | [-25.888, 26.705254968739226, 90.0] | FAIL_A | PERCEPTION_NO_DETECTION: | None | None | False | 0.0 |
| S2_L4_O25 | LR_Scan | run02 | [-25.888, 26.705254968739226, 90.0] | SUCCESS | None | 0.958561360836029 | 0.026505820037655208 | True | 0.02886310098792765 |
| S2_L4_O25 | GeoCAD | run02 | [-25.888, 26.705254968739226, 90.0] | FAIL_A | PERCEPTION_NO_DETECTION: | None | None | False | 0.0 |
| S3_L4_O25 | HR_Scan | run02 | [-25.888, 26.805254968739227, 92.0] | FAIL_D | SPEED_GUARD_0.03 | 0.8176527619361877 | 0.028188241358170246 | True | 0.03056994283817932 |
| S3_L4_O25 | LR_Scan | run02 | [-25.888, 26.805254968739227, 92.0] | SUCCESS | None | 0.9620092511177063 | 0.024284636908571612 | True | 0.029733931918961436 |
| S3_L4_O25 | GeoCAD | run02 | [-25.888, 26.805254968739227, 92.0] | SUCCESS | None | 0.8491916656494141 | 0.025572606190564107 | True | 0.027322661899013962 |
| S4_L4_O25 | HR_Scan | run02 | [-25.888, 26.805254968739227, 88.0] | FAIL_A | PERCEPTION_NO_DETECTION: | None | None | False | 0.0 |
| S4_L4_O25 | LR_Scan | run02 | [-25.888, 26.805254968739227, 88.0] | SUCCESS | None | 0.9571762084960938 | 0.02342209869486026 | True | 0.029360676784503808 |
| S4_L4_O25 | GeoCAD | run02 | [-25.888, 26.805254968739227, 88.0] | SUCCESS | None | 0.8082336783409119 | 0.026336669040562668 | True | 0.025198475592793958 |

HR 실패 원본 RGB/depth、detections、모델 manifest、session 실패 로그의 전체 경로와 SHA는 evidence의 HR_failures_3.json 및 inputs_sha256.json에 있다. actual inference의 후보가 없는 경우 confidence는0이 아니라 N/A이고, 예측 mask도 존재하지 않는다.

## 촬영·GT·가림률·전처리 감사

모든 O25 대응 HR/LR/CAD에서 카메라 optical world transform은 같은 시작점의 fixture와 원소별 **차이0**이었다. 해상도640×480, depth와RGB shape 일치, 저장 PNG의 BGR 값은 numpy RGB의채널역순과pixel exact였다. 전처리는原코드처럼 RGB numpy를BGR로바꿔 imgsize1280의YOLO에전달한다. mask는>.5 후nearest로640×480에복원한다. conf≥.25, NMS IoU.70, device0을유지했다. 촬영 wall/sim 시각과 카메라 XYZ·checks는 camera_occlusion_preprocessing.csv에 있다.

본주행에는fresh semantic GT mask를저장하지않았다. fixture의gt_target_mask_visible.npy는판을넣기전HR정규targetmask이며, 함께저장된gt_panel_mask.npy도판을넣기전이라0픽셀이다. 이를현재O25의GT로오인하지않았다. 대신동결fixture의panel_screen_rect를pixel-center규칙으로raster화했다. 4시작점모두render기록의panel면적및가림률과정확히일치하고카메라변환도exact라위치정합을확인했다. 시각화의초록색은**fixture canonical HR 기준GT−재구성판**이다. 새로운주행프레임의semantic정답이나표현별silhouette정확도인증은아니다.

| 시작 | fixture 실측 가림률 | 판 pixel수 | fresh 주행 GT mask |
| --- | --- | --- | --- |
| S1 | 25.202001% | 2108 | 없음, reference로 명시 |
| S2 | 24.988904% | 1888 | 없음, reference로 명시 |
| S3 | 24.597027% | 1980 | 없음, reference로 명시 |
| S4 | 24.730290% | 1980 | 없음, reference로 명시 |

주행 panel_removed의가림률은fixture실측값을복사한기록이며각주행에서독립실측한값으로부풀리지않는다. 조명은같은동결현장stage를사용하지만독립photometric센서측정은없다. 시작좌표·projection checks·물리공통게이트PASS가모든광학차이를제거한다는뜻은아니다.
## M50 모델 계보와 연결

| 표현 | 선정epoch | 선정데이터/지표 | checkpoint SHA256 |
| --- | --- | --- | --- |
| HR_Scan | 25 | Real Val48 / Mask mAP50-95 | 257d69b3ca845aed41848f6edbf867e131057f48a77e88e1a9e92372aa6ff8ca |
| LR_Scan | 22 | Real Val48 / Mask mAP50-95 | d58e18a87f4cafba6fd92d8bade6e2ff12ad2380db427311b072859fd2cca42f |
| GeoCAD | 22 | Real Val48 / Mask mAP50-95 | bbfb9fc8d0c421154844f7e299b6d8162b9394eb07d36a31110f593c0813ce8f |

실제frozen_model_manifest·설정파일·선정lock·원래epoch checkpoint·배포복사본의SHA가모두일치했다. M50는40epoch학습의Real Val48 Mask mAP 최고선정, imgsz1280계열이다. B1 증강모델의recipev04/200epoch/imgsz640계열로바꿔쓴증거는없다. lock당시real_test_used=false는역사기록이며Real Test189가현재도미개봉이라는뜻은아니다. Test189는잠금후이미평가됐고이번감사나HPO선정에사용하지않는다.

## 저장 입력 재추론 및 모델 교체 진단

O25의12개원본RGB-D에서자기표현모델을원래설정으로재추론했다. 12/12에서후보수·class·confidence(최대차1e−6이내)·mask면적·선택mask pixel XOR가일치했다. 재현되지않는차이는0이다. 결과를원본에덮어쓰지않았다.

동일12이미지×3모델=36회교체진단과HR실패2이미지×3모델의conf.001별도진단6회, 총42회다. 교체모델·낮춘confidence는진단용이며운영성공으로집계하지않는다. 이조건에서LR모델은HR실패이미지에서도목표를검출했다. 따라서HR이미지에검출가능한정보가전혀없다는설명은맞지않는다. 모델가중치·훈련도메인·체크포인트선정의영향이섞여있고순수에셋효과로분리되지않았다.

| HR 원본장면 | 모델 | 진단설정 | 후보수 | 최대confidence | reference IoU 최고 |
| --- | --- | --- | --- | --- | --- |
| S2_L4_O25 | HR_Scan | ORIGINAL_SETTINGS | 0 | None | 0 |
| S2_L4_O25 | HR_Scan | LOW_CONF_DIAGNOSTIC_NOT_OPERATIONAL | 1 | 0.015696251764893532 | 0.9481503058549374 |
| S4_L4_O25 | HR_Scan | ORIGINAL_SETTINGS | 0 | None | 0 |
| S4_L4_O25 | HR_Scan | LOW_CONF_DIAGNOSTIC_NOT_OPERATIONAL | 1 | 0.1203119307756424 | 0.8687760608290409 |
| S2_L4_O25 | LR_Scan | ORIGINAL_SETTINGS | 1 | 0.9598067998886108 | 0.9531802120141343 |
| S2_L4_O25 | LR_Scan | LOW_CONF_DIAGNOSTIC_NOT_OPERATIONAL | 2 | 0.9598067998886108 | 0.9531802120141343 |
| S4_L4_O25 | LR_Scan | ORIGINAL_SETTINGS | 1 | 0.9049816727638245 | 0.9586980306345733 |
| S4_L4_O25 | LR_Scan | LOW_CONF_DIAGNOSTIC_NOT_OPERATIONAL | 2 | 0.9049816727638245 | 0.9586980306345733 |
| S2_L4_O25 | GeoCAD | ORIGINAL_SETTINGS | 0 | None | 0 |
| S2_L4_O25 | GeoCAD | LOW_CONF_DIAGNOSTIC_NOT_OPERATIONAL | 1 | 0.01265182625502348 | 0.95774231678487 |
| S4_L4_O25 | GeoCAD | ORIGINAL_SETTINGS | 1 | 0.879223108291626 | 0.7042310821806347 |
| S4_L4_O25 | GeoCAD | LOW_CONF_DIAGNOSTIC_NOT_OPERATIONAL | 1 | 0.879223108291626 | 0.7042310821806347 |

HR의conf.001진단에서는S2에약.0157, S4에약.1203의낮은confidence로목표형상mask가나왔다. 둘다원래.25문턱미만이다. reference IoU는각약.948/.869로마스크형상을전혀못만든경우와다르다. **이는문턱을낮추면주행이성공한다는실험이아니며문턱을변경할근거로자동사용하지않는다.** 모델confidence의분포/도메인반응이확인된기전이고그훈련상원인은아직가설이다.

## 단계별 성능과 버전 혼재

| 범위 | 표현 | N | 검출 | pose | 계획 | 실제이동 | 작업성공 | 실패원인 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all10 | HR_Scan | 10 | 8 | 8 | 8 | 8 | 7 | {'SPEED_GUARD_0.03': 1, 'PERCEPTION_NO_DETECTION:': 2} |
| all10 | LR_Scan | 10 | 10 | 10 | 10 | 10 | 10 | {} |
| all10 | GeoCAD | 10 | 8 | 8 | 8 | 8 | 8 | {'CAPTURE_BUFFERS_INVALID': 1, 'PERCEPTION_NO_DETECTION:': 1} |
| run01_only | HR_Scan | 3 | 3 | 3 | 3 | 3 | 3 | {} |
| run01_only | LR_Scan | 3 | 3 | 3 | 3 | 3 | 3 | {} |
| run01_only | GeoCAD | 3 | 2 | 2 | 2 | 2 | 2 | {'CAPTURE_BUFFERS_INVALID': 1} |
| run02_only | HR_Scan | 7 | 5 | 5 | 5 | 5 | 4 | {'SPEED_GUARD_0.03': 1, 'PERCEPTION_NO_DETECTION:': 2} |
| run02_only | LR_Scan | 7 | 7 | 7 | 7 | 7 | 7 | {} |
| run02_only | GeoCAD | 7 | 6 | 6 | 6 | 6 | 6 | {'PERCEPTION_NO_DETECTION:': 1} |
| run02_O25 | HR_Scan | 4 | 2 | 2 | 2 | 2 | 1 | {'SPEED_GUARD_0.03': 1, 'PERCEPTION_NO_DETECTION:': 2} |
| run02_O25 | LR_Scan | 4 | 4 | 4 | 4 | 4 | 4 | {} |
| run02_O25 | GeoCAD | 4 | 3 | 3 | 3 | 3 | 3 | {'PERCEPTION_NO_DETECTION:': 1} |

O25는12개모두run02/runner v04/session v03다. 따라서HR1/4·LR4/4·CAD3/4라는O25차이는run01/run02혼재만으로설명되지않는다. run02만의공통7조건에서도HR4/7·LR7/7·CAD6/7로순서는유지된다. 다만표본이적고반복이없어순위의일반화나유의한에셋효과를주장하지않는다. run01의CAD O0실패는CAPTURE_BUFFERS_INVALID였고이를인식모델의성능저하로분류하지않는다.

보정A의위치/횡종오차와경로곡률은matched_O25_case_details.csv에기록했다. 검출된G1입력은전부pose와초기계획을통과했다. HR S3의위치오차는약28.19mm였으나계획은승인됐다. 성공한subset의위치오차만비교해표현의정밀도순위를단정하면선택편향이생긴다.

## HR S3 속도 안전장치1건

원문종료reason은LEGS_INCOMPLETE이지만, step6230/sim103.88333875에서raw root planar speed=.03056994284m/s로고정.03guard가작동했다. PRE인증은있고FINAL인증은없다. 같은시각FD속도는약.02346m/s로원시PhysX순간속도와차이가있다. 기존guard를유지하고FAIL_D/SPEED_GUARD_0.03을보존했다. 후속driver의SUPERVISOR_ABORT는감독종료후증상이지최초원인을바꾸는근거가아니다. 반복실험없이이속도spike를HR에셋의물성효과로단정할수없다. 초기추정에따른경로/조향·물리비결정성·실행부하가가능한원인이다.

## 사실·가능한 원인·미검증 가설

| 구분 | 내용 |
| --- | --- |
| 확인 사실 | HR인식실패2건은원래.25설정에서완전재현. LR모델은동일HR픽셀에서높은confidence로검출. SHA·전처리·같은시작점의카메라변환일치. |
| 확인 사실 | O25는전부같은버전. HR의나머지실패는인식이아니라기존속도guard. CAD촬영실패1건은별도infra. |
| 가능한 원인 | M50모델별가림도메인반응·confidence분포차이가HR2실패의직접경로. 표현별데이터/가중치/선정epoch와에셋외관이함께변한설계. |
| 미검증 가설 | 특정훈련분포나재질색/texture/형상차이가HRconfidence를낮춘원인. M50epoch선정차이의효과. 속도spike의에셋고유물성효과. |
| 검증 한계 | freshsemanticGT없음,같은현장10조건·반복1회,독립photometric측정없음. cross-model결과는진단이지새블라인드성능검증이아님. |

## 필요한 최소 추가 주행 설계 — DRAFT, 실행 안 함

우선추가주행없이동일입력모델교체진단42회로인식기전을확인했다. 속도실패의재현성을확인할최소물리묶음은**S3/L4/O25×HR/LR/CAD×3반복=9회**를권고한다. 기존runner v04/session v03·M50 SHA·A·TC-S·속도.03·조향/충돌/정지기준을그대로고정하고새namespace에서실행한다. 매회freshRGB-D로전체E2E를수행하며GT/frozen pose로대체하지않는다. 표현순서는사전에회전시키고로그·frame·실패·분모9를보존한다. 9회는3개의에셋조건을반복한것이지9개독립현장이아니다. HPO와GPU동시실행은금지한다.

이묶음은추가설계일뿐아직수행하지않았다. 기존3실패를지우거나HR이성공하도록설정을바꾸지않는다. B1 HPO결과로M50주행모델을자동교체하지않는다.

## 시각자료와 보존

모든이미지는외부root `SDG/G1_REPRESENTATION_AUDIT_20261111_v01/panels/`의로컬전용이다. HR실패2개각각RGB/기준GT/원래모든후보(0개)/저신뢰도진단을한화면에제공했고, S1–S4의HR/LR/CAD같은장면패널4개도생성했다. 원본사진에사람형상이있을수있어공개GitHub에이미지를올리지않는다. 텍스트보고서와원인별CSV만동기화대상이다.

PASS: 입력전후SHA불변,3M50 source/locked/model-manifest SHA,12원래설정재현,4fixture raster면적/coverage exact,12cameraT exact,30cell분모/원본결과보존. UNKNOWN: 표현단독인과효과·새freshsemanticGT·추가9회주행. 새주행/렌더/학습0.

## 보정 A의 조건부 오차와 계획 수치 보충

실패 입력은 오차 평균에 넣지 않았다. 아래 종·횡 오차는 부호 있는 평균이며, XY는 거리 오차 평균이다. 표현마다 계산 성공 장면이 다르므로 첫 세 범위의 평균만으로 정밀도 순위를 비교하면 안 된다. 마지막 범위는 세 표현 모두 계산에 성공한 O25의 S1/S3 두 조건만 대응시킨 것이다. 전체 계획 승인 수에는 촬영·인식 실패도 원래 분모로 남겼다.

| 범위 | 표현 | 전체 시도 | 계산 성공 | 계획 승인 | XY 평균 mm | 횡 오차 평균 mm | 종 오차 평균 mm | 계획 최대 곡률 평균 1/m |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all10 | HR_Scan | 10 | 8 | 8 | 9.846 | -9.631 | 1.705 | 0.033390 |
| all10 | LR_Scan | 10 | 10 | 10 | 12.414 | -12.209 | 1.865 | 0.041121 |
| all10 | GeoCAD | 10 | 8 | 8 | 12.354 | -12.183 | 1.394 | 0.046393 |
| run02 | HR_Scan | 7 | 5 | 5 | 12.589 | -12.362 | 1.879 | 0.038993 |
| run02 | LR_Scan | 7 | 7 | 7 | 15.464 | -15.254 | 2.057 | 0.048419 |
| run02 | GeoCAD | 7 | 6 | 6 | 14.915 | -14.755 | 1.401 | 0.051720 |
| O25 | HR_Scan | 4 | 2 | 2 | 24.991 | -24.855 | 2.468 | 0.054713 |
| O25 | LR_Scan | 4 | 4 | 4 | 24.105 | -23.964 | 2.490 | 0.063890 |
| O25 | GeoCAD | 4 | 3 | 3 | 25.840 | -25.805 | 1.335 | 0.075495 |
| O25_common_pose_S1_S3 | HR_Scan | 2 | 2 | 2 | 24.991 | -24.855 | 2.468 | 0.054713 |
| O25_common_pose_S1_S3 | LR_Scan | 2 | 2 | 2 | 23.246 | -23.092 | 2.467 | 0.051326 |
| O25_common_pose_S1_S3 | GeoCAD | 2 | 2 | 2 | 25.592 | -25.561 | 1.252 | 0.056687 |

원자료와 추가 집계: `reports/g1_representation_audit_evidence_20261111_v01/pose_planning_conditional_summary.csv`. 이 수치는 원래 주행의 저장 결과를 요약한 것이며 재추론 결과로 대체하지 않았다.
