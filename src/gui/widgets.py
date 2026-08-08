from __future__ import annotations

from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QApplication, QTableWidget


class ProfileTable(QTableWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(0, 3, parent)

        self.setHorizontalHeaderLabels(
            ["WLAN-Profil", "Authentifizierung", "Passwort"]
        )

        # Einzelne oder mehrere Zellen können markiert werden.
        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectItems
        )
        self.setSelectionMode(
            QTableWidget.SelectionMode.ExtendedSelection
        )

        # Tabelle bleibt schreibgeschützt.
        self.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)

        # Farben für Tabellenkopf, Mauszeiger und Auswahl.
        self.setStyleSheet(
            """
            QHeaderView::section {
                background-color: #D9EAF7;
                color: #1F1F1F;
                padding: 6px;
                border: 1px solid #B7C9D6;
                font-weight: 600;
            }

            QTableWidget::item:hover {
                background-color: #E8F3FC;
                color: #202020;
            }

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

    def keyPressEvent(self, event) -> None:
        """Ermöglicht Ctrl+C für ausgewählte Tabellenzellen."""

        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selected_cells()
            return

        super().keyPressEvent(event)

    def copy_selected_cells(self) -> None:
        """Kopiert ausgewählte Zellen tabellarisch in die Zwischenablage."""

        indexes = self.selectedIndexes()

        if not indexes:
            return

        indexes = sorted(
            indexes,
            key=lambda index: (
                index.row(),
                index.column(),
            ),
        )

        rows: dict[int, dict[int, str]] = {}

        for index in indexes:
            item = self.item(
                index.row(),
                index.column(),
            )

            value = item.text() if item else ""

            rows.setdefault(
                index.row(),
                {},
            )[index.column()] = value

        min_column = min(
            index.column()
            for index in indexes
        )

        max_column = max(
            index.column()
            for index in indexes
        )

        lines: list[str] = []

        for row_number in sorted(rows):
            values = [
                rows[row_number].get(
                    column,
                    "",
                )
                for column in range(
                    min_column,
                    max_column + 1,
                )
            ]

            lines.append("\t".join(values))

        QApplication.clipboard().setText(
            "\n".join(lines)
        )