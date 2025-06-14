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

fi
source ./packenv/bin/activate

pip3 install PySide6 PyInstaller
pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib


pyinstaller --clean -y eisenbuild.linux.py312.onefile.spec
pyinstaller -y eisenbuild.linux.py312.onefile.spec

sudo cp -a dist/eisenban /usr/local/bin


