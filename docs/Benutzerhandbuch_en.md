# WLAN-Manager User Manual

## Start

In the project directory:

```powershell
python src\main.py
```

Windows may request administrator privileges when the program starts.

## Display WLAN profiles

After startup, all saved WLAN profiles are displayed automatically.

Press `F5` to refresh the list.

## Copy content from the profile list

The content of a table cell can be copied to the clipboard.

Right-click the desired cell and select from the context menu:

```text
Copy    Ctrl+C
```

Alternatively, select the desired cell and press:

```text
Ctrl+C
```

This can be used, for example, to copy the WLAN profile name, authentication method, or the password content displayed in the table.

## Display WLAN passwords

Menu:

```text
WLAN > Show passwords
```

Keyboard shortcut:

```text
Ctrl+P
```

The passwords are displayed in plain text.

## Connect to a WLAN

A saved profile can be connected by double-clicking it.

Alternatively:

```text
Profiles > Connect
```

or:

```text
Ctrl+Enter
```

## Back up WLAN profiles

Menu:

```text
File > Back up WLAN profiles...
```

One, several, or all profiles can be selected.

Optionally, a new subfolder containing the date and time can be created.

Disable this option to add backups to an existing folder.

If an XML file already exists, the following options are available:

- Overwrite
- Skip
- Cancel

## Restore WLAN profiles

Menu:

```text
File > Restore WLAN profiles...
```

One, several, or all XML files can be selected.

## Delete WLAN profiles

Menu:

```text
Profiles > Delete WLAN profiles...
```

One, several, or all profiles can be deleted.

A confirmation prompt appears before deletion.

## CSV export

Menu:

```text
File > Export CSV...
```

The CSV file may contain WLAN passwords in plain text.

## Current WLAN connection

Menu:

```text
WLAN > Current connection
```

Keyboard shortcut:

```text
Ctrl+I
```

## Manage automatic WLAN connections and priority

Menu:

```text
WLAN > Manage automatic WLAN connections...
```

This function manages the autoconnect status and priority of saved WLAN profiles.

The table shows:

- **Priority** – the order in which Windows prefers the WLAN profiles.
- **WLAN profile** – the name of the saved WLAN profile.
- **Connect automatically** – indicates with **Yes** or **No** whether Windows may automatically connect using this profile.

### Change WLAN priority

**Priority 1 is the highest priority.**

Use **Move up** or **Move down** to move a profile within the priority order.

The change is saved immediately in Windows. WLAN-Manager then reads the profile list from Windows again and displays the order that is actually stored.

On Windows, WLAN priority is associated with the respective WLAN interface.

### Change autoconnect

Use **Change autoconnect** to switch the selected profile between **Yes** and **No**.

- **Yes** – Windows may automatically connect using this profile.
- **No** – Windows does not automatically connect using this profile. A manual connection is still possible.

The change is saved immediately in Windows and then read back from Windows.

### Notes

Profiles managed by administrative policies or Group Policy may not be modifiable.

**Refresh** reads the current state of the WLAN profiles from Windows again without making any changes.

## Keyboard shortcuts

- `F5` Refresh
- `Ctrl+C` Copy the content of the selected table cell
- `Ctrl+S` Back up
- `Ctrl+R` Restore
- `Del` Delete
- `Ctrl+P` Show passwords
- `Ctrl+I` Current connection
- `Ctrl+Enter` Connect
- `Ctrl+Shift+S` Export CSV
- `Ctrl+Q` Exit
- `F1` About WLAN-Manager

## License and copyright

Copyright © 2026 Urs Mumprecht / Mumprecht Software.

WLAN-Manager is proprietary software and may be used free of charge for private and other non-commercial purposes.

Commercial use, modification, redistribution, republication, or the creation of derivative works is not permitted without the prior written permission of the copyright holder.

The following license applies:

**WLAN-Manager Non-Commercial License, Version 1.0**

The complete license terms are contained in the `LICENSE` file.

## Security

Backup XML files containing plain-text keys and CSV files containing passwords must be treated as confidential.

## WLAN QR code

Select a saved WLAN profile and then choose:

```text
Profiles > Show QR code...
```

Alternatively, the function is available in the profile's right-click menu.

The dialog displays:

- SSID
- Authentication
- Masked WLAN password
- QR code

The password can be displayed if required.

The QR code can be saved as a PNG file or copied to the clipboard as an image. Smartphones and tablets can use the code to import the WLAN credentials.

Enterprise WLAN profiles are currently not supported.

## Help

Press `F1` or choose:

```text
Help > User manual
```

to display this user manual directly in WLAN-Manager.

Under:

```text
Help > Project information
```

technical information about the installed version, Python, PySide6, Windows, and the log directory is displayed.

Under:

```text
Help > About WLAN-Manager
```

the program name, version, company, copyright, and author are displayed.

## Create WLAN profile

Choose:

```text
Profiles > New WLAN profile...
```

to create a new WLAN profile.

Required information:

- Profile name
- SSID
- Security type
- Password for secured WLANs

Additional options:

- Connect automatically
- Allow connection to a hidden SSID

## Edit WLAN profile

Select an existing profile and choose:

```text
Profiles > Edit WLAN profile...
```

or use the corresponding entry in the right-click menu.

The profile name, SSID, security, password, and connection options can be modified.

### Scope and editing existing profiles

For a new profile, you can choose:

- All users
- Current user only

When an existing profile is edited, WLAN-Manager automatically retains its current scope. The existing Windows security configuration is also preserved. This ensures that more complex WPA2/WPA3 profiles are retained; for existing profiles, the editor changes only the profile name, SSID, password, auto-connect setting, and the setting for hidden SSIDs.

WLAN profiles managed by Group Policy are read-only and cannot be edited.

### Password when editing

A valid WLAN key must be specified for a new secured WLAN.

For an existing secured profile:

- If the existing password is displayed, it can be changed.
- If the password field is cleared completely, the existing password remains unchanged.
- If Windows could not provide the password in plain text, the field remains empty. In this case as well, an empty field means: keep the existing password.
- Only when a new password is entered does WLAN-Manager replace the existing key.

For newly set Personal WLAN keys, WLAN-Manager accepts passphrases containing 8 to 63 printable ASCII characters or a 64-character hexadecimal PSK.

No password is stored for open WLANs.
