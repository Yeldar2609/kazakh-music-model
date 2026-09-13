# Kazakh Music Model — ACE-Step-based prototype

A small, reproducible experiment: can a pretrained music model (ACE-Step 1.5, 2B `acestep-v15-turbo`) produce
(a) a dombra instrumental and (b) a short Kazakh vocal passage with dombra accompaniment, and does a tiny LoRA
adapter trained on licensed Kazakh recordings change the result? Built by a beginner in music ML as
independent preparation for a research collaboration; nothing here is a claim of a trained Kazakh music model.

**Four outcomes, reported separately** (see `docs/DECISIONS.md`): infrastructure+data prepared · pretrained
generation works · adapter trained and reloaded · human-reviewed improvement. Current state: `PROJECT_STATUS.md`.

## Pinned foundation
- Engine: `ace-step/ACE-Step-1.5` @ `ca1e85fe…` (2026-08-29), MIT. Weights: HF `ACE-Step/Ace-Step1.5` @ `19671f40…`
  (turbo DiT 4.6 GB + VAE 0.3 GB + Qwen3-Embedding-0.6B 1.1 GB, plus the 3.7 GB planning LM folder which is present
  on disk because upstream's init requires it but is never loaded). `configs/pins.json`, `configs/checkpoint_checksums.json`.
- Kazakh is **not** a supported language code → all Kazakh samples/cases use `language: "unknown"`; lyrics stay Cyrillic.
- Reference: `pymaster17/VocalRender` (score-native singing synthesis) is documented, not used.

## Setup
Requirements: Python 3.11/3.12, `uv`, `ffmpeg`, `git`, NVIDIA GPU with driver ≥ 570 for generation/training (CPU is enough for data prep).
```
git clone https://github.com/ace-step/ACE-Step-1.5.git upstream/ACE-Step-1.5
git -C upstream/ACE-Step-1.5 checkout ca1e85fe9430179831e6bc6be790c332190a3866
cp configs/paths.env.example .env.local      # set KMM_CHECKPOINTS, UV_PROJECT_ENVIRONMENT, KMM_WORK (outside OneDrive)
cd upstream/ACE-Step-1.5 && uv sync --python 3.12
uv run python ../../scripts/diagnose_gpu.py  # real bf16 matmul + torchaudio load; RESULT: OK required
```
Weights: copy the verified `checkpoints` folder (9.4 GB, `CHECKSUMS.json` inside). Fresh download: `uv run --with huggingface_hub[hf_xet] scripts/download_checkpoints.py <dest>`
fetches the pinned revision, including the unused LM folder that upstream's init insists on (else it auto-downloads the
whole repo unpinned — see `docs/TOMORROW_RUNBOOK.md` step 0), and writes `CHECKSUMS.json`.

## Verified tonight (CPU laptop, RTX 3050 Ti 4 GB)
- Upstream docs/source read; language handling, trainer flags, adapter reload path confirmed in code.
- Weights downloaded, sha256 verified against Hugging Face LFS.
- `scripts/validate_dataset.py --selftest` (Kazakh letters round-trip), a synthetic end-to-end run (leakage + duplicate
  detection fired as designed), and the real pilot dataset: 11 crops, 7.0 min, 3 independent recording groups
  (`data/manifests/manifest.json`, sources and licenses in `docs/DATA_SOURCES.md`).
- One 10 s pretrained generation on the laptop (INT8, CPU offload): `outputs/baseline_laptop_smoke/` — evidence the
  engine runs, not the demo baseline.
- GPU-dependent steps are **prepared, awaiting 5090 validation** — see `docs/TOMORROW_RUNBOOK.md`.

## Data workflow (CPU)
1. Put originals in `data/raw/<source>/` with `SOURCE.json` (url, performer, license + evidence URL, group_id). Untouched forever.
2. Plan crops in `data/manifests/crop_plan.csv` (30–40 s each; vocal crops need a lyrics file containing only the words sung in that crop; split by recording).
3. `py -3.12 scripts/build_manifest.py` → 48 kHz PCM crops in `data/processed/` + `data/manifests/manifest.json/.csv`.
4. `py -3.12 scripts/validate_dataset.py` → must print `RESULT: OK` (decodability, silence, clipping, duration, duplicates, lyrics, Kazakh letters, split leakage, licenses).
5. `py -3.12 scripts/export_dataset_json.py` → `data/processed/dataset_train.json`, `dataset_val.json` (ACE-Step/Side-Step format).

## Generation, training, demo
`docs/TOMORROW_RUNBOOK.md` (ordered GPU workflow with expected outputs and recovery) and `docs/MODEL_INTERFACE.md`
(what each script does). Demo: `viewer/index.html` plays saved WAVs only, labelled prerecorded, with honest empty states.

## Limitations (honest)
- Dataset is tiny and license-constrained; crops from one recording are not independent sources.
- No Kazakh language conditioning exists in the model; intelligible Kazakh singing is a target, not an expectation.
- Turbo has no classifier-free guidance and "Medium" fine-tunability; `sft` is the documented next candidate.
- Evaluation is human listening on a handful of matched pairs; training loss is not a quality metric.

Not committed: audio, weights, tensors, outputs, venvs, `upstream/` (all reproducible from pins).
