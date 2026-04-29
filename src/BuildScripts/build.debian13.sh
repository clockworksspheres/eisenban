#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

pushd ..

#if doesn't the packenv directory doesn't exist...
directory="./packenv"
actfile="./packenv/bin/activate"
if [ ! -d "$directory" ]  || [ ! -f "$actfile" ] ; then

   sudo apt install python3-tk
   python -m venv packenv
   source packenv/bin/activate
   pip install --upgrade pip
   pip install astroid
   pip install pylint
   pip install pytest
   pip install pyside6
   pip install pyinstaller
   # pip3 install PySide6 PyInstaller
   # pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib

else
   source packenv/bin/activate
fi
source ./packenv/bin/activate


cp BuildScripts/build.linux.py313.onefile.spec eisenban/build.linux.py313.onefile.spec

pushd eisenban

pyinstaller --clean -y build.linux.py313.onefile.spec
pyinstaller -y build.linux.py313.onefile.spec

rm build.linux.py313.onefile.spec

sudo cp -a dist/eisenban /usr/local/bin

popd
popd

