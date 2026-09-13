# Project status — updated 2026-09-14 00:05 (Sunday night, laptop)

## The four outcomes

| # | Outcome | Status | Evidence |
|---|---------|--------|----------|
| 1 | Infrastructure and data prepared | **Reached (small dataset)** | env synced + `diagnose_gpu.py` RESULT: OK on the laptop; weights sha256-verified; `validate_dataset.py` RESULT: OK on 11 crops |
| 2 | Generation with the existing pretrained model | **Partially reached** | one 10 s dombra clip generated on the laptop (INT8 + CPU offload, not the 5090 settings): `outputs/baseline_laptop_smoke/`. The 9-clip fixed-case baseline is *prepared, awaiting 5090* |
| 3 | Adapter trained, saved, reloaded | **Not started** | scripts + runbook prepared; needs the 5090 |
| 4 | Human-reviewed improvement | **Not started** | needs outcome 3 + a Kazakh listener |

## Completed and tested tonight
- Upstream pinned and read: ACE-Step-1.5 @ `ca1e85fe`, weights @ `19671f40` (`configs/pins.json`, `configs/checkpoint_checksums.json`).
- Language handling verified in source: no `kk`; we use `unknown` (see `docs/DECISIONS.md`).
- Windows CUDA env at `C:\kmm\venv-acestep` (torch 2.7.1+cu128, has sm_120 kernels); GPU diagnostic passes on the RTX 3050 Ti.
- Data tooling tested on synthetic and real audio: crop → manifest → validate (leakage/dupes/lyrics/Kazakh letters/licenses) → ACE-Step dataset JSON.
- Real pilot dataset (Wikimedia Commons, licenses recorded in `data/manifests/sources_wikimedia_commons.SOURCE.json`):
  - 5 files downloaded (11.1 min raw), 4 used in crops: **4 recordings of 3 compositions**; 11 crops, **7.0 min**.
    Training split = 3 recordings of 2 compositions (one hobbyist's dombra recording → 5 crops; two anthem recordings → 4 vocal crops
    with crop-specific Kazakh transcripts cut on subtitle cue times). Validation = 1 separate dombra recording → 2 crops.
    Crops of one recording are counted as one source, never as independent data.
  - No Kazakh singing *with dombra and lyrics* exists in the set; the yurt field recording (human, no transcript) is kept only as a human reference in the viewer.
- **RTRK archive batch downloaded (2026-09-14 00:50):** 116 files / 264.7 min from the state broadcaster's Hugging Face dataset
  (CC BY-NC 4.0 → non-commercial research use only, decision recorded in `docs/DATA_SOURCES.md`): 71 kui, 20 zhyr-terme,
  15 folk-composer songs, 10 lullabies. In `data/raw/rtrk_kazakh_traditional_audio/` with `SOURCE.json`. **Not yet in the
  training set**: instrumentation unverified by ear and no transcripts. Triage sheet `data/manifests/rtrk_triage.csv`;
  transcription draft helper `scripts/transcribe_draft.py`; procedure = runbook step 5a.
- Scripts: `generate_cases.py` (dry-run tested), `check_adapter.py` (tested on fixtures), `preprocess_dataset.{cmd,sh}`, `train_adapter.{cmd,sh}` (argument handling tested with a shim; flags verified against upstream `args.py`), viewer builder + page (rendered and checked at 1280×720).
- Read-only review done; blocker (output layout vs viewer) and high findings fixed.

## Requires human review
- All Kazakh transcripts (`data/lyrics/crops/*.txt`, `data/lyrics/eval_verse_abai.txt`): spelling and the 2006 typo fix `дазағым→қазағым`. `reviewed_by_kazakh_speaker: false`.
- `Moon and stars` (val dombra): listen to confirm it is dombra without a backing track.
- `an12_01` peaks at 0 dBFS (the source file is already at 0 dB): keep or drop after listening.
- Provenance calls: PD-KZ-exempt covers the anthem composition; Commons applies it to the phonogram too. CC BY-SA on `Moon and stars` (val only, not trained on).

## GPU steps still untested (prepared, awaiting 5090 validation)
All of `docs/TOMORROW_RUNBOOK.md` steps 2–7 on the 5090: env sync on that OS, `diagnose_gpu.py`, 9-clip baseline via `generate_cases.py`, preprocessing (two GPU passes), one real optimizer step, pilot training, adapter reload + matched regeneration. Only `initialize_service` + one INT8 generation has ever run (on the laptop).

## Blockers / risks
- Dataset is tiny and off-genre for vocals (anthem with orchestra). Intelligible Kazakh singing is a target, not an expectation.
- Tomorrow's OS and network are unknown; the weights folder must travel with the project (9.4 GB) so nothing is downloaded.
- Presentation hour and GPU window not yet known → the 2 h cutoff in the runbook is unfilled.

## Next action
1. Transfer project folder (now ~1.6 GB with RTRK raw audio) + `C:\kmm\checkpoints` to the 5090 machine (runbook step 0).
2. Run runbook steps 1–4; listen to the baseline.
3. Step 5a: triage the RTRK files by ear, draft + review transcripts for a few terme/songs, expand `crop_plan.csv`, re-validate.
4. Steps 5–7: preprocess, smoke train, pilot, adapter comparison.
Open ask: request access to the gated `yeshpanovrustem/kazakh_songs_asr` (Kazakh songs with verbatim transcripts) with the
founder's Hugging Face account; with a token we can pull sung-Kazakh + lyrics material directly.
