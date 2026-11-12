"""Validate data/manifests/manifest.json. Exit 1 on errors.
Checks: decodable, silent, clipping, duration, duplicates, lyrics sidecars for vocal crops, Kazakh letters
preserved, split leakage by group_id, instrumental flags, license present.
--selftest round-trips all nine Kazakh-specific letters through the JSON writer/reader the pipeline uses.
"""
import argparse, sys, tempfile
from collections import Counter, defaultdict
from pathlib import Path
from kmm_common import ROOT, ffprobe, ffmpeg_stats, read_json, write_json, KAZAKH_LETTERS

MIN_S, MAX_S, WARN_S = 10.0, 240.0, 30.0  # constants.DURATION_MIN; Side-Step --max-duration; Side-Step tip 30-240 s


def selftest():
    s = "әғқңөұүһі ӘҒҚҢӨҰҮҺІ - Желсіз түнде жарық ай"
    p = Path(tempfile.gettempdir()) / "kmm_kk_roundtrip.json"
    write_json(p, {"lyrics": s})
    back = read_json(p)["lyrics"]
    assert back == s, "Kazakh letters did not survive JSON round-trip"
    raw = p.read_bytes()
    assert "ә".encode("utf-8") in raw and b"\\u04d9" not in raw, "writer escaped non-ASCII (ensure_ascii must be False)"
    print("selftest OK: all Kazakh letters round-trip as UTF-8")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="data/manifests/manifest.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    m = read_json(ROOT / a.manifest)["samples"]
    errs, warns = [], []
    seen_sha, groups = {}, defaultdict(set)
    for s in m:
        sid, p = s["sample_id"], ROOT / s["audio_path"]
        if not p.is_file():
            errs.append(f"{sid}: missing {p}")
            continue
        try:
            info = ffprobe(p)
            st = ffmpeg_stats(p)
        except Exception as e:  # noqa: BLE001
            errs.append(f"{sid}: undecodable ({e})")
            continue
        d = info["duration"]
        if d < MIN_S or d > MAX_S:
            errs.append(f"{sid}: duration {d:.1f}s outside [{MIN_S},{MAX_S}]")
        elif d < WARN_S:
            warns.append(f"{sid}: duration {d:.1f}s < {WARN_S}s (Side-Step recommends 30-240 s)")
        if st["rms_db"] is None or st["rms_db"] < -60:
            errs.append(f"{sid}: silent or near-silent (RMS {st['rms_db']} dB)")
        if st["peak_db"] is not None and st["peak_db"] > -0.1:
            warns.append(f"{sid}: peak {st['peak_db']:.2f} dBFS - possible clipping, check the source")
        if info["sample_rate"] != 48000:
            errs.append(f"{sid}: sample rate {info['sample_rate']} != 48000")
        if s["sha256"] in seen_sha:
            errs.append(f"{sid}: duplicate audio of {seen_sha[s['sha256']]}")
        seen_sha[s["sha256"]] = sid
        groups[s["group_id"]].add(s["split"])
        if s["kind"] == "vocal":
            lp = s.get("lyrics_path")
            if not lp or not (ROOT / lp).is_file():
                errs.append(f"{sid}: vocal crop without lyrics file")
                continue
            txt = (ROOT / lp).read_text(encoding="utf-8").strip()
            if not txt or txt == "[Instrumental]":
                errs.append(f"{sid}: lyrics file empty")
            if not any(c in KAZAKH_LETTERS for c in txt):
                warns.append(f"{sid}: lyrics contain none of әғқңөұүһі - transliterated or wrong language?")
            if s.get("is_instrumental"):
                errs.append(f"{sid}: vocal crop flagged is_instrumental")
        elif s["kind"] == "instrumental" and not s.get("is_instrumental"):
            errs.append(f"{sid}: instrumental crop not flagged")
        if not (s.get("license") and s.get("license_evidence_url")):
            (errs if s["split"] == "train" else warns).append(
                f"{sid}: license or license_evidence_url missing - not allowed in the training set")
    for g, splits in groups.items():
        if len(splits) > 1:
            errs.append(f"group {g} appears in splits {sorted(splits)} - leakage")
    kinds = Counter(s["kind"] for s in m)
    splits = Counter(s["split"] for s in m)
    mins = sum(s["duration_s"] for s in m) / 60
    print(f"{len(m)} samples, {mins:.1f} min total, {len(groups)} independent recordings, "
          f"kinds={dict(kinds)}, splits={dict(splits)}")
    for w in warns:
        print(" WARN ", w)
    for e in errs:
        print(" ERROR", e)
    print("RESULT:", "FAIL" if errs else "OK")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
