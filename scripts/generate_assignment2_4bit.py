"""Generate matched local examples with the same NF4 base used for pilot training."""
import argparse
import json
import os
import time
from pathlib import Path

from train_assignment2_4bit import ROOT, load_quantized


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--adapter", type=Path)
    ap.add_argument("--checkpoints", default="C:/kmm/checkpoints")
    ap.add_argument("--cases", type=Path, default=ROOT / "configs/assignment2_eval_cases.json")
    a = ap.parse_args()
    if a.out.exists():
        ap.error("Use a new output directory")
    import torch
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationParams, GenerationConfig, generate_music
    from peft import PeftModel

    class LocalHandler(AceStepHandler):
        def _load_main_model_from_checkpoint(self, *, model_checkpoint_path, **kwargs):
            self.model = load_quantized(Path(model_checkpoint_path).parent)
            self.config = self.model.config
            self._sync_alignment_config()
            self._apply_cuda_bool_argsort_workaround()
            # Quantized token decoding preserves its input dtype; align it with the BF16 output layer.
            self.model.detokenizer.register_forward_pre_hook(
                lambda module, inputs: (inputs[0].to(self.dtype),))
            self.model.eval()
            self.silence_latent = torch.load(Path(model_checkpoint_path) / "silence_latent.pt",
                weights_only=True).transpose(1, 2).to(device="cuda", dtype=self.dtype)
            return "sdpa"

    os.environ["ACESTEP_CHECKPOINTS_DIR"] = a.checkpoints
    handler = LocalHandler()
    status, ok = handler.initialize_service(project_root=str(ROOT / "upstream/ACE-Step-1.5"),
        config_path="acestep-v15-turbo", device="cuda", compile_model=False,
        offload_to_cpu=True, offload_dit_to_cpu=False, quantization=None)
    if not ok:
        raise RuntimeError(status)
    if a.adapter:
        handler.model.decoder = PeftModel.from_pretrained(handler.model.decoder, str(a.adapter))
        handler.model.decoder.eval()
        handler.lora_loaded = True
        handler.use_lora = True
        handler.lora_scale = 1.0
    a.out.mkdir(parents=True)
    case_config = json.loads(a.cases.read_text(encoding="utf-8"))
    cases = case_config["cases"]
    duration = float(case_config.get("duration_seconds", 15))
    if not 1 <= duration <= 60:
        raise ValueError("Comparison duration must be between 1 and 60 seconds")
    for case in cases:
        lyrics = (ROOT / case["lyrics_file"]).read_text(encoding="utf-8") if "lyrics_file" in case else case["lyrics"]
        params = GenerationParams(caption=case["caption"], lyrics=lyrics,
            instrumental=case["instrumental"], vocal_language="unknown", duration=duration,
            inference_steps=8, shift=3.0, seed=1001)
        cfg = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[1001], audio_format="wav")
        start = time.time()
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            result = generate_music(handler, None, params, cfg, save_dir=str(a.out / case["id"]))
        if not result.success:
            raise RuntimeError(str(result.error))
        record = {"case": case["id"], "caption": case["caption"], "lyrics": lyrics,
                  "seed": 1001, "duration_seconds": duration, "steps": 8, "shift": 3.0,
                  "quantization": "NF4", "adapter": str(a.adapter) if a.adapter else None,
                  "seconds": time.time() - start, "files": [x.get("path") for x in result.audios],
                  "human_reviewed": False}
        (a.out / (case["id"] + ".json")).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print(record["case"], record["files"], flush=True)


if __name__ == "__main__":
    main()
