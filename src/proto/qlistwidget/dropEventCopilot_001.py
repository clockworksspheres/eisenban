from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QListWidget

class CustomListWidget(QListWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.name = name

    def dropEvent(self, event: QDropEvent):
        super().dropEvent(event)
        print(f"Item dropped into {self.name}")
        for item in self.selectedItems():
            print(f"→ {item.text()}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Drag and Drop")

        layout = QVBoxLayout(self)

        self.list1 = CustomListWidget("List 1")
        self.list2 = CustomListWidget("List 2")

        self.list1.setDragEnabled(True)
        self.list2.setDragEnabled(True)

        for i in range(5):
            item = QListWidgetItem(f"Item {i}")
            self.list1.addItem(item)

        layout.addWidget(self.list1)
        layout.addWidget(self.list2)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(300, 400)
    window.show()
    app.exec()

