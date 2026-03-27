#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import yt_dlp

# ---------- CONFIG ----------
DOWNLOAD_DIR = "/storage/emulated/0/Music/SpotifyDownloads"
AUDIO_BITRATE = "320"
LOG_FILE = "downloaded_tracks.txt"
# ---------------------------

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
    print("\033[1;36m" + banner + "\033[0m")


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:180]


def download_audio(query: str):
    safe = sanitize_filename(query)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    outtmpl = os.path.join(DOWNLOAD_DIR, f"{safe}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",  # 🔥 better real quality
        "outtmpl": outtmpl,
        "quiet": False,
        "noplaylist": True,
        "default_search": "ytsearch1",  # ✅ KEEPING OLD ACCURACY
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": AUDIO_BITRATE,
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])


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

    # Input handling
    if len(sys.argv) > 1:
        source = sys.argv[1]
        if os.path.isfile(source):
            with open(source, "r", encoding="utf-8") as f:
                tracks = parse_track_list(f.read())
        else:
            tracks = parse_track_list(source)
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

    print(f"\nFound {len(tracks)} tracks.\nStarting download...\n")

    for i, track in enumerate(tracks, 1):
        if track in downloaded_set:
            print(f"[{i}/{len(tracks)}] Skipping (already downloaded): {track}")
            continue

        print(f"[{i}/{len(tracks)}] Downloading: {track}")

        try:
            download_audio(track)
            save_downloaded(track)
        except Exception as e:
            print(f"Failed to download {track}: {e}")

    print("\n✅ All downloads complete! Check your Music/SpotifyDownloads folder.")


if __name__ == "__main__":
    main()
