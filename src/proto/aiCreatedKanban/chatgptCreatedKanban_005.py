import sys
import json
import uuid
from datetime import date

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLabel,
    QInputDialog, QMessageBox, QScrollArea, QMenu,
    QDialog, QTextEdit, QComboBox, QDateEdit
)
from PySide6.QtGui import Qt, QUndoStack, QUndoCommand



# =========================
# MODEL
# =========================

class TaskModel:
    def __init__(self, title, description="", priority="Medium", due_date=None, task_id=None):
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return self.__dict__


class ColumnModel:
    def __init__(self, title):
        self.title = title
        self.tasks = []

    def to_dict(self):
        return {
            "title": self.title,
            "tasks": [t.to_dict() for t in self.tasks]
        }


class BoardModel:
    def __init__(self):
        self.columns = []

    def to_dict(self):
        return [c.to_dict() for c in self.columns]


# =========================
# UNDO COMMANDS
# =========================

class AddTaskCommand(QUndoCommand):
    def __init__(self, column, task):
        super().__init__("Add Task")
        self.column = column
        self.task = task

    def redo(self):
        self.column.tasks.append(self.task)

    def undo(self):
        self.column.tasks.remove(self.task)


class DeleteTaskCommand(QUndoCommand):
    def __init__(self, column, task):
        super().__init__("Delete Task")
        self.column = column
        self.task = task

    def redo(self):
        self.column.tasks.remove(self.task)

    def undo(self):
        self.column.tasks.append(self.task)


# =========================
# VIEW HELPERS
# =========================

class TaskDialog(QDialog):
    def __init__(self, task=None):
        super().__init__()
        self.setWindowTitle("Task")

        layout = QVBoxLayout(self)

        self.title = QInputDialog()
        self.title_edit = QTextEdit(task.title if task else "")
        self.desc_edit = QTextEdit(task.description if task else "")

        self.priority = QComboBox()
        self.priority.addItems(["Low", "Medium", "High"])
        if task:
            self.priority.setCurrentText(task.priority)

        self.due = QDateEdit()
        self.due.setCalendarPopup(True)
        self.due.setDate(date.today())

        save = QPushButton("Save")
        save.clicked.connect(self.accept)

        layout.addWidget(QLabel("Title"))
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.desc_edit)
        layout.addWidget(QLabel("Priority"))
        layout.addWidget(self.priority)
        layout.addWidget(QLabel("Due Date"))
        layout.addWidget(self.due)
        layout.addWidget(save)

    def data(self):
        return {
            "title": self.title_edit.toPlainText(),
            "description": self.desc_edit.toPlainText(),
            "priority": self.priority.currentText(),
            "due_date": self.due.date().toString(Qt.ISODate)
        }


# =========================
# VIEW
# =========================

class KanbanColumnView(QWidget):
    def __init__(self, model, undo_stack):
        super().__init__()
        self.model = model
        self.undo = undo_stack

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.title = QLabel(model.title)
        self.title.setStyleSheet("font-weight:bold")

        self.list = QListWidget()
        self.list.setDragDropMode(QListWidget.DragDrop)
        self.list.setDefaultDropAction(Qt.MoveAction)

        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.menu)

        add = QPushButton("+ Task")
        add.clicked.connect(self.add_task)

        layout.addWidget(self.title)
        layout.addWidget(self.list)
        layout.addWidget(add)

        self.refresh()

    def refresh(self):
        self.list.clear()
        for task in self.model.tasks:
            item = QListWidgetItem(f"{task.title}  [{task.priority}]")
            item.setData(Qt.UserRole, task)
            self.list.addItem(item)

    def add_task(self):
        dlg = TaskDialog()
        if dlg.exec():
            data = dlg.data()
            task = TaskModel(**data)
            self.undo.push(AddTaskCommand(self.model, task))
            self.refresh()

    def menu(self, pos):
        item = self.list.itemAt(pos)
        if not item:
            return

        task = item.data(Qt.UserRole)
        menu = QMenu(self)
        delete = menu.addAction("Delete")
        if menu.exec(self.list.mapToGlobal(pos)) == delete:
            self.undo.push(DeleteTaskCommand(self.model, task))
            self.refresh()


class KanbanBoardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVC Kanban Board")
        self.resize(1100, 550)

        self.model = BoardModel()
        self.undo = QUndoStack(self)

        main = QVBoxLayout(self)

        controls = QHBoxLayout()
        undo = QPushButton("Undo")
        redo = QPushButton("Redo")
        undo.clicked.connect(self.undo.undo)
        redo.clicked.connect(self.undo.redo)
        controls.addWidget(undo)
        controls.addWidget(redo)
        main.addLayout(controls)

        self.container = QWidget()
        self.columns_layout = QHBoxLayout(self.container)
        self.columns_layout.setAlignment(Qt.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container)
        main.addWidget(scroll)

        for name in ("To Do", "In Progress", "Done"):
            self.add_column(name)

    def add_column(self, title):
        col = ColumnModel(title)
        self.model.columns.append(col)
        view = KanbanColumnView(col, self.undo)
        self.columns_layout.addWidget(view)


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = KanbanBoardView()
    win.show()
    sys.exit(app.exec())

