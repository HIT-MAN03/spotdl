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
ARTIST_RESULTS_PER_PAGE = 50
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
    -a, --artist             - Artist mode: browse all songs by artist
    -b, --batch              - Batch download from file or track list

OPTIONS:
    -h, --help               - Show this help message
    -s, --search             - Force search mode (same as default)
    -a, --artist             - Artist mode (browse all artist songs)
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
    spotdl -a taylor swift           # Browse all Taylor Swift songs
    spotdl -q 4 shape of you         # Search with WAV quality
    spotdl -b playlist.txt           # Batch from file
    spotdl -b -q 5 "Artist - Song"   # Batch with FLAC quality
    spotdl --batch                   # Batch mode (paste tracks)

"""
    print(lime_text(help_text))


# Lime color for banner
LIME = "\033[1;92m"  # Bright lime green
RESET = "\033[0m"


def lime_text(text):
    """Apply lime green color to text"""
    result = ""
    lines = text.split('\n')
    for line in lines:
        result += LIME + line + RESET + '\n'
    return result


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
    print(lime_text(banner))
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
        "writethumbnail": True,
        "embed_thumbnail": True,
        "embed_metadata": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": quality_opt["codec"],
            "preferredquality": quality_opt["quality"],
        }, {
            "key": "FFmpegThumbnailsConvertor",
            "format": "jpg",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])


def search_songs(query: str, limit: int = 10):
    """Search for songs and return list of results with titles"""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "default_search": f"ytsearch{limit}",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)

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


def search_artist_tracks(artist_name: str):
    """Search for all tracks by an artist and return list of results"""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "default_search": f"ytsearch{ARTIST_RESULTS_PER_PAGE * 3}",
    }

    search_query = f"{artist_name} official audio"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch{ARTIST_RESULTS_PER_PAGE * 3}:{search_query}", download=False)

    if not result or "entries" not in result:
        return []

    songs = []
    seen_titles = set()
    for entry in result["entries"]:
        if entry:
            title = entry.get("title", "Unknown")
            duration = entry.get("duration", 0)
            
            # Filter to only include songs that mention the artist name
            if artist_name.lower() not in title.lower():
                continue
                
            # Skip duplicates
            if title in seen_titles:
                continue
            seen_titles.add(title)
            
            if duration and isinstance(duration, (int, float)):
                duration_int = int(duration)
                duration_str = f"{duration_int//60}:{duration_int%60:02d}"
            else:
                duration_str = "??"
            songs.append({"title": title, "duration": duration_str})

    return songs


def browse_artist_songs(artist_name: str):
    """Browse artist songs with pagination and multi-select"""
    print(f"\nSearching for all songs by: {artist_name}...")
    songs = search_artist_tracks(artist_name)

    if not songs:
        print("No results found.")
        return []

    total_songs = len(songs)
    total_pages = (total_songs + ARTIST_RESULTS_PER_PAGE - 1) // ARTIST_RESULTS_PER_PAGE
    current_page = 1
    selected_indices = set()

    print(f"\nFound {total_songs} songs by {artist_name}")
    print(f"Use 'n' for next page, 'p' for previous page")
    print(f"Type song numbers separated by commas to select (e.g., 1,3,5)")
    print(f"Type 'd' to download selected songs")
    print(f"Type 'q' to quit\n")

    while True:
        start_idx = (current_page - 1) * ARTIST_RESULTS_PER_PAGE
        end_idx = min(start_idx + ARTIST_RESULTS_PER_PAGE, total_songs)
        page_songs = songs[start_idx:end_idx]

        print(f"\n{'='*60}")
        print(f"Page {current_page}/{total_pages} - Showing songs {start_idx + 1}-{end_idx} of {total_songs}")
        print(f"Selected: {len(selected_indices)} song(s)")
        print(f"{'='*60}")

        for i, song in enumerate(page_songs, start_idx + 1):
            marker = "✓" if i in selected_indices else " "
            print(f"  [{marker}] [{i}] {song['title']} ({song['duration']})")

        print(f"{'='*60}")
        print(f"Commands: [n]ext page | [p]revious | [d]ownload | [q]uit | <numbers> to select")
        
        choice = input("\nEnter command: ").strip().lower()

        if choice == 'q':
            return []
        elif choice == 'n':
            if current_page < total_pages:
                current_page += 1
            else:
                print("Already on last page!")
        elif choice == 'p':
            if current_page > 1:
                current_page -= 1
            else:
                print("Already on first page!")
        elif choice == 'd':
            if not selected_indices:
                print("No songs selected! Select songs first.")
                continue
            selected_songs = [songs[i - 1]["title"] for i in sorted(selected_indices)]
            print(f"\nDownloading {len(selected_songs)} selected song(s):")
            for i, title in enumerate(selected_songs, 1):
                print(f"  {i}. {title}")
            return selected_songs
        else:
            # Parse comma-separated numbers
            try:
                numbers = [int(x.strip()) for x in choice.split(',')]
                for num in numbers:
                    if 1 <= num <= total_songs:
                        if num in selected_indices:
                            selected_indices.remove(num)
                        else:
                            selected_indices.add(num)
                    else:
                        print(f"Invalid number: {num}")
            except ValueError:
                print("Invalid input. Enter numbers separated by commas or use commands.")


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


def show_main_menu():
    """Display main menu with all available options"""
    menu = r"""
┌─────────────────────────────────────────────────────────────────┐
│                    🎵 MAIN MENU 🎵                              │
├─────────────────────────────────────────────────────────────────┤
│  [1] Search Song        - Search and download a specific song   │
│  [2] Browse Artist      - Browse all songs by an artist         │
│  [3] Spotify Playlist   - Download from Spotify playlist URL    │
│  [4] YouTube Playlist   - Download from YouTube playlist URL    │
│  [5] Batch Download     - Download multiple tracks from list    │
│  [6] Quick Download     - Direct download with query            │
│  [7] Change Quality     - Select audio quality (1-5)            │
│  [h] Help               - Show help information                 │
│  [q] Quit               - Exit the program                      │
└─────────────────────────────────────────────────────────────────┘
"""
    print(lime_text(menu))


def download_spotify_playlist(url, quality_opt):
    """Download songs from a Spotify playlist URL"""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": False,
        "noplaylist": False,
        "extract_flat": False,
        "writethumbnail": True,
        "embed_thumbnail": True,
        "embed_metadata": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": quality_opt["codec"],
            "preferredquality": quality_opt["quality"],
        }, {
            "key": "FFmpegThumbnailsConvertor",
            "format": "jpg",
        }],
    }
    
    safe_dir = DOWNLOAD_DIR
    os.makedirs(safe_dir, exist_ok=True)
    outtmpl = os.path.join(safe_dir, "%(playlist)s/%(title)s.%(ext)s")
    ydl_opts["outtmpl"] = outtmpl

    print(f"\nDownloading Spotify playlist...")
    print(f"Quality: {quality_opt['label']}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print("\n✅ Playlist download complete!")


def download_youtube_playlist(url, quality_opt):
    """Download songs from a YouTube playlist URL"""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": False,
        "noplaylist": False,
        "extract_flat": False,
        "writethumbnail": True,
        "embed_thumbnail": True,
        "embed_metadata": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": quality_opt["codec"],
            "preferredquality": quality_opt["quality"],
        }, {
            "key": "FFmpegThumbnailsConvertor",
            "format": "jpg",
        }],
    }
    
    safe_dir = DOWNLOAD_DIR
    os.makedirs(safe_dir, exist_ok=True)
    outtmpl = os.path.join(safe_dir, "%(playlist)s/%(title)s.%(ext)s")
    ydl_opts["outtmpl"] = outtmpl

    print(f"\nDownloading YouTube playlist...")
    print(f"Quality: {quality_opt['label']}")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    print("\n✅ Playlist download complete!")


def main():
    show_banner()

    downloaded_set = load_downloaded()
    quality_opt = QUALITY_OPTIONS["1"]  # Default quality

    # Check for command-line flags first (non-interactive mode)
    args = sys.argv[1:]

    if "-h" in args or "--help" in args or "-help" in args:
        show_help()
        return

    batch_mode = False
    artist_mode = False
    playlist_mode = False
    quality_selected = None

    if "-b" in args or "--batch" in args:
        batch_mode = True
        args = [a for a in args if a not in ["-b", "--batch"]]

    if "-a" in args or "--artist" in args:
        artist_mode = True
        args = [a for a in args if a not in ["-a", "--artist"]]

    if "-p" in args or "--playlist" in args:
        playlist_mode = True
        args = [a for a in args if a not in ["-p", "--playlist"]]

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

    if quality_selected and quality_selected in QUALITY_OPTIONS:
        quality_opt = QUALITY_OPTIONS[quality_selected]

    # If flags provided, run in non-interactive mode
    if artist_mode or batch_mode or playlist_mode:
        # Artist mode
        if artist_mode:
            artist_name = " ".join(args) if args else input("Enter artist name: ").strip()
            if not artist_name:
                print("No artist name provided.")
                return
            selected_songs = browse_artist_songs(artist_name)
            if not selected_songs:
                return
            if not quality_selected:
                quality_opt = select_quality()
            print(f"\nQuality: {quality_opt['label']}")
            for i, song in enumerate(selected_songs, 1):
                print(f"[{i}/{len(selected_songs)}] Downloading: {song}")
                try:
                    download_audio(song, quality_opt)
                    save_downloaded(song)
                except Exception as e:
                    print(f"Failed to download {song}: {e}")
            print(f"\n✅ Downloaded {len(selected_songs)} song(s)!")
            return

        # Playlist mode
        if playlist_mode:
            playlist_url = " ".join(args) if args else input("Enter playlist URL: ").strip()
            if not playlist_url:
                print("No URL provided.")
                return
            if not quality_selected:
                quality_opt = select_quality()
            download_spotify_playlist(playlist_url, quality_opt)
            return

        # Batch mode
        if batch_mode:
            if args:
                source = args[0]
                if os.path.isfile(source):
                    with open(source, "r", encoding="utf-8") as f:
                        tracks = parse_track_list(f.read())
                else:
                    tracks = parse_track_list(" ".join(args))
            else:
                print("Paste your list of songs. Finish with empty line:")
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

            print("\n✅ All downloads complete!")
            return

    # Interactive mode - show main menu
    show_main_menu()

    while True:
        choice = input("\nEnter your choice [1-7] (or 'q' to quit): ").strip().lower()

        if choice == 'q':
            print("\nGoodbye! 👋")
            return
        elif choice == 'h':
            show_help()
            show_main_menu()
            continue
        elif choice == '7':
            quality_opt = select_quality()
            show_main_menu()
            continue
        elif choice == '6':
            query = input("\nEnter song/artist to quick download: ").strip()
            if not query:
                print("No query provided.")
                show_main_menu()
                continue
            print(f"\nDownloading: {query}")
            print(f"Quality: {quality_opt['label']}")
            try:
                download_audio(query, quality_opt)
                save_downloaded(query)
                print("\n✅ Download complete!")
            except Exception as e:
                print(f"Failed to download: {e}")
            show_main_menu()
        elif choice == '5':
            print("\nPaste your list of songs (e.g. 'Artist - Title'). Finish with empty line:")
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
                show_main_menu()
                continue

            quality_opt = select_quality()
            print(f"\nFound {len(tracks)} tracks.")
            print(f"Quality: {quality_opt['label']}")
            print("Starting download...\n")

            for i, track in enumerate(tracks, 1):
                print(f"[{i}/{len(tracks)}] Downloading: {track}")
                try:
                    download_audio(track, quality_opt)
                    save_downloaded(track)
                except Exception as e:
                    print(f"Failed to download {track}: {e}")

            print("\n✅ All downloads complete!")
            show_main_menu()

        elif choice == '4':
            url = input("\nEnter YouTube playlist URL: ").strip()
            if not url:
                print("No URL provided.")
                show_main_menu()
                continue

            quality_opt = select_quality()
            download_youtube_playlist(url, quality_opt)
            show_main_menu()

        elif choice == '3':
            url = input("\nEnter Spotify playlist URL: ").strip()
            if not url:
                print("No URL provided.")
                show_main_menu()
                continue

            quality_opt = select_quality()
            download_spotify_playlist(url, quality_opt)
            show_main_menu()

        elif choice == '2':
            artist_name = input("\nEnter artist name: ").strip()
            if not artist_name:
                print("No artist name provided.")
                show_main_menu()
                continue

            selected_songs = browse_artist_songs(artist_name)
            if not selected_songs:
                show_main_menu()
                continue

            quality_opt = select_quality()
            print(f"\nQuality: {quality_opt['label']}")

            for i, song in enumerate(selected_songs, 1):
                print(f"[{i}/{len(selected_songs)}] Downloading: {song}")
                try:
                    download_audio(song, quality_opt)
                    save_downloaded(song)
                except Exception as e:
                    print(f"Failed to download {song}: {e}")

            print(f"\n✅ Downloaded {len(selected_songs)} song(s)!")
            show_main_menu()

        elif choice == '1':
            query = input("\nEnter song name (with or without artist): ").strip()
            if not query:
                print("No search query provided.")
                show_main_menu()
                continue

            selected_song = select_song(query)
            if not selected_song:
                show_main_menu()
                continue

            quality_opt = select_quality()
            print(f"\nDownloading: {selected_song}")
            print(f"Quality: {quality_opt['label']}")

            try:
                download_audio(selected_song, quality_opt)
                save_downloaded(selected_song)
                print("\n✅ Download complete!")
            except Exception as e:
                print(f"Failed to download: {e}")

            show_main_menu()

        else:
            print("Invalid choice. Enter a number 1-7 or 'q' to quit.")


if __name__ == "__main__":
    main()
