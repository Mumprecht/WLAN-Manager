# WLAN-Manager für Windows

WLAN-Manager ist eine Windows-Anwendung zur komfortablen Verwaltung gespeicherter WLAN-Profile.

Die Anwendung bietet eine grafische Benutzeroberfläche auf Basis von Python und PySide6 und verwendet die Windows-WLAN-Funktionen zur Verwaltung der Profile.

## Funktionen

Der WLAN-Manager unterstützt unter anderem:

* gespeicherte WLAN-Profile anzeigen
* WLAN-Passwörter anzeigen
* Inhalte einzelner Tabellenzellen kopieren
* aktuelle WLAN-Verbindung anzeigen
* mit einem gespeicherten WLAN-Profil verbinden
* neue WLAN-Profile erstellen
* vorhandene WLAN-Profile bearbeiten
* ein, mehrere oder alle WLAN-Profile sichern
* WLAN-Profile aus XML-Dateien wiederherstellen
* ein, mehrere oder alle WLAN-Profile löschen
* WLAN-Daten als CSV exportieren
* WLAN-QR-Codes erzeugen, speichern und kopieren
* integriertes Benutzerhandbuch anzeigen
* Projekt- und Versionsinformationen anzeigen
* automatische Anforderung der erforderlichen Administratorrechte
* benutzerbezogene Protokollierung unter `%LOCALAPPDATA%`

## Sprachen

Die Benutzeroberfläche und das Benutzerhandbuch stehen in folgenden Sprachen zur Verfügung:

* Deutsch
* Englisch
* Französisch
* Italienisch

## Installation für Anwender

Für die Verwendung der fertigen Windows-Version sind weder Python noch PyCharm oder eine andere Entwicklungsumgebung erforderlich.

Die aktuelle Programmversion kann über die **Releases** dieses GitHub-Repositorys heruntergeladen werden.

Nach dem Download kann die bereitgestellte Windows-EXE direkt gestartet werden.

> **Hinweis:** WLAN-Manager benötigt für bestimmte Funktionen Administratorrechte. Die erforderliche Rechteerhöhung wird bei Bedarf automatisch angefordert.

## WLAN-Profile anzeigen

Nach dem Programmstart werden die gespeicherten WLAN-Profile in einer Tabelle angezeigt.

Die Liste kann mit `F5` aktualisiert werden.

### Inhalte kopieren

Der Inhalt einer Tabellenzelle kann mit `Ctrl+C` in die Zwischenablage kopiert werden.

Alternativ kann mit der rechten Maustaste auf eine Zelle geklickt und im Kontextmenü `Kopieren` gewählt werden. Dabei wird der Inhalt der angeklickten Zelle kopiert.

## WLAN-Passwörter

Gespeicherte WLAN-Passwörter können im Klartext angezeigt werden.

Menü:

```text
WLAN > Passwörter anzeigen
```

Tastenkürzel:

```text
Ctrl+P
```

## Aktuelle WLAN-Verbindung

Informationen zur aktuellen WLAN-Verbindung können angezeigt werden über:

```text
WLAN > Aktuelle Verbindung
```

Tastenkürzel:

```text
Ctrl+I
```

## Mit einem WLAN verbinden

Ein gespeichertes WLAN-Profil kann durch Doppelklick verbunden werden.

Alternativ:

```text
Profile > Verbinden
```

oder:

```text
Ctrl+Enter
```

## WLAN-Profile erstellen und bearbeiten

Neue WLAN-Profile können angelegt und vorhandene Profile bearbeitet werden.

Menü:

```text
Profile > Neues WLAN-Profil...
Profile > WLAN-Profil bearbeiten...
```

Unterstützt werden insbesondere:

* WPA2-Personal
* WPA3-Personal
* WPA-Personal
* offene WLANs

Enterprise-WLANs werden im Editor derzeit nicht unterstützt.

Beim Bearbeiten vorhandener Profile werden der vorhandene Gültigkeitsbereich und die Windows-Sicherheitskonfiguration soweit erforderlich beibehalten.

Durch Gruppenrichtlinien verwaltete WLAN-Profile sind schreibgeschützt und können nicht bearbeitet werden.

## WLAN-Profile sichern

Über:

```text
Datei > WLAN-Profile sichern...
```

können ein, mehrere oder alle WLAN-Profile ausgewählt und gesichert werden.

Basis-Zielordner und Backup-Ordnername können getrennt festgelegt werden. Für einen neuen Backup-Ordner wird ein Name mit Datum und Uhrzeit vorgeschlagen.

Wird die Option zum Erzeugen eines neuen Backup-Unterordners deaktiviert, werden die ausgewählten Profile direkt in den gewählten bestehenden Zielordner geschrieben. Dadurch können einzelne Profile später in denselben Backup-Ordner nachgesichert werden.

Existiert dort bereits eine XML-Datei für dasselbe WLAN-Profil, stehen folgende Möglichkeiten zur Verfügung:

* Überschreiben
* Überspringen
* Abbrechen

Die gewählte Behandlung kann auf weitere Konflikte angewendet werden.

## WLAN-Profile wiederherstellen

Über:

```text
Datei > WLAN-Profile wiederherstellen...
```

können ein, mehrere oder alle WLAN-Profile aus XML-Dateien wiederhergestellt werden.

Der Wiederherstellungsdialog unterstützt die Mehrfachauswahl von XML-Dateien.

## WLAN-Profile löschen

Über:

```text
Profile > WLAN-Profile löschen...
```

können ein, mehrere oder alle gespeicherten WLAN-Profile ausgewählt werden.

Der Dialog unterstützt:

* Suche
* Alle auswählen
* Keine auswählen
* Auswahl invertieren

Vor dem Löschen wird die Auswahl zusammengefasst und muss bestätigt werden.

## CSV-Export

WLAN-Daten können exportiert werden über:

```text
Datei > CSV exportieren...
```

Die CSV-Datei kann WLAN-Passwörter im Klartext enthalten.

## WLAN-QR-Code

Für ein gespeichertes WLAN-Profil kann über:

```text
Profile > QR-Code anzeigen...
```

oder über das Rechtsklick-Menü ein Verbindungs-QR-Code erzeugt werden.

Der QR-Code kann:

* direkt angezeigt,
* als PNG gespeichert,
* als Bild in die Zwischenablage kopiert werden.

Das Passwort ist im Dialog standardmäßig maskiert.

Unterstützt werden offene WLANs, WEP sowie WPA/WPA2/WPA3-Personal.

Enterprise-WLANs werden derzeit nicht als QR-Code unterstützt.

## Tastenkürzel

* `F5` – Aktualisieren
* `Ctrl+C` – Inhalt der ausgewählten Tabellenzelle kopieren
* `Ctrl+S` – Sichern
* `Ctrl+R` – Wiederherstellen
* `Entf` – Profile löschen
* `Ctrl+P` – Passwörter anzeigen
* `Ctrl+I` – Aktuelle Verbindung
* `Ctrl+Enter` – Verbinden
* `Ctrl+Shift+S` – CSV exportieren
* `Ctrl+Q` – Beenden
* `F1` – Benutzerhandbuch

## Integrierte Hilfe

Mit `F1` wird das integrierte Benutzerhandbuch geöffnet.

Das Menü `Hilfe` enthält:

* Benutzerhandbuch
* Projektinformationen
* Über WLAN-Manager

Das Benutzerhandbuch wird beim PyInstaller-Build mitgeliefert und steht dadurch auch in der erzeugten EXE zur Verfügung.

## Logdatei

Die Logdatei wird benutzerbezogen gespeichert:

```text
%LOCALAPPDATA%\Mumprecht Software\WLAN-Manager\logs\wlan_manager.log
```

Jeder Windows-Benutzer erhält dadurch sein eigenes Logverzeichnis.

Die Logdatei wird nicht im Build-, Dist- oder Programmverzeichnis erzeugt.

## Sicherheit

WLAN-Manager kann auf sensible WLAN-Konfigurationsdaten zugreifen.

Insbesondere können folgende Dateien vertrauliche Informationen enthalten:

* Backup-XML-Dateien mit WLAN-Schlüsseln im Klartext
* CSV-Exporte mit WLAN-Passwörtern
* erzeugte WLAN-QR-Codes

Auch kopierte WLAN-Passwörter befinden sich nach dem Kopieren in der Windows-Zwischenablage.

Diese Daten sollten entsprechend geschützt und nicht unkontrolliert weitergegeben werden.

## Entwicklung

### Voraussetzungen

Für die Entwicklung werden benötigt:

* Windows
* Python
* Git
* die in `requirements.txt` aufgeführten Python-Pakete

Eine Entwicklungsumgebung wie PyCharm oder Visual Studio Code kann optional verwendet werden.

### Repository klonen

```powershell
git clone https://github.com/Mumprecht/WLAN-Manager.git
cd WLAN-Manager
```

### Virtuelle Python-Umgebung erstellen

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Abhängigkeiten installieren

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Anwendung aus dem Quellcode starten

```powershell
python src\main.py
```

## Versionierung

Die Datei `VERSION` ist die zentrale Quelle für:

* Programmname
* Versionsnummer
* Autor
* Firma
* Copyright

Die Datei `version_info.py` wird für den Windows-Build automatisch erzeugt und darf nicht manuell gepflegt werden.

## Build

Der Build wird über `build.py` erzeugt:

```powershell
python build.py
```

Der Build-Prozess:

1. liest die zentrale Datei `VERSION`,
2. löscht vorhandene Build-Artefakte,
3. erzeugt `version_info.py`,
4. startet PyInstaller,
5. erzeugt die vorgesehenen Distributionen,
6. meldet die resultierenden EXE-Pfade.

Nur die Build-Verzeichnisse bereinigen:

```powershell
python clean.py
```

Weitere Informationen zum Build und zum Release-Prozess befinden sich in der Projektdokumentation.

## Dokumentation

Die Projektdokumentation befindet sich im Verzeichnis `docs`.

Dazu gehören unter anderem:

* `Benutzerhandbuch.md`
* `Benutzerhandbuch_en.md`
* `Benutzerhandbuch_fr.md`
* `Benutzerhandbuch_it.md`
* `Entwicklerhandbuch.md`
* `Architektur.md`
* `BUILD.md`
* `ROADMAP.md`
* `TODO.md`
* `TESTPLAN.md`
* `RELEASE.md`
* `RELEASE_PROCESS.md`

## Lizenz

WLAN-Manager ist proprietäre Software und darf im Rahmen der **WLAN-Manager Non-Commercial License, Version 1.0** kostenlos für private und andere nicht-kommerzielle Zwecke verwendet werden.

Copyright © 2026 Urs Mumprecht / Mumprecht Software.

Kommerzielle Nutzung, Veränderung, Weiterverteilung, Wiederveröffentlichung oder die Erstellung abgeleiteter Werke ist ohne vorherige schriftliche Zustimmung des Rechteinhabers nicht gestattet.

Die vollständigen Lizenzbedingungen befinden sich in der Datei `LICENSE`.

**Lizenz:** WLAN-Manager Non-Commercial License, Version 1.0
