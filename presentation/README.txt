KAZAKH MUSIC GENERATION - Assignment 2 presentation
Yeldar & Aisha

HOW TO OPEN
1. Unzip the folder anywhere (keep index.html, envelope.js and the audio folder together).
2. Double-click index.html. Use Chrome or Edge. No internet and no installation needed.
3. Press F for fullscreen.

KEYS
Right / Left arrow (or Space, PageDown / PageUp)   next / previous slide
F  fullscreen      O  slide overview      N  speaker notes (with timings and handoffs)
M  motion on/off   Home / End  first / last slide      Esc  close overview

WHAT MAKES IT DIFFERENT (rehearse these once)
* Two strings, two presenters. The strip at the bottom is a dombra neck: the gold
  string lights up on Yeldar's slides, the turquoise string on Aisha's. Click a fret to jump.
* Slide 1: pluck the two strings (click them, or press 1 and 2). The sound is made by
  the browser. It is NOT model output, and the slide says so.
* Kazakh Futurism look: neon turquoise and gold, a wireframe steppe, ram-horn ornament as circuitry.
* A sun shaped like a shanyrak rises behind the steppe as the story goes on. The target verse
  is about morning light over the steppe. It stops at first light on purpose.
* Slide 7: blind class test. The two clips are shuffled on every page load and shown as
  "Clip 1" and "Clip 2". Count hands with the + buttons, then press "Reveal identities".
  It is a class poll, not part of the recorded results.
* Slide 8: the strength knob. Press Play, then click 0%, 25%, 50% or 100% (or keys 1-4).
  The clip switches and keeps its place in the verse. All four are real prerecorded outputs.

AUDIO
Nothing plays until you press Play. Only one clip plays at a time.
Click or drag on a waveform to jump to a moment. Replay starts the clip again.
Test the room speakers before class.

PRINT / PDF
Press the Print button (or Ctrl+P), choose "Save as PDF", turn on "Background graphics".
You get one static slide per page.

WHAT IS IN THIS FOLDER
index.html     the whole presentation
envelope.js    loudness curves measured from the four clips (they drive the visuals)
audio/         matched-level listening copies from outputs/assignment2-lighter-2026-11-11/audio
  reference_pretrained.wav   = B_verse_simple_A.wav  pretrained, no adapter        sha256 fdf99391...
  selected_adapter_025.wav   = B_verse_simple_D.wav  final adapter at 25% (chosen)  sha256 8fd81afc...
  adapter_050.wav            = B_verse_simple_B.wav  final adapter at 50%           sha256 1bb2f986...
  adapter_100.wav            = B_verse_simple_C.wav  final adapter at 100%          sha256 0a7835d4...
All four files are byte-identical to the originals and match the playback hashes in
that folder's verification.json. All are model-generated. No training recordings or
transcripts are included.

NOTES
Fonts are the ones built into Windows (Sitka, Segoe UI). On other systems the
browser substitutes a similar font; the Kazakh letters still display.
On a phone the slides become one scrolling page.
