
from . loggers import CyLogger
from . loggers import LogPriority as lp
from . getLibc import getLibc


class genericDeviceController(object):
    """

    @creation date: 2021-10-10
    """
    def __init__(self):
        if isinstance(logger, CyLogger):
            self.logger = logger
        else:
            raise NotACyLoggerError("Passed in value for logger" +
                                    " is invalid, try again.")
        self.header = {"deviceClass": "",
                       "baseClass": "",
                       "deviceId": "",
                       "subSystemId": "",
                       "revisionId": "",
                       "vendorId": "",
                       "defaultCommand": ""
                       }
        command = ""
        status = ""

    def setCommand(self, command=""):
        """

        :param command:
        :return:
        """
        self.command = command

    def getCommand(self):
        """

        :return:
        """
        return self.command

    def getStatus(self):
        """

        :return:
        """
        return self.status

    def getHeader(self):
        """

        :return:
        """
        return self.header


