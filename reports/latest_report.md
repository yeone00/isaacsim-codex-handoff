# C 데이터 마스크 인코딩 복구 및 독립 HPO 재개 — 2026-11-12

## 실제 상태와 기존 실패 보존
C RGB-D 4410/4410, 210 production batches 모두 PASS_CAPTURE. 원본 capture/GT/기존 모델/USD/LOCKED 레시피는 수정하지 않았다. 기존 production controller는 08:44 QA 변환 실패로 종료했다. `dataset_QA_v01/result.json` HOLD_MASK_ENCODING와 production_jobs FAILED 기록은 그대로 보존한다.

원본 usable load instances 13986 중 1782개가 단일 lossless polygon으로 표현되지 않았다. 1689개는 다중 연결 성분, 177개는 구멍 포함(서로 중복 가능), 나머지 단일 성분 93개도 구멍으로 실패했다. 표현 중복 제외 scene ID 327개. 원본 GT를 연결하거나 구멍을 채우거나 인스턴스를 나누지 않았다.

## 별도 bitmap adapter
`scripts/c_depletion_bitmap_adapter_20261112_v01.py` 및 QA worker 별도 구현. `C_BITMAP_PACKAGE_v01`에서 모든 usable instance의 원본 PNG를 직접 읽는다. .txt는 bbox bookkeeping이며 segmentation GT로 쓰지 않는다. Train/Val/Test=1050/210/210 per representation, 70 source families, HR/LR/CAD 공통 split/점유/카메라를 유지한다. 기존 pipeline의 single polygon encoding을 bitmap으로 바꾼 C-only 학습 계보이므로 기존 B1 polygon model과 모든 차이를 HPO 효과라고 주장하지 않는다.

새 QA는 원본 4410건의 파일 SHA·float32 depth·캘리브레이션·벽돌수·cross-rep canonical masks exact 검사를 재실행하여 PASS. 결과는 `dataset_QA_bitmap_v01/result.json`. 구 geometry support 검사이며 동적 안정성/실제 현장 floor datum 인증이 아니다. 원본 1782 인코딩 실패가 사라진 것이 아니라 bitmap 경로에서는 polygon 변환 자체를 사용하지 않는다.

CPU 회귀 32 seeds: 설치된 RandomPerspective의 image/난수 상태와 동일, 동일 행렬의 nearest mask 변환·flip·letterbox·구멍/분리 영역 보존·mask_ratio1 exact 검사 PASS. 실제 3표현 train/val loader 각 3샘플과 collate PASS. mask_ratio4 최종 cv2.resize는 설치된 polygon2mask의 최종 downsample과 동일 방식을 유지한다. augmentation 확률, PhotoDegrade 구현/RNG, optimizer/FP32 boxloss/AMP/batch64/img640는 변경하지 않았다.

기존 PhotoDegrade 삽입기가 class name Format을 검사하여 첫 CPU 통합 검사가 실패했다. 준비만 된 HPO root v01은 미실행 상태로 보존했다. 새 worker v03는 adapter Format class의 표시 이름을 맞추어 원래 삽입기를 그대로 사용한다. 실패한 CPU 시도는 qualification 기록에 명시한다. 새 HPO root는 **C_COMMON_HPO_v02**.

## 실제 독립 재개
service `c-depletion-bitmap-continuation-20261112-v01.service`에서 C-HPO controller v03 실행. HR smoke 2 epochs PASS 후 LR smoke로 자동 전환 확인. 실제 checkpoint/Validation/FP32·AMP audit 검증 후 완료 판정. 후보12개, 최대57 train/5766 epochs, 기본과 B1 C05 포함, Train/Validation만 선택, fresh pretrained, 동일4파라미터 공간 유지. 최종3seed 및 cross-expression Validation 후 static occlusion qualification→Test perception→pose worker 자동 연결. `static_evaluation_capabilities_bitmap_v01.json`에 별도 source SHA 고정. 기존 B1 HPO 완료63+36 원본과 86.459% baseline vs86.308% C05 평균 개선 없음 기록을 유지한다.

기존 watch PID는 중단하지 않았으며 production_status에 포함된 새 C_HPO를 감시한다. 추가 publisher는 기존 Git lock/allowlist/secret scan/remote SHA 검증을 재사용한다. ntfy 기존 private config 유지; 새 인증·서비스 없음. 오래된 failed production service는 재부팅 시 구 실패 경로가 실행되지 않게 enable만 해제했고, 실행 중인 연구 프로세스는 중단하지 않았다. 새 continuation service enable. 재부팅 실제 검증은 미수행. 실패/중단 attempt는 자동 성공/무제한 재시도하지 않는다.

## 기존 Replicator 로그 오류와 구분
`mask_error_audit_v01/result.json`: production210 logs 모두 NumPy 변환 예외가 있으며 총26370 occurrence. 모든210 capture 결과/4410 source SHA·depth·cross-rep canonical 검사는 PASS. 단일 polygon의 표현 불가능성과 이 renderer 예외는 별개 문제이며, 인과관계/완전 무해함을 확인한 것이 아니다. renderer root cause는 미해결로 보존. 원본과 실패 로그를 지우거나 재렌더하지 않았다.

## 상태·재개·다음 단계
외부 root: `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02`.
상태: 상위 root의 `status.sh`, `execution_v02/production_status.json`, **`C_COMMON_HPO_v02/hpo_status.json`** 순으로 확인.
재개: 상위 root `resume.sh`는 live service 중복 실행 없이 start. 중단 attempt는 검토 후 새 attempt가 필요하며 원본 상태를 지우지 않는다.

후속 자동 범위는 C-HPO→최종 모델→가림 생성 QA→인식/pose 정적 평가까지다. 성공 기준 출처(.11m/7.34° vs.10m/5°)와 실제 support datum, ROBUST_A/안전 파일럿 검증 미확정으로 물리pilot/본300/별도O50150은 HOLD, 새 주행0. 성공률/분모를 혼합하지 않는다.


09:37 검증 추가: HR/LR/CAD smoke 각2epoch 모두 PASS/3 checkpoint SHA 및 모든 run checks 확인. 현재 screen_C00_HR_Scan_s42 60epoch 탐색으로 자동 진입. continuation PID106568, HPO PID106572, screen worker PID109027. HPO 소스 lock6개 현재 SHA 일치. 일부 정상 AMP overflow skip는 별도 기록했고 nonfinite forward0; 오류 은폐하지 않음. GPU smoke 증거 bitmap_qualification_v01/GPU_smoke_verified.json. GitHub 원격 검증 commit2776ce1e3fcc2e1e2620efb3dac090e37d2117e6, 추가본 다음 주기 동기화.
