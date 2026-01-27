import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QHBoxLayout, QWidget, QListWidget, 
                              QListWidgetItem, QLabel, QPushButton)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPainter


class DragDropListWidget(QListWidget):
    """Custom QListWidget with drag and drop functionality"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasText():
            # Get the text data
            text = event.mimeData().text()
            
            # Create new item at drop position
            drop_row = self.indexAt(event.position().toPoint()).row()
            if drop_row == -1:
                drop_row = self.count()
                
            new_item = QListWidgetItem(text)
            self.insertItem(drop_row, new_item)
            
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()
            
    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            # Create mime data
            mimeData = QMimeData()
            mimeData.setText(item.text())
            
            # Create drag object
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            
            # Create drag pixmap (optional visual feedback)
            pixmap = item.data(Qt.ItemDataRole.DecorationRole)
            if not pixmap:
                # Create a simple text pixmap if no icon
                from PySide6.QtGui import QPixmap, QPainter, QFont
                pixmap = QPixmap(100, 30)
                pixmap.fill(Qt.GlobalColor.lightGray)
                painter = QPainter(pixmap)
                painter.setPen(Qt.GlobalColor.black)
                painter.setFont(QFont("Arial", 10))
                painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, item.text())
                painter.end()
            
            drag.setPixmap(pixmap)
            
            # Execute drag
            result = drag.exec(supportedActions)
            
            # Remove original item if move was successful
            if result == Qt.DropAction.MoveAction:
                self.takeItem(self.row(item))


class CrossListDragDropWidget(QListWidget):
    """List widget that can accept drops from other lists"""
    
    def __init__(self, accept_external=True, parent=None):
        super().__init__(parent)
        self.accept_external = accept_external
        self.setDragDropMode(QListWidget.DragDropMode.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            if self.accept_external or event.source() == self:
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            
            # Avoid duplicates in the same list
            existing_items = [self.item(i).text() for i in range(self.count())]
            if text not in existing_items:
                drop_row = self.indexAt(event.position().toPoint()).row()
                if drop_row == -1:
                    drop_row = self.count()
                    
                new_item = QListWidgetItem(text)
                self.insertItem(drop_row, new_item)
                
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()
            
    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            mimeData = QMimeData()
            mimeData.setText(item.text())
            
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            
            # Execute drag (copy mode - don't remove original)
            drag.exec(Qt.DropAction.CopyAction)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Drag and Drop List Widgets")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Drag and Drop List Widgets Demo")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)
        
        # Create horizontal layout for list widgets
        lists_layout = QHBoxLayout()
        
        # Left column - Single list reordering
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Reorderable List (Move items within list):"))
        
        self.reorder_list = DragDropListWidget()
        self.reorder_list.addItems([
            "Item 1 - Drag me!",
            "Item 2 - Reorder me!",
            "Item 3 - Move me around!",
            "Item 4 - I can be moved!",
            "Item 5 - Drag and drop!"
        ])
        left_layout.addWidget(self.reorder_list)
        
        # Add button to add new items
        add_btn = QPushButton("Add New Item")
        add_btn.clicked.connect(self.add_item_to_reorder_list)
        left_layout.addWidget(add_btn)
        
        lists_layout.addLayout(left_layout)
        
        # Right column - Cross-list drag and drop
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Cross-List Drag and Drop (Copy between lists):"))
        
        # Source list
        right_layout.addWidget(QLabel("Source List:"))
        self.source_list = CrossListDragDropWidget(accept_external=False)
        self.source_list.addItems([
            "Red",
            "Green", 
            "Blue",
            "Yellow",
            "Purple",
            "Orange"
        ])
        right_layout.addWidget(self.source_list)
        
        # Target list
        right_layout.addWidget(QLabel("Target List:"))
        self.target_list = CrossListDragDropWidget(accept_external=True)
        self.target_list.addItems(["Drop colors here!"])
        right_layout.addWidget(self.target_list)
        
        # Clear button
        clear_btn = QPushButton("Clear Target List")
        clear_btn.clicked.connect(self.clear_target_list)
        right_layout.addWidget(clear_btn)
        
        lists_layout.addLayout(right_layout)
        main_layout.addLayout(lists_layout)
        
        # Instructions
        instructions = QLabel("""
Instructions:
• Left List: Drag items up and down to reorder them within the same list
• Right Lists: Drag items from Source to Target (items are copied, not moved)
• You can drag items between any of the lists that accept external drops
        """)
        instructions.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        main_layout.addWidget(instructions)
        
    def add_item_to_reorder_list(self):
        count = self.reorder_list.count()
        self.reorder_list.addItem(f"New Item {count + 1}")
        
    def clear_target_list(self):
        self.target_list.clear()
        self.target_list.addItem("Drop colors here!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


