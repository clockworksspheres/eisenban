# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["eisenban.py"],
    pathex=[
        ".",
        r".\ui",
        r".\ui\bkp",
        r".\resources\font",
        r".\resources\img",
        r".\resources\icons",
        r".\packenv\bin",
    ],
    binaries=[],
    datas=[
        ("resources/font/*.ttf", "./resources/font"),
        ("resources/font/*.txt", "./resources/font"),
        ("resources/img/*.png", "./resources/img"),
        ("resources/icons/*.ico", "./resources/icons"),
    ],
    hiddenimports=[],
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
    name="eisenban",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r".\resources\icons\E.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="eisenban",
)

