from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from core.models import (
    AutoconnectProfile,
    CurrentConnection,
    EditableWifiProfile,
    WlanProfile,
)


class WlanBackend(ABC):
    """Plattformunabhängige Schnittstelle für WLAN-Funktionen."""

    @abstractmethod
    def profiles(self) -> list[WlanProfile]:
        """Liefert die gespeicherten WLAN-Profile."""
        raise NotImplementedError

    @abstractmethod
    def autoconnect_profiles(self) -> list[AutoconnectProfile]:
        """Liefert Autoconnect-Status und Priorität der WLAN-Profile."""
        raise NotImplementedError

    @abstractmethod
    def current_connection(self) -> CurrentConnection:
        """Liefert Informationen zur aktuellen WLAN-Verbindung."""
        raise NotImplementedError

    @abstractmethod
    def connect_profile(self, profile_name: str) -> None:
        """Verbindet mit einem gespeicherten WLAN-Profil."""
        raise NotImplementedError

    @abstractmethod
    def delete_profile(self, profile_name: str) -> None:
        """Löscht ein gespeichertes WLAN-Profil."""
        raise NotImplementedError

    @abstractmethod
    def delete_all(self):
        """Löscht alle gespeicherten WLAN-Profile."""
        raise NotImplementedError

    @abstractmethod
    def delete_selected(self, profile_names: list[str]):
        """Löscht die ausgewählten WLAN-Profile."""
        raise NotImplementedError

    @abstractmethod
    def export_profile(
        self,
        profile_name: str,
        folder: Path,
        include_password: bool,
    ):
        """Exportiert ein WLAN-Profil."""
        raise NotImplementedError

    @abstractmethod
    def export_all(
        self,
        folder: Path,
        include_password: bool,
    ):
        """Exportiert alle WLAN-Profile."""
        raise NotImplementedError

    @abstractmethod
    def export_selected(
        self,
        profile_names: list[str],
        folder: Path,
        include_password: bool,
    ):
        """Exportiert die ausgewählten WLAN-Profile."""
        raise NotImplementedError

    @abstractmethod
    def existing_export_file(
        self,
        profile_name: str,
        folder: Path,
    ) -> Path | None:
        """Sucht eine bereits vorhandene Exportdatei."""
        raise NotImplementedError

    @abstractmethod
    def export_profile_overwrite(
        self,
        profile_name: str,
        folder: Path,
        include_password: bool,
    ):
        """Exportiert ein WLAN-Profil und überschreibt den vorhandenen Export."""
        raise NotImplementedError

    @abstractmethod
    def import_profile(self, path: Path) -> None:
        """Importiert ein WLAN-Profil."""
        raise NotImplementedError

    @abstractmethod
    def import_all(self, folder: Path):
        """Importiert alle WLAN-Profile eines Ordners."""
        raise NotImplementedError

    @abstractmethod
    def import_selected(self, files: list[Path]):
        """Importiert die ausgewählten WLAN-Profile."""
        raise NotImplementedError

    @abstractmethod
    def export_csv(self, path: Path) -> int:
        """Exportiert die WLAN-Profilliste als CSV."""
        raise NotImplementedError

    @abstractmethod
    def load_profile_for_edit(
        self,
        profile_name: str,
    ) -> EditableWifiProfile:
        """Lädt ein WLAN-Profil zur Bearbeitung."""
        raise NotImplementedError

    @abstractmethod
    def create_profile(
        self,
        profile: EditableWifiProfile,
    ) -> None:
        """Erstellt ein WLAN-Profil."""
        raise NotImplementedError

    @abstractmethod
    def replace_profile(
        self,
        old_profile_name: str,
        profile: EditableWifiProfile,
    ) -> None:
        """Ersetzt ein vorhandenes WLAN-Profil."""
        raise NotImplementedError
