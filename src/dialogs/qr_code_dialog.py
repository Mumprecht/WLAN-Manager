from __future__ import annotations

import re
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.models import WlanProfile
from core.profile_display import (
    authentication_display_text,
    password_display_text,
)
from core.qr_code import (
    WifiQrError,
    save_wifi_qr_png,
    wifi_qr_png_bytes,
)


def _safe_filename(value: str) -> str:
    value = re.sub(r'[\\/:*?"<>|]', "_", value).strip()
    return value or "WLAN"


class QrCodeDialog(QDialog):
    """Zeigt den WLAN-Verbindungs-QR-Code eines gespeicherten Profils."""

    def __init__(
        self,
        profile: WlanProfile,
        default_folder: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.profile = profile
        self.default_folder = default_folder
        self._pixmap = QPixmap()

        self.setWindowTitle(
            self.tr("WLAN-QR-Code – {ssid}").format(ssid=profile.ssid)
        )
        self.setModal(True)
        self.resize(520, 680)

        self.qr_label = QLabel(self)
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setMinimumSize(380, 380)

        self.ssid_edit = QLineEdit(profile.ssid, self)
        self.ssid_edit.setReadOnly(True)

        self.authentication_edit = QLineEdit(
            authentication_display_text(profile),
            self,
        )
        self.authentication_edit.setReadOnly(True)

        self.password_edit = QLineEdit(
            password_display_text(profile),
            self,
        )
        self.password_edit.setReadOnly(True)
        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.show_password_checkbox = QCheckBox(
            self.tr("Passwort anzeigen"),
            self,
        )
        self.show_password_checkbox.toggled.connect(
            self._toggle_password
        )

        form = QFormLayout()
        form.addRow(self.tr("SSID:"), self.ssid_edit)
        form.addRow(
            self.tr("Authentifizierung:"),
            self.authentication_edit,
        )
        form.addRow(self.tr("Passwort:"), self.password_edit)
        form.addRow("", self.show_password_checkbox)

        self.save_button = QPushButton(
            self.tr("QR-Code als PNG speichern..."),
            self,
        )
        self.copy_button = QPushButton(
            self.tr("QR-Code in Zwischenablage kopieren"),
            self,
        )

        self.save_button.clicked.connect(self._save_png)
        self.copy_button.clicked.connect(self._copy_to_clipboard)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            self,
        )
        buttons.rejected.connect(self.reject)

        note = QLabel(
            self.tr(
                "Den QR-Code mit der Kamera bzw. WLAN-Funktion eines "
                "Smartphones oder Tablets scannen."
            ),
            self,
        )
        note.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.qr_label, 1)
        layout.addWidget(note)
        layout.addLayout(form)
        layout.addWidget(self.save_button)
        layout.addWidget(self.copy_button)
        layout.addWidget(buttons)

        self._create_qr_code()

    def _create_qr_code(self) -> None:
        try:
            png_data = wifi_qr_png_bytes(
                self.profile,
                scale=10,
                border=4,
            )
        except WifiQrError:
            raise
        except Exception as exc:
            raise WifiQrError(
                self.tr("Der QR-Code konnte nicht erzeugt werden: {error}").format(error=exc)
            ) from exc

        pixmap = QPixmap()
        if not pixmap.loadFromData(png_data, "PNG"):
            raise WifiQrError(
                self.tr("Der erzeugte QR-Code konnte nicht als Bild geladen werden.")
            )

        self._pixmap = pixmap
        self.qr_label.setPixmap(
            pixmap.scaled(
                380,
                380,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def _toggle_password(self, checked: bool) -> None:
        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Normal
            if checked
            else QLineEdit.EchoMode.Password
        )

    def _save_png(self) -> None:
        suggested = (
            self.default_folder
            / f"{_safe_filename(self.profile.ssid)}_WLAN-QR-Code.png"
        )

        filename, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("WLAN-QR-Code speichern"),
            str(suggested),
            self.tr("PNG-Bild (*.png)"),
        )

        if not filename:
            return

        path = Path(filename)
        if path.suffix.lower() != ".png":
            path = path.with_suffix(".png")

        try:
            save_wifi_qr_png(
                self.profile,
                str(path),
                scale=10,
                border=4,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr("Speichern fehlgeschlagen"),
                str(exc),
            )
            return

        QMessageBox.information(
            self,
            self.tr("QR-Code gespeichert"),
            self.tr("Der QR-Code wurde gespeichert:\n\n{path}").format(path=path),
        )

    def _copy_to_clipboard(self) -> None:
        if self._pixmap.isNull():
            QMessageBox.warning(
                self,
                self.tr("QR-Code nicht verfügbar"),
                self.tr("Es ist kein QR-Code zum Kopieren vorhanden."),
            )
            return

        clipboard = QGuiApplication.clipboard()
        clipboard.setPixmap(self._pixmap)

        QMessageBox.information(
            self,
            self.tr("QR-Code kopiert"),
            self.tr("Der QR-Code wurde als Bild in die Zwischenablage kopiert."),
        )
