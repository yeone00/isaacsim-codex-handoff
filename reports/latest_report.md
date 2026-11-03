# Claude Code GitHub handoff 및 ntfy 알림 설정

작성일: 2026-11-03 KST · 작성: Claude Code (Opus 5.5)

연구 파일, PROJECT_STATE, Git 이력은 바꾸지 않았다. 실험 실행 0, push 0, force push 0. Codex 프로세스는 건드리지 않았다.

## 1. GitHub 연결 상태(확인 결과)

| 항목 | 결과 |
|---|---|
| 로컬 handoff | `~/hh/isaacsim-codex-handoff` (Git 저장소) |
| remote | `origin https://github.com/yeone00/isaacsim-codex-handoff.git` (fetch/push), **PRIVATE**, 기본 브랜치 `main` |
| 동기화 | `git fetch` 후 main…origin/main = **0 ahead / 0 behind** |
| 최신 commit | `2a09cf6 Sync Codex report: b1_red_brick_sdg_quality_optimization_20261103.md` |
| 추적 안 되는 파일 | `codex_notify_sync.py`, `sync_report.sh`, `__pycache__/` (기존 상태 그대로, 손대지 않음) |
| `status/PROJECT_STATE.md` | 연구 저장소 PROJECT_STATE와 SHA 동일 |
| gh 인증 | `yeone00`, keyring, scope `repo, workflow, gist, read:org` (토큰 미출력) |
| GitHub secret | `NTFY_TOPIC` 존재(2026-10-19 등록). 값은 GitHub 밖에서 읽을 수 없다 |
| `handoff/next_task.md` | v48 로봇 오프라인 분석 지시(Mid/Front 100 vs 219). 현재 연구자가 지시한 B1 SDG 작업과는 별도 과제다 |
| `reports/latest_report.md` | B1 적벽돌 품질 개선 보고서(11-03 15:18 동기화) |

기존 Codex 흐름: `~/.codex/config.toml`의 `notify` → `codex_notify_sync.py`(마지막 응답에서 `HANDOFF_REPORT:` 줄을 찾음) → `sync_report.sh`(pull --ff-only, 보고서를 `reports/latest_report.md`로, PROJECT_STATE를 `status/`로 복사, commit, **push**) → GitHub Actions `notify_report.yml`이 `secrets.NTFY_TOPIC`으로 ntfy 발송. 저장소를 새로 만들 필요는 없다.

## 2. Claude Code에서 handoff를 읽고 쓰는 방법

- **읽기:** 작업을 시작할 때 `~/hh/isaacsim-codex-handoff/handoff/next_task.md`를 읽는다(필요하면 `git -C ~/hh/isaacsim-codex-handoff pull --ff-only` 먼저).
- **쓰기:** 보고서는 연구 저장소 `reports/<파일>.md`에 쓰고, 최종 응답 마지막 줄에 `HANDOFF_REPORT: reports/<파일>.md`를 넣는다(AGENTS.md 규칙과 같음).
- **동기화 훅:** `~/.claude/hooks/isaacsim/claude_handoff_sync.py`(Stop 훅). Codex 버전과 같은 검사(reports/ 안, 1 MB 이하, 3시간 이내 수정)를 한다. **기본은 DRY_RUN**이라 `handoff_sync.log`에 "would sync"만 남긴다.
- **push 활성화(별도 승인 필요):** `touch ~/.config/claude-ntfy/HANDOFF_PUSH_APPROVED`. 이후에는 기존 `sync_report.sh`를 그대로 호출해 latest_report와 PROJECT_STATE만 commit/push한다. 대용량 USD·데이터·가중치는 이 스크립트의 대상이 아니다. 끄려면 파일을 지운다.

## 3. ntfy 설정 경로

| 파일 | 역할 |
|---|---|
| `~/.config/claude-ntfy/ntfy.env` | `NTFY_SERVER`, `NTFY_TOPIC` (**chmod 600 필수**, 권한이 넓으면 발송 거부). **아직 생성 전** |
| `~/.claude/hooks/isaacsim/ntfy_notify.py` | 훅 → ntfy. 프로젝트 라벨, 상태, 짧은 작업명만 보냄. 응답 본문·경로·토큰은 보내지 않음 |
| `~/.claude/hooks/isaacsim/ntfy_run.sh` | 장시간 명령 래퍼(종료 코드 + 결과 검증) |
| `~/.claude/hooks/isaacsim/*.log` | 로컬 로그. 이벤트 입력은 **키 이름만** 기록 |
| `~/.claude/settings.json` | 기존 `theme` 유지, `hooks` 추가 |

## 4. 훅별 동작 조건

| 이벤트 | 언제 | 알림 내용 |
|---|---|---|
| `Stop` | Claude의 응답 한 번이 끝났을 때(`stop_hook_active`면 생략) | "Claude response finished" + "백그라운드 작업이 남아 있을 수 있음, 연구 PASS 아님" |
| `Notification` | 권한 승인·입력 대기 등 Claude Code 알림 | "Input or approval needed (notification_type)" — 우선순위 high |
| `StopFailure` | API 오류·사용량 제한으로 턴이 중단됐을 때 | "Claude stopped with an error (오류 종류)" — high |
| `ntfy_run.sh` | 래퍼로 감싼 명령이 실제로 끝났을 때 | exit≠0 → FAILED, exit 0 + verify 실패 → VERIFY_FAILED, 둘 다 통과 → SUCCESS, verify 없음 → EXITED_0 |

Stop은 "Claude가 말을 마쳤다"는 뜻일 뿐이다. 렌더링·학습의 성공 판정은 `ntfy_run.sh`의 종료 코드와 `--verify` 검사로만 한다. 예:

```bash
~/.claude/hooks/isaacsim/ntfy_run.sh --name b1_pilot_HR \
  --verify "test -f <출력경로>/result.json && ! test -f <출력경로>/failure.json" \
  -- /home/user/anaconda3/envs/hh_isaac51/bin/python -u scripts/<스크립트>.py ...
```

## 5. 테스트 결과

| 테스트 | 결과 |
|---|---|
| settings.json JSON/스키마 검사 (`jq -e`, 3 이벤트 4 명령) | PASS |
| 훅 스크립트 pipe 테스트(Stop/Notification/StopFailure 가짜 입력) | PASS — 모두 exit 0, 로그에 키 이름만 기록, 설정 파일이 없어 발송은 SKIP |
| 래퍼 종료 코드 보존 (`true` → 0, `exit 3` → 3) | PASS |
| handoff 동기화 dry-run | PASS — "would sync claude_code_handoff_audit_20261103.md", push 없음 |
| 1. 수동 ntfy 발송 (15:46:24) | 발송 HTTP 200 · **휴대폰 수신 사용자 확인 → PASS** |
| 2. 일반 작업 종료 알림 (실제 Stop 훅, 15:48:18) | 턴 종료 시 자동 발송 HTTP 200 · **수신 확인 → PASS** |
| 3. 입력 대기 알림 (실제 Notification 훅, 질문 창으로 발생, 15:46:55) | 발송 HTTP 200 · **수신 확인 → PASS** |
| 4a. 실패 알림 — StopFailure 모의 입력 (15:46:35) | 발송 HTTP 200 · **수신 확인 → PASS**. 실제 API 오류나 사용량 제한으로 일어난 StopFailure는 아직 관찰하지 못함 |
| 4b. 실패 알림 — 래퍼 `exit 3` (15:46:36) | FAILED 발송 HTTP 200, 래퍼 종료 코드 3 그대로 반환 · **수신 확인 → PASS** |
| 5. 장시간 명령 — `sleep 60` + 결과 파일 확인 (15:47:36) | exit 0 + verify PASS → SUCCESS 발송 HTTP 200 · **수신 확인 → PASS** |

**종합: ntfy 알림 테스트 1–5 PASS (2026-11-03, 휴대폰 수신은 연구자가 확인).** 아직 확인하지 못한 것: 실제 API 오류나 사용량 제한으로 일어나는 StopFailure, GitHub push 자동화(승인 전이라 비활성).

topic 설정 이력: 2026-11-03 15:41에 Claude Code의 `!` 입력창으로 숨김 입력을 시도했으나, 진짜 터미널이 아니어서 입력을 받지 못하고 실패했다(폴더만 생성됨). 이후 일반 터미널에서 `~/.claude/hooks/isaacsim/set_ntfy_topic.sh`로 저장했다(권한 600, 38자, 값은 확인하지 않음). 설정 폴더 권한은 700으로 바꿨다.

## 6. 사용자 확인이 필요한 항목

1. ~~topic 설정~~ → 완료(일반 터미널에서 `set_ntfy_topic.sh`. `!` 입력창 방식은 실패함).
2. ~~테스트 1–5와 휴대폰 수신 확인~~ → 완료, PASS.
3. ~~GitHub push 자동화 활성화~~ → 연구자 승인(2026-11-03 15:49 KST). `~/.config/claude-ntfy/HANDOFF_PUSH_APPROVED` 생성(600). 사전 점검: origin과 0/0, 추적 파일 변경 0, `git push --dry-run` Everything up-to-date. 이후 응답 마지막 줄에 `HANDOFF_REPORT:`가 있으면 기존 `sync_report.sh`가 실행된다. **첫 실제 push PASS(15:50:14):** commit `5964542`가 origin/main에 올라갔고 로컬과 0/0, `latest_report.md` 제목이 이 보고서로 바뀌었다. GitHub Actions "Notify Codex report upload"는 success였고, 휴대폰 수신은 연구자가 확인했다. commit과 알림 문구의 "Codex"는 기존 스크립트를 그대로 쓴 결과다. 이 스크립트는 `reports/latest_report.md`와 `status/PROJECT_STATE.md`만 commit/push하고, force push는 하지 않는다(pull --ff-only). push가 일어나면 GitHub Actions가 기존 ntfy 알림 "Codex report uploaded"를 보낸다. 끄려면 플래그 파일을 지운다.
4. Codex `notify`와 Claude `Stop` 훅이 같은 `sync_report.sh`를 쓴다. 두 도구를 같은 시각에 쓰면 push가 겹칠 수 있다(`pull --ff-only`라 이력을 덮어쓰지는 않고 실패로 끝남).
5. `handoff/next_task.md`가 아직 v48 로봇 과제다. B1 SDG 작업을 다음 과제로 둘지 결정이 필요하다.
