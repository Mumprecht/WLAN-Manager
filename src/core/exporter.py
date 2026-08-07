from __future__ import annotations

from pathlib import Path

from core.netsh import NetshError, require_success, run_netsh
from core.profiles import get_profile_names


def export_profile(
    ssid: str,
    folder: Path,
    include_password: bool,
) -> list[Path]:
    folder.mkdir(parents=True, exist_ok=True)
    before = {path.resolve() for path in folder.glob("*.xml")}

    arguments = [
        "wlan",
        "export",
        "profile",
        f"name={ssid}",
        f"folder={folder}",
    ]

    if include_password:
        arguments.append("key=clear")

    result = run_netsh(arguments)
    require_success(
        result,
        f"Das WLAN-Profil '{ssid}' konnte nicht exportiert werden.",
    )

    after = {path.resolve() for path in folder.glob("*.xml")}
    created = sorted(after - before)

    if not created:
        raise NetshError(
            "netsh meldete keinen Fehler, es wurde jedoch keine neue XML-Datei erstellt."
        )

    return created


def export_all_profiles(
    folder: Path,
    include_password: bool,
) -> tuple[list[str], list[tuple[str, str]]]:
    successful: list[str] = []
    failed: list[tuple[str, str]] = []

    for ssid in get_profile_names():
        try:
            export_profile(ssid, folder, include_password)
            successful.append(ssid)
        except Exception as exc:
            failed.append((ssid, str(exc)))

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
            export_profile(ssid, folder, include_password)
            successful.append(ssid)
        except Exception as exc:
            failed.append((ssid, str(exc)))

    return successful, failed



def find_existing_profile_xml(
    ssid: str,
    folder: Path,
) -> Path | None:
    """
    Sucht die von netsh erwartete XML-Datei für ein Profil.

    netsh erzeugt üblicherweise Dateien im Format:
    Wi-Fi-<SSID>.xml
    """
    expected = folder / f"Wi-Fi-{ssid}.xml"
    if expected.exists():
        return expected

    # Fallback: passende XML-Dateien anhand des SSID-Teils suchen.
    candidates = sorted(
        folder.glob("*.xml"),
        key=lambda path: path.name.casefold(),
    )

    ssid_cf = ssid.casefold()
    for path in candidates:
        if ssid_cf in path.stem.casefold():
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
    existing = find_existing_profile_xml(ssid, folder)

    if existing and existing.exists():
        existing.unlink()

    return export_profile(
        ssid,
        folder,
        include_password,
    )
