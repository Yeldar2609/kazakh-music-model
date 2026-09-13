# Model interface (ACE-Step 1.5 turbo, Kazakh prototype)

Status: every GPU step below is **prepared, awaiting 5090 validation**. Nothing here has run
against the model yet; only `--dry-run`, `check_adapter.py`, argparse and shell-wrapper checks
have executed on the 4 GB laptop. Engine pin: `upstream/ACE-Step-1.5` @ `ca1e85fe` (see
`configs/pins.json`); checkpoint pin: HF `ACE-Step/Ace-Step1.5` @ `19671f40`, components
`acestep-v15-turbo`, `vae`, `Qwen3-Embedding-0.6B` only (the 5Hz planning LM is deliberately absent).

## Environment

| Item | Value |
| --- | --- |
| `.env.local` | `KEY=VALUE` lines, `#` comments, no quoting. Read by every wrapper and by `generate_cases.py`; a variable already set in the shell wins. Template: `configs/paths.env.example`. |
| `KMM_CHECKPOINTS` | Checkpoints root (default `./checkpoints`). Must contain the three component folders with weights. |
| `UV_PROJECT_ENVIRONMENT` | uv reads this from the environment and uses that venv instead of `upstream/ACE-Step-1.5/.venv`; that is how `C:\kmm\venv-acestep` is selected. |
| `KMM_WORK` | Optional. Tensors / training outputs live here; `generate_cases.py` also points `ACESTEP_PROJECT_ROOT` at it so the handler's `.cache/` lands outside this repo. |
| `PYTHONUTF8=1` | Set by all wrappers. `generate_cases.py` also reconfigures stdout/stderr to UTF-8 itself. |

Interpreter rules:

- `py -3.12` (global) has **no torch / safetensors**. It can run `generate_cases.py --dry-run`
  and `check_adapter.py` only.
- Everything that touches the model runs inside the uv env:
  `C:\kmm\venv-acestep\Scripts\python.exe scripts\generate_cases.py ...` or
  `uv run --project upstream/ACE-Step-1.5 python scripts/generate_cases.py ...`.
- Bare `python` on this box is the broken Store 3.8 stub; never use it.

## 1. `scripts/generate_cases.py` — fixed evaluation cases (prepared, awaiting 5090 validation)

Runs `configs/eval_cases.json` (3 cases x 3 seeds = 9 clips at 30 s, 8 steps, shift 3.0,
guidance 1.0, `vocal_language="unknown"`). Baseline and adapter runs are the same command; only
`--adapter` differs, so outputs are directly comparable per `(case, seed)`.

```
# resolved parameters only, no torch (works with py -3.12)
py -3.12 scripts\generate_cases.py --dry-run
py -3.12 scripts\generate_cases.py --dry-run --case-id B_verse_simple --seeds 1001

# baseline (uv env interpreter)
C:\kmm\venv-acestep\Scripts\python.exe scripts\generate_cases.py --cases configs\eval_cases.json --out outputs\baseline

# adapter
C:\kmm\venv-acestep\Scripts\python.exe scripts\generate_cases.py --cases configs\eval_cases.json --out outputs\adapter ^
    --adapter C:\kmm\work\lora1\final --adapter-scale 1.0

# low-VRAM variant / single case / seed override
... --offload-to-cpu --case-id A_dombra_solo --seeds 1001
```

Flags: `--cases`, `--out`, `--adapter <dir with adapter_config.json>`, `--adapter-scale` (upstream
clamps to `[0, 1]`; the sidecar records both requested and effective), `--checkpoints`
(default `KMM_CHECKPOINTS`, else `./checkpoints`), `--device auto|cuda|cpu`, `--offload-to-cpu`,
`--case-id`, `--seeds`, `--dry-run`.

What it does, in order:

1. Loads `.env.local`, resolves every job (per-case `seeds`/`duration`/`steps`/`shift` override the
   file-level defaults; `--seeds` overrides both). Lyrics files are read as UTF-8.
2. Refuses to start unless `acestep-v15-turbo`, `vae`, `Qwen3-Embedding-0.6B` each contain a
   weights file. **Upstream would otherwise auto-download the whole HF repo, unpinned**, because
   its "main model present" check also demands `acestep-5Hz-lm-1.7B`
   (`acestep/model_downloader.py:307-312`, `check_main_model_exists` :386-400). To stop that, the
   script replaces the module-level `check_main_model_exists` that
   `acestep/core/generation/handler/init_service_downloads.py:31` calls with a function that
   returns `True`. It prints `LM presence check neutralised` when it does. No stub LM directory is
   created on disk.
3. Sets `ACESTEP_CHECKPOINTS_DIR` (read first by `init_service_orchestrator.py:122-124`), then
   `AceStepHandler().initialize_service(project_root=<upstream>, config_path="acestep-v15-turbo",
   device, compile_model=False, offload_to_cpu, offload_dit_to_cpu=False, quantization=None)` and
   asserts `handler.is_turbo_model()`.
4. If `--adapter`: `load_lora(dir)` -> `set_use_lora(True)` -> `set_lora_scale(scale)`. Each returns
   a string; anything not starting with the check mark aborts the run.
5. Per job: `GenerationParams(task_type="text2music", caption, lyrics, instrumental, vocal_language,
   bpm, keyscale, timesignature, duration, inference_steps, shift, guidance_scale, seed,
   thinking=False, use_cot_metas/caption/language=False)` and
   `GenerationConfig(batch_size=1, use_random_seed=False, seeds=[seed], audio_format="wav")`, then
   `generate_music(handler, None, params, config, save_dir=out)`. The engine writes `<uuid>.wav`;
   the script renames it to `<case_id>__seed<seed>.wav` and writes `<same>.json`.

Expected output per job:

```
outputs/baseline/A_dombra_solo__seed1001.wav
outputs/baseline/A_dombra_solo__seed1001.json
```

Sidecar fields: `case_id, kind, output_wav, caption, lyrics, lyrics_file, instrumental,
vocal_language, bpm, keyscale, timesignature, seed, seed_used, duration, inference_steps, shift,
guidance_scale, model_variant, config_path, engine_commit, checkpoint_revision, checkpoints_dir,
adapter {path, scale_requested, scale_effective, weights_hash} | null, device, dtype,
offload_to_cpu, wall_time_sec, cuda_max_memory_allocated_bytes, time_costs, sample_rate,
generated_at`. Written with `ensure_ascii=False`.

Expected log lines on first init (not errors): `Model code mismatch detected ... Auto-syncing from
acestep/models/` — the engine copies its own `modeling_acestep_v15_turbo.py` /
`configuration_acestep_v15.py` into the checkpoint folder when they differ from the pinned
snapshot (`init_service_downloads.py:65-76`). `CHECKSUMS.json` from the download script records
`sha256: null` for `.py` files, so it will not flag this.

Notes:
- `params.instrumental` is a field but is **not** forwarded to the DiT (`inference.py` builds
  `dit_generate_kwargs` at ~843-905 without it; only the LM helpers read it). The operative
  instrumental signal for case A is the `[Instrumental]` lyrics text.
- With `llm_handler=None`, `use_lm` is false at `inference.py:655`; caption/lyrics reach the DiT
  unchanged. No LM weights are needed or touched.
- Exit code is non-zero if any job fails; the other jobs still run.

## 2. `scripts/preprocess_dataset.{cmd,sh}` — audio -> training tensors (prepared, awaiting 5090 validation)

```
scripts\preprocess_dataset.cmd  data\processed\dataset_train.json  C:\kmm\work\tensors            [extra args]
bash scripts/preprocess_dataset.sh data/processed/dataset_train.json /c/kmm/work/tensors        [extra args]
```

Runs, from inside `upstream/ACE-Step-1.5`:

```
uv run python -m acestep.training_v2.cli.train_fixed --plain --checkpoint-dir %KMM_CHECKPOINTS% ^
    --model-variant turbo --preprocess --dataset-json <json> --tensor-output <dir> --max-duration 240 [extra]
```

Why the module form and not `train.py fixed --preprocess`: the root parser marks `--dataset-dir`
and `--output-dir` `required=True` for the `fixed` subcommand (`training_v2/cli/args.py:221-237,
305`), so `train.py fixed --preprocess ...` dies with
`error: the following arguments are required: --dataset-dir, --output-dir` (reproduced locally).
The standalone parser (`args.py:29-66`, `require_training_paths=False`) accepts it and
`train_fixed.main()` (`train_fixed.py:213-216`) routes `--preprocess` to the same
`preprocess_audio_files` before checking those paths.

Dataset JSON: full ACE-Step format (`docs/sidestep/Dataset Preparation.md` in upstream) —
`{"metadata": {...}, "samples": [{"audio_path", "filename", "caption", "lyrics",
"is_instrumental", "language": "unknown", ...}]}`. `audio_path` is resolved relative to the JSON
file's directory (`training_v2/preprocess_discovery.py:48-55`). Missing files are skipped with a
warning, not an error — check the `Resolved N audio files from dataset JSON` line against your
sample count. `language` is passed through as metadata only. Two passes (VAE + text encoder, then
DiT encoder) with sequential loading; output is one `.pt` per clip in `<tensor dir>`.

Expected tail:

```
[OK] Preprocessing complete:
     Processed: N/N
     Output:    C:\kmm\work\tensors
```

## 3. `scripts/train_adapter.{cmd,sh}` — LoRA training (prepared, awaiting 5090 validation)

```
scripts\train_adapter.cmd  C:\kmm\work\tensors  C:\kmm\work\lora1  3  [extra args]
bash scripts/train_adapter.sh /c/kmm/work/tensors /c/kmm/work/lora1 3 [extra args]
```

Runs, from inside `upstream/ACE-Step-1.5`:

```
uv run python train.py --yes --plain fixed --checkpoint-dir %KMM_CHECKPOINTS% --model-variant turbo ^
    --dataset-dir <tensors> --output-dir <out> --epochs N --save-every 1 ^
    --batch-size 1 --gradient-accumulation 4 --lr 1e-4 --adapter-type lora --rank 64 --alpha 128 ^
    --shift 3.0 --num-inference-steps 8 [extra]
```

`--yes --plain` are root-parser flags (`args.py:85-97`) and must precede `fixed`; putting them
after the subcommand gives `error: unrecognized arguments: --yes --plain` (reproduced locally).
Extra args are appended last, so they override the defaults (argparse last-wins). Useful extras,
all verified in `args.py`: `--optimizer-type adamw8bit` (:275), `--offload-encoder` (:278),
`--resume-from <out>\checkpoints\epoch_K_loss_X.XXXX` (:307), `--rank 16` (:286), `--warmup-steps` (:269),
`--no-gradient-checkpointing` (:277, on by default), `--num-workers` (:238, forced to 0 on Windows).

Output layout, verified in code (the upstream docs say `epoch_K`; the trainer actually appends the
epoch loss — `trainer_fixed.py:516, 553`, `trainer_helpers.py:148-180, 195-211, 237`):

```
<out>/final/adapter_config.json, adapter_model.safetensors          <- point --adapter here
<out>/checkpoints/epoch_K_loss_0.1234/  (same two files + training_state.pt)
                                        <- also loadable with --adapter, or --resume-from
<out>/runs/                             (TensorBoard)
upstream/ACE-Step-1.5/sidestep.log      (DEBUG log, appended)
```

So a resume looks like `--resume-from C:\kmm\work\lora1\checkpoints\epoch_3_loss_0.2107`; tab-complete
the real name, or pass the `training_state.pt` inside it (Side-Step uses the parent dir).

## 4. `scripts/check_adapter.py` — offline adapter validation

```
py -3.12 scripts\check_adapter.py C:\kmm\work\lora1\final
```

Mirrors what `load_lora` needs (`lora/lifecycle.py:14` requires only `peft_type`; :216-224 checks
`adapter_config.json` exists and validates it; :269 needs `adapter_model.safetensors`). Lists every
tensor name/shape/dtype and the total parameter count via `safetensors.safe_open(framework="np")`
when available, else by parsing the 8-byte length + JSON header (no dependencies). Warns on missing
`r`/`lora_alpha`/`target_modules`, `lora_A`/`lora_B` count mismatch, or `lora_A` dim0 != `r`.
Exit 0 valid, 1 invalid, 2 usage. Tested on synthetic fixtures: valid -> 0, no `peft_type` -> 1,
no weights -> 1 — all through the header-parse path, since `py -3.12` has no safetensors. Expect
header-parse on real adapters too: training precision `auto` gives bf16 on Ampere+, and
`framework="np"` cannot represent bf16, so the numpy path raises and the script falls back
(the fallback line names the exception class so a corrupt file is distinguishable from a dtype
fallback).

## Common failures

| Symptom | Cause / fix |
| --- | --- |
| `Missing checkpoint weights (run the pinned download first ...)` | `KMM_CHECKPOINTS` wrong or download incomplete. Fix the path; do not let upstream download. |
| `Main model not found. Starting automatic download...` | The LM guard did not engage (script modified?). Kill it immediately: this is an unpinned whole-repo download into the pinned dir. |
| `LoRA loading is not supported on quantized models` | `initialize_service` was called with `quantization` set. `generate_cases.py` always passes `None`. |
| `Invalid adapter: expected PEFT LoRA directory containing adapter_config.json` | `--adapter` points at `<out>` instead of `<out>/final` or `<out>/checkpoints/epoch_K_loss_X.XXXX`. Run `check_adapter.py` first. |
| `.cmd` wrapper drops `!` from a pass-through argument | The `.cmd` files use delayed expansion to collect extra args. Use the `.sh` wrapper (Git Bash) for arguments containing `!`. |
| `adapter_config.json is missing required field 'peft_type'` | Not a PEFT export (LoKR produces `lokr_weights.safetensors`, no config). Train with `--adapter-type lora`. |
| Degraded / noisy output with a correctly trained adapter | Wrong turbo settings. Turbo = 8 steps, shift 3.0; base/sft = 50 steps, shift 1.0. `generate_cases.py` refuses non-turbo checkpoints; `--shift 3.0 --num-inference-steps 8` are also passed at training time as metadata. |
| `guidance_scale ... -> 1.0 (turbo does not use CFG)` in the log | Informational: turbo forces CFG off (`generate_music.py:312-318`). |
| `CUDA out of memory` during generation | Re-run with `--offload-to-cpu`; VAE decode of 30 s clips is the peak. Check `cuda_max_memory_allocated_bytes` in the sidecars of the clips that did finish. |
| `CUDA out of memory` during training | Add `--optimizer-type adamw8bit --offload-encoder`, then `--rank 16`. Batch is already 1. |
| Training hangs / crashes in DataLoader on Windows | `num_workers` must be 0 on Windows (spawn multiprocessing); Side-Step forces it (`args.py:15`, `docs/sidestep/Windows Notes.md`). Do not pass `--num-workers N`. |
| `train.py fixed: error: the following arguments are required: --dataset-dir, --output-dir` | You called `train.py fixed --preprocess`. Use the wrapper (module entry point). |
| `train.py: error: unrecognized arguments: --yes --plain` | Flags placed after `fixed`. Put them before the subcommand (the wrapper does). |
| `Resolved N audio files` smaller than the sample count | `audio_path` did not resolve relative to the JSON's directory; missing files are skipped silently. |
| `[FAIL] Model directory not found: ...\acestep-v15-turbo` | `--checkpoint-dir` must be the root containing `acestep-v15-turbo/`, not that folder itself. |
| `uv` creates a new `.venv` under `upstream/` | `UV_PROJECT_ENVIRONMENT` not exported; put it in `.env.local` (wrappers export it). |
| Cyrillic garbled in logs / sidecars | Run through the wrappers (`PYTHONUTF8=1`) or the script (which reconfigures stdio). Sidecars are always UTF-8 with `ensure_ascii=False`. |
| Mojibake when piping `--dry-run` output into another process | The *consumer's* stdin decoding; the JSON on disk / direct stdout is correct UTF-8. |

## Upstream symbols relied on (all in `upstream/ACE-Step-1.5`, commit `ca1e85fe`)

| Symbol | Location |
| --- | --- |
| `AceStepHandler()` and LoRA state attrs `lora_loaded / use_lora / lora_scale` | `acestep/handler.py:62, 157-159` |
| `initialize_service(project_root, config_path, device, use_flash_attention, compile_model, offload_to_cpu, offload_dit_to_cpu, quantization, prefer_source, use_mlx_dit, vae_checkpoint) -> (str, bool)` | `acestep/core/generation/handler/init_service_orchestrator.py:48-61`; checkpoint dir resolution :122-128 |
| `get_checkpoints_dir` / `ACESTEP_CHECKPOINTS_DIR` | `acestep/model_downloader.py:344-360` |
| `MAIN_MODEL_COMPONENTS` (includes the LM) / `check_main_model_exists` / `_contains_model_weights` | `acestep/model_downloader.py:307-312, 386-400, 362-384` |
| `_ensure_models_present` (auto-download trigger) / `_sync_model_code_if_needed` | `acestep/core/generation/handler/init_service_downloads.py:22-62, 65-76`; name-imports at :8-16 |
| `is_turbo_model()` | `acestep/core/generation/handler/init_service_catalog.py:75-79` |
| `_resolve_initialize_device("auto")` | `acestep/core/generation/handler/init_service_setup.py:14-24` |
| `GenerationParams` fields used (`caption, lyrics, instrumental, vocal_language, bpm, keyscale, timesignature, duration, inference_steps, seed, guidance_scale, shift, task_type, thinking, use_cot_metas, use_cot_caption, use_cot_language`) | `acestep/inference.py:111-151, 203-212` |
| `GenerationConfig(batch_size, use_random_seed, seeds, audio_format)` | `acestep/inference.py:236-262` |
| `generate_music(dit_handler, llm_handler, params, config, save_dir, progress) -> GenerationResult` | `acestep/inference.py:514-520`; LM gate :655; seed handling :590-613; save path / `audios[i]["path"]` :1047-1060 |
| `GenerationResult(audios, status_message, extra_outputs, success, error)` | `acestep/inference.py:278-298` |
| turbo forces `guidance_scale=1.0` | `acestep/core/generation/handler/generate_music.py:312-318` |
| `prepare_seeds` (fixed seed when `use_random_seed=False`) | `acestep/core/generation/handler/task_utils.py:19-59` |
| `load_lora` / `add_lora` (quantization refusal :200-205, config check :216-224, `PeftModel.from_pretrained` :269) | `acestep/core/generation/handler/lora/lifecycle.py:319-325, 191-316` |
| `REQUIRED_PEFT_CONFIG_KEYS = ("peft_type",)`, `_validate_peft_adapter_config` | `acestep/core/generation/handler/lora/lifecycle.py:14, 61-84` |
| `set_use_lora(bool) -> str`, `set_lora_scale(scale) -> str` (clamp :103) | `acestep/core/generation/handler/lora/controls.py:35-80, 83-190` |
| `get_lora_weights_hash(handler)` | `acestep/audio_utils.py:451` |
| `AudioSaver.save_audio(..., format="wav")` | `acestep/audio_utils.py:197-260` |
| `VALID_LANGUAGES` (no `kk`; `unknown` present) | `acestep/constants.py:13-20` |
| Training CLI: `build_root_parser` (`--yes/--plain` :85-97, `fixed` :110-116), `build_fixed_standalone_parser` :29-66, `--checkpoint-dir` :163, `--model-variant` :168, `--dataset-dir` :232, `--num-workers` :238, `--lr` :265, `--batch-size` :266, `--gradient-accumulation` :267, `--epochs` :268, `--shift` :273, `--num-inference-steps` :274, `--optimizer-type` :275, `--offload-encoder` :278, `--adapter-type` :282, `--rank` :286, `--alpha` :287, `--output-dir` :305, `--save-every` :306, `--resume-from` :307, `--preprocess` :318, `--audio-dir` :319, `--dataset-json` :320, `--tensor-output` :321, `--max-duration` :322 | `acestep/training_v2/cli/args.py` |
| `train.py` dispatch (`--preprocess` first, then `validate_paths`) / `main` | `train.py:79-108, 112-125` |
| `train_fixed.main()` / `_run_preprocess` | `acestep/training_v2/cli/train_fixed.py:198-224, 134-197` |
| dataset JSON discovery (relative to JSON dir; `audio_dir=None` safe) | `acestep/training_v2/preprocess_discovery.py:24-91` |
| `VARIANT_DIR_MAP["turbo"] = "acestep-v15-turbo"` / `validate_paths` | `acestep/training_v2/cli/args.py:18-22`, `cli/validation.py:14-57` |
| Trainer output: `checkpoints/epoch_{N}_loss_{x:.4f}` and `final/`; per-checkpoint `adapter_config.json` + `adapter_model.safetensors` (PEFT `save_pretrained`) + `training_state.pt` | `acestep/training_v2/trainer_fixed.py:516, 553`; `trainer_helpers.py:148-180, 195-211, 237` |
| Handler progress cache creates its own directory | `acestep/core/generation/handler/progress.py:47-51` |
