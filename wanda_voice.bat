@echo off
TITLE WANDA Voice Assistant
COLOR 0B
ECHO Starting WANDA Voice...
ECHO.

:: Check for WSL
IF EXIST "C:\Windows\System32\wsl.exe" (
    wsl -e bash -c "~/.wanda-system/bin/wanda voice"
) ELSE (
    ECHO WSL (Windows Subsystem for Linux) not found!
    ECHO Please install WSL to run WANDA.
    PAUSE
)
