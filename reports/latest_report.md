# 건설현장 Environment USD 원본 출처·라이선스 추적 조사

조사일: **2026-11-03 KST**. 판정은 **CONFIRMED(직접 근거), LIKELY(유력하나 추가 검증 필요), UNKNOWN(현재 확인 불가)**로 구분한다.

## 1. 조사 개요

**핵심 결론:** 현재 연구에서 참조한 배경의 확인 가능한 로컬 상위 입력은 `Constructionsite_isaac.usdz`다. 연구 파일은 `Downloads/assets_full.zip` 안의 동일 멤버 및 다운로드 폴더의 복사본과 **바이트 단위 SHA256 일치**한다(CONFIRMED). 그러나 이 USDZ 자체가 이미 합성 stage를 export한 패키지여서, 외부에서 최초 배포한 원본 DCC 파일·실제 제작자·최초 다운로드 URL·당시 라이선스까지 확정되지는 않았다(UNKNOWN).

유력한 공개 후보는 CGTrader **Construction site 3D Scan**, 상품ID **4762918**, 게시 계정 **thisismy7thaccountlmao**다(LIKELY). 외관과 규모가 유사하나 공개 원본 파일의 mesh/texture SHA를 확보하지 못했다. **이 계정을 실제 제작자로 확정하거나 해당 페이지 라이선스를 현재 USD에 확정 적용하지 않는다.**

읽기 전용 검색 범위는 `/home/user/hh`, `/home/user/Downloads`, `/home/user/Documents`의 USD/USDA/USDC/USDZ 전체다. **376파일**, USDZ 내부 layer를 더해 중복 identifier를 제거한 **406레이어**, 내부 패키지 멤버 **890개**, composition arc **20,934개**를 조사했다. 이 중 연구용 배경 패키지로 연결되는 파일225개와 다른 환경 파일을 포함한 **관련 후보234파일**을 별도 분류했다. 다른 로봇/벽돌 USD도 전수 목록에 남겼으며 이것들을 모두 건설현장 환경으로 부르지는 않았다.

`Documents/Kit/shared/screenshots`는 권한 거부로 검색하지 못했다. 따라서 PC 전체·삭제된 파일·외부 저장장치까지 전수 확인했다는 뜻은 아니다. 기존 Python 모듈 실행·Isaac Sim/Kit·ROS·렌더·시뮬레이션·USD 저장·패키지 설치는0이다. standalone `pxr.Sdf` 및 `Usd/UsdGeom`으로 layer·배열을 읽었다. 기존 PROJECT_STATE, 코드, USD, 실험 결과, 기존 보고서는 변경하지 않았다.

증거 폴더: [construction_environment_usd_provenance_evidence_20261103_v01](construction_environment_usd_provenance_evidence_20261103_v01/). 모든 파일의 경로·크기·mtime·ctime·SHA는 `usd_file_inventory.csv`; birth time은 `usd_birth_times.csv`; 관련성·원본/파생 분류·실사용 확인 범위는 `environment_relevant_file_inventory.csv`다. 각 파일의 실사용을 파일 존재만으로 확정하지 않았다.

## 2. 현재 연구에서 사용한 환경 USD 식별

네 요청 후보는 **모두 실제 존재**한다(CONFIRMED). 다운로드 폴더의 동일명 복사본도 구분했다.

|ID/역할|검증한 절대 경로|bytes|SHA256|
|---|---|---:|---|
|F1 연구배경패키지|`/home/user/hh/isaac_cosmos/assets/assets/environment/Constructionsite_isaac.usdz`|286948692|`c0bb44d1ef17c96028ec4137e9527675585362634fdac436c15ac4b9ceb81efa`|
|F1D 다운로드복사|`/home/user/Downloads/assets_full/assets/environment/Constructionsite_isaac.usdz`|286948692|`c0bb44d1ef17c96028ec4137e9527675585362634fdac436c15ac4b9ceb81efa`|
|F2 별도NuRec|`/home/user/hh/isaac_cosmos/assets/assets/environment/5F_CLOSED_EV.usdz`|86326118|`892ca7c846bbf2b48399176350185a50fb95bee8997fc1ec57ae50337c822b81`|
|F2D 다운로드복사|`/home/user/Downloads/assets_full/assets/environment/5F_CLOSED_EV.usdz`|86326118|`892ca7c846bbf2b48399176350185a50fb95bee8997fc1ec57ae50337c822b81`|
|F3 연구base scene|`/home/user/hh/isaac_cosmos/sdg_practice/construction_scene_rover_recovery.usd`|30340|`865bb3fd13189bfc4d9e51124828cc646b209ddb06ca5e3412b0e0ef232fd978`|
|F4 조명파생|`/home/user/hh/isaac_cosmos/sdg_final/CONSTRUCTION_SITE_E2E_LIT_20261022_v01/construction_site_e2e_lit.usda`|1478|`4e0ad262a0ce2a733e86e82e2ba69aa0eee42bb87c33086925117956bbddade8`|
|F5 v30 실제입력|`/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03/prepared_site_drive.usda`|196408|`72fda3227219a7f39fea4a3393d3adb036bf6e8eb029adaa4292a62f50bd396f`|
|F6 v43 정적overlay|`/home/user/hh/isaac_cosmos/sdg_final/THREE_REP_OCCLUSION_20261102_v43/static_overlay_v43.usda`|2164|`30f5da0c94de61feead321df67f0b85777268fa0669f08a4d6ff05bfc758f275`|

|ID|현재 파일시스템 birth time|mtime(KST)|
|---|---|---|
|F1|2026-08-11 16:44:34.466532731 +0900|2026-08-10T17:24:21+09:00|
|F1D|2026-08-11 16:48:47.227510359 +0900|2026-08-10T17:24:21+09:00|
|F2|2026-08-11 16:44:30.760861323 +0900|2026-04-02T15:32:30+09:00|
|F2D|2026-08-11 16:48:44.680359729 +0900|2026-04-02T15:32:30+09:00|
|F3|2026-08-27 18:23:19.576203221 +0900|2026-08-28T11:40:18.494819+09:00|
|F4|2026-10-22 11:59:30.957970749 +0900|2026-10-22T11:59:30.957971+09:00|
|F5|2026-11-02 04:08:30.336595983 +0900|2026-11-02T04:08:30.338596+09:00|
|F6|2026-11-02 19:58:12.816080422 +0900|2026-11-02T19:58:12.816080+09:00|

birth time은 **이 파일시스템에서 파일이 만들어진 시각**이며 3D 콘텐츠의 최초 제작 시각이 아니다. mtime은 ZIP의 보존된 과거 시각일 수 있다. ctime은 inode 상태 변경 시각으로 생성 시각과 다르다. `key_file_stat.txt` 및 전수 CSV에 별도로 기록했다.

- **F1 실제 연구 의존성 CONFIRMED:** F3의 `/World/ConstructionSite`가 `../assets/assets/environment/Constructionsite_isaac.usdz`를 직접 reference한다. 최신 v43의 static overlay→v30 prepared stage→기존 task scene→F3→F1 계보도 확인했다. v43 저장 capture_record의 source_stage는F5다. 기존 `docs/PROTOCOL_LOCKS.md`의 base scene 경로 및 SHA와 현재 F3가 일치한다.
- **F2 실사용 UNKNOWN:** 로컬 환경 묶음에 있으나 F3/F4/F5/F6의 건설현장 배경 계보에 들어 있지 않다. package 이름만으로 본 연구에서 사용했다고 쓰지 않는다.
- **F4 실제 연구 preview branch CONFIRMED:** 기존 2026-10-22 보고서 및 `static_preview.png`가 있는 조명 파생 씬이다. F4는 v43→v30 계보의 필수 조상과는 별도 분기다.
- **전체225 연결파일의 개별 runtime 사용 UNKNOWN:** 연결됨·생성됨과 실제 실행됨은 다르다. 핵심 runtime 입력/의존성만 확인 표시했다.

## 3. 원본 및 파생 파일 계보

확인된 **로컬 유입 계보**는 다음과 같다. 화살표가 인터넷 최초 배포자까지 증명하지는 않는다.

```text
외부 최초 제작/DCC 파일/최초 배포 URL             UNKNOWN
                 ↓ 변환·편집 경위 UNKNOWN
Downloads/assets.zip + assets.z01
                 ↓ 셸기록: zip -s 0 assets.zip --out assets_full.zip
Downloads/assets_full.zip
                 ↓ 셸기록: unzip assets_full.zip -d ~/hh/isaac_cosmos/assets
assets/assets/environment/Constructionsite_isaac.usdz
                 ↓ reference
sdg_practice/construction_scene_rover_recovery.usd
                 ↓ 여러 task/mount/controller overlays
        ┌────────┴─────────────────────┐
preview→visible→runtime_fixed→lit     prepared/pilot layers→v30→v43 static overlay
```

`assets.zip` 448,196,322bytes와 `assets.z01` 629,145,600bytes는 파일시스템상 **2026-08-11 11:12 KST**에 생성됐다. 합친 `assets_full.zip`은1,077,341,918bytes, 같은 날16:44:22 KST 생성이다. 연구 F1의 birth16:44:34 KST는 압축 해제 순서와 일치한다. 관련 셸 명령은 `.bash_history-62733.tmp:1800,1802` 등4개 임시 history에 반복 보존돼 있다. history 자체의 신뢰 가능한 명령 실행 timestamp는 없으므로 사용자·정확한 실행 시각을 history만으로 확정하지 않았다.

`assets_full.zip`은34 entry, README/LICENSE 항목0이다. **5개 environment USDZ 모두 ZIP 멤버/Downloads 해제본/연구 해제본 SHA 일치**(CONFIRMED). `download_archive_member_comparison.csv`, `archive_sha256.json`, `relevant_shell_history.csv`에 저장했다. 다른 로봇 파일의 연구용 변경 여부를 배경 원본 판정과 섞지 않았다.

최신 v43 배경 의존성은 **16개 node/15개 arc**의 한 확인 경로로F1에 연결된다. 전체 절대경로는 `key_reference_chains.json`, 모든 연결 파일은 `source_reference_chains.json`에 있다. 원본 package를 합성/flatten하여 다른 원본처럼 기록하지 않았다.

## 4. 파일별 메타데이터와 출처 단서

### F1 — Constructionsite_isaac.usdz

**CONFIRMED:** ZIP 내부는 `Constructionsite_isaac.usd` 26,786,345bytes와 JPEG410개, 총411멤버다. 내부 `.usd`는 헤더 `PXR-USDC`인 binary layer이며 이름의 확장자와 실제 포맷을 구분했다. 원본을 풀어 덮어쓰거나 USD로 재저장하지 않았다. layer1235 prim: Xform3/Scope1/Material410/Shader410/**Mesh1**/GeomSubset410이다.

```text
/World
  /Env
    /Looks/cb5ce5926fdd4ce2b8f8f548239dcfaf_..._jpg/...
    /cb5ce5926fdd4ce2b8f8f548239dcfaf
      /cb5ce5926fdd4ce2b8f8f548239dcfaf       [Mesh]
```

메시는 **194,223정점 /382,994 삼각형 /1,148,982 face index**다. JPEG는 `0/cb5ce5926fdd4ce2b8f8f548239dcfaf_000.jpg` 등의 명칭이며410개다. 숫자는0-padding이 혼재하므로 `_1.jpg`가 있다고 가정하지 않고 실제 ZIP 명단을 사용했다. 샘플은2048×2048이며 모든 이미지의 해상도·EXIF 조사는 `texture_image_metadata.json`에 있다. **EXIF 보유0/410**. ID는 강한 검색 단서지만 MD5나 Sketchfab ID라는 것은 확인되지 않았다.

layer metadata는 defaultPrim=`World`, upAxis=`Z`, metersPerUnit=1, documentation에 합성 stage에서 생성됐다는 문구다. author/copyright/license/URL 및 source-package의 customLayerData/assetInfo 출처 정보는 찾지 못했다. subLayers/reference/payload로 외부 원래 모델을 가리키는 링크도 없다. **이미 composed stage export를 거친 로컬 패키지**라는 점은 확인되지만, 어느 프로그램에서 최초 제작했는지·누가 변환했는지는 UNKNOWN이다. OmniPBR/MDL 명칭은 renderer material 기술이며 NVIDIA가 배경 저작자라는 증거가 아니다.

메타데이터가 비어 있다는 이유로 조사를 중단하지 않고 prim ID·410 texture·정점/면 수·기존 화면·묶음 파일·웹 후보까지 대조했다. 인터넷상 동일 ID 검색은 upstream URL을 복원하지 못했고 Sketchfab 동일 ID API는404였다. **이 ID를 임의의 Sketchfab 다운로드 링크로 확정하지 않는다.**

### F2 — 5F_CLOSED_EV.usdz

**CONFIRMED:** 내부는 `default.usda`806bytes, `gauss.usda`2,243bytes, `Jeonju_114644.nurec`86,322,737bytes의3멤버다. `default.usda`는 `gauss.usda`를reference하고 `/World/gauss` Volume의density/emissive field가같은 `.nurec`를참조한다. `OmniNuRecFieldAsset`, `omni:nurec:isNuRecVolume` 등이있다. mesh/JPEG 기반 F1과 다른 표현이다. 같은묶음의다른환경은 Jeonju_115451/120448/122151 명칭을사용한다.

이명칭은촬영/작업명 단서이며 도시·촬영기관·권리자를 확정하지 않는다. renderSettings와 defaultPrim·단위가있지만 제작자·원 배포 URL·라이선스는 UNKNOWN이다. 현재 연구의F1과 동일 모델·원본이라고묶지않았다.

### F3/F4/F5/F6 — 연구 파생 씬

F3은48 authored prim이며 background package reference에 rover/camera/target/light/graph 등을 추가한다. layer customLayerData에는 cameraSettings, authoring_layer=`./construction_scene_rover_recovery.usd` 등이 있으나 콘텐츠 author/copyright가 아니다. F4는4 authored prim의 lighting overlay로 runtime_fixed를subLayer로두고 Dome 색/강도와RectLight를정의한다. F5/F6은여러 기존task/fixture/representation layer를합성한다.외부robot/brick참조와background의저작권을분리해야한다.

`usd_layer_metadata.json`은406 layer의metadata, `usd_composition_arcs.csv`는subLayer/reference/payload의prim별경로, `usd_asset_texture_paths.csv`는외부asset/texture/MDL경로, `usd_prim_hierarchy.csv`는전체prim계층이다. 모든 layer를read-only로열었고최종 layer failure0이다. shader의string URL/프로그램명도별도검사했으나 배경 원저작자 URL은복원되지않았다. unresolved MDL·로컬의존성은라이선스허가로해석하지않았다.

## 5. 최초 유입 경로 조사 결과

**CONFIRMED:** 2026-08-11에생긴split ZIP/합친ZIP/해제본의존재·byte동일성과압축해제명령흔적. `Downloads`라는디렉터리명만으로특정인터넷사이트에서받았다고판정하지않았다.

**LIKELY:** 이묶음이현재 연구의초기asset유입물이다. 연구용F1은2026-08-10exportmtime를보존하고2026-08-11해제birth를갖는다. F1을직접 참조하는 `construction_scene_step07.usd`/`..._restored.usd`의현재 mtime는2026-08-27, recovery파일birth도8월27일이다. 따라서이시점이초기scene구성의유력구간이다. 파일시각만으로최초 시뮬레이션 실행일을확정하지않았다.

**UNKNOWN:** split ZIP을만든사람,메일/메신저/공유드라이브전달자,최초원 배포다운로드 URL,원본FBX/BLEND/OBJ의위치,구매/무료다운로드영수증,당시 약관. 관련파일의xattr에는다운로드출처가없었다. readable Chrome4개profile의 `History` DB를read-only/immutable로정확한archive/환경파일basename에한정조회했지만일치download행0이었다. activeWAL·삭제/정리/이전PC기록이포함되지않으므로다운로드가없었다는증명은아니다. 무관한개인방문기록·계정정보는보고서/증거에복사하지않았다.

starter와 `isaac_cosmos`는Git저장소가아니다. 접근가능한handoff repo의candidate USD명 Git이력도0이었다. 변경된연구문서가있다고asset저작권허가가생기지는않는다. 관련상위형식/동일이름의FBX/BLEND/OBJ/MTL/glTF/GLB/README/LICENSE경로검색에서도upstream construction asset은찾지못했다. **범위내negative evidence**로남긴다.

## 6. 인터넷 원본 배포처 검색 결과

인터넷접근가능. 검색일2026-11-03. exact파일명·고유ID·construction-site/scan/interior·플랫폼별질의를진행했다. `web_search_log.json`에검색어·공식URL·실패를기록했다.

|조사대상|결과|동일성 판정|
|---|---|---|
|NVIDIA Isaac Sim5.1 공식환경목록|grid/warehouse/hospital/office등. 요청파일명·고유ID를동일원본으로연결하는항목미발견|UNKNOWN; `_isaac`파일명은NVIDIA제작/허가증거아님|
|Omniverse/AirLab/GitHub|AirStack/RAVEN의ConstructionSite stage는발견. localpackage와mesh/texture연결근거없음|UNKNOWN; 이름일치만으로채택하지않음|
|Sketchfab|관련scan 후보들. exactID검색미확인,직접IDAPI404,일부page403|UNKNOWN; 다른모델CC라이선스전용금지|
|CGTrader|Construction site3DScan #4762918 발견|**LIKELY**; 아래대조한계있음|
|Fab/Unreal관련|Joe013 stylized3688tris·immerge rubble scans등발견|local scan과동일 근거없음;상대라이선스차용금지|

공식목록확인근거: [NVIDIA5.1 Environment Assets](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/assets/usd_assets_environments.html), [AirStack scene catalog](https://docs.theairlab.org/main/docs/simulation/scenes/). 카탈로그에없다는사실만으로모든NVIDIA배포물에없다고단정하지않는다.

### 가장 유력한 CGTrader 후보 — 아직 동일성 미확정

공식 상품페이지: [Construction site 3D Scan / model4762918](https://www.cgtrader.com/free-3d-models/scanned/various/3d-scanned-construction-site-performance-friendly). 페이지는제작/게시계정을 `thisismy7thaccountlmao`, 게시일2023-09-08, Matterport Pro3 스캔,BLEND/FBX/JPG와약295MB,정점약195,000/면약385,000으로표시한다. 이는**그상품에대한확인사항**이고우리USD의저작자확정이아니다.

local은194,223정점/382,994면으로표시값대비각약−.398%/−.521%차이다. 규모가가깝지만숫자는정확히같지않다. 변환/삼각분할/페이지반올림가능성을가정해동일성을확정하지않았다. 공개preview와local texture/기존render에서흰콘크리트기둥,창개구,노출케이블트레이,주황색전기함,바닥금속부재등유사한구성을대조했다.이단서와scan형태는LIKELY를뒷받침하지만객체가비슷하다는관측만으로CONFIRMED가되지않는다.

공개preview2장과local410texture전체에SIFT+ratio.7+homography4px 진단을실행했다.최대rawinlier14였으나무관한texture부분이preview의극소영역으로모이는**퇴화대응**을확인하여**동일성증거로거절**했다. 성공처럼보고하지않았다. `public_preview_texture_matches.csv`, `texture_match_summary.json`, `public_candidate_identity_assessment.json`에수치와거절이유를보존했다. 실패한 match그림은확정 매칭그림이아니다.

공개 원본 모델archive를받아mesh/texture SHA를대조하거나모델소유자확인을얻지못했다. **공식 상품URL은존재하지만실제우리파일의다운로드 URL·최초배포처인지는UNKNOWN**이다. publicpreview는검증용증거보관이며논문게재/재배포권리를획득한것이아니다. 상품page의일반HTTP직접fetch는200/emptybody,webreader는본문접근가능이었고previewJPEG는200이었다. 로그인/구매/권리 허가 우회는하지않았다.

## 7. 원저작자 및 라이선스 검증

**현재 연구USD에 확정 적용되는 라이선스: UNKNOWN. 학술 연구·논문 사용 허가: UNKNOWN.** localpackage/묶음안에licensetext가없다는것은공개도메인이라는뜻이아니다.

CGTrader후보의현재 표시는 **Royalty Free License (no AI)**다. 공식약관의21B는머신러닝/신경망 학습 사용에대한추가제한을두고,24조는무료파일도판매자가선택한라이선스를따른다고설명한다. [CGTrader공식약관20/21A/21B/24](https://www.cgtrader.com/pages/terms-and-conditions). **무료=제한없음,학위논문=모든활용자동 허용으로해석하지않는다.** 현재페이지를과거다운로드시점의확정약관으로소급하지않으며,해당candidate가다르거나이전별도 계약이있을가능성도열어둔다.

|확인할권리|현시점판정|필요근거|
|---|---|---|
|원저작자/원 배포기관|UNKNOWN;후보게시계정만확인|모델 파일 동일성+계정/권리자 확인|
|학술 시뮬레이션 사용|UNKNOWN|실제 취득시점/취득주체의license/계약|
|학위논문 스크린샷·결과이미지|UNKNOWN|이미지복제·배포·전자공개권한과표기의무|
|합성데이터생성/모델학습·ML활용|UNKNOWN;후보가맞으면No-AI범위점검필수|과거허가/별도ML허가또는권리자서면해석|
|USD변환·수정|UNKNOWN|정확한사용권및수정허용조건|
|원본/수정USD·texture재배포|허가확인안됨|sourceasset재배포권한별도확인|
|attribution/저작권고지의무|UNKNOWN|정확한asset별license및계약조건|

후보약관21A는프로젝트에포함된사용과독립 asset 재배포를구분한다.논문 이미지공개와편집 가능한USD/texture또는합성데이터셋공개를같은권리로보지않는다.지금자료만으로위법/적법판정을확정하지않는다.

다른사이트일반규정도자동적용하지않았다. [Fab공식설명](https://www.fab.com/eula)은Standard와CC-BY를구분하고독립 asset 재배포제한등을설명한다. [CC BY4.0공식문서](https://creativecommons.org/licenses/by/4.0/)의표기의무를우리USD에적용하려면먼저우리asset에그라이선스가부여됐다는증거가필요하다. NVIDIA/Isaac Sim소프트웨어라이선스도외부콘텐츠권리를대체하지않는다.

## 8. 논문 사용 시 필요한 출처 표기

**확정저작자처럼출처를꾸미지않는다.** 현재내부원고메모에는“로컬입력Constructionsite_isaac.usdz, 원 배포자·라이선스확인중,SHA256…;연구자는로버/목표물/조명등을추가”라고기록할수있다.그러나“출처미상”표기만으로공개권리를해결하지는못한다.

동일성·허가 확보후채울표기틀:

> 환경배경: [확정제작자/권리자], “[확정모델명/버전]”, [공식원본 URL], [취득일/확인일], [정확한라이선스명·원문URL]. 본연구에서USD변환[실제확인된변경],로버·벽돌fixture·카메라·조명을추가함. [필요저작권고지/허가문서식별자].

CGTrader후보가맞더라도해당계정을기재하기전원본확인과historicallicense증거를확보해야한다. 캡션/방법/참고문헌/부록및온라인학위논문에대한고지위치를허가조건에맞춘다. CC BY가실제로확인되면제작자·원본·라이선스링크·변경내역을표기한다.별도 계약이면그문구를따른다.

## 9. 출처 불명확 시 발생 가능한 문제와 대응 방안

1. **파일 동일성/권리연결단절:** splitarchive전달자에게원다운로드page·원본압축파일·영수증·당시 license를요청한다. package의동일ID/410texture/정점수와F1SHA를제공해정확한 버전을찾는다.질문은사용자에게전달했지만본조사에서답변을받았다고기록하지않았다.
2. **논문/ML/데이터배포범위불일치:** 확인대상에는스크린샷·결과 그림·온라인학위논문·합성데이터생성·학습/추론·USD변환·공동연구자공유·원본/수정본공개를명시한다.단순‘연구목적’허가로모두가능하다고추정하지않는다.
3. **candidate license의No-AI가능성:** 원취득시점license와별도합의부터확인하고,기관도서관저작권담당/산학협력단등과적용 범위를검토한다. 현재후보약관을우리과거 연구에자동 소급하거나,ML사용을자동 허용하지않는다.
4. **확인 불가가계속될경우:** 공개논문용이미지사용의서면 허가를확보하거나,권리가 명확한배경/직접제작배경으로대체하는별도계획을세운다.대체가실험조건/결과에미치는영향은별도version과재현성설명으로다룬다.이번작업에서는환경교체·재실험·기존 결과 수정을하지않았다.
5. **증거보존:** 원본과수정본을구분해hash/받은날짜/전달자/원본 URL/licensecopy를보관한다. 원본USD/texture를논문부록이나공개저장소에첨부하기전재배포권을별도로검토한다.

사람이추가 검색할정확한검색어: `"Constructionsite_isaac.usdz"`, `"Constructionsite_isaac.usd"`, `"cb5ce5926fdd4ce2b8f8f548239dcfaf"`, `"Construction site 3D Scan" "4762918"`, `"5F_CLOSED_EV.usdz"`, `"Jeonju_114644.nurec"`. 후보파일을정상취득하면archive/각textureSHA,194223points/382994triangles,410materialsubset,prim/UV배열을대조하고최종동일성 판정을갱신한다.근사면수·비슷한이미지만으로hash불일치를무시하지않는다.

## 10. 최종 결론 및 추가 확인 필요 사항

|질문|답변|판정|
|---|---|---|
|**Q1 최초원본 파일은?**|연구계보상확인된로컬상위 입력은F1 `Constructionsite_isaac.usdz`.ZIP멤버·다운로드복사·연구복사의SHA동일.이미export된USDZ이며그이전외부최초제작/DCC파일은미확인.|로컬상위 입력CONFIRMED / 외부최초원본UNKNOWN|
|**Q2 실제 제작자는?**|확정 불가.CGTrader #4762918의게시계정thisismy7thaccountlmao가유력단서지만우리USD와byte동일성·권리자 신원미확인.|UNKNOWN;후보연결LIKELY|
|**Q3 다운로드처·원본 URL은?**|현재PC유입은assets.zip+assets.z01→assets_full.zip→연구assets.공식CGTrader후보URL은존재하지만이PC파일이그곳에서받은것인지는입증못함.|로컬유입 계보CONFIRMED / 실제원다운로드 URLUNKNOWN|
|**Q4 라이선스·학위논문 사용은?**|우리USD적용license미확인으로사용 가능확답불가.유력후보현재 표시No-AI;동일성·당시취득 조건·이미지/ML/공개범위서면 확인필요.|UNKNOWN|
|**Q5 원본대비얼마나수정?**|받은로컬USDZ와연구용USDZ는byte변경0.그에대한4개핵심파생씬의points/facecounts/indices/normals/UV및worldtransform도exact동일.로버/목표물/카메라/조명등stage구성은추가됨.외부DCC원본→현재USDZ변환/수정정도는미확인.|검사한배경배열/변환불변CONFIRMED / 외부최초원본대비변경UNKNOWN|
|**Q6 논문 전조치는?**|archive전달자·원취득자에게모델page/원본 파일/과거license/영수증요청→동일성검증→논문그림·ML·공개범위허가 확보→정확한출처작성.불가하면권리가 명확한대체안과연구영향을별도 검토.|추가 확인필수|

Q5의수치근거는 `composed_environment_geometry_comparison.json`이다.4개stage(F3/F4/F5/F6)에서5개배열의NumPy전체바이트SHA와값/shape를대조했고mesh world transform도같다.관련조상layer의`/World/ConstructionSite`아래authoredopinion은원래package reference1개였다.이것은전체로봇실험모든stage의물리설정·조명불변이나외부원제작물과의동일성을뜻하지않는다. initialfingerprint CSV의`*_display_string_sha256`는배열표시문자열digest이며정확한전체배열판정에는사용하지않았다.

**검사결과:** source USD376개+PROJECT_STATE1개=377개시작/종료SHA보존PASS,layer406개최종readPASS/failure0,packaged환경5개동일성PASS,4개핵심scene배경geometry/worldtransformPASS.외부원 제작자/원URL/licenseUNKNOWN. 보고서및신규증거폴더만작성했다.기존 보고서 덮어쓰기0,PROJECT_STATE 변경0,시뮬레이션0,외부 연락/게시/기존 파일 수정0.

실패/한계도보존했다. initialpseudoRoot.GetAsText표시probe는지원되지않아exit1,첫backgroundinspection은child지속실행미확인으로결과없음,attempt02는SdfLayerOffsetPythonconverter,attempt03은빈assetpath예외로실패했다.이후offset읽기/빈경로처리를보완한attempt04는exit0으로406layer검사를완료했다.원본 조작으로오류를우회하지않았다.없던texture `_1.jpg`표본명probe도실패후실제ZIP명단으로해결했다.403/404/emptybody/timeout웹시도및퇴화image-matching도성공으로바꾸지않았다.지원코드snapshot·로그·SHA는증거폴더에있다.원격Git동기화상태는이번조사에서확인하지않았다.
