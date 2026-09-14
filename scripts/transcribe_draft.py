"""DRAFT transcription of Kazakh vocal recordings with faster-whisper. Output is a diagnostic aid only:
a Kazakh speaker must correct it before any words are attached to a training crop.
Usage: uv run --with faster-whisper python scripts/transcribe_draft.py <audio> [<audio> ...] [--model large-v3] [--device cuda|cpu]
Writes data/lyrics/drafts/<stem>.draft.txt per file (one line per segment: start<TAB>end<TAB>text).
The model is loaded once for all files; existing drafts are skipped unless --overwrite.
"""
import argparse, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio", nargs="+")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--compute-type", default=None, help="default: float16 on cuda, int8 on cpu")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--no-vad", action="store_true",
                    help="disable Silero VAD: it is speech-trained and drops most sung passages (0 segments on songs)")
    a = ap.parse_args()
    if a.device == "cuda":
        try:
            import torch  # noqa: F401  (on Windows this registers torch's bundled cuBLAS/cuDNN DLLs for ctranslate2)
        except ImportError:
            pass
    from faster_whisper import WhisperModel
    ct = a.compute_type or ("float16" if a.device == "cuda" else "int8")
    model = WhisperModel(a.model, device=a.device, compute_type=ct)
    out_dir = ROOT / "data" / "lyrics" / "drafts"
    out_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for audio in a.audio:
        out = out_dir / (Path(audio).stem + ".draft.txt")
        if out.exists() and not a.overwrite:
            print("skip (exists)", out.relative_to(ROOT))
            continue
        t0 = time.perf_counter()
        try:
            # condition_on_previous_text=False limits the repeated-line loops Whisper falls into over music.
            segments, info = model.transcribe(audio, language="kk", vad_filter=not a.no_vad, beam_size=5,
                                              condition_on_previous_text=False)
            lines = [f"# DRAFT (faster-whisper {a.model}, lang=kk, vad={not a.no_vad}, "
                     f"audio {info.duration:.1f}s) - NOT REVIEWED. Correct by ear before use."]
            for s in segments:
                lines.append(f"{s.start:7.2f}\t{s.end:7.2f}\t{s.text.strip()}")
        except Exception as exc:  # keep going; one bad file must not stop the batch
            failures += 1
            print(f"FAIL {audio}: {exc}")
            continue
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"-> {out.relative_to(ROOT)}  ({len(lines) - 1} segments, {time.perf_counter() - t0:.1f}s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
