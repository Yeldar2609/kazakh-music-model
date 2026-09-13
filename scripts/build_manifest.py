"""Crop raw recordings per data/manifests/crop_plan.csv into data/processed/ and write the manifest.

crop_plan.csv columns: sample_id, raw_path (project-relative), start_s, end_s, kind (instrumental|vocal),
split (train|val), caption, lyrics_path (project-relative .txt for vocal crops: the words sung IN THIS CROP only), notes,
group_id (optional; same value for different recordings of the same song so they never straddle splits).
Processing is deliberately minimal: cut + resample to 48 kHz (model requirement) + PCM 16-bit. No normalisation,
no filters. Raw files are never modified. Re-running overwrites processed crops deterministically.
"""
import argparse, csv, subprocess, sys
from kmm_common import ROOT, ffprobe, sha256, load_source_provenance, read_csv, write_json, KAZAKH_LETTERS

TARGET_SR = 48000  # acestep/training_v2/preprocess_vae.py: TARGET_SR = 48000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default="data/manifests/crop_plan.csv")
    ap.add_argument("--out", default="data/manifests/manifest.json")
    args = ap.parse_args()
    rows = read_csv(ROOT / args.plan)
    if not rows:
        print("crop plan is empty - nothing to do")
        return 0
    samples, errors = [], []
    for r in rows:
        sid = r["sample_id"].strip()
        raw = ROOT / r["raw_path"].strip()
        if not raw.is_file():
            errors.append(f"{sid}: raw file missing {raw}")
            continue
        start, end = float(r["start_s"]), float(r["end_s"])
        out = ROOT / "data" / "processed" / f"{sid}.wav"
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", str(raw),
               "-ar", str(TARGET_SR), "-c:a", "pcm_s16le", str(out)]
        if subprocess.run(cmd).returncode != 0:
            errors.append(f"{sid}: ffmpeg crop failed")
            continue
        info = ffprobe(out)
        prov = load_source_provenance(raw)
        kind = r["kind"].strip().lower()
        lyrics_path = (r.get("lyrics_path") or "").strip()
        lyrics_text = None
        if kind == "vocal":
            if not lyrics_path or not (ROOT / lyrics_path).is_file():
                errors.append(f"{sid}: vocal crop needs lyrics_path")
                continue
            lyrics_text = (ROOT / lyrics_path).read_text(encoding="utf-8").strip()
        samples.append({
            "sample_id": sid,
            "audio_path": out.relative_to(ROOT).as_posix(),
            "raw_path": raw.relative_to(ROOT).as_posix(),
            "original_filename": raw.name,
            "source_url": prov.get("url"),
            "performer": prov.get("performer"),
            "license": prov.get("license"),
            "license_evidence_url": prov.get("license_evidence_url"),
            "allowed_uses": prov.get("allowed_uses"),  # only what SOURCE.json states; never invented
            "group_id": (r.get("group_id") or "").strip() or prov.get("group_id") or f"{prov.get('source_slug', 'raw')}/{raw.stem}",
            "crop_start_s": start,
            "crop_end_s": end,
            "duration_s": round(info["duration"], 3),
            "sample_rate": info["sample_rate"],
            "channels": info["channels"],
            "kind": kind,
            "is_instrumental": kind == "instrumental",
            "sung_language": None if kind == "instrumental" else "Kazakh (kk)",
            "acestep_language_code": "unknown",
            "caption": r["caption"].strip(),
            "lyrics_path": lyrics_path or None,
            "lyrics_has_kazakh_letters": bool(lyrics_text and any(ch in KAZAKH_LETTERS for ch in lyrics_text)),
            "sha256": sha256(out),
            "split": r["split"].strip().lower(),
            "notes": r.get("notes", ""),
        })
        print(f"ok  {sid}  {info['duration']:.1f}s  {kind}  split={r['split']}")
    write_json(ROOT / args.out, {"target_sample_rate": TARGET_SR, "samples": samples})
    if samples:  # CSV twin for humans
        with open(ROOT / args.out.replace(".json", ".csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(samples[0].keys()))
            w.writeheader()
            w.writerows(samples)
    print(f"wrote {len(samples)} samples -> {args.out}; {len(errors)} errors")
    for e in errors:
        print(" ERROR", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
