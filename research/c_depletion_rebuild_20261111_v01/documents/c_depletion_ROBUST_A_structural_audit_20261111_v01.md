# ROBUST_A의 C 부분적재 호환성 구조 감사 — 2026-11-11

확인된 사실: `evaluation/b5_robust_20261110_v01.py`는 mask/depth/camera와 **layer_count task metadata**를 입력으로 받는다. load-top q99에서 layer_count×.09m를 빼 pallet top을 추론하고, sensed floor+.144m와3cm 이내인지 비교한다. 실제floor가보이고불일치하면floor+.144를쓴다. floor없으면load-top branch를쓴다. B1에서는NuRec배경depth가없어floor관측이안될수있다고원본에명시돼있다.

.144m는팔레트설계두께다. 일반적인world pallet_top은floor_z+.144m이며,적재물top은그위의잔여높이다. 원본 q99는실제로관측된상위점의분위수여서부분최상층이가려지면실제최고높이를대표하지않을수있다. partial形상의loadface로완전직사각footprint중심을역산하는fallback도편향가능성이있다. pallet face가충분히보이는branch가이를완화할가능성은있지만새C센서검증은아직없다.

현재Stage4 perception CLI는 `--layer-count`를1/4만허용한다. 현행runner는L1/L4만지원한다. C60은3층,C40은2층이라는정답을manifest로직접알려주는것은새운용prior정책이며현재지시의C정답누수금지와충돌한다. 기존코드를그대로C호환이라고선언할수없다.

다음표는floor_z=0,실제최상층이완벽히관측된다는가정의**수식 반례**다. 새추론·새센서평가결과가아니다. nominal4층입력을고정하면C60/40/20에서이만큼pallet datum이낮아진다. floorbranch가관측되면결과가다를수있다.

| C | 정답잔여층수(평가용) | 적재물최상면 z m | 4층prior로역산한pallet z m | 실제 .144 대비 bias m |
| --- | --- | --- | --- | --- |
| C100 | 4 | .504 | .144 | 0 |
| C80 | 4 | .504 | .144 | 0 |
| C60 | 3 | .414 | .054 | −.090 |
| C40 | 2 | .324 | −.036 | −.180 |
| C20 | 1 | .234 | −.126 | −.270 |

좌표복원은raw projection에서fx/fy를얻고T=inv(cameraViewTransform).T의회전에diag(1,−1,−1)를적용한다. depth는distance_to_image_plane,m이며optical(right,down,forward)→world,m,Z-up이다. 최종pose는center_x/y와heading mod180이다. PRE/FINAL은예측중심과고정task_yaw로생성하고,GT FINAL은별도evaluate_terminal에서만사용한다. 현재stage3 outcome의DESIGN_CENTER/CANON_FINAL은고정좌표여서새10시나리오에서그대로사용할수없다. 새scenario별eval-only GT계약이필수다.

알고리즘계보:

- ORIG_v44: depth에서floor/pallet datum을찾고고정4층의기존core를사용한다.
- B1ADAPT SENSEDTOP: design floor z0,manifest layer count,largest depth-gap cluster 및기존surface plane gates다.
- B1ADAPT PRIORTOP: 같은적응판의design prior pallet top=.144m branch다.
- ROBUST_A: farthest major depth cluster,sensed-floor/load-top fallback,depth-continuous growth,pallet/load face기반추정이다. 위두 B1ADAPT와같지않다.

제안(미구현): C/잔여slot/정답층수를전달하지않고센서의pallet vertical face/실제support datum을우선추정하는별도C-compatible version,필요시1–4층sensor hypothesis를GT없이비교하고불확실하면거절하는계약을사전고정한다. 이는기존ROBUST_A의수정판이며기존A결과와섞지않는다. 어떤후보가적절한지는새C RGB-D·calibration·GT분리·실패분모·경로검증전에미정이다. 이번에는새알고리즘을구현하거나데이터로튜닝하지않았다.

PASS: 코드구조/입력의존성/좌표계/기준면구분/기존SHA. UNKNOWN: 새C의실제계산성공·오차·GT비사용호환성·path/safety. 따라서Cpose gate와물리주행은HOLD다. 증거는 `reports/c_depletion_preparation_evidence_20261111_v01/`의source SHA와수식반례CSV다.
