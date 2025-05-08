#!/usr/bin/env -S python -u

from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click here!", self)
        self.label.setGeometry(50, 50, 100, 30)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.label.setText("Left Button Clicked")
        elif event.button() == Qt.MouseButton.RightButton:
            self.label.setText("Right Button Clicked")
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("Middle Button Clicked")
        else:
            self.label.setText("Other Button Clicked")

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()
