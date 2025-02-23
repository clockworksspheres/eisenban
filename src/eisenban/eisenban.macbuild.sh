#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

#if doesn't exist...
# python3 -m venv temp
# source temp/bin/activate

# pip3 install PySide6 PyInstaller
# pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib

pyinstaller --clean -y eisenban.macos.spec
pyinstaller -y eisenban.macos.spec
#cp -a resources dist/eisenban.app/Contents/MacOS
cp -a resources dist/eisenban.app/Contents/Resources



