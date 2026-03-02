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
                # Create QMimeData with item text and source widget ID
                mime_data = QMimeData()
                mime_data.setText(item.text())
                mime_data.setData("application/x-source-widget", str(id(self)).encode())

                # Create and start drag operation
                drag = QDrag(self)
                drag.setMimeData(mime_data)
                result = drag.exec(Qt.MoveAction)

                # If drop was successful and to another widget, remove the item
                if result == Qt.MoveAction and drag.target() != self:
                    print(f"{self.name}: Drop successful to another widget, removing item '{item.text()}'")
                    row = self.row(item)
                    self.takeItem(row)
                else:
                    print(f"{self.name}: Drop failed, canceled, or within same widget")

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Accept drag if it contains text and is a move action
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            print(f"{self.name}: Drag entered with text '{event.mimeData().text()}'")
            event.acceptProposedAction()
        else:
            print(f"{self.name}: Drag rejected (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        # Accept move events to ensure drop is allowed
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        # Handle drop for reordering within this list or adding from another list
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            text = event.mimeData().text()
            source_widget_id = event.mimeData().data("application/x-source-widget").data().decode()
            is_same_widget = source_widget_id == str(id(self))

            if is_same_widget:
                # Reorder within the same list
                drop_item = self.itemAt(event.pos())
                drop_row = self.row(drop_item) if drop_item else self.count()
                source_item = None
                for i in range(self.count()):
                    if self.item(i).text() == text:
                        source_item = self.item(i)
                        break
                if source_item:
                    source_row = self.row(source_item)
                    if source_row != drop_row:
                        print(f"{self.name}: Reordering item '{text}' from row {source_row} to {drop_row}")
                        item = self.takeItem(source_row)
                        self.insertItem(drop_row, item)
                    else:
                        print(f"{self.name}: Item '{text}' dropped at same position, no change")
            else:
                # Add item from another list
                print(f"{self.name}: Dropped item '{text}' from another widget")
                drop_item = self.itemAt(event.pos())
                drop_row = self.row(drop_item) if drop_item else self.count()
                self.insertItem(drop_row, text)

            event.acceptProposedAction()
        else:
            print(f"{self.name}: Drop rejected (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            event.ignore()

class MainWindow(QWidget):
    def __init__(self, num_lists=3):
        super().__init__()
        self.setWindowTitle("Drag and Drop Between N QListWidgets with Reordering")
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


