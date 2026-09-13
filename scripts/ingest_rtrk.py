"""Ingest the selected RTRK archive files: copy from the download dir into data/raw/rtrk_kazakh_traditional_audio/,
write SOURCE.json (license, provenance, ffprobe, sha256 per file) and a human triage sheet
data/manifests/rtrk_triage.csv (fill 'keep' and 'instrument' by ear before planning crops).
Usage: py -3.12 scripts/ingest_rtrk.py [--src C:\\kmm\\rtrk]
"""
import argparse, csv, datetime, json, shutil, sys
from pathlib import Path
from kmm_common import ROOT, ffprobe, sha256, write_json

SLUG = "rtrk_kazakh_traditional_audio"
CARD = "https://huggingface.co/datasets/rtrk/kazakh-traditional-audio"
LICENSE = "CC BY-NC 4.0 (dataset card: 'non-commercial use only')"
ALLOWED = "non-commercial research and demo only; adapters trained on it must not be released or used commercially; attribute RTRK Kazakhstan"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=r"C:\kmm\rtrk")
    a = ap.parse_args()
    src = Path(a.src)
    sel = json.loads((src / "selection.json").read_text(encoding="utf-8"))
    dest = ROOT / "data" / "raw" / SLUG
    dest.mkdir(parents=True, exist_ok=True)
    files, triage = [], []
    for r in sel:
        f = src / "raw" / "data" / r["file_name"]
        if not f.is_file():
            print("missing (not downloaded):", r["file_name"])
            continue
        out = dest / f.name
        if not out.is_file() or out.stat().st_size != f.stat().st_size:
            shutil.copy2(f, out)
        info = ffprobe(out)
        cat = r["file_name"].split("/")[0]
        files.append({
            "filename": out.name, "category": cat, "title": r["title"], "type": r["type"], "language_metadata": r["language"],
            "url": f"{CARD}/blob/main/data/{r['file_name']}", "performer": "unnamed (RTRK archive)",
            "license": LICENSE, "license_evidence_url": CARD, "allowed_uses": ALLOWED,
            "attribution": "RTRK Kazakhstan JSC, 'Kazakh Traditional Audio Archive', Hugging Face, CC BY-NC 4.0",
            "group_id": f"{SLUG}/{out.stem}", "downloaded_at": datetime.date.today().isoformat(),
            "sha256": sha256(out), "ffprobe": info,
            "lyrics_available": False, "lyrics_location": None,
        })
        triage.append({"filename": out.name, "category": cat, "title": r["title"], "duration_s": round(info["duration"], 1),
                       "keep": "", "instrument": "", "vocal": "", "notes": ""})
        print("ok", out.name, cat, r["title"], f"{info['duration']:.0f}s")
    write_json(dest / "SOURCE.json", {
        "source": "RTRK Kazakh Traditional Audio Archive", "source_slug": SLUG, "source_url": CARD,
        "uploader": "Republican Television and Radio Corporation 'Kazakhstan' JSC (HF org rtrk)",
        "license": LICENSE, "allowed_uses": ALLOWED, "collected_by": "lead session", "downloaded_at": datetime.date.today().isoformat(),
        "note": "Instrumentation and vocal content NOT verified by ear at ingest; see data/manifests/rtrk_triage.csv. No transcripts in the source.",
        "files": files})
    with open(ROOT / "data" / "manifests" / "rtrk_triage.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(triage[0].keys()))
        w.writeheader()
        w.writerows(triage)
    print(f"{len(files)} files -> {dest.relative_to(ROOT)}; SOURCE.json + data/manifests/rtrk_triage.csv written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
