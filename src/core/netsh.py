from __future__ import annotations

import locale
import re
import subprocess
from dataclasses import dataclass
from typing import Iterable


class NetshError(RuntimeError):
    pass


@dataclass(slots=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def combined(self) -> str:
        return "\n".join(part for part in (self.stdout, self.stderr) if part)


def _decode(data: bytes) -> str:
    encodings = [
        locale.getpreferredencoding(False),
        "utf-8",
        "cp850",
        "cp1252",
    ]
    seen: set[str] = set()

    for encoding in encodings:
        if not encoding or encoding.lower() in seen:
            continue
        seen.add(encoding.lower())
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass

    return data.decode("utf-8", errors="replace")


def run_netsh(arguments: Iterable[str]) -> CommandResult:
    completed = subprocess.run(
        ["netsh.exe", *list(arguments)],
        capture_output=True,
        check=False,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return CommandResult(
        returncode=completed.returncode,
        stdout=_decode(completed.stdout),
        stderr=_decode(completed.stderr),
    )


def require_success(result: CommandResult, message: str) -> str:
    if result.returncode != 0:
        details = result.combined.strip()
        raise NetshError(f"{message}\n\n{details}".strip())
    return result.combined


def looks_like_missing_wireless_interface(text: str) -> bool:
    patterns = (
        r"there is no wireless interface",
        r"keine drahtlosschnittstelle",
        r"keine wlan-schnittstelle",
    )
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def looks_like_location_permission_error(text: str) -> bool:
    patterns = (
        r"ms-settings:privacy-location",
        r"WlanQueryInterface.*(?:Fehler|error)\s*5",
        r"Zugriff verweigert",
        r"Access is denied",
    )
    return any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns)
