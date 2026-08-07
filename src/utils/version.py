from __future__ import annotations

import sys
from pathlib import Path


class AppInfo:
    """Liest die Projektinformationen aus der Datei VERSION."""

    if getattr(sys, "frozen", False):
        # PyInstaller: Datendateien liegen im Bundle-Verzeichnis.
        PROJECT_ROOT = Path(sys._MEIPASS)
    else:
        # Entwicklung aus dem Quellcode.
        PROJECT_ROOT = Path(__file__).resolve().parents[2]

    VERSION_FILE = PROJECT_ROOT / "VERSION"

    _data: dict[str, str] = {}

    if VERSION_FILE.exists():
        for line in VERSION_FILE.read_text(
            encoding="utf-8"
        ).splitlines():

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                _data[key.strip()] = value.strip()

    NAME = _data.get("Name", "WLAN-Manager")
    VERSION = _data.get("Version", "Unbekannt")
    AUTHOR = _data.get("Author", "Urs Mumprecht")
    COMPANY = _data.get("Company", "Mumprecht Software")
    COPYRIGHT = _data.get(
        "Copyright",
        "2026 Urs Mumprecht",
    )

    @classmethod
    def title(cls) -> str:
        """Fenstertitel."""
        return f"{cls.NAME} {cls.VERSION}"

    @classmethod
    def about(cls) -> str:
        """Text für den Dialog 'Über WLAN-Manager'."""
        return (
            f"{cls.NAME}\n"
            f"Version {cls.VERSION}\n\n"
            f"{cls.COPYRIGHT}\n"
            f"{cls.COMPANY}\n\n"
            f"Autor: {cls.AUTHOR}"
        )

    @classmethod
    def version_string(cls) -> str:
        """Programmname mit Versionsnummer."""
        return f"{cls.NAME} Version {cls.VERSION}"