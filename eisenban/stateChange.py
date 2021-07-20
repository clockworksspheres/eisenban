from state import *

class stateChange(object):

  """
  :version:
  :author:
  """

  """ ATTRIBUTES

  taskId  (private)

  fromState  (private)

  changeTimeStamp  (private)

  toState  (private)

  """

  def getCurrentState(self):
    """
     

    @return state :
    @author
    """
    pass

  def getStateRange(self, from = 0, toState = 0):
    """
     

    @param signed long int from : 
    @param signed long int toState : 
    @return array :
    @author
    """
    pass

  def getCompleteStateRange(self):
    """
     

    @return array :
    @author
    """
    pass

  def getLastState(self):
    """
     

    @return state :
    @author
    """
    pass

  def getStateMinusN(self, stateNumber = 0):
    """
     

    @param double stateNumber : 
    @return  :
    @author
    """
    pass

  def getFirstState(self):
    """
     

    @return state :
    @author
    """
    pass

  def setNewState(self, taskId = 0, fromState = {}, toState = {}):
    """
     

    @param double taskId : 
    @param dict fromState : 
    @param dict toState : 
    @return  :
    @author
    """
    pass

  def getChangeTimeStamp(self, taskId = 0, fromState = {}, toState = {}):
    """
     

    @param double taskId : 
    @param dict fromState : 
    @param dict toState : 
    @return  :
    @author
    """
    pass



