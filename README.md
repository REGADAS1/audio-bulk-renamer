# Audio Bulk Renamer 🎵

> ⚠️ This repository contains only the source code and does **not** distribute any compiled version of the final product. The project was developed by me as part of a professional collaboration and is shared here strictly for portfolio purposes.

---

**Audio Bulk Renamer** is a cross-platform desktop application designed for **batch renaming audio files** with optional metadata inspection and editing. Built with `PySide6`, it's tailored for **sound engineers**, **musicians**, and **audio professionals** who need a fast and visually pleasing tool to organize and prepare files.

---

## 🎯 Features

- ✅ Drag-and-drop interface for `.wav` and `.mp3` files
- ✅ Add prefix / suffix / replace text in filenames
- ✅ Audio info preview:
    - Format, Sample Rate, Bit Depth
    - Bitrate (for MP3), Duration, Channels
- ✅ Edit **ID3 tags** in `.mp3` files (title, artist, album, genre, year, ISRC, etc.)
- ✅ Edit **BWF metadata** in `.wav` files via `bwfmetaedit`
- ✅ Audio analysis powered by `ffprobe` (optional dependency)


---

## 🖥️ Tech Stack

- Python 3.x
- [PySide6](https://doc.qt.io/qtforpython/)
- [mutagen](https://mutagen.readthedocs.io/) (for ID3 tags)
- [tinytag](https://github.com/devsnd/tinytag) (for audio analysis)
- `ffprobe` (from FFmpeg, for detailed audio metadata)
- `bwfmetaedit` (for BWF-compliant `.wav` metadata editing)

---

## 🚫 What's not included

To respect the commercial scope of the project and protect client interests, the following are **excluded**:

- ❌ Any compiled executables (`.exe`, `.app`, `.dmg`)
- ❌ Commercial icons, branding or graphics
- ❌ Distribution-ready installers or assets

---

## 🧑‍💻 Author & Credits

This application was designed and built by **me** as part of a commissioned collaboration for a client in the audio industry, **GP Mastering**. The public version is intended as a **technical portfolio sample only**.

---

## 🎧 Contact for Commercial Use

This project was originally developed in collaboration with:

**GP Mastering – Audio Mastering Services**  
📍 Portugal  
🌐 [www.gpmastering.com](http://www.gpmastering.com)  
📩 [info@gpmastering.com](mailto:info@gpmastering.com)  
📱 [WhatsApp / Phone](https://wa.me/351967733683): +351 967 733 683  
📸 [Instagram – @gpmastering](https://instagram.com/gpmastering)

> For inquiries about licensing, branded versions, or commercial distribution of the software, please contact GP Mastering directly.

---

## 📎 Legal & License

This source code is provided under the MIT License, limited to this repository version.

> **Do not** use this codebase for redistribution or commercial purposes without explicit permission from the original author.

---

## 📸 Screenshots

_Add a few images or a GIF demo here if desired._

---

## 🎨 Note: A custom-branded user interface was included in the final commercial release, which is not part of this public repository.

---

## 📌 Roadmap (optional)

- [ ] Export metadata to CSV
- [ ] Support for FLAC and AIFF files
- [ ] Enhanced metadata batch editing capabilities
- [ ] File renaming presets and configuration saving
