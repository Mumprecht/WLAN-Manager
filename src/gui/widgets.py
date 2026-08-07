from __future__ import annotations

from PySide6.QtWidgets import QTableWidget


class ProfileTable(QTableWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(0, 3, parent)
        self.setHorizontalHeaderLabels(
            ["WLAN-Profil", "Authentifizierung", "Passwort"]
        )
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
