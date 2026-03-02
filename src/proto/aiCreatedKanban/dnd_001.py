import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QHBoxLayout, QLabel, QVBoxLayout
)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag

class DraggableListWidget(QListWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)                  # Allow drops into this list
        self.setDragEnabled(True)                  # Allow dragging out of this list
        self.setDefaultDropAction(Qt.CopyAction)   # Copy instead of move

        # Optional: visual feedback
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setDragDropMode(QListWidget.DragDrop)

        # Add a title label above the list
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(self)  # This is wrong — we'll fix layout in main window

    # The above layout attempt was incorrect. We'll handle layout in the main window instead.

class TwoColumnDragDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Two-Column Drag & Drop Example")
        self.resize(600, 400)

        # Main horizontal layout for two columns
        main_layout = QHBoxLayout(self)

        # Left list (source)
        self.left_list = QListWidget()
        self.left_list.setAcceptDrops(True)
        self.left_list.setDragEnabled(True)
        self.left_list.setDefaultDropAction(Qt.CopyAction)

        left_title = QLabel("Source (drag from here)")
        left_title.setAlignment(Qt.AlignCenter)
        left_vbox = QVBoxLayout()
        left_vbox.addWidget(left_title)
        left_vbox.addWidget(self.left_list)
        main_layout.addLayout(left_vbox)

        # Right list (target)
        self.right_list = QListWidget()
        self.right_list.setAcceptDrops(True)
        self.right_list.setDragEnabled(True)  # Optional: allow dragging back
        self.right_list.setDefaultDropAction(Qt.CopyAction)

        right_title = QLabel("Target (drop here)")
        right_title.setAlignment(Qt.AlignCenter)
        right_vbox = QVBoxLayout()
        right_vbox.addWidget(right_title)
        right_vbox.addWidget(self.right_list)
        main_layout.addLayout(right_vbox)

        # Populate left list with sample items
        for i in range(1, 11):
            self.left_list.addItem(f"Item {i}")

    # No need to override events — QListWidget handles internal + inter-widget drag/drop
    # automatically when dragEnabled and acceptDrops are set!

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TwoColumnDragDrop()
    window.show()
    sys.exit(app.exec())
    
