# Presenter briefing: everything you need to explain this project

Written for the person presenting, who is new to music machine learning. Read the 60-second and 3-minute versions
until you can say them without notes. Every fact here has a file behind it (section 12).

---

## 1. Where things truly stand (say this first, not last)

| # | Outcome | Status | Evidence |
|---|---------|--------|----------|
| 1 | Infrastructure and data prepared | **Reached, small scale** | pinned engine + weights with checksums; validated 11-crop dataset; 116 archive files staged for triage |
| 2 | Generation with the existing pretrained model | **Partial** | one 10-second dombra clip on a 4 GB laptop GPU (INT8, CPU offload). The nine-clip fixed-case baseline on the RTX 5090 is prepared, not yet run |
| 3 | Adapter trained, saved, reloaded | **Not started** | scripts and runbook prepared, verified against upstream source, never executed on a GPU |
| 4 | Human-reviewed improvement | **Not started** | needs outcome 3 plus a Kazakh listener |

Never say "we trained a model" or "our model". Say: **"an ACE-Step-based prototype: we built and verified the
pipeline and the dataset; adapter training is prepared, not executed."** If the researcher pushes, the honest sentence is:
"Only one thing has ever run against the model, a 10-second instrumental smoke test on my laptop."

---

## 2. The 60-second version (spoken)

"I wanted to find out whether an existing open music model can produce a dombra instrumental and a short passage of
Kazakh singing, and whether a small adapter trained on licensed Kazakh recordings changes the result. I picked
ACE-Step 1.5, a pretrained text-to-music model, and pinned one exact version of the code and the weights so anyone
can reproduce the setup. I built the data pipeline: raw recordings with license evidence, 30-to-45-second crops with
crop-specific transcripts, a validator that rejects silent, duplicated, unlicensed or leaking samples, and an export
into the trainer's format. I wrote the generation, training and comparison scripts against the actual upstream source,
and a runbook that proves the GPU works before any model runs. The dataset today is small: eleven validated crops from
four recordings, plus 265 minutes from the Kazakh state broadcaster's archive that still need listening and transcript
review. The model has generated one instrumental clip so far. Training is the next step, on the 5090."

## 3. The 3-minute version (spoken)

Add to the above:

- **Why ACE-Step.** It generates complete music, vocals and accompaniment, from a text caption plus lyrics, runs on one
  consumer GPU, has a documented adapter-training path and a documented way to load the adapter back at inference.
  The alternative, VocalRender, is a score-native singing synthesiser: it needs every syllable annotated with MIDI pitch
  and note duration and renders only the voice. I kept the raw recordings and transcripts so that annotation could be
  done later.
- **Why the small "turbo" checkpoint.** It generates in 8 denoising steps, so the evaluation loop is fast. The cost: it
  is a distilled model with no classifier-free guidance and rated "Medium" fine-tunability by its authors. The
  50-step "sft" checkpoint is the documented next candidate if adapter results are weak.
- **The Kazakh problem.** ACE-Step has no Kazakh language code. I read the source: the code is just a text header fed
  into the text encoder, not a validated capability. So every Kazakh sample uses the documented `unknown` code, lyrics
  stay in Kazakh Cyrillic, and I never relabel Kazakh as Russian. Intelligible Kazakh singing is a target, not an
  expectation.
- **What "improvement" would mean.** Human listening on matched pairs: same caption, same lyrics, same seed, same
  settings, only the adapter differs. Training loss going down is not evidence of better music.
- **Honesty about scale.** Crops of one recording are one source, not many. The vocal training material is an
  orchestral anthem, off-genre for folk singing. The single Kazakh-singing-with-dombra field recording has no
  transcript, so it is a human reference in the demo, never a training sample.

---

## 4. What the project is, and is not

**Is:** a reproducible, honestly labelled experiment harness around a pretrained model, with a license-audited
mini-dataset, fixed evaluation cases, and a demo that plays saved audio only.

**Is not:** a Kazakh music model, a trained system, a proof that adapters help, or a dataset of sufficient size. It is
also not a claim that adding a language code creates language ability.

---

## 5. The pipeline, stage by stage

Each stage: what it does, why it exists, the command, what success looks like.

### 5.1 Pin the engine and the weights
- **What:** clone ACE-Step 1.5 at commit `ca1e85fe` (2026-08-29); download the weights from Hugging Face repo
  `ACE-Step/Ace-Step1.5` at revision `19671f40` and record every file's sha256.
- **Why:** "reproducible" means someone else gets the same bytes. Upstream changes weekly.
- **Command:** `scripts/download_checkpoints.py` (pinned revision, checksums into `CHECKSUMS.json`, compared against
  `configs/checkpoint_checksums.json`).
- **Success:** every weight file's sha256 matches the Hugging Face LFS record (verified).
- **Trap we hit:** upstream's "is the model present?" check demands the planning language-model folder too; without it,
  service init silently downloads the whole repository unpinned. We keep that folder on disk and never load it.

### 5.2 Prove the GPU, not just the import
- **What:** `scripts/diagnose_gpu.py` prints the torch build, the GPU's compute capability, the kernel architectures in
  the wheel, runs a real bf16 matrix multiply on the GPU with a timing, and loads a WAV through torchaudio.
- **Why:** `import torch` succeeding tells you nothing about whether the wheel has kernels for an RTX 5090 (Blackwell,
  `sm_120`) or whether audio decoding works.
- **Success:** `RESULT: OK`, arch list contains `sm_120`, matmul finite. Verified on the laptop (sm_86) with the same wheel.

### 5.3 Baseline generation with fixed cases, before any training
- **What:** `scripts/generate_cases.py` runs three cases × three seeds × 30 s: (A) solo dombra instrumental, (B) a
  public-domain Abai verse with simple accompaniment, (C) the same verse with dombra-led accompaniment.
- **Why:** you cannot say an adapter changed anything unless the unchanged model's output is saved first, with the
  exact caption, lyrics, seed, steps, shift and checkpoint revision in a JSON sidecar next to each WAV.
- **Settings for turbo:** 8 inference steps; `shift = 3.0` set manually; guidance scale is forced to 1.0 by the pipeline
  (turbo has no classifier-free guidance); quantization off (required for adapters later); planning LM disabled so
  nothing rewrites our prompts; `vocal_language = "unknown"`.
- **Success:** 9 WAVs + 9 sidecars under `outputs/baseline/<case>/`.

### 5.4 Raw data with provenance
- **What:** originals go untouched into `data/raw/<source>/` with a `SOURCE.json` listing, per file: URL, performer,
  license verbatim, the URL where the license is stated, a group id (one per original performance), sha256, ffprobe
  facts, and whether lyrics exist.
- **Why:** a researcher will ask "may you use this?" for every file. The answer must be on disk, not in memory.
- **Sources today:** Wikimedia Commons (CC BY / CC BY-SA / public domain), the RTRK state broadcaster's archive on
  Hugging Face (CC BY-NC 4.0), a museum's archival films (CC BY-SA 4.0).

### 5.5 Crop plan → manifest
- **What:** `data/manifests/crop_plan.csv` lists each crop (start, end, kind, split, caption, lyrics file, group id).
  `scripts/build_manifest.py` cuts 30–45 s crops with ffmpeg, resamples to 48 kHz (the model's rate), and writes
  `manifest.json` with all required fields.
- **Why crops are minimal:** only cut and resample. No normalisation, no filters, so the instrument's sound is untouched.
- **Vocal crops:** the transcript file contains only the words sung inside that crop, cut on subtitle cue boundaries.
  A whole-song lyric attached to every excerpt would teach the model wrong alignments.

### 5.6 Validate
- **What:** `scripts/validate_dataset.py` checks every crop: decodable, not silent, clipping, duration in range,
  duplicate audio (sha256), vocal crops have lyrics, Kazakh letters (ә ғ қ ң ө ұ ү һ і) survive, license + evidence URL
  present for the training split, and **no recording group appears in both train and validation** (leakage).
- **Why:** a tiny dataset fails silently in these exact ways. A self-test round-trips all nine Kazakh-specific letters.
- **Success:** `RESULT: OK`. It printed OK on the 11-crop set; it correctly FAILED on a synthetic set with deliberate leakage.

### 5.7 Export to the trainer's format
- `scripts/export_dataset_json.py` writes `dataset_train.json` / `dataset_val.json` in the exact format the upstream
  trainer reads (caption, lyrics or `[Instrumental]`, `is_instrumental`, `language: "unknown"`, unknown BPM/key left empty).

### 5.8 Preprocess on the GPU
- **What:** the trainer's preprocessing turns each clip into tensors: the **VAE** compresses audio into a small latent
  representation; the **text encoder** (Qwen3-Embedding-0.6B) turns caption and lyrics into embeddings.
- **Why:** training then works on these compact tensors instead of raw audio. Two GPU passes, done once.
- **Command:** `scripts/preprocess_dataset.cmd|.sh` → `python -m acestep.training_v2.cli.train_fixed --preprocess …`
  (the module entry point is required; the top-level `train.py fixed --preprocess` rejects the call).

### 5.9 Train a LoRA adapter
- **What:** the 2-billion-parameter model stays frozen. **LoRA** adds small low-rank matrices to the attention layers
  (rank 64, alpha 128) and trains only those, a few tens of millions of parameters.
- **Why:** a few minutes of audio cannot retrain a 2B model, but can nudge its style through a small adapter. Also fits
  in memory and trains in minutes.
- **Command:** `scripts/train_adapter.cmd|.sh` → `train.py --yes --plain fixed …` with batch 1, gradient accumulation 4,
  learning rate 1e-4, shift 3.0, 8 steps.
- **Procedure:** a 1-epoch smoke run first to see one real optimizer step with finite loss, step time and peak VRAM;
  then size the pilot to the time window. Checkpoints hold optimizer state (full resume); `final/` holds adapter-only
  weights. Each checkpoint dir is about 0.5 GB, so save every 25 epochs, not every epoch.
- **Success:** finite loss values, `final/adapter_config.json` + `adapter_model.safetensors`, `check_adapter.py` exits 0.

### 5.10 Reload the adapter and compare
- **What:** the same generation script with `--adapter <dir>`; it calls the upstream `load_lora`, `set_use_lora`,
  `set_lora_scale`, and records upstream's own "adapter active" flags in the sidecar.
- **Why matched:** same cases, seeds, duration, steps, shift. Only the adapter differs, so any audible change is
  attributable.

### 5.11 Human listening
- Dombra likeness, recognisable Kazakh words and pronunciation, lyric adherence, coherence and artifacts, and whether
  the adapter helped or harmed. Machine transcription is a diagnostic aid, never proof of correct singing.

### 5.12 The demo viewer
- `viewer/index.html` plays saved WAVs only, side by side per seed: "Pretrained (no adaptation)", "Pretrained + our
  adapter", "Human recording (reference, NOT generated)". A visible PRERECORDED banner; honest empty states when an
  output does not exist. No live generation on stage.

---

## 6. Glossary (plain words)

- **Text-to-music model:** takes a caption and lyrics, produces audio.
- **Diffusion / flow model:** generates by starting from noise and removing it in steps; the "steps" are those denoising passes.
- **Turbo / distilled:** a version trained to do the job in 8 steps instead of 50; faster, less controllable.
- **Classifier-free guidance (CFG):** a knob that pushes output toward the prompt; turbo models do not have it (forced to 1.0).
- **Shift (3.0):** how denoising effort is distributed across steps; the turbo model expects 3.0. Wrong shift degrades audio.
- **Seed:** the random starting point; fixing it makes runs comparable.
- **VAE / latents:** a compressor that turns audio into a compact representation and back.
- **Text encoder (Qwen3-Embedding-0.6B):** turns text into numbers the music model conditions on. Byte-level tokenizer, so
  Kazakh Cyrillic is representable. Representable is not understood: the model never saw Kazakh singing.
- **DiT:** the diffusion transformer, the 2B-parameter core that does the denoising.
- **LoRA / PEFT:** parameter-efficient fine-tuning; small trainable matrices added to a frozen model. Rank = their size.
- **Optimizer step / gradient accumulation:** one weight update; accumulation of 4 means four clips contribute to each update.
- **Epoch:** one pass over all training clips.
- **Checkpoint vs adapter weights:** checkpoint = adapter + optimizer state (resumable); adapter-only = what inference loads.
- **Sample rate 48 kHz:** the model's audio rate; we resample crops to it.
- **Split leakage:** the same recording in both training and validation; makes validation meaningless.
- **group_id:** one value per original performance, used to keep all its crops on one side of the split.
- **Licenses:** public domain (free), CC BY (credit), CC BY-SA (credit + share derivatives alike), CC BY-NC (credit, no
  commercial use). ND (no derivatives) and "all rights reserved" are excluded.
- **sha256 pinning:** a fingerprint of a file; if it matches, you have the identical bytes.

---

## 7. Decisions and trade-offs ("we chose X over Y because Z; the cost is W")

1. **ACE-Step over VocalRender.** Complete music from caption + lyrics, one GPU, documented adapter path. Cost: no
   score control, no guarantee of Kazakh. VocalRender needs per-syllable pitch/duration scores and renders vocals only.
2. **turbo over sft/base.** Fast 8-step loop. Cost: no CFG, "Medium" fine-tunability. sft is the named next candidate.
   We do not switch to XL just because the 5090 has memory; the whole chain stays on one base checkpoint.
3. **LoRA over LoKR.** Upstream calls LoRA stable and recommended, LoKR experimental.
4. **`unknown` language code.** No `kk` exists; the code is a text header, not a capability. Never relabel as `ru`/`az`,
   never translate, never transliterate.
5. **Planning LM disabled.** We supply captions and lyrics explicitly; nothing rewrites them.
6. **Baseline before training.** Otherwise there is nothing to compare against.
7. **CC BY-NC material accepted.** This is a non-commercial research demo. Any adapter trained on RTRK data must never
   be released or used commercially; a commercial path would require removing it and retraining.
8. **Save-every 25, output outside the synced project folder.** Each checkpoint is ~0.5 GB.

---

## 8. The data story (with exact numbers)

| Pool | Numbers | State |
|---|---|---|
| Wikimedia Commons | 5 files downloaded, 4 used in crops: **4 recordings of 3 compositions**; 11 crops, **7.0 min** | validated; train = 1 hobbyist dombra recording (5 crops) + 2 anthem recordings (4 vocal crops with cue-aligned transcripts); val = 1 separate dombra recording (2 crops) |
| RTRK state broadcaster archive (HF, CC BY-NC 4.0) | 116 files, **265 min**: 71 kui, 20 zhyr-terme, 15 folk-composer songs, 10 lullabies | staged, **not in the training set**: instrumentation unverified by ear, no transcripts |
| Candidate lyrics for RTRK sung files | 45 files: 14/15 songs, 8/20 terme, generic lullaby text ×10 | **all unverified** until checked against the recording by a Kazakh speaker |
| Museum films (CC BY-SA) + official anthem (PD) | 18.7 + 7.7 + 3.2 min | licensed references only |
| Everything else | 534 queries across 22 repositories and archives | zero new clean recordings; reports in `docs/DATA_*` |

Human reference only: a 30-second field recording of a singer with dombra at Nauryz 2015 (CC BY 2.0). No transcript,
so it never trains; it is shown, labelled as a human recording, to remind the audience what the target sounds like.

Excluded on principle: "Master of Dombra" (uncredited third-party performer, no human Commons review); all Europeana
Kazakh items (in copyright); YouTube rips; anything ND.

Open, needs the founder: the gated `yeshpanovrustem/kazakh_songs_asr` corpus, the only sung-Kazakh-with-text corpus that
exists (4.5 h, 195 songs, non-commercial, gated). Request access with your own Hugging Face account.

---

## 9. Limitations and expected failure modes

- Vocal training material is an orchestral state anthem, off-genre. Expect the adapter to pull toward choir + orchestra.
- With 5 dombra crops from one performer, expect memorisation of that recording rather than "dombra" in general.
- The model has no Kazakh conditioning. Recognisable words would be a surprise, not the plan.
- A short fine-tune can degrade everything (worse coherence, artifacts). That is a valid result and gets shown.
- Evaluation is a handful of matched pairs judged by ear. Report it as weak evidence, never as a metric.

---

## 10. Questions the researcher may ask, with answers

- **"Did you train the model?"** No. The pretrained model is unchanged. An adapter training run is prepared and
  verified against the source but has not been executed; when it runs, the comparison is adapter vs the same base model.
- **"Why cfg-dropout 0.15 on a model not trained with CFG?"** It is the upstream corrected trainer's default. Whether it
  helps turbo is an open question I would ablate (0.0 vs 0.15) given GPU time.
- **"Why rank 64?"** Upstream default and its documented "good default"; rank 16 is the fallback under memory or
  overfitting pressure. I would sweep it if results justified it.
- **"How would you evaluate beyond listening?"** Blind A/B with a Kazakh speaker on matched pairs; automatic
  transcription of the vocal only as a diagnostic; a held-out recording never trained on; audio embedding distance to
  real dombra as a weak automatic signal.
- **"With 50 GPU hours?"** Triage and transcribe the RTRK archive to 20–40 reviewed crops; ablate cfg-dropout, rank and
  the sft checkpoint; blind listening panel; then decide whether VocalRender-style score annotation is worth it.
- **"How does this connect to VocalRender?"** It does not use it. It preserves raw recordings and transcripts so
  per-syllable pitch/duration annotation could be added later. The gap is exactly that annotation.
- **"What is the RTRK provenance risk?"** The dataset card says CC BY-NC 4.0 from the state broadcaster's own archive;
  per-recording performer rights are not itemised. Non-commercial research use only; I would not release weights.
- **"How did you configure inference?"** 8 steps, shift 3.0 set explicitly, guidance forced to 1.0 by the pipeline,
  quantization off, planning LM off, fixed seeds, 30 s, language `unknown`.

---

## 11. How to describe the AI-assisted process (say it proactively)

"I set the goals, the constraints and the honesty rules, then directed AI coding agents to do bounded pieces: one for
the environment, one for data sourcing, one for the model interface, one for the demo viewer, and a read-only reviewer
after integration. Every agent got its own files and had to report what it verified and what it could not. The reviewer
caught a real blocker before it reached the GPU. Every training flag was checked against the upstream source, and the
decisions are mine. The parts that need a human ear, listening to the archive and checking Kazakh transcripts, I do
myself." Tools: Claude Code with sub-agents for the build; Codex for the web-scale data search.

---

## 12. Next steps, in order (on the 5090)

1. Clone the repo; runbook step 0 rebuilds weights and raw audio by script.
2. Step 1: hardware and tool check (`nvidia-smi`, driver ≥ 570, CUDA ≥ 12.8).
3. Step 2–3: env sync, `diagnose_gpu.py` must print `RESULT: OK` with `sm_120`.
4. Step 4: nine-clip baseline. Listen. **This alone upgrades outcome 2 to "reached".**
5. Step 5a: ear triage of RTRK, transcript review, expand the crop plan, re-validate.
6. Steps 5–7: preprocess, 1-epoch smoke, sized pilot, adapter reload, matched comparison.
7. Listening notes in the viewer; update `PROJECT_STATUS.md`.

## 13. Where each claim's evidence lives

| Claim | File |
|---|---|
| Pins and checksums | `configs/pins.json`, `configs/checkpoint_checksums.json` |
| Engine and checkpoint decisions, Kazakh handling | `docs/DECISIONS.md` |
| Dataset facts | `data/manifests/manifest.json`, `data/manifests/sources_*.SOURCE.json` |
| License audits and search coverage | `docs/DATA_SOURCES.md`, `docs/DATA_SOURCES_CODEX.md`, `docs/DATA_LEADS_ROUND2.md`, `docs/DATA_REPOS_ROUND2.md` |
| Scripts and verified upstream symbols (file:line) | `docs/MODEL_INTERFACE.md` |
| GPU workflow with expected outputs and recovery | `docs/TOMORROW_RUNBOOK.md` |
| The one model run so far | `outputs/baseline_laptop_smoke/*.json` |
| Status and open items | `PROJECT_STATUS.md` |
