# import standard libraries
import re
import os

# local, program specific library
from .loggers import CyLogger
from .loggers import LogPriority as lp


class Conf(object) :
    """
    Class for holding the configuration variables

    Intended initialization happens in program_options.py.

    @author: Roy Nielsen
    """    
    def __init__(self) :
        self.version = "0.0.0.0"
        self.options = []
        self.logger = CyLogger()
        psudopath = os.path.abspath(os.path.dirname(__file__))
        partialpath = psudopath.split("/")
        self.appPath = os.path.join("/", "/".join(partialpath[:-1]))

    def getVersion(self) :
        """
        getter for application version

        format: "run_once.py 1.7.x.x"
        """
        return self.version

    def setVersion(self, version="0.0.0.0") :
        """
        setter for application version

        format: "run_once.py 1.7.x.x"
        """
        self.version = version

    def setLogger(self, logger=False):
        """
        setter for command line options
        """
        self.logger = logger

    def getLogger(self):
        """
        getter for command line options
        """
        return self.logger

    def setCurrentRepo(self, repoPath=""):
        """
        Setter for the password
        """
        self.currentRepoPath = repoPath

    def getCurrentRepo(self):
        """
        Getter for the password
        """
        return self.currentRepoPath

    def setCurrentVarFilePath(self, varFilePath):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        self.currentVarFilePath = varFilePath
    
    def getCurrentVarFilePath(self):
        '''
        Getter for the full packer json file path

        @author: Roy Nielsen
        '''
        return self.currentVarFilePath
    
    def returnConf(self) :
        """
        return self...
        """
        return self

    def printSelf(self) :
        """
        print current Configuration
        """
        print "---==# #==---"
        print "script version:  " + str(self.version)
        print "---==# #==---"

    def loggerSelf(self) :
        """
        log current Configuration via logger function
        """
        self.logger.log(lp.DEBUG, "---==# #==---")
        self.logger.log(lp.DEBUG, "script version:  " + str(self.version))
        self.logger.log(lp.DEBUG, "---==# #==---")
