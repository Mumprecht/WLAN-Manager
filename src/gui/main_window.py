from __future__ import annotations

import subprocess
from pathlib import Path

from PySide6.QtCore import QPoint, QSettings, Qt
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QTableWidgetItem,
)

from core.models import WlanProfile
from core.profile_editor import EditableWifiProfile
from core.wlan_manager import WlanManager
from dialogs.backup_dialog import BackupDialog
from dialogs.restore_dialog import RestoreDialog
from dialogs.overwrite_dialog import OverwriteDialog
from dialogs.delete_profiles_dialog import DeleteProfilesDialog
from dialogs.qr_code_dialog import QrCodeDialog
from dialogs.help_dialog import HelpDialog
from dialogs.project_info_dialog import ProjectInfoDialog
from dialogs.profile_edit_dialog import ProfileEditDialog
from gui.dialogs import confirm
from gui.widgets import ProfileTable
from utils.logger import configure_logging
from utils.version import AppInfo


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.log = configure_logging()
        self.manager = WlanManager()
        self._profiles: list[WlanProfile] = []

        self.settings = QSettings(
            "Mumprecht Software",
            "WLAN-Manager",
        )

        self.setWindowTitle(AppInfo.title())
        self.resize(1000, 650)

        self._build_actions()
        self._build_menu()
        self._build_toolbar()
        self._build_ui()
        self._build_statusbar()
        self._restore_window_settings()

        self.refresh_profiles()




    def _build_actions(self) -> None:
        self.action_refresh = QAction("Aktualisieren", self)
        self.action_refresh.setShortcut(QKeySequence("F5"))
        self.action_refresh.setStatusTip(
            "Gespeicherte WLAN-Profile neu einlesen"
        )
        self.action_refresh.triggered.connect(self.refresh_profiles)

        self.action_current_connection = QAction(
            "Aktuelle Verbindung",
            self,
        )
        self.action_current_connection.setShortcut(
            QKeySequence("Ctrl+I")
        )
        self.action_current_connection.setStatusTip(
            "Informationen zur aktuellen WLAN-Verbindung anzeigen"
        )
        self.action_current_connection.triggered.connect(
            self.show_current_connection
        )

        self.action_show_passwords = QAction(
            "Passwörter anzeigen",
            self,
        )
        self.action_show_passwords.setShortcut(
            QKeySequence("Ctrl+P")
        )
        self.action_show_passwords.setStatusTip(
            "Gespeicherte WLAN-Passwörter im Klartext anzeigen"
        )
        self.action_show_passwords.triggered.connect(
            self.show_passwords
        )

        self.action_connect = QAction("Verbinden", self)
        self.action_connect.setShortcut(QKeySequence("Ctrl+Enter"))
        self.action_connect.setStatusTip(
            "Mit dem ausgewählten gespeicherten WLAN-Profil verbinden"
        )
        self.action_connect.triggered.connect(
            self.connect_selected_profile
        )

        self.action_backup_profiles = QAction(
            "WLAN-Profile sichern...",
            self,
        )
        self.action_backup_profiles.setShortcut(
            QKeySequence("Ctrl+S")
        )
        self.action_backup_profiles.setStatusTip(
            "Ein, mehrere oder alle WLAN-Profile sichern"
        )
        self.action_backup_profiles.triggered.connect(
            self.backup_profiles
        )

        self.action_restore_profiles = QAction(
            "WLAN-Profile wiederherstellen...",
            self,
        )
        self.action_restore_profiles.setShortcut(
            QKeySequence("Ctrl+R")
        )
        self.action_restore_profiles.setStatusTip(
            "WLAN-Profile aus XML-Dateien wiederherstellen"
        )
        self.action_restore_profiles.triggered.connect(
            self.restore_profiles
        )

        self.action_export_csv = QAction("CSV exportieren...", self)
        self.action_export_csv.setShortcut(
            QKeySequence("Ctrl+Shift+S")
        )
        self.action_export_csv.setStatusTip(
            "WLAN-Profile als CSV-Datei exportieren"
        )
        self.action_export_csv.triggered.connect(
            self.export_profiles_csv
        )

        self.action_new_profile = QAction(
            "Neues WLAN-Profil...",
            self,
        )
        self.action_new_profile.setStatusTip(
            "Ein neues WLAN-Profil erstellen"
        )
        self.action_new_profile.triggered.connect(
            self.create_new_profile
        )

        self.action_edit_profile = QAction(
            "WLAN-Profil bearbeiten...",
            self,
        )
        self.action_edit_profile.setStatusTip(
            "Das ausgewählte WLAN-Profil bearbeiten"
        )
        self.action_edit_profile.triggered.connect(
            self.edit_selected_profile
        )

        self.action_delete_profiles = QAction(
            "WLAN-Profile löschen...",
            self,
        )
        self.action_delete_profiles.setShortcut(
            QKeySequence("Delete")
        )
        self.action_delete_profiles.setStatusTip(
            "Ein oder mehrere WLAN-Profile löschen"
        )
        self.action_delete_profiles.triggered.connect(
            self.delete_profiles
        )

        self.action_qr_code = QAction(
            "QR-Code anzeigen...",
            self,
        )
        self.action_qr_code.setStatusTip(
            "WLAN-Verbindungs-QR-Code für das ausgewählte Profil anzeigen"
        )
        self.action_qr_code.triggered.connect(
            self.show_selected_qr_code
        )

        self.action_help = QAction("Benutzerhandbuch", self)
        self.action_help.setShortcut(QKeySequence("F1"))
        self.action_help.setStatusTip(
            "Integriertes Benutzerhandbuch öffnen"
        )
        self.action_help.triggered.connect(self.show_help)

        self.action_project_info = QAction(
            "Projektinformationen",
            self,
        )
        self.action_project_info.setStatusTip(
            "Technische Informationen für Support und Fehlersuche anzeigen"
        )
        self.action_project_info.triggered.connect(
            self.show_project_info
        )

        self.action_about = QAction("Über WLAN-Manager", self)
        self.action_about.setStatusTip(
            "Programminformationen anzeigen"
        )
        self.action_about.triggered.connect(self.show_about)

        self.action_exit = QAction("Beenden", self)
        self.action_exit.setShortcut(QKeySequence("Ctrl+Q"))
        self.action_exit.setStatusTip("WLAN-Manager beenden")
        self.action_exit.triggered.connect(self.close)
    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("&Datei")
        file_menu.addAction(self.action_backup_profiles)
        file_menu.addAction(self.action_restore_profiles)
        file_menu.addSeparator()
        file_menu.addAction(self.action_export_csv)
        file_menu.addSeparator()
        file_menu.addAction(self.action_exit)

        wlan_menu = self.menuBar().addMenu("&WLAN")
        wlan_menu.addAction(self.action_refresh)
        wlan_menu.addAction(self.action_current_connection)
        wlan_menu.addAction(self.action_show_passwords)

        profile_menu = self.menuBar().addMenu("&Profile")
        profile_menu.addAction(self.action_new_profile)
        profile_menu.addAction(self.action_edit_profile)
        profile_menu.addSeparator()
        profile_menu.addAction(self.action_connect)
        profile_menu.addAction(self.action_qr_code)
        profile_menu.addSeparator()
        profile_menu.addAction(self.action_delete_profiles)

        help_menu = self.menuBar().addMenu("&Hilfe")
        help_menu.addAction(self.action_help)
        help_menu.addAction(self.action_project_info)
        help_menu.addSeparator()
        help_menu.addAction(self.action_about)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Hauptwerkzeuge", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(self.action_refresh)
        toolbar.addAction(self.action_current_connection)
        toolbar.addAction(self.action_show_passwords)
        toolbar.addSeparator()
        toolbar.addAction(self.action_delete_profiles)
    def _build_ui(self) -> None:
        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)

        self.table = ProfileTable(self)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.table.customContextMenuRequested.connect(
            self._show_profile_context_menu
        )
        self.table.cellDoubleClicked.connect(
            self._on_profile_double_clicked
        )
        self.table.horizontalHeader().sortIndicatorChanged.connect(
            self._remember_sorting
        )

        layout.addWidget(self.table)
        self.setCentralWidget(central)

    def _build_statusbar(self) -> None:
        status = QStatusBar(self)
        self.setStatusBar(status)

        self.profile_count_label = QLabel("0 WLAN-Profile", self)
        self.shortcut_hint_label = QLabel(
            "F5 Aktualisieren · Ctrl+S Sichern · Entf Löschen",
            self,
        )
        self.version_label = QLabel(f"Version {AppInfo.VERSION}", self)

        status.addWidget(self.profile_count_label)
        status.addWidget(self.shortcut_hint_label, 1)
        status.addPermanentWidget(self.version_label)


    def _restore_window_settings(self) -> None:
        geometry = self.settings.value("main_window/geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)

        state = self.settings.value("main_window/state")
        if state is not None:
            self.restoreState(state)

        header_state = self.settings.value("profile_table/header_state")
        if header_state is not None:
            self.table.horizontalHeader().restoreState(
                header_state
            )

        sort_column = self.settings.value(
            "profile_table/sort_column",
            0,
            type=int,
        )
        sort_order_value = self.settings.value(
            "profile_table/sort_order",
            int(Qt.SortOrder.AscendingOrder.value),
            type=int,
        )

        try:
            sort_order = Qt.SortOrder(sort_order_value)
        except ValueError:
            sort_order = Qt.SortOrder.AscendingOrder

        if 0 <= sort_column < self.table.columnCount():
            self.table.sortItems(sort_column, sort_order)

    def _save_window_settings(self) -> None:
        self.settings.setValue(
            "main_window/geometry",
            self.saveGeometry(),
        )
        self.settings.setValue(
            "main_window/state",
            self.saveState(),
        )
        self.settings.setValue(
            "profile_table/header_state",
            self.table.horizontalHeader().saveState(),
        )

        header = self.table.horizontalHeader()
        self.settings.setValue(
            "profile_table/sort_column",
            header.sortIndicatorSection(),
        )
        self.settings.setValue(
            "profile_table/sort_order",
            header.sortIndicatorOrder().value,
        )

        self.settings.sync()

    def _remember_sorting(
        self,
        logical_index: int,
        order: Qt.SortOrder,
    ) -> None:
        self.settings.setValue(
            "profile_table/sort_column",
            logical_index,
        )
        self.settings.setValue(
            "profile_table/sort_order",
            order.value,
        )

    def _selected_profile(self) -> WlanProfile | None:
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.information(
                self,
                "Kein Profil ausgewählt",
                "Bitte zuerst ein WLAN-Profil in der Tabelle auswählen.",
            )
            return None

        item = self.table.item(row, 0)
        if item is None:
            return None

        ssid = item.text()
        for profile in self._profiles:
            if profile.ssid == ssid:
                return profile

        return None

    def _show_exception(self, title: str, exception: Exception) -> None:
        self.log.exception(title)
        QMessageBox.critical(self, title, str(exception))
        self.statusBar().showMessage(f"Fehler: {exception}", 8000)

    def refresh_profiles(self) -> None:
        try:
            self.statusBar().showMessage("WLAN-Profile werden gelesen …")

            profiles = self.manager.profiles()
            self._profiles = profiles

            self.table.setSortingEnabled(False)
            self.table.setRowCount(len(profiles))

            for row_index, profile in enumerate(profiles):
                values = [
                    profile.ssid,
                    profile.authentication,
                    "••••••••" if profile.has_password else profile.password,
                ]

                for column, value in enumerate(values):
                    self.table.setItem(row_index, column, QTableWidgetItem(value))

            if self.settings.value(
                "profile_table/header_state"
            ) is None:
                self.table.resizeColumnsToContents()

            self.table.setSortingEnabled(True)

            sort_column = self.settings.value(
                "profile_table/sort_column",
                0,
                type=int,
            )
            sort_order_value = self.settings.value(
                "profile_table/sort_order",
                int(Qt.SortOrder.AscendingOrder.value),
                type=int,
            )
            try:
                sort_order = Qt.SortOrder(sort_order_value)
            except ValueError:
                sort_order = Qt.SortOrder.AscendingOrder

            if 0 <= sort_column < self.table.columnCount():
                self.table.sortItems(sort_column, sort_order)

            self.profile_count_label.setText(
                f"{len(profiles)} WLAN-Profil(e)"
            )
            self.statusBar().showMessage("Bereit", 2500)

        except Exception as exc:
            self._profiles = []
            self.table.setRowCount(0)
            self.profile_count_label.setText("0 WLAN-Profile")
            self._show_exception("Profile konnten nicht gelesen werden", exc)

    def show_passwords(self) -> None:
        if not self._profiles:
            QMessageBox.information(
                self, "Keine Profile", "Es sind keine WLAN-Profile vorhanden."
            )
            return

        if not confirm(
            self,
            "Passwörter anzeigen",
            "Die WLAN-Passwörter werden im Klartext angezeigt.\n\nFortfahren?",
            warning=True,
        ):
            return

        passwords = {profile.ssid: profile.password for profile in self._profiles}

        for row_index in range(self.table.rowCount()):
            ssid_item = self.table.item(row_index, 0)
            if ssid_item:
                self.table.setItem(
                    row_index,
                    2,
                    QTableWidgetItem(passwords.get(ssid_item.text(), "<nicht auslesbar>")),
                )

        self.statusBar().showMessage(
            "Passwörter werden im Klartext angezeigt.", 5000
        )

    def show_selected_password(self) -> None:
        profile = self._selected_profile()
        if not profile:
            return

        QMessageBox.information(
            self,
            f"Passwort – {profile.ssid}",
            f"WLAN-Profil: {profile.ssid}\n\nPasswort: {profile.password}",
        )

    def connect_selected_profile(self) -> None:
        profile = self._selected_profile()
        if not profile:
            return

        try:
            self.manager.connect_profile(profile.ssid)
            self.statusBar().showMessage(
                f"Verbindungsanforderung für '{profile.ssid}' wurde gesendet.",
                5000,
            )
        except Exception as exc:
            self._show_exception("Verbindung fehlgeschlagen", exc)


    def delete_profiles(
        self,
        preselected_ssid: str | None = None,
    ) -> None:
        if not self._profiles:
            QMessageBox.information(
                self,
                "Keine Profile",
                "Es sind keine WLAN-Profile vorhanden.",
            )
            return

        dialog = DeleteProfilesDialog(
            profiles=self._profiles,
            parent=self,
        )

        if preselected_ssid:
            for row in range(
                dialog.profile_selector.table.rowCount()
            ):
                item = dialog.profile_selector.table.item(row, 0)
                if not item:
                    continue

                ssid = str(
                    item.data(Qt.ItemDataRole.UserRole)
                )

                item.setCheckState(
                    Qt.CheckState.Checked
                    if ssid == preselected_ssid
                    else Qt.CheckState.Unchecked
                )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        profiles = dialog.selected_profiles()
        names = [profile.ssid for profile in profiles]

        detail_lines = "\n".join(
            f"• {name}" for name in names[:15]
        )

        if len(names) > 15:
            detail_lines += (
                f"\n• ... und {len(names) - 15} weitere"
            )

        answer = QMessageBox.warning(
            self,
            "WLAN-Profile wirklich löschen?",
            f"Es werden {len(names)} WLAN-Profil(e) gelöscht:\n\n"
            f"{detail_lines}\n\n"
            "Dabei werden auch die gespeicherten WLAN-Passwörter entfernt.\n"
            "Dieser Vorgang kann nicht rückgängig gemacht werden.",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        successful, failed = self.manager.delete_selected(
            names
        )

        message = (
            f"Ausgewählt: {len(names)}\n"
            f"Erfolgreich gelöscht: {len(successful)}\n"
            f"Fehlgeschlagen: {len(failed)}"
        )

        if failed:
            message += "\n\n" + "\n".join(
                f"{name}: {error}"
                for name, error in failed
            )

            QMessageBox.warning(
                self,
                "Löschen abgeschlossen",
                message,
            )
        else:
            QMessageBox.information(
                self,
                "Löschen abgeschlossen",
                message,
            )

        self.refresh_profiles()

    def delete_selected_profile_via_dialog(self) -> None:
        profile = self._selected_profile()
        if not profile:
            return

        self.delete_profiles(
            preselected_ssid=profile.ssid
        )



    def create_new_profile(self) -> None:
        dialog = ProfileEditDialog(
            title="Neues WLAN-Profil erstellen",
            parent=self,
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        profile = dialog.profile()

        if any(
            existing.ssid == profile.profile_name
            for existing in self._profiles
        ):
            QMessageBox.warning(
                self,
                "Profil bereits vorhanden",
                f"Ein WLAN-Profil mit dem Namen '{profile.profile_name}' "
                "ist bereits vorhanden.\n\n"
                "Bitte verwende für dieses Profil die Funktion "
                "'WLAN-Profil bearbeiten...'.",
            )
            return

        try:
            self.manager.create_profile(profile)
            QMessageBox.information(
                self,
                "WLAN-Profil gespeichert",
                f"Das WLAN-Profil '{profile.profile_name}' wurde gespeichert.",
            )
            self.refresh_profiles()
        except Exception as exc:
            self._show_exception(
                "WLAN-Profil konnte nicht gespeichert werden",
                exc,
            )

    def edit_selected_profile(self) -> None:
        selected = self._selected_profile()
        if not selected:
            return

        try:
            editable = self.manager.load_profile_for_edit(
                selected.ssid
            )
        except Exception as exc:
            self._show_exception(
                "WLAN-Profil konnte nicht für die Bearbeitung geladen werden",
                exc,
            )
            return

        dialog = ProfileEditDialog(
            title=f"WLAN-Profil bearbeiten – {selected.ssid}",
            profile=editable,
            parent=self,
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        updated = dialog.profile()

        try:
            self.manager.replace_profile(
                selected.ssid,
                updated,
            )
            QMessageBox.information(
                self,
                "WLAN-Profil gespeichert",
                f"Das WLAN-Profil '{updated.profile_name}' wurde aktualisiert.",
            )
            self.refresh_profiles()
        except Exception as exc:
            self._show_exception(
                "WLAN-Profil konnte nicht aktualisiert werden",
                exc,
            )


    def backup_profiles(
        self,
        preselected_ssid: str | None = None,
    ) -> None:
        if not self._profiles:
            QMessageBox.information(
                self,
                "Keine Profile",
                "Es sind keine WLAN-Profile vorhanden.",
            )
            return

        dialog = BackupDialog(
            profiles=self._profiles,
            default_base_folder=self.manager.downloads_folder(),
            parent=self,
        )

        if preselected_ssid:
            for row in range(
                dialog.profile_selector.table.rowCount()
            ):
                item = dialog.profile_selector.table.item(row, 0)
                if not item:
                    continue

                ssid = str(
                    item.data(Qt.ItemDataRole.UserRole)
                )

                item.setCheckState(
                    Qt.CheckState.Checked
                    if ssid == preselected_ssid
                    else Qt.CheckState.Unchecked
                )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        profiles = dialog.selected_profiles()
        target = dialog.target_folder()
        include_password = dialog.include_passwords()

        try:
            target.mkdir(parents=True, exist_ok=True)

            successful: list[str] = []
            skipped: list[str] = []
            failed: list[tuple[str, str]] = []

            remembered_action: str | None = None

            for profile in profiles:
                existing = self.manager.existing_export_file(
                    profile.ssid,
                    target,
                )

                action = None

                if existing is not None:
                    if remembered_action is not None:
                        action = remembered_action
                    else:
                        conflict_dialog = OverwriteDialog(
                            profile_name=profile.ssid,
                            filename=existing.name,
                            parent=self,
                        )

                        conflict_dialog.exec()
                        decision = conflict_dialog.decision()
                        action = decision.action

                        if (
                            decision.apply_to_all
                            and action
                            in {
                                OverwriteDialog.ACTION_OVERWRITE,
                                OverwriteDialog.ACTION_SKIP,
                            }
                        ):
                            remembered_action = action

                    if action == OverwriteDialog.ACTION_CANCEL:
                        break

                    if action == OverwriteDialog.ACTION_SKIP:
                        skipped.append(profile.ssid)
                        continue

                try:
                    if existing is not None:
                        self.manager.export_profile_overwrite(
                            profile.ssid,
                            target,
                            include_password,
                        )
                    else:
                        self.manager.export_profile(
                            profile.ssid,
                            target,
                            include_password,
                        )

                    successful.append(profile.ssid)

                except Exception as exc:
                    failed.append(
                        (profile.ssid, str(exc))
                    )

            message = (
                f"Zielordner:\n{target}\n\n"
                f"Ausgewählt: {len(profiles)}\n"
                f"Erfolgreich: {len(successful)}\n"
                f"Übersprungen: {len(skipped)}\n"
                f"Fehlgeschlagen: {len(failed)}"
            )

            if failed:
                message += "\n\n" + "\n".join(
                    f"{name}: {error}"
                    for name, error in failed
                )

            if failed:
                QMessageBox.warning(
                    self,
                    "Sicherung abgeschlossen",
                    message,
                )
            else:
                QMessageBox.information(
                    self,
                    "Sicherung abgeschlossen",
                    message,
                )

        except Exception as exc:
            self._show_exception(
                "Sicherung fehlgeschlagen",
                exc,
            )
    def backup_selected_profile(self) -> None:
        profile = self._selected_profile()
        if not profile:
            return

        self.backup_profiles(
            preselected_ssid=profile.ssid
        )

    def restore_profiles(self) -> None:
        dialog = RestoreDialog(
            default_source_folder=self.manager.downloads_folder(),
            parent=self,
        )

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        files = dialog.selected_files()

        try:
            successful, failed = self.manager.import_selected(
                files
            )

            message = (
                f"Ausgewählt: {len(files)}\n"
                f"Erfolgreich: {len(successful)}\n"
                f"Fehlgeschlagen: {len(failed)}"
            )

            if failed:
                message += "\n\n" + "\n".join(
                    f"{name}: {error}"
                    for name, error in failed
                )
                QMessageBox.warning(
                    self,
                    "Wiederherstellung abgeschlossen",
                    message,
                )
            else:
                QMessageBox.information(
                    self,
                    "Wiederherstellung abgeschlossen",
                    message,
                )

            self.refresh_profiles()

        except Exception as exc:
            self._show_exception(
                "Wiederherstellung fehlgeschlagen",
                exc,
            )

    def export_profiles_csv(self) -> None:
        default_path = self.manager.default_csv_path()

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "CSV-Datei speichern",
            str(default_path),
            "CSV-Dateien (*.csv)",
        )

        if not filename:
            return

        path = Path(filename)
        if path.suffix.lower() != ".csv":
            path = path.with_suffix(".csv")

        if not confirm(
            self,
            "CSV-Export",
            "Die CSV-Datei enthält vorhandene WLAN-Passwörter im Klartext.\n\nFortfahren?",
            warning=True,
        ):
            return

        try:
            count = self.manager.export_csv(path)
            QMessageBox.information(
                self,
                "CSV-Export erfolgreich",
                f"Datei:\n{path}\n\nAnzahl Profile: {count}",
            )
        except Exception as exc:
            self._show_exception("CSV-Export fehlgeschlagen", exc)

    def show_current_connection(self) -> None:
        try:
            connection = self.manager.current_connection()

            if not connection.ssid:
                QMessageBox.information(
                    self,
                    "Aktuelle WLAN-Verbindung",
                    "Der Computer ist aktuell mit keinem WLAN verbunden.",
                )
                return

            values = [
                ("Schnittstelle", connection.interface),
                ("Status", connection.status),
                ("SSID", connection.ssid),
                ("BSSID", connection.bssid),
                ("Funktyp", connection.radio_type),
                ("Authentifizierung", connection.authentication),
                ("Verschlüsselung", connection.cipher),
                ("Kanal", connection.channel),
                ("Empfangsrate", connection.receive_rate),
                ("Senderate", connection.transmit_rate),
                ("Signal", connection.signal),
            ]

            text = "\n".join(
                f"{label}: {value}" for label, value in values if value
            )

            QMessageBox.information(
                self, "Aktuelle WLAN-Verbindung", text
            )

        except PermissionError as exc:
            answer = QMessageBox.warning(
                self,
                "Standortberechtigung fehlt",
                f"{exc}\n\nStandorteinstellungen jetzt öffnen?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )

            if answer == QMessageBox.StandardButton.Yes:
                subprocess.Popen(
                    ["start", "ms-settings:privacy-location"],
                    shell=True,
                )

        except Exception as exc:
            self._show_exception(
                "WLAN-Verbindung konnte nicht gelesen werden", exc
            )

    def _show_profile_context_menu(self, position: QPoint) -> None:
        index = self.table.indexAt(position)
        if not index.isValid():
            return

        # Die angeklickte Zelle wird zur aktuellen Zelle.
        # Profilbezogene Aktionen verwenden weiterhin die Zeile dieser Zelle.
        self.table.setCurrentCell(
            index.row(),
            index.column(),
        )

        menu = QMenu(self)
        menu.addAction(self.action_edit_profile)

        copy_action = menu.addAction("Kopieren")
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.setShortcutVisibleInContextMenu(True)

        def copy_cell() -> None:
            item = self.table.item(
                index.row(),
                index.column(),
            )
            if item is not None:
                QApplication.clipboard().setText(item.text())

        copy_action.triggered.connect(copy_cell)

        menu.addSeparator()
        menu.addAction(self.action_connect)
        menu.addAction(self.action_qr_code)
        menu.addSeparator()

        show_password_action = menu.addAction("Passwort anzeigen")
        show_password_action.triggered.connect(self.show_selected_password)

        menu.addSeparator()

        backup_action = menu.addAction("Profil sichern...")
        backup_action.triggered.connect(
            self.backup_selected_profile
        )

        menu.addSeparator()
        delete_action = menu.addAction("Profil löschen...")
        delete_action.triggered.connect(
            self.delete_selected_profile_via_dialog
        )

        menu.exec(self.table.viewport().mapToGlobal(position))

    def _on_profile_double_clicked(self, row: int, column: int) -> None:
        del row, column
        self.connect_selected_profile()



    def show_selected_qr_code(self) -> None:
        profile = self._selected_profile()
        if not profile:
            return

        try:
            dialog = QrCodeDialog(
                profile=profile,
                default_folder=self.manager.downloads_folder(),
                parent=self,
            )
            dialog.exec()
        except Exception as exc:
            self._show_exception(
                "QR-Code konnte nicht erzeugt werden",
                exc,
            )


    def show_help(self) -> None:
        dialog = HelpDialog(self)
        dialog.exec()

    def show_project_info(self) -> None:
        dialog = ProjectInfoDialog(self)
        dialog.exec()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._save_window_settings()
        super().closeEvent(event)

    def show_about(self) -> None:
        QMessageBox.about(
            self,
            "Über WLAN-Manager",
            AppInfo.about(),
        )
