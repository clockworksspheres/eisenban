from PySide6 import QtGui, QtCore, QtWidgets
import sys
import pathlib

class ThumbListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.model().rowsInserted.connect(self.handleRowsInserted, QtCore.Qt.QueuedConnection)

    def handleRowsInserted(self, parent, first, last):
        for index in range(first, last + 1):
            item = self.item(index)
            if item is not None and self.itemWidget(item) is None:
                index, name, icon = item.data(QtCore.Qt.UserRole)
                widget = QCustomQWidget()
                widget.setTextUp(index)
                widget.setTextDown(name)
                widget.setIcon(icon)
                item.setSizeHint(widget.sizeHint())
                self.setItemWidget(item, widget)

class Dialog_01(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.listItems = {}
        myQWidget = QtWidgets.QWidget()
        myBoxLayout = QtWidgets.QHBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)

        self.myQListWidget = ThumbListWidget(self)
        myBoxLayout.addWidget(self.myQListWidget)

        images_files_dir = pathlib.Path(__file__).parent.absolute().joinpath("custom_qlistwidget")
        for data in [
            ('No.1', 'Meyoko', pathlib.Path(images_files_dir).joinpath('among-us-small-green.png')),
            ('No.2', 'Nyaruko', pathlib.Path(images_files_dir).joinpath('among-us-small-yellow.png')),
            ('No.3', 'Louise', pathlib.Path(images_files_dir).joinpath('among-us-small-red.png'))
        ]:
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setData(QtCore.Qt.UserRole, data)
            self.myQListWidget.addItem(myQListWidgetItem)

        self.listWidgetB = ThumbListWidget(self)
        myBoxLayout.addWidget(self.listWidgetB)

class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        self.textDownQLabel = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.iconQLabel = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480, 320)
    sys.exit(app.exec())


