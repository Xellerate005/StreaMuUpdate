# -*- mode: python ; coding: utf-8 -*-
# Build with:  python -m PyInstaller --noconfirm --clean proxy.spec
from PyInstaller.utils.hooks import collect_all, collect_submodules

ONEFILE = False  # True = single .exe (slower start, more antivirus false positives)

datas, binaries, hiddenimports = [], [], []

# yt_dlp loads extractors dynamically; certifi ships cacert.pem as data.
for pkg in ("yt_dlp", "certifi"):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# uvicorn picks its loop/protocol/lifespan implementations by string name;
# anyio loads its backend the same way.
hiddenimports += collect_submodules("uvicorn")
hiddenimports += collect_submodules("anyio")
hiddenimports += ["opus_probe", "webm_opus_remux"]

# Dev tools and other things that should never be shipped.
excludes = ["mypy", "mypyc", "ruff", "pytest", "tkinter", "pip"]

a = Analysis(
    ["proxy.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
)
pyz = PYZ(a.pure)

if ONEFILE:
    exe = EXE(
        pyz, a.scripts, a.binaries, a.datas, [],
        name="StreaMu-Server",
        console=True,  # keep the console: it shows logs and the error prompt
        upx=False,
    )
else:
    exe = EXE(
        pyz, a.scripts, [],
        exclude_binaries=True,
        name="StreaMu-Server",
        console=True,
        upx=False,
    )
    coll = COLLECT(
        exe, a.binaries, a.datas,
        name="StreaMu-Server",
        upx=False,
    )
