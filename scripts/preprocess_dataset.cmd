@echo off
rem Preprocess a dataset JSON into training tensors with upstream Side-Step (ACE-Step 1.5 turbo).
rem Usage: scripts\preprocess_dataset.cmd <dataset.json> <tensor_output_dir> [extra train_fixed args]
rem Reads KEY=VALUE lines from .env.local (KMM_CHECKPOINTS, UV_PROJECT_ENVIRONMENT, ...); already-set
rem environment variables win. GPU step: prepared, awaiting 5090 validation.
setlocal EnableDelayedExpansion
if "%~2"=="" (
  echo usage: %~nx0 ^<dataset.json^> ^<tensor_output_dir^> [extra args]
  exit /b 2
)
set "ROOT=%~dp0.."
if exist "%ROOT%\.env.local" (
  for /f "usebackq eol=# tokens=1* delims==" %%A in ("%ROOT%\.env.local") do if not defined %%A set "%%A=%%B"
)
if not defined KMM_CHECKPOINTS set "KMM_CHECKPOINTS=%ROOT%\checkpoints"
set "PYTHONUTF8=1"
set "DATASET_JSON=%~f1"
set "TENSOR_OUT=%~f2"
set "EXTRA="
shift
shift
if "%~1"=="" goto run
:collect
set "EXTRA=!EXTRA! %1"
shift
if not "%~1"=="" goto collect
:run
cd /d "%ROOT%\upstream\ACE-Step-1.5" || exit /b 1
echo [preprocess_dataset] checkpoints=%KMM_CHECKPOINTS% env=%UV_PROJECT_ENVIRONMENT%
rem The module entry point is used on purpose: `train.py fixed --preprocess` rejects a call
rem without --dataset-dir/--output-dir (argparse required=True in training_v2/cli/args.py).
uv run python -m acestep.training_v2.cli.train_fixed --plain ^
  --checkpoint-dir "%KMM_CHECKPOINTS%" --model-variant turbo ^
  --preprocess --dataset-json "%DATASET_JSON%" --tensor-output "%TENSOR_OUT%" ^
  --max-duration 240 !EXTRA!
exit /b %ERRORLEVEL%
