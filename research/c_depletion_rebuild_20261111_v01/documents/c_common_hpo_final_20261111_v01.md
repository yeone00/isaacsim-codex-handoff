# C 데이터 전용 공통 HPO 최종 자동 집계

{
  "selection": {
    "candidate_id": 6,
    "params": {
      "lr0": 0.000888131352250591,
      "weight_decay": 0.0008730658008775225,
      "lrf": 0.13119036537141066,
      "warmup_epochs": 4.486041867303101
    },
    "score": 0.9432983046074382,
    "rule": "200epoch own-validation mask-only mean; ties lowest candidate id; no Test",
    "protocol_sha256": "e29a63be4eb45d6acc7bee602270920cacfa8f0fa528f67026008633457efa08"
  },
  "seed_summary": [
    {
      "candidate_id": 0,
      "rep": "HR_Scan",
      "n": 1,
      "mean": 0.9436677060440373,
      "sd": null,
      "seed_metrics": {
        "42": 0.9436677060440373
      }
    },
    {
      "candidate_id": 0,
      "rep": "LR_Scan",
      "n": 1,
      "mean": 0.9295142220990564,
      "sd": null,
      "seed_metrics": {
        "42": 0.9295142220990564
      }
    },
    {
      "candidate_id": 0,
      "rep": "GeoCAD",
      "n": 1,
      "mean": 0.9554379082398287,
      "sd": null,
      "seed_metrics": {
        "42": 0.9554379082398287
      }
    },
    {
      "candidate_id": 6,
      "rep": "HR_Scan",
      "n": 3,
      "mean": 0.9427946456535125,
      "sd": 0.001404866854639785,
      "seed_metrics": {
        "42": 0.9428226306356432,
        "43": 0.9441853109534577,
        "44": 0.9413759953714365
      }
    },
    {
      "candidate_id": 6,
      "rep": "LR_Scan",
      "n": 3,
      "mean": 0.9329454105446141,
      "sd": 0.001205178554431954,
      "seed_metrics": {
        "42": 0.9318487993017541,
        "43": 0.9327517335620786,
        "44": 0.9342356987700097
      }
    },
    {
      "candidate_id": 6,
      "rep": "GeoCAD",
      "n": 3,
      "mean": 0.9549840209307077,
      "sd": 0.00029742772302890336,
      "seed_metrics": {
        "42": 0.9552234838849172,
        "43": 0.9546510844569516,
        "44": 0.9550774944502542
      }
    }
  ],
  "total_worker_wall_seconds": 25928.752110242844,
  "failed_jobs": [
    "crossval_C00_HR_Scan_s42_to_LR_Scan",
    "crossval_C00_HR_Scan_s42_to_GeoCAD",
    "crossval_C00_LR_Scan_s42_to_HR_Scan",
    "crossval_C00_LR_Scan_s42_to_GeoCAD",
    "crossval_C00_GeoCAD_s42_to_HR_Scan",
    "crossval_C00_GeoCAD_s42_to_LR_Scan",
    "crossval_C06_HR_Scan_s42_to_LR_Scan",
    "crossval_C06_HR_Scan_s42_to_GeoCAD",
    "crossval_C06_LR_Scan_s42_to_HR_Scan",
    "crossval_C06_LR_Scan_s42_to_GeoCAD",
    "crossval_C06_GeoCAD_s42_to_HR_Scan",
    "crossval_C06_GeoCAD_s42_to_LR_Scan",
    "crossval_C06_HR_Scan_s43_to_LR_Scan",
    "crossval_C06_HR_Scan_s43_to_GeoCAD",
    "crossval_C06_LR_Scan_s43_to_HR_Scan",
    "crossval_C06_LR_Scan_s43_to_GeoCAD",
    "crossval_C06_GeoCAD_s43_to_HR_Scan",
    "crossval_C06_GeoCAD_s43_to_LR_Scan",
    "crossval_C06_HR_Scan_s44_to_LR_Scan",
    "crossval_C06_HR_Scan_s44_to_GeoCAD",
    "crossval_C06_LR_Scan_s44_to_HR_Scan",
    "crossval_C06_LR_Scan_s44_to_GeoCAD",
    "crossval_C06_GeoCAD_s44_to_HR_Scan",
    "crossval_C06_GeoCAD_s44_to_LR_Scan"
  ],
  "test_used": false,
  "seed42_selection_bias": true,
  "rng_policy": "UNCHANGED v04 locked PhotoDegrade implementation: Python global random seeded per Ultralytics worker; Gaussian noise uses numpy.default_rng(random.getrandbits(32)); NOT documented per-sample (seed,epoch,index) generator. Same workers=8 and fixed run seed. No RNG repair; fresh baseline controls share implementation. Exact bitwise cross-machine reproducibility not claimed."
}

전체 후보: /home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02/C_COMMON_HPO_v02/hpo_results.csv
교차표현 Validation: /home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/execution_v02/C_COMMON_HPO_v02/jobs.json
기존 모델·Test·Stage4 결과는 변경하지 않음. seed42는 탐색과 중복되어 선택 편향 가능. RNG는 기존 worker Python random/getrandbits 구현 유지. 독립 blind Test 미실행.
