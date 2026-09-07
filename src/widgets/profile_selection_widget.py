from __future__ import annotations

from collections.abc import Iterable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.models import WlanProfile
from core.profile_display import authentication_display_text


class ProfileSelectionWidget(QWidget):
    """Wiederverwendbare Mehrfachauswahl für WLAN-Profile."""

    def __init__(
        self,
        profiles: Iterable[WlanProfile],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._profiles = list(profiles)

        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText(self.tr("Profile suchen..."))

        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(
            [self.tr("Auswahl"), self.tr("WLAN-Profil"), self.tr("Authentifizierung")]
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setSortingEnabled(False)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.select_all_button = QPushButton(self.tr("Alle auswählen"), self)
        self.select_none_button = QPushButton(self.tr("Keine auswählen"), self)
        self.invert_button = QPushButton(self.tr("Invertieren"), self)

        self.status_label = QLabel(self)

        button_row = QHBoxLayout()
        button_row.addWidget(self.select_all_button)
        button_row.addWidget(self.select_none_button)
        button_row.addWidget(self.invert_button)
        button_row.addStretch(1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search_edit)
        layout.addWidget(self.table)
        layout.addLayout(button_row)
        layout.addWidget(self.status_label)

        self.search_edit.textChanged.connect(self._apply_filter)
        self.select_all_button.clicked.connect(self.select_all)
        self.select_none_button.clicked.connect(self.select_none)
        self.invert_button.clicked.connect(self.invert_selection)

        self._populate()

    def _populate(self) -> None:
        self.table.setRowCount(len(self._profiles))

        for row, profile in enumerate(self._profiles):
            check_item = QTableWidgetItem("")
            check_item.setFlags(
                check_item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )
            check_item.setCheckState(Qt.CheckState.Checked)
            check_item.setData(
                Qt.ItemDataRole.UserRole,
                profile.ssid,
            )

            name_item = QTableWidgetItem(profile.ssid)
            auth_item = QTableWidgetItem(
                authentication_display_text(profile)
            )

            self.table.setItem(row, 0, check_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, auth_item)

        self.table.resizeColumnsToContents()
        self._update_status()

    def _apply_filter(self, text: str) -> None:
        needle = text.strip().casefold()

        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 1)
            auth_item = self.table.item(row, 2)

            haystack = " ".join(
                [
                    name_item.text() if name_item else "",
                    auth_item.text() if auth_item else "",
                ]
            ).casefold()

            self.table.setRowHidden(
                row,
                bool(needle) and needle not in haystack,
            )

        self._update_status()

    def _visible_rows(self) -> list[int]:
        return [
            row
            for row in range(self.table.rowCount())
            if not self.table.isRowHidden(row)
        ]

    def _set_visible_check_state(
        self,
        state: Qt.CheckState,
    ) -> None:
        for row in self._visible_rows():
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(state)

        self._update_status()

    def select_all(self) -> None:
        self._set_visible_check_state(Qt.CheckState.Checked)

    def select_none(self) -> None:
        self._set_visible_check_state(Qt.CheckState.Unchecked)

    def invert_selection(self) -> None:
        for row in self._visible_rows():
            item = self.table.item(row, 0)
            if not item:
                continue

            new_state = (
                Qt.CheckState.Unchecked
                if item.checkState() == Qt.CheckState.Checked
                else Qt.CheckState.Checked
            )
            item.setCheckState(new_state)

        self._update_status()

    def selected_profiles(self) -> list[WlanProfile]:
        names: set[str] = set()

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                names.add(str(item.data(Qt.ItemDataRole.UserRole)))

        return [
            profile
            for profile in self._profiles
            if profile.ssid in names
        ]

    def selected_count(self) -> int:
        return len(self.selected_profiles())

    def _update_status(self) -> None:
        total = len(self._profiles)
        selected = self.selected_count()
        visible = len(self._visible_rows())

        if visible == total:
            self.status_label.setText(
                self.tr("{selected} von {total} Profil(en) ausgewählt").format(
                    selected=selected,
                    total=total,
                )
            )
        else:
            self.status_label.setText(
                self.tr(
                    "{selected} von {total} Profil(en) ausgewählt · {visible} sichtbar"
                ).format(
                    selected=selected,
                    total=total,
                    visible=visible,
                )
            )
