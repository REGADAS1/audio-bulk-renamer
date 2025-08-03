from pathlib import Path
from tinytag import TinyTag
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TSRC

def format_duration(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02}:{secs:02}:{millis:03}"

def get_file_metadata(file_path):
    """Reads audio file metadata with detailed information."""
    tag = TinyTag.get(file_path)
    info = {
        "format": Path(file_path).suffix.lower().replace(".", ""),  # ex: 'mp3'
        "duration": format_duration(tag.duration) if tag.duration else "",
        "samplerate": tag.samplerate or "",
        "bitrate": tag.bitrate or "",
        "bitdepth": getattr(tag, "bitdepth", "") or "",
        "channels": tag.channels or ""
    }
    # Tags ID3 apenas para MP3
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
    return info

def save_mp3_tags(file_path, title=None, artist=None, album=None, year=None, genre=None, track=None, isrc=None):
    """Saves the ID3 tags to the MP3 file."""
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
