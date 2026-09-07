from __future__ import annotations

from pathlib import Path

from core.csv_export import export_profiles_to_csv
from core.exporter import (
    export_all_profiles,
    export_profile,
    export_profile_overwrite,
    export_selected_profiles,
    find_existing_profile_xml,
)
from core.importer import (
    import_all_profiles,
    import_profile,
    import_selected_profiles,
)
from core.models import CurrentConnection, EditableWifiProfile, WlanProfile
from core.profile_editor import (
    install_profile,
    load_profile_for_edit,
    replace_profile,
)
from core.profiles import (
    connect_profile,
    delete_all_profiles,
    delete_profile,
    delete_selected_profiles,
    get_all_profile_details,
    get_current_connection,
)
from core.wlan_backend import WlanBackend


class WindowsWlanBackend(WlanBackend):
    """WLAN-Backend für Microsoft Windows."""

    def profiles(self) -> list[WlanProfile]:
        return get_all_profile_details()

    def current_connection(self) -> CurrentConnection:
        return get_current_connection()

    def connect_profile(self, profile_name: str) -> None:
        connect_profile(profile_name)

    def delete_profile(self, profile_name: str) -> None:
        delete_profile(profile_name)

    def delete_all(self):
        return delete_all_profiles()

    def delete_selected(self, profile_names: list[str]):
        return delete_selected_profiles(profile_names)

    def export_profile(
        self,
        profile_name: str,
        folder: Path,
        include_password: bool,
    ):
        return export_profile(
            profile_name,
            folder,
            include_password,
        )

    def export_all(
        self,
        folder: Path,
        include_password: bool,
    ):
        return export_all_profiles(
            folder,
            include_password,
        )

    def export_selected(
        self,
        profile_names: list[str],
        folder: Path,
        include_password: bool,
    ):
        return export_selected_profiles(
            profile_names,
            folder,
            include_password,
        )

    def existing_export_file(
        self,
        profile_name: str,
        folder: Path,
    ) -> Path | None:
        return find_existing_profile_xml(
            profile_name,
            folder,
        )

    def export_profile_overwrite(
        self,
        profile_name: str,
        folder: Path,
        include_password: bool,
    ):
        return export_profile_overwrite(
            profile_name,
            folder,
            include_password,
        )

    def import_profile(self, path: Path) -> None:
        import_profile(path)

    def import_all(self, folder: Path):
        return import_all_profiles(folder)

    def import_selected(self, files: list[Path]):
        return import_selected_profiles(files)

    def export_csv(self, path: Path) -> int:
        return export_profiles_to_csv(path)

    def load_profile_for_edit(
        self,
        profile_name: str,
    ) -> EditableWifiProfile:
        return load_profile_for_edit(profile_name)

    def create_profile(
        self,
        profile: EditableWifiProfile,
    ) -> None:
        install_profile(profile)

    def replace_profile(
        self,
        old_profile_name: str,
        profile: EditableWifiProfile,
    ) -> None:
        replace_profile(
            old_profile_name,
            profile,
        )
