# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/shoheishimizu/Python/webp-converter/webp-converter.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    name='webp-converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/shoheishimizu/Python/webp-converter/webp-app.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='webp-converter',
)
app = BUNDLE(
    coll,
    name='webp-converter.app',
    icon='/Users/shoheishimizu/Python/webp-converter/webp-app.ico',
    bundle_identifier=None,
)
