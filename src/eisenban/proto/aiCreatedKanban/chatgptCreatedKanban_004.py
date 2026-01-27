import sys
import json
import uuid
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton,
    QInputDialog, QLabel, QMessageBox, QScrollArea,
    QFileDialog, QMenu
)
from PySide6.QtCore import Qt

AUTOSAVE_FILE = "kanban_autosave.json"


# ---------------- TASK ITEM ----------------
class TaskItem(QListWidgetItem):
    def __init__(self, title, task_id=None, created_at=None):
        super().__init__(title)

        self.task_id = task_id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now().isoformat()

        self.setData(Qt.UserRole, {
            "id": self.task_id,
            "created_at": self.created_at
        })


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
        self.title_label.mouseDoubleClickEvent = self.rename_column

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

        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(
            self.show_task_menu
        )
        self.list_widget.itemDoubleClicked.connect(
            self.rename_task
        )

        # Add task
        add_task_btn = QPushButton("+ Add Task")
        add_task_btn.clicked.connect(self.add_task)

        layout.addLayout(header)
        layout.addWidget(self.list_widget)
        layout.addWidget(add_task_btn)

        self.setFixedWidth(240)

    # ---------- Column ----------
    def rename_column(self, event):
        text, ok = QInputDialog.getText(
            self, "Rename Column", "Column name:",
            text=self.title_label.text()
        )
        if ok and text.strip():
            self.title_label.setText(text)

    def delete_column(self):
        if QMessageBox.question(
            self, "Delete Column",
            "Delete this column and all tasks?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            self.remove_callback(self)

    # ---------- Tasks ----------
    def add_task(self):
        text, ok = QInputDialog.getText(
            self, "New Task", "Task title:"
        )
        if ok and text.strip():
            self.list_widget.addItem(TaskItem(text))

    def rename_task(self, item):
        text, ok = QInputDialog.getText(
            self, "Rename Task", "Task title:",
            text=item.text()
        )
        if ok and text.strip():
            item.setText(text)

    def delete_task(self):
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
        rename = menu.addAction("Rename")
        delete = menu.addAction("Delete")

        action = menu.exec(self.list_widget.mapToGlobal(pos))
        if action == rename:
            self.rename_task(item)
        elif action == delete:
            self.delete_task()

    # ---------- Serialization ----------
    def to_dict(self):
        return {
            "title": self.title_label.text(),
            "tasks": [
                {
                    "id": item.data(Qt.UserRole)["id"],
                    "title": item.text(),
                    "created_at": item.data(Qt.UserRole)["created_at"]
                }
                for item in (
                    self.list_widget.item(i)
                    for i in range(self.list_widget.count())
                )
            ]
        }

    def from_dict(self, data):
        self.title_label.setText(data["title"])
        self.list_widget.clear()
        for task in data["tasks"]:
            self.list_widget.addItem(
                TaskItem(
                    task["title"],
                    task["id"],
                    task["created_at"]
                )
            )


# ---------------- BOARD ----------------
class KanbanBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced PySide6 Kanban")
        self.resize(1000, 500)

        main = QVBoxLayout(self)

        # Controls
        controls = QHBoxLayout()
        add_col = QPushButton("+ Column")
        save_btn = QPushButton("💾 Save")
        load_btn = QPushButton("📂 Load")

        add_col.clicked.connect(self.add_column)
        save_btn.clicked.connect(self.save_json)
        load_btn.clicked.connect(self.load_json)

        controls.addWidget(add_col)
        controls.addStretch()
        controls.addWidget(save_btn)
        controls.addWidget(load_btn)
        main.addLayout(controls)

        # Scroll area
        self.container = QWidget()
        self.columns_layout = QHBoxLayout(self.container)
        self.columns_layout.setAlignment(Qt.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container)
        main.addWidget(scroll)

        # Load autosave or defaults
        if not self.load_autosave():
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

        col = KanbanColumn(name, self.remove_column)
        self.columns_layout.addWidget(col)

    def remove_column(self, col):
        col.setParent(None)
        col.deleteLater()

    def clear(self):
        while self.columns_layout.count():
            w = self.columns_layout.takeAt(0).widget()
            if w:
                w.deleteLater()

    # ---------- Persistence ----------
    def serialize(self):
        return [
            self.columns_layout.itemAt(i).widget().to_dict()
            for i in range(self.columns_layout.count())
        ]

    def deserialize(self, data):
        self.clear()
        for col in data:
            widget = KanbanColumn(col["title"], self.remove_column)
            widget.from_dict(col)
            self.columns_layout.addWidget(widget)

    def save_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Board", "", "JSON (*.json)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.serialize(), f, indent=2)

    def load_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Board", "", "JSON (*.json)"
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.deserialize(json.load(f))

    def load_autosave(self):
        try:
            with open(AUTOSAVE_FILE, "r", encoding="utf-8") as f:
                self.deserialize(json.load(f))
            return True
        except Exception:
            return False

    def closeEvent(self, event):
        with open(AUTOSAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.serialize(), f, indent=2)
        event.accept()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    board = KanbanBoard()
    board.show()
    sys.exit(app.exec())


