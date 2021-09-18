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

### Controller core

For this app, the controller/state engine tells the model to change state, passes in the current state and the "next"
state, sends the data to either a decoupled state manager, or the model, that containes its own state manager to manage
the dynamic state of the data in memory.

This way, the controller doesn't have to know the details of the model to make the state change, and the model can be completely decoupled from the controller.  The controller or state
engine then becomes a traffic cop, or train station switching hub, between view, model, devices and API's (like REST)

For those familiar with older chipsets - the controller then becomes something like a north bridge, directing data
traffic to the different app compnents, or sub components, with instructions on what it expects to be done with that
data.

Each section in the app, such as Model and View, then become like a device off the north bridge - that take the data
and the instructions and perform the expected action.

### the Model device

The Model device, takes the data, has a "model controller" to handle how dynamic data is manimpulated.


State

S1 = State One
S2 = State Two
P1 = Priority One
P2 = Priority Two

For the type of data in this model
S1P1 -> S2P1 -> Slog
S1P1 -> S2P2 -> Slog -> Plog
S1P1 -> S1P2 -> Plog

S1P1 -> S


### the View device

The View device, takes the data, has a "view controller" to handle how dynamic data is presented to a user.

### the API device

The API device, takes the data, has an "API controller" to handle how dynamic data is presented to an API, like a
REST interface, or a plugin type interface.

### the CRUD device

The CRUD device, takes the data, has a "storage controller" to handle how dynamic data is stored on non-volitile
storage.  This could be in the form of a CSV, YAML, JSON files, or into a database.  The first three just have
filesystem interaction, while the CRUD device controller will need to have a database driver or hook to write to
a database, like SQL or NOSQL type database.  Perhaps the SQL driver(s) may include mysql, mariadb, postgres, oracle,
mssql, and the NOSQL controller could perform similarly for those types of database interactions.


### printers??

Not sure yet where to put printers, probably categorize them as a view, as it is a presentation of the dynamic data
at the time of the print.










## CRUD Store controller

CRUD is an old computer science term to abstract the following storage paradigm:

* Create
* Read
* Update
* Delete

This can be applied to both SQL databases and REST web interfaces.  One can consider CSV and plain text files
as well.

The eisenban project will prototype this kind of factory based model to be duplicated and re-used
in future projects like the learning-and-research-accellerator project.

### crudInMemInstanceEngine.py 

This inherits the crudStoreEngine.py, and is specific to modifying the instance data store in memory, that has already
been loaded, or is being created.  

## API device controller

Comparing CRUD to SQL terminology

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

## State Management device

The intention is to record all state changes and actions, so the data can be mined for future planning
improvements by the user.  Tasks can be either archived, or deleted, but messing with a "revert"
function is against the purpose of working on continuous improvement as well as transparency, therefore
to be avoided at all costs.

The State Management device will attempt to abstract the idea of state change.  This device may be specific to the
data in the model, so it may only be able to be used as a reference for other state management devices for other
projects, rather than be used directly in multiple projects.




### Wish List of instructions to be implemented by the Controller core - and directed to the right device

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
  - Current Statek h]
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

