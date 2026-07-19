#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

echo "----------===== ### =====----------"
echo " ### starting RHEL based build ###"

pushd ..

directory="./projEnv"
actfile="$directory/bin/activate"
if [ ! -d "$directory" ]  || [ ! -f "$actfile" ] ; then

   sudo dnf install python3-tk

   python3 -m venv $directory
   source $actfile

   pip install -r requirements.txt

else
   source $actfile
fi


cp BuildScripts/build.linux.py313.onefile.spec eisenban/build.linux.py313.onefile.spec

pushd eisenban

pyinstaller --clean -y build.linux.py313.onefile.spec
pyinstaller -y build.linux.py313.onefile.spec

rm build.linux.py313.onefile.spec

sudo cp -a dist/eisenban /usr/local/bin

popd
popd

