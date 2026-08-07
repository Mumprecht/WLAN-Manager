
# Änderungsprotokoll

## 2.5.2 – 07.08.2026

- Echte integrierte Hilfefunktion ergänzt.
- F1 öffnet jetzt das Benutzerhandbuch statt des Über-Dialogs.
- Benutzerhandbuch wird beim PyInstaller-Build mit ausgeliefert.
- Hilfe-Menü erweitert um:
  - Benutzerhandbuch
  - Projektinformationen
  - Über WLAN-Manager
- Neuer Dialog "Projektinformationen" mit Python-, PySide6-, Windows- und Laufzeitinformationen.
- Logdatei aus dem Build-/dist-Verzeichnis nach `%LOCALAPPDATA%\Mumprecht Software\WLAN-Manager\logs` verschoben.
- Dadurch kann `clean.py` den dist-Ordner nach beendetem Programm zuverlässig löschen.
- Keine Änderungen an WLAN-, Backup-, Restore-, Lösch- oder QR-Code-Funktionen.


# Änderungsprotokoll

## 2.5.1 – 07.08.2026

- Build-Prozess automatisiert.
- Neues `build.py` für einen vollständigen Onedir-Release-Build.
- Neues `clean.py` zum Bereinigen von `build`, `dist` und `version_info.py`.
- `tools/generate_version_info.py` überarbeitet und validiert jetzt die zentrale Datei `VERSION`.
- Windows-Dateiversionsinformationen werden weiterhin automatisch aus `VERSION` erzeugt.
- `WLAN-Manager.spec` als reproduzierbare Onedir-Build-Konfiguration aktualisiert.
- Build-Ausgabe zeigt Programmname, Versionsnummer und resultierenden EXE-Pfad.
- Keine Änderungen an der WLAN-Funktionalität gegenüber Version 2.5.0.


# Änderungsprotokoll

## 2.5.0 – 07.08.2026

- WLAN-QR-Code-Funktion ergänzt.
- QR-Code kann für das ausgewählte gespeicherte WLAN-Profil angezeigt werden.
- QR-Code kann als PNG-Datei gespeichert werden.
- QR-Code kann als Bild in die Windows-Zwischenablage kopiert werden.
- Passwort ist im QR-Dialog standardmäßig maskiert und kann bei Bedarf eingeblendet werden.
- Offene WLANs werden unterstützt.
- WEP sowie WPA/WPA2/WPA3-Personal werden für das standardisierte WLAN-QR-Format unterstützt.
- Enterprise-WLAN-Profile werden mit einer verständlichen Meldung abgewiesen.
- QR-Code-Funktion ist im Profilmenü und im Rechtsklick-Kontextmenü verfügbar.
- Segno 1.6.6 als QR-Code-Abhängigkeit ergänzt.
- Automatische Tests für grundlegende QR-Code-Daten ergänzt.


# Änderungsprotokoll

## 2.4.1 – 07.08.2026

- Maintenance Release ohne neue WLAN-Funktionen.
- Projektdokumentation vollständig erweitert.
- ROADMAP.md ergänzt.
- TODO.md ergänzt.
- TESTPLAN.md mit vollständiger Release-Checkliste ergänzt.
- Architektur des Programms dokumentiert.
- Entwicklerhandbuch ergänzt.
- Benutzerhandbuch ergänzt.
- Release-Prozess dokumentiert.
- Versionsnummer zentral auf 2.4.1 angehoben.


# Änderungsprotokoll

## 2.4.0 – 07.08.2026

- Bedienkomfort und dauerhafte GUI-Einstellungen erweitert.
- Fenstergröße und Fensterposition werden beim Beenden gespeichert und beim nächsten Start wiederhergestellt.
- Zustand der Hauptfenster-Toolbar wird gespeichert.
- Spaltenbreiten und Tabellenkopf-Zustand werden gespeichert.
- Sortierspalte und Sortierreihenfolge der WLAN-Profilliste werden gespeichert.
- Alternierende Tabellenzeilen verbessern die Lesbarkeit.
- Tastenkürzel ergänzt:
  - F5 = Aktualisieren
  - Ctrl+S = WLAN-Profile sichern
  - Ctrl+R = WLAN-Profile wiederherstellen
  - Entf = WLAN-Profile löschen
  - Ctrl+P = Passwörter anzeigen
  - Ctrl+I = aktuelle WLAN-Verbindung anzeigen
  - Ctrl+Enter = mit ausgewähltem Profil verbinden
  - Ctrl+Shift+S = CSV exportieren
  - Ctrl+Q = Beenden
  - F1 = Über WLAN-Manager
- Statusleiste zeigt eine kompakte Übersicht wichtiger Tastenkürzel.
- Bestehende QSettings für zuletzt verwendete Sicherungs- und Wiederherstellungsordner bleiben erhalten.


# Änderungsprotokoll

## 2.3.0 – 07.08.2026

- Profilverwaltung beim Löschen vereinheitlicht.
- Neuer Dialog "WLAN-Profile löschen..." mit Mehrfachauswahl.
- Ein, mehrere oder alle WLAN-Profile können gleichzeitig ausgewählt werden.
- Suchfeld sowie "Alle auswählen", "Keine auswählen" und "Invertieren" werden wiederverwendet.
- Separate Funktionen "Ein Profil löschen" und "Alle Profile löschen" wurden entfernt.
- Vor dem Löschen erscheint eine Sicherheitsabfrage mit Zusammenfassung der ausgewählten Profile.
- Das Rechtsklick-Menü eines Profils öffnet denselben Löschdialog mit diesem Profil vorausgewählt.
- Kernlogik unterstützt jetzt das gezielte Löschen einer Liste von WLAN-Profilen.
- Bedienlogik von Sichern, Wiederherstellen und Löschen ist damit konsistenter.


# Änderungsprotokoll

## 2.2.1 – 07.08.2026

- Konfliktbehandlung beim Nachsichern in bereits bestehende Backup-Ordner ergänzt.
- Vor dem Export wird geprüft, ob für das WLAN-Profil bereits eine XML-Datei existiert.
- Bei Konflikten stehen "Überschreiben", "Überspringen" und "Abbrechen" zur Verfügung.
- Die gewählte Konfliktaktion kann optional für alle weiteren Konflikte übernommen werden.
- Beim Überschreiben wird die vorhandene XML-Datei entfernt und das aktuelle WLAN-Profil neu exportiert.
- Zusammenfassung zeigt zusätzlich die Anzahl übersprungener Profile.
- Damit können geänderte WLAN-Profile gezielt in bestehende Backup-Ordner nachgesichert werden.


# Änderungsprotokoll

## 2.2.0 – 07.08.2026

- Sicherung und Wiederherstellung vereinheitlicht.
- Neuer Menüpunkt "WLAN-Profile sichern..." ersetzt Einzelprofil-Export und "Alle sichern".
- Beliebig viele gespeicherte WLAN-Profile können gleichzeitig ausgewählt werden.
- Suchfeld sowie "Alle auswählen", "Keine auswählen" und "Invertieren" ergänzt.
- Profile können direkt in einen bestehenden Ordner nachgesichert werden.
- Optional kann weiterhin automatisch ein neuer Unterordner mit Datum/Uhrzeit erzeugt werden.
- Zielpfad wird im Sicherungsdialog live angezeigt.
- Option zum Mitsichern der WLAN-Passwörter ist direkt im Sicherungsdialog enthalten.
- Rechtsklick auf ein einzelnes Profil öffnet denselben Sicherungsdialog mit diesem Profil vorausgewählt.
- Neuer Dialog "WLAN-Profile wiederherstellen..." mit Mehrfachauswahl von XML-Dateien.
- Wiederherstellungsdialog unterstützt Suche, Alle/Keine/Invertieren.
- Zuletzt verwendete Sicherungs- und Wiederherstellungsordner werden gespeichert.
- Neue wiederverwendbare Komponenten `ProfileSelectionWidget` und `FolderSelector`.
- Dialoge und Widgets wurden aus der bisherigen GUI-Struktur weiter modularisiert.


# Änderungsprotokoll

## 2.1.0 – 07.08.2026

- Neuer eigener PySide6-Dialog für WLAN-Backups.
- Zielordner und Backup-Ordnername sind getrennt wählbar.
- Backup-Ordnername wird automatisch mit Datum und Uhrzeit vorgeschlagen.
- Der vorgeschlagene Ordnername kann frei geändert werden.
- Live-Vorschau des vollständigen Zielpfads ergänzt.
- Option "WLAN-Passwörter mitsichern" direkt in den Backup-Dialog integriert.
- Zuletzt verwendeter Basis-Zielordner wird mit QSettings gespeichert.
- Windows-ungültige Ordnernamen werden geprüft.
- Bereits vorhandene Zielordner werden vor der Verwendung bestätigt.
- Der Zielordner wird erst beim eigentlichen Backup angelegt.

## 2.0.2 – 07.08.2026

- Backup-Dialog verbessert.
- Vorgeschlagener Sicherungsordner enthält Datum und Uhrzeit.
- Vorgeschlagener Backup-Ordner wird vor dem Dialog automatisch angelegt.
- Der Ordnerdialog öffnet sich direkt im vorgeschlagenen Backup-Ordner.
- Ein anderer oder neuer Zielordner kann im Windows-Ordnerdialog gewählt werden.
- Bei Abbruch wird ein leer angelegter Vorschlagsordner wieder entfernt.

## 2.0.1 – 07.08.2026

- Redundante Schaltflächenleiste unter der Tabelle entfernt.
- Menüstruktur vereinfacht und logisch neu gruppiert.
- Toolbar auf vier häufig benötigte Funktionen reduziert.
- Tabelle von vier auf drei Spalten vereinfacht.
- Spalte "Passwort vorhanden" entfernt.
- Hauptüberschrift im Fenster entfernt.
- Statusleiste zeigt Profilanzahl und Version.
- Rechtsklick-Menü für profilbezogene Funktionen ergänzt.
- Doppelklick auf ein Profil verbindet mit dem gespeicherten WLAN.
- Verbinden mit gespeichertem Profil über `netsh wlan connect` ergänzt.
- Versionsinformationen werden zentral aus der Datei `VERSION` gelesen.

## 2.0.0 – 06.08.2026

- Professionelle Projektstruktur mit `src`-Layout.
- GUI, WLAN-Logik, Import, Export und Hilfsfunktionen getrennt.
- Zentrale Fassade `WlanManager` eingeführt.
- Logging ergänzt.
- PyCharm-kompatible Struktur.
- Funktionsumfang der PowerShell-Version übernommen.
