# -*- mode: python ; coding: utf-8 -*-
#
# https://stackoverflow.com/questions/41870727/pyinstaller-adding-data-files
#

a = Analysis(
    ['eisenban.py'],
    pathex=['.', './ui', './ui/bkp', './resources/font', './resources/img', './resources/icons', './packenv/bin', './packenv/include', './packenv/lib/python3.13/site-packages'],
    binaries=[],
    datas=[("resources/font/*.ttf",   "./resources/font"), 
           ("resources/font/*.txt",   "./resources/font"), 
           ("resources/img/*.png",    "./resources/img"), 
           ("resources/icons/*.icns",  "./resources/icns")], 
    hiddenimports=['python3','python*','PySide6.*'],
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
    [],
    exclude_binaries=True,
    name='eisenban',
    debug=True,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='org.clockworksspheres.eisenban',
)
app = BUNDLE(
    coll,
    name='eisenban.app',
    icon='E.icns',
    bundle_identifier='org.clockworksspheres.eisenban',
)
