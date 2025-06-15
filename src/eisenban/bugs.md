# Bugs that cannot be logged via the eisenboard

Non-functioning, known GUI problems


## Linux bugs - can't move cards, 

1. Found by running onefile, trying to move a card from one column to another
  *  indexing not working
  *  not writing changes to the file
```
$ dist/eisenban -t eisenboard
Starting Eisenban...
Current directory: "/tmp/_MEIrdqxrM"
dbdir detected
Reading table file...
Loaded 1 board
+--"eisenban" [4 panels]
|   +--"todo" [2 cards]
|   |   +--"File menu"
|   |   +--"Board menu"
|   +--"shelve" [1 card]
|   |   +--"multiple instances on macos for eisenban.app"
|   +--"done" [0 card]
|   +--"research" [1 card]
|   |   +--"menu system"
Table read from the table file
Table path: "eisenboard/Table.pickle"
Table instance initialized and read successfully
Going to main screen...
Moving 1 Card (['Board menu']) from panel "todo" to panel "todo"
Moved card "Board menu" to index=1
todo
Table written to the table file
Moving 1 Card (['Board menu']) from panel "todo" to panel "todo"
Moved card "Board menu" to index=1
todo
Table written to the table file
```
