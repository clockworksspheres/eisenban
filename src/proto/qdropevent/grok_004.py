import sys
from PySide6.QtWidgets import QApplication, QListWidget, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QDragEnterEvent, QDropEvent

class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)  # Enable dragging
        self.setAcceptDrops(True)  # Enable dropping
        self.setDefaultDropAction(Qt.MoveAction)  # Default to move action
        self.setSelectionMode(QListWidget.SingleSelection)  # Single item selection
        self.setStyleSheet("border: 2px solid black; padding: 5px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item:
                # Create QMimeData with item text
                mime_data = QMimeData()
                mime_data.setText(item.text())

                # Create and start drag operation
                drag = QDrag(self)
                drag.setMimeData(mime_data)
                result = drag.exec(Qt.MoveAction)

                # If drop was successful, remove the item from the source
                if result == Qt.MoveAction:
                    row = self.row(item)
                    self.takeItem(row)

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Accept drag if it contains text and is a move action
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        # Handle drop by adding the item to this list
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            text = event.mimeData().text()
            self.addItem(text)
            event.acceptProposedAction()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Between QListWidgets")
        layout = QHBoxLayout(self)

        # Create two draggable list widgets
        self.list1 = DraggableListWidget()
        self.list2 = DraggableListWidget()

        # Populate list1 with initial items
        self.list1.addItems(["Item 1", "Item 2", "Item 3"])
        # Populate list2 with initial items
        self.list2.addItems(["Item A", "Item B"])

        # Add widgets to layout
        layout.addWidget(self.list1)
        layout.addWidget(self.list2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


