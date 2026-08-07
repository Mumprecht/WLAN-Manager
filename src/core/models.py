from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WlanProfile:
    ssid: str
    authentication: str = "-"
    password: str = "<nicht auslesbar>"

    @property
    def has_password(self) -> bool:
        return self.password not in {
            "",
            "<nicht auslesbar>",
            "<Fehler beim Auslesen>",
            "<offenes WLAN – kein Passwort>",
        }


@dataclass(slots=True)
class CurrentConnection:
    interface: str = ""
    status: str = ""
    ssid: str = ""
    bssid: str = ""
    radio_type: str = ""
    authentication: str = ""
    cipher: str = ""
    channel: str = ""
    receive_rate: str = ""
    transmit_rate: str = ""
    signal: str = ""
