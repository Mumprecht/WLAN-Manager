from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from core.models import WlanProfile
from widgets.folder_selector import FolderSelector
from widgets.profile_selection_widget import ProfileSelectionWidget


INVALID_FOLDER_CHARS = re.compile(r'[\\/:*?"<>|]')


class BackupDialog(QDialog):
    """Mehrfachauswahl und Zielsteuerung für WLAN-Backups."""

    SETTINGS_ORGANIZATION = "Mumprecht Software"
    SETTINGS_APPLICATION = "WLAN-Manager"
    SETTINGS_KEY_BASE_FOLDER = "backup/base_folder"

    def __init__(
        self,
        profiles: list[WlanProfile],
        default_base_folder: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("WLAN-Profile sichern")
        self.setModal(True)
        self.resize(820, 650)

        self._settings = QSettings(
            self.SETTINGS_ORGANIZATION,
            self.SETTINGS_APPLICATION,
        )

        saved_folder = self._settings.value(
            self.SETTINGS_KEY_BASE_FOLDER,
            str(default_base_folder),
            type=str,
        )

        self.profile_selector = ProfileSelectionWidget(
            profiles,
            self,
        )

        self.folder_selector = FolderSelector(
            Path(saved_folder),
            self,
        )

        self.create_subfolder_checkbox = QCheckBox(
            "Neuen Backup-Unterordner mit Datum/Uhrzeit erzeugen",
            self,
        )
        self.create_subfolder_checkbox.setChecked(True)

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

        form = QFormLayout()
        form.addRow("Zielordner:", self.folder_selector)
        form.addRow("", self.create_subfolder_checkbox)
        form.addRow("Unterordner:", self.folder_name_edit)
        form.addRow("", self.include_passwords_checkbox)
        form.addRow("Vollständiger Zielpfad:", self.preview_label)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.buttons.button(
            QDialogButtonBox.StandardButton.Save
        ).setText("Sichern")

        root = QVBoxLayout(self)
        root.addWidget(QLabel("Zu sichernde WLAN-Profile:", self))
        root.addWidget(self.profile_selector, 1)
        root.addLayout(form)
        root.addWidget(self.buttons)

        self.buttons.accepted.connect(self._validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        self.folder_selector.path_edit.textChanged.connect(
            self._update_preview
        )
        self.folder_name_edit.textChanged.connect(
            self._update_preview
        )
        self.create_subfolder_checkbox.toggled.connect(
            self._on_subfolder_toggled
        )
        self.include_passwords_checkbox.toggled.connect(
            self._refresh_suggested_folder_name
        )

        self._refresh_suggested_folder_name()
        self._on_subfolder_toggled(True)

    def _suggested_folder_name(self) -> str:
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        if self.include_passwords_checkbox.isChecked():
            suffix = "WLAN-Backup_mit_Passwoertern"
        else:
            suffix = "WLAN-Backup"

        return f"{stamp}_{suffix}"

    def _refresh_suggested_folder_name(self) -> None:
        if self.create_subfolder_checkbox.isChecked():
            self.folder_name_edit.setText(
                self._suggested_folder_name()
            )
            self.folder_name_edit.selectAll()

        self._update_preview()

    def _on_subfolder_toggled(self, checked: bool) -> None:
        self.folder_name_edit.setEnabled(checked)

        if checked and not self.folder_name_edit.text().strip():
            self.folder_name_edit.setText(
                self._suggested_folder_name()
            )

        self._update_preview()

    def _update_preview(self) -> None:
        base_text = self.folder_selector.path_edit.text().strip()

        if not base_text:
            self.preview_label.setText(
                "<kein Zielordner ausgewählt>"
            )
            return

        base = Path(base_text)

        if self.create_subfolder_checkbox.isChecked():
            name = self.folder_name_edit.text().strip()
            target = base / name if name else base
        else:
            target = base

        self.preview_label.setText(str(target))

    def _validate_and_accept(self) -> None:
        if not self.profile_selector.selected_profiles():
            QMessageBox.warning(
                self,
                "Keine Profile ausgewählt",
                "Bitte mindestens ein WLAN-Profil auswählen.",
            )
            return

        base = self.folder_selector.path()

        if not str(base).strip():
            QMessageBox.warning(
                self,
                "Zielordner fehlt",
                "Bitte einen Zielordner auswählen.",
            )
            return

        if not base.exists() or not base.is_dir():
            QMessageBox.warning(
                self,
                "Zielordner nicht gefunden",
                f"Der Zielordner existiert nicht:\n\n{base}",
            )
            return

        if self.create_subfolder_checkbox.isChecked():
            name = self.folder_name_edit.text().strip()

            if not name:
                QMessageBox.warning(
                    self,
                    "Unterordner fehlt",
                    "Bitte einen Namen für den Backup-Unterordner eingeben.",
                )
                return

            if name in {".", ".."} or INVALID_FOLDER_CHARS.search(name):
                QMessageBox.warning(
                    self,
                    "Ungültiger Ordnername",
                    'Der Ordnername darf folgende Zeichen nicht enthalten:\n\n'
                    r'\ / : * ? " < > |',
                )
                return

            if name.endswith(" ") or name.endswith("."):
                QMessageBox.warning(
                    self,
                    "Ungültiger Ordnername",
                    "Der Ordnername darf nicht mit einem Leerzeichen "
                    "oder Punkt enden.",
                )
                return

        self._settings.setValue(
            self.SETTINGS_KEY_BASE_FOLDER,
            str(base),
        )
        self.accept()

    def selected_profiles(self) -> list[WlanProfile]:
        return self.profile_selector.selected_profiles()

    def include_passwords(self) -> bool:
        return self.include_passwords_checkbox.isChecked()

    def target_folder(self) -> Path:
        base = self.folder_selector.path()

        if self.create_subfolder_checkbox.isChecked():
            return base / self.folder_name_edit.text().strip()

        return base
