# Clipo AI

Turn a long video into vertical (9:16) shorts with AI captions — fully local, no cloud, no subscription.

```
Video URL -> Download -> Analyze -> Find highlights -> 9:16 crop -> AI captions -> Export Shorts
```

## Features

- **Paste a URL and go** — YouTube/direct links via yt-dlp, or pick a local file
- **AI transcription** — faster-whisper with word-level timestamps (tiny/base/small/medium)
- **Highlight detection** — offline heuristic: speech density, hook words, sentence starts, audio energy
- **Auto framing** — YuNet face detection + smooth multi-face tracking steers the 9:16 crop (`Framing: auto`)
- **Caption scrubbing** — detects burned-in captions in the source and erases them (inpainting) before re-captioning
- **Karaoke captions** — per-word highlight, custom size/position/colors, burned in
- **Guaranteed audio** — explicit stream mapping, loudness normalized to -16 LUFS, post-export audio validation
- **Live UI** — step checklist, progress bar, cancel support, friendly error messages
- **Portable build** — single zip that runs on any Windows 10/11 PC (no Python needed)

## Requirements

- Windows 10/11 (macOS/Linux work for development with minor tweaks)
- Python 3.11 (3.10-3.12)
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) on PATH (`winget install Gyan.FFmpeg`)

## Setup & run

```bat
git clone https://github.com/<you>/clipo-ai.git
cd clipo-ai
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py
```

The first transcription downloads the Whisper model you select (`small` ~= 460 MB, once, then cached).

## Build the portable exe

```bat
build_exe.bat
```

Outputs into `dist\`:

| Artifact | Purpose |
| --- | --- |
| `ClipoAI\ClipoAI.exe` | folder build, starts fast |
| `ClipoAI_onefile.exe` | single portable exe |
| `ClipoAI-portable.zip` | shareable zip: exe + ffmpeg + ffprobe + README |

## Project structure

```
app/
  config.py            persisted settings (%APPDATA%/ClipoAI)
  ui/
    main_window.py     CustomTkinter window, settings dialog
    widgets.py         pipeline step checklist
    theme.py           colors/fonts
  core/
    pipeline.py        orchestration (worker thread, progress, cancel)
    downloader.py      yt-dlp with audio verification + retry
    prober.py          ffprobe wrapper
    transcriber.py     faster-whisper (word timestamps, VAD)
    highlights.py      offline highlight scoring
    faces.py           YuNet face detection + smooth tracking
    caption_scrubber.py burned-in caption detection + inpainting
    cropper.py         9:16 framing, dynamic crop, loudnorm, export
    captions.py        ASS karaoke caption builder
    errors.py          friendly error types
  utils/
    ffmpeg_loc.py      locate ffmpeg (PATH or bundled)
tests/
  test_pipeline.py     end-to-end test on a synthetic TTS video
scripts/               icon + zip packaging helpers
assets/                icon, YuNet model
```

## Settings

Persisted to `%APPDATA%\ClipoAI\settings.json`: number of shorts, min/max length, Whisper model, framing mode, caption font size / position / words-per-line / highlight color, remove-captions toggle, output folder.

## Tests

```bat
.venv\Scripts\python tests\test_pipeline.py
```

Builds a synthetic narrated video (Windows SAPI TTS), runs the whole pipeline (transcribe, highlights, face track, caption scrub, export), and validates: 1080x1920, expected durations, audio present, burned-in captions removed.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| App seems not to open | First launch of the onefile exe unpacks for 15-30 s; also allow it in SmartScreen ("More info" -> "Run anyway"). Crash details: `%USERPROFILE%\ClipoAI\crash.log` |
| "ffmpeg was not found" | Install FFmpeg or place `ffmpeg.exe`/`ffprobe.exe` next to the app |
| Download fails on a site | Update yt-dlp: `.venv\Scripts\pip install -U yt-dlp` |
| No captions in output | Video has no speech (handled: captions skipped) or try a larger model |
| Shorts silent | Check the log's `Audio check:` line; sources without audio produce silent shorts by design |

## Legal

Only download and reuse content you own or have permission to use — the app requires you to confirm this before every run. For free safe sources see Pexels, Pixabay, Mixkit, YouTube's Creative Commons filter, or Blender open movies (credit CC-BY authors as required).

## License

[MIT](LICENSE)
