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
        # 大型の不要なサードパーティモジュールのみ除外
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        
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
    argv_emulation=True,  # macOSで重要
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['./webp-app.ico'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='webp-converter'
)

app = BUNDLE(
    coll,
    name='webp-converter.app',
    icon='./webp-app.ico',
    bundle_identifier='com.yourname.webpconverter',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'NSHighResolutionCapable': True,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Image files',
                'CFBundleTypeRole': 'Editor',
                'LSItemContentTypes': ['public.image'],
                'LSHandlerRank': 'Owner'
            }
        ]
    },
)
