# WLAN-Manager Windows – Version 2.6.0

Zielprojekt:

```text
C:\Python-Projekte\WLAN-Manager
```

## Installation

Den Inhalt dieses Pakets in das bestehende PyCharm-Projekt kopieren.

Anschliessend im PyCharm-Terminal:

```powershell
cd C:\Python-Projekte\WLAN-Manager
python -m pip install --upgrade pip
pip install -r requirements.txt
python src\main.py
```

## Wichtige PyCharm-Einstellung

`src` als **Sources Root** markieren:

1. Rechtsklick auf `src`
2. `Mark Directory as`
3. `Sources Root`

## Funktionen

- WLAN-Profile anzeigen
- Passwörter anzeigen
- Profile löschen
- Einzelprofil exportieren
- Backup aller Profile
- Einzelprofil oder ganzen Ordner importieren
- CSV-Export
- aktuelle WLAN-Verbindung anzeigen
- automatische UAC-Anforderung

## Sicherheit

XML-Dateien mit `key=clear` und CSV-Dateien können WLAN-Passwörter im
Klartext enthalten.


## Versionierung

Die Datei `VERSION` ist die zentrale Quelle für Programmname, Version, Autor, Firma und Copyright.


## Backup-Dialog

Beim vollständigen WLAN-Backup können Basis-Zielordner und Backup-Ordnername
getrennt festgelegt werden. Der Ordnername wird mit Datum und Uhrzeit
vorgeschlagen, kann aber frei geändert werden. Der zuletzt verwendete
Basis-Zielordner wird gespeichert.


## Sicherung und Wiederherstellung ab Version 2.2.0

Die bisher getrennten Funktionen für Einzelprofil-Export und vollständiges
Backup wurden durch einen gemeinsamen Sicherungsdialog ersetzt. Dort können
ein, mehrere oder alle WLAN-Profile ausgewählt werden.

Wird "Neuen Backup-Unterordner mit Datum/Uhrzeit erzeugen" deaktiviert,
werden die ausgewählten Profile direkt in den gewählten bestehenden
Zielordner geschrieben. Dadurch können später einzelne Profile in denselben
Ordner nachgesichert werden.

Die Wiederherstellung verwendet ebenfalls einen gemeinsamen Dialog mit
Mehrfachauswahl der XML-Dateien.


## Nachsichern in bestehende Backup-Ordner

Wird beim Sichern kein neuer Unterordner erzeugt, können ausgewählte WLAN-Profile
direkt in einen bestehenden Backup-Ordner geschrieben werden. Falls dort bereits
eine XML-Datei für dasselbe WLAN-Profil existiert, fragt das Programm, ob sie
überschrieben, übersprungen oder der Vorgang abgebrochen werden soll. Die Auswahl
kann auf alle weiteren Konflikte angewendet werden.


## Mehrfaches Löschen von Profilen

Über `Profile > WLAN-Profile löschen...` können ein, mehrere oder alle
gespeicherten WLAN-Profile ausgewählt werden. Der Dialog unterstützt Suche,
Alle auswählen, Keine auswählen und Invertieren. Vor dem Löschen wird die
Auswahl nochmals zusammengefasst und muss bestätigt werden.


## Bedienkomfort ab Version 2.4.0

Fenstergröße, Fensterposition, Tabellen-Spaltenbreiten und Sortierung werden
automatisch gespeichert. Zusätzlich stehen Tastenkürzel für die wichtigsten
Funktionen zur Verfügung:

- F5: Aktualisieren
- Ctrl+S: Sichern
- Ctrl+R: Wiederherstellen
- Entf: Profile löschen
- Ctrl+P: Passwörter anzeigen
- Ctrl+I: Aktuelle Verbindung
- Ctrl+Enter: Verbinden
- Ctrl+Shift+S: CSV exportieren
- Ctrl+Q: Beenden
- F1: Über WLAN-Manager


## Dokumentation

Die Projektdokumentation befindet sich im Ordner `docs`:

- `Benutzerhandbuch.md`
- `Entwicklerhandbuch.md`
- `Architektur.md`
- `ROADMAP.md`
- `TODO.md`
- `TESTPLAN.md`
- `RELEASE_PROCESS.md`


## WLAN-QR-Code

Für ein gespeichertes WLAN-Profil kann über `Profile > QR-Code anzeigen...`
oder über das Rechtsklick-Menü ein Verbindungs-QR-Code erzeugt werden.

Der QR-Code kann:

- direkt angezeigt,
- als PNG gespeichert,
- als Bild in die Zwischenablage kopiert werden.

Das Passwort ist im Dialog standardmäßig maskiert.

Unterstützt werden offene WLANs, WEP sowie WPA/WPA2/WPA3-Personal.
Enterprise-WLANs werden derzeit nicht als QR-Code unterstützt.

Zusätzliche Abhängigkeit:

```powershell
python -m pip install -r requirements.txt
```


## Automatisierter Build

Ab Version 2.5.1 kann der komplette Onedir-Build mit einem Befehl erzeugt werden:

```powershell
python build.py
```

`build.py`:

1. liest die zentrale Datei `VERSION`,
2. löscht vorhandene `build`- und `dist`-Verzeichnisse,
3. erzeugt `version_info.py`,
4. startet PyInstaller mit `WLAN-Manager.spec`,
5. meldet den resultierenden EXE-Pfad.

Nur bereinigen:

```powershell
python clean.py
```

Die Datei `version_info.py` wird automatisch generiert und darf nicht manuell
gepflegt werden. Die einzige Quelle für Versions- und Herstellerinformationen
ist weiterhin `VERSION`.


## Integrierte Hilfe

Ab Version 2.5.2 öffnet `F1` das integrierte Benutzerhandbuch.

Das Menü `Hilfe` enthält:

- Benutzerhandbuch
- Projektinformationen
- Über WLAN-Manager

Das Benutzerhandbuch wird beim PyInstaller-Build mitgeliefert und funktioniert
dadurch auch aus der erzeugten EXE.

## Logdatei

Die Logdatei befindet sich nun unter:

```text
%LOCALAPPDATA%\Mumprecht Software\WLAN-Manager\logs\wlan_manager.log
```

Sie wird nicht mehr im Build- oder dist-Verzeichnis erzeugt.


## WLAN-Profile erstellen und bearbeiten

Ab Version 2.6.0 können gespeicherte WLAN-Profile nicht nur angezeigt,
gesichert, wiederhergestellt und gelöscht, sondern auch erstellt und bearbeitet
werden.

Menü:

```text
Profile > Neues WLAN-Profil...
Profile > WLAN-Profil bearbeiten...
```

Unterstützt werden:

- WPA2-Personal
- WPA3-Personal
- WPA-Personal
- offene WLANs

Enterprise-WLANs werden im Editor derzeit nicht unterstützt.
