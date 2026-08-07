from pathlib import Path


class AppInfo:
    """Liest die Projektinformationen aus der Datei VERSION."""

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    VERSION_FILE = PROJECT_ROOT / "VERSION"

    _data = {}

    if VERSION_FILE.exists():
        for line in VERSION_FILE.read_text(encoding="utf-8").splitlines():

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                _data[key.strip()] = value.strip()

    NAME = _data.get("Name", "")
    VERSION = _data.get("Version", "")
    AUTHOR = _data.get("Author", "")
    COMPANY = _data.get("Company", "")
    COPYRIGHT = _data.get("Copyright", "")

    @classmethod
    def title(cls):
        return f"{cls.NAME} {cls.VERSION}"