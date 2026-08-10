# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


PROJECT_ROOT = Path(SPECPATH)
SRC_DIR = PROJECT_ROOT / "src"


a = Analysis(
    [str(SRC_DIR / "main.py")],
    pathex=[str(SRC_DIR)],
    binaries=[],
    datas=[
        (str(PROJECT_ROOT / "VERSION"), "."),
        (str(PROJECT_ROOT / "LICENSE"), "."),
        (
            str(PROJECT_ROOT / "docs" / "Benutzerhandbuch.md"),
            "docs",
        ),
        (
            str(
                PROJECT_ROOT
                / "src"
                / "resources"
                / "icons"
                / "WLAN-Manager_Icon.ico"
            ),
            "resources/icons",
        ),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="WLAN-Manager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    version=str(PROJECT_ROOT / "version_info.py"),
    icon=str(
        PROJECT_ROOT
        / "src"
        / "resources"
        / "icons"
        / "WLAN-Manager_Icon.ico"
    ),
)