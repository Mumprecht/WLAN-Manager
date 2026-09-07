from __future__ import annotations

from PySide6.QtCore import QCoreApplication

from core.models import CurrentConnection, WlanProfile


def authentication_display_text(profile: WlanProfile) -> str:
    """Liefert die lokalisierte Anzeige der Authentifizierung."""

    authentication = (profile.authentication or "").strip()

    if authentication.casefold() in {"open", "offen"}:
        return QCoreApplication.translate(
            "ProfileDisplay",
            "Offen",
        )

    return authentication


def password_display_text(profile: WlanProfile) -> str:
    """Liefert die lokalisierte Anzeige eines Passwort-Sonderwerts."""

    if profile.password == "<nicht auslesbar>":
        return QCoreApplication.translate(
            "ProfileDisplay",
            "<nicht auslesbar>",
        )

    if profile.password == "<Fehler beim Auslesen>":
        return QCoreApplication.translate(
            "ProfileDisplay",
            "<Fehler beim Auslesen>",
        )

    if profile.password == "<offenes WLAN – kein Passwort>":
        return QCoreApplication.translate(
            "ProfileDisplay",
            "<offenes WLAN – kein Passwort>",
        )

    return profile.password


def current_connection_status_display_text(
    connection: CurrentConnection,
) -> str:
    """Liefert den lokalisierten Verbindungsstatus."""

    status = (connection.status or "").strip()
    normalized = status.casefold()

    if normalized in {"connected", "verbunden"}:
        return QCoreApplication.translate(
            "ProfileDisplay",
            "Verbunden",
        )

    if normalized in {"disconnected", "getrennt"}:
        return QCoreApplication.translate(
            "ProfileDisplay",
            "Getrennt",
        )

    return status


def current_connection_authentication_display_text(
    connection: CurrentConnection,
) -> str:
    """Liefert die lokalisierte Authentifizierung der Verbindung."""

    authentication = (connection.authentication or "").strip()

    if authentication.casefold() in {"open", "offen"}:
        return QCoreApplication.translate(
            "ProfileDisplay",
            "Offen",
        )

    return authentication
