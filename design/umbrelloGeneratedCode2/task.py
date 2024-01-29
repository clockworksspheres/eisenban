from **kwargs import *
from state import *
from note import *

class task(object):

  """
  :version:
  :author:
  """

  """ ATTRIBUTES

  title  (private)

  taskId  (private)

  creationTimeStamp  (private)

  initialTargetCompletionTimestamp  (private)

  currentState  (private)

  description  (private)

  currentTargetCompletionTimestamp  (private)

  atomic_task_id  (private)

  taskNote  (private)

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
    


  def set(self, _kwargs):
    """
     

    @param **kwargs _kwargs : 
    @return **kwargs :
    @author
    """
    
         verifyingInputList [ title, 
                taskId, 
                creationTimeStamp, 
                initialTargetCreationTimeStamp, 
                currentState, 
                description, 
                currentTargetCompletionTimestamp, 
                atomic_task_id, 
                taskNote ]
     
        if "serviceName" in kwargs && in verifyingInputList:
                self.servicename = kwargs.get("serviceName")
            elif "servicename" in kwargs:
                self.servicename = kwargs.get("servicename")
            else:
                self.servicename = ""
    


  def get(self, _kwargs):
    """
     

    @param **kwargs _kwargs : 
    @return **kwargs :
    @author
    """
    pass



