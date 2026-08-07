from core.models import WlanProfile


def test_open_network_has_no_password() -> None:
    profile = WlanProfile(
        ssid="Offenes WLAN",
        authentication="Open",
        password="<offenes WLAN – kein Passwort>",
    )
    assert profile.has_password is False


def test_secured_network_has_password() -> None:
    profile = WlanProfile(
        ssid="Test",
        authentication="WPA2-Personal",
        password="secret",
    )
    assert profile.has_password is True
