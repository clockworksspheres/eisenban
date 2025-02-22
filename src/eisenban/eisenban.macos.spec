# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['eisenban.py'],
    pathex=['.', './ui', './ui/bkp', './resources/font', './resources/img', '/Users/victor/Documents/src/github/roynielsen17/Kanbaru/src/kanbaru/packenv/bin', '/Users/victor/Documents/src/github/roynielsen17/Kanbaru/src/kanbaru/packenv/include', '/Users/victor/Documents/src/github/roynielsen17/Kanbaru/src/kanbaru/packenv/lib'],
    binaries=[],
    datas=[("resources/font/NotoSans.ttf",   "Resources"), 
           ("resources/font/Arimo-Medium.ttf",   "Resources"), 
           ("resources/img/bg.png",          "Resources"), 
           ("resources/img/delete.png",      "Resources"), 
           ("resources/img/down-arrow.png",  "Resources"), 
           ("resources/img/icon.png",        "Resources"), 
           ("resources/img/kanbaru.png",     "Resources"), 
           ("resources/img/left-arrow.png",  "Resources"), 
           ("resources/img/logout.png",      "Resources"), 
           ("resources/img/right-arrow.png", "Resources"), 
           ("resources/img/settings.png",    "Resources"), 
           ("resources/img/settings_2.png",  "Resources"), 
           ("resources/img/up-arrow.png",    "Resources")],
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
    strip=False,
    upx=True,
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
    icon=None,
    bundle_identifier='org.clockworksspheres.eisenban',
)
