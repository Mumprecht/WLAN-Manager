from __future__ import annotations

import csv
from pathlib import Path

from core.profiles import get_all_profile_details


def export_profiles_to_csv(csv_path: Path) -> int:
    rows = sorted(
        get_all_profile_details(),
        key=lambda row: row.ssid.casefold(),
    )

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(["SSID", "Authentifizierung", "Passwort"])

        for row in rows:
            writer.writerow(
                [row.ssid, row.authentication, row.password]
            )

    return len(rows)
