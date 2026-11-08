# Real labels_v02 사람 검토용 로컬 인터페이스 (2026-11-08)

성격: 도구 구현과 시험이다.
- **실제 사람 검토 0건. 승인 0건.** 시험 저장은 별도 폴더 `review_work_SYSTEM_TEST_NOT_HUMAN_20261108_v01`에만 했다(검토자 이름 SYSTEM_TEST_NOT_HUMAN). 이 이름은 실제 작업 폴더와 확정 도구에서 거부된다.
- 39개 학습, HPO, B1 test, Real Test189 추론은 하지 않았다.
- 원본 yolo_real_v01 라벨 전체 hash가 전후 같다.

## 구현
- `scripts/label_review_server_20261108_v01.py`
  - 표준 라이브러리 HTTP 서버, 127.0.0.1 전용
  - 원본은 읽기만 하고, 이미지별 상태 JSON과 추가 전용 `history.jsonl`을 쓴다.
  - "검토 완료" 저장은 서버 검증을 통과해야 한다: 검토자 이름, 모든 초안과 원본의 결정, R2–R4, 결정과 R2의 일관성, 시험용 검토자 이름 금지.
  - 원본·초안 polygon은 클라이언트 값을 받지 않는다.
  - SAM2.1 box→mask 제안(train/val만). test 이미지 요청은 404를 돌려준다.
- `scripts/label_review_ui_20261108_v01.html`(외부 라이브러리 없음)
  - Tier A / B / 전체 탭, 상태 필터, 진행 현황
  - 원본 / 초안 / 작업본 겹침 토글과 채움 조절
  - 휠 확대, 드래그 이동, 맞춤, 이전 / 다음(←/→)
  - 꼭짓점 이동·추가·삭제, polygon 그리기, box→SAM, 분리(SPLIT), GROUP 표시
  - 진행 중 저장, 이동 시 자동 저장, 재개
- `scripts/export_label_review_20261108_v01.py`: 상태를 기존 400행·102행 체크리스트 형식 + polygon 파일로 내보낸다.
- `scripts/finalize_real_labels_v02_20261108_v02.py`: export 폴더를 입력으로 받는다. 음성 이미지(R2=NO_ORIGINAL)를 처리하고 시험 검토자를 거부한다. v01은 보존했다.
- 사용법: `reports/real_labels_v02_review_20261108_v01/REVIEW_TOOL_USAGE.md`

## 시험(시험 폴더만 사용)
| 시험 | 결과 |
|---|---|
| 헤드리스 Chrome self-test 1차 | 목록 400 / Tier A 80, 이미지 972×1296 로딩, 초기 초안·원본 미결, 꼭짓점 수정 → EDIT, NEW 추가, 미완료 상태에서 "검토 완료" 거부, 진행 중 저장, 다시 불러온 상태가 같음(재개), 원본 polygon 불변, 다음 이미지 이동, 다시 열어도 수정 유지: **14/14 true** |
| 2차(서버 규칙 추가 후) | 같은 항목 13/14 true. `all_undecided_initially`만 false인데, 1차 저장 상태가 재개되었기 때문이다(재개 기능 확인). |
| API | SAM box → 128점 polygon, 분리(원본 REPLACED + SPLIT 부분) 후 검토 완료 저장 성공. 거부 확인: 검토자 없음, 초안 미결, 음성에 R2=OK, R2=OK와 분리 모순. 클라이언트가 원본 polygon을 바꾸려는 시도 무시, test 이미지 404, `--no-sam` 시 SAM 거부 |
| export | 400행 / 102행 형식 유지. 상태가 저장된 2장만 IN_PROGRESS, 나머지는 PENDING. additions / replacements / edited 파일 생성 |
| finalize v02 | 미완료 504행(시험 검토자 포함)으로 거부, 아무것도 쓰지 않음 |
| 화면 | 헤드리스 스크린샷으로 배치 확인(목록 / 이미지 / 패널) |

- 시험 중 발견해 고친 것
  - 서버에 결정과 R2의 일관성 규칙, 시험 검토자 금지를 추가했다.
  - 시험 서버를 `pkill -f`로 끄다가 자기 셸이 함께 종료됐다(exit 144). 이후 PID로 종료했다. 데이터에는 영향이 없다.

## 남은 일
1. **[사람]** 검토 도구로 400장 검토(Tier A 80장 편집, Tier B 320장 확인)
2. export → finalize v02 → `labels_v02` + `APPROVAL.json`
3. 프로토콜 v02 label sha 채움 → LOCKED. recipe v04 LOCKED
4. trainer v07 smoke → 39 run
