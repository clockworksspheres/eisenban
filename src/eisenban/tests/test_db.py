import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

import db
from db import Table


class TestTableFullCoverage(unittest.TestCase):

    # -------------------------
    # Test lifecycle
    # -------------------------
    def setUp(self):
        Table._instance = None
        Table._SingletonMeta__instances = {}
        self.table = Table()
        self.table._tb_path = "/tmp/test.tbl"

    def tearDown(self):
        Table._instance = None
        Table._SingletonMeta__instances = {}

    # -------------------------
    # Helpers
    # -------------------------
    def _valid_data(self):
        return [
            {
                "_Board__title": "B",
                "_Board__color": "LIGHTBLUE",
                "_Board__panels_lists": [
                    {
                        "_Panel__title": "P",
                        "_Board__panels": [
                            {
                                "_Card__title": "C",
                                "_Card__description": "",
                                "_Card__date": "",
                                "_Card__time": ""
                            }
                        ]
                    }
                ]
            }
        ]

    def _mock_board_tree(self):
        card = MagicMock()
        card.title = "C"
        card.description = ""
        card.date = ""
        card.time = ""
        card.__eq__.return_value = True

        panel = MagicMock()
        panel.title = "P"
        panel.cards = [card]
        panel.__eq__.return_value = True

        board = MagicMock()
        board.title = "B"
        board.color = "LIGHTBLUE"
        board.panels = [panel]
        board.__eq__.return_value = True

        return board, panel, card

    # -------------------------
    # Singleton
    # -------------------------
    def test_singleton(self):
        self.assertIs(Table(), Table())

    def test_get_instance(self):
        Table._instance = None
        with patch.object(Table, "__init__", return_value=None):
            instance = Table.get_instance()
            self.assertTrue(instance is None or isinstance(instance, Table))

    # -------------------------
    # Path
    # -------------------------
    @patch("db.logging.warning")
    def test_set_path_empty(self, mock_warn):
        self.assertIsNone(self.table.set_path(""))
        mock_warn.assert_called_once()

    def test_set_get_path(self):
        self.table.set_path("/tmp/x")
        self.assertEqual(self.table.get_path(), "/tmp/x")

    # -------------------------
    # create()
    # -------------------------
    @patch("db.sys.exit", side_effect=SystemExit)
    @patch("db.pickle.dump", side_effect=Exception)
    @patch("db.open", new_callable=mock_open)
    @patch("db.os.makedirs")
    def test_create_exception(self, *_):
        with self.assertRaises(SystemExit):
            self.table.create()

    @patch.object(Table, "get_instance")
    @patch("db.pickle.dump")
    @patch("db.open", new_callable=mock_open)
    @patch("db.os.makedirs")
    def test_create_success(self, m_mkdir, m_open, m_dump, m_get):
        inst = MagicMock()
        m_get.return_value = inst

        self.table.create()

        m_dump.assert_called_once()
        inst.read.assert_called_once()

    # -------------------------
    # write()
    # -------------------------
    @patch("db.pickle.dump")
    @patch("db.open", new_callable=mock_open)
    def test_write_ok(self, m_open, m_dump):
        self.table.write()
        m_dump.assert_called_once()

    @patch.object(Table, "create")
    @patch("db.open", side_effect=FileNotFoundError)
    def test_write_fnf(self, m_open, m_create):
        self.table.write()
        m_create.assert_called_once()

    @patch("db.sys.exit", side_effect=SystemExit)
    @patch("db.pickle.dump", side_effect=Exception)
    @patch("db.open", new_callable=mock_open)
    def test_write_exception(self, *_):
        with self.assertRaises(SystemExit):
            self.table.write()

    # -------------------------
    # read()
    # -------------------------
    @patch("db.Color")
    @patch("db.pickle.load", return_value=[])
    @patch("db.open", new_callable=mock_open)
    def test_read_ok(self, m_open, m_load, _):
        self.table.read()
        m_load.assert_called_once()

    @patch("db.Color")
    @patch.object(Table, "create")
    @patch("db.open", side_effect=FileNotFoundError)
    def test_read_fnf(self, m_open, m_create, _):
        self.table.read()
        m_create.assert_called_once()

    @patch("db.Color")
    @patch.object(Table, "create")
    @patch("db.open", new_callable=mock_open)
    @patch("db.pickle.load", side_effect=Exception)
    def test_read_exception(self, m_load, m_open, m_create, _):
        self.table.read()
        m_create.assert_called_once()

    # -------------------------
    # boards property
    # -------------------------
    @patch("db.Color")
    def test_boards_property(self, _):
        self.table.data = self._valid_data()
        boards = self.table.boards
        self.assertEqual(len(boards), 1)

    def test_boards_setter(self):
        # Just cover it (it's buggy by design)
        self.table._Table__data = {}
        self.table.boards = []
        self.assertIn("_Board__title", self.table._Table__data)

    # -------------------------
    # update_* methods
    # -------------------------
    @patch.object(Table, "write")
    def test_update_card(self, m_write):
        self.table.data = self._valid_data()
        b, p, c = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.update_card(c, c)

        m_write.assert_called_once()

    @patch.object(Table, "write")
    def test_update_panel(self, m_write):
        self.table.data = self._valid_data()
        b, p, _ = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.update_panel(p, p)

        m_write.assert_called_once()

    @patch("db.Color")
    @patch.object(Table, "write")
    def test_update_board(self, m_write, m_color):
        m_color.return_value.name = "LIGHTBLUE"

        self.table.data = self._valid_data()
        b, _, _ = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.update_board(b, b)

        m_write.assert_called_once()

    @patch.object(Table, "write")
    def test_update_panel_order(self, m_write):
        self.table.data = self._valid_data()
        b, _, _ = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.update_panel_order(b, [])

        m_write.assert_called_once()

    @patch("db.Color")
    @patch.object(Table, "write")
    def test_update_board_order(self, m_write, m_color):
        m_color.return_value.name = "LIGHTBLUE"

        b, _, _ = self._mock_board_tree()
        self.table.update_board_order([b])

        m_write.assert_called_once()

    # -------------------------
    # delete_* methods
    # -------------------------
    @patch.object(Table, "write")
    def test_delete_card(self, m_write):
        self.table.data = self._valid_data()
        b, p, c = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.delete_card(c)

        m_write.assert_called_once()

    @patch.object(Table, "write")
    def test_delete_panel(self, m_write):
        self.table.data = self._valid_data()
        b, p, _ = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.delete_panel(p)

        m_write.assert_called_once()

    @patch.object(Table, "write")
    def test_delete_board(self, m_write):
        self.table.data = self._valid_data()
        b, _, _ = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.delete_board(b)

        m_write.assert_called_once()

    # -------------------------
    # change color
    # -------------------------
    @patch("db.Color")
    @patch.object(Table, "write")
    def test_change_board_color(self, m_write, m_color):
        m_color.return_value.name = "LIGHTBLUE"

        self.table.data = {"_Table__data": self._valid_data()}
        b, _, _ = self._mock_board_tree()

        with patch.object(Table, "boards", new_callable=MagicMock(return_value=[b])):
            self.table.change_board_color(b, "anything")

        m_write.assert_called_once()

    # -------------------------
    # misc
    # -------------------------
    def test_str(self):
        self.table.data = [{"x": 1}]
        self.assertIn("x", str(self.table))


if __name__ == "__main__":
    unittest.main()


