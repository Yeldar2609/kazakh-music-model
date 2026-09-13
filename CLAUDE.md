# Kazakh Music Model (ACE-Step-based prototype)

Small, honest research prototype: generate dombra instrumentals and Kazakh vocal passages with the pretrained
ACE-Step 1.5 `acestep-v15-turbo` model, then train and compare a LoRA adapter on a tiny licensed dataset.
Owner is a beginner in music ML: explain what/why/command/success for each stage. Presentation: Mon 14 Sep 2026 pm.

## Ground rules
- Engine + weights are pinned in `configs/pins.json`. Never switch model variant (no XL, no sft) without a written decision in `docs/DECISIONS.md`.
- Kazakh has no ACE-Step language code: use `language: "unknown"`. Never relabel as `ru`/`az`, never translate lyrics, never transliterate. Keep UTF-8 (`PYTHONUTF8=1`, `encoding="utf-8"`, `ensure_ascii=False`).
- Four outcomes are reported separately: (1) infra+data prepared, (2) pretrained generation works, (3) adapter trained+reloaded, (4) human-reviewed improvement. Never describe pretrained output as "ours"; loss going down is not musical proof.
- No training data without license evidence in `data/raw/<source>/SOURCE.json`. Vocal crops carry only the words sung inside the crop. Split by original recording (`group_id`), never by crop.
- Never substitute unrelated audio, TTS, or dummy files for generated results. The viewer shows honest empty states.
- Do not publish, upload recordings, purchase services, or contact researchers.

## Layout
- `upstream/ACE-Step-1.5` — pinned clone (read-only; gitignored). `upstream/VocalRender` — reference only.
- `scripts/` — diagnostics, manifest/validate/export, generation, training wrappers, viewer manifest.
- `configs/` — pins, eval cases, paths template. `.env.local` holds machine paths (gitignored).
- `data/raw` (originals, untouched) → `data/processed` (48 kHz crops + dataset JSON) ; `data/manifests`, `data/lyrics` are versioned.
- `outputs/baseline`, `outputs/adapter`, `outputs/training` — saved audio + JSON sidecars. `viewer/` — offline demo page.
- Heavy, machine-local: weights `KMM_CHECKPOINTS`, venv `UV_PROJECT_ENVIRONMENT`, tensors `KMM_WORK` (see `configs/paths.env.example`).

## Commands (Windows: `py -3.12`; bare `python` is a broken Store stub. Linux: `python3`)
- Env: `cd upstream/ACE-Step-1.5 && uv sync` (with `UV_PROJECT_ENVIRONMENT` set). GPU proof: `uv run python ../../scripts/diagnose_gpu.py`.
- Data: edit `data/manifests/crop_plan.csv` → `py -3.12 scripts/build_manifest.py` → `py -3.12 scripts/validate_dataset.py` → `py -3.12 scripts/export_dataset_json.py`.
- Generation / training / viewer: see `docs/TOMORROW_RUNBOOK.md` and `docs/MODEL_INTERFACE.md`.

## Status
Read `PROJECT_STATUS.md` first; update it at the end of every session.
