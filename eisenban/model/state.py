import copy
import traceback

from priority import *

class state(priority):

  """
  :version:
  :author:
  """

  """ ATTRIBUTES

  taskId  (private)

  notesOnThisState  (private)

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
      self.notesOnThisNewState = notesOnThisNewState
    else:
      self.notesOnThisNewState = ""

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

    self.enteredThisStateTimestamp = getCurrentDateTimeStamp()

    if isinstance(targetCompletionTimestamp, str):
      self.targetCompletionTimestamp = targetCompletionTimestamp
    else:
      self.targetCompletionTimestamp = ""

    if isinstance(currentPriority, priority):
      self.currentPriority = copy.deepcopy(currentPriority)
    else:
      # TODO: implement defaulting this branch to highest nice level, urgent=True, important=True, place in the backlog
      #       to make sure this issue gets immediate triage to the right priority and state.





# TODO: use below as templates for getters and setters, etc of the state object's class properties.

  def setNiceLevel(self, newNiceLevel=0):
    """
     Acts as unix "nice" levels for processes, range -20 to 20.  Using that as it is
     familiar to systems programmers and *nix admins, and any student that has
     operated in a unix environment.

    @param short int newNiceLevel :
    @return  :
    @author : Roy Nielsen
    """
    if isinstance(newNiceLevel, int) and newNiceLevel < 20 and newNiceLevel > -20:
      self.niceLevel = newNiceLevel
    else:
      self.niceLevel = 0

  def setImportant(self, important=True):
    """
     Set the Eisenhower matrix "important" attribute to the priority.  Default "True"

    @param bool important :
    @return  :
    @author : Roy Nielsen
    """
    if isinstance(important, bool):
      self.important = important
    else:
      self.important = True

  def setUrgent(self, urgent=True):
    """
     Set the Eisenhower matrix attribute "Urgent".  Bool, default True

    @param bool urgent :
    @return  :
    @author : Roy Nielsen
    """
    if isinstance(urgent, bool):
      self.urgent = urgent
    else:
      self.urgent = True

  def setPrioityNotes(self, priorityNotes=""):
    """
     Not required - notes on why the current priority was chosen.  Default is an
     empty string.

    @param string priorityNotes :
    @return  :
    @author : Roy Nielsen
    """
    if isinstance(priorityNotes, str):
      self.priorityNotes = priorityNotes
    else:
      priorityNotes = ""

  def getNiceLevel(self, niceLevel=0):
    """
     Return the nice level of this priority.

    @param signed int niceLevel :
    @return string :
    @author : Roy Nielsen
    """
    return self.niceLevel

  def getImportant(self, important=True):
    """
     Return the Esienhower matrix "Important" value.

    @param bool important :
    @return bool :
    @author : Roy Nielsen
    """
    return self.important

  def getUrgent(self, urgent=True):
    """
     Return the Eisenhower matrix value bool.

    @param bool urgent :
    @return bool :
    @author : Roy Nielsen
    """
    return self.urgent

  def getPriorityNotes(self, priorityNotes=""):
    """


    @param string priorityNotes :
    @return string :
    @author : Roy Nielsen
    """
    return self.priorityNotes

    def __str__(self):
      """
      :return: Return a string representation of the class data
      """
      return "niceLvl: {}, urgent: {}, important: {}, priorityNotes: {}".format(self.niceLevel, self.urgent,
                                                                                self.important, self.priorityNotes)

    def __repr__(self):
      """
      :return: Return the data structure represented by this class
      """
      return {priority:
                {"niceLvl": self.niceLevel,
                 "urgent": self.urgent,
                 "important": self.important,
                 "priorityNotes": self.priorityNotes}
              }


