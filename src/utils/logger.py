from __future__ import annotations

import logging

from utils.paths import log_dir


def configure_logging() -> logging.Logger:
    """Konfiguriert das zentrale Dateilogging des WLAN-Managers."""
    log_file = log_dir() / "wlan_manager.log"

    logger = logging.getLogger("wlan_manager")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = False

    logger.info("Logging gestartet: %s", log_file)

    return logger
