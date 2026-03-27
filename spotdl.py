#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import yt_dlp

# ---------- CONFIG ----------
DOWNLOAD_DIR = "downloads"
AUDIO_BITRATE = "320"  # kbps for mp3 extraction
LOG_FILE = "downloaded_tracks.txt"  # tracks already downloaded
# ---------------------------

# ---------- ASCII HEADER ----------
ASCII_ART = r"""
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
"""

# ---------- FUNCTIONS ----------

def sanitize_filename(name: str) -> str:
    """Remove illegal characters from filenames"""
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:180] if len(name) > 180 else name

def download_audio_mp3(query: str) -> str:
    """Download a single track from YouTube and convert to mp3"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    safe_base = sanitize_filename(query)
    mp3_path = os.path.join(DOWNLOAD_DIR, f"{safe_base}.mp3")

    if os.path.exists(mp3_path):
        return mp3_path

    outtmpl = os.path.join(DOWNLOAD_DIR, f"{safe_base}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "quiet": True,
        "noplaylist": True,
        "default_search": "ytsearch1",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": AUDIO_BITRATE,
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(query, download=True)

    if not os.path.exists(mp3_path):
        raise RuntimeError(f"Download finished but MP3 not found: {mp3_path}")

    return mp3_path

def download_all(tracks: list[str]) -> list[tuple[str, str]]:
    """
    Download all tracks, skipping already downloaded ones.
    Returns list of tuples: (track_query, mp3_path)
    """
    results = []

    # Load already downloaded tracks
    downloaded_set = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            downloaded_set = set(line.strip() for line in f if line.strip())

    total = len(tracks)
    for i, track in enumerate(tracks, start=1):
        if track in downloaded_set:
            print(f"[{i}/{total}] Skipping already downloaded: {track}")
            continue

        print(f"[{i}/{total}] Downloading: {track}")
        try:
            mp3_file = download_audio_mp3(track)
            results.append((track, mp3_file))
            downloaded_set.add(track)
            # Append to log immediately
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(track + "\n")
            print(f"Saved: {mp3_file}\n")
        except Exception as e:
            print(f"Failed: {track}\nReason: {e}\n")

    return results

def main() -> None:
    print(ASCII_ART)
    print("Paste your list of songs below. One per line. Enter an empty line to finish.\n")

    tracks = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        line = line.strip()
        if not line:
            break
        tracks.append(line)

    if not tracks:
        print("No tracks provided. Exiting.")
        return

    print(f"\n{len(tracks)} tracks to download.\nStarting download...\n")
    downloaded = download_all(tracks)

    print("\n✅ Download phase complete.")
    print(f"Downloaded successfully: {len(downloaded)} / {len(tracks)}")
    print(f"Check your '{DOWNLOAD_DIR}' folder for the files.")

if __name__ == "__main__":
    main()
