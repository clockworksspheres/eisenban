from state import *

class task(object):

  """
  :version:
  :author:
  """

  """ ATTRIBUTES

  title  (private)

  id  (private)

  creationTimeStamp  (private)

  initialTargetCompletionTimestamp  (private)

  currentState  (private)

  description  (private)

  currentTargetCompletionTimestamp  (private)

  """

  def __init__(self, title = "", taskId = "", creationTimeStamp = "", initialTargetCompletionTimestamp = "", currentState = "", description = ""):
    """
     Class initialization method

    @param string title : 
    @param string taskId : 
    @param string creationTimeStamp : 
    @param string initialTargetCompletionTimestamp : 
    @param string currentState : 
    @param string description : 
    @return  :
    @author
    """
    self.title = title
    self.taskid = taskid
    self.creationTimestamp = creationTimestamp
    self.initialTargetCompletionTimestamp = initialTargetCompletionTimestamp
    self.currentTargetCompletionTimestamp = initialTargetCompletionTimestamp
    self.currentState = currentState
    self.description = description
    


  def setTitle(self, title):
    """
     Set the title to a passed in value

    @param string title : 
    @return  :
    @author
    """
    self.title = title


  def setTaskId(self, taskId = ""):
    """
     Setter for the task id

    @param string taskId : 
    @return string :
    @author
    """
    self.taskId = taskId


  def setDescription(self, description):
    """
     Set the description to a passed in value

    @param string description : 
    @return  :
    @author
    """
    self.description = description


  def setInitialCompletionTimestamp(self, initialCompletionTimestamp):
    """
     Set the initial completion timestamp - for when the intended target completion
     time is.

    @param string initialCompletionTimestamp : 
    @return  :
    @author
    """
    self.initialCompletionTimestamp = initialCompletionTimestamp


  def setCurrentCompletionTimestamp(self, currentCompletionTimestamp = ""):
    """
     Setter for the current completion timestamp attribute of the class

    @param string currentCompletionTimestamp : 
    @return string :
    @author
    """
    self.currentCompletionTimestamp = currentCompletionTimestamp


  def getTaskId(self):
    """
     Return the current value of the task id

    @return string :
    @author
    """
    return self.taskid


  def getTitle(self):
    """
     Getter for the title attribute of the class

    @return string :
    @author
    """
    return self.title


  def getDescription(self):
    """
     Getter for the description attribute of the class

    @return string :
    @author
    """
    return self.description


  def getCreationTimestamp(self):
    """
     Getter for the creation timestamp attribute of the class

    @return string :
    @author
    """
    return self.creationTimestamp


  def getInitialTargetCompletionTimestamp(self):
    """
     Getter for the initial Target Completion Timestamp

    @return string :
    @author
    """
    return self.initialTargetCompletionTimestamp


  def getCurrentCompletionTimestamp(self):
    """
     Getter for the current completion timestamp attribute of the class

    @return string :
    @author
    """
    return self.currentCompletionTimestamp




