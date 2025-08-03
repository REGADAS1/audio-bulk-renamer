from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel, QLineEdit, QMessageBox
from pathlib import Path
from metadata import get_file_metadata
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TSRC

class TagEditorDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit ID3 Tags - {Path(file_path).name}")
        self.file_path = file_path

        form_layout = QFormLayout(self)

        info = get_file_metadata(file_path)

        self.title_edit = QLineEdit(info.get("title", "") or "")
        self.artist_edit = QLineEdit(info.get("artist", "") or "")
        self.album_edit = QLineEdit(info.get("album", "") or "")
        self.year_edit = QLineEdit(info.get("year", "") or "")
        self.genre_edit = QLineEdit(info.get("genre", "") or "")
        track_val = info.get("track", "") or ""
        if "/" in track_val:
            track_val = track_val.split("/")[0]
        self.track_edit = QLineEdit(track_val)
        self.isrc_edit = QLineEdit(info.get("isrc", "") or "")

        form_layout.addRow("Title:", self.title_edit)
        form_layout.addRow("Artist:", self.artist_edit)
        form_layout.addRow("Album:", self.album_edit)
        form_layout.addRow("Year:", self.year_edit)
        form_layout.addRow("Genre:", self.genre_edit)
        form_layout.addRow("Track:", self.track_edit)
        form_layout.addRow("ISRC Code:", self.isrc_edit)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form_layout.addWidget(btn_box)
        btn_box.accepted.connect(self.save_and_close)
        btn_box.rejected.connect(self.reject)

    def save_and_close(self):
        try:
            audio = EasyID3(self.file_path)
            audio['title'] = self.title_edit.text().strip()
            audio['artist'] = self.artist_edit.text().strip()
            audio['album'] = self.album_edit.text().strip()
            audio['date'] = self.year_edit.text().strip()
            audio['genre'] = self.genre_edit.text().strip()
            audio['tracknumber'] = self.track_edit.text().strip()
            audio.save()

            id3 = ID3(self.file_path)
            isrc_text = self.isrc_edit.text().strip()
            if isrc_text:
                id3.add(TSRC(encoding=3, text=isrc_text))
            else:
                if 'TSRC' in id3:
                    del id3['TSRC']
            id3.save()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error saving tags: {e}")
            return
        else:
            QMessageBox.information(self, "Success", "ID3 tags updated successfully!")
            self.accept()
