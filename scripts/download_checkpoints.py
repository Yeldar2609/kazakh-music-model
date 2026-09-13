# Pinned, filtered download of only the ACE-Step components this project uses.
import hashlib, json, os, sys, time
from huggingface_hub import snapshot_download

REPO = "ACE-Step/Ace-Step1.5"
REV = "19671f406d603126926c1b7e2adc169acbcade22"   # pinned 2026-02-03 commit
DEST = sys.argv[1] if len(sys.argv) > 1 else r"C:\kmm\checkpoints"
PATTERNS = ["acestep-v15-turbo/*", "vae/*", "Qwen3-Embedding-0.6B/*", "acestep-5Hz-lm-1.7B/*", "config.json", "README.md"]  # LM is never loaded, but upstream init requires the folder

t0 = time.time()
path = snapshot_download(repo_id=REPO, revision=REV, local_dir=DEST, allow_patterns=PATTERNS)
print("downloaded to", path, "in", round(time.time() - t0), "s", flush=True)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

out = {"repo": REPO, "revision": REV, "files": {}}
for root, _, files in os.walk(DEST):
    for fn in files:
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, DEST).replace("\\", "/")
        if rel.startswith(".cache"):
            continue
        out["files"][rel] = {"bytes": os.path.getsize(p), "sha256": sha256(p) if fn.endswith((".safetensors", ".pt")) else None}
with open(os.path.join(DEST, "CHECKSUMS.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("checksums written", flush=True)
