from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QGroupBox, QGridLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QHeaderView, QFormLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError, TSRC
import renamer
from metadata import get_file_metadata


def format_duration(seconds_str):
    try:
        seconds = float(seconds_str)
    except Exception:
        return "00:00:000"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes:02}:{secs:02}:{millis:03}"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Namae – GP Mastering")
        self.setWindowIcon(QIcon("GP_icon.ico"))
        self.resize(900, 600)
        self.setAcceptDrops(True)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "", "File", "New File Name Preview",
            "File Type", "Sample Rate", "Bit Depth",
            "Bitrate", "Length", "Channels"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setColumnWidth(0, 30)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        for i in range(3, 9):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        main_layout.addWidget(self.table)

        # Layout de opções e contacto
        options_container = QHBoxLayout()
        main_layout.addLayout(options_container)

        # Opções de renomeação
        options_group = QGroupBox("Rename Files")
        options_layout = QGridLayout()
        options_group.setLayout(options_layout)

        self.prefix_edit = QLineEdit()
        self.suffix_edit = QLineEdit()
        self.find_edit = QLineEdit()
        self.replace_edit = QLineEdit()

        options_layout.addWidget(QLabel("Before:"), 0, 0)
        options_layout.addWidget(self.prefix_edit, 0, 1)
        options_layout.addWidget(QLabel("After:"), 1, 0)
        options_layout.addWidget(self.suffix_edit, 1, 1)
        options_layout.addWidget(QLabel("Find:"), 2, 0)
        options_layout.addWidget(self.find_edit, 2, 1)
        options_layout.addWidget(QLabel("Replace with:"), 3, 0)
        options_layout.addWidget(self.replace_edit, 3, 1)

        options_container.addWidget(options_group, stretch=3)

        # Contacto
        contact_group = QGroupBox("Contact info")
        contact_layout = QFormLayout()
        contact_group.setLayout(contact_layout)

        name_label = QLabel("<b>GP Mastering</b>")
        phone_label = QLabel('<a href="https://wa.me/351967733683">+351 967 733 683</a>')
        phone_label.setOpenExternalLinks(True)
        site_label = QLabel('<a href="http://www.gpmastering.com">www.gpmastering.com</a>')
        site_label.setOpenExternalLinks(True)
        insta_label = QLabel('<a href="https://instagram.com/gpmastering">@gpmastering</a>')
        insta_label.setOpenExternalLinks(True)

        contact_layout.addRow(name_label)
        contact_layout.addRow("WhatsApp:", phone_label)
        contact_layout.addRow("Website:", site_label)
        contact_layout.addRow("Instagram:", insta_label)

        options_container.addWidget(contact_group, stretch=2)

        # Botões
        btn_layout = QHBoxLayout()
        self.rename_btn = QPushButton("Rename Files")
        self.tag_btn = QPushButton("Edit Metadata")
        self.tag_btn.setEnabled(False)
        btn_layout.addWidget(self.rename_btn)
        btn_layout.addWidget(self.tag_btn)
        main_layout.addLayout(btn_layout)

        self.rename_btn.clicked.connect(self.perform_rename)
        self.tag_btn.clicked.connect(self.open_tag_editor)

        for edit in (self.prefix_edit, self.suffix_edit, self.find_edit, self.replace_edit):
            edit.textChanged.connect(self.update_preview_names)

        self.files = []
        self.selected_file = None
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.cellClicked.connect(self.remove_file_click)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            self.add_files(file_paths)

    def add_files(self, file_paths):
        for file_path in file_paths:
            if file_path in self.files:
                continue
            self.files.append(file_path)
            row = self.table.rowCount()
            self.table.insertRow(row)

            info = get_file_metadata(file_path)

            remove_item = QTableWidgetItem("❌")
            remove_item.setTextAlignment(Qt.AlignCenter)
            remove_item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(row, 0, remove_item)

            file_item = QTableWidgetItem(Path(file_path).name)
            file_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 1, file_item)

            self.table.setItem(row, 2, QTableWidgetItem(""))  # pré-visualização

            self.table.setItem(row, 3, QTableWidgetItem(info.get("format", "")))
            self.table.setItem(row, 4, QTableWidgetItem(str(info.get("samplerate", ""))))
            self.table.setItem(row, 5, QTableWidgetItem(str(info.get("bitdepth", ""))))
            self.table.setItem(row, 6, QTableWidgetItem(str(info.get("bitrate", ""))))
            self.table.setItem(row, 7, QTableWidgetItem(info.get("duration", "")))
            self.table.setItem(row, 8, QTableWidgetItem(str(info.get("channels", ""))))

        self.update_preview_names()

    def update_preview_names(self):
        prefix = self.prefix_edit.text()
        suffix = self.suffix_edit.text()
        find_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        for idx, file_path in enumerate(self.files):
            new_name = renamer.generate_new_name(file_path, prefix, suffix, find_text, replace_text)
            self.table.setItem(idx, 2, QTableWidgetItem(new_name))

    def perform_rename(self):
        prefix = self.prefix_edit.text()
        suffix = self.suffix_edit.text()
        find_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        result = renamer.rename_files(self.files, prefix, suffix, find_text, replace_text)
        renamed_count = len(result)
        if renamed_count == 0:
            QMessageBox.information(self, "Renaming", "No files were renamed.")
        else:
            for i, old_path in enumerate(list(self.files)):
                new_path = old_path
                for r in result:
                    if Path(r).name == Path(old_path).name:
                        new_path = r
                        break
                self.files[i] = new_path
                self.table.setItem(i, 1, QTableWidgetItem(Path(new_path).name))
            QMessageBox.information(self, "Renaming", f"{renamed_count} file(s) renamed.")

    def on_selection_changed(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.files):
            self.selected_file = None
            self.tag_btn.setEnabled(False)
        else:
            self.selected_file = self.files[row]
            self.tag_btn.setEnabled(
                self.selected_file.lower().endswith(".mp3") or self.selected_file.lower().endswith(".wav")
            )

    def open_tag_editor(self):
        from tag_editor import TagEditorDialog
        if self.selected_file:
            dialog = TagEditorDialog(self.selected_file, self)
            dialog.exec()

    def remove_file_click(self, row, col):
        if col == 0:
            self.files.pop(row)
            self.table.removeRow(row)

    def on_cell_double_clicked(self, row, col):
        if 0 <= row < len(self.files):
            self.selected_file = self.files[row]
            self.open_tag_editor()
