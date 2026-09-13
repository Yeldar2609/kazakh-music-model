#!/usr/bin/env bash
# Train a LoRA adapter on preprocessed tensors with upstream Side-Step (ACE-Step 1.5 turbo).
# Usage: scripts/train_adapter.sh <tensor_dir> <output_dir> <epochs> [extra train.py fixed args]
#   e.g. extra: --optimizer-type adamw8bit --offload-encoder --resume-from <out>/checkpoints/epoch_3_loss_0.2107
# Each saved epoch dir is ~0.5 GB (adapter + training_state.pt): default --save-every 10; a pilot
# should pass --save-every 25 and an output dir under KMM_WORK, then copy only final/ into the project.
# Later flags override the defaults below (argparse last-wins). Reads KEY=VALUE lines from
# .env.local; already-set environment variables win. GPU step: prepared, awaiting 5090 validation.
set -euo pipefail
if [ $# -lt 3 ]; then
  echo "usage: $0 <tensor_dir> <output_dir> <epochs> [extra args]" >&2
  exit 2
fi
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -f "$ROOT/.env.local" ]; then
  while IFS='=' read -r key value || [ -n "$key" ]; do
    key="${key%%[[:space:]]*}"; value="${value%$'\r'}"
    case "$key" in ''|\#*) continue ;; esac
    [ -z "${!key:-}" ] && export "$key=$value"
  done < "$ROOT/.env.local"
fi
export KMM_CHECKPOINTS="${KMM_CHECKPOINTS:-$ROOT/checkpoints}"
export PYTHONUTF8=1
# Absolutise both paths BEFORE cd-ing into the upstream clone.
TENSOR_DIR="$(cd "$1" && pwd)"
OUT_DIR="$(mkdir -p "$2" && cd "$2" && pwd)"
EPOCHS="$3"
shift 3
cd "$ROOT/upstream/ACE-Step-1.5"
echo "[train_adapter] checkpoints=$KMM_CHECKPOINTS env=${UV_PROJECT_ENVIRONMENT:-<uv default>} epochs=$EPOCHS"
# --yes --plain are ROOT-level flags and must come before the `fixed` subcommand.
exec uv run python train.py --yes --plain fixed \
  --checkpoint-dir "$KMM_CHECKPOINTS" --model-variant turbo \
  --dataset-dir "$TENSOR_DIR" --output-dir "$OUT_DIR" \
  --epochs "$EPOCHS" --save-every 10 \
  --batch-size 1 --gradient-accumulation 4 --lr 1e-4 \
  --adapter-type lora --rank 64 --alpha 128 \
  --shift 3.0 --num-inference-steps 8 "$@"
