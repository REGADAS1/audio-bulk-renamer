# tag_editor_wav.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from pathlib import Path
from metadata import get_wav_isrc, set_wav_isrc

class TagEditorWavDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit ISRC – {Path(file_path).name}")
        self.file_path = file_path

        layout = QVBoxLayout(self)

        # Campo ISRC
        self.isrc_edit = QLineEdit()
        self.isrc_edit.setText(get_wav_isrc(file_path))
        layout.addWidget(QLabel("ISRC:"))
        layout.addWidget(self.isrc_edit)

        # Botão de gravar
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_and_close)
        layout.addWidget(self.save_btn)

    def save_and_close(self):
        isrc = self.isrc_edit.text().strip()
        if not isrc:
            QMessageBox.warning(self, "Warning", "ISRC cannot be empty.")
            return

        success = set_wav_isrc(self.file_path, isrc)
        if success:
            QMessageBox.information(self, "Success", "ISRC updated successfully!")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to update ISRC.")
