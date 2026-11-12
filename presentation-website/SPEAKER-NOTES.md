# Yeldar and Aisha: presentation notes

Seven minutes total, approximately 3 minutes 30 seconds each. Leave 2–3 minutes for questions.

## Slide 1

Our project asks whether adapting a pretrained model with Kazakh singing data produces music we prefer. We wanted a model that could connect Kazakh lyrics with musical expression, including dombra accompaniment. This is a dataset-enrichment experiment, not an attempt to train a foundation model from scratch.

We are Yeldar and Aisha. Today we will explain the data, show how the experiment fitted on a laptop, and let you hear the comparison. We separate technical completion from musical quality.

Yeldar: 40 seconds. Hand over to Aisha.

## Slide 2

There are three challenges: language, musical character, and listener preference. The words should connect to the singing. Melody, phrasing and accompaniment should also make musical sense. A result can satisfy a numerical objective and still be unpleasant to hear.

We used an existing music-generation model. The new dataset was originally created for speech recognition, but we used its aligned singing and text pairs for conditional music generation. We did not train a speech recognizer.

Aisha: 45 seconds. Hand over to Yeldar.

## Slide 3

The source dataset contains 3,013 segments from 195 songs and 36 artists. After filtering and exact audio deduplication, 2,977 clips remained. We used 2,316 for training, 334 for validation and 327 for testing.

The split groups normalized artist and song identities so clips from the same identified song stay together. Artists may still appear across splits. This does not detect every cover or near-duplicate. The material contains isolated singing with aligned lyrics, rather than full arrangements. Its gated academic-use recordings are not included in this presentation.

Yeldar: 50 seconds. Point to the three segments of the split. Hand over to Aisha.

## Slide 4

ACE-Step supplies the pretrained music model. We kept its base weights frozen and trained a rank-eight LoRA adapter, which learns smaller adjustments to existing layers. About 5.5 million adapter parameters were trainable.

Four-bit storage reduced the memory needed for the base, and gradient checkpointing saved memory by recalculating intermediate values. This made training possible on the laptop. Saving memory proves feasibility, not good music. Our contribution is data preparation, the local training workflow and the controlled comparison.

Aisha: 45 seconds. The moving dots illustrate the process; they are not live model activity. Hand over to Yeldar.

## Slide 5

The laptop has an RTX 3050 Ti GPU with four gigabytes of memory. The full run completed 3,088 updates in 66.3 minutes of training time. Its peak allocated GPU memory was about 1.43 GiB. Preparation, loading and generation are excluded from that time.

Every one of the 2,316 eligible new training clips appeared once. Every fourth update reused an original music crop, giving 772 additional updates over nine crops. We checked the log: no validation or test clip IDs were used. We saved intermediate adapters and retained the pretrained reference.

Yeldar: 45 seconds. This timeline is a replay of completed milestones. Hand over to Aisha.

## Slide 6

An earlier small pilot reduced mean held-out flow loss by 14.9 percent relative to the original-data adapter, on 16 test clips from eight songs. But the owner described the generated music as terrible.

Flow loss measures the training objective. It is not pronunciation accuracy or musical quality. In the later full-strength checkpoint comparison, the owner again preferred the pretrained reference for the simple-vocal example. That motivated a follow-up using a weaker adapter influence, rather than selecting a model solely by loss.

Aisha: 40 seconds. Hand over to Yeldar for the first half of the listening demo.

## Slide 7

Yeldar, first 45 seconds: explain that the two clips use the same prompt, lyrics, seed and 30-second duration. Play the reference for about 25 seconds, then pause. These are prerecorded generated samples, not training recordings. The playback copies have matched RMS levels, which reduces loudness bias but does not guarantee identical perceived loudness.

Aisha, next 45 seconds: play the selected example for the same 25-second interval. It uses the final trained adapter at 25% strength. The owner chose this version for melody and accompaniment. During rehearsal, add a specific audible observation and timestamp in your own words. The target lyrics are available below; do not claim verified pronunciation.

90 seconds total, split equally. Audio never starts automatically. Allow about 50 seconds for playback and 40 seconds for explanation and handoff.

## Slide 8

In the first comparison, the pretrained model won against the full-strength trained checkpoints on the simple-vocal case. We then compared the final adapter at 25, 50 and 100 percent influence against the pretrained reference.

The owner selected sample D, which was the 25-percent version, for melody and accompaniment. This suggests gentler adaptation was preferable for this example. Twenty-five percent means influence during generation, not the fraction of training data. All eligible training clips were still used.

Aisha: 35 seconds. State that this is one listener, one prompt and one seed. Hand over to Yeldar.

## Slide 9

We demonstrated that full-data adapter training can run on this laptop, and we built reproducible listening comparisons. Our selected example came from the trained adapter at a gentler strength. The preference is limited, and pronunciation remains unverified.

The next steps are more listeners, more prompts and seeds, native-speaker assessment, and more suitable licensed accompaniment data. The isolated-vocal dataset and small original music set limit what this experiment can teach about arrangements. Thank you. We are ready for questions.

Yeldar: 30 seconds. Total presentation target: 7 minutes. Q&A: 2–3 minutes. Suggested speaking time: 3 minutes 30 seconds each.