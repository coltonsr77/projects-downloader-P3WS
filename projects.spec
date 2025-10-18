# projects_downloader.spec
# PyInstaller build script for Projects Downloader (v0.1)
# Author: coltonsr77
# GitHub: https://github.com/coltonsr77/projects-downloader-P3WS

from PyInstaller.utils.hooks import collect_submodules
import os

# --- SETTINGS ---
APP_NAME = "ProjectsDownloader"
APP_VERSION = "0.1"
APP_AUTHOR = "coltonsr77"
APP_DESCRIPTION = "A desktop tool to download GitHub repositories or individual files easily."
MAIN_FILE = "app_gui.py"     # GUI entry point

# Hidden imports for customtkinter
hiddenimports = collect_submodules('customtkinter')

# --- ANALYSIS ---
a = Analysis(
    [MAIN_FILE],
    pathex=[],
    binaries=[],
    datas=[
        ("requirements.txt", "."),  # include requirements file
        ("github_downloader.py", "."),  # include the downloader logic
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # GUI app (set to True for CLI version)
    version=os.path.join(os.getcwd(), "version.txt") if os.path.exists("version.txt") else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)
