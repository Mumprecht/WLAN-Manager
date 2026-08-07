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
