# ⚡ Heavenly Demon Spotify Downloader

A powerful Python tool to download Spotify tracks and playlists from YouTube in high-quality MP3 format.

## Features

- 🎵 Download tracks from YouTube using Spotify track names
- 🎧 High-quality 320kbps MP3 output
- 📝 Tracks are logged to avoid re-downloading
- 🚀 Fast and lightweight
- 💻 Works on Termux (Android) and Linux

---

## 📥 COMPLETE INSTALLATION GUIDE FOR NEWBIES

Follow these steps in order:

### Step 1: Install Git (Required to Clone the Repo)

```bash
pkg update && pkg upgrade
pkg install git
```

### Step 2: Clone the Repository

```bash
cd ~
git clone <YOUR_GIT_REPO_URL_HERE>
```

> ⚠️ Replace `<YOUR_GIT_REPO_URL_HERE>` with your actual GitHub/Git repo URL (e.g., `https://github.com/YOUR_USERNAME/spotdl.git`)

### Step 3: Install Python and Dependencies

```bash
pkg install python ffmpeg
pip install yt_dlp
```

### Step 4: Make the Script Executable

```bash
chmod +x ~/bin/spotdl
chmod +x ~/bin/spotdl.py
```

### Step 5: Add bin to PATH (Optional but Recommended)

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 Quick One-Line Setup (Copy & Paste Everything)

```bash
pkg update && pkg upgrade && pkg install git python ffmpeg && pip install yt_dlp && cd ~ && git clone <YOUR_GIT_REPO_URL_HERE> && chmod +x ~/bin/spotdl ~/bin/spotdl.py && echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

> ⚠️ Remember to replace `<YOUR_GIT_REPO_URL_HERE>` with your actual repo URL!

---

## Usage

## Usage

### Quick Download (Single Track)
```bash
spotdl "Artist Name - Song Title"
# or
python spotdl.py "Artist Name - Song Title"
```

**Examples:**
```bash
spotdl "Just Pete - Drowning"
spotdl "The Weeknd - Blinding Lights"
```

### Interactive Mode (Multiple Tracks)
```bash
spotdl
# or
python spotdl.py
```
Then paste your list of songs (one per line) and press Enter on an empty line to start.

### From File
```bash
spotdl tracks.txt
# or
python spotdl.py tracks.txt
```

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
