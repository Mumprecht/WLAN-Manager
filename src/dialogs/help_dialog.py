from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMessageBox,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from utils.paths import bundled_document


class HelpDialog(QDialog):
    """Integriertes Benutzerhandbuch."""

    HELP_FILE = "docs/Benutzerhandbuch.md"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("WLAN-Manager – Benutzerhandbuch")
        self.resize(900, 700)

        title = QLabel("<h2>WLAN-Manager – Benutzerhandbuch</h2>", self)

        self.browser = QTextBrowser(self)
        self.browser.setOpenExternalLinks(True)
        self.browser.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            self,
        )
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.browser, 1)
        layout.addWidget(buttons)

        self._load_help()

    def _load_help(self) -> None:
        path = bundled_document(self.HELP_FILE)

        if not path.exists():
            self.browser.setPlainText(
                "Das Benutzerhandbuch wurde nicht gefunden.\n\n"
                f"Erwarteter Pfad:\n{path}"
            )
            return

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Hilfe konnte nicht geladen werden",
                str(exc),
            )
            return

        self.browser.setMarkdown(content)
