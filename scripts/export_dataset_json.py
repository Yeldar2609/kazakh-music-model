"""manifest.json -> ACE-Step / Side-Step dataset JSON (full format, docs/sidestep/Dataset Preparation.md).
Writes data/processed/dataset_<split>.json; audio_path is relative to that JSON's directory.
language is always "unknown" (no Kazakh code in acestep/constants.py); bpm/keyscale/timesignature stay unknown.
Samples without license evidence are skipped."""
import argparse, datetime, sys
from pathlib import Path
from kmm_common import ROOT, read_json, write_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="data/manifests/manifest.json")
    ap.add_argument("--custom-tag", default="")
    a = ap.parse_args()
    m = read_json(ROOT / a.manifest)["samples"]
    out_dir = ROOT / "data" / "processed"
    for split in sorted({s["split"] for s in m}):
        ok = lambda s: s.get("license") and s.get("license_evidence_url")  # noqa: E731
        rows = [s for s in m if s["split"] == split and ok(s)]
        skipped = [s["sample_id"] for s in m if s["split"] == split and not ok(s)]
        samples = []
        for s in rows:
            lyrics = "[Instrumental]" if s["is_instrumental"] else (ROOT / s["lyrics_path"]).read_text(encoding="utf-8").strip()
            samples.append({
                "id": s["sample_id"],
                "audio_path": "./" + Path(s["audio_path"]).relative_to("data/processed").as_posix(),
                "filename": Path(s["audio_path"]).name,
                "caption": s["caption"],
                "genre": "",
                "lyrics": lyrics,
                "bpm": None,
                "keyscale": "",
                "timesignature": "",
                "duration": s["duration_s"],
                "language": "unknown",
                "is_instrumental": bool(s["is_instrumental"]),
                "custom_tag": a.custom_tag,
                "labeled": True,
                "prompt_override": None,
            })
        doc = {
            "metadata": {
                "name": f"kmm_{split}",
                "custom_tag": a.custom_tag,
                "tag_position": "prepend",
                "created_at": datetime.datetime.now().isoformat(),
                "num_samples": len(samples),
                "all_instrumental": all(x["is_instrumental"] for x in samples) if samples else True,
                "genre_ratio": 0,
            },
            "samples": samples,
        }
        write_json(out_dir / f"dataset_{split}.json", doc)
        print(f"{split}: {len(samples)} samples -> data/processed/dataset_{split}.json"
              + (f"  (skipped, no license: {skipped})" if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
