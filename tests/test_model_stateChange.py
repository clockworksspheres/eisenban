#!/usr/bin/python -u
"""
Template for tests

"""

#--- Native python libraries
import re
import os
import sys
import time
import unittest
import tempfile
import ctypes as C
from datetime import datetime

#--- non-native python libraries in this source tree
from eisenban.lib.loggers import CyLogger
from eisenban.lib.loggers import LogPriority as lp


class test_model_stateChange(unittest.TestCase):
    """
    Test unionfs functionality of ramdisks

    @author: Roy Nielsen
    """

    @classmethod
    def setUpClass(self):
        """
        Initializer
        """
        # self.libc = self.getLibc()
     
    ##################################

    def setUp(self):
        """
        This method runs before each test case.
        """
        pass


###############################################################################
##### Method Tests

    ##################################

    def test_one(self):
        """
        """
        self.assertTrue(False, "False is not True...")

    ##################################

    def test_two(self):
        """
        """
        self.assertTrue(False, "False is not True...")

###############################################################################
##### unittest Tear down
    @classmethod
    def tearDownClassInstanceSpecifics(self):
        """
        teardown tasks
        """
        pass

###############################################################################

if __name__ == "__main__":
    unittest.main()
