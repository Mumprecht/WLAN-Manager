from __future__ import annotations

import html
import re
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PySide6.QtCore import QCoreApplication

from core.models import EditableWifiProfile
from core.netsh import NetshError, require_success, run_netsh



PROFILE_NS = "http://www.microsoft.com/networking/WLAN/profile/v1"
ET.register_namespace("", PROFILE_NS)


def _escape(value: str) -> str:
    return html.escape(value, quote=False)


def validate_personal_key(password: str) -> None:
    """
    Validiert einen neu zu setzenden Personal-WLAN-Schlüssel.

    Akzeptiert:
    - 8 bis 63 druckbare ASCII-Zeichen als Passphrase
    - genau 64 hexadezimale Zeichen als PSK
    """
    if re.fullmatch(r"[0-9A-Fa-f]{64}", password):
        return

    if not 8 <= len(password) <= 63:
        raise ValueError(
            QCoreApplication.translate(
                "ProfileEditor",
"Das WLAN-Passwort muss 8 bis 63 Zeichen lang sein "
"oder aus genau 64 hexadezimalen Zeichen bestehen."
            )
        )

    if any(ord(char) < 32 or ord(char) > 126 for char in password):
        raise ValueError(
            QCoreApplication.translate("ProfileEditor", "Die Passphrase darf nur druckbare ASCII-Zeichen enthalten.")
        )


def _scope_from_text(text: str) -> str:
    value = text.casefold()

    if "group policy" in value or "gruppenricht" in value:
        return "group"

    if "all user" in value or "alle benutzer" in value:
        return "all"

    if "current user" in value or "aktueller benutzer" in value:
        return "current"

    raise NetshError(
        QCoreApplication.translate("ProfileEditor", "Der Gültigkeitsbereich des WLAN-Profils konnte nicht bestimmt werden.")
    )


def get_profile_scope(profile_name: str) -> str:
    result = run_netsh(
        ["wlan", "show", "profile", f"name={profile_name}"]
    )
    require_success(
        result,
        QCoreApplication.translate("ProfileEditor", "Das WLAN-Profil '{profile_name}' konnte nicht gelesen werden.").format(profile_name=profile_name),
    )

    for line in result.combined.splitlines():
        match = re.match(
            r"^\s*(Applied|Angewendet)\s*:\s*(.+?)\s*$",
            line,
            re.IGNORECASE,
        )
        if match:
            return _scope_from_text(match.group(2))

    # Fallback: bekannte Begriffe im gesamten Text suchen.
    return _scope_from_text(result.combined)


def _export_profile_xml_text(profile_name: str) -> str:
    with tempfile.TemporaryDirectory(prefix="wlan_manager_edit_") as temp_dir:
        folder = Path(temp_dir)

        result = run_netsh(
            [
                "wlan",
                "export",
                "profile",
                f"name={profile_name}",
                "key=clear",
                f"folder={folder}",
            ]
        )
        require_success(
            result,
            QCoreApplication.translate("ProfileEditor", "Das WLAN-Profil '{profile_name}' konnte nicht für die Bearbeitung exportiert werden.").format(profile_name=profile_name),
        )

        files = sorted(folder.glob("*.xml"))
        if not files:
            raise NetshError(
                QCoreApplication.translate(
                "ProfileEditor",
"Windows meldete einen erfolgreichen Export, "
"aber es wurde keine WLAN-XML-Datei gefunden."
            )
            )

        return files[0].read_text(encoding="utf-8-sig")


def _find_text(root: ET.Element, path: str, default: str = "") -> str:
    element = root.find(path)
    return element.text.strip() if element is not None and element.text else default


def load_profile_for_edit(profile_name: str) -> EditableWifiProfile:
    scope = get_profile_scope(profile_name)

    if scope == "group":
        raise PermissionError(
            QCoreApplication.translate(
                "ProfileEditor",
"Dieses WLAN-Profil wird durch eine Gruppenrichtlinie verwaltet "
"und kann im WLAN-Manager nicht bearbeitet werden."
            )
        )

    xml_text = _export_profile_xml_text(profile_name)
    root = ET.fromstring(xml_text)

    profile_xml_name = _find_text(root, f"{{{PROFILE_NS}}}name", profile_name)
    ssid = _find_text(
        root,
        f"{{{PROFILE_NS}}}SSIDConfig/{{{PROFILE_NS}}}SSID/{{{PROFILE_NS}}}name",
        profile_xml_name,
    )
    connection_mode = _find_text(
        root,
        f"{{{PROFILE_NS}}}connectionMode",
        "auto",
    )
    non_broadcast = _find_text(
        root,
        f"{{{PROFILE_NS}}}SSIDConfig/{{{PROFILE_NS}}}nonBroadcast",
        "false",
    )

    key_material = root.find(f".//{{{PROFILE_NS}}}keyMaterial")
    password = (
        key_material.text
        if key_material is not None and key_material.text
        else ""
    )

    authentications: list[str] = []
    for element in root.findall(f".//{{{PROFILE_NS}}}authentication"):
        if element.text:
            value = element.text.strip()
            if value and value not in authentications:
                authentications.append(value)

    encryptions: list[str] = []
    for element in root.findall(f".//{{{PROFILE_NS}}}encryption"):
        if element.text:
            value = element.text.strip()
            if value and value not in encryptions:
                encryptions.append(value)

    description_parts: list[str] = []
    if authentications:
        description_parts.append(" / ".join(authentications))
    if encryptions:
        description_parts.append("Cipher: " + " / ".join(encryptions))

    is_open = any(value.casefold() == "open" for value in authentications)

    return EditableWifiProfile(
        profile_name=profile_xml_name,
        ssid=ssid,
        security="existing",
        password=password,
        autoconnect=connection_mode.casefold() == "auto",
        hidden=non_broadcast.casefold() == "true",
        scope=scope,
        source_xml=xml_text,
        security_description=" · ".join(description_parts)
        or QCoreApplication.translate("ProfileEditor", "Bestehende Windows-Konfiguration"),
        is_open=is_open,
    )


def _authentication_xml(profile: EditableWifiProfile) -> tuple[str, str, str]:
    security = profile.security.strip().casefold()

    if security == "open":
        return "open", "none", ""

    if security == "wpa2-personal":
        auth = "WPA2PSK"
        encryption = "AES"
    elif security == "wpa3-personal":
        auth = "WPA3SAE"
        encryption = "AES"
    elif security == "wpa-personal":
        auth = "WPAPSK"
        encryption = "TKIP"
    else:
        raise ValueError(
            QCoreApplication.translate("ProfileEditor", "Nicht unterstützter Sicherheitstyp: {security}").format(security=profile.security)
        )

    if not profile.password:
        raise ValueError(
            QCoreApplication.translate("ProfileEditor", "Für ein neues geschütztes WLAN muss ein Passwort angegeben werden.")
        )

    validate_personal_key(profile.password)

    shared_key = f"""
        <sharedKey>
            <keyType>passPhrase</keyType>
            <protected>false</protected>
            <keyMaterial>{_escape(profile.password)}</keyMaterial>
        </sharedKey>"""

    return auth, encryption, shared_key


def build_profile_xml(profile: EditableWifiProfile) -> str:
    auth, encryption, shared_key = _authentication_xml(profile)

    connection_mode = "auto" if profile.autoconnect else "manual"
    non_broadcast = "true" if profile.hidden else "false"

    ssid_hex = _ssid_hex(profile.ssid)

    return f"""<WLANProfile xmlns="{PROFILE_NS}">
    <name>{_escape(profile.profile_name)}</name>
    <SSIDConfig>
        <SSID>
            <hex>{ssid_hex}</hex>
            <name>{_escape(profile.ssid)}</name>
        </SSID>
        <nonBroadcast>{non_broadcast}</nonBroadcast>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>{connection_mode}</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>{auth}</authentication>
                <encryption>{encryption}</encryption>
                <useOneX>false</useOneX>
            </authEncryption>{shared_key}
        </security>
    </MSM>
</WLANProfile>
"""


def _ssid_hex(ssid: str) -> str:
    return ssid.encode("utf-8").hex().upper()


def _update_existing_xml(profile: EditableWifiProfile) -> str:
    if not profile.source_xml:
        raise ValueError(QCoreApplication.translate("ProfileEditor", "Das ursprüngliche WLAN-Profil fehlt."))

    root = ET.fromstring(profile.source_xml)

    root_name = root.find(f"{{{PROFILE_NS}}}name")
    if root_name is not None:
        root_name.text = profile.profile_name

    ssid_name = root.find(
        f"{{{PROFILE_NS}}}SSIDConfig/{{{PROFILE_NS}}}SSID/{{{PROFILE_NS}}}name"
    )
    if ssid_name is not None:
        ssid_name.text = profile.ssid

    ssid_hex = root.find(
        f"{{{PROFILE_NS}}}SSIDConfig/{{{PROFILE_NS}}}SSID/{{{PROFILE_NS}}}hex"
    )
    if ssid_hex is not None:
        ssid_hex.text = _ssid_hex(profile.ssid)

    connection_mode = root.find(f"{{{PROFILE_NS}}}connectionMode")
    if connection_mode is not None:
        connection_mode.text = "auto" if profile.autoconnect else "manual"

    non_broadcast = root.find(
        f"{{{PROFILE_NS}}}SSIDConfig/{{{PROFILE_NS}}}nonBroadcast"
    )
    if non_broadcast is not None:
        non_broadcast.text = "true" if profile.hidden else "false"

    if not profile.is_open and profile.password:
        validate_personal_key(profile.password)

        key_material = root.find(f".//{{{PROFILE_NS}}}keyMaterial")
        if key_material is None:
            raise ValueError(
                QCoreApplication.translate(
                "ProfileEditor",
"Das vorhandene Profil enthält kein bearbeitbares keyMaterial. "
"Das Passwort kann deshalb nicht geändert werden."
            )
            )

        key_material.text = profile.password

        protected = root.find(f".//{{{PROFILE_NS}}}protected")
        if protected is not None:
            protected.text = "false"

    # Ist das Passwortfeld bei einem bestehenden geschützten Profil leer,
    # bleibt das vorhandene keyMaterial im exportierten XML unverändert.
    return ET.tostring(
        root,
        encoding="unicode",
        xml_declaration=False,
    )


def _install_xml(
    xml_text: str,
    profile_name: str,
    scope: str,
) -> None:
    if scope not in {"all", "current"}:
        raise ValueError(
            QCoreApplication.translate("ProfileEditor", "Ungültiger Profil-Gültigkeitsbereich: {scope}").format(scope=scope)
        )

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".xml",
            prefix="wlan_manager_",
            encoding="utf-8",
            delete=False,
        ) as handle:
            handle.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            handle.write(xml_text)
            temp_path = Path(handle.name)

        result = run_netsh(
            [
                "wlan",
                "add",
                "profile",
                f"filename={temp_path}",
                f"user={scope}",
            ]
        )

        require_success(
            result,
            QCoreApplication.translate("ProfileEditor", "Das WLAN-Profil '{profile_name}' konnte nicht gespeichert werden.").format(profile_name=profile_name),
        )
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass


def install_profile(profile: EditableWifiProfile) -> None:
    if profile.scope == "group":
        raise PermissionError(
            QCoreApplication.translate("ProfileEditor", "Gruppenrichtlinienprofile können nicht gespeichert werden.")
        )

    xml_text = build_profile_xml(profile)
    _install_xml(xml_text, profile.profile_name, profile.scope)


def delete_profile_by_name(profile_name: str) -> None:
    result = run_netsh(
        [
            "wlan",
            "delete",
            "profile",
            f"name={profile_name}",
        ]
    )
    require_success(
        result,
        QCoreApplication.translate("ProfileEditor", "Das WLAN-Profil '{profile_name}' konnte nicht gelöscht werden.").format(profile_name=profile_name),
    )


def replace_profile(
    old_profile_name: str,
    profile: EditableWifiProfile,
) -> None:
    if profile.scope == "group":
        raise PermissionError(
            QCoreApplication.translate("ProfileEditor", "Gruppenrichtlinienprofile können nicht bearbeitet werden.")
        )

    if not profile.source_xml:
        # Fallback für Profile, die nicht aus dem Editor geladen wurden.
        install_profile(profile)
        return

    xml_text = _update_existing_xml(profile)

    # Bei gleichem Namen ersetzt netsh das Profil innerhalb desselben Scopes.
    # Bei Umbenennung zuerst das neue Profil sicher anlegen, danach das alte löschen.
    _install_xml(xml_text, profile.profile_name, profile.scope)

    if old_profile_name and old_profile_name != profile.profile_name:
        delete_profile_by_name(old_profile_name)
