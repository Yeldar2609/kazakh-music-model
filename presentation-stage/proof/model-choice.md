# Model choice and inputs

## Engine: why ACE-Step 1.5 (pinned)

- Repo `ace-step/ACE-Step-1.5` @ `ca1e85fe9430179831e6bc6be790c332190a3866` (2026-08-29). Weights HF
  `ACE-Step/Ace-Step1.5` @ `19671f406d603126926c1b7e2adc169acbcade22`. See `configs/pins.json`.
- It generates **complete music** (vocals + accompaniment) from caption + lyrics, has a documented LoRA
  training path (`train.py fixed`, Side-Step integrated upstream), documented adapter reload
  (`load_lora`, `set_use_lora`, `set_lora_scale`), and runs on a single consumer GPU.
- VocalRender (`pymaster17/VocalRender` @ `c0ab96e1…`) is a *score-native singing voice synthesiser*: its input
  is an interleaved word / MIDI-pitch / note-duration score plus BPM (see `upstream/VocalRender/examples/inference_input.json`).
  It renders only the vocal line, not accompaniment, and its released data are Mandarin/other datasets
  (CrawlSinger-OS, Opencpop). To use it for Kazakh we would need per-syllable pitch and note-value
  annotations for every training clip, plus a separate accompaniment path. Raw recordings and transcripts are
  preserved under `data/raw/` and `data/lyrics/` so that annotation could be done later.

## Checkpoint: why `acestep-v15-turbo` (2B)

- User request: small, fast first experiment. Turbo generates in 8 steps (`shift=3.0`), so evaluation loops are fast.
- Compatibility verified in source: the upstream trainer's defaults target turbo (`--shift 3.0`,
  `--num-inference-steps 8`, `VARIANT_DIR_MAP["turbo"]`); Side-Step's corrected `fixed` mode is documented as
  correct for turbo, base and sft (`docs/sidestep/Shift and Timestep Sampling.md`). Reload path checks only
  for a PEFT `adapter_config.json`, independent of variant.
- Trade-off recorded: the model zoo rates turbo fine-tunability "Medium" vs "Easy" for base/sft, and turbo
  cannot use classifier-free guidance. If adapter results are weak, `acestep-v15-sft` (50 steps, CFG, "Easy")
  is the documented next candidate. We do **not** switch to XL because a GPU is large; the whole pipeline
  (preprocess → train → reload) stays on the same base checkpoint.
- The planning LM (`acestep-5Hz-lm-1.7B`) is disabled: captions and lyrics are supplied explicitly and the
  generation script passes `llm_handler=None`, so it cannot rewrite our prompts. Its folder is nevertheless
  present on disk (3.7 GB): upstream's "main model present?" check requires it, and without it
  `initialize_service` starts an unpinned whole-repository download (observed tonight on the laptop).

## Kazakh language handling (verified in source)

- `acestep/constants.py` `VALID_LANGUAGES` has no `kk`. `unknown` is the documented fallback.
- The DiT path does not validate the code: `prompt_utils._format_lyrics` writes a header
  `# Languages\n{language}\n\n# Lyric\n{lyrics}` into the Qwen3-Embedding-0.6B text encoder. `VALID_LANGUAGES`
  is enforced only by the LM's constrained decoder, which we do not use.
- Therefore every Kazakh sample and every eval case uses `language: "unknown"`. We never label Kazakh as
  Russian or Azerbaijani, never translate lyrics, and do not pretend adding `kk` to a list creates ability.
- Lyrics stay in Kazakh Cyrillic. The Qwen3 tokenizer is byte-level BPE, so ә ғ қ ң ө ұ ү һ і are representable.
  `scripts/validate_dataset.py --selftest` proves they survive our writer/reader; scripts force UTF-8.
