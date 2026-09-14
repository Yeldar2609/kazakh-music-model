#!/usr/bin/env python
"""Add instrumental crops for RTRK kui marked 'dombra solo' by ear to data/manifests/crop_plan.csv.

Selection comes only from the human triage sheet data/manifests/rtrk_triage.csv:
category=kui, keep=y, instrument=dombra solo, vocal=n. Vocal RTRK files are NOT added here: they need
reviewed crop-specific transcripts first (CLAUDE.md ground rules).

Crops: 36 s, two per recording (one if the file is shorter than 82 s), placed at ~20 % and ~58 % of the
duration, never in the first 5 s or last 3 s. A window whose RMS is below -40 dBFS is moved forward in 4 s
steps (archival broadcasts can start or pause in silence). Each recording is its own group_id (SOURCE.json);
--val recordings go entirely to split=val. Re-running replaces earlier rtrk_ rows, other rows are kept.
Usage: C:\\kmm\\venv-acestep\\Scripts\\python.exe scripts/plan_rtrk_crops.py [--val kui_010.wav kui_050.wav]
"""
import argparse
import csv
import random
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
TRIAGE = ROOT / "data" / "manifests" / "rtrk_triage.csv"
PLAN = ROOT / "data" / "manifests" / "crop_plan.csv"
RAW_DIR = "data/raw/rtrk_kazakh_traditional_audio"
CROP_S, HEAD_S, TAIL_S, MIN_RMS_DB = 36.0, 5.0, 3.0, -40.0
CAPTION = "solo dombra, Kazakh kui, two-string plucked lute, unaccompanied, archival broadcast recording"
COLS = ["sample_id", "raw_path", "start_s", "end_s", "kind", "split", "caption", "lyrics_path", "notes", "group_id"]


def rms_db(audio, sr, start):
    seg = audio[int(start * sr):int((start + CROP_S) * sr)]
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12)


def place(audio, sr, duration, frac, not_before):
    start = max(HEAD_S, not_before, round(duration * frac, 1))
    last = duration - TAIL_S - CROP_S
    while start <= last:
        if rms_db(audio, sr, start) >= MIN_RMS_DB:
            return round(start, 1)
        start += 4.0
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--val", nargs="*", default=None, help="kui filenames held out (default: 2 picked with seed 42)")
    ap.add_argument("--dense", action="store_true",
                    help="tile each recording with back-to-back 36 s crops (2 s apart) instead of two crops per file; "
                         "same recordings, more of each one is used (dataset v3)")
    args = ap.parse_args()

    with open(TRIAGE, encoding="utf-8-sig", newline="") as fh:
        kept = [r for r in csv.DictReader(fh)
                if r["category"] == "kui" and r["keep"] == "y" and r["instrument"] == "dombra solo" and r["vocal"] == "n"]
    val = set(args.val) if args.val is not None else set(random.Random(42).sample(sorted(r["filename"] for r in kept), 2))

    with open(PLAN, encoding="utf-8-sig", newline="") as fh:
        plan = [r for r in csv.DictReader(fh) if not r["sample_id"].startswith("rtrk_")]

    added, skipped = [], []
    for r in kept:
        stem = Path(r["filename"]).stem
        audio, sr = sf.read(ROOT / RAW_DIR / r["filename"], dtype="float32", always_2d=True)
        audio = audio.mean(axis=1)
        duration = len(audio) / sr
        starts, not_before = [], 0.0
        if args.dense:
            while True:
                s = place(audio, sr, duration, 0.0, not_before)
                if s is None:
                    break
                starts.append(s)
                not_before = s + CROP_S + 2.0
        else:
            fracs = (0.20, 0.58) if duration >= 82 else (0.30,)
            for frac in fracs:
                s = place(audio, sr, duration, frac, not_before)
                if s is not None:
                    starts.append(s)
                    not_before = s + CROP_S + 2.0
        if not starts:
            skipped.append(r["filename"])
            continue
        split = "val" if r["filename"] in val else "train"
        for n, s in enumerate(starts, 1):
            added.append({
                "sample_id": f"rtrk_{stem}_{n:02d}", "raw_path": f"{RAW_DIR}/{r['filename']}",
                "start_s": f"{s:.1f}", "end_s": f"{s + CROP_S:.1f}", "kind": "instrumental", "split": split,
                "caption": CAPTION, "lyrics_path": "",
                "notes": f"kui '{r['title']}'; dombra solo confirmed by ear in rtrk_triage.csv; crop {n} of {len(starts)}"
                         + ("; held-out validation recording" if split == "val" else ""),
                "group_id": f"rtrk_kazakh_traditional_audio/{stem}",
            })

    with open(PLAN, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(plan + added)
    n_val = sum(a["split"] == "val" for a in added)
    print(f"kept kui recordings: {len(kept)}; crops added: {len(added)} ({len(added) - n_val} train / {n_val} val); "
          f"val recordings: {sorted(val)}; skipped (no non-silent window): {skipped}")


if __name__ == "__main__":
    main()
