# Release-Prozess -- WLAN-Manager

Dieses Dokument beschreibt den verbindlichen Ablauf für die Erstellung,
Prüfung, Versionierung und Veröffentlichung eines Releases des
WLAN-Managers.

## 1. Grundsatz

Ein veröffentlichter Release wird nachträglich nicht verändert.
Änderungen am Programm, an Build-Dateien oder an der Dokumentation
werden nach einem veröffentlichten Release in einem neuen Commit und --
sofern es sich um eine neue Veröffentlichung handelt -- unter einer
neuen Versionsnummer vorgenommen.

Referenz-Release: - Version: `2.5.2` - Git-Tag: `v2.5.2` - Git-Commit:
`f760b91` - Branch: `main` - Remote: `origin` - GitHub-Repository:
`Mumprecht/WLAN-Manager` - Status: veröffentlicht und eingefroren

## 2. Entwicklung abschließen

Vor einem Release müssen die vorgesehenen Änderungen vollständig
implementiert und die betroffenen Funktionen getestet sein. Dazu gehören
insbesondere Programmstart, WLAN-Profilverwaltung, Sicherung und
Wiederherstellung, Löschen, Passwortanzeige, QR-Code, Hilfe,
Projektinformationen und Logging.

## 3. Versionsnummer aktualisieren

Die zentrale Datei `VERSION` wird auf die neue Version gesetzt:

``` text
Version=2.6.0
Name=WLAN-Manager
Author=Urs Mumprecht
Company=Mumprecht Software
Copyright=2026 Urs Mumprecht
```

`VERSION` ist die zentrale Quelle für die Release-Version.

## 4. Dokumentation aktualisieren

Vor dem Build sind mindestens zu prüfen: - `CHANGELOG.md` -
`README.md` - `docs/Benutzerhandbuch.md` - `docs/BUILD.md` -
`docs/TESTPLAN.md` - `docs/RELEASE.md`

## 5. Release-Build erstellen

Alle laufenden WLAN-Manager-Instanzen schließen und im
Projektverzeichnis ausführen:

``` powershell
cd C:\Python-Projekte\WLAN-Manager
python clean.py
python build.py
```

Standardmäßig werden Onedir und OneFile gebaut.

Onedir:

``` text
C:\Python-Projekte\WLAN-Manager\dist\WLAN-Manager\WLAN-Manager.exe
```

Die Onedir-EXE benötigt den zugehörigen Verzeichnisbaum einschließlich
`_internal`.

OneFile:

``` text
C:\Python-Projekte\WLAN-Manager\dist\WLAN-Manager.exe
```

Diese EXE ist für die einfache Weitergabe vorgesehen.

Nur Onedir:

``` powershell
python build.py --onedir
```

Nur OneFile:

``` powershell
python build.py --onefile
```

## 6. Release-Build testen

Mindestens prüfen: - Programm startet - korrekte Versionsnummer -
Windows-Dateieigenschaften korrekt - `F1` öffnet das Benutzerhandbuch -
`Hilfe > Benutzerhandbuch` - `Hilfe > Projektinformationen` -
`Hilfe > Über WLAN-Manager` - QR-Code - Sicherung und
Wiederherstellung - Passwortanzeige - Löschen - Logging

Logverzeichnis:

``` text
%LOCALAPPDATA%\Mumprecht Software\WLAN-Manager\logs
```

Die OneFile-EXE zusätzlich an einen anderen Ort, z. B. auf den Desktop,
kopieren und dort starten.

## 7. Git-Status prüfen

``` powershell
git status
```

Alle zum Release gehörenden Änderungen müssen berücksichtigt sein.

## 8. Release committen

``` powershell
git add .
git commit -m "Release vX.Y.Z"
git status
```

Erwartet:

``` text
nothing to commit, working tree clean
```

## 9. Git-Tag setzen

Erst nach dem vollständigen Release-Commit:

``` powershell
git tag -a vX.Y.Z -m "Release WLAN-Manager vX.Y.Z"
git log --oneline --decorate -5
```

## 10. Zu GitHub übertragen

``` powershell
git push
git push origin vX.Y.Z
```

Danach:

``` powershell
git status
git log --oneline --decorate -5
```

## 11. GitHub Release erstellen

1.  Im Repository `Mumprecht/WLAN-Manager` den Bereich **Releases**
    öffnen.
2.  Neuen Release erstellen.
3.  Den bereits vorhandenen Tag `vX.Y.Z` auswählen.
4.  Release-Titel setzen, z. B. `WLAN-Manager v2.6.0`.
5.  Release Notes eintragen.
6.  `dist\WLAN-Manager.exe` (OneFile) als Asset hochladen.
7.  Einen produktiven Release nicht als Pre-release markieren.
8.  Release veröffentlichen.

GitHub stellt zusätzlich automatisch ZIP- und TAR.GZ-Archive des
Quellcodes bereit.

## 12. Abschlusskontrolle

Nach Veröffentlichung prüfen: - Release sichtbar - korrekter Tag und
Commit - `WLAN-Manager.exe` unter Assets - EXE kann heruntergeladen
werden - heruntergeladene EXE startet - Versionsanzeige stimmt

## 13. Release einfrieren

Nach erfolgreicher Veröffentlichung gilt der Release als eingefroren.
Der Tag wird nicht auf einen späteren Commit verschoben und das Programm
wird nicht unter derselben Versionsnummer durch veränderten Code
ersetzt.

Nachfolgende Änderungen erfolgen als neue Entwicklung und erhalten beim
nächsten Release eine neue Versionsnummer.

## 14. Kurz-Checkliste

``` text
[ ] Entwicklung abgeschlossen
[ ] Funktionen getestet
[ ] VERSION aktualisiert
[ ] CHANGELOG aktualisiert
[ ] Dokumentation geprüft
[ ] python clean.py
[ ] python build.py
[ ] Onedir getestet
[ ] OneFile getestet
[ ] OneFile außerhalb dist getestet
[ ] git status geprüft
[ ] git add .
[ ] Release-Commit erstellt
[ ] git status = clean
[ ] Release-Tag erstellt
[ ] git push
[ ] Release-Tag zu GitHub gepusht
[ ] GitHub Release erstellt
[ ] WLAN-Manager.exe hochgeladen
[ ] Release veröffentlicht
[ ] veröffentlichte EXE getestet
[ ] Release eingefroren
```

## 15. Referenz: Release v2.5.2

``` text
Version:        2.5.2
Commit:         f760b91
Tag:            v2.5.2
Branch:         main
Remote:         origin
Repository:     Mumprecht/WLAN-Manager
Build:          Onedir und OneFile
GitHub Release: veröffentlicht
Status:         eingefroren
```

`docs/RELEASE.md` wurde erst nach dem Einfrieren von `v2.5.2` erstellt.
Sie gehört deshalb bewusst zum nachfolgenden Git-Stand und nicht mehr
zum veröffentlichten Commit `f760b91`.
