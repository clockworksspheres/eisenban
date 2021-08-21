import copy
import traceback

from priority import Priority

class State(priority):

  """
  :version:
  :author:
  """

  """ ATTRIBUTES

  taskId  (private)

  notesOnThisNewState  (private)

  kanbanColumn  (private)

  holdUntil  (private)

  holdNotes  (private)

  enteredThisStateTimestamp  (private)

  targetCompletionTimestamp  (private)

  currentPriority  (private)

   index into array indicating which named column is the current state.


  currentKanbanColumn  (private)

  """
  def __init__(self, config={}, notesOnThisNewState=0, kanbanColumn=True, holdUntil=True, holdNotes="", targetCompletionTimestamp="", currentPriority="", holdNotes=""):
    """


    @param signed int niceLevel :
    @param bool urgent :
    @param bool important :
    @param string priorityNotes :
    @return  :
    @author : Roy Nielsen

    :TODO: Need to initialize priority if passed in???

    """
    #####
    # Global App configuration, passed in on the command line or from a config file, or set as defaults
    # TODO: Need to create config object and initialization
    # TODO: Need to initialze 'type' of config, both as passed in, and as part of type checking
    # TODO: Need to import or create logger, insert to config object, or pass in separately?  check out other clockworkspheres apps
    if isinstance(config, dict):
      self.config = config
    else:
      self.config = {}

    if isinstance(taskId, int) and taskId > 0:
      self.taskId = taskId
    else:
      self.taskId = 1

    if isinstance(notesOnThisNewState, str):
      self.notesOnThisState = notesOnThisNewState
    else:
      self.notesOnThisState = ""

    #####
    #  kanbanColumn or current State at task resides in
    try:
      if self.kanbanColumns = self.config.kanbanColumns
    except IndexError as err:
      # TODO: implement defaulting this branch to highest nice level, urgent=True, important=True, place in the backlog
      #       to make sure this issue gets immediate triage to the right priority and state.
      self.logger.log("ERROR", traceback.format_exc("Not a valid kanban column for this app, defaulting to backlog"))

    if newKanbanColumn in self.kanbanColumns:
      self.kanbanColumn = newKanbanColumn
    else:
      self.kanbanColumn = "backlog"

    # TODO: Need better way to represent target datetime, than a string? CCYY-MM-DD_HH-MM to start?
    if isinstance(holdUntil, str):
      self.holdUntil = holdUntil
    else:
      self.holdUntil = ""

    self.enteredThisStateTimestamp = self.config.getCurrentDateTimeStamp()

    if isinstance(targetCompletionTimestamp, str):
      self.targetCompletionTimestamp = targetCompletionTimestamp
    else:
      self.targetCompletionTimestamp = ""

    if isinstance(currentPriority, priority):
      self.currentPriority = copy.deepcopy(currentPriority)
    else:
      # TODO: implement defaulting this branch to highest nice level, urgent=True, important=True, place in the backlog
      #       to make sure this issue gets immediate triage to the right priority and state.

  def __str__(self):
    """
    :return: Return a string representation of the class data
    """
    state = "taskId: {}, " \
            "currentKanbanColumn: {}, " \
            "currentKanbanColumns: {}, " \
            "priority: {}, " \
            "onHold: {}, " \
            "holdUntil: {}, " \
            "internalState: {}, " \
            "notesOnThisState: {}, " \
            "enteredThisStateTimestamp: {}, " \
            "targetCompletionTimestamp: {}, ".format(self.taskId,
                                                     self.currentKanbanColumn,
                                                     self.currentKanbanColumns,
                                                     self.priority,
                                                     self.onHold,
                                                     self.holdUntil,
                                                     self.notesOnThisState,
                                                     self.enteredThisStateTimestamp,
                                                     self.targetCompletionTimestamp)
      return state

  def __repr__(self):
    """
    :return: Return the data structure represented by this class
    """
    return {state:
              {"taskId": self.taskId,
               "currentKanbanColumn": self.currentKanbanColumn,
               "currentKanbanColumns": self.currentKanbanColumns,
               "priority": self.priority,
               "onHold": self.onHold,
               "holdUntil": self.holdUntil,
               "notesOnThisState": self.notesOnThisState,
               "enteredThisStateTimestamp": self.enteredThisStateTimestamp,
               "targetCompletionTimestamp": self.targetCompletionTimestamp}
            }

  def setTaskId(self, taskId=1):
    """
    :param taskId:
    :return:
    """
    # TODO: figure out how to set up autoindexing of task ID's in the state manager
    self.taskId = taskId

  def addKanbanColumn(self, kanbanColumn=""):
    """

    :param kanbanColumn:
    :return:
    """
    if isinstance(kanbanColumn, str):
      self.kanbanColumns.append(kanbanColumn)
    else:
      self.logger.log(lp.ERROR, "Type Error, this won't work...")
      self.logger.log(lp.ERROR, traceback.format_exc())
      raise TypeError

  def addKanbanColumns(self, kanbanColumns=[]):
    """

    :param kanbanColumns:
    :return:
    """
    if isinstance(kanbanColumn, str):
      self.kanbanColumns + kanbanColumns
    else:
      self.logger.log(lp.ERROR, "Type Error, this won't work...")
      self.logger.log(lp.ERROR, traceback.format_exc())
      raise TypeError

  def setKanbanColumns(self, kanbanColumns=[]):
    """

    :param kanbanColumns:
    :return:
    """
    if isinstance(kanbanColumn, str):
      self.kanbanColumns = kanbanColumns
    else:
      self.logger.log(lp.ERROR, "Type Error, this won't work...")
      self.logger.log(lp.ERROR, traceback.format_exc())
      raise TypeError

  def setNewCurrentPriority(self, newPriority={}):
    """

    :param currentPriority:
    :return:
    """
    self.currentPriority.setPriority(newPriority)

  def setOnHold(self, onHold=False):

    """

    :param onHold:
    :return:
    """
    self.onHold = onHold

  def setHoldUntil(self, holdUntil=""):
    """

    :param holdUntil:  Initial format of the DateTime string will be CCYY-MM-DD_HH-MM-SS, easily parseable
    :return:
    """
    self.holdUntil = holdUntil

  def setNotesOnThisState(self, notes=""):
    """

    :param notes:
    :return:
    """
    self.notesOnThisState = notes

  def setTargetCompletionTimestamp(self, targetCompletionTimestamp=""):
    """

    :param targetCompletionTimestamp:
    :return:
    """
    self.targetCompletionTimestamp = targetCompletionTimestamp

  def deleteKanbanColumn(self, kanbanColumn=""):
    """

    :param kanbanColumn:
    :return:
    """
    # TODO:
    pass

  def deleteKanbanColumns(self, kanbanColumns=[]):
    """

    :param kanbanColumns:
    :return:
    """
    # TODO:
    pass

  def getTaskId(self):
    """

    :return:
    """
    return self.taskId

  def getKanbanColumn(self):
    """

    :return:
    """
    return self.kanbanColumn

  def getKanbanColumns(self):
    """

    :return:
    """
    return self.kanbanColumns

  def getCurrentPriority(self):
    """

    :return:
    """
    return self.currentPriority

  def getOnHold(self):
    """

    :return:
    """
    return self.onHold

  def getHoldUntil(self):
    """

    :return:  Initial format of the DateTime string will be CCYY-MM-DD_HH-MM-SS, easily parseable
    """
    return self.holdUntil

  def getNotesOnThisState(self):
    """

    :return:
    """
    return self.notesOnThisState

  def getTargetCompletionTimestamp(self):
    """

    :return:  Initial format of the DateTime string will be CCYY-MM-DD_HH-MM-SS, easily parseable
    """
    return self.targetCompletionTimestamp

