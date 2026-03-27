# ⚡ Heavenly Demon Spotify Downloader

A powerful Python tool to download Spotify tracks and playlists from YouTube in high-quality MP3 format.

## Features

- 🎵 Download tracks from YouTube using Spotify track names
- 🎧 High-quality 320kbps MP3 output
- 📝 Tracks are logged to avoid re-downloading
- 🚀 Fast and lightweight
- 💻 Works on Termux (Android) and Linux

## Requirements

- Python 3
- `yt_dlp` (`pip install yt_dlp`)
- `ffmpeg` (for audio extraction)

### Install Dependencies (Termux)

```bash
pkg install python ffmpeg
pip install yt_dlp
```

## Usage

1. Run the script:
   ```bash
   ./spotdl
   # or
   python spotdl.py
   ```

2. Paste your list of songs (one per line)
3. Press Enter on an empty line to start downloading

## Example

```
██╗  ██╗███████╗ █████╗ ██╗   ██╗███████╗███╗   ██╗██╗     ██╗   ██╗
██║  ██║██╔════╝██╔══██╗██║   ██║██╔════╝████╗  ██║██║     ╚██╗ ██╔╝
███████║█████╗  ███████║██║   ██║█████╗  ██╔██╗ ██║██║      ╚████╔╝
██╔══██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║       ╚██╔╝
██║  ██║███████╗██║  ██║ ╚████╔╝ ███████╗██║ ╚████║███████╗   ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝

██████╗ ███████╗███╗   ██╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║
██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

        ⚡ HEAVENLY DEMON SPOTIFY DOWNLOADER ⚡
```

## Files

| File | Description |
|------|-------------|
| `spotdl` | Bash wrapper script |
| `spotdl.py` | Main Python script |
| `downloads/` | Output folder for MP3 files |
| `downloaded_tracks.txt` | Log of downloaded tracks |

## Configuration

Edit these variables in `spotdl.py` to customize:

```python
DOWNLOAD_DIR = "downloads"      # Output directory
AUDIO_BITRATE = "320"           # MP3 quality (kbps)
LOG_FILE = "downloaded_tracks.txt"  # Track log file
```

## Author

**HIT-MAN03**

## License

MIT License
