import logging
from base64 import b64decode

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QPaintEvent, QPainter, QPainterPath, QPixmap, QRegion
from PySide6.QtWidgets import QMainWindow

from ui.about_ui import Ui_About
from utils import get_current_directory, overrides


class About(QMainWindow):
    def __init__(self, color: str) -> None:
        QMainWindow.__init__(self)

        self.ui: Ui_About = Ui_About()
        self.ui.setupUi(self)

        self.count: int = 0

        self.setWindowModality(Qt.ApplicationModal)

    @overrides(QMainWindow)
    def paintEvent(self, event: QPaintEvent) -> None:
        """Override paintEvent() to make the window rounded."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)

        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
