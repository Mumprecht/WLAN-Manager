from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = PROJECT_ROOT / "VERSION"
OUTPUT_FILE = PROJECT_ROOT / "version_info.py"


def read_version() -> dict[str, str]:
    """Liest die zentrale Datei VERSION ein."""
    if not VERSION_FILE.exists():
        raise FileNotFoundError(
            f"VERSION-Datei wurde nicht gefunden: {VERSION_FILE}"
        )

    data: dict[str, str] = {}

    for line in VERSION_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()

    required = (
        "Version",
        "Name",
        "Author",
        "Company",
        "Copyright",
    )

    missing = [key for key in required if not data.get(key)]
    if missing:
        raise ValueError(
            "Folgende Einträge fehlen in VERSION: "
            + ", ".join(missing)
        )

    return data


def version_tuple(version: str) -> tuple[int, int, int, int]:
    """Wandelt z. B. 2.5.1 in (2, 5, 1, 0) um."""
    parts = version.split(".")

    if not 1 <= len(parts) <= 4:
        raise ValueError(
            f"Ungültige Versionsnummer: {version}"
        )

    try:
        numbers = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError(
            f"Ungültige Versionsnummer: {version}"
        ) from exc

    while len(numbers) < 4:
        numbers.append(0)

    return tuple(numbers[:4])


def escape_value(value: str) -> str:
    """Maskiert einfache Anführungszeichen für PyInstaller-Versionstexte."""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def create_version_file(data: dict[str, str]) -> str:
    version = version_tuple(data["Version"])

    company = escape_value(data["Company"])
    name = escape_value(data["Name"])
    copyright_text = escape_value(data["Copyright"])
    version_text = escape_value(data["Version"])

    return f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version},
    prodvers={version},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', '{company}'),
          StringStruct('FileDescription', '{name}'),
          StringStruct('FileVersion', '{version_text}'),
          StringStruct('InternalName', '{name}'),
          StringStruct('OriginalFilename', '{name}.exe'),
          StringStruct('ProductName', '{name}'),
          StringStruct('ProductVersion', '{version_text}'),
          StringStruct('LegalCopyright', '{copyright_text}')
        ]
      )
    ]),
    VarFileInfo([
      VarStruct('Translation', [1033, 1200])
    ])
  ]
)
"""


def generate() -> Path:
    """Erzeugt version_info.py und gibt den Pfad zurück."""
    data = read_version()
    OUTPUT_FILE.write_text(
        create_version_file(data),
        encoding="utf-8",
    )
    return OUTPUT_FILE


def main() -> int:
    output = generate()
    print(f"Erstellt: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
