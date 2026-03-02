import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QScrollArea
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Font Zoom Example – Ctrl + Mouse Wheel")
        self.resize(800, 600)

        # Central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("Large heading text – try zooming!"))
        layout.addWidget(QLabel("Normal label text."))
        
        button = QPushButton("A sample button")
        layout.addWidget(button)

        # A scrollable text area (common case where wheel events get consumed)
        text_edit = QTextEdit()
        text_edit.setPlainText(
            "This is a QTextEdit inside the window.\n"
            "Normally, scrolling with the mouse wheel here would scroll the text.\n"
            "But when you hold Ctrl, it will zoom the entire application's font instead!\n\n"
            + "Lorem ipsum " * 200
        )
        
        # Wrap it in a QScrollArea to make it even more realistic
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(text_edit)
        layout.addWidget(scroll_area, stretch=1)

        # Install event filter on the central widget to catch all wheel events
        central_widget.installEventFilter(self)

        # Set initial application font (optional – adjust starting size here)
        app_font = QApplication.font()
        app_font.setPointSize(12)
        QApplication.setFont(app_font)

    def eventFilter(self, obj, event):
        """Catch wheel events anywhere over the central area."""
        if event.type() == QEvent.Type.Wheel:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Ctrl + Wheel → zoom font
                delta = event.angleDelta().y()
                step = 1 if delta > 0 else -1

                current_font = QApplication.font()
                new_size = max(8, current_font.pointSize() + step)  # Minimum size 8

                current_font.setPointSize(new_size)
                QApplication.setFont(current_font)

                event.accept()
                return True  # Event handled – don't pass to children

        # For all other events, let normal processing continue
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

