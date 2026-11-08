# labels_v02 실제 검토 시작 안내 (2026-11-08)

## 서버 상태
- 실행 중: `scripts/label_review_server_20261108_v01.py`
  - 작업 폴더: **`/home/user/hh/isaac_cosmos/real_benchmark/cvut_real_labels_v02_20261108/review_work_v01`**(실제 작업 폴더, 시험 폴더 아님)
  - 포트 8765, 127.0.0.1 전용, SAM 켜짐
- 시작 시점 상태: 400장 모두 NOT_STARTED, `state/` 비어 있음. 시험 폴더(`review_work_SYSTEM_TEST_NOT_HUMAN_20261108_v01`)와는 별개다.
- 터미널 세션과 분리(setsid / nohup)해 띄웠다. Claude Code에 지시를 입력하는 동안에도 유지된다.
- 로그: `/home/user/hh/isaac_cosmos/real_benchmark/cvut_real_labels_v02_20261108/review_server_v01.log`
- 접속: **http://127.0.0.1:8765/**
- 종료(작업 내용은 저장된 상태로 남는다):
  `kill $(ps -C python -o pid=,args= | grep 'label_review_server_20261108_v01.py --work-dir .*review_work_v01' | awk '{print $1}')`
- 다시 실행: `reports/real_labels_v02_review_20261108_v01/REVIEW_TOOL_USAGE.md`의 명령. 저장된 지점부터 이어진다.

## 순서
1. **Tier A 80장**: 왼쪽 목록의 Tier A 탭. `TIER_A_REVIEW_ORDER.md`가 같은 순서로 AI 힌트를 정리해 두었다(우선순위 높음 18장, 보통 62장).
2. 그다음 **Tier B 320장**: 목록이 비슷한 장면 순서이므로 → 키로 넘기며 놓친 적재물만 확인한다.

## 결정 고르기
| 대상 | 선택 | 언제 |
|---|---|---|
| 원본(초록) | KEEP | 대상 팔레트 하나를 정확히 덮음 → R2 = OK |
| | EDIT | 경계가 틀려 꼭짓점을 고침 → R2 = BOUNDARY_ERROR |
| | REPLACED(`분리`) | 옆 팔레트와 합쳐져 나눔 → R2 = MERGED_WITH_NEIGHBOUR |
| | REJECT | 적재물이 아님 → R2 = NOT_A_LOAD |
| 초안(자홍 D#) | ACCEPT | 팔레트 1개분 적재물을 그대로 잘 덮음 |
| | EDIT | 대체로 맞지만 경계를 고쳐야 함(꼭짓점을 드래그하면 자동으로 EDIT) |
| | SPLIT | 초안 하나가 팔레트 여러 개를 덮음 → `분리` 후 부분마다 추가 |
| | REJECT | 적재물이 아님, 410px 미만, 또는 다른 인스턴스와 중복 |

- **누락 적재물 추가**
  - `polygon 그리기`(D): 클릭으로 점을 찍고 Enter로 닫는다.
  - `box→SAM2.1`(B): 적재물을 감싸도록 박스를 드래그하면 SAM 마스크가 NEW로 추가된다. 필요하면 꼭짓점을 고친다. 마음에 들지 않으면 삭제하고 박스를 다시 그린다(= 마스크 재생성).
  - 초안이 더미 일부만 덮으면 초안을 REJECT하고, 팔레트마다 box→SAM으로 새로 만드는 것이 빠를 때가 많다.
- **검토자가 반드시 직접 정하는 것**
  - 모든 초안과 원본의 결정. 처음에는 모두 "— 미결 —"이고, 그림에는 `?`가 붙는다.
  - R2, R3(약 410px 미만 적재물이 보였는지), R4(가림)
- **문제가 없는 이미지**: 원본 KEEP(음성이면 R2 = NO_ORIGINAL), R3 / R4 → `검토 완료로 저장`
- **저장**
  - `S` 또는 `저장(진행 중)`. 다른 이미지로 넘어갈 때 자동 저장된다.
  - `검토 완료로 저장`은 조건을 다 채워야 통과하고, 빠진 항목은 빨간 글씨로 보여 준다.
  - 같은 브라우저에서는 검토자 이름이 기억된다.

## 주의
- 도구는 아무것도 자동 승인하지 않는다. AI 힌트와 SAM 결과는 제안일 뿐이다.
- 검토 화면과 이미지에는 사람 얼굴이 있다. 스크린샷이나 작업 폴더를 GitHub에 올리지 않는다.
- 검토가 끝나면 export → finalize v02 → `labels_v02`를 만든다(별도 지시 후 실행).
