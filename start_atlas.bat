@echo off
title OBSIDIAN ATLAS

cd /d "%~dp0"



:: First-time setup only
if not exist atlas_setup.done (

    if not exist venv (
        echo [1/4] Creating virtual environment...
        python -m venv venv
    )

    call venv\Scripts\activate

    echo.
    echo [2/4] Installing Python dependencies...
    pip install -r requirements.txt

    echo.
    echo [3/4] Installing Playwright Chromium...
    playwright install chromium

    echo.
    echo Setup Complete > atlas_setup.done

) else (

    call venv\Scripts\activate

)
echo.
echo [4/4] Launching OBSIDIAN ATLAS...
python launcher.py

pause