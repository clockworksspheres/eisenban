import os
import sys
import unittest
from unittest.mock import patch, MagicMock

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

import eisenban.utils


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def make_key_event(key):
    return QKeyEvent(QKeyEvent.KeyPress, key, Qt.NoModifier)


# -------------------------------------------------
# Tests
# -------------------------------------------------
class TestUtils(unittest.TestCase):

    # -------------------------
    # overrides()
    # -------------------------
    def test_overrides_success(self):
        class Base:
            def foo(self): pass

        @eisenban.utils.overrides(Base)
        def foo():
            return "ok"

        self.assertEqual(foo(), "ok")

    def test_overrides_failure(self):
        class Base:
            def foo(self): pass

        with self.assertRaises(AssertionError):
            @eisenban.utils.overrides(Base)
            def bar():
                pass

    # -------------------------
    # hex_to_rgba()
    # -------------------------
    def test_hex_to_rgba(self):
        self.assertEqual(
            eisenban.utils.hex_to_rgba("rgb(1,2,3)"),
            "rgba(1,2,3, 255)"
        )

    def test_hex_to_rgba_multiple(self):
        self.assertEqual(
            eisenban.utils.hex_to_rgba("rgb(10,20,30)"),
            "rgba(10,20,30, 255)"
        )

    # -------------------------
    # modify_hex_color()
    # -------------------------
    def test_modify_hex_color_lighten(self):
        self.assertEqual(
            eisenban.utils.modify_hex_color("#000000", 30),
            "#1e1e1e"
        )

    def test_modify_hex_color_clamp_upper(self):
        self.assertEqual(
            eisenban.utils.modify_hex_color("#ffffff", 30),
            "#ffffff"
        )

    def test_modify_hex_color_clamp_lower(self):
        self.assertEqual(
            eisenban.utils.modify_hex_color("#101010", -20),
            "#000000"
        )

    def test_modify_hex_color_mid(self):
        self.assertEqual(
            eisenban.utils.modify_hex_color("#112233", 10),
            "#1b2c3d"
        )

    # -------------------------
    # get_current_directory()
    # -------------------------
    @patch.object(sys, "frozen", False, create=True)
    def test_get_current_directory_normal(self):
        path = eisenban.utils.get_current_directory()
        self.assertTrue(os.path.isabs(path))

    @patch.object(sys, "frozen", True, create=True)
    @patch.object(sys, "_MEIPASS", "/tmp/testpath", create=True)
    def test_get_current_directory_frozen(self):
        path = eisenban.utils.get_current_directory()
        self.assertEqual(path, "/tmp/testpath")

    # -------------------------
    # setup_font_db()
    # -------------------------
    @patch("eisenban.utils.QFontDatabase")
    @patch("eisenban.utils.get_current_directory", return_value="/base")
    def test_setup_font_db_success(self, mock_base, mock_qfont):
        mock_qfont.addApplicationFont.return_value = 1
        mock_qfont.applicationFontFamilies.return_value = ["Arial"]

        result = eisenban.utils.setup_font_db("font.ttf")

        self.assertEqual(result, ["Arial"])
        mock_qfont.addApplicationFont.assert_called_once()

    @patch("eisenban.utils.QFontDatabase")
    @patch("eisenban.utils.get_current_directory", return_value="/base")
    def test_setup_font_db_failure(self, mock_base, mock_qfont):
        mock_qfont.addApplicationFont.return_value = -1

        with self.assertRaises(Exception):
            eisenban.utils.setup_font_db("font.ttf")

    # -------------------------
    # keyPressEvent()
    # -------------------------
    def test_keypress_enter_with_parent(self):
        func = MagicMock()
        parent = MagicMock()

        event = make_key_event(Qt.Key_Return)

        eisenban.utils.keyPressEvent(event, parent, func)

        func.assert_called_once_with(parent)

    def test_keypress_enter_without_parent(self):
        func = MagicMock()

        event = make_key_event(Qt.Key_Return)

        eisenban.utils.keyPressEvent(event, None, func)

        func.assert_called_once_with()

    def test_keypress_enter_no_function(self):
        event = make_key_event(Qt.Key_Return)

        result = eisenban.utils.keyPressEvent(event, None, None)

        self.assertIsNone(result)

    def test_keypress_other_key(self):
        func = MagicMock()

        event = make_key_event(Qt.Key_A)

        result = eisenban.utils.keyPressEvent(event, None, func)

        func.assert_not_called()
        self.assertIsNone(result)

    def test_keypress_key_enter_variant(self):
        func = MagicMock()

        event = make_key_event(Qt.Key_Enter)

        eisenban.utils.keyPressEvent(event, None, func)

        func.assert_called_once()


# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    unittest.main()

