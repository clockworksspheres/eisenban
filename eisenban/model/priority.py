
import traceback


class Priority(object):

  """
  :version: 0.1
  :author: Roy Nielsen

  ATTRIBUTES

  The priority data structure has the following layout: 

  niceLevel: Similar to the *nix "nice command" where the lower (even negative) priority, the more important this is.

  urgent:  True or False, per the Eisenhower Productivity Matrix

  important:  True or False, per the Eisenhower Productivity Matrix

  priorityNotes: Any kind of note that needs to be recorded due to a priority assignment or change.

  References to definitions and usage of a Eisenhower Productivity Matrix:
    * [Eisenhower Matrix: How to Prioritise and Master Productivity](https://www.techtello.com/eisenhower-productivity-matrix/)
    * [The Eisenhower Matrix](https://todoist.com/productivity-methods/eisenhower-matrix)
    * [How to overcome procrastination with the Eisenhower matrix](https://www.lucidchart.com/blog/eisenhower-matrix)
    * [Implementing the Eisenhower Matrix in Evernote](https://filterize.net/blog/using-filterize/eisenhower-matrix/)

  References to other Eisenhower Productivity Matrix projects on Github:
    * [https://github.com/LakithKarunaratne/Eisenhower](https://github.com/LakithKarunaratne/Eisenhower)
    * [https://github.com/Lleafll/eisenhower](https://github.com/Lleafll/eisenhower)
    * [https://github.com/Ghalko/ironChart](https://github.com/Ghalko/ironChart)
    * [https://github.com/maciek-nowak/eisenhower-matrix](https://github.com/maciek-nowak/eisenhower-matrix)
    * [https://github.com/sthompson232/Eisenhowers-Quadrant](https://github.com/sthompson232/Eisenhowers-Quadrant)

  """

  def __init__(self, niceLevel = 0, urgent = True, important = True, priorityNotes = ""):
    """
     

    @param signed int niceLevel : 
    @param bool urgent : 
    @param bool important : 
    @param string priorityNotes : 
    @return  :
    @author : Roy Nielsen
    """
    if isinstance(niceLevel, int) and niceLevel < 20 and niceLevel > -20:
      self.niceLevel = niceLevel
    else:
      self.niceLevel = 0

    if isinstance(urgent, bool):
      self.urgent = urgent
    else:
      self.urgent = True

    if isinstance(important, bool):
      self.important = important
    else:
      self.important = True

    if isinstance(priorityNotes, str):
      self.priorityNotes = priorityNotes
    else:
      priorityNotes = ""

  def setNiceLevel(self, newNiceLevel = 0):
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

  def setImportant(self, important = True):
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

  def setUrgent(self, urgent = True):
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

  def setPrioityNotes(self, priorityNotes = ""):
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

  def getNiceLevel(self, niceLevel = 0):
    """
     Return the nice level of this priority.

    @param signed int niceLevel : 
    @return string :
    @author : Roy Nielsen
    """
    return self.niceLevel

  def getImportant(self, important = True):
    """
     Return the Esienhower matrix "Important" value.

    @param bool important : 
    @return bool :
    @author : Roy Nielsen
    """
    return self.important

  def getUrgent(self, urgent = True):
    """
     Return the Eisenhower matrix value bool.

    @param bool urgent : 
    @return bool :
    @author : Roy Nielsen
    """
    return self.urgent

  def getPriorityNotes(self, priorityNotes = ""):
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
      return "niceLvl: {}, urgent: {}, important: {}, priorityNotes: {}".format(self.niceLevel, self.urgent, self.important, self.priorityNotes)

    def __repr__(self):
      """
      :return: Return the data structure represented by this class
      """
      return {priority:
                { "niceLvl": self.niceLevel,
                  "urgent": self.urgent,
                  "important": self.important,
                  "priorityNotes": self.priorityNotes }
             }
