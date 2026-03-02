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
        self.setWindowTitle("Different Font Sizes + Global Zoom (Ctrl + Wheel / +/-)")
        self.resize(800, 600)

        # Base sizes defined here — these are multiplied by the global zoom factor
        self.base_sizes = {}  # Will store widget → base point size

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Heading - large
        heading = QLabel("This is a LARGE heading (24pt base)")
        heading_font = QFont()
        heading_font.setPointSize(24)
        heading_font.setBold(True)
        heading.setFont(heading_font)
        self.base_sizes[heading] = 24
        layout.addWidget(heading)

        # Subheading - medium
        subheading = QLabel("This is a medium subheading (18pt base)")
        sub_font = QFont()
        sub_font.setPointSize(18)
        subheading.setFont(sub_font)
        self.base_sizes[subheading] = 18
        layout.addWidget(subheading)

        # Normal text
        normal = QLabel("This is normal body text (12pt base)")
        normal_font = QFont()
        normal_font.setPointSize(12)
        normal.setFont(normal_font)
        self.base_sizes[normal] = 12
        layout.addWidget(normal)

        # Small text
        small = QLabel("This is small caption text (10pt base)")
        small_font = QFont()
        small_font.setPointSize(10)
        small.setFont(small_font)
        self.base_sizes[small] = 10
        layout.addWidget(small)

        # Button with custom size
        button = QPushButton("Button with 14pt base text")
        button_font = QFont()
        button_font.setPointSize(14)
        button.setFont(button_font)
        self.base_sizes[button] = 14
        layout.addWidget(button)

        # Scrollable text area - also gets its own base size
        text_edit = QTextEdit()
        text_edit.setPlainText(
            "This QTextEdit uses 12pt base font.\n\n"
            "Try zooming with:\n"
            "• Ctrl + Mouse Wheel\n"
            "• Ctrl + +\n"
            "• Ctrl + -\n\n"
            "All widgets keep their relative sizes but scale together!\n\n"
            + "Sample text " * 100
        )
        edit_font = QFont()
        edit_font.setPointSize(12)
        text_edit.setFont(edit_font)
        self.base_sizes[text_edit] = 12

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(text_edit)
        layout.addWidget(scroll_area, stretch=1)

        # Install event filter for wheel events
        central_widget.installEventFilter(self)

        # Set up keyboard shortcuts
        self.setup_zoom_shortcuts()

        # Start with zoom factor = 1.0
        self.zoom_factor = 1.0
        self.apply_zoom()

    def setup_zoom_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+="), self).activated.connect(lambda: self.change_zoom(0.1))
        QShortcut(QKeySequence("Ctrl+-"), self).activated.connect(lambda: self.change_zoom(-0.1))
        QShortcut(QKeySequence("Ctrl++"), self).activated.connect(lambda: self.change_zoom(0.1))

    def change_zoom(self, delta: float):
        self.zoom_factor = max(0.5, min(3.0, self.zoom_factor + delta))  # Limit between 50% and 300%
        self.apply_zoom()

    def apply_zoom(self):
        """Apply current zoom factor to all tracked widgets"""
        for widget, base_size in self.base_sizes.items():
            new_size = int(base_size * self.zoom_factor)
            new_size = max(6, new_size)  # Minimum readable size
            font = widget.font()
            font.setPointSize(new_size)
            widget.setFont(font)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                delta = event.angleDelta().y()
                step = 0.1 if delta > 0 else -0.1
                self.change_zoom(step)
                event.accept()
                return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: Set a clean default font
    app_font = QFont("Segoe UI", 10)  # This is fallback; we override per-widget anyway
    app.setFont(app_font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

