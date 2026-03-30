#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import yt_dlp

# ---------- CONFIG ----------
DOWNLOAD_DIR = "/storage/emulated/0/Music/SpotifyDownloads"
AUDIO_BITRATE = "320"
LOG_FILE = "downloaded_tracks.txt"
SEARCH_RESULTS = 10
# ---------------------------

QUALITY_OPTIONS = {
    "1": {"format": "bestaudio[ext=m4a]/bestaudio/best", "codec": "mp3", "quality": "320", "label": "MP3 320kbps"},
    "2": {"format": "bestaudio[ext=m4a]/bestaudio/best", "codec": "mp3", "quality": "192", "label": "MP3 192kbps"},
    "3": {"format": "bestaudio[ext=m4a]/bestaudio/best", "codec": "mp3", "quality": "128", "label": "MP3 128kbps"},
    "4": {"format": "bestaudio", "codec": "wav", "quality": "", "label": "WAV (Lossless)"},
    "5": {"format": "bestaudio[ext=flac]/bestaudio", "codec": "flac", "quality": "", "label": "FLAC (Lossless)"},
}


def show_help():
    """Display help information"""
    help_text = r"""
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

USAGE:
    spotdl [OPTIONS] [SEARCH_QUERY]

MODES:
    (default) Search Mode    - Search songs, select by number, choose quality
    -b, --batch              - Batch download from file or track list

OPTIONS:
    -h, --help               - Show this help message
    -s, --search             - Force search mode (same as default)
    -b, --batch              - Batch mode for multiple tracks
    -q, --quality <NUM>      - Select audio quality (1-5)

QUALITY OPTIONS:
    [1] MP3 320kbps          - High quality MP3 (default)
    [2] MP3 192kbps          - Medium quality MP3
    [3] MP3 128kbps          - Standard quality MP3
    [4] WAV (Lossless)       - Uncompressed audio
    [5] FLAC (Lossless)      - Compressed lossless audio

EXAMPLES:
    spotdl                           # Interactive search mode
    spotdl daylight                  # Search for "daylight"
    spotdl -q 4 shape of you         # Search with WAV quality
    spotdl -b playlist.txt           # Batch from file
    spotdl -b -q 5 "Artist - Song"   # Batch with FLAC quality
    spotdl --batch                   # Batch mode (paste tracks)

"""
    print("\033[1;36m" + help_text + "\033[0m")


# Rainbow colors
RAINBOW_COLORS = [
    "\033[1;31m",  # Red
    "\033[1;33m",  # Yellow
    "\033[1;32m",  # Green
    "\033[1;36m",  # Cyan
    "\033[1;34m",  # Blue
    "\033[1;35m",  # Magenta
]
RESET = "\033[0m"


def rainbow_text(text):
    """Apply rainbow colors to text"""
    result = ""
    color_idx = 0
    for char in text:
        if char == '\n':
            result += char + RESET
            color_idx = 0
        else:
            result += RAINBOW_COLORS[color_idx % len(RAINBOW_COLORS)] + char
            color_idx += 1
    return result + RESET


def show_banner():
    banner = r"""
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
    """
    
    # Animated loading effect
    loading_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    print()
    for _ in range(2):
        for frame in loading_frames:
            print(f"\r\033[1;33m{frame}\033[0m Loading...", end="", flush=True)
            time.sleep(0.08)
    
    print("\r" + " " * 20 + "\r", end="", flush=True)
    print(rainbow_text(banner))
    print()


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:180]


def download_audio(query: str, quality_opt: dict = None):
    if quality_opt is None:
        quality_opt = QUALITY_OPTIONS["1"]
    
    safe = sanitize_filename(query)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    outtmpl = os.path.join(DOWNLOAD_DIR, f"{safe}.%(ext)s")

    ydl_opts = {
        "format": quality_opt["format"],
        "outtmpl": outtmpl,
        "quiet": False,
        "noplaylist": True,
        "default_search": "ytsearch1",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": quality_opt["codec"],
            "preferredquality": quality_opt["quality"],
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])


def search_songs(query: str):
    """Search for songs and return list of results with titles"""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "default_search": "ytsearch10",
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch10:{query}", download=False)
    
    if not result or "entries" not in result:
        return []
    
    songs = []
    for entry in result["entries"]:
        if entry:
            title = entry.get("title", "Unknown")
            duration = entry.get("duration", 0)
            if duration and isinstance(duration, (int, float)):
                duration_int = int(duration)
                duration_str = f"{duration_int//60}:{duration_int%60:02d}"
            else:
                duration_str = "??"
            songs.append({"title": title, "duration": duration_str})
    
    return songs


def select_quality():
    """Display quality options and let user select"""
    print("\nSelect audio quality:")
    for key, opt in QUALITY_OPTIONS.items():
        print(f"  [{key}] {opt['label']}")
    
    while True:
        choice = input("\nEnter quality number (default: 1): ").strip()
        if not choice:
            return QUALITY_OPTIONS["1"]
        if choice in QUALITY_OPTIONS:
            return QUALITY_OPTIONS[choice]
        print("Invalid choice, try again.")


def select_song(query: str):
    """Search for songs and let user select by number"""
    print(f"\nSearching for: {query}...")
    songs = search_songs(query)
    
    if not songs:
        print("No results found.")
        return None
    
    print(f"\nFound {len(songs)} results:")
    for i, song in enumerate(songs, 1):
        print(f"  [{i}] {song['title']} ({song['duration']})")
    
    while True:
        choice = input("\nEnter song number to download (or 'q' to cancel): ").strip()
        if choice.lower() == 'q':
            return None
        if not choice.isdigit():
            print("Invalid choice, try again.")
            continue
        
        num = int(choice)
        if 1 <= num <= len(songs):
            return songs[num - 1]["title"]
        print(f"Enter a number between 1 and {len(songs)}.")


def parse_track_list(input_text: str):
    tracks = []
    for line in input_text.splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'^\d+\.\s*', '', line)
        tracks.append(line)
    return tracks


def load_downloaded():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def save_downloaded(track):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(track + "\n")


def main():
    show_banner()
    
    downloaded_set = load_downloaded()
    quality_opt = QUALITY_OPTIONS["1"]  # Default quality

    # Check for help flag first
    args = sys.argv[1:]
    
    if "-h" in args or "--help" in args or "-help" in args:
        show_help()
        return

    # Check for batch mode (-b flag) or quality flag (-q)
    batch_mode = False
    quality_selected = None
    
    if "-b" in args or "--batch" in args:
        batch_mode = True
        args = [a for a in args if a not in ["-b", "--batch"]]
    
    if "-q" in args or "--quality" in args:
        if "-q" in args:
            idx = args.index("-q")
            quality_selected = args[idx + 1] if idx + 1 < len(args) else None
            args.pop(idx)
            if quality_selected:
                args.pop(idx)
        elif "--quality" in args:
            idx = args.index("--quality")
            quality_selected = args[idx + 1] if idx + 1 < len(args) else None
            args.pop(idx)
            if quality_selected:
                args.pop(idx)
    
    # If quality selected via flag, use it
    if quality_selected and quality_selected in QUALITY_OPTIONS:
        quality_opt = QUALITY_OPTIONS[quality_selected]

    # Search mode (DEFAULT): search for songs and select by number
    if not batch_mode:
        if len(args) > 0:
            query = " ".join(args)
        else:
            query = input("Enter song name (with or without artist): ").strip()
        
        if not query:
            print("No search query provided.")
            return
        
        selected_song = select_song(query)
        if not selected_song:
            return
        
        # Select quality if not already selected via flag
        if not quality_selected:
            quality_opt = select_quality()
        
        print(f"\nDownloading: {selected_song}")
        print(f"Quality: {quality_opt['label']}")
        
        try:
            download_audio(selected_song, quality_opt)
            save_downloaded(selected_song)
            print("\n✅ Download complete!")
        except Exception as e:
            print(f"Failed to download: {e}")
        return

    # Batch mode: process multiple tracks from file or list
    if len(args) > 0:
        source = args[0]
        if os.path.isfile(source):
            with open(source, "r", encoding="utf-8") as f:
                tracks = parse_track_list(f.read())
        else:
            tracks = parse_track_list(" ".join(args))
    else:
        print("Paste your list of songs (e.g. 'Artist - Title'). Finish with empty line:")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            lines.append(line)
        tracks = parse_track_list("\n".join(lines))

    if not tracks:
        print("No tracks provided.")
        return

    print(f"\nFound {len(tracks)} tracks.")
    print(f"Quality: {quality_opt['label']}")
    print("Starting download...\n")

    for i, track in enumerate(tracks, 1):
        if track in downloaded_set:
            print(f"[{i}/{len(tracks)}] Skipping (already downloaded): {track}")
            continue

        print(f"[{i}/{len(tracks)}] Downloading: {track}")

        try:
            download_audio(track, quality_opt)
            save_downloaded(track)
        except Exception as e:
            print(f"Failed to download {track}: {e}")

    print("\n✅ All downloads complete! Check your Music/SpotifyDownloads folder.")


if __name__ == "__main__":
    main()
