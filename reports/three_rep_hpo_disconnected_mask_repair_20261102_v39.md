# v39 — 3-rep bitmap repair 미완료 / source identity 확인 필요

2026-11-02 KST. **Stage-1 launch-ready NO; NOT_LAUNCHED; trials started=0. 새 6-image/1-epoch smoke NOT_RUN(시도0, exit/metrics N/A). Kit/ROS/robot motion/retry=0, research denominator=0, steering HOLD.**

이번 작업은 요청한 end-to-end repair를 완료하지 못했다. 새 감사 코드의 잘못된 해시 해석으로 CPU 감사가 exit1로 멈췄다. metadata의 `canonical_mask_hash`를 PNG 파일 SHA256 앞16자로 가정했으나, 원래 계산법을 입증하지 못한 검사였다. 이것을 데이터 변조 또는 authoritative lock 위반이라고 단정하지 않는다. 기준 해시를 바꾸거나 검사를 제거해 PASS를 만들지 않았다. bitmap adapter·augmentation·loss minibatch 검증은 미구현/미검증이다. 기존 stock smoke PASS는 새 경로의 증거가 아니다.

## 실제 증거와 중단 지점

새 외부 namespace: [/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261102_v39](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261102_v39).

- [status.json](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261102_v39/status.json): FAIL_STOP 및 전체 traceback. CPU 감사1회/실패1회, GPU smoke0회. 재실행하지 않음.
- [source_evidence.json](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261102_v39/source_evidence.json): 실제 경로·SHA·pixel 수·원본 비교와 두 사례 재현.
- [historical_31.json](/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_HPO_20261102_v39/historical_31.json): 기존 fidelity CSV의 train27/val4 기록 보존. 전체 새 QA 결과가 아님.
- 새 [감사 코드](../scripts/three_rep_bitmap_audit_20261102_v39.py): compile PASS, 실행 FAIL. **현재 그대로 재실행하면 namespace 충돌로 거절하며 학습용 loader가 아니다.**

첫 `TRN_000001 Load_01` metadata 선언은 `d4d2a2a4976b7a4d`. 실제 PNG SHA256은 `bf7ec8b7c3c9a35453209a073532b8f6a10a5bccf1998fd5c0c6fa8724b60695`; decoded uint8(0/255)는 `bb2887188133f5e71ee83ff708d3287381c0254d84b2073fef19449188af4602`; uint8(0/1)는 `0d675392fe54de9290b029157d99b52ee5902e8e02ec88b951ea9cd90d18e23c`. 해시의 입력 표현/생성 출처가 미해결이다. pixel 수11319는 metadata와 일치한다. 해당 파일과 아래 두 실패 사례 모두 original v01 PNG와 v03 PNG의 전체 SHA가 동일했다. 따라서 현재 증거로 원본 bitmap 훼손을 주장하지 않는다.

| 사례 | 이번 직접 재래스터화한 기존 polygon IoU | 추가 px | 새 loss target after |
|---|---:|---:|---|
| TRN_000661 Load_02 | 0.676320272572402 | 190 | NOT_VERIFIED |
| VAL_000151 Load_02 | 0.7846836847946725 | 194 | NOT_VERIFIED |

full-train/val QA: **완료0/7200 images**. 첫 scene source 검사 중 중단됐으며 새 검출 총수 UNKNOWN, 역사31개 대비 새 검출수 UNKNOWN이다. bridge/holes/multiple supports/negative tests 및 no-augmentation exact roundtrip NOT_RUN. 누락 파일은 처리한 첫 입력에서0; 전체 누락 여부 UNKNOWN. manifest mapping(image SHA/GT SHA/target SHA/loader/config SHA)은 미완료이며 존재한다고 주장하지 않는다. sample 제외/자동 재생성0.

최종 manifest expected SHA `2a4782911ef334fc640e9f90ee8120e48ab3c30e25da47603004978835626bf8` 일치, 2800 unique scenes 및 train2000/val400/test400 확인, scene_seed 전체 unique 확인. fidelity CSV/summary의 lock dependency SHA도 일치했다. representation별 전체 image membership·capture/view metadata·augmentation split leakage 검증은 아직 완료하지 못했다. Test/Real Test189 labels·M50 모델은 읽거나 수정하지 않았으며 test 평가0.

## 확인한 원문과 실제 loss 경로

[2026-10-29 원문 보고서](three_rep_hpo_start_20261029_v01.md), `/home/user/assemble_canonical_gt_v03.py`, `/home/user/canonical_gt_to_yolo_seg_v03.py`, `/home/user/hh/isaac_cosmos/scripts/training/run_common_hpo_stage1_v01.py`를 정적으로 읽었다. assembler는 original2598/new187/old15 경로를 구분하고 원본 metadata를 복사한다. converter는 train/val에서 `usable`인 load를 한 instance로 유지한다. original2598 생성기의 short hash 계약은 확인하지 못했다. 다른 nonideal 코드의 hash 함수를 nominal 원본의 authority로 대체하지 않는다. legacy Python import/실행0.

설치 `ultralytics/models/yolo/segment/train.py`와 `utils/loss.py`를 읽었다. segmentation loss는 batch['masks'] tensor를 직접 소비하며 overlap=False에서는 batch_idx별 instance tensor를 고른다. 이 설치본은 prototype 해상도가 다르면 proto를 bilinear로 mask 크기에 맞춘다(loss.py 518–521). 따라서 bitmap adapter 구현 가능성은 있으나 stock polygon 변환을 우회하는 dataset/transform/validation 경로와 호출 증거는 이번에 만들지 못했다. 보간·ignore·instance ownership 정책도 아직 적격화되지 않았다. 이를 training target 보존 PASS로 표현하지 않는다.

HPO protocol은 **Ray Tune OptunaSearch(TPE)+ASHA,40 trials×최대60epochs,grace15,reduction3**, YOLO11n-seg `/home/user/yolo11n-seg.pt`,640/batch64/workers8/AdamW/seed42, pooled val Mask mAP50-95 selector. Stage2 Top5×3rep×150epochs 제안 유지. lr0[1e-4,5e-3]/lrf[.01,.20]/momentum[.85,.98]/weight_decay[1e-6,1e-3]/warmup[0,5]/box[4,12]/cls[.2,1]/dfl[.5,3]/mask_ratio{2,4} 그대로다. 교수 브리핑의 prospective 공간은 사용하지 않았다.

**실행 가능한 Stage1 command 없음**: 새 loader와 smoke 미적격이므로 원본 stock launcher를 새 실행 명령으로 제시하지 않는다. 상한2400 trial-epochs/14,400,000 train-image exposures(6000/epoch; validation 별도), single GPU 순차 검색을 계획할 수 있지만 walltime·batch64 peak VRAM은 UNKNOWN이다. 6장 smoke로 batch64 적합성을 추정해 보장하지 않는다. 전체 검색은 새 loader/QA/smoke 및 예산 검증 뒤 사용자의 별도 실행 승인 gate를 유지한다.

환경 정적 확인: sdg_tools Python 및 설치 source 존재. nvidia-smi 당시 RTX5090 32607MiB 중257MiB 사용, 표시된 작업은 desktop graphics뿐이었다. 해당 시점 process 조회에서 Kit/ROS/경쟁 학습 작업은 발견되지 않았다. torch CUDA 연산 검증·GPU학습은 수행하지 않았다. 패키지 설치0/다른 process 종료0.

## Steering decision note — 기존 증거만 사용

[v38 기존 보고서](construction_site_steering_characterization_and_hr_live_20261102_v38.md)의 15° command, 독립20° measured emergency angle, max .02m/s,50ms control, configured286.4788818359375°/s를 구분한다. HR/LR/CAD28.406/31.389/29.885°/s는 planner 요구량이며 측정 허용 한계가 아니다. 실측 rate-abort와 작은 smooth stationary sweep의 amplitude/ramp/hold/reversal/settling·허용오차는 **UNDEFINED**. 장치/actuator·drive 및 controller 조건에 적용되는 traceable source와 그에 근거한 수치·중단/zero/복원 절차를 명시한 characterization 정책의 명시적 승인이 필요하다. 설정 cap/관측 max를 universal safe bound로 채택하지 않는다.

v30 raw 실제 telemetry **존재 확인**: [steps.jsonl](/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03/attempt_0001/steps.jsonl), SHA `9a77f63c3fe6c1f9e930f2bac46b3cf8505b246acecd2cc48a48747ceeae8215`. 첫 record에 sim_s/wall_s/q_rad/dq_rad_s/named_joint_state가 있다. 후속 별도 retrospective observation은 joint ID mapping·단위·sample timing 검증 후 가능하다. 이번 rate 계산0이며 안전한계 도출0. 추가 rover audit/Kit0. v30 old-quintic physical PASS와 v31/LR·v32/CAD planner FAIL, v35/36 offline27/55221 및 v38 CPU7/7 이력 불변.

## 변경·다음 행동

변경: 새 감사 코드1개, 본 보고서, latest_report, PROJECT_STATE append, 새 외부 namespace의 status/historical31/source evidence. 원본 dataset/manifest/labels/weights/locks/USD/역사출력 수정0. 구현 SHA는 아래와 같다. 원격 mirror는 기존 HANDOFF_REPORT 로컬 동기화 경로로 요청하며 `.git` 부재로 GitHub 반영 완료를 확인하지 못했다.

다음 단일 작업은 **original nominal metadata의 canonical_mask_hash 생성 코드/입력 표현을 확보하여 권위 있는 identity 검증을 해결**하는 것이다. 그 뒤 새 버전에서 전체 source QA→bitmap dataset 및 동일 공간 augmentation adapter→실제 loss minibatch exact QA→한 번의 제한 smoke 순서로 진행한다. 현재 end-to-end repair 및 launch qualification 미완료 상태를 유지한다.

감사 구현 SHA256: `928cdeb9d0bb7b09ac9f67ffcfb04f5ea67204bc582afeb12c3b4bd9c157bc76`. 독립 expected 없는 신규 코드 observed hash이며 완성 loader의 SHA가 아니다.
