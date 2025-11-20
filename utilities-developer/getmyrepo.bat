@echo off
setlocal

:: Check if PYTHON_EXE is already set
if defined PYTHON_EXE goto PYTHON_OK

:: Try to find Python using 'py -3' first (Windows Python Launcher - preferred)
py -3 -c "exit()" >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py -3"
    goto PYTHON_OK
)

:: Fallback: try 'py' (launches latest Python 3 if available)
py -c "exit()" >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py"
    goto PYTHON_OK
)

:: Final fallback: try 'python'
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto PYTHON_OK
)

:: If we get here, no Python found
echo.
echo ERROR: Python interpreter not found!
echo.
echo Tried:
echo   - py -3
echo   - py
echo   - python
echo.
echo Please ensure Python is installed and available in PATH.
echo You can download it from https://www.python.org/downloads/
echo.
pause
exit /b 1

:PYTHON_OK
echo Using Python: %PYTHON_EXE%

:: Change to the directory where this batch script is located
cd /d "%~dp0"

:: Run the getmyrepo Python script with all passed arguments
%PYTHON_EXE% getmyrepo %*

:: Preserve error level from Python script
exit /b %errorlevel%