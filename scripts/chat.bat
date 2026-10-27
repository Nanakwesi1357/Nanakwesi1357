@echo off
REM Launch the zero-dependency chat client. Any extra arguments are passed
REM straight through, e.g.  chat.bat --model qwen2.5:7b
py "%~dp0..\app\chat.py" %*
if errorlevel 1 (
    echo.
    echo If Python was not found, install it from https://www.python.org/downloads/
    echo and tick "Add python.exe to PATH" during installation.
    pause
)
