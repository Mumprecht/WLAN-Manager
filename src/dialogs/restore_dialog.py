from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from widgets.folder_selector import FolderSelector


class RestoreDialog(QDialog):
    """Auswahl einzelner oder mehrerer WLAN-XML-Dateien."""

    SETTINGS_ORGANIZATION = "Mumprecht Software"
    SETTINGS_APPLICATION = "WLAN-Manager"
    SETTINGS_KEY_SOURCE_FOLDER = "restore/source_folder"

    def __init__(
        self,
        default_source_folder: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(self.tr("WLAN-Profile wiederherstellen"))
        self.setModal(True)
        self.resize(820, 600)

        self._settings = QSettings(
            self.SETTINGS_ORGANIZATION,
            self.SETTINGS_APPLICATION,
        )

        saved_folder = self._settings.value(
            self.SETTINGS_KEY_SOURCE_FOLDER,
            str(default_source_folder),
            type=str,
        )

        saved_path = Path(saved_folder)
        if saved_path.exists() and saved_path.is_dir():
            initial_folder = saved_path
        else:
            initial_folder = Path(default_source_folder)
            self._settings.setValue(
                self.SETTINGS_KEY_SOURCE_FOLDER,
                str(initial_folder),
            )
            self._settings.sync()

        self.folder_selector = FolderSelector(
            initial_folder,
            self,
        )

        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText(self.tr("XML-Dateien suchen..."))

        self.table = QTableWidget(0, 2, self)
        self.table.setHorizontalHeaderLabels(
            [self.tr("Auswahl"), self.tr("XML-Datei")]
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
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

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.buttons.button(
            QDialogButtonBox.StandardButton.Ok
        ).setText(self.tr("Wiederherstellen"))

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(self.tr("Quellordner:"), self))
        layout.addWidget(self.folder_selector)
        layout.addWidget(self.search_edit)
        layout.addWidget(self.table, 1)
        layout.addLayout(button_row)
        layout.addWidget(self.status_label)
        layout.addWidget(self.buttons)

        self.folder_selector.path_edit.textChanged.connect(
            self._reload_files
        )
        self.search_edit.textChanged.connect(self._apply_filter)
        self.select_all_button.clicked.connect(self.select_all)
        self.select_none_button.clicked.connect(self.select_none)
        self.invert_button.clicked.connect(self.invert_selection)
        self.buttons.accepted.connect(self._validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        self._reload_files()

    def _reload_files(self) -> None:
        folder = self.folder_selector.path()
        files = (
            sorted(
                folder.glob("*.xml"),
                key=lambda path: path.name.casefold(),
            )
            if folder.exists() and folder.is_dir()
            else []
        )

        self.table.setRowCount(len(files))

        for row, path in enumerate(files):
            check_item = QTableWidgetItem("")
            check_item.setFlags(
                check_item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )
            check_item.setCheckState(Qt.CheckState.Checked)
            check_item.setData(
                Qt.ItemDataRole.UserRole,
                str(path),
            )

            self.table.setItem(row, 0, check_item)
            self.table.setItem(row, 1, QTableWidgetItem(path.name))

        self.table.resizeColumnsToContents()
        self._apply_filter(self.search_edit.text())
        self._update_status()

    def _apply_filter(self, text: str) -> None:
        needle = text.strip().casefold()

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            haystack = item.text().casefold() if item else ""

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

    def select_all(self) -> None:
        for row in self._visible_rows():
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(Qt.CheckState.Checked)

        self._update_status()

    def select_none(self) -> None:
        for row in self._visible_rows():
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(Qt.CheckState.Unchecked)

        self._update_status()

    def invert_selection(self) -> None:
        for row in self._visible_rows():
            item = self.table.item(row, 0)
            if not item:
                continue

            item.setCheckState(
                Qt.CheckState.Unchecked
                if item.checkState() == Qt.CheckState.Checked
                else Qt.CheckState.Checked
            )

        self._update_status()

    def selected_files(self) -> list[Path]:
        result: list[Path] = []

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if not item:
                continue

            if item.checkState() == Qt.CheckState.Checked:
                result.append(
                    Path(
                        str(
                            item.data(
                                Qt.ItemDataRole.UserRole
                            )
                        )
                    )
                )

        return result

    def _update_status(self) -> None:
        self.status_label.setText(
            self.tr("{selected} von {total} Datei(en) ausgewählt").format(
                selected=len(self.selected_files()),
                total=self.table.rowCount(),
            )
        )

    def _validate_and_accept(self) -> None:
        folder = self.folder_selector.path()

        if not folder.exists() or not folder.is_dir():
            QMessageBox.warning(
                self,
                self.tr("Quellordner nicht gefunden"),
                self.tr(
                    "Der Quellordner existiert nicht:\\n\\n{folder}"
                ).format(folder=folder),
            )
            return

        files = self.selected_files()

        if not files:
            QMessageBox.warning(
                self,
                self.tr("Keine Dateien ausgewählt"),
                self.tr("Bitte mindestens eine WLAN-XML-Datei auswählen."),
            )
            return

        self._settings.setValue(
            self.SETTINGS_KEY_SOURCE_FOLDER,
            str(folder),
        )
        self.accept()
