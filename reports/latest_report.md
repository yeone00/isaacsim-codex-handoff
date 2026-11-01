# v29 — 메모리·종료 원인 미확정, Kit 재실행 차단

2026-11-02 KST. **BLOCKED / Kit 신규 0회, retry0, HR PRE·FINAL NOT_RUN.** 메모리 원인 제거와 실제 Kit 종료 수정은 입증하지 못했다. 따라서 사용자 조건7에 따라 live run root를 만들지 않았다. v28 engineering **0/1 FAIL**, science denominator0 그대로다. LR/CAD·324/432·training0.

| 실제 측정 | RSS bytes | PSS bytes | 해석 |
|---|---:|---:|---|
| v21 기존 motion-GC 진입 | 6,603,423,744 | UNKNOWN | 성공 baseline, 전체 run peak 7,181,115,392 |
| v28 기존 motion-GC 진입 | 22,329,970,688 | UNKNOWN | 20.7964 GiB, 이미 8 GiB 초과 |
| v28 같은 scope 복구 | 22,329,970,688 | UNKNOWN | 0.002579초, scope 증가0 |
| v29 offline v21 stage-open | 302,993,408 | 300,339,200 | 별도 standalone USD 프로세스 |
| v29 offline pilot stage-open | 306,733,056 | 303,978,496 | 별도 standalone USD 프로세스 |

RSS는 `MotionGC.rss()`의 `/proc/self/statm` resident pages×page size다. v28 `run_status.json`의 **Kit-owner Python PID1966007 자신**이며 outer runner·ROS observer PID1967081·별도 sdg_tools YOLO/B4/ROI/B5 worker의 합이 아니다. GPU VRAM도 아니다. `enter()`가 paused `gc.collect()` 후 base를 기록하고 GC를 disable하며, `timeline.play()` 뒤 첫 `tick()` 맨 앞 check에서 거절했다. driver 생성 전이고 scope 내 leak/GC pause의 증거가 아니다. v28 startup→scene→capture→B5→PRE sweep의 RSS/PSS/VRAM 시계열은 **미기록**이므로 단계별 증가량 UNKNOWN. 두 run 간 약14.65 GiB 차이를 한 run의 phase growth로 부르지 않는다.

## 확인한 차이와 원인 판정

[독립 USD probe v21](construction_site_memory_probe_20261102_v29_v21.jsonl), [pilot](construction_site_memory_probe_20261102_v29_v28.jsonl): 같은 발견된 hh_isaac51 Python+USD 라이브러리로 read-only stage open, 작은 inventory만 수행, 각각 exit0/60초 제한. Kit·renderer·PhysX cook·capture·geometry array 전개 없음. pilot probe 입력은 v24 HR parent overlay이며 v28 실행 중 stage의 capture graph/PhysX correction까지 재현한 것이 아니다.

v21/pilot instance322/22, mesh321/321, used-layer27/29, enabled collider314/42를 관측했다. 이는 authored/composed USD inventory이며 실제 PhysX shape 수가 아니다. pilot42에는 union28 외 rover/환경 collider가 포함된다. v23 prepare는 300 AssetRef를 명시적으로 `SetInstanceable(False)`하고 새 PilotVisual reference 아래 기존 native physics를 비활성화한다. **300 HR visual의 인스턴싱 소실은 확인된 구성 차이이며 renderer geometry 복제의 유력한 조사 후보**다. 그러나 USD-open 차이는3,739,648바이트뿐이며 renderer 메모리 차이는 측정하지 않았다. 원인으로 확정하거나 instanceable을 임의 복구하지 않았다. 복구 시 native collider 재등장/physics override 무효 가능성을 먼저 검사해야 한다.

capture는 annotator3개를 attach하고 explicit detach/destroy 없이 반환한다. v21도 같은 capture 구조이며, v28 capture AST는 기존 v27과 같다. 이 사실만으로 14.65 GiB 증가나 close hang을 귀속할 수 없다. B4/B5는 별도 worker가 종료한 뒤 owner가 목표 JSON을 읽는다. owner로 PyTorch tensor를 옮기거나 worker로 메모리를 숨기는 변경0. actor signature는 physics enable/schema/relationship만 보유하며 mesh points 전체를 문자열로 저장하는 구조가 아니다. swept support JSON 48,060개는 기존 v21에도 있는 경로다. 모든 후보의 인과관계는 UNKNOWN이다.

## Kit 종료와 작은 진단 패치

v28 observer exit0/driver 없음/GC restore 완료 뒤 `persist_before_close` provisional이 존재하지만 Kit close 완료 로그가 없다. outer watchdog25초→owned child terminate→5초 뒤 kill/exit−9다. runtime 말미 `omni.hydratexture.plugin was already released` 경고는 보이지만 대기 callback/renderer/Replicator stack이 없어 특정 shutdown ordering 결함의 증거는 아니다. **실제 hang 수정 UNKNOWN**, timeout 확대·cleanup 순서 변경·임의 resource detach0.

새 `scripts/construction_site_perception_session_20261102_v29.py`는 **계측용 초안이며 실행 승인/PASS runtime가 아니다**. 기존 session에 startup/before derive/derived/attached/before·after capture/worker exit/pre-drive/finally paused/close enter·return checkpoint만 추가했다. `evaluation/construction_site_diagnostics_20261102_v29.py`는 owner PID/PPID·RSS/PSS/private/HWM·별도 GPU MiB·GC stats·작은 stage count·명시적 lifetime 상태를 기록한다. mesh array나 전체 Python object graph를 수집하지 않는다. motion tick 계측0, finally 계측은 pause/GC restore 뒤다. close는 원래 함수를 한 번 호출하고 10초 간격 Python stack을 남기도록 했으며 기존 watchdog를 늘리지 않았다. native C++ 대기는 Python stack만으로 확정할 수 없다. 현재 코드에 새 GC collection/메모리 상한 변경0. 실행 runner는 추가하지 않았다.

[검증·소스 SHA](construction_site_diagnostics_20261102_v29.json): compile PASS, 입력101 SHA/실행 snapshot90 mismatch0. [CPU5/5](construction_site_diagnostics_cpu_20261102_v29_recheck02.log)는 실제 PID ownership, 원래8GiB 거절/GC 복구, close 정상/예외에서 provisional 선기록·close1회·실패기록, 원래 session 전체 AST에서 계측 제거 시 동일함을 확인했다. pre-driver receipt는 MISSING/NOT_APPLICABLE_PRE_DRIVER로 유지했다. **mock close 검사는 실제 observer/Kit shutdown 보증이 아니다.** 초기 system-Python CPU 검사는 pxr import 실패했고 원래 실패 로그를 보존했다. 검토한 pure classifier AST만 추출해 재검사했다.

[v21 stop20/20](construction_site_stop_cpu_20261102_v29.log), [scene3/3·변조거절12/12](construction_site_scene_guards_20261102_v29.json), [known9 SHA·행수](construction_site_known_locks_20261102_v29.json) PASS. ROI/B5 알고리즘·300 visual·28/native0 admission·graph·controller·TF/GID/contact/speed/stop의 소스는 그대로다. ROI 재선택/새 perception 없음. frozen pairing 재실험은 없으며 known-subset PASS를 전체 readiness로 확대하지 않는다.

현재 host MemTotal527,619,000kB/MemAvailable514,614,188kB를 기록했다. 현재 진단 owner cgroup와 부모 memory.max/high는 max, scope memory.peak41,971,482,624바이트다. **이는 누적 cgroup 집계이지 v28 Kit peak/당시 available RAM 증거가 아니다.** hardware-policy mismatch는 아직 미확정이며, 정책개정안도 구현하지 않았다. 원래8GiB absolute/768MiB growth/600초 한도를 유지한다.

다음 실제 gate는 **인스턴싱 소실과 resource lifetime 중 RSS 증가를 재현하는 원인 및 close 대기 지점을 입증하는 것**이다. 현재 증거로는 두 source fix의 offline PASS를 만들 수 없다. 원인 미확정 상태에서 동일 live 시도를 반복하지 않는다. HR PRE/FINAL·독립 normal-stop·실제 clean exit는 계속 미완료다.
