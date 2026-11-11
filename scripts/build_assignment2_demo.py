"""Package only generated audio and aggregate experiment results for offline class use."""
import argparse
import html
import json
import shutil
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("C:/kmm/assignment2"))
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.out.exists():
        ap.error("Use a new versioned output folder")
    variants = [("Pretrained", "audio_final_pretrained"),
                ("Original data", "audio_final_original"),
                ("Enriched data", "audio_final_enriched")]
    cases = [("A_dombra_solo", "Dombra instrumental"), ("B_verse_simple", "Simple Kazakh vocal"),
             ("C_verse_dombra_led", "Dombra-led Kazakh vocal")]
    sources = []
    for label, folder in variants:
        for case, title in cases:
            paths = list((a.root / folder / case).glob("*.wav"))
            if len(paths) != 1:
                raise ValueError(f"Expected one generated WAV for {folder}/{case}")
            sources.append((folder, case, paths[0]))
    evaluation = json.loads((a.root / "evaluation_test.json").read_text())
    a.out.mkdir(parents=True)
    (a.out / "audio").mkdir()
    for folder, case, source in sources:
        shutil.copy2(source, a.out / "audio" / f"{folder}_{case}.wav")
    metric_rows = "".join(f"<tr><th scope='row'>{html.escape(label)}</th><td>{row['mean_flow_loss']:.4f}</td></tr>"
                          for (label, _), row in zip(variants, evaluation["results"]))
    sections = []
    for case, title in cases:
        cards = []
        for label, folder in variants:
            src = f"audio/{folder}_{case}.wav"
            cards.append(f"<article><h3>{label}</h3><audio controls preload='metadata' aria-label='{label}: {title}' src='{src}'></audio><a href='{src}' download>Download WAV</a></article>")
        metadata = json.loads((a.root / "audio_final_pretrained" / (case + ".json")).read_text(encoding="utf-8"))
        lyrics = html.escape(metadata["lyrics"])
        sections.append(f"<section><h2>{title}</h2><div class='grid'>{''.join(cards)}</div><details><summary>Prompt and target lyrics</summary><p>{html.escape(metadata['caption'])}</p><pre>{lyrics}</pre></details></section>")
    document = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kazakh Music Model | Assignment 2</title><style>
:root{color-scheme:light;--bg:#f7f7f5;--panel:#fff;--text:#17181a;--muted:#4f5358;--line:#cfd2d6;--accent:#0b5cad}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:17px/1.55 system-ui,Arial,sans-serif}
main{max-width:1200px;margin:auto;padding:40px 24px}h1{font-size:clamp(30px,4vw,48px);line-height:1.15}h2{margin-top:0}h3{font-size:19px}
header{margin-bottom:40px}.muted{color:var(--muted)}.notice{padding:16px;background:#fff2c2;border-left:4px solid #c99a00}
section{margin:32px 0;padding:26px;background:var(--panel);border:1px solid var(--line);border-radius:8px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
audio{display:block;width:100%;margin:12px 0}a{color:var(--accent)}details{margin-top:24px}summary{cursor:pointer}pre{white-space:pre-wrap;font:inherit}
table{border-collapse:collapse;width:100%;max-width:600px}th,td{padding:10px;text-align:left;border-bottom:1px solid var(--line)}:focus-visible{outline:3px solid #e98200;outline-offset:3px}
@media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:24px 16px}section{padding:20px}}
</style><main><header><p class="muted">Assignment 2 · Local research pilot · 11 November 2026</p><h1>Kazakh music: listen to the experiment</h1>
<p>Can aligned sung lyrics improve a small music-model adapter?</p><p class="notice">These are prerecorded AI-generated examples. Pronunciation and musical quality have not been verified by a Kazakh listener.</p></header>
<section><h2>The controlled comparison</h2><p>Pretrained reference, 100 updates on original data, and 100 updates alternating original and new vocal data. All use the same NF4 base, rank-8 adapter setting, seed 1001, 15-second duration and eight generation steps.</p>
<p>The new pilot selected 64 vocal training clips from three downloaded dataset shards. The 100-update enriched run uses 50 new-vocal and 50 original-data updates. Validation and test each contain 16 clips from separate songs.</p></section>
<section><h2>Held-out test result</h2><p>Mean flow-matching error on 16 test clips; lower is better for this objective.</p><table><thead><tr><th>Model</th><th>Mean error</th></tr></thead><tbody>METRIC_ROWS</tbody></table><p class="muted">This is not a pronunciation accuracy or music-quality score. One pilot run and one noise draw per clip do not establish a general improvement.</p></section>
SECTIONS
<section><h2>How to assess the audio</h2><p>Compare the same row at the same volume. Check which target words you can hear, whether the phrasing sounds natural, and whether the accompaniment fits. Record failures as well as preferences.</p>
<p>Source dataset: <a href="https://huggingface.co/datasets/yeshpanovrustem/kazakh_songs_asr">Kazakh Songs ASR</a>. Its restricted recordings and transcripts are not included in this package. Use this demonstration for the non-commercial class project.</p></section>
<footer><p>ACE-Step 1.5 + local LoRA adaptation. The foundation model was pretrained; this project trains a small adapter.</p></footer></main></html>"""
    document = document.replace("METRIC_ROWS", metric_rows).replace("SECTIONS", "".join(sections))
    (a.out / "index.html").write_text(document, encoding="utf-8")
    assert len(list((a.out / "audio").glob("*.wav"))) == 9
    print(a.out / "index.html")


if __name__ == "__main__":
    main()
