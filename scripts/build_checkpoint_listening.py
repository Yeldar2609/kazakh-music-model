"""Build a blind, offline listening sheet for the completed full-data checkpoints."""
import argparse
import hashlib
import html
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, default=Path("C:/kmm/assignment2/full_v1"))
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        ap.error("Use a new output folder")
    variants = ["audio_pretrained", "audio_step_772", "audio_step_1544", "audio_step_3088"]
    cases = json.loads((ROOT / "configs/assignment2_full_eval_cases.json").read_text(encoding="utf-8"))["cases"]
    sources = {(v, c["id"]): list((a.run / v / c["id"]).glob("*.wav")) for v in variants for c in cases}
    if any(len(paths) != 1 for paths in sources.values()):
        raise ValueError("All twelve checkpoint/reference WAVs must exist")
    completion = json.loads((a.run / "COMPLETE.json").read_text())
    assert completion["new_unique_clips"] == 2316 and completion["updates"] == 3088
    import numpy as np
    import soundfile as sf
    audio_checks = {}
    for case in cases:
        reference = None
        hashes = set()
        for variant in variants:
            path = sources[(variant, case["id"])][0]
            samples, rate = sf.read(path)
            assert np.isfinite(samples).all() and np.max(np.abs(samples)) > 0, path
            assert abs(len(samples) / rate - 30) < 0.1, path
            record = json.loads((a.run / variant / (case["id"] + ".json")).read_text(encoding="utf-8"))
            settings = {key: record[key] for key in ("caption", "lyrics", "seed", "duration_seconds", "steps", "shift", "quantization")}
            if reference is None:
                reference = settings
            assert settings == reference, "Checkpoint generation settings differ"
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            hashes.add(digest)
            audio_checks[variant + "/" + case["id"]] = {"source_sha256": digest, "seconds": len(samples) / rate, "sample_rate": rate, "source_rms": float(np.sqrt(np.mean(samples * samples)))}
        assert len(hashes) == 4, "Identical checkpoint audio requires investigation"
    a.out.mkdir(parents=True)
    (a.out / "audio").mkdir()
    rng = random.Random(20261111)
    sections, key = [], {}
    for case in cases:
        target_rms = min(audio_checks[v + "/" + case["id"]]["source_rms"] for v in variants)
        order = variants.copy()
        rng.shuffle(order)
        cards = []
        for label, variant in zip("ABCD", order):
            item = case["id"] + "_" + label
            key[item] = variant
            source = sources[(variant, case["id"])][0]
            check = audio_checks[variant + "/" + case["id"]]
            gain = target_rms / check["source_rms"]
            samples, rate = sf.read(source)
            destination = a.out / "audio" / (item + ".wav")
            # Attenuation only keeps louder examples from winning just on playback level.
            sf.write(destination, samples * gain, rate, subtype=sf.info(source).subtype)
            playback, _ = sf.read(destination)
            assert abs(float(np.sqrt(np.mean(playback * playback))) - target_rms) < 0.0001
            check.update({"playback_gain": gain, "playback_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(), "blind_label": item})
            options = '<option value="">Not rated</option>' + ''.join(f'<option value="{n}">{n}</option>' for n in range(1, 6))
            cards.append(f'<article><h3>Sample {label}</h3><audio controls preload="metadata" src="audio/{item}.wav" aria-label="{item}"></audio>'
                         f'<label>Overall sound, 1 poor to 5 good <select name="{item}_score">{options}</select></label>'
                         f'<label>What sounds good or wrong? <textarea name="{item}_notes" rows="3"></textarea></label></article>')
        sections.append(f'<section><h2>{html.escape(case["id"].replace("_", " "))}</h2><p>{html.escape(case["caption"])}</p>'
                        f'<div class="grid">{"".join(cards)}</div><details><summary>Target lyrics</summary><pre>{html.escape(case.get("lyrics", ""))}</pre></details></section>')
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kazakh music checkpoint listening</title>
<style>body{font:17px/1.5 system-ui,sans-serif;background:#f7f7f5;color:#17181a;margin:0}main{max-width:1250px;margin:auto;padding:32px 20px}h1{line-height:1.2}section{background:white;border:1px solid #cfd2d6;padding:24px;margin:28px 0;border-radius:8px}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}audio,select,textarea{width:100%;box-sizing:border-box}label{display:block;margin:16px 0}textarea,select,button{font:inherit}button{padding:10px 18px;cursor:pointer}pre{white-space:pre-wrap;font:inherit}.note{background:#fff2c2;padding:16px}:focus-visible{outline:3px solid #e98200;outline-offset:3px}@media(max-width:1000px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){.grid{grid-template-columns:1fr}}</style>
<main><h1>Which checkpoint actually sounds better?</h1><p>Compare samples within the same row. Each uses the same prompt, verse, seed and 30-second duration. Labels are shuffled separately for each row.</p>
<p>Playback copies have matching average signal levels within each row, so louder output has less advantage. Original generated files remain unchanged. This matches RMS level, not exact perceived loudness.</p>
<p class="note">Choose by sound: clear words, pleasant melody, natural phrasing, accompaniment and absence of glitches. You can prefer the pretrained version or reject every version. Model loss is deliberately absent.</p>
<form id="ratings">SECTIONS</form><button id="export" type="button">Download my listening notes</button><p id="status" role="status">Ratings are saved in this browser when available. Export a copy before closing.</p>
<details><summary>Reveal checkpoint identities after listening</summary><pre id="key"></pre></details>
<p>These are generated research examples, not source recordings. No model is declared best before listening.</p></main>
<script>
const mapping=KEY, form=document.getElementById('ratings'), storageKey='kmm-full-v1-listening';
document.getElementById('key').textContent=JSON.stringify(mapping,null,2);
try{const saved=JSON.parse(localStorage.getItem(storageKey)||'{}');for(const el of form.elements){if(saved[el.name]!==undefined)el.value=saved[el.name];}}catch(e){document.getElementById('status').textContent='Browser storage unavailable. Export notes before closing.';}
function values(){return Object.fromEntries(new FormData(form));}
form.addEventListener('input',()=>{try{localStorage.setItem(storageKey,JSON.stringify(values()));}catch(e){document.getElementById('status').textContent='Could not save in browser. Export notes before closing.';}});
document.getElementById('export').addEventListener('click',()=>{const blob=new Blob([JSON.stringify({run:'full_v1',ratings:values(),mapping},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='checkpoint-listening-notes.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause();})));
</script></html>'''
    (a.out / "index.html").write_text(document.replace("SECTIONS", ''.join(sections)).replace("KEY", json.dumps(key)), encoding="utf-8")
    (a.out / "verification.json").write_text(json.dumps({"training": completion, "audio": audio_checks}, indent=2))
    assert len(list((a.out / "audio").glob("*.wav"))) == 12
    print(a.out / "index.html")


if __name__ == "__main__":
    main()
