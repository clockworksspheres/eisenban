import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QHBoxLayout, QWidget, QListWidget, 
                              QListWidgetItem, QLabel, QPushButton,
                              QAbstractItemView, QFrame, QGroupBox,
                              QScrollArea, QGridLayout)
from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QDrag, QPainter, QPixmap, QFont, QColor, QBrush


class AdvancedDragDropListWidget(QListWidget):
    """Advanced list widget supporting both internal reordering and cross-list drag/drop"""
    
    # Signal emitted when an item is dropped from another list
    item_received = Signal(str, object)  # text, source_widget
    item_removed = Signal(str, object)   # text, target_widget
    
    def __init__(self, list_name="", accept_external=True, parent=None):
        super().__init__(parent)
        self.list_name = list_name
        self.accept_external = accept_external
        self.drag_start_position = None
        self.dragged_item = None
        
        # Configure drag and drop
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        
        # Visual styling
        self.setStyleSheet("""
            QListWidget {
                border: 2px solid #cccccc;
                border-radius: 8px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QListWidget::item:selected {
                background-color: #007acc;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e9ecef;
            }
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()
            self.dragged_item = self.itemAt(event.position().toPoint())
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
            
        self.start_custom_drag()
        
    def start_custom_drag(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return
            
        # Create MIME data with multiple items
        mime_data = QMimeData()
        
        # Store item texts and source info
        item_texts = [item.text() for item in selected_items]
        item_data = {
            'texts': item_texts,
            'source_list': self.list_name,
            'source_widget_id': id(self)
        }
        
        mime_data.setText('\n'.join(item_texts))
        mime_data.setData("application/x-listwidget-items", str(item_data).encode())
        
        # Create drag object
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        
        # Create custom drag pixmap
        pixmap = self.create_multi_item_drag_pixmap(selected_items)
        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())
        
        # Execute drag
        result = drag.exec(Qt.DropAction.MoveAction | Qt.DropAction.CopyAction)
        
        # Handle the result
        if result == Qt.DropAction.MoveAction:
            # Items were moved, remove them from source
            for item in selected_items:
                row = self.row(item)
                if row >= 0:
                    self.takeItem(row)
                    
    def create_multi_item_drag_pixmap(self, items):
        """Create a pixmap showing multiple dragged items"""
        if len(items) == 1:
            return self.create_single_item_pixmap(items[0])
        else:
            return self.create_multiple_items_pixmap(items)
            
    def create_single_item_pixmap(self, item):
        """Create pixmap for single item drag"""
        # Get item rect
        rect = self.visualItemRect(item)
        
        # Create pixmap
        pixmap = QPixmap(rect.width() + 20, rect.height() + 10)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background with gradient
        gradient_rect = pixmap.rect().adjusted(5, 5, -5, -5)
        painter.fillRect(gradient_rect, QColor(70, 130, 180, 200))
        painter.setPen(QColor(50, 110, 160))
        painter.drawRoundedRect(gradient_rect, 5, 5)
        
        # Draw text
        painter.setPen(Qt.white)
        painter.setFont(self.font())
        painter.drawText(gradient_rect, Qt.AlignCenter, item.text())
        
        painter.end()
        return pixmap
        
    def create_multiple_items_pixmap(self, items):
        """Create pixmap for multiple items drag"""
        pixmap = QPixmap(200, 60)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw stacked rectangles to show multiple items
        for i in range(min(3, len(items))):
            offset = i * 3
            rect = pixmap.rect().adjusted(offset, offset, -20+offset, -20+offset)
            
            alpha = 220 - (i * 30)
            painter.fillRect(rect, QColor(70, 130, 180, alpha))
            painter.setPen(QColor(50, 110, 160))
            painter.drawRoundedRect(rect, 5, 5)
            
        # Draw count text
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        text = f"{len(items)} items"
        painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
        
        painter.end()
        return pixmap
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-listwidget-items"):
            # Check if we accept external drops
            if self.accept_external:
                self.setStyleSheet(self.styleSheet() + """
                    QListWidget {
                        border: 2px dashed #007acc;
                        background-color: #f0f8ff;
                    }
                """)
                event.accept()
            else:
                # Only accept from self
                data = eval(event.mimeData().data("application/x-listwidget-items").data().decode())
                if data.get('source_widget_id') == id(self):
                    event.accept()
                else:
                    event.ignore()
        else:
            event.ignore()
            
    def dragLeaveEvent(self, event):
        # Reset styling
        self.setStyleSheet("""
            QListWidget {
                border: 2px solid #cccccc;
                border-radius: 8px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QListWidget::item:selected {
                background-color: #007acc;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e9ecef;
            }
        """)
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-listwidget-items"):
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        # Reset styling first
        self.dragLeaveEvent(event)
        
        if not event.mimeData().hasFormat("application/x-listwidget-items"):
            event.ignore()
            return
            
        # Parse the dropped data
        try:
            data = eval(event.mimeData().data("application/x-listwidget-items").data().decode())
            item_texts = data['texts']
            source_widget_id = data['source_widget_id']
            is_external_drop = source_widget_id != id(self)
        except:
            event.ignore()
            return
            
        # Get drop position
        drop_index = self.indexAt(event.position().toPoint())
        if drop_index.isValid():
            target_row = drop_index.row()
        else:
            target_row = self.count()
            
        # Handle internal vs external drops
        if is_external_drop:
            # External drop - add items (copy or move based on modifier keys)
            if event.keyboardModifiers() & Qt.ControlModifier:
                # Copy operation
                event.setDropAction(Qt.DropAction.CopyAction)
                action_text = "copied"
            else:
                # Move operation
                event.setDropAction(Qt.DropAction.MoveAction)
                action_text = "moved"
                
            # Add items at drop position
            for i, text in enumerate(item_texts):
                # Avoid duplicates in the same list
                existing_texts = [self.item(j).text() for j in range(self.count())]
                if text not in existing_texts:
                    new_item = QListWidgetItem(text)
                    self.insertItem(target_row + i, new_item)
                    
            # Emit signal
            for text in item_texts:
                self.item_received.emit(text, self)
                
        else:
            # Internal drop - reorder items
            if not item_texts:
                event.ignore()
                return
                
            # Find current positions of dragged items
            item_positions = []
            for text in item_texts:
                for i in range(self.count()):
                    if self.item(i).text() == text:
                        item_positions.append((i, text))
                        break
                        
            # Sort by position (highest first)
            item_positions.sort(key=lambda x: x[0], reverse=True)
            
            # Remove items
            for pos, text in item_positions:
                self.takeItem(pos)
                
            # Adjust target row
            removed_before_target = sum(1 for pos, _ in item_positions if pos < target_row)
            adjusted_target = target_row - removed_before_target
            
            # Insert items at new position
            for i, (_, text) in enumerate(reversed(item_positions)):
                new_item = QListWidgetItem(text)
                self.insertItem(adjusted_target + i, new_item)
                new_item.setSelected(True)
                
        event.accept()


class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Multi-List Drag & Drop Task Manager")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Advanced Task Manager - Drag & Drop Between Lists")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            margin: 15px;
            color: #2c3e50;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Create scroll area for the lists
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)
        
        # Create multiple lists with different purposes
        self.lists = {}
        list_configs = [
            ("backlog", "📋 Backlog", ["🎯 Plan quarterly goals", "📊 Analyze user feedback", "🔍 Research competitors"]),
            ("todo", "📝 To Do", ["✉️ Reply to emails", "📞 Call client about project", "📝 Write project proposal"]),
            ("in_progress", "⚡ In Progress", ["💻 Develop new feature", "🐛 Fix critical bug"]),
            ("review", "👀 In Review", ["📋 Code review for John", "✅ Test new deployment"]),
            ("done", "✅ Done", ["🎉 Launch marketing campaign", "📈 Monthly report completed"])
        ]
        
        for list_id, title, initial_items in list_configs:
            list_widget = self.create_task_list(title, initial_items, list_id)
            self.lists[list_id] = list_widget
            scroll_layout.addWidget(list_widget)
            
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        main_layout.addWidget(scroll_area)
        
        # Control panel
        self.create_control_panel(main_layout)
        
        # Instructions
        self.create_instructions(main_layout)
        
    def create_task_list(self, title, initial_items, list_id):
        """Create a task list widget with header and controls"""
        group_box = QGroupBox()
        group_box.setFixedWidth(280)
        layout = QVBoxLayout(group_box)
        
        # Header
        header = QLabel(title)
        header.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #34495e;
            padding: 8px;
            background-color: #ecf0f1;
            border-radius: 4px;
            margin-bottom: 5px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # List widget
        list_widget = AdvancedDragDropListWidget(list_id, accept_external=True)
        list_widget.addItems(initial_items)
        list_widget.setMinimumHeight(300)
        
        # Connect signals
        list_widget.item_received.connect(self.on_item_received)
        list_widget.item_removed.connect(self.on_item_removed)
        
        layout.addWidget(list_widget)
        
        # Add item button
        add_btn = QPushButton(f"+ Add to {title}")
        add_btn.clicked.connect(lambda: self.add_item_to_list(list_widget, title))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(add_btn)
        
        # Clear button
        clear_btn = QPushButton("Clear List")
        clear_btn.clicked.connect(lambda: self.clear_list(list_widget))
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(clear_btn)
        
        return group_box
        
    def create_control_panel(self, main_layout):
        """Create control panel with global actions"""
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                margin: 10px 0;
            }
        """)
        control_layout = QHBoxLayout(control_frame)
        
        # Global actions
        actions = [
            ("🔄 Shuffle All Lists", self.shuffle_all_lists),
            ("📊 Show Statistics", self.show_statistics),
            ("🗑️ Clear All Lists", self.clear_all_lists),
            ("🎯 Add Sample Tasks", self.add_sample_tasks)
        ]
        
        for text, callback in actions:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 0 5px;
                }
                QPushButton:hover {
                    background-color: #545b62;
                }
            """)
            control_layout.addWidget(btn)
            
        main_layout.addWidget(control_frame)
        
    def create_instructions(self, main_layout):
        """Create instructions panel"""
        instructions = QLabel("""
<b>🎯 Task Manager Instructions:</b><br><br>
<b>Drag & Drop Operations:</b><br>
• <b>Internal Reordering:</b> Drag items within the same list to reorder them<br>
• <b>Cross-List Movement:</b> Drag items between different lists to move them<br>
• <b>Copy Mode:</b> Hold <b>Ctrl</b> while dropping to copy items instead of moving<br>
• <b>Multi-Selection:</b> Hold <b>Ctrl/Cmd</b> and click to select multiple items, then drag them together<br><br>
<b>Visual Cues:</b><br>
• Lists highlight with blue dashed border when you can drop items<br>
• Drag preview shows single item or item count for multiple selections<br>
• Items maintain their order when moved as a group<br><br>
<b>Workflow:</b> Move tasks from Backlog → To Do → In Progress → Review → Done
        """)
        instructions.setStyleSheet("""
            background-color: #e8f4fd; 
            padding: 15px; 
            border-radius: 8px;
            border-left: 4px solid #2196F3;
            margin-top: 10px;
            line-height: 1.4;
        """)
        main_layout.addWidget(instructions)
        
    def add_item_to_list(self, group_box, title):
        """Add a new item to the specified list"""
        # Find the list widget within the group box
        list_widget = None
        for child in group_box.findChildren(AdvancedDragDropListWidget):
            list_widget = child
            break
            
        if list_widget:
            count = list_widget.count()
            new_item = f"🆕 New task {count + 1}"
            list_widget.addItem(new_item)
            
    def clear_list(self, group_box):
        """Clear the specified list"""
        # Find the list widget within the group box
        list_widget = None
        for child in group_box.findChildren(AdvancedDragDropListWidget):
            list_widget = child
            break
            
        if list_widget:
            list_widget.clear()
            
    def shuffle_all_lists(self):
        """Shuffle all lists"""
        import random
        for group_box in self.lists.values():
            list_widget = None
            for child in group_box.findChildren(AdvancedDragDropListWidget):
                list_widget = child
                break
                
            if list_widget and list_widget.count() > 1:
                items = [list_widget.item(i).text() for i in range(list_widget.count())]
                random.shuffle(items)
                list_widget.clear()
                list_widget.addItems(items)
                
    def show_statistics(self):
        """Show statistics about all lists"""
        stats = []
        total_items = 0
        
        for list_id, group_box in self.lists.items():
            list_widget = None
            for child in group_box.findChildren(AdvancedDragDropListWidget):
                list_widget = child
                break
                
            if list_widget:
                count = list_widget.count()
                total_items += count
                stats.append(f"{list_id.replace('_', ' ').title()}: {count} items")
                
        stats_text = "\n".join(stats) + f"\n\nTotal items: {total_items}"
        
        # Create a simple dialog-like display (using a label for simplicity)
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("Task Statistics")
        msg.setText(stats_text)
        msg.exec()
        
    def clear_all_lists(self):
        """Clear all lists"""
        for group_box in self.lists.values():
            self.clear_list(group_box)
            
    def add_sample_tasks(self):
        """Add sample tasks to lists"""
        sample_tasks = {
            "backlog": ["🎨 Design new UI", "📱 Mobile app research", "🔒 Security audit"],
            "todo": ["☕ Team standup", "📧 Client follow-up", "📝 Documentation update"],
            "in_progress": ["⚙️ Database optimization"],
            "review": ["🧪 Unit test coverage"],
            "done": ["🚀 Server deployment"]
        }
        
        for list_id, tasks in sample_tasks.items():
            if list_id in self.lists:
                group_box = self.lists[list_id]
                list_widget = None
                for child in group_box.findChildren(AdvancedDragDropListWidget):
                    list_widget = child
                    break
                    
                if list_widget:
                    for task in tasks:
                        list_widget.addItem(task)
                        
    def on_item_received(self, text, target_widget):
        """Handle item received signal"""
        print(f"Item '{text}' was dropped into list")
        
    def on_item_removed(self, text, source_widget):
        """Handle item removed signal"""
        print(f"Item '{text}' was removed from list")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = TaskManagerWindow()
    window.show()
    
    sys.exit(app.exec())


