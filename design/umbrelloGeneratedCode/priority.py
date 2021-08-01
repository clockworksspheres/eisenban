
class priority(object):

  """
  :version:
  :author:
  """

  """ ATTRIBUTES

  niceLvl  (private)

  urgent  (private)

  important  (private)

  priorityNotes  (private)

  """

  def __init__(self, niceLevel = 0, urgent = True, important = True, priorityNotes = ""):
    """
     

    @param signed int niceLevel : 
    @param bool urgent : 
    @param bool important : 
    @param string priorityNotes : 
    @return  :
    @author
    """
    pass

  def setNiceLevel(self, newNiceLevel = 0):
    """
     Acts as unix "nice" levels for processes, range -20 to 20.  Using that as it is
     familiar to systems programmers and *nix admins, and any student that has
     operated in a unix environment.

    @param short int newNiceLevel : 
    @return  :
    @author
    """
    pass

  def setImportant(self, important = True):
    """
     Set the Eisenhower matrix "important" attribute to the priority.  Default "True"

    @param bool important : 
    @return  :
    @author
    """
    pass

  def setUrgent(self, urgent = True):
    """
     Set the Eisenhower matrix attribute "Urgent".  Bool, default True

    @param bool urgent : 
    @return  :
    @author
    """
    pass

  def setPrioityNotes(self, priorityNotes = ""):
    """
     Not required - notes on why the current priority was chosen.  Default is an
     empty string.

    @param string priorityNotes : 
    @return  :
    @author
    """
    pass

  def getNiceLevel(self, niceLevel = 0):
    """
     Return the nice level of this priority.

    @param signed int niceLevel : 
    @return string :
    @author
    """
    pass

  def getImportant(self, important = True):
    """
     Return the Esienhower matrix "Important" value.

    @param bool important : 
    @return bool :
    @author
    """
    pass

  def getUrgent(self, urgent = True):
    """
     Return the Eisenhower matrix value bool.

    @param bool urgent : 
    @return bool :
    @author
    """
    pass

  def getPriorityNotes(self, priorityNotes = ""):
    """
     

    @param string priorityNotes : 
    @return string :
    @author
    """
    pass



