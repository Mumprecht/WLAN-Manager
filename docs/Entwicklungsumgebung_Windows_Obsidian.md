# Entwicklungsumgebung unter Windows einrichten

> Praxisleitfaden für eine einheitliche Entwicklungsumgebung mit Python,
> PowerShell, PyCharm, Visual Studio Code, Git und GitHub.

## 1. Ziel

Auf einem Windows-11-Rechner wird eine einheitliche Entwicklungsumgebung
eingerichtet für:

-   Python
-   PowerShell 7
-   PyCharm
-   Visual Studio Code
-   Git
-   GitHub
-   strukturierte Projektablagen
-   virtuelle Python-Umgebungen
-   Dokumentation und Releases

Ein Projekt wird nur einmal gespeichert und kann wahlweise mit PyCharm,
Visual Studio Code oder PowerShell bearbeitet werden.

Beispiel:

``` text
C:\Python-Projekte\WLAN-Manager
```

------------------------------------------------------------------------

## 2. Empfohlene Verzeichnisstruktur

Entwicklungsprojekte sollten in eigenen Verzeichnissen liegen:

``` text
C:\
├── Python-Projekte\
├── PowerShell-Projekte\
└── Tools\
```

Empfohlen:

``` text
C:\Python-Projekte
C:\PowerShell-Projekte
C:\Tools
```

Projektbezogene Dokumentationen bleiben möglichst beim jeweiligen
Projekt.

### Beispiel eines Python-Projekts

``` text
C:\Python-Projekte\MeinProjekt
│
├── .git\
├── .venv\
├── docs\
├── src\
├── tests\
│
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
└── VERSION
```

> \[!IMPORTANT\] Quellcode gehört ins Projektverzeichnis. Die virtuelle
> Umgebung `.venv` gehört ebenfalls zum lokalen Projekt, wird aber nicht
> in Git gespeichert.

------------------------------------------------------------------------

## 3. Windows vorbereiten

Windows zuerst vollständig aktualisieren:

**Einstellungen → Windows Update → Nach Updates suchen**

Danach prüfen, ob WinGet verfügbar ist:

``` powershell
winget --version
```

------------------------------------------------------------------------

## 4. PowerShell 7 installieren

Windows PowerShell 5.1 bleibt Bestandteil von Windows. Für die
Entwicklungsarbeit wird zusätzlich PowerShell 7 installiert.

``` powershell
winget install --id Microsoft.PowerShell --source winget
```

Danach ein neues Terminal öffnen und prüfen:

``` powershell
pwsh --version
```

Ausführliche Versionsinformationen:

``` powershell
$PSVersionTable
```

### Execution Policy

Für eigene lokale Skripte:

``` powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Kontrolle:

``` powershell
Get-ExecutionPolicy -List
```

`Unrestricted` oder ein dauerhaftes `Bypass` sollte für die normale
Entwicklungsumgebung nicht verwendet werden.

------------------------------------------------------------------------

## 5. Python mit dem Python Install Manager installieren

Für Windows wird der **Python Install Manager** verwendet. Damit lassen
sich Python-Versionen zentral installieren und verwalten.

### 5.1 Python Install Manager installieren

``` powershell
winget install 9NQ7512CXL7T
```

Danach PowerShell neu starten.

### 5.2 Verfügbare Python-Versionen anzeigen

``` powershell
py list --online
```

### 5.3 Aktuelle Version eines Python-Zweigs installieren

Beispiel:

``` powershell
py install 3.14
```

Damit wird die aktuelle verfügbare Version des angegebenen Python-Zweigs
installiert.

### 5.4 Installation prüfen

``` powershell
python --version
py --version
py list
```

Python-Pfad prüfen:

``` powershell
where.exe python
```

Pip prüfen:

``` powershell
python -m pip --version
```

### 5.5 Mehrere Python-Versionen

Der Python Install Manager kann mehrere Python-Versionen parallel
verwalten. Das ist beispielsweise nützlich, wenn ein älteres Projekt
noch eine ältere Python-Version benötigt.

> \[!TIP\] Für neue Projekte wird trotzdem immer eine projektspezifische
> `.venv` verwendet. Der Python Install Manager verwaltet die
> Python-Runtimes; `.venv` trennt die Abhängigkeiten der einzelnen
> Projekte.

------------------------------------------------------------------------

## 6. Virtuelle Python-Umgebungen

Jedes Python-Projekt erhält eine eigene virtuelle Umgebung.

Beispiel:

``` powershell
cd C:\Python-Projekte
New-Item -ItemType Directory MeinProjekt
cd MeinProjekt
python -m venv .venv
```

Aktivieren:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Danach erscheint beispielsweise:

``` text
(.venv) PS C:\Python-Projekte\MeinProjekt>
```

Kontrolle:

``` powershell
where.exe python
```

Der erste Treffer sollte auf die virtuelle Umgebung zeigen:

``` text
C:\Python-Projekte\MeinProjekt\.venv\Scripts\python.exe
```

Pakete immer möglichst über den aktiven Interpreter installieren:

``` powershell
python -m pip install Paketname
```

Beispiel:

``` powershell
python -m pip install PySide6
```

Abhängigkeiten installieren:

``` powershell
python -m pip install -r requirements.txt
```

------------------------------------------------------------------------

## 7. PyCharm installieren und einrichten

PyCharm wird als Python-IDE verwendet.

Nach der Installation ein bestehendes Projekt über **File → Open**
öffnen:

``` text
C:\Python-Projekte\MeinProjekt
```

### Projektinterpreter

PyCharm soll die virtuelle Umgebung des Projekts verwenden:

``` text
C:\Python-Projekte\MeinProjekt\.venv\Scripts\python.exe
```

Kontrolle unter:

**Settings → Project → Python Interpreter**

> \[!IMPORTANT\] PyCharm erhält keine eigene Kopie des Projekts. PyCharm
> arbeitet direkt mit dem normalen Projektverzeichnis.

------------------------------------------------------------------------

## 8. Visual Studio Code installieren und einrichten

Visual Studio Code wird als universeller Editor eingesetzt, unter
anderem für:

-   Python
-   PowerShell
-   Markdown
-   JSON
-   YAML
-   Git
-   Konfigurationsdateien

### Empfohlene Erweiterungen

Mindestens:

-   **Python** von Microsoft
-   **PowerShell** von Microsoft

Optional:

-   GitLens
-   Markdown All in One
-   YAML

### Python-Interpreter auswählen

Projekt mit **File → Open Folder** öffnen.

Danach:

**Ctrl + Shift + P → Python: Select Interpreter**

und auswählen:

``` text
.venv\Scripts\python.exe
```

Auch VS Code arbeitet damit direkt auf demselben Projekt wie PyCharm.

------------------------------------------------------------------------

## 9. Git installieren

Git ist die lokale Versionsverwaltung. GitHub ist der Online-Dienst für
die zentralen Git-Repositories.

Git for Windows installieren und danach prüfen:

``` powershell
git --version
where.exe git
```

### Git einmalig konfigurieren

``` powershell
git config --global user.name "Vorname Nachname"
git config --global user.email "name@example.com"
git config --global init.defaultBranch main
```

Kontrolle:

``` powershell
git config --global --list
```

------------------------------------------------------------------------

## 10. GitHub

Auf GitHub wird für ein Projekt ein zentrales Repository angelegt.

Der Zusammenhang ist:

``` text
Projektdateien
      │
      ▼
lokales Git-Repository
      │
      │ git push / git pull
      ▼
GitHub-Repository
```

Bei einem bereits lokal vorhandenen Projekt auf GitHub zunächst ein
**leeres Repository** anlegen. README, `.gitignore` und LICENSE nicht
nochmals automatisch erzeugen, wenn diese Dateien bereits lokal
vorhanden sind.

------------------------------------------------------------------------

## 11. Projekt mit Git verwalten

Zum Projekt wechseln:

``` powershell
cd C:\Python-Projekte\MeinProjekt
```

Git initialisieren:

``` powershell
git init
```

Status:

``` powershell
git status
```

Dateien hinzufügen:

``` powershell
git add .
```

Commit:

``` powershell
git commit -m "Initiale Version"
```

### Mit GitHub verbinden

``` powershell
git remote add origin <GitHub-Repository-Adresse>
git branch -M main
git push -u origin main
```

------------------------------------------------------------------------

## 12. Normaler Git-Arbeitsablauf

Vor Arbeitsbeginn auf einem weiteren Rechner:

``` powershell
git pull
```

Nach Änderungen:

``` powershell
git status
git add .
git commit -m "Beschreibung der Änderung"
git push
```

Merkschema:

``` text
Bearbeiten
   ↓
git status
   ↓
git add .
   ↓
git commit
   ↓
git push
   ↓
GitHub
```

------------------------------------------------------------------------

## 13. `.gitignore` für Python

Empfohlener Grundinhalt:

``` gitignore
# Python
__pycache__/
*.py[cod]
*$py.class

# Virtuelle Umgebung
.venv/

# Tests
.pytest_cache/
.coverage
htmlcov/

# Build
build/
dist/

# Temporäre Dateien
*.tmp
*.log

# Betriebssystem
Thumbs.db
.DS_Store
```

Optional, wenn IDE-Einstellungen nicht versioniert werden sollen:

``` gitignore
.idea/
.vscode/
```

> \[!NOTE\] Eine PyInstaller-`.spec`-Datei kann für reproduzierbare
> Builds wichtig sein und sollte dann bewusst mit Git verwaltet werden.

------------------------------------------------------------------------

## 14. Empfohlene Python-Projektstruktur

``` text
MeinProjekt\
│
├── .venv\
├── docs\
├── src\
│   ├── main.py
│   ├── core\
│   ├── gui\
│   ├── utils\
│   └── resources\
│
├── tests\
│
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
└── VERSION
```

### Bedeutung

  Element              Zweck
  -------------------- ----------------------------------
  `.venv`              virtuelle Python-Umgebung
  `src`                Programmcode
  `tests`              automatisierte Tests
  `docs`               Projektdokumentation
  `README.md`          Projektbeschreibung
  `CHANGELOG.md`       Änderungshistorie
  `VERSION`            Versionsinformationen
  `LICENSE`            Lizenz
  `requirements.txt`   Python-Abhängigkeiten
  `.gitignore`         von Git auszuschließende Dateien

------------------------------------------------------------------------

## 15. Versionsschema

Empfohlen wird Semantic Versioning:

``` text
MAJOR.MINOR.PATCH
```

Beispiele:

``` text
1.0.0   Erste produktive Version
1.0.1   Fehlerkorrektur
1.1.0   Neue, kompatible Funktion
2.0.0   Größere bzw. inkompatible Änderung
```

### Git-Tag für ein Release

``` powershell
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Damit bleibt nachvollziehbar, welcher Git-Stand zu einer
veröffentlichten Version gehört.

------------------------------------------------------------------------

## 16. Markdown und Obsidian

Projektbezogene Dokumentationen können als Markdown gespeichert werden:

``` text
README.md
CHANGELOG.md
docs\Installation.md
docs\Bedienung.md
```

Markdown kann unter anderem direkt gelesen und bearbeitet werden mit:

-   Obsidian
-   Visual Studio Code
-   PyCharm
-   GitHub

Obsidian eignet sich zusätzlich für übergreifende technische
Dokumentationen und persönliche Wissenssammlungen.

------------------------------------------------------------------------

## 17. Ablagen sauber trennen

### Entwicklungsprojekte

``` text
C:\Python-Projekte
C:\PowerShell-Projekte
```

### Allgemeine Werkzeuge

``` text
C:\Tools
```

### Downloads

``` text
C:\Users\<Benutzer>\Downloads
```

### Build-Ergebnisse

Projektbezogen beispielsweise:

``` text
C:\Python-Projekte\MeinProjekt\dist
```

### Projektdokumentation

``` text
C:\Python-Projekte\MeinProjekt\docs
```

------------------------------------------------------------------------

## 18. GitHub statt Cloud-Synchronisation für Quellcode

Quellcode sollte nicht primär über OneDrive, Dropbox oder vergleichbare
Synchronisationsdienste zwischen Entwicklungsrechnern abgeglichen
werden.

Für Quellcode wird verwendet:

``` text
Git + GitHub
```

Vorteile:

-   Versionshistorie
-   Commits
-   Tags
-   Branches
-   Vergleich verschiedener Versionen
-   Wiederherstellung älterer Stände
-   Zusammenarbeit
-   Synchronisation mehrerer Entwicklungsrechner

------------------------------------------------------------------------

## 19. Projekt auf einen zweiten Rechner übernehmen

Repository klonen:

``` powershell
cd C:\Python-Projekte
git clone <GitHub-Repository-Adresse>
cd MeinProjekt
```

Virtuelle Umgebung **neu** erstellen:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Abhängigkeiten installieren:

``` powershell
python -m pip install -r requirements.txt
```

> \[!IMPORTANT\] Die `.venv` wird nicht zwischen Rechnern kopiert und
> nicht nach GitHub übertragen.

------------------------------------------------------------------------

## 20. Neuer Windows-Entwicklungsrechner -- Checkliste

Diese Checkliste kann bei jeder Neuinstallation verwendet werden.

### Schritt 1 -- Windows aktualisieren

**Einstellungen → Windows Update → Nach Updates suchen**

### Schritt 2 -- WinGet prüfen

``` powershell
winget --version
```

### Schritt 3 -- PowerShell 7 installieren

``` powershell
winget install --id Microsoft.PowerShell --source winget
```

Prüfen:

``` powershell
pwsh --version
```

### Schritt 4 -- Execution Policy

``` powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Get-ExecutionPolicy -List
```

### Schritt 5 -- Entwicklungsverzeichnisse anlegen

``` powershell
New-Item -ItemType Directory -Path C:\Python-Projekte -Force
New-Item -ItemType Directory -Path C:\PowerShell-Projekte -Force
New-Item -ItemType Directory -Path C:\Tools -Force
```

### Schritt 6 -- Python Install Manager installieren

``` powershell
winget install 9NQ7512CXL7T
```

PowerShell danach neu öffnen.

### Schritt 7 -- Python installieren

Verfügbare Versionen:

``` powershell
py list --online
```

Gewünschten aktuellen stabilen Zweig installieren, beispielsweise:

``` powershell
py install 3.14
```

Prüfen:

``` powershell
python --version
py --version
py list
python -m pip --version
where.exe python
```

### Schritt 8 -- Git installieren und konfigurieren

Nach der Git-Installation:

``` powershell
git --version
where.exe git
```

Konfigurieren:

``` powershell
git config --global user.name "Vorname Nachname"
git config --global user.email "name@example.com"
git config --global init.defaultBranch main
git config --global --list
```

### Schritt 9 -- GitHub einrichten

Bei GitHub anmelden und später für jedes Projekt ein Repository anlegen.

### Schritt 10 -- PyCharm installieren

Projektinterpreter immer auf die jeweilige `.venv` setzen.

### Schritt 11 -- Visual Studio Code installieren

Mindestens die Erweiterungen **Python** und **PowerShell** von Microsoft
installieren.

### Schritt 12 -- Testprojekt erstellen

``` powershell
cd C:\Python-Projekte
New-Item -ItemType Directory Testprojekt
cd Testprojekt
python -m venv .venv
.\.venv\Scripts\Activate.ps1
New-Item -ItemType Directory src
```

`src\main.py`:

``` python
print("Python-Entwicklungsumgebung funktioniert.")
```

Start:

``` powershell
python .\src\main.py
```

### Schritt 13 -- Git testen

``` powershell
git init
git status
git add .
git commit -m "Initiale Version"
```

### Schritt 14 -- Abschlusskontrolle

``` powershell
python --version
python -m pip --version
where.exe python

pwsh --version
where.exe pwsh

git --version
where.exe git

winget --version
```

------------------------------------------------------------------------

## 21. Standardvorlage für ein neues Python-Projekt

### 21.1 Projekt erstellen

``` powershell
cd C:\Python-Projekte
New-Item -ItemType Directory MeinProjekt
cd MeinProjekt
```

### 21.2 Verzeichnisse und virtuelle Umgebung

``` powershell
New-Item -ItemType Directory src
New-Item -ItemType Directory tests
New-Item -ItemType Directory docs
python -m venv .venv
```

### 21.3 Grunddateien

``` powershell
New-Item .gitignore
New-Item README.md
New-Item CHANGELOG.md
New-Item requirements.txt
New-Item VERSION
New-Item LICENSE
New-Item .\src\main.py
```

Ergebnis:

``` text
MeinProjekt\
│
├── .venv\
├── docs\
├── src\
│   └── main.py
├── tests\
│
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
└── VERSION
```

### 21.4 Umgebung aktivieren

``` powershell
.\.venv\Scripts\Activate.ps1
where.exe python
```

### 21.5 `main.py`

``` python
def main():
    print("MeinProjekt")


if __name__ == "__main__":
    main()
```

Start:

``` powershell
python .\src\main.py
```

### 21.6 `VERSION`

Beispiel:

``` text
Version=0.1.0
Name=MeinProjekt
Author=Vorname Nachname
Company=
Copyright=2026
```

Alternativ kann bei anderen Projekten nur die Versionsnummer gespeichert
werden. Wichtig ist eine konsistente Konvention.

### 21.7 `CHANGELOG.md`

``` markdown
# Changelog

Alle wichtigen Änderungen dieses Projekts werden hier dokumentiert.

## [0.1.0]

### Hinzugefügt

- Projektstruktur erstellt
- Erste Programmversion
```

### 21.8 `requirements.txt`

Die Datei kann anfangs leer sein.

Beispiel für PySide6:

``` text
PySide6>=6.7,<7
```

Installieren:

``` powershell
python -m pip install -r requirements.txt
```

### 21.9 Git initialisieren

``` powershell
git init
git status
git add .
git commit -m "Projektstruktur erstellt"
```

### 21.10 Mit GitHub verbinden

``` powershell
git remote add origin <GitHub-Repository-Adresse>
git branch -M main
git push -u origin main
```

------------------------------------------------------------------------

## 22. Empfohlener Gesamtaufbau

``` text
Windows 11
│
├── PowerShell 7
│
├── Python Install Manager
│   ├── Python 3.14
│   └── bei Bedarf weitere Python-Versionen
│
├── Git for Windows
├── PyCharm
├── Visual Studio Code
│   ├── Python Extension
│   └── PowerShell Extension
│
└── Entwicklungsablage
    │
    ├── Python-Projekte\
    │   ├── Projekt-A\
    │   │   ├── .git\
    │   │   ├── .venv\
    │   │   ├── src\
    │   │   ├── tests\
    │   │   └── docs\
    │   └── Projekt-B\
    │
    ├── PowerShell-Projekte\
    └── Tools\
```

------------------------------------------------------------------------

## 23. Wichtigste Grundregeln

1.  Jedes Projekt besitzt ein eigenes Verzeichnis.
2.  Jedes Python-Projekt besitzt eine eigene `.venv`.
3.  `.venv` wird nicht in Git bzw. GitHub gespeichert.
4.  Python-Runtimes werden mit dem Python Install Manager verwaltet.
5.  PyCharm und VS Code verwenden dasselbe Projektverzeichnis.
6.  Beide IDEs verwenden die `.venv` des jeweiligen Python-Projekts.
7.  Python-Pakete werden projektspezifisch installiert.
8.  Quellcode wird mit Git versioniert.
9.  GitHub dient als zentrales Repository.
10. README und weitere Dokumentationen werden vorzugsweise in Markdown
    geführt.
11. Änderungen werden im `CHANGELOG.md` dokumentiert.
12. Veröffentlichte Versionen erhalten Versionsnummern und Git-Tags.
13. Auf einem zweiten Rechner wird das Repository geklont und `.venv`
    neu erstellt.
14. Vor der Arbeit auf mehreren Rechnern Änderungen mit GitHub
    synchronisieren.
15. Quellcode nicht durch bloße Cloud-Dateisynchronisation versionieren.

------------------------------------------------------------------------

## 24. Kurzreferenz

### Neue virtuelle Umgebung

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Pakete installieren

``` powershell
python -m pip install -r requirements.txt
```

### Git-Änderungen speichern

``` powershell
git status
git add .
git commit -m "Beschreibung"
git push
```

### Änderungen holen

``` powershell
git pull
```

### Release markieren

``` powershell
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Entwicklungsumgebung prüfen

``` powershell
python --version
py --version
py list
python -m pip --version
pwsh --version
git --version
winget --version
```

------------------------------------------------------------------------

## 25. Offizielle Dokumentationen

-   Python: <https://www.python.org/>
-   Python unter Windows: <https://docs.python.org/3/using/windows.html>
-   PowerShell: <https://learn.microsoft.com/powershell/>
-   PyCharm: <https://www.jetbrains.com/pycharm/>
-   Visual Studio Code: <https://code.visualstudio.com/>
-   Git: <https://git-scm.com/>
-   GitHub: <https://github.com/>
-   GitHub-Dokumentation: <https://docs.github.com/>

------------------------------------------------------------------------

**Stand:** 9. August 2026
