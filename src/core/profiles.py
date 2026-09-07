from __future__ import annotations

import re

from PySide6.QtCore import QCoreApplication

from core.models import CurrentConnection, WlanProfile
from core.netsh import (
    NetshError,
    looks_like_location_permission_error,
    looks_like_missing_wireless_interface,
    require_success,
    run_netsh,
)
from core.wlan_native import (
    NativeWifiError,
    delete_profile as delete_profile_native,
)



def get_profile_names(
    preserve_order: bool = False,
) -> list[str]:
    result = run_netsh(["wlan", "show", "profiles"])
    text = result.combined

    if looks_like_missing_wireless_interface(text):
        raise NetshError(
            QCoreApplication.translate("Profiles", "Es wurde keine verfügbare WLAN-Schnittstelle gefunden.\n\n{details}").format(details=text)
        )

    profiles: list[str] = []

    for line in text.splitlines():
        match = re.match(r"^\s{4,}[^:]+:\s*(.+?)\s*$", line)
        if not match:
            continue

        name = match.group(1).strip()
        if name and not re.fullmatch(r"<.*>", name):
            profiles.append(name)

    unique = list(dict.fromkeys(profiles))

    if preserve_order:
        return unique

    unique = sorted(unique, key=str.casefold)
    if not unique:
        return []

    if result.returncode != 0:
        raise NetshError(
            QCoreApplication.translate("Profiles", "Die WLAN-Profile konnten nicht gelesen werden.\n\n{details}").format(details=text)
        )

    return unique


def get_profile_details(ssid: str) -> WlanProfile:
    result = run_netsh(["wlan", "show", "profile", f"name={ssid}", "key=clear"])

    if result.returncode != 0:
        raise NetshError(
            QCoreApplication.translate("Profiles", "Das WLAN-Profil '{ssid}' konnte nicht gelesen werden.\n\n{details}").format(
                ssid=ssid, details=result.combined
            )
        )

    authentication = "-"
    password = "<nicht auslesbar>"
    security_key: str | None = None

    for line in result.combined.splitlines():
        if authentication == "-":
            match = re.match(
                r"^\s*(Authentication|Authentifizierung)\s*:\s*(.+?)\s*$",
                line,
                re.IGNORECASE,
            )
            if match:
                authentication = match.group(2).strip()

        match = re.match(
            r"^\s*(Key Content|Schl.*sselinhalt)\s*:\s*(.*)$",
            line,
            re.IGNORECASE,
        )
        if match:
            password = match.group(2).strip()

        match = re.match(
            r"^\s*(Security key|Sicherheitsschl.*ssel)\s*:\s*(.+?)\s*$",
            line,
            re.IGNORECASE,
        )
        if match:
            security_key = match.group(2).strip()

    if (
        password == "<nicht auslesbar>"
        and security_key
        and re.fullmatch(r"(Absent|Nicht vorhanden)", security_key, re.IGNORECASE)
    ):
        password = "<offenes WLAN – kein Passwort>"

    return WlanProfile(
        ssid=ssid,
        authentication=authentication,
        password=password,
    )


def get_all_profile_details() -> list[WlanProfile]:
    profiles: list[WlanProfile] = []

    for ssid in get_profile_names():
        try:
            profiles.append(get_profile_details(ssid))
        except Exception:
            profiles.append(
                WlanProfile(
                    ssid=ssid,
                    authentication="-",
                    password="<Fehler beim Auslesen>",
                )
            )

    return profiles


def delete_profile(ssid: str) -> None:
    """Löscht genau ein WLAN-Profil case-sensitiv."""
    try:
        delete_profile_native(ssid)
    except NativeWifiError as exc:
        raise NetshError(str(exc)) from exc


def delete_all_profiles() -> tuple[list[str], list[tuple[str, str]]]:
    """Löscht alle WLAN-Profile einzeln und case-sensitiv."""
    successful: list[str] = []
    failed: list[tuple[str, str]] = []

    for ssid in get_profile_names():
        try:
            delete_profile_native(ssid)
            successful.append(ssid)
        except NativeWifiError as exc:
            failed.append((ssid, str(exc)))

    return successful, failed


def get_current_connection() -> CurrentConnection:
    result = run_netsh(["wlan", "show", "interfaces"])
    text = result.combined

    if looks_like_location_permission_error(text):
        raise PermissionError(
            QCoreApplication.translate(
                "Profiles",
"Windows verweigert den Zugriff auf die WLAN-Informationen.\n\n"
"Aktiviere unter Einstellungen > Datenschutz und Sicherheit > "
"Standort mindestens die Standortdienste."
            )
        )

    if result.returncode != 0:
        raise NetshError(
            QCoreApplication.translate("Profiles", "Die WLAN-Schnittstelle konnte nicht gelesen werden.\n\n{details}").format(details=text)
        )

    properties: dict[str, str] = {}

    for line in text.splitlines():
        match = re.match(r"^\s*([^:]+?)\s*:\s*(.*?)\s*$", line)
        if not match:
            continue

        name = match.group(1).strip()
        value = match.group(2).strip()

        mapping = {
            "Name": "interface",
            "State": "status",
            "Status": "status",
            "SSID": "ssid",
            "BSSID": "bssid",
            "Radio type": "radio_type",
            "Funktyp": "radio_type",
            "Authentication": "authentication",
            "Authentifizierung": "authentication",
            "Cipher": "cipher",
            "Verschlüsselung": "cipher",
            "Channel": "channel",
            "Kanal": "channel",
            "Signal": "signal",
        }

        key = mapping.get(name)
        if key:
            properties[key] = value
        elif re.fullmatch(
            r"Receive rate \(Mbps\)|Empfangsrate \(MBit/s\)",
            name,
        ):
            properties["receive_rate"] = f"{value} MBit/s"
        elif re.fullmatch(
            r"Transmit rate \(Mbps\)|Übertragungsrate \(MBit/s\)",
            name,
        ):
            properties["transmit_rate"] = f"{value} MBit/s"

    if not properties.get("ssid"):
        return CurrentConnection()

    return CurrentConnection(**properties)



def connect_profile(ssid: str) -> None:
    """Verbindet mit einem bereits gespeicherten WLAN-Profil."""
    result = run_netsh(["wlan", "connect", f"name={ssid}"])
    require_success(
        result,
        QCoreApplication.translate("Profiles", "Die Verbindung mit dem WLAN-Profil '{ssid}' konnte nicht hergestellt werden.").format(ssid=ssid),
    )



def delete_selected_profiles(
    ssids: list[str],
) -> tuple[list[str], list[tuple[str, str]]]:
    """Löscht genau die ausgewählten WLAN-Profile case-sensitiv."""
    successful: list[str] = []
    failed: list[tuple[str, str]] = []

    for ssid in ssids:
        try:
            delete_profile_native(ssid)
            successful.append(ssid)
        except NativeWifiError as exc:
            failed.append((ssid, str(exc)))

    return successful, failed
