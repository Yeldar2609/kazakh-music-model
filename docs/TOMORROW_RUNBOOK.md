# Tomorrow's GPU runbook (RTX 5090 machines) — Mon 14 Sep 2026

Every step here is **prepared, awaiting 5090 validation** unless marked VERIFIED. Run steps in order on ONE
machine first. Only after step 6 works may a second machine run an independent job (e.g. baseline generation
there, training here). GPUs on separate machines never pool memory.

Time plan (fill in): GPU access starts __:__ ; presentation __:__ ; **hard stop for GPU work = presentation − 2 h**.
Reserve the last 90–120 min for export, playback check in the viewer, rehearsal.

Legend: `PS>` Windows PowerShell, `$` Linux bash. Paths are relative to the project folder `Kazak Music Model`.
`py -3.12` = the Windows Python launcher; if it is absent, every `py -3.12 scripts/x.py` also works as
`C:\kmm\venv-acestep\Scripts\python.exe scripts\x.py` (Windows) or `$UV_PROJECT_ENVIRONMENT/bin/python scripts/x.py` (Linux).
Prefer the venv interpreter over `uv run --project …`: the latter re-syncs into `upstream/ACE-Step-1.5/.venv` if the env var is not exported.
PowerShell 5.1 has no `&&`: run chained commands as separate lines.

**Data state:** as of Sunday night the pilot dataset exists and validates (11 crops, 7.0 min, 3 recording groups; 9 train / 2 val;
`data/processed/dataset_train.json` + `dataset_val.json` are committed). If you add recordings, re-run
`build_manifest.py → validate_dataset.py → export_dataset_json.py` (CPU) and require `RESULT: OK` before step 5.
Steps 1–4 (env + baseline) never depend on the dataset.

---

## 0. Transfer (from tonight's laptop)

Copy **two folders**, never the venv:
1. Project folder `Kazak Music Model` (code, docs, configs, `data/`, `outputs/`; `upstream/` is included — it is the pinned clone).
2. Weights folder `C:\kmm\checkpoints` (9.4 GB; `CHECKSUMS.json` inside, all five weight files verified against Hugging Face LFS sha256). It includes the unused `acestep-5Hz-lm-1.7B` folder on purpose: upstream's "main model present?" check requires it, and without it `initialize_service` starts an unpinned whole-repo download (that is exactly what happened on the laptop tonight). Keep the folder; never load the LM.

LocalSend is installed on this Desktop and works across Windows/Linux/mac. A USB drive also works.
On the destination **overwrite** the copied `.env.local` (it carries the laptop's `C:\kmm\...` paths) with that machine's paths from
`configs/paths.env.example`. On Linux use e.g. `KMM_CHECKPOINTS=/home/<you>/kmm/checkpoints`, `UV_PROJECT_ENVIRONMENT=/home/<you>/kmm/venv-acestep`.
The wrappers read `.env.local`; plain `uv run …` commands do NOT, so in every new shell also `export UV_PROJECT_ENVIRONMENT=…`
(PowerShell: `$env:UV_PROJECT_ENVIRONMENT="…"`) or uv will silently build a second venv under `upstream/ACE-Step-1.5/.venv`.

Expected: `configs/pins.json` present; `upstream/ACE-Step-1.5` at commit `ca1e85f` (`git -C upstream/ACE-Step-1.5 rev-parse HEAD`).
If `upstream/` did not transfer: run the `clone_command` from `configs/pins.json`.

## 1. Detect the machine (2 min) — do not assume OS, VRAM, admin

```
PS> nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv ; nvidia-smi | findstr "CUDA Version"
$  nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv ; nvidia-smi | grep "CUDA Version"
PS> py -3.12 --version ; uv --version ; ffmpeg -version | Select-Object -First 1 ; git --version
$  python3 --version ; uv --version ; ffmpeg -version | head -1 ; git --version
```
Expected: RTX 5090, 32 GB, driver ≥ 570 and CUDA ≥ 12.8 in the banner (Blackwell needs cu128 wheels), Python 3.11 or 3.12, uv, ffmpeg, git.
- No uv → Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`; Linux `curl -LsSf https://astral.sh/uv/install.sh | sh` (user-local, no admin).
- No Python 3.12 → `uv python install 3.12` (user-local).
- Linux without ffmpeg shared libs: torchaudio/torchcodec loading will fail in step 3; install ffmpeg via the package manager or ask the admin.
- Check free disk ≥ 25 GB (`Get-PSDrive C` / `df -h .`) and RAM (`systeminfo | findstr Memory` / `free -g`).

## 2. Environment (10–20 min, network)

```
PS> $env:UV_PROJECT_ENVIRONMENT="C:\kmm\venv-acestep"; cd upstream\ACE-Step-1.5; uv sync --python 3.12
$  export UV_PROJECT_ENVIRONMENT=/opt/kmm/venv-acestep   # or ~/kmm/venv-acestep ; cd upstream/ACE-Step-1.5 && uv sync --python 3.12
```
`uv.lock` pins torch 2.7.1+cu128 (Windows) / 2.10.0+cu128 (Linux x86_64). Both cu128 wheels carry sm_120 (Blackwell) kernels.
Expected: ends with "Installed N packages", no "error". Failure "no matching distribution torch==…+cu128" → OS/arch not covered by the lock (e.g. aarch64 uses cu130) — stop and report; do not hand-edit pins.

## 3. GPU proof (1 min) — imports alone are not enough

```
PS> uv run python ..\..\scripts\diagnose_gpu.py
$  uv run python ../../scripts/diagnose_gpu.py
```
Expected: `gpu : NVIDIA GeForce RTX 5090 … capability sm_120`, arch list contains `sm_120`, a bf16 4096² matmul ×10 in tens of ms with `finite=True`, `torchaudio.load: shape (1, 48000)`, `RESULT: OK`.
- `RESULT: FAIL … lacks kernels for sm_120` → wrong torch wheel; re-check step 2 used the project `uv.lock`.
- `torchaudio.load failed` → missing ffmpeg libraries (Linux) — fix before any preprocessing.
- `cuda.is_available() False` → driver too old or wrong device; `nvidia-smi` must show CUDA ≥ 12.8.

## 4. Baseline generation with the unchanged pretrained model (5–10 min) — SAVE BEFORE ANY TRAINING

```
PS> cd ..\.. ; py -3.12 scripts\generate_cases.py --dry-run
PS> C:\kmm\venv-acestep\Scripts\python.exe scripts\generate_cases.py --cases configs\eval_cases.json --out outputs\baseline --checkpoints C:\kmm\checkpoints
$  cd ../.. ; "$UV_PROJECT_ENVIRONMENT/bin/python" scripts/generate_cases.py --cases configs/eval_cases.json --out outputs/baseline --checkpoints /path/to/checkpoints
```
(`--dry-run` prints the resolved cases without importing torch.) 3 cases × 3 seeds × 30 s, turbo 8 steps shift 3.0, LM disabled, quantization off. The script refuses to start if any of the three required component folders lacks weights, and it neutralises upstream's auto-download check so nothing is fetched from the network. A one-time log line "Model code mismatch detected … Auto-syncing" is benign (engine `.py` files copied into the checkpoint dir). Details: `docs/MODEL_INTERFACE.md`.
Expected: `outputs/baseline/<case>/<case>_seed<seed>.wav` + `.json` sidecar for all 9; first load ~1–2 min, then seconds per clip.
Listen to one of each case immediately (any player). A_dombra_solo must be instrumental; B/C must contain vocals.
- CUDA OOM (should not happen on 32 GB) → add `--offload-to-cpu`.
- Silence / NaN audio → record it, keep the file (failed outputs are evidence), try another seed; do not delete.

**Checkpoint reached: outcome 2 (pretrained generation) is now demonstrable from saved audio.** Run `py -3.12 scripts/build_viewer_manifest.py` and open `viewer/index.html`.

## 5. Dataset preprocessing (GPU, 5–15 min for ≤40 clips)

Prerequisites (CPU, done tonight or now): `crop_plan.csv` filled → `build_manifest.py` → `validate_dataset.py` prints `RESULT: OK` → `export_dataset_json.py` wrote `data/processed/dataset_train.json` and `dataset_val.json`.

```
PS> scripts\preprocess_dataset.cmd data\processed\dataset_train.json C:\kmm\work\tensors_train
$  scripts/preprocess_dataset.sh data/processed/dataset_train.json /path/kmm/work/tensors_train
```
(wrapper = `uv run python -m acestep.training_v2.cli.train_fixed --plain --checkpoint-dir <ckpt> --model-variant turbo --preprocess --dataset-json … --tensor-output …` run inside `upstream/ACE-Step-1.5`. The module entry is deliberate: `train.py fixed --preprocess` rejects the call because `--dataset-dir/--output-dir` are required there. See `docs/MODEL_INTERFACE.md`.)
Expected: two passes logged (VAE+text encoder, then DiT encoder), one `.pt` per sample in the tensor dir, count = number of samples. Do the same for `dataset_val.json` → `tensors_val` (used only for listening, never trained on).
- "Audio file from JSON not found" → `audio_path` is relative to the JSON's folder (`data/processed`); rerun export.
- OOM in pass 2 → `--max-duration 60` (our crops are ≤ 40 s anyway).

## 6. One real optimizer step, then a bounded pilot (measure first)

Smoke run, 1 epoch, saves every epoch:
```
PS> scripts\train_adapter.cmd C:\kmm\work\tensors_train outputs\training\smoke 1
$  scripts/train_adapter.sh /path/kmm/work/tensors_train outputs/training/smoke 1
```
(wrapper = `uv run python train.py --yes --plain fixed --checkpoint-dir … --model-variant turbo --dataset-dir … --output-dir … --epochs N --save-every 1 --batch-size 1 --gradient-accumulation 4 --lr 1e-4 --rank 64 --alpha 128 --adapter-type lora --shift 3.0 --num-inference-steps 8`; `--yes --plain` must come BEFORE `fixed`, the wrapper does this.)
Expected in the log: dataset size, then `Loss`/`Step`/`Epoch` lines with finite loss values (not `nan`/`inf`; step-level loss prints every 10 optimizer steps, so a 1-epoch smoke with few clips may show only the epoch line), then `outputs/training/smoke/final/adapter_config.json` + `adapter_model.safetensors`, and `checkpoints/epoch_1_loss_0.XXXX/` (the trainer appends the loss to the folder name) with `training_state.pt`. Gradient norms are logged to TensorBoard only (`runs/`), not the console. Note: the smoke run's ~8 optimizer steps sit inside the default 100-step LR warm-up, so its loss is not comparable to the pilot.
Measure disk: `du -sh outputs/training/smoke/checkpoints/*` — each epoch dir is roughly 0.5 GB (adapter + optimizer state). Note **step time** and **peak VRAM** (`nvidia-smi` in a second terminal, or the TensorBoard `runs/`).
Validate the artefact: `py -3.12 scripts/check_adapter.py outputs/training/smoke/final` → prints tensor count/shapes, exit 0.

Pilot budget: optimizer steps per epoch = ceil(N_samples / 4). Choose epochs so that (epochs × steps/epoch × measured step time) ≤ 45 min, leaving time for adapter generation. Start there, e.g. with 30 clips at ~1 s/step: 200 epochs ≈ 8 steps × 200 × 1 s ≈ 27 min. Do **not** copy the tutorial's 500–800 epochs blindly.
Checkpoint budget: epochs ÷ save-every × 0.5 GB must fit the disk; write the pilot under `KMM_WORK` (outside OneDrive) and copy only `final/` back into `outputs/training/`.
```
PS> scripts\train_adapter.cmd C:\kmm\work\tensors_train C:\kmm\work\pilot 200 --save-every 25
PS> Copy-Item -Recurse C:\kmm\work\pilot\final outputs\training\pilot\final
```
Resume after interruption: add `--resume-from C:\kmm\work\pilot\checkpoints\epoch_N_loss_X.XXXX` (tab-complete the real name; full resume: adapter + optimizer + scheduler state). Validation tensors are not consumed by the trainer; `dataset_val.json` exists so the held-out recording is never trained on and can be listened to against the adapter.
Windows note: DataLoader workers are forced to 0 (upstream behaviour) — expected, not an error.

## 7. Adapter reload + matched comparison (5–10 min)

```
PS> py -3.12 scripts\check_adapter.py outputs\training\pilot\final
PS> C:\kmm\venv-acestep\Scripts\python.exe scripts\generate_cases.py --cases configs\eval_cases.json --out outputs\adapter --checkpoints C:\kmm\checkpoints --adapter outputs\training\pilot\final --adapter-scale 1.0
```
Same cases, seeds, duration, steps, shift as step 4; only the adapter differs. Expected: `✅` load message in the log, 9 WAVs + sidecars with `adapter: {path, scale, …}` and upstream's own `lora_loaded/use_lora` flags. A second pass at another strength (`--adapter-scale 0.5`) must go to `outputs/adapter` with a different case set or be documented by hand: the viewer only reads `outputs/baseline`, `outputs/adapter`, `outputs/human_reference`.
- "LoRA loading is not supported when quantization is active" → the script initialises with `quantization=None`; if you changed that, revert.
- "expected PEFT LoRA directory containing adapter_config.json" → point at `…/final` or `…/checkpoints/epoch_N`, not at a file.

Intermediate checkpoints are inference-ready too: compare `epoch_50` vs `final` if time allows.

## 8. Listening + demo build (last 90–120 min, no GPU needed)

```
PS> py -3.12 scripts\build_viewer_manifest.py ; start viewer\index.html
```
Human review with a Kazakh speaker: dombra likeness, recognisable words + pronunciation, lyric adherence, coherence/artifacts, adapter helps/harms. Write notes in the viewer, export JSON, save into `outputs/listening_notes.json`.
Update `PROJECT_STATUS.md` (which of the 4 outcomes were reached) and `HANDOFF_TO_CHATGPT.md`.

## Recovery cheat-sheet

| Symptom | Likely cause | Action |
|---|---|---|
| `fatal: permission denied` on clone | SSH key / protected folder | use the HTTPS URL from `configs/pins.json`, clone into a user-writable folder |
| `python` prints 3.8 / opens Store (Windows) | Store stub on PATH | use `py -3.12` or `uv run python` |
| Kazakh letters show as `?` or `\u04d9` | non-UTF-8 default | `PYTHONUTF8=1` (wrappers set it), never `ensure_ascii=True` |
| Long-path errors (Windows, no admin) | MAX_PATH | keep work dirs short (`C:\kmm\work`), not inside deep OneDrive paths |
| Training "completes" with 0 steps | tensor dir empty / wrong path | `ls` the tensor dir; rerun preprocessing |
| Adapter output identical to baseline | `set_use_lora` not applied or scale 0 | check the `✅` load line and sidecar `adapter` field |
