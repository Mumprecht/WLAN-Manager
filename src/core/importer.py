from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QCoreApplication

from core.netsh import require_success, run_netsh



def import_profile(xml_path: Path) -> None:
    if not xml_path.is_file():
        raise FileNotFoundError(QCoreApplication.translate("Importer", "Die Datei wurde nicht gefunden:\n{path}").format(path=xml_path))

    if xml_path.suffix.lower() != ".xml":
        raise ValueError(QCoreApplication.translate("Importer", "Es muss eine XML-Datei ausgewählt werden."))

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
        QCoreApplication.translate("Importer", "Das WLAN-Profil konnte nicht importiert werden."),
    )


def import_all_profiles(
    folder: Path,
) -> tuple[list[str], list[tuple[str, str]]]:
    if not folder.is_dir():
        raise FileNotFoundError(QCoreApplication.translate("Importer", "Der Ordner wurde nicht gefunden:\n{folder}").format(folder=folder))

    files = sorted(folder.glob("*.xml"), key=lambda path: path.name.casefold())

    if not files:
        raise FileNotFoundError(
            QCoreApplication.translate("Importer", "Im ausgewählten Ordner wurden keine XML-Dateien gefunden.")
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
