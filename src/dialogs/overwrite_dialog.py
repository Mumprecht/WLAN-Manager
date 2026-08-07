from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


@dataclass(slots=True)
class OverwriteDecision:
    action: str
    apply_to_all: bool = False


class OverwriteDialog(QDialog):
    """Entscheidung bei bereits vorhandener Exportdatei."""

    ACTION_OVERWRITE = "overwrite"
    ACTION_SKIP = "skip"
    ACTION_CANCEL = "cancel"

    def __init__(
        self,
        profile_name: str,
        filename: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("Datei bereits vorhanden")
        self.setModal(True)
        self.resize(560, 220)

        self._decision = OverwriteDecision(
            action=self.ACTION_CANCEL,
            apply_to_all=False,
        )

        message = QLabel(
            f"Für das WLAN-Profil\n\n"
            f"{profile_name}\n\n"
            f"existiert im Zielordner bereits die Datei:\n\n"
            f"{filename}\n\n"
            f"Wie soll verfahren werden?",
            self,
        )
        message.setWordWrap(True)

        self.apply_to_all_checkbox = QCheckBox(
            "Diese Auswahl für alle weiteren Konflikte übernehmen",
            self,
        )

        self.overwrite_button = QPushButton("Überschreiben", self)
        self.skip_button = QPushButton("Überspringen", self)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        button_box.button(
            QDialogButtonBox.StandardButton.Cancel
        ).setText("Abbrechen")

        self.overwrite_button.clicked.connect(
            lambda: self._finish(self.ACTION_OVERWRITE)
        )
        self.skip_button.clicked.connect(
            lambda: self._finish(self.ACTION_SKIP)
        )
        button_box.rejected.connect(
            lambda: self._finish(self.ACTION_CANCEL)
        )

        layout = QVBoxLayout(self)
        layout.addWidget(message)
        layout.addWidget(self.apply_to_all_checkbox)
        layout.addStretch(1)
        layout.addWidget(self.overwrite_button)
        layout.addWidget(self.skip_button)
        layout.addWidget(button_box)

    def _finish(self, action: str) -> None:
        self._decision = OverwriteDecision(
            action=action,
            apply_to_all=self.apply_to_all_checkbox.isChecked(),
        )

        if action == self.ACTION_CANCEL:
            self.reject()
        else:
            self.accept()

    def decision(self) -> OverwriteDecision:
        return self._decision
