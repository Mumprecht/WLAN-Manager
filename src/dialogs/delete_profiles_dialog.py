from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from core.models import WlanProfile
from widgets.profile_selection_widget import ProfileSelectionWidget


class DeleteProfilesDialog(QDialog):
    """Mehrfachauswahl für das Löschen gespeicherter WLAN-Profile."""

    def __init__(
        self,
        profiles: list[WlanProfile],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(self.tr("WLAN-Profile löschen"))
        self.setModal(True)
        self.resize(760, 560)

        self.profile_selector = ProfileSelectionWidget(
            profiles,
            self,
        )

        warning_label = QLabel(
            self.tr("Wähle ein oder mehrere WLAN-Profile aus, die gelöscht werden sollen."),
            self,
        )
        warning_label.setWordWrap(True)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.buttons.button(
            QDialogButtonBox.StandardButton.Ok
        ).setText(self.tr("Löschen"))

        layout = QVBoxLayout(self)
        layout.addWidget(warning_label)
        layout.addWidget(self.profile_selector, 1)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self._validate_and_accept)
        self.buttons.rejected.connect(self.reject)

    def _validate_and_accept(self) -> None:
        if not self.profile_selector.selected_profiles():
            QMessageBox.warning(
                self,
                self.tr("Keine Profile ausgewählt"),
                self.tr("Bitte mindestens ein WLAN-Profil zum Löschen auswählen."),
            )
            return

        self.accept()

    def selected_profiles(self) -> list[WlanProfile]:
        return self.profile_selector.selected_profiles()
