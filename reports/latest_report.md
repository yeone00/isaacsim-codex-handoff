# 건설현장 조명 복구 및 단일 정적 렌더 — 2026-10-22

**HEADLESS_VISUAL_PASS / load PASS / capture PASS / host EXITED 0 / GUI_VISUAL_UNKNOWN.** 실제 저장 PNG를 직접 열어 청록색 로버 본체·바퀴·흰 rolltainer 프레임, 벽돌 적층·팔레트, 현장 바닥·기둥·창을 식별했다. 어두운 원거리 배경은 남지만 대상 식별을 막지 않는다. 추가 렌더/재시도0. 이전 어두운 이미지 FAIL, 비동기 capture AssertionError, 사용자 GUI core dump는 기존 기록 그대로 보존한다.

## 바로 열 파일과 렌더 증거

- **GUI에서 열 USD 하나:** `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/construction_site_e2e_lit.usda`
- 원본 렌더 PNG(1000×625): `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/static_preview.png`
- 밝기 가공 없는 좌우 비교: `/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/before_after.png`
- USD SHA256: `4e0ad262a0ce2a733e86e82e2ba69aa0eee42bb87c33086925117956bbddade8`
- PNG SHA256: `96177043e2978af808900144977e77f7014d38bcdd7c635ca185d41c5cbf8bdc`

Isaac Sim 5.1 GUI에서 위 USD 하나를 File → Open으로 연다. Play, Script Editor, 카메라 조작이나 추가 스크린샷 진단은 필요하지 않다. GUI 자체는 이번에 관측하지 않았으므로 GUI 가시성/재오픈 lifecycle 무크래시는 UNKNOWN이다. 참조 자산은 기존 절대경로에서 읽으므로 이 USD는 asset 전체를 내장한 배포 패키지가 아니다.

## 어두움의 확인 근거와 변경

기존 PNG를 직접 열고 RGB 픽셀을 분석했다. 완전 검정 픽셀15.19712%, 벽돌/팔레트 고정 사각영역의 검정51.0591%였다. 파일 부재나 빈 capture가 아니라 창밖만 밝고 실내 본체·적재물이 묻히는 실제 영상이었다.

실제 합성 USD의 활성 조명은 무텍스처 Dome 하나(intensity350, color .65/.72/.85, exposure0)였다. 이전 preview layer는 `/World/SDGLighting_v02/WorkLight_Left`, `WorkLight_Right`를 각각 active=false로 작성했다. 원본 recovery USD에는 흰 Dome2500과 Rect 작업등6000 두 개가 있다. 과거 성공 HR2.0m demo의 `scene_ready.json`/`photometric_readback.json`도 읽었다: Dome8000, ISO400, shutter50, f/5, ACES6. 이 데모는 다른 관측 조건이므로 현장 프리뷰의 정답 노출로 취급하지 않았다.

주된 원인 후보는 **실내 직접 작업광 부재와 Dome 감광**이다. 새 layer는 Dome을 원본의 흰2500으로 복원하고 `/World/ConstructionPreviewWorkLight` RectLight 하나(intensity6000, 3×2m)를 기존 preview camera 위치/방향에서 대상 쪽으로 비추게 추가했다. Light의 transform만 기존 camera world transform에서 복사했다. 카메라·물체의 pose/optics, 재질·texture·binding은 바꾸지 않았다. 대체 재질 없음. 기존 두 작업등은 복구하지 않아 과거 위치의 불필요한 조명을 활성화하지 않았다.

노출/tone/color 설정은 변경하지 않았다. 새 실제 Kit readback은 ACES op6, ISO100, exposureTime≈.02s(cameraShutter50), f/5, cm2Factor1, sRGB gamma=true, whitepoint1/1/1, OCIO=false, colorcorr=false, histogram=false, autoExposureMode1/fixed, aa exposure1, ambientLightIntensity0, indirectDiffuse=true, skipMostLights=false다. 실제 viewport 제품의 `invertColorCorrection=true`, `invertToneMap=true`도 그대로이며 밝아진 PNG가 생성됐다. 따라서 이 두 flag를 어두움의 확정 원인으로 주장하지 않는다. 세부 값은 `runtime_settings.json`에 있다. Dome/작업등 개별 기여와 warmup 차이(기존12→이번120 update)는 분리 실험하지 않았으므로 단일 원인·정량 기여는 UNKNOWN이다.

## 실제 이미지 판정과 수치

밝기는 **저장된 display RGB/255의 .2126R+.7152G+.0722B**이며 scene-linear 광도 측정이 아니다. ROI는 segmentation이 아닌 동일 고정 픽셀 영역이다. 이미지를 보정해서 PASS로 만들지 않았다.

|지표|이전 dark PNG|새 실제 PNG|
|---|---:|---:|
|전체 p10|0.000000|0.082337|
|전체 p50|0.007843|0.365555|
|전체 p90|0.031105|0.713993|
|RGB 비영 픽셀|84.80288%|99.98992%|
|RGB 완전 검정|15.19712%|0.01008%|
|어느 채널이든255 클리핑|0%|0%|
|로버 본체 영역 p50|0.008126|0.607843|
|벽돌/팔레트 영역 p50|0|0.212531|
|현장 영역 p50|0.015969|0.298322|

**시각 판정 PASS**는 실제 이미지에서 본체·바퀴와 적층 경계·팔레트 및 현장 구조가 인지되는 것을 근거로 했다. 300개 전체의 개별 식별, 재질 충실도/MDL dependency closure, 실제 로봇 배포나 연구 perception 성능을 인증하지 않는다.

## 단일 runtime과 capture 완료

명령은 `python3 scripts/run_construction_site_lit_once_20261022_v01.py`였다. `/proc` comm/cmdline gate에서 기존 Isaac/Kit/SimulationApp 프로세스0을 확인했다(`kit_launch_ledger.json`). exclusive-create ledger가 같은 output 재실행을 거부한다.

실제 `/home/user/anaconda3/envs/hh_isaac51/bin/python` + Isaac Sim5.1 `isaacsim.exp.base.python.kit`/SimulationApp, headless RayTracedLighting. 환경은 EULA YES, PYTHONPATH 제거. 패키지 설치/업데이트 없음. timeline stopped, 활성 ROS extension0, 활성 OmniGraph0, physics.play0, motion0이다. USD edit target은 session layer이며 runtime save는 없다.

캡처를 한 번만 요청했다. future 완료 후에도 update를 계속하면서 파일의 비영 크기 안정화3회, PNG signature·각 chunk CRC·IEND·zlib 압축 해제를 확인했다. 11 update/0.167s 후 1138884바이트 PNG가 검증됐다. **내부 `kit_internal_result.json`은 load/capture PASS**, **외부 `kit_host_exit.json`은 EXITED/returncode0**, wrapper exit0이다. `kit_shutdown.json`은 없으므로 `app.close()`의 Python return은 UNKNOWN이며 내부 capture PASS/host exit0와 구분한다. Native expired-prim/core dump signature는 이번 log에 없다.

원본 rolltainer의 reference scope 밖 material binding 경고와 fabric의 rear_right_steer_link/visuals/mesh_0 경고는 log에 남아 있다. 이 경고를 제거하거나 임의 asset 변경하지 않았다. GUI callback 전체와 모든 dependency의 무결함을 주장하지 않는다.

## 보존·검사·변경 파일

- 입력 runtime USD SHA256 `97da3867a2297f2f90d10ce120280c06e4b1cc71833e51d7862e8399794c3ab6`, 이전 PNG SHA256 `4f2aabda24be8ff8be2d10199a5068234c161721b6c920b1867eec349dc9a083` 일치.
- 기존 manifest source hash와 used-layer23 SHA를 실행 전/후 검증 PASS. 모든 절대경로/hash는 `manifest.json.source_hashes`, 이전 demo 증거 hash는 `prior_photometric_evidence.json`, code/output hash는 `final_evidence.json`에 있다.
- 로버/현장/fixture 전체 prim 속성·relationship의 전후 signature 일치 PASS. 메시 points·xform·재질 binding·subset·membership 포함이며 frustum/bbox/camera matrix audit를 반복하지 않았다. 실제 nonempty brick meshes300, rover1, PhysicsScene1, graph0, camera2, RenderProduct1, `/Render` active, calibration 활성 빈 컨테이너2 유지. 새 layer의 authored 변경은 Dome 속성2개+RectLight뿐이다.
- Offline10 checks PASS, 신규 Python4개 AST PASS 및 shell syntax PASS, PNG 부분파일/CRC 등5 checks PASS, 알려진9 locks hash/count 재검증 PASS(known subset 한정), post-runtime7 checks PASS. source/원본/이전 output 변경 없음.
- 신규 `scripts/build_construction_site_lit_20261022_v01.py`, 대응 `.sh`, `scripts/check_construction_site_lit_kit_20261022_v01.py`, `scripts/run_construction_site_lit_once_20261022_v01.py`, `analysis/construction_site_lit_image_metrics_20261022_v01.py`, 이 보고서; `docs/PROJECT_STATE.md` append. Bulk USD/PNG/log/JSON은 외부 output에만 저장. Git staging/push/remote 변경 없음.

실용적인 headless 밝기 blocker는 이번 이미지에서 해소했다. GUI_VISUAL은 UNKNOWN으로 남긴다. 다음 작업은 필요시 **위 최종 USD 하나 열기**이며 추가 수동 진단을 요구하지 않는다. 이 조명은 preview 전용으로 연구 lighting lock을 대체하지 않는다. controller/ROS publisher/HOLD graph/training/ENG001/QUAL12/432 실행0, 연구 분모 기여0. 기존 실패·protocol·threshold·checkpoint는 보존했다.
