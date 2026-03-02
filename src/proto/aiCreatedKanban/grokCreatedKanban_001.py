import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QPushButton, QLineEdit, QMessageBox,
    QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

DATA_FILE = "kanban_data.json"

class CardItem(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 8px;
                margin: 4px;
            }
        """)

class KanbanColumn(QListWidget):
    def __init__(self, title):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerItem)
        self.title = title

    def startDrag(self, event):
        index = self.currentIndex()
        if not index.isValid():
            return
        drag = QDrag(self)
        mime = self.mimeData([index])
        drag.setMimeData(mime)
        # Optional: set a pixmap preview
        item_widget = self.itemWidget(self.itemFromIndex(index))
        if item_widget:
            pixmap = item_widget.grab()
            drag.setPixmap(pixmap)
        drag.exec(Qt.MoveAction)

class KanbanBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple PySide6 Kanban Board")
        self.resize(1200, 800)

        self.columns = {
            "To Do": KanbanColumn("To Do"),
            "In Progress": KanbanColumn("In Progress"),
            "Done": KanbanColumn("Done")
        }

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        for title, column in self.columns.items():
            col_widget = QWidget()
            col_layout = QVBoxLayout(col_widget)

            header = QLabel(f"<h2>{title}</h2>")
            header.setAlignment(Qt.AlignCenter)
            col_layout.addWidget(header)

            # Add task input
            input_layout = QHBoxLayout()
            self.task_input = QLineEdit()
            self.task_input.setPlaceholderText("Enter new task...")
            add_btn = QPushButton("Add")
            add_btn.clicked.connect(lambda _, t=title: self.add_task(t))
            input_layout.addWidget(self.task_input)
            input_layout.addWidget(add_btn)
            col_layout.addLayout(input_layout)

            # The list
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(column)
            scroll.setMinimumWidth(300)
            col_layout.addWidget(scroll)

            # Delete selected button
            del_btn = QPushButton("Delete Selected")
            del_btn.clicked.connect(lambda _, c=column: self.delete_selected(c))
            col_layout.addWidget(del_btn)

            main_layout.addWidget(col_widget)

        self.load_data()

    def add_task(self, column_title):
        text = self.task_input.text().strip()
        if not text:
            return
        column = self.columns[column_title]
        item = QListWidgetItem(column)
        card = CardItem(text)
        item.setSizeHint(card.sizeHint())
        column.addItem(item)
        column.setItemWidget(item, card)
        self.task_input.clear()
        self.save_data()

    def delete_selected(self, column):
        item = column.currentItem()
        if item:
            reply = QMessageBox.question(self, "Confirm Delete", "Delete this task?")
            if reply == QMessageBox.Yes:
                row = column.row(item)
                column.takeItem(row)
                self.save_data()

    def save_data(self):
        data = {}
        for title, column in self.columns.items():
            tasks = []
            for i in range(column.count()):
                item = column.item(i)
                widget = column.itemWidget(item)
                if widget:
                    tasks.append(widget.label.text())
            data[title] = tasks
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", str(e))

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            for title, tasks in data.items():
                if title in self.columns:
                    column = self.columns[title]
                    for task_text in tasks:
                        item = QListWidgetItem(column)
                        card = CardItem(task_text)
                        item.setSizeHint(card.sizeHint())
                        column.addItem(item)
                        column.setItemWidget(item, card)
        except Exception as e:
            QMessageBox.warning(self, "Load Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Nice modern look
    window = KanbanBoard()
    window.show()
    sys.exit(app.exec())

