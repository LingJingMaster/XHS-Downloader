# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 获取项目根目录
project_root = Path(__file__).parent.absolute()

# 添加数据文件和资源文件
datas = [
    # 配置文件
    (str(project_root / 'settings.json'), '.'),
    
    # 静态资源文件
    (str(project_root / 'static' / 'XHS-Downloader.tcss'), 'static'),
    (str(project_root / 'static' / 'XHS-Downloader.icns'), 'static'),
    (str(project_root / 'static' / 'XHS-Downloader.ico'), 'static'),
    (str(project_root / 'static' / 'XHS-Downloader.png'), 'static'),
    (str(project_root / 'static' / 'XHS-Downloader.jpg'), 'static'),
    (str(project_root / 'static' / 'XHS-Downloader.js'), 'static'),
    (str(project_root / 'static' / 'Release_Notes.md'), 'static'),
    
    # 多语言文件
    (str(project_root / 'locale'), 'locale'),
]

# 隐藏导入 - 确保所有必要的模块都被包含
hiddenimports = [
    'source',
    'source.application',
    'source.CLI',
    'source.expansion',
    'source.module',
    'source.translation',
    'source.TUI',
    'aiofiles',
    'aiosqlite',
    'httpx',
    'httpx._client',
    'httpx._transports',
    'httpx._transports.default',
    'lxml',
    'lxml.etree',
    'lxml.html',
    'textual',
    'textual.app',
    'textual.widgets',
    'fastapi',
    'uvicorn',
    'click',
    'emoji',
    'pyperclip',
    'pyyaml',
    'rookiepy',
    'rookiepy.chrome',
    'rookiepy.edge',
    'rookiepy.firefox',
    'rookiepy.opera',
    'rookiepy.safari',
]

# 排除不需要的模块
excludes = [
    'tkinter',
    'unittest',
    'test',
    'pydoc_data',
    'xml',
    'xmlrpc',
]

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='XHS-Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'static' / 'XHS-Downloader.ico') if sys.platform == 'win32' else str(project_root / 'static' / 'XHS-Downloader.icns'),
)