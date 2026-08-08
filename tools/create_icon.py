from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE = (
    PROJECT_ROOT
    / "src"
    / "resources"
    / "icons"
    / "WLAN-Manager_Icon.png"
)

TARGET = (
    PROJECT_ROOT
    / "src"
    / "resources"
    / "icons"
    / "WLAN-Manager_Icon.ico"
)

SIZES = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


def main() -> int:
    if not SOURCE.exists():
        print(f"Quelldatei nicht gefunden: {SOURCE}")
        return 1

    image = Image.open(SOURCE).convert("RGBA")

    if image.width != image.height:
        size = min(image.width, image.height)
        left = (image.width - size) // 2
        top = (image.height - size) // 2
        image = image.crop(
            (
                left,
                top,
                left + size,
                top + size,
            )
        )

    image.save(
        TARGET,
        format="ICO",
        sizes=SIZES,
    )

    print("ICO-Datei erfolgreich erstellt:")
    print(TARGET)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
