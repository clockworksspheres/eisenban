# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/
# amoung others... including
# https://pyinstaller.org/en/stable/

# before script is run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
# powershell -File ".\eisenbuild.windows.ps1"

pushd ..

$directory = ".\projEnv"
$actfile = "$directory\Scripts\Activate.ps1"
if (!(Test-Path -Path $directory -PathType Container)) {
   #if (!(Test-Path -Path ".\packenv" -PathType Container)) {
   
   python -m venv $directory

   .\projenv\Scripts\Activate.ps1

   pip install -r requirements.txt
} else {
   powershell -File $actfile
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

