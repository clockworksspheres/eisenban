import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QHBoxLayout, QWidget, QListWidget, 
                              QListWidgetItem, QLabel, QPushButton,
                              QAbstractItemView)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPainter, QPixmap, QFont


class ReorderableListWidget(QListWidget):
    """Custom list widget with smooth item reordering"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Enable drag and drop for internal reordering
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        
    def dropEvent(self, event):
        # Get the item being dragged
        dragged_item = self.currentItem()
        if not dragged_item:
            return
            
        # Get drop position
        drop_index = self.indexAt(event.position().toPoint())
        
        # If dropping at the end, use count as index
        if not drop_index.isValid():
            target_row = self.count()
        else:
            target_row = drop_index.row()
            
        # Get current row of dragged item
        current_row = self.row(dragged_item)
        
        # Don't do anything if dropping on the same position
        if current_row == target_row:
            return
            
        # Remove item from current position
        item = self.takeItem(current_row)
        
        # Adjust target row if we removed an item before it
        if current_row < target_row:
            target_row -= 1
            
        # Insert at new position
        self.insertItem(target_row, item)
        self.setCurrentItem(item)
        
        event.accept()


class AdvancedReorderListWidget(QListWidget):
    """Advanced reorderable list with visual feedback and constraints"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.drag_start_position = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
            
        if not self.drag_start_position:
            return
            
        # Check if we've moved far enough to start a drag
        if ((event.position().toPoint() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
            
        # Start custom drag
        self.start_custom_drag()
        
    def start_custom_drag(self):
        item = self.currentItem()
        if not item:
            return
            
        # Create MIME data
        mime_data = QMimeData()
        mime_data.setText(item.text())
        mime_data.setData("application/x-item-index", str(self.row(item)).encode())
        
        # Create drag object
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        
        # Create custom drag pixmap with visual feedback
        pixmap = self.create_drag_pixmap(item)
        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())
        
        # Execute drag
        result = drag.exec(Qt.DropAction.MoveAction)
        
    def create_drag_pixmap(self, item):
        """Create a custom pixmap for drag visualization"""
        # Get item rect
        rect = self.visualItemRect(item)
        
        # Create pixmap
        pixmap = QPixmap(rect.size())
        pixmap.fill(Qt.transparent)
        
        # Paint the item onto the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background with transparency
        painter.fillRect(pixmap.rect(), Qt.GlobalColor.lightGray)
        painter.setOpacity(0.8)
        
        # Draw text
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(self.font())
        painter.drawText(pixmap.rect(), Qt.AlignCenter, item.text())
        
        painter.end()
        return pixmap
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-item-index"):
            event.accept()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-item-index"):
            # Provide visual feedback for drop position
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if not event.mimeData().hasFormat("application/x-item-index"):
            event.ignore()
            return
            
        # Get source index
        source_index = int(event.mimeData().data("application/x-item-index").data().decode())
        
        # Get target index
        drop_index = self.indexAt(event.position().toPoint())
        if drop_index.isValid():
            target_index = drop_index.row()
        else:
            target_index = self.count()
            
        # Don't move if same position
        if source_index == target_index:
            event.ignore()
            return
            
        # Move the item
        self.move_item(source_index, target_index)
        event.accept()
        
    def move_item(self, from_index, to_index):
        """Move item from one index to another"""
        # Take item from source
        item = self.takeItem(from_index)
        
        # Adjust target index if necessary
        if from_index < to_index:
            to_index -= 1
            
        # Insert at target
        self.insertItem(to_index, item)
        self.setCurrentItem(item)


class MultiSelectReorderListWidget(QListWidget):
    """List widget that supports multi-item selection and reordering"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Multi-select
        
    def dropEvent(self, event):
        # Get all selected items
        selected_items = self.selectedItems()
        if not selected_items:
            return
            
        # Get drop position
        drop_index = self.indexAt(event.position().toPoint())
        if drop_index.isValid():
            target_row = drop_index.row()
        else:
            target_row = self.count()
            
        # Store item data
        items_data = []
        for item in selected_items:
            items_data.append((self.row(item), item.text()))
            
        # Sort by row index (highest first to avoid index shifting)
        items_data.sort(key=lambda x: x[0], reverse=True)
        
        # Remove items from their current positions
        for row, text in items_data:
            self.takeItem(row)
            
        # Adjust target row based on removed items
        removed_before_target = sum(1 for row, _ in items_data if row < target_row)
        adjusted_target = target_row - removed_before_target
        
        # Insert items at new position
        for i, (_, text) in enumerate(reversed(items_data)):
            new_item = QListWidgetItem(text)
            self.insertItem(adjusted_target + i, new_item)
            new_item.setSelected(True)
            
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 List Widget Item Reordering")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("List Widget Item Reordering Examples")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 15px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Create horizontal layout for different list types
        lists_layout = QHBoxLayout()
        
        # Simple reorderable list
        simple_layout = QVBoxLayout()
        simple_layout.addWidget(QLabel("Simple Reorderable List:"))
        
        self.simple_list = ReorderableListWidget()
        self.simple_list.addItems([
            "🥇 First Place",
            "🥈 Second Place", 
            "🥉 Third Place",
            "🏃 Fourth Place",
            "🚶 Fifth Place"
        ])
        simple_layout.addWidget(self.simple_list)
        
        # Add/Remove buttons
        simple_btn_layout = QHBoxLayout()
        add_simple_btn = QPushButton("Add Item")
        remove_simple_btn = QPushButton("Remove Selected")
        add_simple_btn.clicked.connect(self.add_simple_item)
        remove_simple_btn.clicked.connect(self.remove_simple_item)
        simple_btn_layout.addWidget(add_simple_btn)
        simple_btn_layout.addWidget(remove_simple_btn)
        simple_layout.addLayout(simple_btn_layout)
        
        lists_layout.addLayout(simple_layout)
        
        # Advanced reorderable list
        advanced_layout = QVBoxLayout()
        advanced_layout.addWidget(QLabel("Advanced Reorderable List:"))
        
        self.advanced_list = AdvancedReorderListWidget()
        self.advanced_list.addItems([
            "🎵 Favorite Song #1",
            "🎵 Favorite Song #2",
            "🎵 Favorite Song #3",
            "🎵 Favorite Song #4",
            "🎵 Favorite Song #5"
        ])
        advanced_layout.addWidget(self.advanced_list)
        
        # Shuffle button
        shuffle_btn = QPushButton("Shuffle List")
        shuffle_btn.clicked.connect(self.shuffle_advanced_list)
        advanced_layout.addWidget(shuffle_btn)
        
        lists_layout.addLayout(advanced_layout)
        
        # Multi-select reorderable list
        multi_layout = QVBoxLayout()
        multi_layout.addWidget(QLabel("Multi-Select Reorderable List:"))
        
        self.multi_list = MultiSelectReorderListWidget()
        self.multi_list.addItems([
            "📝 Task 1: Important",
            "📝 Task 2: Medium",
            "📝 Task 3: Low Priority",
            "📝 Task 4: Urgent",
            "📝 Task 5: Can Wait",
            "📝 Task 6: Critical",
            "📝 Task 7: Optional"
        ])
        multi_layout.addWidget(self.multi_list)
        
        # Multi-select buttons
        multi_btn_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        clear_selection_btn = QPushButton("Clear Selection")
        select_all_btn.clicked.connect(self.multi_list.selectAll)
        clear_selection_btn.clicked.connect(self.multi_list.clearSelection)
        multi_btn_layout.addWidget(select_all_btn)
        multi_btn_layout.addWidget(clear_selection_btn)
        multi_layout.addLayout(multi_btn_layout)
        
        lists_layout.addLayout(multi_layout)
        main_layout.addLayout(lists_layout)
        
        # Instructions
        instructions = QLabel("""
<b>Instructions:</b><br>
• <b>Simple List:</b> Drag items up/down to reorder. Basic drag and drop functionality.<br>
• <b>Advanced List:</b> Enhanced drag with custom visual feedback and smooth animations.<br>
• <b>Multi-Select List:</b> Hold Ctrl/Cmd to select multiple items, then drag to move them together.<br><br>
<b>Tips:</b><br>
• All lists support keyboard navigation (↑↓ arrows)<br>
• You can also use mouse wheel to scroll through long lists<br>
• Selected items are highlighted and move as a group in multi-select mode
        """)
        instructions.setStyleSheet("""
            background-color: #f5f5f5; 
            padding: 15px; 
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
            margin-top: 10px;
        """)
        main_layout.addWidget(instructions)
        
    def add_simple_item(self):
        count = self.simple_list.count()
        self.simple_list.addItem(f"🆕 New Item #{count + 1}")
        
    def remove_simple_item(self):
        current_row = self.simple_list.currentRow()
        if current_row >= 0:
            self.simple_list.takeItem(current_row)
            
    def shuffle_advanced_list(self):
        import random
        # Get all items
        items = []
        for i in range(self.advanced_list.count()):
            items.append(self.advanced_list.item(i).text())
            
        # Shuffle and repopulate
        random.shuffle(items)
        self.advanced_list.clear()
        self.advanced_list.addItems(items)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


