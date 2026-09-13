"""GPU / environment proof. Run with the ACE-Step venv python. Exit 1 on any hard failure.
Proves: torch+CUDA import, device + arch list, a REAL bf16 matmul on the GPU, torchaudio can load a WAV.
"""
import os, platform, shutil, subprocess, sys, tempfile, time, wave, struct, math

fail = []
print(f"platform : {platform.platform()}  python {sys.version.split()[0]}  exe {sys.executable}")
print(f"ffmpeg   : {shutil.which('ffmpeg')}")
try:
    smi = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"],
                         capture_output=True, text=True, timeout=20)
    print(f"nvidia-smi: {smi.stdout.strip() or smi.stderr.strip()}")
except Exception as e:  # noqa: BLE001
    print(f"nvidia-smi: not available ({e})")

try:
    import torch, torchaudio
    print(f"torch    : {torch.__version__}  torchaudio {torchaudio.__version__}  cuda build {torch.version.cuda}")
except Exception as e:  # noqa: BLE001
    print(f"FAIL import torch/torchaudio: {e}"); sys.exit(1)

if not torch.cuda.is_available():
    fail.append("torch.cuda.is_available() is False")
else:
    p = torch.cuda.get_device_properties(0)
    cap = torch.cuda.get_device_capability(0)
    archs = torch.cuda.get_arch_list()
    print(f"gpu      : {p.name}  VRAM {p.total_memory/2**30:.1f} GiB  capability sm_{cap[0]}{cap[1]}")
    print(f"arch list: {archs}")
    need = f"sm_{cap[0]}{cap[1]}"
    if need not in archs and not any(a.startswith(f"sm_{cap[0]}") for a in archs):
        fail.append(f"torch build lacks kernels for {need} (has {archs}) — wrong wheel for this GPU")
    # real GPU op
    torch.cuda.reset_peak_memory_stats()
    a = torch.randn(4096, 4096, device="cuda", dtype=torch.bfloat16)
    b = torch.randn(4096, 4096, device="cuda", dtype=torch.bfloat16)
    torch.cuda.synchronize(); t0 = time.time()
    for _ in range(10):
        c = a @ b
    torch.cuda.synchronize(); dt = time.time() - t0
    ok = torch.isfinite(c.float()).all().item()
    tflops = 10 * 2 * 4096**3 / dt / 1e12
    print(f"bf16 matmul x10: {dt*1000:.0f} ms  ~{tflops:.1f} TFLOP/s  finite={ok}  peak {torch.cuda.max_memory_allocated()/2**20:.0f} MiB")
    if not ok:
        fail.append("matmul produced non-finite values")

# torchaudio load smoke test (this is what upstream preprocessing uses)
tmp = os.path.join(tempfile.gettempdir(), "kmm_diag.wav")
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes(b"".join(struct.pack("<h", int(8000 * math.sin(2 * math.pi * 440 * i / 48000))) for i in range(48000)))
try:
    x, sr = torchaudio.load(tmp)
    print(f"torchaudio.load: shape {tuple(x.shape)} sr {sr}")
except Exception as e:  # noqa: BLE001
    fail.append(f"torchaudio.load failed: {e}")

print("RESULT:", "FAIL" if fail else "OK")
for f in fail:
    print(" -", f)
sys.exit(1 if fail else 0)
