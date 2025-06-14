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
   pip3 install --upgrade pip

   pip3 install PySide6 PyInstaller
   pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib
else
   source packenv/bin/activate
fi
export PATH=".":$PATH
###
# DOES NOT WORK - need to figure out why...
#./gen_qrc-0.0.3.py

#pyside6-rcc eisenban.qrc -o eisenban_rc.py

pushd ui; python3 compile_uifiles.py; popd

pyinstaller --clean -y eisenbuild.macos.onefile.spec
pyinstaller -y eisenbuild.macos.onefile.spec
### DOES NOT WORK... need to figure out why...
cp -a dist/eisenban ~/Desktop
open ~/Desktop/eisenban



