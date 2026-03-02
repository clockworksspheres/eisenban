import sys
from PySide6.QtWidgets import QApplication, QListWidget, QHBoxLayout, QWidget, QAbstractItemView
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QDragEnterEvent, QDragMoveEvent, QDropEvent

class DraggableListWidget(QListWidget):
    def __init__(self, name="List"):
        super().__init__()
        self.name = name
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.setStyleSheet("border: 2px solid black; padding: 5px; min-width: 200px; min-height: 200px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.position().toPoint())
            # item = self.itemAt(event.position())
            if item:
                print(f"{self.name}: Initiating drag for item '{item.text()}' at position {event.position().toPoint()}")
                mime_data = QMimeData()
                mime_data.setText(item.text())
                # mime_data.setData("application/x-source-widget", str(id(self)).encode())
                print(f"{self.name}: " + str(mime_data.hasText()))
                drag = QDrag(self)
                drag.setMimeData(mime_data)
                result = drag.exec(Qt.MoveAction)

                ###
                #  Drag result: Qt.MoveAction, target: None, is_same_widge    t: False
                target = drag.target()
                # print(f"{self.name}: Drag result: Qt.MoveAction, target: {type(target).__name__ if target else 'None'}, is_same_widge    t: {target == self}")
                print(f"target: {str(target)}")
                ###

                if result == Qt.MoveAction:
                    target = drag.target()
                    print(f"{self.name}: Drag result: Qt.MoveAction, target: {type(target).__name__ if target else 'None'}, is_same_widget: {target == self}")
                    if target and target != self:
                        print(f"{self.name}: Drop successful to another widget, removing item '{item.text()}'")
                        row = self.row(item)
                        if row >= 0:
                            self.takeItem(row)
                        else:
                            print(f"{self.name}: Item '{item.text()}' no longer exists")
                    else:
                        print(f"{self.name}: Drop within same widget, handled by dropEvent")
                elif result == Qt.IgnoreAction:
                    print(f"{self.name}: Drop failed or canceled (Qt.IgnoreAction)")
                else:
                    print(f"{self.name}: Unexpected drag result: {result}")
            else:
                print(f"{self.name}: No item at position {event.position().toPoint()}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData.hasText():
            print(f"{self.name}: Drag entered, text: '{event.mimeData().text()}', action: {event.proposedAction()}")
            event.acceptProposedAction()
        else:
            print(f"{self.name}: Drag rejected in dragEnterEvent (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            # event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData.hasText():
            event.acceptProposedAction()
        else:
            print(f"{self.name}: Drag rejected in dragMoveEvent (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            # event.ignore()

    def dropEvent(self, event: QDropEvent):
        print("Entered dropEvent")
        if event.mimeData.hasText():
            print("Entered if hasText()")
            text = event.mimeData().text()
            source_widget_id = event.mimeData().data("application/x-source-widget").data().decode()
            is_same_widget = source_widget_id == str(id(self))

            drop_index = self.indexAt(event.position().toPoint())
            drop_row = drop_index.row() if drop_index.isValid() else self.count()
            print(f"{self.name}: Drop position at row {drop_row} for item '{text}'")

            if is_same_widget:
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
                if source_row < drop_row:
                    drop_row -= 1
                if source_row != drop_row:
                    print(f"{self.name}: Reordering item '{text}' from row {source_row} to {drop_row}")
                    item = self.takeItem(source_row)
                    if item:
                        self.insertItem(drop_row, item)
                    else:
                        print(f"{self.name}: Failed to take item at row {source_row}")
                        event.ignore()
                        return
                else:
                    print(f"{self.name}: Item '{text}' dropped at same position, no change")
            else:
                print(f"{self.name}: Dropped item '{text}' from another widget")
                self.insertItem(drop_row, text)

            event.setDropAction(Qt.MoveAction)
            event.acceptProposedAction()
            print(f"{self.name}: Drop accepted with action: {event.dropAction()}")
        else:
            print(f"{self.name}: Drop rejected in dropEvent (hasText: {event.mimeData().hasText()}, action: {event.proposedAction()})")
            event.ignore()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Between Two QListWidgets with Reordering")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # Create two draggable list widgets
        self.list1 = DraggableListWidget("List 1")
        self.list2 = DraggableListWidget("List 2")
        self.list1.addItems([f"Item {i + 1} (List 1)" for i in range(3)])
        self.list2.addItems([f"Item {i + 1} (List 2)" for i in range(3)])
        layout.addWidget(self.list1)
        layout.addWidget(self.list2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())


