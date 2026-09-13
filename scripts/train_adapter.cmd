@echo off
rem Train a LoRA adapter on preprocessed tensors with upstream Side-Step (ACE-Step 1.5 turbo).
rem Usage: scripts\train_adapter.cmd <tensor_dir> <output_dir> <epochs> [extra train.py fixed args]
rem   e.g. extra: --optimizer-type adamw8bit --offload-encoder --resume-from <out>\checkpoints\epoch_3_loss_0.2107
rem Each saved epoch dir is ~0.5 GB (adapter + training_state.pt): default --save-every 10; a pilot
rem should pass --save-every 25 and an output dir under KMM_WORK, then copy only final\ into the project.
rem Later flags override the defaults below (argparse last-wins). Reads KEY=VALUE lines from
rem .env.local; already-set environment variables win. GPU step: prepared, awaiting 5090 validation.
setlocal EnableDelayedExpansion
if "%~3"=="" (
  echo usage: %~nx0 ^<tensor_dir^> ^<output_dir^> ^<epochs^> [extra args]
  exit /b 2
)
set "ROOT=%~dp0.."
if exist "%ROOT%\.env.local" (
  for /f "usebackq eol=# tokens=1* delims==" %%A in ("%ROOT%\.env.local") do if not defined %%A set "%%A=%%B"
)
if not defined KMM_CHECKPOINTS set "KMM_CHECKPOINTS=%ROOT%\checkpoints"
set "PYTHONUTF8=1"
set "TENSOR_DIR=%~f1"
set "OUT_DIR=%~f2"
set "EPOCHS=%~3"
set "EXTRA="
shift
shift
shift
if "%~1"=="" goto run
:collect
set "EXTRA=!EXTRA! %1"
shift
if not "%~1"=="" goto collect
:run
cd /d "%ROOT%\upstream\ACE-Step-1.5" || exit /b 1
echo [train_adapter] checkpoints=%KMM_CHECKPOINTS% env=%UV_PROJECT_ENVIRONMENT% epochs=%EPOCHS%
rem --yes --plain are ROOT-level flags and must come before the `fixed` subcommand.
uv run python train.py --yes --plain fixed ^
  --checkpoint-dir "%KMM_CHECKPOINTS%" --model-variant turbo ^
  --dataset-dir "%TENSOR_DIR%" --output-dir "%OUT_DIR%" ^
  --epochs %EPOCHS% --save-every 10 ^
  --batch-size 1 --gradient-accumulation 4 --lr 1e-4 ^
  --adapter-type lora --rank 64 --alpha 128 ^
  --shift 3.0 --num-inference-steps 8 !EXTRA!
exit /b %ERRORLEVEL%
