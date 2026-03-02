import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QDragEnterEvent, QDropEvent

class DragSourceLabel(QLabel):
    def __init__(self, text, is_draggable=False):
        super().__init__(text)
        self.setStyleSheet("border: 1px solid black; padding: 10px;")
        self._drag_data = text if is_draggable else None  # Only store data for draggable fields
        self._is_draggable = is_draggable  # Flag to indicate if this label is draggable

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._is_draggable:
            # Create QMimeData and set the data
            mime_data = QMimeData()
            mime_data.setText(self._drag_data)

            # Create and start the drag operation
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            # Use Qt.MoveAction to indicate a move operation
            result = drag.exec(Qt.MoveAction)

            # If the drop was accepted, clear the source text
            if result == Qt.MoveAction:
                self.setText("")
                self._drag_data = None
                self._is_draggable = False  # Prevent further drags

class DropTargetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)  # Enable drop events
        self.label = QLabel("Drop here", self)
        self.label.setStyleSheet("border: 2px dashed blue; padding: 20px;")
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Accept the drag event if it contains text and is a move action
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        # Retrieve and display the dropped data
        if event.mimeData().hasText() and event.proposedAction() == Qt.MoveAction:
            text = event.mimeData().text()
            self.label.setText(f"Dropped: {text}")
            event.acceptProposedAction()  # Accept the move action

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Click and Drag Specific Field with Delete")
        layout = QVBoxLayout(self)

        # Create multiple source labels, only some are draggable
        source1 = DragSourceLabel("Draggable Field", is_draggable=True)
        source2 = DragSourceLabel("Non-Draggable Field", is_draggable=False)
        source3 = DragSourceLabel("Another Draggable Field", is_draggable=True)
        target = DropTargetWidget()

        # Add widgets to layout
        layout.addWidget(source1)
        layout.addWidget(source2)
        layout.addWidget(source3)
        layout.addWidget(target)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


