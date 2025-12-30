import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QScrollArea
)
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtCore import Qt, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Font Zoom Example – Ctrl + Wheel | Ctrl + + | Ctrl + -")
        self.resize(800, 600)

        # Central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("Large heading text – try zooming!"))
        layout.addWidget(QLabel("Normal label text."))
        
        button = QPushButton("A sample button")
        layout.addWidget(button)

        # Scrollable text area
        text_edit = QTextEdit()
        text_edit.setPlainText(
            "This is a QTextEdit inside the window.\n"
            "Scroll normally without Ctrl.\n"
            "Hold Ctrl + Wheel or use Ctrl++ / Ctrl+- to zoom the whole app font!\n\n"
            + "Lorem ipsum " * 200
        )
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(text_edit)
        layout.addWidget(scroll_area, stretch=1)

        # Install event filter for Ctrl + Mouse Wheel
        central_widget.installEventFilter(self)

        # Set initial font size
        app_font = QApplication.font()
        app_font.setPointSize(12)
        QApplication.setFont(app_font)

        # Add keyboard shortcuts: Ctrl + + and Ctrl + -
        self.setup_zoom_shortcuts()

    def setup_zoom_shortcuts(self):
        """Create shortcuts for Ctrl++ (zoom in) and Ctrl+- (zoom out)"""
        # Ctrl + = (which is usually the + key) for zoom in
        shortcut_in = QShortcut(QKeySequence("Ctrl+="), self)
        shortcut_in.activated.connect(lambda: self.adjust_font_size(1))

        # Ctrl + - for zoom out
        shortcut_out = QShortcut(QKeySequence("Ctrl+-"), self)
        shortcut_out.activated.connect(lambda: self.adjust_font_size(-1))

        # Optional: Also support Ctrl + Shift + = if someone uses that for +
        shortcut_in_alt = QShortcut(QKeySequence("Ctrl++"), self)
        shortcut_in_alt.activated.connect(lambda: self.adjust_font_size(1))

    def adjust_font_size(self, step: int):
        """Increase or decrease application font size"""
        current_font = QApplication.font()
        new_size = max(8, current_font.pointSize() + step)
        current_font.setPointSize(new_size)
        QApplication.setFont(current_font)

    def eventFilter(self, obj, event):
        """Handle Ctrl + Mouse Wheel"""
        if event.type() == QEvent.Type.Wheel:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                delta = event.angleDelta().y()
                step = 1 if delta > 0 else -1
                self.adjust_font_size(step)
                event.accept()
                return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


