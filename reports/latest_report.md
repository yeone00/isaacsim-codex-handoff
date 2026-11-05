# B1 NuRec 가림 검출 · matte 바닥 소규모 진단 (HR, train 13 job)

실행: 2026-11-03 15:52–16:04 KST · 보고서 작성: 2026-11-05 · 작성: Claude Code (Opus 5.5)

성격: **진단 pilot**. 데이터셋 생성 0, canonical GT 생성 0, 학습 0, 물리·주행 0. 원본 USDZ, 브릭, manifest, 기존 출력, PROJECT_STATE는 변경하지 않았다. train 행만 사용했고 val/test는 열지 않았다.

출력 루트 `R = /home/user/hh/isaac_cosmos/sdg_final/B1_RED_NUREC_VIS_PILOT_20261103_v01`

## 1. 결론

| 질문 | 판정 | 근거 |
|---|---|---|
| NuRec를 끈 물체 전용 렌더(O)가 기준 이미지로 쓸 만한가? | **PASS** | 추천 ROI 12 job, 가려지지 않은 브릭 픽셀에서 \|I−O\| 중앙값 2–3/255, p95 8–14 → NuRec가 메시 조명을 거의 바꾸지 않음 |
| E/I/O 3장으로 NuRec 가림을 검출할 수 있는가? | **PASS (양성 대조군 기준)** | R3 대조군: 완전가림 판정 기준 보임 비율 0.793(2026-11-03 별도 측정 20.9 % 가림과 일치), 반투명 포함 soft 가시도 0.424. 지도상 위치가 RGB의 장비·벽 가림과 일치 |
| 추천 ROI 3곳(이번 12 job)에 NuRec 가림이 있는가? | 12 job 31 load 모두 완전가림 판정 보임 비율 ≥ 0.991 | 단, 1400 장면 전체는 **UNKNOWN**. 12개 층별 대표 장면 결과일 뿐이다 |
| matte/shadow catcher 바닥으로 접촉 그림자를 만들 수 있는가? | **FAIL (이 방식)** | matte plane이 NuRec 바닥을 **검게 덮었다**. 바닥 영역 \|M−I\| 평균 191–227/255. RTX matte pass는 dome 배경과 합성할 뿐 NuRec Volume을 배경으로 취급하지 않는 것으로 보인다 |

![R3 양성 대조군: I | E | O | 가시도 지도(초록 보임, 빨강 가림) | matte 바닥](b1_nurec_visibility_matte_pilot_20261105_v01/panel_R3_control.png)

![R1 D4 load5: 가림 없음, matte 바닥은 검게 실패](b1_nurec_visibility_matte_pilot_20261105_v01/panel_R1_D4_L3plus.png)

[R4 D1 L3+ 패널](b1_nurec_visibility_matte_pilot_20261105_v01/panel_R4_D1_L3plus.png)

## 2. 무엇을 했나

- **job 선정(렌더 전에 고정):** red v03 manifest(SHA `56c8acbb…e0`) train 행만 사용했다. R1/R5/R4 × 거리 D1/D4 × load 1개/3개 이상의 각 층에서 scene_seed가 가장 작은 행을 골라 12개다. 여기에 이미 가림이 확인된 R3에 TRN_000027 장면을 둔 양성 대조군 1개를 더했다. 조명은 manifest에 이미 변환된 값이 들어 있으므로 scale 1, bias 0이다. ISO25 / shutter50 / f5 / ACES. `R/jobs_v01.json` SHA `8ee05720…98ce`.
- **job마다 같은 카메라로 5장:** E 빈 배경 · EO 빈 배경+NuRec 숨김 · I 배치 · O 배치+NuRec 숨김 · M 배치+matte 바닥(z=0). 실제 표현 instance mask를 load별로 저장했다.
- **표현:** HR_Scan 1개 세션.
- **분석 정의:** `analysis/b1_nurec_visibility_pilot_analysis_20261103_v01.py` 맨 위 주석에 있다.
  - 완전가림 판정(hard): \|I−E\| > τ (τ = 물체에서 15px 이상 떨어진 배경 차분의 99.9 percentile).
  - soft 가시도: v = clip(<I−E, O−E>/\|O−E\|², 0, 1), \|O−E\| ≥ 12인 픽셀에서만 계산한다.
- **NuRec 숨김 확인:** 13/13에서 E와 EO의 차이가 커서 숨김이 실제로 작동했다.

## 3. 실패 기록(보존)

1. **capture v01 FAIL:** `NUREC_PRIM_NOT_FOUND`. `/World/gauss`를 가정했지만 실제 합성 경로는 `/World/gauss/gauss`였다(default.usda의 참조 + gauss.usda의 defaultPrim). 출력 `R/capture_HR_v01/failure.json`을 보존했다.
   - **중요:** 예외가 났는데도 Python 프로세스 종료 코드가 **0**이었다. Isaac `SimulationApp.close()`가 종료 코드를 덮어쓰는 것으로 보인다. `ntfy_run.sh --verify`의 `result.json` 확인이 VERIFY_FAILED로 잡아냈다. 앞으로 Isaac 실행의 성공 여부는 종료 코드가 아니라 결과 파일로 판정해야 한다.
2. **capture v02 PASS:** NuRec prim을 `omni:nurec:isNuRecVolume` 속성으로 찾도록 고쳤다(diff는 4줄). 13/13 PASS, renderer `[Error]` 0줄, 587 s(job당 중앙값 46.7 s).
3. **matte 바닥 FAIL:** 위 1절과 같다.

## 4. 해석의 한계

- soft 가시도는 "반투명 NuRec가 앞에 있다"는 합성 모델의 근사다. 정확한 값은 완전히 보이거나(α=0) 완전히 가려진 경우(α=1)에만 보장된다. 소수점 값 자체를 측정값으로 쓰지 않는다.
- 아주 작은 mask(예: load4 241px, 224px)는 경계 픽셀이 대부분이라 soft 값이 낮게 나왔다(0.70, 0.74). 완전가림 판정 보임 비율은 1.0이었다. 판정 규칙에는 최소 픽셀 수 또는 경계 침식(erosion)을 넣어야 한다.
- R3에서는 반투명 벽 때문에 \|I−O\|가 컸다(중앙값 50). 이는 조명 차이가 아니라 가림 효과이며, 조명 점검은 가리지 않은 장면 기준이다.
- HR 1표현만 확인했다. LR/CAD는 실루엣이 조금 달라 별도 확인이 필요하다.
- 이번 결과로 NuRec 바닥 높이나 접촉을 알 수는 없다. depth는 여전히 무효다.

## 5. 다음 단계 제안

1. **가시도 QA를 production에 넣기:** 장면마다 E 1장(표현 공통) + 표현별 O 1장을 추가한다.
   - 이번 측정 기준(job당 약 47 s, 5장)을 단순 비례하면 1400×3 데이터 + E/O 추가 시간이 기존 계획보다 크게 늘어난다. 정확한 시간은 production pilot에서 다시 측정해야 한다.
   - NuRec 숨김 전환 비용이 클 수 있다. 같은 NuRec 상태끼리 렌더를 묶는 순서를 시험할 가치가 있다.
2. **판정 규칙 문서화(생성 전 잠금):**
   - 지표: load별 완전가림 판정 보임 비율(주), soft 가시도(보조).
   - FLAG 기준: 예) primary load 보임 비율 < 0.9. train 결과로만 정한다.
   - 최소 픽셀 수와 경계 침식 방식.
   - 처리: 삭제 없이 FLAG만 기록하고, 세 표현을 같이 처리한다.
3. **접촉 그림자 대안(미실행, 별도 amendment 필요):** differential rendering. NuRec를 숨긴 상태에서 보통 회색 바닥 plane을 놓고 물체 있음/없음 2장을 렌더해 그림자 비율 S를 만든 뒤, 바닥 픽셀에서 I에 곱한다. 이는 RGB 생성 방식의 변경이므로 기존 GT 정의와 분리해 버전을 따로 기록한다. 또는 접촉 realism을 연구 범위 밖의 알려진 제한으로 남겨 두는 선택지도 있다.
4. **바닥 높이:** `.nurec` Gaussian 점군에서 ROI별 바닥 평면을 추정하는 오프라인 분석(미실행).

## 6. 파일

- 코드: `scripts/prepare_b1_nurec_visibility_pilot_jobs_20261103_v01.py`(`3c17f21f…`), `scripts/b1_red_nurec_visibility_pilot_capture_20261103_v01.py`(`c0b48648…`, 실패 보존), `…_v02.py`(`8c5676c9…`), `analysis/b1_nurec_visibility_pilot_analysis_20261103_v01.py`(`0ed58e3f…`)
- 출력: `R/capture_HR_v01`(FAIL), `R/capture_HR_v02`(이미지·mask·ledger·events), `R/analysis_HR_v02_a01`(CSV·패널), stdout 로그 2개
- 보고서 첨부: `b1_nurec_visibility_matte_pilot_20261105_v01/` 아래 CSV 2개와 패널 3장
- 실행 명령: `ntfy_run.sh --name b1_nurec_vis_pilot_HR_v02 --verify "grep PASS_CAPTURE result.json" -- hh_isaac51/bin/python -u scripts/…_v02.py --config B1_RED_QUALITY_20261103_v01/config.json --jobs R/jobs_v01.json --output R/capture_HR_v02 --representation HR_Scan`
- PROJECT_STATE: 변경하지 않음(연구자 지시). 반영 승인 대기.
