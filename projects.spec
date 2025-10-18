# github_downloader.spec
# PyInstaller spec file for building the GitHub Downloader app

from PyInstaller.utils.hooks import collect_submodules
import os

# ---- SETTINGS ----
# Choose the main file to build
MAIN_FILE = "app_gui.py"   # or "github_downloader.py" for CLI

# Collect all hidden imports for customtkinter
hiddenimports = collect_submodules('customtkinter')

# Path to icon (optional)
ICON_PATH = os.path.join(os.getcwd(), "icon.ico")

a = Analysis(
    [MAIN_FILE],
    pathex=[],
    binaries=[],
    datas=[
        ("requirements.txt", "."),  # include requirements file
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
    name="GitHubDownloader",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # change to True for CLI version
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="GitHubDownloader",
)
