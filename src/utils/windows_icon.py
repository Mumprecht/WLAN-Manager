from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes
from pathlib import Path


WM_SETICON = 0x0080

ICON_SMALL = 0
ICON_BIG = 1

IMAGE_ICON = 1
LR_LOADFROMFILE = 0x0010


def set_native_window_icon(
    hwnd: int,
    icon_path: str | Path,
) -> None:
    """
    Setzt das kleine und grosse Icon eines nativen Windows-Fensters.

    ICON_SMALL wird unter anderem für kleine Fensterdarstellungen verwendet.
    ICON_BIG wird unter anderem für Alt+Tab verwendet.
    """

    if sys.platform != "win32":
        return

    path = str(Path(icon_path).resolve())

    user32 = ctypes.WinDLL(
        "user32",
        use_last_error=True,
    )

    load_image = user32.LoadImageW
    load_image.argtypes = [
        wintypes.HINSTANCE,
        wintypes.LPCWSTR,
        wintypes.UINT,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.UINT,
    ]
    load_image.restype = wintypes.HANDLE

    send_message = user32.SendMessageW
    send_message.argtypes = [
        wintypes.HWND,
        wintypes.UINT,
        wintypes.WPARAM,
        wintypes.LPARAM,
    ]
    send_message.restype = ctypes.c_ssize_t

    small_icon = load_image(
        None,
        path,
        IMAGE_ICON,
        16,
        16,
        LR_LOADFROMFILE,
    )

    if not small_icon:
        error = ctypes.get_last_error()
        raise OSError(
            error,
            f"Das kleine Windows-Icon konnte nicht geladen werden: {path}",
        )

    big_icon = load_image(
        None,
        path,
        IMAGE_ICON,
        32,
        32,
        LR_LOADFROMFILE,
    )

    if not big_icon:
        error = ctypes.get_last_error()
        raise OSError(
            error,
            f"Das grosse Windows-Icon konnte nicht geladen werden: {path}",
        )

    send_message(
        wintypes.HWND(hwnd),
        WM_SETICON,
        ICON_SMALL,
        small_icon,
    )

    send_message(
        wintypes.HWND(hwnd),
        WM_SETICON,
        ICON_BIG,
        big_icon,
    )