"""Check the offline deck's assets, selected audio provenance and slide structure."""
import sys
import hashlib
import json
import soundfile as sf
from html.parser import HTMLParser
from pathlib import Path

root = Path(__file__).resolve().parents[1] / (sys.argv[1] if len(sys.argv)>1 else "presentation-website")


class Deck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.slides, self.assets, self.audio = [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "section" and "slide" in a.get("class", "").split():
            self.slides.append(a)
        if tag in {"script", "audio", "img"} and "src" in a:
            self.assets.append(a["src"])
        if tag == "link" and a.get("rel") == "stylesheet":
            self.assets.append(a["href"])
        if tag == "audio":
            assert "autoplay" not in a
            self.audio.append(a)


page = Deck()
page.feed((root / "index.html").read_text(encoding="utf-8"))
assert len(page.ids) == len(set(page.ids)), "Duplicate HTML IDs"
expected_count = 10 if root.name == "presentation-stage" else 9
assert [s["id"] for s in page.slides] == [f"slide-{i}" for i in range(1, expected_count + 1)]
assert all(s["aria-labelledby"] in page.ids and s.get("data-speaker") for s in page.slides)
assert all("hidden" in s and "inert" in s for s in page.slides[1:])
assert len(page.audio) == 2
assert all(not a.startswith(("http:", "https:", "//")) and (root / a).is_file() for a in page.assets)
evidence = json.loads((root / "evidence.json").read_text())
assert evidence["presenters"] == (["Yeldar", "Aisha", "Dimash"] if root.name == "presentation-stage" else ["Yeldar", "Aisha"])
assert evidence["audio"]["selected"]["variant"] == "audio_scale_025/B_verse_simple"
for name, record in evidence["audio"].items():
    path = root / "audio" / (name + ".wav")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
    info = sf.info(path)
    assert info.channels == 2 and info.samplerate == 48000
    assert info.duration == 30
data = (root / "waveforms.js").read_text().removeprefix("window.KMM_WAVEFORMS = ").strip().removesuffix(";")
assert all(len(values) == 120 and all(0 <= v <= 1 for v in values) for values in json.loads(data).values())
print(f"PASS: {expected_count} slides, offline dependencies, exact selected audio, durations and waveform data")

if root.name == "presentation-stage":
    html = (root / "index.html").read_text(encoding="utf-8")
    assert not any(x in html.lower() for x in ["owner", "assignment 02", "12 nov 2026", 'id="overview"', 'id="notes"', 'class="controls"'])
    proof = json.loads((root / "proof/verified-run.json").read_text())
    assert hashlib.sha256((root / "proof/training-steps.jsonl").read_bytes()).hexdigest() == proof["training_log_sha256"]
    assert proof["updates"] == 3088 and len(proof["checkpoints"]) == 4

if root.name == "presentation-stage":
    assert not any(x in html.lower() for x in ["sample d", "preferred", "preference", "listening choice"])
    assert all((root / "proof" / n).is_file() for n in ["song-triage.csv", "data-validation-code.py", "generation-settings.json", "model-choice.md"])
