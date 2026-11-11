# Assignment 2: Kazakh sung-language adaptation

## Status, 11 November 2026

Hugging Face access, all six downloads, checksums, preparation and both 100-update
training runs are complete. The owner judged the pilot music poor despite lower
loss. The full-data follow-up and twelve matched audio clips are complete for
the 12 November deadline. Listener preference remains open. See
[full-run status](ASSIGNMENT2_FULL_RUN.md) and the
[updated defense](ASSIGNMENT2_FULL_DEFENSE.md). The
[pilot results](ASSIGNMENT2_RESULTS.md) remain a historical record. The plan below
records the initial design, rather than the current full-run configuration.

Current laptop: RTX 3050 Ti, 4 GB VRAM, 16 GB RAM, about 1.8 GB RAM free at
inspection. Previous training used approximately 5 GB VRAM on an RTX 5060 8 GB.
The original training loader moves the full unquantized model to the chosen
device. Its weights alone occupy 4.46 GiB in BF16. The owner confirmed the larger
GPU machine is unavailable. A separate NF4 loader now supports a local pilot:
the synthetic backward/update test passed at 1,304 MiB peak allocated GPU memory,
and a 25-update real-audio test reached approximately 1,465 MiB. The first save
failed on upstream path-safety validation; the corrected run explicitly scopes
the save root to its new output folder. Completion and adapter files must be
verified before reporting a saved model. Presentation deadline: 12 November 2026.

Local scripts reuse the pinned upstream preprocessor, flow-matching loss and
adapter injection. NF4 double quantization, rank 8/alpha 16, BF16 computation,
batch size 1, gradient checkpointing and AdamW at 1e-4 make this a different
training configuration from the September rank-64 runs. Compare new matched
runs rather than attributing differences from September solely to the dataset.
New dependency: bitsandbytes 0.50.2. Data reader: pyarrow 26.0.1.

The initial `tensors_original` preparation truncated clips to 30 seconds and is
excluded from experiments. `tensors_original_full` preserves the complete clips
(36-45 seconds) and aligned lyrics. Only nine original training recordings/crops
are present locally; the 197-row historical manifest is not a complete local
dataset. Report the nine items as crops, not nine independent recordings.

## Assignment fit

Direction: NLP, specifically sung Kazakh language generation. Ask the instructor
to confirm that sung-language generation qualifies for the NLP track, since the
assignment explicitly lists NLP/LLM or computer vision rather than general audio.
Option B: enrich the original instrumental-heavy training set with aligned
Kazakh vocals, then compare original and enriched data under matched settings.
The gated dataset has a custom non-commercial academic licence; it is not an
unrestricted open-source dataset. Do not describe it as such for Option A.

Dataset: https://huggingface.co/datasets/yeshpanovrustem/kazakh_songs_asr
The card reports 3,013 excerpts, 195 songs, 36 artists and about 4.5 hours.
These are source-separated vocals, not full music arrangements. They may help
lyric conditioning but may weaken accompaniment. Improvement is a hypothesis.
Keep downloaded audio and transcripts outside GitHub; access does not imply
permission to redistribute the dataset or its recordings.

## Experiment protocol

1. Download the pinned revision into `C:/kmm/assignment2/source`.
2. Run `scripts/prepare_assignment2.py` using Python with pyarrow and soundfile.
   This writes only to `C:/kmm/assignment2/prepared`. Exact audio duplicates are
   removed. Clips outside 2-30 seconds are excluded and reported. Split by
   normalized artist plus song, deterministically about 80/10/10. This protects
   against same-song leakage, but is not an unseen-artist benchmark.
3. Review the audit and listen to representative clips. Check transcripts and
   source separation before training. The split must not be changed after results.
4. On suitable hardware, run matched training from the same base checkpoint:
   original data versus original data plus a documented vocal proportion.
   Keep optimizer, update count, rank, seeds and evaluation prompts fixed.
   Retain the untouched pretrained model as a third reference.
5. Use validation only for model choice. Reserve test songs for final evaluation.
   For generation, use new owner-written Kazakh lyrics with identical prompts,
   seeds, duration and inference settings across all models.
6. Save logs, settings, dataset audit, adapter checksums and generated WAV files.
   Evaluate intelligibility with native-speaker transcriptions and WER/CER against
   the prompted lyrics, plus blinded ratings for naturalness and accompaniment.
   Report the sample count and individual scores. ASR error is only a proxy;
   do not equate lower training loss with better pronunciation or music.

## Seven-minute presentation and 2-3 minute Q&A

- 0:00-0:45: question and why Kazakh vocal data was missing.
- 0:45-1:45: baseline architecture, pretrained model versus trained adapter.
- 1:45-2:45: original versus enriched dataset, restrictions and song-level split.
- 2:45-3:45: controlled experiment and reproducibility settings.
- 3:45-5:15: matched audio demonstration with blinded labels.
- 5:15-6:15: measured results, listener scores and failure cases.
- 6:15-7:00: limitations, conclusion and source-code walkthrough entry point.

Prepare answers about leakage, dataset licensing, overfitting, sung versus spoken
language, GPU limits and the distinction between generation and recognition.
Do not fill results slides until measurements exist. The existing browser viewer
can be the MVP demonstration. Export a self-contained permitted generated-audio
demo for class; do not package the gated training recordings.

Administrative requirements: individual work is allowed; teams up to six must
share an ICT Lab Instructor. Owner must select the appropriate presentation slot.
The assignment box is for grades, not file submission.
