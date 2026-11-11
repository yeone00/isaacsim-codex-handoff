# C 복구 준비·독립 감시·GitHub/ntfy 통합 인수인계 — 2026-11-11

최종 지시 적용: **PREPARATION_ONLY**. 기존 L-HPO는 절대 수정·중단하지 않고, 새 렌더·학습·Isaac Sim 주행은 별도 승인 전 실행하지 않는다. 48시간은강제시한이아니며기록/정확성/연속감시를우선한다. 기존결과와새C결과를재라벨링·합산하지않는다.

새 root: `/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01`.

## 실제 완료와 준비 중인 부분

실제 기존 연구: B1 L1–L4의48모델,Stage1/2 및Stage3/4는각원래분모/버전의결과다. 현재L-HPO는별도tmux에서RUNNING. 이전원래C알고리즘의200경로/9600제거/840state/1680manifest/3표현metadata5040검증은완료돼있다. 새controller는그고정입력의SHA와증거를다시검사하는CPU작업→준비문서/허가gate검사로자동전환한다.

아직미구현/미검증: B1환경용C RGB-D/GT mask adapter,물리support/overlap/floating QA,새split family/partial shape중복정책,새C dataset lock,새C학습·평가adapter,ROBUST_A C호환수정판/센서검증,기술pilot,100조건/300실행manifest 및단일성공기준. 이들을완료한것처럼실행기가판정하지않는다. 자동화는현재CPU준비/감시/통합범위이며전연구GPUpipeline완성으로주장하지않는다.

## 방법론·계획 산출물

- `docs/c_depletion_chapter3_methodology_DRAFT_20261111_v01.md`: 논문제3장에쓸수있는설계/기존수행/미수행범위와통계한계.
- `docs/c_depletion_dataset_and_model_plan_DRAFT_20261111_v01.md`: grouped split/QA/재사용/P0–P3/모델선정.
- `reports/c_depletion_ROBUST_A_structural_audit_20261111_v01.md`: .144m기준과적재물top·층수입력·좌표변환·수식반례.
- `docs/c_depletion_300drive_protocol_DRAFT_20261111_v01.md`: 10base×5C×2O×3표현300, G1single-only,진입조건과성공기준HOLD.

11cm/7.34177432289679°의현행MAIN출처는full_e2e_targets 및stage3_outcome에서확인했다.10cm/5°를현행잠금의tasksuccess로입증하는자료는찾지못했다.10cm충돌clearance와혼동하지않는다. 양자를새C본실험기준으로사전확정하기전주행금지,비열등성10%p도미확정이다.

ROBUST_A는layer_count task metadata에의존하고현CLI는1/4만허용한다. nominal4prior를고정하면이상적센서에서도C60/40/20의pallet추정bias가−.09/−.18/−.27m인수식반례가있다. 실제오차로보고하지않으며새C의정답층수/slot을입력으로넣어해결하지않는다. 기존A원본은보존했다.

## 독립 동작과 관측

controller/watchdog는Python표준라이브러리만쓰고기존ntfy hook/config 및GitHub checkout을재사용한다.새Telegram/새topic/인증변경0. controller는허가범위와protocol/code SHA를검사하고CPU2단계후HOLD를유지한다. watchdog는HPO PID/heartbeat/epoch진행·GPU/디스크·loadavg·C상태를30초간격감시하고15분snapshot을남긴다. 학습진행15분정지는가능한HANG경고이지자동kill근거가아니다. 현재HPO의epoch약4초·초기화수십초에비해보수적인감시창이다. GPU프로세스종료/재시작/안전기준변경권한은없다.

ntfy queue는확인된HTTP200만DELIVERED로기록하고실패는60초부터최대1시간backoff재시도한다. 같은event key는중복전송하지않고지속오류재알림은30분단위로제한한다. 휴대폰실제수신은HTTP성공과별도이며사용자확인없이는확인완료라하지않는다.

GitHub는기존`/home/user/hh/isaacsim-codex-handoff`의인증/origin을재사용한다.기존sync_report.sh는latest보고서2개만덮어쓰는turnhook이어서독립감시와코드/프로토콜동기화에는새bounded publisher를추가했다.기존hook/remote는수정하지않는다. 새namespace `research/c_depletion_rebuild_20261111_v01/`에허용목록의텍스트만복사·credential패턴검사·특정파일stage·commit/push한다.기존trackeddirty/divergent history는동기화만PENDING_RETRY로남기고로컬연구는계속한다.heartbeat마다commit안함;중요event는최대5분,정기상태는30분간격이다.원격refs/heads/main SHA가local commit와같아야VERIFIED다.원본images/depth/checkpoint/USD/private ntfy config는게시하지않는다.

기존HPO최종완료/오류도watchdog가감지해ntfy와GitHub요약에반영하되,그종료를신규C GPU실행허가로취급하지않는다. Codex호출은모든루프/전환/전송의의존성이아니다.

## 복구·상태·남은 시간

상태는root의pipeline_status.json,watchdog_status.json,hpo기존hpo_status.json,github_sync_status.json부터읽는다. jobs.json은완료result SHA와실제COMPLETED를검사해SKIPPED_VERIFIED로재사용한다.미완료이전attempt는INTERRUPTED/HOLD로남기고자동재시도하지않는다. 전역controller lock·root lock·watchdog lock·git lock사용.현재GPUjob0이므로기존HPOGPUlock을취득하거나새GPU작업을launch하지않는다.

독립구동PID·실제서비스와ntfy/remote검증결과는아래최종확인절에기록한다. systemd user enable/linger지원과실제재부팅검증은구분한다.재부팅을시험하려고워크스테이션을재부팅하지않는다.기존tmux HPO는현재대로유지하고reboot자동resume를새로부착하지않는다.

기존G1성공25회의평균479.04s(약8분)→300회39.92h,보수적9분이면45h.빠른인식실패까지섞은전체평균으로전체성공주행시간을낮추지않는다.새RGB-D/QA8–12h·P0–P2학습2–3h·평가/pilot2–6h·현재HPO잔여를더하면향후실제작업은대략55–70h범위이며,이는새capture throughput없음/재시도/HOLD대기제외의거친추정이다.실제작업허가후단계실측으로갱신해야한다.현재HOLD종료시간은확정할수없다.48h에도분모축소/결과성공처리/자동강제종료하지않는다.

현재핵심BLOCKER는새실행별도승인없음,성공기준미확정,새Cdataset/GT/모델/pose/physics QA없음이다. 원래알고리즘근거부족은해소됐지만MNIDB_0006 C20중복과C100공통템플릿을데이터독립성정책에반영해야한다.

## 최종 실제 실행 확인 — 2026-11-11T18:36:10.022011+09:00

- systemd user controller `c-depletion-controller-20261111-v01.service`, PID3509437; watchdog `c-depletion-watchdog-20261111-v01.service`, PID3514993 (runtime v03). 두 서비스 active,CPUQuota각10%of1core,MemoryMax각256MiB,Nice15. 사용자service manager가부모이며Codex subprocess가아니다.
- CPU Stage0 고정입력검증→문서/허가gate검증2개가별도worker PID로자동전환해COMPLETED. result SHA재검증PASS. 현재HOLD는연구/실행허가gate에따른정상대기다. 새GPU작업0.
- 기존HPO PID3130638 및 tmux `b1_common_hpo_20261111_v01` 유지, 조회시 `full_C05_GeoCAD_s42` epoch120, RUNNING. 원래HPO코드5개SHA불변. GPU경합없음.
- ntfy기존설정/스크립트재사용HTTP200,연구자가실제휴대폰「수신했음」확인. 알림설정새로할필요없음. root의watchdog_memory.json/outbox에전송·retry기록,phone_receipt_confirmation.json에수신확인보존.
- GitHub자동push 및원격SHA일치확인: `f9cae69380e01be4f7de7d572e5b4bf8e23909a4` (이최종문구동기화전실제검증commit). 이후최신은github_sync_status.json과원격으로확인. 기존remote/인증/turnhook미수정.
- 최초publisher v01은secret scanner자신의PEM규칙문자열을잘못검출해PENDING_RETRY. 원본/실패기록을보존하고v02의실제PEM행anchoring으로수정,실제PEM거절회귀PASS. v03은HPO가계속진행하는개별FAILED/INTERRUPTED worker도30초관측후즉시알림대상에추가. 원래protocol/code hash는갱신하지않고runtime_amendment_v02/v03과새소스SHA로추가버전을기록했다. 수정후원격VERIFIED.
- systemd두unit enable 및Linger=yes확인: logout/boot시사용자manager의준비감시서비스재기동구성. 실제logout/reboot는HPO보호를위해실행하지않았으므로boot실증PASS가아님. 기존tmux HPO는reboot자동복구대상에추가하지않았고프로세스가없어지면알림/HOLD다.

상태/재개명령:
```bash
CROOT=/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01
"$CROOT/status.sh"
"$CROOT/resume.sh"
```
resume는동일systemd서비스를start하므로살아있는controller중복생성없음. 완료CPUjob은artifact검증후SKIPPED_VERIFIED,미완료는INTERRUPTED/HOLD. 기존HPO를재시작하는명령이아니다.

검증: AST/실행범위상향거절/protocol변조거절/실제PEM거절/고정입력·결과SHA/systemd단위검사/독립PID·자동CPU전환/휴대폰수신/원격commit확인PASS. 후속C GPU실험·재부팅실험NOT_RUN. 다음은미확정성공기준·split/중복정책·센서기반datum계약을확정하고새Cadapter/QA를별도version으로준비하는작업이다.

## HPO 계획 개정분 — 2026-11-11T19:16:37.531172+09:00

신규 C QA/split/manifest 잠금 후 **C 전용 공통 HPO 필수** 단계를 추가한다. 현재 L-HPO는 그대로 완료 후 예비 탐색으로 보존한다. 기존 전이 보조 대조만의 안은 `docs/c_depletion_common_hpo_plan_AMENDMENT_20261111_v01.md`로 대체하며 다른 지시는 유지한다. 순서: C dataset/QA/split → C-HPO → 최종모델/seed반복 → 인식 → pose/ROBUST_A → 기술pilot → G1 300. 계획JSON은root/execution_plan_amendment_v01.json 및pipeline_plan_current.json. 실제C-HPO adapter/새GPU는미구현·미실행/비승인,HOLD유지. 기존runtime코드/부모protocol/QA gate SHA변경0.
