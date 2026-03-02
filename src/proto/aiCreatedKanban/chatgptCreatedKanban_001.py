import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton,
    QInputDialog, QLabel, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt


class KanbanColumn(QWidget):
    def __init__(self, title, remove_callback):
        super().__init__()

        self.remove_callback = remove_callback

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold;")
        delete_btn = QPushButton("✕")
        delete_btn.setFixedWidth(25)
        delete_btn.clicked.connect(self.delete_column)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(delete_btn)

        # Task list
        self.list_widget = QListWidget()
        self.list_widget.setDragEnabled(True)
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDropIndicatorShown(True)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)
        self.list_widget.setDragDropMode(QListWidget.InternalMove)

        # Add task button
        add_task_btn = QPushButton("+ Add Task")
        add_task_btn.clicked.connect(self.add_task)

        layout.addLayout(header_layout)
        layout.addWidget(self.list_widget)
        layout.addWidget(add_task_btn)

        self.setFixedWidth(220)

    def add_task(self):
        text, ok = QInputDialog.getText(self, "New Task", "Task name:")
        if ok and text.strip():
            self.list_widget.addItem(QListWidgetItem(text))

    def delete_column(self):
        reply = QMessageBox.question(
            self,
            "Delete Column",
            "Are you sure you want to delete this column?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.remove_callback(self)


class KanbanBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Kanban Board")
        self.resize(900, 400)

        main_layout = QVBoxLayout(self)

        # Top controls
        add_column_btn = QPushButton("+ Add Column")
        add_column_btn.clicked.connect(self.add_column)
        main_layout.addWidget(add_column_btn)

        # Scrollable area for columns
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

    def add_column(self, name=None):
        if not name:
            name, ok = QInputDialog.getText(self, "New Column", "Column name:")
            if not ok or not name.strip():
                return

        column = KanbanColumn(name, self.remove_column)
        self.columns_layout.addWidget(column)

    def remove_column(self, column):
        column.setParent(None)
        column.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KanbanBoard()
    window.show()
    sys.exit(app.exec())

