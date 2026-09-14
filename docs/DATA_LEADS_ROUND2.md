# Data leads, round 2 (2026-09-14)

Follow-up to `DATA_SOURCES_CODEX.md` rows 3, 4 and 6. Rules applied: allowed = PD, CC0, CC BY, CC BY-SA, CC BY-NC(-SA) (NC flagged); not allowed = ND, all-rights-reserved, unclear uploader rights. No sign-ups, uploads, contacts or YouTube downloads. Licences quoted verbatim with the URL where stated.

**Net result: 1 new original fetched (the museum film, 460.611 s, CC BY-SA 4.0, VRT-confirmed). Master_of_Dombra stays a candidate (no file). kui-gen-dataset is not publicly accessible (private or deleted, not gated).**

Access notes for whoever repeats this: Python `urllib` fails TLS on this box ("certificate has expired"), so all fetches used `curl` with a User-Agent header; the Commons `action=parse` call hit the MediaWiki rate limit once ("You are making too many requests to the API") and succeeded on a single retry; `archive.org/wayback/available` returned HTTP 429 once and was not retried.

---

## Lead 1 — Commons `File:Master_of_Dombra.webm` (693 s, CC BY 3.0 via YouTube review)

**Decision: NOT FETCHED. Written: `data/raw/commons_master_of_dombra/DECISION.md` only.** No SOURCE.json, no manifest mirror, no bytes.

### What was checked

| Item | URL |
|---|---|
| Commons file page + imageinfo/extmetadata + last 20 revisions + categories | https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo%7Crevisions%7Ccategories&titles=File:Master_of_Dombra.webm |
| Commons upload log | https://commons.wikimedia.org/w/api.php?action=query&list=logevents&letitle=File:Master_of_Dombra.webm |
| Rendered file page (review box text) | https://commons.wikimedia.org/wiki/File:Master_of_Dombra.webm |
| File talk page, `User:Ербол Акпанов`, `User talk:Ербол Акпанов` | all **missing** on Commons (the name is only the YouTube channel credit; the Commons uploader was *Ser Amantio di Nicolao*) |
| YouTube oEmbed (public JSON) | https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=IyqdmbYs5EA&format=json |
| YouTube watch page HTML (public, no download) | https://www.youtube.com/watch?v=IyqdmbYs5EA |
| YouTube channel About and Videos tabs (public HTML) | https://www.youtube.com/@kazakhreview/about , https://www.youtube.com/@kazakhreview/videos |
| Wayback snapshot cited by YouTubeReviewBot | https://web.archive.org/web/20200212163514/https://www.youtube.com/watch?v=IyqdmbYs5EA |
| Frame stills (Commons thumb service and YouTube hqdefault thumbnail) | https://commons.wikimedia.org/w/thumb.php?f=Master_of_Dombra.webm&width=640 , https://i.ytimg.com/vi/IyqdmbYs5EA/hqdefault.jpg |

### Verbatim evidence

- Commons extmetadata: `LicenseShortName = "CC BY 3.0"`, `UsageTerms = "Creative Commons Attribution 3.0"`, `LicenseUrl = "https://creativecommons.org/licenses/by/3.0"`, `Attribution = "Ербол Акпанов"`, `Artist = <a href="https://www.youtube.com/channel/UCqzzD4mEiEZZYri049Kk7HQ">Ербол Акпанов</a>`.
- Current wikitext (rev 1073125905): `{{YouTube CC-BY|Ербол Акпанов}}` and `{{YouTubeReview|id=IyqdmbYs5EA|ChannelName=Kazakh review|ChannelID=UCqzzD4mEiEZZYri049Kk7HQ|title=Master of Dombra |archive=https://web.archive.org/web/20200212163514/https://www.youtube.com/watch?v=IyqdmbYs5EA|date=2020-02-12}}`; description is just "Master of Dombra"; `permission=` is empty.
- Upload log 2019-08-06, user *Ser Amantio di Nicolao*: "Imported media from https://www.youtube.com/watch?v=IyqdmbYs5EA".
- YouTubeReviewBot 2019-12-04: "License review status: Passed file, retrieved data from youtube.com/watch?v=IyqdmbYs5EA , checked page on 2019-12-04". 2020-02-12: "License review passed … Title of video: Master of Dombra … Channel Name: Kazakh review … Channel ID: UCqzzD4mEiEZZYri049Kk7HQ … Archived Video on WayBack Machine".
- Rendered Commons review box: "…was reviewed on 12 February 2020 by the automatic software YouTubeReviewBot , which confirmed that this video was available there under the stated Creative Commons license on that date. … **The bot only checks for the license, human review is still required to check if the video is a derivative work**, has freedom of panorama related issues and other copyright problems that might be present in the video."
- Wayback 2020 snapshot: "Creative Commons Attribution license (reuse allowed)"; `ownerChannelName":"Kazakh review"`.
- Live YouTube page (2026-09-14): License row "Creative Commons Attribution license (reuse allowed)"; `"ownerChannelName":"Yerbol Akpanov"`; `"uploadDate":"2018-04-08T20:38:12-07:00"`; `"shortDescription":""`; `"keywords":["КазНАУ","казахстан","агро"]`; `"category":"Music"`; `"viewCount":"959"`; channel `"subscriberCountText":"30.4K subscribers"`.
- oEmbed: `{"title":"Master of Dombra","author_name":"Yerbol Akpanov","author_url":"https://www.youtube.com/@kazakhreview"}`.
- Channel About: `"description":"Best music"`, `"joinedDateText":"Joined Feb 21, 2012"`, `"videoCountText":"1,210 videos"`, `"viewCountText":"7,488,977 views"`, one external link (Instagram `erbol8884`). Videos tab, first 30 items (all within 3 months): "Botagoz", "Sunshine in My Pocket", "The Tongue That Teaches", "The First Scar and the First Hug", "for relaxation", "The Last Move", "На полную", "The Pulse That Almost Stopped", "The Hush of the First Snow", … "The Hymn to Love", "Why Did You Get Me in a State" (3–397 views each).
- Frame stills: a seated young man in a light-blue jacket playing dombra in a banquet hall, microphone stand in front, guests standing behind; filmed from the audience. No broadcaster logo visible in the stills inspected.

### Why it stays a candidate

Gate part (a) — a Commons YouTubeReview confirming the CC BY tag — is met (twice by bot, plus Wayback and live page). Gate part (b) — nothing contradicting that the channel owner is the performer/rights holder — fails: the stills show an uncredited third-party performer being filmed; the channel owner is at most the videographer, whose CC BY cannot cover the performer's rights or the composition; the video description is empty; the channel profile (1,210 videos, "Best music", generic English song titles) reads as an aggregator; and Commons' own notice says human review is still required and none was ever done. This is "unclear uploader rights" under the project rules. What would flip it is spelled out in DECISION.md (a credit naming the performer as the channel owner, or a documented performer/composer permission, or a human Commons review).

### Files written

- `data/raw/commons_master_of_dombra/DECISION.md` (no media, no SOURCE.json) — sha256 `94ecc81af7a9aff7e0b190b65edf43bf0fd025969512c8dc9355a3785385b6be`, 4,941 bytes.

---

## Lead 2 — Commons `File:Жамбыл Жабаев туралы фильм.webm` (museum donation, CC BY-SA 4.0)

**Decision: FETCHED as a raw reference (not training-ready). Grouped with the sibling archival recording.**

### What was checked

| Item | URL |
|---|---|
| Commons imageinfo (url, size, sha1, extmetadata) + full revision history (10 revisions) + categories | https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo%7Crevisions%7Ccategories&titles=File:%D0%96%D0%B0%D0%BC%D0%B1%D1%8B%D0%BB%20%D0%96%D0%B0%D0%B1%D0%B0%D0%B5%D0%B2%20%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8B%20%D1%84%D0%B8%D0%BB%D1%8C%D0%BC.webm |
| File page | https://commons.wikimedia.org/wiki/File:%D0%96%D0%B0%D0%BC%D0%B1%D1%8B%D0%BB_%D0%96%D0%B0%D0%B1%D0%B0%D0%B5%D0%B2_%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8B_%D1%84%D0%B8%D0%BB%D1%8C%D0%BC.webm |
| Frozen evidence revision | https://commons.wikimedia.org/w/index.php?oldid=1185035712 |
| Original download | https://upload.wikimedia.org/wikipedia/commons/c/cc/%D0%96%D0%B0%D0%BC%D0%B1%D1%8B%D0%BB_%D0%96%D0%B0%D0%B1%D0%B0%D0%B5%D0%B2_%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8B_%D1%84%D0%B8%D0%BB%D1%8C%D0%BC.webm |

### Verbatim evidence

- Wikitext (rev 1185035712): `|source=Zhambyl museum |author=Zhambyl museum |permission={{PermissionTicket|id=2025081310002993|user=Lvova}}` … `{{cc-by-sa 4.0}}`; categories `Videos from Kazakhstan`, `Zhambyl museum`, `Files Uploaded by User:Sofiemama`, `Content donated by Zhambyl Museum`.
- extmetadata: `UsageTerms = "Creative Commons Attribution-Share Alike 4.0"`, `LicenseShortName = "CC BY-SA 4.0"`, `LicenseUrl = "https://creativecommons.org/licenses/by-sa/4.0"`, `Credit = "Zhambyl museum"`, `Artist = "Zhambyl museum"`; categories include `Items with VRTS permission confirmed`.
- Rendered permission notice: "The Wikimedia Foundation has received an e-mail confirming that the copyright holder has approved publication under the terms mentioned on this page. This correspondence has been reviewed by a Volunteer Response Team (VRT) member and stored in our permission archive. The correspondence is available to trusted volunteers as ticket #2025081310002993."
- Revision trail: uploaded 2025-08-10 by *Sofiemama* with `{{Permission_pending}}` ("Uploaded a work by Zhambyl museum from Zhambyl museum with UploadWizard"); AntiCompositeBot no-licence tag 2025-08-10; VRT member *Lvova* added the ticket and `{{cc-by-sa 4.0}}` on 2025-08-15 ("VRTS permission added", "This file has a license"); category edit 2026-03-22. Same ticket number as the already-fetched sibling.

### Integrity

- Commons imageinfo: size 416,712,804 bytes, SHA1 `35b6031a90297ff3df3b4a59cf851bb1546f7e92`, 720x540, video/webm, duration 460.611 s.
- Local: size 416,712,804 (match), SHA1 match, **SHA256 `ffd7646c2a5629706841a9944c89bdf2e0b88480524a2e863b706dc5ac70a6f3`**. curl HTTP 200 in 22.1 s; `downloaded_at` 2026-09-14T04:06:53Z.
- ffprobe (a:0): vorbis, 44100 Hz, 2 ch, 460.611 s. Full audio decode with `-xerror`: exit 0.
- volumedetect: mean −40.0 dBFS, max −15.3 dBFS — a very quiet transfer (about 22 dB below the sibling). Needs gain before any use; possibly a high noise floor. The sibling archival file peaks at +1.46 dBFS by astats (0.0 by volumedetect), i.e. at/above full scale — possible clipping there.

### Segment scan (both museum files)

Method: `ffmpeg silencedetect` (audio stream only) to find gaps, complement → continuous-sound ranges, keep ranges ≥ 30 s, then `astats` overall RMS/peak per range. Threshold sweep (d = 1.0 s):

| file | gate | gaps | ranges ≥ 30 s |
|---|---|---|---|
| film | −50 dB | 0 | 1 (whole file) |
| film | −45 dB | 5 | 3 |
| film | **−42 dB** | 14 | **3** |
| film | −40 dB | 18 | 4 |
| film | −38 dB | 18 | 3 |
| archival | −35 / −30 dB | 1 / 2 | 2 / 2 |
| archival | −27 dB | 4 | 4 |
| archival | **−25 dB** | 7 | **7** |
| archival | −22 / −20 dB | 14 / 23 | 10 / 11 |

A "file mean − 15 dB" gate (−55 dB film, −33.3 dB archival) produced zero gaps in both files, so the gates were chosen from the sweep: −42 dB for the film, −25 dB for the archival file. Written to `data/raw/zhambyl_museum_codex_film/segments.csv` (10 rows; columns file, start_s, end_s, duration_s, mean_db, note; the note records gate, peak and that content/instrument is not identified by ear):

| file | start_s | end_s | duration_s | mean_db |
|---|---:|---:|---:|---:|
| Жамбыл Жабаев туралы фильм.webm | 27.316 | 65.731 | 38.415 | −41.19 |
| Жамбыл Жабаев туралы фильм.webm | 96.621 | 326.077 | 229.456 | −39.90 |
| Жамбыл Жабаев туралы фильм.webm | 426.018 | 460.611 | 34.593 | −37.19 |
| Жамбыл Жабаевтың мұрағаттық бейнежазбасы.webm | 0.000 | 66.454 | 66.454 | −20.89 |
| Жамбыл Жабаевтың мұрағаттық бейнежазбасы.webm | 67.561 | 136.389 | 68.827 | −20.09 |
| Жамбыл Жабаевтың мұрағаттық бейнежазбасы.webm | 137.439 | 307.255 | 169.816 | −15.77 |
| Жамбыл Жабаевтың мұрағаттық бейнежазбасы.webm | 308.432 | 449.194 | 140.761 | −15.67 |
| Жамбыл Жабаевтың мұрағаттық бейнежазбасы.webm | 453.436 | 806.143 | 352.707 | −18.10 |
| Жамбыл Жабаевтың мұрағаттық бейнежазбасы.webm | 808.022 | 874.884 | 66.862 | −22.01 |
| Жамбыл Жабаевтың мұрағаттық бейнежазбасы.webm | 876.035 | 1123.570 | 247.535 | −23.02 |

These are level-continuity candidates only. Nothing here says what plays in them; that is for a human ear.

### Files written

| file | sha256 | bytes |
|---|---|---:|
| `data/raw/zhambyl_museum_codex_film/Жамбыл Жабаев туралы фильм.webm` | `ffd7646c2a5629706841a9944c89bdf2e0b88480524a2e863b706dc5ac70a6f3` | 416,712,804 |
| `data/raw/zhambyl_museum_codex_film/SOURCE.json` | `f3947630d93abe604892379aac9cfc66903007d3fab86eaeb3acefce9fb5d4f6` | 5,266 |
| `data/manifests/sources_zhambyl_museum_codex_film.SOURCE.json` (byte-identical mirror) | `f3947630d93abe604892379aac9cfc66903007d3fab86eaeb3acefce9fb5d4f6` | 5,266 |
| `data/raw/zhambyl_museum_codex_film/segments.csv` | `8a26aefc239ad88eaffb370c0ceabf1f7db445fcca14956a23e49e40c9afb420` | 3,008 |

SOURCE.json sets `group_id = zhambyl_museum_codex/archival_compilation_172158642` (same conservative group as the sibling, because the prior audit flagged possible footage overlap), `training_ready: false`, `verified_by_ear: false`, `noncommercial_restriction: false`, and embeds the evidence wikitext, VRT note, SHA1 verification, decode test and volume figures. The sibling's SOURCE.json was not modified.

---

## Lead 3 — Hugging Face `Eraly-ml/kui-gen-dataset`

**Decision: not accessible; not gated; either private or deleted. Nothing written to `data/`.**

### What was checked (all with a plain User-Agent, no token)

| URL | Result |
|---|---|
| https://huggingface.co/api/datasets/Eraly-ml/kui-gen-dataset (also `?full=true`, `/tree/main`, `/discussions`, `/croissant`) | HTTP 401 `{"error":"Invalid username or password."}` |
| https://huggingface.co/datasets/Eraly-ml/kui-gen-dataset/raw/main/README.md and `/resolve/main/README.md` | HTTP 401 "Invalid username or password." |
| https://huggingface.co/datasets/Eraly-ml/kui-gen-dataset (web page) | `<title>404 – Hugging Face</title>` |
| https://datasets-server.huggingface.co/info?dataset=Eraly-ml/kui-gen-dataset (and `/is-valid`) | HTTP 401 "The dataset does not exist, or is not accessible without authentication (private or gated). Please check the spelling of the dataset name or retry with authentication." |
| https://huggingface.co/api/datasets?author=Eraly-ml&full=true | HTTP 200, **3 datasets**: `Eraly-ml/mental_health_counseling_conversations-kk` (openrail, text), `Eraly-ml/kk-cc-data` (text), `Eraly-ml/TinyStories-kazakh-instruct` (text). No kui-gen. |
| https://huggingface.co/api/datasets?author=Eraly-ml&search=kui ; `?search=kui-gen` ; `?search=dombra` ; `?search=dombyra` ; `?search=күй` | `[]` for all (the generic `?search=kui` hits are unrelated: "kuih", "kuiper", …) |
| https://huggingface.co/api/users/Eraly-ml/overview | `"fullname":"Yeraly Gainulla"`, `"numDatasets":3`, `"numModels":10`, `"numSpaces":4`, `"details":"NLP"` |
| https://huggingface.co/api/models?author=Eraly-ml , `/api/spaces?author=Eraly-ml` | 10 models (KazBERT family, Skin-AI, TogyzkumalakRL, Kimi-K3 Kazakh CPT, …), 4 spaces; none music/audio |
| Control: https://huggingface.co/api/datasets/Eraly-ml/does-not-exist-xyz123 | HTTP 401 "Invalid username or password." — **HF returns the same 401 for a non-existent repo**, so the 401 alone proves nothing |
| Author homepage https://eraly-ml.github.io/ → http://yeraly.dsml.kz/ | lists KazBERT, DSML Young, SemEval-2026 Task 13 system, Cross-Kingdom Virtual Cells, Sentra, FLL 2026 robotics; no kui/dombra/audio project |
| GitHub https://api.github.com/users/Eraly-ml/repos (32 repos) and repo search `kui-gen OR kui_gen OR kuigen` | no kui-gen / dombra repository |
| Wayback availability API for the dataset page | HTTP 429 (once; not retried) |

### What it was (search-engine residue only)

Web search still indexes `https://huggingface.co/datasets/Eraly-ml/kui-gen-dataset/viewer` and a file `https://huggingface.co/datasets/Eraly-ml/kui-gen-dataset/resolve/main/metadata_with_descriptions.jsonl?download=true`; the search snippet describes entries such as "Zhalgyzayak (Lonely One)" as "a melancholic kui with instrumentation suggesting a dombra-centric arrangement with a mournful and reflective tone" — i.e. at some point it was a public dataset of audio files plus text descriptions of küys, apparently for text-to-music ("kui-gen") work. Both URLs now return 401. The snippet gives no licence, no author of the recordings, no count and no duration.

### Assessment

- **Gated?** No. Gated datasets appear in public author listings with `gated: "auto"/"manual"` (seen for other repos in the same search results); this one is absent from the author's 3-item public listing, so it is **private or deleted**, not gated. There is no gate to request through.
- **Licence:** not retrievable; nothing verbatim exists to quote. The descriptions in the snippet read like generated captions, which would also raise the question of where the underlying recordings came from.
- Do not count it. If it ever reappears publicly, evaluate its card and per-recording provenance from scratch.

---

## Unresolved doubts (all leads)

1. **Master_of_Dombra**: performer identity and consent unknown; küy composer unknown (could be a living composer); no human Commons review. Licence tag itself is solid. Decision reversible only with new evidence (see DECISION.md).
2. **Museum film**: content not heard; unknown whether it repeats the sibling's footage or contains third-party broadcast material re-donated by the museum (the VRT ticket covers the museum's grant; it cannot be verified from outside whether the museum holds every underlying performance). Audio is ~22 dB quieter than the sibling; the sibling's astats peak of +1.46 dBFS suggests clipping in places. ShareAlike terms must be preserved for any derivative.
3. **Segment table**: gates were picked by sweep, not by ear; rows are level-continuity candidates and may straddle scene cuts, narration and music alike.
4. **kui-gen-dataset**: existence of a former public version is inferred from search-engine residue only; licence, size and provenance are unknown; Wayback check not completed (429).
5. Nothing new is training-ready. Raw minutes added: 460.611 s of CC BY-SA 4.0 documentary audio, in the same source group as the earlier 1123.570 s file.
