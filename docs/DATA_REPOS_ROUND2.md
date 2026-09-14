# Data repositories, round 2 (2026-09-14) — REPOSITORIES agent

Scope: public data repositories and APIs, with Latin, Cyrillic (Kazakh/Russian) and Chinese query variants, extending
`docs/DATA_SOURCES_CODEX.md` (rows 1–50, not repeated here; cross-referenced as "CODEX #n") and `docs/DATA_LEADS_ROUND2.md`.
Licence rules as briefed: allowed = PD, CC0, CC BY, CC BY-SA, CC BY-NC(-SA) (NC flagged); not allowed = ND, all-rights-reserved,
unclear rights, gated (listed, never bypassed). No sign-ups, uploads, contacts or YouTube downloaders were used.

## Result in one paragraph

**Files fetched into `data/raw/`: 0. New independent recordings: 0. New minutes: 0.** 534 logged queries across 22 sources
(§3) surfaced exactly one new licence-clean, provenance-clean Kazakh dombra item — the Zhambyl museum's VRT-confirmed
`File:Жамбылдың домбырасы.webm` (CC BY-SA 4.0) — and it is a 26.334 s museum-exhibit clip of the instrument itself, so it fails
the 30 s floor and is not a performance (row 51). Everything else was either speech (ISSAI/OpenSLR/Common Voice corpora, sizes
recorded in §2.3), In-Copyright institutional archives (Europeana/Philharmonie de Paris/BnF), ND stock tracks (Jamendo via
Openverse), unlicensed hobby repos on GitHub, non-Kazakh "kui" false positives (Chuvash, Tatar, Dravidian Kui, Paiwan names), or
gated/private/restricted (Kazakh Songs ASR, KazLibri, kui-gen-dataset, Zenodo "Digital Yurt"). No sung-Kazakh corpus with
per-utterance text exists in the open; the only one that exists at all (yeshpanovrustem/kazakh_songs_asr, 3,013 line-level
segments, 4.5 h, 195 commercial songs) is gated + non-commercial and was confirmed as such by its LREC 2026 paper.

No file in `data/raw/`, `data/manifests/`, `data/lyrics/` or any other project file was created or modified by this agent; the
only write is this document. Raw evidence (every API response, `queries.jsonl`, `hits.jsonl`, scripts, the staged 2 MB clip and
its contact sheet) is in the session scratchpad
`C:\kmm\round2_repositories_claude\` (copied out of the session scratchpad; outside the repository)
(`round2_search.py`, `round2_extra.py`, `commons_round2.py`, `evidence/`).

## 1. Counting rules

| Decision | Rows | Meaning |
|---|---:|---|
| FETCHED | 0 | nothing met licence + ≥30 s + clearly dombra/Kazakh singing + clean provenance |
| CANDIDATE | 3 | needs a human decision (rights request, gated access, or another network) — rows 57, 64(b), 77 |
| EXCLUDED | 28 | rejected for this ingest, reason in the row (includes row 72, unclear rights) |
| NOT REACHABLE | 1 | row 81 (nlrk.kz); the 5 unreachable *platforms* are listed separately in §4, not as inventory rows |

Total: 32 inventory rows (51–82). One row may stand for a whole repository or catalogue. Rows start at 51 to continue the Codex inventory.

## 2. Inventory (new rows only)

Licence cells quote the observed label verbatim; "no licence stated" is an audit result, not a quotation. Durations are
source metadata unless marked "measured". Evidence URLs are the pages/API responses the licence string was read from.

### 2.1 Wikimedia Commons (CirrusSearch `filetype:audio|video` with Latin + Cyrillic terms)

| # | Source / URL | Title | Performer | Licence verbatim + evidence | Type | Duration | Lyrics | Decision / reason |
|---:|---|---|---|---|---|---|---|---|
| 51 | [Commons File:Жамбылдың домбырасы.webm](https://commons.wikimedia.org/wiki/File:%D0%96%D0%B0%D0%BC%D0%B1%D1%8B%D0%BB%D0%B4%D1%8B%D2%A3_%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0%D1%81%D1%8B.webm) (pageid 172155580) | Жамбылдың домбырасы / Zhambyl's Dombyra | none (exhibit clip of Zhambyl's own dombra, captions "шамамен 1885 жылдары жасалған") | "Creative Commons Attribution-Share Alike 4.0" — `{{cc-by-sa 4.0}}` + `{{PermissionTicket|id=2025081310002993}}`, category "Items with VRTS permission confirmed"; author/source "Zhambyl museum"; evidence: file page rev 1262331890 (`evidence/commons_round2_candidates_meta.json`) | museum object video; audio = unidentified music bed, unverified by ear | **26.334 s measured** (vp8 1136×640 + vorbis 44.1 kHz mono; mean −21.5 dB, peak −0.9 dB; full decode OK; SHA1 9d733d19… = Commons; SHA256 09074cd9…; not in existing hashes) | no | **EXCLUDED** — below the 30 s floor and not a performance (frames show the instrument on a table with captions). Staged only in scratch; **not** copied to `data/raw`. Strongest provenance of anything found this round; same VRT ticket as the two museum films already on disk. |
| 52 | Commons `File:Kazakhstan anthem a cappella.ogg` (pageid 118281255, uploader Krishtpt35) — still indexed by Openverse as `by-sa 4.0` | Kazakhstan anthem a cappella | Krishtpt35 (own work) | Commons log: **deleted 2023-05-30 by Krd, "No permission since 22 May 2023"** (`evidence/commons_anthem_acappella_log.json`) | vocal | unknown | anthem text known | **EXCLUDED** — file no longer exists; permission was refused. Openverse index is stale; do not trust its licence label. |
| 53 | [Commons File:Anthem of Kazakhstan 1991-2006.ogg](https://commons.wikimedia.org/wiki/File:Anthem_of_Kazakhstan_1991-2006.ogg) | State Anthem of the Kazakh SSR (band arrangement) | United States Navy Band | "Public domain" — `{{PD-USGov-Military-Navy}}` (performance) + `{{PD-KZ-exempt}}` (composition); evidence: file page rev 1051611739 | instrumental brass band | unknown (10.3 MB ogg) | n/a | **EXCLUDED** — no dombra, no voice (sibling of DATA_SOURCES row 11). |
| 54 | [Commons File:Coffin Dance on Komus (dombra).webm](https://commons.wikimedia.org/wiki/File:Coffin_Dance_on_Komus_(dombra).webm) | Coffin Dance on Komus (dombra) | Lev Tannagashev (Shor kai-komus) | "Creative Commons Attribution 3.0" — `{{YouTube CC-BY}}` + `{{YouTubeReview … date=2021-05-23}}` | 2-string lute, Shor (Siberia), internet meme tune | unknown (2 MB) | n/a | **EXCLUDED** — not Kazakh, not a küy; "dombra" only in the YouTube title. |
| 55 | [Commons File:Kazakh Girl.webm](https://commons.wikimedia.org/wiki/File:Kazakh_Girl.webm) | Kazakh Girl | NotGypsy (own work) | "Creative Commons Attribution-Share Alike 4.0" — `{{self|cc-by-sa-4.0}}` | speech (reading in English) | unknown (15 MB) | n/a | **EXCLUDED** — speech, English. |
| 56 | [Commons File:Traditional wedding of Kazakhs in China.webm](https://commons.wikimedia.org/wiki/File:Traditional_wedding_of_Kazakhs_in_China.webm) and [File:A Kazakh in China devoted his life to accordion.webm](https://commons.wikimedia.org/wiki/File:A_Kazakh_in_China_devoted_his_life_to_accordion.webm) | China News Service reports (Xinjiang Kazakhs) | CNS; interviewees speak Mandarin | "Creative Commons Attribution 3.0" — `{{YouTube CC-BY}}` (CNS YouTube channel) | news video, Mandarin speech, accordion | 102 MB / 62 MB | n/a | **EXCLUDED** — no Kazakh singing, no dombra; description says Kazakh language "not featured". |

Other Commons hits in these searches were pronunciation clips (`LL-*`, `Kk-*`, "Kazakh word …"), Soyuz launches, Adhan, post-office
news (`.ogv`), and the already-inventoried files (Moon and stars, Boz salkin, Master of Dombra, Singing in the Yurt, Paidang Sabardang,
Anthem of the Kazakh SSR, both museum films) — none new. 14 Cyrillic/English Commons searches did not run (network drop, §4).

### 2.2 Repositories: Zenodo, Figshare, Dataverse, OSF, Dryad, ScienceDB, IEEE DataPort, Openverse, Europeana

| # | Source / URL | Title | Performer | Licence verbatim + evidence | Type | Duration | Lyrics | Decision / reason |
|---:|---|---|---|---|---|---|---|---|
| 57 | [Zenodo 15689217](https://zenodo.org/records/15689217) | Digital Yurt (Yegizova, Gulniza, 2025-06-18) | unnamed | **no licence field; `access_right: restricted`; 0 files listed** (Zenodo API record) | multimedia project incl. "lullaby audio recordings" | unknown | unknown | **CANDIDATE** — the only Kazakh-vocal audio lead in Zenodo; restricted = gated, not requested. A human may ask the depositor; content (own recordings? language?) unknown. |
| 58 | [Zenodo 19327769](https://zenodo.org/records/19327769) | Central Asian Turkic Discourse Corpus (CATDiC) v1.1 — `kazakh.zip` | n/a | cc-by-4.0 (Zenodo API) | text corpus | n/a | n/a | **EXCLUDED** — text only (hit for "kazakh AND audio" because of wording). |
| 59 | Zenodo `kui` / `kuy` / `terme` hits (908 / 145 / 2,772 records) | e.g. "KUY-QO'SHIQ - TILI BILAN TA'SIRLI", Xorazm musiqa PDFs, Estonian "Kui …", "terme" = Italian spa towns | — | mostly cc-by-4.0 PDFs | publications, not audio | — | — | **EXCLUDED** — Uzbek "kuy" essays and unrelated languages; 0 Zenodo records carry Kazakh dombra/singing audio for any of 25 queries (§3). Codex's PDF-only dombra records (CODEX #42–44) re-confirmed: `dombra` = 8 hits, all PDF. |
| 60 | Figshare (61 queries; item_type dataset/media/any) | "Kui Tjuveljelem …" (British Museum, Paiwan builder), "Consent form by Kui …", "Weaving terme" (CODEX #49) | — | CC BY-NC-SA 4.0 (BM) | photos/video of house building, textiles | — | — | **EXCLUDED** — name/word false positives; 0 relevant for dombra / dombyra / домбыра / күй / кюй / қазақ әні / казахская песня / Kazakh singing / 冬不拉. |
| 61 | Harvard Dataverse (+9 other instances) | QazLip (lip-movement commands), MATERIAL Kazakh-English Language Pack (LDC), "national films released Kazakhstan…", Central Asian Food, SUSADICA surveys, Xinjiang bat acoustics | — | various (CC0 / LDC terms) | speech-video, text, images | — | — | **EXCLUDED** — no music. Other instances (dataverse.nl/.no, GRO Göttingen, TDL, UNC, AUSSDA, Edmond, UVA, demo): 0 relevant for dombra / kazakh / kui / домбыра / күй / қазақ. |
| 62 | Europeana API (57 queries, `profile=rich`, with `reusability=open|permission|restricted` and `qf=TYPE:SOUND|VIDEO`) | [Philharmonie de Paris "Musiques et danses d'Asie centrale : joute des bardes" (Salamatkan Sadykova, dombra)](https://www.europeana.eu/item/614/UNI2_0082237); ["Playing of the bardes of Central Asia" video (Hamit Rayimbergen, dombra)](https://www.europeana.eu/item/614/UNI4_0240445); ["The roads of the East – Central Asia: Step music"](https://www.europeana.eu/item/614/UNI2_0937192); [BnF "Chants des peuples soviétiques : Kazakhstan" (Soultanov F., dombra)](https://www.europeana.eu/item/9200516/ark__12148_bpt6k88251927) | named Kazakh dombra players / Soviet-era Kazakh singers | `http://rightsstatements.org/vocab/InC/1.0/` on every one (API `rights` field) | vocal+dombra / dombra solo, concert & LP recordings | unknown | no | **EXCLUDED** — In Copyright. Of 234 unique SOUND/VIDEO items returned, 186 are InC; the 45 open-licensed ones are bird songs (Naturalis), Estonian/Tatar/Dravidian "Kui" (BnF Archives de la Parole, PD mark) and one Ars Electronica video. `reusability=open` + `TYPE:SOUND` = **0** for dombra, kazakh, домбра. |
| 63 | Openverse audio API (16 queries, anonymous page_size 20) | Jamendo "Dombyra On The Road", "Dombyra slow 1", "Ordinary Dombyra", "Fast Dombyra 1", "Kazakh Night 1/2", "Kazakh Thrill 1–3", "Kazakh Strings fast" (Vladimir Ney) | Vladimir Ney | `by-nc-nd 3.0` (Openverse licence field) | synth/ethnic stock instrumentals | 16–92 s | n/a | **EXCLUDED** — ND (same family as CODEX #30 / DATA_SOURCES row 19). Remaining hits: Commons pronunciation clips (<3 s), Freesound station announcements (CODEX #33), Commons [Kui tuva üä tüttär.ogg](https://commons.wikimedia.org/w/index.php?curid=155075485) CC BY-SA 3.0 41.8 s — a **Chuvash** song, not Kazakh; and the deleted a-cappella anthem (row 52). |
| 64 | Dryad, ScienceDB, IEEE DataPort, Mendeley Data | — | — | — | — | — | — | (a) **EXCLUDED** — Dryad 0/7 queries; IEEE DataPort search page returns only its two featured items for every query; Mendeley/ScienceDB via web search 0. (b) **CANDIDATE** for a human only in the sense that ScienceDB's public search API is 404 and its site was not browsed manually; Xinjiang-Kazakh (哈萨克/冬不拉) material would live there if anywhere. |

### 2.3 Sung-Kazakh / speech corpora (sizes recorded; all speech unless stated)

| # | Source / URL | Title | Speakers | Licence verbatim + evidence | Type | Size | Text | Decision / reason |
|---:|---|---|---|---|---|---|---|---|
| 65 | [ACL Anthology 2026.lrec-1.431](https://aclanthology.org/2026.lrec-1.431/) → HF `yeshpanovrustem/kazakh_songs_asr` | Using Songs to Improve Kazakh ASR (Yeshpanov, LREC 2026) | 36 commercial artists, 195 songs | paper: "released on Hugging Face for research purposes under a **gated, non-commercial licence**"; HF card `license: other`, gated manual | **sung Kazakh, line-level** | 3,013 pairs, ~4.5 h | yes, verbatim per line | **EXCLUDED** (gated; underlying songs commercial) — cross-ref CODEX #16, DATA_SOURCES row 14. The only sung-Kazakh corpus with per-utterance text that exists. |
| 66 | [HF yeshpanovrustem/kazlibri](https://huggingface.co/datasets/yeshpanovrustem/kazlibri) | KazLibri (narrated books) | narrators | gated manual; `extra_gated_prompt`: "Use of this dataset for commercial purposes is strictly prohibited…"; card: "released strictly for research and educational purposes only" | read speech | 4,441 utterances, 3.43 GB download | yes | **EXCLUDED** — speech, gated NC. |
| 67 | [OpenSLR 102](https://www.openslr.org/102/) / [HF issai/Kazakh_Speech_Corpus_2](https://huggingface.co/datasets/issai/Kazakh_Speech_Corpus_2) / [ISSAI datasets](https://issai.nu.edu.kz/issai-datasets/) | KSC (2021) / KSC2 (2022) | crowd | KSC: "Attribution 4.0 International (CC BY 4.0)" (OpenSLR); KSC2: CC BY 4.0 (ISSAI page) but HF card says `license: mit` — inconsistent | read speech | KSC ~332 h / 153k utt.; KSC2 ~1,200 h | yes | **EXCLUDED** — speech. Sizes recorded as briefed. |
| 68 | [OpenSLR 140](https://www.openslr.org/140/) | Kazakh Speech Dataset (KSD, Mansurova & Kadyrbek 2023) | crowd | "Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0 US)" (OpenSLR) | read speech | 554 h / 204,250 utt.; 4 zips 12–16 GB | yes | **EXCLUDED** — speech. |
| 69 | [HF issai/KazakhTTS](https://huggingface.co/datasets/issai/KazakhTTS), [ai4kazakh/ISSAI_KazakhTTS2](https://huggingface.co/datasets/ai4kazakh/ISSAI_KazakhTTS2), [issai/KazEmoTTS](https://huggingface.co/datasets/issai/KazEmoTTS) / [ai4kazakh/ISSAI_KazEmoTTS](https://huggingface.co/datasets/ai4kazakh/ISSAI_KazEmoTTS) | KazakhTTS (93 h, 2 speakers), KazakhTTS2 (271 h, 5 speakers), KazEmoTTS (74.85 h, 3 narrators, 6 emotions) | professional readers | ISSAI page: CC BY 4.0 for KazakhTTS2; arXiv 2404.01033: KazEmoTTS "under the Creative Commons Attribution 4.0 International License"; HF cards carry no licence field | TTS read speech | 93 h / 271 h / 74.85 h | yes | **EXCLUDED** — speech (cross-ref DATA_SOURCES row 15). |
| 70 | [cv-dataset scripted-speech cv-corpus-26.0-2026-06-12.json](https://raw.githubusercontent.com/common-voice/cv-dataset/main/datasets/scripted-speech/cv-corpus-26.0-2026-06-12.json) (`locales.kk`) | Mozilla Common Voice Scripted Speech 26.0 — Kazakh | 204 contributors | CC0 (Common Voice policy; per-release page on Mozilla Data Collective is a JS shell) | read speech | **2,888 clips, 3.98 h total, 2.52 h validated, 82,320,197 B** (25.0: 2,834 clips / 3.89 h / 2.5 h validated; Data Collective page for 24.0: 2,750 clips, 3.76 h, 2.39 h validated, 193 speakers) | yes | **EXCLUDED** — speech; size recorded as briefed. HF `common_voice_17_0` card: "Effective October 2025, Mozilla Common Voice datasets are now exclusively available on the Mozilla Data Collective" (login required there). |

### 2.4 GitHub (39 repo/code searches, incl. Cyrillic and 冬不拉; 25 new repo trees audited via `gh api`)

| # | Source / URL | Title | Performer | Licence + evidence | Type | Duration | Lyrics | Decision / reason |
|---:|---|---|---|---|---|---|---|---|
| 71 | [msagatov98/DombyraUirenu](https://github.com/msagatov98/DombyraUirenu) | dombyra learning app (2020) | unknown | **no licence file** (`gh api repos/... .license = null`); README 404 | 10 küy mp3s (`res/kuis/kui0–9.mp3`, 1.2–9.6 MB each), 10 song mp3s, 40 voice/note clips; 44.6 MB | unknown | no | **EXCLUDED** — no licence, no provenance (app assets, likely ripped). Not downloaded. |
| 72 | [almita215/Kazakhstan](https://github.com/almita215/Kazakhstan) | educational site (2026) | unknown | no licence | `media/music.mp3` (2.0 MB), `media/kz.mp4` (25 MB) | unknown | no | **EXCLUDED** — unclear rights (no licence, no source stated); would only become a candidate if the author documents the recording's origin. Not downloaded. |
| 73 | [TempiSkat/DombraFinal](https://github.com/TempiSkat/DombraFinal) `song1.mp3` (745 KB); [zhanibek05/dombyra_notes](https://github.com/zhanibek05/dombyra_notes) (20 note mp3s, 0.6 MB); [baeuke/dombyra-tuner](https://github.com/baeuke/dombyra-tuner) `tuner.mp3`; [bakythanlym-maker/sandyq-dombyra](https://github.com/bakythanlym-maker/sandyq-dombyra) (11 KB m4a); [zhanibek05/dombra-AI-server](https://github.com/zhanibek05/dombra-AI-server) (MIDI only) | virtual-dombra / tuner apps | — | no licence files | single notes, tuner tones, one short song | <30 s or unknown | no | **EXCLUDED** — samples/notes, no rights statement (same pattern as CODEX #36–41). |
| 74 | [byergesh/Dombyra-Chords-Classification](https://github.com/byergesh/Dombyra-Chords-Classification) | 22-class dombyra chord sound classification (2024) | — | no licence; notebooks only | audio **not in repo** | — | — | **EXCLUDED** — data withheld; no releases. |
| 75 | [ouiMalika/dombra-tab-generator](https://github.com/ouiMalika/dombra-tab-generator), [aiaulym1101-glitch/an-kuy-academy](https://github.com/aiaulym1101-glitch/an-kuy-academy), [badelbeknarkulan70-sys/my-kuy-creative-project](https://github.com/badelbeknarkulan70-sys/my-kuy-creative-project), [Makkssat/aisultan-dombyra-music](https://github.com/Makkssat/aisultan-dombyra-music), [daniyalbazarbek/DombyraAPP](https://github.com/daniyalbazarbek/DombyraAPP) (MIT), [srmbackisdeveloper/DombyraWorld](https://github.com/srmbackisdeveloper/DombyraWorld), [a1pamys/Shyrqa](https://github.com/a1pamys/Shyrqa) (guitar chords for Kazakh songs), [yourbaur/auenCloud-iOS](https://github.com/yourbaur/auenCloud-iOS), [zzertexx/dombyra.plus](https://github.com/zzertexx/dombyra.plus), [astigmacist/dombra-tuner](https://github.com/astigmacist/dombra-tuner), 5× AlisherToleukhanov-sketch tuner repos, [Sagynysh1704/dombyra_tabs](https://github.com/Sagynysh1704/dombyra_tabs), [nurnurgulseilhanova-rgb/dombyra_by_sultan_elamanov](https://github.com/nurnurgulseilhanova-rgb/dombyra_by_sultan_elamanov) | code / websites / tabs | — | mostly no licence | **0 audio files** in trees; 0 releases | — | — | **EXCLUDED** — no audio. GitHub code search (`dombra extension:wav|mp3`, `домбыра extension:mp3`, `күй extension:mp3`, …) returned 0 real hits; `filename:metadata.csv` hits are place-name false positives. |

### 2.5 Academic and other

| # | Source / URL | Title | Licence + evidence | Type | Decision / reason |
|---:|---|---|---|---|---|
| 76 | [Astana IT University journal, art. 476](https://journal.astanait.edu.kz/index.php/ojs/article/view/476) | Classification of Kazakh Music Genres Using ML (Mimenbayeva et al.) — 800 tracks, 5 genres (classical, jazz, Kazakh rock/hip-hop/pop) | article CC BY-NC-ND 4.0; **dataset not released** (no URL/DOI) | mainstream genres, not dombra | **EXCLUDED** — unreleased, off-genre. |
| 77 | [archive.org: MusicRepublic "World Traditional Music from LPs and Cassettes" full archive](https://archive.org/details/musicrepublic-world-traditional-music-from-lps-and-cassettes-full-archive) (from web search: includes "Voyage en URSS n°7 Kazakhstan & Kirghistan", M. Khamzin, dombra) | LP/cassette rips of Melodiya / Le Chant du Monde records | **could not be read** — archive.org reset every connection (§4); Melodiya-era phonograms are in copyright unless the item's `licenseurl` says otherwise | dombra solo / vocal, 1960s–80s LPs | **CANDIDATE** for a human on another network: read the item's `licenseurl`/`rights`; expect "unclear rights" → exclude. Not fetched. |
| 78 | [UNESCO ICH RL 00996 "Kazakh traditional art of Dombra Kuy"](https://ich.unesco.org/en/RL/kazakh-traditional-art-of-dombra-kuy-00996) | nomination video | "© 2013 by A. Suleyev"; photos "© S. Suleimenova-Bazargalieva"; no open licence | video with dombra | **EXCLUDED** — all rights reserved. |
| 79 | HF `Eraly-ml/kui-gen-dataset` | (cross-ref CODEX #6; DATA_LEADS_ROUND2 Lead 3) | API / README / tree / `resolve` all HTTP 401 "Invalid username or password."; author listing (3 datasets, 10 models, all NLP) does not include it | was: küy audio + kk/en descriptions (search-engine residue: Байжұма, Ақшолпан, Жігер) | **EXCLUDED** — private or deleted, not gated; nothing to request. |
| 80 | [kazneb.kz audio catalogue](https://kazneb.kz/ru/catalogue/result?dType=15) | "Қазақтың дәстүрлі 1000 күйі" (EL production company, 2009, 41 CDs) — e.g. [Ақсақ қаз, Б. Мусин, 01:23](https://kazneb.kz/ru/catalogue/view/1510479) | catalogue exposes performer, track, duration, "Мәдени мұра" programme; **no terms/agreement page** (`/ru/agreement`, `/ru/rules` → 404; About page describes KazNEB as a Ministry of Culture state information system, no reuse grant) | dombra solo | **EXCLUDED** — no allowed licence (cross-ref CODEX #7–9). Best-documented Kazakh küy repertoire anywhere; rights would have to be negotiated by a human. |
| 81 | [nlrk.kz](https://nlrk.kz/ru) | National Library of RK | HTTP 200, 845-byte JS shell; `/api/` 404 | — | **NOT REACHABLE** as content. |
| 82 | Europeana "kui" Archives de la Parole (BnF): "Ižbuldin: duet; Ahmed-Safa Kui" (Tatar), "Kui ma olin wäiksekene" (Estonian), "[Marriage song] in Kui from Vizagapatam" (Dravidian Kui) | 1910s–30s field recordings | `creativecommons.org/publicdomain/mark/1.0/` / `NoC-OKLR` | vocal, non-Kazakh | **EXCLUDED** — not Kazakh; "kui" homonyms. |

## 3. Query log (every query run: source + query + HTTP + hit count)

534 rows. Sources and query sets: Latin (`dombra`, `dombyra`, `kui`, `kuy`, `terme`, `zhyr`, `qazaq`, `Kazakh folk song`,
`Kazakh singing`, `Kazakh music dataset`), Kazakh Cyrillic (`домбыра`, `күй`, `қазақ әні`, `жыр`, `терме`, `қобыз`), Russian
(`домбра`, `кюй`, `казахская песня`, `казахская музыка`), Chinese (`冬不拉`, `哈萨克 民歌`, `哈萨克族 音乐`, `哈萨克 演唱`). All Cyrillic
was percent-encoded by `requests` (Codex's earlier Cyrillic→`?` and Zenodo 400s were encoding/page-size faults: Zenodo anonymous
`size` max is 25, so every Zenodo query below was paged 4×25). Hit counts are the API's own totals; "—" = the endpoint returns
no count (page scrape, direct file, etc.).


#### Hugging Face (72 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| hf | `dombra [datasets]` | https://huggingface.co/api/datasets?search=dombra | 200 | 0 |  |
| hf | `dombra [models]` | https://huggingface.co/api/models?search=dombra | 200 | 1 |  |
| hf | `dombyra [datasets]` | https://huggingface.co/api/datasets?search=dombyra | 200 | 0 |  |
| hf | `dombyra [models]` | https://huggingface.co/api/models?search=dombyra | 200 | 1 |  |
| hf | `домбыра [datasets]` | https://huggingface.co/api/datasets?search=домбыра | 200 | 0 |  |
| hf | `домбыра [models]` | https://huggingface.co/api/models?search=домбыра | 200 | 0 |  |
| hf | `домбра [datasets]` | https://huggingface.co/api/datasets?search=домбра | 200 | 0 |  |
| hf | `домбра [models]` | https://huggingface.co/api/models?search=домбра | 200 | 0 |  |
| hf | `kui [datasets]` | https://huggingface.co/api/datasets?search=kui | 200 | 43 |  |
| hf | `kui [models]` | https://huggingface.co/api/models?search=kui | 200 | 87 |  |
| hf | `kuy [datasets]` | https://huggingface.co/api/datasets?search=kuy | 200 | 19 |  |
| hf | `kuy [models]` | https://huggingface.co/api/models?search=kuy | 200 | 71 |  |
| hf | `күй [datasets]` | https://huggingface.co/api/datasets?search=күй | 200 | 0 |  |
| hf | `күй [models]` | https://huggingface.co/api/models?search=күй | 200 | 0 |  |
| hf | `кюй [datasets]` | https://huggingface.co/api/datasets?search=кюй | 200 | 0 |  |
| hf | `кюй [models]` | https://huggingface.co/api/models?search=кюй | 200 | 0 |  |
| hf | `zhyr [datasets]` | https://huggingface.co/api/datasets?search=zhyr | 200 | 0 |  |
| hf | `zhyr [models]` | https://huggingface.co/api/models?search=zhyr | 200 | 0 |  |
| hf | `terme [datasets]` | https://huggingface.co/api/datasets?search=terme | 200 | 48 |  |
| hf | `terme [models]` | https://huggingface.co/api/models?search=terme | 200 | 11 |  |
| hf | `qazaq [datasets]` | https://huggingface.co/api/datasets?search=qazaq | 200 | 0 |  |
| hf | `qazaq [models]` | https://huggingface.co/api/models?search=qazaq | 200 | 2 |  |
| hf | `kazakh song [datasets]` | https://huggingface.co/api/datasets?search=kazakh song | 200 | 1 |  |
| hf | `kazakh song [models]` | https://huggingface.co/api/models?search=kazakh song | 200 | 0 |  |
| hf | `kazakh music [datasets]` | https://huggingface.co/api/datasets?search=kazakh music | 200 | 0 |  |
| hf | `kazakh music [models]` | https://huggingface.co/api/models?search=kazakh music | 200 | 0 |  |
| hf | `kazakh sing [datasets]` | https://huggingface.co/api/datasets?search=kazakh sing | 200 | 0 |  |
| hf | `kazakh sing [models]` | https://huggingface.co/api/models?search=kazakh sing | 200 | 0 |  |
| hf | `kazakh folk [datasets]` | https://huggingface.co/api/datasets?search=kazakh folk | 200 | 0 |  |
| hf | `kazakh folk [models]` | https://huggingface.co/api/models?search=kazakh folk | 200 | 0 |  |
| hf | `казах [datasets]` | https://huggingface.co/api/datasets?search=казах | 200 | 0 |  |
| hf | `казах [models]` | https://huggingface.co/api/models?search=казах | 200 | 0 |  |
| hf | `қазақ [datasets]` | https://huggingface.co/api/datasets?search=қазақ | 200 | 0 |  |
| hf | `қазақ [models]` | https://huggingface.co/api/models?search=қазақ | 200 | 0 |  |
| hf | `kazakh audio [datasets]` | https://huggingface.co/api/datasets?search=kazakh audio | 200 | 1 |  |
| hf | `kazakh audio [models]` | https://huggingface.co/api/models?search=kazakh audio | 200 | 0 |  |
| hf | `kazakh vocal [datasets]` | https://huggingface.co/api/datasets?search=kazakh vocal | 200 | 0 |  |
| hf | `kazakh vocal [models]` | https://huggingface.co/api/models?search=kazakh vocal | 200 | 0 |  |
| hf | `kk music [datasets]` | https://huggingface.co/api/datasets?search=kk music | 200 | 0 |  |
| hf | `kk music [models]` | https://huggingface.co/api/models?search=kk music | 200 | 1 |  |
| hf | `author=Eraly-ml [datasets]` | https://huggingface.co/api/datasets?author=Eraly-ml | 200 | 3 |  |
| hf | `author=Eraly-ml [models]` | https://huggingface.co/api/models?author=Eraly-ml | 200 | 10 |  |
| hf | `author=rtrk [datasets]` | https://huggingface.co/api/datasets?author=rtrk | 200 | 1 |  |
| hf | `author=rtrk [models]` | https://huggingface.co/api/models?author=rtrk | 200 | 0 |  |
| hf | `author=issai [datasets]` | https://huggingface.co/api/datasets?author=issai | 200 | 77 |  |
| hf | `author=issai [models]` | https://huggingface.co/api/models?author=issai | 200 | 37 |  |
| hf | `author=ai4kazakh [datasets]` | https://huggingface.co/api/datasets?author=ai4kazakh | 200 | 3 |  |
| hf | `author=ai4kazakh [models]` | https://huggingface.co/api/models?author=ai4kazakh | 200 | 0 |  |
| hf | `author=yeshpanovrustem [datasets]` | https://huggingface.co/api/datasets?author=yeshpanovrustem | 200 | 8 |  |
| hf | `author=yeshpanovrustem [models]` | https://huggingface.co/api/models?author=yeshpanovrustem | 200 | 2 |  |
| hf | `author=IS2AI [datasets]` | https://huggingface.co/api/datasets?author=IS2AI | 200 | 0 |  |
| hf | `author=IS2AI [models]` | https://huggingface.co/api/models?author=IS2AI | 200 | 0 |  |
| hf | `author=KazNU [datasets]` | https://huggingface.co/api/datasets?author=KazNU | 200 | 0 |  |
| hf | `author=KazNU [models]` | https://huggingface.co/api/models?author=KazNU | 200 | 0 |  |
| hf | `author=kazakh-ai [datasets]` | https://huggingface.co/api/datasets?author=kazakh-ai | 200 | 0 |  |
| hf | `author=kazakh-ai [models]` | https://huggingface.co/api/models?author=kazakh-ai | 200 | 0 |  |
| hf | `author=SILA-AI [datasets]` | https://huggingface.co/api/datasets?author=SILA-AI | 200 | 0 |  |
| hf | `author=SILA-AI [models]` | https://huggingface.co/api/models?author=SILA-AI | 200 | 0 |  |
| hf | `author=Kazakhstan [datasets]` | https://huggingface.co/api/datasets?author=Kazakhstan | 200 | 0 |  |
| hf | `author=Kazakhstan [models]` | https://huggingface.co/api/models?author=Kazakhstan | 200 | 0 |  |
| hf | `direct Eraly-ml/kui-gen-dataset` | https://huggingface.co/api/datasets/Eraly-ml/kui-gen-dataset?full=true | 401 | — | {'error': 'Invalid username or password.'} |
| hf | `direct mozilla-foundation/common_voice_17_0` | https://huggingface.co/api/datasets/mozilla-foundation/common_voice_17_0?full=true | 200 | — | {'_id': '68fbbe8e691e0c27af4ae1d6', 'id': 'mozilla-foundation/common_voice_17_0', 'author': 'mozilla-foundation', 'sha': '11dc88355e899d1... |
| hf | `direct mozilla-foundation/common_voice_16_1` | https://huggingface.co/api/datasets/mozilla-foundation/common_voice_16_1?full=true | 401 | — | {'error': 'Invalid username or password.'} |
| hf | `direct issai/KazakhTTS` | https://huggingface.co/api/datasets/issai/KazakhTTS?full=true | 200 | — | {'_id': '678a563b1cfff01c1fab0d64', 'id': 'issai/KazakhTTS', 'author': 'issai', 'sha': '821c7d583331fd2ae50283a00147772ef0734fd2', 'lastM... |
| hf | `direct ai4kazakh/ISSAI_KazakhTTS2` | https://huggingface.co/api/datasets/ai4kazakh/ISSAI_KazakhTTS2?full=true | 200 | — | {'_id': '69ca1f01b70d117a465014c5', 'id': 'ai4kazakh/ISSAI_KazakhTTS2', 'author': 'ai4kazakh', 'sha': 'bcf754ffb4074e48e6dae6aa7e0b83630f... |
| hf | `direct issai/Kazakh_Speech_Corpus_2` | https://huggingface.co/api/datasets/issai/Kazakh_Speech_Corpus_2?full=true | 200 | — | {'_id': '678a563c4c08258a520fb007', 'id': 'issai/Kazakh_Speech_Corpus_2', 'author': 'issai', 'sha': 'cececbec1049f93f34a7421552500da01971... |
| hf | `冬不拉 [datasets]` | https://huggingface.co/api/datasets?search=冬不拉 | 200 | 0 |  |
| hf | `哈萨克 民歌 [datasets]` | https://huggingface.co/api/datasets?search=哈萨克 民歌 | 200 | 0 |  |
| hf | `哈萨克族 音乐 [datasets]` | https://huggingface.co/api/datasets?search=哈萨克族 音乐 | 200 | 0 |  |
| hf | `哈萨克 演唱 [datasets]` | https://huggingface.co/api/datasets?search=哈萨克 演唱 | 200 | 0 |  |
| hf | `kazakh kui [datasets]` | https://huggingface.co/api/datasets?search=kazakh kui | 200 | 0 |  |
| hf | `kazakh dombra [datasets]` | https://huggingface.co/api/datasets?search=kazakh dombra | 200 | 0 |  |

#### Europeana (57 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| europeana | `dombra [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich | 200 | 81 |  |
| europeana | `dombra [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&qf=TYPE%3A... | 200 | 4 |  |
| europeana | `dombra [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&qf=TYPE%3A... | 200 | 2 |  |
| europeana | `dombyra [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombyra&rows=100&profile=rich | 200 | 0 |  |
| europeana | `dombyra [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombyra&rows=100&profile=rich&qf=TYPE%3... | 200 | 0 |  |
| europeana | `dombyra [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombyra&rows=100&profile=rich&qf=TYPE%3... | 200 | 0 |  |
| europeana | `домбра [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&ro... | 200 | 0 |  |
| europeana | `домбра [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&ro... | 200 | 0 |  |
| europeana | `домбра [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&ro... | 200 | 0 |  |
| europeana | `домбыра [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0... | 200 | 0 |  |
| europeana | `домбыра [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0... | 200 | 0 |  |
| europeana | `домбыра [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0... | 200 | 0 |  |
| europeana | `kui [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kui&rows=100&profile=rich | 200 | 13684 |  |
| europeana | `kui [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kui&rows=100&profile=rich&qf=TYPE%3ASOUND | 200 | 31 |  |
| europeana | `kui [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kui&rows=100&profile=rich&qf=TYPE%3AVIDEO | 200 | 4 |  |
| europeana | `kuy [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kuy&rows=100&profile=rich | 200 | 115 |  |
| europeana | `күй [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D2%AF%D0%B9&rows=100&profile=rich | 200 | 0 |  |
| europeana | `күй [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D2%AF%D0%B9&rows=100&profile=ric... | 200 | 0 |  |
| europeana | `күй [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D2%AF%D0%B9&rows=100&profile=ric... | 200 | 0 |  |
| europeana | `кюй [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D1%8E%D0%B9&rows=100&profile=rich | 200 | 0 |  |
| europeana | `қазақ әні [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B+%D3%99%D... | 200 | 0 |  |
| europeana | `казахская песня [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0... | 200 | 0 |  |
| europeana | `казахская музыка [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0... | 200 | 0 |  |
| europeana | `казахская музыка [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0... | 200 | 0 |  |
| europeana | `казахская музыка [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0... | 200 | 0 |  |
| europeana | `Kazakh folk song [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=Kazakh+folk+song&rows=100&profile=rich | 200 | 1 |  |
| europeana | `Kazakh folk song [reusability=None qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=Kazakh+folk+song&rows=100&profile=rich&... | 200 | 0 |  |
| europeana | `Kazakh folk song [reusability=None qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=Kazakh+folk+song&rows=100&profile=rich&... | 200 | 0 |  |
| europeana | `Kazakh singing [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=Kazakh+singing&rows=100&profile=rich | 200 | 1 |  |
| europeana | `terme [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=terme&rows=100&profile=rich | 200 | 31312 |  |
| europeana | `zhyr [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=zhyr&rows=100&profile=rich | 200 | 0 |  |
| europeana | `жыр [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B6%D1%8B%D1%80&rows=100&profile=rich | 200 | 0 |  |
| europeana | `терме [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D1%82%D0%B5%D1%80%D0%BC%D0%B5&rows=100... | 200 | 464 |  |
| europeana | `Kazakh music dataset [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=Kazakh+music+dataset&rows=100&profile=rich | 200 | 0 |  |
| europeana | `qazaq music [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=qazaq+music&rows=100&profile=rich | 200 | 0 |  |
| europeana | `dombra [reusability=open qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&reusabilit... | 200 | 26 |  |
| europeana | `dombra [reusability=open qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&reusabilit... | 200 | 0 |  |
| europeana | `dombra [reusability=open qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&reusabilit... | 200 | 0 |  |
| europeana | `kazakh [reusability=open qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 1932 |  |
| europeana | `kazakh [reusability=open qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 0 |  |
| europeana | `kazakh [reusability=open qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 0 |  |
| europeana | `домбра [reusability=open qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&ro... | 200 | 0 |  |
| europeana | `домбра [reusability=open qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&ro... | 200 | 0 |  |
| europeana | `домбра [reusability=open qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&ro... | 200 | 0 |  |
| europeana | `kazakh [reusability=permission qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 229 |  |
| europeana | `kazakh [reusability=permission qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 9 |  |
| europeana | `kazakh [reusability=permission qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 111 |  |
| europeana | `dombra [reusability=restricted qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&reusabilit... | 200 | 25 |  |
| europeana | `dombra [reusability=restricted qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&reusabilit... | 200 | 0 |  |
| europeana | `dombra [reusability=restricted qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dombra&rows=100&profile=rich&reusabilit... | 200 | 0 |  |
| europeana | `kazakh [reusability=restricted qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 179 |  |
| europeana | `kazakh [reusability=restricted qf=TYPE:SOUND]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 20 |  |
| europeana | `kazakh [reusability=restricted qf=TYPE:VIDEO]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kazakh&rows=100&profile=rich&reusabilit... | 200 | 2 |  |
| europeana | `казах* [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%2A&rows=... | 200 | 2245 |  |
| europeana | `qazaq [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=qazaq&rows=100&profile=rich | 200 | 3 |  |
| europeana | `kobyz [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=kobyz&rows=100&profile=rich | 200 | 33 |  |
| europeana | `dutar kazakh [reusability=None qf=None]` | https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=dutar+kazakh&rows=100&profile=rich | 200 | 3 |  |

#### Figshare (61 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| figshare | `dombra [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=dombra | 200 | 0 | title-relevant=0 |
| figshare | `dombra [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=dombra | 200 | 0 | title-relevant=0 |
| figshare | `dombra [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=dombra | 200 | 0 | title-relevant=0 |
| figshare | `dombyra [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=dombyra | 200 | 0 | title-relevant=0 |
| figshare | `dombyra [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=dombyra | 200 | 0 | title-relevant=0 |
| figshare | `dombyra [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=dombyra | 200 | 0 | title-relevant=0 |
| figshare | `домбра [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=домбра | 200 | 0 | title-relevant=0 |
| figshare | `домбра [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=домбра | 200 | 0 | title-relevant=0 |
| figshare | `домбра [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=домбра | 200 | 0 | title-relevant=0 |
| figshare | `домбыра [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=домбыра | 200 | 0 | title-relevant=0 |
| figshare | `домбыра [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=домбыра | 200 | 0 | title-relevant=0 |
| figshare | `домбыра [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=домбыра | 200 | 0 | title-relevant=0 |
| figshare | `kui [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=kui | 200 | 100 | title-relevant=4 |
| figshare | `kui [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=kui | 200 | 100 | title-relevant=7 |
| figshare | `kui [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=kui | 200 | 100 | title-relevant=0 |
| figshare | `kuy [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=kuy | 200 | 26 | title-relevant=4 |
| figshare | `kuy [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=kuy | 200 | 19 | title-relevant=7 |
| figshare | `kuy [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=kuy | 200 | 100 | title-relevant=51 |
| figshare | `күй [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=күй | 200 | 0 | title-relevant=0 |
| figshare | `күй [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=күй | 200 | 0 | title-relevant=0 |
| figshare | `күй [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=күй | 200 | 0 | title-relevant=0 |
| figshare | `кюй [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=кюй | 200 | 0 | title-relevant=0 |
| figshare | `кюй [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=кюй | 200 | 0 | title-relevant=0 |
| figshare | `кюй [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=кюй | 200 | 0 | title-relevant=0 |
| figshare | `қазақ әні [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=қазақ әні | 200 | 0 | title-relevant=0 |
| figshare | `қазақ әні [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=қазақ әні | 200 | 0 | title-relevant=0 |
| figshare | `қазақ әні [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=қазақ әні | 200 | 0 | title-relevant=0 |
| figshare | `казахская песня [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=казахская песня | 200 | 0 | title-relevant=0 |
| figshare | `казахская песня [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=казахская песня | 200 | 0 | title-relevant=0 |
| figshare | `казахская песня [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=казахская песня | 200 | 0 | title-relevant=0 |
| figshare | `казахская музыка [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=казахская музыка | 200 | 0 | title-relevant=0 |
| figshare | `казахская музыка [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=казахская музыка | 200 | 0 | title-relevant=0 |
| figshare | `казахская музыка [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=казахская музыка | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh folk song [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh folk song | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh folk song [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh folk song | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh folk song [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh folk song | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh singing [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh singing | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh singing [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh singing | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh singing [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh singing | 200 | 0 | title-relevant=0 |
| figshare | `terme [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=terme | 200 | 100 | title-relevant=0 |
| figshare | `terme [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=terme | 200 | 100 | title-relevant=0 |
| figshare | `terme [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=terme | 200 | 100 | title-relevant=0 |
| figshare | `zhyr [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=zhyr | 200 | 5 | title-relevant=0 |
| figshare | `zhyr [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=zhyr | 200 | 0 | title-relevant=0 |
| figshare | `zhyr [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=zhyr | 200 | 9 | title-relevant=0 |
| figshare | `жыр [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=жыр | 200 | 0 | title-relevant=0 |
| figshare | `жыр [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=жыр | 200 | 0 | title-relevant=0 |
| figshare | `жыр [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=жыр | 200 | 0 | title-relevant=0 |
| figshare | `терме [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=терме | 200 | 1 | title-relevant=1 |
| figshare | `терме [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=терме | 200 | 2 | title-relevant=1 |
| figshare | `терме [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=терме | 200 | 4 | title-relevant=3 |
| figshare | `Kazakh music dataset [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh music dataset | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh music dataset [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh music dataset | 200 | 0 | title-relevant=0 |
| figshare | `Kazakh music dataset [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=Kazakh music dataset | 200 | 0 | title-relevant=0 |
| figshare | `qazaq music [item_type=dataset]` | https://api.figshare.com/v2/articles/search?search_for=qazaq music | 200 | 0 | title-relevant=0 |
| figshare | `qazaq music [item_type=media]` | https://api.figshare.com/v2/articles/search?search_for=qazaq music | 200 | 0 | title-relevant=0 |
| figshare | `qazaq music [item_type=any]` | https://api.figshare.com/v2/articles/search?search_for=qazaq music | 200 | 0 | title-relevant=0 |
| figshare | `冬不拉` | https://api.figshare.com/v2/articles/search | 200 | 0 |  |
| figshare | `哈萨克 民歌` | https://api.figshare.com/v2/articles/search | 200 | 0 |  |
| figshare | `哈萨克族 音乐` | https://api.figshare.com/v2/articles/search | 200 | 0 |  |
| figshare | `哈萨克 演唱` | https://api.figshare.com/v2/articles/search | 200 | 0 |  |

#### Dataverse (128 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| dataverse:dataverse.harvard.edu | `dombra [type=file]` | https://dataverse.harvard.edu/api/search?q=dombra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `dombra [type=dataset]` | https://dataverse.harvard.edu/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `dombyra [type=file]` | https://dataverse.harvard.edu/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `dombyra [type=dataset]` | https://dataverse.harvard.edu/api/search?q=dombyra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `домбра [type=file]` | https://dataverse.harvard.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `домбра [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `домбыра [type=file]` | https://dataverse.harvard.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `домбыра [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page... | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `kui [type=file]` | https://dataverse.harvard.edu/api/search?q=kui&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `kui [type=dataset]` | https://dataverse.harvard.edu/api/search?q=kui&type=dataset&per_page=100 | 200 | 25 | relevant=0 |
| dataverse:dataverse.harvard.edu | `kuy [type=file]` | https://dataverse.harvard.edu/api/search?q=kuy&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `kuy [type=dataset]` | https://dataverse.harvard.edu/api/search?q=kuy&type=dataset&per_page=100 | 200 | 25 | relevant=0 |
| dataverse:dataverse.harvard.edu | `күй [type=file]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `күй [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D2%AF%D0%B9&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `кюй [type=file]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D1%8E%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `кюй [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D1%8E%D0%B9&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `қазақ әні [type=file]` | https://dataverse.harvard.edu/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B+%D3%99%D0%BD%D1%96&type=file&per_... | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `қазақ әні [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B+%D3%99%D0%BD%D1%96&type=dataset&p... | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `казахская песня [type=file]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F+%D0%BF%D0... | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `казахская песня [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F+%D0%BF%D0... | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `казахская музыка [type=file]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F+%D0%BC%D1... | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `казахская музыка [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F+%D0%BC%D1... | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `Kazakh folk song [type=file]` | https://dataverse.harvard.edu/api/search?q=Kazakh+folk+song&type=file&per_page=100 | 200 | 880 | relevant=1 |
| dataverse:dataverse.harvard.edu | `Kazakh folk song [type=dataset]` | https://dataverse.harvard.edu/api/search?q=Kazakh+folk+song&type=dataset&per_page=100 | 200 | 935 | relevant=0 |
| dataverse:dataverse.harvard.edu | `Kazakh singing [type=file]` | https://dataverse.harvard.edu/api/search?q=Kazakh+singing&type=file&per_page=100 | 200 | 225 | relevant=3 |
| dataverse:dataverse.harvard.edu | `Kazakh singing [type=dataset]` | https://dataverse.harvard.edu/api/search?q=Kazakh+singing&type=dataset&per_page=100 | 200 | 152 | relevant=11 |
| dataverse:dataverse.harvard.edu | `terme [type=file]` | https://dataverse.harvard.edu/api/search?q=terme&type=file&per_page=100 | 200 | 5556 | relevant=0 |
| dataverse:dataverse.harvard.edu | `terme [type=dataset]` | https://dataverse.harvard.edu/api/search?q=terme&type=dataset&per_page=100 | 200 | 12300 | relevant=2 |
| dataverse:dataverse.harvard.edu | `zhyr [type=file]` | https://dataverse.harvard.edu/api/search?q=zhyr&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `zhyr [type=dataset]` | https://dataverse.harvard.edu/api/search?q=zhyr&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `жыр [type=file]` | https://dataverse.harvard.edu/api/search?q=%D0%B6%D1%8B%D1%80&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `жыр [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D0%B6%D1%8B%D1%80&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `терме [type=file]` | https://dataverse.harvard.edu/api/search?q=%D1%82%D0%B5%D1%80%D0%BC%D0%B5&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `терме [type=dataset]` | https://dataverse.harvard.edu/api/search?q=%D1%82%D0%B5%D1%80%D0%BC%D0%B5&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.harvard.edu | `Kazakh music dataset [type=file]` | https://dataverse.harvard.edu/api/search?q=Kazakh+music+dataset&type=file&per_page=100 | 200 | 25847 | relevant=2 |
| dataverse:dataverse.harvard.edu | `Kazakh music dataset [type=dataset]` | https://dataverse.harvard.edu/api/search?q=Kazakh+music+dataset&type=dataset&per_page=100 | 200 | 303695 | relevant=0 |
| dataverse:dataverse.harvard.edu | `qazaq music [type=file]` | https://dataverse.harvard.edu/api/search?q=qazaq+music&type=file&per_page=100 | 200 | 1142 | relevant=0 |
| dataverse:dataverse.harvard.edu | `qazaq music [type=dataset]` | https://dataverse.harvard.edu/api/search?q=qazaq+music&type=dataset&per_page=100 | 200 | 884 | relevant=0 |
| dataverse:dataverse.nl | `dombra [type=file]` | https://dataverse.nl/api/search?q=dombra&type=file&per_page=100 | 200 | 1 | relevant=0 |
| dataverse:dataverse.nl | `dombra [type=dataset]` | https://dataverse.nl/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.nl | `dombyra [type=file]` | https://dataverse.nl/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.nl | `домбыра [type=file]` | https://dataverse.nl/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.nl | `домбыра [type=dataset]` | https://dataverse.nl/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.nl | `kazakh [type=file]` | https://dataverse.nl/api/search?q=kazakh&type=file&per_page=100 | 200 | 105 | relevant=0 |
| dataverse:dataverse.nl | `kazakh [type=dataset]` | https://dataverse.nl/api/search?q=kazakh&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.nl | `kui [type=file]` | https://dataverse.nl/api/search?q=kui&type=file&per_page=100 | 200 | 204 | relevant=0 |
| dataverse:dataverse.nl | `күй [type=file]` | https://dataverse.nl/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.nl | `қазақ [type=file]` | https://dataverse.nl/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `dombra [type=file]` | https://dataverse.no/api/search?q=dombra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `dombra [type=dataset]` | https://dataverse.no/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `dombyra [type=file]` | https://dataverse.no/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `домбыра [type=file]` | https://dataverse.no/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `домбыра [type=dataset]` | https://dataverse.no/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `kazakh [type=file]` | https://dataverse.no/api/search?q=kazakh&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `kazakh [type=dataset]` | https://dataverse.no/api/search?q=kazakh&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `kui [type=file]` | https://dataverse.no/api/search?q=kui&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `күй [type=file]` | https://dataverse.no/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.no | `қазақ [type=file]` | https://dataverse.no/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `dombra [type=file]` | https://data.goettingen-research-online.de/api/search?q=dombra&type=file&per_page=100 | 500 | — | relevant=0 |
| dataverse:data.goettingen-research-online.de | `dombra [type=dataset]` | https://data.goettingen-research-online.de/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `dombyra [type=file]` | https://data.goettingen-research-online.de/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `домбыра [type=file]` | https://data.goettingen-research-online.de/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=fil... | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `домбыра [type=dataset]` | https://data.goettingen-research-online.de/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dat... | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `kazakh [type=file]` | https://data.goettingen-research-online.de/api/search?q=kazakh&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `kazakh [type=dataset]` | https://data.goettingen-research-online.de/api/search?q=kazakh&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `kui [type=file]` | https://data.goettingen-research-online.de/api/search?q=kui&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `күй [type=file]` | https://data.goettingen-research-online.de/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.goettingen-research-online.de | `қазақ [type=file]` | https://data.goettingen-research-online.de/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.tdl.org | `dombra [type=file]` | https://dataverse.tdl.org/api/search?q=dombra&type=file&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `dombra [type=dataset]` | https://dataverse.tdl.org/api/search?q=dombra&type=dataset&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `dombyra [type=file]` | https://dataverse.tdl.org/api/search?q=dombyra&type=file&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `домбыра [type=file]` | https://dataverse.tdl.org/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `домбыра [type=dataset]` | https://dataverse.tdl.org/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `kazakh [type=file]` | https://dataverse.tdl.org/api/search?q=kazakh&type=file&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `kazakh [type=dataset]` | https://dataverse.tdl.org/api/search?q=kazakh&type=dataset&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `kui [type=file]` | https://dataverse.tdl.org/api/search?q=kui&type=file&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `күй [type=file]` | https://dataverse.tdl.org/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 403 | — | relevant=0 |
| dataverse:dataverse.tdl.org | `қазақ [type=file]` | https://dataverse.tdl.org/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 403 | — | relevant=0 |
| dataverse:demo.dataverse.org | `dombra [type=file]` | https://demo.dataverse.org/api/search?q=dombra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `dombra [type=dataset]` | https://demo.dataverse.org/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `dombyra [type=file]` | https://demo.dataverse.org/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `домбыра [type=file]` | https://demo.dataverse.org/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `домбыра [type=dataset]` | https://demo.dataverse.org/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `kazakh [type=file]` | https://demo.dataverse.org/api/search?q=kazakh&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `kazakh [type=dataset]` | https://demo.dataverse.org/api/search?q=kazakh&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `kui [type=file]` | https://demo.dataverse.org/api/search?q=kui&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `күй [type=file]` | https://demo.dataverse.org/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:demo.dataverse.org | `қазақ [type=file]` | https://demo.dataverse.org/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.unc.edu | `dombra [type=file]` | https://dataverse.unc.edu/api/search?q=dombra&type=file&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `dombra [type=dataset]` | https://dataverse.unc.edu/api/search?q=dombra&type=dataset&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `dombyra [type=file]` | https://dataverse.unc.edu/api/search?q=dombyra&type=file&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `домбыра [type=file]` | https://dataverse.unc.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `домбыра [type=dataset]` | https://dataverse.unc.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `kazakh [type=file]` | https://dataverse.unc.edu/api/search?q=kazakh&type=file&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `kazakh [type=dataset]` | https://dataverse.unc.edu/api/search?q=kazakh&type=dataset&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `kui [type=file]` | https://dataverse.unc.edu/api/search?q=kui&type=file&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `күй [type=file]` | https://dataverse.unc.edu/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 401 | — | relevant=0 |
| dataverse:dataverse.unc.edu | `қазақ [type=file]` | https://dataverse.unc.edu/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 401 | — | relevant=0 |
| dataverse:data.aussda.at | `dombra [type=file]` | https://data.aussda.at/api/search?q=dombra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.aussda.at | `dombra [type=dataset]` | https://data.aussda.at/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.aussda.at | `dombyra [type=file]` | https://data.aussda.at/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.aussda.at | `домбыра [type=file]` | https://data.aussda.at/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.aussda.at | `домбыра [type=dataset]` | https://data.aussda.at/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.aussda.at | `kazakh [type=file]` | https://data.aussda.at/api/search?q=kazakh&type=file&per_page=100 | 200 | 5 | relevant=0 |
| dataverse:data.aussda.at | `kazakh [type=dataset]` | https://data.aussda.at/api/search?q=kazakh&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.aussda.at | `kui [type=file]` | https://data.aussda.at/api/search?q=kui&type=file&per_page=100 | 200 | 1 | relevant=0 |
| dataverse:data.aussda.at | `күй [type=file]` | https://data.aussda.at/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:data.aussda.at | `қазақ [type=file]` | https://data.aussda.at/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `dombra [type=file]` | https://edmond.mpg.de/api/search?q=dombra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `dombra [type=dataset]` | https://edmond.mpg.de/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `dombyra [type=file]` | https://edmond.mpg.de/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `домбыра [type=file]` | https://edmond.mpg.de/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `домбыра [type=dataset]` | https://edmond.mpg.de/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `kazakh [type=file]` | https://edmond.mpg.de/api/search?q=kazakh&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `kazakh [type=dataset]` | https://edmond.mpg.de/api/search?q=kazakh&type=dataset&per_page=100 | 200 | 1 | relevant=0 |
| dataverse:edmond.mpg.de | `kui [type=file]` | https://edmond.mpg.de/api/search?q=kui&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `күй [type=file]` | https://edmond.mpg.de/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:edmond.mpg.de | `қазақ [type=file]` | https://edmond.mpg.de/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `dombra [type=file]` | https://dataverse.lib.virginia.edu/api/search?q=dombra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `dombra [type=dataset]` | https://dataverse.lib.virginia.edu/api/search?q=dombra&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `dombyra [type=file]` | https://dataverse.lib.virginia.edu/api/search?q=dombyra&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `домбыра [type=file]` | https://dataverse.lib.virginia.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=file&per_pa... | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `домбыра [type=dataset]` | https://dataverse.lib.virginia.edu/api/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&type=dataset&per... | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `kazakh [type=file]` | https://dataverse.lib.virginia.edu/api/search?q=kazakh&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `kazakh [type=dataset]` | https://dataverse.lib.virginia.edu/api/search?q=kazakh&type=dataset&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `kui [type=file]` | https://dataverse.lib.virginia.edu/api/search?q=kui&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `күй [type=file]` | https://dataverse.lib.virginia.edu/api/search?q=%D0%BA%D2%AF%D0%B9&type=file&per_page=100 | 200 | 0 | relevant=0 |
| dataverse:dataverse.lib.virginia.edu | `қазақ [type=file]` | https://dataverse.lib.virginia.edu/api/search?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&type=file&per_page=100 | 200 | 0 | relevant=0 |

#### GitHub (39 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| github | `repos: dombra` | https://api.github.com/search/repositories?q=dombra | 200 | 47 | new=47 |
| github | `repos: dombyra` | https://api.github.com/search/repositories?q=dombyra | 200 | 40 | new=40 |
| github | `repos: домбыра` | https://api.github.com/search/repositories?q=домбыра | 200 | 2 | new=2 |
| github | `repos: домбра` | https://api.github.com/search/repositories?q=домбра | 200 | 0 | new=0 |
| github | `repos: kui kazakh` | https://api.github.com/search/repositories?q=kui kazakh | 200 | 0 | new=0 |
| github | `repos: kuy kazakh` | https://api.github.com/search/repositories?q=kuy kazakh | 200 | 0 | new=0 |
| github | `repos: күй` | https://api.github.com/search/repositories?q=күй | 200 | 0 | new=0 |
| github | `repos: кюй` | https://api.github.com/search/repositories?q=кюй | 200 | 0 | new=0 |
| github | `repos: kazakh music` | https://api.github.com/search/repositories?q=kazakh music | 200 | 8 | new=8 |
| github | `repos: kazakh song` | https://api.github.com/search/repositories?q=kazakh song | 200 | 1 | new=1 |
| github | `repos: kazakh folk` | https://api.github.com/search/repositories?q=kazakh folk | 200 | 2 | new=2 |
| github | `repos: qazaq music` | https://api.github.com/search/repositories?q=qazaq music | 200 | 1 | new=1 |
| github | `repos: kazakh singing` | https://api.github.com/search/repositories?q=kazakh singing | 200 | 0 | new=0 |
| github | `repos: kazakh audio dataset` | https://api.github.com/search/repositories?q=kazakh audio dataset | 200 | 4 | new=4 |
| github | `repos: zhyr` | https://api.github.com/search/repositories?q=zhyr | 200 | 139 | new=50 |
| github | `repos: terme kazakh` | https://api.github.com/search/repositories?q=terme kazakh | 200 | 0 | new=0 |
| github | `repos: қазақ әні` | https://api.github.com/search/repositories?q=қазақ әні | 200 | 0 | new=0 |
| github | `repos: казахская музыка` | https://api.github.com/search/repositories?q=казахская музыка | 200 | 0 | new=0 |
| github | `repos: kobyz` | https://api.github.com/search/repositories?q=kobyz | 200 | 9 | new=9 |
| github | `repos: қобыз` | https://api.github.com/search/repositories?q=қобыз | 200 | 1 | new=1 |
| github | `repos: 冬不拉` | https://api.github.com/search/repositories?q=冬不拉 | 200 | 3 | new=3 |
| github | `repos: dombra dataset` | https://api.github.com/search/repositories?q=dombra dataset | 200 | 0 | new=0 |
| github | `repos: dombra transcription` | https://api.github.com/search/repositories?q=dombra transcription | 200 | 0 | new=0 |
| github | `repos: 哈萨克 民歌` | https://api.github.com/search/repositories?q=哈萨克 民歌 | 200 | 0 | new=0 |
| github | `repos: kui generation` | https://api.github.com/search/repositories?q=kui generation | 200 | 7 | new=7 |
| github | `repos: kazakh lyrics` | https://api.github.com/search/repositories?q=kazakh lyrics | 200 | 1 | new=1 |
| github | `repos: 哈萨克族 音乐` | https://api.github.com/search/repositories?q=哈萨克族 音乐 | 200 | 0 | new=0 |
| github | `code: dombra extension:wav` | https://api.github.com/search/code?q=dombra extension:wav | 200 | 0 | items=0 |
| github | `repos: 哈萨克 演唱` | https://api.github.com/search/repositories?q=哈萨克 演唱 | 200 | 0 | new=0 |
| github | `code: dombra extension:mp3` | https://api.github.com/search/code?q=dombra extension:mp3 | 200 | 0 | items=0 |
| github | `code: dombyra extension:wav` | https://api.github.com/search/code?q=dombyra extension:wav | 200 | 0 | items=0 |
| github | `code: dombyra extension:mp3` | https://api.github.com/search/code?q=dombyra extension:mp3 | 200 | 0 | items=0 |
| github | `code: kui kazakh extension:wav` | https://api.github.com/search/code?q=kui kazakh extension:wav | 200 | 0 | items=0 |
| github | `code: домбыра extension:mp3` | https://api.github.com/search/code?q=домбыра extension:mp3 | 200 | 0 | items=0 |
| github | `code: күй extension:mp3` | https://api.github.com/search/code?q=күй extension:mp3 | 200 | 0 | items=0 |
| github | `code: kazakh extension:mp3 song` | https://api.github.com/search/code?q=kazakh extension:mp3 song | 200 | 0 | items=0 |
| github | `code: dombra filename:metadata.csv` | https://api.github.com/search/code?q=dombra filename:metadata.csv | 200 | 3 | items=3 |
| github | `code: dombyra filename:README.md dataset` | https://api.github.com/search/code?q=dombyra filename:README.md dataset | 200 | 0 | items=0 |
| github | `code: kazakh song lyrics extension:json audio` | https://api.github.com/search/code?q=kazakh song lyrics extension:json audio | 200 | 1100 | items=50 |

#### Dryad (7 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| dryad | `dombra` | https://datadryad.org/api/v2/search?q=dombra&per_page=100 | 200 | 0 |  |
| dryad | `dombyra` | https://datadryad.org/api/v2/search?q=dombyra&per_page=100 | 200 | 0 |  |
| dryad | `kazakh music` | https://datadryad.org/api/v2/search?q=kazakh+music&per_page=100 | 200 | 0 |  |
| dryad | `kazakh song` | https://datadryad.org/api/v2/search?q=kazakh+song&per_page=100 | 200 | 0 |  |
| dryad | `kazakh singing` | https://datadryad.org/api/v2/search?q=kazakh+singing&per_page=100 | 200 | 0 |  |
| dryad | `домбыра` | https://datadryad.org/api/v2/search?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&per_page=100 | 200 | 0 |  |
| dryad | `күй` | https://datadryad.org/api/v2/search?q=%D0%BA%D2%AF%D0%B9&per_page=100 | 200 | 0 |  |

#### ScienceDB (7 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| scidb | `dombra` | https://www.scidb.cn/api/sdb-query-service/public/search?keyword=dombra&pageSize=50&pageNum=1 | 404 | — | {'timestamp': 1789359407598, 'status': 404, 'error': 'Not Found', 'message': '', 'path': '/public/search'} |
| scidb | `kazakh music` | https://www.scidb.cn/api/sdb-query-service/public/search?keyword=kazakh+music&pageSize=50&pageNum=1 | 404 | — | {'timestamp': 1789359408080, 'status': 404, 'error': 'Not Found', 'message': '', 'path': '/public/search'} |
| scidb | `kazakh song` | https://www.scidb.cn/api/sdb-query-service/public/search?keyword=kazakh+song&pageSize=50&pageNum=1 | 404 | — | {'timestamp': 1789359408558, 'status': 404, 'error': 'Not Found', 'message': '', 'path': '/public/search'} |
| scidb | `冬不拉` | https://www.scidb.cn/api/sdb-query-service/public/search?keyword=%E5%86%AC%E4%B8%8D%E6%8B%89&pageSize=50&pa... | 404 | — | {'timestamp': 1789359408967, 'status': 404, 'error': 'Not Found', 'message': '', 'path': '/public/search'} |
| scidb | `哈萨克 民歌` | https://www.scidb.cn/api/sdb-query-service/public/search?keyword=%E5%93%88%E8%90%A8%E5%85%8B+%E6%B0%91%E6%A... | 404 | — | {'timestamp': 1789359409386, 'status': 404, 'error': 'Not Found', 'message': '', 'path': '/public/search'} |
| scidb | `哈萨克族 音乐` | https://www.scidb.cn/api/sdb-query-service/public/search?keyword=%E5%93%88%E8%90%A8%E5%85%8B%E6%97%8F+%E9%9... | 404 | — | {'timestamp': 1789359409798, 'status': 404, 'error': 'Not Found', 'message': '', 'path': '/public/search'} |
| scidb | `哈萨克 演唱` | https://www.scidb.cn/api/sdb-query-service/public/search?keyword=%E5%93%88%E8%90%A8%E5%85%8B+%E6%BC%94%E5%9... | 404 | — | {'timestamp': 1789359410213, 'status': 404, 'error': 'Not Found', 'message': '', 'path': '/public/search'} |

#### IEEE DataPort (3 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| ieee-dataport | `kazakh` | https://ieee-dataport.org/search?q=kazakh | 200 | 2 |  |
| ieee-dataport | `dombra` | https://ieee-dataport.org/search?q=dombra | 200 | 2 |  |
| ieee-dataport | `kazakh music` | https://ieee-dataport.org/search?q=kazakh+music | 200 | 2 |  |

#### Common Voice (4 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| commonvoice | `cv-dataset/datasets listing` | https://api.github.com/repos/common-voice/cv-dataset/contents/datasets | 200 | 3 | code-switching, scripted-speech, spontaneous-speech |
| commonvoice | `https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0/raw/main/README.md` | https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0/raw/main/README.md | 200 | — | --- task_categories: - automatic-speech-recognition ---  Effective October 2025, Mozilla Common Voice datasets are now e |
| commonvoice | `https://commonvoice.mozilla.org/api/v1/languages/kk/stats` | https://commonvoice.mozilla.org/api/v1/languages/kk/stats | 401 | — |  |
| commonvoice | `https://datacollective.mozillafoundation.org/` | https://mozilladatacollective.com/ | 200 | — | <!DOCTYPE html><html lang="en-US" dir="ltr"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-wid |

#### kazneb.kz (9 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| kazneb | `https://kazneb.kz/ru` | https://kazneb.kz/ru | 200 | — | len=20000 links=[] mentions=[] |
| kazneb | `https://kazneb.kz/ru/agreement` | https://kazneb.kz/ru/agreement | 404 | — | len=20000 links=[] mentions=[] |
| kazneb | `https://kazneb.kz/ru/rules` | https://kazneb.kz/ru/rules | 404 | — | len=20000 links=[] mentions=[] |
| kazneb | `https://kazneb.kz/ru/page/agreement` | https://kazneb.kz/ru/page/agreement | 404 | — | len=20000 links=[] mentions=[] |
| kazneb | `https://kazneb.kz/ru/catalogue/result?dType=15&query=%D0%BA%D2%AF%D0%B9` | https://kazneb.kz/ru/catalogue/result?dType=15&query=%D0%BA%D2%AF%D0%B9 | 200 | — | len=20000 links=[] mentions=[] |
| kazneb | `https://kazneb.kz/ru/catalogue/view/1510479` | https://kazneb.kz/ru/catalogue/view/1510479 | 200 | — | len=20000 links=[] mentions=[] |
| kazneb | `https://kazneb.kz/ru/catalogue/result?dType=15` | https://kazneb.kz/ru/catalogue/result?dType=15 | 200 | — |  <!DOCTYPE html> <html lang="ru" dir="ltr" class="h-100">   <head>     <meta charset="utf-8" /> <script async src="https |
| kazneb | `https://kazneb.kz/ru/agreement` | https://kazneb.kz/ru/agreement | 404 | — |  <!DOCTYPE html> <html lang="ru" dir="ltr" class="h-100">   <head>     <meta charset="utf-8" /> <noscript><meta http-equ |
| kazneb | `https://kazneb.kz/ru/about` | https://kazneb.kz/ru/about | 200 | — |  <!DOCTYPE html> <html lang="ru" dir="ltr" class="h-100">   <head>     <meta charset="utf-8" /> <noscript><meta http-equ |

#### nlrk.kz (5 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| nlrk | `https://nlrk.kz/ru` | https://nlrk.kz/ru | 200 | — | len=845 links=[] mentions=[] |
| nlrk | `https://nlrk.kz/` | https://nlrk.kz/ | 200 | — | len=845 links=[] mentions=[] |
| nlrk | `https://nlrk.kz/ru/electronic-resources` | https://nlrk.kz/ru/electronic-resources | 200 | — | len=845 links=[] mentions=[] |
| nlrk | `https://nlrk.kz/ru` | https://nlrk.kz/ru | 200 | — | <!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-sc |
| nlrk | `https://nlrk.kz/api/` | https://nlrk.kz/api/ | 404 | — |  |

#### UNESCO ICH (2 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| unesco | `https://ich.unesco.org/en/RL/kazakh-traditional-art-of-dombra-kuy-00996` | https://ich.unesco.org/en/RL/kazakh-traditional-art-of-dombra-kuy-00996 | 200 | — | len=20000 links=[] mentions=[] |
| unesco | `https://ich.unesco.org/en/terms-of-use-00223` | https://ich.unesco.org/en/terms-of-use-00223 | 200 | — | len=20000 links=[] mentions=[] |

#### arXiv (9 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| arxiv | `all:dombra` | https://export.arxiv.org/api/query?search_query=all%3Adombra&max_results=50 | 429 | — | parsed=0 |
| arxiv | `all:dombyra` | https://export.arxiv.org/api/query?search_query=all%3Adombyra&max_results=50 | 429 | — | parsed=0 |
| arxiv | `all:kazakh AND all:music` | https://export.arxiv.org/api/query?search_query=all%3Akazakh+AND+all%3Amusic&max_results=50 | 503 | — | parsed=0 |
| arxiv | `all:kazakh AND all:singing` | https://export.arxiv.org/api/query?search_query=all%3Akazakh+AND+all%3Asinging&max_results=50 | 429 | — | parsed=0 |
| arxiv | `all:kazakh AND all:song` | https://export.arxiv.org/api/query?search_query=all%3Akazakh+AND+all%3Asong&max_results=50 | 429 | — | parsed=0 |
| arxiv | `all:kui AND all:kazakh` | https://export.arxiv.org/api/query | ERR:ReadTimeout | — | parsed=0 |
| arxiv | `all:kazakh AND all:audio AND all:dataset` | https://export.arxiv.org/api/query?search_query=all%3Akazakh+AND+all%3Aaudio+AND+all%3Adataset&max_results=50 | 503 | — | parsed=0 |
| arxiv | `abs:"Kazakh" AND abs:"speech corpus"` | https://export.arxiv.org/api/query | ERR:ReadTimeout | — | parsed=0 |
| arxiv | `all:qazaq AND all:music` | https://export.arxiv.org/api/query?search_query=all%3Aqazaq+AND+all%3Amusic&max_results=50 | 503 | — | parsed=0 |

#### Zenodo (25 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| zenodo | `dombra` | https://zenodo.org/api/records?q=dombra&size=25&page=1 | 200 | 8 | relevant_with_media_or_dataset=0 |
| zenodo | `dombyra` | https://zenodo.org/api/records?q=dombyra&size=25&page=1 | 200 | 0 | relevant_with_media_or_dataset=0 |
| zenodo | `домбра` | https://zenodo.org/api/records?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&size=25&page=1 | 200 | 0 | relevant_with_media_or_dataset=0 |
| zenodo | `домбыра` | https://zenodo.org/api/records?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&size=25&page=1 | 200 | 1 | relevant_with_media_or_dataset=0 |
| zenodo | `kui` | https://zenodo.org/api/records?q=kui&size=25&page=4 | 200 | 908 | relevant_with_media_or_dataset=7 |
| zenodo | `kuy` | https://zenodo.org/api/records?q=kuy&size=25&page=4 | 200 | 145 | relevant_with_media_or_dataset=6 |
| zenodo | `күй` | https://zenodo.org/api/records?q=%D0%BA%D2%AF%D0%B9&size=25&page=1 | 200 | 23 | relevant_with_media_or_dataset=0 |
| zenodo | `кюй` | https://zenodo.org/api/records?q=%D0%BA%D1%8E%D0%B9&size=25&page=1 | 200 | 1 | relevant_with_media_or_dataset=0 |
| zenodo | `қазақ әні` | https://zenodo.org/api/records?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B+%D3%99%D0%BD%D1%96&size=25&page=4 | 200 | 352 | relevant_with_media_or_dataset=0 |
| zenodo | `казахская песня` | https://zenodo.org/api/records?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F+%D0%BF%D0%B5%D1%81%... | 200 | 74 | relevant_with_media_or_dataset=0 |
| zenodo | `казахская музыка` | https://zenodo.org/api/records?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F+%D0%BC%D1%83%D0%B7%... | 200 | 335 | relevant_with_media_or_dataset=0 |
| zenodo | `Kazakh folk song` | https://zenodo.org/api/records?q=Kazakh+folk+song&size=25&page=4 | 200 | 49521 | relevant_with_media_or_dataset=0 |
| zenodo | `Kazakh singing` | https://zenodo.org/api/records?q=Kazakh+singing&size=25&page=4 | 200 | 4822 | relevant_with_media_or_dataset=5 |
| zenodo | `terme` | https://zenodo.org/api/records?q=terme&size=25&page=4 | 200 | 2772 | relevant_with_media_or_dataset=24 |
| zenodo | `zhyr` | https://zenodo.org/api/records?q=zhyr&size=25&page=1 | 200 | 3 | relevant_with_media_or_dataset=0 |
| zenodo | `жыр` | https://zenodo.org/api/records?q=%D0%B6%D1%8B%D1%80&size=25&page=1 | 200 | 18 | relevant_with_media_or_dataset=0 |
| zenodo | `терме` | https://zenodo.org/api/records?q=%D1%82%D0%B5%D1%80%D0%BC%D0%B5&size=25&page=1 | 200 | 3 | relevant_with_media_or_dataset=0 |
| zenodo | `Kazakh music dataset` | https://zenodo.org/api/records?q=Kazakh+music+dataset&size=25&page=4 | 200 | 306632 | relevant_with_media_or_dataset=5 |
| zenodo | `qazaq music` | https://zenodo.org/api/records?q=qazaq+music&size=25&page=4 | 200 | 28174 | relevant_with_media_or_dataset=0 |
| zenodo | `kazakh {"type": "dataset"}` | https://zenodo.org/api/records?q=kazakh&size=25&page=4&type=dataset | 200 | 138 | relevant_with_media_or_dataset=68 |
| zenodo | `kazakh {"type": "video"}` | https://zenodo.org/api/records?q=kazakh&size=25&page=1&type=video | 200 | 1 | relevant_with_media_or_dataset=0 |
| zenodo | `kazakh {"type": "other"}` | https://zenodo.org/api/records?q=kazakh&size=25&page=1&type=other | 200 | 3 | relevant_with_media_or_dataset=2 |
| zenodo | `kazakh AND (audio OR music OR song OR dombra OR singing)` | https://zenodo.org/api/records?q=kazakh+AND+%28audio+OR+music+OR+song+OR+dombra+OR+singing%29&size=25&page=4 | 200 | 83 | relevant_with_media_or_dataset=2 |
| zenodo | `казах AND (музыка OR песня OR домбра)` | https://zenodo.org/api/records?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85+AND+%28%D0%BC%D1%83%D0%B7%D1%8B%D0%BA%D0%B0... | 200 | 13 | relevant_with_media_or_dataset=0 |
| zenodo | `kazakh AND audio {"type": "dataset"}` | https://zenodo.org/api/records?q=kazakh+AND+audio&size=25&page=1&type=dataset | 200 | 1 | relevant_with_media_or_dataset=1 |

#### Papers with Code (1 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| paperswithcode | `https://paperswithcode.com/search?q=kazakh` | https://huggingface.co/papers/trending | 200 | — | <!doctype html> <html class=""> 	<head> 		<meta charset="utf-8" />  		<meta name="viewport" content="width=device-width, |

#### ISSAI (5 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| issai | `https://raw.githubusercontent.com/IS2AI/Kazakh_TTS/main/README.md` | https://raw.githubusercontent.com/IS2AI/Kazakh_TTS/main/README.md | 200 | — | <!-- #region --> # KazakhTTS RECIPE  This is the recipe of Kazakh text-to-speech model based on KazakhTTS and KazakhTTS2 |
| issai | `https://raw.githubusercontent.com/IS2AI/Kazakh_Speech_Corpus_2/main/README.md` | https://raw.githubusercontent.com/IS2AI/Kazakh_Speech_Corpus_2/main/README.md | 404 | — | 404: Not Found |
| issai | `https://raw.githubusercontent.com/IS2AI/KazakhTTS2/main/README.md` | https://raw.githubusercontent.com/IS2AI/KazakhTTS2/main/README.md | 404 | — | 404: Not Found |
| issai | `https://issai.nu.edu.kz/kz-speech-corpus/` | https://issai.nu.edu.kz/kz-speech-corpus/ | 200 | — |  <!DOCTYPE html> <html lang="en">  <head> 	<meta charset="UTF-8"> 	<meta name="viewport" content="width=device-width, in |
| issai | `https://issai.nu.edu.kz/kazakh-tts/` | https://issai.nu.edu.kz | 200 | — |  <!DOCTYPE html> <html lang="en">  <head> 	<meta charset="UTF-8"> 	<meta name="viewport" content="width=device-width, in |

#### OSF (12 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| osf | `dombra [nodes]` | https://api.osf.io/v2/nodes/?filter%5Btitle%5D=dombra&page%5Bsize%5D=100 | 502 | — |  |
| osf | `dombra [registrations]` | https://api.osf.io/v2/registrations/?filter%5Btitle%5D=dombra&page%5Bsize%5D=100 | 200 | 0 |  |
| osf | `dombyra [nodes]` | https://api.osf.io/v2/nodes/?filter%5Btitle%5D=dombyra&page%5Bsize%5D=100 | 200 | 0 |  |
| osf | `dombyra [registrations]` | https://api.osf.io/v2/registrations/?filter%5Btitle%5D=dombyra&page%5Bsize%5D=100 | 200 | 0 |  |
| osf | `kazakh [nodes]` | https://api.osf.io/v2/nodes/ | ERR:ReadTimeout | — |  |
| osf | `kazakh [registrations]` | https://api.osf.io/v2/registrations/ | ERR:ReadTimeout | — |  |
| osf | `домбыра [nodes]` | https://api.osf.io/v2/nodes/ | ERR:ReadTimeout | — |  |
| osf | `домбыра [registrations]` | https://api.osf.io/v2/registrations/ | ERR:ReadTimeout | — |  |
| osf | `күй [nodes]` | https://api.osf.io/v2/nodes/?filter%5Btitle%5D=%D0%BA%D2%AF%D0%B9&page%5Bsize%5D=100 | 502 | — |  |
| osf | `күй [registrations]` | https://api.osf.io/v2/registrations/ | ERR:ReadTimeout | — |  |
| osf | `kui [nodes]` | https://api.osf.io/v2/nodes/ | ERR:ConnectionError | — |  |
| osf | `kui [registrations]` | https://api.osf.io/v2/registrations/ | ERR:ConnectionError | — |  |

#### Internet Archive (1 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| archive.org | `(dombra OR dombyra OR домбыра OR домбра OR күй OR кюй OR "kazakh folk" OR "kazakh song" OR "казахская" OR "қазақ") AND mediatype:(audio OR movies)` | https://archive.org/advancedsearch.php | ERR:ConnectionError | — | single allowed retry |

#### Openverse (16 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| openverse | `dombra` | https://api.openverse.org/v1/audio/?q=dombra&page_size=20&page=1 | 200 | 1 | page1=1 |
| openverse | `dombyra` | https://api.openverse.org/v1/audio/?q=dombyra&page_size=20&page=1 | 200 | 6 | page1=6 |
| openverse | `домбыра` | https://api.openverse.org/v1/audio/?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%8B%D1%80%D0%B0&page_size=20&page=1 | 200 | 0 | page1=0 |
| openverse | `домбра` | https://api.openverse.org/v1/audio/?q=%D0%B4%D0%BE%D0%BC%D0%B1%D1%80%D0%B0&page_size=20&page=1 | 200 | 1 | page1=1 |
| openverse | `күй` | https://api.openverse.org/v1/audio/?q=%D0%BA%D2%AF%D0%B9&page_size=20&page=1 | 200 | 0 | page1=0 |
| openverse | `кюй` | https://api.openverse.org/v1/audio/?q=%D0%BA%D1%8E%D0%B9&page_size=20&page=1 | 200 | 0 | page1=0 |
| openverse | `kui` | https://api.openverse.org/v1/audio/?q=kui&page_size=20&page=1 | 200 | 12 | page1=12 |
| openverse | `kuy` | https://api.openverse.org/v1/audio/?q=kuy&page_size=20&page=1 | 200 | 12 | page1=12 |
| openverse | `kazakh` | https://api.openverse.org/v1/audio/?q=kazakh&page_size=20&page=1 | 200 | 51 | page1=20 |
| openverse | `қазақ` | https://api.openverse.org/v1/audio/?q=%D2%9B%D0%B0%D0%B7%D0%B0%D2%9B&page_size=20&page=1 | 200 | 1 | page1=1 |
| openverse | `казахская песня` | https://api.openverse.org/v1/audio/?q=%D0%BA%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B0%D1%8F+%D0%BF%D0%B5%D... | 200 | 0 | page1=0 |
| openverse | `kazakh song` | https://api.openverse.org/v1/audio/?q=kazakh+song&page_size=20&page=1 | 200 | 0 | page1=0 |
| openverse | `kazakh folk` | https://api.openverse.org/v1/audio/?q=kazakh+folk&page_size=20&page=1 | 200 | 0 | page1=0 |
| openverse | `kobyz` | https://api.openverse.org/v1/audio/?q=kobyz&page_size=20&page=1 | 200 | 0 | page1=0 |
| openverse | `zhyr` | https://api.openverse.org/v1/audio/?q=zhyr&page_size=20&page=1 | 200 | 0 | page1=0 |
| openverse | `terme kazakh` | https://api.openverse.org/v1/audio/?q=terme+kazakh&page_size=20&page=1 | 200 | 0 | page1=0 |

#### commons (24 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| commons | `filetype:audio kazakh` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio kazakh | 200 | 216 | File:Kazakh word Seng.ogg; File:Kazakh word "men".ogg; File:Kazakh word sen.ogg; File:Kazakh word Ol.ogg; File:Anthem of the Kazakh Sovie... |
| commons | `filetype:video kazakh` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video kazakh | 200 | 49 | File:A Kazakh in China devoted his life to accordion.webm; File:Moon and stars.webm; File:Kazakh Girl.webm; File:Награждение волонтеров Н... |
| commons | `filetype:audio dombra` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio dombra | 200 | 2 | File:Домбра.ogg |
| commons | `filetype:video dombra` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video dombra | 200 | 7 | File:Moon and stars.webm; File:Boz salkin - dombra боз салкин.webm; File:Master of Dombra.webm; File:Жамбылдың домбырасы.webm; File:Singi... |
| commons | `filetype:audio dombyra` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio dombyra | 200 | 1 | File:Домбра.ogg |
| commons | `filetype:video dombyra` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video dombyra | 200 | 5 | File:Moon and stars.webm; File:Жамбылдың домбырасы.webm; File:Boz salkin - dombra боз салкин.webm; File:Master of Dombra.webm; File:Singi... |
| commons | `filetype:audio домбыра` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio домбыра | 200 | 2 | File:Домбра.ogg |
| commons | `filetype:video домбыра` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video домбыра | 200 | 7 | File:Moon and stars.webm; File:Boz salkin - dombra боз салкин.webm; File:Master of Dombra.webm; File:Жамбылдың домбырасы.webm; File:Singi... |
| commons | `imageinfo for 6 new candidate files (batched)` | https://commons.wikimedia.org/w/api.php?prop=imageinfo|revisions&titles=... | 200 | 6 | Жамбылдың домбырасы; Kazakh Girl; Traditional wedding; accordion; Anthem 1991-2006; Coffin Dance on Komus |
| commons | `logevents File:Kazakhstan anthem a cappella.ogg` | https://commons.wikimedia.org/w/api.php?list=logevents | 200 | 2 | Openverse still indexes this file; Commons page is missing |
| commons | `filetype:audio күй` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio күй | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video күй` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video күй | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:audio қазақ` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio қазақ | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video қазақ` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video қазақ | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:audio казахская` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio казахская | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video казахская` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video казахская | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:audio kobyz` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio kobyz | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video kazakhstan music` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video kazakhstan music | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:audio kazakh song` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio kazakh song | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video Kazakhstan folk` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video Kazakhstan folk | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video zhambyl` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video zhambyl | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video жамбыл` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video жамбыл | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:audio kazakh anthem` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:audio kazakh anthem | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |
| commons | `filetype:video kazakh singing` | https://commons.wikimedia.org/w/api.php?list=search&srsearch=filetype:video kazakh singing | NOT RUN | — | script aborted by network drop (RemoteDisconnected) before this query; not rerun per coordinator instruction |

#### WebFetch (23 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| webfetch | `archive.org advancedsearch: (dombra OR dombyra OR домбыра OR домбра OR күй OR кюй) AND mediatype:(audio OR movies)` | https://archive.org/advancedsearch.php?q=(dombra+OR+dombyra+OR+...)&output=json | ECONNRESET | — | alternate network path (WebFetch) also reset; archive.org unreachable both ways |
| webfetch | `archive.org advancedsearch: ("kazakh folk" OR "kazakh song" OR "kazakh music" OR казахская OR қазақ OR qazaq) AND mediatype:(audio OR movies)` | https://archive.org/advancedsearch.php?q=...&output=json | ECONNRESET | — |  |
| webfetch | `archive.org advancedsearch: dombra AND mediatype:audio` | https://archive.org/advancedsearch.php?q=dombra+AND+mediatype%3Aaudio&output=json | ECONNRESET | — | simplified retry |
| webfetch | `archive.org advancedsearch: kazakh AND mediatype:audio` | https://archive.org/advancedsearch.php?q=kazakh+AND+mediatype%3Aaudio&output=json | ECONNRESET | — |  |
| webfetch | `archive.org details: musicrepublic-world-traditional-music-from-lps-and-cassettes-full-archive` | https://archive.org/details/musicrepublic-world-traditional-music-from-lps-and-cassettes-full-archive | ECONNRESET | — | item surfaced by web search (LP rips incl. 'Voyage en URSS n°7 Kazakhstan' with M. Khamzin, dombra); licence field could not be read |
| webfetch | `archive.org metadata API: musicrepublic-world-traditional-music-from-lps-and-cassettes-full-archive` | https://archive.org/metadata/musicrepublic-world-traditional-music-from-lps-and-cassettes-full-archive | ECONNRESET | — |  |
| webfetch | `api.osf.io nodes filter[title]=kazakh` | https://api.osf.io/v2/nodes/?filter[title]=kazakh&page[size]=100 | TIMEOUT 60s | — | alternate network path also times out |
| webfetch | `api.osf.io nodes filter[title]=dombra` | https://api.osf.io/v2/nodes/?filter[title]=dombra&page[size]=100 | TIMEOUT 60s | — |  |
| webfetch | `osf.io/search?q=kazakh music` | https://osf.io/search?q=kazakh%20music&resourceType=Project,Registration,Preprint | 200 | — | JS shell, no results rendered |
| webfetch | `Mozilla Data Collective: Common Voice Scripted Speech 24.0 - Kazakh` | https://mozilladatacollective.com/datasets/cmj8u3pbb00dhnxxbsqe4vbpc | 301 then 200 | — | JS shell ('Loading datasets...'); numbers taken from cv-dataset GitHub JSON instead |
| webfetch | `OpenSLR 140 Kazakh Speech Dataset (KSD)` | https://www.openslr.org/140/ | 200 | — | 554 h, 204,250 utterances, 'Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0 US)'; read speech |
| webfetch | `OpenSLR 102 Kazakh Speech Corpus (KSC)` | https://www.openslr.org/102/ | 200 | — | ~332 h, >153,000 utterances, 'Attribution 4.0 International (CC BY 4.0)'; read speech |
| webfetch | `ISSAI datasets page` | https://issai.nu.edu.kz/issai-datasets/ | 200 | 14 | 14 datasets listed; KSC2 ~1,200 h CC BY 4.0, KazakhTTS2 271 h CC BY 4.0; no singing/music dataset |
| webfetch | `kazneb.kz/ru/agreement` | https://kazneb.kz/ru/agreement | 403 (WebFetch) / 404 (local curl) | — | no terms page found; /ru/rules and /ru/page/agreement 404 |
| webfetch | `kaggle.com/datasets?search=dombra` | https://www.kaggle.com/datasets?search=dombra | 200 | — | JS shell; no listing rendered; Kaggle API needs credentials |
| webfetch | `ACL Anthology 2026.lrec-1.431 (Using Songs to Improve Kazakh ASR)` | https://aclanthology.org/2026.lrec-1.431/ | 200 | — | confirms 3,013 pairs / 4.5 h / 195 songs / 36 artists; 'released on Hugging Face for research purposes under a gated, non-commercial lice... |
| webfetch | `export.arxiv.org all:dombra OR all:dombyra` | https://export.arxiv.org/api/query?search_query=all:dombra+OR+all:dombyra&max_results=50 | 429 | — | rate-limited from both network paths |
| webfetch | `export.arxiv.org all:kazakh AND all:music` | https://export.arxiv.org/api/query?search_query=all:kazakh+AND+all:music&max_results=50 | 429 | — |  |
| webfetch | `huggingface.co/Eraly-ml profile` | https://huggingface.co/Eraly-ml | 200 | — | Yeraly Gainulla; 10 models, 3 datasets (NLP); kui-gen-dataset NOT listed publicly |
| webfetch | `loc.gov/audio ?q=kazakh fo=json` | https://www.loc.gov/audio/?q=kazakh&fo=json | 403 | — | 403 from alternate path as well (Codex also got 403) |
| webfetch | `sounds.bl.uk` | https://sounds.bl.uk/ | DNS ENOTFOUND | — | host does not resolve from either path |
| webfetch | `UNESCO ICH RL 00996 Kazakh traditional art of Dombra Kuy` | https://ich.unesco.org/en/RL/kazakh-traditional-art-of-dombra-kuy-00996 | 200 | — | one embedded YouTube video '© 2013 by A. Suleyev'; photos '© S. Suleimenova-Bazargalieva'; no open licence |
| webfetch | `Astana IT University journal article 476 (Classification of Kazakh music genres)` | https://journal.astanait.edu.kz/index.php/ojs/article/view/476 | 200 | — | 800 tracks / 5 genres (classical, jazz, Kazakh rock, hip hop, pop); no dataset link; article CC BY-NC-ND 4.0 |

#### WebSearch (24 queries)

| Source | Query | Endpoint / URL | HTTP | Hits | Note |
|---|---|---|---|---|---|
| websearch | `site:kaggle.com/datasets dombra OR dombyra OR "kazakh music" OR "kazakh songs" OR "kazakh folk"` | WebSearch | 200 | 0 | no Kaggle dataset pages returned |
| websearch | `Kazakh dombra dataset audio recordings kui download "CC BY" OR "creative commons" OR zenodo OR figshare OR "open data"` | WebSearch | 200 | 10 | only ISSAI speech corpora (KSC, KSD, KazakhTTS/2) |
| websearch | `Kazakh singing voice dataset OR corpus "Kazakh" song lyrics audio paper 2024 OR 2025 OR 2026 arxiv OR ISMIR OR ICASSP OR Interspeech` | WebSearch | 200 | 9 | no Kazakh singing corpus; KSC2 (speech) only |
| websearch | `"домбыра" OR "домбра" күй аудио датасет OR "открытые данные" OR "creative commons" записи скачать архив` | WebSearch | 200 | 10 | pirate mp3 sites and generic CC-audio blog posts only |
| websearch | `kaggle dataset dombra kazakh instrument audio` | WebSearch | 200 | 6 | commercial sample libraries only (Big Fish, Impact Soundworks) |
| websearch | `kaggle "kazakh" songs OR music OR "kui" dataset audio wav mp3` | WebSearch | 200 | 10 | surfaced ACL Anthology page for Kazakh Songs ASR; no Kaggle Kazakh dataset |
| websearch | `"dombra" OR "dombyra" transcription OR classification dataset github OR zenodo audio recordings kazakh kui deep learning 2023 OR 2024 OR 2025` | WebSearch | 200 | 9 | KazEmoTTS (speech) only |
| websearch | `"Kazakh" music emotion recognition dataset OR "kazakh traditional music" dataset paper audio clips` | WebSearch | 200 | 8 | KazEmoTTS 74.85 h CC BY 4.0 (speech); no music emotion dataset |
| websearch | `site:archive.org dombra OR dombyra OR "kazakh folk" audio` | WebSearch | 200 | 6 | surfaced MusicRepublic LP-rip archive (Khamzin, dombra) and Smithsonian Bardic Divas podcast page |
| websearch | `Common Voice Kazakh kk hours validated "Common Voice" 17..22 kazakh` | WebSearch | 200 | 10 | CV 24.0 kk: 2,750 clips, 3.76 h, 2.39 h validated, 193 speakers (Data Collective page) |
| websearch | `kazneb.kz "1000 күй" OR "1000 кюев" аудио пользовательское соглашение авторские права условия использования` | WebSearch | 200 | 8 | no kazneb terms page indexed; caravan.kz article on the 2009 CD set |
| websearch | `kaggle.com/datasets kazakh dombyra OR "домбыра" OR "kazakh instruments" OR "kazakh folk music"` | WebSearch | 200 | 0 | no Kaggle pages |
| websearch | `Eraly-ml kui-gen-dataset huggingface kazakh kui generation` | WebSearch | 200 | 9 | cached snippets of the now-private dataset: kui titles Байжұма, Ақшолпан, Жігер with kk descriptions + audio |
| websearch | `"dombra" OR "dombyra" OR "kazakh" site:zenodo.org audio OR recording OR dataset` | WebSearch | 200 | 0 | no Zenodo pages returned |
| websearch | `site:ismir.net OR site:archives.ismir.net OR site:zenodo.org ISMIR kazakh OR dombra OR "central asian" music dataset paper` | WebSearch | 200 | 0 | no ISMIR paper on Kazakh music |
| websearch | `site:isca-archive.org kazakh singing OR song OR music corpus` | WebSearch | 200 | 6 | KSC2 (Interspeech 2022, speech) only |
| websearch | `ieeexplore OR ICASSP "Kazakh" dombra OR kui OR "traditional music" dataset audio classification recognition 2020..2026` | WebSearch | 200 | 10 | Astana IT Univ. 800-track genre paper (not released); no ICASSP Kazakh music dataset |
| websearch | `"冬不拉" 数据集 OR 语料 音频 哈萨克 民歌 OR 演唱 下载` | WebSearch | 200 | 8 | Chinese-language angle (Xinjiang Kazakh): media articles/Bilibili only, no dataset |
| websearch | `site:data.mendeley.com OR site:ieee-dataport.org OR site:datadryad.org kazakh music OR dombra OR "kazakh song"` | WebSearch | 200 | 0 | no repository pages |
| websearch | `"dombra" OR "dombyra" OR "kazakh" site:openverse.org OR site:jamendo.com OR site:ccmixter.org OR site:freemusicarchive.org 2025 OR 2026` | WebSearch | 200 | 0 | nothing new on CC music platforms |
| websearch | `site:scidb.cn OR site:science-data-bank 哈萨克 OR 冬不拉 音乐 数据集` | WebSearch | 200 | 0 | ScienceDB: no Kazakh/dombra dataset |
| websearch | `"Kazakh" "singing" OR "songs" corpus OR dataset huggingface 2025 2026 -speech kk audio lyrics "traditional" OR "folk"` | WebSearch | 200 | 9 | only yeshpanovrustem/kazakh_songs_asr (gated NC) again |
| websearch | `site:arxiv.org dombra OR dombyra kazakh music` | WebSearch | 200 | 0 | no arXiv paper on dombra |
| websearch | `site:arxiv.org "Kazakh" singing OR "song" OR "kui" audio dataset -"speech corpus"` | WebSearch | 200 | 8 | KazakhTTS, KazakhTTS2, KazEmoTTS (all speech) |

## 4. Not reachable / coverage limits (2026-09-14, this network)

| Platform | What happened | Status |
|---|---|---|
| Internet Archive (`archive.org/advancedsearch.php`, `/details/`, `/metadata/`) | local curl: connect timeout 40 s; WebFetch path: `read ECONNRESET` on 6 different URLs (one allowed retry used) | **NOT REACHABLE** — MusicRepublic item (row 77) unread |
| OSF API (`api.osf.io/v2/nodes|registrations`) | 8/12 calls timed out / 502; `dombyra` and `dombra [registrations]` returned 0 public nodes; WebFetch path also 60 s timeout; `osf.io/search` is a JS shell | partial — 0 hits where it answered |
| arXiv export API | HTTP 429 on all 9 queries (plus 503/ReadTimeout), both network paths; WebSearch fallback used (`site:arxiv.org`) — only KazakhTTS/TTS2/KazEmoTTS/KSC papers | **NOT REACHABLE** (rate-limited) |
| Library of Congress `loc.gov/audio ?fo=json` | HTTP 403 (as in CODEX) | not reachable |
| British Library Sounds | DNS `ENOTFOUND sounds.bl.uk` | not reachable |
| Kaggle | dataset listing is a JS shell; API needs credentials; 4 web searches found **no** Kazakh/dombra dataset page | metadata-only, nothing found |
| Papers with Code | `paperswithcode.com/search?q=kazakh` returns a 1.5 MB shell (site redirects to HF Papers since 2025) | superseded; HF Papers covered via WebSearch |
| Openverse API | anonymous `page_size` max 20 (first attempt at 50 → 401); rerun at 20 with pagination — complete | complete |
| Wikimedia Commons API | rate-limited once ("too many requests") then `RemoteDisconnected` mid-script; 10 of 24 `filetype:` searches ran (all Latin + `домбыра`); 14 (`күй`, `қазақ`, `казахская`, `kobyz`, `zhambyl`, `жамбыл`, `kazakh anthem/singing/song`, `kazakhstan music/folk`) did **not** run and were not retried per coordinator instruction | partial |
| ScienceDB (`scidb.cn`) | public search API path 404; web search 0 | not searched effectively |
| ISSAI GitHub READMEs (`IS2AI/Kazakh_Speech_Corpus_2`, `KazakhTTS2`) | 404 (repos renamed); sizes/licences taken from OpenSLR + issai.nu.edu.kz instead | ok |
| Common Voice per-language page | Mozilla Data Collective = JS shell ("Loading datasets…"); numbers taken from `common-voice/cv-dataset` release JSON (authoritative) | ok |
| kazneb.kz | catalogue readable; no terms page exists at any guessed path | ok |

## 5. Ranked "best next sources"

1. **Zhambyl Museum's Commons donation** (`Category:Content donated by Zhambyl Museum`, VRT ticket 2025081310002993) — the only
   provenance-clean CC BY-SA Kazakh material found in two rounds. This round's new clip (row 51) is 26 s; enumerate the whole
   category (`list=categorymembers`, one API call when Commons stops rate-limiting) for any further audio/video ≥ 30 s, and finish
   listening to the two films already on disk. No contact needed.
2. **Existing RTRK pool** (116 files, CC BY-NC 4.0) — still the only sizeable dombra/zhyr set on disk; per-recording provenance
   review + Kazakh-speaker transcription is worth more than any repository search (unchanged from CODEX #1).
3. **`yeshpanovrustem/kazakh_songs_asr`** — the only sung-Kazakh + per-line-text corpus in existence (row 65). Gated, NC,
   commercial songs: a founder decision on whether to request access for non-commercial research; never mirror-bypass.
4. **kazneb "1000 күй"** (row 80) — 41 CDs of named küys/performers with durations, state cultural-heritage programme; a rights
   request by a human to the Ministry of Culture / EL production is the only route, but the repertoire metadata alone is
   useful for the lyrics/title work.
5. **Zenodo "Digital Yurt"** (row 57) — restricted record advertising Kazakh lullaby recordings; a human could ask the depositor
   for the licence and file list.
6. **Internet Archive from another network** — MusicRepublic LP archive (row 77) and the still-unrun IA term sweep; expect
   mostly in-copyright Melodiya rips, so read `licenseurl` before hoping.
7. **Remaining 14 Commons CirrusSearch queries** (Cyrillic `күй`/`қазақ`/`казахская`, `zhambyl`, `kobyz`) — cheap, one script,
   run when Commons rate limits reset; the Latin sweep found nothing new, so expectation is low.
8. **Europeana** — fully searched with the API this round; every Kazakh dombra/vocal item (Philharmonie de Paris, BnF) is InC.
   Nothing to do unless the project can license from those institutions.
9. **Speech corpora as phonetic reference only** (rows 67–70: KSC 332 h CC BY 4.0, KSD 554 h CC BY-SA 3.0, KazakhTTS2 271 h
   CC BY 4.0, KazEmoTTS 74.85 h CC BY 4.0, Common Voice kk 2.52 h validated CC0) — none is singing; keep out of the music
   training set.
10. **Chinese-side repositories (ScienceDB, Xinjiang institutions)** for 哈萨克族/冬不拉 material — unsearched in practice (API 404);
    a Chinese-reading human could try the ScienceDB web UI. Low expectation of open licences.

## 6. Human decisions still open

- Whether to request access to `kazakh_songs_asr` (row 65) and/or the Zenodo "Digital Yurt" depositor (row 57) — both are NC/restricted.
- Whether to retry Internet Archive and the 14 unrun Commons queries from another network.
- Row 51 stays EXCLUDED (26 s exhibit clip); note only that its audio bed is unidentified and may be a third-party recording the museum added — not verified, not needed.
