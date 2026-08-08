from __future__ import annotations

from datetime import datetime
from pathlib import Path

from core.csv_export import export_profiles_to_csv
from core.exporter import (
    export_all_profiles,
    export_profile,
    export_selected_profiles,
    export_profile_overwrite,
    find_existing_profile_xml,
)
from core.importer import (
    import_all_profiles,
    import_profile,
    import_selected_profiles,
)
from core.qr_code import wifi_qr_data
from core.profile_editor import (
    EditableWifiProfile,
    install_profile,
    replace_profile,
    load_profile_for_edit,
)
from core.profiles import (
    delete_all_profiles,
    delete_selected_profiles,
    delete_profile,
    get_all_profile_details,
    get_current_connection,
    connect_profile,
)
from core.netsh import get_downloads_folder


class WlanManager:
    """Fassade zwischen GUI und WLAN-Funktionen."""

    @staticmethod
    def profiles():
        return get_all_profile_details()

    @staticmethod
    def current_connection():
        return get_current_connection()

    @staticmethod
    def connect_profile(ssid: str) -> None:
        connect_profile(ssid)

    @staticmethod
    def delete_profile(ssid: str) -> None:
        delete_profile(ssid)

    @staticmethod
    def delete_all():
        return delete_all_profiles()

    @staticmethod
    def delete_selected(ssids: list[str]):
        return delete_selected_profiles(ssids)

    @staticmethod
    def export_profile(ssid: str, folder: Path, include_password: bool):
        return export_profile(ssid, folder, include_password)

    @staticmethod
    def export_all(folder: Path, include_password: bool):
        return export_all_profiles(folder, include_password)

    @staticmethod
    def export_selected(
        ssids: list[str],
        folder: Path,
        include_password: bool,
    ):
        return export_selected_profiles(
            ssids,
            folder,
            include_password,
        )

    @staticmethod
    def existing_export_file(
        ssid: str,
        folder: Path,
    ) -> Path | None:
        return find_existing_profile_xml(ssid, folder)

    @staticmethod
    def export_profile_overwrite(
        ssid: str,
        folder: Path,
        include_password: bool,
    ):
        return export_profile_overwrite(
            ssid,
            folder,
            include_password,
        )

    @staticmethod
    def import_profile(path: Path) -> None:
        import_profile(path)

    @staticmethod
    def import_all(folder: Path):
        return import_all_profiles(folder)

    @staticmethod
    def import_selected(files: list[Path]):
        return import_selected_profiles(files)

    @staticmethod
    def export_csv(path: Path) -> int:
        return export_profiles_to_csv(path)

    @staticmethod
    def load_profile_for_edit(profile_name: str) -> EditableWifiProfile:
        return load_profile_for_edit(profile_name)

    @staticmethod
    def create_profile(profile: EditableWifiProfile) -> None:
        install_profile(profile)

    @staticmethod
    def replace_profile(
        old_profile_name: str,
        profile: EditableWifiProfile,
    ) -> None:
        replace_profile(old_profile_name, profile)

    @staticmethod
    def qr_data(profile) -> str:
        return wifi_qr_data(profile)

    @staticmethod
    def downloads_folder() -> Path:
        return get_downloads_folder()

    @staticmethod
    def default_backup_folder(include_password: bool) -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        suffix = (
            "WLAN-Backup_mit_Passwoertern"
            if include_password
            else "WLAN-Export_ohne_Klartextpasswoerter"
        )
        return get_downloads_folder() / f"{timestamp}_{suffix}"

    @staticmethod
    def default_csv_path() -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        return get_downloads_folder() / f"{timestamp}_WLAN-Profile.csv"
