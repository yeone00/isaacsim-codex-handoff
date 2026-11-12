"""C-V02 frozen final seed42 perception and unchanged ROBUST_A with explicit occupied-layer task prior.
C-only CLI permits1,2,3,4; legacyStage4 source/results untouched. No re-identification/physical launch.
Input: sensor capture + operator task metadata + SHA-locked final mixed model selection, never GT pose/mask/slots.
"""
import argparse, hashlib, json, sys, time, traceback
from pathlib import Path
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R))
SENSOR_FILES = ('front_rgb.npy', 'front_rgb.png', 'front_depth.npy', 'camera_metadata.json')
ROBUST_CODE = R / 'evaluation/b5_robust_20261110_v01.py'
ROBUST_FROZEN = Path('/home/user/hh/isaac_cosmos/sdg_final/B5_ROBUST_20261110_v01_run01/frozen_config.json')
ROBUST_CODE_SHA = '0b1e5f46702d4af0c4d4abc4b7d1c5fe9d29cc07c9f34b4a1592990ac296ae29'
ROBUST_CONFIG_SHA = '35cf0a78d4c73919ab2a03378341fb90433aeaeeab306a605d064d98a0cfc529'
from evaluation.stage4_ablation_b_logic_20261110_v01 import REID_CENTROID_GATE_M, REID_POSE_GATE_M, reid_select, pose_gate  # noqa: E402
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def clean(x):
    """JSON-safe copy: non-finite floats -> None (recorded as null, never silently dropped), numpy -> python."""
    import math
    if hasattr(x, 'tolist') and not isinstance(x, (str, bytes)): x = x.tolist()
    if isinstance(x, float): return x if math.isfinite(x) else None
    if isinstance(x, dict): return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    return x


def mask_centroid_xy(mask, depth, meta_text):
    """Median world XY of valid-depth mask pixels (sensor only)."""
    import numpy as np
    from evaluation.b1_b5_adapter_20261110_v01 import _calibration, world_points
    cal, T = _calibration(meta_text); world, valid, _, _ = world_points(depth, cal, T)
    sel = mask & valid
    if sel.sum() < 20: return None
    return [float(np.median(world[sel][:, 0])), float(np.median(world[sel][:, 1]))]


def robust_pose(mask, depth, meta_text, layer_count):
    from evaluation import b5_robust_20261110_v01 as rb
    assert sha(ROBUST_CODE) == ROBUST_CODE_SHA, 'ROBUST_A_CODE_SHA_MISMATCH'
    frozen = json.loads(ROBUST_FROZEN.read_text()); cfg = frozen['config']
    assert frozen['config_sha256'] == ROBUST_CONFIG_SHA and rb.config_sha(dict(rb.DEFAULT_CONFIG, **cfg)) == ROBUST_CONFIG_SHA, 'ROBUST_A_CONFIG_SHA_MISMATCH'
    assert frozen['estimator_code_sha256'] == ROBUST_CODE_SHA, 'ROBUST_A_FROZEN_CODE_SHA_MISMATCH'
    out = rb.estimate_pose(mask, depth, meta_text, int(layer_count), config=cfg)
    out['method'] = 'ROBUST_A'; out['code_sha256'] = ROBUST_CODE_SHA; out['frozen_config_sha256'] = ROBUST_CONFIG_SHA
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--capture', type=Path, required=True)
    ap.add_argument('--representation', choices=['HR_Scan', 'LR_Scan', 'GeoCAD'], required=True)
    ap.add_argument('--layer-count', type=int, choices=[1, 2, 3, 4], required=True, help='task metadata (ROBUST_A API input; ORIG_v44 ignores it)')
    ap.add_argument('--pose-method', choices=['ROBUST_A'], required=True)
    ap.add_argument('--mode', choices=['initial'], required=True)
    ap.add_argument('--reference', type=Path, default=None, help='reobs: INITIAL capture dir (sensor files + selected_mask.npy + predicted_pre_final.json)')
    ap.add_argument('--task-metadata',type=Path,required=True);ap.add_argument('--task-registry',type=Path,required=True);ap.add_argument('--task-registry-sha',required=True);ap.add_argument('--model-lock',type=Path,required=True);ap.add_argument('--model-lock-sha',required=True)
    a = ap.parse_args(); O = a.capture
    from evaluation.c_v02_task_layer_prior_20261112_v02 import validate_task
    task_metadata=json.loads(a.task_metadata.read_text());assert validate_task(task_metadata)==a.layer_count
    assert sha(a.task_registry)==a.task_registry_sha,'TASK_REGISTRY_SHA_MISMATCH'
    assert json.loads(a.task_registry.read_text())[task_metadata['task_id']]==task_metadata,'TASK_NOT_IN_LOCKED_REGISTRY'
    assert sha(a.model_lock)==a.model_lock_sha,'FINAL_MODEL_LOCK_MISMATCH'
    def emit(n, d):
        with (O / n).open('x') as f: json.dump(clean(d), f, indent=2, allow_nan=False, default=lambda x: x.tolist() if hasattr(x, 'tolist') else str(x))
    res = dict(task_prior_used=True,GT_pose_mask_slots_used=False,task_metadata=task_metadata,schema='C_V02_task_prior_perception_v01', status='INTERNAL_EXCEPTION', mode=a.mode, pose_method=a.pose_method, representation=a.representation, GT_input=False,
               sensor_inputs={n: sha(O / n) for n in SENSOR_FILES if (O / n).exists()}, code_sha256=sha(__file__), started_wall_s=time.time())
    try:
        assert all((O / n).exists() for n in SENSOR_FILES), 'SENSOR_INPUT_MISSING'
        import numpy as np, cv2, torch, ultralytics
        from ultralytics import YOLO
        from scripts.full_e2e_perception_worker_v01 import select_detection
        from evaluation import b1_b5_adapter_20261110_v01 as b5
        from evaluation.full_e2e_sensor_datum_adapter_v02 import verify_core
        from evaluation.full_e2e_targets_v01 import generate
        verify_core('/home/user/eval_step25_pose_final_locked_v01.py')
        locked=json.loads(a.model_lock.read_text());selected=next(m for m in locked['models'] if m['rep']==a.representation and int(m['seed'])==42);spec=dict(path=selected['checkpoint'],sha256=selected['sha256']);assert locked.get('status')=='LOCKED'
        observed = sha(spec['path']); assert observed == spec['sha256'], 'MODEL_SHA_MISMATCH'
        model = YOLO(spec['path']); names = model.names
        emit('frozen_model_manifest.json', dict(representation=a.representation, recipe='C_V02_FINAL_MIXTURE_SEED42_PREDECLARED', checkpoint=spec, observed_sha256=observed, class_names=names,
                                                imgsz=640, conf=.25, iou=.70, mask_threshold=.5, versions=dict(torch=torch.__version__, ultralytics=ultralytics.__version__, numpy=np.__version__),
                                                input_rgb=str(O / 'front_rgb.png'), input_sha256=sha(O / 'front_rgb.png'), scene_inference_calls=1, gt_input=False))
        rgb = np.load(O / 'front_rgb.npy'); depth = np.load(O / 'front_depth.npy'); meta_text = (O / 'camera_metadata.json').read_text()
        t0 = time.monotonic()
        result = model.predict(source=rgb[:, :, ::-1].copy(), imgsz=640, conf=.25, iou=.70, max_det=100, retina_masks=True, device=0, verbose=False)[0]
        res['inference_s'] = time.monotonic() - t0
        cv2.imwrite(str(O / 'detection_overlay.png'), result.plot())
        candidates = []; rows = []
        if result.masks is not None:
            for i, (m, cls, conf) in enumerate(zip(result.masks.data.cpu().numpy(), result.boxes.cls.cpu().numpy(), result.boxes.conf.cpu().numpy())):
                mask = cv2.resize((m > .5).astype(np.uint8), (640, 480), interpolation=cv2.INTER_NEAREST).astype(bool)
                candidates.append(dict(detector_index=i, class_name=names[int(cls)], confidence=float(conf), mask=mask))
                rows.append(dict(index=i, class_id=int(cls), class_name=names[int(cls)], confidence=float(conf), mask_area_px=int(mask.sum()),
                                 depth_valid_pixels=int((mask & np.isfinite(depth) & (depth > 0)).sum()),
                                 centroid_xy_m=mask_centroid_xy(mask, depth, meta_text) if names[int(cls)] == 'brick_load' else None))
        mask = None; reid = None
        loads = [c for c in candidates if c['class_name'] == 'brick_load']
        if a.mode == 'initial':
            if loads:
                picked = select_detection(candidates); mask = picked['mask']
                res.update(detection_conf=picked['confidence'], detector_index=picked['detector_index'])
            sel_rule = 'highest confidence brick_load, tie smallest detector index; no GT'
        else:
            ref = a.reference; ref_mask = np.load(ref / 'selected_mask.npy'); ref_depth = np.load(ref / 'front_depth.npy')
            ref_c = mask_centroid_xy(ref_mask, ref_depth, (ref / 'camera_metadata.json').read_text())
            ref_pred = json.loads((ref / 'predicted_pre_final.json').read_text())['pose']
            reid = dict(reference_capture=str(ref), reference_mask_centroid_xy=ref_c, reference_center_xy=[ref_pred['center_x_m'], ref_pred['center_y_m']],
                        centroid_gate_m=REID_CENTROID_GATE_M, pose_gate_m=REID_POSE_GATE_M, candidates=[])
            table = [dict(detector_index=c['detector_index'], class_name=c['class_name'], confidence=c['confidence'], centroid_xy_m=r['centroid_xy_m']) for c, r in zip(candidates, rows)]
            sel, nearest, ranked = reid_select(table, ref_c)
            reid['candidates'] = [dict(dist_to_reference_m=d, neg_conf=nc, detector_index=i) for d, nc, i in ranked]
            if sel is not None:
                picked = next(c for c in candidates if c['detector_index'] == sel); mask = picked['mask']
                res.update(detection_conf=picked['confidence'], detector_index=sel); reid.update(selected_detector_index=sel, selected_dist_m=nearest, centroid_gate='PASS')
            else:
                reid.update(selected_detector_index=None, selected_dist_m=nearest, centroid_gate='FAIL' if loads else 'NO_BRICK_LOAD')
            sel_rule = 'reobs re-identification: nearest 3D mask centroid to the initial selected mask centroid, gate %.2f m' % REID_CENTROID_GATE_M
        emit('detections.json', dict(detections=rows, yolo_inference_ran=True, selection=sel_rule, mode=a.mode))
        if mask is not None: np.save(O / 'selected_mask.npy', mask); res['mask_area_px'] = int(mask.sum())
        res['perception_status'] = 'DETECTED' if mask is not None else ('NO_DETECTION' if not loads else 'REID_FAILED')
        # both pose methods on the same selected mask (diagnostic record); the group method drives
        orig, files = b5.run_orig_v44(O.name, rgb, depth, meta_text, mask)
        if mask is not None and 'sensor_roi.npy' in files: np.save(O / 'sensor_roi.npy', files['sensor_roi.npy'])
        emit('pose_ORIG_v44.json', dict(orig, method='ORIG_v44', ast_sha256=b5.ORIG_AST_SHA256, v44_file_sha256=b5.V44_FILE_SHA256))
        try:
            from evaluation.c_v02_task_layer_prior_20261112_v02 import estimate
            robust = estimate(mask, depth, meta_text, task_metadata)
        except AssertionError as exc: robust = dict(status='LOCK_FAILURE', reason=str(exc), pose=None)
        emit('pose_ROBUST_A.json', {k: v for k, v in robust.items() if k != 'diag'})
        primary = orig if a.pose_method == 'ORIG_v44' else robust
        if a.pose_method == 'ROBUST_A' and primary.get('status') == 'LOCK_FAILURE': raise RuntimeError('ROBUST_A_LOCK_FAILURE:' + str(primary.get('reason')))
        res['pose_status'] = primary['status']; res['pose_reason'] = primary.get('reason')
        res['diagnostic_pose'] = {m: (None if not p.get('pose') else [p['pose']['center_x_m'], p['pose']['center_y_m']]) for m, p in (('ORIG_v44', orig), ('ROBUST_A', robust))}
        if mask is not None and primary['status'] == 'B5_COMPUTED' and primary.get('pose'):
            pose = primary['pose']
            if reid is not None:
                okg, d = pose_gate([pose['center_x_m'], pose['center_y_m']], reid['reference_center_xy'])
                reid.update(center_shift_m=d, pose_gate='PASS' if okg else 'FAIL')
            if reid is None or reid['pose_gate'] == 'PASS':
                targets = generate({k: pose[k] for k in ['center_x_m', 'center_y_m']}, {'task_yaw_deg': 90., 'designated_face': 'local_-X'})
                emit('predicted_pre_final.json', dict(targets=targets, pose=pose, pose_method=a.pose_method, mode=a.mode,
                                                      source='fresh RGB-D -> frozen C-V02 mixed seed42 -> %s' % a.pose_method, GT_input=False))
                res['status'] = 'TARGETS_READY'; res['predicted_center_xy'] = [pose['center_x_m'], pose['center_y_m']]; res['targets'] = targets
            else:
                res['status'] = 'REID_FAILED'; res['failure_reason'] = 'REID_POSE_GATE'
        else:
            res['status'] = ('NO_DETECTION' if not loads else 'REID_FAILED') if mask is None else 'POSE_FAILED'
        if reid is not None: emit('reidentification.json', reid); res['reid'] = {k: v for k, v in reid.items() if k != 'candidates'}
    except BaseException as exc:
        res.update(status='INTERNAL_EXCEPTION', failure_reason=repr(exc), traceback=traceback.format_exc())
    res['ended_wall_s'] = time.time()
    emit('perception_result.json', res)
    return 0

if __name__ == '__main__':
    from evaluation.c_v02_task_layer_prior_20261112_v02 import deny_evaluation_GT_reads
    with deny_evaluation_GT_reads():raise SystemExit(main())
