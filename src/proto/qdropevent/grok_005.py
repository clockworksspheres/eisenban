import sys
from PySide6.QtWidgets import QApplication, QListWidget, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent

class DraggableListWidget(QListWidget):
    def __init__(self, name="List"):
        super().__init__()
        self.name = name  # For debugging
        self.setDragEnabled(True)  # Enable dragging
        self.setAcceptDrops(True)  # Enable dropping
        self.setDefaultDropAction(Qt.MoveAction)  # Default to move action
        self.setSelectionMode(QListWidget.SingleSelection)  # Single item selection
        self.setStyleSheet("border: 2px solid black; padding: 5px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item:
                print(f"{self.name}: Initiating drag for item '{item.text()}'")
                # Create QMimeData with item text
                mime_data = QMimeData()
                mime_data.setText(item.text())

                # Create and start drag operation
                drag = QDrag(self)
                drag.setMimeData(mime_data)
                result = drag.exec(Qt.MoveAction)

                # If drop was successful, remove the item from the source
                if result == Qt.MoveAction:
                    print(f"{self.name}: Drop successful, removing item '{item.text()}'")
                    row = self.row(item)
                    self.takeItem(row)
                else:
                    print(f"{self.name}: Drop failed or canceled")

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Accept drag if it contains text and is a move action
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            print(f"{self.name}: Drag entered with text '{event.mimeData().text()}'")
            event.acceptProposedAction()
        else:
            print(f"{self.name}: Drag rejected (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        # Explicitly accept move events to ensure drop is allowed
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        # Handle drop by adding the item to this list
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            text = event.mimeData().text()
            print(f"{self.name}: Dropped item '{text}'")
            self.addItem(text)
            event.acceptProposedAction()
        else:
            print(f"{self.name}: Drop rejected (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            event.ignore()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Between QListWidgets")
        layout = QHBoxLayout(self)

        # Create two draggable list widgets
        self.list1 = DraggableListWidget("List 1")
        self.list2 = DraggableListWidget("List 2")

        # Populate list1 and list2 with initial items
        self.list1.addItems(["Item 1", "Item 2", "Item 3"])
        self.list2.addItems(["Item A", "Item B"])

        # Add widgets to layout
        layout.addWidget(self.list1)
        layout.addWidget(self.list2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


