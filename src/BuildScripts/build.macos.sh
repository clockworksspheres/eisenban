#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

#if doesn't the packenv directory doesn't exist...

pushd ..

directory="./packenv"
actfile="./packenv/bin/activate"
if [ ! -d "$directory" ]  || [ ! -f "$actfile" ] ; then

   brew install python-tk
   python -m venv packenv
   source packenv/bin/activate
   pip install --upgrade pip
   pip install firebase-admin
   pip install pyside6
   pip install pyinstaller
   # pip install --force-reinstall --no-cache-dir Tk
   # pip install --force-reinstall --no-cache-dir PyInstaller
   # pip install --upgrade PyInstaller pyinstaller-hooks-contrib
else
   source packenv/bin/activate
fi
export PATH=".":$PATH
###
# DOES NOT WORK - need to figure out why...
#./gen_qrc-0.0.3.py

#pyside6-rcc eisenban.qrc -o eisenban_rc.py

# pushd ui; python3 compile_uifiles.py; popd

cp BuildScripts/build.macos.spec eisenban

pushd eisenban

#pushd ui; python3 compile_uifiles.py; popd

echo "----- start pyinstaller --clean -y eisenbuild.macos.spec -----"
pyinstaller --clean -y build.macos.spec
echo "----- end pyinstaller --clean -y eisenbuild.macos.spec -----"
echo " ===== start pyinstaller -y eisenbuild.macos.spec ====="
pyinstaller -y build.macos.spec
rm build.macos.spec
echo "===== end pyinstaller -y eisenbuild.macos.spec ====="
### DOES NOT WORK... need to figure out why...
cp -a resources dist/eisenban.app/Contents/Resources
cp -a resources dist/eisenban.app/Contents
cp -a dist/eisenban.app ~/Desktop
open ~/Desktop/eisenban.app

popd
popd

