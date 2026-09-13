#!/usr/bin/env python
"""Validate a PEFT LoRA adapter directory without loading torch or the model.

    py -3.12 scripts/check_adapter.py <adapter_dir>

Checks mirror what upstream load_lora() needs
(acestep/core/generation/handler/lora/lifecycle.py: adapter_config.json present,
'peft_type' key present, adapter_model.safetensors for PeftModel.from_pretrained),
then lists every tensor (name, shape, dtype) and the total parameter count.
Uses safetensors.safe_open(framework="np") when safetensors + numpy are
installed, otherwise parses the 8-byte-length + JSON safetensors header directly.
Exit code 0 = valid, 1 = invalid, 2 = usage.
"""

import json
import os
import struct
import sys

REQUIRED_KEYS = ("peft_type",)  # lifecycle.py REQUIRED_PEFT_CONFIG_KEYS
EXPECTED_KEYS = ("r", "lora_alpha", "target_modules", "base_model_name_or_path")
WEIGHTS = "adapter_model.safetensors"
CONFIG = "adapter_config.json"

DTYPE_BYTES = {
    "F64": 8, "F32": 4, "F16": 2, "BF16": 2, "I64": 8, "I32": 4, "I16": 2, "I8": 1,
    "U8": 1, "BOOL": 1, "F8_E4M3": 1, "F8_E5M2": 1,
}


def read_header(path):
    """Return (tensors: {name: (shape, dtype)}, metadata) by parsing the safetensors header."""
    with open(path, "rb") as fh:
        n = struct.unpack("<Q", fh.read(8))[0]
        header = json.loads(fh.read(n).decode("utf-8"))
    meta = header.pop("__metadata__", None)
    tensors = {k: (tuple(v["shape"]), v["dtype"]) for k, v in header.items()}
    return tensors, meta


def read_with_safetensors(path):
    from safetensors import safe_open  # noqa: F401 (optional)
    import numpy  # noqa: F401 (framework="np" needs it)
    tensors = {}
    with safe_open(path, framework="np") as sf:
        meta = sf.metadata()
        for name in sf.keys():
            arr = sf.get_tensor(name)
            tensors[name] = (tuple(arr.shape), str(arr.dtype))
    return tensors, meta


def numel(shape):
    n = 1
    for d in shape:
        n *= d
    return n


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    adapter = os.path.abspath(sys.argv[1])
    problems = []
    warnings = []

    if not os.path.isdir(adapter):
        print(f"INVALID: not a directory: {adapter}")
        return 1

    cfg_path = os.path.join(adapter, CONFIG)
    cfg = None
    if not os.path.isfile(cfg_path):
        problems.append(f"missing {CONFIG} (upstream load_lora refuses the dir)")
    else:
        try:
            with open(cfg_path, encoding="utf-8") as fh:
                cfg = json.load(fh)
            if not isinstance(cfg, dict):
                problems.append(f"{CONFIG} must be a JSON object")
                cfg = None
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"could not read {CONFIG}: {exc}")
    if cfg is not None:
        for key in REQUIRED_KEYS:
            if key not in cfg:
                problems.append(f"{CONFIG} missing required key '{key}'")
        for key in EXPECTED_KEYS:
            if key not in cfg:
                warnings.append(f"{CONFIG} has no '{key}' (unusual for a PEFT LoRA export)")
        print(f"config: peft_type={cfg.get('peft_type')} r={cfg.get('r')} lora_alpha={cfg.get('lora_alpha')} "
              f"target_modules={cfg.get('target_modules')}")

    weights_path = os.path.join(adapter, WEIGHTS)
    if not os.path.isfile(weights_path):
        problems.append(f"missing {WEIGHTS} (PeftModel.from_pretrained needs it)")
        tensors = {}
    else:
        try:
            tensors, meta = read_with_safetensors(weights_path)
            source = "safetensors"
        except Exception as exc:  # no safetensors/numpy, or bf16 (not representable in numpy)
            tensors, meta = read_header(weights_path)
            source = f"header-parse; safetensors path unavailable: {type(exc).__name__}"
        print(f"weights: {weights_path} ({os.path.getsize(weights_path)} bytes, read via {source})")
        if meta:
            print(f"metadata: {meta}")
        total = 0
        lora_a = lora_b = 0
        for name in sorted(tensors):
            shape, dtype = tensors[name]
            total += numel(shape)
            if ".lora_A." in name or name.endswith("lora_A.weight"):
                lora_a += 1
                if cfg and isinstance(cfg.get("r"), int) and shape and shape[0] != cfg["r"]:
                    warnings.append(f"{name}: dim0={shape[0]} but config r={cfg['r']}")
            elif ".lora_B." in name or name.endswith("lora_B.weight"):
                lora_b += 1
            print(f"  {name}  shape={list(shape)}  dtype={dtype}")
        print(f"tensors: {len(tensors)}  lora_A: {lora_a}  lora_B: {lora_b}  total params: {total:,}")
        if not tensors:
            problems.append(f"{WEIGHTS} contains no tensors")
        if lora_a != lora_b:
            warnings.append(f"lora_A/lora_B count mismatch ({lora_a} vs {lora_b})")
        if tensors and lora_a == 0:
            warnings.append("no lora_A tensors found; is this really a PEFT LoRA?")

    for w in warnings:
        print(f"WARNING: {w}")
    if problems:
        for p in problems:
            print(f"ERROR: {p}")
        print(f"INVALID: {adapter}")
        return 1
    print(f"OK: {adapter}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
