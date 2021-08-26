#!/usr/bin/env -S python -u
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

#####
# Include the parent project directory in the PYTHONPATH
appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(appendDir)

#--- non-native python libraries in this source tree
from eisenban.lib.loggers import CyLogger
from eisenban.lib.loggers import LogPriority as lp


class test_model_priority(unittest.TestCase):
    """

    """

    ###############################################################################
    ##### unittest Set Up
    @classmethod
    def setUpClass(self):
        """
        This method runs before all test cases
        """
        pass
     
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
    ##### unittest Tear Down

    def tearDown(self):
        """
        teardown tasks
        """
        pass

    ##################################
    @classmethod
    def tearDownClass(self):
        """
        teardown tasks
        """
        pass

###############################################################################


if __name__ == "__main__":
    unittest.main()
