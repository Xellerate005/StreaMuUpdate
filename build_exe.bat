@echo off
cd /d %~dp0
title StreaMu - Build EXE
echo ==============================================
echo  StreaMu - Build Windows executable
echo ==============================================
echo.

for %%F in (proxy.py opus_probe.py webm_opus_remux.py proxy.spec) do (
    if not exist %%F (
        echo [ERROR] Missing file: %%F
        echo Put it in the same folder as build_exe.bat and run again.
        goto :fail
    )
)

if not exist build-venv\Scripts\python.exe (
    echo [INFO] Creating clean build environment...
    python -m venv build-venv
    if errorlevel 1 goto :fail
)

echo [INFO] Installing build dependencies...
build-venv\Scripts\python.exe -m pip install --upgrade pip
build-venv\Scripts\python.exe -m pip install --upgrade pyinstaller starlette uvicorn yt-dlp certifi
if errorlevel 1 goto :fail

echo [INFO] Building...
build-venv\Scripts\python.exe -m PyInstaller --noconfirm --clean proxy.spec
if errorlevel 1 goto :fail

echo.
echo [OK] Done. Run: dist\StreaMu-Server\StreaMu-Server.exe
pause
exit /b 0

:fail
echo.
echo [FAILED] See the messages above.
pause
exit /b 1
