# Handoff for review (paste into ChatGPT)

I am a beginner in music ML preparing an independent prototype to show researchers on Mon 14 Sep 2026 (afternoon).
Please review the plan and the runbook for mistakes, unjustified claims, and missing checks. Be blunt.

## What the prototype is
An ACE-Step 1.5 based prototype: pretrained 2B `acestep-v15-turbo` (repo commit `ca1e85fe`, weights HF `ACE-Step/Ace-Step1.5`
@ `19671f40`) generating (A) a solo dombra instrumental, (B) a short Kazakh verse (Abai, public domain) with simple
accompaniment, (C) the same verse with dombra-led accompaniment; then a LoRA adapter trained with upstream's integrated
Side-Step trainer (`train.py fixed`, rank 64, lr 1e-4, batch 1 × accum 4) on a tiny licensed dataset, and a matched
comparison (same captions, lyrics, seeds 1001–1003, 30 s, 8 steps, shift 3.0) of pretrained vs pretrained+adapter.
Nothing is trained from scratch. The optional planning LM is disabled. VocalRender (score-native SVS) is documented as
a reference only: it needs per-syllable pitch/note-duration scores and renders vocals only.

## Facts verified in the upstream source
- `acestep/constants.py` `VALID_LANGUAGES` has no Kazakh code; `unknown` is the documented fallback. The DiT path does not
  validate the code (it is a `# Languages\n<code>` text header into Qwen3-Embedding-0.6B). We use `unknown` and never
  relabel as ru/az. Kazakh Cyrillic is kept; UTF-8 round-trip is tested.
- Trainer flags all exist in `acestep/training_v2/cli/args.py`; `--yes --plain` are root flags (before `fixed`);
  preprocessing must use `python -m acestep.training_v2.cli.train_fixed --preprocess …` because `train.py fixed` requires
  `--dataset-dir/--output-dir`. Checkpoints are saved as `checkpoints/epoch_N_loss_X.XXXX/` with `training_state.pt`
  (full resume) and `final/` (adapter only).
- Adapter reload at inference: `handler.load_lora(dir)`, `set_use_lora(True)`, `set_lora_scale(x)`; quantization must be None.
- `initialize_service` auto-downloads the whole HF repo (unpinned) if the LM folder is missing; we therefore keep the
  unused LM folder on disk and the generation script also stubs that check.
- Windows torch 2.7.1+cu128 / Linux 2.10.0+cu128 from `uv.lock`; both carry sm_120 (RTX 5090). Verified on the laptop
  that the wheel's arch list includes sm_120 and a bf16 matmul runs.

## Done tonight (laptop, RTX 3050 Ti 4 GB, Windows 11, no admin)
- Env synced; GPU diagnostic OK; weights downloaded and sha256-verified against HF LFS.
- One real 10 s dombra generation with the pretrained model (INT8 + CPU offload). Not the demo baseline.
- Dataset: 11 crops / 7.0 min / 3 independent recordings from Wikimedia Commons (CC BY 3.0 dombra hobbyist recording of a
  Kyrgyz tune → 5 train crops; CC BY-SA 4.0 dombra folklore video → 2 val crops; two public-domain anthem recordings →
  4 vocal train crops with transcripts cut on subtitle cue times). No Kazakh-sung + dombra + lyrics material exists in it.
- Validation checks: decodability, silence, clipping, duration, duplicate audio, lyrics presence and Kazakh letters,
  split leakage by recording group, license + evidence URL required for the training split.
- Scripts for generation/training/adapter check/viewer, all dry-run or fixture tested; nothing beyond one INT8
  generation has touched a model.

## What I will claim on Monday
Outcome 1 (infrastructure + small dataset) is real. Outcome 2 (pretrained generation) will be shown from saved 5090
baseline audio if tomorrow's run works; otherwise the laptop clip with its caveats. Outcome 3/4 only if training runs
and a Kazakh speaker listens. I will not claim the model "learned Kazakh" and will not use training loss as quality.

## Questions for you
1. Any flaw in training a turbo (distilled, no-CFG) model with the corrected continuous-timestep trainer and cfg-dropout 0.15?
2. With 4 vocal crops of an orchestral anthem and 5 dombra crops from one performer, what is the most honest expected
   effect of a rank-64 LoRA, and what failure modes (memorising the anthem, degrading everything) should I test for?
3. What extra check would you add before calling an adapter "loaded and active" beyond the loader's ✅ message, the
   upstream `lora_loaded/use_lora/lora_scale/lora_weights_hash` fields, and A/B listening with fixed seeds?
4. Anything in the runbook order (baseline before training, save-every budget, resume) you would change?
