from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget


def confirm(
    parent: QWidget,
    title: str,
    text: str,
    *,
    warning: bool = False,
) -> bool:
    method = QMessageBox.warning if warning else QMessageBox.question
    result = method(
        parent,
        title,
        text,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return result == QMessageBox.StandardButton.Yes
