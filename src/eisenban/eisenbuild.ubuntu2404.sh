#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

#if doesn't the packenv directory doesn't exist...

directory="./packenv"
actfile="./packenv/bin/activate"
if [ ! -d "$directory" ]  || [ ! -f "$actfile" ] ; then
   python3 -m venv packenv
   source packenv/bin/activate

   pip3 install PySide6 PyInstaller
   pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib
else
   source packenv/bin/activate
fi

pyinstaller --clean -y eisenbuild.linux.onefile.spec
pyinstaller -y eisenbuild.linux.py312.onefile.spec
#cp -a resources dist/eisenban.app/Contents/MacOS
#cp -a resources dist/eisenban.app/Contents/Resources



