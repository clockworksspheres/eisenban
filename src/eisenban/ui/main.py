import datetime
import logging
import sys

from PySide6.QtCore import QCoreApplication, QEvent, QSize, Qt, Slot
from PySide6.QtGui import QCursor, QDragMoveEvent, QDropEvent, QFont
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea,
                               QApplication, QFrame, QLabel, QListWidget,
                               QListWidgetItem, QMainWindow, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)


from db import Table
from dialog import dialog_factory, input_dialog_factory
from eisenban_objects import Board, Card, Panel
from ui.about import About
from ui.app_settings import AppSettings
from ui.board_settings import BoardSettings
from ui.card_description import CardDescription
from ui.main_ui import Ui_MainWindow
from utils import (hex_to_rgba, keyPressEvent, modify_hex_color, overrides,
                   setup_font_db)


class CustomListWidget(QListWidget):
    """Custom QListWidget class"""

    def __init__(self: QListWidget, parent: QMainWindow, board: Board,
                 color: str) -> None:
        super().__init__()
        self.parent_ = parent
        self.board = board



        # Enable drag and drop
        # self.ui.listWidget = QListWidget()

        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setAcceptDrops(True)
        # Enable multiple selection
        self.setSelectionMode(QListWidget.ExtendedSelection)




        self.setObjectName(u"listWidget")
        size_policy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        size_policy2.setHorizontalStretch(0)
        size_policy2.setVerticalStretch(0)
        size_policy2.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy2)
        self.setMaximumSize(QSize(260, 16777215))
        self.setFocusPolicy(Qt.TabFocus)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.setAutoScroll(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setProperty("isWrapping", False)
        self.setSpacing(5)
        self.setUniformItemSizes(True)
        self.setWordWrap(True)
        self.verticalScrollBar().setSingleStep(10)
        self.setSelectionRectVisible(True)
        self.setStyleSheet(
            f"""
            QListWidget {{
                background-color: #ebecf0;
                border-radius: 10px;
                color: #000000;
            }}
            QListWidget::item {{
                height: 40px;
                padding: 0 8px 0 8px;
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0.5, x2:0.95, y2:0.5,
                    stop:0 {color},
                    stop:0.0338983 {color},
                    stop:0.039548 rgba(255, 255, 255, 255),
                    stop:1 rgba(255, 255, 255, 255)
                );
                color: #000000;
                border-radius: 5px;
            }}
            QListWidget::item:hover {{
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0.5, x2:0.95, y2:0.5,
                    stop:0 {color},
                    stop:0.0338983 {color},
                    stop:0.039548 rgba(226, 228, 233, 255),
                    stop:1 rgba(226, 228, 233, 255)
                );
                color: #000000;
            }}
            QListWidget::item:selected {{
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0.5, x2:0.95, y2:0.5,
                    stop:0 {color},
                    stop:0.0338983 {color},
                    stop:0.039548 rgba(204, 204, 204, 255),
                    stop:1 rgba(204, 204, 204, 255)
                );
                color: #000000;
            }}
            QListWidget::item:focus {{
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0.5, x2:0.95, y2:0.5,
                    stop:0 {color},
                    stop:0.0338983 {color},
                    stop:0.039548 rgba(204, 204, 204, 255),
                    stop:1 rgba(204, 204, 204, 255));
                    color: #000000
            }}
            QScrollBar:vertical {{
                border: none;
                background: #ebecf0;
                width: 10px;
                margin: 1px 0 0 0;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #bfc0c5;
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #afb0b4;
            }}
            QScrollBar::handle:vertical:pressed {{
                background-color: #929497;
            }}
            QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar::add-line:vertical {{
                height: 0;
            }}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            QScrollBar QMenu {{
                background-color: #454c5a;
                border: none;
                padding: 5px;
                margin: 0px;
                font-size: 13px;
            }}
            QScrollBar QMenu::item {{
                padding: 5px 13px 5px 13px;
                color: #ffffff;
            }}
            QScrollBar QMenu::item:selected {{
                border-radius: 5px;
                background-color: {color};
                color: #000000;
            }}
            """
        )

    @Slot()
    @overrides(QListWidget)
    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        """Override the dragMoveEvent method to customize the drag and drop
        event
        - Scroll the main window when the cursor is near the left or right of
        the main window
        - Accept the drag and drop event if the cursor is over a list widget

        Parameters
        ----------
        event : QDragMoveEvent
            The drag and drop event
        """
        cursor_pos = self.parent_.mapFromGlobal(QCursor.pos())
        if cursor_pos.x() > self.parent_.width() + self.parent_.x() - 100:
            self.parent_.horizontalScrollBar().setValue(
                self.parent_.horizontalScrollBar().value() + 8)
        elif cursor_pos.x() < self.parent_.x() + 100:
            self.parent_.horizontalScrollBar().setValue(
                self.parent_.horizontalScrollBar().value() - 8)

        super().dragMoveEvent(event)

    @Slot()
    @overrides(QListWidget)
    def dropEvent(self, event: QDropEvent) -> None:
        """Override the dropEvent method to customize the drop event
        - Check if the item to be dropped has the qabstractitemmodeldatalist
        format
        - Get the source widget and the destination widget at the current mouse
        position
        - Get the items that are being dragged
        - Remove those items from the source widget
        - Add those items to the destination widget at the mouse position
        - Log the move and update the table

        Parameters
        ----------
        event : QDropEvent
            The drop even
        """

        if event.keyboardModifiers() == Qt.ControlModifier:
            return event.ignore()
        if not event.mimeData().hasFormat(
                'application/x-qabstractitemmodeldatalist'):
            return event.ignore()
        source_widget = event.source()
        dest_widget = QApplication.widgetAt(QCursor().pos()).parent()
        items = source_widget.selectedItems()

        logging.info(
            f'Moving {len(items)} Card{"s" if len(items) > 1 else ""} '
            f'({[item.data(Qt.UserRole).title for item in items]}) '
            f'from panel "{source_widget.data.title}" to panel '
            f'"{dest_widget.data.title}"')

        for i, item in enumerate(items):


            index = dest_widget.row(dest_widget.itemAt(event.pos()))
            if index < 0:
                index = dest_widget.count()

            index += i
            if source_widget == dest_widget:
                if len(items) > 1:
                    index -= 1
                dest_widget.insertItem(index, item)

            logging.info(
                f'Moved card "{item.data(Qt.UserRole).title}" to {index=}')
            
            MainScreen.change_card(self.parent, self.board, source_widget, dest_widget,
                                   item.data(Qt.UserRole), index)
            source_widget.takeItem(source_widget.row(item))
            data = Table.get_instance().data
            # Table.get_instance().data = data
            Table.get_instance().write()
        event.accept()

        super().dropEvent(event)


class MainScreen(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.table = Table.get_instance()

        self.current_board: Board = Table.get_instance().boards[0]

        self.ui.btn_app_settings.clicked.connect(
            lambda: self.show_app_settings())
        self.ui.btn_board_settings.clicked.connect(
            lambda: self.show_board_settings())
        self.ui.btn_add_board.clicked.connect(
            lambda: self.add_board())

        self.ui.btn_app_settings.keyPressEvent = lambda event: keyPressEvent(
            event, self, self.show_app_settings())
        self.ui.btn_board_settings.keyPressEvent = lambda event: \
            keyPressEvent(
                event, self, self.show_board_settings())
        self.ui.btn_add_board.keyPressEvent = lambda event: keyPressEvent(
            event, self, self.add_board())

        self.update_whole_page()

    def update_whole_page(self) -> None:
        tb_boards = Table.get_instance().boards
        push_buttons = []

        def on_button_click(board):
            def callback():
                updated_board = self.get_updated_board(board)
                self.change_board(updated_board)
            return callback

        for index, board in enumerate(tb_boards):
            print(f'     index: {index}, board: {str(board)}')
            updated_board = self.get_updated_board(board)
            new_button = self.board_factory(updated_board, 'Arimo-Medium.ttf', is_constructed=index == 0)
            new_button.board = board
            new_name = f"{new_button.__class__.__name__}_{id(new_button)}"
            setattr(self.ui, new_name, new_button)
            push_buttons.append(getattr(self.ui, new_name))
            push_buttons[index].setObjectName(new_name)
            self.ui.verticalLayout_4.addWidget(push_buttons[index])
            push_buttons[index].clicked.connect(
                on_button_click(board))

        self.ui.vertSpacer_scrollAreaContent = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.verticalLayout_4.addItem(
            self.ui.vertSpacer_scrollAreaContent)

        self.add_panel_button(
            Table.get_instance().boards[0], 'Arimo-Medium.ttf')

        self.ui.label_board.setText(
            f"{Table.get_instance().boards[0].title[:40]}"
            f"{(Table.get_instance().boards[0].title[40:] and '...')}")

        self.setup_font('Arimo-Medium.ttf')

        self.ui.label_logo.mousePressEvent = lambda event: self.show_about(
            event)

    def show_about(self, event: QEvent) -> None:
        """Shows the about dialog"""
        self.about = About(self.current_board.color)
        self.about.show()

    def board_factory(self, board: Board, font: str,
                      is_constructed: bool = True) -> QPushButton:
        """Creates a board button widget
        - Add a push button widget to the parent UI with specified style
        - If the board is displayed, construct the list widgets and card
        widgets

        Parameters
        ----------
        parent : QMainWindow
            The parent window
        board : Board
            The board object
        font : str
            The font to use
        is_constructed : bool, optional
            Load the board if True, by default True
        Returns
        -------
        QPushButton
            The board widget
        """
        if board is None:
            self.current_board = Table.get_instance().boards[-1]
            board = self.current_board

        self.ui.label_board.setText(
            board.title[:40] + (board.title[40:] and '...'))

        self.ui.btn_board = QPushButton(
            self.ui.scrollAreaContent_panel_left)
        self.ui.btn_board.setObjectName(u"btn_board")
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.ui.btn_board.sizePolicy().hasHeightForWidth())
        self.ui.btn_board.setSizePolicy(size_policy)
        self.ui.btn_board.setMinimumSize(QSize(128, 40))
        self.ui.btn_board.setMaximumSize(QSize(142, 40))
        self.ui.btn_board.setCursor(QCursor(Qt.PointingHandCursor))
        self.ui.btn_board.setFocusPolicy(Qt.TabFocus)
        self.ui.btn_board.setStyleSheet(
            """
            QPushButton {
                background-color: """ + f"{board.color}" + """;
                color: #ffffff;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color:
                 """ + f"{modify_hex_color(board.color, -30)}" + """;
            }
            QPushButton:focus {
                border-color: #000000;
                border-width: 1.5px;
                border-style: solid;
            }
            """
        )
        self.ui.btn_board.setText(
            board.title[:12] + (board.title[12:] and '...'))
        font_tb = setup_font_db(font)[0]
        self.ui.btn_board.setFont(QFont(font_tb, 12))

        if is_constructed:
            self.ui.scrollArea_panel_right.setStyleSheet(
                f"""
            QScrollBar:vertical {{
                width: 10px;
                margin: 0 0 0 0;
                background-color: #acb2bf
            }}
            QScrollBar:horizontal {{
                border: none;
                background: #454c5a;
                height: 10px;
                margin: 0 0 0 1px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: #76829b;
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: #646e83;
            }}
            QScrollBar::handle:horizontal:pressed {{
                background-color: #576072;
            }}
            QScrollBar::sub-line:horizontal {{
                height: 0;
            }}
            QScrollBar::add-line:horizontal {{
                height: 0;
            }}

            QScrollBar::up-arrow:horizontal,
            QScrollBar::down-arrow:horizontal {{
                background: none;
            }}
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {{
                background: none;
            }}
            QScrollBar QMenu {{
                background-color: #454c5a;
                border: none;
                padding: 5px;
                margin: 0px;
                font-size: 13px;
            }}
            QScrollBar QMenu::item {{
                padding: 5px 13px 5px 13px;
            }}
            QScrollBar QMenu::item:selected {{
                border-radius: 5px;
                background-color: {modify_hex_color(self.current_board.color)};
                color: #000000;
            }}
            """
            )
            color = hex_to_rgba(board.color)
            self.ui.label_board.setStyleSheet(
                f"""
                background-color: qlineargradient(
                    spread:pad,
                    x1:0.5, y1:0.5,
                    x2:0.95, y2:0.5,
                    stop:0 {color},
                    stop:1 rgba(69, 76, 90, 255)
                );
                color: #FFFFFF;
                """
            )
            self.ui.scrollArea_panel_left.setStyleSheet(
                f"""
                QScrollBar:vertical {{
                    border: none;
                    background: #282c34;
                    width: 10px;
                    margin: 1px 0 0 5px;
                    border-radius: 2px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: #454c5a;
                    min-height: 30px;
                    border-radius: 2px;
                }}
                QScrollBar::handle:vertical:hover {{
                    background-color: #343a44;
                }}
                QScrollBar::handle:vertical:pressed {{
                    background-color: #323741;
                }}
                QScrollBar::sub-line:vertical {{
                    height: 0;
                }}
                QScrollBar::add-line:vertical {{
                    height: 0;
                }}
                QScrollBar::up-arrow:vertical,
                QScrollBar::down-arrow:vertical {{
                    background: none;
                }}
                QScrollBar::add-page:vertical,
                QScrollBar::sub-page:vertical {{
                    background: none;
                }}
                QScrollBar QMenu {{
                    background-color: #454c5a;
                    border: none;
                    padding: 5px;
                    margin: 0px;
                    font-size: 13px;
                }}
                QScrollBar QMenu::item {{
                    padding: 5px 13px 5px 13px;
                }}
                QScrollBar QMenu::item:selected {{
                    border-radius: 5px;
                    background-color: {modify_hex_color(
                        self.current_board.color)};
                    color: #000000;
                }}
                """
            )
            for panel in board.panels:
                qwidget = self.panel_factory(panel, font, board.color)
                self.ui.horizontalLayout_5.addWidget(qwidget)
        return self.ui.btn_board

    def panel_factory(self, panel: Panel, font: str,
                      color: str) -> QWidget:
        """Creates a panel widget
        - Add a panel widget to the parent UI with specified style
        - Create a new name for the panel with its class name and id
        - Set the new name as an attribute of the parent UI and as the
          object name of the panel
        - Delete the old name attribute from the parent UI
        - Set the panel data attribute as the Panel class object

        Parameters
        ----------
        color
        parent : QMainWindow
            The parent window
        panel : Panel
            The panel object
        font : str
            The font to use

        Returns
        -------
        QWidget
            The panel widget
        """
        size_policy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy1.setHorizontalStretch(0)
        size_policy1.setVerticalStretch(0)

        self.ui.panel = QWidget(self.ui.scrollAreaContent_panel_right)
        self.ui.panel.setObjectName(u"panel")

        size_policy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        size_policy2.setHorizontalStretch(0)
        size_policy2.setVerticalStretch(0)
        size_policy2.setHeightForWidth(
            self.ui.panel.sizePolicy().hasHeightForWidth())
        self.ui.panel.setSizePolicy(size_policy2)
        self.ui.panel.setMinimumSize(QSize(260, 0))
        self.ui.verticalLayout_1 = QVBoxLayout(self.ui.panel)
        self.ui.verticalLayout_1.setSpacing(0)
        self.ui.verticalLayout_1.setObjectName(u"verticalLayout_1")
        self.ui.verticalLayout_1.setContentsMargins(0, 0, 0, 0)

        self.ui.widget = QWidget(self.ui.panel)
        self.ui.widget.setObjectName(u"widget_list_1")

        size_policy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy3.setHorizontalStretch(0)
        size_policy3.setVerticalStretch(0)
        size_policy3.setHeightForWidth(
            self.ui.widget.sizePolicy().hasHeightForWidth())
        self.ui.widget.setSizePolicy(size_policy3)
        self.ui.widget.setStyleSheet(
            """
            background-color: #ebecf0;
            border-radius: 10px;
            """
        )
        self.ui.verticalLayout_2 = QVBoxLayout(self.ui.widget)
        self.ui.verticalLayout_2.setObjectName(u"verticalLayout_11")
        self.ui.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.ui.label_list = QLabel(self.ui.widget)
        self.ui.label_list.setObjectName(u"label_list")
        size_policy1.setHeightForWidth(
            self.ui.label_list.sizePolicy().hasHeightForWidth())
        self.ui.label_list.setSizePolicy(size_policy1)
        self.ui.label_list.setMinimumSize(QSize(0, 30))
        self.ui.label_list.setStyleSheet(
            """
            color: #282c33;
            background-color: #ebecf0;
            border-radius: 5px;
            padding: 5px 0 0 5px;
            """
        )
        self.ui.label_list.setMargin(0)
        self.ui.verticalLayout_2.addWidget(self.ui.label_list)

        self.ui.listWidget = CustomListWidget(
            self.ui.scrollArea_panel_right, self.current_board,
            modify_hex_color(color))
        self.ui.verticalLayout_2.addWidget(self.ui.listWidget)

        self.ui.widget_add_card = QWidget(self.ui.widget)
        self.ui.widget_add_card.setObjectName(u"widget_add_card")
        size_policy1.setHeightForWidth(
            self.ui.widget_add_card.sizePolicy().hasHeightForWidth())
        self.ui.widget_add_card.setSizePolicy(size_policy1)

        self.ui.verticalLayout_3 = QVBoxLayout(self.ui.widget_add_card)
        self.ui.verticalLayout_3.setObjectName(u"verticalLayout_6")
        self.ui.verticalLayout_3.setContentsMargins(6, 0, 6, 6)

        self.ui.btn_add_card = QPushButton(self.ui.widget_add_card)
        self.ui.btn_add_card.setObjectName(u"btn_add_card_list_1")
        self.ui.btn_add_card.setMinimumSize(QSize(0, 25))
        self.ui.btn_add_card.setCursor(QCursor(Qt.PointingHandCursor))
        self.ui.btn_add_card.setFocusPolicy(Qt.TabFocus)
        self.ui.btn_add_card.setStyleSheet(
            """
            QPushButton {
                background-color: #ebecf0;
                color: #6a758b;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #dadbe2;
                color: #505b76;
            }
            QPushButton:focus {
                border-color: #000000;
                border-width: 1.5px;
                border-style: solid;
            }
            """
        )
        self.ui.verticalLayout_3.addWidget(self.ui.btn_add_card)
        self.ui.verticalLayout_2.addWidget(self.ui.widget_add_card)
        self.ui.verticalLayout_1.addWidget(self.ui.widget)
        self.ui.listWidget.setSortingEnabled(False)

        font_tb = setup_font_db(font)
        self.ui.label_list.setFont(QFont(font_tb[0], 12, QFont.Bold))
        self.ui.btn_add_card.setFont(QFont(font_tb[0], 12))

        self.ui.btn_add_card.clicked.connect(
            lambda: self.add_card(panel))

        new_name = f"{self.ui.listWidget.__class__.__name__}_"
        f"{id(self.ui.listWidget)}"
        setattr(self.ui, new_name, self.ui.listWidget)
        listWidget = getattr(self.ui, new_name)
        listWidget.setObjectName(new_name)
        delattr(self.ui, "listWidget")
        setattr(listWidget, "data", panel)

        for index, card in enumerate(panel.cards):
            qlistwidgetitem = self.card_factory(
                listWidget, card, font, index)
            listWidget.addItem(qlistwidgetitem)

        listWidget.clicked.connect(
            lambda event: self.show_card_description(
                event,
                listWidget,
                color
            )
        )

        self.ui.label_list.setText(
            QCoreApplication.translate(
                "MainWindow",
                panel.title[:25] + (panel.title[25:] and '...'), None
            )
        )
        self.ui.btn_add_card.setText(
            QCoreApplication.translate(
                "MainWindow", u"+ Add a card", None
            )
        )

        return self.ui.panel

    def card_factory(self, qlistwidget: QListWidget, card: Card, font: str, index: int) -> QListWidgetItem:
        """Create a card item at the given QListWidget index
        - Create a new name for the card with its class name and id
        - Set the new name as an attribute of the parent UI and as the
          object name of the card
        - Delete the old name attribute from the parent UI
        - Set the card flags
        - Set the card data as the Card class object

        Parameters
        ----------
        qlistwidget : QListWidget
            The QListWidget to add the card item to
        parent : Ui_MainWindow
            The parent UI
        card : Card
            The card to add to the panel
        font : str
            The font to use
        index : int
            The index to add the card item to

        Returns
        -------
        QListWidgetItem
            The card item
        """
        self.ui.qlistwidgetitem = QListWidgetItem(qlistwidget)
        new_name = f"{self.ui.qlistwidgetitem.__class__.__name__}_"
        f"{id(self.ui.qlistwidgetitem)}"
        setattr(self.ui, new_name, self.ui.qlistwidgetitem)
        list_widget_item = getattr(self.ui, new_name)
        delattr(self.ui, "qlistwidgetitem")
        list_widget_item.setFlags(
            Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable
            | Qt.ItemIsEnabled)
        list_widget_item = qlistwidget.item(index)
        list_widget_item.setData(Qt.UserRole, card)
        list_widget_item.setText(
            QCoreApplication.translate("MainWindow", card.title, None)
        )
        font_tb = setup_font_db(font)[0]
        list_widget_item.setFont(QFont(font_tb, 12))

        return list_widget_item

    def add_panel_button(self, board: Board, font: str) -> None:
        """Add a button to add a new panel

        Parameters
        ----------
        parent : Ui_MainWindow
            The main window
        board : Board
            The board to add the panel to
        font : str
            The font to use
        """
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        self.ui.list_add = QWidget(self.ui.scrollAreaContent_panel_right)
        self.ui.list_add.setObjectName(u"list_add")
        size_policy.setHeightForWidth(
            self.ui.list_add.sizePolicy().hasHeightForWidth())
        self.ui.list_add.setSizePolicy(size_policy)
        self.ui.list_add.setMinimumSize(QSize(250, 0))
        self.ui.verticalLayout_9 = QVBoxLayout(self.ui.list_add)
        self.ui.verticalLayout_9.setSpacing(0)
        self.ui.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.ui.verticalLayout_9.setContentsMargins(0, 0, 6, 0)
        self.ui.btn_add_list = QPushButton(self.ui.list_add)
        self.ui.btn_add_list.setObjectName(u"btn_add_list")
        self.ui.btn_add_list.setMinimumSize(QSize(0, 30))
        self.ui.btn_add_list.setCursor(QCursor(Qt.PointingHandCursor))
        self.ui.btn_add_list.setFocusPolicy(Qt.TabFocus)
        self.ui.btn_add_list.setStyleSheet(
            """
            QPushButton {
                background-color: #acb2bf;
                color: #ffffff;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7e828c;
            }
            QPushButton:focus {
                border-color: #000000;
                border-width: 1.5px;
                border-style: solid;
            }
            """
        )
        self.ui.verticalLayout_9.addWidget(self.ui.btn_add_list)
        self.ui.vertSpacer_list_add = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.verticalLayout_9.addItem(self.ui.vertSpacer_list_add)
        self.ui.btn_add_list.setText(
            QCoreApplication.translate("MainWindow", u"+ Add a panel", None))
        self.ui.scrollAreaContent_panel_right.layout().addWidget(
            self.ui.list_add)
        self.ui.horzSpacer_panel_right = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ui.horizontalLayout_5.addItem(self.ui.horzSpacer_panel_right)
        self.ui.btn_add_list.clicked.connect(
            lambda: self.add_panel(board))

        font_tb = setup_font_db(font)[0]
        self.ui.btn_add_list.setFont(QFont(font_tb, 12))

    def show_app_settings(self) -> None:
        """Show the application settings window

        Parameters
        ----------
        parent : Ui_MainWindow
            The main window
        """
        self.app_settings = AppSettings(self.current_board)
        self.app_settings.setWindowModality(Qt.ApplicationModal)
        self.app_settings.show()
        self.app_settings.raise_()
        while self.app_settings.isVisible():
            QCoreApplication.processEvents()
        try:
            self.clear_page()
            self.update_whole_page()
            if self.current_board not in Table.get_instance().boards:
                self.current_board = Table.get_instance().boards[-1]
            self.change_board(self.current_board)
        except AttributeError:
            return None

    def show_board_settings(self) -> None:
        """Show the board settings window

        Parameters
        ----------
        parent : Ui_MainWindow
            The main window
        """
        self.board_settings = BoardSettings(self.current_board)
        index = Table.get_instance().boards.index(self.current_board)
        self.board_settings.setWindowModality(Qt.ApplicationModal)
        self.board_settings.show()
        while self.board_settings.isVisible():
            QCoreApplication.processEvents()
        self.clear_page()
        self.update_whole_page()
        self.change_board(Table.get_instance().boards[index])

    def show_card_description(self, event: QEvent, list_widget: QListWidget, color: str) -> None:
        """Show the card description window

        Parameters
        ----------
        list_widget
        color
        event : QMouseEvent
            The mouse event
        parent : QListWidget
            The parent QListWidget
        """
        card = list_widget.item(event.row()).data(Qt.UserRole)
        card_description = CardDescription(card, color)
        card_description.setWindowModality(Qt.ApplicationModal)
        card_description.show()
        while card_description.isVisible():
            QCoreApplication.processEvents()
        self.clear_page()
        self.update_whole_page()
        self.change_board(self.get_updated_board(self.current_board))

    def get_updated_board(self, current_board: Board) -> Board:
        """Get the current board

        Returns
        -------
        Board
            The current board
        """
        for board in Table.get_instance().boards:
            if board.title == current_board.title:
                return board

    def add_board(self) -> None:
        """Add a new board

        Parameters
        ----------
        parent : Ui_MainWindow
            The main window
        """
        while True:
            text = input_dialog_factory(
                title="Add a board",
                msg="Enter a new board title: ",
                btn_color=self.current_board.color
            )
            if text is None:
                return None
            if any(board.title == text for
                   board in Table.get_instance().boards):
                dialog_factory(
                    title="Invalid Title",
                    msg=f'Board "{text}" already exists!',
                    yes_no=False,
                    btn_color=self.current_board.color
                )
                continue
            elif text:
                break
            dialog_factory(
                title="Invalid Title",
                msg="Board title cannot be empty!",
                yes_no=False,
                btn_color=self.current_board.color
            )
        data = Table.get_instance().data
        data.append(
            {
                "_Board__title": text,
                "_Board__panels_lists": [],
                "_Board__color": "LIGHTBLUE"
            }
        )
        Table.get_instance().data = data
        Table.get_instance().write()
        logging.info(f'Board "{text}" added')
        self.clear_page()
        self.update_whole_page()
        self.change_board(Table.get_instance().boards[-1])

    def add_panel(self, board: Board) -> None:
        """Add a new panel

        Parameters
        ----------
        parent : Ui_MainWindow
            The main window
        board : Board
            The board to add the panel to
        """
        while True:
            text = input_dialog_factory(
                title="New panel",
                msg="Enter a new panel title:",
                btn_color=self.current_board.color
            )
            if text is None:
                return None

            if any(panel.title == text for panel in self.current_board.panels):
                dialog_factory(
                    title="Invalid Title",
                    msg=f'Panel "{text}" already exists!',
                    yes_no=False,
                    btn_color=self.current_board.color)
                continue

                
            '''
            if any(panel.title == text for
                   other_board in Table.get_instance().boards for
                   panel in other_board.panels):
                dialog_factory(
                    title="Invalid Title",
                    msg=f'Panel "{text}" already exists!',
                    yes_no=False,
                    btn_color=self.current_board.color)
                continue
            '''

            if text:
                break
            dialog_factory(
                title="Invalid Title",
                msg="Panel title cannot be empty!",
                yes_no=False,
                btn_color=self.current_board.color)
        data = Table.get_instance().data
        for i, tb_board in enumerate(Table.get_instance().boards):
            if tb_board.title == board.title:
                panels_list = data[i].get(
                    "_Board__panels_lists")
                try:
                    panel = {
                        "_Panel__title": text,
                        "_Board__panels": []
                    }
                    panels_list.append(panel)
                except AttributeError:
                    panels_list = [{
                        "_Panel__title": text, "_Board__panels": []
                    }]
                    data.get(
                        "_Table__data")[i]["_Board__panels_lists"] = \
                        panels_list
                Table.get_instance().data = data
                Table.get_instance().write()
                logging.info(f'Panel "{text}" added to board {board.title}')
                self.change_board(
                    Table.get_instance().boards[i]) 
                self.ui.scrollArea_panel_right.horizontalScrollBar(
                ).setValue(
                    self.ui.scrollArea_panel_right.horizontalScrollBar(
                    ).maximum())
                return None

    def add_card(self, panel: Panel) -> None:
        """Add a new card

        Parameters
        ----------
        parent : Ui_MainWindow
            The main window
        panel : Panel
            The panel to add the card to
        """
        while True:
            text = input_dialog_factory(
                title="New card",
                msg="Enter a new card title:",
                btn_color=self.current_board.color
            )
            if text is None:
                return None
            if text:
                break
            dialog_factory(
                title="Invalid Title",
                msg="Card title cannot be empty!",
                yes_no=False,
                btn_color=self.current_board.color
            )
        data = Table.get_instance().data
        for i, board in enumerate(Table.get_instance().boards):
            if board.title == self.current_board.title:
                for j, panel_ in enumerate(board.panels):
                    if panel_.title == panel.title:
                        if any(card.title == text for card in panel_.cards):
                            dialog_factory(
                                title="Invalid Title",
                                msg=f'Card "{text}" already exists!',
                                yes_no=False,
                                btn_color=self.current_board.color
                            )
                            self.add_card(panel)
                            return None
                        try:
                            data[i].get(
                                "_Board__panels_lists")[j].get(
                                "_Board__panels").append({
                                    "_Card__title": text,
                                    "_Card__description": "",
                                    "_Card__date": datetime.date.today()
                                    .strftime("%d-%m-%Y"),
                                    "_Card__time": datetime.datetime.now()
                                    .strftime("%H:%M")
                                })
                        except KeyError:
                            data.get(
                                "_Table__data")[i].get(
                                    "_Board__panels_lists")[j]["_Board__panels"] =\
                                [{
                                    "_Card__title": text,
                                    "_Card__description": "",
                                    "_Card__date": datetime.date.today()
                                    .strftime("%d-%m-%Y"),
                                    "_Card__time": datetime.datetime.now()
                                    .strftime("%H:%M")
                                }]
                        Table.get_instance().data = data
                        Table.get_instance().write()
                        logging.info(
                            f'Card "{text}" added to panel "{panel.title}"')
                        self.change_board(Table.get_instance().boards[i])

    def change_board(self, board: Board) -> None:
        """Change the board to the specified board
        - Remove all widgets from the layout
        - Create the new board
        - Remove the add panel button and horizontal spacer then add panel
        button again

        Parameters
        ----------
        parent : Ui_MainWindow
            The parent widget
        board : Board
            The board to change to
        """
        self.current_board = board
        layout = self.ui.scrollAreaContent_panel_right.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                layout.removeWidget(widget)
                widget.deleteLater()
        self.board_factory(board, 'Arimo-Medium.ttf')
        self.ui.list_add.setParent(None)
        self.ui.horizontalLayout_5.removeItem(
            self.ui.horzSpacer_panel_right)
        self.add_panel_button(board, 'Arimo-Medium.ttf')

    def change_card(self, board: Board, source: Panel, destination: Panel, card: Card,
                    index: int = None) -> None:
        """Change the card in a panel to another panel
        - Get the data from the table
        - Find the source panel and the specified card
        - Find the destination panel and add the card at a specified index
        - Remove the card from the source panel
        - Update the table

        Parameters
        ----------
        source : Panel
            The source panel
        destination : Panel
            The destination panel
        card : Card
            The card to move
        index : int, optional
            The index position to add the card in the destination panel,
            by default None (adds at the end)
        """
        data = Table.get_instance().data
        for i, b in enumerate(Table.get_instance().boards):
            if b.title == board.title:
                break
        print(source.data.title)
        '''
        source_list = next(
            (pan for pan in data[i].get("_Board__panels_lists", [])
             if pan.get("_Panel__title") == getattr(source, "data").title), {})
        '''
        source_list = {}
        for pan in data[i].get("_Board__panels_lists", []):
            if pan.get("_Panel__title") == getattr(source, "data").title:
                source_list = pan
                break
        '''
        card_to_move = next(
            (card_ for card_ in source_list.get("_Board__panels", [])
             if card_.get("_Card__title") == card.title), {})
        '''
        card_to_move = {}
        for card_ in source_list.get("_Board__panels", []):
            if card_.get("_Card__title") == card.title:
                card_to_move = card_
                break
        if card_to_move:
            source_list.get("_Board__panels").remove(card_to_move)
            '''
            dest_list = next(
                (pan for pan in data[i].get("_Board__panels_lists", [])
                 if pan.get("_Panel__title") == getattr(
                     destination, "data").title), {})
            '''
            dest_list = {}
            for pan in data[i].get("_Board__panels_lists", []):
                if pan.get("_Panel__title") == getattr(destination, "data").title:
                    dest_list = pan
                    break

            try:
                if index is None or index >= len(dest_list["_Board__panels"]):
                    dest_list["_Board__panels"].append(card_to_move)
                else:
                    dest_list["_Board__panels"].insert(index, card_to_move)
            except KeyError:
                dest_list["_Board__panels"] = [card_to_move]
            Table.get_instance().data = data

    def clear_page(self) -> None:
        """Clear the page
        - Remove all widgets from the layout

        """
        layout = self.ui.scrollAreaContent_panel_right.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                layout.removeWidget(widget)
                widget.deleteLater()
        layout = self.ui.scrollAreaContent_panel_left.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                layout.removeWidget(widget)
                widget.deleteLater()
        self.ui.verticalLayout_4.removeItem(
            self.ui.vertSpacer_scrollAreaContent)
        self.ui.horzSpacer_panel_right.changeSize(
            0, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)

    def setup_font(self, font: str) -> None:
        arimo = setup_font_db(font)[0]
        self.ui.label_logo.setFont(QFont(arimo, 36))
        self.ui.label_board.setFont(QFont(arimo, 28))
        self.ui.btn_add_board.setFont(QFont(arimo, 12))
        self.ui.btn_board_settings.setFont(QFont(arimo, 12))
        self.ui.btn_app_settings.setFont(QFont(arimo, 12))

