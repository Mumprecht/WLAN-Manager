from __future__ import annotations

from io import BytesIO

import segno
from segno import helpers

from core.models import WlanProfile


class WifiQrError(ValueError):
    """Das WLAN-Profil kann nicht als Verbindungs-QR-Code dargestellt werden."""


NO_PASSWORD_VALUES = {
    "",
    "<nicht auslesbar>",
    "<Fehler beim Auslesen>",
}

OPEN_NETWORK_VALUES = {
    "<offenes WLAN – kein Passwort>",
}


def _qr_security(profile: WlanProfile) -> tuple[str | None, str | None]:
    """
    Übersetzt die Windows-Authentifizierung in das WLAN-QR-Format.

    Segno unterstützt für WLAN-QR-Codes WEP, WPA und ungeschützte Netze.
    WPA2/WPA3-Personal werden deshalb als WPA codiert.
    Enterprise-Profile werden bewusst nicht unterstützt.
    """
    authentication = (profile.authentication or "").strip().casefold()
    password = profile.password or ""

    if "enterprise" in authentication:
        raise WifiQrError(
            "WLAN-QR-Codes für Enterprise-Profile werden derzeit nicht unterstützt."
        )

    if (
        password in OPEN_NETWORK_VALUES
        or "open" in authentication
        or "offen" in authentication
    ):
        return "nopass", None

    if password in NO_PASSWORD_VALUES:
        raise WifiQrError(
            "Für dieses geschützte WLAN ist kein auslesbares Passwort vorhanden."
        )

    if "wep" in authentication:
        return "WEP", password

    if any(
        token in authentication
        for token in (
            "wpa",
            "wpa2",
            "wpa3",
            "personal",
            "psk",
            "sae",
        )
    ):
        return "WPA", password

    if password:
        # Windows kann je nach Sprache / Adapter leicht abweichende
        # Authentifizierungsbezeichnungen liefern. Bei vorhandenem Passwort
        # verwenden wir WPA als konservativen Fallback.
        return "WPA", password

    raise WifiQrError(
        "Der Sicherheitstyp dieses WLAN-Profils kann nicht bestimmt werden."
    )


def wifi_qr_data(profile: WlanProfile) -> str:
    """Erzeugt den standardisierten WIFI:-Text für das Profil."""
    security, password = _qr_security(profile)

    return helpers.make_wifi_data(
        ssid=profile.ssid,
        password=password,
        security=security,
        hidden=False,
    )


def wifi_qr_code(profile: WlanProfile) -> segno.QRCode:
    """Erzeugt einen normalen QR-Code (kein Micro-QR-Code)."""
    data = wifi_qr_data(profile)
    return segno.make_qr(data, error="M")


def wifi_qr_png_bytes(
    profile: WlanProfile,
    *,
    scale: int = 10,
    border: int = 4,
) -> bytes:
    """Rendert den WLAN-QR-Code als PNG in den Speicher."""
    qr = wifi_qr_code(profile)
    buffer = BytesIO()
    qr.save(
        buffer,
        kind="png",
        scale=scale,
        border=border,
    )
    return buffer.getvalue()


def save_wifi_qr_png(
    profile: WlanProfile,
    filename: str,
    *,
    scale: int = 10,
    border: int = 4,
) -> None:
    """Speichert den QR-Code als PNG-Datei."""
    qr = wifi_qr_code(profile)
    qr.save(
        filename,
        kind="png",
        scale=scale,
        border=border,
    )
