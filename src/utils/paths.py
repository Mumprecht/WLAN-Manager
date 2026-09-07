from __future__ import annotations

import os
import sys
from pathlib import Path


def project_root() -> Path:
    """Projektwurzel bzw. PyInstaller-Bundlewurzel."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


def local_app_data() -> Path:
    """Benutzerbezogener Anwendungsordner unter LOCALAPPDATA."""
    base = os.environ.get("LOCALAPPDATA")

    if base:
        root = Path(base)
    else:
        root = Path.home() / "AppData" / "Local"

    return root / "Mumprecht Software" / "WLAN-Manager"


def log_dir() -> Path:
    path = local_app_data() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def bundled_document(relative_path: str) -> Path:
    """Pfad zu einer mit PyInstaller gebündelten Datei."""
    return project_root() / relative_path


def resource_path(relative_path: str) -> Path:
    """Pfad zu einer Programmressource in Entwicklung und PyInstaller."""

    if getattr(sys, "frozen", False):
        # PyInstaller-Bundle
        return project_root() / "resources" / relative_path

    # Entwicklungsumgebung
    return project_root() / "src" / "resources" / relative_path


def get_downloads_folder() -> Path:
    """Ermittelt den Download-Ordner des aktuellen Benutzers."""
    home = Path.home()

    candidates = [
        home / "Downloads",
        Path(os.environ.get("USERPROFILE", str(home))) / "Downloads",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]
