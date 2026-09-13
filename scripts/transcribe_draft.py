"""DRAFT transcription of a Kazakh vocal recording with faster-whisper. Output is a diagnostic aid only:
a Kazakh speaker must correct it before any words are attached to a training crop.
Usage: uv run --with faster-whisper python scripts/transcribe_draft.py <audio> [--model large-v3] [--device cuda|cpu]
Writes data/lyrics/drafts/<stem>.draft.txt  (one line per segment: start<TAB>end<TAB>text) and prints it.
"""
import argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--compute-type", default=None, help="default: float16 on cuda, int8 on cpu")
    a = ap.parse_args()
    from faster_whisper import WhisperModel
    ct = a.compute_type or ("float16" if a.device == "cuda" else "int8")
    model = WhisperModel(a.model, device=a.device, compute_type=ct)
    segments, info = model.transcribe(a.audio, language="kk", vad_filter=True, beam_size=5)
    out = ROOT / "data" / "lyrics" / "drafts" / (Path(a.audio).stem + ".draft.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# DRAFT (faster-whisper {a.model}, lang=kk, prob={info.language_probability:.2f}) - NOT REVIEWED. Correct by ear before use."]
    for s in segments:
        lines.append(f"{s.start:7.2f}\t{s.end:7.2f}\t{s.text.strip()}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("->", out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
