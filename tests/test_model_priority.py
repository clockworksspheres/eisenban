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
from eisenban.lib.libHelperExceptions import NotValidForThisOS


class test_model_priority(unittest.TestCase):
    """

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
        pass

    ##################################

    def test_two(self):
        """
        """
        pass

###############################################################################
##### unittest Tear down
    @classmethod
    def tearDownClassInstanceSpecifics(self):
        """
        teardown tasks
        """
        pass

###############################################################################

