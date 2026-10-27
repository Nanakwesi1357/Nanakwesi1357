@echo off
setlocal
echo ============================================================
echo   Open WebUI - a beautiful browser interface for your AI
echo ============================================================
echo.
echo First run downloads extra components ^(a few hundred MB^).
echo Afterwards it opens at http://localhost:8080
echo Close this window to stop the server.
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo Python not found. Install from https://www.python.org/downloads/
    echo and tick "Add python.exe to PATH".
    pause
    exit /b 1
)

echo Installing/updating Open WebUI...
py -m pip install --user -U open-webui
if errorlevel 1 (
    echo Install failed. Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Starting server - your browser will be able to open http://localhost:8080
echo The first launch can take a minute; press Ctrl+C here to stop it.
echo.
py -m open_webui serve
pause
