"""Re-download every raw source recording listed in data/manifests/sources_*.SOURCE.json into data/raw/<source_slug>/,
verifying sha256 against the record. Audio is not in git; this script makes a fresh clone self-sufficient.
Usage: uv run --with "huggingface_hub[hf_xet]" scripts/fetch_raw_sources.py [--only <slug>]
Wikimedia files come from upload.wikimedia.org (needs a User-Agent); RTRK files from the Hugging Face dataset repo.
"""
import argparse, sys, urllib.request
from pathlib import Path
from kmm_common import ROOT, read_json, sha256

RTRK_REPO = "rtrk/kazakh-traditional-audio"
UA = "kazakh-music-model-prototype/0.1 (research; contact via GitHub Yeldar2609)"


def fetch_url(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="source_slug to fetch (default: all)")
    a = ap.parse_args()
    bad = 0
    for src in sorted((ROOT / "data" / "manifests").glob("sources_*.SOURCE.json")):
        doc = read_json(src)
        slug = doc["source_slug"]
        if a.only and slug != a.only:
            continue
        out_dir = ROOT / "data" / "raw" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SOURCE.json").write_bytes(src.read_bytes())
        for f in doc["files"]:
            name = f.get("filename") or f.get("file")
            dest = out_dir / name
            if dest.is_file() and sha256(dest) == f["sha256"]:
                print("ok  ", slug, name)
                continue
            try:
                if slug.startswith("rtrk"):
                    from huggingface_hub import hf_hub_download
                    p = hf_hub_download(RTRK_REPO, repo_type="dataset", filename=f"data/{f['category']}/{name}",
                                        local_dir=out_dir / "_hf")
                    Path(p).replace(dest)
                else:
                    url = f.get("download_url") or f["url"]
                    if "upload.wikimedia.org" not in url:
                        raise RuntimeError(f"no direct download URL recorded: {url}")
                    fetch_url(url, dest)
            except Exception as e:  # noqa: BLE001
                bad += 1
                print("FAIL", slug, name, "-", e)
                continue
            if sha256(dest) != f["sha256"]:
                bad += 1
                print("FAIL", slug, name, "- sha256 mismatch vs SOURCE.json (kept for inspection)")
            else:
                print("got ", slug, name)
        hf_tmp = out_dir / "_hf"
        if hf_tmp.exists():
            import shutil
            shutil.rmtree(hf_tmp, ignore_errors=True)
    print("RESULT:", "FAIL" if bad else "OK", f"({bad} problems)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
