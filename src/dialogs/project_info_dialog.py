from __future__ import annotations

import platform
import sys

from PySide6 import __version__ as pyside_version
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from utils.paths import log_dir
from utils.version import AppInfo


class ProjectInfoDialog(QDialog):
    """Technische Informationen für Support und Fehlersuche."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("WLAN-Manager – Projektinformationen")
        self.resize(620, 420)

        form = QFormLayout()
        form.addRow("Programm:", QLabel(AppInfo.NAME))
        form.addRow("Version:", QLabel(AppInfo.VERSION))
        form.addRow("Firma:", QLabel(AppInfo.COMPANY))
        form.addRow("Autor:", QLabel(AppInfo.AUTHOR))
        form.addRow("Python:", QLabel(platform.python_version()))
        form.addRow("PySide6:", QLabel(pyside_version))
        form.addRow("Windows:", QLabel(platform.platform()))
        form.addRow(
            "Betriebsart:",
            QLabel(
                "PyInstaller-EXE"
                if getattr(sys, "frozen", False)
                else "Entwicklungsumgebung"
            ),
        )
        form.addRow("Logverzeichnis:", QLabel(str(log_dir())))

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            self,
        )
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch(1)
        layout.addWidget(buttons)
