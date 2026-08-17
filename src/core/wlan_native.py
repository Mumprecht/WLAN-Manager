from __future__ import annotations

import ctypes
from ctypes import wintypes



ERROR_SUCCESS = 0
ERROR_ACCESS_DENIED = 5
ERROR_NOT_FOUND = 1168

WLAN_API_VERSION_2_0 = 2
WLAN_MAX_NAME_LENGTH = 256

# WlanGetProfile: Klartextschlüssel anfordern.
WLAN_PROFILE_GET_PLAINTEXT_KEY = 0x00000004


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", ctypes.c_ubyte * 8),
    ]


class WLAN_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        (
            "strInterfaceDescription",
            ctypes.c_wchar * WLAN_MAX_NAME_LENGTH,
        ),
        ("isState", wintypes.DWORD),
    ]


class WLAN_INTERFACE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", wintypes.DWORD),
        ("dwIndex", wintypes.DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1),
    ]


class NativeWifiError(RuntimeError):
    """Fehler der Windows Native Wi-Fi API."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(QCoreApplication.translate("WlanNative", "{message} (Windows-Fehler {code})").format(message=message, code=code))
        self.code = code


_wlanapi = ctypes.WinDLL(
    "wlanapi.dll",
    use_last_error=True,
)

_wlanapi.WlanOpenHandle.argtypes = [
    wintypes.DWORD,
    ctypes.c_void_p,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.POINTER(wintypes.HANDLE),
]
_wlanapi.WlanOpenHandle.restype = wintypes.DWORD

_wlanapi.WlanCloseHandle.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
]
_wlanapi.WlanCloseHandle.restype = wintypes.DWORD

_wlanapi.WlanEnumInterfaces.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_void_p),
]
_wlanapi.WlanEnumInterfaces.restype = wintypes.DWORD

_wlanapi.WlanGetProfile.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(GUID),
    wintypes.LPCWSTR,
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_void_p),
    ctypes.POINTER(wintypes.DWORD),
    ctypes.POINTER(wintypes.DWORD),
]
_wlanapi.WlanGetProfile.restype = wintypes.DWORD


_wlanapi.WlanDeleteProfile.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(GUID),
    wintypes.LPCWSTR,
    ctypes.c_void_p,
]
_wlanapi.WlanDeleteProfile.restype = wintypes.DWORD

_wlanapi.WlanFreeMemory.argtypes = [
    ctypes.c_void_p,
]
_wlanapi.WlanFreeMemory.restype = None


def _copy_guid(source: GUID) -> GUID:
    target = GUID()
    ctypes.memmove(
        ctypes.byref(target),
        ctypes.byref(source),
        ctypes.sizeof(GUID),
    )
    return target


def _enumerate_interface_guids(
    client_handle: wintypes.HANDLE,
) -> list[GUID]:
    interface_list_ptr = ctypes.c_void_p()

    result = _wlanapi.WlanEnumInterfaces(
        client_handle,
        None,
        ctypes.byref(interface_list_ptr),
    )

    if result != ERROR_SUCCESS:
        raise NativeWifiError(
            result,
            QCoreApplication.translate("WlanNative", "Die WLAN-Schnittstellen konnten nicht gelesen werden."),
        )

    if not interface_list_ptr.value:
        return []

    try:
        interface_list = ctypes.cast(
            interface_list_ptr,
            ctypes.POINTER(WLAN_INTERFACE_INFO_LIST),
        ).contents

        first_item_address = (
            interface_list_ptr.value
            + WLAN_INTERFACE_INFO_LIST.InterfaceInfo.offset
        )

        items = ctypes.cast(
            first_item_address,
            ctypes.POINTER(WLAN_INTERFACE_INFO),
        )

        return [
            _copy_guid(items[index].InterfaceGuid)
            for index in range(interface_list.dwNumberOfItems)
        ]

    finally:
        _wlanapi.WlanFreeMemory(interface_list_ptr)


def get_profile_xml(
    profile_name: str,
    include_password: bool,
) -> str:
    """
    Liest die XML-Repräsentation eines WLAN-Profils über die
    Windows Native Wi-Fi API.

    Der Profilname wird von Windows exakt an WlanGetProfile übergeben.
    Bei include_password=True wird der Klartextschlüssel angefordert.
    """
    negotiated_version = wintypes.DWORD()
    client_handle = wintypes.HANDLE()

    result = _wlanapi.WlanOpenHandle(
        WLAN_API_VERSION_2_0,
        None,
        ctypes.byref(negotiated_version),
        ctypes.byref(client_handle),
    )

    if result != ERROR_SUCCESS:
        raise NativeWifiError(
            result,
            QCoreApplication.translate("WlanNative", "Die Windows WLAN-API konnte nicht geöffnet werden."),
        )

    try:
        interface_guids = _enumerate_interface_guids(
            client_handle
        )

        if not interface_guids:
            raise NativeWifiError(
                ERROR_NOT_FOUND,
                QCoreApplication.translate("WlanNative", "Es wurde keine WLAN-Schnittstelle gefunden."),
            )

        access_denied = False

        for interface_guid in interface_guids:
            profile_xml_ptr = ctypes.c_void_p()
            flags = wintypes.DWORD(
                WLAN_PROFILE_GET_PLAINTEXT_KEY
                if include_password
                else 0
            )
            granted_access = wintypes.DWORD()

            result = _wlanapi.WlanGetProfile(
                client_handle,
                ctypes.byref(interface_guid),
                profile_name,
                None,
                ctypes.byref(profile_xml_ptr),
                ctypes.byref(flags),
                ctypes.byref(granted_access),
            )

            if result == ERROR_NOT_FOUND:
                continue

            if result == ERROR_ACCESS_DENIED:
                access_denied = True
                continue

            if result != ERROR_SUCCESS:
                raise NativeWifiError(
                    result,
                    QCoreApplication.translate("WlanNative", "Das WLAN-Profil '{profile_name}' konnte nicht gelesen werden.").format(
                        profile_name=profile_name
                    ),
                )

            if not profile_xml_ptr.value:
                raise NativeWifiError(
                    ERROR_NOT_FOUND,
                    QCoreApplication.translate("WlanNative", "Das WLAN-Profil '{profile_name}' lieferte keine XML-Daten.").format(
                        profile_name=profile_name
                    ),
                )

            try:
                return ctypes.wstring_at(
                    profile_xml_ptr.value
                )
            finally:
                _wlanapi.WlanFreeMemory(
                    profile_xml_ptr
                )

        if access_denied:
            raise NativeWifiError(
                ERROR_ACCESS_DENIED,
                QCoreApplication.translate("WlanNative", "Auf das WLAN-Profil '{profile_name}' konnte nicht zugegriffen werden.").format(
                    profile_name=profile_name
                ),
            )

        raise NativeWifiError(
            ERROR_NOT_FOUND,
            QCoreApplication.translate("WlanNative", "Das WLAN-Profil '{profile_name}' wurde auf keiner WLAN-Schnittstelle gefunden.").format(
                profile_name=profile_name
            ),
        )

    finally:
        _wlanapi.WlanCloseHandle(
            client_handle,
            None,
        )


def delete_profile(profile_name: str) -> None:
    """Löscht ein WLAN-Profil case-sensitiv über WlanDeleteProfile."""
    negotiated_version = wintypes.DWORD()
    client_handle = wintypes.HANDLE()

    result = _wlanapi.WlanOpenHandle(
        WLAN_API_VERSION_2_0,
        None,
        ctypes.byref(negotiated_version),
        ctypes.byref(client_handle),
    )
    if result != ERROR_SUCCESS:
        raise NativeWifiError(
            result,
            QCoreApplication.translate("WlanNative", "Die Windows WLAN-API konnte nicht geöffnet werden."),
        )

    try:
        interface_guids = _enumerate_interface_guids(client_handle)
        if not interface_guids:
            raise NativeWifiError(
                ERROR_NOT_FOUND,
                QCoreApplication.translate("WlanNative", "Es wurde keine WLAN-Schnittstelle gefunden."),
            )

        deleted = False
        access_denied = False

        for interface_guid in interface_guids:
            result = _wlanapi.WlanDeleteProfile(
                client_handle,
                ctypes.byref(interface_guid),
                profile_name,
                None,
            )

            if result == ERROR_SUCCESS:
                deleted = True
            elif result == ERROR_NOT_FOUND:
                continue
            elif result == ERROR_ACCESS_DENIED:
                access_denied = True
            else:
                raise NativeWifiError(
                    result,
                    QCoreApplication.translate("WlanNative", "Das WLAN-Profil '{profile_name}' konnte nicht gelöscht werden.").format(
                        profile_name=profile_name
                    ),
                )

        if deleted:
            return

        if access_denied:
            raise NativeWifiError(
                ERROR_ACCESS_DENIED,
                QCoreApplication.translate(
                "WlanNative",
"Das WLAN-Profil '{profile_name}' konnte wegen fehlender Berechtigung nicht gelöscht werden."
            ).format(profile_name=profile_name),
            )

        raise NativeWifiError(
            ERROR_NOT_FOUND,
            QCoreApplication.translate("WlanNative", "Das WLAN-Profil '{profile_name}' wurde auf keiner WLAN-Schnittstelle gefunden.").format(
                profile_name=profile_name
            ),
        )
    finally:
        _wlanapi.WlanCloseHandle(client_handle, None)
from PySide6.QtCore import QCoreApplication
