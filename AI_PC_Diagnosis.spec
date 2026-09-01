# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.utils.hooks import collect_submodules


# ============================================================
# Hidden Imports
# ============================================================

hiddenimports = []

hiddenimports += collect_submodules("gui")
hiddenimports += collect_submodules("diagnosis")


# ============================================================
# Analysis
# ============================================================

a = Analysis(
    ["gui/gui_main.py"],

    pathex=[
        ".",
    ],

    binaries=[],

    datas=[],

    hiddenimports=hiddenimports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,

    optimize=0,
)


# ============================================================
# Pythonコード
# ============================================================

pyz = PYZ(
    a.pure
)


# ============================================================
# EXE
# ============================================================

exe = EXE(
    pyz,

    a.scripts,

    [],

    exclude_binaries=True,

    name="AI_PC_Diagnosis",

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
)


# ============================================================
# Collect
# ============================================================

coll = COLLECT(
    exe,

    a.binaries,

    a.datas,

    strip=False,

    upx=True,

    upx_exclude=[],

    name="AI_PC_Diagnosis",
)