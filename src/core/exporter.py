from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from core.netsh import NetshError
from core.profiles import get_profile_names
from core.wlan_native import NativeWifiError, get_profile_xml


INVALID_FILENAME_CHARS = re.compile(
    r'[<>:"/\\|?*\x00-\x1f]'
)


def _profile_name_from_xml_text(xml_text: str) -> str | None:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None

    for child in root:
        if child.tag.rsplit("}", 1)[-1] == "name":
            return (child.text or "").strip()

    return None


def _profile_name_from_xml_file(path: Path) -> str | None:
    try:
        xml_text = path.read_text(
            encoding="utf-8-sig"
        )
    except (OSError, UnicodeError):
        return None

    return _profile_name_from_xml_text(xml_text)


def _safe_filename_part(value: str) -> str:
    safe = INVALID_FILENAME_CHARS.sub("_", value)
    safe = safe.rstrip(" .")

    if not safe:
        safe = "WLAN-Profil"

    return safe


def _backup_filename(profile_name: str) -> str:
    """
    Erzeugt einen lesbaren und gleichzeitig case-sensitiv eindeutigen
    Dateinamen.

    Der Hash wird aus dem exakten Profilnamen erzeugt. Damit erhalten
    z. B. 'wetterhorn1' und 'Wetterhorn1' auch auf einem
    case-insensitiven Windows-Dateisystem unterschiedliche Dateinamen.
    """
    safe_name = _safe_filename_part(profile_name)

    digest = hashlib.sha256(
        profile_name.encode("utf-8")
    ).hexdigest()[:8].upper()

    return f"Wi-Fi-{safe_name}__{digest}.xml"


def export_profile(
    ssid: str,
    folder: Path,
    include_password: bool,
) -> list[Path]:
    folder.mkdir(parents=True, exist_ok=True)

    try:
        xml_text = get_profile_xml(
            ssid,
            include_password,
        )
    except NativeWifiError as exc:
        raise NetshError(str(exc)) from exc

    xml_profile_name = _profile_name_from_xml_text(
        xml_text
    )

    if xml_profile_name != ssid:
        raise NetshError(
            f"Das gelesene WLAN-Profil stimmt nicht mit "
            f"'{ssid}' überein."
        )

    destination = folder / _backup_filename(ssid)

    if destination.exists():
        raise NetshError(
            f"Für das WLAN-Profil '{ssid}' existiert bereits "
            f"eine Sicherungsdatei: {destination.name}"
        )

    destination.write_text(
        xml_text,
        encoding="utf-8",
    )

    return [destination.resolve()]


def export_all_profiles(
    folder: Path,
    include_password: bool,
) -> tuple[list[str], list[tuple[str, str]]]:
    successful: list[str] = []
    failed: list[tuple[str, str]] = []

    for ssid in get_profile_names():
        try:
            export_profile(
                ssid,
                folder,
                include_password,
            )
            successful.append(ssid)
        except Exception as exc:
            failed.append(
                (ssid, str(exc))
            )

    return successful, failed


def export_selected_profiles(
    ssids: list[str],
    folder: Path,
    include_password: bool,
) -> tuple[list[str], list[tuple[str, str]]]:
    """Exportiert genau die ausgewählten WLAN-Profile."""
    folder.mkdir(parents=True, exist_ok=True)

    successful: list[str] = []
    failed: list[tuple[str, str]] = []

    for ssid in ssids:
        try:
            export_profile(
                ssid,
                folder,
                include_password,
            )
            successful.append(ssid)
        except Exception as exc:
            failed.append(
                (ssid, str(exc))
            )

    return successful, failed


def find_existing_profile_xml(
    ssid: str,
    folder: Path,
) -> Path | None:
    """
    Sucht eine vorhandene Backup-XML anhand des exakten,
    case-sensitiven Profilnamens im XML-Inhalt.

    Dadurch werden auch ältere Backup-Dateien ohne Hash-Suffix erkannt.
    """
    if not folder.exists() or not folder.is_dir():
        return None

    for path in sorted(
        folder.glob("*.xml"),
        key=lambda item: item.name.casefold(),
    ):
        if _profile_name_from_xml_file(path) == ssid:
            return path

    return None


def export_profile_overwrite(
    ssid: str,
    folder: Path,
    include_password: bool,
) -> list[Path]:
    """
    Exportiert ein Profil und ersetzt eine vorhandene passende XML-Datei.
    """
    existing = find_existing_profile_xml(
        ssid,
        folder,
    )

    if existing and existing.exists():
        existing.unlink()

    return export_profile(
        ssid,
        folder,
        include_password,
    )
