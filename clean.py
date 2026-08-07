from __future__ import annotations

import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

DIRECTORIES_TO_REMOVE = (
    PROJECT_ROOT / "build",
    PROJECT_ROOT / "dist",
)

FILES_TO_REMOVE = (
    PROJECT_ROOT / "version_info.py",
)


def remove_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
        print(f"Gelöscht: {path}")
    else:
        print(f"Nicht vorhanden: {path}")


def remove_file(path: Path) -> None:
    if path.exists():
        path.unlink()
        print(f"Gelöscht: {path}")
    else:
        print(f"Nicht vorhanden: {path}")


def main() -> int:
    print("WLAN-Manager – Build-Verzeichnisse bereinigen")
    print()

    for directory in DIRECTORIES_TO_REMOVE:
        remove_directory(directory)

    for file in FILES_TO_REMOVE:
        remove_file(file)

    print()
    print("Bereinigung abgeschlossen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
