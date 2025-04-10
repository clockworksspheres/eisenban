

import os
import re
import sys
import psygnal
import threading
import traceback

sys.path.append("../../..")

from eisenban.lib.loggers import CyLogger
from eisenban.lib.loggers import LogPriority as lp
from eisenban.lib.loggers import MockLogger


class OSNotValidForRunWith(BaseException):
    """
    Custom Exception
    """
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class NotACyLoggerError(BaseException):
    """
    Custom Exception
    """
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class SetCommandTypeError(BaseException):
    """
    Custom Exception
    """
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)



class RunThread(threading.Thread):
    """
    Use a thread & subprocess.Popen to run something

    To use - where command could be an array, or a string... :

    run_thread = RunThread(<command>, message_level)
    run_thread.start()
    run_thread.join()
    print run_thread.stdout

    @author: Roy Nielsen
    """
    def __init__(self, command, logger, myshell=False):
        """
        Initialization method
        """
        self.command = command
        self.logger = logger
        self.retout = None
        self.reterr = None
        self.shell = myshell
        threading.Thread.__init__(self)

        if isinstance(self.command, list):
            self.shell = True
            self.printcmd = " ".join(self.command)
        if isinstance(self.command, (str,)):
            self.shell = False
            self.printcmd = self.command

        if isinstance(logger, CyLogger):
            self.logger = logger
        else:
            raise NotACyLoggerError("Passed in value for logger " +
                                    "is invalid, try again.")

        self.logger.log(lp.INFO, "Initialized runThread...")

    ##########################################################################

    def run(self):
        if self.command:
            try:
                p = Popen(self.command, stdout=PIPE,
                                        stderr=PIPE,
                                        shell=self.shell)
                self.retout, self.reterr = p.communicate()
                self.logger.log(lp.WARNING, "Finished \"run\" of: " +
                                str(self.command))
            except SubprocessError as err:
                self.logger.log(lp.WARNING, "Exception trying to open: " +
                                str(self.command))
                self.logger.log(lp.WARNING, traceback.format_exc())
                self.logger.log(lp.WARNING, str(err))
                raise err
            else:
                try:
                    self.retout, self.reterr = p.communicate()
                except SubprocessError as err:
                    self.logger.log(lp.WARNING, "Exception trying to open: " +
                                    str(self.printcmd))
                    self.logger.log(lp.WARNING, "Associated exception: " +
                                    str(err))
                    raise err
                else:
                    self.logger.log(lp.WARNING, "Finished \"run\" of: " +
                                    str(self.printcmd))

    ##########################################################################

    def getStdout(self):
        """
        Getter for standard output

        @author: Roy Nielsen
        """
        self.logger.log(lp.INFO, "Getting stdout...")
        return self.retout

    ##########################################################################

    def getStderr(self):
        """
        Getter for standard err

        @author: Roy Nielsen
        """
        self.logger.log(lp.DEBUG, "Getting stderr...")
        return self.reterr

##############################################################################

def runMyThreadCommand(cmd, logger, myshell=False):
    """
    Use the RunThread class to get the stdout and stderr of a command

    @author: Roy Nielsen
    """
    retval = None
    reterr = None
    if not isinstance(logger, CyLogger):
        raise NotACyLoggerError("Passed in value for logger is "
                                "invalid, try again.")
    print(str(cmd))
    print(str(logger))
    if cmd and logger:
        run_thread = RunThread(cmd, logger, myshell)
        run_thread.start()
        # run_thread.run()
        run_thread.join()
        retval = run_thread.getStdout()
        reterr = run_thread.getStderr()
    else:
        logger.log(lp.INFO, "Invalid parameters, please report this as a bug.")

    return retval, reterr

