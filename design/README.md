# Design notes

# WARNING

1. This directory is intended to be used as a loose ideas of future direction for the project.

2. The further the modification date of this file is from the current date - the less likely these file match the actual details of the design.  Design changes are often made to released software projects (in general) where design documents may not be updated or curated.

## Purpose

Purpose of this directory is to record design decisions, backround perspectives, editors and tools used throughout the
design, architecture, implementation, test, promotion, production, documentation and maintenance of this software system.

## Model View Controller(MVC) conversion to Model View State Machine(MVSM)

This project, in combination with the learning-and-research-accellerator projects helped morph the design method or
terminoligy used for new clockworksspheres projects re-defining the "controller" as a "state manager".  The "state
manager" includes what I call an Interface, Queue, Dispatcher(IQD).  The "state Management" section will manage the
state of the model as well as recording state changes, while the IQD provides a code or object interface and control
of the software system.

## State Management Engine

The intention is to record all state changes and actions, so the data can be mined for future planning
improvements by the user.  Tasks can be either archived, or deleted, but messing with a "revert"
function is against the purpose of working on continuous improvement as well as transparency, therefore
to be avoided at all costs.

The State Management Engine will attempt to abstract the idea of state change, so it can be replicated for multiple 
projects.

The State Management Engine will abstract the notion of state such that an instruction to change state can be given to
the state management engine, without actually changing the data in a dynamic model.  If this framework is successful,
it can be pulled out and plopped down in other projects, and used directly without any required modification to the
project it is plopped down into.

Possibly considering a factory object, but likely going to approach a simpler object or pattern first.

## CRUD Store Engine

CRUD is an old computer science term to abstract the following storage paradigm:

* Create
* Read
* Update
* Delete

This can be applied to both SQL databases and REST web interfaces.  One can consider CSV and plain text files
as well.

The eisenban project will prototype this kind of factory based model to be duplicated and re-used
in future projects like the learning-and-research-accellerator project.

### Comparing CRUD to SQL terminology

| CRUD | SQL |
|---|---|
| Create | Insert |
| Read | Select |
| Update | Update |
| Delete | Delete |

### Comparing CRUD to REST technology

| CRUD | REST |
|---|---|
| Create | POST |
| Read | GET |
| Update | PUT |
| Delete | DELETE |




### Wish List of Actions to be implemented by the State Management System and IQD

#### Create

* New Task + New State + New Priorty + Target DateTime
* New State + New Priority + Target DateTime
* New Priority + Target DateTime
* Start New Task List/DB/File

#### Change

* Change State
* Change Priority
* Change State and Priority
* Change State and Priority and TargetDateTime
* Change Target DateTime

#### Backup

#### Retire

* Delete Task
* Archive Task
* Delete File
* Archive File
* Delete Db
* Archive Db

#### Present Model info in Dict form to Software Interface (could be view, could be plugin, could be inter-app comms) 

* Return Dict to View interface
  - entire list
  - task
  - list of tasks in kanban column
  - list of tasks in eisenhower matrix section
  - few more combinations of the above
  - table data struct for kanban view
  - table data struct for Eisenhower Matrix view
  - by DateTime

#### Potential Plugins, or interactions with other apps

* Plugin or I/O interface 
  - Print/Send/Notify/timer/calendar Task (provide middleware interface that plugins providers can butt up to)
  - Task History
  - Current State
  - Task History Range
  - iCal Target Dates, Meetings, 
  - Timer/Timer Schedule
  - Reminders/Reminders Schedule
  - send a view dict to one of the Plugin or I/O mechanisms 
  
## Utilities used:

My personal preference is to use locally installed apps for design works, as I take my dev machine with me places, and do not always have internet to access internet based web applications for design work.  These applications can all be installed locally, although some can be available via internet services.

### UML

| Tool | Description | Project link | Tutorials | Windows package sources | macOS package sources | Linux package sources | Source code Repository |
----- | ----- | ----- | ----- | ----- | ----- | ----- | -----
| Umbrello  | KDE hosted UML project | https://umbrello.kde.org/  | https://umbrello.kde.org/documentation.php  | https://community.chocolatey.org/packages/umbrello | https://invent.kde.org/packaging/homebrew-kdebrew | https://snapcraft.io/umbrello | https://github.com/KDE/umbrello |
| drawio | diagram builder | https://www.diagrams.net/ | https://drawio-app.com/tutorials/ | https://community.chocolatey.org/packages/drawio | https://formulae.brew.sh/cask/drawio | https://snapcraft.io/drawio | https://github.com/jgraph/drawio-desktop |

### Python editors
| Tool | Description | Project link | Tutorials | Windows package sources | macOS package sources | Linux package sources |
----- | ----- | ----- | ----- | ----- | ----- | -----
| pycharm  | IDE for Python programming | https://www.jetbrains.com/pycharm/ |  | choco install pycharm-community | https://formulae.brew.sh/cask/pycharm-ce | | | 
| geany | Geany is a powerful, stable and lightweight programmer's text editor that provides tons of useful features without bogging down your workflow. | https://www.geany.org/ |  | https://community.chocolatey.org/packages/geany | https://formulae.brew.sh/cask/geany |  |
| eclipse |  |  |  |

### .md files

| Tool | Description | Project link | Tutorials | Windows package sources | macOS package sources | Linux package sources |
----- | ----- | ----- | ----- | ----- | ----- | -----
| Vim  |  |  | 
| Intellij Idea |  |  |  |

### State Diagrams

| Tool | Description | Project link | Tutorials | Windows package sources | macOS package sources | Linux package sources |
----- | ----- | ----- | ----- | ----- | ----- | -----
| drawio | diagram builder | https://www.diagrams.net/ | https://drawio-app.com/tutorials/ | https://community.chocolatey.org/packages/drawio | https://formulae.brew.sh/cask/drawio | https://snapcraft.io/drawio | https://github.com/jgraph/drawio-desktop |

## Personal git server

| Tool | Description | Project link | Tutorials | Windows package sources | macOS package sources | Linux package sources |
----- | ----- | ----- | ----- | ----- | ----- | -----
| gogs | Personal git server | https://github.com/gogs/gogs | | | |

### 

