# Saved-output viewer (offline, no server)

Double-click `viewer/index.html` (Chrome/Edge, `file://` is fine). It plays only WAVs already saved under `outputs/`; nothing is generated live and nothing autoplays.

1. Generate outputs (baseline / adapter sidecars under `outputs/<label>/<case_id>/`; optional `outputs/human_reference/<case_id>/*.wav`).
2. `py -3.12 scripts/build_viewer_manifest.py` writes `viewer/manifest.json` and `viewer/manifest.js` (the page reads the `.js` because Chrome cannot fetch JSON from `file://`). Existing `listening_notes` in `manifest.json` are preserved; `--notes <exported.json>` merges notes exported from the page.
3. If `manifest.js` is absent, the page falls back to an inline example built into `index.html` that carries the cases, lyrics and settings but NO outputs and NO notes, so only empty states render (it can never look like results). Adapter players show `adapter.scale_effective` when the sidecar has it (with the requested scale if different), else `adapter.scale`.

Listening notes save to the browser's localStorage per WAV path. "Export notes as JSON" shows them in a textarea (copy/paste; downloads may be blocked); "Import notes JSON" applies a pasted export.
Keyboard: Tab to a player card, Space to play/pause. Playing one card pauses the others.
`manifest.json` / `manifest.js` are generated (paths, dates, sizes) and are not in `.gitignore`; decide whether to commit them.
