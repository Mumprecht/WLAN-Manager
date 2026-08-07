# Requirements-Dateien

## requirements.txt
Laufzeit-Abhängigkeiten des Programms.

Installation:
    python -m pip install -r requirements.txt

## requirements-build.txt
Zusätzlich benötigte Pakete zum Erstellen der EXE.

Installation:
    python -m pip install -r requirements-build.txt

## requirements-dev.txt
Komplette Entwicklungsumgebung.

Installation:
    python -m pip install -r requirements-dev.txt

## requirements-lock.txt
Beispiel einer fest eingefrorenen Paketliste.
Nach jeder freigegebenen Version aktualisieren mit:

    python -m pip freeze > requirements-lock.txt
