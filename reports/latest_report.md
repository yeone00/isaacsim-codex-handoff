# B1 HR/LR/CAD NuRec 가림 비교 · 가시도 QA 초안 · production pilot 비용

실행·작성: 2026-11-05 KST · Claude Code (Opus 5.5)

성격: train 행만 쓴 진단 및 소규모 production pilot.
- 전체 4,200장 생성 0, YOLO 학습 0, val/test 렌더 0.
- 원본 USD/브릭/manifest/기존 결과는 변경하지 않았다. 변경 0건은 SHA 게이트로 확인했다.
- matte/그림자 작업은 보류했다(실행 0).

경로:
- `R = /home/user/hh/isaac_cosmos/sdg_final/B1_RED_NUREC_VIS_PILOT_20261103_v01` (진단)
- `PR = /home/user/hh/isaac_cosmos/sdg_final/B1_RED_PRODUCTION_PILOT_20261105_v01` (production pilot)

## 1. 요약

| 항목 | 결과 |
|---|---|
| 3표현 가림 진단 (같은 13 job·카메라·설정) | HR/LR/CAD 각 13/13 PASS, renderer Error 0 |
| 추천 ROI 31 load: 2px 침식 기준 보임 비율 최소 | HR 0.997 / LR 0.994 / CAD 0.998. 표현 간 최대 차이 0.006 |
| R3 양성 대조군 | 보임 비율 0.815 / 0.814 / 0.826, soft 0.441 / 0.437 / 0.476. 세 표현이 같은 가림을 검출 |
| production pilot (train 12장면, 41 load) | E/O 포함 3표현 모두 검증 PASS, 123 load-표현 보임 비율 최소 0.990 |
| **production 결함 발견** | RGB 전용 연속 렌더에서 LR/CAD **브릭이 렌더되지 않음**(11/12). v03에서 수정·검증 PASS |
| 표현 간 pairing (카메라/조명/브릭 수/mask 일치) | PASS (12장면, 78 load 쌍). 고장 난 실행은 검사기가 FAIL로 잡음 |
| 전체 1400×3 예상 시간 | RGB+HR canonical **약 4.4 h** · +E(주 QA) **약 5.5 h** · +E+O(보조 QA 포함) **약 18.3 h** |

## 2. HR/LR/CAD 가림 비교

동일한 `R/jobs_v01.json` 13 job(추천 ROI 12 + R3 대조군)을 같은 스크립트 `b1_red_nurec_visibility_pilot_capture_20261103_v02.py`로 표현별 fresh Kit에서 실행했다. matte 바닥 렌더도 같은 절차의 일부로 그대로 수행했지만 해석에는 쓰지 않는다(보류).

| 지표 (침식 2px) | HR | LR | CAD |
|---|---:|---:|---:|
| 추천 ROI load 보임 비율 최소 | 0.99728 | 0.99418 | 0.99771 |
| R3 대조군 보임 비율 | 0.81454 | 0.81371 | 0.82615 |
| R3 대조군 soft | 0.44101 | 0.43658 | 0.47641 |
| R3 load mask 픽셀 | 16397 | 16452 | 16723 |

- 추천 ROI 31 load에서 세 표현의 보임 비율 최대 차이는 0.00574이다. 이번 조건에서는 표현 간 차이가 거의 없다.
- R3에서 CAD가 약 0.012 높다. CAD 실루엣이 조금 커서(16723px) 가려지지 않은 가장자리가 더 많이 포함된 것과 맞는 방향이다. 다만 n=1이므로 일반화하지 않는다.
- **결정성:** 같은 job의 빈 배경 E는 세션 간 비트 단위로 같지 않다(평균 0.03–0.16/255, 고립 픽셀 최대 90). 그래서 E는 같은 세션에서 렌더해야 한다.
- 근거: `load_visibility_3rep.csv`, `cross_rep_spread.csv`, `empty_background_determinism.csv`, `diag_3rep_summary.json`

## 3. 가시도 QA 규칙 초안

전문: `docs/b1_visibility_qa_rule_DRAFT_20261105_v01.md` (DRAFT, 임계값 미확정)

- **주 지표:** 각 표현의 실제 load mask를 2px 침식한 영역에서 \|I−E\| > τ 비율(`vis_hard_e2`). E와 I만 있으면 계산된다.
- **보조 지표:** soft 가시도(`vis_soft_e2`). O 렌더가 필요하다.
- **범주:** LOW_SUPPORT(`px_e2 < N_min`) → FLAG(`< T_flag`) → WATCH → OK. 세 표현 중 하나라도 primary load가 FLAG면 base scene 전체를 FLAG로 표시하고, 세 표현을 함께 관리한다.
- **임계값 결정:** train 분포와 R3 대조군만 사용하고 새 버전 문서로 잠근다. 모델 성능은 쓰지 않는다.
- **처리:** 자동 삭제·대체 없음. H1(유지+FLAG 기록) / H2(학습만 제외) / H3(사전 규칙 대체) 중 연구자가 선택한다.
- **침식 근거:**
  - 원본 약 240px인 가는 load는 2px 침식 후 0–3px만 남아 LOW_SUPPORT에 해당한다.
  - 침식하면 soft의 경계 편향이 줄었다(추천 ROI 최소 0.658 → 0.952).
  - 대조군 보임 비율은 침식 깊이 0→3px에 따라 0.793→0.824로 조금 움직인다. 침식 깊이도 고정 정의로 잠가야 한다.

## 4. production pilot과 발견한 결함

**새 entrypoint:** `scripts/b1_red_production_capture_20261105_v03.py`

- red v03 manifest(SHA 확인)를 직접 읽고, 행마다 ROI 변환을 적용한다. 설정은 ISO25/ACES, dome은 manifest 값 그대로다.
- `--splits`로 허용한 split만 처리하며, 64장면을 넘으면 `--allow-production`이 필요하다.
- 장면별 PASS/FAIL을 기록하고 계속 진행한다. resume을 지원한다.
- E/O/canonical은 옵션이며 단계별 시간을 기록한다.
- 입력 해시 게이트에서는 PROJECT_STATE.md만 명시적으로 제외한다(살아 있는 문서이며 렌더 입력이 아님, 제외 사실을 기록).

**pilot 행:** 렌더 전 규칙으로 고정했다. 3 ROI × scene_seed가 가장 작은 train 4행 = 12장면, load 41개, 장면당 평균 3.42(manifest 평균 2.98).

**결함과 수정 이력(모두 보존):**

| 버전 | 구성 | 결과 |
|---|---|---|
| v01 | E+O(+HR canonical) | 3표현 검증 PASS |
| v01 | RGB 전용 LR | **FAIL 11/12** `ACTUAL_INSTANCE_MASK_EMPTY` — RGB에 브릭 없이 파레트만 찍힘 |
| v02 | + USD 로딩 대기, 빈 mask 재렌더 최대 5회 | **FAIL** LR 11/12, CAD 11/12. 로딩 대기 0회, 재시도 5회 모두 실패 → 원인이 파일 로딩이 아님 |
| v03 | + 이전 장면 삭제 직후 Kit update 8회 | **PASS** LR/CAD 12/12, 재시도 0, pairing PASS |

![RGB 전용 v01 LR: 왼쪽 정상(E/O 실행), 오른쪽 브릭 누락](b1_nurec_visibility_3rep_and_production_pilot_20261105_v01/LR_rgb_only_v01_missing_bricks.png)

- **해석:** 브릭은 instanceable 참조다. 이전 장면 삭제와 같은 프로토타입의 재생성이 한 프레임 안에서 일어나면 LR/CAD instance가 그려지지 않은 것으로 보인다. HR은 canonical 단계가 중간 렌더 역할을 해서 문제가 드러나지 않았다. 이 원인은 v03 수정으로 해결된 결과에서 추론한 것이며 내부 원인을 직접 증명한 것은 아니다.
- **기존 결과 영향 점검:** E/O를 넣은 실행, 진단 v02, Codex 품질 pilot 72장의 표현 간 mask 일치도를 확인했다. IoU 최소 0.85(224px mask), Codex 72장 최소 0.96, 면적비 0.95–1.04로 브릭 누락 징후는 없었다.
- **새 안전장치:**
  - `verify_b1_production_capture_20261105_v01.py`: 결과 파일, 장면 수, PNG 디코딩/SHA, mask 수, renderer Error 0을 검사한다.
  - `verify_b1_crossrep_pairing_20261105_v01.py`: 카메라, 조명, 브릭 수, load mask IoU ≥ 0.7, 면적비 0.8–1.25를 검사한다. 이는 공학적 점검값이며 QA 임계값이 아니다.
  - 고장 난 v01 결과에 검사기를 돌리면 FAIL로 나오는 것도 확인했다(음성 대조).

RGB 전용 v03 결과는 이전 E/O 실행과 렌더 잡음 수준으로만 달랐다(평균 차이 ≤ 1.7/255).

## 5. production 예상 비용 (단일 GPU, 순차, 실측 기반)

장면당 평균 시간(12장면, 초)이다. 괄호는 사용한 실행이다.

| 구성 | HR (canonical 포함) | LR | CAD | base scene당 합 | 1400장면 |
|---|---:|---:|---:|---:|---:|
| C0 RGB만 | 4.91 (noEO v02) | 3.16 (noEO v03) | 3.27 (noEO v03) | 11.3 s | **약 4.4 h** |
| C1 + E (주 QA) | 5.93 (Eonly v03) | 3.99 (Eonly v03) | 약 4.35 (추정: C0 + E 1.08 s) | 14.3 s | **약 5.5 h** |
| C2 + E + O (보조 QA) | 17.45 (v01) | 14.72 (v01) | 14.82 (v01) | 47.0 s | **약 18.3 h** |

- Kit 시작은 세션당 약 20 s로 무시할 수준이다.
- O 렌더의 실제 비용은 NuRec 숨김/표시 전환이며 장면당 약 11 s다. 이 비용은 다음 렌더 단계로 미뤄져 기록된다. 단계별 표에서 "O 0.6 s"로 보이는 것은 오해이며, 장면 전체 시간으로 비교해야 한다.
- pilot의 장면당 load 수가 manifest보다 많아 추정은 약간 보수적이다. 위 시간에는 val/test가 포함되어 있다(1400 = 전체).
- **디스크:** 표현·장면당 약 0.3 MB(RGB만)~0.6 MB(E 포함) → 전체 약 1.5–2.5 GB. 여유 공간은 242 GB다.
- **권장:** C1(E만 추가)이 주 지표 계산에 충분하고 비용 증가는 약 +1.1 h다. O(soft)는 HR 1표현만 또는 FLAG 후보 장면만 사후에 따로 렌더하면 비용을 크게 줄일 수 있다. 이 방식은 미실행 설계다.

## 6. 다음 단계 진입 조건

**대량 생성(4,200장) 진입 전 필요 조건:**

1. 연구자 승인 필요:
   - QA DRAFT에서 침식 깊이, 범주 구조, FLAG 처리 방식(H1/H2/H3)
   - production 구성(C1 권장, 또는 C2)
2. **train 먼저 생성:** `--splits train --allow-production`. 이어서 표현별 검증 PASS, 3표현 pairing PASS, QA 계산을 한다.
3. train QA 분포와 대조군으로 `N_min`, `T_flag`, `T_watch`를 결정하고 QA 규칙 **v02로 잠금**한다.
4. 그다음 val/test를 같은 코드 버전, 같은 설정, 같은 QA 규칙으로 생성하고 검증한다.
5. 모든 split에서 장면별 FAIL 0이거나, FAIL이 있으면 원인 기록과 같은 버전 resume으로 해소한다. 분모에서 제외하지 않는다.

**YOLO 재학습 진입 조건:**
- 위 데이터 패키지가 완성되어 있어야 한다.
- export/폴리곤 검사 PASS
- 학습 adapter dry-run
- v42에서 남은 resume 문제의 확인

별도 승인을 받는다.

## 7. 보존과 기록

- **보존한 실패 실행:** 진단 v01(경로 FAIL), production v01 RGB 전용 LR(브릭 누락), v02 LR/CAD(수정 실패). 출력, 로그, 검증 JSON을 모두 보존했다.
- **Isaac 종료 코드:** 모든 실행이 종료 코드 0이었다. 실패 판정은 결과 파일 검증으로만 했다. ntfy 알림도 이 검증 결과로 SUCCESS/VERIFY_FAILED를 구분했다.
- **코드:**
  - `scripts/b1_red_production_capture_20261105_v01/v02/v03.py` (`2a90892b` / `8d98cc91` / `edc7aabf`)
  - `scripts/verify_b1_production_capture_20261105_v01.py` (`20ebd89e`)
  - `scripts/verify_b1_crossrep_pairing_20261105_v01.py` (`e61181ec`)
  - `analysis/b1_nurec_visibility_3rep_compare_20261105_v01.py` (`27479318`)
  - `analysis/b1_production_pilot_cost_qa_20261105_v01.py` (`9851781a`)
- **주의:** PROJECT_STATE에 이번 작업을 append하면 SHA가 바뀐다. 그러면 PROJECT_STATE를 입력 해시로 검사하는 기존 Codex 스크립트(v05/v06, 준비 v01)와 진단 v02는 SOURCE_HASH_MISMATCH로 멈춘다. 이 스크립트들을 다시 쓰려면 기대 해시를 고치는 것이 아니라, 해당 항목을 명시적으로 제외한 새 버전이 필요하다. production v01–v03은 이미 제외하도록 작성했다.
- 접촉 그림자: 알려진 제한으로 기록했고 보류 중이다(QA DRAFT 6절).
- **PROJECT_STATE append(2026-11-05):** 11-03 Codex B1 작업, 11-03 Claude 감사/설정, 11-03 진단, 11-05 이번 작업을 4개 항목으로 끝에 추가했다. 기존 186,607바이트의 SHA가 이전 값 `d919282d…f19aa`와 같음을 확인했다(PREFIX_UNCHANGED_PASS). 새 SHA는 `6b1b3d68…6049`다.
