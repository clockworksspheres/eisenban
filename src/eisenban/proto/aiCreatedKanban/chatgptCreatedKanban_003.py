import sys
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton,
    QInputDialog, QLabel, QMessageBox, QScrollArea,
    QFileDialog, QMenu
)
from PySide6.QtCore import Qt


# ---------------- COLUMN ----------------
class KanbanColumn(QWidget):
    def __init__(self, title, remove_callback):
        super().__init__()
        self.remove_callback = remove_callback

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Header
        header = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold;")

        delete_btn = QPushButton("✕")
        delete_btn.setFixedWidth(24)
        delete_btn.clicked.connect(self.delete_column)

        header.addWidget(self.title_label)
        header.addStretch()
        header.addWidget(delete_btn)

        # Task list
        self.list_widget = QListWidget()
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)
        self.list_widget.setDragDropMode(QListWidget.DragDrop)

        # Task deletion
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(
            self.show_task_menu
        )

        # Add task button
        add_task_btn = QPushButton("+ Add Task")
        add_task_btn.clicked.connect(self.add_task)

        layout.addLayout(header)
        layout.addWidget(self.list_widget)
        layout.addWidget(add_task_btn)

        self.setFixedWidth(230)

    # ---------- Tasks ----------
    def add_task(self):
        text, ok = QInputDialog.getText(self, "New Task", "Task name:")
        if ok and text.strip():
            self.list_widget.addItem(QListWidgetItem(text))

    def delete_selected_task(self):
        item = self.list_widget.currentItem()
        if item:
            self.list_widget.takeItem(
                self.list_widget.row(item)
            )

    def show_task_menu(self, pos):
        item = self.list_widget.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)
        delete_action = menu.addAction("Delete Task")
        action = menu.exec(self.list_widget.mapToGlobal(pos))

        if action == delete_action:
            self.delete_selected_task()

    # ---------- Column ----------
    def delete_column(self):
        reply = QMessageBox.question(
            self,
            "Delete Column",
            "Delete this column and all its tasks?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.remove_callback(self)

    # ---------- Serialization ----------
    def to_dict(self):
        return {
            "title": self.title_label.text(),
            "tasks": [
                self.list_widget.item(i).text()
                for i in range(self.list_widget.count())
            ]
        }

    def from_dict(self, data):
        self.title_label.setText(data["title"])
        self.list_widget.clear()
        for task in data["tasks"]:
            self.list_widget.addItem(task)


# ---------------- BOARD ----------------
class KanbanBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Kanban Board")
        self.resize(950, 480)

        main_layout = QVBoxLayout(self)

        # Top buttons
        controls = QHBoxLayout()
        add_col_btn = QPushButton("+ Add Column")
        save_btn = QPushButton("💾 Save")
        load_btn = QPushButton("📂 Load")

        add_col_btn.clicked.connect(self.add_column)
        save_btn.clicked.connect(self.save_to_json)
        load_btn.clicked.connect(self.load_from_json)

        controls.addWidget(add_col_btn)
        controls.addStretch()
        controls.addWidget(save_btn)
        controls.addWidget(load_btn)

        main_layout.addLayout(controls)

        # Scroll area
        self.columns_container = QWidget()
        self.columns_layout = QHBoxLayout(self.columns_container)
        self.columns_layout.setAlignment(Qt.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.columns_container)

        main_layout.addWidget(scroll)

        # Default columns
        for name in ("To Do", "In Progress", "Done"):
            self.add_column(name)

    # ---------- Columns ----------
    def add_column(self, name=None):
        if not name:
            name, ok = QInputDialog.getText(
                self, "New Column", "Column name:"
            )
            if not ok or not name.strip():
                return

        column = KanbanColumn(name, self.remove_column)
        self.columns_layout.addWidget(column)

    def remove_column(self, column):
        column.setParent(None)
        column.deleteLater()

    def clear_columns(self):
        while self.columns_layout.count():
            item = self.columns_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # ---------- Save / Load ----------
    def save_to_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Board", "", "JSON Files (*.json)"
        )
        if not path:
            return

        data = [
            self.columns_layout.itemAt(i).widget().to_dict()
            for i in range(self.columns_layout.count())
        ]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_from_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Board", "", "JSON Files (*.json)"
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.clear_columns()
        for col_data in data:
            column = KanbanColumn(
                col_data["title"], self.remove_column
            )
            column.from_dict(col_data)
            self.columns_layout.addWidget(column)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    board = KanbanBoard()
    board.show()
    sys.exit(app.exec())


