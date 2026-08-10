### SHA-256-Prüfsumme

`WLAN-Manager.exe`

```text
4627C6CE452A62C61E2E0F53BC6822CE180CC6498B8C9531C0FF4E95D9962887
```

Die Prüfsumme kann unter Windows mit PowerShell überprüft werden:

```powershell
Get-FileHash .\WLAN-Manager.exe -Algorithm SHA256
```

### Windows Defender SmartScreen

WLAN-Manager ist derzeit nicht digital signiert. Windows Defender SmartScreen
kann deshalb beim ersten Start nach dem Herunterladen eine Warnung anzeigen.

Wenn WLAN-Manager von diesem offiziellen GitHub-Release heruntergeladen wurde,
kann die heruntergeladene Datei anhand der oben angegebenen SHA-256-Prüfsumme
überprüft werden.

Nach erfolgreicher Prüfung kann das Programm über:

1. **Weitere Informationen / More info**
2. **Trotzdem ausführen / Run anyway**

gestartet werden.