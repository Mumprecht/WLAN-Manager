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

from utils.language import get_language
from utils.paths import bundled_document


class HelpDialog(QDialog):
    """Integriertes Benutzerhandbuch."""

    HELP_FILES = {
        "de": "docs/Benutzerhandbuch.md",
        "en": "docs/Benutzerhandbuch_en.md",
        "fr": "docs/Benutzerhandbuch_fr.md",
        "it": "docs/Benutzerhandbuch_it.md",
    }

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle(self.tr("WLAN-Manager – Benutzerhandbuch"))
        self.resize(900, 700)

        title = QLabel(self.tr("<h2>WLAN-Manager – Benutzerhandbuch</h2>"), self)

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
        language = get_language()
        relative_path = self.HELP_FILES.get(language, self.HELP_FILES["de"])
        path = bundled_document(relative_path)

        if not path.exists():
            self.browser.setPlainText(
                self.tr("Das Benutzerhandbuch wurde nicht gefunden.\n\nErwarteter Pfad:\n{path}").format(path=path)
            )
            return

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr("Hilfe konnte nicht geladen werden"),
                str(exc),
            )
            return

        self.browser.setMarkdown(content)
