from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QSettings

from utils.paths import resource_path


ORGANIZATION_NAME = "Mumprecht Software"
APPLICATION_NAME = "WLAN-Manager"
LANGUAGE_SETTING = "ui/language"
DEFAULT_LANGUAGE = "de"


@dataclass(frozen=True, slots=True)
class Language:
    code: str
    name: str


SUPPORTED_LANGUAGES = (
    Language("de", "Deutsch"),
    Language("en", "English"),
    Language("fr", "Français"),
    Language("it", "Italiano"),
)


def get_language() -> str:
    """Liest die gespeicherte Sprache."""
    settings = QSettings(
        ORGANIZATION_NAME,
        APPLICATION_NAME,
    )

    language = settings.value(
        LANGUAGE_SETTING,
        DEFAULT_LANGUAGE,
        type=str,
    )

    valid_codes = {
        item.code
        for item in SUPPORTED_LANGUAGES
    }

    if language not in valid_codes:
        return DEFAULT_LANGUAGE

    return language


def set_language(language: str) -> None:
    """Speichert die gewünschte Sprache."""
    valid_codes = {
        item.code
        for item in SUPPORTED_LANGUAGES
    }

    if language not in valid_codes:
        raise ValueError(
            f"Nicht unterstützte Sprache: {language}"
        )

    settings = QSettings(
        ORGANIZATION_NAME,
        APPLICATION_NAME,
    )

    settings.setValue(
        LANGUAGE_SETTING,
        language,
    )
    settings.sync()


def translation_file(language: str) -> Path:
    """
    Liefert den Pfad zur kompilierten Qt-Übersetzungsdatei (.qm).

    Deutsch ist die Quellsprache und benötigt keine eigene .qm-Datei.
    """
    return resource_path(
        f"translations/wlan_manager_{language}.qm"
    )
