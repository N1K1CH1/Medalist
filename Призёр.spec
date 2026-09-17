# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PySide6 import __path__ as pyside_path

block_cipher = None

pyside_dir = pyside_path[0]
plugins_dir = os.path.join(pyside_dir, 'Qt', 'plugins')

qt_plugins = [
    (os.path.join(plugins_dir, 'platforms', 'qwindows.dll'), 'PySide6/Qt/plugins/platforms'),
    (os.path.join(plugins_dir, 'styles', 'qwindowsvistastyle.dll'), 'PySide6/Qt/plugins/styles'),
    (os.path.join(plugins_dir, 'imageformats', 'qjpeg.dll'), 'PySide6/Qt/plugins/imageformats'),
    (os.path.join(plugins_dir, 'imageformats', 'qgif.dll'), 'PySide6/Qt/plugins/imageformats'),
]

hidden_imports = [
    'PySide6',
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtNetwork',
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.styles',
    'json',
    'subprocess',
    'sys',
    'os'
]

a = Analysis(
    ['main.py', 'logic.py', 'gui.py'],
    pathex=[],
    binaries=[],
    datas=[('questions.json', '.'), ('Характеристика.txt', '.'), ('Описание.txt', '.'), ('start.png', '.'), ('icon.ico', '.')],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Призёр',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
