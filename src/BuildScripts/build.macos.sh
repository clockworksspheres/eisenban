#!/bin/bash

# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-pyinstaller-macos-dmg/
# amoung others... including
# https://pyinstaller.org/en/stable/

#export PYENV_ROOT="$HOME/.pyenv"
#export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
#eval "$(pyenv init -)"

#pyenv global 3.11
#python --version

echo "----------===== ### =====----------"
echo " ### starting macOS based build ###"

pushd ..

directory="./projEnv"
actfile="$directory/bin/activate"
if [ ! -d "$directory" ]  || [ ! -f "$actfile" ] ; then
   python3 -m venv $directory
   source $actfile

   pip install -r requirements.txt

else
   source $actfile
fi
export PATH=".":$PATH
###
# DOES NOT WORK - need to figure out why...
#./gen_qrc-0.0.3.py

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

