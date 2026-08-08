from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from core.profile_editor import EditableWifiProfile, validate_personal_key


class ProfileEditDialog(QDialog):
    SECURITY_OPTIONS = (
        ("WPA2-Personal", "wpa2-personal"),
        ("WPA3-Personal", "wpa3-personal"),
        ("WPA-Personal", "wpa-personal"),
        ("Offenes WLAN", "open"),
    )

    SCOPE_OPTIONS = (
        ("Alle Benutzer", "all"),
        ("Nur aktueller Benutzer", "current"),
    )

    def __init__(
        self,
        *,
        title: str,
        profile: EditableWifiProfile | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._source_profile = profile
        self._is_edit_mode = profile is not None and profile.source_xml is not None

        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(620, 390)

        self.profile_name_edit = QLineEdit(self)
        self.ssid_edit = QLineEdit(self)

        self.security_combo = QComboBox(self)
        for label, value in self.SECURITY_OPTIONS:
            self.security_combo.addItem(label, value)

        self.scope_combo = QComboBox(self)
        for label, value in self.SCOPE_OPTIONS:
            self.scope_combo.addItem(label, value)

        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_note = QLabel(self)
        self.password_note.setWordWrap(True)

        self.show_password_checkbox = QCheckBox("Passwort anzeigen", self)
        self.autoconnect_checkbox = QCheckBox("Automatisch verbinden", self)
        self.hidden_checkbox = QCheckBox(
            "Verbinden, auch wenn die SSID nicht ausgestrahlt wird",
            self,
        )
        self.security_note = QLabel(self)
        self.security_note.setWordWrap(True)

        self.autoconnect_checkbox.setChecked(True)

        self.show_password_checkbox.toggled.connect(
            self._toggle_password
        )
        self.security_combo.currentIndexChanged.connect(
            self._update_password_state
        )

        form = QFormLayout()
        form.addRow("Profilname:", self.profile_name_edit)
        form.addRow("SSID:", self.ssid_edit)
        form.addRow("Sicherheit:", self.security_combo)
        form.addRow("", self.security_note)
        form.addRow("Passwort:", self.password_edit)
        form.addRow("", self.password_note)
        form.addRow("", self.show_password_checkbox)
        form.addRow("Gültigkeit:", self.scope_combo)
        form.addRow("", self.autoconnect_checkbox)
        form.addRow("", self.hidden_checkbox)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.buttons.button(
            QDialogButtonBox.StandardButton.Save
        ).setText("Speichern")

        self.buttons.accepted.connect(self._validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addStretch(1)
        layout.addWidget(self.buttons)

        if profile is not None:
            self._load_profile(profile)
        else:
            self.password_note.setText(
                "Für ein neues geschütztes WLAN ist ein Passwort erforderlich: "
                "8 bis 63 druckbare ASCII-Zeichen oder 64 hexadezimale Zeichen."
            )

        self._update_password_state()

    def _load_profile(self, profile: EditableWifiProfile) -> None:
        self.profile_name_edit.setText(profile.profile_name)
        self.ssid_edit.setText(profile.ssid)
        self.password_edit.setText(profile.password)

        if self._is_edit_mode and not profile.is_open:
            if profile.password:
                self.password_note.setText(
                    "Das vorhandene Passwort wurde aus Windows gelesen. "
                    "Lässt du das Feld leer, bleibt das bestehende Passwort unverändert."
                )
            else:
                self.password_note.setText(
                    "Das vorhandene Passwort konnte nicht im Klartext gelesen werden. "
                    "Feld leer lassen = bestehendes Passwort unverändert lassen. "
                    "Nur für eine Passwortänderung ein neues Passwort eingeben."
                )

        self.autoconnect_checkbox.setChecked(profile.autoconnect)
        self.hidden_checkbox.setChecked(profile.hidden)

        if self._is_edit_mode:
            label = profile.security_description or "Bestehende Windows-Konfiguration"
            self.security_combo.clear()
            self.security_combo.addItem(label, "existing")
            self.security_combo.setEnabled(False)
            self.security_note.setText(
                "Beim Bearbeiten bleibt die vorhandene Windows-Sicherheitskonfiguration "
                "unverändert; nur das Passwort und die allgemeinen Profileinstellungen "
                "werden angepasst."
            )
        else:
            self.security_note.clear()
            for index in range(self.security_combo.count()):
                if self.security_combo.itemData(index) == profile.security:
                    self.security_combo.setCurrentIndex(index)
                    break

        for index in range(self.scope_combo.count()):
            if self.scope_combo.itemData(index) == profile.scope:
                self.scope_combo.setCurrentIndex(index)
                break

        if self._is_edit_mode:
            self.scope_combo.setEnabled(False)

    def _toggle_password(self, checked: bool) -> None:
        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Normal
            if checked
            else QLineEdit.EchoMode.Password
        )

    def _update_password_state(self) -> None:
        if self._is_edit_mode and self._source_profile is not None:
            is_open = self._source_profile.is_open
        else:
            is_open = self.security_combo.currentData() == "open"

        self.password_edit.setEnabled(not is_open)
        self.show_password_checkbox.setEnabled(not is_open)

        if is_open:
            self.password_edit.clear()
            self.show_password_checkbox.setChecked(False)
            self.password_note.setText(
                "Offenes WLAN: Es wird kein Passwort gespeichert."
            )
        elif not self._is_edit_mode:
            self.password_note.setText(
                "Für ein neues geschütztes WLAN ist ein Passwort erforderlich: "
                "8 bis 63 druckbare ASCII-Zeichen oder 64 hexadezimale Zeichen."
            )

    def _validate_and_accept(self) -> None:
        profile_name = self.profile_name_edit.text().strip()
        ssid = self.ssid_edit.text().strip()
        password = self.password_edit.text()

        if not profile_name:
            QMessageBox.warning(
                self,
                "Profilname fehlt",
                "Bitte einen Profilnamen eingeben.",
            )
            return

        if not ssid:
            QMessageBox.warning(
                self,
                "SSID fehlt",
                "Bitte die SSID des WLANs eingeben.",
            )
            return

        if len(ssid.encode("utf-8")) > 32:
            QMessageBox.warning(
                self,
                "SSID zu lang",
                "Eine WLAN-SSID darf maximal 32 Byte lang sein.",
            )
            return

        if self._is_edit_mode and self._source_profile is not None:
            is_open = self._source_profile.is_open
        else:
            is_open = self.security_combo.currentData() == "open"

        if not is_open:
            # Bei bestehenden Profilen bedeutet ein leeres Feld:
            # vorhandenen Schlüssel unverändert lassen.
            must_validate = (not self._is_edit_mode) or bool(password)

            if must_validate:
                try:
                    validate_personal_key(password)
                except ValueError as exc:
                    QMessageBox.warning(
                        self,
                        "Ungültiges Passwort",
                        str(exc),
                    )
                    return

        self.accept()

    def profile(self) -> EditableWifiProfile:
        source = self._source_profile

        return EditableWifiProfile(
            profile_name=self.profile_name_edit.text().strip(),
            ssid=self.ssid_edit.text().strip(),
            security=(
                source.security
                if self._is_edit_mode and source is not None
                else str(self.security_combo.currentData())
            ),
            password=self.password_edit.text(),
            autoconnect=self.autoconnect_checkbox.isChecked(),
            hidden=self.hidden_checkbox.isChecked(),
            scope=(
                source.scope
                if self._is_edit_mode and source is not None
                else str(self.scope_combo.currentData())
            ),
            source_xml=source.source_xml if source is not None else None,
            security_description=(
                source.security_description if source is not None else ""
            ),
            is_open=source.is_open if source is not None else False,
        )
