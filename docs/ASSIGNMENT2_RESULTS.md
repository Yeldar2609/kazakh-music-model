# Assignment 2: verified pilot results

11 November 2026. The experiment ran locally on the RTX 3050 Ti 4 GB laptop.

Owner feedback after listening: the pilot music sounds terrible. The numerical
result below does not establish an audible improvement. The completed full-data
follow-up is documented in [ASSIGNMENT2_FULL_RUN.md](ASSIGNMENT2_FULL_RUN.md).

## Measured result

| Model | Validation flow loss | Test flow loss |
|---|---:|---:|
| Pretrained reference | 1.297839 | 1.384789 |
| Original-data adapter | 1.107257 | 1.214504 |
| Enriched-data adapter | 0.984930 | 1.033698 |

The enriched adapter has **14.9% lower mean test loss** than the original-data
adapter, and 25.4% lower than the pretrained reference. It has lower loss on all
16 test clips. These clips come from eight separate songs; they are not 16
independent songs. Validation contains 16 clips from 10 songs. Each model uses
the same per-clip noise seed and conditioning dropout is disabled for evaluation.

This measures flow-matching error, not word accuracy, pronunciation or musical
quality. Native-speaker listening is still required. There is one training seed,
one noise draw per evaluated clip and no confidence interval. The 100-update
experiment was fixed before examining test results; no test-driven tuning was done.

## What was actually trained

- Same pinned ACE-Step 1.5 turbo base for all models. This project trains an
  adapter, not the foundation model from scratch.
- NF4 double quantization, BF16 compute, rank 8 / alpha 16, batch 1, gradient
  checkpointing, AdamW learning rate 0.0001, gradient clipping 1.0, seed 42.
- 5,505,024 trainable adapter parameters; the base is frozen.
- Original control: 100 updates over nine complete original crops from three
  recordings. This is not the historical 197-crop dataset, whose remaining audio
  is not present on the laptop.
- Enriched: 100 updates alternating new and original data equally. The selected
  new pool contains 64 clips from 40 songs, but this run encounters 50 of those
  clips, with 50 original-data updates. Equal updates do not mean equal audio
  seconds because the original crops are longer.
- Control: 294.70 seconds, 1,465 MiB peak allocated GPU memory. Enriched: 205.54
  seconds, 1,462 MiB. Timings exclude loading, preprocessing and generation.

The uncompressed model weights alone occupy 4.46 GiB. The new compressed route
makes local training possible. It reuses the pinned upstream preprocessor,
corrected flow-matching loss, adapter injection and checkpoint writer. The
upstream checkout remains unchanged. Dependencies added: bitsandbytes 0.50.2 and
pyarrow 26.0.1; existing torch is 2.7.1+cu128.

## Data and provenance

[Kazakh Songs ASR](https://huggingface.co/datasets/yeshpanovrustem/kazakh_songs_asr),
revision `af4b5d48283b0a9e42ce302c72b1cb38fa2c7bf2`. All six files passed SHA256
checks against Hugging Face LFS metadata. Full preparation retained 2,977 of 3,013
clips: 2,316 train, 334 validation, 327 test. Thirty-six were excluded by preparation
checks. The pilot selection uses only the first three shards.

Split by normalized artist plus song before selection, using deterministic hash
buckets. Remove exact audio duplicates. Select complete 3-10 second clips by audio
hash: 64 train (345.78 s), 16 validation (85.37 s), 16 test (81.69 s). Selected song
groups and audio hashes are disjoint. This is not an unseen-artist benchmark;
covers or near-duplicates under different metadata are not automatically detected.

The licence is gated, non-commercial academic use, not unrestricted open source.
Source recordings and transcripts stay outside GitHub and OneDrive. The final
demo includes generated audio only. Source-separated vocals may affect accompaniment.

## Honest audio comparison

Three cases, each 15 seconds: dombra instrumental, simple vocal, dombra-led vocal.
All models use seed 1001, eight generation steps, shift 3.0 and the same NF4 base.

The old Abai demonstration verse overlapped one selected training transcript.
It was replaced by an original draft verse in `configs/assignment2_eval_cases.json`.
No exact line overlaps the 64 selected new training clips. The draft still needs
native-speaker review. Earlier Abai outputs are excluded from the final demo.

## Local evidence and reproduction

Evidence root: `C:/kmm/assignment2`. Aggregate results and adapter hashes are in
`docs/assignment2_results.json`; no source recordings or transcripts are included.
Use `C:/kmm/venv-acestep/Scripts/python.exe` with the following scripts.

1. Download the pinned revision with `hf download`, dataset repo type, to
   `C:/kmm/assignment2/source`. Authentication stays in the local HF credential store.
2. `scripts/prepare_assignment2.py --pilot` prepares the first three shards.
   `scripts/select_assignment2_pilot.py` freezes 64/16/16 clips. Preparation without
   `--pilot` audits the full corpus. These commands preserve source files.
3. `scripts/train_assignment2_4bit.py preprocess --dataset <json> --out <new_dir>`
   converts each split to tensors. Full original crops use `original_local.json`
   and `tensors_original_full`; never truncate aligned vocal crops.
4. Train the control with `train --tensors <original_tensors> --out <new_run> --steps 100`.
   Train enriched with `train --tensors <new_tensors> --original-tensors <original_tensors>
   --out <new_run> --steps 100`. Both start from the same frozen base.
5. Saved adapters: `original_4bit_100/final/adapter` and
   `enriched_4bit_100/final/adapter`. Validate with `scripts/check_adapter.py`.
6. `scripts/generate_assignment2_4bit.py --adapter <adapter> --out <new_audio_dir>`;
   omit adapter for the pretrained reference. The new evaluation config is default.
7. `scripts/evaluate_assignment2.py --tensors <held_out_dir> --adapters <control>
   <enriched> --out <new_results.json>`. Never pass training tensors as held-out data.
8. `scripts/build_assignment2_demo.py --out <new_demo_dir>` packages the final nine
   WAVs and aggregate test results. Its directory names match this recorded run.

All experiment output folders are versioned; scripts refuse overwrites. Checkpoints
are saved every 25 updates. The small loop does not implement optimizer-state resume.

Passed: split self-test, synthetic Parquet preparation test, synthetic 4-bit
forward/backward/update, real preprocessing, both training runs, adapter validation
and paired held-out evaluation. Generation uses a local BF16 detokenizer input cast
to resolve a quantized inference dtype mismatch without changing upstream.

The initial 30-second original preparation is excluded because it truncated lyrics.
A first 25-step run failed at saving; the corrected output-root scope was tested.
Diagnostic failed runs remain separate from final outputs.

## Before class

Use the presentation and offline comparison page; rehearse seven minutes plus
two to three minutes of questions. Confirm the NLP track interpretation and book
the correct instructor's time slot. Individual projects are allowed. Nothing goes
in the Assignment 2 grading box. Structured native-speaker evaluation remains
open. The full-data follow-up and current deliverables are documented separately
in ASSIGNMENT2_FULL_RUN.md.
