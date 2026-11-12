# C100 균형 보강 및 가림 평가 계획 추가안 — DRAFT

상위 기존 C_DEPLETION_REBUILD 계획의 변경 제안만 기록한다. **현재 실행기·dataset·HPO·단계 전환에 적용하지 않았다.** 근거: `reports/c100_balance_b1_l4_reuse_and_hpo_plan_audit_20261112_v01.md`.

1. C-V01 O0 4,410장은 보존하고 C-HPO를 계속한다. 기존Test/모델노출을기록한다.
2. 최소보강안:70기본환경을50/10/10split그대로유지. C100 기존view0+새view4개로350/표현(250/50/50), 신규280/표현·840총. 부분C각350은그대로. 새O0 5,250장(Train3750/Val750/Test750)은별도versionedroot/recipe/manifest/SHA계보. 기존B1 L4 직접호환추가RGB-D0, canonicalGT/환경참조는새관측수에포함하지않는다.
3. 촬영조건4개는실측허용범위/QA를확인한후Test성능을보기전에정한다. 기존anchorpaired분석과추가C100-view분석을구분한다. C100만view분포가넓어지는교란을명시. 전체상태의view를대응시키는대안은별도추가4200렌더제안으로유지한다.
4. 신규Train/Val에서는기본+현재Val상위서로다른비기본3후보의공통설정을200epoch×3표현×seed42로검증(12모델),선정후seed43/44×3표현(6모델). 최대18학습/3600epoch의제한적재선정안. 후보/예산/metric/동점규칙은실행전새잠금. 기존모델이어학습이나Test재선정금지.
5. O0만훈련/선정. O25/O50평가는Test계보에서만생성,각O0와잔여이력·camera·환경을대응. 실제coverage/GT 독립QA,같은최종checkpoint로세O조건평가. balanced안Test O별750총2250,그중가림1500. 기존계획대비추가가림240,보강신규O0840과합계1080관측증가.
6. 기존qualification 엔지니어링 fixture는Train을쓰지만모델평가/학습/선정에쓰지않고논문가림Test분모에서제외한다. 가림평가계보는Test전용이다. 이미지수가독립환경수가아님을명시한다.
7. 현재자동정적평가계획을바꾸지않으며새dataset생성/HPO의실행승인으로사용하지않는다. 물리pilot/300/별도150HOLD유지.
