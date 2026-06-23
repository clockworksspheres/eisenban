import unittest
from unittest.mock import patch, MagicMock, Mock

# Replace with your actual module
from eisenban.eisenban_objects import Card, Panel, Board, Color


class TestCard(unittest.TestCase):

    def test_card_creation_defaults(self):
        card = Card()
        self.assertEqual(card.title, "New Card")
        self.assertEqual(card.date, "")
        self.assertEqual(card.time, "")
        self.assertEqual(card.description, "")

    def test_title_setter_valid(self):
        card = Card()
        card.title = "Test"
        self.assertEqual(card.title, "Test")

    def test_title_setter_none(self):
        card = Card()
        with self.assertRaises(ValueError):
            card.title = None

    @patch("eisenban.eisenban_objects.datetime")
    def test_date_valid(self, mock_datetime):
        mock_datetime.strptime = MagicMock()

        card = Card()
        card.date = "2024-01-01"

        mock_datetime.strptime.assert_called_once_with("2024-01-01", "%Y-%m-%d")

    @patch("eisenban.eisenban_objects.datetime")
    def test_date_invalid_format(self, mock_datetime):
        mock_datetime.strptime.side_effect = ValueError()

        card = Card()
        with self.assertRaises(ValueError):
            card.date = "invalid-date"

    @patch("eisenban.eisenban_objects.datetime")
    def test_time_valid(self, mock_datetime):
        mock_datetime.strptime = MagicMock()

        card = Card()
        card.time = "12:30"

        mock_datetime.strptime.assert_called_once_with("12:30", "%H:%M")

    @patch("eisenban.eisenban_objects.datetime")
    def test_time_invalid(self, mock_datetime):
        mock_datetime.strptime.side_effect = ValueError()

        card = Card()
        with self.assertRaises(ValueError):
            card.time = "99:99"

    def test_card_equality(self):
        c1 = Card("A", "01-01-2024", "10:00", "desc")
        c2 = Card("A", "01-01-2024", "10:00", "desc")

        self.assertEqual(c1, c2)

    def test_card_inequality_with_mock(self):
        c1 = Card("A")

        mock_card = MagicMock()
        mock_card.title = "B"
        mock_card.date = ""
        mock_card.time = ""
        mock_card.description = ""

        self.assertFalse(c1 == mock_card)

    def test_card_str(self):
        card = Card("A", "01-01-2024", "10:00", "desc")
        s = str(card)
        self.assertIn("title='A'", s)


class TestPanel(unittest.TestCase):

    def test_panel_creation(self):
        panel = Panel("Test Panel")
        self.assertEqual(panel.title, "Test Panel")
        self.assertEqual(panel.cards, [])

    def test_add_card(self):
        '''
        panel = Panel()
        card = Card("A")

        # NOTE: your setter has a logic bug; still testing behavior
        with self.assertRaises(ValueError):
            panel.cards = card
        '''
        panel = Panel()
        card = Card("A")

        panel.cards = card

        self.assertIn(card, panel.cards)

    def test_add_duplicate_card(self):
        panel = Panel()
        card = Card("A")

        panel.cards = card

        with self.assertRaises(ValueError):
            panel.cards = card

    def test_add_card_none(self):
        panel = Panel()

        with self.assertRaises(ValueError):
            panel.cards = None

    def test_title_setter_none(self):
        panel = Panel()
        with self.assertRaises(ValueError):
            panel.title = None

    def test_panel_equality(self):
        card = Card("A")
        p1 = Panel("P", [card])
        p2 = Panel("P", [card])

        self.assertEqual(p1, p2)

    def test_panel_str_with_mock_cards(self):
        mock_card = MagicMock()
        mock_card.title = "MockCard"

        panel = Panel("Panel", [mock_card])
        s = str(panel)

        self.assertIn("MockCard", s)


class TestBoard(unittest.TestCase):

    def test_board_creation_valid_color(self):
        board = Board("Board1", "LIGHTBLUE")
        self.assertEqual(board.title, "Board1")
        self.assertEqual(board.color, Color.LIGHTBLUE.value)

    def test_board_invalid_color(self):
        with self.assertRaises(ValueError):
            Board("Board", "INVALID")

    def test_color_setter_valid(self):
        board = Board()
        board.color = Color.LIGHTBLUE.value
        self.assertEqual(board.color, Color.LIGHTBLUE.value)

    def test_color_setter_invalid(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.color = "INVALID"

    def test_add_panel(self):
        board = Board()
        panel = Panel("P")

        board.panels = panel
        self.assertIn(panel, board.panels)

    def test_add_duplicate_panel(self):
        board = Board()
        panel = Panel("P")

        board.panels = panel
        with self.assertRaises(ValueError):
            board.panels = panel

    def test_board_equality_with_mock(self):
        board = Board("B", "LIGHTBLUE", [])

        mock_board = MagicMock()
        mock_board.title = "B"
        mock_board.color = Color.LIGHTBLUE.value
        mock_board.panels = []

        self.assertTrue(board == mock_board)

    def test_board_str(self):
        board = Board("B", "LIGHTBLUE")
        s = str(board)

        self.assertIn("title='B'", s)
        self.assertIn("LIGHTBLUE", s)


if __name__ == "__main__":
    unittest.main()

