from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Configure drag-and-drop settings
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setAcceptDrops(True)
        # Enable multiple selection
        self.setSelectionMode(QListWidget.ExtendedSelection)

    def dropEvent(self, event):
        # Print MIME data formats and selected items for debugging
        print(f"Drop event in {self.objectName()}: MIME formats = {event.mimeData().formats()}")
        super().dropEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Multiple Items")
        self.resize(400, 300)

        # Create main widget and layout
        main_widget = QWidget()
        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        # Create source and target list widgets using CustomListWidget
        self.source_list = CustomListWidget()
        self.source_list.setObjectName("SourceList")
        self.target_list = CustomListWidget()
        self.target_list.setObjectName("TargetList")

        # Add sample items to source list
        for i in range(5):
            self.source_list.addItem(f"Item {i+1}")

        # Add widgets to layout
        layout.addWidget(self.source_list)
        layout.addWidget(self.target_list)

        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

