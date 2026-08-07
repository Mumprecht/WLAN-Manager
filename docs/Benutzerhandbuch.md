# Benutzerhandbuch WLAN-Manager

## Start

Im Projektverzeichnis:

```powershell
python src\main.py
```

Beim Start kann Windows Administratorrechte anfordern.

## WLAN-Profile anzeigen

Nach dem Start werden alle gespeicherten WLAN-Profile automatisch angezeigt.

Mit `F5` kann die Liste aktualisiert werden.

## WLAN-Passwörter anzeigen

Menü:

```text
WLAN > Passwörter anzeigen
```

Tastenkürzel:

```text
Ctrl+P
```

Die Passwörter werden im Klartext angezeigt.

## Mit einem WLAN verbinden

Ein gespeichertes Profil kann durch Doppelklick verbunden werden.

Alternativ:

```text
Profile > Verbinden
```

oder:

```text
Ctrl+Enter
```

## WLAN-Profile sichern

Menü:

```text
Datei > WLAN-Profile sichern...
```

Es können ein, mehrere oder alle Profile ausgewählt werden.

Optional kann ein neuer Unterordner mit Datum und Uhrzeit erzeugt werden.

Zum Nachsichern in einen bestehenden Ordner wird diese Option deaktiviert.

Falls eine XML-Datei bereits existiert, stehen folgende Optionen zur Verfügung:

- Überschreiben
- Überspringen
- Abbrechen

## WLAN-Profile wiederherstellen

Menü:

```text
Datei > WLAN-Profile wiederherstellen...
```

Es können ein, mehrere oder alle XML-Dateien ausgewählt werden.

## WLAN-Profile löschen

Menü:

```text
Profile > WLAN-Profile löschen...
```

Es können ein, mehrere oder alle Profile gelöscht werden.

Vor dem Löschen erscheint eine Sicherheitsabfrage.

## CSV-Export

Menü:

```text
Datei > CSV exportieren...
```

Die CSV-Datei kann WLAN-Passwörter im Klartext enthalten.

## Aktuelle WLAN-Verbindung

Menü:

```text
WLAN > Aktuelle Verbindung
```

Tastenkürzel:

```text
Ctrl+I
```

## Tastenkürzel

- `F5` Aktualisieren
- `Ctrl+S` Sichern
- `Ctrl+R` Wiederherstellen
- `Entf` Löschen
- `Ctrl+P` Passwörter anzeigen
- `Ctrl+I` Aktuelle Verbindung
- `Ctrl+Enter` Verbinden
- `Ctrl+Shift+S` CSV exportieren
- `Ctrl+Q` Beenden
- `F1` Über WLAN-Manager

## Sicherheit

Backup-XML-Dateien mit Klartextschlüsseln sowie CSV-Dateien mit Passwörtern sind vertraulich zu behandeln.


## WLAN-QR-Code

Ein gespeichertes WLAN-Profil auswählen und anschließend:

```text
Profile > QR-Code anzeigen...
```

Alternativ steht die Funktion im Rechtsklick-Menü des Profils zur Verfügung.

Der Dialog zeigt:

- SSID
- Authentifizierung
- maskiertes WLAN-Passwort
- QR-Code

Das Passwort kann bei Bedarf eingeblendet werden.

Der QR-Code kann als PNG gespeichert oder als Bild in die Zwischenablage
kopiert werden. Smartphones und Tablets können den Code verwenden, um die
WLAN-Zugangsdaten zu übernehmen.

Enterprise-WLAN-Profile werden derzeit nicht unterstützt.


## Hilfe

Mit `F1` oder über:

```text
Hilfe > Benutzerhandbuch
```

wird dieses Benutzerhandbuch direkt im WLAN-Manager angezeigt.

Unter:

```text
Hilfe > Projektinformationen
```

werden technische Informationen zur installierten Version, Python, PySide6,
Windows sowie zum Logverzeichnis angezeigt.

Unter:

```text
Hilfe > Über WLAN-Manager
```

werden Programmname, Version, Firma, Copyright und Autor angezeigt.
