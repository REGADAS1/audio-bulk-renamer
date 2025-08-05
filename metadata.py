from pathlib import Path
from tinytag import TinyTag
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TSRC
import subprocess
import json
import os

# Caminhos corretos (ficheiros estão na raiz)
BWF_METAEDIT_PATH = os.path.join(os.path.dirname(__file__), "bwfmetaedit.exe")
FFPROBE_PATH = os.path.join(os.path.dirname(__file__), "ffprobe.exe")

def format_duration(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02}:{secs:02}:{millis:03}"

def get_file_metadata(file_path):
    tag = TinyTag.get(file_path)
    info = {
        "format": Path(file_path).suffix.lower().replace(".", ""),
        "duration": format_duration(tag.duration) if tag.duration else "",
        "samplerate": tag.samplerate or "",
        "bitrate": tag.bitrate or "",
        "bitdepth": getattr(tag, "bitdepth", "") or "",
        "channels": tag.channels or ""
    }

    if file_path.lower().endswith(".mp3"):
        try:
            id3 = EasyID3(file_path)
            full = ID3(file_path)
            info.update({
                "title": id3.get("title", [""])[0],
                "artist": id3.get("artist", [""])[0],
                "album": id3.get("album", [""])[0],
                "year": id3.get("date", [""])[0],
                "genre": id3.get("genre", [""])[0],
                "track": id3.get("tracknumber", [""])[0],
                "isrc": full.get("TSRC").text[0] if "TSRC" in full else ""
            })
        except Exception:
            pass
    elif file_path.lower().endswith(".wav"):
        info["isrc"] = get_wav_isrc(file_path)

    return info

def save_mp3_tags(file_path, title=None, artist=None, album=None, year=None, genre=None, track=None, isrc=None):
    try:
        audio = EasyID3(file_path)
    except Exception:
        audio = EasyID3()
    if title: audio["title"] = title
    if artist: audio["artist"] = artist
    if album: audio["album"] = album
    if year: audio["date"] = year
    if genre: audio["genre"] = genre
    if track: audio["tracknumber"] = track
    audio.save(file_path)

    id3 = ID3(file_path)
    if isrc:
        id3.add(TSRC(encoding=3, text=isrc))
    elif "TSRC" in id3:
        del id3["TSRC"]
    id3.save(file_path)

# === WAV: ISRC reading with ffprobe ===
def get_wav_isrc(filepath):
    try:
        result = subprocess.run(
            [
                FFPROBE_PATH,
                "-v", "quiet",
                "-print_format", "json",
                "-show_entries", "format_tags",
                filepath
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        tags = json.loads(result.stdout).get("format", {}).get("tags", {})
        return tags.get("ISRC", "") or tags.get("isrc", "")
    except Exception as e:
        print(f"[FFPROBE Error] ao ler ISRC: {e}")
        return ""

# === WAV: ISRC writing with bwfmetaedit ===
def set_wav_isrc(filepath, isrc_code):
    try:
        subprocess.run(
            [BWF_METAEDIT_PATH, f"--ISRC={isrc_code}", filepath],
            check=True
        )
        return True
    except Exception as e:
        print(f"[BWFMetaEdit Error] ao escrever ISRC: {e}")
        return False
