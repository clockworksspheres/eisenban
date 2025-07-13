from PySide6 import QtWidgets, QtCore

class MyListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            # Add the dropped items to the list
            for link in links:
                item = QtWidgets.QListWidgetItem(link)
                self.addItem(item)
        else:
            super().dropEvent(event)

# Usage
app = QtWidgets.QApplication([])
list_widget1 = MyListWidget()
list_widget2 = MyListWidget()

layout = QtWidgets.QVBoxLayout()
layout.addWidget(list_widget1)
layout.addWidget(list_widget2)

window = QtWidgets.QWidget()
window.setLayout(layout)
window.show()

app.exec()

