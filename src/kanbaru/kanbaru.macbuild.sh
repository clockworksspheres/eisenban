#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

#if doesn't exist...
# python3 -m venv temp
# source temp/bin/activate

# pip3 install python6
# pip3 install pyinstaller
# pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib

pyinstaller --clean -y kanbaru.macos.spec
pyinstaller -y kanbaru.macos.spec
#cp -a resources dist/kanbaru.app/Contents/MacOS
cp -a resources dist/kanbaru.app/Contents/Resources



