@echo off
setlocal
echo ============================================================
echo   Local AI - setup for Windows
echo ============================================================
echo.

echo [1/4] Checking for Ollama...
where ollama >nul 2>nul
if errorlevel 1 (
    echo.
    echo   Ollama is not installed yet ^(or not on your PATH^).
    echo   1. Download it here: https://ollama.com/download
    echo   2. Run the installer, accept the defaults.
    echo   3. Close this window, open a NEW one, and run setup.bat again.
    echo.
    pause
    exit /b 1
)
ollama --version
echo.

echo [2/4] Checking for Python...
where py >nul 2>nul
if errorlevel 1 (
    echo   Python not found. The chat app needs it:
    echo   1. Download from https://www.python.org/downloads/
    echo   2. IMPORTANT: tick "Add python.exe to PATH" during install.
    echo   3. Re-run this script.
    echo.
    pause
    exit /b 1
)
py --version
echo.

echo [3/4] Downloading the starter model qwen2.5:3b ^(about 2 GB, one time^)...
echo       This is the fast model tuned for 12 GB machines. It resumes if
echo       the connection drops - just run setup.bat again.
ollama pull qwen2.5:3b
if errorlevel 1 (
    echo.
    echo   The download failed. Check your connection and run setup.bat again
    echo   - Ollama resumes partial downloads.
    pause
    exit /b 1
)
echo.

echo [4/4] Quick smoke test...
ollama list
echo.
echo ============================================================
echo   Done. Your local AI is ready.
echo.
echo   Start chatting:     scripts\chat.bat
echo   Or directly:        ollama run qwen2.5:3b
echo.
echo   Want the stronger 4.7 GB model when you have bandwidth:
echo       ollama pull qwen2.5:7b
echo       scripts\chat.bat --model qwen2.5:7b
echo ============================================================
pause
