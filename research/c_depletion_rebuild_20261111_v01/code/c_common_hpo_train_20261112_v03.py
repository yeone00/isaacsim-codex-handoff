"""B1 common-HPO worker v01. Derived from audited trainer v05; unchanged FP32/AMP and failure checks.
Adds frozen v04 PhotoDegrade, only FOUR HPO parameters, B1 Val200-only selection.
No old best checkpoint warm start; no test/realval dataset is linked or read.
"""
import argparse, hashlib, json, shutil, sys, time, traceback, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluation.c_common_hpo_policy_20261111_v01 import sha,load_protocol,validate_params,BASE_RECIPE,gpu_gate
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--protocol-sha',required=True)
ap.add_argument('--candidate',type=int,required=True);ap.add_argument('--rep',choices=['HR_Scan','LR_Scan','GeoCAD'],required=True)
ap.add_argument('--seed',type=int,choices=[42,43,44],required=True);ap.add_argument('--phase',choices=['smoke','screen','full','final','baseline_control'],required=True)
ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
HP=load_protocol(a.root,a.protocol_sha)
candidates=json.loads((a.root/'candidates.json').read_text());assert sha(a.root/'candidates.json')==HP['candidates_sha256']
params=candidates[a.candidate]['params'];validate_params(params)
if a.phase in ['smoke','screen','full']:assert a.seed==42
if a.phase=='baseline_control':assert a.candidate==0 and a.seed in [43,44]
if a.phase=='final':assert json.loads((a.root/'selection_lock.json').read_text())['candidate_id']==a.candidate
RC=json.loads(BASE_RECIPE.read_text());RSHA=sha(BASE_RECIPE)
a.stop_after_epochs={'smoke':2,'screen':60}.get(a.phase)
a.smoke_epochs=None;a.compare_fp16_path=False
gate=gpu_gate(allowed_pids=(os.getpid(),os.getppid()))
assert gate['clear'],gate
O=a.output.resolve();O.mkdir(parents=True,exist_ok=False)
import torch
from ultralytics import YOLO
from ultralytics.models.yolo.segment.train import SegmentationTrainer
from ultralytics.utils.torch_utils import unwrap_model
sys.path.insert(0,str(Path(__file__).resolve().parent))
import b1_fp32_boxloss_20261108_v01 as FB
import b1_mixing_data_20261108_v01 as MD
import c_depletion_bitmap_adapter_20261112_v01 as BM
BM.BitmapFormat.__name__="Format" # original PhotoDegrade insertion locates Format by name
assert sha(BM.__file__)==RC["bitmap_adapter"]["sha256"]
D=RC['data'];P=Path(D['package']);TRANSFORMS={}
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,default=str))
input_manifest=json.loads((a.root/'train_val_inputs.json').read_text());assert sha(a.root/'train_val_inputs.json')==HP['train_val_inputs_sha256']
input_guard=input_manifest['by_rep'][a.rep]
assert all(sha(p)==h for p,h in input_guard.items()),'TRAIN_VAL_INPUT_HASH_MISMATCH'
gates=dict(package_checks=sha(P/'package_checks.json')==D['package_checks_sha256'],data_yaml=sha(P/a.rep/'data.yaml')==D['data_yaml_sha256'][a.rep],weights=sha(RC['model']['weights'])==RC['model']['sha256'],fp32_box_module=sha(Path(__file__).resolve().parent/'b1_fp32_boxloss_20261108_v01.py')==RC['amendment']['module']['scripts/b1_fp32_boxloss_20261108_v01.py'],photo_module=sha(Path(__file__).resolve().parent/'b1_mixing_data_20261108_v01.py')==next(iter(RC['custom_photometric']['module'].values())))
assert all(gates.values()),gates
# Same sorted image membership and S__ aliases as the v04 synthetic100:real0 view.
V=O/'dataset'
for split in ['train','val']:
    for kind in ['images','labels']:
        target=V/kind/split;target.mkdir(parents=True)
        for f in sorted((P/a.rep/kind/split).iterdir()):
            if f.suffix.lower() not in (['.png','.jpg','.jpeg'] if kind=='images' else ['.txt']):continue
            name=('S__'+f.name) if split=='train' else f.name
            (target/name).symlink_to(f.resolve())
    assert len(list((V/'images'/split).iterdir()))==len(list((V/'labels'/split).iterdir()))==D['split_counts'][split]
(O/'data.yaml').write_text(f"path: {V}\ntrain: images/train\nval: images/val\nnames:\n  0: brick_load\n")
status=dict(state='RUNNING',rep=a.rep,seed=a.seed,phase=a.phase,candidate_id=a.candidate,params=params,recipe=str(BASE_RECIPE),recipe_sha256=RSHA,hpo_protocol_sha256=a.protocol_sha,gates=gates,command=[sys.executable,*sys.argv],started=time.time(),torch=torch.__version__,gpu=torch.cuda.get_device_name(0),rng_policy=HP['rng_policy'],initial_weights=RC['model'],test_data_access=False,realval_access=False)
dump(O/'run_status.json',status)
audit = dict(calls=[], epochs=[], best=None, lr_iter=[], batches=[], nonfinite_forward=[], loss_compare=[])
SCALE_MIN = 2.0 ** -8
class B1Trainer(SegmentationTrainer):
    def build_dataset(self, img_path, mode='train', batch=None):
        ds = BM.dataset(self,img_path,mode,batch)
        if mode == 'train': TRANSFORMS['train'] = MD.insert_photo(ds, RC['custom_photometric']['ops'])
        else: TRANSFORMS[mode] = [type(x).__name__ for x in ds.transforms.transforms]
        return ds
    def get_validator(self):
        from copy import copy
        return BM.CBitmapValidator(self.test_loader,save_dir=self.save_dir,args=copy(self.args),_callbacks=self.callbacks)
    def _setup_train(self):
        super()._setup_train()
        if not self.resume: self.scaler = torch.amp.GradScaler('cuda', enabled=self.amp, init_scale=RC['amp_grad_scaler_init_scale'])
        self.real_updates = 0; self._consec_nf = 0
        unwrap_model(self.model).criterion = FB.SegLossFP32Box(unwrap_model(self.model), compare=a.compare_fp16_path, compare_log=audit['loss_compare'] if a.compare_fp16_path else None, probe=True)
    def preprocess_batch(self, batch):
        self._cur_files = list(batch.get('im_file', [])); return super().preprocess_batch(batch)
    def optimizer_step(self):
        st = lambda: max([float(s['step']) for s in self.optimizer.state.values()] or [0])
        b, sb = st(), self.scaler.get_scale()
        gn = torch.sqrt(sum((p.grad.detach().float() ** 2).sum() for p in self.model.parameters() if p.grad is not None)).item() / max(sb, 1e-30)
        loss_finite = bool(self.loss is not None and torch.isfinite(self.loss).all())
        super().optimizer_step()
        af = st(); self.real_updates += int(af > b); skipped = af <= b
        kind = 'STEP' if not skipped else ('NONFINITE_FORWARD' if not loss_finite else 'GRAD_OVERFLOW_SKIP')
        if not skipped and not loss_finite: kind = 'ANOMALY_STEP_WITH_NONFINITE_LOSS'
        audit['calls'].append(dict(epoch=self.epoch + 1, batch=self._bi, adamw_before=b, adamw_after=af, scale_before=sb, scale_after=self.scaler.get_scale(), skipped=skipped,
                                   kind=kind, loss_finite=loss_finite, grad_norm_unscaled=gn))
        if kind == 'NONFINITE_FORWARD':
            self._consec_nf += 1
            audit['nonfinite_forward'].append(dict(epoch=self.epoch + 1, batch=self._bi, loss_items={k: float(v) for k, v in self.loss_items.items()}, scale_before=sb,
                                                   scale_after=self.scaler.get_scale(), files=self._cur_files))
        else: self._consec_nf = 0
        if kind == 'ANOMALY_STEP_WITH_NONFINITE_LOSS': raise RuntimeError('optimizer stepped with a non-finite loss')
        if self._consec_nf >= 3: raise RuntimeError('3 consecutive non-finite forward batches')
        if self.scaler.is_enabled() and self.scaler.get_scale() < SCALE_MIN: raise RuntimeError(f'GradScaler scale {self.scaler.get_scale()} < 2^-8')
        assert all(torch.isfinite(p).all() for p in self.model.parameters()), 'nonfinite weights'
    def _handle_nan_recovery(self, epoch):  # v05: forward losses are audited per batch in optimizer_step; never reload/retry
        if self.fitness is not None and not torch.isfinite(torch.tensor(float(self.fitness))): raise RuntimeError('nonfinite validation fitness; no retry')
        return False

fp = lambda m: float(sum(p.detach().double().abs().sum().item() for p in m.parameters()))
def on_train_start(t):
    status.update(nb=len(t.train_loader), accumulate=t.accumulate, batch=t.batch_size, loader_workers=t.train_loader.num_workers,
                  train_images=len(t.train_loader.dataset), val_images=len(t.test_loader.dataset), amp=bool(t.amp), init_scale=t.scaler.get_scale(),
                  weight_fingerprint_init=fp(t.model), transforms=dict(TRANSFORMS)); dump(O / 'run_status.json', status)
def on_epoch_start(t):
    t._oom_retries = 3; torch.cuda.reset_peak_memory_stats(); t._ep_t0 = time.time(); t._bi = -1
def on_batch_start(t):
    t._bi += 1
def on_batch_end(t):  # lr actually used for this batch (warmup sets it at batch start) + per-batch loss items
    audit['lr_iter'].append([t.epoch + 1, t._bi] + [float(x['lr']) for x in t.optimizer.param_groups])
    audit['batches'].append([t.epoch + 1, t._bi] + [float(v) for v in t.loss_items.values()])
def on_epoch_end(t):
    calls = [c for c in audit['calls'] if c['epoch'] == t.epoch + 1]
    bl = [r for r in audit['batches'] if r[0] == t.epoch + 1]; fin = [r for r in bl if all(abs(x) < float('inf') and x == x for x in r[2:])]
    names = list(t.loss_items.keys())
    audit['epochs'].append(dict(epoch=t.epoch + 1, train_loss={k: float(v) for k, v in t.label_loss_items(t.tloss).items()}, optimizer_step_calls=len(calls),
                                skipped_steps=sum(c['skipped'] for c in calls), nonfinite_forward=sum(c['kind'] == 'NONFINITE_FORWARD' for c in calls),
                                grad_overflow_skips=sum(c['kind'] == 'GRAD_OVERFLOW_SKIP' for c in calls), nonfinite_batches_logged=len(bl) - len(fin),
                                train_loss_finite_batches_mean_DIAGNOSTIC_ONLY={n: (sum(r[2 + i] for r in fin) / len(fin) if fin else None) for i, n in enumerate(names)},
                                grad_norm_unscaled_max=max([c['grad_norm_unscaled'] for c in calls if c['kind'] == 'STEP'] or [0]), adamw_counter=max([c['adamw_after'] for c in calls] or [0]), real_updates=t.real_updates,
                                ema_updates=t.ema.updates, weight_fingerprint=fp(t.model), ema_fingerprint=fp(t.ema.ema), scale=t.scaler.get_scale(),
                                peak_alloc_bytes=torch.cuda.max_memory_allocated(), peak_reserved_bytes=torch.cuda.max_memory_reserved(),
                                lr={k: float(v) for k, v in t.lr.items()}, train_epoch_s=time.time() - t._ep_t0))
def on_fit_epoch_end(t):
    m = {k: float(v) for k, v in t.metrics.items()}
    open_entry = bool(audit['epochs']) and audit['epochs'][-1]['epoch'] == t.epoch + 1 and 'val' not in audit['epochs'][-1]
    if not open_entry:  # final_eval() of Ultralytics best.pt (epoch temporarily +1, after the loop); not used for selection
        audit['final_eval_ultralytics_best'] = m; dump(O / 'audit.json', audit); return
    e = audit['epochs'][-1]; assert e['epoch'] == t.epoch + 1 and 'val' not in e; e['val'] = m
    vm = t.validator.metrics; e['val_extra'] = dict(mask_map50=float(vm.seg.map50), mask_map75=float(vm.seg.map75), mask_map5095=float(vm.seg.map),
                                                    box_map50=float(vm.box.map50), box_map75=float(vm.box.map75), box_map5095=float(vm.box.map))
    e['fit_epoch_s'] = time.time() - t._ep_t0
    key = 'metrics/mAP50-95(M)'
    value = float(vm.seg.map)  # v04 B1-val selection uses unrounded MASK metric
    if audit['best'] is None or value > audit['best']['val_mask_map5095']:
        assert t.last.exists(); shutil.copy2(t.last, t.wdir / 'best_val_maskmAP5095.pt')
        audit['best'] = dict(epoch=t.epoch + 1, val_mask_map5095=value, checkpoint=str(t.wdir / 'best_val_maskmAP5095.pt'), sha256=sha(t.wdir / 'best_val_maskmAP5095.pt'))
    with (O / 'epochs.jsonl').open('a') as f: f.write(json.dumps(e, default=str) + '\n')
    dump(O / 'audit.json', audit)
    if a.stop_after_epochs is not None and t.epoch + 1 >= a.stop_after_epochs: t.stop = True  # smoke truncation; loop breaks after this callback

try:
    y = YOLO(RC['model']['weights'])
    for ev, fn in [('on_train_start', on_train_start), ('on_train_epoch_start', on_epoch_start), ('on_train_batch_start', on_batch_start), ('on_train_batch_end', on_batch_end), ('on_train_epoch_end', on_epoch_end), ('on_fit_epoch_end', on_fit_epoch_end)]:
        y.add_callback(ev, fn)
    kw = dict(RC['train_args']); kw.update(params); kw.update(seed=a.seed, data=str(O / 'data.yaml'), project=str(O), name='train', exist_ok=False)
    status['train_kwargs'] = kw; dump(O / 'run_status.json', status)
    y.train(trainer=B1Trainer, **kw)
    ne = a.stop_after_epochs or kw['epochs']; E = audit['epochs']
    assert all(sha(p) == h for p, h in input_guard.items()), 'TRAIN_VAL_INPUT_CHANGED'
    checks = dict(all_epochs_ran=len(E) == ne, every_epoch_real_update=all(e['adamw_counter'] > (E[i - 1]['adamw_counter'] if i else 0) for i, e in enumerate(E)),
                  no_runaway_amp_skips=sum(e['skipped_steps'] for e in E) <= max(5, 0.01 * sum(e['optimizer_step_calls'] for e in E)),
                  weights_changed=E[-1]['weight_fingerprint'] != status['weight_fingerprint_init'],
                  ema_updated=E[-1]['ema_updates'] == sum(e['optimizer_step_calls'] for e in E) > 0,
                  selection_from_training_epoch=audit['best'] is not None and 1 <= audit['best']['epoch'] <= ne, finite_losses=all(all(abs(v) < float('inf') for v in e['train_loss'].values()) for e in E),
                  val_metric_finite=all(abs(e['val']['metrics/mAP50-95(M)']) < float('inf') for e in E), selection_checkpoint=audit['best'] is not None,
                  no_nonfinite_forward=len(audit['nonfinite_forward']) == 0, fp32_box_dtypes=FB.probe_record().get('bbox_iou', {}).get('box1') == 'torch.float32' == FB.probe_record().get('bbox_iou', {}).get('box2'))
    st_ = 'PASS' if all(checks.values()) else ('FLAGGED_NONFINITE_FORWARD' if not checks['no_nonfinite_forward'] and all(v for k, v in checks.items() if k not in ('no_nonfinite_forward', 'finite_losses')) else 'FAIL_AUDIT')
    checks['photo_train_only'] = 'PhotoDegrade' in TRANSFORMS.get('train', []) and 'PhotoDegrade' not in TRANSFORMS.get('val', [])
    st_ = st_ if checks['photo_train_only'] else 'FAIL_AUDIT'
    status.update(state=st_, checks=checks, fp32_probe=FB.probe_record(), nonfinite_forward_total=len(audit['nonfinite_forward']),
                  grad_overflow_skips_total=sum(c['kind'] == 'GRAD_OVERFLOW_SKIP' for c in audit['calls']), best=audit['best'], amp_skipped_total=sum(e['skipped_steps'] for e in E),
                  optimizer_step_calls_total=sum(e['optimizer_step_calls'] for e in E), real_updates_total=E[-1]['real_updates'], ended=time.time())
except BaseException as ex:
    status.update(state='FAILED', error=repr(ex), traceback=traceback.format_exc(), fp32_probe=FB.probe_record(), ended=time.time()); dump(O / 'run_status.json', status); dump(O / 'audit.json', audit); raise
dump(O / 'run_status.json', status); dump(O / 'audit.json', audit)
print(json.dumps({k: status.get(k) for k in ['state', 'checks', 'best', 'nb', 'accumulate', 'loader_workers', 'amp_skipped_total', 'real_updates_total']}, indent=1, default=str))
