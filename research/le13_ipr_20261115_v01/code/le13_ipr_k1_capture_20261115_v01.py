"""LE13 independent pose-precision replication (IPR) static K1 capture v01 (2026-11-15). Fresh Kit, no physics playback, no motion.
Derived from scripts/d600_site_capture_20261115_v02.py (drive-site stage handling unchanged: prepared_site_drive.usda, drive-builder
prims disabled, site dome per row, Kit default exposure as the drive session). Differences:
  * C-V02 4-layer load (the drive geometry) at the LE13 centre (20.5, 13.5), yaw 0, from the prelock capture manifest;
  * the Rover is KEPT and placed at the start pose exactly as the drive scene builder does (matrix xform, z -0.00835194), no physics;
  * camera = the LE13 drive K1 rover camera: intrinsics focal 1.93 / h-aperture 3.896 (fx = fy = 317.04) and the recorded
    T_world_optical of the row's start id (prelock/start_cameras.json); the rendered pose is verified against it (< 1e-4);
  * output per capture in the drive K1 format: front_rgb.npy/.png, front_depth.npy (distance_to_image_plane), camera_metadata.json
    (calibration + raw_parameters), and evaluation-only GT under eval_gt_only/ (never passed to perception).
"""
import argparse, csv, json, sys, os, time, traceback, math, resource
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation.c_depletion_geometry_20261111_v01 import sha, usd_functions, RGB, GT
ap = argparse.ArgumentParser(); ap.add_argument('--manifest', type=Path, required=True); ap.add_argument('--rep', choices=['HR_Scan', 'LR_Scan', 'GeoCAD'], required=True)
ap.add_argument('--output', type=Path, required=True); ap.add_argument('--starts', type=Path, required=True); a = ap.parse_args()
STARTS = json.loads(a.starts.read_text())
DES = Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/C_V02_20261112_v01/data_design_v01')
ANCH = Path('/home/user/hh/isaac_cosmos/sdg_final/C_DEPLETION_REBUILD_20261111_v01/asset_anchor_audit_v01/asset_anchor_audit.json')
C = json.loads((DES / 'capture_config.json').read_text())
for p, h in C['sources_sha256'].items(): assert sha(p) == h, p
assert sha(C['background']) == C['background_sha256']
for q in C['assets'].values(): assert sha(q['path']) == q['sha256']
anchor = json.loads(ANCH.read_text()); assert anchor['state'] == 'PASS_CENTERED_ENCLOSURE_GEOMETRY'; anchor_rep = next(r for r in anchor['checks'] if r['rep'] == a.rep); assert sha(anchor_rep['path']) == anchor_rep['sha256']
rows = [r for r in csv.DictReader(a.manifest.open()) if r['rep'] == a.rep]; assert rows
BASE = '/home/user/hh/isaac_cosmos/sdg_final/PILOT_SITE_HR_ADMISSION_20261102_v30_03/prepared_site_drive.usda'
PH = C['photometric']
O = a.output; O.mkdir(parents=True, exist_ok=True); app = None; started = time.time()
def dump(n, x):
    p = O / n; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(x, indent=1, default=lambda v: v.tolist() if hasattr(v, 'tolist') else str(v)))
def event(st, **kw):
    with (O / 'events.jsonl').open('a') as f: f.write(json.dumps(dict(time=time.time(), state=st, pid=os.getpid(), **kw)) + '\n')
event('STARTED', rep=a.rep, scenes=len(rows), manifest_sha256=sha(a.manifest), code_sha256=sha(__file__))
try:
    from evaluation.b1_common_hpo_policy_20261111_v01 import gpu_gate
    g = gpu_gate((os.getpid(), os.getppid())); assert g['clear'], g
    from isaacsim import SimulationApp
    app = SimulationApp({'headless': True, 'width': 640, 'height': 480, 'renderer': 'RayTracedLighting', 'multi_gpu': False, 'extra_args': ['--/app/window/enabled=false', '--/app/livestream/enabled=false', '--/UJITSO/geometry=true', '--/omni/replicator/captureOnPlay=false', '--/exts/omni.kit.scripting.allowed=false', '--/metricsAssembler/operationMode=0']})
    import numpy as np, omni.usd, omni.timeline, omni.replicator.core as rep, carb.settings
    from PIL import Image
    from pxr import Usd, UsdGeom, UsdLux, Sdf, Gf, Semantics
    tl = omni.timeline.get_timeline_interface(); tl.stop(); ctx = omni.usd.get_context(); ctx.new_stage(); stage = ctx.get_stage(); stage.GetRootLayer().subLayerPaths = [BASE]; stage.SetEditTarget(stage.GetRootLayer()); UsdGeom.SetStageUpAxis(stage, 'Z'); UsdGeom.SetStageMetersPerUnit(stage, 1.); stage.GetRootLayer().SetPermissionToSave(False)
    root = '/World/IPRK1'; xf = UsdGeom.Xformable(UsdGeom.Xform.Define(stage, root)); tr = xf.AddTranslateOp(); rz = xf.AddRotateZOp(); scene = root + '/Scene'
    cam = UsdGeom.Camera.Define(stage, root + '/Camera'); cam.CreateFocalLengthAttr(1.9299999475479126); cam.CreateHorizontalApertureAttr(3.8959999084472656); cam.CreateVerticalApertureAttr(3.8959999084472656 * 480 / 640); cam.CreateClippingRangeAttr((.05, 1000.)); camop = UsdGeom.Xformable(cam).MakeMatrixXform()
    FX = 1.9299999475479126 / 3.8959999084472656 * 640
    disabled = []
    for path in ['/World/ENG_FE2E/Fixture', '/World/PilotStaticUnion_v24']:
        p = stage.GetPrimAtPath(path)
        if p.IsValid(): p.SetActive(False); disabled.append(path)
    for p in list(stage.Traverse()):
        if any(t in str(p.GetPath()).lower() for t in ['stage3occluder', 'occlusionpanel', 'occluderworld']): p.SetActive(False); disabled.append(str(p.GetPath()))
    rover = UsdGeom.Xformable(stage.GetPrimAtPath('/World/ENG_FE2E/Rover')); assert rover.GetPrim().IsValid()
    domes = [UsdLux.DomeLight(p) for p in stage.Traverse() if p.IsA(UsdLux.DomeLight)]; assert domes, 'NO_SITE_DOME'
    lights = [(str(p.GetPath()), p.GetTypeName()) for p in stage.Traverse() if p.HasAPI(UsdLux.LightAPI)]
    volumes = [p for p in stage.Traverse() if p.GetAttribute('omni:nurec:isNuRecVolume').IsValid() and p.GetAttribute('omni:nurec:isNuRecVolume').Get()]
    event('SITE_STAGE', disabled=disabled, lights=lights, nurec=[str(v.GetPath()) for v in volumes])
    class _NU:
        def MakeVisible(self):
            for v in volumes: UsdGeom.Imageable(v).MakeVisible()
    nu = _NU()
    sett = carb.settings.get_settings()
    ns = usd_functions(RGB, ['create_box', 'create_pallet', 'iterate_pattern', 'create_actual_brick', 'create_actual_bundle', 'create_actual_load', 'cluster_offsets'], dict(UsdGeom=UsdGeom, UsdLux=UsdLux, Gf=Gf, stage=stage, json=json, Path=Path, math=math))
    original_brick = ns['create_actual_brick']
    def centered_brick(path, local_y, asset_path):
        original_brick(path, local_y, asset_path); ref = stage.GetPrimAtPath(path + '/SideStanding/AssetRef'); refxf = UsdGeom.Xformable(ref)
        assert not refxf.GetOrderedXformOps(), 'UNEXPECTED_REFERENCED_ROOT_XFORM'; refxf.AddTranslateOp().Set(Gf.Vec3d(*anchor_rep['new_instance_translation_local']))
    ns['create_actual_brick'] = centered_brick
    cn = usd_functions(GT, ['create_box', 'apply_class_semantics', 'iterate_pattern', 'parse_retention_mask', 'create_canonical_bundle', 'create_canonical_load'], dict(UsdGeom=UsdGeom, Gf=Gf, Semantics=Semantics, stage=stage, json=json))
    product = rep.create.render_product(str(cam.GetPath()), (640, 480)); anns = {n: rep.AnnotatorRegistry.get_annotator(n) for n in ['rgb', 'instance_id_segmentation', 'distance_to_image_plane', 'camera_params']}
    for an in anns.values(): an.attach(product.path)
    def updates(n):
        for _ in range(n): assert not tl.is_playing(); app.update()
    def reset():
        updates(16); ctx.reset_renderer_accumulation(); updates(4)
        for _ in range(6): rep.orchestrator.step(rt_subframes=8, delta_time=0, pause_timeline=True); assert not tl.is_playing()
        assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024 <= 8 * 1024 ** 3, 'CPU_RSS_8_GIB_LIMIT'
    def pixels(name):
        d = anns[name].get_data(); return d['data'] if isinstance(d, dict) and 'data' in d else d
    def image(path, array): path.parent.mkdir(parents=True, exist_ok=True); Image.fromarray(array).save(path)
    def rgb(): x = np.asarray(pixels('rgb'))[:, :, :3].astype('uint8'); assert x.shape == (480, 640, 3); return x.copy()
    def masks():
        d = anns['instance_id_segmentation'].get_data(); ar = np.squeeze(np.asarray(d['data'])); mapping = d['info'].get('idToLabels', {})
        def one(needle):
            ids = [int(k) for k, v in mapping.items() if needle in str(v)]; return np.isin(ar, ids), len(ids)
        return one
    updates(70)
    for row in rows:
        sid = row['capture_id']; CO = O / sid
        if (O / 'complete' / f'{sid}.json').exists() and json.loads((O / 'complete' / f'{sid}.json').read_text()).get('state') == 'PASS_CAPTURE': continue
        rec = dict(capture_id=sid, rep=a.rep, params=dict(row), started=time.time()); event('SCENE_STARTED', capture_id=sid)
        try:
            tr.Set(Gf.Vec3d(0., 0., 0.)); rz.Set(0.); nu.MakeVisible()  # world coordinates (no ROI frame)
            stinfo = STARTS[row['start_id']]; sx, sy, syaw = stinfo['start_xy_yaw']
            rm = Gf.Matrix4d(); rm.SetRotate(Gf.Rotation(Gf.Vec3d(0, 0, 1), float(syaw))); rm.SetTranslateOnly(Gf.Vec3d(float(sx), float(sy), -.00835194)); rover.ClearXformOpOrder(); rover.MakeMatrixXform().Set(rm)
            Topt = np.array(stinfo['T_world_optical'], float); Mu = Topt.copy(); Mu[:3, :3] = Mu[:3, :3] @ np.diag([1, -1, -1])
            camop.Set(Gf.Matrix4d(*Mu.T.flatten().tolist()))
            for dm in domes: dm.CreateIntensityAttr(float(row['dome_intensity']))
            if stage.GetPrimAtPath(scene): stage.RemovePrim(scene)
            UsdGeom.Xform.Define(stage, scene); lr = scene + '/Load_01'; load = UsdGeom.Xform.Define(stage, lr); lxf = UsdGeom.Xformable(load.GetPrim())
            lxf.AddTranslateOp().Set(Gf.Vec3d(float(row['load_center_x_m']), float(row['load_center_y_m']), 0.)); lxf.AddRotateZOp().Set(float(row['load_yaw_deg'])); ns['create_pallet'](lr + '/T11_Pallet')
            created = ns['create_actual_load'](lr, row['layer_phase'], Path(C['assets']['red__' + a.rep]['path']), row['mask_by_layer_json']); assert created == int(row['retained_brick_count'])
            for _ in range(3000):
                _, fl, tf = ctx.get_stage_loading_status()
                if not (fl or tf): break
                updates(1)
            else: raise RuntimeError('STAGE_LOADING_TIMEOUT')
            reset(); tries = 0
            while not masks()('/Load_01/ActualBrickLoad/')[0].any() and tries < 5: tries += 1; updates(60); reset()
            stage.GetPrimAtPath(lr).SetActive(False); reset(); empty = rgb(); stage.GetPrimAtPath(lr).SetActive(True); reset()
            I = rgb(); dep = np.squeeze(np.asarray(pixels('distance_to_image_plane'))).astype(np.float32).copy(); assert dep.shape == (480, 640)
            get = masks(); act, n = get('/Load_01/ActualBrickLoad/'); assert n == int(row['retained_brick_count']), ('ACTUAL_INSTANCE_COUNT_MISMATCH', n); pallet = get('/T11_Pallet')[0]
            assert act.any(), 'ACTUAL_INSTANCE_MASK_EMPTY'
            image(CO / 'eval_gt_only' / 'mask_actual.png', act.astype('uint8') * 255); image(CO / 'eval_gt_only' / 'mask_pallet.png', pallet.astype('uint8') * 255)
            image(CO / 'front_rgb.png', I); np.save(CO / 'front_rgb.npy', I); np.save(CO / 'front_depth.npy', dep)
            par = {k: (np.asarray(v).tolist() if hasattr(v, 'shape') else v) for k, v in anns['camera_params'].get_data().items()}; pr = np.array(par['cameraProjection'], float).reshape(4, 4); vw = np.array(par['cameraViewTransform'], float).reshape(4, 4); T = np.linalg.inv(vw).T; T[:3, :3] = T[:3, :3] @ np.diag([1, -1, -1]); M = np.array(UsdGeom.XformCache().GetLocalToWorldTransform(cam.GetPrim())).T; M[:3, :3] = M[:3, :3] @ np.diag([1, -1, -1]); fx = pr[0, 0] * 320; fy = pr[1, 1] * 240
            assert np.max(abs(T - M)) < 1e-4 and abs(fx - fy) < .01 * fx and abs(fx - FX) < 1., ('CAMERA_REGISTRATION_FAILED', fx, fy, FX)
            assert np.max(abs(T - Topt)) < 1e-4, ('K1_CAMERA_POSE_MISMATCH', float(np.max(abs(T - Topt))))
            dump(sid + '/camera_metadata.json', dict(calibration=dict(width=640, height=480, fx=fx, fy=fy, cx=320., cy=240., depth_semantic='distance_to_image_plane', depth_unit_m=1., T_world_optical=T.tolist(), provenance=dict(camera_prim=str(cam.GetPath()), convention='optical_right_down_forward_world_m_column', source='IPR static K1 replica of drive start ' + row['start_id'])), checks=dict(renderer_optical_world_match=True, k1_pose_matches_drive_record=True, timeline_stopped=True), raw_parameters=par, depth_valid_pixels=int((np.isfinite(dep) & (dep > 0)).sum()), physics_play_calls=0))
            mat = UsdGeom.XformCache().GetLocalToWorldTransform(stage.GetPrimAtPath(lr)); tt = mat.ExtractTranslation(); axis = mat.TransformDir(Gf.Vec3d(1, 0, 0))
            gtpose = dict(center_x_m=tt[0], center_y_m=tt[1], floor_z_m=tt[2], pallet_top_z_m=tt[2] + .144, yaw_deg=math.degrees(math.atan2(axis[1], axis[0])))
            row2 = dict(row, scene_id=sid)
            stage.GetPrimAtPath(lr + '/ActualBrickLoad').SetActive(False); cn['create_canonical_load'](lr, row2); reset(); can, n2 = masks()('/Load_01/CanonicalBrickGT/'); assert n2 == int(row['retained_bundle_count']), 'CANONICAL_INSTANCE_COUNT_MISMATCH'
            image(CO / 'eval_gt_only' / 'mask_canonical.png', can.astype('uint8') * 255); stage.GetPrimAtPath(lr + '/CanonicalBrickGT').SetActive(False); stage.GetPrimAtPath(lr + '/ActualBrickLoad').SetActive(True)
            from scipy import ndimage as nd
            diff = np.abs(I.astype(np.int16) - empty.astype(np.int16)).max(2); bgm = ~nd.binary_dilation(act | pallet, iterations=15); tau = max(int(np.percentile(diff[bgm], 99.9)), 2)
            me = nd.binary_erosion(act, iterations=2); vis = float((diff[me] > tau).mean()) if me.sum() else 0.
            image(CO / 'eval_gt_only' / 'empty.png', empty)
            valid = np.isfinite(dep) & (dep > 0); ys, xs = np.nonzero(can); gray = I.astype(float) @ [.299, .587, .114]
            clip = lambda m: dict(top=bool(m[0].any()), bottom=bool(m[-1].any()), left=bool(m[:, 0].any()), right=bool(m[:, -1].any()))
            qa = dict(canonical_px=int(can.sum()), actual_px=int(act.sum()), pallet_px=int(pallet.sum()), canonical_clipped=clip(can), pallet_clipped=clip(pallet),
                      depth_valid_target_px=int((valid & act).sum()), depth_valid_target_frac=float((valid & act).sum() / max(act.sum(), 1)), lum_image=float(gray.mean()), lum_brick=float(gray[act].mean()),
                      canon_actual_iou=float((can & act).sum() / max((can | act).sum(), 1)), bbox=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
                      vis_hard_e2=vis, vis_tau=tau, vis_eroded_px=int(me.sum()))
            files = [CO / 'front_rgb.png', CO / 'front_rgb.npy', CO / 'front_depth.npy', CO / 'camera_metadata.json', CO / 'eval_gt_only' / 'mask_canonical.png', CO / 'eval_gt_only' / 'mask_actual.png']
            rec.update(state='PASS_CAPTURE', created_bricks=created, load_retries=tries, qa=qa, fx=fx, GT_eval_only=dict(target=gtpose, retention=json.loads(row['mask_by_layer_json'])), files_sha256={str(f): sha(f) for f in files}, ended=time.time())
        except Exception:
            rec.update(state='FAILED', traceback=traceback.format_exc()); dump('complete/' + sid + '.json', rec); event('SCENE_FAILED', capture_id=sid); raise
        dump('complete/' + sid + '.json', rec); event('SCENE_COMPLETED', capture_id=sid)
    dump('result.json', dict(state='PASS_CAPTURE', rep=a.rep, declared=len(rows), manifest_sha256=sha(a.manifest), code_sha256=sha(__file__), elapsed_seconds=time.time() - started, physics_play=0, robot_motion=0))
    for an in anns.values(): an.detach(product.path)
    product.destroy(); ctx.close_stage()
except BaseException:
    dump('failure.json', dict(state='FAILED', traceback=traceback.format_exc(), declared=len(rows))); event('FAILED'); raise
finally:
    if app: app.close()
