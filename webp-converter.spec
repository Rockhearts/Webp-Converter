# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['./webp-converter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 完全に不要なモジュール
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL._tkinter_finder',
        'distutils',
        'email',
        'http',
        'urllib',
        'xml',
        'json',
        'html',
        'encodings.idna',
        'encodings.punycode',
        'doctest',
        'pydoc',
        'unittest',
        'test',
        
        # PyQt5の不要なモジュール（より厳密に）
        'PyQt5.QtWebEngine',
        'PyQt5.QtWebEngineCore', 
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtQuick',
        'PyQt5.QtQml',
        'PyQt5.QtQmlModels',
        'PyQt5.QtNetwork',
        'PyQt5.QtSql',
        'PyQt5.QtTest',
        'PyQt5.QtXml',
        'PyQt5.QtXmlPatterns',
        'PyQt5.QtDBus',
        'PyQt5.QtSvg',
        'PyQt5.QtPrintSupport',
        'PyQt5.QtHelp',
        'PyQt5.QtDesigner',
        'PyQt5.QtWebSockets',
        'PyQt5.QtPositioning',
        'PyQt5.QtLocation',
        'PyQt5.QtSensors',
        'PyQt5.QtSerialPort',
        'PyQt5.QtBluetooth',
        'PyQt5.QtNfc',
        'PyQt5.QtMultimedia',
        'PyQt5.QtMultimediaWidgets',
        'PyQt5.QtOpenGL',
        'PyQt5.QtQuickWidgets'
    ],
    noarchive=False,  # アーカイブ有効化
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# onefile形式を試す
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # onefileの場合はここに含める
    a.datas,     # onefileの場合はここに含める
    [],
    name='webp-converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=['vcruntime140.dll'],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['./webp-app.ico'],
)

app = BUNDLE(
    exe,
    name='webp-converter.app',
    icon='./webp-app.ico',
    bundle_identifier=None,
)
