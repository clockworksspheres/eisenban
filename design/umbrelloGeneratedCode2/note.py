from attachments import *
from stateChange import *

class note(object):

  """
  :version:
  :author:
  """

  """ ATTRIBUTES

   Single word or short string


  title  (private)

  note  (private)

  attachment  (private)

  longNote  (private)

  atomic_task_id  (private)

  """

  def getAtomicTaskId(self, atomic_task_id):
    """
     

    @param atomic_uuid atomic_task_id : 
    @return atomic_uuid :
    @author
    """
    return self.atomic_task_id


  def setAtomicTaskId(self, atomic_task_id):
    """
     

    @param atomic_uuid atomic_task_id : 
    @return atomic_uuid :
    @author
    """
    pass

  def setTitle(self, title):
    """
     

    @param  title : 
    @return string :
    @author
    """
    pass

  def getDescription(self, description):
    """
     

    @param string description : 
    @return string :
    @author
    """
    return self.description


  def getTitle(self, title):
    """
     

    @param string title : 
    @return string :
    @author
    """
    return self.title


  def setNote(self, note = ""):
    """
     

    @param string note : 
    @return string :
    @author
    """
    pass

  def getNote(self, getNote):
    """
     

    @param string getNote : 
    @return string :
    @author
    """
    pass

  def setAttachment(self, attachment):
    """
     

    @param attachments attachment : 
    @return attachments :
    @author
    """
    pass

  def getLongNote(self, longNote):
    """
     

    @param string longNote : 
    @return stateChange :
    @author
    """
    pass

  def getAttachment(self, attachment):
    """
     

    @param attachments attachment : 
    @return attachments :
    @author
    """
    return self.attachment




