# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path


PROJECT_ROOT = Path(SPECPATH)
SRC_DIR = PROJECT_ROOT / "src"


a = Analysis(
    [str(SRC_DIR / "main.py")],
    pathex=[str(SRC_DIR)],
    binaries=[],
    datas=[
        # Programm- und Lizenzinformationen
        (
            str(PROJECT_ROOT / "VERSION"),
            ".",
        ),
        (
            str(PROJECT_ROOT / "LICENSE"),
            ".",
        ),

        # Benutzerhandbücher
        (
            str(
                PROJECT_ROOT
                / "docs"
                / "Benutzerhandbuch.md"
            ),
            "docs",
        ),
        (
            str(
                PROJECT_ROOT
                / "docs"
                / "Benutzerhandbuch_en.md"
            ),
            "docs",
        ),
        (
            str(
                PROJECT_ROOT
                / "docs"
                / "Benutzerhandbuch_fr.md"
            ),
            "docs",
        ),
        (
            str(
                PROJECT_ROOT
                / "docs"
                / "Benutzerhandbuch_it.md"
            ),
            "docs",
        ),

        # Übersetzungsdateien
        (
            str(
                PROJECT_ROOT
                / "src"
                / "resources"
                / "translations"
                / "wlan_manager_en.qm"
            ),
            "resources/translations",
        ),
        (
            str(
                PROJECT_ROOT
                / "src"
                / "resources"
                / "translations"
                / "wlan_manager_fr.qm"
            ),
            "resources/translations",
        ),
        (
            str(
                PROJECT_ROOT
                / "src"
                / "resources"
                / "translations"
                / "wlan_manager_it.qm"
            ),
            "resources/translations",
        ),

        # Programmsymbol
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
    version=str(
        PROJECT_ROOT / "version_info.py"
    ),
    icon=str(
        PROJECT_ROOT
        / "src"
        / "resources"
        / "icons"
        / "WLAN-Manager_Icon.ico"
    ),
)