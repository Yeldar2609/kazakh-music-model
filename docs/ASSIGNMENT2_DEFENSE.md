# Seven-minute defense and questions

Rehearse with a timer. Aim for seven minutes of presentation, then two to three
minutes of questions. Open the slide deck, offline `index.html`, and source code
before class. Use headphones during rehearsal and check the classroom speakers.
Do not invent listening results; add your own observations after hearing the clips.

## 0:00-0:35 | Question

My project asks whether adding Kazakh singing with aligned lyrics helps a music
generation model. I use an existing pretrained model and train small adapters.
The goal is not to build a foundation model from scratch. It is a controlled
dataset-enrichment experiment, with generated examples and an objective test.
This fits the dataset-comparison route of Assignment 2, subject to the instructor
accepting sung-language generation within the NLP track.

## 0:35-1:15 | Why change the data?

The earlier work focused heavily on dombra instrumentals. The local original
training set available now contains nine crops from three recordings. That is
very little aligned Kazakh vocal material. The new dataset offers short sung
phrases paired with manually aligned text. My hypothesis is that those pairs
can improve lyric conditioning. However, isolated vocals may also weaken the
model's accompaniment, so a lower numerical error alone is not enough.

## 1:15-2:05 | Data and leakage

The source corpus contains 3,013 segments from 195 songs and 36 artists. I
downloaded all six files and verified their checksums, but the experiment is a
small pilot, not full-corpus training. The pilot selects 64 new training clips,
16 validation clips and 16 test clips. I split by artist and song before selecting
clips, so segments from one song stay together. Exact duplicate audio is removed.
The test clips represent eight songs. Artists may occur across splits, so I do
not claim unseen-artist generalization. The dataset is gated for non-commercial
academic use, and its original recordings are not in the shareable demo.

## 2:05-2:50 | What I changed in the model setup

The full model weights need more memory than this laptop's four-gigabyte GPU.
I kept the base frozen and compressed its weights to four bits, while training
a rank-eight LoRA adapter. LoRA learns small corrections to existing layers.
Gradient checkpointing reduces memory use by recalculating some intermediate
values. The actual training peak was about 1.43 gigabytes. This shows the local
method works, but saving memory is separate from improving musical quality.

## 2:50-3:35 | Fair comparison

There are three models: the pretrained reference, an adapter trained only on the
original data, and an enriched-data adapter. Both trained adapters use 100 updates,
the same base, rank, learning rate, random seed and optimizer. The enriched run
alternates new and original examples, giving 50 updates to each source. It uses
50 of the 64 selected new clips. The original clips are longer, so equal updates
are not equal seconds of audio. That is one limitation of this small experiment.

## 3:35-4:30 | Explain the result carefully

The model learns to remove noise from an audio representation. Flow-matching loss
measures how well it predicts the required change. I evaluated each model with
the same noise seed for each held-out clip, so noise differences do not explain
the comparison. Mean test loss was 1.3848 for the pretrained model, 1.2145 for the
original-data adapter and 1.0337 for the enriched adapter. That is a 14.9 percent
reduction relative to the original-data adapter. All 16 test clips had lower
error. This is encouraging, but it is not a 14.9 percent increase in pronunciation
accuracy. There is only one pilot run, and some test clips belong to the same song.

## 4:30-5:45 | Audio demonstration

Open the comparison page. Play the simple-vocal row, 15 seconds per model, in
order: pretrained, original-data, enriched-data. Then play 15 seconds of the
enriched dombra-led case. Allow 15 seconds to describe a specific observation
from your own rehearsal. Point to the target lyrics if words are unclear.

Every clip uses the same prompt, seed, duration and generation settings within
its comparison row. The demonstration verse was replaced after discovering
overlap between the old verse and a training transcript. The new draft has no
exact-line overlap with the selected training clips. Its Kazakh wording still
needs native-speaker review. Do not call the output natural or fluent unless
you can support that with actual listener feedback.

## 5:45-6:25 | Show the code

Open `scripts/prepare_assignment2.py` at `split_for`, then show
`scripts/train_assignment2_4bit.py` at `load_quantized` and the alternating
training groups. Explain that the underlying loss and model are reused from
ACE-Step; your work is data preparation, the memory-compatible training route,
controlled comparison and evaluation. Show `docs/assignment2_results.json` for
the recorded numbers and adapter checksums.

## 6:25-7:00 | Conclusion

The main result is that a local, small adapter experiment using new aligned vocal
data reduced held-out flow loss. The next question is whether people hear better
Kazakh and better music. To answer that, I need native-speaker transcriptions and
blind listening ratings, more test songs and repeated training seeds. I also need
to check that stronger vocal adaptation does not damage dombra accompaniment.
The current result supports further testing, rather than a claim of a finished
Kazakh music product.

## Likely questions

**Did you train the whole model?** No. The pretrained base is frozen; 5,505,024
adapter parameters are trainable.

**Why an ASR dataset for music generation?** It provides sung audio with aligned
text. We use the pairs to condition generation, not to train a recognizer. Its
isolated-vocal format is useful but differs from full arrangements.

**What prevents leakage?** Song grouping precedes selection, audio hashes are
disjoint and exact duplicates are removed. This does not automatically detect
all covers, near-duplicates or exposure during unknown foundation pretraining.

**What does 14.9% mean?** Relative reduction in mean flow loss against the
original-data adapter on this fixed test. It is not word accuracy or a listener score.

**Why not train on everything?** This was a bounded pilot to verify the local
training route and controlled comparison. The full corpus is downloaded and
prepared for a larger follow-up. More data does not remove the need for evaluation.

**Can you share the data?** No redistribution is implied by access. The demo contains
generated output and aggregate results; original restricted audio/transcripts remain local.

**What remains?** Native-speaker listening, repeated runs and broader evaluation.
Before class, book the correct instructor's slot. There is no submission required
in the Assignment 2 grading box.
