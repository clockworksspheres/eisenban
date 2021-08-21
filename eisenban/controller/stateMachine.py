"""

"""
# python standard libraries
import traceback

# third party libraries

# libraries from this software
from state import State
from priority import Priority


class StateEngine():

    kanbanColumns=["backlog", "in progress", "done", "on hold indefinitely", "on hold until", "archive"]

    def __init__(self):
        pass

    def changeState(self, newState={}):
        pass

    def archiveTask(self, taskId="", taskName=""):
        pass

    def deleteTask(self taskId="", taskName=""):
        pass

    def loadTasks(self, taskFileToLoad=""):
        pass

    def saveTasks(self, taskFileToSave=""):
        pass

    def listLoadedTasks(self, ):
        pass

    def listTasksFromFile(self, taskFileToLoadAndList=""):

    def printLoadedTasks(self):
        pass

    def printTasksFromFile(self, taskFileToLoadAndPrint=""):
        pass

    def newTask(self):
        pass

    def newKanbanColumn(self):
        pass

    def changeKanbanColumn(self):
        pass

    def changePriority(self):
        pass

    def changeKanbanColumn(self):
        pass

    def getDispatcher(self):
        """

        :param self:
        :return:

        More Notes: check out - https://stackoverflow.com/questions/9205081/is-there-a-way-to-store-a-function-in-a-list-or-dictionary-so-that-when-the-inde

        excerpt:
        Functions are first class objects in Python and so you can dispatch using a dictionary. For example, if foo and bar are functions, and dispatcher is a dictionary like so.

            dispatcher = {'foo': foo, 'bar': bar}
        Note that the values are foo and bar which are the function objects, and NOT foo() and bar().

        To call foo, you can just do dispatcher['foo']()

        EDIT: If you want to run multiple functions stored in a list, you can possibly do something like this.

            dispatcher = {'foobar': [foo, bar], 'bazcat': [baz, cat]}

            def fire_all(func_list):
                for f in func_list:
                    f()

            fire_all(dispatcher['foobar'])
        edited Feb 9 '12 at 3:53  answered Feb 9 '12 at 3:41  Praveen Gollakota
        """
        pass

