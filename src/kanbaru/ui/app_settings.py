import logging
from typing import List

from PySide6.QtCore import QEvent
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow

from db import Table
from dialog import dialog_factory
from kanbaru_objects import Board
from ui.about import About
from ui.app_settings_ui import Ui_SettingsWindow
from utils import keyPressEvent, modify_hex_color, setup_font_db


class AppSettings(QMainWindow):
    def __init__(self, board: Board) -> None:
        QMainWindow.__init__(self)

        self.ui: Ui_SettingsWindow = Ui_SettingsWindow()
        self.ui.setupUi(self)

        self.board: Board = board
        self.title: str = board.title
        self.color: str = board.color
        self.boards_to_delete: List[Board] = []
        self.new_board_order: List[Board] = []

        self.ui.btn_delete.clicked.connect(self.delete)
        self.ui.btn_cancel.clicked.connect(self.close)
        self.ui.btn_save.clicked.connect(self.save)

        self.ui.btn_delete.keyPressEvent = lambda event: keyPressEvent(
            event, function=self.delete(event))
        self.ui.btn_cancel.keyPressEvent = lambda event: keyPressEvent(
            event, function=self.close)
        self.ui.btn_save.keyPressEvent = lambda event: keyPressEvent(
            event, function=self.save)

        self.ui.listWidget_manage_board.verticalScrollBar().setSingleStep(10)
        self.ui.listWidget_manage_board.model().rowsMoved.connect(
            self.rowsMoved)

        self.setup_font()

        self.ui.listWidget_manage_board.addItems(
            [board.title for board in Table.get_instance().boards])

        stylesheet = \
            f"""
            QPushButton {{
                background-color: {self.color};
                color: #ffffff;
            }}
            QPushButton:hover {{
                background-color: {modify_hex_color(self.color, -30)};
            }}
            QPushButton:focus {{
                border-color: #000000;
                border-width: 1.5px;
                border-style: solid;
            }}
            """
        self.ui.label_app_settings.setStyleSheet(
            f"""
            background-color: qlineargradient(
                spread: pad,
                x1: 0.5,
                y1: 0.5,
                x2: 0.95,
                y2: 0.5,
                stop: 0 {self.color},
                stop: 1 rgba(69, 76, 90, 255)
            );
            color: #ffffff;
            padding: 0 0 0 10px;
            """
        )
        self.ui.listWidget_manage_board.setStyleSheet(
            f"""
            QListWidget::item {{
                height: 40px;
                padding: 0 8px 0 8px
            }}
            QListWidget::item {{
                background-color: #ffffff;
                color: #000000;
                border-radius: 5px
            }}
            QListWidget::item:hover {{
                background-color: #e2e4e9;
                color: #000000
            }}
            QListWidget::item:selected {{
                background-color: #cccccc;
                color: #000000
            }}
            QListWidget::item:focus {{
                background-color: #cccccc;
                color: #000000
            }}
            QScrollBar:vertical {{
                border: none;
                background: #f4f5f7;
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
                color: #ffffff;
            }}
            QScrollBar QMenu::item:selected {{
                border-radius: 5px;
                background-color: {modify_hex_color(self.color)};
                color: #000000;
            }}
            """
        )
        self.ui.btn_about.setStyleSheet(stylesheet)
        self.ui.btn_save.setStyleSheet(stylesheet)

        self.ui.btn_about.clicked.connect(
            lambda event: self.show_about(event, board.color))

    def show_about(self, event: QEvent, color: str) -> None:
        """Shows the about dialog"""
        self.about: About = About(color)
        self.about.show()

    def delete(self, event: QEvent) -> None:
        """Deletes the selected board(s)"""
        selected_all = self.ui.listWidget_manage_board.selectedItems()
        if len(selected_all) == 0:
            dialog_factory(
                title="Invalid Selection",
                msg="Please select a board to delete. You can also select "
                "multiple boards to delete at the same time.",
                yes_no=False,
                btn_color=self.color
            )
            return None
        if len(selected_all) == len(Table.get_instance().boards):
            dialog_factory(
                title="Invalid Selection",
                msg="You cannot delete all boards. Please select at least one "
                "board to keep.",
                yes_no=False,
                btn_color=self.color
            )
            return None
        msg_list = '\n'.join(
            ["  - " + item for item in list(
                map(lambda x: x.text(), selected_all))])
        if dialog_factory(
            title="Delete Board",
            msg="Are you sure you want to delete "
            f"{'these boards' if len(selected_all) > 1 else 'this board'}?"
            f"\n{msg_list}\n\nYou can still undo by pressing the Cancel "
            "button.",
            btn_color=self.color
        ):
            for selected_board in selected_all:
                board_obj = next(
                    (board for board in Table.get_instance().boards if
                     board.title == selected_board.text()), None)
                self.boards_to_delete.append(board_obj)
                self.ui.listWidget_manage_board.takeItem(
                    self.ui.listWidget_manage_board.row(selected_board))

    def save(self) -> None:
        """Deletes the selected boards and saves the new board order"""
        for board in self.boards_to_delete:
            Table.get_instance().delete_board(board)
        if len(self.new_board_order) != 0:
            Table.get_instance().update_board_order(self.new_board_order)
        self.close()

    def rowsMoved(self) -> None:
        """Updates the new board order when the user changes the board order"""
        self.new_board_order = [
            self.ui.listWidget_manage_board.item(i).text()
            for i in range(self.ui.listWidget_manage_board.count())
        ]
        self.new_board_order = [
            next((board for board in Table.get_instance().boards
                  if board.title == board_title), None)
            for board_title in self.new_board_order
        ]

    def setup_font(self) -> None:
        andika = setup_font_db("Andika-Regular.ttf")[0]
        self.ui.label_app_settings.setFont(QFont(andika, 28))
        self.ui.label_manage_board.setFont(QFont(andika, 14, QFont.Bold))
        self.ui.label_manage_board_desc.setFont(QFont(andika, 11))
        self.ui.btn_delete.setFont(QFont(andika, 12))
        self.ui.btn_cancel.setFont(QFont(andika, 12))
        self.ui.btn_save.setFont(QFont(andika, 12))
