#!/usr/bin/env bash
# Preprocess a dataset JSON into training tensors with upstream Side-Step (ACE-Step 1.5 turbo).
# Usage: scripts/preprocess_dataset.sh <dataset.json> <tensor_output_dir> [extra train_fixed args]
# Reads KEY=VALUE lines from .env.local (KMM_CHECKPOINTS, UV_PROJECT_ENVIRONMENT, ...); already-set
# environment variables win. GPU step: prepared, awaiting 5090 validation.
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "usage: $0 <dataset.json> <tensor_output_dir> [extra args]" >&2
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
DATASET_JSON="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
TENSOR_OUT="$(mkdir -p "$2" && cd "$2" && pwd)"
shift 2
cd "$ROOT/upstream/ACE-Step-1.5"
echo "[preprocess_dataset] checkpoints=$KMM_CHECKPOINTS env=${UV_PROJECT_ENVIRONMENT:-<uv default>}"
# Module entry point on purpose: `train.py fixed --preprocess` rejects a call without
# --dataset-dir/--output-dir (argparse required=True in training_v2/cli/args.py).
exec uv run python -m acestep.training_v2.cli.train_fixed --plain \
  --checkpoint-dir "$KMM_CHECKPOINTS" --model-variant turbo \
  --preprocess --dataset-json "$DATASET_JSON" --tensor-output "$TENSOR_OUT" \
  --max-duration 240 "$@"
