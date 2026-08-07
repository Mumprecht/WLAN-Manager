# Release-Prozess

## 1. Version festlegen

Die neue Versionsnummer wird in `VERSION` eingetragen.

Beispiel:

```text
Version=2.4.1
```

## 2. Änderungen dokumentieren

`CHANGELOG.md` ergänzen.

## 3. Dokumentation aktualisieren

Prüfen und gegebenenfalls anpassen:

- README.md
- Benutzerhandbuch.md
- Entwicklerhandbuch.md
- ROADMAP.md
- TODO.md
- TESTPLAN.md

## 4. Syntaxprüfung

Alle Python-Dateien müssen ohne Syntaxfehler kompilierbar sein.

## 5. Funktionstest

`docs/TESTPLAN.md` vollständig durchgehen.

## 6. Git Commit

Beispiel:

```powershell
git add .
git commit -m "Release v2.4.1"
```

## 7. Git Tag

```powershell
git tag -a v2.4.1 -m "WLAN-Manager v2.4.1"
```

## 8. Release-Paket

Erst nach bestandenem Testplan wird ein ZIP- oder EXE-Release erzeugt.
