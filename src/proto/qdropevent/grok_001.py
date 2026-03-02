import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDrag

class DragSourceLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("border: 1px solid black; padding: 10px;")
        self._drag_data = text  # Data to send

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Create QMimeData and set the data
            mime_data = QMimeData()
            mime_data.setText(self._drag_data)  # Example: sending text data

            # Create and start the drag operation
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.CopyAction)

class DropTargetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)  # Enable drop events
        self.label = QLabel("Drop here", self)
        self.label.setStyleSheet("border: 2px dashed blue; padding: 20px;")
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Accept the drag event if it contains text
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        # Retrieve and display the dropped data
        if event.mimeData().hasText():
            text = event.mimeData().text()
            self.label.setText(f"Dropped: {text}")
            event.acceptProposedAction()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Example")
        layout = QVBoxLayout(self)

        # Create drag source and drop target
        source = DragSourceLabel("Drag this text")
        target = DropTargetWidget()

        layout.addWidget(source)
        layout.addWidget(target)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


