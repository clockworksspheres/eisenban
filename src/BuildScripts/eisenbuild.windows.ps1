# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/
# amoung others... including
# https://pyinstaller.org/en/stable/

# before script is run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# powershell -File ".\eisenban.windows.ps1"

pushd ..


$FolderPath = ".\packenv"
if (!(Test-Path -Path $FolderPath -PathType Container)) {
   
   python3 -m venv packenv
   .\packenv\Scripts\Activate.ps1

   pip install --upgrade pip
   pip install firebase-admin   
   pip3 install PySide6 
   pip3 install PyInstaller
   # pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib

} else {
    .\packenv\Scripts\Activate.ps1
}

cp BuildScripts/eisenbuild.windows11.onefile.spec eisenban

pushd eisenban

#####
# Do every time, to make sure everyone knows source of E.ico icon, so 
# proper license can be found
cp .\resources\icons\Barkerbaggies-Bag-O-Tiles-E.ico .\resources\icons\E.ico

pyinstaller --clean -y eisenbuild.windows11.onefile.spec
pyinstaller -y eisenbuild.windows11.onefile.spec

rm eisenbuild.windows11.onefile.spec

popd
popd

