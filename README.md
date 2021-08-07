# eisenban
productivity software - combining the Eisenhower Matrix and Kanban methodologies

Simple app for managing time

## Intended Design notes, thoughts, diagrams, etc

[eisenban design documentation](https://github.com/clockworksspheres/eisenban/blob/main/design/README.md)

## Data Model

Considering a data structure model something like:

```
{
     {
         task: {id: "", 
                title: "", 
                description: "", 
                creationTimestamp: "", 
                initialTargetCompletionTimestamp: ""
                },
     }
     {
         state: {task: {id: "", title: ""}, 
                notes: "", 
                priority: {}, 
                kanbanColumns: [backLog, inProgress, done, hold, delegated], 
                currentState: ""
                holdUntil: "", 
                holdNotes: "", 
                targetCompletionTimestamp: ""
                }
     }
     {
         priority: {niceLvl: "", 
                    urgent: bool, 
                    important: bool,
                    priorityNotes: ""
                    }
     }
     {
         move: {task: {id: "", 
                       title: ""
                       }, 
                fromState: {}, 
                toState: {}, 
                moveTimestamp: ""
                }
     }

}
```

parent template to be created that will provide default handlers for each piece of data for whether that data is included in processing or not.

# References:

## References describing the Eisenhower Matrix:

* [Eisenhower Matrix: How to Prioritise and Master Productivity](https://www.techtello.com/eisenhower-productivity-matrix/)
* [The Eisenhower Matrix](https://todoist.com/productivity-methods/eisenhower-matrix)
* [How to overcome procrastination with the Eisenhower matrix](https://www.lucidchart.com/blog/eisenhower-matrix)
* [Implementing the Eisenhower Matrix in Evernote](https://filterize.net/blog/using-filterize/eisenhower-matrix/)

## References describing Kanban:

* [Kanban (development)](https://en.wikipedia.org/wiki/Kanban_(development))
* [What is Kanban?](https://www.digite.com/kanban/what-is-kanban/)
* [Introduction to Kanban](https://www.planview.com/resources/guide/introduction-to-kanban/)


## a few other github personal kanban projects

* [https://github.com/MrChuckomo/kanban_tkinter](https://github.com/MrChuckomo/kanban_tkinter)
* [https://github.com/kitplummer/clikan](https://github.com/kitplummer/clikan)
* [https://github.com/piooca/cli-kanban1.git](https://github.com/piooca/cli-kanban1.git)
* [https://github.com/bmulobi/bc-15-KanBan-CLI-project.git](https://github.com/bmulobi/bc-15-KanBan-CLI-project.git)
* [https://github.com/timhemel/clikb](https://github.com/timhemel/clikb)
* [https://github.com/WesleyWWhelan/KanbanBoard](https://github.com/WesleyWWhelan/KanbanBoard)
* [https://github.com/Saizzou/Kanban_PyQt5](https://github.com/Saizzou/Kanban_PyQt5)

## a few other personal eisenhower matrix projects

* [https://github.com/LakithKarunaratne/Eisenhower](https://github.com/LakithKarunaratne/Eisenhower)
* [https://github.com/Lleafll/eisenhower](https://github.com/Lleafll/eisenhower)
* [https://github.com/Ghalko/ironChart](https://github.com/Ghalko/ironChart)
* [https://github.com/maciek-nowak/eisenhower-matrix](https://github.com/maciek-nowak/eisenhower-matrix)
* [https://github.com/sthompson232/Eisenhowers-Quadrant](https://github.com/sthompson232/Eisenhowers-Quadrant)

