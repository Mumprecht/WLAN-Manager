# Build-Anleitung

## Voraussetzungen

Die virtuelle Umgebung muss aktiviert sein und die Build-Abhängigkeiten müssen
installiert sein:

```powershell
python -m pip install -r requirements-build.txt
```

## Onedir-Build

Im Projektverzeichnis:

```powershell
python build.py
```

Der Build-Prozess liest die zentrale Datei `VERSION`, erzeugt daraus die
Windows-Dateiversionsinformationen und startet anschließend PyInstaller.

Die fertige EXE befindet sich standardmäßig unter:

```text
dist\WLAN-Manager\WLAN-Manager.exe
```

## Bereinigen

```powershell
python clean.py
```

Dabei werden gelöscht:

- `build`
- `dist`
- die generierte Datei `version_info.py`

## Versionspflege

Ausschließlich die Datei `VERSION` wird manuell gepflegt.

Beispiel:

```text
Version=2.5.1
Name=WLAN-Manager
Author=Urs Mumprecht
Company=Mumprecht Software
Copyright=2026 Urs Mumprecht
```

`version_info.py` wird bei jedem Build automatisch neu erzeugt.


## Mitgelieferte Datendateien

Die PyInstaller-Spec-Datei bindet folgende Datendateien ein:

- `VERSION`
- `docs\Benutzerhandbuch.md`

Dadurch funktionieren Versionsanzeige und integrierte Hilfe auch aus dem
PyInstaller-Build.
