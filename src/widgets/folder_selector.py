from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)


class FolderSelector(QWidget):
    """Einheitliche Auswahl eines Basisordners."""

    def __init__(
        self,
        initial_folder: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.path_edit = QLineEdit(str(initial_folder), self)
        self.browse_button = QPushButton("Durchsuchen...", self)
        self.browse_button.clicked.connect(self._browse)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.path_edit, 1)
        layout.addWidget(self.browse_button)

    def _browse(self) -> None:
        selected = QFileDialog.getExistingDirectory(
            self,
            "Ordner auswählen",
            self.path_edit.text().strip(),
            QFileDialog.Option.ShowDirsOnly,
        )

        if selected:
            self.path_edit.setText(selected)

    def path(self) -> Path:
        return Path(self.path_edit.text().strip())
