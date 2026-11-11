# B1 HR/LR/CAD 공통 HPO 독립 실행 인수인계 — 2026-11-11

## 실행 상태

실제 GPU 학습 RUNNING. Controller PID **3130638**, tmux session **b1_common_hpo_20261111_v01**. 최초 시작 14:01:48 KST. 상태는 외부 root의 hpo_status.json이 최신 권위 자료다. 보고서 작성 시점 스냅샷과 현재 상태가 다를 수 있다.

외부 root: `/home/user/hh/isaac_cosmos/sdg_final/B1_COMMON_HPO_20261111_v01`.

기존 main120과 별도 O50 12셀 종료를 파일과 프로세스로 확인했다. 신규 Isaac/ROS/주행0, 기존 프로세스 종료0. 시작 시 GPU compute는 기존 RustDesk535MiB뿐, 디스크124GB 여유. 패키지 설치/업그레이드0. Ultralytics8.4.129, PyTorch2.7.1+cu128, Optuna5.0.0 유지. pretrained SHA55ed65c56c91713d23e8402371c6c49a6fd84f257f7dce452e8d70e41dcbe152 검증.

## 잠근 탐색과 예산

기존 더 큰 설계는 이번 지시의12후보 예산으로 대체했다. 기본C00+Optuna RandomSampler11개, sampler seed20261111. 작은 예산에서 TPE 우월성을 가정하지 않고 독립 random 탐색을 선택했다. 후보는 성능을 보기 전에 생성·잠금. 실제 설정은 candidates.json, 결과는 hpo_results.csv. 모든 학습은 동일 pretrained에서 새로 시작한다.

- 3표현×2epoch qualification smoke, 결과 선정에 사용하지 않음.
- 12후보×3표현×seed42×60epoch. 학습률 일정은epochs200 그대로 두고60에서정지. 단축 순위의 late-improver 누락 가능성 명시.
- 상위 새후보3개+기본설정×3표현×200epoch, 모두 pretrained부터 새 학습. 단축 checkpoint 이어학습 안 함.
- 선정 설정과 기본설정 seed43/44×3표현×200epoch. seed42는 full 결과 재사용하며 탐색 선택 편향을 명시. 선정설정이 기본이면 중복 학습 생략.
- 최대63학습run/6966 model-epochs. 실패 자동 재시도/추가후보0. 별도 명시적 중단 복구 시 새 attempt 수·비용 추가 기록.
- 최종 checkpoint는 각 모델 자기표현 Val200의 unrounded Mask mAP50–95 strict-greater, 동점 최초epoch. 공통 점수는 세 표현 완전한 성능의 산술평균; 하나라도 실패하면 후보 불완전/선정 제외. 후보 동점은 낮은ID(기본우선).
- Test/가림Test/RealTest189 선정·조기종료 사용0. Train1000/Val200만 symlink한 전용view. 기존v04 Q1의 own-Val checkpoint 기준 유지; 과거 combined/realval checkpoint 기준을 HPO에 쓰지 않으며 추가 realval inference는 하지 않는다. 선정lock 이후 cross-rep Val만 보조 평가.

기존48모델/데이터/분할/Stage4/모델 가중치/안전 기준 불변. 고정 AdamW·batch64·img640·maskratio4·200epochs·AMP·FP32box·workers8·v04 증강을 유지했다. 탐색 seed/학습 seed/고정 dataset scene membership을 protocol.json에서 분리 기록했다. Test를 새 독립 검증으로 주장하지 않는다.

## RNG

기존 PhotoDegrade 원본 SHA 검증 후 그대로 import한다. 실제 Python 전역 random(UL worker seed), noise는 random.getrandbits(32)로 numpy.default_rng를 만든다. 문서의(run seed,epoch,index) per-sample generator 설명과 불일치는 유지·공개한다. RNG 수정0; 새 기본설정도 동일 실행기로 대조. bitwise 완전 재현성을 주장하지 않는다.

## 자동 실행·안전·복구

Python controller가 각 GPU subprocess를 순차 실행한다. 전역flock 및root lock으로중복 controller 방지, 각job전 기존Isaac/train/GPU owner 및25GiB디스크reserve검사. 완료는exit0뿐아니라PASS audit·전체epoch·로그·checkpoint SHA·Val·FP32/photo검사를 통과해야 한다. 실패/중단 로그와 attempt 보존. 중단을 성공으로 처리하지 않는다.

상태 hpo_status.json/hpo_progress.md/hpo_results.csv/jobs.json: 실행 중 약10초 간격, status_snapshots.jsonl: controller가15분 간격 기록. AI 호출이나 cron 의존 없음. hpo_errors.log와각run log/status/traceback에 오류 보존. baseline/qualification 실패·자원충돌은BLOCKED; 다른후보 실패는분모를남기고계속. 정상완료된후보는검증후skip한다.

상태 확인:
```bash
/home/user/hh/isaac_cosmos/sdg_final/B1_COMMON_HPO_20261111_v01/status.sh
tmux attach -t b1_common_hpo_20261111_v01
```
attach는 세션 존재만 확인하는 용도이며 실제 로그는 root/logs/에 저장된다. Ctrl-b,d로 detach. Ctrl-c로 학습을 중단하지 않는다.

안전한 재개:
```bash
/home/user/hh/isaac_cosmos/sdg_final/B1_COMMON_HPO_20261111_v01/resume.sh
```
기존 세션이 살아 있으면 중복 시작 안 함. 죽은 세션에서는 동일 protocol SHA로 재시작하고 verified 완료는skip; interrupted attempt는기록보존후동일pretrained부터새attempt로재실행한다. checkpoint resume 호환성을 검증하지 않았으므로 epoch 이어학습으로 주장하지 않는다. FAILED는자동retry안함; 원인검토가필요하다. 살아있는이전worker는PID검사로BLOCKED하고종료하지않는다. 머신재부팅 후 자동boot서비스는설치하지않았으며위명령으로재개한다.

## 독립 실행 검증과 한계

실행 시작 tool이 반환된 뒤에도 HR→LR→CAD smoke가각각다른PID로자동전환됐다. controller3130638의조상은tmux세션의bash3130636/서버3130635이며Codex tool프로세스가아니다. 따라서Codex사용량소진/대화종료와무관하게OS/tmux가살아있으면계속실행된다. 전원off/재부팅/수동kill까지견디는것으로주장하지않는다. 세부증거 launch_verification.json.

CPU 정책/범위/소스AST/동결SHA/TrainVal회원/패키지버전 사전 검사 PASS. 최초CPU테스트는부동소수점정확등호(.4)때문에실패하여tolerance1e-12로고친뒤PASS; 데이터나기대SHA변경0. root잠금·GPU실행전오류였고본학습실패로숨기지않는다. GPU smoke 증거는각run run_status.json/audit.json. 기존원본과과거실패불변.

완료 시 controller가 final_summary.json, reports/b1_common_hpo_final_20261111_v01.md와 PROJECT_STATE 종료기록을 자동작성한다. 학습곡선원본은각run epochs.jsonl/results.csv/audit.json; 논문용최종그래프·기존48모델과전체비교는종료후별도분석으로남는다. 신규blindTest 및50:50보조학습은이번실행에포함하지않는다.

## 잠근 실제 후보

| ID | lr0 | weight_decay | lrf | warmup_epochs |
| --- | --- | --- | --- | --- |
| C00 | 0.001 | 0.0005 | 0.1 | 3 |
| C01 | 0.000455751421 | 1.499813774e-05 | 0.1182994657 | 2.553403233 |
| C02 | 0.0004912784866 | 0.0006696140875 | 0.2366322628 | 2.260882014 |
| C03 | 0.001564485305 | 0.0001352098476 | 0.09991252986 | 1.220917643 |
| C04 | 0.0002251911145 | 2.436431971e-05 | 0.1015164748 | 4.120894824 |
| C05 | 0.0004324018443 | 0.0007619289253 | 0.2077884398 | 2.325817028 |
| C06 | 0.0006176898401 | 0.000187005529 | 0.2234789956 | 4.478797275 |
| C07 | 0.0004379838322 | 3.086660291e-05 | 0.1847739766 | 3.012606517 |
| C08 | 0.0002820926121 | 2.645665896e-05 | 0.1118812108 | 2.354255127 |
| C09 | 0.0004673722712 | 3.249469199e-05 | 0.1692400831 | 1.794858586 |
| C10 | 0.001051947519 | 0.0001094527152 | 0.1587492623 | 2.328941628 |
| C11 | 0.0009263038569 | 1.379048132e-05 | 0.1736845619 | 2.35293425 |

## 실제 탐색 진입 확인

14:03 KST 기준 HR/LR/CAD smoke3개 모두 PASS, 자동으로 C00 기본설정 HR seed42의 실제60epoch 탐색으로 진입했다. Controller PID3130638, 학습PID3133146. epoch10 완료 및 Mask mAP50–95 .78878587 기록, last.pt와 best_val_maskmAP5095.pt 생성. 이는 초기 중간값이며 최종 성능이 아니다. 실제 후보의 고정train_args 차이0, pretrained동일, 코드SHA불변검증. 살아있는세션에서 resume.sh는 NO_OP라중복없음. GPU학습은1개(약11.6GiB)이고기존RustDesk만함께있다.
