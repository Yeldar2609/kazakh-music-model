# Full-data experiment: seven-minute defense

Script for the 12 November presentation. Full training and twelve comparison
clips are complete; see ASSIGNMENT2_FULL_RUN.md for verification. Before presenting,
replace the listening paragraph with your actual observations. Rehearse with a
timer; allow 2–3 minutes
afterward for questions.

## 0:00–0:40 | Research question

My project asks whether adding Kazakh singing with aligned lyrics improves an
existing music-generation model. The goal is understandable Kazakh singing and
pleasant music, including dombra accompaniment. I use a pretrained model and
train a small adapter on a laptop. My contribution is the data preparation,
memory-efficient training setup, and comparison of generated outputs. This uses
Assignment 2's dataset-enrichment route. I will confirm the instructor accepts
sung-language generation within the NLP track.

## 0:40–1:25 | Why a second experiment?

The earlier local data available for this experiment consisted of nine crops
from three recordings. A small pilot added new vocal examples. Its held-out
numerical error decreased, but I judged the generated music poor. That is an
important negative result: lower model loss did not establish better music.
The follow-up uses the complete eligible training split and compares several
checkpoints by listening. I will not automatically choose the last checkpoint.

## 1:25–2:15 | Dataset and separation

The Kazakh Songs ASR corpus has 3,013 segments from 195 songs and 36 artists.
It contains isolated singing with aligned text, rather than complete musical
arrangements. After filtering and exact audio deduplication, 2,977 clips remain:
2,316 for training, 334 for validation, and 327 for testing. The split groups
normalized artist and song names, so clips from the same identified song stay
together. Artists can appear across splits; this is not an unseen-artist test.
The validation and test clips are excluded from training. The original gated
recordings and transcripts stay local and are not included in the demo package.

## 2:15–3:05 | How it fits on this laptop

This laptop has four gigabytes of graphics memory. The base model stays frozen
and uses four-bit weight storage. A rank-eight LoRA adapter learns small changes
to the model, with about 5.5 million trainable parameters. Gradient checkpointing
saves memory by recalculating intermediate values. This makes the experiment
practical locally, although it does not guarantee good music. The full run uses
a smaller learning rate than the pilot to make adaptation more gradual.

## 3:05–3:50 | Full-run design

The completed run had 3,088 updates and took 66.3 minutes of training time.
Each of the 2,316 new training clips appeared
once. Every fourth update uses an original music crop, giving 772 such updates.
Those nine original crops repeat, so accompaniment diversity remains limited.
The new material is isolated vocals, which may help lyric conditioning but can
also weaken the arrangement. I save intermediate adapters and generate examples
from updates 772, 1,544, and 3,088, alongside the unmodified pretrained model.
The training log verifies which examples were actually used.

## 3:50–5:20 | Listening demonstration

Open the full-run listening page. Before class, choose one row and rehearse four
15-second excerpts from the same portion of its 30-second samples. That takes
one minute. Use the remaining 30 seconds to explain the comparison and your
observations. If no version sounds acceptable, say so directly.

Within each row, the prompt, lyrics, seed, duration, and generation settings are
the same. Playback copies have matched average signal levels. The labels are
shuffled independently for each row so I can listen
before revealing checkpoint identities. I assess clear words, melody, phrasing,
accompaniment, and glitches. The demonstration verse has no exact-line overlap
with the training transcripts, but its wording still needs native-speaker review.

**First listening result:** I selected sample A in the simple-vocal row. The
identity reveal showed the pretrained reference. On this example, I preferred
the original model over all three full-strength trained checkpoints. My priority
for further improvement is melody and accompaniment. This is one listener's
preference on one case, not proof about every prompt. A follow-up compares lighter
adapter strengths. Add a specific audible observation and timestamp during rehearsal.

## 5:20–6:10 | Show the implementation

Show the data split and filtering in scripts/prepare_assignment2.py. Then show
the sample schedule and frozen-base adapter training in
scripts/train_assignment2_4bit.py. Finally show the coverage count in the full-run
record and the listening page. Explain that ACE-Step supplies the underlying
model and training objective. I adapted the workflow to the laptop, prepared
the new dataset, and built a matched checkpoint comparison. I do not claim to
have designed the foundation model or trained all of its weights.

## 6:10–7:00 | What the experiment can establish

The experiment tests whether broader vocal training helps this local setup and
whether intermediate checkpoints sound better than the final one. Completion
and training coverage are measurable. Musical quality still requires listening.
This is one training seed and one generation seed per case, with three prompts.
The checkpoint comparison also does not isolate dataset size from learning
rate and update count, because those changed from the pilot. A stronger study
would use several listeners, more prompts and seeds, native-speaker transcription
of the vocals, and richer licensed accompaniment data. My conclusion should
match the audio we heard, even if that conclusion is that more work is needed.

## Questions to prepare for

- **Why use an ASR dataset?** It supplies aligned sung text and audio. We use
  those pairs for conditional generation, not to train a speech recognizer.
- **Did you use all the data?** All eligible training clips participate once.
  Held-out validation and test clips remain separate. Filtered clips are excluded.
- **Does lower loss mean better singing?** No. Our pilot showed why listening
  is necessary. Flow loss is not word accuracy or a musical-quality score.
- **Why only one pass?** It is a bounded local experiment for the deadline.
  More passes could improve adaptation or overfit; intermediate audio matters.
- **Is the final checkpoint best?** Only listening can answer for these samples.
  The pretrained reference is allowed to win, and every sample can be rejected.
- **What leakage remains possible?** Song grouping and exact audio hashes do
  not detect every cover, near-duplicate, or unknown foundation pretraining item.
- **Can others reproduce it?** The configuration, code, fixed dataset revision,
  coverage logs and generation settings document the run. Dataset access and
  compatible hardware are still required; bit-for-bit GPU identity is not promised.

Before class: verify the correct instructor's presentation slot, open the slides
and offline demo, rehearse for at least seven minutes, and test the speakers.
The assignment instructions say no upload to the grading box is required.
