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
from core.models import (
    AutoconnectProfile,
    CurrentConnection,
    EditableWifiProfile,
    WlanProfile,
)
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
from core.wlan_native import (
    get_profile_names_in_preference_order,
    set_profile_autoconnect as native_set_profile_autoconnect,
    set_profile_position,
)


class WindowsWlanBackend(WlanBackend):
    """WLAN-Backend für Microsoft Windows."""

    def profiles(self) -> list[WlanProfile]:
        return get_all_profile_details()

    def current_connection(self) -> CurrentConnection:
        return get_current_connection()

    def autoconnect_profiles(self) -> list[AutoconnectProfile]:
        result: list[AutoconnectProfile] = []

        for priority, profile_name in enumerate(
            get_profile_names_in_preference_order(),
            start=1,
        ):
            editable = load_profile_for_edit(profile_name)

            result.append(
                AutoconnectProfile(
                    profile_name=profile_name,
                    autoconnect=editable.autoconnect,
                    priority=priority,
                )
            )

        return result

    def set_profile_priority(
        self,
        profile_name: str,
        priority: int,
    ) -> None:
        if priority < 1:
            raise ValueError(
                "Die WLAN-Priorität muss mindestens 1 sein."
            )

        profile_names = get_profile_names_in_preference_order()

        if profile_name not in profile_names:
            raise ValueError(
                f"Das WLAN-Profil {profile_name!r} wurde nicht gefunden."
            )

        if priority > len(profile_names):
            raise ValueError(
                "Die WLAN-Priorität darf nicht größer als "
                f"{len(profile_names)} sein."
            )

        # Öffentliche API: 1 = höchste Priorität.
        # Windows Native Wi-Fi: 0 = höchste Position.
        set_profile_position(
            profile_name,
            priority - 1,
        )


    def set_profile_autoconnect(
        self,
        profile_name: str,
        enabled: bool,
    ) -> None:
        native_set_profile_autoconnect(
            profile_name,
            enabled,
        )


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
