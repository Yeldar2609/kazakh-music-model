# Full training and listening comparison

Started 11 November 2026; assignment due 12 November. The owner judged the pilot
music poor despite its lower held-out flow loss. That metric did not establish
audible quality. Do not describe the pilot as a successful musical improvement.

Run root: `C:/kmm/assignment2/full_v1`. Original experiments remain intact.

- All 2,316 eligible training clips, from 152 songs, participate exactly once.
- Validation (334 clips) and test (327 clips) remain outside training.
- Every fourth update uses an original local music crop: 2,316 new-data updates
  plus 772 original-data updates, 3,088 total. The nine old crops repeat; this
  preserves some accompaniment exposure but does not guarantee musical quality.
- Fresh frozen NF4 base, rank 8 / alpha 16, AdamW learning rate 0.00002,
  batch 1, gradient checkpointing, seed 42.
- Checkpoints every 772 updates; compare audio at 772, 1,544 and 3,088, plus
  the pretrained reference. Identical prompts, lyrics, seed and 30-second duration
  from `configs/assignment2_full_eval_cases.json`, giving the verse more space.
- Original draft demonstration lyrics have no exact-line overlap with any of the
  2,316 training transcripts. Native-speaker wording review remains open.
- Select for intelligibility, melody, natural phrasing, accompaniment and audible
  artifacts. Never choose solely by training or held-out flow loss.
- `scripts/build_checkpoint_listening.py` creates an offline page with separately
  shuffled A-D labels for each case, ratings, notes and an identity reveal. The
  listener may prefer the pretrained model or reject every candidate.

The runner prevents idle system sleep while active and restores the previous
execution-state request on exit. Keep the laptop plugged in; do not close its lid
or manually put it to sleep. No paid compute is used.

Preparation completed at approximately 15:45 local time on 11 November:
2,316 processed, zero failed. Training completed at approximately 16:51 local
time: 3,088 updates in 3,977.16 seconds (66.29 minutes), with 1,462 MiB peak
allocated GPU memory. Loading and preparation are excluded from this timing.

Verified: the log contains every one of the 2,316 intended training IDs exactly
once, no validation/test IDs, and 772 updates over the nine original crops.
All four saved checkpoints contain finite weights and have distinct checksums.
The final adapter matches checkpoint 3,088. Aggregate evidence and adapter hashes
are in `assignment2_full_results.json`.

Status: training and all 12 matched audio examples completed on 11 November.
The runner's `COMPLETE.json` confirms completion. The owner selected sample A
in the simple-vocal row, which maps to the pretrained reference. Thus the
full-strength trained checkpoints did not win this one listener comparison.
The owner wants better melody and accompaniment. A follow-up generated all three cases with the final
adapter at 25% and 50% strength, holding prompts, lyrics, seed and duration fixed.
All 192 LoRA layers were scaled and checked against alpha/rank times the chosen
factor. Its separate page is `outputs/assignment2-lighter-2026-11-11/index.html`.
It compares pretrained, 25%, 50% and 100% versions with matched playback RMS.
This is an inference-strength comparison, not another training run.

Follow-up listening result: the owner selected D in the lighter page's
`B_verse_simple` row. Its verified identity is the final checkpoint at 25% adapter
strength (`audio_scale_025`). Select this clip for the class demo. It was preferred
over the reference, 50% and 100% versions on this case for melody/accompaniment.
This is one listener, one prompt and one seed, with no numeric rating or
timestamped critique. It does not establish broader quality or pronunciation gains.
Selected playback: `outputs/assignment2-lighter-2026-11-11/audio/B_verse_simple_D.wav`.

Offline comparison: `outputs/assignment2-full-2026-11-11/index.html`. The page
contains the pretrained reference and checkpoints 772, 1,544 and 3,088, with
three cases per model. Each WAV is stereo, 48 kHz and 30 seconds long. Each row's
four source files have different checksums and identical generation settings.
Playback copies are attenuated to the lowest RMS level within their row, reducing
loudness bias without altering the original generated files. RMS matching does
not guarantee identical perceived loudness. Gains and source/playback hashes are
recorded in the package's `verification.json`.

Browser checks passed on an offline file copy: all twelve players loaded, playback
advanced, starting another player paused the previous one, ratings survived reload,
and exported JSON contained the entered rating, note and all twelve identities.
Desktop and 390-pixel layouts were inspected; no horizontal overflow appeared.
Synthetic QA ratings were cleared and do not count as listener results.

## Reproduce the local run

Use a new run directory to preserve existing results. The commands below use
the current Windows environment and the already prepared, access-controlled
dataset. The pinned ACE-Step checkout and model weights must already exist.
Dataset download requires approved Hugging Face access. Never put the token in
a command, notebook, screenshot, or repository file.

```powershell
$python = 'C:/kmm/venv-acestep/Scripts/python.exe'
$run = 'C:/kmm/assignment2/full_reproduction'
& $python scripts/train_assignment2_4bit.py preprocess --dataset C:/kmm/assignment2/prepared/dataset_train.json --out "$run/tensors_train"
# Proceed only when preparation_result.json reports 2316 processed and zero failed.
& $python scripts/train_assignment2_4bit.py train --tensors "$run/tensors_train" --original-tensors C:/kmm/assignment2/tensors_original_full --original-every 4 --lr 0.00002 --steps 3088 --save-every 772 --out "$run/training"
& $python scripts/generate_assignment2_4bit.py --cases configs/assignment2_full_eval_cases.json --out "$run/audio_pretrained"
foreach ($step in 772,1544,3088) {
    & $python scripts/generate_assignment2_4bit.py --cases configs/assignment2_full_eval_cases.json --adapter "$run/training/step_$step/adapter" --out "$run/audio_step_$step"
}
```

The active local runner additionally verifies the training log covers all 2,316
distinct new IDs before writing its completion record. Checkpoint folders save
adapter weights, not optimizer state, so this script cannot resume an interrupted
optimizer run exactly. Preserve a finished checkpoint for inference if interrupted.

The listening-page builder checks all 12 WAVs are finite, non-silent and 30 seconds
long, verifies matched generation settings, and rejects identical audio across
checkpoints. Its verification file records audio checksums and training counts.
These are integrity checks, not evidence that the music sounds good.

After the reproduction commands above, build its original comparison with:

```powershell
& $python scripts/build_checkpoint_listening.py --run $run --out outputs/assignment2-reproduction
```

The builder verifies completion and unique sample coverage directly from the
training log, so the separate local orchestration wrapper is not required.
For the strength follow-up, generate into fresh audio_scale_025 and audio_scale_050
folders using `--adapter-scale 0.25` and `--adapter-scale 0.5` respectively, with
the final adapter and the same full evaluation config. Then run the builder with
`--variants audio_pretrained audio_scale_025 audio_scale_050 audio_step_3088`
and a new output directory. Rating storage is separate for each variant set.
