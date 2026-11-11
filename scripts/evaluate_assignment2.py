"""Paired held-out flow-loss comparison; this is not a music-quality score."""
import argparse
import json
from pathlib import Path

from train_assignment2_4bit import load_quantized


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tensors", type=Path, required=True)
    ap.add_argument("--adapters", type=Path, nargs="+", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    import torch
    from safetensors.torch import load_file
    from peft import get_peft_model_state_dict, set_peft_model_state_dict
    from acestep.training_v2.fixed_lora_module import FixedLoRAModule
    from acestep.training_v2.configs import TrainingConfigV2, LoRAConfigV2
    files = sorted(p for p in a.tensors.glob("*.pt") if not p.name.endswith(".tmp.pt"))
    if not files or a.out.exists():
        raise ValueError("Require held-out tensors and a new output file")
    cfg = TrainingConfigV2()
    cfg.cfg_ratio = 0
    torch.manual_seed(42)
    module = FixedLoRAModule(load_quantized("C:/kmm/checkpoints"), LoRAConfigV2(r=8, alpha=16),
                            cfg, torch.device("cuda"), torch.bfloat16)
    module.eval()
    rows = []
    expected = get_peft_model_state_dict(module.model.decoder)
    for adapter in [None] + a.adapters:
        if adapter:
            weights = load_file(str(adapter / "adapter_model.safetensors"))
            if weights.keys() != expected.keys() or any(weights[k].shape != expected[k].shape for k in weights):
                raise ValueError("Adapter keys or shapes do not match the evaluation model")
            set_peft_model_state_dict(module.model.decoder, weights)
        losses = []
        with torch.inference_mode():
            for i, path in enumerate(files):
                torch.manual_seed(10000 + i)
                sample = torch.load(path, map_location="cpu", weights_only=True)
                batch = {k: v.unsqueeze(0) for k, v in sample.items() if isinstance(v, torch.Tensor)}
                loss = module.training_step(batch)
                if not torch.isfinite(loss):
                    raise RuntimeError("Nonfinite evaluation loss")
                losses.append({"sample": path.stem, "loss": float(loss)})
        row = {"adapter": str(adapter) if adapter else "pretrained",
               "mean_flow_loss": sum(x["loss"] for x in losses) / len(losses), "samples": losses}
        rows.append(row)
        print(row["adapter"], row["mean_flow_loss"], flush=True)
    a.out.write_text(json.dumps({"metric": "paired held-out flow matching MSE",
        "limitation": "Does not measure intelligibility, naturalness or music quality",
        "tensor_directory": str(a.tensors), "results": rows}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
