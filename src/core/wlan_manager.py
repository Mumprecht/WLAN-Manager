from __future__ import annotations

from datetime import datetime
from pathlib import Path

from core.models import EditableWifiProfile
from core.qr_code import wifi_qr_data
from core.wlan_backend import WlanBackend
from utils.paths import get_downloads_folder
from platforms.backend_factory import create_wlan_backend


class WlanManager:
    """Plattformunabhängige Fassade zwischen GUI und WLAN-Backend."""

    def __init__(self, backend: WlanBackend | None = None) -> None:
        self.backend = backend or create_wlan_backend()

    def profiles(self):
        return self.backend.profiles()

    def current_connection(self):
        return self.backend.current_connection()

    def autoconnect_profiles(self):
        return self.backend.autoconnect_profiles()

    def set_profile_priority(
        self,
        profile_name: str,
        priority: int,
    ) -> None:
        self.backend.set_profile_priority(
            profile_name,
            priority,
        )

    def connect_profile(self, ssid: str) -> None:
        self.backend.connect_profile(ssid)

    def delete_profile(self, ssid: str) -> None:
        self.backend.delete_profile(ssid)

    def delete_all(self):
        return self.backend.delete_all()

    def delete_selected(self, ssids: list[str]):
        return self.backend.delete_selected(ssids)

    def export_profile(
        self,
        ssid: str,
        folder: Path,
        include_password: bool,
    ):
        return self.backend.export_profile(
            ssid,
            folder,
            include_password,
        )

    def export_all(
        self,
        folder: Path,
        include_password: bool,
    ):
        return self.backend.export_all(
            folder,
            include_password,
        )

    def export_selected(
        self,
        ssids: list[str],
        folder: Path,
        include_password: bool,
    ):
        return self.backend.export_selected(
            ssids,
            folder,
            include_password,
        )

    def existing_export_file(
        self,
        ssid: str,
        folder: Path,
    ) -> Path | None:
        return self.backend.existing_export_file(
            ssid,
            folder,
        )

    def export_profile_overwrite(
        self,
        ssid: str,
        folder: Path,
        include_password: bool,
    ):
        return self.backend.export_profile_overwrite(
            ssid,
            folder,
            include_password,
        )

    def import_profile(self, path: Path) -> None:
        self.backend.import_profile(path)

    def import_all(self, folder: Path):
        return self.backend.import_all(folder)

    def import_selected(self, files: list[Path]):
        return self.backend.import_selected(files)

    def export_csv(self, path: Path) -> int:
        return self.backend.export_csv(path)

    def load_profile_for_edit(
        self,
        profile_name: str,
    ) -> EditableWifiProfile:
        return self.backend.load_profile_for_edit(
            profile_name
        )

    def create_profile(
        self,
        profile: EditableWifiProfile,
    ) -> None:
        self.backend.create_profile(profile)

    def replace_profile(
        self,
        old_profile_name: str,
        profile: EditableWifiProfile,
    ) -> None:
        self.backend.replace_profile(
            old_profile_name,
            profile,
        )

    @staticmethod
    def qr_data(profile) -> str:
        return wifi_qr_data(profile)

    @staticmethod
    def downloads_folder() -> Path:
        return get_downloads_folder()

    @staticmethod
    def default_backup_folder(
        include_password: bool,
    ) -> Path:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H%M%S"
        )
        suffix = (
            "WLAN-Backup_mit_Passwoertern"
            if include_password
            else "WLAN-Export_ohne_Klartextpasswoerter"
        )
        return get_downloads_folder() / (
            f"{timestamp}_{suffix}"
        )

    @staticmethod
    def default_csv_path() -> Path:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H%M%S"
        )
        return get_downloads_folder() / (
            f"{timestamp}_WLAN-Profile.csv"
        )
