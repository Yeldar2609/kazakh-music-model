#!/usr/bin/env python
"""Generate the fixed evaluation cases (configs/eval_cases.json) with ACE-Step 1.5 turbo.

One WAV + one JSON sidecar per (case, seed), laid out as
    <out>/<case_id>/<case_id>_seed<seed>.wav  +  .json
Baseline run and adapter run use the same script; only --adapter/--adapter-scale differ.

Run with the uv environment interpreter (torch is required unless --dry-run):
    C:\\kmm\\venv-acestep\\Scripts\\python.exe scripts\\generate_cases.py --cases configs/eval_cases.json --out outputs/baseline
    uv run --project upstream/ACE-Step-1.5 python scripts/generate_cases.py ...
--dry-run prints the resolved parameters and never imports torch, so it also works
with a plain interpreter (`py -3.12`, or the venv python / `uv run --project upstream/ACE-Step-1.5 python`).

GPU steps are prepared but not yet validated on the 5090.
"""

import argparse
import datetime as _dt
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPSTREAM = os.path.join(ROOT, "upstream", "ACE-Step-1.5")
PINS = os.path.join(ROOT, "configs", "pins.json")
CONFIG_NAME = "acestep-v15-turbo"  # DiT subfolder under the checkpoints dir
REQUIRED_COMPONENTS = ("acestep-v15-turbo", "vae", "Qwen3-Embedding-0.6B")
# Same list as upstream acestep/model_downloader.py:_contains_model_weights
WEIGHT_FILENAMES = (
    "model.safetensors",
    "model.safetensors.index.json",
    "pytorch_model.bin",
    "pytorch_model.bin.index.json",
    "diffusion_pytorch_model.safetensors",
    "diffusion_pytorch_model.safetensors.index.json",
    "diffusion_pytorch_model.bin",
    "diffusion_pytorch_model.bin.index.json",
)

if UPSTREAM not in sys.path:
    sys.path.insert(0, UPSTREAM)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def load_env_local():
    """Read KEY=VALUE lines from .env.local into os.environ (existing vars win)."""
    path = os.path.join(ROOT, ".env.local")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def resolve_jobs(args):
    """Return (defaults, [job dict, ...]) with every parameter resolved. No torch."""
    cases = read_json(args.cases)
    pins = read_json(PINS) if os.path.isfile(PINS) else {}
    defaults = {
        "model_variant": cases.get("model_variant", "turbo"),
        "inference_steps": int(cases.get("inference_steps", 8)),
        "shift": float(cases.get("shift", 3.0)),
        "guidance_scale": float(cases.get("guidance_scale", 1.0)),
        "duration": float(cases.get("duration_seconds", 30)),
        "seeds": list(cases.get("seeds", [1001])),
        "vocal_language": cases.get("vocal_language", "unknown"),
        "engine_commit": pins.get("engine", {}).get("revision"),
        "checkpoint_revision": pins.get("checkpoint", {}).get("revision"),
    }
    seeds_override = [int(s) for s in args.seeds] if args.seeds else None

    jobs = []
    for case in cases["cases"]:
        if args.case_id and case["id"] != args.case_id:
            continue
        if "lyrics_file" in case:
            lyrics_path = os.path.join(ROOT, case["lyrics_file"])
            with open(lyrics_path, encoding="utf-8") as fh:
                lyrics = fh.read().strip()
        else:
            lyrics = case.get("lyrics", "")
            lyrics_path = None
        seeds = seeds_override or case.get("seeds") or defaults["seeds"]
        for seed in seeds:
            jobs.append({
                "case_id": case["id"],
                "kind": case.get("kind"),
                "caption": case["caption"],
                "lyrics": lyrics,
                "lyrics_file": case.get("lyrics_file"),
                "instrumental": bool(case.get("instrumental", False)),
                "bpm": case.get("bpm"),
                "keyscale": case.get("keyscale") or "",
                "timesignature": case.get("timesignature") or "",
                "vocal_language": case.get("vocal_language", defaults["vocal_language"]),
                "seed": int(seed),
                "duration": float(case.get("duration", defaults["duration"])),
                "inference_steps": int(case.get("steps", defaults["inference_steps"])),
                "shift": float(case.get("shift", defaults["shift"])),
                "guidance_scale": defaults["guidance_scale"],
            })
    if not jobs:
        sys.exit(f"No cases matched (case_id={args.case_id!r}) in {args.cases}")
    return defaults, jobs


def check_checkpoints(ckpt_dir):
    """Refuse to start unless the three pinned components are present.

    Upstream initialize_service() would otherwise auto-download the WHOLE
    HF repo (unpinned) because it also expects the LM we deliberately skip.
    """
    missing = []
    for comp in REQUIRED_COMPONENTS:
        comp_dir = os.path.join(ckpt_dir, comp)
        if not any(os.path.exists(os.path.join(comp_dir, f)) for f in WEIGHT_FILENAMES):
            missing.append(comp_dir)
    if missing:
        sys.exit("Missing checkpoint weights (run the pinned download first, no auto-download here):\n  "
                 + "\n  ".join(missing))


def run(args, defaults, jobs):
    ckpt_dir = os.path.abspath(args.checkpoints)
    check_checkpoints(ckpt_dir)
    # Orchestrator reads ACESTEP_CHECKPOINTS_DIR first (init_service_orchestrator.py:122-124);
    # ACESTEP_PROJECT_ROOT keeps the handler's .cache/ out of this repo (progress.py:20-32).
    os.environ["ACESTEP_CHECKPOINTS_DIR"] = ckpt_dir
    os.environ.setdefault("ACESTEP_PROJECT_ROOT", os.environ.get("KMM_WORK") or UPSTREAM)
    os.makedirs(args.out, exist_ok=True)

    import torch
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationConfig, GenerationParams, generate_music
    from acestep.audio_utils import get_lora_weights_hash
    import acestep.core.generation.handler.init_service_downloads as _dl

    # _ensure_models_present (init_service_downloads.py:31) calls the module-global
    # check_main_model_exists, which demands acestep-5Hz-lm-1.7B too. We have the
    # three DiT/VAE/text-encoder dirs (checked above) and never want the downloader.
    def _only_required_components(checkpoints_dir=None):
        return True
    _dl.check_main_model_exists = _only_required_components
    print("[generate_cases] LM presence check neutralised (LM disabled by design; no auto-download).")

    handler = AceStepHandler()
    status, ok = handler.initialize_service(
        project_root=UPSTREAM,
        config_path=CONFIG_NAME,
        device=args.device,
        compile_model=False,
        offload_to_cpu=args.offload_to_cpu,
        offload_dit_to_cpu=False,
        quantization=None,
    )
    print(status)
    if not ok:
        sys.exit("initialize_service failed")
    if not handler.is_turbo_model():
        sys.exit(f"{CONFIG_NAME} did not load as a turbo model; refusing (steps/shift are turbo values)")

    adapter_info = None
    if args.adapter:
        adapter_dir = os.path.abspath(args.adapter)
        msg = handler.load_lora(adapter_dir)
        print(msg)
        if not msg.startswith("✅"):
            sys.exit("LoRA load failed")
        msg = handler.set_use_lora(True)
        print(msg)
        if not msg.startswith("✅"):
            sys.exit("set_use_lora failed")
        msg = handler.set_lora_scale(args.adapter_scale)
        print(msg)
        if msg.startswith("❌"):
            sys.exit("set_lora_scale failed")
        if msg.startswith("⚠️"):
            print(f"[generate_cases] WARNING from set_lora_scale: {msg}")
        if abs(handler.lora_scale - args.adapter_scale) > 1e-9:
            print(f"[generate_cases] WARNING: requested scale {args.adapter_scale} clamped to {handler.lora_scale}")
        adapter_info = {
            "path": adapter_dir,
            "scale": handler.lora_scale,
            "scale_requested": args.adapter_scale,
            "scale_effective": handler.lora_scale,
            "weights_hash": get_lora_weights_hash(handler),
        }

    use_cuda = torch.cuda.is_available() and str(handler.device).startswith("cuda")
    failures = 0
    for job in jobs:
        # Layout contract shared with the viewer builder: outputs/<label>/<case_id>/<case_id>_seed<seed>.{wav,json}
        case_dir = os.path.join(args.out, job["case_id"])
        os.makedirs(case_dir, exist_ok=True)
        stem = f"{job['case_id']}_seed{job['seed']}"
        wav_path = os.path.join(case_dir, stem + ".wav")
        json_path = os.path.join(case_dir, stem + ".json")
        print(f"\n=== {job['case_id']}/{stem} ===")

        params = GenerationParams(
            task_type="text2music",
            caption=job["caption"],
            lyrics=job["lyrics"],
            instrumental=job["instrumental"],
            vocal_language=job["vocal_language"],
            bpm=job["bpm"],
            keyscale=job["keyscale"],
            timesignature=job["timesignature"],
            duration=job["duration"],
            inference_steps=job["inference_steps"],
            shift=job["shift"],
            guidance_scale=job["guidance_scale"],
            seed=job["seed"],
            thinking=False,
            use_cot_metas=False,
            use_cot_caption=False,
            use_cot_language=False,
        )
        config = GenerationConfig(
            batch_size=1,
            use_random_seed=False,
            seeds=[job["seed"]],
            audio_format="wav",
        )

        if use_cuda:
            torch.cuda.reset_peak_memory_stats()
        t0 = time.perf_counter()
        result = generate_music(handler, None, params, config, save_dir=case_dir)
        wall = time.perf_counter() - t0
        peak = torch.cuda.max_memory_allocated() if use_cuda else None

        saved = result.audios[0].get("path") if (result.success and result.audios) else ""
        if not saved:
            failures += 1
            print(f"FAILED: {result.error or result.status_message}")
            continue
        os.replace(saved, wav_path)
        # Upstream's own record of adapter state at generation time (inference.py:985-988):
        # independent evidence that the LoRA was actually active for this clip.
        engine_params = result.audios[0].get("params", {})
        engine_lora = {k: engine_params.get(k) for k in ("lora_loaded", "use_lora", "lora_scale", "lora_weights_hash")}

        sidecar = {
            "case_id": job["case_id"],
            "kind": job["kind"],
            "output_wav": os.path.basename(wav_path),
            "output_rel": f"{job['case_id']}/{os.path.basename(wav_path)}",
            "caption": job["caption"],
            "lyrics": job["lyrics"],
            "lyrics_file": job["lyrics_file"],
            "instrumental": job["instrumental"],
            "vocal_language": job["vocal_language"],
            "bpm": job["bpm"],
            "keyscale": job["keyscale"],
            "timesignature": job["timesignature"],
            "seed": job["seed"],
            "seed_used": result.audios[0]["params"].get("seed"),
            "duration": job["duration"],
            "inference_steps": job["inference_steps"],
            "shift": job["shift"],
            "guidance_scale": job["guidance_scale"],
            "model_variant": defaults["model_variant"],
            "config_path": CONFIG_NAME,
            "engine_commit": defaults["engine_commit"],
            "checkpoint_revision": defaults["checkpoint_revision"],
            "checkpoints_dir": ckpt_dir,
            "adapter": adapter_info,
            "engine_lora_state": engine_lora,
            "device": str(handler.device),
            "dtype": str(handler.dtype),
            "offload_to_cpu": bool(args.offload_to_cpu),
            "wall_time_s": round(wall, 3),
            "peak_vram_bytes": peak,
            "time_costs": result.extra_outputs.get("time_costs"),
            "sample_rate": result.audios[0].get("sample_rate"),
            "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        }
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(sidecar, fh, ensure_ascii=False, indent=2)
        print(f"saved {wav_path} ({wall:.1f}s, peak VRAM {peak})")

    if failures:
        sys.exit(f"{failures} of {len(jobs)} generations failed")


def main():
    load_env_local()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", default=os.path.join(ROOT, "configs", "eval_cases.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "outputs", "baseline"))
    ap.add_argument("--adapter", default=None, help="dir containing adapter_config.json (LoRA); omit for baseline")
    ap.add_argument("--adapter-scale", type=float, default=1.0, help="LoRA scale, clamped to [0,1] by upstream")
    ap.add_argument("--checkpoints", default=os.environ.get("KMM_CHECKPOINTS") or os.path.join(ROOT, "checkpoints"))
    ap.add_argument("--device", default="auto", help="auto | cuda | cpu (upstream resolves 'auto')")
    ap.add_argument("--offload-to-cpu", action="store_true")
    ap.add_argument("--case-id", default=None)
    ap.add_argument("--seeds", nargs="+", type=int, default=None, help="override seeds for every case")
    ap.add_argument("--dry-run", action="store_true", help="print resolved params, no torch import")
    args = ap.parse_args()

    defaults, jobs = resolve_jobs(args)
    if args.dry_run:
        print(json.dumps({
            "checkpoints": os.path.abspath(args.checkpoints),
            "upstream": UPSTREAM,
            "out": os.path.abspath(args.out),
            "adapter": os.path.abspath(args.adapter) if args.adapter else None,
            "adapter_scale": args.adapter_scale if args.adapter else None,
            "device": args.device,
            "offload_to_cpu": args.offload_to_cpu,
            "defaults": defaults,
            "jobs": jobs,
        }, ensure_ascii=False, indent=2))
        return
    run(args, defaults, jobs)


if __name__ == "__main__":
    main()
