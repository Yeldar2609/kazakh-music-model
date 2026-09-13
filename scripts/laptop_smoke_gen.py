# Tonight-only smoke attempt on the 4 GB RTX 3050 Ti: tier-1 route (INT8 + full CPU offload, LM disabled).
# Not a deliverable. Success = a real WAV from the pretrained model; failure is recorded, not hidden.
import os, sys, time, json
PROJ = r"C:\Users\yelda\OneDrive\Desktop\Kazak Music Model"
sys.path.insert(0, os.path.join(PROJ, "upstream", "ACE-Step-1.5"))
os.environ.setdefault("ACESTEP_CHECKPOINTS_DIR", r"C:\kmm\checkpoints")
os.environ.setdefault("PYTHONUTF8", "1")
import torch
from acestep.handler import AceStepHandler
from acestep.inference import GenerationParams, GenerationConfig, generate_music

quant = sys.argv[1] if len(sys.argv) > 1 else "int8_weight_only"
quant = None if quant == "none" else quant
out = os.path.join(PROJ, "outputs", "baseline_laptop_smoke")
t0 = time.time()
h = AceStepHandler()
msg, ok = h.initialize_service(project_root=PROJ, config_path="acestep-v15-turbo", device="cuda",
                               compile_model=bool(quant), offload_to_cpu=True, offload_dit_to_cpu=True,
                               quantization=quant)
print("init:", ok, msg[:300], f"{time.time()-t0:.0f}s", flush=True)
if not ok:
    sys.exit(1)
params = GenerationParams(caption="solo dombra, Kazakh traditional two-string plucked lute, unaccompanied kui, no vocals",
                          lyrics="[Instrumental]", instrumental=True, vocal_language="unknown",
                          duration=10, inference_steps=8, shift=3.0, seed=1001)
cfg = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[1001], audio_format="wav")
t1 = time.time()
res = generate_music(h, None, params, cfg, save_dir=out)
print("gen ok:", res.success, "err:", getattr(res, "error", None), f"{time.time()-t1:.0f}s",
      "peak VRAM MiB:", torch.cuda.max_memory_allocated() // 2**20 if torch.cuda.is_available() else None, flush=True)
for a in (res.audios or []):
    print("saved:", a.get("path"), "seed:", a.get("params", {}).get("seed"))
