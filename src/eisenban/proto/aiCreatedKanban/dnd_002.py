import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QHBoxLayout, QLabel, QVBoxLayout
)
from PySide6.QtCore import Qt

class TwoColumnMoveDragDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Drag & Drop: Move from Source to Destination")
        self.resize(600, 400)

        # Main layout: two columns side by side
        main_layout = QHBoxLayout(self)

        # === Left column: Source ===
        self.source_list = QListWidget()
        self.source_list.setAcceptDrops(True)          # Allow drops (in case you drag back)
        self.source_list.setDragEnabled(True)          # Allow dragging items out
        self.source_list.setDefaultDropAction(Qt.MoveAction)  # Key: move, not copy

        source_title = QLabel("Source\n(Drag items from here)")
        source_title.setAlignment(Qt.AlignCenter)
        source_vbox = QVBoxLayout()
        source_vbox.addWidget(source_title)
        source_vbox.addWidget(self.source_list)
        main_layout.addLayout(source_vbox)

        # === Right column: Destination ===
        self.dest_list = QListWidget()
        self.dest_list.setAcceptDrops(True)            # Must accept drops
        self.dest_list.setDragEnabled(True)            # Optional: allow dragging back to source
        self.dest_list.setDefaultDropAction(Qt.MoveAction)

        dest_title = QLabel("Destination\n(Drop items here)")
        dest_title.setAlignment(Qt.AlignCenter)
        dest_vbox = QVBoxLayout()
        dest_vbox.addWidget(dest_title)
        dest_vbox.addWidget(self.dest_list)
        main_layout.addLayout(dest_vbox)

        # Populate source with sample items
        for i in range(1, 11):
            self.source_list.addItem(f"Item {i}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TwoColumnMoveDragDrop()
    window.show()
    sys.exit(app.exec())
    
