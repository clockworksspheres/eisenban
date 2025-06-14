#!/usr/bin/env -S python -u

import logging
import os
import sys

from optparse import OptionParser

from tkinter import Tk, messagebox

if sys.version_info < (3, 10):
    print("Python 3.10 or higher is required to run Eisenban. Please consider "
          "upgrading.")
    sys.exit(1)

try:
    from PySide6.QtWidgets import QApplication, QMainWindow
    from db import Table
    from ui.main import MainScreen
    from ui.welcome import WelcomeScreen
    from utils import get_current_directory
except ModuleNotFoundError:
    logging.warning("Required modules not found. Prompting user to install...")
    root = Tk()
    root.withdraw()
    response = messagebox.askyesno(
        "Error: Module Not Found",
        "Required modules not found. Would you like to install them now?\n\n"
        "Required modules: PySide6, firebase-admin"
    )

    if response:
        path = os.path.dirname(os.path.abspath(__file__))
        try:
            import pip
            pip.main(
                ["install", "-r", f"{os.path.join(path, 'requirements.txt')}"]
            )
        except ModuleNotFoundError:
            logging.warning(
                "pip not found. Installing pip now. This is a risky move. "
                "btw why don't you have pip installed yet?"
            )
            import ensurepip
            ensurepip.bootstrap()
            pip.main(["install", "-r", "requirements.txt"])
        finally:
            from PySide6.QtWidgets import QApplication, QMainWindow

            from db import Table
            from ui.main import MainScreen
            from ui.welcome import WelcomeScreen
            from utils import get_current_directory
    else:
        sys.exit(1)


class Eisenban(QMainWindow):
    def __init__(self, dbdir="") -> None:
        QMainWindow.__init__(self)

        # Get current directory
        self.tb_path = None
        self.path = get_current_directory()

        logging.info("Starting Eisenban...")
        logging.info(f'Current directory: "{self.path}"')

        # Initialize local table
        self.initialize_local_table(dbdir)

        # straight to the main screen
        self.show_main_screen()

    @staticmethod
    def init_event_logger(path: str, fmt: str, debug: bool = False,
                          stdout: bool = False) -> None:
        """Initializes the event logger.
        - Set the path of the event log file
        - Set the format of the event log file
        - Set the debug level of the event log file
        - Set up the event logger
        """
        logging.basicConfig(
            filename=path,
            filemode="w",
            format=fmt,
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.DEBUG if debug else logging.INFO,
        )
        if stdout:
            logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    def initialize_local_table(self, dbdir: str) -> None:
        """Initializes the table instance.
        - Determine table path
        - Create table instance
        - Set table path
        - Read table file
        """
        if dbdir:
            logging.info("dbdir detected")
            self.tb_path = os.path.join(
                dbdir, "Table.pickle"
            )
        
        else:
            if sys.platform == "win32":
                logging.info("Windows OS detected")
                self.tb_path = os.path.join(
                    os.path.expanduser(
                        "~"), "Documents", "Eisenban", "Table.pickle"
                )
            else:
                logging.info("Unix OS detected")
                self.tb_path = os.path.join(
                    os.path.expanduser("~"), "Eisenban", "Table.pickle"
                )
        tb = Table.get_instance()
        tb.set_path(self.tb_path)
        tb.read()
        logging.info(f'Table path: "{tb.get_path()}"')
        logging.info("Table instance initialized and read successfully")

    def show_main_screen(self):
        """Shows the main screen."""
        logging.info("Going to main screen...")
        MainScreen(self)


def init_event_logger(path: str, fmt: str, debug: bool = False,
                      stdout: bool = False) -> None:
    """Initializes the event logger.
    - Set the path of the event log file
    - Set the format of the event log file
    - Set the debug level of the event log file
    - Set up the event logger
    """
    logging.basicConfig(
        filename=path,
        filemode="w",
        format=fmt,
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.DEBUG if debug else logging.INFO,
    )
    if stdout:
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


if __name__ == "__main__":
    from multiprocessing import freeze_support, set_start_method
    freeze_support()
    set_start_method('spawn', force=True)

    parser = OptionParser(usage="\n\n%prog [options]\n\n", version="0.8.6")

    parser.add_option("-t", "--table", dest="table",
                    default="",
                    help="Name of the directory you want the database table to be stored")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                    default=0, help="Print debug messages")
    parser.add_option("-v", "--verbose", action="store_true",
                    dest="verbose", default=0,
                    help="Print status messages")

    (opts, args) = parser.parse_args()


    app = QApplication(sys.argv)

    # Set up event logger
    init_event_logger(
        os.path.join(get_current_directory(), "event.log"),
        "%(asctime)s - %(levelname)s - %(message)s",
        stdout=True,
        debug=True if "--debug" in sys.argv else False,
    )

    window = Eisenban(opts.table)
    window.show()
    sys.exit(app.exec())
