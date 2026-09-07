from __future__ import annotations

import sys

from core.wlan_backend import WlanBackend


def create_wlan_backend() -> WlanBackend:
    """Erzeugt das WLAN-Backend für das aktuelle Betriebssystem."""

    if sys.platform == "win32":
        from platforms.windows.wlan_backend import WindowsWlanBackend

        return WindowsWlanBackend()

    if sys.platform.startswith("linux"):
        raise NotImplementedError(
            "Das Linux-WLAN-Backend ist noch nicht implementiert."
        )

    if sys.platform == "darwin":
        raise NotImplementedError(
            "Das macOS-WLAN-Backend ist noch nicht implementiert."
        )

    raise NotImplementedError(
        f"Das Betriebssystem '{sys.platform}' wird nicht unterstützt."
    )
