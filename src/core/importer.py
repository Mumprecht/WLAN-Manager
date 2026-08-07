from __future__ import annotations

from pathlib import Path

from core.netsh import require_success, run_netsh


def import_profile(xml_path: Path) -> None:
    if not xml_path.is_file():
        raise FileNotFoundError(f"Die Datei wurde nicht gefunden:\n{xml_path}")

    if xml_path.suffix.lower() != ".xml":
        raise ValueError("Es muss eine XML-Datei ausgewählt werden.")

    result = run_netsh(
        [
            "wlan",
            "add",
            "profile",
            f"filename={xml_path}",
            "user=all",
        ]
    )

    require_success(
        result,
        "Das WLAN-Profil konnte nicht importiert werden.",
    )


def import_all_profiles(
    folder: Path,
) -> tuple[list[str], list[tuple[str, str]]]:
    if not folder.is_dir():
        raise FileNotFoundError(f"Der Ordner wurde nicht gefunden:\n{folder}")

    files = sorted(folder.glob("*.xml"), key=lambda path: path.name.casefold())

    if not files:
        raise FileNotFoundError(
            "Im ausgewählten Ordner wurden keine XML-Dateien gefunden."
        )

    successful: list[str] = []
    failed: list[tuple[str, str]] = []

    for path in files:
        try:
            import_profile(path)
            successful.append(path.name)
        except Exception as exc:
            failed.append((path.name, str(exc)))

    return successful, failed



def import_selected_profiles(
    files: list[Path],
) -> tuple[list[str], list[tuple[str, str]]]:
    """Importiert genau die ausgewählten XML-Dateien."""
    successful: list[str] = []
    failed: list[tuple[str, str]] = []

    for path in files:
        try:
            import_profile(path)
            successful.append(path.name)
        except Exception as exc:
            failed.append((path.name, str(exc)))

    return successful, failed
