# Project status — updated 2026-09-14 11:55 (Monday, RTX 5060 8 GB desktop)

## The four outcomes

| # | Outcome | Status | Evidence |
|---|---------|--------|----------|
| 1 | Infrastructure and data prepared | **Reached (small dataset)** | GPU machine rebuilt from GitHub: weights sha256 5/5, raw sources `RESULT: OK`, `diagnose_gpu.py` RESULT: OK (RTX 5060, sm_120), `validate_dataset.py` RESULT: OK (11 crops, 7.0 min, 3 recordings) |
| 2 | Generation with the existing pretrained model | **Reached** | 9/9 clips `outputs/baseline/` (3 cases × 3 seeds, 30 s, turbo 8 steps shift 3.0, no quantization, CPU offload), ~4.3 s/clip, peak 5.8 GB. **Not yet listened to.** |
| 3 | Adapter trained, saved, reloaded | **Reached (pilot)** | LoRA r64/α128, 200 epochs = 600 steps, 10 m 49 s, peak 5.0 GiB, epoch loss 1.09 → 0.71 (training evidence only). `outputs/training/pilot/final` passes `check_adapter.py`; reloaded for 9/9 matched clips in `outputs/adapter/` with upstream `lora_loaded/use_lora: true`, scale 1.0 |
| 3b | Adapter v2 on the expanded dataset | **Reached (trained + reloaded)** | dataset v2 = 122 crops / 73.6 min / 62 recordings (+59 RTRK kui, triaged by ear). LoRA r64, 60 epochs = 1740 steps, 39 m 21 s, peak 5.0 GiB, epoch loss 1.12 → 0.72 (flat from epoch 30). `outputs/training/kui_v2/final` passes `check_adapter.py`; 9/9 matched clips in `outputs/adapter_kui_v2/`, `use_lora: true`, hash `53fa15cc` |
| 3c | Adapter v3 (same 62 recordings, dense crops) | **Reached (trained + reloaded)** | dataset v3 = 206 crops / 124.0 min / 62 recordings. LoRA r64, 40 epochs = 2000 steps, 44 m 33 s, peak 5.0 GiB, epoch loss 1.03 → 0.71 (flat from epoch 10). `outputs/training/kui_v3/final` OK; 9/9 clips `outputs/adapter_kui_v3/`, hash `033d0f57`. v3 clips correlate 0.63–0.86 with v2 at equal seeds: a refinement of v2, not a new direction |
| 4 | Human-reviewed improvement | **Owner impression only** | owner: v2 "a bit better than the original, still sounds like AI". Viewer has 36 clips (baseline / pilot / v2 / v3); per-clip notes and a Kazakh listener still needed |

## Monday 14 Sep — GPU run on the RTX 5060 (8 GB, not the 5090)
- Machine: Windows 11, RTX 5060 8 GB, driver 610.47, 32 GB RAM. Installed user-local: uv, Python 3.12 (via uv), ffmpeg 9 shared (winget).
  No `py` launcher: use `C:\kmm\venv-acestep\Scripts\python.exe`.
- 8 GB adjustments and the path-safety fix are in `docs/DECISIONS.md` (2026-09-14 entry). Training settings stayed the planned
  rank 64 + `--offload-encoder`; generation adds `--offload-to-cpu`.
- New `scripts/sidestep_train.py`: both `train_adapter` wrappers now go through it (upstream rejected tensor dirs outside its clone).
  Caveat: upstream's CLI exits 0 even when training fails; read the "Training Complete / TRAINING FAILED" banner.
- Wikimedia returned HTTP 429 on the first raw fetch; a rerun after 90 s fetched the rest.
- Logs: `C:\kmm\work\*.log`. Pilot checkpoints every 25 epochs in `C:\kmm\work\pilot\checkpoints\` (epoch 25…200).
- Dataset is still the 11-crop pilot set; step 5a (RTRK triage) needs a listener and was not done.
- The 9 adapter clips differ clearly from baseline at equal seeds (waveform correlation 0.07–0.41). That shows the adapter is
  active, **not** that it is better. With 9 training clips (5 dombra crops of one recording + 4 anthem crops) overfitting is expected.

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

- **Round-2 data search (2026-09-14 morning, Codex round 1 + Claude sub-agents):** inventories in `docs/DATA_SOURCES_CODEX.md`,
  `docs/DATA_LEADS_ROUND2.md`, `docs/DATA_REPOS_ROUND2.md`. Outcome: no new clean solo-dombra corpus and no sung-Kazakh-with-lyrics
  corpus exists in open sources; RTRK remains the dataset. Added as licensed references only: official anthem recording (PD, 3.2 min),
  two Zhambyl museum films (CC BY-SA, 18.7 + 7.7 min, quiet, content unheard, `segments.csv` lists candidate ranges).
  "Master of Dombra" stays excluded (uncredited performer). **45 candidate lyric texts** for the RTRK sung files in
  `data/lyrics/candidates/` (14/15 songs, 8/20 terme, generic lullaby text ×10), all `UNVERIFIED` until checked against the recording.
- Repo: https://github.com/Yeldar2609/kazakh-music-model (private). Clone + `fetch_raw_sources.py` + `download_checkpoints.py` rebuild everything.

## Requires human review
- All Kazakh transcripts (`data/lyrics/crops/*.txt`, `data/lyrics/eval_verse_abai.txt`): spelling and the 2006 typo fix `дазағым→қазағым`. `reviewed_by_kazakh_speaker: false`.
- `Moon and stars` (val dombra): listen to confirm it is dombra without a backing track.
- `an12_01` peaks at 0 dBFS (the source file is already at 0 dB): keep or drop after listening.
- Provenance calls: PD-KZ-exempt covers the anthem composition; Commons applies it to the phonogram too. CC BY-SA on `Moon and stars` (val only, not trained on).

## GPU steps still untested (prepared, awaiting 5090 validation)
Superseded 2026-09-14: runbook steps 0–4 and 5–7 all ran on the RTX 5060 (see above). Still untested: step 5a (Whisper transcription drafts), `--resume-from`, the Linux `.sh` wrappers.

## Blockers / risks
- Dataset is tiny and off-genre for vocals (anthem with orchestra). Intelligible Kazakh singing is a target, not an expectation.
- Tomorrow's OS and network are unknown; the weights folder must travel with the project (9.4 GB) so nothing is downloaded.
- Presentation hour and GPU window not yet known → the 2 h cutoff in the runbook is unfilled.

## Monday 14 Sep, afternoon — dataset v2 and adapter v2
- Machine survived the planned reset intact (USB backup `D:\KMM_backup_2026-09-14` was not needed; `RESTORE.md` is on it).
- Owner triaged all 116 RTRK files in `viewer/triage.html` (new; data from `scripts/build_triage_page_data.py`).
- `scripts/plan_rtrk_crops.py` added 111 kui crops; build → validate `RESULT: OK` → export. Decisions and exclusions in
  `docs/DECISIONS.md` (2026-09-14 afternoon). Tensors `C:\kmm\work\tensors_train_v2` (116) / `tensors_val_v2` (6).
- Whisper large-v3 drafts for all 45 sung RTRK files in `data/lyrics/drafts/` (run with `--no-vad`: VAD dropped singing).
  44/45 have text; `an_001` is a hallucination loop. All UNREVIEWED: not usable for training until a Kazakh speaker corrects them.
- v2 checkpoints every 10 epochs in `C:\kmm\work\kui_v2\checkpoints\`; logs `C:\kmm\work\train_kui_v2.log`.
- The v2 set is ~96 % instrumental dombra: listen whether B/C still sing (risk noted in DECISIONS).
- **First listening note (project owner, not yet a Kazakh-speaker review), 2026-09-14:** "this version is a bit better
  relative to the original version … It definitely still sounds like AI but it is getting better." Counts toward outcome 4 as
  an informal owner impression only; per-clip notes and a Kazakh speaker are still needed.

- **v3 (evening):** dense tiling of the same kui (`plan_rtrk_crops.py --dense`); tensors `C:\kmm\work\tensors_train_v3` (197);
  checkpoints `C:\kmm\work\kui_v3\checkpoints\` every 10 epochs. Loss curve flat after epoch 10 → the instrumental side is
  saturating on 59 recordings; the next real gain needs *new* sources or vocal data, not more epochs.

## Next action
1. Listen in `viewer/index.html` (baseline / pilot / v2 / v3 per seed), write per-clip notes, export to `outputs/listening_notes.json`.
2. Vocal data: a Kazakh speaker corrects drafts for a few of the 27 dombra+voice files (18 terme, 9 songs) → vocal crops → retrain v3.
3. Optional: v2 at `--adapter-scale 0.5`, or checkpoint `epoch_30`, if v2 overpowers the vocal prompts.
Open ask: request access to the gated `yeshpanovrustem/kazakh_songs_asr` (Kazakh songs with verbatim transcripts) with the
founder's Hugging Face account; with a token we can pull sung-Kazakh + lyrics material directly.

## 2026-11-11: Assignment 2 completed pilot
- Verified access and all six SHA256-checked Kazakh Songs ASR shards; full preparation retained 2,977 clips. Restricted data stays at C:/kmm/assignment2.
- Local NF4/rank-8 adapter training works on the 4 GB RTX 3050 Ti. Original and enriched runs each completed 100 updates and saved adapters; peak GPU allocation about 1.43 GiB.
- Enriched held-out flow loss 1.033698 versus original 1.214504, a 14.9% reduction on 16 clips from eight songs. This is not a pronunciation or music-quality measurement.
- Nine matched 15-second final WAVs, offline demo and ZIP: outputs/assignment2-2026-11-11. Presentation: page://page_6e44bb30eee88191b6f5bb1a6b13710a.
- New demonstration verse avoids exact-line overlap with selected training data. Human listening and Kazakh wording review remain open.
- Read docs/ASSIGNMENT2_RESULTS.md and docs/ASSIGNMENT2_DEFENSE.md. Code and documentation are local working-tree changes, not pushed.

## 2026-11-11: full-data follow-up requested
- Owner feedback: pilot music sounds terrible; lower loss is not a quality success.
- Full run started at C:/kmm/assignment2/full_v1: 2316 distinct new clips plus 772 original-data updates, learning rate 0.00002, checkpoint listening comparisons planned. Assignment due 12 November.
- Read docs/ASSIGNMENT2_FULL_RUN.md. Do not report completion or improved sound before evidence and listening.

## 2026-11-11: full-data run completed
- 3,088 updates completed in 3,977.16 seconds (66.29 minutes), peak allocated GPU memory 1,462 MiB.
- Coverage audit: all 2,316 intended new training IDs exactly once, zero validation/test IDs, 772 original-data updates over nine crops. Four valid distinct checkpoints; final matches step 3,088.
- Twelve stereo 48 kHz, 30-second examples: pretrained and checkpoints 772, 1,544, 3,088 across three prompts. Offline listening page: outputs/assignment2-full-2026-11-11/index.html.
- Listening copies use matched RMS levels and shuffled A-D labels per row. Originals remain unchanged. Offline playback, pause-on-other-play, rating persistence, export payload and desktop/mobile layout checks passed.
- Slides updated in page://page_6e44bb30eee88191b6f5bb1a6b13710a. Seven-minute guide: docs/ASSIGNMENT2_FULL_DEFENSE.md. Full-run measurements: docs/assignment2_full_results.json.
- Owner's checkpoint preference is pending. No audible improvement has been established; do not pick the winner by loss.
