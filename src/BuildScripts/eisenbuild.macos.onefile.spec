# -*- mode: python ; coding: utf-8 -*-
#
# https://stackoverflow.com/questions/41870727/pyinstaller-adding-data-files
#

a = Analysis(
    ['eisenban.py'],
    pathex=['.', './ui', './ui/bkp', './resources/font', './resources/img', './resources/icons'],
    binaries=[],
    datas=[("resources/font/*.ttf",   "./resources/font"), 
           ("resources/font/*.txt",   "./resources/font"), 
           ("resources/img/*.png",    "./resources/img"), 
           ("resources/icons/*.icns",  "./resources/icns")], 
    hiddenimports=[ ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='eisenban',
    debug=True,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon='E.icns',
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onfile=True,
)
