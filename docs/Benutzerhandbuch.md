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

## Inhalte aus der Profilliste kopieren

Der Inhalt einer Tabellenzelle kann in die Zwischenablage kopiert werden.

Dazu mit der rechten Maustaste auf die gewünschte Zelle klicken und im
Kontextmenü auswählen:

```text
Kopieren    Ctrl+C
```

Alternativ kann die gewünschte Zelle ausgewählt und mit:

```text
Ctrl+C
```

kopiert werden.

Damit können beispielsweise der WLAN-Profilname, die Authentifizierung oder
der in der Tabelle angezeigte Passwortinhalt kopiert werden.

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

## Automatische WLAN-Verbindungen und Priorität verwalten

Menü:

```text
WLAN > Automatische WLAN-Verbindungen verwalten...
```

Mit dieser Funktion werden der Autoconnect-Status und die Priorität der gespeicherten WLAN-Profile verwaltet.

Die Tabelle zeigt:

- **Priorität** – Reihenfolge, in der Windows die WLAN-Profile bevorzugt.
- **WLAN-Profil** – Name des gespeicherten WLAN-Profils.
- **Automatisch verbinden** – zeigt mit **Ja** oder **Nein**, ob Windows automatisch eine Verbindung mit diesem Profil herstellen darf.

### WLAN-Priorität ändern

**Priorität 1 ist die höchste Priorität.**

Ein Profil kann mit **Nach oben** oder **Nach unten** in der Prioritätsreihenfolge verschoben werden.

Die Änderung wird sofort in Windows gespeichert. Anschliessend liest WLAN-Manager die Profilliste erneut aus Windows ein und zeigt die tatsächlich gespeicherte Reihenfolge an.

Die WLAN-Priorität ist unter Windows an die jeweilige WLAN-Schnittstelle gebunden.

### Autoconnect ändern

Mit **Autoconnect ändern** wird die Einstellung des ausgewählten Profils zwischen **Ja** und **Nein** umgeschaltet.

- **Ja** – Windows darf automatisch eine Verbindung mit diesem Profil herstellen.
- **Nein** – Windows stellt mit diesem Profil nicht automatisch eine Verbindung her. Eine manuelle Verbindung bleibt weiterhin möglich.

Die Änderung wird sofort in Windows gespeichert und danach erneut aus Windows eingelesen.

### Hinweise

Profile, die durch administrative Vorgaben oder Gruppenrichtlinien verwaltet werden, können möglicherweise nicht geändert werden.

**Aktualisieren** liest den aktuellen Zustand der WLAN-Profile erneut aus Windows ein, ohne eine Änderung vorzunehmen.

## Tastenkürzel

- `F5` Aktualisieren
- `Ctrl+C` Inhalt der ausgewählten Tabellenzelle kopieren
- `Ctrl+S` Sichern
- `Ctrl+R` Wiederherstellen
- `Entf` Löschen
- `Ctrl+P` Passwörter anzeigen
- `Ctrl+I` Aktuelle Verbindung
- `Ctrl+Enter` Verbinden
- `Ctrl+Shift+S` CSV exportieren
- `Ctrl+Q` Beenden
- `F1` Über WLAN-Manager

## Lizenz und Copyright

Copyright © 2026 Urs Mumprecht / Mumprecht Software.

Der WLAN-Manager ist proprietäre Software und darf für private und andere
nicht-kommerzielle Zwecke kostenlos verwendet werden.

Kommerzielle Nutzung, Änderungen, Weiterverteilung, Wiederveröffentlichung
oder die Erstellung abgeleiteter Werke sind ohne vorherige schriftliche
Genehmigung des Urheberrechtsinhabers nicht gestattet.

Es gilt die:

**WLAN-Manager Non-Commercial License, Version 1.0**

Die vollständigen Lizenzbedingungen befinden sich in der Datei `LICENSE`.

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

## WLAN-Profil erstellen

Über:

```text
Profile > Neues WLAN-Profil...
```

kann ein neues WLAN-Profil angelegt werden.

Erforderliche Angaben:

- Profilname
- SSID
- Sicherheitstyp
- Passwort bei geschützten WLANs

Zusätzliche Optionen:

- automatisch verbinden
- Verbindung mit versteckter SSID erlauben

## WLAN-Profil bearbeiten

Ein bestehendes Profil auswählen und:

```text
Profile > WLAN-Profil bearbeiten...
```

oder den entsprechenden Eintrag im Rechtsklick-Menü verwenden.

Dabei können Profilname, SSID, Sicherheit, Passwort und Verbindungsoptionen
angepasst werden.

### Gültigkeitsbereich und Bearbeitung vorhandener Profile

Bei einem neuen Profil kann gewählt werden:

- Alle Benutzer
- Nur aktueller Benutzer

Beim Bearbeiten eines vorhandenen Profils übernimmt der WLAN-Manager den
vorhandenen Gültigkeitsbereich automatisch. Die vorhandene Windows-
Sicherheitskonfiguration wird ebenfalls beibehalten. Dadurch bleiben auch
komplexere WPA2/WPA3-Profile erhalten; im Editor werden bei bestehenden
Profilen nur Profilname, SSID, Passwort, Auto-Connect und die Einstellung für
versteckte SSIDs geändert.

Durch Gruppenrichtlinien verwaltete WLAN-Profile sind schreibgeschützt und
können nicht bearbeitet werden.

### Passwort beim Bearbeiten

Bei einem neuen geschützten WLAN muss ein gültiger WLAN-Schlüssel angegeben
werden.

Bei einem bestehenden geschützten Profil gilt:

- Wird das vorhandene Passwort angezeigt, kann es geändert werden.
- Wird das Passwortfeld vollständig geleert, bleibt das bisherige Passwort
  unverändert.
- Konnte Windows das Passwort nicht im Klartext liefern, bleibt das Feld leer.
  Auch dann bedeutet ein leeres Feld: vorhandenes Passwort beibehalten.
- Erst wenn ein neues Passwort eingegeben wird, ersetzt der WLAN-Manager den
  bisherigen Schlüssel.

Für neu gesetzte Personal-WLAN-Schlüssel akzeptiert der WLAN-Manager
Passphrasen mit 8 bis 63 druckbaren ASCII-Zeichen oder einen 64-stelligen
hexadezimalen PSK.

Bei offenen WLANs wird kein Passwort gespeichert.
