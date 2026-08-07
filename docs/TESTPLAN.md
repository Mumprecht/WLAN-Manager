# TESTPLAN

Dieser Testplan ist vor jeder Freigabe einer neuen Version vollständig durchzugehen.

## 1. Programmstart
- [ ] Start mit `python src\main.py`
- [ ] UAC-Abfrage funktioniert
- [ ] Hauptfenster öffnet sich
- [ ] Versionsnummer stimmt
- [ ] Fensterposition wird wiederhergestellt
- [ ] Fenstergröße wird wiederhergestellt

## 2. WLAN-Profile
- [ ] Gespeicherte Profile werden vollständig angezeigt
- [ ] Authentifizierung wird korrekt angezeigt
- [ ] Sortierung funktioniert
- [ ] Spaltenbreiten bleiben gespeichert
- [ ] F5 aktualisiert die Profilliste

## 3. Passwörter
- [ ] Passwörter können angezeigt werden
- [ ] Sonderzeichen werden korrekt dargestellt
- [ ] Offene WLANs werden korrekt erkannt
- [ ] `Ctrl+P` funktioniert

## 4. Verbinden
- [ ] Verbindung per Doppelklick funktioniert
- [ ] Verbindung per Kontextmenü funktioniert
- [ ] `Ctrl+Enter` funktioniert

## 5. Aktuelle Verbindung
- [ ] Aktuelle SSID wird angezeigt
- [ ] Signalstärke wird angezeigt
- [ ] Kanal wird angezeigt
- [ ] Standortberechtigungsfehler wird sinnvoll behandelt
- [ ] `Ctrl+I` funktioniert

## 6. Sichern
- [ ] Einzelnes Profil sichern
- [ ] Mehrere Profile sichern
- [ ] Alle Profile sichern
- [ ] Sicherung mit Passwörtern
- [ ] Sicherung ohne Klartextpasswörter
- [ ] Neuer Unterordner mit Datum/Uhrzeit
- [ ] Direktes Nachsichern in bestehenden Ordner
- [ ] Konflikt: Überschreiben
- [ ] Konflikt: Überspringen
- [ ] Konflikt: Abbrechen
- [ ] Auswahl für alle Konflikte übernehmen
- [ ] `Ctrl+S` funktioniert

## 7. Wiederherstellen
- [ ] Einzelnes XML-Profil wiederherstellen
- [ ] Mehrere XML-Profile wiederherstellen
- [ ] Alle XML-Profile wiederherstellen
- [ ] Suchfeld funktioniert
- [ ] Alle / Keine / Invertieren funktioniert
- [ ] `Ctrl+R` funktioniert

## 8. Löschen
- [ ] Einzelnes Profil löschen
- [ ] Mehrere Profile löschen
- [ ] Alle Profile löschen
- [ ] Sicherheitsabfrage erscheint
- [ ] Kontextmenü startet denselben Löschdialog
- [ ] `Entf` funktioniert

## 9. CSV-Export
- [ ] CSV-Datei wird erstellt
- [ ] Semikolon als Trennzeichen
- [ ] UTF-8/Excel-kompatibel
- [ ] Passwörter korrekt
- [ ] `Ctrl+Shift+S` funktioniert

## 10. Sonstiges
- [ ] Kontextmenü vollständig
- [ ] `F1` öffnet Über-Dialog
- [ ] `Ctrl+Q` beendet das Programm
- [ ] Logdatei wird geschrieben
- [ ] Keine unerwarteten Fehlermeldungen


## 11. QR-Code
- [ ] QR-Code für WPA2-Personal anzeigen
- [ ] QR-Code für WPA3-Personal anzeigen
- [ ] QR-Code für offenes WLAN anzeigen
- [ ] Passwort standardmäßig maskiert
- [ ] Passwort ein-/ausblenden
- [ ] QR-Code als PNG speichern
- [ ] gespeicherten PNG-QR-Code mit Smartphone testen
- [ ] QR-Code in Zwischenablage kopieren
- [ ] kopierten QR-Code in Bildprogramm einfügen
- [ ] Enterprise-Profil liefert verständliche Meldung
- [ ] SSID/Passwort mit Sonderzeichen testen


## 12. Hilfe
- [ ] F1 öffnet das Benutzerhandbuch
- [ ] Benutzerhandbuch wird vollständig angezeigt
- [ ] Hilfe funktioniert aus PyCharm
- [ ] Hilfe funktioniert aus der PyInstaller-EXE
- [ ] Projektinformationen öffnen
- [ ] Version in Projektinformationen stimmt
- [ ] Logverzeichnis wird korrekt angezeigt
- [ ] Über WLAN-Manager zeigt Version 2.5.2
