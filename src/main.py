from __future__ import annotations

import sys

from PySide6.QtCore import QTimer, QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from core.permissions import ensure_elevated
from gui.main_window import MainWindow
from utils.language import get_language, translation_file
from utils.paths import resource_path
from utils.version import AppInfo
from utils.windows_icon import set_native_window_icon


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

    translator = QTranslator(app)
    language = get_language()

    if language != "de":
        qm_file = translation_file(language)

        if qm_file.exists():
            if translator.load(str(qm_file)):
                app.installTranslator(translator)

    icon_path = resource_path(
        "icons/WLAN-Manager_Icon.ico"
    )

    icon = QIcon(str(icon_path))
    app.setWindowIcon(icon)

    try:
        window = MainWindow()

        # Qt-Icon setzen.
        window.setWindowIcon(icon)

        # Fenster zuerst vollständig erzeugen und anzeigen.
        window.show()

        # Native Windows-Icons erst setzen, wenn das Fenster
        # bereits im Windows-Fenstersystem vorhanden ist.
        QTimer.singleShot(
            0,
            lambda: set_native_window_icon(
                int(window.winId()),
                icon_path,
            ),
        )

        # Sicherheitshalber nach kurzer Verzögerung nochmals setzen.
        # Zu diesem Zeitpunkt hat Windows auch den Taskleisten-
        # Eintrag vollständig aufgebaut.
        QTimer.singleShot(
            500,
            lambda: set_native_window_icon(
                int(window.winId()),
                icon_path,
            ),
        )

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
