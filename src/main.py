from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from core.permissions import ensure_elevated
from gui.main_window import MainWindow
from utils.paths import resource_path
from utils.version import AppInfo


def main() -> int:
    if sys.platform != "win32":
        print(
            "Dieses Programm ist ausschliesslich für Windows vorgesehen.",
            file=sys.stderr,
        )
        return 1

    if not ensure_elevated():
        return 0

    app = QApplication(sys.argv)

    app.setApplicationName(AppInfo.NAME)
    app.setApplicationVersion(AppInfo.VERSION)

    icon = QIcon(
        str(
            resource_path(
                "icons/WLAN-Manager_Icon.ico"
            )
        )
    )

    app.setWindowIcon(icon)

    try:
        window = MainWindow()
        window.setWindowIcon(icon)
        window.show()

        return app.exec()

    except Exception as exc:
        QMessageBox.critical(
            None,
            "Schwerer Fehler",
            f"Das Programm konnte nicht gestartet werden.\n\n{exc}",
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())