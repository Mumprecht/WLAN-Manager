# GitHub-Anleitung – Neue WLAN-Manager-Version veröffentlichen

Diese Anleitung beschreibt den Standardablauf, wenn eine neue Version des WLAN-Managers entwickelt, getestet, mit Git versioniert und auf GitHub veröffentlicht wird.

Repository:

```text
https://github.com/Mumprecht/WLAN-Manager
```

Lokales Projektverzeichnis:

```text
C:\Python-Projekte\WLAN-Manager
```

## 1. Grundprinzip

Für jede veröffentlichte Version gilt:

1. Änderungen entwickeln.
2. Neue Version vollständig testen.
3. Versionsnummer und Änderungsprotokoll aktualisieren.
4. Release-Build erzeugen.
5. Änderungen mit Git committen.
6. Einen Git-Tag für die Version erstellen.
7. Commit und Tag zu GitHub übertragen.
8. Auf GitHub einen Release aus dem vorhandenen Tag erstellen.
9. Die fertige `WLAN-Manager.exe` als Release-Datei hochladen.
10. Den veröffentlichten Release danach nicht mehr verändern.

Beispiel:

```text
Version: 2.6.2
Git-Tag: v2.6.2
Release-Titel: WLAN-Manager v2.6.2
```

## 2. Projekt öffnen und virtuelle Umgebung aktivieren

PowerShell öffnen:

```powershell
cd C:\Python-Projekte\WLAN-Manager
.\.venv\Scripts\Activate.ps1
```

Danach sollte der Prompt ungefähr so aussehen:

```text
(.venv) PS C:\Python-Projekte\WLAN-Manager>
```

Zur Kontrolle:

```powershell
python --version
where.exe python
```

Der erste Python-Pfad sollte aus `.venv` stammen.

## 3. Vor Beginn einer neuen Version Git prüfen

Vor neuen Änderungen:

```powershell
git status
```

Ideal:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

Zusätzlich:

```powershell
git log --oneline --decorate -5
```

## 4. Neue Version entwickeln

Die gewünschten Änderungen durchführen und während der Entwicklung testen:

```powershell
python src\main.py
```

Noch keinen Release-Tag setzen.

## 5. Versionsnummer aktualisieren

Die zentrale Versionsdatei ist:

```text
<Projektordner>\VERSION
```

Beispiel:

```text
Version=X.Y.Z
Name=WLAN-Manager
Author=Urs Mumprecht
Company=Mumprecht Software
Copyright=2026 Urs Mumprecht
```

`build.py` liest diese Versionsnummer und erzeugt daraus die Windows-Versionsinformationen für die EXE.

## 6. CHANGELOG aktualisieren

Die Datei `CHANGELOG.md` wird ergänzt. Der neue Abschnitt steht oben; frühere Einträge bleiben erhalten.

Beispiel:

```markdown
# Änderungsprotokoll

## X.Y.Z – TT.MM.JJJJ

- Neue Funktion A ergänzt.
- Bedienung von Funktion B verbessert.
- Fehler C korrigiert.

## 2.6.2 – 08.08.2026

...
```

## 7. Dokumentation und Abhängigkeiten prüfen

Je nach Änderung prüfen bzw. anpassen:

```text
README.md
docs\Benutzerhandbuch.md
docs\TESTPLAN.md
docs\RELEASE.md
requirements.txt
requirements-build.txt
requirements-dev.txt
requirements-lock.txt
```

Neue Python-Abhängigkeiten gehören in die passende Requirements-Datei.

## 8. Release-Build erzeugen

Alle laufenden WLAN-Manager-Instanzen schließen.

Dann:

```powershell
python clean.py
python build.py
```

Der Build erzeugt:

### OneFile

```text
C:\Python-Projekte\WLAN-Manager\dist\WLAN-Manager.exe
```

Diese Datei wird normalerweise auf GitHub als Release-Asset veröffentlicht.

### Onedir

```text
C:\Python-Projekte\WLAN-Manager\dist\WLAN-Manager\WLAN-Manager.exe
```

Diese Variante benötigt den gesamten Ordner einschließlich `_internal`.

## 9. Release-Build testen

Vor dem Git-Commit mindestens prüfen:

- Programm startet.
- Versionsnummer stimmt.
- WLAN-Profile werden angezeigt.
- Sicherung funktioniert.
- Wiederherstellung funktioniert.
- Löschen funktioniert.
- Passwortanzeige funktioniert.
- Profil erstellen/bearbeiten funktioniert.
- QR-Code funktioniert.
- Hilfe/F1 funktioniert.
- Projektinformationen stimmen.
- Programmsymbol ist korrekt.
- OneFile-EXE funktioniert außerhalb des Projektverzeichnisses.

## 10. Git-Status prüfen

```powershell
git status
```

Optional kompakt:

```powershell
git status --short
```

Temporäre Testdateien, Build-Verzeichnisse oder lokale IDE-Dateien sollen nicht in den Release-Commit gelangen.

## 11. Änderungen vormerken

Wenn alle Änderungen zum Release gehören:

```powershell
git add .
```

Bei kleinen Releases können auch gezielt Dateien vorgemerkt werden:

```powershell
git add CHANGELOG.md
git add VERSION
git add src\core\profile_editor.py
```

Danach:

```powershell
git status
```

Unter `Changes to be committed:` dürfen nur die gewünschten Release-Dateien stehen.

## 12. Release-Commit erstellen

Beispiel:

```powershell
git commit -m "Release vX.Y.Z"
```

Danach:

```powershell
git status
git log --oneline --decorate -5
```

## 13. Git-Tag erstellen

Erst nach dem vollständigen Release-Commit:

```powershell
git tag -a vX.Y.Z -m "Release WLAN-Manager vX.Y.Z"
```

Kontrolle:

```powershell
git log --oneline --decorate -5
```

Beispiel:

```text
abc1234 (HEAD -> main, tag: vX.Y.Z) Release vX.Y.Z
```

Ein Git-Tag markiert einen bestimmten Commit.

## 14. Commit zu GitHub übertragen

```powershell
git push
```

Kontrolle:

```powershell
git status
```

Ideal:

```text
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

## 15. Release-Tag zu GitHub übertragen

Tags werden separat gepusht:

```powershell
git push origin vX.Y.Z
```

## 16. GitHub Release erstellen

Im Browser das Repository öffnen und zu `Releases` gehen.

Dann:

```text
Create a new release
```

### Tag

Den bereits hochgeladenen Tag auswählen:

```text
vX.Y.Z
```

### Release-Titel

```text
WLAN-Manager vX.Y.Z
```

### Release Notes

Kurz die wichtigsten Änderungen für Anwender zusammenfassen.

Beispiel:

```markdown
## WLAN-Manager vX.Y.Z

### Wichtigste Änderungen

- Neue Funktion A.
- Verbesserung B.
- Fehler C behoben.

### Download

Für Windows die Datei `WLAN-Manager.exe` unter Assets herunterladen und starten.
```

## 17. EXE als Release-Asset hochladen

Auf der Release-Seite unter `Attach binaries` diese Datei auswählen:

```text
C:\Python-Projekte\WLAN-Manager\dist\WLAN-Manager.exe
```

Nicht die Onedir-EXE einzeln hochladen.

## 18. Release veröffentlichen

Vorher prüfen:

```text
Tag:            vX.Y.Z
Release title:  WLAN-Manager vX.Y.Z
Release notes:  vorhanden
Asset:          WLAN-Manager.exe
Pre-release:    Nein
Latest:         bei aktueller Produktivversion Ja
```

Dann `Publish release`.

## 19. Abschlusskontrolle

Nach der Veröffentlichung:

```powershell
git status
git log --oneline --decorate -5
```

Auf GitHub prüfen:

- Release sichtbar
- Tag korrekt
- Commit korrekt
- `WLAN-Manager.exe` unter Assets vorhanden
- Download funktioniert
- heruntergeladene EXE startet

## 20. Patch-Release

Bei einem Fehler in einer bereits veröffentlichten Version wird der alte Release nicht verändert.

Beispiel:

```text
2.6.0 → Fehler gefunden
2.6.1 → Bugfix
```

Ablauf:

```text
VERSION ändern
CHANGELOG ergänzen
Fehler korrigieren
testen
bauen
committen
taggen
pushen
neuen GitHub Release erstellen
```

Der alte Tag bleibt unverändert.

## 21. Häufige Git-Befehle

```powershell
git status
git status --short
git log --oneline --decorate -5
git tag
git remote -v
git add .
git commit -m "Release vX.Y.Z"
git tag -a vX.Y.Z -m "Release WLAN-Manager vX.Y.Z"
git push
git push origin vX.Y.Z
```

## 22. Tag versehentlich zu früh erstellt

Solange der Tag noch nicht veröffentlicht wurde:

```powershell
git tag -d vX.Y.Z
```

Danach den richtigen Commit erstellen und den Tag neu setzen:

```powershell
git tag -a vX.Y.Z -m "Release WLAN-Manager vX.Y.Z"
```

Bei bereits veröffentlichten Releases besser eine neue Versionsnummer verwenden.

## 23. Remote-Verbindung prüfen

```powershell
git remote -v
```

Erwartet:

```text
origin  https://github.com/Mumprecht/WLAN-Manager.git (fetch)
origin  https://github.com/Mumprecht/WLAN-Manager.git (push)
```

## 24. Git-Benutzerinformationen prüfen

```powershell
git config --global user.name
git config --global user.email
```

Falls nötig:

```powershell
git config --global user.name "Mumprecht Urs"
git config --global user.email "urs@mumprecht.ch"
```

## 25. Kurzablauf für jeden Release

```powershell
cd C:\Python-Projekte\WLAN-Manager
.\.venv\Scripts\Activate.ps1

git status

# VERSION und CHANGELOG aktualisieren
# Änderungen testen

python clean.py
python build.py

# Release-EXE testen

git status
git add .
git status
git commit -m "Release vX.Y.Z"

git tag -a vX.Y.Z -m "Release WLAN-Manager vX.Y.Z"

git push
git push origin vX.Y.Z

git status
git log --oneline --decorate -5
```

Danach auf GitHub:

```text
Releases
→ Create a new release
→ vorhandenen Tag vX.Y.Z auswählen
→ Release-Titel eintragen
→ Release Notes eintragen
→ dist\WLAN-Manager.exe hochladen
→ Publish release
```

## 26. Merksatz

```text
Entwickeln
→ Testen
→ VERSION
→ CHANGELOG
→ Build
→ EXE testen
→ Git add
→ Commit
→ Tag
→ Push
→ Tag pushen
→ GitHub Release
→ EXE hochladen
→ Veröffentlichen
```
