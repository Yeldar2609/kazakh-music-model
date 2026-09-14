#!/usr/bin/env python
"""Write viewer/triage_data.js from data/manifests/rtrk_triage.csv for the offline triage page (viewer/triage.html).

Existing keep/instrument/vocal/notes values in the CSV are carried into the page, so a partly filled sheet
can be continued. Also flags whether a candidate lyric text and a Whisper draft exist for each file.
Usage: py -3.12 scripts/build_triage_page_data.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "manifests" / "rtrk_triage.csv"
OUT = ROOT / "viewer" / "triage_data.js"


def main():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as fh:  # the sheet may carry a BOM from spreadsheet tools
        rows = list(csv.DictReader(fh))
    for r in rows:
        stem = Path(r["filename"]).stem
        r["audio_rel"] = f"../data/raw/rtrk_kazakh_traditional_audio/{r['filename']}"
        r["has_candidate_lyrics"] = (ROOT / "data" / "lyrics" / "candidates" / f"{stem}.txt").is_file()
        r["has_whisper_draft"] = (ROOT / "data" / "lyrics" / "drafts" / f"{stem}.draft.txt").is_file()
    OUT.write_text("window.TRIAGE_ROWS = " + json.dumps(rows, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} files")


if __name__ == "__main__":
    main()
