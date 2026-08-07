from core.models import WlanProfile
from core.qr_code import WifiQrError, wifi_qr_data


def test_wpa_profile_qr_data() -> None:
    profile = WlanProfile(
        ssid="TestNetz",
        authentication="WPA2-Personal",
        password="Geheim123",
    )

    data = wifi_qr_data(profile)

    assert data.startswith("WIFI:")
    assert "T:WPA;" in data
    assert "S:TestNetz;" in data
    assert "P:Geheim123;" in data


def test_open_profile_qr_data() -> None:
    profile = WlanProfile(
        ssid="Gastnetz",
        authentication="Open",
        password="<offenes WLAN – kein Passwort>",
    )

    data = wifi_qr_data(profile)

    assert "T:nopass;" in data
    assert "S:Gastnetz;" in data


def test_enterprise_profile_is_rejected() -> None:
    profile = WlanProfile(
        ssid="Firma",
        authentication="WPA2-Enterprise",
        password="secret",
    )

    try:
        wifi_qr_data(profile)
    except WifiQrError:
        pass
    else:
        raise AssertionError("Enterprise-Profil wurde unerwartet akzeptiert.")
