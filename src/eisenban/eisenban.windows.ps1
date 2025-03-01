# highly modified version of:
# https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/
# amoung others... including
# https://pyinstaller.org/en/stable/

# before script is run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# powershell -File ".\eisenban.windows.ps1"

#if doesn't exist...
# cd to the eisenban source root
 
# python3 -m venv packenv
# packenv/Scripts/Activate.ps1

# pip3 install PySide6 PyInstaller
# pip3 install --upgrade PyInstaller pyinstaller-hooks-contrib


# before script is run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# powershell -File ".\eisenban.windows.ps1"

cp .\resources\icons\Barkerbaggies-Bag-O-Tiles-E.ico .\resources\icons\E.ico

pyinstaller --clean -y eisenban.windows11.onefile.spec
pyinstaller -y eisenban.windows11.onefile.spec



