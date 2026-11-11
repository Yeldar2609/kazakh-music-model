"""Freeze the small 3-10 second pilot selection after song-level splitting."""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("C:/kmm/assignment2"))
    a = ap.parse_args()
    summary = {}
    for split, count in [("train", 64), ("val", 16), ("test", 16)]:
        document = json.loads((a.root / "prepared_pilot" / f"dataset_{split}.json").read_text(encoding="utf-8"))
        rows = sorted((s for s in document["samples"] if 3 <= s["duration"] <= 10), key=lambda s: s["id"])[:count]
        if len(rows) != count:
            raise ValueError("Not enough eligible clips for the fixed pilot")
        document["samples"] = rows
        document["metadata"]["num_samples"] = count
        (a.root / f"pilot_{split}_64.json").write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")
        summary[split] = {"count": count, "seconds": sum(s["duration"] for s in rows), "sample_ids": [s["id"] for s in rows]}
    sets = [set(v["sample_ids"]) for v in summary.values()]
    assert not (sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
    (a.root / "pilot_selection.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("Selected 64 training, 16 validation and 16 test clips")


if __name__ == "__main__":
    main()
