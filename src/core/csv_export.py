from __future__ import annotations

import csv
from pathlib import Path

from PySide6.QtCore import QCoreApplication

from core.profile_display import (
    authentication_display_text,
    password_display_text,
)
from core.profiles import get_all_profile_details



def export_profiles_to_csv(csv_path: Path) -> int:
    rows = sorted(
        get_all_profile_details(),
        key=lambda row: row.ssid.casefold(),
    )

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(
            [
                "SSID",
                QCoreApplication.translate("CsvExport", "Authentifizierung"),
                QCoreApplication.translate("CsvExport", "Passwort"),
            ]
        )

        for row in rows:
            writer.writerow(
                [
                    row.ssid,
                    authentication_display_text(row),
                    password_display_text(row),
                ]
            )

    return len(rows)
