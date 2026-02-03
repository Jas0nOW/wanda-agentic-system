@echo off
REM WANDA Agentic System - Windows Installer
REM https://github.com/jas0nOW/wanda-agentic-system

echo.
echo ========================================
echo   WANDA Agentic System - Windows Setup
echo ========================================
echo.

REM Check prerequisites
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found. Install from https://python.org
    pause
    exit /b 1
)

where git >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git not found. Install from https://git-scm.com
    pause
    exit /b 1
)

echo [OK] Prerequisites met

REM Set install directory
set INSTALL_DIR=%USERPROFILE%\.wanda-system

REM Clone or update
if exist "%INSTALL_DIR%\.git" (
    echo Updating existing installation...
    cd /d "%INSTALL_DIR%"
    git pull
) else (
    echo Cloning repository...
    git clone https://github.com/jas0nOW/wanda-agentic-system "%INSTALL_DIR%"
    cd /d "%INSTALL_DIR%"
)

echo.
echo What would you like to install?
echo   1) Agent System only
echo   2) Voice Assistant only  
echo   3) Everything (recommended)
echo.
set /p CHOICE="Choice [3]: "
if "%CHOICE%"=="" set CHOICE=3

if "%CHOICE%"=="1" goto agents
if "%CHOICE%"=="2" goto voice
goto both

:agents
call :install_agents
goto done

:voice
call :install_voice
goto done

:both
call :install_agents
call :install_voice
goto done

:install_agents
echo.
echo Installing Agent System...

REM Create directories
if not exist "%APPDATA%\opencode\profiles\stable" mkdir "%APPDATA%\opencode\profiles\stable"
if not exist "%APPDATA%\opencode\profiles\experimental" mkdir "%APPDATA%\opencode\profiles\experimental"

REM Copy profiles
copy /Y "%INSTALL_DIR%\wanda-agents\profiles\opencode.jsonc" "%APPDATA%\opencode\profiles\"
copy /Y "%INSTALL_DIR%\wanda-agents\profiles\stable\opencode.json" "%APPDATA%\opencode\profiles\stable\"
copy /Y "%INSTALL_DIR%\wanda-agents\profiles\experimental\opencode.json" "%APPDATA%\opencode\profiles\experimental\"

REM Copy GEMINI.md
if not exist "%USERPROFILE%\.gemini" mkdir "%USERPROFILE%\.gemini"
copy /Y "%INSTALL_DIR%\wanda-agents\GEMINI.md" "%USERPROFILE%\.gemini\"

echo [OK] Agent System installed
echo.
echo Next: Add Antigravity account to %APPDATA%\opencode\antigravity-accounts.json
goto :eof

:install_voice
echo.
echo Installing Voice Assistant...
cd /d "%INSTALL_DIR%\wanda-voice"

REM Create venv
if not exist "venv" python -m venv venv

REM Activate and install
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo [OK] Voice Assistant installed
echo.
echo Run: python %INSTALL_DIR%\wanda-voice\main.py
goto :eof

:done
echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Installed to: %INSTALL_DIR%
echo.
echo Quick Start:
echo   Agent System: opencode --profile experimental
echo   Voice: python %INSTALL_DIR%\wanda-voice\main.py
echo.
echo Update: cd %INSTALL_DIR% ^&^& git pull
echo.
pause
