# ⚡ Heavenly Demon Spotify Downloader

A powerful Python tool to search and download Spotify tracks from YouTube in multiple quality formats (MP3, WAV, FLAC).

## ✨ Features

- 🏠 **Interactive Main Menu** - Choose from 7 options on launch
- 🔍 **Search Mode** - Search songs by name, select from results, pick quality
- 🎤 **Browse Artist Mode** - Enter artist name, browse all their songs with pagination (50/page), multi-select by number, download multiple at once
- 🎵 **Spotify Playlist Download** - Paste Spotify playlist URL, download all tracks
- 📺 **YouTube Playlist Download** - Paste YouTube playlist URL, download all tracks
- 📋 **Batch Mode** - Download multiple tracks from file or pasted list
- 🎚️ **Quality Selection** - Choose from 5 quality options (MP3 320/192/128, WAV, FLAC)
- ⚡ **Quick Download** - Direct download without browsing results
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

### 🏠 Interactive Menu (Recommended)
Just run `spotdl` and you'll see the main menu with all options:

```bash
spotdl
```

**Menu Options:**
| # | Option | Description |
|---|--------|-------------|
| 1 | Search & Download a Single Song | Search YouTube, pick one song, choose quality |
| 2 | Browse Artist Songs | Enter artist name, browse all their songs (50/page), multi-select |
| 3 | Download from Spotify Playlist URL | Paste Spotify playlist URL, download all tracks |
| 4 | Download from YouTube Playlist URL | Paste YouTube playlist URL, download all tracks |
| 5 | Batch Download from File/List | Load tracks from file or paste a list |
| 6 | Quick Download | Direct download with query |
| 7 | Change Quality | Select audio quality (1-5) |
| h | Help | Show detailed help & usage info |
| q | Quit | Exit the program |

### 🎤 Browse Artist Mode
Browse all songs by an artist with pagination and multi-select:

```bash
spotdl -a "Taylor Swift"
spotdl -a "The Weeknd"
spotdl --artist "Drake"
```

**Interactive flow:**
1. Enter artist name
2. View paginated list of songs (50 per page)
3. Navigate: `n` = next page, `p` = previous page
4. Select songs: type numbers separated by commas (e.g., `1,3,5,10`)
5. Toggle: typing the same number again deselects it
6. Download: type `d` to download all selected songs
7. Quit: type `q` to cancel

**Example:**
```
Page 1/3 - Showing songs 1-50 of 127
==========================================
[ ] [1] Taylor Swift - Shake It Off (3:40)
[ ] [2] Taylor Swift - Blank Space (3:52)
[✓] [3] Taylor Swift - Love Story (3:56)
...
Enter command: 1,3,5    ← selects songs 1, 3, and 5
Enter command: 3        ← deselects song 3
Enter command: d        ← downloads selected songs
```

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

### 🎵 Playlist Download
Download entire playlists from Spotify or YouTube:

```bash
spotdl -p "https://open.spotify.com/playlist/..."
spotdl --playlist "https://www.youtube.com/playlist?list=..."
```

**Interactive flow:**
1. Paste playlist URL
2. Choose quality
3. All tracks download automatically

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

# Artist mode (browse all songs by artist)
spotdl -a "Taylor Swift"       # Browse Taylor Swift songs
spotdl -a "The Weeknd"         # Browse The Weeknd songs
spotdl --artist "Drake"        # Browse Drake songs

# Playlist mode
spotdl -p "https://open.spotify.com/playlist/..."  # Spotify playlist
spotdl -p "https://www.youtube.com/playlist?list=..."  # YouTube playlist
spotdl --playlist "URL"        # Same as -p

# Search with pre-selected quality
spotdl -q 4 "daylight"      # WAV quality
spotdl -q 5 "shape of you"  # FLAC quality

# Batch mode (multiple tracks)
spotdl -b "Artist - Song1" "Artist - Song2"
spotdl -b playlist.txt
spotdl --batch

# Combine options
spotdl -a "Taylor Swift" -q 4    # Artist mode with WAV
spotdl -b -q 5 playlist.txt      # Batch with FLAC
spotdl -p "URL" -q 3             # Playlist with MP3 128
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

### v3.0
- ✅ Added interactive main menu with 7 options
- ✅ Added Browse Artist mode with pagination (50 songs/page)
- ✅ Added multi-select for artist songs (comma-separated numbers)
- ✅ Added Spotify playlist URL download
- ✅ Added YouTube playlist URL download
- ✅ Added Quick Download option
- ✅ Added `-a/--artist` flag for artist mode
- ✅ Added `-p/--playlist` flag for playlist mode
- ✅ Next/Previous page navigation for artist browsing
- ✅ Toggle select/deselect for artist songs

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
