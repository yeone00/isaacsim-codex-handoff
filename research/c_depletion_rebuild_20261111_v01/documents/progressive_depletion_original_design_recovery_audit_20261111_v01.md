# Progressive Depletion 원래 설계 복원 및 B1 생성 경로 감사 — 2026-11-11

## 핵심 판정

**원래 C100→C80→C60→C40→C20 구현과 생성 기록이 실제로 보존돼 있다. 현재 B1의 L1–L4는 그것을 실행한 결과가 아니라 완전한 층 수를 바꾸는 별도 Nominal 생성 경로다.** 따라서 25/50/75/100%를 C20/40/60/80/100으로 이름만 바꾸어 복구할 수 없다. 원래 연구 질문이 비정형 부분 적재라면 부분 최상층을 잃은 B1만으로 그 질문을 검증할 수 없다. B1의 기존 결과는 L1–L4 전체층 실험으로 유효 범위를 한정해 보존한다.

4층 × 층당 Bundle5 15묶음 × 묶음당 벽돌5개 = **300개**다. 한 층은75개다. 다른 층수·층당 개수 설명을 새 보고서에 사용하지 않는다. 과거 문서·잠금은 삭제하거나 조용히 수정하지 않고 이 정정 보고서를 연결한다.

이번 작업은 CPU stdlib·nice15·ionice idle의 기존 CSV/JSON/코드 정적 분석이다. legacy 모듈 import/실행, 신규 데이터셋·시나리오·렌더·추론·학습·주행 모두0. 기존 HPO는 중지하거나 설정을 바꾸지 않았다.

## 1. 원래 알고리즘과 권위 자료

- 생성기: `/home/user/hh/isaac_cosmos/scripts/build_nonideal_depletion_manifest_v01.py`. top-level에 mkdir·CSV 쓰기가 있으므로 import/실행하지 않고 읽기만 했다.
- 잠금: `SDG/nonideal_depletion_v01/design_v01/NONIDEAL_DEPLETION_V01_DESIGN_LOCK.json`, SHA `147cfece6eac2d3dec8ab35815426740be47a08860534b2f9939cc3894bc0f5c`.
- manifest 1,680행 SHA `f0d750eff63c574be45887a860aba04d542811d5e0df5e60c88a95166d339b4d`.
- trajectory states 840행 SHA `91be95a38da7c3bb87ade9f7bc1e46e2aa96c9840cdbb4e96735731fa58020b3`.
- 제거 이력 9,600행 SHA `e872fffbf5a62ec901d9aa531b4b67be2556ca8bb0c2fae0293e4fa2268f1422`.
- geometry 원본 `/home/user/nonideal_matched_canonical_gt_production_v03.py`의 Pattern A/B와 실제 RGB production·B1의 Nominal source Pattern A/B가 일치한다. source/dependency SHA는 lock과 대조했다. 전체 입력 경로·SHA는 evidence/inputs_sha256.json.

C100(60묶음)에서 시작해 최고 비어 있지 않은 층만 살핀다. 그 층의 잔여 Bundle5가 차지하는 10×9 격자에서 바깥 경계에 닿거나, 경계로부터 4-neighbor flood-fill된 빈 공간에 접한 묶음만 후보로 삼는다. 밀폐된 내부 빈 공간은 외부 노출로 취급하지 않는다. 매 단계 정렬된 후보 집합을 다시 계산한 뒤 고정 rng.choice로 하나를 제거한다. 상층을 모두 비운 후 하층으로 내려가며12묶음마다 저장한다. 네 번 저장하므로 총48묶음/240개를 제거한다.

Pattern A/B는 각15개 직사각 Bundle5 footprint로10×9 격자를 빈틈·중복 없이 타일링한다. S는2×3, R은3×2 격자 셀이다. **격자 셀6개가 벽돌6개라는 뜻이 아니다.** 실제 create_actual_bundle은 offset −2/−1/0/+1/+2 × .057m에 벽돌5개를 만들고5를 반환한다. CELL=.095m, 층 높이 .090m, pallet 높이 .144m다. 아래 층의 위치·방향은 그대로 두고 해당 묶음만 삭제한다. phase는 ABAB 또는 BABA로 고정된다.

| 상태 | 잔여 벽돌 | 잔여 Bundle5 | L1/L2/L3/L4 묶음 수 | 최상층 잔여 |
| --- | --- | --- | --- | --- |
| C100 | 300 | 60 | 15/15/15/15 | L4,15 |
| C80 | 240 | 48 | 15/15/15/3 | L4,3 |
| C60 | 180 | 36 | 15/15/6/0 | L3,6 |
| C40 | 120 | 24 | 15/9/0/0 | L2,9 |
| C20 | 60 | 12 | 12/0/0/0 | L1,12 |

원본은40환경 × 2재료 × [FULL1 + trajectory5×부분상태4] =1,680 base scene다. material을 제외한 geometry state는840개다. C100은 trajectory마다 중복 저장하지 않는다. 과거 Proxy도 별도 archive에 있지만 이번 표현 정합 검증은 HR/LR/CAD3개만 대상으로 했다.

## 2. 실제 제거 이력 검증

독립 CPU 검사기로 **기존에 저장된** 이력200경로×48단계를 순서대로 검증했다. 새 환경이나 새 학습 샘플을 생성한 것이 아니다. 각 단계의 최고층·외부 노출 후보·정렬·seeded rng.choice 결과가 저장된 제거와9,600/9,600 일치한다. 12단계마다 기존 snapshot에 도달하고, C20⊂C40⊂C60⊂C80⊂C100의 strict inclusion800전이가 모두 성립한다. 묶음 내5개 벽돌을 함께 제거하므로 벽돌 집합도 같은 포함 관계다.

manifest1,680행을840trajectory state와 다시 대응해 두 재료의 잔여 ID·phase·mask가 일치함을 확인했다. 이어 실제 RGB production metadata1,680×3표현=5,040개에서 manifest SHA, 잔여 묶음, mask_by_layer, 실제 생성 brick reference 수, 실행 source SHA를 모두 검증했다. 같은 제거 이력이 HR/LR/CAD에 실제 전달됐다는 기록 증거는 PASS다. 이번에 모든 RGB를 재렌더하거나 픽셀로 벽돌을 다시 센 것은 아니다.

**안정성 해석:** 최고층부터 제거하고 아래 완전한 층을 유지하므로 명목 격자에서 공중 부유층은 만들지 않는다. 그러나 생성기 자체가 CoG·마찰·접촉·붕괴·그리퍼 접근 공간을 시뮬레이션하지 않으며 그 검증을 주장하지 않는다고 명시한다. 외부 노출은2D footprint 규칙이지 실제 카메라 가시성 또는 물리적 파지 가능성 보장이 아니다. 이것은 별도 물리 preflight가 필요하다.

## 3. seed의 실제 역할과 잔여 형상 고유성

원본의5개는 **환경별 T01–T05 제거 경로**다. 전역에 동일 seed5개만 쓰는 구조가 아니다. master260929, 환경ID, T번호를 문자열 `260929|MNIDB_xxxx|Txx`로 결합한 SHA256 첫8hex를32bit seed로 바꾼다. 40환경에서200개 경로를 만든다. material과 표현은 seed 계산에 넣지 않으므로 같은 환경·T에서 두 재료와 세 표현에 같은 이력을 적용한다. HPO의 sampler20261111·학습42/43/44·B1 scene_seed와 구분해야 한다.

형상 비교에는 이미지/seed/hash 차이가 아닌 **잔여 Bundle ID + phase + 명목 로컬 x/y/z 중심 좌표 및 방향의 exact set**을 사용했다. 환경의 world pose·카메라·조명·재료를 빼고 형상만 비교했다. 위치는 원본 grid로부터 정수 micrometer로 계산했다. 같은 slot 안에서 HR/LR/CAD mesh 자체가 같다는 뜻은 아니다.

| C | 기존 geometry state 수 | 전체40환경에서 고유 형상 | 각 환경5경로 내부 고유 수 | 동일 환경 중복 쌍 |
| --- | --- | --- | --- | --- |
| C100 | 40 | 2 | {'1': 40} | 0 |
| C80 | 200 | 184 | {'5': 40} | 0 |
| C60 | 200 | 197 | {'5': 40} | 0 |
| C40 | 200 | 198 | {'5': 40} | 0 |
| C20 | 200 | 174 | {'5': 39, '4': 1} | 1 |

C100의2개는 ABAB/BABA의 phase 차이다. 같은 환경에서는 공유FULL1개뿐이므로 5개의 고유 형상으로 세지 않는다. 부분 상태는 전체 환경 사이에도 형상 반복이 있으며,200경로라고200개 독립 형상은 아니다.

**확인된 중복:** MNIDB_0006/BABA/C20에서 T02(seed3281395651)와 T05(seed2131428289)의 잔여 L1 bundle ID가 똑같이 `[1,2,5,6,7,8,9,10,11,13,14,15]`다. seed와 제거 순서가 달라도 최종 형상은 같다. 이 환경의 C20은5경로/4고유형상이며 그대로 보존한다. 나머지39환경의 C20 및 모든환경 C80/C60/C40은 각5고유형상이었다.

다음은 MNIDB_0001에서 다섯 seed가 남긴 최상층의 실제 Bundle ID다. 아래의 완전한 층은 앞 표와 같다. 모든40환경840state·26,400묶음의 실제grid좌표/명목mm위치는 별도CSV에 있다.

| T | seed | C80 L4 | C60 L3 | C40 L2 | C20 L1 |
| --- | --- | --- | --- | --- | --- |
| T01 | 2282867795 | [7, 13, 14] | [1, 2, 3, 8, 9, 14] | [2, 5, 6, 7, 9, 10, 11, 12, 15] | [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 15] |
| T02 | 2095838417 | [2, 6, 9] | [3, 5, 8, 9, 12, 14] | [1, 4, 5, 6, 8, 10, 11, 14, 15] | [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 15] |
| T03 | 3009675888 | [10, 13, 14] | [2, 3, 5, 6, 12, 13] | [5, 6, 7, 8, 9, 10, 12, 14, 15] | [1, 2, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15] |
| T04 | 2505136018 | [1, 4, 13] | [3, 10, 11, 12, 13, 15] | [1, 3, 4, 5, 6, 7, 10, 12, 14] | [1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 14, 15] |
| T05 | 1548221560 | [2, 13, 14] | [1, 2, 4, 8, 10, 14] | [1, 2, 3, 5, 6, 10, 11, 14, 15] | [1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15] |

시각 증거: `progressive_depletion_design_audit_evidence_20261111_v01/existing_first_environment_5seed_top_slots.svg`. 기존slot을 그린 도식이며 시뮬레이션 캡처가 아니다. C100의 FULL을 비교 편의상5칸에 반복 표시했을 뿐 새 샘플5개로 세지 않는다. SVG의 숫자는 Bundle ID, 초록은잔여, 회색은제거다.

## 4. 현재 B1과 차이표

실제 B1 train/val/test package records4,200행→고정red manifest1,400행→각표현 capture의 complete JSON4,200개를 대조했다. 실행기는 `scripts/b1_red_production_capture_20261105_v03.py`; 그 안의 AST loader가 `/home/user/step21_b2b_production_rgb_iso400_v02.py`의 iterate_pattern/create_actual_load/build_scene을 사용한다. canonical은 `/home/user/nonideal_canonical_nominal_replay_v02.py`다. `scripts/b1_sdg_capture_20261103_v01.py`를 확인했지만 그 초기adapter가 실제최종production인 것처럼 바꾸어 쓰지 않았다. invocation의 code SHA와 실행원본이 일치한다.

build_scene의 expected는 load_count×layer_count×75다. iterate_pattern은 layer_phase의 각 층에 Pattern A/B15묶음을 모두 만들며 잔여mask/제거history 인자를 받지 않는다. 실제 complete 기록의 bricks_expected=bricks_created, 각load mapped_ids=75×층수가4,200/4,200 일치했다. 여러팔레트가 있는 scene은 각팔레트가 같은 전체층수 조건이다. 장면 전체 brick수를 팔레트1개의 brick수로 오인하지 않는다.

| 항목 | 원래 Progressive Depletion | 현재 B1 L1–L4 |
| --- | --- | --- |
| 기준/수준 | full300에서300/240/180/120/60 | 75/150/225/300;25/50/75/100% |
| 생성 연산 | 최고층 외부노출 Bundle5 순차삭제 | phase문자열 길이만큼 전체층생성 |
| Bundle5 자체 | 5벽돌 묶음 단위 제거 | 5벽돌 묶음 배치는 있음, 삭제는 없음 |
| A/B | ABAB/BABA 유지, 삭제된묶음제외 | A/B,AB/BA,ABA/BAB,ABAB/BABA |
| 비정형 최상층 | 3/6/9/12묶음 | 언제나15묶음 완전층 |
| 누적부분집합 | 동일환경·T의C전이보존 | 장면별다른seed/조건;공통삭제이력없음 |
| seed역할 | 환경×T제거선택 | 고정scene seed/분할/배치/조명/위치등의장면신원;제거선택아님 |
| 표현대응 | 공통잔여mask+seed | 공통scene/완전층phase;부분삭제전달없음 |
| 연구질문 | 감소량 및 비정형 잔여형상 | 전체층수/높이 변화의Nominal인식 |

현재 B1의 팔레트 형상은 각L마다 두 phase variant뿐이다. 서로 다른scene seed는카메라·배경·배치·load수변동을동반해도부분잔여형상다양성을뜻하지않는다. L1=346장면,L2=342,L3=366,L4=346(합1,400); 각L의부분최상층형상수0이다.

| L | train 장면/표현 | val 장면/표현 | test 장면/표현 | 벽돌/팔레트 |
| --- | --- | --- | --- | --- |
| L1 | 254 | 47 | 45 | 75 |
| L2 | 240 | 52 | 50 | 150 |
| L3 | 262 | 50 | 54 | 225 |
| L4 | 244 | 51 | 51 | 300 |

세표현의장면수는같다. 과거PROJECT_STATE의「L1–L4로대체」는기존작업의변경기록이며C80 등을 생성한증거가아니다. 이번감사는누가언제어떤논의로변경을승인했는지까지확정하지않는다. 확인한것은원본설계와실제생성경로의차이다.

## 5. 기존 자료 재사용 범위

| 자료 | 가능한 재사용 | 제한/금지 |
| --- | --- | --- |
| 원래depletion840geometry/1680scene | 제거알고리즘·slot·누적이력·도식·기존benchmark의정의검증 | 전부test인원manifest를새train/val에넣지않음;이미본benchmark를blind라하지않음 |
| 원래RGB/GT/pose 결과 | 과거환경조건을명시한보조mechanism/OOD분석 | B1배경·카메라·촬영과동일조건으로합치지않음;새연구의원본대체불가 |
| B1 Train/Val/Test1000/200/200 | 기존L버전학습·HPO·인식·가림·pose결과보존;고정모델의추후C검증baseline | L1/2/3을C20/40/60 등으로 재라벨링금지;새C평균으로소급집계금지 |
| B1 L4 RGB/GT | C100의명목배치공통;새protocol의배경/pose/분할/annotation까지동일하면제한적재사용검토 | geometry만같다고새C paired scene의FULL로자동편입불가 |
| B1모델48개 및진행HPO | 고정legacybaseline/이전데이터최적화로보존 | 새C에최적이라는주장금지;테스트로모델재선정금지 |
| 기존Stage4 M50/G0–G3/O50 | 기존고정분모·버전조건의물리결과 | 새B1/C모델과동일실험으로혼합/소급변경불가 |

또한 `/home/user/build_morphology_aware_depletion_manifest_v01.py`의기존Train/Val-only2400설계는C수준·제거rule을참고할수있는별도역사자료다. donor환경을한번씩할당한설계이므로동일환경에서5C를모두대응시킨nested주행설계와동일하다고하지않는다. 이번감사에서그root전체를새잠금으로승격하거나실행하지않았다.

## 6. 현재 HPO 영향과 진행률

HPO를중지·재시작·패키지변경하지않았다. 별도tmux의기존L버전실험으로보존한다. 정상종료후선정된설정은 **B1 L1–L4 Validation에서선정된공통설정**으로만부른다. 새C데이터셋의목적함수가바뀌므로전이성은아직UNKNOWN이다. 본감사나기존Test결과로현재후보순위·승격·학습파라미터를바꾸지않는다.

상태조회 2026-11-11T18:05:28.566030+09:00: RUNNING, controller PID3130638, 현재 `full_C05_HR_Scan_s42` epoch83. 초기12후보×3표현의60epoch탐색은전부완료했다. 17:59스냅샷의학습누적3365/최대6966 model-epochs=48.31%;이는최대예산대비이며벽시계진행률이나63run의비율과다르다. 선정이기본설정이면중복seed실행이줄어총량이작아진다. 오류0/중단0으로기록됨. 최신상태는 `SDG/B1_COMMON_HPO_20261111_v01/hpo_status.json`을먼저확인한다.

## 7. C 설계 복귀의 최소 재생성·재학습·재평가안 — DRAFT, 미실행

1. **설계·검증 코드 잠금:** 기존geometry/외부노출/순서/seed/부분집합을그대로보존하는새adapter를계획한다. 현재B1 full-layer source에mask입력을억지로대입하지않는다. 기존원본수정금지. 모델성능과무관하게새version의scene계보·phase·잔여slot·derivedseed·capture환경·pairedrepresentation을먼저잠근다. 지지안정성·충돌overlay·GT역할검증을독립gate로둔다. 이번에는새scene membership조차생성하지않았다.
2. **분할:** 동일환경·모든T·5C·가림파생은같은split으로묶는다. C간nested관련성을무시한이미지무작위분할은금지한다. 원래depletion/기존B1평가환경과의독립성은ID문자열뿐아니라source geometry/background/camera lineage로검증한다. 새로운scene seed만바꿔독립blind라고하지않는다.
3. **원래5경로와FULL중복제거를보존하는구체예시:** train50환경/val10환경/test10환경 × [FULL1+5T×4부분]=1050/210/210 base scenes/표현, 합1470×3=4410 RGB다. 50/10/10은실행확정이아닌최소규모안이고,기존1000/200/200을맞추려고임의잔여state를잘라내지않는다. 새시점·가림이포함된별도blindTest는추가분모를사전에명시해야한다. 기존B1과학습이미지수5%차이및모델-epoch당update차이도보고한다. 단순명목총량만맞춘공정비교라고하지않는다.
4. **재생성:** C80/60/40/20의RGB·canonical/visible GT·필요한depth/camera를새namespace에서짝지어생성해야한다. 현재완전층사진을crop해서만들수없다. 동일조건검증없는C100도새paired묶음의일부로촬영하는것이기본안이다. 새가림O25의실제가림측정과GT정합을다시검증하고O50는보조로분리한다. 생성전소량qualification은향후별도선행gate이며이번실행0이다.
5. **최소학습:** 기존L-HPO의선정설정과원래기본설정을새C Train/Val에서동일pretrained·3표현·seed42로새학습(최대6모델)하고각200epoch·Val mask기준대조한다. 동일설정이면중복생략3모델이다. 이비교는hyperparameter transfer검증이지새C에대한완전HPO가아니다. 새Val로새설정이선정되면그선정과한계를공개한다. 선택후seed43/44를양설정에같이추가하면총최대18모델(설정동일이면9)로평균/표본SD와seed42선택편향을보고할수있다. 즉기존HPO최적값을무검증승계하지않고,Test로설정선정하지않는다. 새C전체HPO를할지는이후별도예산/잠금문제다.
6. **재평가:** 잠근기존L모델과새C모델을같은C Test에서비교;자기/교차표현Mask mAP·목표선택·실제가림별성능·조건부pose오차·전체pose계산성공률·path승인·물리주행단계를분리한다. B5/A의top面/높이prior가부분층에어떻게반응하는지저장RGB-D 오프라인감사부터한다. GT슬롯/잔여율을운용pose입력에누출시키지않는다. M50와B1모델계보/카메라해상도/전처리도별도로잠그고동일모델로자동간주하지않는다.

위환경수·sample수·학습안은새실험제안이다. 현재잠긴Train/Val/Test나HPO설정을개정한것이아니며이번턴신규생성·재학습은없다.

## 8. 300회 물리 주행 수정안 — DRAFT, 미실행

| 수준 | O0 / 표현 | O25 / 표현 | 표현당 | 3표현합계 |
| --- | --- | --- | --- | --- |
| C100 | 10 | 10 | 20 | 60 |
| C80 | 10 | 10 | 20 | 60 |
| C60 | 10 | 10 | 20 | 60 |
| C40 | 10 | 10 | 20 | 60 |
| C20 | 10 | 10 | 20 | 60 |
| 합계 | 50 | 50 | 100 | 300 |

10개공통base scenario를선정해각base에같은T제거이력의5C와같은O0/O25카메라·시작조건을대응시킨다. 예를들어10개서로다른환경/시작조건에T01–T05를각2개씩사전배정한다. 각환경의derivedseed는원래규칙을따르고표현에독립이다. C100은경로마다새고유형상인척중복하지않는다. 만약2환경×5T를10으로구성한다면C100은반복조건이되므로그구조를그대로기록해야한다. 기본권고는10개명시적base의짝비교이며,이base의실제좌표·선정은이번에생성하지않았다.

300은10base×5C×2O×3표현의실행수다. 독립환경300개가아니며동일이력의C전이·같은base의O/표현은관련표본이다. 분석은base/환경cluster또는반복측정을고려한다. O50는별도root·분모로계획하고300에합치지않는다. 모델체크포인트·선정데이터·제거geometry·B5/Aversion·성공기준·안전상한·실행순서·실패분류를선행잠금한다. 표현순서는성공결과와무관한균형순서로계획한다. HPO와동시GPU주행금지,기존물리안전상한완화금지. freshRGB-D FullE2E를사용하며frozenGT pose대체금지. 현재는감사완료에따른계획안뿐,실행승인이나300회run manifest가아니다.

## 9. 선행연구 재확인 및 인용 경계

연구별확인수준을구분했다. 아래는원본논문·저자/기관·공식출판기록을우선확인한것이고,접근차단된PDF를모두정독했다고하지않는다. 우리Bundle5·C20간격·seed choice의직접출처는로컬연구설계다. 관련연구는문제배경/접근성/지지관계의동기이며세부규칙제안자로인용하지않는다.

| 연구 | 서지/확인 수준 | 본 연구와 관련되는 범위 |
| --- | --- | --- |
| Caccavale et al.,2020 | R.Caccavale,P.Arpenti,G.Paduano,A.Fontanellli,V.Lippiello,L.Villani,B.Siciliano. *A Flexible Robotic Depalletizing System for Supermarket Logistics*. IEEE RA-L5(3):4471–4476. DOI10.1109/LRA.2020.3000427. [기관원기록/초록](https://www.iris.unina.it/handle/11588/832425) 확인;저자preprintPDF는403으로전체재열람미완료 | 센서정보/작업제약에따른하역계획·감시·적응. 우리5벽돌묶음이나C간격출처아님 |
| Motoda et al.,2023 | T.Motoda,D.Petit,T.Nishi,K.Nagata,W.Wan,K.Harada. *Multi-Step Object Extraction Planning From Clutter Based on Support Relations*. IEEE Access11:45129–45139. DOI10.1109/ACCESS.2023.3273289. [저자서지](https://tomohiromotoda.github.io/) 및 [IEEE공식초록](https://ieeexplore.ieee.org/abstract/document/10117592) 검색결과확인;직접본문접근418/원논문전체미확인 | 지지관계·collapse prediction graph로순서와안전추출을고려. 우리2D노출규칙을해당논문의지지그래프구현이라고주장불가 |
| Ruttico,Pacini & Beltracchi,2024 | *BRIX: an autonomous system for brick wall construction*. Construction Robotics8,article10. DOI10.1007/s41693-024-00123-z. [출판사원문](https://link.springer.com/article/10.1007/s41693-024-00123-z) 확인 | rover+협동arm의brick wall construction시스템. 본문팔레트3×3×3예시도우리4층×15Bundle와다름 |
| Rim & Lim,2011 | S.-C.Rim,K.-S.Lim. *Pallet Consolidation Problems in Distribution Centers*. 대한산업공학회지37(4):289–296. DOI10.7232/JKIIE.2011.37.4.289. [학회논문제공페이지/초록](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE01907732), [저자기관서지](https://www.ajou.ac.kr/ie/people/prof-search-popup.do?article_no=132540&empl_no=199111051&mode=profView) 확인;PDF403/전체원문미확인 | 부분적재팔레트의공간문제·합적최적화. 로봇Bundle제거알고리즘으로인용불가 |
| Jeevanandam et al.,2025 | S.S.Jeevanandam,S.Inuganti,S.Govil,D.Stricker,J.Rambach. *JENGA: Object selection and pose estimation for robotic grasping from a stack*. IROS2025기록([DFKI](https://www-live.dfki.de/web/forschung/projekte-publikationen/publikation/16049)), [arXiv2506.13425v1 원문](https://arxiv.org/html/2506.13425v1) 확인 | pose·maskvisibility·IMU높이로높은층/비가림의적절한대상을선택. 우리의load-level간격·5seed노출삭제와동일설계아님 |

PDF접근오류403/418 및DOI해석오류는자료확보한계로남긴다. 서지와초록을확인한논문을전체원문검증완료로승격하지않는다. 실제원고의세부알고리즘비교에는접근미완료3논문의저자PDF/기관원문추가확인이필요하다.

## 10. 산출물·검증 상태·다음 조치

PASS: lock/dependency SHA,840state/9600history/200seed경로/800strictnesting,1680manifest↔840state↔2재료,5040실제RGBmetadata↔3표현,4200 B1complete,고유geometry exact-set비교,원본입력SHA불변. FAIL(설계동일성): B1L1–L4는ProgressiveDepletion의대체로동일하지않음. UNKNOWN: 동적지지안정성,새C에서L-HPO전이성,접근차단3논문전체원문. 기존HPO RUNNING/보호,신규GPU작업0.

증거폴더 `reports/progressive_depletion_design_audit_evidence_20261111_v01/`:

- `audit_result.json`, `inputs_sha256.json`, `manifest_to_trajectory_pairing.json`, `historical_representation_pairing.json`
- `history_replay_200_trajectories.csv`, `unique_shapes_by_environment_condition.csv`, `shape_uniqueness_summary.json`, `duplicate_seed_shapes.json`
- `all_840_existing_states_top_layer.csv`, `existing_bundle_slot_positions.csv`, `existing_first_environment_5seed_top_slots.svg`
- `B1_actual_completion_4200_rows.csv`, `B1_split_level_counts.csv`, `B1_geometry_diversity.json`, `HPO_snapshot.json`

새분석코드 `analysis/progressive_depletion_design_audit_20261111_v01.py`는원본legacy를import하지않는다. broad텍스트검색출력truncation/없는추정경로조회exit2는발견탐색오류이며실험실패가아니다. 그후실제invocation으로경로를확인했다. 다음단일작업은새C설계의분할/분모/잔여slot adapter/평가·안전gate를DRAFT→별도잠금으로구체화하는것이다. 자동렌더/학습/주행은개시하지않는다.

최종재확인: 고정입력9257개SHA불변, HPO잠긴코드5개SHA불변, 분석AST·SVG XML PASS. HPO 최신 2026-11-11T18:05:58.577876+09:00 full_C05_HR_Scan_s42 epoch91 RUNNING. 증거 `final_preservation_checks.json`.
