"""Local 4-bit training using the pinned upstream preprocessor and training loss."""
import argparse
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "upstream/ACE-Step-1.5"))


def sample_position(step, original_every, mixed):
    if not mixed:
        return 0, step
    if (step + 1) % original_every == 0:
        return 1, step // original_every
    return 0, step - step // original_every


def load_quantized(checkpoint_dir, variant="turbo", device="cuda", precision="bf16"):
    import torch
    from transformers import AutoModel, BitsAndBytesConfig
    if variant != "turbo" or not str(device).startswith("cuda"):
        raise ValueError("This training route requires the pinned turbo model and CUDA")
    model = AutoModel.from_pretrained(
        str(Path(checkpoint_dir) / "acestep-v15-turbo"),
        trust_remote_code=True, attn_implementation="sdpa", dtype=torch.bfloat16,
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16),
        device_map={"": "cuda:0"}, low_cpu_mem_usage=True)
    for p in model.parameters():
        p.requires_grad = False
    return model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["preprocess", "train", "smoke"])
    ap.add_argument("--dataset", type=Path)
    ap.add_argument("--tensors", type=Path)
    ap.add_argument("--original-tensors", type=Path, help="Interleave original-data updates at --original-every intervals")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--steps", type=int, default=100)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--save-every", type=int, default=25)
    ap.add_argument("--original-every", type=int, default=2)
    ap.add_argument("--checkpoints", default="C:/kmm/checkpoints")
    a = ap.parse_args()
    import torch
    if a.steps < 1 or a.save_every < 1 or a.original_every < 2 or not 0 < a.lr <= 1e-3:
        ap.error("Require positive steps/save interval, original-every >= 2, and 0 < lr <= 0.001")
    if a.out.exists():
        ap.error("Use a new output directory to preserve earlier experiments")
    a.out.mkdir(parents=True)
    torch.manual_seed(42)
    random.seed(42)
    if a.mode == "preprocess":
        if not a.dataset or not a.dataset.is_file():
            ap.error("preprocess requires an existing dataset JSON")
        rows = json.loads(a.dataset.read_text(encoding="utf-8"))["samples"]
        if not rows or any(not 0 < row["duration"] <= 60 for row in rows):
            raise ValueError("Require complete clips up to 60 seconds; do not truncate aligned lyrics")
        from acestep.training_v2 import model_loader
        from acestep.training_v2.preprocess import preprocess_audio_files
        # Upstream has no quantized loader hook; replace it for this process only.
        model_loader.load_decoder_for_training = load_quantized
        result = preprocess_audio_files(None, str(a.out), a.checkpoints,
            dataset_json=str(a.dataset), device="cuda", precision="bf16", max_duration=60,
            progress_callback=lambda i, n, msg: print(i, n, msg, flush=True))
        (a.out / "preparation_result.json").write_text(json.dumps(result, indent=2))
        if result["failed"] or not result["processed"]:
            raise RuntimeError(f"Incomplete preprocessing: {result}")
        return
    from acestep.training_v2.fixed_lora_module import FixedLoRAModule
    from acestep.training_v2.configs import LoRAConfigV2, TrainingConfigV2
    from acestep.training.lora_checkpoint import save_lora_weights
    from acestep.training.path_safety import set_safe_root
    set_safe_root(str(a.out.resolve()))
    if a.mode == "train":
        if not a.tensors:
            ap.error("train requires a tensor directory")
        files = sorted(p for p in a.tensors.glob("*.pt") if not p.name.endswith(".tmp.pt"))
        if not files:
            raise ValueError("No prepared training tensors")
        groups = [files]
        if a.original_tensors:
            original = sorted(p for p in a.original_tensors.glob("*.pt") if not p.name.endswith(".tmp.pt"))
            if not original or set(original) & set(files):
                raise ValueError("Original and new tensor groups must be nonempty and separate")
            groups.append(original)
    model = load_quantized(a.checkpoints)
    cfg = TrainingConfigV2()
    module = FixedLoRAModule(model, LoRAConfigV2(r=8, alpha=16), cfg,
                            torch.device("cuda"), torch.bfloat16)
    module.train()
    module.model.decoder.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    module.force_input_grads_for_checkpointing = True
    params = [p for p in module.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(params, lr=a.lr)
    start = time.time()
    settings = {"mode": a.mode, "steps": a.steps, "seed": 42, "rank": 8, "alpha": 16,
                "lr": a.lr, "original_every": a.original_every, "save_every": a.save_every,
                "batch_size": 1, "quantization": "NF4 double quantization, BF16 compute",
                "dataset": str(a.dataset), "tensors": str(a.tensors),
                "original_tensors": str(a.original_tensors), "quality_evaluated": False}
    (a.out / "settings.json").write_text(json.dumps(settings, indent=2))
    with (a.out / "steps.jsonl").open("w") as log:
        for step in range(a.steps if a.mode == "train" else 1):
            if a.mode == "smoke":
                from acestep.training_v2.make_test_fixtures import generate_single_sample
                sample = generate_single_sample("synthetic_only", latent_length=64, encoder_length=16)
            else:
                group_number, sample_number = sample_position(step, a.original_every, len(groups) > 1)
                group = groups[group_number]
                index = sample_number % len(group)
                if index == 0:
                    random.shuffle(group)
                sample = torch.load(group[index], map_location="cpu", weights_only=True)
            batch = {k: v.unsqueeze(0) for k, v in sample.items() if isinstance(v, torch.Tensor)}
            optimizer.zero_grad(set_to_none=True)
            loss = module.training_step(batch)
            if not torch.isfinite(loss):
                raise RuntimeError("Nonfinite training loss")
            loss.backward()
            if not any(p.grad is not None and p.grad.abs().sum() > 0 for p in params):
                raise RuntimeError("No adapter gradients")
            torch.nn.utils.clip_grad_norm_(params, 1.0, error_if_nonfinite=True)
            optimizer.step()
            row = {"step": step + 1, "loss": float(loss.detach()),
                   "seconds": time.time() - start,
                   "peak_vram_mib": torch.cuda.max_memory_allocated() // 2**20}
            if a.mode == "train":
                row["source"] = "new" if group_number == 0 else "original"
                row["sample"] = group[index].stem
            log.write(json.dumps(row) + "\n")
            log.flush()
            print(row, flush=True)
            if a.mode == "train" and (step + 1) % a.save_every == 0:
                save_lora_weights(model, str(a.out / f"step_{step+1}"))
    if a.mode == "train":
        save_lora_weights(model, str(a.out / "final"))
    (a.out / "COMPLETE.json").write_text(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
