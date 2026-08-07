from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from tools.generate_version_info import generate, read_version


PROJECT_ROOT = Path(__file__).resolve().parent

ONEDIR_SPEC = PROJECT_ROOT / "WLAN-Manager.spec"
ONEFILE_SPEC = PROJECT_ROOT / "WLAN-Manager-OneFile.spec"

BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"

ONEDIR_EXE = DIST_DIR / "WLAN-Manager" / "WLAN-Manager.exe"
ONEFILE_EXE = DIST_DIR / "WLAN-Manager.exe"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build-Skript für den WLAN-Manager."
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--onedir",
        action="store_true",
        help="Nur den Onedir-Build erstellen.",
    )

    group.add_argument(
        "--onefile",
        action="store_true",
        help="Nur den OneFile-Build erstellen.",
    )

    return parser.parse_args()


def remove_old_builds() -> None:
    """Löscht alte Build- und Dist-Verzeichnisse."""
    for path in (BUILD_DIR, DIST_DIR):
        if path.exists():
            print(f"Lösche: {path}")
            shutil.rmtree(path)


def run_pyinstaller(spec_file: Path, label: str) -> None:
    """Startet PyInstaller mit der angegebenen Spec-Datei."""
    if not spec_file.exists():
        raise FileNotFoundError(
            f"Spec-Datei nicht gefunden: {spec_file}"
        )

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_file),
    ]

    print()
    print("-" * 72)
    print(f" {label}")
    print("-" * 72)
    print()
    print("PyInstaller wird gestartet:")
    print(
        " ".join(
            f'"{part}"' if " " in part else part
            for part in command
        )
    )
    print()

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
    )


def check_result(path: Path, label: str) -> bool:
    """Prüft, ob die erwartete EXE erzeugt wurde."""
    if path.exists():
        print(f"[OK] {label}")
        print(f"     {path}")
        return True

    print(f"[FEHLER] {label}")
    print(f"         Erwartete Datei nicht gefunden:")
    print(f"         {path}")
    return False


def main() -> int:
    args = parse_args()

    print("=" * 72)
    print(" WLAN-Manager – Release Build")
    print("=" * 72)
    print()

    try:
        version_data = read_version()
    except Exception as exc:
        print(f"FEHLER beim Lesen von VERSION: {exc}")
        return 1

    print(
        f"Baue {version_data['Name']} "
        f"Version {version_data['Version']}"
    )
    print()

    build_onedir = not args.onefile
    build_onefile = not args.onedir

    try:
        remove_old_builds()

        generated = generate()
        print(
            "Windows-Versionsinformation erzeugt: "
            f"{generated.name}"
        )

        if build_onedir:
            run_pyinstaller(
                ONEDIR_SPEC,
                "Onedir-Build",
            )

        if build_onefile:
            run_pyinstaller(
                ONEFILE_SPEC,
                "OneFile-Build",
            )

    except PermissionError as exc:
        print()
        print("FEHLER: Eine Datei oder ein Verzeichnis ist noch geöffnet.")
        print(
            "Bitte alle laufenden WLAN-Manager-Instanzen schließen "
            "und den Build erneut starten."
        )
        print()
        print(exc)
        return 1

    except subprocess.CalledProcessError as exc:
        print()
        print(
            "FEHLER: PyInstaller wurde mit "
            f"Code {exc.returncode} beendet."
        )
        return exc.returncode or 1

    except Exception as exc:
        print()
        print(f"FEHLER: {exc}")
        return 1

    print()
    print("=" * 72)
    print(" BUILD-ERGEBNIS")
    print("=" * 72)

    success = True

    if build_onedir:
        success &= check_result(
            ONEDIR_EXE,
            "Onedir-EXE",
        )

    if build_onefile:
        success &= check_result(
            ONEFILE_EXE,
            "OneFile-EXE",
        )

    print("=" * 72)

    if success:
        print()
        print("Build erfolgreich abgeschlossen.")
        return 0

    print()
    print("Build abgeschlossen, aber mindestens eine EXE fehlt.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
