import sys
from PySide6.QtWidgets import QApplication, QListWidget, QHBoxLayout, QWidget
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
        self.setStyleSheet("border: 2px solid black; padding: 5px; min-width: 150px;")

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
    def __init__(self, num_lists=3):
        super().__init__()
        self.setWindowTitle("Drag and Drop Between N QListWidgets")
        layout = QHBoxLayout(self)

        # Create n draggable list widgets
        self.lists = []
        for i in range(num_lists):
            list_widget = DraggableListWidget(f"List {i + 1}")
            # Populate each list with unique initial items
            list_widget.addItems([f"Item {j + 1} (List {i + 1})" for j in range(3)])
            self.lists.append(list_widget)
            layout.addWidget(list_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(num_lists=3)  # Change num_lists to create more lists
    window.show()
    sys.exit(app.exec())


