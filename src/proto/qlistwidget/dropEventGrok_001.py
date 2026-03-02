from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop QListWidgets")
        self.resize(400, 300)

        # Create main widget and layout
        main_widget = QWidget()
        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        # Create source and target list widgets
        self.source_list = QListWidget()
        self.target_list = QListWidget()

        # Enable drag and drop
        self.source_list.setDragEnabled(True)
        self.source_list.setDragDropMode(QListWidget.DragDrop)
        self.source_list.setDefaultDropAction(Qt.MoveAction)
        self.source_list.setAcceptDrops(True)

        self.target_list.setAcceptDrops(True)
        self.target_list.setDragDropMode(QListWidget.DragDrop)
        self.target_list.setDefaultDropAction(Qt.MoveAction)

        # Add some sample items to source list
        for i in range(5):
            self.source_list.addItem(f"Item {i+1}")

        # Add widgets to layout
        layout.addWidget(self.source_list)
        layout.addWidget(self.target_list)

        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

