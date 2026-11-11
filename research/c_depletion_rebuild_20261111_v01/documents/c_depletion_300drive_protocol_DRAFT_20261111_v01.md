# C 조건 G1 300회 물리 주행 프로토콜 (DRAFT/HOLD)

10개공통base×C100/C80/C60/C40/C20×O0/O25×HR_Scan/LR_Scan/GeoCAD=300. 표현당100회,고정분모300. 동일base는같은제거경로·시작점·카메라·조명·환경으로짝지어진다. 최종100조건manifest는아직없고실제좌표/Scene ID를생성하지않았다. O50는별도강건성분모다. 같은base의C/O/표현은반복측정이고300독립환경이아니다.

운용은G1 ROBUST_A 단일촬영·단일접근,중간재인식없음. 현재M50를신규C model로조용히바꾸지않는다. 최종checkpointSHA·학습/선정계보·전처리·640/1280해상도·confidence/NMS·목표선택정책을선행잠금해야한다. C모델운용해상도변경이필요하면별도검증된version으로분리한다.

성공판정은현재미확정이다. 과거 .11m/7.34177432289679°는 evaluation/full_e2e_targets_v01.py와stage3_outcome의MAIN이다. .10m/5°를현행잠금success로확인한로컬증거는발견하지못했다. 기존10cm clearance는별도안전거리이지10cm pose tolerance의출처가아니다. 5mm/2°는observed PRE/FINAL 도달/정지인증조건이며GT FINAL오차대와다르다. 원본결과와안전조건은보존하되C본실험의단일기준이사전확정되기전에는launch하지않는다. 어떤기준을채택해도현재결과를보고택하면안된다.

필수진입gate: 새dataset/GT QA PASS,checkpoint/data/code SHA 잠금,C전범위pose/ROBUST_A/GT누수감사 PASS,충돌/속도/조향/정지조건 PASS,C5수준×O0/O25를포괄하는사전기술pilot PASS,100조건/300실행membership잠금,최종성공판정잠금,raw로그·RGB-D·mask·trace·영상저장검사 PASS,별도신규실행승인. pilot은300분모에합치지않는다. 이들gate는현재UNKNOWN/UNRESOLVED/NOT_RUN이며자동완료로처리하지않는다.

안전은기존.03m/s guard·조향/곡률/tracking/충돌/stop certificate·quiet/graph/TF·메모리조건을유지한다. 안전위반/환경이상/로봇상태불명은HOLD후알림이며성공할때까지재실행하지않는다. 통상인식/pose/plan실패는실패로남긴뒤사전다음조건으로진행할수있지만현재실행범위에는주행이포함되지않는다. 최종pose평가는GT canonical FINAL을사용하고GT를target생성에주입하지않는다.

결과는작업성공/검출/올바른목표/pose계산/plan/실제이동/최종오차/속도/충돌/정숙/촬영·TF·인프라를분리한다. 각시행입력·버전·failreason·rawtrace보존. Wilson은기술구간,짝비교는base대응표와cluster불확실성,비열등성은별도사전마진/가설/검정력계획이다. 10%p는확정마진이아니다.

48시간은강제종료조건이아니다. 기존G1성공25회의wall평균479.04199s,중앙481.18139s로300회약39.92h다. 보수적9분/회는45h다. 초기실패까지포함한30회평균417.33s를성공적인전체주행계획의대표속도로사용하면낙관편향이있다. 여기에dataset/학습/평가/QA/pilot시간이추가돼48h완료를보장하지않는다. 새pilot throughput확보후ETA를갱신하고시간을맞추려분모/기준을줄이지않는다.
