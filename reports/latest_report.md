# G0–G3 긴급 인수인계: 실행 보호 및 CPU 진단 (2026-11-11 v01)

## 현재 판정

확인 시각: **2026-11-11T10:14:28+09:00**. 본 주행 큐는 **107/120 종료 결과 확보, 잔여 13개**다. 잔여에는 실행 중 항목이 포함된다. 파일럿은 별도 12/12 결과가 있다. 본 주행 전체 완료는 **NOT_COMPLETE**이며 최종 효과 검정은 아직 하지 않았다.

기존 batch PID 2157667, 상위 shell PID 2157662, 알림 watchdog PID 1427871을 확인했다. 초기 확인 당시 Kit PID 2798811, runner PID 2798712가 106번 `main_S1_L1_O0_GeoCAD_G3_t1`을 수행했고 10:09:45 SUCCESS로 종료됐다. 이후 큐가 자동 진행했다. 마지막 읽은 batch 이벤트는 `RUN_START` / `main_S1_L1_O0_GeoCAD_G1_t1` / `2026-11-11T10:12:46`다. 동적 PID는 이후 항목에서 바뀐다. 원본 프로세스를 중지·재시작하지 않았고 새 Kit/ROS/GPU 추론을 실행하지 않았다.

원래 shell은 main 종료 후 `--phase o50`도 순차 실행하도록 이미 설정되어 있다. O50 12개는 본 120개 분모와 별도다. main 종료만으로 GPU가 비었다고 판단하면 안 된다. run02에서 이번 확인 시 STOP/HOLD 파일은 발견되지 않았다. run01에는 기존 STOP_BATCH가 있다. 알림 프로세스의 생존은 확인했지만 휴대폰 수신은 검증하지 않았다. watchdog 완료 감시 경로가 run01/DONE*에 고정되어 있어 run02 완료 인식은 별도 확인이 필요하다. 이를 실행 중 수정하지 않았다.

## 집계 원칙과 중간 결과

아래는 **기존 v04 큐가 선택하는 결과의 진행표**다. G0/G1은 run01 결과가 있으면 재실행하지 않고, G2/G3는 run02에서 별도 실행한다. 따라서 이것을 단일 코드 버전의 원본 120회 결과라고 부르면 안 된다. 각 군 계획 분모는 30, 총 120이다. 미실행은 실패나 성공으로 임의 환산하지 않는다.

| 군 | 종료/계획 | 성공 | 실패 분류 |
|---|---:|---:|---|
| G0 | 27/30 | 0 | FAIL_B 25, FAIL_A 2 |
| G1 | 26/30 | 21 | FAIL_E 1, FAIL_A 3, FAIL_D 1 |
| G2 | 27/30 | 0 | FAIL_B 25, FAIL_A 2 |
| G3 | 27/30 | 21 | FAIL_D 4, FAIL_A 2 |

`latest_progress.json`은 모든 원본/개선 시도와 SHA를 별도 보존한다. **최초 시도 기준 G3**는 {'SUCCESS': 15, 'FAIL_E': 6, 'FAIL_D': 4, 'FAIL_A': 2}이다. run01의 G3 메모리 실패 6개를 run02 성공으로 덮어 집계하지 않는다. run01은 38회 원본 결과(G3 성공4/실패6 포함)를 보존하고, run02는 수정 실행 묶음이다. 초기에 수집한 run02 86개와 이후 증가한 결과는 각각 inventory.json / latest_progress.json에서 구분된다. 최초 시도도 중간에 버전이 바뀐 혼합 코호트이므로, 최종 보고서는 전체 시도 이력·버전별 결과와 조건이 맞는 비교를 함께 제시해야 한다.

파일 존재만 확인하지 않았다. 초기 inventory에서 기록된 SUCCESS 전부 runner exit0 및 lifecycle_eligible=true였다. 최종 스냅샷의 실행 코드 사본 해시 비교 2608개에서 불일치 0개다. 다만 모든 프레임·전체 물리 trace와 종료 인증을 다시 검증한 최종 실험 검증은 아직 UNKNOWN이다.

## G3 메모리: 8 GiB 초과라는 설명 정정

원본 실패 6개 모두 `GC_MEMORY_BOUND`이며 실제 중단 조건은 **GC 구간 시작 대비 RSS 증가 768 MiB 초과**다. guard는 `used <= base + 768 MiB AND used <= 8 GiB`, 시간 600초를 함께 검사한다. 원본 로그에서 6개 peak RSS는 **6.827–6.995 GiB**, 증가량 **768.45–769.50 MiB**, 경과 **455.72–469.83초**다. 따라서 이 6개를 8 GiB 절대 한도 초과나 CUDA OOM이라고 쓰는 것은 근거와 맞지 않는다. 자세한 수치는 memory_failure_classification.json에 있다.

`rss()`는 `/proc/self/statm`의 resident page 수 × page size로 **Kit 자신의 CPU RSS**를 잰다. CUDA VRAM 및 별도 인식 subprocess 메모리의 합계가 아니다. 초기 nvidia-smi의 Kit VRAM 8833 MiB와 CPU 8 GiB guard를 비교하여 오류라고 판단하면 안 된다. subprocess 포함 전체 메모리 최고값은 이 guard만으로 알 수 없다.

이미 인계 전에 runner v04 / session v03가 작성되어 run02를 실행 중이었다. v02→v03 실제 diff는 설명문과 W 정지 이후 `restore(); gc.collect(); reobserve(); enter()` 구간이다. 8 GiB·768 MiB·600초 수치는 그대로다. 단, **768 MiB 기준점을 W에서 다시 잡으므로 전체 주행의 허용 증가량 의미는 달라진다.** 단순 누수 제거 또는 안전 동작 완전 동일로 해석하지 않는다.

초기 수집 자료에서 W 재설정 기록 20건 모두 collect 전후 RSS가 같았다. HR L1 예에서는 6,779,453,440 bytes로 전후 동일했고 재시작 기준은 6,820,691,968 bytes였다. 이 수정은 장시간 GC 구간의 운영상 중단을 피하지만, 메모리 보유 자체가 제거됐다는 증거는 없다. 이번에는 상속한 수정안을 검증했으며 새 세션 패치를 만들거나 실행 중 코드를 수정하지 않았다.

정적 코드에서 `records.append(r)`와 `JSONLTail.rows.extend(...)`가 매 tick의 큰 dict를 주행 전체 동안 보유하고, TIMING.rows도 누적됨을 확인했다. 이것은 보유량 증가의 구체적 후보다. 재촬영은 기존 render product/annotator를 다시 사용하고, 인식은 별도 subprocess에서 모델을 로드한 뒤 종료한다. 영상을 JPG로 기록하며 프레임 배열을 리스트로 쌓는 코드 증거는 확인되지 않았다. 모델·RenderProduct 중복 적재, CUDA 참조 누수, native simulator 자원 누수는 **미입증**이다. allocation profiler 없이 Python 보유량만이 모든 RSS 증가를 설명한다고 단정하지 않는다.

다음 수정 후보는 전체 원본 trace를 디스크에 보존하면서 정지 인증에 필요한 데이터만 메모리에 유지하는 별도 버전이다. `confirmed_stop`이 사용하는 시간 구간과 이전 leg 경계를 먼저 검증해야 하며 무조건 deque로 자르면 안 된다. 8 GiB 절대 guard를 유지하고, 구간별 guard와 전체 주행 증가량을 함께 기록해야 한다. 현재 주행에는 적용하지 않는다. 원본 6개 실패와 수정 시도의 대응 비교는 최종 표에서 분리한다.

## G0/G2 B5: 동일 입력 재계산

이번 CPU 진단은 S1–S4 × 3표현 × L4/O0의 G1 저장 입력 12개를 선언했다. GeoCAD S1 G1은 원래 `CAPTURE_BUFFERS_INVALID`로 RGB-D 자체가 없어 NOT_REPLAYABLE로 남겼다. 나머지 **11개 동일 RGB-D·mask 입력**에 ORIG_v44와 frozen ROBUST_A를 적용했다. GT·새 추론·시뮬레이션은 쓰지 않았다.

- ORIG_v44: 11/11 DATUM_REJECTED, 기존 status/reason과 일치.
- ROBUST_A: 11/11 B5_COMPUTED, 기존 중심 좌표와 최대 절대차 **0.0 m**.
- 원본 후보 면은 있었지만 5×5 erosion 후 주요 후보가 **49–84점**만 남아 100점 기준을 통과하지 못했다. 다른 띠 후보는 침식 후 0점이었다.
- 원본은 지면 위 .144±.020 m 표면, mask 7×7 제외, component>=25, erosion5×5 후 >=100, inlier80%, 3mm 잔차·5도 기울기 등의 고정 조건을 적용한다. 이 표본의 첫 실패는 erosion 이후 면 지지점 부족이다. 기준을 낮춰 원본 성공으로 바꾸지 않았다.

따라서 새 시작점에서 팔레트 윗면을 **전혀 못 본다**고 단정할 수 없다. 윗면 후보는 관측되나 얇은 영상 띠가 기존 ROI 처리 후 부족해진다. 저장 입력으로 같은 실패가 재현되어 실행기 인자 전달 오류가 필수 원인은 아니다. 좌표계 정합성의 독립 실측까지 증명한 것은 아니며 다른 조건도 이 11개만으로 모두 설명하지 않는다. 기존 로컬 orig_failure_check_b는 62개 재현을 기록하나 이번 독립 재실행 분모는 11개다.

보정 A는 `evaluation/b5_robust_20261110_v01.py`다. code SHA `0b1e5f46702d4af0c4d4abc4b7d1c5fe9d29cc07c9f34b4a1592990ac296ae29`, frozen config SHA `35cf0a78d4c73919ab2a03378341fb90433aeaeeab306a605d064d98a0cfc529`를 실제 검증했다. 센서 floor/load-top 기반 datum, 깊이 연속 영역 확장, 팔레트 수직면 및 실루엣 midpoint, 모호한 장단축 중심의 평균을 사용한다. layer_count는 작업 메타데이터다. 고정 task center나 GT pose를 입력하지 않는다. 단순 B5 임계값 완화가 아니라 별도 추정기다.

B는 초기 PRE에서 0.80m 뒤의 W에서 인증 정지 후 재촬영한다. 초기 mask 3D centroid와 가장 가까운 검출을 0.30m gate로 재식별하고, pose 변화 0.25m gate를 적용한다. 재추정은 초기값을 대체한다. 초기 가림판은 모든 군에서 주행 전에 제거되므로 재인식은 가림 없는 관측이다. 이 효과를 지속 가림 상황의 재인식 효과로 일반화하지 않는다.

## 시각자료

실제 저장 RGB·detector overlay·주행 중 JPG 8개 패널을 `reports/stage4_handoff_evidence_20261111_v01/actual_saved_frames_contact_sheet_LOCAL_ONLY.png`에 정리했다. 원본 경로/SHA/패널 종류는 contact_sheet_provenance.json에 있다. G0/G1 초기 비교, G3 초기/W 재관측, 실제 robotcam 중간/마지막 저장 프레임이다. 마지막 저장 프레임을 별도 증거 없이 최종 정지 인증 시각이라고 부르지 않는다.

현재 조사한 Stage4 run01/run02 및 Stage3 main 폴더에서 MP4/AVI/WebM은 발견되지 않았다. JPG가 있다는 사실을 MP4 녹화 완료로 쓰지 않는다. top-down·외부 로봇 시점·계획 경로/B5 투영·CAD 실패 전용 패널과 대표 영상은 미완료다. 재현 영상은 기존 전체 큐(main 뒤 O50 포함) 종료 및 GPU 비점유 검증 후에만 별도 촬영하며 성공률 분모에 추가하지 않는다. NuRec 배경에 사람 형상이 있어 이미지/contact sheet 및 process dump는 공개 동기화 대상이 아니다. 이번 공개 인수인계 대상은 이 텍스트 보고서 하나다.

## 검증·실패·남은 작업

PASS: matrix SHA, main120 unique·각 scene/rep 4군 pairing, 초기 모든 코드 사본 및 최종 추가 사본 hash, design SHA, 모델 설정 4개의 실제 checkpoint SHA, known-lock9 hash/count(108/432), frozen core AST 일치, 보정 A 7건 및 B 로직13건 CPU 회귀검사, 동일 입력11개 재현. 과거432 설계는 Stage4 120행과 별도이며 추가 실행하지 않았다.

FAIL(보존): 첫 replay의 잘못된 저장 파일명, 둘째 replay의 원본 촬영 실패 입력 부재, pytest 부재 exit1. 저장 파일명은 수정했고 촬영 실패는 제외 성공 처리 없이 NOT_REPLAYABLE로 남겼다. 설치 없이 기존 minimal runner/unittest로 회귀검사했다. git status exit128(.git 없음), glob 검색 exit2도 audit_attempt_failures.txt에 기록했다. 연구 실패 분모에 audit 명령 실패를 넣지 않는다.

UNKNOWN/NOT_DONE: 120회 전체 종료·최종 trace 검증, 버전별 paired 통계, 전체 메모리 allocation 원인 분해, native/CUDA 자원 누수 유무, 영상 패키지, 원격 동기화 완료. 실제 외부 검증은 red-only이며 실제 로봇 배치 검증이 아니다. 10 scene×3rep×4군이고 반복/표현을 독립 장면으로 부풀리지 않는다. 비유의를 동등성으로 해석하지 않는다.

로컬 폴더는 Git 저장소가 아니다. GitHub API read로 yeone00/isaacsim-codex-handoff의 main branch 존재를 확인했지만 게시·push·remote 변경은 하지 않았다. 과거 handoff/next_task.md는 실행하지 않았다. 이 보고서의 HANDOFF_REPORT marker로 텍스트 동기화를 요청하며 원격 반영은 UNKNOWN이다.

다음 순서: (1) 기존 batch 그대로 유지, main과 이어지는 o50의 상태·terminal artifact 확인, (2) latest_progress의 시도별 이력을 기준으로 원본/수정 결과를 따로 검증, (3) G3 6개 대응 재실행 비교 및 나머지 memory profile 해석, (4) 버전·scene pairing을 유지한 최종 A/B 효과 분석, (5) GPU가 빈 후에만 부족한 대표 캡처/영상 확보. 자동 재시도는 추가하지 않는다.

중단 시에는 PID/ROS191/GPU/STOP·HOLD와 각 cell 결과를 먼저 대조한다. 기존 `stage4_ablation_batch_20261110_v04.py --phase main`은 디렉터리 존재만으로 SKIP_EXISTS하므로 **불완전 디렉터리를 복구하는 안전한 resume 명령이 아니다**. 현재는 재개가 필요 없으며 실행하지 않았다. 새 실행이 필요하면 불완전 cell을 별도 새 출력 경로의 재실행 묶음으로 기록하고 기존 실패를 보존해야 한다.

## 변경 파일과 재현 명령

새 코드: `analysis/stage4_handoff_audit_20261111_v01.py`, `analysis/stage4_saved_pose_audit_20261111_v01.py`. 보고서 및 evidence JSON/CSV/로컬 전용 PNG, `reports/known_locks_handoff_20261111_v01.json` 생성. `docs/PROJECT_STATE.md`는 이번 인수인계 기록을 추가한다. 원본 실행기·설정·lock·기존 결과는 불변이다.

실행한 주요 명령:

```text
python3 analysis/stage4_handoff_audit_20261111_v01.py
/home/user/anaconda3/envs/sdg_tools/bin/python analysis/stage4_saved_pose_audit_20261111_v01.py
python3 scripts/verify_known_locks.py --out reports/known_locks_handoff_20261111_v01.json
CUDA_VISIBLE_DEVICES='' OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/user/anaconda3/envs/sdg_tools/bin/python tests/test_b5_robust_20261110_v01.py
CUDA_VISIBLE_DEVICES='' OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/user/anaconda3/envs/sdg_tools/bin/python -I tests/test_stage4_ablation_b_logic_20261110_v01.py
```

증거 폴더는 이번 감사 전용이다. inventory.json은 초기105개 스냅샷, progress_update.json은106개, latest_progress.json은 위 시각의 107개를 보존한다. audit 스크립트는 출력 디렉터리가 이미 있으면 실패하므로 반복 실행 시 새 버전 출력 경로를 먼저 지정·구현해야 한다. 실행 재시작 도구가 아니다.
