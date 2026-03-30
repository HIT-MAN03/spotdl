# ⚡ Heavenly Demon Spotify Downloader

A powerful Python tool to search and download Spotify tracks from YouTube in multiple quality formats (MP3, WAV, FLAC).

## ✨ New Features

- 🔍 **Search Mode** - Search songs by name (with or without artist), select from 10 results
- 🎚️ **Quality Selection** - Choose from 5 quality options (MP3 320/192/128, WAV, FLAC)
- 📋 **Batch Mode** - Download multiple tracks from file or list
- 📝 **Download Log** - Tracks are logged to avoid re-downloading
- 🚀 **Fast & Lightweight** - Works on Termux (Android) and Linux

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
git clone https://github.com/HIT-MAN03/spotdl.git
```

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
pkg update && pkg upgrade && pkg install git python ffmpeg && pip install yt_dlp && git clone https://github.com/HIT-MAN03/spotdl.git && chmod +x ~/spotdl/bin/spotdl ~/spotdl/bin/spotdl.py && echo 'export PATH="$HOME/spotdl/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

---

## 📖 Usage

### 🔍 Search Mode (Default)
Search for songs, select by number, choose quality:

```bash
spotdl
spotdl "daylight"
spotdl "shape of you"
```

**Interactive flow:**
1. Enter song name (with or without artist)
2. View 10 search results with duration
3. Select song by number (1-10)
4. Choose audio quality (1-5)

### 🎚️ Quality Options

| # | Quality | Description |
|---|---------|-------------|
| 1 | MP3 320kbps | High quality MP3 (default) |
| 2 | MP3 192kbps | Medium quality MP3 |
| 3 | MP3 128kbps | Standard quality MP3 |
| 4 | WAV | Uncompressed lossless |
| 5 | FLAC | Compressed lossless |

### 🎯 Command Line Options

```bash
# Show help
spotdl -h
spotdl --help

# Search with pre-selected quality
spotdl -q 4 "daylight"      # WAV quality
spotdl -q 5 "shape of you"  # FLAC quality

# Batch mode (multiple tracks)
spotdl -b "Artist - Song1" "Artist - Song2"
spotdl -b playlist.txt
spotdl --batch

# Combine options
spotdl -b -q 5 playlist.txt    # Batch with FLAC
spotdl -q 1 "song name"        # Search with MP3 320
```

### 📋 Batch Mode Examples

**From file:**
```bash
spotdl -b tracks.txt
```

**From command line:**
```bash
spotdl -b "Just Pete - Drowning" "The Weeknd - Blinding Lights"
```

**Paste interactively:**
```bash
spotdl --batch
# Paste your list, press Enter on empty line to start
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `spotdl` | Bash wrapper script |
| `spotdl.py` | Main Python script |
| `~/Music/SpotifyDownloads/` | Output folder for audio files |
| `downloaded_tracks.txt` | Log of downloaded tracks |

---

## ⚙️ Configuration

Edit these variables in `spotdl.py` to customize:

```python
DOWNLOAD_DIR = "/storage/emulated/0/Music/SpotifyDownloads"  # Output directory
AUDIO_BITRATE = "320"           # Default MP3 quality (kbps)
SEARCH_RESULTS = 10             # Number of search results
LOG_FILE = "downloaded_tracks.txt"  # Track log file
```

---

## 🎯 Examples

```
██╗  ██╗███████╗ █████╗ ██╗   ██╗███████╗███╗   ██╗██╗     ██╗   ██╗
██║  ██║██╔════╝██╔══██╗██║   ██║██╔════╝████╗  ██║██║     ╚██╗ ██╔╝
███████║█████╗  ███████║██║   ██║█████╗  ██╔██╗ ██║██║      ╚████╔╝ 
██╔══██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║       ╚██╔╝  
██║  ██║███████╗██║  ██║ ╚████╔╝ ███████╗██║ ╚████║███████╗   ██║  
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝  

██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║
██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

        ⚡ HEAVENLY DEMON SPOTIFY DOWNLOADER ⚡
```

---

## ❓ Troubleshooting

**JavaScript runtime warning:**
```
WARNING: [youtube] No supported JavaScript runtime could be found.
```
Install a JS runtime for best results:
```bash
pkg install nodejs
# or
pkg install deno
```

**Permission denied:**
```bash
chmod +x ~/bin/spotdl ~/bin/spotdl.py
```

**Command not found:**
```bash
export PATH="$HOME/bin:$PATH"
source ~/.bashrc
```

---

## 📝 Changelog

### v2.0
- ✅ Added search mode with song selection
- ✅ Added 5 quality options (MP3, WAV, FLAC)
- ✅ Added help system (-h flag)
- ✅ Added batch mode (-b flag)
- ✅ Fixed duration display bug

### v1.0
- Initial release with basic download functionality

---

## 👤 Author

**HIT-MAN03**

## 📄 License

MIT License
