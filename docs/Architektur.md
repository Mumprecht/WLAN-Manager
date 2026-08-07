# Architektur des WLAN-Managers

## Übersicht

Der WLAN-Manager verwendet eine klar getrennte Schichtenarchitektur:

```text
GUI
↓
MainWindow
↓
Dialogs / Widgets
↓
WlanManager
↓
Core-Module
↓
netsh.exe
```

## GUI

Die grafische Oberfläche basiert auf PySide6.

`src/gui/main_window.py` enthält das Hauptfenster, Menü, Toolbar, Statusleiste und die zentralen Benutzeraktionen.

## Dialoge

Die Dialoge kapseln komplexere Benutzerinteraktionen, z. B.:

- Sicherung mehrerer WLAN-Profile
- Wiederherstellung mehrerer XML-Profile
- Löschen mehrerer WLAN-Profile
- Konfliktbehandlung beim Überschreiben

## Widgets

Wiederverwendbare GUI-Komponenten befinden sich in `src/widgets`.

Beispiele:

- `ProfileSelectionWidget`
- `FolderSelector`

## WlanManager

`src/core/wlan_manager.py` bildet die Fassade zwischen GUI und Fachlogik.

Die GUI soll möglichst nicht direkt mit `netsh` arbeiten.

## Core

Die Core-Module enthalten die eigentliche WLAN-Logik:

- Profile lesen
- Passwörter auslesen
- Profile löschen
- Profile exportieren
- Profile importieren
- CSV erzeugen
- Verbindung herstellen
- aktuelle Verbindung auslesen

## netsh

Alle Windows-WLAN-Funktionen werden letztlich über `netsh.exe` ausgeführt.

Die Ausgabe von `netsh` wird sprach- und codierungsrobust verarbeitet.

## Versionierung

Die Datei `VERSION` im Projektstamm ist die zentrale Quelle für:

- Programmname
- Version
- Autor
- Firma
- Copyright

`src/utils/version.py` liest diese Datei über `AppInfo`.
