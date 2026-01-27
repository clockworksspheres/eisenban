import sys
from PySide6.QtWidgets import QApplication, QListWidget, QHBoxLayout, QWidget, QAbstractItemView
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent

class DraggableListWidget(QListWidget):
    def __init__(self, name="List"):
        super().__init__()
        self.name = name  # For debugging
        self.setDragEnabled(True)  # Enable custom dragging
        self.setAcceptDrops(True)  # Enable dropping
        self.setDefaultDropAction(Qt.MoveAction)  # Default to move action
        self.setSelectionMode(QListWidget.SingleSelection)  # Single item selection
        self.setDragDropMode(QAbstractItemView.NoDragDrop)  # Disable built-in drag-and-drop
        self.setStyleSheet("border: 2px solid black; padding: 5px; min-width: 150px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item:
                print(f"{self.name}: Initiating drag for item '{item.text()}'")
                # Store item text and source widget ID in QMimeData
                mime_data = QMimeData()
                mime_data.setText(item.text())
                mime_data.setData("application/x-source-widget", str(id(self)).encode())

                # Start drag operation
                drag = QDrag(self)
                drag.setMimeData(mime_data)
                result = drag.exec(Qt.MoveAction)

                # Remove item only if dropped to another widget
                if result == Qt.MoveAction:
                    if drag.target() and drag.target() != self:
                        print(f"{self.name}: Drop successful to another widget, removing item '{item.text()}'")
                        row = self.row(item)
                        if row >= 0:  # Ensure item still exists
                            self.takeItem(row)
                    else:
                        print(f"{self.name}: Drop within same widget, handled by dropEvent")
                else:
                    print(f"{self.name}: Drop failed or canceled")
            else:
                print(f"{self.name}: No item at position {event.pos()}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Accept any move action with text
        if event.mimeData().hasText():
            print(f"{self.name}: Drag entered with text '{event.mimeData().text()}'")
            event.acceptProposedAction()
        else:
            print(f"{self.name}: Drag rejected (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        # Accept move events to allow dropping
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            source_widget_id = event.mimeData().data("application/x-source-widget").data().decode()
            is_same_widget = source_widget_id == str(id(self))

            # Calculate drop row
            drop_index = self.indexAt(event.pos())
            drop_row = drop_index.row() if drop_index.isValid() else self.count()
            print(f"{self.name}: Drop position at row {drop_row} for item '{text}'")

            if is_same_widget:
                # Reorder within the same list
                source_row = -1
                for i in range(self.count()):
                    item = self.item(i)
                    if item and item.text() == text:
                        source_row = i
                        break
                if source_row == -1:
                    print(f"{self.name}: Source item '{text}' not found, ignoring reorder")
                    event.ignore()
                    return
                # Adjust drop row for removal
                if source_row < drop_row:
                    drop_row -= 1
                # Reorder only if positions differ
                if source_row != drop_row and source_row != drop_row - 1:
                    print(f"{self.name}: Reordering item '{text}' from row {source_row} to {drop_row}")
                    item = self.takeItem(source_row)
                    if item:  # Ensure item is valid
                        self.insertItem(drop_row, item)
                    else:
                        print(f"{self.name}: Failed to take item at row {source_row}")
                        event.ignore()
                        return
                else:
                    print(f"{self.name}: Item '{text}' dropped at same or adjacent position, no change")
            else:
                # Add item from another list
                print(f"{self.name}: Dropped item '{text}' from another widget")
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


