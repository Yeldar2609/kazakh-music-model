"""Shared helpers: project root, ffprobe/ffmpeg wrappers, sha256, provenance lookup. Stdlib only."""
import csv, hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KAZAKH_LETTERS = "әғқңөұүһіӘҒҚҢӨҰҮҺІ"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe(path):
    """Return {duration, sample_rate, channels, codec} or raise."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
         "format=duration:stream=sample_rate,channels,codec_name", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    st = j["streams"][0]
    return {"duration": float(j["format"]["duration"]), "sample_rate": int(st["sample_rate"]),
            "channels": int(st["channels"]), "codec": st["codec_name"]}


def ffmpeg_stats(path):
    """Peak (dBFS) and RMS (dB) over the whole file via ffmpeg astats. Decoding failure raises."""
    r = subprocess.run(["ffmpeg", "-v", "info", "-nostats", "-i", str(path),
                        "-af", "astats=measure_perchannel=none:measure_overall=Peak_level+RMS_level",
                        "-f", "null", "-"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-400:])
    peak = rms = None
    for line in r.stderr.splitlines():
        if "Peak level dB:" in line:
            peak = float(line.split(":")[-1])
        elif "RMS level dB:" in line:
            rms = float(line.split(":")[-1])
    return {"peak_db": peak, "rms_db": rms}


def load_source_provenance(raw_path):
    """Find SOURCE.json in the raw file's folder and return the entry for that file (or {})."""
    src = Path(raw_path).parent / "SOURCE.json"
    if not src.is_file():
        return {"source_slug": Path(raw_path).parent.name}
    data = json.loads(src.read_text(encoding="utf-8"))
    files = data.get("files", []) if isinstance(data, dict) else data
    name = Path(raw_path).name
    for f in files:
        if Path(f.get("filename") or f.get("path") or "").name == name:
            f = dict(f)
            f.setdefault("source_slug", Path(raw_path).parent.name)
            return f
    return {"source_slug": Path(raw_path).parent.name}


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
