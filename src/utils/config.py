from __future__ import annotations

from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = SRC_DIR.parent
RESOURCES_DIR = SRC_DIR / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
STYLES_DIR = RESOURCES_DIR / "styles"
DOCS_DIR = PROJECT_DIR / "docs"
