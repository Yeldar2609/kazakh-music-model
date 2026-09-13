#!/usr/bin/env python3
"""Build viewer/manifest.json + viewer/manifest.js from saved outputs.

Scans (project-relative, override with --outputs-root):
    outputs/baseline/<case_id>/<case_id>_seed<seed>.wav  (+ .json sidecar)
    outputs/adapter/<case_id>/<case_id>_seed<seed>.wav   (+ .json sidecar)
    outputs/human_reference/<case_id>/*.wav              (sidecar optional)

Reads the case list from configs/eval_cases.json and pins from configs/pins.json.
Preserves listening_notes from an existing viewer/manifest.json (merge key:
case + label + seed, plus wav filename as tiebreaker), and can merge notes
exported from the viewer via --notes <exported.json>.

Writes viewer/manifest.json and viewer/manifest.js (`window.KMM_MANIFEST = ...;`)
because Chrome cannot fetch JSON from a file:// page.

Run:  py -3.12 scripts/build_viewer_manifest.py
Never writes audio. Never deletes anything.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path, PurePosixPath

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LABEL_DIRS = ["baseline", "adapter", "human_reference"]
SIDECAR_FIELDS = [
    "case_id", "caption", "lyrics", "vocal_language", "seed", "duration",
    "inference_steps", "shift", "model_variant", "engine_commit",
    "checkpoint_revision", "adapter", "wall_time_s", "peak_vram_bytes",
]
DATE_KEYS = ["generated_at", "generated_on", "timestamp", "created_at", "date"]
SEED_RE = re.compile(r"_seed(\d+)$")


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def file_date(path: Path) -> str:
    ts = path.stat().st_mtime
    return dt.datetime.fromtimestamp(ts).isoformat(timespec="seconds")


def load_cases(config_path: Path):
    cfg = read_json(config_path)
    cases = []
    for c in cfg["cases"]:
        lyrics = c.get("lyrics")
        lyrics_reviewed = None
        lyrics_source = None
        if lyrics is None and c.get("lyrics_file"):
            lf = PROJECT_ROOT / c["lyrics_file"]
            if lf.exists():
                lyrics = lf.read_text(encoding="utf-8")
                lyrics_source = c["lyrics_file"]
                meta = lf.with_suffix("").with_suffix(".meta.json")
                if meta.exists():
                    m = read_json(meta)
                    lyrics_reviewed = m.get("reviewed_by_kazakh_speaker")
                    lyrics_source = m.get("source", lyrics_source)
            else:
                lyrics = f"(lyrics file missing: {c['lyrics_file']})"
        cases.append({
            "id": c["id"],
            "kind": c.get("kind"),
            "caption": c.get("caption", ""),
            "lyrics": lyrics or "",
            "lyrics_source": lyrics_source,
            "lyrics_reviewed_by_kazakh_speaker": lyrics_reviewed,
            "language": cfg.get("vocal_language", "unknown"),
            "instrumental": bool(c.get("instrumental")),
            "entries": [],
        })
    settings = {
        "model_variant": cfg.get("model_variant"),
        "inference_steps": cfg.get("inference_steps"),
        "shift": cfg.get("shift"),
        "guidance_scale": cfg.get("guidance_scale"),
        "duration_seconds": cfg.get("duration_seconds"),
        "seeds": list(cfg.get("seeds", [])),
        "vocal_language": cfg.get("vocal_language", "unknown"),
    }
    return cases, settings


def merge_key(case_id: str, label: str, seed, wav: str) -> str:
    return f"{case_id}|{label}|{seed}|{PurePosixPath(wav).name}"


def scan_entries(outputs_root: Path, viewer_dir: Path, case_id: str):
    entries = []
    for label in LABEL_DIRS:
        d = outputs_root / label / case_id
        if not d.is_dir():
            continue
        stems = sorted({p.stem for p in d.glob("*.wav")} | {p.stem for p in d.glob("*.json")})
        for stem in stems:
            wav = d / f"{stem}.wav"
            wav_missing = not wav.exists()
            sidecar_path = wav.with_suffix(".json")
            sidecar = None
            sidecar_error = None
            if sidecar_path.exists():
                try:
                    sidecar = read_json(sidecar_path)
                except (OSError, ValueError) as e:
                    sidecar_error = f"{type(e).__name__}: {e}"
            m = SEED_RE.search(wav.stem)
            seed = None
            if sidecar and sidecar.get("seed") is not None:
                seed = sidecar["seed"]
            elif m:
                seed = int(m.group(1))
            gen_on, gen_src = None, None
            if sidecar:
                for k in DATE_KEYS:
                    if sidecar.get(k):
                        gen_on, gen_src = str(sidecar[k]), f"sidecar.{k}"
                        break
            if gen_on is None and not wav_missing:
                gen_on, gen_src = file_date(wav), "wav file mtime"
            if gen_on is None and sidecar_path.exists():
                gen_on, gen_src = file_date(sidecar_path), "sidecar file mtime"
            fields = {k: (sidecar.get(k) if sidecar else None) for k in SIDECAR_FIELDS}
            try:
                rel = PurePosixPath(Path("..") / wav.relative_to(viewer_dir.parent)).as_posix()
            except ValueError:
                rel = wav.resolve().as_uri()
            entries.append({
                "label": label,
                "seed": seed,
                "wav": rel,
                "wav_missing": wav_missing,
                "wav_bytes": None if wav_missing else wav.stat().st_size,
                "generated_on": gen_on,
                "generated_on_source": gen_src,
                "sidecar_missing": sidecar is None,
                "sidecar_error": sidecar_error,
                "sidecar": fields,
                "listening_notes": "",
            })
    return entries


def load_existing_notes(viewer_dir: Path) -> dict[str, str]:
    notes: dict[str, str] = {}
    p = viewer_dir / "manifest.json"
    if not p.exists():
        return notes
    try:
        old = read_json(p)
    except (OSError, ValueError) as e:
        print(f"warning: could not read existing {p}: {e}", file=sys.stderr)
        return notes
    for c in old.get("cases", []):
        for e in c.get("entries", []):
            n = e.get("listening_notes") or ""
            if n:
                notes[merge_key(c["id"], e["label"], e.get("seed"), e.get("wav", ""))] = n
    return notes


def load_exported_notes(path: Path) -> dict[str, str]:
    """Viewer export shape: [{case, label, seed, wav, listening_notes}] or {wav: note}."""
    data = read_json(path)
    notes: dict[str, str] = {}
    if isinstance(data, dict) and "notes" in data:
        data = data["notes"]
    if isinstance(data, list):
        for e in data:
            n = e.get("listening_notes") or ""
            if n:
                notes[merge_key(e["case"], e["label"], e.get("seed"), e.get("wav", ""))] = n
    elif isinstance(data, dict):
        for wav, n in data.items():
            if n:
                notes[f"wav:{PurePosixPath(wav).name}"] = n
    return notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outputs-root", default=str(PROJECT_ROOT / "outputs"))
    ap.add_argument("--viewer-dir", default=str(PROJECT_ROOT / "viewer"))
    ap.add_argument("--cases", default=str(PROJECT_ROOT / "configs" / "eval_cases.json"))
    ap.add_argument("--pins", default=str(PROJECT_ROOT / "configs" / "pins.json"))
    ap.add_argument("--notes", default=None, help="JSON exported from the viewer's 'Export notes' button; merged into listening_notes")
    args = ap.parse_args(argv)

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    outputs_root = Path(args.outputs_root).resolve()
    viewer_dir = Path(args.viewer_dir).resolve()
    viewer_dir.mkdir(parents=True, exist_ok=True)

    cases, settings = load_cases(Path(args.cases))
    pins = {}
    if Path(args.pins).exists():
        p = read_json(Path(args.pins))
        pins = {
            "engine_revision": p.get("engine", {}).get("revision"),
            "checkpoint_revision": p.get("checkpoint", {}).get("revision"),
            "checkpoint_repo": p.get("checkpoint", {}).get("hf_repo"),
        }

    old_notes = load_existing_notes(viewer_dir)
    exported = load_exported_notes(Path(args.notes)) if args.notes else {}

    seeds = set(settings["seeds"])
    total = 0
    for c in cases:
        c["entries"] = scan_entries(outputs_root, viewer_dir, c["id"])
        for e in c["entries"]:
            k = merge_key(c["id"], e["label"], e["seed"], e["wav"])
            n = exported.get(k) or exported.get(f"wav:{PurePosixPath(e['wav']).name}") or old_notes.get(k) or ""
            e["listening_notes"] = n
            if e["seed"] is not None and e["label"] != "human_reference":
                seeds.add(e["seed"])
        total += len(c["entries"])

    manifest = {
        "_note": "Generated by scripts/build_viewer_manifest.py. Human reference recordings are NOT generated; the viewer labels them separately.",
        "built_at": dt.datetime.now().isoformat(timespec="seconds"),
        "outputs_root": outputs_root.as_posix(),
        "settings": settings,
        "pins": pins,
        "seeds": sorted(seeds),
        "cases": cases,
    }

    write_json(viewer_dir / "manifest.json", manifest)
    js = "window.KMM_MANIFEST = " + json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n"
    with (viewer_dir / "manifest.js").open("w", encoding="utf-8", newline="\n") as f:
        f.write(js)

    print(f"wrote {viewer_dir / 'manifest.json'} and manifest.js: {len(cases)} cases, {total} entries, seeds {sorted(seeds)}")
    for c in cases:
        by = {}
        for e in c["entries"]:
            by[e["label"]] = by.get(e["label"], 0) + 1
        print(f"  {c['id']}: " + (", ".join(f"{k}={v}" for k, v in sorted(by.items())) or "no saved outputs"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
