from __future__ import annotations

import ctypes
import subprocess
import sys
from pathlib import Path


def is_administrator() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def ensure_elevated() -> bool:
    if is_administrator():
        return True

    executable = sys.executable

    if getattr(sys, "frozen", False):
        arguments = subprocess.list2cmdline(sys.argv[1:])
        working_directory = str(Path(executable).resolve().parent)
    else:
        script = str(Path(sys.argv[0]).resolve())
        arguments = subprocess.list2cmdline([script, *sys.argv[1:]])
        working_directory = str(Path(script).parent)

    result = ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        executable,
        arguments,
        working_directory,
        1,
    )

    return False if result <= 32 else False
