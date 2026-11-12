"""Prepare gated sung-vocal data locally; never publish recordings or transcripts."""
import argparse
import hashlib
import io
import json
from pathlib import Path

REVISION = "af4b5d48283b0a9e42ce302c72b1cb38fa2c7bf2"


def split_for(artist, song):
    key = "|".join(x.strip().casefold() for x in (artist, song))
    bucket = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) % 10
    return "test" if bucket == 0 else "val" if bucket == 1 else "train"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("C:/kmm/assignment2"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--pilot", action="store_true", help="Use already verified shards; label the subset explicitly")
    args = ap.parse_args()
    if args.selftest:
        assert split_for(" Artist ", "Song") == split_for("artist", " song ")
        assert {split_for("artist", str(i)) for i in range(100)} == {"train", "val", "test"}
        print("Self-test passed")
        return
    import pyarrow.parquet as pq
    import soundfile as sf
    import numpy as np

    files = sorted((args.root / "source/kazakh_songs_asr").glob("*.parquet"))
    if args.pilot:
        files = files[:3]
        if len(files) != 3:
            raise RuntimeError("The reproducible pilot requires the first three verified shards")
    if not files or (len(files) != 6 and not args.pilot):
        raise RuntimeError("Download all six pinned dataset shards before preparation")
    out = args.root / ("prepared_pilot" if args.pilot else "prepared")
    out.mkdir(parents=True, exist_ok=True)
    samples = {key: [] for key in ("train", "val", "test")}
    seen = set()
    excluded = []
    groups = {key: set() for key in samples}
    for file in files:
        for batch in pq.ParquetFile(file).iter_batches(batch_size=8):
            for row in batch.to_pylist():
                raw = row["audio"]["bytes"]
                digest = hashlib.sha256(raw).hexdigest()
                if digest in seen:
                    excluded.append({"sha256": digest, "reason": "duplicate audio"})
                    continue
                seen.add(digest)
                lyrics = row["transcription"].strip()
                artist, song = row["artist_name"], row["song_title"]
                if not artist or not song or not lyrics:
                    raise ValueError("Missing song identity or transcript")
                audio, sr = sf.read(io.BytesIO(raw), always_2d=True)
                if sr <= 0 or not np.isfinite(audio).all():
                    raise ValueError("Invalid audio samples or sample rate")
                duration = len(audio) / sr
                if not len(audio) or np.max(np.abs(audio)) < 1e-5:
                    excluded.append({"sha256": digest, "reason": "silent audio"})
                    continue
                if duration < 2 or duration > 30:
                    excluded.append({"sha256": digest, "reason": "outside 2-30 second range"})
                    continue
                split = split_for(artist, song)
                groups[split].add((artist.strip().casefold(), song.strip().casefold()))
                path = out / "audio" / (digest + ".wav")
                path.parent.mkdir(exist_ok=True)
                if not path.exists():
                    sf.write(path, audio, sr, subtype="PCM_16")
                samples[split].append({
                    "id": digest, "audio_path": str(path.resolve()), "filename": path.name,
                    "caption": "Solo Kazakh singing, isolated vocal, expressive melodic phrasing.",
                    "genre": "", "lyrics": lyrics, "bpm": None, "keyscale": "",
                    "timesignature": "", "duration": duration, "language": "unknown",
                    "is_instrumental": False, "custom_tag": "", "labeled": True,
                    "prompt_override": None,
                })
    assert all(samples.values()), "Every split must contain samples"
    assert not (groups["train"] & groups["val"] or groups["train"] & groups["test"] or groups["val"] & groups["test"])
    for split, rows in samples.items():
        document = {"metadata": {"name": "assignment2_" + split, "num_samples": len(rows),
                    "custom_tag": "", "tag_position": "prepend", "all_instrumental": False, "genre_ratio": 0}, "samples": rows}
        (out / f"dataset_{split}.json").write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {"dataset": "yeshpanovrustem/kazakh_songs_asr", "revision": REVISION,
              "source_shards": [f.name for f in files], "pilot_subset": args.pilot,
              "restriction": "Non-commercial academic use; keep source audio and transcripts local",
              "split_unit": "artist plus song title; deterministic SHA256 buckets 80/10/10",
              "splits": {s: {"samples": len(r), "songs": len(groups[s]), "seconds": sum(x["duration"] for x in r)} for s, r in samples.items()},
              "excluded": excluded}
    (out / "audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["splits"], indent=2))


if __name__ == "__main__":
    main()
