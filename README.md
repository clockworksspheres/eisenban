 This is a fork of the Kanbaru project which can be found here:

[Kanbaru](https://github.com/dulapahv/Kanbaru)

[Kanbaru License](https://github.com/dulapahv/Kanbaru/blob/main/LICENSE)

A Kanban-style, list-making project management application that helps you organize and visualize your tasks efficiently and effectively.

Eisenban is a re-branded version of Kanbaru, as the Kanbaru project is frozen and no longer developed.

Eisenban is short for Eisenhower method Kanban board.  The Eisenhower method has not yet been integrated into the project.

## FAQ: 

### Q: Drag and drop isn't working on Linux

_A._ Short answer:  If one is having trouble with drag and drop on Linux, it's likely a Wayland problem - one needs to set:  
  
export QT_QPA_PLATFORM=xcb  
  
in their ~/.bashrc (or similar shell config) or run the script/program with  
  
QT_QPA_PLATFORM=xcp <​script/program> <​script/program-options>  
  
for the app to work

Long answer: [[dragNdropProblemsOnLinux]]

