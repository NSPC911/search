@echo off
if "%1"=="" (
    echo Run 'search --help' for more info!
    exit /b 1
)
python "%~dp0search.py" %*