import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton, QLineEdit,
    QMessageBox, QScrollArea, QInputDialog, QMenu
)
from PySide6.QtCore import Qt, QMimeData, QByteArray
from PySide6.QtGui import QAction

DATA_FILE = "kanban_data.json"
CUSTOM_MIME = "application/x-kanban-card-text"

class CardItem(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        layout.setContentsMargins(8, 8, 8, 8)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 4px;
            }
            QWidget:hover {
                background-color: #f5f5f5;
            }
        """)

class KanbanColumn(QListWidget):
    def __init__(self, title="New Column"):
        super().__init__()
        self.title = title
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

    def mimeTypes(self):
        return [CUSTOM_MIME] + super().mimeTypes()

    def mimeData(self, items):
        mime = super().mimeData(items)
        if items:
            item = items[0]
            widget = self.itemWidget(item)
            if widget and isinstance(widget, CardItem):
                mime.setData(CUSTOM_MIME, widget.label.text().encode("utf-8"))
        return mime

    def dropEvent(self, event):
        source = event.source()

        # Let Qt perform the actual move first
        super().dropEvent(event)

        # Re-apply the custom card using our serialized text
        if event.mimeData().hasFormat(CUSTOM_MIME):
            text = event.mimeData().data(CUSTOM_MIME).data().decode("utf-8")

            # The dropped item is usually the last one added (or currentItem)
            dropped_item = self.item(self.count() - 1)
            if dropped_item is None:
                dropped_item = self.currentItem()

            if dropped_item and self.itemWidget(dropped_item) is None:
                card = CardItem(text)
                dropped_item.setSizeHint(card.sizeHint())
                self.setItemWidget(dropped_item, card)

        # Save after successful drop
        window = self.window()
        if isinstance(window, KanbanBoard):
            window.save_data()

class KanbanBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Kanban Board - Working Drag & Drop")
        self.resize(1400, 800)

        self.columns = {}
        self.column_order = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.add_column_widget = self.create_add_column_widget()
        self.main_layout.addWidget(self.add_column_widget)

        self.load_data()

        if not self.column_order:
            for title in ["To Do", "In Progress", "Done"]:
                self.add_column(title)

    def create_column_widget(self, title):
        column = KanbanColumn(title)

        col_container = QWidget()
        col_layout = QVBoxLayout(col_container)

        header = QLabel(f"<h2>{title}</h2>")
        header.setAlignment(Qt.AlignCenter)
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(lambda pos, t=title: self.column_context_menu(pos, t))
        col_layout.addWidget(header)

        input_layout = QHBoxLayout()
        task_input = QLineEdit()
        task_input.setPlaceholderText("New task...")
        task_input.returnPressed.connect(lambda: self.add_task(title, task_input))
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(lambda: self.add_task(title, task_input))
        input_layout.addWidget(task_input)
        input_layout.addWidget(add_btn)
        col_layout.addLayout(input_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(column)
        scroll.setMinimumWidth(300)
        scroll.setMaximumWidth(400)
        col_layout.addWidget(scroll)

        del_btn = QPushButton("Delete Selected")
        del_btn.clicked.connect(lambda: self.delete_selected(column))
        col_layout.addWidget(del_btn)

        return col_container, column, task_input

    def add_column(self, title):
        if title in self.columns:
            QMessageBox.warning(self, "Duplicate", f"Column '{title}' already exists.")
            return

        col_widget, column, task_input = self.create_column_widget(title)

        self.columns[title] = {
            "widget": column,
            "container": col_widget,
            "input": task_input
        }
        self.column_order.append(title)
        self.main_layout.insertWidget(self.main_layout.count() - 1, col_widget)
        self.save_data()

    def rename_column(self, old_title):
        new_title, ok = QInputDialog.getText(self, "Rename Column", "New name:", text=old_title)
        if not ok or not new_title.strip() or new_title == old_title:
            return
        new_title = new_title.strip()
        if new_title in self.columns:
            QMessageBox.warning(self, "Error", "Column name already exists.")
            return

        col_data = self.columns.pop(old_title)
        col_data["widget"].title = new_title
        header = col_data["container"].layout().itemAt(0).widget()
        header.setText(f"<h2>{new_title}</h2>")
        self.columns[new_title] = col_data
        idx = self.column_order.index(old_title)
        self.column_order[idx] = new_title
        self.save_data()

    def delete_column(self, title):
        if len(self.columns) <= 1:
            QMessageBox.warning(self, "Error", "Cannot delete the last column.")
            return
        reply = QMessageBox.question(self, "Delete", f"Delete '{title}' and all its tasks?")
        if reply == QMessageBox.Yes:
            col_data = self.columns.pop(title)
            self.main_layout.removeWidget(col_data["container"])
            col_data["container"].deleteLater()
            self.column_order.remove(title)
            self.save_data()

    def column_context_menu(self, pos, title):
        menu = QMenu(self)
        menu.addAction(QAction("Rename Column", self, triggered=lambda: self.rename_column(title)))
        menu.addAction(QAction("Delete Column", self, triggered=lambda: self.delete_column(title)))
        menu.exec(self.sender().mapToGlobal(pos))

    def create_add_column_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addStretch()
        btn = QPushButton("＋ Add Column")
        btn.setFixedWidth(300)
        btn.setStyleSheet("padding: 15px; font-size: 16px;")
        btn.clicked.connect(self.prompt_new_column)
        layout.addWidget(btn)
        layout.addStretch()
        return widget

    def prompt_new_column(self):
        title, ok = QInputDialog.getText(self, "New Column", "Column name:")
        if ok and title.strip():
            self.add_column(title.strip())

    def add_task(self, column_title, input_widget):
        text = input_widget.text().strip()
        if not text:
            return
        column = self.columns[column_title]["widget"]
        item = QListWidgetItem(column)
        card = CardItem(text)
        item.setSizeHint(card.sizeHint())
        column.addItem(item)
        column.setItemWidget(item, card)
        input_widget.clear()
        self.save_data()

    def delete_selected(self, column):
        item = column.currentItem()
        if item and QMessageBox.question(self, "Delete", "Delete this task?") == QMessageBox.Yes:
            row = column.row(item)
            column.takeItem(row)
            self.save_data()

    def save_data(self):
        data = {"column_order": self.column_order, "columns": {}}
        for title in self.column_order:
            column = self.columns[title]["widget"]
            tasks = []
            for i in range(column.count()):
                widget = column.itemWidget(column.item(i))
                if widget:
                    tasks.append(widget.label.text())
            data["columns"][title] = tasks
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Save failed: {e}")

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for title in data.get("column_order", []):
                if title in data.get("columns", {}):
                    self.add_column(title)
                    column = self.columns[title]["widget"]
                    for text in data["columns"][title]:
                        item = QListWidgetItem(column)
                        card = CardItem(text)
                        item.setSizeHint(card.sizeHint())
                        column.addItem(item)
                        column.setItemWidget(item, card)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Load failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = KanbanBoard()
    window.show()
    sys.exit(app.exec())

