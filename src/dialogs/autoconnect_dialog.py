from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.models import AutoconnectProfile
from core.wlan_manager import WlanManager


class AutoconnectDialog(QDialog):
    """Verwaltet Autoconnect und Priorität gespeicherter WLAN-Profile."""

    def __init__(
        self,
        manager: WlanManager,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.manager = manager
        self._profiles: list[AutoconnectProfile] = []

        self.setWindowTitle(
            self.tr("Automatische WLAN-Verbindungen verwalten")
        )
        self.setModal(True)
        self.resize(820, 620)

        info_label = QLabel(
            self.tr(
                "Die Reihenfolge bestimmt die WLAN-Priorität. "
                "Priorität 1 ist die höchste. Änderungen werden "
                "sofort in Windows gespeichert."
            ),
            self,
        )
        info_label.setWordWrap(True)

        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(
            [
                self.tr("Priorität"),
                self.tr("WLAN-Profil"),
                self.tr("Automatisch verbinden"),
            ]
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)

        # Gleiche Auswahlfarben wie in der Haupttabelle.
        self.table.setStyleSheet(
            """
            QTableWidget::item:selected {
                background-color: #CFE8FF;
                color: #202020;
            }

            QTableWidget::item:selected:active {
                background-color: #B9DCFA;
                color: #202020;
            }

            QTableWidget::item:selected:!active {
                background-color: #DCECF7;
                color: #202020;
            }
            """
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents,
        )
        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch,
        )
        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self.move_up_button = QPushButton(
            self.tr("Nach oben"),
            self,
        )
        self.move_down_button = QPushButton(
            self.tr("Nach unten"),
            self,
        )
        self.autoconnect_button = QPushButton(
            self.tr("Autoconnect ändern"),
            self,
        )
        self.refresh_button = QPushButton(
            self.tr("Aktualisieren"),
            self,
        )

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.move_up_button)
        action_layout.addWidget(self.move_down_button)
        action_layout.addWidget(self.autoconnect_button)
        action_layout.addStretch(1)
        action_layout.addWidget(self.refresh_button)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            self,
        )
        self.buttons.button(
            QDialogButtonBox.StandardButton.Close
        ).setText(
            self.tr("Schliessen")
        )

        layout = QVBoxLayout(self)
        layout.addWidget(info_label)
        layout.addWidget(self.table, 1)
        layout.addLayout(action_layout)
        layout.addWidget(self.buttons)

        self.table.itemSelectionChanged.connect(
            self._update_buttons
        )
        self.move_up_button.clicked.connect(
            self._move_up
        )
        self.move_down_button.clicked.connect(
            self._move_down
        )
        self.autoconnect_button.clicked.connect(
            self._toggle_autoconnect
        )
        self.refresh_button.clicked.connect(
            self._refresh
        )
        self.buttons.rejected.connect(self.reject)

        self._refresh()

    def _selected_profile(
        self,
    ) -> AutoconnectProfile | None:
        row = self.table.currentRow()

        if row < 0 or row >= len(self._profiles):
            return None

        return self._profiles[row]

    def _refresh(
        self,
        selected_profile_name: str | None = None,
    ) -> None:
        if selected_profile_name is None:
            selected = self._selected_profile()
            if selected is not None:
                selected_profile_name = selected.profile_name

        try:
            profiles = self.manager.autoconnect_profiles()
        except Exception as exc:
            self._profiles = []
            self.table.setRowCount(0)
            self._update_buttons()

            QMessageBox.critical(
                self,
                self.tr(
                    "WLAN-Profile konnten nicht gelesen werden"
                ),
                str(exc),
            )
            return

        self._profiles = profiles

        self.table.setRowCount(len(profiles))

        selected_row = -1

        for row, profile in enumerate(profiles):
            priority = (
                str(profile.priority)
                if profile.priority is not None
                else "-"
            )

            values = [
                priority,
                profile.profile_name,
                self.tr("Ja")
                if profile.autoconnect
                else self.tr("Nein"),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)

                if column == 0:
                    item.setTextAlignment(
                        int(
                            Qt.AlignmentFlag.AlignCenter
                            | Qt.AlignmentFlag.AlignVCenter
                        )
                    )

                self.table.setItem(
                    row,
                    column,
                    item,
                )

            if profile.profile_name == selected_profile_name:
                selected_row = row

        if selected_row >= 0:
            self.table.selectRow(selected_row)
            self.table.setCurrentCell(
                selected_row,
                1,
            )
        elif profiles:
            self.table.selectRow(0)
            self.table.setCurrentCell(
                0,
                1,
            )

        self._update_buttons()

    def _update_buttons(self) -> None:
        profile = self._selected_profile()

        if profile is None:
            self.move_up_button.setEnabled(False)
            self.move_down_button.setEnabled(False)
            self.autoconnect_button.setEnabled(False)
            return

        priority = profile.priority

        self.move_up_button.setEnabled(
            priority is not None
            and priority > 1
        )
        self.move_down_button.setEnabled(
            priority is not None
            and priority < len(self._profiles)
        )
        self.autoconnect_button.setEnabled(True)

    def _move_up(self) -> None:
        profile = self._selected_profile()

        if (
            profile is None
            or profile.priority is None
            or profile.priority <= 1
        ):
            return

        try:
            self.manager.set_profile_priority(
                profile.profile_name,
                profile.priority - 1,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr(
                    "WLAN-Priorität konnte nicht geändert werden"
                ),
                str(exc),
            )
            return

        self._refresh(profile.profile_name)

    def _move_down(self) -> None:
        profile = self._selected_profile()

        if (
            profile is None
            or profile.priority is None
            or profile.priority >= len(self._profiles)
        ):
            return

        try:
            self.manager.set_profile_priority(
                profile.profile_name,
                profile.priority + 1,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr(
                    "WLAN-Priorität konnte nicht geändert werden"
                ),
                str(exc),
            )
            return

        self._refresh(profile.profile_name)

    def _toggle_autoconnect(self) -> None:
        profile = self._selected_profile()

        if profile is None:
            return

        try:
            self.manager.set_profile_autoconnect(
                profile.profile_name,
                not profile.autoconnect,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr(
                    "Autoconnect konnte nicht geändert werden"
                ),
                str(exc),
            )
            return

        self._refresh(profile.profile_name)
