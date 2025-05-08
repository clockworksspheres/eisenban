#!/usr/bin/env -S python -u

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QMenu, QVBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Right-click me")
        self.button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.show_context_menu)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

    def show_context_menu(self, position):
        menu = QMenu(self)

        action_1 = QAction("Action 1", self)
        action_1.triggered.connect(self.do_action_1)
        menu.addAction(action_1)

        action_2 = QAction("Action 2", self)
        action_2.triggered.connect(self.do_action_2)
        menu.addAction(action_2)

        menu.exec(self.button.mapToGlobal(position))

    def do_action_1(self):
        print("Action 1 triggered")

    def do_action_2(self):
        print("Action 2 triggered")


if __name__ == "__main__":
    app = QApplication()
    widget = MyWidget()
    widget.show()
    app.exec()


