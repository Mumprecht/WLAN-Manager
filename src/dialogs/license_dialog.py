from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
)


class LicenseDialog(QDialog):
    """Zeigt die vollständigen Lizenzbedingungen des WLAN-Managers."""

    def __init__(
        self,
        license_path: Path,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(self.tr("Lizenz"))
        self.resize(860, 680)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel(
            "WLAN-Manager Non-Commercial License, Version 1.0",
            self,
        )
        title_font = QFont(title.font())
        title_font.setBold(True)
        title_font.setPointSize(title_font.pointSize() + 1)
        title.setFont(title_font)

        layout.addWidget(title)

        text_edit = QPlainTextEdit(self)
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.WidgetWidth
        )

        try:
            license_text = license_path.read_text(encoding="utf-8")
        except OSError as exc:
            license_text = (
                self.tr("Die Lizenzdatei konnte nicht gelesen werden.\n\n{error}").format(error=exc)
            )

        text_edit.setPlainText(license_text)
        layout.addWidget(text_edit, 1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            parent=self,
        )
        buttons.rejected.connect(self.reject)
        buttons.clicked.connect(self.accept)

        layout.addWidget(buttons)
