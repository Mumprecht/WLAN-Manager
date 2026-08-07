# Entwicklerhandbuch

## Projektpfad

```text
C:\Python-Projekte\WLAN-Manager
```

## Entwicklungsumgebung

- Windows 11
- Python
- PyCharm
- PySide6
- virtuelle Umgebung `.venv`

## Projektprinzipien

1. GUI und WLAN-Logik bleiben getrennt.
2. `netsh`-Aufrufe gehören ausschließlich in den Core-Bereich.
3. Wiederverwendbare Auswahlelemente werden als Widgets implementiert.
4. Dialoge enthalten nur UI-Logik und delegieren Fachlogik an `WlanManager`.
5. Versionsinformationen werden ausschließlich aus `VERSION` gelesen.
6. Jede Release-Version erhält einen Eintrag im `CHANGELOG.md`.

## Namenskonventionen

- Python-Dateien: `snake_case.py`
- Klassen: `PascalCase`
- Funktionen und Variablen: `snake_case`
- Konstanten: `UPPER_CASE`

## QSettings

QSettings speichert unter anderem:

- Fenstergeometrie
- Fensterzustand
- Spaltenbreiten
- Sortierung
- zuletzt verwendete Sicherungsordner
- zuletzt verwendete Wiederherstellungsordner

## Logging

Die Logging-Konfiguration befindet sich in:

```text
src/utils/logger.py
```

Fehler in GUI-Aktionen sollen zusätzlich protokolliert werden.

## Neue Funktionen

Bei neuen Funktionen ist folgende Reihenfolge einzuhalten:

1. Core-Funktion implementieren
2. Methode in `WlanManager` bereitstellen
3. GUI/Dialog implementieren
4. Testplan ergänzen
5. CHANGELOG ergänzen
6. Versionsnummer erhöhen

## Releases

Siehe `docs/RELEASE_PROCESS.md`.
