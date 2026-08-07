from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


INVALID_FOLDER_CHARS = re.compile(r'[\\/:*?"<>|]')


class BackupDialog(QDialog):
    """Dialog zur Auswahl des Zielpfads für ein vollständiges WLAN-Backup."""

    SETTINGS_ORGANIZATION = "Mumprecht Software"
    SETTINGS_APPLICATION = "WLAN-Manager"
    SETTINGS_KEY_BASE_FOLDER = "backup/base_folder"

    def __init__(self, default_base_folder: Path, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("WLAN-Backup erstellen")
        self.setModal(True)
        self.resize(720, 260)

        self._settings = QSettings(
            self.SETTINGS_ORGANIZATION,
            self.SETTINGS_APPLICATION,
        )

        saved_folder = self._settings.value(
            self.SETTINGS_KEY_BASE_FOLDER,
            str(default_base_folder),
            type=str,
        )

        self.base_folder_edit = QLineEdit(saved_folder, self)
        self.folder_name_edit = QLineEdit(self)
        self.include_passwords_checkbox = QCheckBox(
            "WLAN-Passwörter mitsichern",
            self,
        )
        self.include_passwords_checkbox.setChecked(True)

        self.preview_label = QLabel(self)
        self.preview_label.setWordWrap(True)
        self.preview_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        browse_button = QPushButton("Durchsuchen...", self)
        browse_button.clicked.connect(self._browse_base_folder)

        folder_row = QHBoxLayout()
        folder_row.addWidget(self.base_folder_edit, 1)
        folder_row.addWidget(browse_button)

        form = QFormLayout()
        form.addRow("Zielordner:", folder_row)
        form.addRow("Ordnername:", self.folder_name_edit)
        form.addRow("", self.include_passwords_checkbox)
        form.addRow("Vollständiger Zielpfad:", self.preview_label)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )
        self.buttons.button(
            QDialogButtonBox.StandardButton.Save
        ).setText("Sichern")
        self.buttons.accepted.connect(self._validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addStretch(1)
        root.addWidget(self.buttons)

        self.base_folder_edit.textChanged.connect(self._update_preview)
        self.folder_name_edit.textChanged.connect(self._update_preview)
        self.include_passwords_checkbox.toggled.connect(
            self._refresh_suggested_folder_name
        )

        self._refresh_suggested_folder_name()

    def _browse_base_folder(self) -> None:
        current = self.base_folder_edit.text().strip()

        selected = QFileDialog.getExistingDirectory(
            self,
            "Zielordner auswählen",
            current,
            QFileDialog.Option.ShowDirsOnly,
        )

        if selected:
            self.base_folder_edit.setText(selected)

    def _suggested_folder_name(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        if self.include_passwords_checkbox.isChecked():
            suffix = "WLAN-Backup_mit_Passwoertern"
        else:
            suffix = "WLAN-Backup"

        return f"{timestamp}_{suffix}"

    def _refresh_suggested_folder_name(self) -> None:
        self.folder_name_edit.setText(self._suggested_folder_name())
        self.folder_name_edit.selectAll()
        self._update_preview()

    def _update_preview(self) -> None:
        base = self.base_folder_edit.text().strip()
        name = self.folder_name_edit.text().strip()

        if not base:
            self.preview_label.setText("<kein Zielordner ausgewählt>")
            return

        if not name:
            self.preview_label.setText(str(Path(base)))
            return

        self.preview_label.setText(str(Path(base) / name))

    def _validate_and_accept(self) -> None:
        base_text = self.base_folder_edit.text().strip()
        folder_name = self.folder_name_edit.text().strip()

        if not base_text:
            QMessageBox.warning(
                self,
                "Zielordner fehlt",
                "Bitte einen Zielordner auswählen.",
            )
            return

        base_folder = Path(base_text)

        if not base_folder.exists():
            QMessageBox.warning(
                self,
                "Zielordner nicht gefunden",
                f"Der Zielordner existiert nicht:\n\n{base_folder}",
            )
            return

        if not base_folder.is_dir():
            QMessageBox.warning(
                self,
                "Ungültiger Zielordner",
                f"Der angegebene Pfad ist kein Ordner:\n\n{base_folder}",
            )
            return

        if not folder_name:
            QMessageBox.warning(
                self,
                "Ordnername fehlt",
                "Bitte einen Namen für den Backup-Ordner eingeben.",
            )
            return

        if folder_name in {".", ".."}:
            QMessageBox.warning(
                self,
                "Ungültiger Ordnername",
                "Dieser Ordnername ist nicht zulässig.",
            )
            return

        if INVALID_FOLDER_CHARS.search(folder_name):
            QMessageBox.warning(
                self,
                "Ungültiger Ordnername",
                'Der Ordnername darf folgende Zeichen nicht enthalten:\n\n'
                r'\ / : * ? " < > |',
            )
            return

        if folder_name.endswith(" ") or folder_name.endswith("."):
            QMessageBox.warning(
                self,
                "Ungültiger Ordnername",
                "Ein Windows-Ordnername darf nicht mit einem Leerzeichen "
                "oder Punkt enden.",
            )
            return

        target = base_folder / folder_name

        if target.exists():
            answer = QMessageBox.question(
                self,
                "Zielordner existiert bereits",
                f"Der Zielordner existiert bereits:\n\n{target}\n\n"
                "Soll dieses Verzeichnis für das Backup verwendet werden?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if answer != QMessageBox.StandardButton.Yes:
                return

        self._settings.setValue(
            self.SETTINGS_KEY_BASE_FOLDER,
            str(base_folder),
        )

        self.accept()

    def target_folder(self) -> Path:
        return (
            Path(self.base_folder_edit.text().strip())
            / self.folder_name_edit.text().strip()
        )

    def include_passwords(self) -> bool:
        return self.include_passwords_checkbox.isChecked()
